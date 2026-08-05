import numpy as np

from pdoe.cqit import (
    candidate_new_physics_flag,
    compose_redshifts,
    conditional_bell_fidelity,
    inverse_redshift,
    novelty_classification,
    redshifted_mode_parameters,
    residual_significance,
    standard_channel_budget,
)


def test_redshift_composition_group_law():
    assert np.isclose(compose_redshifts(1.0, 2.0), 5.0)


def test_inverse_redshift_cancels():
    for z in [0.01, 1.0, 10.0]:
        assert np.isclose(compose_redshifts(z, inverse_redshift(z)), 0.0)


def test_mode_center_and_bandwidth_scale_together():
    center, width = redshifted_mode_parameters(100.0, 4.0, z=3.0)
    assert np.isclose(center, 25.0)
    assert np.isclose(width, 1.0)
    assert np.isclose(width / center, 0.04)


def test_channel_budget_separates_time_dilation_and_loss():
    budget = standard_channel_budget(
        emitted_uses_per_second=1000.0,
        z=3.0,
        geometric_transmissivity=0.2,
        detector_efficiency=0.5,
        mode_capture=0.5,
    )
    assert np.isclose(budget.observed_mode_uses_per_second, 250.0)
    assert np.isclose(budget.effective_transmissivity, 0.05)
    assert np.isclose(budget.detected_uses_per_second, 12.5)


def test_perfect_common_channel_preserves_conditional_bell_state():
    assert np.isclose(conditional_bell_fidelity(), 1.0)


def test_differential_polarization_effect_is_detectable():
    assert conditional_bell_fidelity(polarization_rotation_rad=np.pi / 4) < 0.51


def test_standard_null_has_zero_residual():
    sig = residual_significance([1.0, 2.0], [1.0, 2.0], [0.1, 0.2])
    assert np.allclose(sig, 0.0)


def test_discovery_screen_requires_two_independent_hits():
    assert not candidate_new_physics_flag([5.2, 1.0])
    assert candidate_new_physics_flag([5.2, -6.1, 0.4])


def test_novelty_map_does_not_label_known_redshift_as_new_physics():
    rows = novelty_classification()
    known = [row for row in rows if "finite-bandwidth" in row["item"]][0]
    assert known["new_physics"] is False
