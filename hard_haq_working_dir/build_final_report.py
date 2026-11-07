"""Assemble the single-file research record from the saved analyses and data."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
intro = r'''# Final ion-trap optimization and materials research report

Prepared for the HardHaq2026 project. Investigation date: 6 November 2026.

## Final answer and its evidence level

The recommended next design to validate uses equal 200 µm RF rails, a 5 µm gap, a 26.71361 µm center, 5 µm gold electrodes and a 500 µm fused-silica wafer. Its finite-gap field screen predicts approximately **151.75 meV depth**, **58 µm height above the metal**, and **6.9446 MHz minimum radial secular frequency**, after quasi-static retuning to **50.14137 MHz**, **100 V peak** and **q = 0.395**.

This is a recommended candidate, not a certified fabricated device or a proven joint global optimum. The starter originally fixes the center at 60 µm: the recommended geometry assumes that restriction is relaxed, as in the working notebook. If the original restriction remains, the offline symmetric result is 200 µm rails, 5 µm gap, 60 µm center and 35.28477 MHz, predicting 144.29 meV at q = 0.4. Its thickness has not been jointly reoptimized in the finite-gap screen.

Gold-coated copper is a credible second material candidate, with estimated electrode resistance about 23% lower than solid gold for equal total thickness using bulk room-temperature data. **No additional trap-depth gain has been demonstrated from changing the material.** At the same actual electrode voltage and geometry the ideal electrostatic depth is unchanged. The potential benefit is reduced conductor dissipation; total power savings and ion motional heating require separate evaluation.

## How we arrived at the answer

1. **Read the project inputs.** The starter notebook defines a five-wire surface trap for 40Ca+, its field extraction and scoring. The working notebook preserves a 150.543 meV result with a 44.348 µm center. We identified that this center differs from the starter's fixed 60 µm rule and kept those scopes separate.
2. **Correct the initial optimization argument.** Reducing RF frequency raises depth but also raises q. Greater height can lower q at fixed voltage/frequency, but it also weakens confinement. We therefore optimized depth subject to q rather than minimizing q itself. We also corrected the interpretation of the published 3.68 ratio: it is RF width divided by RF separation, not fabrication gap.
3. **Eliminate unnecessary electrical searches.** For each geometry, use the highest feasible voltage and the lowest drive frequency allowed by q and the drive bounds. This follows directly from the voltage/frequency scaling laws in the RF pseudopotential approximation. The reported candidates all permit 100 V.
4. **Search geometry offline.** An analytic gapless-plane field model located the RF null and off-axis saddle candidates, allowing a fair unequal-rail comparison. Differential evolution searched the geometric ranges. Even with independent rail widths, the best solutions approached equal widths. Closed-form checks and a second random seed supported the numerical result; they do not prove a real-device global optimum.
5. **Allow the center to vary separately.** Relaxing that restriction raised the ideal prediction to about 153.147 meV at q = 0.4. Several scaled geometries attain essentially the same ideal depth; a 26.71361 µm center is a convenient representative rather than a unique optimum.
6. **Research feasible thicknesses.** Published surface traps support several-micrometre plated gold and wafers hundreds of micrometres thick. We screened 2, 5 and 10 µm metal against 300 and 500 µm silica, rather than allowing physically unbounded dimensions.
7. **Run six finite-gap cloud field solves.** All use the same lateral candidate and 50 MHz drive. We fixed the vertical simulation window at −4000 to +4000 µm so the wafer's bottom dielectric interface sits inside the domain. Each result was retuned by electrostatic scaling to q = 0.395. Five-micrometre gold led the thickness screen; changing wafer thickness had negligible effect. An earlier original-window solve was excluded after a console-output failure; it is not part of the six-case comparison.
8. **Investigate materials without claiming a PEC loss result.** The simulation uses perfect electric conductors, so it cannot rank real metals by resistance. We instead reviewed an experimentally demonstrated Cu/Au trap and calculated sheet conductance and skin depths using cited bulk resistivities. Film-quality sensitivity showed that a poorer copper film could erase the gain.
9. **Choose a practical candidate and preserve uncertainty.** Retain the 500 µm wafer and solid gold reference. Evaluate Cu/Au with measured coupons and a complete RF feed/resonator model before changing the fabrication specification.

## What has and has not been established

| Question | Supported answer | Evidence |
|---|---|---|
| Equal or unequal RF widths for this score? | Equal widths favored in the screened model | Offline constrained searches plus relevant literature |
| Does a higher ion always give the best constrained depth? | No; height, field gradient and drive frequency must be optimized together | Pseudopotential and Mathieu scaling |
| Which tested metal thickness leads? | 5 µm, with only a small margin over 10 µm | Six finite-gap field screens, then drive scaling |
| Should the wafer be thinned for depth? | No meaningful benefit in these cases | 300 versus 500 µm comparison |
| Can Cu/Au reduce conductor loss? | Plausible; roughly 23% in the bulk uniform-current estimate | Material data, calculation and fabrication precedent |
| Does Cu/Au increase depth at 100 V? | No established gain | PEC model cannot evaluate losses; ideal fields depend on boundary voltages |
| Is physical operation guaranteed? | No | Packaging, DC confinement, surface quality, heating and breakdown are not qualified |

In particular, the 5 versus 10 µm depth difference is about 0.2%, so mesh convergence is needed before asserting its ranking. The RF-only cross-section does not establish the total 3D escape depth after axial DC confinement. A finer mesh, a solve at the final retuned frequency, actual package boundaries and fabrication tolerances remain necessary.

## Reading this report

The three analyses below preserve the equations, numerical results, research links and limitations behind the recommendation. The resource register afterward adds relevant discoveries that were not used to establish the result. Finding a resource is not the same as verifying or relying on its full text. Secondary mirrors are identified separately. This file is self-contained for the findings; scripts and raw data are listed for reproducibility.

'''

additional = r'''
## Additional resource register

The core sources used for the decisions are linked beside the claims in the analyses above. This register records additional resources found in the notebooks or search results. Unless explicitly discussed above, these were background/discovery items, not quantitative evidence for the final design. Some PDFs or publisher pages could not be opened in full; no unread content is treated as verified.

### Foundational and project-bibliography resources

- [House, Analytic model for electrostatic fields in surface-electrode ion traps](https://doi.org/10.1103/PhysRevA.78.033402) — original notebook reference for the analytic field/height approximation; not newly reviewed in full.
- [Leibfried et al., Quantum dynamics of single trapped ions](https://doi.org/10.1103/RevModPhys.75.281) — original notebook reference for RF dynamics and pseudopotential theory.
- [Gerasin et al., Optimized Surface Ion Trap Design for Tight Confinement and Separation of Ion Chains](https://doi.org/10.3390/quantum6030029) — existing project bibliography; not used to calculate the new optimum.
- [Abbasov et al., Surface-Electrode Ion Trap Development](https://doi.org/10.1134/S0021364023602063) — existing bibliography and search discovery; finite-geometry comparisons are relevant background.
- [Nizamani & Hensinger, publisher DOI](https://doi.org/10.1007/s00340-011-4803-x) — journal version of the arXiv paper used above.
- [PhotonForge Technology documentation](https://docs.flexcompute.com/projects/photonforge/en/latest/_autosummary/photonforge.Technology.html) and [PortSpec documentation](https://docs.flexcompute.com/projects/photonforge/en/latest/_autosummary/photonforge.PortSpec.html) — links supplied in the starter notebook; execution used the locally installed package and starter implementation.

### Other trap-design papers and demonstrations discovered

- [Guidelines for Designing Surface Ion Traps Using the Boundary Element Method](https://www.mdpi.com/1424-8220/16/5/616) — design workflow, analytic assumptions and realistic numerical geometry; also found as a [PMC copy](https://pmc.ncbi.nlm.nih.gov/articles/PMC4883307/), which returned an access challenge on opening.
- [Controlling trapping potentials and stray electric fields in a microfabricated ion trap through design and compensation](https://doi.org/10.1088/1367-2630/14/7/073012) — asymmetric five-wire implementation.
- [Optimization of two-dimensional ion trap arrays for quantum simulation](https://doi.org/10.1088/1367-2630/14/8/085009) — analytic/numerical comparisons in other trap geometries.
- [Surface Ion Trap for Fast Microwave Gates](https://www.mdpi.com/2674-0729/4/4/41) — another geometry and electrical-parameter optimization study.
- [Electron impact ionization loading of a surface electrode ion trap](https://arxiv.org/abs/quant-ph/0603142) — loading and depth-related background.
- [Demonstration of a microfabricated surface electrode ion trap](https://arxiv.org/abs/1008.0990) — microfabrication and experimental demonstration.
- [Cryogenic surface ion trap based on intrinsic silicon](https://doi.org/10.1088/1367-2630/16/11/113068) — different substrate, temperatures and electrode construction.
- [Fabrication and heating rate study of microscopic surface electrode ion traps](https://arxiv.org/abs/1009.2834) — gold-on-sapphire experimental background.
- [Ion trap with gold-plated alumina: substrate and surface characterization](https://arxiv.org/abs/2207.06878) — related materials and substrate characterization.
- [Surface-electrode ion trap design for near-field microwave quantum gates](https://doi.org/10.1007/s00340-023-08030-x) — sapphire substrate and microwave-driven design; not evidence that silica has identical properties.
- [Design of a surface electrode trap for parallel ion strings](https://doi.org/10.1088/0953-4075/47/3/035301) — plated-gold/alumina construction.
- [A microfabricated ion trap chip with a sloped loading slot to minimize exposing trapped ions to stray charges](https://doi.org/10.1088/2058-9565/ac107d) — gold-coated aluminum and dielectric-exposure considerations.
- [Scallop smoothing process for uniform gold coating on DRIE-etched surfaces in ion-trap chips](https://doi.org/10.1186/s40486-025-00248-y) — fabrication details for a different multilayer process.
- [Test and Characterization of Multilayer Ion Traps on Fused Silica](https://doi.org/10.1002/qute.202500412) — fused-silica multilayer trap background.
- [TSV-integrated Surface Electrode Ion Trap for Scalable Quantum Information Processing](https://arxiv.org/abs/2101.00869) — integrated interconnect fabrication.
- [Fabrication of Surface Ion Traps with Integrated Current Carrying Wires enabling High Magnetic Field Gradients](https://arxiv.org/abs/2202.02313) — integrated copper wires; these are not identical to replacing exposed RF rails.
- [Large-Scale Fabrication of Surface Ion Traps on a 300 mm Glass Wafer](https://doi.org/10.1002/pssb.202000589) — journal publication related to the Cu/Au glass-wafer work used above.
- [3D integration of CMOS-compatible surface electrode ion trap and silicon photonics for scalable quantum computing](https://doi.org/10.1109/ECTC.2019.00266) — related Cu/Au fabrication conference work.
- [Reduction of heating rate in a microfabricated ion trap by pulsed-laser cleaning](https://doi.org/10.1088/1367-2630/13/12/123023) — aluminum alloy surfaces and cleaning, cited in the earlier material discussion.
- [Monolithic segmented three-dimensional ion trap for quantum technology applications](https://doi.org/10.1103/srq8-cgnt) — discovery concerning a different 3D architecture; not compared numerically here.

### Fabrication, theses, institutional and commercial resources

- [Leibniz University Hannover, Surface-Electrode Trap Fabrication](https://www.iqo.uni-hannover.de/en/arbeitsgruppen/trapped-ion-quantum-engineering/research-projects/surface-electrode-trap-fabrication) — institutional description of thick plated gold, narrow gaps and adhesion/seed layers.
- [Engineered microwave control for trapped ions, thesis](https://edocs.tib.eu/files/e01dh16/863830021.pdf) — electrode-thickness and dielectric-shielding background.
- [ECTI 2010 booklet, including NPL fabrication poster](https://www.sussex.ac.uk/physics/iqt/ECTI/index_files/Booklet3.pdf) — gold-coated silica/silicon 3D fabrication; different from our planar chip.
- [Oxford thesis, Benchmarking](https://ora.ox.ac.uk/objects/uuid%3A3fdb0b98-3c50-483c-b66e-132495ce71af/files/dwm117p323) — search excerpt on approximately 5 µm Au on 0.5 mm sapphire.
- [Oxford thesis, A high-fidelity microwave driven…](https://ora.ox.ac.uk/objects/uuid%3A9cafcc3e-32c2-41dc-874d-632dcc402428/files/mcdf5a66054ae2e7960ce5f04d388fa1a) — related gold/sapphire apparatus description.
- [Joger thesis (2013)](https://www.quantenbit.physik.uni-mainz.de/files/2015/11/pub_dipl_Joger2013.pdf) — fused-silica trap fabrication background.
- [NIST-hosted trapped-ion review PDF](https://tf.nist.gov/general/pdf/2740.pdf) — search excerpt on materials, RF dissipation and thermal considerations.
- [Nanoscale interfacial structure for Novel Opto-electronic and Ion-trapping, dissertation](https://escholarship.org/content/qt6t85h2k4/qt6t85h2k4_noSplash_3387c11bbe936b4c73c8fbf145025d53.pdf) — materials and surface-cleanliness background.
- [neQxt commercial ion trap](https://www.neqxt.org/products/ion-trap/) — manufacturer example of coated fused silica in a different 3D design; not independent performance validation for this project.
- [Ion trap manufacturing methods, patent](https://patents.google.com/patent/EP4645178B1/en) and [Device for trapping an ion…, patent](https://patents.google.com/patent/WO2021006811A1/en) — process concepts, not experimental proof of this design.

### Electrical, diffusion and thin-film resources discovered

- [Effects of barrier composition and electroplating chemistry on adhesion and voiding in copper/dielectric diffusion barrier films, NIST](https://www.nist.gov/publications/effects-barrier-composition-and-electroplating-chemistry-adhesion-and-voiding) — process-dependent interfaces.
- [Properties of electroplated copper thin film and its interfacial reactions](https://www.sciencedirect.com/science/article/pii/S0921510700005444) — film properties and diffusion barriers in a different stack.
- [Use of WNx as diffusion barrier for copper](https://ir.lib.nycu.edu.tw/bitstream/11536/27384/1/000187081900046.pdf) — barrier research, not a selected trap recipe.
- [Electroplated products and electroplating bath, patent](https://data.epo.org/publication-server/rest/v1.2/patents/EP3540097NWA1/document.html) — diffusion-related discovery; not used for the recommended stack.
- [The Influence of the Skin Phenomenon on the Impedance of Thin Conductive Layers](https://www.mdpi.com/2079-9292/12/23/4834) — finite-thickness impedance research.
- [Electromagnetic Characterisation of Materials by Using Transmission/Reflection Devices](https://www.mdpi.com/2079-9292/6/4/95) — sheet-impedance treatment background.
- [Thin Ohmic or superconducting strip with an applied ac electric current](https://arxiv.org/abs/cond-mat/0603416) — strip-current crowding and impedance background.
- [Study of the anomalous skin effect of normal conducting film](https://arxiv.org/abs/2004.11462) — regime-dependent skin effects; not used in the room-temperature estimate.
- [Skin Effect, textbook chapter](https://doi.org/10.1007/978-3-031-14186-7_10) and [US Particle Accelerator School surface-resistance notes](https://uspas.fnal.gov/materials/04UW/SNS_Front-End.ppt.pdf) — supporting skin-effect background; MIT text was the primary explanatory reference used.
- [High-precision reflectometer for submillimeter wavelengths](https://opg.optica.org/josab/abstract.cfm?uri=josab-12-2-212) — resistivity table discovery; not a low-frequency trap model.
- [Research Measurements material data](https://researchmeasurements.com/298-2/) — compilation found during conductivity search; final numbers instead use Matula's primary reference.

### Secondary mirrors and search-only discoveries

The following helped discover papers or appeared in search results but were not used as primary technical evidence:

- [Academia mirror of Nizamani & Hensinger](https://www.academia.edu/89968282/Optimum_electrode_configurations_for_fast_ion_separation_in_microfabricated_surface_ion_traps).
- [ResearchGate figure from Nizamani & Hensinger](https://www.researchgate.net/figure/The-planar-trap-designs-a-with-outer-segmented-static-electrodes-and-rf-electrodes_fig2_45930360).
- [Academia mirror of Allcock et al.](https://www.academia.edu/4921263/Implementation_of_a_symmetric_surface_electrode_ion_trap_with_field_compensation_using_a_modulated_Raman_effect).
- [ArxivLens mirror of the Cu/Au glass-wafer paper](https://arxivlens.com/paperview/viewpdf/functional-surface-ion-traps-on-a-12-inch-glass-wafer-for-quantum-applications-9014-2108931).
- [AlphaXiv mirror of Schmied](https://www.alphaxiv.org/abs/0910.4517), [MaRDI record](https://portal.mardi4nfdi.de/wiki/Electrostatics_of_gapped_and_finite_surface_electrodes), and [University of Basel PDF mirror](https://atom.physik.unibas.ch/fileadmin/user_upload/atom_physik/People/Roman_Schmid/SurfacePattern/1_Schmied2010a.pdf). The Basel PDF timed out on opening.
- [EurekaMag record of the integration conference paper](https://eurekamag.com/research/103/246/103246508.php).
- [SciRate records for related fabrication work](https://scirate.com/search?q=au%3AHenner_T+in%3Aphysics).
- [Wikipedia resistivity table](https://en.wikipedia.org/wiki/Electrical_resistivity_and_conductivity), [element resistivity data](https://en.wikipedia.org/wiki/Electrical_resistivities_of_the_elements_%28data_page%29), [gold](https://en.wikipedia.org/wiki/Gold), [gold plating](https://en.wikipedia.org/wiki/Gold_plating), and [skin effect](https://en.wikipedia.org/wiki/Skin_effect). Not used as primary inputs.
- [Physics Factbook gold resistivity](https://hypertextbook.com/facts/2004/JennelleBaptiste.shtml), [Refmanual resistivity table](https://refmanual.com/charts/electrical/resistivity/), [Distymap resistivity compilation](https://distymap.com/tools/resistivity-metals), and [LibreTexts resistance explanation](https://eng.libretexts.org/Bookshelves/Electrical_Engineering/Electronics/DC_Electrical_Circuit_Analysis_-_A_Practical_Approach_%28Fiore%29/02%3A_Basic_Quantities/2.07%3A_Resistance_and_Conductance) — discovery/background, superseded by primary reference inputs.

Searches also returned unrelated or unsuitable material: decorative gold/silica laser structuring, nanoscale electrode gaps, semiconductor thin-film measurements, Casimir effects, generic conductivity calculators, student tables, and an unverified Reddit trap-design post. These did not contribute to the answer. They are recorded here as excluded search noise rather than scientific resources supporting the recommendation.

## Project evidence and reproduction

| File | Role |
|---|---|
| `starter_file_given.ipynb` | Original geometry, constraints, solver and score |
| `Traped ion working file.ipynb` | Existing exploration and saved 150.543 meV output |
| `../running_bib.txt` | Original three-entry project bibliography |
| `optimize_trap.py` | Reproducible analytic geometry search and checks |
| `trap_optimization_results.json` | Saved analytic results |
| `sweep_thickness.py` | Six-case finite-gap cloud screen |
| `thickness_screen_results.json` | Saved finite-gap/scaled results |
| `recommended_thickness_candidate.json` | Chosen thickness candidate and operating point |
| `compare_rf_materials.py` | Sheet-resistance and skin-depth estimates and checks |
| `rf_material_comparison.json` | Saved material calculation results |

Run the following from the repository root:

```powershell
.venv/Scripts/python.exe hard_haq_working_dir/optimize_trap.py
.venv/Scripts/python.exe hard_haq_working_dir/compare_rf_materials.py
```

The thickness script invokes cloud solves and may consume credits if the results are not cached:

```powershell
.venv/Scripts/python.exe hard_haq_working_dir/sweep_thickness.py
```

The original notebooks were preserved. No finite-conductivity cloud material comparison, thermal qualification, physical fabrication or experimental trap-depth measurement was performed in this investigation.
'''

parts = [intro]
for title, name in [
    ('Analysis 1: geometry, stability and symmetry', 'trap_optimization_research.md'),
    ('Analysis 2: physical thicknesses and finite-gap simulation', 'thickness_research.md'),
    ('Analysis 3: RF electrode material comparison', 'rf_material_research.md'),
]:
    content = (ROOT/name).read_text(encoding='utf-8').split('\n', 1)[1]
    # Nest the source report headings under its section in this final document.
    content = '\n'.join('#'+line if line.startswith('#') else line for line in content.splitlines())
    parts.append(f'\n## {title}\n'+content+'\n')
parts.append(additional)
out = ROOT/'FINAL_ION_TRAP_RESEARCH_REPORT.md'
out.write_text('\n'.join(parts), encoding='utf-8')
print(f'Created {out.name}: {len(out.read_text(encoding="utf-8").split())} words')
