import math

import numpy as np

from pdoe.continuous_loss import (
    T_CMB0_K,
    cmb_temperature_significance,
    distance_duality_eta,
    distance_from_redshift,
    equivalent_linear_eta0_at_z1,
    eta0_significance,
    f_ap_lcdm,
    f_ap_static_loss,
    h0_si,
    local_fractional_shift,
    loss_coefficient_per_m,
    per_event_log_loss,
    photon_energy_ratio,
    redshift_from_distance,
    required_stochastic_events,
    run_audit,
    static_luminosity_distance,
    time_dilation_significance,
    tolman_surface_brightness_ratio,
)


def test_loss_law_round_trip():
    for z in [1e-6, 0.1, 1.0, 10.0]:
        r = distance_from_redshift(z)
        assert math.isclose(
            redshift_from_distance(r), z, rel_tol=1e-12, abs_tol=1e-15
        )


def test_hubble_loss_coefficient():
    assert math.isclose(
        loss_coefficient_per_m(), h0_si() / 299_792_458.0, rel_tol=1e-15
    )
    assert 7e-27 < loss_coefficient_per_m() < 8e-27


def test_energy_ratio():
    assert photon_energy_ratio(1.0) == 0.5
    assert photon_energy_ratio(9.0) == 0.1


def test_static_luminosity_distance_scalings():
    r = 2.0
    assert math.isclose(static_luminosity_distance(r, 3.0, 0.0), 4.0)
    assert math.isclose(static_luminosity_distance(r, 3.0, 1.0), 8.0)


def test_distance_duality_failure():
    assert math.isclose(distance_duality_eta(1.0, 0.0), 2 ** -1.5)
    assert math.isclose(distance_duality_eta(1.0, 1.0), 0.5)
    assert eta0_significance(equivalent_linear_eta0_at_z1(0.0)) > 20
    assert eta0_significance(equivalent_linear_eta0_at_z1(1.0)) > 15


def test_tolman_static_scalings_are_too_shallow():
    assert math.isclose(tolman_surface_brightness_ratio(1.0, 0.0), 0.5)
    assert math.isclose(tolman_surface_brightness_ratio(1.0, 1.0), 0.25)
    assert 2 ** -4 == 0.0625


def test_supernova_time_dilation_falsifies_pure_loss():
    assert time_dilation_significance(0.0) > 80
    assert time_dilation_significance(1.0) < 1


def test_cmb_temperature():
    assert cmb_temperature_significance(T_CMB0_K) > 40
    assert cmb_temperature_significance(T_CMB0_K * 1.89) < 1


def test_stochastic_broadening_requirement():
    n_events = required_stochastic_events(1.0, 1 / 140_000)
    assert n_events > 9e9
    assert per_event_log_loss(1.0, n_events) < 1e-10


def test_bao_geometry_difference():
    differences = [
        f_ap_static_loss(z) / f_ap_lcdm(z) - 1 for z in [0.5, 1.0, 2.33]
    ]
    assert differences[0] > 0.04
    assert abs(differences[1]) < 0.03
    assert differences[2] < -0.10


def test_local_effect_is_tiny():
    assert local_fractional_shift(149_597_870_700.0) < 2e-15


def test_full_audit_is_fail_closed():
    report = run_audit()
    assert report["n_tests"] == 9
    assert report["n_falsified"] >= 5
    assert report["whole_new_physics_confirmed"] is False
    assert "falsified" in report["verdict"].lower()
