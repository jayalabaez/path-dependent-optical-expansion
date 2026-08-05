import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import numpy as np

from pdoe.falsification import (
    effective_average_photon_speed_excess,
    gw170817_falsification,
    homogeneous_index_time_dilation,
    static_euclidean_distance_duality_eta,
    static_optical_hubble_times,
)


def test_static_optical_photon_arrives_far_too_early_at_gw170817_redshift():
    _, _, advance = static_optical_hubble_times(0.0098)
    years = advance / (365.25 * 86400.0)
    assert 6.0e5 < years < 7.5e5


def test_effective_speed_excess_is_order_half_z_at_low_z():
    z = 1e-4
    delta = float(effective_average_photon_speed_excess(z))
    assert np.isclose(delta, z / 2.0, rtol=1e-4)


def test_gw170817_rejects_full_smooth_photon_only_redshift():
    result = gw170817_falsification()
    assert result["speed_bound_mismatch_factor"] > 1e12
    assert result["timing_mismatch_factor"] > 1e13
    assert result["max_smooth_local_optical_fraction_of_redshift"] < 1e-12


def test_static_euclidean_branch_violates_distance_duality():
    assert np.isclose(static_euclidean_distance_duality_eta(1.0), 0.5)


def test_homogeneous_index_can_reproduce_time_dilation_kinematically():
    assert np.isclose(homogeneous_index_time_dilation(1.0), 2.0)
