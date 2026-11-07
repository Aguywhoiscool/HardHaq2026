"""Offline gapless-plane screening; finite-gap cloud validation is still required.

Run: .venv/Scripts/python.exe hard_haq_working_dir/optimize_trap.py
Widths and coordinates are micrometres, voltage is peak, frequency is Hz.
"""
import json
from pathlib import Path

import numpy as np
from numpy.polynomial import Polynomial as P
from scipy.constants import atomic_mass, elementary_charge as Q
from scipy.optimize import differential_evolution, minimize_scalar

M = 40 * atomic_mass


def geometry(left, right, gap, center=60.0):
    # Split each gap between its neighbouring electrodes, as in the starter.
    a, b, c = center + gap, left + gap, right + gap
    edges = np.array([-a / 2 - b, -a / 2, a / 2, a / 2 + c]) / 100
    signs = np.array([1, -1, 1, -1])
    denominator = P.fromroots(edges)
    numerator = P([0.0])
    for i, sign in enumerate(signs):
        numerator += sign * P.fromroots(np.delete(edges, i))
    nulls = [w for w in numerator.roots() if w.imag > 1e-7]
    if len(nulls) != 1:
        raise ValueError('Expected one upper-half-plane RF null')
    null = nulls[0]
    # |F|^2 stationary points away from the null satisfy F'(w)=0.
    stationary = numerator.deriv() * denominator - numerator * denominator.deriv()
    saddles = [w for w in stationary.trim(1e-10).roots() if w.imag > 1e-7]
    def field(w):
        return np.sum(signs / (w - edges)) / (np.pi * 100)  # per um
    saddle = min(saddles, key=lambda w: abs(field(w)) ** 2)
    gradient = abs(numerator.deriv()(null) / denominator(null)) / (np.pi * 100**2)
    return dict(height_um=float(null.imag * 100), null_y_um=float(null.real * 100),
                saddle_y_um=float(saddle.real * 100), saddle_height_um=float(saddle.imag * 100),
                gradient_per_um2=float(gradient), saddle_field2=float(abs(field(saddle))**2))


def metrics(left, right, gap, center=60.0, voltage=100.0, q_limit=0.4):
    g = geometry(left, right, gap, center)
    # q = 2 Q V G / (m Omega^2); best drive is the lowest permitted by q.
    omega = max(2 * np.pi * 10e6, np.sqrt(2 * Q * voltage * g['gradient_per_um2'] * 1e12 / (M * q_limit)))
    secular = Q * voltage * g['gradient_per_um2'] * 1e12 / (np.sqrt(2) * M * omega)
    q = 2 * np.sqrt(2) * secular / omega
    depth = Q * voltage**2 * g['saddle_field2'] * 1e12 / (4 * M * omega**2) * 1e3
    checks = dict(height=50 <= g['height_um'] <= 100, secular=secular / (2*np.pi) >= 1e6,
                  mathieu=q <= q_limit + 1e-12, drive=10e6 <= omega/(2*np.pi) <= 60e6,
                  voltage=10 <= voltage <= 100, features=min(center, left, right, gap) >= 5,
                  widths=20 <= left <= 200 and 20 <= right <= 200, gap=5 <= gap <= 20)
    return dict(left_width_um=float(left), right_width_um=float(right), gap_um=float(gap),
                center_width_um=float(center), voltage_V=voltage, frequency_Hz=float(omega/(2*np.pi)),
                secular_Hz=float(secular/(2*np.pi)), q=float(q), depth_meV=float(depth),
                checks={key: bool(value) for key, value in checks.items()}, **g)


def optimize(asymmetric=False, free_center=False, seed=7, q_limit=0.4):
    bounds = [(20, 200)] * (2 if asymmetric else 1) + [(5, 20)]
    if free_center:
        bounds += [(5, 200)]  # exploratory; the starter does not permit this change
    def unpack(x):
        left, right = (x[0], x[1]) if asymmetric else (x[0], x[0])
        return left, right, x[2 if asymmetric else 1], x[-1] if free_center else 60
    def objective(x):
        r = metrics(*unpack(x), q_limit=q_limit)
        if not all(r['checks'].values()):
            return 1e4 + abs(r['height_um'] - np.clip(r['height_um'], 50, 100))
        return -r['depth_meV']
    result = differential_evolution(objective, bounds, seed=seed, tol=1e-9, popsize=12)
    return metrics(*unpack(result.x), q_limit=q_limit)


def verify():
    # Independent closed-form symmetric null, field gradient and vertical saddle.
    for width, gap, center in [(120, 10, 60), (200, 5, 44.348), (80, 20, 60)]:
        r = geometry(width, width, gap, center)
        a, b = (center + gap)/2, (center + gap)/2 + width + gap
        h = np.sqrt(a*b)
        # d[(t-ab)/((t+a^2)(t+b^2))]/dt = 0, with t=z^2.
        saddle2 = a*b + np.sqrt(a*b)*(a+b)
        assert np.isclose(r['height_um'], h)
        assert np.isclose(r['saddle_height_um'], np.sqrt(saddle2))
        expected_gradient = 4*(b-a)/(np.pi*np.sqrt(a*b)*(a+b)**2)
        assert np.isclose(r['gradient_per_um2'], expected_gradient)
        assert abs(r['null_y_um']) < 1e-7
    r1, r2 = metrics(100, 160, 10), metrics(160, 100, 10)
    assert np.isclose(r1['depth_meV'], r2['depth_meV'])
    assert np.isclose(r1['null_y_um'], -r2['null_y_um'])


if __name__ == '__main__':
    verify()
    results = {}
    for name, asym, free in [('starter_symmetric', False, False), ('starter_asymmetric', True, False),
                              ('exploratory_symmetric', False, True), ('exploratory_asymmetric', True, True)]:
        results[name] = optimize(asym, free)
    results['starter_symmetric_margin'] = optimize(q_limit=0.395)
    results['notebook_geometry_prediction'] = metrics(200, 200, 5, 44.348)
    center_fit = minimize_scalar(lambda c: -metrics(200, 200, 5, c)['depth_meV'],
                                 bounds=(15, 60), method='bounded')
    results['exploratory_canonical'] = metrics(200, 200, 5, center_fit.x)
    results['asymmetric_2_to_1_example'] = metrics(200, 100, 5)
    output = Path(__file__).with_name('trap_optimization_results.json')
    output.write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    for name, r in results.items():
        print(name, {k: round(r[k], 6) for k in ['left_width_um','right_width_um','gap_um','center_width_um','height_um','frequency_Hz','q','depth_meV']})
