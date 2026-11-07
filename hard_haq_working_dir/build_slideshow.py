"""Create an editable PowerPoint, a matching PDF and PNG slide previews offline."""
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT/'presentation_assets'
ASSETS.mkdir(exist_ok=True)
PREVIEWS = ASSETS/'slides'
PREVIEWS.mkdir(exist_ok=True)
BG, PANEL, TEXT, MUTED, CYAN, GOLD = '#101b2b', '#1b2b40', '#f3f6fa', '#b4c2d3', '#61d6d0', '#f0bd62'
W, H = 1600, 900
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(16), Inches(9)
slides, notes, issues = [], [], []
fontroot = Path('C:/Windows/Fonts')
regular = fontroot/'segoeui.ttf'
bold = fontroot/'segoeuib.ttf'
def font(size, heavy=False):
    return ImageFont.truetype(str(bold if heavy else regular), round(size*100/72))
def rgb(color): return RGBColor.from_string(color.lstrip('#'))

class Slide:
    def __init__(self, title, section, source='', note=''):
        self.s = prs.slides.add_slide(prs.slide_layouts[6])
        self.s.background.fill.solid(); self.s.background.fill.fore_color.rgb = rgb(BG)
        self.im = Image.new('RGB', (W,H), BG); self.draw = ImageDraw.Draw(self.im)
        self.rect(.55,.48,.08,.31,CYAN)
        self.text(section.upper(), .8,.45,14,.35,12,CYAN,True)
        self.text(title,.8,1.0,14.4,1.03,32,TEXT,True)
        self.text(source,.8,8.45,13.8,.35,9,MUTED)
        self.text(f'{len(slides)+1:02d}',15,8.43,.6,.35,11,MUTED)
        self.s.notes_slide.notes_text_frame.text = note+'\n\nSources: '+source
        slides.append(self); notes.append((title,note,source))
    def rect(self,x,y,w,h,color):
        self.draw.rectangle((round(x*100),round(y*100),round((x+w)*100),round((y+h)*100)),fill=color)
        r=self.s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        r.fill.solid();r.fill.fore_color.rgb=rgb(color);r.line.fill.background()
    def text(self,text,x,y,w,h,size=22,color=TEXT,heavy=False):
        f=font(size,heavy); result=[]
        for para in str(text).split('\n'):
            line=''
            for word in para.split():
                trial=(line+' '+word).strip()
                if self.draw.textlength(trial,font=f)>w*100-8 and line:
                    result.append(line);line=word
                else:line=trial
            result.append(line)
        lh=round(size*100/72*1.28)
        if len(result)*lh>h*100+8: issues.append((len(slides)+1,text[:55],len(result)*lh,h*100))
        for i,line in enumerate(result): self.draw.text((round(x*100),round(y*100)+i*lh),line,font=f,fill=color)
        shape=self.s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
        tf=shape.text_frame;tf.clear();tf.word_wrap=False
        tf.margin_left=tf.margin_top=tf.margin_bottom=tf.margin_right=0
        for i,line in enumerate(result):
            p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.text=line
            p.font.name='Segoe UI';p.font.size=Pt(size);p.font.bold=heavy;p.font.color.rgb=rgb(color)
            p.space_after=Pt(0);p.line_spacing=1.28
        return shape
    def image(self,path,x,y,w,h):
        image=Image.open(path).convert('RGB'); iw,ih=image.size
        scale=min(w*100/iw,h*100/ih); nw,nh=round(iw*scale),round(ih*scale)
        xx=x*100+(w*100-nw)/2; yy=y*100+(h*100-nh)/2
        self.im.paste(image.resize((nw,nh),Image.Resampling.LANCZOS),(round(xx),round(yy)))
        self.s.shapes.add_picture(str(path),Inches(xx/100),Inches(yy/100),width=Inches(nw/100),height=Inches(nh/100))
    def bullets(self,items,x=.9,y=2.4,w=14,h_each=.95,size=23):
        for i,item in enumerate(items):
            self.text('•',x,y+i*h_each,.3,.5,size,CYAN)
            self.text(item,x+.4,y+i*h_each,w-.4,h_each-.08,size)
    def card(self,label,value,x,y,w=4.4,detail=''):
        self.rect(x,y,w,2.0,PANEL)
        self.text(label,x+.25,y+.18,w-.5,.45,15,MUTED)
        self.text(value,x+.25,y+.7,w-.5,.7,31,CYAN,True)
        if detail:self.text(detail,x+.25,y+1.46,w-.5,.4,12,MUTED)
    def table(self,headers,rows,x=.9,y=2.35,widths=None,row_h=.65,size=18):
        if widths is None:widths=[14.2/len(headers)]*len(headers)
        for j,row in enumerate([headers]+rows):
            xx=x
            for i,item in enumerate(row):
                self.rect(xx,y+j*row_h,widths[i]-.025,row_h-.025, '#29435b' if j==0 else PANEL)
                self.text(item,xx+.12,y+j*row_h+.11,widths[i]-.24,row_h-.15,size,CYAN if j==0 else TEXT,j==0)
                xx+=widths[i]

def chart_style(ax):
    ax.set_facecolor(BG);ax.tick_params(colors=MUTED,labelsize=12)
    ax.spines[['top','right']].set_visible(False)
    for p in ('bottom','left'):ax.spines[p].set_color(MUTED)
    ax.yaxis.label.set_color(TEXT);ax.xaxis.label.set_color(TEXT)
    ax.grid(axis='y',color='#304358',alpha=.6);ax.set_axisbelow(True)

data=json.loads((ROOT/'thickness_screen_results.json').read_text())
fig,ax=plt.subplots(figsize=(11,4.5),facecolor=BG)
x=np.arange(3)
for j,sub in enumerate((500,300)):
    vals=[next(r['retuned_depth_meV'] for r in data if r['metal_thickness_um']==m and r['substrate_thickness_um']==sub) for m in (2,5,10)]
    bars=ax.bar(x+(j-.5)*.34,vals,width=.32,label=f'{sub} µm silica',color=CYAN if j==0 else GOLD)
    for b,v in zip(bars,vals):ax.text(b.get_x()+b.get_width()/2,v+.07,f'{v:.2f}',ha='center',color=TEXT,fontsize=11)
ax.set_xticks(x,['2 µm gold','5 µm gold','10 µm gold']);ax.set_ylim(148,153)
ax.set_ylabel('RF-only depth (meV)');chart_style(ax)
leg=ax.legend(facecolor=PANEL,edgecolor=PANEL);plt.setp(leg.get_texts(),color=TEXT)
fig.tight_layout();fig.savefig(ASSETS/'thickness_chart.png',dpi=160);plt.close(fig)

mat=json.loads((ROOT/'rf_material_comparison.json').read_text())
fig,ax=plt.subplots(figsize=(9,4.5),facecolor=BG)
names=['5 µm Au','4.8 µm Cu + 0.2 µm Au','4.5 µm Cu + 0.5 µm Au']
vals=[100,76.531543,77.670802]
bars=ax.barh(names[::-1],vals[::-1],color=[GOLD,CYAN,MUTED]);chart_style(ax)
ax.set_xlim(0,115);ax.set_xlabel('Estimated electrode resistance (% of solid gold)')
for b,v in zip(bars,vals[::-1]):ax.text(v+1,b.get_y()+b.get_height()/2,f'{v:.1f}%',va='center',color=TEXT,fontsize=13)
fig.tight_layout();fig.savefig(ASSETS/'material_chart.png',dpi=160);plt.close(fig)

s=Slide('Surface ion trap optimization','HardHaq2026 • research presentation',
        'Project notebooks + completed geometry, thickness and material analyses',
        'This presentation preserves the user’s documented hypotheses and corrections, then separates analytic predictions, finite-gap field screens and material estimates. No new simulation was run for the presentation.')
s.text('From a first hypothesis to a physically plausible candidate',.9,2.45,13,1.4,35,CYAN,True)
s.text('Original notebook exploration • constrained RF optimization\nSymmetry • electrode thickness • substrate thickness • materials',.9,4.25,13,1.5,23)
s.text('40Ca+  |  100 V peak  |  ~50 MHz  |  5 µm gold on 500 µm silica',.9,6.55,14,1,20,GOLD)

s=Slide('The recommended candidate','Result', 'Thickness screen + quasi-static retuning; center-width restriction relaxed',
        'The 151.75 meV candidate is the best practical choice among six screened thickness combinations at one lateral geometry, not a global optimum. The actual fields were solved at 50 MHz, then scaled to q=0.395. The final-frequency solve and mesh convergence remain outstanding.')
s.card('RF-only depth','151.75 meV',.9,2.35,4.45,'Finite-gap field screen, then scaling')
s.card('Height above metal','58 µm',5.75,2.35,4.45,'q target = 0.395')
s.card('Drive frequency','50.141 MHz',10.6,2.35,4.45,'100 V peak on equal RF rails')
s.bullets(['Both RF rails: 200 µm; common gap: 5 µm; center: 26.71361 µm.',
           'Gold thickness: 5 µm; fused-silica substrate: 500 µm.',
           'Minimum radial secular frequency: 6.945 MHz; validate before fabrication.'],y=5.1,h_each=.9,size=22)

s=Slide('Define the allowed design space','Constraints','Starter notebook, parameter and score cells',
        'The starter fixes the center at 60 µm, gold at 2 µm and substrate at 500 µm. The working notebook changes the center. The user later explicitly allowed thickness and material investigation. We keep the strict and relaxed scopes separate.')
s.table(['Quantity','Requirement'],[['RF width','20–200 µm'],['Electrode gap','5–20 µm'],['RF voltage / drive','10–100 V peak / 10–60 MHz'],['Ion height / secular minimum','50–100 µm / ≥1 MHz'],['Mathieu / minimum feature','q ≤ 0.4 / ≥5 µm']],widths=[5,9.2],size=19)
s.text('Scope change: the starter fixes center = 60 µm; the later candidate varies it.',.95,7.25,14,.7,20,GOLD)

s=Slide('Depth and stability must be optimized together','Physics','Starter physics primer; additional geometry analysis',
        'E is peak RF field, Ω=2πf, e is ion charge and m is the mass of 40Ca+. The secular relation and Mathieu mapping use the pseudopotential approximation. These are not exact stability or full 3D escape calculations.')
s.text('Ψ = e² |E_RF|² / (4 m Ω²)',1,2.45,14,.8,31,CYAN,True)
s.text('Depth ∝ V² / f²       Secular frequency ∝ V / f       q ∝ V / f²',1,3.65,14,1.0,25)
s.bullets(['Lower frequency increases depth, but also increases q.',
           'A higher ion can reduce q at fixed drive, while weakening confinement.',
           'Optimize depth subject to q ≤ 0.4; do not minimize q by itself.'],y=5.0,h_each=.9,size=22)

s=Slide('Your first hypothesis: go lower','Original notebook • cells 3–6','Traped ion working file.ipynb, original markdown and embedded Desmos images',
        'The user wrote that lowering Ω raises pseudopotential and that a lower height intuitively gives a deeper well. They used Desmos to find low-height geometric bounds. This is the documented exploratory hypothesis, not a claim that the constrained optimum must always lie at minimum height.')
s.text('“intuitivley lower height = deeper well (I think theres no proof)”',.9,2.2,14,1,23,GOLD)
s.image(ASSETS/'notebook_cell_5.png',.9,3.3,7.0,3.7)
s.image(ASSETS/'notebook_cell_6.png',8.1,3.3,7.0,3.7)
s.text('You explored the height boundary in Desmos before testing the RF stability constraint.',.95,7.45,14,.7,19)

s=Slide('The first candidates failed the Mathieu check','Original notebook • cell 7','User’s recorded failed trials; not rerun for this deck',
        'The notebook records two geometry trials that failed because of the Mathieu parameter. Complete electrical settings are not recorded alongside both trials, so the table reports only the geometry and the recorded outcome. The failure changed the search strategy.')
s.table(['RF width','Gap','Recorded outcome'],[['39.423007 µm','5 µm','FAIL: Mathieu constraint'],['20 µm','12.5879626 µm','FAIL: Mathieu constraint']],widths=[4,4,6.2],row_h=.9,size=21)
s.text('Your correction: simply shrinking the RF drive frequency is suboptimal.',1,5.65,14,1,25,CYAN,True)
s.text('Next idea: choose a frequency that just satisfies q ≤ 0.4.',1,7.0,14,.8,22)

s=Slide('The 3.68 ratio: useful, but easy to misread','Original notebook • cells 7–9','[1] Nizamani & Hensinger; user-provided paper figure in notebook',
        'The user first interpreted 3.68 as RF width divided by fabrication gap, then corrected it to rail width divided by RF separation. The paper’s optimum also holds height, voltage and frequency fixed, whereas our later search retunes frequency under the Mathieu constraint. The image is preserved from the user’s notebook and attributed to the paper.')
s.image(ASSETS/'notebook_cell_7.png',.9,2.2,6,5.65)
s.text('First reading: RF width / gap ≈ 3.68\n\nCorrect meaning: RF width / separation between RF rails ≈ 3.68',7.4,2.5,7.4,2.8,24)
s.text('The published optimum is conditional on fixed height, voltage and frequency.',7.4,6.0,7.3,1.5,23,GOLD)

s=Slide('Your next idea: use height to control q','Original notebook • cell 9','Notebook notes and intermediate parameter set; [1] geometry-ratio context',
        'The user noticed the height dependence in a published q expression and considered higher positions to reduce q. The notes identify an intermediate height around 73.10266 µm while still using the early ratio interpretation. The parameter set is historical, not the final validated optimum.')
s.image(ASSETS/'notebook_cell_9.png',.9,2.2,3.9,5.6)
s.text('You recognized that increasing height can reduce q at fixed RF settings.',5.2,2.45,9.7,1.3,25,CYAN,True)
s.text('Intermediate recorded trial:\nRF width = 73.6 µm; gap = 20 µm\n100 V peak; drive = 40.875 MHz',5.2,4.25,9.7,2.2,24)
s.text('This motivated balancing height and frequency rather than minimizing both.',5.2,7.0,9.7,.9,20,GOLD)

s=Slide('Correcting the ratio produced your first strong result','Original notebook • historical milestone','Notebook cell 9 + earlier saved output inspected during this investigation',
        'Notebook markdown records approximately 150.4 meV near 40.6 MHz. At the start of this session, the saved numerical output was 150.543 meV, q=0.4, at 40.5823859 MHz, 44.348 µm center and 2 µm metal. The file has since been updated by the user. This slide preserves that milestone without portraying it as the current notebook output.')
s.table(['Parameter','Historical value'],[['RF width / gap','200 µm / 5 µm'],['Center width','44.348 µm'],['RF voltage / drive','100 V / 40.5823859 MHz'],['Saved depth / q','150.543 meV / 0.400']],widths=[6,8.2],row_h=.8,size=21)
s.text('This changed the center from the starter’s fixed 60 µm value.',1,6.75,14,.9,23,GOLD)

s=Slide('Your notebook now saves a later operating point','Current saved notebook output','Traped ion working file.ipynb, parameter cell 10 and outputs 20, 24',
        'At presentation creation the notebook parameter cell specifies 200 µm RF rails, 5 µm gap, 26.71361 µm center, 5 µm metal, 500 µm substrate, 100 V and 49.4 MHz. Saved output shows 151.622 meV, q=0.39911176, 59 µm height and radial frequencies 6.89/6.97 MHz. We inspected the saved file; we did not re-execute it to verify output provenance.')
s.card('Saved depth','151.622 meV',.9,2.35,4.45,'49.4 MHz • 100 V peak')
s.card('Saved Mathieu q','0.39911176',5.75,2.35,4.45,'All notebook score checks pass')
s.card('Saved ion height','59 µm',10.6,2.35,4.45,'Radial frequencies: 6.89 / 6.97 MHz')
s.text('Center = 26.71361 µm; metal = 5 µm; substrate = 500 µm.',1,5.25,14,.9,24)
s.text('A saved notebook result—not a new run performed for this presentation.',1,6.7,14,1,22,GOLD)

s=Slide('Why the final effective ratio is about 6.46','Constrained geometry optimization','[1] fixed-parameter optimum; optimize_trap.py uses the Mathieu-constrained objective',
        'Define a_eff=center+gap and b_eff=RF width+gap as in the starter. The selected geometry has 205/31.71361≈6.464. The gapless constrained search finds this ratio when center and RF frequency may vary at fixed maximum voltage. It is not a newly proven universal ratio and has not been jointly reoptimized for finite thickness.')
s.text('Published objective: maximize depth at fixed height, voltage and frequency.',1,2.35,14,1.2,25)
s.text('Our objective: maximize depth while allowing height and frequency to vary, with q ≤ 0.4.',1,3.85,14,1.3,25,CYAN,True)
s.text('b_eff / a_eff = (200 + 5) / (26.71361 + 5) ≈ 6.46',1,5.6,14,1,30,GOLD,True)
s.text('The objectives differ; the paper’s 3.68 value was not disproved.',1,7.15,14,.8,21)

s=Slide('The geometry search favored symmetric RF rails','Equal vs. unequal rails','Analytic gapless-plane searches; [1] and [2] provide symmetry/cooling context',
        'Each rail was independently allowed between 20 and 200 µm at a common 5–20 µm gap; all voltages are equal-phase. The fixed-center asymmetric search converged back to equal widths. A 2:1 rail example is shallower in the same model. This is numerical screening evidence, not a full finite-gap asymmetry sweep.')
s.table(['Fixed 60 µm center','RF widths','Predicted depth'],[['Equal rails','200 / 200 µm','144.290 meV'],['Widths independently optimized','≈200 / 200 µm','144.290 meV'],['Illustrative 2:1 rails','200 / 100 µm','134.202 meV']],widths=[6.4,3.9,3.9],row_h=.85,size=19)
s.text('All three: 100 V; drive individually retuned to q = 0.4.',1,6.1,14,.7,20,MUTED)
s.text('Unequal rails may help mode orientation; symmetric rails can use DC fields for rotation [2].',1,7.1,14,1,21,CYAN)

s=Slide('Offline search, then a realistic field screen','Numerical method','optimize_trap.py + sweep_thickness.py; [5] finite-electrode corrections',
        'Offline code analytically solves the two-strip complex field, locates the RF null and saddle candidates, computes the local gradient, selects the lowest drive satisfying q, and runs differential evolution over geometry. Symmetric height, saddle, gradient and reflection checks pass. The finite-gap solver reconstructs unit-voltage electrode fields from quasi-TEM modes.')
s.bullets(['Analytic field → RF null, local gradient and off-axis saddle candidates.',
           'Choose 100 V and the lowest feasible drive at the target q.',
           'Search widths/gap; repeat with center fixed and then free.',
           'Verify the selected geometry using finite-gap fields and thickness cases.',
           'Use convergence and hardware measurements before claiming a physical optimum.'],y=2.35,h_each=1.05,size=22)

s=Slide('The notebook’s field maps show the trapping mechanism','Saved notebook visualization','Original notebook plots: mode fields and pseudopotential, cells 18 and 22',
        'These images are extracted directly from saved notebook outputs. The two quasi-TEM modes are combined to impose unit RF-rail voltage and central/outer grounds. The pseudopotential minimum marks the ion and the escape saddle sets the RF barrier. These are not new plots generated from a new cloud solve.')
s.image(ASSETS/'notebook_plot_18_0.png',.9,2.3,7.0,4.7)
s.image(ASSETS/'notebook_plot_22_0.png',8.1,2.1,7.0,5.8)
s.text('Mode fields combine to enforce electrode voltages.',.95,7.35,7,.7,17)
s.text('Depth is the saddle barrier above the RF null.',8.15,7.8,7,.5,17)

s=Slide('Thickness must remain fabrication-plausible','Physical design','[3], [4], [5], [12]; proposed screen bounds are engineering choices',
        'Six combinations were chosen: gold thickness 2,5,10 µm and fused silica thickness 300,500 µm. Published related devices demonstrate several-micrometre gold and narrow gaps. Quartz and fused silica are distinct materials, so examples support process plausibility without guaranteeing this design. Adhesion, seed stack, overplating, bake and final gap need qualification.')
s.table(['Dimension','Screened choices','Reason'],[['Gold thickness','2, 5, 10 µm','Related plated-electrode precedents'],['Silica wafer','300, 500 µm','Hundreds of µm; keep 500 µm baseline'],['Finished electrode gap','≥5 µm','Check sidewalls and plating growth']],widths=[4,4.4,5.8],row_h=.9,size=19)
s.text('A 10 µm-high electrode across a 5 µm gap is more demanding to fabricate.',1,6.3,14,1,22,GOLD)
s.text('Reasonable dimensions ≠ qualified device: package, breakdown and thermal checks remain.',1,7.45,14,.7,19)

s=Slide('Five-micrometre gold led the six-case thickness screen','Finite-gap results','thickness_screen_results.json; fields solved at 50 MHz, then rescaled to q = 0.395',
        'All six retain 200 µm rails,5 µm gap,26.71361 µm center and100 V. The vertical window is fixed −4000 to +4000 µm with air below the physical wafer. Gold5/silica500 predicts151.751954 meV at50.141372 MHz. Gold5/silica300 is151.752843, essentially identical. The 0.2% gap between5 and10 µm metal is not established beyond mesh error.')
s.image(ASSETS/'thickness_chart.png',.9,2.15,14.2,4.6)
s.text('Keep the 500 µm wafer: thinning produced negligible depth benefit.',1,6.95,14,.75,23,CYAN,True)
s.text('5 vs. 10 µm differs by only ~0.2%; a finer mesh is needed to establish the ranking.',1,7.75,14,.55,18,GOLD)

s=Slide('Three result records—three different comparisons','Evidence and operating points','Earlier session record; current saved notebook; completed fixed-window thickness screen',
        'Do not rank these as a controlled head-to-head experiment. The historical center and thickness differ; the latest saved notebook has the original lower-window convention and49.4 MHz; the thickness screen includes air below the wafer in a fixed window and rescales to q=.395. The deck preserves each evidence record and does not claim a 151.622→151.752 improvement from an isolated variable.')
s.table(['Record','Depth','Drive','q'],[['Historical notebook milestone','150.543 meV','40.582 MHz','0.400'],['Current saved notebook','151.622 meV','49.400 MHz','0.39911'],['5 µm / 500 µm thickness screen','151.752 meV','50.141 MHz','0.395']],widths=[6.1,2.9,2.9,2.3],row_h=.9,size=18)
s.text('Geometry, domain and q differ; these are not directly comparable depth gains.',1,6.4,14,1,23,GOLD,True)
s.text('The 153.147 meV analytic optimum is also a different, gapless q = 0.4 calculation.',1,7.65,14,.6,19)

s=Slide('Material choice changes loss, not the ideal boundary field','RF electrode materials','[6] working Cu/Au trap; [7] material data; existing field solver uses PEC',
        'The selected simulation models the conductor as PEC, so merely swapping material labels produces no calculated depth change. At equal actual voltage,phase and external geometry an equipotential conductor generates essentially the same electrostatic field. Finite conductivity can change the real feed voltage or phase; the full drive network is required to quantify this.')
s.bullets(['Baseline: 5 µm gold; retain the demonstrated field geometry.',
           'Alternative: Cu core with a continuous thin Au surface finish.',
           'At fixed 100 V on the electrode: no demonstrated direct depth gain.',
           'Potential benefit: less conductor dissipation to maintain that voltage.'],y=2.35,h_each=1.1,size=23)
s.text('A full feed + resonator model is needed for power, phase and temperature predictions.',1,7.25,14,.9,21,GOLD)

s=Slide('Cu/Au may reduce electrode resistance by about 23%','Material calculation','[7] bulk resistivities at 293 K; [8] skin effect; compare_rf_materials.py',
        'Use Au rho2.214e−8 and Cu1.678e−8 Ωm from Matula. Sum in-plane layer conductances t/rho. At50.141 MHz skin depths are10.58 µmAu and9.21 µmCu, so uniform-current sheet conductance is a useful first approximation for a5 µm film, not an exact RF strip resistance. The estimate omits seed/barrier, edge crowding, surface roughness and process-dependent resistivity.')
s.image(ASSETS/'material_chart.png',.9,2.25,10.5,4.6)
s.text('5 µm total metal\n\nBulk data at 293 K\n\nNo measured-film or full RF loss simulation',11.65,2.6,3.4,3.8,20,GOLD)
s.text('If electrodes cause only 10% of total system loss, the estimated total saving is ~2.35%.',1,7.15,14,1,21,CYAN)

s=Slide('What sources 8–11 add to the material decision','Practical interpretation','IEEE_BIBLIOGRAPHY.md, references [8]–[11]',
        'These references do not determine the optimal geometry or prove more trap depth. They explain current penetration, distinguish RF heating from ion motional heating, identify photocharging risk and motivate bake-stack qualification. Inference about copper process reliability is limited to the cited studies and must be tested for the actual package.')
s.table(['Source','What it changes in our decision'],[['[8] Skin effect','Thin gold does not force all current to stay in gold.'],['[9] Ion motional heating','Lower conductor resistance is not proof of lower ion heating.'],['[10] Laser charging','Surface material can affect stray fields under illumination.'],['[11] Cu–Au diffusion','Check coating integrity after the actual vacuum bake.']],widths=[4,10.2],row_h=.95,size=19)

s=Slide('What remains before calling this a physical optimum','Validation', 'Current results are RF-only screens and material estimates',
        'No finite-conductivity cloud simulation, fabricated test coupon, full resonator characterization or physical trap measurement was performed by the assistant. The working notebook contains saved results supplied by the user. The recommended geometry needs axial DC fields, electrical/thermal/breakdown tests, tolerances and more rigorous convergence. The q=.395 target gives modest numerical margin but is not hardware tolerance qualification.')
s.bullets(['Re-solve at the final drive frequency; refine mesh and domain.',
           'Include axial DC confinement and search the full escape barrier.',
           'Check finished gaps, adhesion, roughness and dimensional tolerances.',
           'Measure plated-film resistance and post-bake coating quality.',
           'Model leads, bonds, return paths and resonator; verify RF phase and temperature.'],y=2.35,h_each=1.05,size=22)

s=Slide('The strongest conclusions we can defend','Findings','Project calculations + six finite-gap field screens + cited material studies',
        'These conclusions deliberately distinguish measured hardware evidence in the literature from model predictions in this project. Gold-coated copper remains a candidate to test rather than the final confirmed material. The original hypotheses and revisions are part of the documented development path, not errors hidden by the final result.')
s.bullets(['Your failed low-frequency trials identified the stability tradeoff.',
           'Correcting the meaning—and assumptions—of the geometry ratio mattered.',
           'Symmetric rails led the constrained analytic depth search.',
           '5 µm gold on 500 µm silica is the recommended screened candidate.',
           'Cu/Au offers a plausible conductor-loss benefit, with no established depth gain.'],y=2.35,h_each=1.05,size=23)

bib=(ROOT/'IEEE_BIBLIOGRAPHY.md').read_text(encoding='utf-8')
entries=re.findall(r'^\[(\d+)\] (.+)$',bib,re.M)
for page in range(3):
    s=Slide(f'References {page*4+1}–{page*4+4}','IEEE bibliography','Full clickable references are in the PowerPoint speaker notes and IEEE_BIBLIOGRAPHY.md',
            '\n\n'.join(f'[{n}] {entry}' for n,entry in entries[page*4:page*4+4]))
    for j,(n,entry) in enumerate(entries[page*4:page*4+4]):
        citation=entry.split(' [Online].')[0]
        s.text(f'[{n}] {citation}',.95,2.2+j*1.45,14.1,1.25,17)
        url=re.search(r'Available: <([^>]+)>',entry).group(1)
        shape=s.text('Open source ↗',.95,3.3+j*1.45,14,.32,10,CYAN)
        shape.text_frame.paragraphs[0].runs[0].hyperlink.address=url

if issues: raise RuntimeError(f'Text overflow candidates: {issues}')
for i,s in enumerate(slides,1):s.im.save(PREVIEWS/f'slide_{i:02d}.png')
prs.save(ROOT/'ION_TRAP_FINDINGS.pptx')
slides[0].im.save(ROOT/'ION_TRAP_FINDINGS.pdf','PDF',save_all=True,append_images=[s.im for s in slides[1:]],resolution=100)
out=['# Presentation speaker notes\n','Source notebook: `Traped ion working file.ipynb`. Original notebook images are embedded; charts are generated from saved data.\n']
for i,(title,note,source) in enumerate(notes,1):out.append(f'## Slide {i}: {title}\n\n{note}\n\nSources: {source}\n')
(ROOT/'ION_TRAP_PRESENTATION_NOTES.md').write_text('\n'.join(out),encoding='utf-8')
thumbw,thumbh=400,225
contact=Image.new('RGB',(thumbw*4,thumbh*((len(slides)+3)//4)),BG)
for i,s in enumerate(slides):contact.paste(s.im.resize((thumbw,thumbh)),((i%4)*thumbw,(i//4)*thumbh))
contact.save(ASSETS/'presentation_contact_sheet.jpg',quality=90)
print(f'Created {len(slides)} slides: PowerPoint, PDF, notes and preview images.')
