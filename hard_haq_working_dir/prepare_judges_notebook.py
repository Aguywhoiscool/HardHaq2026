"""Create a separate annotated notebook; preserve original code and saved outputs."""
import copy
import json
from pathlib import Path
import uuid

ROOT = Path(__file__).resolve().parent
PATH = ROOT/'Traped ion working file.ipynb'
OUTPUT = ROOT/'Ion trap - decisions and justification.ipynb'
BACKUP = ROOT/'notebook_backups'/'Traped ion working file.before_cleanup.ipynb'
BACKUP.parent.mkdir(exist_ok=True)
if not BACKUP.exists():
    BACKUP.write_bytes(PATH.read_bytes())
original = json.loads(BACKUP.read_text(encoding='utf-8'))
cells = original['cells']

def md(text, old=None):
    cell=copy.deepcopy(cells[old]) if old is not None else {'cell_type':'markdown','metadata':{},'id':uuid.uuid4().hex[:8]}
    cell['source']=text.strip().splitlines(keepends=True)
    return cell

def code(i): return copy.deepcopy(cells[i])

new=[md(r'''
# Surface Ion Trap Optimization
### Constrained geometry optimization for a single $^{40}\mathrm{Ca}^{+}$ ion

**Objective:** maximize the RF pseudopotential depth while meeting the ion-height, radial-frequency, Mathieu-stability and fabrication constraints.

## Result at a glance

| Saved performance | Value | Challenge requirement |
|:---|---:|:---|
| **RF-only trap depth** | **151.622 meV** | Maximize |
| Ion height above the electrodes | 59.000 µm | 50–100 µm |
| Lateral / vertical secular frequency | 6.89 / 6.97 MHz | Both ≥1 MHz |
| Mathieu parameter | 0.39911176 | ≤0.4 |
| Peak RF voltage | 100 V | ≤100 V |
| Smallest drawn feature or gap | 5 µm | ≥5 µm |

**All checks in the notebook score function pass.** These values summarize the saved outputs reproduced in Section 3 below; they are not experimental measurements.

### Selected operating point

| Parameter | Value |
|:---|---:|
| RF electrode widths | 200 µm each, symmetric |
| Gap between neighboring electrodes | 5 µm |
| Central ground electrode width | 26.71361 µm |
| Electrode thickness | 5 µm |
| Fused-silica substrate thickness | 500 µm |
| RF voltage amplitude | 100 V peak |
| RF drive frequency | 49.4 MHz |

> **Design scope:** the starter notebook fixes the center width at 60 µm and metal thickness at 2 µm. This investigation treats those dimensions as additional design variables. The saved score passes the coded checks, which do not enforce those original fixed dimensions.

**Guide:** [1. Design development](#1-design-development) · [2. Model and implementation](#2-model-and-implementation) · [3. Results and score](#3-results-and-score) · [4. Interpretation and next steps](#4-interpretation-and-next-steps) · [5. Sources](#5-sources)
'''),md(r'''
## 1. Design development

The development record below preserves the initial hypotheses, unsuccessful trials and corrections that led to the selected design. Historical parameter sets are distinguished from the executable parameters in Section 2.

### 1.1 Initial hypothesis: strengthen confinement at lower height

The RF pseudopotential is

$$\Psi(\mathbf r)=\frac{e^2|\mathbf E_{\mathrm{RF}}(\mathbf r)|^2}{4m\Omega^2},\qquad \Omega=2\pi f_{\mathrm{RF}}.$$

For a fixed geometry and voltage, lowering the drive frequency increases the pseudopotential. The initial hypothesis was that reducing ion height would also strengthen confinement; this was an exploratory assumption rather than a proof of the constrained optimum. The first Desmos plots explored the lowest allowed height and corresponding width/gap boundaries.
'''),md(r'''
**Original geometry exploration — allowed height surface**

![Desmos exploration of the ion-height constraint](attachment:image.png)
''',5),md(r'''
**Original boundary exploration — minimum-height candidates**

The intersection of the height boundary and the parameter limits suggested two initial test geometries.

![Desmos intersections used to select initial geometry trials](attachment:image.png)
''',6),md(r'''
### 1.2 Failed trials identified the stability limit

| RF width (µm) | Gap (µm) | Recorded result |
|---:|---:|:---|
| 39.423007 | 5 | Failed the Mathieu constraint |
| 20 | 12.5879626 | Failed the Mathieu constraint |

The complete RF settings for both trials were not recorded alongside the geometry, so these are historical outcomes rather than fully reproducible comparison points.

The failure motivated enforcing stability while tuning frequency:

$$q_M=\frac{2\sqrt{2}\,\omega_{\mathrm{sec}}}{\Omega},\qquad
\omega_{\mathrm{sec}}=\sqrt{\frac{1}{m}\frac{\partial^2\Psi}{\partial r^2}}.$$

For a fixed geometry,

$$\Psi\propto\frac{V_{\mathrm{RF}}^2}{\Omega^2},\qquad
\omega_{\mathrm{sec}}\propto\frac{V_{\mathrm{RF}}}{\Omega},\qquad
q_M\propto\frac{V_{\mathrm{RF}}}{\Omega^2}.$$

**Conclusion:** lowering frequency alone is insufficient; it must remain high enough to satisfy $q_M\leq0.4$.

### 1.3 Literature-guided electrode ratio

Nizamani and Hensinger [1] identify a depth-maximizing RF-width/separation ratio near 3.68 for equal-width rails at fixed height and RF settings. The figure below was used during the original investigation.

![Published geometric-factor curves for equal and unequal RF electrode widths; Nizamani and Hensinger, Fig. 3](attachment:image.png)
''',7),md(r'''
**Original Desmos comparison — applying the proposed ratio**

The ratio was initially interpreted as RF width divided by the fabrication gap. This interpretation was subsequently corrected: the denominator is the separation between the RF electrodes, including the central electrode region.

![Original Desmos plot used while testing the electrode ratio](attachment:image.png)
''',8),md(r'''
### 1.4 Balance ion height, geometry and drive frequency

The next step considered increasing ion height to reduce the field gradient and Mathieu parameter at fixed RF settings. A geometry-factor expression recorded during this stage was

$$q_M=2\sqrt{2}\frac{f_{\mathrm{sec}}}{f_{\mathrm{RF}}}
=\frac{2\epsilon eV_{\mathrm{RF}}}{m h^2(2\pi f_{\mathrm{RF}})^2},$$

where $\epsilon$ represents a geometry-dependent factor; height therefore cannot be optimized independently of electrode geometry.

The early Desmos exploration reported a height boundary near 73.10266 µm while the original ratio interpretation was still being investigated.

![Original Desmos height and ratio exploration](attachment:image.png)

#### Historical parameter milestones

| Stage | RF width (µm) | Gap (µm) | Center (µm) | Peak RF (V) | Drive (MHz) | Interpretation |
|:---|---:|---:|---:|---:|---:|:---|
| Intermediate trial | 73.6 | 20 | 60 | 100 | 40.875 | Based on the early ratio interpretation |
| Corrected separation | 200 | 5 | 44.348 | 100 | 40.6 | Recorded score ≈150.4 meV |
| Frequency refinement | 200 | 5 | 44.348 | 100 | 40.5823859 | Historical refinement near the Mathieu limit |
| Current notebook | 200 | 5 | 26.71361 | 100 | 49.4 | Saved result: 151.622 meV |

The original tuning notes also recorded $V/f^2=64/(32.7\times10^6)^2$ near a Mathieu-limited operating point. This is a historical scaling reference, not an additional current simulation result. The corrected-separation trial recorded approximately 1.5041 meV per volt; the current saved score records approximately 1.5162 meV per volt.

#### Why the selected effective ratio is about 6.46

Using the starter's gap-sharing approximation,

$$a_{\mathrm{eff}}=w_{\mathrm{center}}+g,\qquad
b_{\mathrm{eff}}=w_{\mathrm{RF}}+g,$$

$$\frac{b_{\mathrm{eff}}}{a_{\mathrm{eff}}}
=\frac{200+5}{26.71361+5}\approx6.46.$$

This does not contradict the published 3.68 value: the later search allows frequency and height to vary while enforcing the Mathieu bound, so it optimizes a different objective. The ideal-model ratio is not a proven global optimum for finite-thickness electrodes.
''',9),md(r'''
## 2. Model and implementation

### 2.1 Dependencies

The implementation uses NumPy, SciPy, Matplotlib, PhotonForge and Tidy3D. All original executable cells are retained in their original execution order, including the field reconstruction and score calculation.
'''),code(1),md(r'''
### 2.2 Active design parameters

The cell below defines the operating point used by the saved results. Widths, gaps and thicknesses are in **µm**, voltage is the **peak RF amplitude**, and frequency is in **Hz**. Both RF rails have the same width and phase.
'''),code(10),md(r'''
### 2.3 Material constants and analytic height estimate

The ion is $^{40}\mathrm{Ca}^{+}$ and the substrate is fused silica with relative permittivity 3.8. The gapless estimate provides a geometry check before the finite-gap solve:

$$h_{\mathrm{estimate}}=\frac12\sqrt{a_{\mathrm{eff}}(a_{\mathrm{eff}}+2b_{\mathrm{eff}})}.$$

The estimate and the sampled finite-gap height need not agree exactly.
'''),code(12),md(r'''
### 2.4 Cross-section, technology and mesh

The model is translationally invariant along the trap axis. Gold electrodes are represented as perfect electric conductors (PEC), so the calculation captures the field geometry but does not predict material resistance or RF heating. Mirror symmetry is valid because both RF rails are identical and driven in phase.

The following cell constructs the cross-section, applies mesh refinement and plots the geometry and grid. The original solver-window definition is retained.
'''),code(14),md(r'''
### 2.5 Cloud mode solve

The solver returns two quasi-TEM modes used to reconstruct the field of the desired electrode voltages.

> **Execution note:** this cell submits a PhotonForge cloud solve and may consume simulation credits when no cached result exists. Existing outputs can be reviewed without rerunning it.
'''),code(16),md(r'''
### 2.6 Mode-field visualization

The two mode fields are basis solutions. Neither alone is the final trap field; their weighted combination enforces the RF and ground electrode voltages.
'''),code(18),md(r'''
## 3. Results and score

### 3.1 Reconstruct the RF field and calculate confinement

The mode-voltage matrix determines the weights that set the RF rails to unit voltage and the central/outer electrodes to RF ground. The combined field is scaled by the selected RF voltage and converted to pseudopotential energy.

For this symmetric cross-section, the code finds the ion on the symmetry axis, locates the barrier above it, fits the local radial curvatures and calculates both secular frequencies. The higher secular frequency sets $q_M$; the lower frequency is checked against the 1 MHz requirement.
'''),code(20),md(r'''
### 3.2 Pseudopotential landscape

The dark minimum marks the RF null and the cyan escape marker identifies the sampled barrier above it. The plotted depth is the **RF-only radial escape barrier** of this cross-section, not a fully qualified three-dimensional trapping depth with axial DC confinement.
'''),code(22),md(r'''
### 3.3 Constraint checks and score

The original score function returns depth only when all coded checks pass. The printed score is rounded to one decimal place; the saved confinement output above reports **151.622 meV**.

The voltage-normalized diagnostic is retained, but the challenge objective is depth rather than meV per volt. The function does not enforce the starter's original fixed center width or metal thickness.
'''),code(24),md(r'''
## 4. Interpretation and next steps

### Findings

- **Stability controls frequency selection:** lowering the drive increases both depth and Mathieu parameter, so the search must enforce the stability bound throughout.
- **Symmetric rails remain the selected layout:** the separate analytic search with independent rail widths converged to approximately equal widths; this is model evidence rather than a complete finite-gap asymmetry study.
- **Several-micrometre metal is fabrication-plausible:** the separate six-case thickness screen favored 5 µm metal and found negligible depth benefit from reducing the wafer from 500 to 300 µm.
- **Material changes require a loss model:** Cu/Au is an experimentally demonstrated alternative [3], but the PEC calculation cannot establish a conductor-loss or material-dependent depth advantage.

### Distinguish the notebook result from the separate thickness screen

| Record | Depth (meV) | Drive (MHz) | Mathieu parameter | Model/output status |
|:---|---:|---:|---:|:---|
| This notebook | 151.622 | 49.4 | 0.39911176 | Saved output using the original window definition |
| Separate 5 µm / 500 µm thickness screen | 151.752 | 50.141 | 0.395 | Fixed-window field solve with air below the wafer; frequency rescaled |

These records differ in simulation boundaries and operating point and should not be presented as a controlled depth improvement. The thickness screen is documented in [the research report](FINAL_ION_TRAP_RESEARCH_REPORT.md) and [its saved results](thickness_screen_results.json).

### Remaining validation

1. Confirm mesh/domain convergence and solve at the final selected RF frequency.
2. Include axial DC confinement and search the complete escape barrier.
3. Check the final fabricated gap, electrode tolerances, adhesion and breakdown behavior.
4. For a material change, measure film resistance and model the RF feed, resonator, phase balance and thermal behavior.

The current values are numerical results, not experimental device measurements. No cloud solves were submitted during this presentation-only notebook cleanup.

## 5. Sources

[1] A. H. Nizamani and W. K. Hensinger, “Optimum electrode configurations for fast ion separation in microfabricated surface ion traps,” *Appl. Phys. B*, vol. 106, no. 2, pp. 327–338, 2012, doi: [10.1007/s00340-011-4803-x](https://doi.org/10.1007/s00340-011-4803-x). **Contribution:** electrode-width/separation ratio and asymmetric geometry context.

[2] D. T. C. Allcock et al., “Implementation of a symmetric surface electrode ion trap with field compensation using a modulated Raman effect,” *New J. Phys.*, vol. 12, Art. no. 053026, 2010, doi: [10.1088/1367-2630/12/5/053026](https://arxiv.org/abs/0909.3272). **Contribution:** symmetric layouts with DC-controlled mode rotation.

[3] J. Tao et al., “Functional surface ion traps on a 12-inch glass wafer for quantum applications,” arXiv:2002.11470, 2020. [Online](https://arxiv.org/pdf/2002.11470). **Contribution:** working Cu/Au electrodes on a glass substrate; fabrication precedent rather than a measured improvement for this design.

[4] R. Schmied, “Electrostatics of gapped and finite surface electrodes,” *New J. Phys.*, vol. 12, Art. no. 023038, 2010, doi: [10.1088/1367-2630/12/2/023038](https://doi.org/10.1088/1367-2630/12/2/023038). **Contribution:** finite-electrode and dielectric corrections beyond the ideal gapless model.

**Project basis:** [starter notebook](starter_file_given.ipynb). Additional fabrication, resistance, skin-effect and surface-physics references are collected in the [IEEE bibliography](IEEE_BIBLIOGRAPHY.md).
''')]

justifications = {
    '### 2.1 Dependencies': r'''
**Justification:** retain the starter's numerical and field-solver tools so comparisons use the same physical model and unit conventions. This avoids attributing a change in solver implementation to a change in trap geometry.
''',
    '### 2.2 Active design parameters': r'''
#### Why these values were selected

| Decision | Justification and evidence | Qualification |
|:---|:---|:---|
| Equal RF rails | Independent-width analytic screening returned approximately equal widths, supporting symmetry for the depth objective. | Unequal rails may still be useful for optical access or mode orientation; those are different objectives. |
| RF width = 200 µm | The constrained analytic search favored the upper allowed rail width for the fixed-center comparison; the final geometry retains that width. | The final finite-thickness geometry was not jointly optimized over every parameter. |
| Gap = 5 µm | Select the smallest permitted gap as a screened candidate while limiting exposed dielectric and retaining the fabrication constraint. | Finished gaps must remain at least 5 µm after plating; a smaller gap does not guarantee greater depth in every geometry. |
| Center = 26.71361 µm | Relaxing the fixed-center rule allowed an analytic geometry with a larger depth-to-stability benefit; the value is one representative of an ideal-model optimum family. | It changes the starter's fixed 60 µm center and is not a unique physical optimum. |
| RF amplitude = 100 V peak | At fixed frequency, depth scales as voltage squared; after retuning to a fixed Mathieu bound, depth increases approximately linearly with voltage. | The voltage must be sustainable at the electrode, with the stability bound and practical breakdown limit enforced. |
| Drive = 49.4 MHz | This is the operating point stored in the current notebook, whose saved output gives $q_M=0.39911176$ and passes the score. | It is not the 50.141 MHz operating point of the separate fixed-window thickness screen. |
| Metal = 5 µm | Several-micrometre plated gold is supported by fabrication literature, and 5 µm led the six-case thickness screen. | The small predicted advantage over 10 µm is not established beyond mesh uncertainty. |

These explanations combine the recorded development history with the later analysis; they do not imply that every final value was established by the original early trials.
''',
    '### 2.3 Material constants and analytic height estimate': r'''
**Decision:** retain the 500 µm fused-silica wafer and use the analytic height as a screening check. **Reason:** the separate 300/500 µm comparison showed negligible depth benefit from thinning, while retaining the original substrate avoids an unnecessary fabrication change. The height estimate is evaluated before a cloud solve because it can reject unsuitable geometry cheaply; it is not substituted for the finite-gap result.
''',
    '### 2.4 Cross-section, technology and mesh': r'''
**Justification of the model:** the RF wavelength is far larger than the chip cross-section, so the near field can be approximated as quasi-static. A two-dimensional, mirror-symmetric calculation reduces the work for identical rails; it would be inappropriate for unequal rails without removing the imposed symmetry. PEC represents equipotential metal for field-shape screening, but deliberately omits conductor losses.

**Mesh decision:** resolve the ion and escape region with the starter's local refinement rather than relying on the metre-scale RF wavelength to set the grid. The saved plots expose the geometry and mesh for review. Keeping the original window here preserves the saved workflow; a fixed window with air below the wafer was used separately when comparing substrate thicknesses.
''',
    '### 2.5 Cloud mode solve': r'''
**Justification:** obtain field basis functions for the actual finite-gap cross-section instead of relying only on the analytic gapless approximation. Two modes are retained for the symmetric half-cross-section so that the RF-rail voltage and central-ground condition can be imposed independently during reconstruction. Reusing a field solution for voltage-only scaling avoids unnecessary geometry solves.
''',
    '### 2.6 Mode-field visualization': r'''
**Reason for this check:** inspect whether the calculated fields occupy the expected electrode region before interpreting a trap depth. A visually plausible mode is not sufficient evidence of the correct trap voltage pattern; the voltage-matrix reconstruction in the next section is still required.
''',
    '### 3.1 Reconstruct the RF field and calculate confinement': r'''
**Justification of the calculation:** individual transmission-line modes do not necessarily put both grounds at zero, so their weights are solved from conductor voltages before calculating pseudopotential. Subtracting the ion energy from the saddle energy measures the escape barrier. The lower radial secular frequency is used for the confinement requirement, while the higher one is used for the Mathieu bound, preventing a favorable direction from hiding a weaker or less stable direction.

**Geometric assumption:** the axial saddle search is appropriate to the selected symmetric layout. An asymmetric design would require a two-dimensional null/saddle search and the full local curvature matrix.
''',
    '### 3.2 Pseudopotential landscape': r'''
**Reason for this figure:** connect the numerical score to the physical shape of the trapping well. The minimum and saddle should be inside the sampled and refined region; a boundary maximum could otherwise be mistaken for a resolved escape point. A convergence study is still required to quantify the numerical accuracy.
''',
    '### 3.3 Constraint checks and score': r'''
**Decision rule:** prefer a feasible design over a deeper but unstable candidate. The pass/fail checks therefore precede accepting the depth as a score. Listing the fixed-dimension scope exception separately makes clear why passing the numerical function is not equivalent to meeting every unmodified starter specification.
''',
}
for cell in new:
    if cell['cell_type']!='markdown':continue
    source=''.join(cell['source'])
    for heading,explanation in justifications.items():
        if heading in source:
            source=source.rstrip()+'\n\n'+explanation.strip()+'\n'
    if source.startswith('# Surface Ion Trap Optimization'):
        source=source.replace('# Surface Ion Trap Optimization', '# Surface Ion Trap Optimization — Decisions and Justification',1)
        source=source.replace('**Guide:**', '**Reading note:** historical hypotheses and failed trials are preserved as development evidence; explanations of later choices are identified separately from those original trials.\n\n**Guide:**')
    cell['source']=source.splitlines(keepends=True)

result=copy.deepcopy(original)
result['cells']=new
result['nbformat_minor']=max(result.get('nbformat_minor',0),5)
for c in new:
    if 'id' not in c:c['id']=uuid.uuid4().hex[:8]
before=[c for c in original['cells'] if c['cell_type']=='code']
after=[c for c in result['cells'] if c['cell_type']=='code']
assert before==after, 'Executable cells or saved outputs changed'
oldattachments=[c.get('attachments') for c in original['cells'] if c.get('attachments')]
newattachments=[c.get('attachments') for c in new if c.get('attachments')]
assert oldattachments==newattachments, 'Notebook attachments changed'
assert len({c['id'] for c in new})==len(new)
OUTPUT.write_text(json.dumps(result,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
print(f'Created separate notebook: {OUTPUT.name}')
print(f'{len(before)} code cells unchanged; all saved outputs and {len(oldattachments)} attachment groups preserved.')
print(f'Backup: {BACKUP.relative_to(ROOT)}')
