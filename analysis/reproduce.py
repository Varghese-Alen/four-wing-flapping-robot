#!/usr/bin/env python3
"""Read retained computational results; evaluate prescribed geometry, not dynamics."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
METHODS = ("no spring", "best fixed", "selectable optimized")
LABELS = ("No spring", "Best fixed", "Optimised menu")
COLOURS = ("#526F83", "#AB7B46", "#48252F")


def rows(name):
    with (DATA / name).open(newline="") as stream:
        return list(csv.DictReader(stream))


def document(name):
    return json.loads((DATA / name).read_text())


def integrate(values, phase):
    """Trapezoidal integral over dimensionless cycle phase."""
    return float(np.sum((values[1:] + values[:-1]) * np.diff(phase) * 0.5))


def prescribed_kinematics(phase, frequency=20.0):
    """Exact selected four-bar closure and analytic derivatives at constant speed.

    This is a geometric evaluation, not a time integration or dynamic solution.
    Front/rear angles are opposite signed departures from the mean rocker angle.
    """
    c = document("inputs/model-constants.json")
    phase = np.asarray(phase, dtype=float)
    theta = c["phase_rad"] + 2 * np.pi * phase
    crank, ground = c["crank_m"], c["ground_m"]
    coupler, rocker = c["coupler_m"], c["rocker_m"]
    crank_tip = np.stack((-ground + crank * np.cos(theta), crank * np.sin(theta)), axis=-1)
    distance = np.linalg.norm(crank_tip, axis=-1)
    along = (rocker**2 - coupler**2 + distance**2) / (2 * distance)
    height = np.sqrt(rocker**2 - along**2)
    perpendicular = lambda v: np.stack((-v[..., 1], v[..., 0]), axis=-1)
    rocker_tip = (along[..., None] * crank_tip + height[..., None] * perpendicular(crank_tip)) / distance[..., None]
    beta = np.arctan2(rocker_tip[..., 1], rocker_tip[..., 0])
    crank_vector = crank_tip + np.array([ground, 0.0])
    first = perpendicular(crank_vector)
    second = -crank_vector
    link = crank_tip - rocker_tip
    tangent = perpendicular(rocker_tip)
    dot = lambda a, b: np.sum(a * b, axis=-1)
    denominator = dot(link, tangent)
    jacobian = dot(link, first) / denominator
    curvature = (dot(first, first) - 2 * dot(first, tangent) * jacobian
                 + (rocker**2 + dot(link, rocker_tip)) * jacobian**2
                 + dot(link, second)) / denominator
    angle = beta - c["mean_beta_rad"]
    speed = 2 * np.pi * frequency
    return {"phase": phase, "time_s": phase / frequency,
            "crank_angle_rad": theta, "front_angle_rad": angle,
            "rear_angle_rad": -angle, "front_rate_rad_s": jacobian * speed,
            "front_accel_rad_s2": curvature * speed**2}


def stiffness_grid():
    table = rows("results/stiffness-frequency-grid.csv")
    frequencies = sorted({float(r["frequency_Hz"]) for r in table})
    multipliers = sorted({float(r["multiplier"]) for r in table})
    lookup = {(float(r["frequency_Hz"]), float(r["multiplier"])): float(r["Ppositive_W"]) for r in table}
    savings = np.array([[100 * (1 - lookup[f, m] / lookup[f, 0])
                         for f in frequencies] for m in multipliers], dtype="<f8")
    return np.array(frequencies), np.array(multipliers), savings


def readout():
    table = rows("results/comparison.csv")
    config = document("inputs/experiment-config.json")
    mission = config["mission_Hz"]
    weights = config["mission_weights"]
    methods = METHODS + ("selectable prescribed",)
    lookup = {(float(r["frequency_Hz"]), r["method"]): r for r in table}
    means = {m: sum(w * float(lookup[f, m]["Ppositive_W"]) for f, w in zip(mission, weights)) for m in methods}
    torque = {m: 1000 * float(lookup[20, m]["peak_motor_Nm"]) for m in METHODS}
    conditional = rows("results/conditional-samples.csv")
    advantages = np.array([float(r["best_fixed_W"]) - float(r["selectable_optimized_W"]) for r in conditional])
    _, _, savings = stiffness_grid()
    constants = document("inputs/model-constants.json")
    pair_stiffness = 2 * constants["spring_torque_Nm"][-1] / constants["spring_angle_rad"][-1]
    inertia = constants["groups"]["R"]["root"]
    storage = {"dry_Hz": float(np.sqrt(pair_stiffness / inertia) / (2 * np.pi)),
               "added_inertia_hypothesis_Hz": float(np.sqrt(pair_stiffness / (inertia + constants["added_air_pair_kgm2"])) / (2 * np.pi)),
               "target_Hz": [16, 18], "selected_drive_Hz": 20}
    histories = {}
    for method in METHODS:
        with np.load(DATA / "results" / ("history-f20-" + method.replace(" ", "_") + ".npz"), allow_pickle=False) as h:
            phase = h["phase"]
            power = h["total_power_W"]
            positive = integrate(np.maximum(power, 0), phase)
            negative = integrate(np.maximum(-power, 0), phase)
            signed = integrate(power, phase)
            kin = prescribed_kinematics(phase)
            components = sum(h[k] for k in ("inertia_power_W", "aero_power_W", "spring_power_W", "springloss_power_W"))
            histories[method] = {"samples": len(phase), "positive_W": positive,
                                 "negative_W": negative, "signed_W": signed,
                                 "peak_mNm": float(1000 * max(np.max(np.abs(h["torque_R_Nm"])), np.max(np.abs(h["torque_L_Nm"])))),
                                 "power_identity_error_W": abs(positive - negative - signed),
                                 "component_max_error_W": float(np.max(np.abs(power - components))),
                                 "angle_max_error_rad": float(np.max(np.abs(kin["front_angle_rad"] - h["root_angle_rad"]))),
                                 "rate_max_error_rad_s": float(np.max(np.abs(kin["front_rate_rad_s"] - h["root_rate_rad_s"]))),
                                 "acceleration_max_error_rad_s2": float(np.max(np.abs(kin["front_accel_rad_s2"] - h["root_accel_rad_s2"])))}
    advantage = means["best fixed"] - means["selectable optimized"]
    refinement = document("results/fixed-grid-audit.json")["fixed_refinement"][-1]
    return {"scope": "Readout of retained computational screening; no new dynamics runs",
            "mission_Hz": mission, "mission_positive_mechanical_W": means,
            "optimised_menu_advantage_mW": 1000 * advantage,
            "optimised_menu_advantage_percent": 100 * advantage / means["best fixed"],
            "initial_menu_penalty_mW": 1000 * (means["selectable prescribed"] - means["best fixed"]),
            "torque_20Hz_mNm": torque,
            "conditional": {"cases": len(conditional), "negative_advantages": int(np.count_nonzero(advantages < 0))},
            "stiffness_grid": {"cases": int(savings.size), "shape": list(savings.shape),
                               "negative_savings": int(np.count_nonzero(savings < 0)),
                               "minimum_percent": float(savings.min()), "maximum_percent": float(savings.max()),
                               "values_sha256_float64_le_C_order": hashlib.sha256(savings.tobytes()).hexdigest()},
            "storage_frequency": storage, "retained_fixed_refinement": refinement,
            "histories_20Hz": histories}


def svg_start(title, subtitle, height=430):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 {height}" role="img">',
            f'<title>{escape(title)}</title><desc>{escape(subtitle)}</desc>',
            f'<rect width="920" height="{height}" fill="#FAF7F0"/>',
            '<g font-family="sans-serif" fill="#30252B">',
            f'<text x="36" y="38" font-size="23">{escape(title)}</text>',
            f'<text x="36" y="65" font-size="13">{escape(subtitle)}</text>']


def svg_finish(parts):
    return "\n".join(parts + ["</g></svg>"]) + "\n"


def blend(value):
    neutral = (239, 228, 209)
    end = (82, 111, 131) if value < 0 else (72, 37, 47)
    fraction = min(abs(float(value)) / 60, 1)
    return "#" + "".join(f"{round(a + fraction * (b - a)):02x}" for a, b in zip(neutral, end))


def figures(summary):
    outputs = {}
    parts = svg_start("Positive mechanical input power", "Equal-weight mean at 17, 18.5 and 20 Hz; both drives; computational screening")
    for index, (method, label, colour) in enumerate(zip(METHODS, LABELS, COLOURS)):
        value = summary["mission_positive_mechanical_W"][method]
        y = 115 + index * 77
        parts += [f'<text x="36" y="{y + 28}" font-size="17">{label}</text>',
                  f'<rect x="230" y="{y}" width="{value / 2.5 * 540:.4f}" height="43" fill="{colour}"/>',
                  f'<text x="{240 + value / 2.5 * 540:.4f}" y="{y + 28}" font-size="17">{value:.6f} W</text>']
    parts += [f'<text x="36" y="366" font-size="14">Optimised menu: {summary["optimised_menu_advantage_mW"]:.3f} mW below the grid-best fixed spring.</text>',
              f'<text x="36" y="394" font-size="14">Initial menu: {summary["initial_menu_penalty_mW"]:.3f} mW worse. These are not electrical savings.</text>']
    outputs["power-summary.svg"] = svg_finish(parts)
    parts = svg_start("Ideal input-shaft torque at 20 Hz", "Right drive, full retained cycle; output torque divided by ideal ratio 20; not measured motor torque")
    for tick in (-3, -1.5, 0, 1.5, 3):
        y = 245 - tick * 43
        parts += [f'<path d="M80,{y} H870" stroke="#DDD3C5"/>',
                  f'<text x="32" y="{y + 5}" font-size="12">{tick:g}</text>']
    for method, label, colour in zip(METHODS, LABELS, COLOURS):
        with np.load(DATA / "results" / ("history-f20-" + method.replace(" ", "_") + ".npz"), allow_pickle=False) as h:
            points = " ".join(f"{80 + p * 790:.3f},{245 - t * 1000 * 43:.3f}" for p, t in zip(h["phase"], h["torque_R_Nm"]))
        parts.append(f'<polyline points="{points}" fill="none" stroke="{colour}" stroke-width="1.8"/>')
        i = METHODS.index(method)
        parts.append(f'<text x="{80 + i * 260}" y="91" fill="{colour}" font-size="13">{label}: {summary["torque_20Hz_mNm"][method]:.6f} mNm</text>')
    parts += ['<text x="36" y="110" font-size="12">mNm</text>']
    for phase in (0, .25, .5, .75, 1):
        parts.append(f'<text x="{80 + phase * 790 - 8}" y="391" font-size="12">{phase:g}</text>')
    parts.append('<text x="390" y="416" font-size="13">Cycle phase</text>')
    outputs["torque-cycle.svg"] = svg_finish(parts)
    frequencies, multipliers, savings = stiffness_grid()
    grid_summary = summary["stiffness_grid"]
    parts = svg_start("Stiffness-frequency screening grid", f'{grid_summary["cases"]:,} retained cases; {grid_summary["negative_savings"]} negative savings; no interpolation or new evaluation', 520)
    xedges = np.r_[11.5, (frequencies[:-1] + frequencies[1:]) / 2, 24.5]
    yedges = np.r_[0, (multipliers[:-1] + multipliers[1:]) / 2, 3]
    x = lambda f: 100 + (f - 11.5) / 13 * 650
    y = lambda m: 395 - m / 3 * 285
    for i, _ in enumerate(multipliers):
        for j, _ in enumerate(frequencies):
            parts.append(f'<rect x="{x(xedges[j]):.4f}" y="{y(yedges[i+1]):.4f}" width="{x(xedges[j+1])-x(xedges[j]):.4f}" height="{y(yedges[i])-y(yedges[i+1]):.4f}" fill="{blend(savings[i,j])}"/>')
    for f in (12, 15, 18, 20, 24):
        parts.append(f'<text x="{x(f)-7:.2f}" y="416" font-size="12">{f}</text>')
    for m in (0, 1, 2, 3):
        parts.append(f'<text x="73" y="{y(m)+4:.2f}" font-size="12">{m}</text>')
    parts += ['<text x="335" y="443" font-size="14">Frequency [Hz]</text>',
              '<text transform="translate(35,350) rotate(-90)" font-size="14">Stiffness multiplier</text>']
    for i in range(120):
        value = 60 - i
        parts.append(f'<rect x="787" y="{110+i*2.375:.3f}" width="24" height="2.4" fill="{blend(value)}"/>')
    for val in (-60, 0, 60):
        parts.append(f'<text x="821" y="{110+(60-val)/120*285+4:.2f}" font-size="12">{val}%</text>')
    parts += ['<text x="770" y="95" font-size="12">Saving</text>',
              '<text x="36" y="478" font-size="13">100 × (1 − positive mechanical power / no-spring power at the same frequency).</text>',
              '<text x="36" y="501" font-size="13">Negative values are worse; the colour scale is fixed at −60% to +60%.</text>']
    outputs["stiffness-grid.svg"] = svg_finish(parts)
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "reproduced")
    parser.add_argument("--samples", type=int, default=257, help="Prescribed-motion samples including both endpoints")
    args = parser.parse_args()
    if args.samples < 3:
        parser.error("--samples must be at least 3")
    summary = readout()
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    for name, content in figures(summary).items():
        (args.output / name).write_text(content)
    motion = prescribed_kinematics(np.linspace(0, 1, args.samples))
    with (args.output / "prescribed-kinematics.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(motion)
        writer.writerows(zip(*motion.values()))
    print(json.dumps(summary, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
