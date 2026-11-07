# Final presentation notes

Sources are shown in the bottom-right corner of each slide.

## Slide 1

Title slide. Latest numerical result is read directly from the final annotated notebook. No cloud solver is run by this presentation script.

Sources: 

References:
Final notebook: parameters and saved outputs — file:///C:/Users/jacob/OneDrive/Documents/coding%20projects/HardHaq2026/hard_haq_working_dir/Ion%20trap%20-%20decisions%20and%20justification.ipynb

## Slide 2

The original starter fixes center width60 µm and metal2 µm. The final investigation relaxes those dimensions; passing the score does not establish compliance with unmodified fixed starter dimensions. RF voltage is peak amplitude, frequencyHz and lengthsµm.

Sources: 

References:
Starter notebook: constraints and RF model — file:///C:/Users/jacob/OneDrive/Documents/coding%20projects/HardHaq2026/hard_haq_working_dir/starter_file_given.ipynb
Final notebook: parameters and saved outputs — file:///C:/Users/jacob/OneDrive/Documents/coding%20projects/HardHaq2026/hard_haq_working_dir/Ion%20trap%20-%20decisions%20and%20justification.ipynb

## Slide 3

The original notes hypothesized lowerheight and lowerdrive for stronger depth. Initial39.423007/5 µm and20/12.5879626 µm geometries were recorded failing Mathieu. The3.68 ratio was initially confused with width/gap, then corrected to width/separation. Historical trials support the development path but do not isolate controlled improvements between the old and new scores.

Sources: 

References:
Final notebook: development notes and saved score — file:///C:/Users/jacob/OneDrive/Documents/coding%20projects/HardHaq2026/hard_haq_working_dir/Ion%20trap%20-%20decisions%20and%20justification.ipynb
Nizamani & Hensinger, 2012 • doi:10.1007/s00340-011-4803-x — https://doi.org/10.1007/s00340-011-4803-x

## Slide 4

The3.68 value maximizes a fixed-height depth factor for fixed RF drive. The later analytic constrained search permits height and frequency variation at fixed qmax. In the starter gap-sharing model a_eff=center+gap,b_eff=RFwidth+gap, giving205/31.71361≈6.46. This is an ideal-model optimum family, not a universal finite-thickness optimum. G is the local field gradient per volt.

Sources: 

References:
Nizamani & Hensinger, 2012 • doi:10.1007/s00340-011-4803-x — https://doi.org/10.1007/s00340-011-4803-x
Project constrained geometry model: optimize_trap.py — file:///C:/Users/jacob/OneDrive/Documents/coding%20projects/HardHaq2026/hard_haq_working_dir/optimize_trap.py

## Slide 5

The fixed60 µmcenter comparison isgapless RF-only. Equal200/200 rails give144.290 meV at individually selected drive and q=.4. Independent-width optimization converges to equal widths; illustrative200/100 µmrails give134.202. Allcock demonstrates DC mode rotation with symmetric RF layout. This is not a full finite-gap asymmetry optimization.

Sources: 

References:
Project analytic results: trap_optimization_results.json — file:///C:/Users/jacob/OneDrive/Documents/coding%20projects/HardHaq2026/hard_haq_working_dir/trap_optimization_results.json
Allcock et al., 2010 • doi:10.1088/1367-2630/12/5/053026 — https://arxiv.org/abs/0909.3272

## Slide 6

Six finite-gap field cases kept lateral geometryfixed and solved at50 MHz, then rescaled toq=.395. The5/500 combination gives151.752 meV at50.141MHz; it is not the final notebook run at q≈.4. Changing silica300 vs500µmhas negligible depth effect.5 vs10µmmetal differs≈.2%, so the screen selects a practical candidate without proving a precise continuous optimum. Britton quartz fabrication precedent is related but not an identical fusedsilica process.

Sources: 

References:
Project thickness screen: thickness_screen_results.json — file:///C:/Users/jacob/OneDrive/Documents/coding%20projects/HardHaq2026/hard_haq_working_dir/thickness_screen_results.json
Britton, 2008 • plated-gold trap fabrication — https://www.nist.gov/system/files/documents/2017/05/09/Joe-Britton.pdf

## Slide 7

At equal5 µmtotal metal,4.8µmCu+.2µmAu predicts sheet resistance.7653 of5µmAu using bulk293Kresistivities. The calculation is a uniform-current approximation, not anRF finite-conductivity simulation. WorkingCu/Au surface traps on glass have experimentalprecedent. LowerRF conductor loss is not lower ion motionalheating; at fixed actualvoltage andgeometry no additionaldepth gain is established.

Sources: 

References:
Tao et al., 2020 • arXiv:2002.11470 — https://arxiv.org/pdf/2002.11470
Matula, 1979 • bulk resistivity reference data — https://srd.nist.gov/JPCRD/jpcrd155.pdf

## Slide 8

The final notebook currently saves depth153.643meV,height58.000µm,radial frequencies6.99/7.05MHz,q=0.39999986,at49.82812MHz. Code and outputs were inspected,not independently cloudrerun. All five coded scorechecks pass; parameter boundsalso pass in the expanded scope. qmargin is tiny,so this is a numerical result at currentresolution,not a precisionvalidated globaloptimum.

Sources: 

References:
Final notebook: parameters and saved outputs — file:///C:/Users/jacob/OneDrive/Documents/coding%20projects/HardHaq2026/hard_haq_working_dir/Ion%20trap%20-%20decisions%20and%20justification.ipynb

## Slide 9

At the current simulation resolution,all coded constraints pass for the expanded design. The current q is only1.4e−7below.4 and physical or numericaluncertainty is not qualified. Mesh/domain checks,full axial DC confinement,RF feednetwork,breakdown and thermalchecks remain relevant before physicalqualification. The concise slide states scope without repeating the full audit. The depth result is a model prediction,not a hardwaremeasurement or proof of globaloptimality.

Sources: 

References:
Final notebook: score and model assumptions — file:///C:/Users/jacob/OneDrive/Documents/coding%20projects/HardHaq2026/hard_haq_working_dir/Ion%20trap%20-%20decisions%20and%20justification.ipynb
Schmied, 2010 • finite-electrode modeling, doi:10.1088/1367-2630/12/2/023038 — https://doi.org/10.1088/1367-2630/12/2/023038
