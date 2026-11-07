"""Room-temperature material screening, not a finite-conductivity trap solve.

Uses Matula bulk resistivities at 293 K. Thin-film sheet conductance assumes
uniform tangential E across layers; skin depths report its range of validity.
Actual AC resistance needs current crowding, leads and measured film properties.
"""
import json
from pathlib import Path
from math import pi, sqrt

RHO_AU = 2.214e-8  # ohm m, Matula/NIST, 293 K
RHO_CU = 1.678e-8
MU0 = 4e-7 * pi
HERE = Path(__file__).resolve().parent


def sheet_resistance(layers):
    """Parallel in-plane conductance; layers are (thickness_m, resistivity)."""
    return 1 / sum(t / rho for t, rho in layers)


def compare(frequency=50.141371901853874e6):
    baseline = sheet_resistance([(5e-6, RHO_AU)])
    cases = {
        '5um_Au': [(5e-6, RHO_AU)],
        '4.8um_Cu_0.2um_Au': [(4.8e-6, RHO_CU), (0.2e-6, RHO_AU)],
        '4.5um_Cu_0.5um_Au': [(4.5e-6, RHO_CU), (0.5e-6, RHO_AU)],
        # Sensitivity, not a measured process result.
        '4.8um_Cu_0.2um_Au_Cu_resistivity_x1.5': [(4.8e-6, 1.5*RHO_CU), (0.2e-6, RHO_AU)],
    }
    results = {'frequency_Hz': frequency, 'temperature_K': 293,
               'skin_depth_um': {name: sqrt(rho/(pi*frequency*MU0))*1e6
                                 for name, rho in [('Au', RHO_AU), ('Cu', RHO_CU)]},
               'cases': {}}
    for name, layers in cases.items():
        sheet = sheet_resistance(layers)
        results['cases'][name] = {
            'uniform_current_sheet_resistance_ohm_per_square': sheet,
            'uniform_current_resistance_ohm_per_mm_at_200um_width': sheet*5,
            'electrode_resistance_ratio_to_Au': sheet/baseline,
        }
    ratio = results['cases']['4.8um_Cu_0.2um_Au']['electrode_resistance_ratio_to_Au']
    results['total_loss_sensitivity'] = [
        {'fraction_of_original_loss_in_replaced_electrodes': eta,
         'predicted_fractional_total_loss_reduction': eta*(1-ratio)}
        for eta in (0.1, 0.5, 1.0)]
    return results


if __name__ == '__main__':
    assert abs(sheet_resistance([(5e-6, RHO_AU)])-RHO_AU/5e-6) < 1e-12
    assert sheet_resistance([(4.8e-6, RHO_CU), (.2e-6, RHO_AU)]) < sheet_resistance([(5e-6, RHO_AU)])
    output = compare()
    (HERE/'rf_material_comparison.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps(output, indent=2))
