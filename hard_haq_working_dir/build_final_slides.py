"""Create a new concise deck from the current final notebook, with corner citations."""
from pathlib import Path
import ast
import json
import re

ROOT=Path(__file__).resolve().parent
framework=(ROOT/'build_slideshow.py').read_text(encoding='utf-8').split('data=json.loads',1)[0]
exec(compile(framework,str(ROOT/'build_slideshow.py'),'exec'))

NOTEBOOK=ROOT/'Ion trap - decisions and justification.ipynb'
n=json.loads(NOTEBOOK.read_text(encoding='utf-8'))
code='\n'.join(''.join(c['source']) for c in n['cells'] if c['cell_type']=='code')
params={}
for node in ast.parse(code).body:
    if isinstance(node,ast.Assign):
        try:value=ast.literal_eval(node.value)
        except (ValueError,TypeError):continue
        for target in node.targets:
            if isinstance(target,ast.Name):params[target.id]=value
out='\n'.join(''.join(o.get('text',[])) for c in n['cells'] for o in c.get('outputs',[]))
def value(pattern):return re.search(pattern,out).group(1)
depth=value(r'Trap depth: ([0-9.]+)')
q=value(r'Mathieu parameter q: ([0-9.]+)')
height=value(r'Ion height above the electrodes: ([0-9.]+)')
fy=value(r'Secular frequency, lateral: ([0-9.]+)')
fz=value(r'Secular frequency, vertical: ([0-9.]+)')
freq=params['f_rf']/1e6

def corner(slide,*citations):
    """Right-align compact source labels in the bottom-right corner."""
    for i,(label,url) in enumerate(citations):
        label='Source: '+label
        width=slide.draw.textlength(label,font=font(10))/100+.20
        assert width<10.5
        shape=slide.text(label,15.0-width,7.94+i*.27,width,.28,10,MUTED)
        shape.text_frame.paragraphs[0].runs[0].hyperlink.address=url
    slide.s.notes_slide.notes_text_frame.text+='\n\nReferences:\n'+'\n'.join(a+' — '+b for a,b in citations)

nb=('Final notebook: parameters and saved outputs',NOTEBOOK.as_uri())
starter=('Starter notebook: constraints and RF model',(ROOT/'starter_file_given.ipynb').as_uri())
ratio=('Nizamani & Hensinger, 2012 • doi:10.1007/s00340-011-4803-x','https://doi.org/10.1007/s00340-011-4803-x')
allcock=('Allcock et al., 2010 • doi:10.1088/1367-2630/12/5/053026','https://arxiv.org/abs/0909.3272')
thick=('Project thickness screen: thickness_screen_results.json',(ROOT/'thickness_screen_results.json').as_uri())
tao=('Tao et al., 2020 • arXiv:2002.11470','https://arxiv.org/pdf/2002.11470')
matula=('Matula, 1979 • bulk resistivity reference data','https://srd.nist.gov/JPCRD/jpcrd155.pdf')

s=Slide('Surface Ion Trap Optimization','HardHaq2026',note='Title slide. Latest numerical result is read directly from the final annotated notebook. No cloud solver is run by this presentation script.')
s.text('Geometry, stability and fabrication',1,2.6,14,1.1,36,CYAN,True)
s.text('A constrained numerical study of a single calcium-ion surface trap',1,4.2,14,1.2,25)
s.text(f'{depth} meV • {freq:.8g} MHz • 100 V peak',1,6.2,14,.9,27,GOLD)
corner(s,nb)

s=Slide('Objective: maximize depth within the constraints','Design objective',note='The original starter fixes center width60 µm and metal2 µm. The final investigation relaxes those dimensions; passing the score does not establish compliance with unmodified fixed starter dimensions. RF voltage is peak amplitude, frequencyHz and lengthsµm.')
s.table(['Requirement','Allowed value'],[['Ion height / radial frequency','50–100 µm / ≥1 MHz'],['Mathieu / peak voltage','q ≤0.4 / ≤100 V'],['RF width / gap','20–200 µm / 5–20 µm'],['RF drive','10–60 MHz']],widths=[6.4,7.8],row_h=.8,size=21)
s.text('Expanded scope: center width and layer thicknesses are design variables.',1,6.4,14,1,23,CYAN,True)
corner(s,starter,nb)

s=Slide('Development: hypothesis, failure, correction','Notebook investigation',note='The original notes hypothesized lowerheight and lowerdrive for stronger depth. Initial39.423007/5 µm and20/12.5879626 µm geometries were recorded failing Mathieu. The3.68 ratio was initially confused with width/gap, then corrected to width/separation. Historical trials support the development path but do not isolate controlled improvements between the old and new scores.')
s.bullets(['Initial hypothesis: lower ion height and RF frequency to strengthen trapping.',
           'Failed trials showed that lowering frequency could violate the Mathieu limit.',
           'Correct the electrode-separation ratio and tune frequency near q =0.4.'],y=2.4,h_each=1.15,size=25)
s.text('Recorded progress: ~150.5 meV milestone → latest saved result '+depth+' meV.',1,6.35,14,1,23,GOLD)
corner(s,('Final notebook: development notes and saved score',NOTEBOOK.as_uri()),ratio)

s=Slide('Why the selected effective ratio is about 6.46','Geometry and stability',note='The3.68 value maximizes a fixed-height depth factor for fixed RF drive. The later analytic constrained search permits height and frequency variation at fixed qmax. In the starter gap-sharing model a_eff=center+gap,b_eff=RFwidth+gap, giving205/31.71361≈6.46. This is an ideal-model optimum family, not a universal finite-thickness optimum. G is the local field gradient per volt.')
s.text('Depth ∝ V²/f²        q ∝ V G/f²',1,2.35,14,.9,32,CYAN,True)
s.bullets(['3.68 refers to RF width / RF separation—not the fabrication gap.',
           'The constrained search varies height and frequency, changing the optimum.',
           '(200 + 5)/(26.71361 + 5) ≈ 6.46 in the effective-width model.'],y=3.85,h_each=1.1,size=23)
corner(s,ratio,('Project constrained geometry model: optimize_trap.py',(ROOT/'optimize_trap.py').as_uri()))

s=Slide('Symmetric rails led the modeled depth search','Symmetry',note='The fixed60 µmcenter comparison isgapless RF-only. Equal200/200 rails give144.290 meV at individually selected drive and q=.4. Independent-width optimization converges to equal widths; illustrative200/100 µmrails give134.202. Allcock demonstrates DC mode rotation with symmetric RF layout. This is not a full finite-gap asymmetry optimization.')
s.table(['Fixed 60 µm center','Predicted depth'],[['Equal rails: 200 / 200 µm','144.29 meV'],['Independent widths: ≈200 / 200 µm','144.29 meV'],['Unequal example: 200 / 100 µm','134.20 meV']],widths=[9.4,4.8],row_h=.9,size=21)
s.text('Asymmetry may help mode orientation; it did not improve this depth objective.',1,6.4,14,1,23,CYAN,True)
corner(s,('Project analytic results: trap_optimization_results.json',(ROOT/'trap_optimization_results.json').as_uri()),allcock)

s=Slide('Thickness selection: 5 µm gold, 500 µm silica','Fabrication-aware screening',note='Six finite-gap field cases kept lateral geometryfixed and solved at50 MHz, then rescaled toq=.395. The5/500 combination gives151.752 meV at50.141MHz; it is not the final notebook run at q≈.4. Changing silica300 vs500µmhas negligible depth effect.5 vs10µmmetal differs≈.2%, so the screen selects a practical candidate without proving a precise continuous optimum. Britton quartz fabrication precedent is related but not an identical fusedsilica process.')
s.image(ASSETS/'thickness_chart.png',.9,2.15,14.2,4.4)
s.text('Retain the 500 µm wafer: thinning offered negligible modeled depth benefit.',1,6.7,14,.85,22,CYAN,True)
corner(s,thick,('Britton, 2008 • plated-gold trap fabrication','https://www.nist.gov/system/files/documents/2017/05/09/Joe-Britton.pdf'))

s=Slide('Gold-coated copper: a loss-reduction option','Materials',note='At equal5 µmtotal metal,4.8µmCu+.2µmAu predicts sheet resistance.7653 of5µmAu using bulk293Kresistivities. The calculation is a uniform-current approximation, not anRF finite-conductivity simulation. WorkingCu/Au surface traps on glass have experimentalprecedent. LowerRF conductor loss is not lower ion motionalheating; at fixed actualvoltage andgeometry no additionaldepth gain is established.')
s.text('~23% lower estimated electrode resistance',1,2.35,14,1.15,32,CYAN,True)
s.bullets(['Candidate stack: 4.8 µm copper +0.2 µm gold.',
           'Potential benefit: less conductor loss at the same electrode voltage.',
           'No demonstrated trap-depth increase at the same 100 V amplitude.'],y=4.0,h_each=1.0,size=24)
corner(s,tao,matula)

s=Slide('Final notebook: design and saved performance','Final result',note=f'The final notebook currently saves depth{depth}meV,height{height}µm,radial frequencies{fy}/{fz}MHz,q={q},at{freq:.8g}MHz. Code and outputs were inspected,not independently cloudrerun. All five coded scorechecks pass; parameter boundsalso pass in the expanded scope. qmargin is tiny,so this is a numerical result at currentresolution,not a precisionvalidated globaloptimum.')
s.table(['Design','Value'],[['RF width / gap / center','200 /5 /26.71361 µm'],['Gold / fused-silica thickness','5 /500 µm'],['Voltage / RF frequency',f'100 V peak /{freq:.8g} MHz']],widths=[6.5,7.7],row_h=.78,size=21)
s.card('Saved RF-only depth',depth+' meV',.9,5.8,4.45)
s.card('Height above metal',f'{float(height):g} µm',5.75,5.8,4.45)
s.card('Mathieu parameter',q,10.6,5.8,4.45)
corner(s,nb)

s=Slide('Conclusion','Findings',note='At the current simulation resolution,all coded constraints pass for the expanded design. The current q is only1.4e−7below.4 and physical or numericaluncertainty is not qualified. Mesh/domain checks,full axial DC confinement,RF feednetwork,breakdown and thermalchecks remain relevant before physicalqualification. The concise slide states scope without repeating the full audit. The depth result is a model prediction,not a hardwaremeasurement or proof of globaloptimality.')
s.text('The design passes all coded constraints\nat the current simulation resolution.',1,2.4,14,1.8,32,CYAN,True)
s.bullets(['Symmetric RF rails and a constrained frequency search produced the selected design.',
           'Several-micrometre gold is a practical fabrication candidate.',
           'The result is an RF-only prediction; device performance remains to be validated.'],y=4.9,h_each=.9,size=22)
corner(s,('Final notebook: score and model assumptions',NOTEBOOK.as_uri()),('Schmied, 2010 • finite-electrode modeling, doi:10.1088/1367-2630/12/2/023038','https://doi.org/10.1088/1367-2630/12/2/023038'))

if issues:raise RuntimeError(issues)
output=ROOT/'ION_TRAP_FINAL_CORNER_SOURCES'
prs.save(output.with_suffix('.pptx'))
slides[0].im.save(output.with_suffix('.pdf'),'PDF',save_all=True,append_images=[s.im for s in slides[1:]],resolution=100)
notes=['# Final presentation notes\n\nSources are shown in the bottom-right corner of each slide.\n']
for i,slide in enumerate(slides,1):
    notes.append(f'## Slide {i}\n\n'+slide.s.notes_slide.notes_text_frame.text+'\n')
output.with_suffix('.md').write_text('\n'.join(notes),encoding='utf-8')
contact=Image.new('RGB',(1200,675),BG)
for i,s in enumerate(slides):contact.paste(s.im.resize((400,225)),((i%3)*400,(i//3)*225))
contact.save(ASSETS/'final_corner_sources_contact_sheet.jpg',quality=90)
print(f'Created {len(slides)} slides; latest saved depth {depth} meV; citations in bottom-right corners.')
