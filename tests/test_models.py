import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import numpy as np
import pytest

from pdoe.audit import branch_audit
from pdoe.models import (
    C_KM_S,
    arrival_delay_seconds,
    beam_expansion_redshift,
    conformal_photon_speed,
    disformal_photon_speed,
    disformal_redshift,
    exponential_path_redshift,
    gauge_kinetic_wkb_amplitude,
    lcdm_luminosity_distance,
    measured_crest_spacing,
    required_static_speed_ratio,
    spherical_wave,
    static_luminosity_distance,
    stationary_frequency,
)


def test_low_z_lcdm_hubble_law():
    z = np.array([1e-5, 2e-5])
    dl = lcdm_luminosity_distance(z)
    expected = C_KM_S / 70.0 * z
    assert np.allclose(dl, expected, rtol=5e-5)


def test_exponential_path_redshift_zero():
    assert exponential_path_redshift(0.0, 0.1) == 0.0


def test_beam_model_depends_on_reference_scale():
    z1 = beam_expansion_redshift(1e9, 1.0, 0.01)
    z2 = beam_expansion_redshift(1e9, 1e3, 0.01)
    assert z1 != z2


def test_static_distance_positive():
    assert np.all(static_luminosity_distance(np.array([0.1, 1.0]), 1.0) > 0)


def test_spherical_wave_keeps_wavelength():
    r = np.linspace(1.0, 40.0, 40_000)
    field = spherical_wave(r, wavelength=1.0)
    spacing = measured_crest_spacing(r, field)
    assert np.isclose(spacing.mean(), 1.0, rtol=2e-3)


def test_gauge_kinetic_prefactor_changes_amplitude_not_phase_law():
    B = np.array([1.0, 4.0])
    amp = gauge_kinetic_wkb_amplitude(B)
    assert np.allclose(amp, [1.0, 0.5])


def test_conformal_factor_does_not_change_light_speed():
    assert np.all(conformal_photon_speed([0.2, 1.0, 10.0]) == 1.0)


def test_disformal_speed_and_signature():
    assert np.isclose(disformal_photon_speed(0.1), np.sqrt(0.9))
    with pytest.raises(ValueError):
        disformal_photon_speed(1.0)


def test_static_disformal_redshift_requires_speed_ratio():
    assert np.isclose(disformal_redshift(1.0, 1.0, 2.0, 1.0), 1.0)
    assert np.isclose(required_static_speed_ratio(1.0), 2.0)


def test_stationary_frequency_is_conserved():
    lam = np.linspace(0, 100, 1000)
    assert np.all(stationary_frequency(37.0, lam) == 37.0)


def test_multimessenger_delay_scale():
    delay = arrival_delay_seconds(40.0, 1e-15)
    assert 4.0 < delay < 4.2


def test_audit_has_only_one_core_open_branch():
    rows = branch_audit()
    statuses = {row["branch"]: row["status"] for row in rows}
    assert statuses["Disformal scalar-photon metric"].startswith("MATHEMATICALLY OPEN")
    assert statuses["Circumference coupling Gamma=alpha theta_opt"] == "REJECTED"
