#!/usr/bin/env python3
"""Display retained numerical tables; no model integration or parameter search.
Copyright (c) 2026 Alen Mammen Varghese. SPDX-License-Identifier: MIT
Run: python3 tools/make_website_plots.py (NumPy, Matplotlib and Pillow required).
"""
from pathlib import Path
import csv, json, math, io, hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import ListedColormap
from PIL import Image
R=Path(__file__).resolve().parents[1]; OUT=R/'media'; OUT.mkdir(exist_ok=True)
font_manager.fontManager.addfont(str(OUT/'fonts/Lato-Regular.ttf'))
assert Path(font_manager.findfont('Lato',fallback_to_default=False)).name=='Lato-Regular.ttf'
DATA=R/'analysis/data'; BG='#F2EADC'; INK='#101211'; PLUM='#48252F'; GOLD='#857861'; GREEN='#2F4A3A'
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Lato','DejaVu Sans'],'font.size':24,'text.color':INK,'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK,'svg.fonttype':'path','axes.unicode_minus':True})
def lab(rgb):
 c=np.asarray(rgb); c=np.where(c<=.04045,c/12.92,((c+.055)/1.055)**2.4)
 xyz=np.array([[.4124564,.3575761,.1804375],[.2126729,.7151522,.0721750],[.0193339,.1191920,.9503041]])@c/np.array([.95047,1,1.08883]);f=np.where(xyz>(6/29)**3,np.cbrt(xyz),xyz/(3*(6/29)**2)+4/29)
 return np.array([116*f[1]-16,500*(f[0]-f[1]),200*(f[1]-f[2])])
def rgb(l):
 fy=(l[0]+16)/116;f=np.array([fy+l[1]/500,fy,fy-l[2]/200]);xyz=np.where(f>6/29,f**3,3*(6/29)**2*(f-4/29))*np.array([.95047,1,1.08883]);c=np.linalg.inv(np.array([[.4124564,.3575761,.1804375],[.2126729,.7151522,.0721750],[.0193339,.1191920,.9503041]]))@xyz
 return np.clip(np.where(c<=.0031308,12.92*c,1.055*np.maximum(c,0)**(1/2.4)-.055),0,1)
neutral=lab(np.array([239,228,209])/255);positive=lab(np.array([72,37,47])/255);negative=np.array([positive[0],-4,-13])
# Matched lightness on the two arms; this is not a certified uniform colour map.
colours=[rgb(neutral*(1-abs(t))+(negative if t<0 else positive)*abs(t))for t in np.linspace(-1,1,257)]
palette=ListedColormap(colours)
def finish(fig,name,title,description):
 name=name+'-'+theme
 svg=OUT/(name+'.svg');fig.savefig(svg,facecolor=BG,metadata={'Title':title,'Description':description,'Creator':'Portfolio display script','Date':None})
 text=svg.read_text();start=text.index('<svg ');end=text.index('>',start);text=text[:end]+ ' role="img" aria-label="'+title+'"'+text[end:];svg.write_text(text)
 buf=io.BytesIO();fig.savefig(buf,format='png',dpi=100,facecolor=BG);buf.seek(0);im=Image.open(buf).convert('RGB');im.save(OUT/(name+'-1600.webp'),lossless=True,method=4);im.resize((800,round(im.height/2)),Image.Resampling.LANCZOS).save(OUT/(name+'-800.webp'),lossless=True,method=4);plt.close(fig)
summary=json.loads((DATA/'results/summary.json').read_text());rows=list(csv.DictReader((DATA/'results/comparison.csv').open()))
# Values come directly from retained rows, equally weighted over the three frequencies.
record=summary['mission_nominal_Ppositive_W']
values=[record[k] for k in ['no spring','best fixed','selectable optimized']]
assert np.allclose(values,[2.144117426002209,1.8017642926779402,1.7981761969290264],rtol=0,atol=1e-12)
# The independent readout tests also compare these means with comparison.csv.
grid=list(csv.DictReader((DATA/'results/stiffness-frequency-grid.csv').open()));freq=np.array(sorted({float(r['frequency_Hz'])for r in grid}));multipliers=np.array(sorted({float(r['multiplier'])for r in grid}));p=np.zeros((len(multipliers),len(freq)))
for row in grid:p[np.where(multipliers==float(row['multiplier']))[0][0],np.where(freq==float(row['frequency_Hz']))[0][0]]=float(row['Ppositive_W'])
z=100*(1-p/p[0]);assert z.shape==(121,14) and (z<0).sum()==137
kin=json.loads((DATA/'results/kinematics.json').read_text());const=json.loads((DATA/'inputs/model-constants.json').read_text());kp=2*const['spring_torque_Nm'][-1]/const['spring_angle_rad'][-1]
assert hashlib.sha256(z.astype('<f8').tobytes()).hexdigest()=='fc8ad6a1589ef62882287f25dbd3abb460a0699fc48eb29c5b2f57d8245a9831'
for theme,BG,INK,GRID in [('light','#F2EADC','#101211','#D5C6B0'),('dark','#101211','#F2EADC','#595A53')]:
 plt.rcParams.update({'text.color':INK,'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK,'axes.edgecolor':INK})
 fig=plt.figure(figsize=(16,9),dpi=100,facecolor=BG);ax=fig.add_axes([.25,.21,.63,.70]);ax.set_facecolor(BG)
 ax.barh([2,1,0],values,height=.46,color=[GOLD,GREEN,PLUM]);ax.set_yticks([2,1,0],['No spring','Fixed spring','Three settings']);ax.tick_params(axis='y',length=0,pad=20)
 ax.set_xlim(0,2.5);ax.set_xticks([0,.5,1,1.5,2,2.5]);ax.set_xlabel('Calculated mechanical input power (W)',labelpad=20)
 ax.grid(axis='x',color=GRID,lw=1);ax.set_axisbelow(True)
 for spine in ax.spines.values():spine.set_visible(False)
 for y,val in zip([2,1,0],values):ax.text(val+.045,y,f'{val:.3f}',va='center',fontsize=25,color=INK)
 finish(fig,'result-bars','Calculated mechanical input power','Equal weighted mean positive mechanical power for both drives at 17, 18.5 and 20 Hz. No spring 2.144117426 W; fixed 1.801764293 W; three settings 1.798176197 W. The menu adds 0.19914346 percent versus fixed. Not electrical power.')
 fig=plt.figure(figsize=(16,12),dpi=100,facecolor=BG);ax=fig.add_axes([.13,.19,.64,.73]);ax.set_facecolor(BG);levels=np.linspace(-60,60,13);cont=ax.contourf(freq,multipliers*kp*1000,z,levels=levels,cmap=palette,vmin=-60,vmax=60)
 ax.contour(freq,multipliers*kp*1000,z,levels=[0],colors='#101211',linewidths=1)
 for label,lam in zip('ABC',[1.375,1.625,1.9]):
  ax.axhline(lam*kp*1000,color=GOLD,lw=1.2);ax.text(12.2,lam*kp*1000+2,label,color='#101211',fontsize=20,bbox={'facecolor':'#EFE4D1','edgecolor':'none','pad':2})
 f=np.linspace(12,24,150);inertia=const['groups']['R']['root']+const['added_air_pair_kgm2'];ax.plot(f,(2*np.pi*f)**2*inertia*1000,'--',color='#101211',lw=1.6)
 ax.plot(20,1.9*kp*1000,'o',markerfacecolor='#EFE4D1',markeredgecolor='#101211',markersize=13,markeredgewidth=2)
 ax.set_xlim(12,24);ax.set_ylim(0,multipliers[-1]*kp*1000);ax.set_xlabel('Prescribed flapping frequency (Hz)',labelpad=18);ax.set_ylabel('Pair output stiffness (N·mm/rad)',labelpad=16)
 cax=fig.add_axes([.83,.19,.025,.73]);cb=fig.colorbar(cont,cax=cax,ticks=np.arange(-60,61,20));cb.set_label('Saving versus no spring (%)',labelpad=20)
 finish(fig,'stiffness-map','Stiffness and frequency power map','All 1,694 retained samples. Plum shows savings; blue shows losses. Scale minus 60 to plus 60 percent. A, B and C are abstract torque scalings; B is the fixed setting. Dashed curve: storage estimate. Circle: sampled 20 Hz reference, not adopted optimum. Values are conditional model results, not measurements.')
print('Wrote both themes: 121 x 14 samples; 137 negative cases; exact retained digest')
