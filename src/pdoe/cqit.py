"""Cosmological Quantum Information Transport (CQIT) null model.

CQIT is not a claim of new physics.  It factors a redshifted optical link into
well-defined standard components:

    N_standard = D_receiver o L_eta o U_z

where U_z is coherent spectral/temporal mode dilation, L_eta is a pure-loss
channel, and D_receiver describes detector bandwidth, mode matching, and
ordinary readout noise.  Only statistically significant residuals after this
null model are candidates for additional physics.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np


def compose_redshifts(z1, z2):
    """Compose successive redshifts using (1+z_total)=(1+z1)(1+z2)."""
    z1 = np.asarray(z1, dtype=float)
    z2 = np.asarray(z2, dtype=float)
    if np.any(z1 <= -1) or np.any(z2 <= -1):
        raise ValueError("redshifts must be greater than -1")
    return (1.0 + z1) * (1.0 + z2) - 1.0


def inverse_redshift(z):
    """Return the inverse frequency dilation, represented as a negative redshift."""
    z = np.asarray(z, dtype=float)
    if np.any(z <= -1):
        raise ValueError("redshift must be greater than -1")
    return 1.0 / (1.0 + z) - 1.0


def redshifted_mode_parameters(center_frequency: float, bandwidth: float, z: float):
    """Center and bandwidth of a coherently dilated finite-bandwidth mode."""
    if center_frequency <= 0 or bandwidth <= 0 or z <= -1:
        raise ValueError("invalid frequency, bandwidth, or redshift")
    scale = 1.0 + z
    return center_frequency / scale, bandwidth / scale


def binary_entropy(probability):
    """Binary Shannon entropy in bits."""
    p = np.asarray(probability, dtype=float)
    if np.any((p < 0) | (p > 1)):
        raise ValueError("probability must be in [0,1]")
    out = np.zeros_like(p)
    mask = (p > 0) & (p < 1)
    pm = p[mask]
    out[mask] = -pm * np.log2(pm) - (1.0 - pm) * np.log2(1.0 - pm)
    return out


@dataclass(frozen=True)
class ChannelBudget:
    """Resource-relative information budget for one cosmological optical link."""

    emitted_uses_per_second: float
    observed_mode_uses_per_second: float
    detected_uses_per_second: float
    classical_bits_per_second: float
    erasure_quantum_qubits_per_second: float
    conditional_state_fidelity: float
    effective_transmissivity: float
    redshift: float

    def as_dict(self):
        return asdict(self)


def standard_channel_budget(
    emitted_uses_per_second: float,
    z: float,
    geometric_transmissivity: float,
    detector_efficiency: float = 1.0,
    mode_capture: float = 1.0,
    qber: float = 0.0,
    conditional_decoherence: float = 0.0,
):
    """Compute the standard redshift + loss + receiver information budget.

    Classical rate assumes an orthogonal binary alphabet with erasure and a
    binary-symmetric error rate ``qber`` on detected events.  The quantum rate
    uses the unassisted qubit-erasure capacity max(0, 2*eta-1) per emitted use.
    Conditional fidelity describes a surviving, detected photon's internal
    state and is therefore separate from erasure probability.
    """
    scalars = [
        emitted_uses_per_second,
        geometric_transmissivity,
        detector_efficiency,
        mode_capture,
        qber,
        conditional_decoherence,
    ]
    if emitted_uses_per_second < 0 or z < 0:
        raise ValueError("rate and redshift must be non-negative")
    if any(not (0 <= x <= 1) for x in scalars[1:]):
        raise ValueError("channel probabilities must be in [0,1]")

    observed_rate = emitted_uses_per_second / (1.0 + z)
    eta = geometric_transmissivity * detector_efficiency * mode_capture
    detected_rate = observed_rate * eta
    classical_rate = detected_rate * float(1.0 - binary_entropy(np.array([qber]))[0])
    quantum_rate = observed_rate * max(0.0, 2.0 * eta - 1.0)
    fidelity = 1.0 - conditional_decoherence

    return ChannelBudget(
        emitted_uses_per_second=float(emitted_uses_per_second),
        observed_mode_uses_per_second=float(observed_rate),
        detected_uses_per_second=float(detected_rate),
        classical_bits_per_second=float(classical_rate),
        erasure_quantum_qubits_per_second=float(quantum_rate),
        conditional_state_fidelity=float(fidelity),
        effective_transmissivity=float(eta),
        redshift=float(z),
    )


def conditional_bell_fidelity(polarization_rotation_rad: float = 0.0, dephasing: float = 0.0):
    """Bell-state fidelity conditioned on both photons being detected.

    A common polarization-independent redshift/loss channel leaves the Bell
    state unchanged.  Differential polarization rotation and dephasing reduce
    fidelity and are clean targets for beyond-null-model searches.
    """
    if not (0 <= dephasing <= 1):
        raise ValueError("dephasing must be in [0,1]")
    return float((1.0 - dephasing) * np.cos(polarization_rotation_rad) ** 2 + 0.5 * dephasing)


def residual_significance(observed, expected, sigma):
    """Signed Gaussian residual significance."""
    observed = np.asarray(observed, dtype=float)
    expected = np.asarray(expected, dtype=float)
    sigma = np.asarray(sigma, dtype=float)
    if np.any(sigma <= 0):
        raise ValueError("sigma must be positive")
    return (observed - expected) / sigma


def candidate_new_physics_flag(significances, threshold_sigma: float = 5.0, minimum_independent_hits: int = 2):
    """Conservative discovery-screen flag for independent residual tests.

    This is a project triage rule, not a statistical discovery theorem.  A
    claim still requires systematics control, trials correction, and an
    independently reproduced physical model.
    """
    s = np.abs(np.asarray(significances, dtype=float))
    if threshold_sigma <= 0 or minimum_independent_hits < 1:
        raise ValueError("invalid threshold")
    return bool(np.count_nonzero(s >= threshold_sigma) >= minimum_independent_hits)


def novelty_classification():
    """Machine-readable separation between known physics and project scope."""
    return [
        {
            "item": "finite-bandwidth redshift as mode dilation/mixing",
            "classification": "established literature",
            "new_physics": False,
        },
        {
            "item": "loss and detector mismatch reducing accessible capacity",
            "classification": "standard quantum information",
            "new_physics": False,
        },
        {
            "item": "horizon rate tending to zero asymptotically",
            "classification": "standard relativistic causal behavior",
            "new_physics": False,
        },
        {
            "item": "integrated receiver-relative CQIT null-test pipeline",
            "classification": "research software/synthesis; novelty unverified",
            "new_physics": False,
        },
        {
            "item": "reproducible residual beyond dilation, loss, mismatch, and known noise",
            "classification": "candidate new physics only if observed and independently confirmed",
            "new_physics": True,
        },
    ]
