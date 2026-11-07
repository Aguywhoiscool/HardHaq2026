"""Build the concise presentation with visible sources on every slide."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# Reuse drawing/export primitives without generating the longer presentation.
framework = (ROOT/'build_slideshow.py').read_text(encoding='utf-8').split('data=json.loads', 1)[0]
exec(compile(framework, str(ROOT/'build_slideshow.py'), 'exec'))

def source(slide, *items):
    """Visible readable citations, with clickable destinations in PowerPoint."""
    for i, (label, target) in enumerate(items):
        box = slide.text('Source: '+label, .9, 7.94+i*.30, 13.95, .3, 11, MUTED)
        box.text_frame.paragraphs[0].runs[0].hyperlink.address=target
    slide.s.notes_slide.notes_text_frame.text += '\n\n'+'\n'.join(label+' — '+target for label,target in items)

notebook=(ROOT/'Traped ion working file.ipynb').as_uri()
starter=(ROOT/'starter_file_given.ipynb').as_uri()
results=(ROOT/'thickness_screen_results.json').as_uri()
geometry=(ROOT/'trap_optimization_results.json').as_uri()
materials=(ROOT/'rf_material_comparison.json').as_uri()

s=Slide('Surface Ion Trap Optimization','HardHaq2026',note='Title slide for the concise presentation. The investigation covers the documented notebook development, constrained depth optimization, symmetry, fabrication thicknesses and RF material comparison.')
s.text('Geometry, stability and fabrication',.95,2.65,14,1.2,36,CYAN,True)
s.text('A numerical investigation of a single calcium-ion surface trap',.95,4.25,14,1.15,26)
s.text('Design development  •  Simulation findings  •  Material comparison',.95,6.15,14,.95,22,GOLD)
source(s,('Project investigation: working notebook and annotated decision record',(ROOT/'Ion trap - decisions and justification.ipynb').as_uri()))

s=Slide('Surface ion trap: findings and recommendation','HardHaq2026',note='Concise synthesis of notebook development, geometry screening, six finite-gap thickness cases and material calculations. The recommended center requires relaxing the starter fixed-center restriction.')
s.text('151.75 meV predicted RF-only depth',.95,2.35,14,1.1,36,CYAN,True)
s.text('Symmetric 200 µm RF rails • 5 µm gaps\n5 µm gold • 500 µm fused silica',.95,4.05,14,1.7,27)
s.text('100 V peak  |  50.141 MHz  |  q = 0.395',.95,6.4,14,.8,27,GOLD)
source(s,('Project finite-gap thickness screen: thickness_screen_results.json',results))

s=Slide('Objective and constraints','Design scope',note='The objective is maximum RF-only depth subject to the starter constraints. The later design permits a changed center, metal thickness and substrate thickness. The center is fixed at60 µm in the original starter, so scope must be explicit.')
s.table(['Constraint','Limit'],[['Height / radial frequency','50–100 µm / ≥1 MHz'],['Mathieu / voltage','q ≤0.4 / ≤100 V peak'],['RF width / gap','20–200 µm / 5–20 µm'],['Drive frequency','10–60 MHz']],widths=[6.2,8],row_h=.78,size=21)
s.text('Extended design: center width and layer thicknesses may vary.',1,6.35,14,.9,24,CYAN,True)
source(s,('starter_file_given.ipynb — parameter and score cells',starter),('Working notebook — revised center and metal thickness',notebook))

s=Slide('Notebook development: three key steps','Original investigation',note='The early notebook explored minimum height and lower drive, then recorded two failed geometry trials:39.423007 µmRF width with5 µm gap and20 µmRF width with12.5879626 µm gap. The notes attribute failure to q. The ratio was initially misread as width/gap before being corrected. The historical saved result150.543 meV was observed earlier in this session; the current saved output151.622 meV is distinct and was not independently rerun.')
s.bullets(['Start: lower height and lower RF frequency to increase depth.',
           'Failure: low-frequency trials exceeded the Mathieu limit.',
           'Revision: correct the 3.68 ratio and retune frequency near q = 0.4.'],y=2.35,h_each=1.15,size=25)
s.text('Recorded milestone: ~150.5 meV → current saved output: 151.622 meV.',1,6.3,14,1.0,23,GOLD)
source(s,('Traped ion working file.ipynb — notes in cells 3–9; saved outputs 20 and 24',notebook))

s=Slide('Why the final ratio differs from 3.68','Geometry and stability',note='Nizamani and Hensinger optimize a geometry factor at fixed height, voltage and frequency. The later analytic search allows height and frequency to vary while constraining q. The starter gap-sharing approximation givesa_eff=center+gap andb_eff=RFwidth+gap.205/31.71361≈6.46. This ratio has not been jointly reoptimized for finite thickness.')
s.text('Depth ∝ V²/f²        q ∝ V G/f²',1,2.35,14,.9,32,CYAN,True)
s.bullets(['3.68 means RF width / RF separation—not fabrication gap.',
           'The paper holds height and RF settings fixed; the constrained search varies them.',
           'Selected effective ratio: (200 + 5)/(26.71361 + 5) ≈ 6.46.'],y=3.75,h_each=1.15,size=23)
source(s,('[1] Nizamani & Hensinger, Appl. Phys. B (2012), doi:10.1007/s00340-011-4803-x','https://doi.org/10.1007/s00340-011-4803-x'),('Project constrained analytic search: optimize_trap.py',(ROOT/'optimize_trap.py').as_uri()))

s=Slide('Symmetric rails led the depth search','Symmetry comparison',note='For fixed60 µm center, equal rails achieve144.290 meV; independently optimized unequal widths converge back to200/200 µm. The illustrative200/100 µm pair gives134.202 meV. Each uses100 V and its own drive atq=.4. These are gapless predictions, not a new finite-gap asymmetric sweep. DC quadrupoles can provide mode rotation in a symmetric RF layout.')
s.table(['RF rails; center =60 µm','Predicted depth'],[['Equal: 200 / 200 µm','144.29 meV'],['Independent-width search: ≈200 / 200 µm','144.29 meV'],['Illustrative unequal: 200 / 100 µm','134.20 meV']],widths=[9.3,4.9],row_h=.88,size=21)
s.text('Asymmetry can aid mode orientation; it did not improve this modeled depth objective.',1,6.35,14,1.1,23,CYAN,True)
source(s,('Project gapless-plane results: trap_optimization_results.json',geometry),('[2] Allcock et al., New J. Phys. (2010), doi:10.1088/1367-2630/12/5/053026','https://arxiv.org/abs/0909.3272'))

s=Slide('Thickness: retain 5 µm gold on 500 µm silica','Six finite-gap field screens',note='The same200 µm rails,5 µm gap and26.71361 µm center are used throughout. Fields were solved at50 MHz with a fixed−4000 to+4000 µm domain including air below the wafer; frequency and depth were scaled toq=.395. The5 vs10 µm depth margin is about0.2%, below an established convergence guarantee. Quartz fabrication precedent is related to but not identical to fused silica.')
s.image(ASSETS/'thickness_chart.png',.9,2.05,14.2,4.45)
s.text('Wafer thinning offered negligible benefit; the 5 vs. 10 µm ranking needs a finer mesh.',1,6.65,14,.9,22,GOLD)
source(s,('Project six-case finite-gap field results; retuned to q =0.395',results),('[3] Britton, microfabrication dissertation (2008) — plated-gold fabrication precedent','https://www.nist.gov/system/files/documents/2017/05/09/Joe-Britton.pdf'))

s=Slide('Cu/Au may reduce loss—not ideal trap depth','Electrode materials',note='Compare5 µmAu with4.8 µmCu+.2 µmAu at equal total thickness. Bulk293 Kresistivities give a uniform-current sheet resistance ratio.7653, about23.5%less. This is not measured RF strip resistance. Skin depths are10.58 µmAu and9.21 µmCu. At fixed actual electrode voltage and shape PEC depth is unchanged. A complete network and measured films are needed for total savings. Surface charging,diffusion and ion motional heating are separate concerns.')
s.text('~23% lower estimated electrode resistance',1,2.35,14,1.1,32,CYAN,True)
s.bullets(['Candidate: 4.8 µm copper + 0.2 µm gold; same 5 µm total thickness.',
           'At the same 100 V electrode amplitude: no demonstrated depth gain.',
           'Film quality, coating integrity and RF feed losses require validation.'],y=4.0,h_each=1.05,size=23)
source(s,('[6] Tao et al., working Cu/Au surface trap, arXiv:2002.11470 (2020)','https://arxiv.org/pdf/2002.11470'),('[7] Matula, J. Phys. Chem. Ref. Data (1979); resistance estimates in rf_material_comparison.json','https://srd.nist.gov/JPCRD/jpcrd155.pdf'))

s=Slide('Final candidate and saved notebook result','Operating points',note='The recommended screen uses5 µmgold and500 µmsilica,100 V,26.71361 µmcenter,200 µmrails,5 µmgap. Predicted q=.395,depth151.752 meV,height58 µm,min radial6.945 MHz anddrive50.141 MHz come from fixed-window solved fields plus scaling. The current notebook saves151.622 meV at49.4 MHz,q=.39911176,height59 µm with original window conventions. These are not controlled head-to-head results; no improvement claim is made from their numerical difference.')
s.table(['Parameter','Recommended screened candidate'],[['RF width / gap / center','200 / 5 / 26.71361 µm'],['Gold / silica thickness','5 / 500 µm'],['Voltage / frequency / q','100 V / 50.141 MHz / 0.395'],['Depth / height / radial minimum','151.75 meV / 58 µm / 6.945 MHz']],widths=[6.4,7.8],row_h=.82,size=20)
s.text('Notebook saves 151.622 meV at 49.4 MHz; domain and q differ, so compare cautiously.',1,6.6,14,.95,21,GOLD)
source(s,('Fixed-window field screen + frequency scaling: recommended_thickness_candidate.json',(ROOT/'recommended_thickness_candidate.json').as_uri()),('Current saved notebook outputs — inspected, not re-executed for this deck',notebook))

s=Slide('What remains before fabrication','Validation',note='The model is RF-only and no hardware has been fabricated or measured during this investigation. The5 µmmetal choice is a screening recommendation. Mesh/domain convergence and final-drive solve remain. Axial DC confinement can lower the real escape barrier. Cu/Au estimates need measured films and bake qualification. The q margin does not qualify fabrication or RF tolerance.')
s.bullets(['Verify the final drive point with mesh and domain convergence.',
           'Include axial DC confinement and the full escape barrier.',
           'Check finished gaps, adhesion, post-bake coating and breakdown.',
           'Measure the RF network, voltage balance, power loss and temperature.'],y=2.35,h_each=1.1,size=25)
source(s,('[5] Schmied, finite-electrode and dielectric corrections, New J. Phys. (2010)','https://doi.org/10.1088/1367-2630/12/2/023038'),('[11] Copper diffusion through gold coatings, Anal. Chim. Acta (2023)','https://www.sciencedirect.com/science/article/pii/S0003267023006499'))

if issues:raise RuntimeError(f'Text overflow: {issues}')
for i,s in enumerate(slides,1):s.im.save(PREVIEWS/f'short_slide_{i:02d}.png')
prs.save(ROOT/'ION_TRAP_FINDINGS_WITH_TITLE.pptx')
slides[0].im.save(ROOT/'ION_TRAP_FINDINGS_WITH_TITLE.pdf','PDF',save_all=True,append_images=[s.im for s in slides[1:]],resolution=100)
notesout=[f'# Concise presentation notes\n\n{len(slides)} slides, including a dedicated title slide; source citations appear on every slide.\n']
for i,(title,note,_) in enumerate(notes,1):
    notesout.append(f'## Slide {i}: {title}\n\n'+slides[i-1].s.notes_slide.notes_text_frame.text+'\n')
(ROOT/'ION_TRAP_PRESENTATION_NOTES.md').write_text('\n'.join(notesout),encoding='utf-8')
contact=Image.new('RGB',(1200,225*((len(slides)+2)//3)),BG)
for i,s in enumerate(slides):contact.paste(s.im.resize((400,225)),((i%3)*400,(i//3)*225))
contact.save(ASSETS/'concise_contact_sheet.jpg',quality=90)
print(f'Updated PowerPoint, PDF and notes: {len(slides)} slides, visible sources on each.')
