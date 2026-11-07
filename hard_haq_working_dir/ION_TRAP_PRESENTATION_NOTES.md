# Concise presentation notes

Nine slides; source citations appear on every slide.

## Slide 1: Surface ion trap: findings and recommendation

Concise synthesis of notebook development, geometry screening, six finite-gap thickness cases and material calculations. The recommended center requires relaxing the starter fixed-center restriction.

Sources: 

Project finite-gap thickness screen: thickness_screen_results.json — file:///C:/Users/jacob/OneDrive/Documents/coding%20projects/HardHaq2026/hard_haq_working_dir/thickness_screen_results.json

## Slide 2: Objective and constraints

The objective is maximum RF-only depth subject to the starter constraints. The later design permits a changed center, metal thickness and substrate thickness. The center is fixed at60 µm in the original starter, so scope must be explicit.

Sources: 

starter_file_given.ipynb — parameter and score cells — file:///C:/Users/jacob/OneDrive/Documents/coding%20projects/HardHaq2026/hard_haq_working_dir/starter_file_given.ipynb
Working notebook — revised center and metal thickness — file:///C:/Users/jacob/OneDrive/Documents/coding%20projects/HardHaq2026/hard_haq_working_dir/Traped%20ion%20working%20file.ipynb

## Slide 3: Notebook development: three key steps

The early notebook explored minimum height and lower drive, then recorded two failed geometry trials:39.423007 µmRF width with5 µm gap and20 µmRF width with12.5879626 µm gap. The notes attribute failure to q. The ratio was initially misread as width/gap before being corrected. The historical saved result150.543 meV was observed earlier in this session; the current saved output151.622 meV is distinct and was not independently rerun.

Sources: 

Traped ion working file.ipynb — notes in cells 3–9; saved outputs 20 and 24 — file:///C:/Users/jacob/OneDrive/Documents/coding%20projects/HardHaq2026/hard_haq_working_dir/Traped%20ion%20working%20file.ipynb

## Slide 4: Why the final ratio differs from 3.68

Nizamani and Hensinger optimize a geometry factor at fixed height, voltage and frequency. The later analytic search allows height and frequency to vary while constraining q. The starter gap-sharing approximation givesa_eff=center+gap andb_eff=RFwidth+gap.205/31.71361≈6.46. This ratio has not been jointly reoptimized for finite thickness.

Sources: 

[1] Nizamani & Hensinger, Appl. Phys. B (2012), doi:10.1007/s00340-011-4803-x — https://doi.org/10.1007/s00340-011-4803-x
Project constrained analytic search: optimize_trap.py — file:///C:/Users/jacob/OneDrive/Documents/coding%20projects/HardHaq2026/hard_haq_working_dir/optimize_trap.py

## Slide 5: Symmetric rails led the depth search

For fixed60 µm center, equal rails achieve144.290 meV; independently optimized unequal widths converge back to200/200 µm. The illustrative200/100 µm pair gives134.202 meV. Each uses100 V and its own drive atq=.4. These are gapless predictions, not a new finite-gap asymmetric sweep. DC quadrupoles can provide mode rotation in a symmetric RF layout.

Sources: 

Project gapless-plane results: trap_optimization_results.json — file:///C:/Users/jacob/OneDrive/Documents/coding%20projects/HardHaq2026/hard_haq_working_dir/trap_optimization_results.json
[2] Allcock et al., New J. Phys. (2010), doi:10.1088/1367-2630/12/5/053026 — https://arxiv.org/abs/0909.3272

## Slide 6: Thickness: retain 5 µm gold on 500 µm silica

The same200 µm rails,5 µm gap and26.71361 µm center are used throughout. Fields were solved at50 MHz with a fixed−4000 to+4000 µm domain including air below the wafer; frequency and depth were scaled toq=.395. The5 vs10 µm depth margin is about0.2%, below an established convergence guarantee. Quartz fabrication precedent is related to but not identical to fused silica.

Sources: 

Project six-case finite-gap field results; retuned to q =0.395 — file:///C:/Users/jacob/OneDrive/Documents/coding%20projects/HardHaq2026/hard_haq_working_dir/thickness_screen_results.json
[3] Britton, microfabrication dissertation (2008) — plated-gold fabrication precedent — https://www.nist.gov/system/files/documents/2017/05/09/Joe-Britton.pdf

## Slide 7: Cu/Au may reduce loss—not ideal trap depth

Compare5 µmAu with4.8 µmCu+.2 µmAu at equal total thickness. Bulk293 Kresistivities give a uniform-current sheet resistance ratio.7653, about23.5%less. This is not measured RF strip resistance. Skin depths are10.58 µmAu and9.21 µmCu. At fixed actual electrode voltage and shape PEC depth is unchanged. A complete network and measured films are needed for total savings. Surface charging,diffusion and ion motional heating are separate concerns.

Sources: 

[6] Tao et al., working Cu/Au surface trap, arXiv:2002.11470 (2020) — https://arxiv.org/pdf/2002.11470
[7] Matula, J. Phys. Chem. Ref. Data (1979); resistance estimates in rf_material_comparison.json — https://srd.nist.gov/JPCRD/jpcrd155.pdf

## Slide 8: Final candidate and saved notebook result

The recommended screen uses5 µmgold and500 µmsilica,100 V,26.71361 µmcenter,200 µmrails,5 µmgap. Predicted q=.395,depth151.752 meV,height58 µm,min radial6.945 MHz anddrive50.141 MHz come from fixed-window solved fields plus scaling. The current notebook saves151.622 meV at49.4 MHz,q=.39911176,height59 µm with original window conventions. These are not controlled head-to-head results; no improvement claim is made from their numerical difference.

Sources: 

Fixed-window field screen + frequency scaling: recommended_thickness_candidate.json — file:///C:/Users/jacob/OneDrive/Documents/coding%20projects/HardHaq2026/hard_haq_working_dir/recommended_thickness_candidate.json
Current saved notebook outputs — inspected, not re-executed for this deck — file:///C:/Users/jacob/OneDrive/Documents/coding%20projects/HardHaq2026/hard_haq_working_dir/Traped%20ion%20working%20file.ipynb

## Slide 9: What remains before fabrication

The model is RF-only and no hardware has been fabricated or measured during this investigation. The5 µmmetal choice is a screening recommendation. Mesh/domain convergence and final-drive solve remain. Axial DC confinement can lower the real escape barrier. Cu/Au estimates need measured films and bake qualification. The q margin does not qualify fabrication or RF tolerance.

Sources: 

[5] Schmied, finite-electrode and dielectric corrections, New J. Phys. (2010) — https://doi.org/10.1088/1367-2630/12/2/023038
[11] Copper diffusion through gold coatings, Anal. Chim. Acta (2023) — https://www.sciencedirect.com/science/article/pii/S0003267023006499
