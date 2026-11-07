"""Audit current saved results and synchronize stale Markdown without rerunning code."""
import ast
import copy
import json
from pathlib import Path
import re
from datetime import datetime

ROOT=Path(__file__).resolve().parent
path=ROOT/'Ion trap - decisions and justification.ipynb'
raw=path.read_bytes()
notebook=json.loads(raw.decode('utf-8'))
before=copy.deepcopy(notebook)
all_code='\n'.join(''.join(c['source']) for c in notebook['cells'] if c['cell_type']=='code')
parameters={}
for node in ast.parse(all_code).body:
    if isinstance(node,ast.Assign):
        try:value=ast.literal_eval(node.value)
        except (ValueError,TypeError):continue
        for name in node.targets:
            if isinstance(name,ast.Name):parameters[name.id]=value
text='\n'.join(''.join(o.get('text',[])) for c in notebook['cells'] for o in c.get('outputs',[]))
def capture(pattern):return re.search(pattern,text).group(1)
height=capture(r'Ion height above the electrodes: ([0-9.]+)')
fy=capture(r'Secular frequency, lateral: ([0-9.]+)')
fz=capture(r'Secular frequency, vertical: ([0-9.]+)')
q=capture(r'Mathieu parameter q: ([0-9.]+)')
depth=capture(r'Trap depth: ([0-9.]+)')
normalized=capture(r'meV per voltage: ([0-9.]+)')
frequency=parameters['f_rf']/1e6
for c in notebook['cells']:
    if c['cell_type']!='markdown':continue
    s=''.join(c['source'])
    if s.startswith('# Surface Ion Trap Optimization'):
        s=re.sub(r'(\| Ion height above the electrodes \| )[^|]+',rf'\g<1>{height} µm ',s)
        s=re.sub(r'(\| Lateral / vertical secular frequency \| )[^|]+',rf'\g<1>{fy} / {fz} MHz ',s)
        s=re.sub(r'(\| Mathieu parameter \| )[^|]+',rf'\g<1>{q} ',s)
        s=re.sub(r'(\| \*\*RF-only trap depth\*\* \| )[^|]+',rf'\g<1>**{depth} meV** ',s)
        s=re.sub(r'(\| RF drive frequency \| )[^|]+',rf'\g<1>{frequency:.9g} MHz ',s)
        marker='\n\n> **Recheck:** the saved result is within the coded Mathieu limit, but its margin is only about 0.000035% of that limit. It is a numerical boundary candidate, not a tolerance-qualified hardware operating point. The code and saved outputs were inspected, not rerun, during this recheck.\n'
        if '> **Recheck:**' not in s:s+=marker
    if '| Current notebook |' in s:
        s=s.replace('| Current notebook | 200 | 5 | 26.71361 | 100 | 49.4 | Saved result: 151.622 meV |',
                    '| Previous saved operating point | 200 | 5 | 26.71361 | 100 | 49.4 | Earlier saved result: 151.622 meV |\n'
                    f'| Current notebook | 200 | 5 | 26.71361 | 100 | {frequency:.9g} | Saved result: {depth} meV |')
        s=s.replace('the current saved score records approximately 1.5162 meV per volt',
                    f'the current saved score records approximately {float(normalized):.4f} meV per volt')
        s=re.sub(r'\| Current notebook \|[^\n]+',f'| Current notebook | 200 | 5 | 26.71361 | 100 | {frequency:.9g} | Saved result: {depth} meV |',s)
    if '| Drive = 49.4 MHz |' in s:
        s=s.replace('| Drive = 49.4 MHz | This is the operating point stored in the current notebook, whose saved output gives $q_M=0.39911176$ and passes the score. |',
                    f'| Drive = {frequency:.9g} MHz | This is the operating point stored in the current notebook, whose saved output gives $q_M={q}$ and passes the score. |')
    if '### 2.2 Active design parameters' in s:
        s=re.sub(r'\| Drive = [0-9.]+ MHz \|',f'| Drive = {frequency:.9g} MHz |',s)
    if '### 3.3 Constraint checks and score' in s:
        s=re.sub(r'reports \*\*[0-9.]+ meV\*\*',f'reports **{depth} meV**',s)
    c['source']=s.splitlines(keepends=True)

getcode=lambda n:[c for c in n['cells'] if c['cell_type']=='code']
assert getcode(before)==getcode(notebook)
backup=ROOT/'notebook_backups'/f'Ion trap decisions.before_recheck_{datetime.now():%Y%m%d_%H%M%S}.ipynb'
backup.write_bytes(raw)
path.write_text(json.dumps(notebook,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')

f0=parameters['f_rf'];q0=float(q);d0=float(normalized)*parameters['v_rf']
qtarget=.395
margin_f=f0*(q0/qtarget)**.5
margin_d=d0*qtarget/q0
boundary_f=f0*(q0/.4)**.5
report=f'''# Final notebook recheck

Notebook: `Ion trap - decisions and justification.ipynb`.

## Current saved operating point

| Item | Value |
|---|---:|
| RF width, each rail | {parameters['rf_width']} µm |
| Gap | {parameters['gap']} µm |
| Center | {parameters['center_width']} µm |
| Metal / silica thickness | {parameters['metal_thickness']} / {parameters['substrate_thickness']} µm |
| RF voltage | {parameters['v_rf']} V peak |
| RF frequency | {frequency:.9g} MHz |
| Saved depth | {depth} meV |
| Saved height above metal | {height} µm |
| Saved lateral / vertical secular frequency | {fy} / {fz} MHz |
| Saved Mathieu q | {q} |

## Findings

1. The code parses, and execution counts run sequentially from 1 through 9. This supports a coherent saved execution record, but is not independent confirmation that every output was generated from the current source.
2. The pseudopotential uses peak RF amplitude and angular drive frequency with the expected factor 1/4. Squared V/µm fields are converted by 10^12, energies by e and 10^3 to meV, and fitted J/µm² curvatures by 10^12 to SI. These unit conversions are consistent.
3. The Mathieu calculation uses the larger radial frequency and the confinement check uses the smaller. The saved q and drive imply a maximum secular frequency of {q0*f0/(2*2**.5)/1e6:.6f} MHz, consistent with the printed {fz} MHz.
4. The saved score prints all five checks as passing. The RF width, gap and frequency also fall inside the starter parameter ranges. The center and metal thickness differ from the starter's fixed dimensions, so the result is valid only for the expanded design scope.
5. The claimed 151.75 meV earlier recommendation is superseded as the latest saved notebook result by {depth} meV. It remains a separate q=0.395, fixed-domain screen and must not be treated as the same run.
6. The gapless analytic verification passes independently for symmetric null height, saddle, gradient and reflection of unequal rails. A separate scalar optimization reproduces the ideal effective ratio near 6.4641016 and a symmetric gapless depth of 153.146915 meV at 100 V and q=0.4. The finite-gap saved result is about 0.32% higher; an ideal-model optimum is not an upper bound for a different electrode model.

## Numerical margin

The reported q is below 0.4 by {(.4-q0):.9f}, only {100*(.4-q0)/.4:.7f}% of the limit. Electrostatic scaling places the boundary at {boundary_f/1e6:.9f} MHz, about {f0-boundary_f:.2f} Hz below the current drive. That margin is much smaller than the numerical uncertainty established so far; tuning more decimal places does not establish a more reliable physical optimum.

At unchanged field geometry and voltage, retuning to q=0.395 predicts approximately **{margin_f/1e6:.6f} MHz** and **{margin_d:.3f} meV**. These are scaling estimates, not new cloud results. The notebook input was not changed to this margin setting.

## Remaining limits of the calculation

- The ion and escape barrier are found on the symmetry axis. This is appropriate for the selected symmetric RF layout, but not a complete 2D/3D barrier search with added DC fields or asymmetric geometry.
- A 0.5 µm sampling grid and a ±3 µm parabola fit sit on fields from the current 1 µm mesh. Convergence of height, fitted q and barrier has not been demonstrated, and q near 0.4 is particularly sensitive to small errors.
- The current window reaches the physical substrate bottom; the thickness-screen script instead includes air below the wafer. These boundary conventions must be held fixed in a controlled comparison.
- PEC omits conductor losses, and axial DC confinement and practical packaging are absent. No material-dependent depth improvement or fabricated-device performance is established.
- This audit did not submit cloud solves or independently reconstruct the latest fields from solver data; it reviewed stored source and outputs and ran offline analytic checks.

## Markdown corrections applied

Updated the stale summary height, secular frequencies and q; synchronized the operating frequency in the justification table; labeled the 49.4 MHz / 151.622 meV record as historical; updated the voltage-normalized score; and corrected the 153.642/153.643 rounding mismatch. All executable cells, outputs, execution counts and attachments were preserved. A pre-edit backup was saved at `{backup.relative_to(ROOT)}`.

## References

- [Nizamani and Hensinger, geometry-factor and electrode-ratio analysis](https://arxiv.org/pdf/1007.3542).
- `starter_file_given.ipynb`: reference pseudopotential, field reconstruction, curvature fits and scoring.
- `optimize_trap.py`: independent gapless field checks and constrained geometry model.
- `thickness_screen_results.json`: separate fixed-window screen at q=0.395.
'''
(ROOT/'FINAL_NOTEBOOK_RECHECK.md').write_text(report,encoding='utf-8')
print(f'Checked saved depth {depth} meV at {frequency:.9g} MHz; synchronized Markdown only.')
print('All code and saved outputs preserved; report: FINAL_NOTEBOOK_RECHECK.md')
