# Physical thickness choices for the surface ion trap

## Scope and fabrication constraints

Treat `metal_thickness` and `substrate_thickness` as independent physical dimensions, not as free scale factors in the gapless optimizer. For an initial fabrication-aware screen, use 2–10 µm electroplated gold and 300–500 µm fused silica. These are engineering screening bounds, not a claim that every point has been experimentally qualified. Keep 500 µm silica as the default mechanical choice unless a resolved numerical improvement justifies thinning. A 300 µm wafer is a candidate requiring a wafer supplier and mounting/process review; 500 µm has direct precedent below.

Electroplated 5 µm gold on 500 µm fused silica is a reasonable initial candidate. A 10 µm electrode with a 5 µm finished gap has a thickness/gap ratio of 2; use a patterned plating mold and qualify lateral overgrowth, sidewall shape, adhesion and residual stress. The finished minimum gap, not just the mask gap, must remain at least 5 µm. This is more demanding than the 5 µm metal candidate and is not automatically preferable.

Thicker gold can reduce conductor resistance and shield exposed gap dielectric, but increases sidewall capacitance and changes fields. Lower resistance does not appear as a benefit in the PEC model. Substrate thickness affects the dielectric interfaces and capacitance; it does not independently change the ion height as an electrode-spacing parameter would. Backside ground metallization or a nearby metal mount would change the boundary conditions and must be modeled for the actual package. No such backside ground is assumed in this screen.

## Sources and what they establish

- [Chiaverini et al., Surface-electrode architecture for ion-trap quantum information processing (2005), §6 and figure 7](https://tf.nist.gov/general/pdf/2019.pdf): a gold-on-fused-silica five-wire chip with a 500 µm substrate. This is direct support for retaining the original wafer thickness.
- [Britton, Microfabrication techniques for trapped ion quantum information processing (2008), discussion near figure 2.16](https://www.nist.gov/system/files/documents/2017/05/09/Joe-Britton.pdf): reports a fused-quartz surface trap with 6 µm electroplated gold and 8 µm gaps, with reduced exposure to dielectric charging as a motivation. This supports several-micrometre plated gold; it does not qualify our 5 µm gap at all thicknesses.
- [McCormick, Control and measurement of a single-ion quantum harmonic oscillator, §4.1.1](https://www.nist.gov/document/katherine-mccormick-phd-thesis): documents 8 µm electroplated gold on crystalline quartz with 5 µm electrode gaps. This supports feasibility of thick gold and narrow gaps in a related material system. Crystalline quartz is not fused silica, so this is not a dielectric-material substitution in our model.
- [Schmied, Electrostatics of gapped and finite surface electrodes (2010)](https://doi.org/10.1088/1367-2630/12/2/023038): explicitly studies finite electrode thickness and dielectric effects; an illustrative ring trap showed modest secular-frequency corrections. Its result is not a guaranteed error bound or direction of change for this five-wire trap.

The choice of 300 µm as a lower exploratory bound and the preference for a 5 µm gold starting point are engineering judgments informed by these precedents, not published optima for this exact layout. Physical operability also requires a qualified adhesion/seed stack, clean ultra-high-vacuum packaging, an RF resonator that supplies the required loaded voltage and thermal/breakdown checks. Our electrostatic/PEC depth calculation does not establish those properties.

## Numerical screen

`sweep_thickness.py` evaluates gold thicknesses 2, 5 and 10 µm on 300 and 500 µm silica, keeping the symmetric lateral candidate fixed at 200 µm RF width, 5 µm gap and 26.71361 µm center. This is a thickness comparison at one lateral geometry, not a joint global optimization. The center change remains outside the starter's original fixed-center rule, as discussed in the earlier report.

Unlike the starter, the simulation extends to z = -4000 µm for every wafer thickness. This puts air below the wafer and prevents changes in the numerical window size from being mistaken for thickness effects. The upper boundary remains at +4000 µm. Outer lateral grounds are as in the starter. Boundary and mesh convergence are still required for final selection.

All six fields are solved at 50 MHz and 100 V peak. For each, the RF frequency is rescaled to target q = 0.395, preserving a margin below 0.4; reported depth and secular frequency use the same quasi-static scaling. Ion height is measured from the **metal top surface**, z_ion - metal_thickness. The sampling grid extends beyond the saddle and the original 1 µm mesh and 3 µm parabola-fit method are retained for initial comparability. Solve again at the final drive and refine the mesh before claiming a precision optimum.

Results are written incrementally to `thickness_screen_results.json`. An initial run with the original lower boundary completed a field solve but stopped at console Unicode output; that result is excluded from this fixed-window comparison.

## Completed screening results

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
