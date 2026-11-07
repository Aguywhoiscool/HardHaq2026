# Final notebook recheck

Notebook: `Ion trap - decisions and justification.ipynb`.

## Current saved operating point

| Item | Value |
|---|---:|
| RF width, each rail | 200 µm |
| Gap | 5 µm |
| Center | 26.71361 µm |
| Metal / silica thickness | 5.0 / 500.0 µm |
| RF voltage | 100 V peak |
| RF frequency | 49.82812 MHz |
| Saved depth | 153.643 meV |
| Saved height above metal | 58.000 µm |
| Saved lateral / vertical secular frequency | 6.99 / 7.05 MHz |
| Saved Mathieu q | 0.39999986 |

## Findings

1. The code parses, and execution counts run sequentially from 1 through 9. This supports a coherent saved execution record, but is not independent confirmation that every output was generated from the current source.
2. The pseudopotential uses peak RF amplitude and angular drive frequency with the expected factor 1/4. Squared V/µm fields are converted by 10^12, energies by e and 10^3 to meV, and fitted J/µm² curvatures by 10^12 to SI. These unit conversions are consistent.
3. The Mathieu calculation uses the larger radial frequency and the confinement check uses the smaller. The saved q and drive imply a maximum secular frequency of 7.046758 MHz, consistent with the printed 7.05 MHz.
4. The saved score prints all five checks as passing. The RF width, gap and frequency also fall inside the starter parameter ranges. The center and metal thickness differ from the starter's fixed dimensions, so the result is valid only for the expanded design scope.
5. The claimed 151.75 meV earlier recommendation is superseded as the latest saved notebook result by 153.643 meV. It remains a separate q=0.395, fixed-domain screen and must not be treated as the same run.
6. The gapless analytic verification passes independently for symmetric null height, saddle, gradient and reflection of unequal rails. A separate scalar optimization reproduces the ideal effective ratio near 6.4641016 and a symmetric gapless depth of 153.146915 meV at 100 V and q=0.4. The finite-gap saved result is about 0.32% higher; an ideal-model optimum is not an upper bound for a different electrode model.

## Numerical margin

The reported q is below 0.4 by 0.000000140, only 0.0000350% of the limit. Electrostatic scaling places the boundary at 49.828111280 MHz, about 8.72 Hz below the current drive. That margin is much smaller than the numerical uncertainty established so far; tuning more decimal places does not establish a more reliable physical optimum.

At unchanged field geometry and voltage, retuning to q=0.395 predicts approximately **50.142487 MHz** and **151.723 meV**. These are scaling estimates, not new cloud results. The notebook input was not changed to this margin setting.

## Remaining limits of the calculation

- The ion and escape barrier are found on the symmetry axis. This is appropriate for the selected symmetric RF layout, but not a complete 2D/3D barrier search with added DC fields or asymmetric geometry.
- A 0.5 µm sampling grid and a ±3 µm parabola fit sit on fields from the current 1 µm mesh. Convergence of height, fitted q and barrier has not been demonstrated, and q near 0.4 is particularly sensitive to small errors.
- The current window reaches the physical substrate bottom; the thickness-screen script instead includes air below the wafer. These boundary conventions must be held fixed in a controlled comparison.
- PEC omits conductor losses, and axial DC confinement and practical packaging are absent. No material-dependent depth improvement or fabricated-device performance is established.
- This audit did not submit cloud solves or independently reconstruct the latest fields from solver data; it reviewed stored source and outputs and ran offline analytic checks.

## Markdown corrections applied

Updated the stale summary height, secular frequencies and q; synchronized the operating frequency in the justification table; labeled the 49.4 MHz / 151.622 meV record as historical; updated the voltage-normalized score; and corrected the 153.642/153.643 rounding mismatch. All executable cells, outputs, execution counts and attachments were preserved. A pre-edit backup was saved at `notebook_backups\Ion trap decisions.before_recheck_20261106_220621.ipynb`.

## References

- [Nizamani and Hensinger, geometry-factor and electrode-ratio analysis](https://arxiv.org/pdf/1007.3542).
- `starter_file_given.ipynb`: reference pseudopotential, field reconstruction, curvature fits and scoring.
- `optimize_trap.py`: independent gapless field checks and constrained geometry model.
- `thickness_screen_results.json`: separate fixed-window screen at q=0.395.
