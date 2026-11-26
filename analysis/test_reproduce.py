"""Regression tests for readout and prescribed geometry; no dynamics solver."""
import unittest
import xml.etree.ElementTree as ET

import numpy as np
import reproduce as r


class RetainedEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summary = r.readout()

    def test_sealed_mission_power(self):
        expected = (2.144117426002209, 1.8017642926779402, 1.7981761969290264)
        original = r.document("results/summary.json")["mission_nominal_Ppositive_W"]
        for method, value in zip(r.METHODS, expected):
            self.assertAlmostEqual(self.summary["mission_positive_mechanical_W"][method], value, places=12)
            self.assertAlmostEqual(original[method], value, places=12)

    def test_initial_menu_is_worse(self):
        self.assertAlmostEqual(self.summary["initial_menu_penalty_mW"], 10.848150059460604, places=10)
        self.assertAlmostEqual(self.summary["optimised_menu_advantage_mW"], 3.588095748913833, places=10)
        self.assertAlmostEqual(self.summary["optimised_menu_advantage_percent"], 0.19914345974638506, places=11)

    def test_fixed_objective_and_refinement(self):
        best = min(r.rows("results/fixed-objective.csv"), key=lambda row: float(row["mission_Ppositive_W"]))
        self.assertEqual(float(best["multiplier"]), 1.625)
        self.assertAlmostEqual(float(best["mission_Ppositive_W"]), 1.8017642926779402, places=12)
        refined = self.summary["retained_fixed_refinement"]
        self.assertAlmostEqual(refined["frozen_menu_advantage_W"], 0.0035869584841936586, places=14)
        self.assertAlmostEqual(refined["frozen_menu_advantage_percent"], 0.19908046589902756, places=12)

    def test_conditional_cases_keep_negative_outcomes(self):
        self.assertEqual(self.summary["conditional"], {"cases": 1000, "negative_advantages": 9})
        for row in r.rows("results/conditional-samples.csv"):
            advantage = float(row["best_fixed_W"]) - float(row["selectable_optimized_W"])
            self.assertAlmostEqual(advantage, float(row["modular_advantage_W"]), places=14)

    def test_complete_stiffness_grid_and_sealed_array(self):
        grid = self.summary["stiffness_grid"]
        self.assertEqual(grid["shape"], [121, 14])
        self.assertEqual(grid["cases"], 1694)
        self.assertEqual(grid["negative_savings"], 137)
        self.assertEqual(grid["values_sha256_float64_le_C_order"], "fc8ad6a1589ef62882287f25dbd3abb460a0699fc48eb29c5b2f57d8245a9831")
        self.assertAlmostEqual(grid["minimum_percent"], -55.84222669192194, places=11)
        self.assertAlmostEqual(grid["maximum_percent"], 16.134738316975337, places=11)

    def test_torque_from_tables_and_histories(self):
        expected = (2.3245311158525084, 1.677929889047573, 1.571341065517272)
        for method, value in zip(r.METHODS, expected):
            self.assertAlmostEqual(self.summary["torque_20Hz_mNm"][method], value, places=12)
            self.assertAlmostEqual(self.summary["histories_20Hz"][method]["peak_mNm"], value, places=12)

    def test_history_integrals_and_components(self):
        table = {row["method"]: row for row in r.rows("results/comparison.csv") if float(row["frequency_Hz"]) == 20}
        for method, h in self.summary["histories_20Hz"].items():
            self.assertEqual(h["samples"], 4097)
            self.assertAlmostEqual(h["positive_W"], float(table[method]["Ppositive_W"]), places=10)
            self.assertAlmostEqual(h["negative_W"], float(table[method]["Pnegative_W"]), places=10)
            self.assertAlmostEqual(h["signed_W"], float(table[method]["Psigned_W"]), places=10)
            self.assertLess(h["power_identity_error_W"], 1e-11)
            self.assertLess(h["component_max_error_W"], 1e-11)

    def test_exact_geometry_matches_retained_motion(self):
        for h in self.summary["histories_20Hz"].values():
            self.assertLess(h["angle_max_error_rad"], 1e-12)
            self.assertLess(h["rate_max_error_rad_s"], 1e-10)
            self.assertLess(h["acceleration_max_error_rad_s2"], 1e-8)
        motion = r.prescribed_kinematics(np.linspace(0, 1, 4097))
        np.testing.assert_allclose(motion["rear_angle_rad"], -motion["front_angle_rad"], atol=0)
        self.assertAlmostEqual(np.ptp(motion["front_angle_rad"]) * 180 / np.pi, 48, places=5)
        for key in ("front_angle_rad", "front_rate_rad_s", "front_accel_rad_s2"):
            self.assertAlmostEqual(float(motion[key][0]), float(motion[key][-1]), places=8)

    def test_storage_conflict(self):
        stored = self.summary["storage_frequency"]
        original = r.document("results/kinematics.json")
        self.assertAlmostEqual(stored["dry_Hz"], 23.77789448590115, places=11)
        self.assertAlmostEqual(stored["added_inertia_hypothesis_Hz"], 14.325359571012624, places=11)
        self.assertAlmostEqual(stored["dry_Hz"], original["storage_fn_dry_Hz"], places=12)
        self.assertEqual(stored["target_Hz"], [16, 18])
        self.assertEqual(stored["selected_drive_Hz"], 20)

    def test_spring_constants_match_input_table(self):
        constants = r.document("inputs/model-constants.json")
        selected = sorted((row for row in r.rows("inputs/formed_states.csv") if row["case"] == "formed_fine_pos"), key=lambda row: float(row["angle_deg"]))
        np.testing.assert_allclose(constants["spring_angle_rad"][1:], [np.deg2rad(float(row["angle_deg"])) for row in selected], rtol=0, atol=1e-15)
        np.testing.assert_allclose(constants["spring_torque_Nm"][1:], [float(row["bottom_torque_Nm"]) for row in selected], rtol=0, atol=0)

    def test_retained_quadrature_checks(self):
        checks = r.rows("results/quadrature-checks.csv")
        self.assertEqual(len(checks), 15)
        self.assertTrue(all(row["passed"] == "True" for row in checks))

    def test_svg_figures_are_well_formed_and_complete(self):
        figures = r.figures(self.summary)
        self.assertEqual(len(figures), 3)
        for text in figures.values():
            ET.fromstring(text)
            self.assertNotIn("nan", text.lower())
        torque = ET.fromstring(figures["torque-cycle.svg"])
        lines = torque.findall(".//{http://www.w3.org/2000/svg}polyline")
        self.assertEqual(len(lines), 3)
        self.assertTrue(all(len(line.attrib["points"].split()) == 4097 for line in lines))


if __name__ == "__main__":
    unittest.main(verbosity=2)
