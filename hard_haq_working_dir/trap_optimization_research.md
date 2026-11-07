# Trap depth optimization and symmetry comparison

## Recommendation

Keep equal-width RF rails for this depth objective. The offline constrained search converged to equal widths even when each rail was free to vary. Use the finite-gap PhotonForge calculation to validate the candidates below before claiming a new score.

| Case | RF widths (µm) | Gap (µm) | Center (µm) | Peak RF (V) | Drive (MHz) | Height (µm) | Secular (MHz) | q | Depth (meV) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Starter constraints, predicted optimum | 200 / 200 | 5 | 60 | 100 | 35.28477 | 87.856 | 4.990 | 0.400 | 144.290 |
| Starter constraints, stability margin | 200 / 200 | 5 | 60 | 100 | 35.50739 | 87.856 | 4.959 | 0.395 | 142.487 |
| Exploratory center change, predicted optimum | 200 / 200 | 5 | 26.71361 | 100 | 49.03802 | 59.178 | 6.935 | 0.400 | 153.147 |
| Example with unequal rails | 200 / 100 | 5 | 60 | 100 | 42.16278 | 73.889 | 5.963 | 0.400 | 134.202 |

All table values are gapless-plane predictions, not new PhotonForge results. The starter explicitly fixes the center at 60 µm and exposes only RF width, gap, voltage and frequency. Unequal rails and changing the center are exploratory extensions. Existing working-notebook outputs report 150.543 meV for 200 µm rails, 5 µm gap, 44.348 µm center, 100 V and 40.5823859 MHz. Preserve that result; it uses a different center from the starter. The offline model predicts 149.810 meV for that geometry at its own q-limited 40.46426 MHz. Agreement is about 0.5% in depth, but this is one comparison, not an error bound.

## Constraints and optimization

Enforced: RF widths 20–200 µm, common gap 5–20 µm, voltage 10–100 V peak, drive 10–60 MHz, ion height 50–100 µm, radial secular frequency at least 1 MHz, q at most 0.4 and minimum feature at least 5 µm. The exploratory center search uses 5–200 µm as an explicitly assumed range. Gold thickness, substrate and dielectric remain inputs of the original finite-gap model; the offline approximation does not resolve them.

Let G be the RF field-gradient magnitude per volt at the null, in m⁻². For this two-dimensional, equal-phase RF model:

    ω_sec = e V G / (sqrt(2) m Ω)
    q = 2 e V G / (m Ω²)
    Ω_best = max(2π × 10 MHz, sqrt(2 e V G / (m q_limit)))

Reject a geometry if the resulting drive exceeds 60 MHz or the secular minimum fails. At fixed geometry the maximum feasible voltage gives the greatest depth: in the q-limited regime depth scales linearly with V, and at the frequency floor it scales quadratically. All reported optima reach 100 V. The implementation checks the remaining constraints explicitly.

The 3.68 ratio in Nizamani and Hensinger is **RF width / RF separation**, at fixed height, voltage and frequency. It is not RF width / fabrication gap. Using the starter's gap-sharing approximation, these widths are b = rf_width + gap and a = center_width + gap. Optimizing frequency while enforcing q changes the objective, so imposing 3.68 is not justified here. The exploratory q-limited optimum has b/a about 6.464. Multiple overall scales attain the same optimum depth in the ideal model; the 26.71361 µm center is one convenient representative, not a unique geometry.

`optimize_trap.py` uses the exact two-strip gapless electric field. It solves for the RF null and all upper-half-plane nonzero stationary points of field magnitude using polynomial roots, and uses the lowest saddle barrier. It does not assume an on-axis saddle for unequal rails. The local field gradient gives the full isotropic radial pseudopotential curvature in this ideal 2D RF-only problem. Differential evolution searches geometry with a reproducible seed; a second seed independently reproduced the fixed-center symmetric and unrestricted-rail results. These numerical searches are evidence, not a global-optimality proof for real electrodes.

## What the research says

1. [Nizamani & Hensinger, Optimum electrode configurations for fast ion separation in microfabricated surface ion traps](https://arxiv.org/pdf/1007.3542), §2, equations 2–5 and figures 2–3: equal rails maximize the plotted fixed-height depth factor more strongly than the illustrated 2:1 rail case. Unequal widths can rotate the principal axes for laser cooling and shift the ion laterally. Their 3.68 optimum applies to a different fixed-parameter objective from the q-limited search here.
2. [Allcock et al., Implementation of a symmetric surface electrode ion trap with field compensation using a modulated Raman effect](https://arxiv.org/abs/0909.3272): a symmetric electrode pattern can also allow mode rotation and efficient cooling with a single beam parallel to the surface. Rail asymmetry is therefore not mandatory for cooling access; DC electrode design matters.
3. [Wesenberg, Electrostatics of surface-electrode ion traps](https://arxiv.org/abs/0808.1623): analytic gapless-plane methods characterize geometry, confinement and depth, and static control fields can substantially alter the depth. The RF-only objective here omits those DC contributions.

Interpretation: for this five-wire surface layout, choose symmetric rails when maximizing the stated RF depth score. Consider unequal rails when mode orientation or optical access is an explicit requirement, and compare both designs under the same electrical and geometric constraints. Do not assume asymmetry improves depth.

Terminology matters: some papers call *all* single-plane surface traps asymmetric compared with conventional three-dimensional traps whose electrodes surround the ion. That comparison is different from unequal versus equal RF rails on the same chip. The present search addresses the latter; its constraints do not define a fair comparison to a conventional 3D Paul trap.

## Finite-gap validation and safe retuning

Run the candidate geometry in the original solver. Reuse a solved field when changing only voltage. If the computed q is q₀ at f₀ and V₀, choose

    f_new = f₀ sqrt[(V_new / V₀) (q₀ / q_target)]

with q_target = 0.395 initially. Check the frequency bounds, both secular frequencies, ion height and depth again. In the electrostatic approximation, depth rescales by (V_new/V₀)²(f₀/f_new)² and secular frequency by (V_new/V₀)(f₀/f_new). A new solve verifies any frequency-dependent solver changes.

An unequal-rail PhotonForge model requires removing mirror symmetry, enough independent conductor modes to impose both RF voltages and the central ground voltage (normally three with connected outer grounds), and a 2D null/saddle search with Hessian eigenvalues. Merely changing one width in the current notebook produces an invalid comparison. Verify mesh and domain convergence, including extending the refined region beyond the saddle, for the final candidate. A real 3D trap also needs axial DC confinement, which can lower the radial escape barrier.

## Reproduce

From the repository root:

    .venv/Scripts/python.exe hard_haq_working_dir/optimize_trap.py

This runs offline, checks the symmetric closed-form null, saddle and gradient, checks reflection invariance for unequal rails, and saves `trap_optimization_results.json`. No cloud simulation was submitted for this analysis. The original notebooks and their saved results are unchanged.
