"""Finite-gap PhotonForge thickness screen using the starter's field extraction.

Submits up to six cloud mode solves. Results are screening estimates, not
fabrication qualification. Run from the repository root with the project venv.
"""
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

os.environ.setdefault('MPLBACKEND', 'Agg')
import numpy as np

HERE = Path(__file__).resolve().parent
CELLS = json.loads((HERE / 'starter_file_given.ipynb').read_text(encoding='utf-8'))['cells']


def evaluate(thickness, substrate):
    ns = {'__name__': '__thickness_screen__'}
    def cell(i):
        source = ''.join(CELLS[i]['source'])
        if i == 14:
            # Resolve the physical wafer bottom inside a fixed air domain.
            source = source.replace('limits=(-substrate_thickness, top_height)',
                                    'limits=(-4000.0, top_height)')
        exec(compile(source, f'starter_cell_{i}', 'exec'), ns)
    cell(4)
    cell(8)
    ns.update(rf_width=200.0, gap=5.0, center_width=26.71361,
              metal_thickness=float(thickness), substrate_thickness=float(substrate),
              v_rf=100.0, f_rf=50e6)
    cell(12)
    # Geometry cell also plots; Agg keeps the sweep noninteractive.
    cell(14)
    cell(16)
    cell(20)
    cell(24)
    cell(26)
    cell(27)
    q_target = 0.395
    ratio = np.sqrt(ns['q_mathieu'] / q_target)
    frequency = ns['f_rf'] * ratio
    depth = ns['trap_depth'] / ratio**2
    secular = ns['f_secular'] / ratio
    height = ns['ion_height']
    checks = dict(height=50 <= height <= 100, secular=secular >= 1e6,
                  drive=10e6 <= frequency <= 60e6, depth=depth > 0)
    ns['plt'].close('all')
    return dict(metal_thickness_um=thickness, substrate_thickness_um=substrate,
                rf_width_um=200.0, gap_um=5.0, center_width_um=26.71361,
                voltage_V=100.0, q_target=q_target,
                ion_height_um=float(height), retuned_frequency_Hz=float(frequency),
                retuned_secular_Hz=float(secular), retuned_depth_meV=float(depth),
                checks={k: bool(v) for k, v in checks.items()},
                note='Frequency retuned using electrostatic scaling; solve at final frequency and refine mesh to confirm.')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    output = HERE / 'thickness_screen_results.json'
    results = []
    with ProcessPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(evaluate, metal, substrate): (metal, substrate)
                   for substrate in (500, 300) for metal in (2, 5, 10)}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            output.write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
            print(json.dumps(result), flush=True)
