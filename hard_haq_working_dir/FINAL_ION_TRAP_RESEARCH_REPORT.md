# Final ion-trap optimization and materials research report

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



## Analysis 1: geometry, stability and symmetry

### Recommendation

Keep equal-width RF rails for this depth objective. The offline constrained search converged to equal widths even when each rail was free to vary. Use the finite-gap PhotonForge calculation to validate the candidates below before claiming a new score.

| Case | RF widths (µm) | Gap (µm) | Center (µm) | Peak RF (V) | Drive (MHz) | Height (µm) | Secular (MHz) | q | Depth (meV) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Starter constraints, predicted optimum | 200 / 200 | 5 | 60 | 100 | 35.28477 | 87.856 | 4.990 | 0.400 | 144.290 |
| Starter constraints, stability margin | 200 / 200 | 5 | 60 | 100 | 35.50739 | 87.856 | 4.959 | 0.395 | 142.487 |
| Exploratory center change, predicted optimum | 200 / 200 | 5 | 26.71361 | 100 | 49.03802 | 59.178 | 6.935 | 0.400 | 153.147 |
| Example with unequal rails | 200 / 100 | 5 | 60 | 100 | 42.16278 | 73.889 | 5.963 | 0.400 | 134.202 |

All table values are gapless-plane predictions, not new PhotonForge results. The starter explicitly fixes the center at 60 µm and exposes only RF width, gap, voltage and frequency. Unequal rails and changing the center are exploratory extensions. Existing working-notebook outputs report 150.543 meV for 200 µm rails, 5 µm gap, 44.348 µm center, 100 V and 40.5823859 MHz. Preserve that result; it uses a different center from the starter. The offline model predicts 149.810 meV for that geometry at its own q-limited 40.46426 MHz. Agreement is about 0.5% in depth, but this is one comparison, not an error bound.

### Constraints and optimization

Enforced: RF widths 20–200 µm, common gap 5–20 µm, voltage 10–100 V peak, drive 10–60 MHz, ion height 50–100 µm, radial secular frequency at least 1 MHz, q at most 0.4 and minimum feature at least 5 µm. The exploratory center search uses 5–200 µm as an explicitly assumed range. Gold thickness, substrate and dielectric remain inputs of the original finite-gap model; the offline approximation does not resolve them.

Let G be the RF field-gradient magnitude per volt at the null, in m⁻². For this two-dimensional, equal-phase RF model:

    ω_sec = e V G / (sqrt(2) m Ω)
    q = 2 e V G / (m Ω²)
    Ω_best = max(2π × 10 MHz, sqrt(2 e V G / (m q_limit)))

Reject a geometry if the resulting drive exceeds 60 MHz or the secular minimum fails. At fixed geometry the maximum feasible voltage gives the greatest depth: in the q-limited regime depth scales linearly with V, and at the frequency floor it scales quadratically. All reported optima reach 100 V. The implementation checks the remaining constraints explicitly.

The 3.68 ratio in Nizamani and Hensinger is **RF width / RF separation**, at fixed height, voltage and frequency. It is not RF width / fabrication gap. Using the starter's gap-sharing approximation, these widths are b = rf_width + gap and a = center_width + gap. Optimizing frequency while enforcing q changes the objective, so imposing 3.68 is not justified here. The exploratory q-limited optimum has b/a about 6.464. Multiple overall scales attain the same optimum depth in the ideal model; the 26.71361 µm center is one convenient representative, not a unique geometry.

`optimize_trap.py` uses the exact two-strip gapless electric field. It solves for the RF null and all upper-half-plane nonzero stationary points of field magnitude using polynomial roots, and uses the lowest saddle barrier. It does not assume an on-axis saddle for unequal rails. The local field gradient gives the full isotropic radial pseudopotential curvature in this ideal 2D RF-only problem. Differential evolution searches geometry with a reproducible seed; a second seed independently reproduced the fixed-center symmetric and unrestricted-rail results. These numerical searches are evidence, not a global-optimality proof for real electrodes.

### What the research says

1. [Nizamani & Hensinger, Optimum electrode configurations for fast ion separation in microfabricated surface ion traps](https://arxiv.org/pdf/1007.3542), §2, equations 2–5 and figures 2–3: equal rails maximize the plotted fixed-height depth factor more strongly than the illustrated 2:1 rail case. Unequal widths can rotate the principal axes for laser cooling and shift the ion laterally. Their 3.68 optimum applies to a different fixed-parameter objective from the q-limited search here.
2. [Allcock et al., Implementation of a symmetric surface electrode ion trap with field compensation using a modulated Raman effect](https://arxiv.org/abs/0909.3272): a symmetric electrode pattern can also allow mode rotation and efficient cooling with a single beam parallel to the surface. Rail asymmetry is therefore not mandatory for cooling access; DC electrode design matters.
3. [Wesenberg, Electrostatics of surface-electrode ion traps](https://arxiv.org/abs/0808.1623): analytic gapless-plane methods characterize geometry, confinement and depth, and static control fields can substantially alter the depth. The RF-only objective here omits those DC contributions.

Interpretation: for this five-wire surface layout, choose symmetric rails when maximizing the stated RF depth score. Consider unequal rails when mode orientation or optical access is an explicit requirement, and compare both designs under the same electrical and geometric constraints. Do not assume asymmetry improves depth.

Terminology matters: some papers call *all* single-plane surface traps asymmetric compared with conventional three-dimensional traps whose electrodes surround the ion. That comparison is different from unequal versus equal RF rails on the same chip. The present search addresses the latter; its constraints do not define a fair comparison to a conventional 3D Paul trap.

### Finite-gap validation and safe retuning

Run the candidate geometry in the original solver. Reuse a solved field when changing only voltage. If the computed q is q₀ at f₀ and V₀, choose

    f_new = f₀ sqrt[(V_new / V₀) (q₀ / q_target)]

with q_target = 0.395 initially. Check the frequency bounds, both secular frequencies, ion height and depth again. In the electrostatic approximation, depth rescales by (V_new/V₀)²(f₀/f_new)² and secular frequency by (V_new/V₀)(f₀/f_new). A new solve verifies any frequency-dependent solver changes.

An unequal-rail PhotonForge model requires removing mirror symmetry, enough independent conductor modes to impose both RF voltages and the central ground voltage (normally three with connected outer grounds), and a 2D null/saddle search with Hessian eigenvalues. Merely changing one width in the current notebook produces an invalid comparison. Verify mesh and domain convergence, including extending the refined region beyond the saddle, for the final candidate. A real 3D trap also needs axial DC confinement, which can lower the radial escape barrier.

### Reproduce

From the repository root:

    .venv/Scripts/python.exe hard_haq_working_dir/optimize_trap.py

This runs offline, checks the symmetric closed-form null, saddle and gradient, checks reflection invariance for unequal rails, and saves `trap_optimization_results.json`. No cloud simulation was submitted for this analysis. The original notebooks and their saved results are unchanged.


## Analysis 2: physical thicknesses and finite-gap simulation

### Scope and fabrication constraints

Treat `metal_thickness` and `substrate_thickness` as independent physical dimensions, not as free scale factors in the gapless optimizer. For an initial fabrication-aware screen, use 2–10 µm electroplated gold and 300–500 µm fused silica. These are engineering screening bounds, not a claim that every point has been experimentally qualified. Keep 500 µm silica as the default mechanical choice unless a resolved numerical improvement justifies thinning. A 300 µm wafer is a candidate requiring a wafer supplier and mounting/process review; 500 µm has direct precedent below.

Electroplated 5 µm gold on 500 µm fused silica is a reasonable initial candidate. A 10 µm electrode with a 5 µm finished gap has a thickness/gap ratio of 2; use a patterned plating mold and qualify lateral overgrowth, sidewall shape, adhesion and residual stress. The finished minimum gap, not just the mask gap, must remain at least 5 µm. This is more demanding than the 5 µm metal candidate and is not automatically preferable.

Thicker gold can reduce conductor resistance and shield exposed gap dielectric, but increases sidewall capacitance and changes fields. Lower resistance does not appear as a benefit in the PEC model. Substrate thickness affects the dielectric interfaces and capacitance; it does not independently change the ion height as an electrode-spacing parameter would. Backside ground metallization or a nearby metal mount would change the boundary conditions and must be modeled for the actual package. No such backside ground is assumed in this screen.

### Sources and what they establish

- [Chiaverini et al., Surface-electrode architecture for ion-trap quantum information processing (2005), §6 and figure 7](https://tf.nist.gov/general/pdf/2019.pdf): a gold-on-fused-silica five-wire chip with a 500 µm substrate. This is direct support for retaining the original wafer thickness.
- [Britton, Microfabrication techniques for trapped ion quantum information processing (2008), discussion near figure 2.16](https://www.nist.gov/system/files/documents/2017/05/09/Joe-Britton.pdf): reports a fused-quartz surface trap with 6 µm electroplated gold and 8 µm gaps, with reduced exposure to dielectric charging as a motivation. This supports several-micrometre plated gold; it does not qualify our 5 µm gap at all thicknesses.
- [McCormick, Control and measurement of a single-ion quantum harmonic oscillator, §4.1.1](https://www.nist.gov/document/katherine-mccormick-phd-thesis): documents 8 µm electroplated gold on crystalline quartz with 5 µm electrode gaps. This supports feasibility of thick gold and narrow gaps in a related material system. Crystalline quartz is not fused silica, so this is not a dielectric-material substitution in our model.
- [Schmied, Electrostatics of gapped and finite surface electrodes (2010)](https://doi.org/10.1088/1367-2630/12/2/023038): explicitly studies finite electrode thickness and dielectric effects; an illustrative ring trap showed modest secular-frequency corrections. Its result is not a guaranteed error bound or direction of change for this five-wire trap.

The choice of 300 µm as a lower exploratory bound and the preference for a 5 µm gold starting point are engineering judgments informed by these precedents, not published optima for this exact layout. Physical operability also requires a qualified adhesion/seed stack, clean ultra-high-vacuum packaging, an RF resonator that supplies the required loaded voltage and thermal/breakdown checks. Our electrostatic/PEC depth calculation does not establish those properties.

### Numerical screen

`sweep_thickness.py` evaluates gold thicknesses 2, 5 and 10 µm on 300 and 500 µm silica, keeping the symmetric lateral candidate fixed at 200 µm RF width, 5 µm gap and 26.71361 µm center. This is a thickness comparison at one lateral geometry, not a joint global optimization. The center change remains outside the starter's original fixed-center rule, as discussed in the earlier report.

Unlike the starter, the simulation extends to z = -4000 µm for every wafer thickness. This puts air below the wafer and prevents changes in the numerical window size from being mistaken for thickness effects. The upper boundary remains at +4000 µm. Outer lateral grounds are as in the starter. Boundary and mesh convergence are still required for final selection.

All six fields are solved at 50 MHz and 100 V peak. For each, the RF frequency is rescaled to target q = 0.395, preserving a margin below 0.4; reported depth and secular frequency use the same quasi-static scaling. Ion height is measured from the **metal top surface**, z_ion - metal_thickness. The sampling grid extends beyond the saddle and the original 1 µm mesh and 3 µm parabola-fit method are retained for initial comparability. Solve again at the final drive and refine the mesh before claiming a precision optimum.

Results are written incrementally to `thickness_screen_results.json`. An initial run with the original lower boundary completed a field solve but stopped at console Unicode output; that result is excluded from this fixed-window comparison.

### Completed screening results

All six cases pass the modeled height, secular-frequency and drive-frequency checks at the retuned q target of 0.395 and 100 V peak. Values below use the finite-gap solved fields and quasi-static drive retuning.

| Gold (um) | Silica (um) | Depth (meV) | Drive (MHz) | Height above metal (um) |
|---:|---:|---:|---:|---:|
| 2 | 500 | 150.1008 | 49.65387 | 59.0 |
| 5 | 500 | 151.7520 | 50.14137 | 58.0 |
| 10 | 500 | 151.4487 | 50.17628 | 58.0 |
| 2 | 300 | 150.1067 | 49.65320 | 59.0 |
| 5 | 300 | 151.7528 | 50.14127 | 58.0 |
| 10 | 300 | 151.4487 | 50.17629 | 58.0 |

Recommendation: use 5 um gold and retain the 500 um fused-silica wafer for the next prototype model. The 300 versus 500 um wafer effect is negligible in this screen and does not justify thinning for depth alone. The 5 um metal gives about 1.1% more depth than 2 um at the same q target; the 5 versus 10 um difference is only about 0.2%, so its ranking is not established beyond discretization error. This is the best of six screened thickness combinations, not a continuous or joint geometry optimum. Keep the 26.71361 um center and 200 um rails only if the previously relaxed center-width assumption applies. The drive starting value is 50.14137 MHz, radial secular minimum approximately 6.9446 MHz, and modeled height 58 um. Do not compare these q=0.395 depths directly with earlier q=0.4 optima as if the electrical operating points were identical.


## Analysis 3: RF electrode material comparison

### Finding and recommended next candidate

Gold-coated copper is a credible alternative for reducing conductor losses. Keep the existing 5 µm gold candidate as the reference. For a comparison with unchanged external geometry, screen nominal 4.8 µm Cu + 0.2 µm Au, or 4.5 µm Cu + 0.5 µm Au, on the same 500 µm fused-silica substrate. These are proposed comparison stacks, not qualified fabrication recipes. Adhesion, seed and any diffusion-barrier layers must fit within the chosen total electrode envelope or be included explicitly in the field geometry. Only the RF rails need change for this comparison; keep the grounds and their boundaries consistent.

There is no established depth gain from replacing gold at a fixed actual electrode voltage of 100 V peak. The benefit is potentially less power required to hold that voltage. A better conductor could recover voltage lost in a real feed network, but depth or stability improvements cannot be inferred from conductivity alone.

### Direct experimental precedent

[Tao et al., Functional surface ion traps on a 12-inch glass wafer for quantum applications](https://arxiv.org/pdf/2002.11470), pp. 1–3, describes a symmetric five-wire trap with 5 µm gaps, approximately 3 µm electroplated Cu and 0.2 µm protective Au over a Ti/Cu seed. Their packaged trap operated at 32.7 MHz and was baked at 130 °C for a week. This supports feasibility of a Cu/Au surface-electrode process, not automatic qualification of our proposed stack on fused silica. Their substrate was Corning SWG 8.5 glass, not our fused silica. They identify Au overhangs during seed etching as a source of leakage/shorts and report imperfect micromotion-compensation stability. These process issues matter when adopting that approach.

### Quantitative screening at 50.141 MHz

Bulk resistivity inputs at 293 K come from [R. A. Matula, Electrical resistivity of copper, gold, palladium, and silver, Journal of Physical and Chemical Reference Data 8, 1147 (1979), NIST-hosted tables](https://srd.nist.gov/JPCRD/jpcrd155.pdf): Cu 1.678 × 10⁻⁸ Ω m and Au 2.214 × 10⁻⁸ Ω m. These are high-purity annealed bulk reference values, not measured electroplated-film properties. They can differ from handbook values for other material conditions.

For approximately uniform in-plane current, sheet conductance is the sum of each layer's thickness divided by its resistivity:

    R_sheet = 1 / sum(t_i / rho_i)
    R_per_length = R_sheet / rail_width
    skin_depth = sqrt(rho / (pi f mu0))

The [MIT electromagnetic fields text, §14.9](https://web.mit.edu/6.013_book/www/chapter14/14.9.html) explains skin-depth-limited conduction and transmission-line loss. Calculated skin depths here are 10.58 µm for Au and 9.21 µm for Cu. A 5 µm electrode is thinner than either depth, so a uniform-current sheet model is a useful first estimate, but not an exact RF strip-resistance model. Current crowding at lateral edges, proximity to grounds and the return geometry can still raise resistance. A 0.2 µm gold finish is much thinner than its skin depth, so it does not confine all the RF current to gold.

| Equal total thickness | Estimated sheet resistance (mΩ/square) | Estimated resistance per mm for 200 µm rail (Ω/mm) | Change from gold |
|---|---:|---:|---:|
| 5 µm Au | 4.428 | 0.02214 | baseline |
| 4.8 µm Cu + 0.2 µm Au | 3.389 | 0.01694 | −23.5% |
| 4.5 µm Cu + 0.5 µm Au | 3.439 | 0.01720 | −22.3% |

These are calculated estimates, not cloud finite-conductivity simulations. The current PEC calculation contains no material loss and cannot validate them. `compare_rf_materials.py` reproduces the values, checks the sheet-conductance calculation and saves `rf_material_comparison.json`.

Film quality can erase the gain: a sensitivity case with Cu resistivity 1.5 times the bulk reference and Au unchanged makes the 4.8/0.2 stack about 13.1% more resistive than the reference gold. This multiplier is hypothetical, not a measured result. Measure sheet resistance on process coupons before trusting the bulk comparison.

### Consequences for power, depth and heating

At equal current, conductor power is I_rms² R. If the replaced rails account for a fraction eta of original total dissipated power, the approximate total reduction is eta × 23.5%, assuming the same drive frequency and voltage and unchanged other losses. Examples: eta = 0.1 gives 2.35% total power reduction; eta = 0.5 gives 11.7%. The complete resonator, bond wires, feeds, ground returns and dielectric loss are not specified in this repository's cross-section model, so no absolute power, loaded Q or temperature rise is established.

The existing RF-only screened depth of roughly 151.75 meV at 100 V and q = 0.395 is a PEC geometry result. Keep it as the reference, not a separately validated Cu/Au prediction. At the same external electrode shape, voltage and frequency, ideal electrostatic confinement is material-independent. At fixed source power instead of fixed electrode voltage, reduced loss may raise the voltage, but the 100 V cap and q constraint must still be enforced. The resonator must be retuned and both RF rails must have matching amplitude and phase; finite-conductivity feeds can alter those quantities.

Do not equate lower RF conductor heating with lower ion motional heating. [Chiaverini & Sage, Physical Review A 89, 012318 (2014)](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.89.012318) measured similar heating behavior for gold and niobium traps and linked it to non-material-specific surface contaminants. This is not a direct Cu/Au comparison; it shows why bulk conductivity is insufficient to predict motional noise.

### Surface and fabrication considerations

Prefer a continuous gold finish over intentionally exposed copper for this comparison. Keep the top surface and relevant sidewalls covered where the chosen fabrication process allows. [Wang et al., Laser-induced charging of microfabricated ion traps](https://arxiv.org/pdf/1108.0092) compared Au, Cu and Al at 6 K and found wavelength-dependent charging, with more charging on aluminum under their conditions. This supports investigating surface chemistry, not a universal charging guarantee for room-temperature Ca+ operation.

[Analytic procedure for the evaluation of copper intermetallic diffusion in electroplated gold coatings with energy dispersive X-ray microanalysis (2023)](https://www.sciencedirect.com/science/article/pii/S0003267023006499) examines diffusion through sub-micrometre Au coatings after 100–200 °C heat treatments. This makes the planned UHV bake and any barrier choice relevant. It does not prescribe a specific barrier for an ion trap. Qualify the stack against the actual bake cycle; do not add an unmodeled generic plating barrier and assume magnetic, RF and vacuum compatibility.

### Next validation steps

1. Fabricate or obtain representative Au and Cu/Au coupons and measure sheet resistance, total thickness, roughness, coating continuity, adhesion and post-bake changes. Maintain a finished gap of at least 5 µm.
2. Add measured conductor properties to a finite-conductivity RF model of both rails, actual lead lengths/tapers, bond wires, return paths, substrate dielectric loss and package. Resolve the thin Au layer or use a validated multilayer impedance treatment; an opaque thick-metal approximation alone is inappropriate for a film thinner than its skin depth.
3. Compare input power and rail amplitude/phase at the same 100 V electrode amplitude near 50 MHz. Verify loaded resonator Q and temperature rise experimentally, then recompute the pseudopotential if the RF boundary voltages or geometry differ.

No additional cloud mode solves were submitted for this material comparison: rerunning the existing PEC model with a changed material label would not answer the loss question. The research supports a Cu/Au prototype comparison, while solid gold remains the reference until the process and RF measurements establish an advantage.


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
