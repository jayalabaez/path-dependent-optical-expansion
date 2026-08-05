import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import numpy as np
from pdoe.comprehensive import (
    ap_relative_difference,
    cmb_temperature_measurement_test,
    conditional_clock_drift_mismatch,
    firas_fractional_energy_injection_limit,
    lcdm_redshift_drift,
    liouville_redshift_blackbody_residual,
    linear_liv_fractional_speed_bound,
    photon_mass_speed_deficit,
    static_optical_redshift_drift,
)


def test_static_constant_cmb_temperature_is_rejected_at_over_40_sigma():
    result = cmb_temperature_measurement_test()
    assert result["constant_temperature_pull_sigma"] > 40.0
    assert abs(result["standard_pull_sigma"]) < 1.0


def test_inferred_cmb_beta_is_consistent_with_zero():
    result = cmb_temperature_measurement_test()
    assert abs(result["inferred_beta"]) < result["inferred_beta_sigma"]


def test_liouville_transport_preserves_blackbody_exactly():
    assert liouville_redshift_blackbody_residual(3.0) < 1e-12


def test_firas_energy_fraction_is_tiny():
    assert firas_fractional_energy_injection_limit() < 4e-5


def test_static_ap_mapping_deviates_at_high_redshift():
    diff = float(ap_relative_difference(np.array([2.33]))[0])
    assert abs(diff) > 0.1


def test_optical_and_lcdm_redshift_drift_have_opposite_sign_at_z4():
    _, optical = static_optical_redshift_drift(3.962)
    _, lcdm = lcdm_redshift_drift(3.962)
    assert float(optical) > 0
    assert float(lcdm) < 0


def test_linear_liv_cannot_make_large_optical_speed_change():
    assert float(linear_liv_fractional_speed_bound(1.0)) < 1e-28


def test_photon_mass_effect_at_optical_energy_is_negligible():
    assert float(photon_mass_speed_deficit(1.0)) < 1e-28


def test_gauge_kinetic_clock_drift_is_conditionally_excluded():
    assert conditional_clock_drift_mismatch()["mismatch_factor"] > 1e7
