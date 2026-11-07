# Gold versus gold-coated copper for the RF rails

## Finding and recommended next candidate

Gold-coated copper is a credible alternative for reducing conductor losses. Keep the existing 5 µm gold candidate as the reference. For a comparison with unchanged external geometry, screen nominal 4.8 µm Cu + 0.2 µm Au, or 4.5 µm Cu + 0.5 µm Au, on the same 500 µm fused-silica substrate. These are proposed comparison stacks, not qualified fabrication recipes. Adhesion, seed and any diffusion-barrier layers must fit within the chosen total electrode envelope or be included explicitly in the field geometry. Only the RF rails need change for this comparison; keep the grounds and their boundaries consistent.

There is no established depth gain from replacing gold at a fixed actual electrode voltage of 100 V peak. The benefit is potentially less power required to hold that voltage. A better conductor could recover voltage lost in a real feed network, but depth or stability improvements cannot be inferred from conductivity alone.

## Direct experimental precedent

[Tao et al., Functional surface ion traps on a 12-inch glass wafer for quantum applications](https://arxiv.org/pdf/2002.11470), pp. 1–3, describes a symmetric five-wire trap with 5 µm gaps, approximately 3 µm electroplated Cu and 0.2 µm protective Au over a Ti/Cu seed. Their packaged trap operated at 32.7 MHz and was baked at 130 °C for a week. This supports feasibility of a Cu/Au surface-electrode process, not automatic qualification of our proposed stack on fused silica. Their substrate was Corning SWG 8.5 glass, not our fused silica. They identify Au overhangs during seed etching as a source of leakage/shorts and report imperfect micromotion-compensation stability. These process issues matter when adopting that approach.

## Quantitative screening at 50.141 MHz

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

## Consequences for power, depth and heating

At equal current, conductor power is I_rms² R. If the replaced rails account for a fraction eta of original total dissipated power, the approximate total reduction is eta × 23.5%, assuming the same drive frequency and voltage and unchanged other losses. Examples: eta = 0.1 gives 2.35% total power reduction; eta = 0.5 gives 11.7%. The complete resonator, bond wires, feeds, ground returns and dielectric loss are not specified in this repository's cross-section model, so no absolute power, loaded Q or temperature rise is established.

The existing RF-only screened depth of roughly 151.75 meV at 100 V and q = 0.395 is a PEC geometry result. Keep it as the reference, not a separately validated Cu/Au prediction. At the same external electrode shape, voltage and frequency, ideal electrostatic confinement is material-independent. At fixed source power instead of fixed electrode voltage, reduced loss may raise the voltage, but the 100 V cap and q constraint must still be enforced. The resonator must be retuned and both RF rails must have matching amplitude and phase; finite-conductivity feeds can alter those quantities.

Do not equate lower RF conductor heating with lower ion motional heating. [Chiaverini & Sage, Physical Review A 89, 012318 (2014)](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.89.012318) measured similar heating behavior for gold and niobium traps and linked it to non-material-specific surface contaminants. This is not a direct Cu/Au comparison; it shows why bulk conductivity is insufficient to predict motional noise.

## Surface and fabrication considerations

Prefer a continuous gold finish over intentionally exposed copper for this comparison. Keep the top surface and relevant sidewalls covered where the chosen fabrication process allows. [Wang et al., Laser-induced charging of microfabricated ion traps](https://arxiv.org/pdf/1108.0092) compared Au, Cu and Al at 6 K and found wavelength-dependent charging, with more charging on aluminum under their conditions. This supports investigating surface chemistry, not a universal charging guarantee for room-temperature Ca+ operation.

[Analytic procedure for the evaluation of copper intermetallic diffusion in electroplated gold coatings with energy dispersive X-ray microanalysis (2023)](https://www.sciencedirect.com/science/article/pii/S0003267023006499) examines diffusion through sub-micrometre Au coatings after 100–200 °C heat treatments. This makes the planned UHV bake and any barrier choice relevant. It does not prescribe a specific barrier for an ion trap. Qualify the stack against the actual bake cycle; do not add an unmodeled generic plating barrier and assume magnetic, RF and vacuum compatibility.

## Next validation steps

1. Fabricate or obtain representative Au and Cu/Au coupons and measure sheet resistance, total thickness, roughness, coating continuity, adhesion and post-bake changes. Maintain a finished gap of at least 5 µm.
2. Add measured conductor properties to a finite-conductivity RF model of both rails, actual lead lengths/tapers, bond wires, return paths, substrate dielectric loss and package. Resolve the thin Au layer or use a validated multilayer impedance treatment; an opaque thick-metal approximation alone is inappropriate for a film thinner than its skin depth.
3. Compare input power and rail amplitude/phase at the same 100 V electrode amplitude near 50 MHz. Verify loaded resonator Q and temperature rise experimentally, then recompute the pseudopotential if the RF boundary voltages or geometry differ.

No additional cloud mode solves were submitted for this material comparison: rerunning the existing PEC model with a changed material label would not answer the loss question. The research supports a Cu/Au prototype comparison, while solid gold remains the reference until the process and RF measurements establish an advantage.
