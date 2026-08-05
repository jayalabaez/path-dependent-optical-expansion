import numpy as np

from pdoe.quantum_information import (
    accessible_information_rate,
    bosonic_entropy_g,
    cycles_in_observation_window,
    de_sitter_horizon_scaling,
    distribution_std,
    fixed_detector_capture_probability,
    gaussian_spectral_mode,
    gaussian_time_probability,
    matched_detector_capture_probability,
    mode_overlap,
    one_cycle_redshift,
    pure_loss_classical_capacity,
    redshifted_gaussian_mode,
    single_photon_erasure_classical_information,
    single_photon_erasure_quantum_capacity,
)


def test_redshifted_mode_is_normalized():
    nu = np.linspace(0.001, 180.0, 200_000)
    shifted = redshifted_gaussian_mode(nu, center=100.0, sigma=4.0, z=3.0)
    assert np.isclose(np.trapezoid(np.abs(shifted) ** 2, nu), 1.0, atol=2e-8)


def test_matched_detector_recovers_unit_fidelity():
    nu = np.linspace(0.001, 180.0, 120_000)
    assert matched_detector_capture_probability(nu, 100.0, 4.0, z=5.0) > 1.0 - 1e-12


def test_fixed_detector_loses_mode_overlap():
    nu = np.linspace(0.001, 180.0, 120_000)
    p0 = fixed_detector_capture_probability(nu, 100.0, 4.0, z=0.0)
    p1 = fixed_detector_capture_probability(nu, 100.0, 4.0, z=1.0)
    assert p0 > 1.0 - 1e-12
    assert p1 < 1e-8


def test_redshift_stretches_temporal_width():
    t = np.linspace(-50.0, 50.0, 300_000)
    p0 = gaussian_time_probability(t, sigma_t=1.0, z=0.0)
    p4 = gaussian_time_probability(t, sigma_t=1.0, z=4.0)
    assert np.isclose(distribution_std(t, p4) / distribution_std(t, p0), 5.0, rtol=2e-5)


def test_finite_redshift_never_makes_zero_cycles():
    assert cycles_in_observation_window(5e14, z=1e12, duration_s=1.0) > 0
    assert np.isclose(one_cycle_redshift(5e14, 1.0), 5e14 - 1.0)


def test_pure_loss_capacities_vanish_at_zero_transmissivity():
    assert bosonic_entropy_g(np.array([0.0]))[0] == 0.0
    assert pure_loss_classical_capacity(np.array([0.0]), 1.0)[0] == 0.0
    assert single_photon_erasure_classical_information(np.array([0.0]))[0] == 0.0
    assert single_photon_erasure_quantum_capacity(np.array([0.0]))[0] == 0.0


def test_quantum_erasure_capacity_threshold():
    assert single_photon_erasure_quantum_capacity(np.array([0.49]))[0] == 0.0
    assert np.isclose(single_photon_erasure_quantum_capacity(np.array([0.75]))[0], 0.5)


def test_accessible_rate_has_loss_and_time_dilation_factors():
    rate = accessible_information_rate(1000.0, z=3.0, geometric_transmissivity=0.2)
    assert np.isclose(rate, 50.0)


def test_de_sitter_horizon_is_asymptotic_not_finite_flattening():
    eps = np.array([1e-2, 1e-6, 1e-12])
    z, rate = de_sitter_horizon_scaling(eps)
    assert np.all(np.diff(z) > 0)
    assert np.all(np.diff(rate) < 0)
    assert np.all(rate > 0)
    assert rate[-1] < 1.1e-12
