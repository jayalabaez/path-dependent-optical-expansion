"""Quantum-information diagnostics for cosmologically redshifted light.

The module separates four physically different effects:

1. coherent redshift of a finite-bandwidth photon mode;
2. mode mismatch in a detector that is not retuned;
3. pure photon loss / erasure;
4. asymptotic information-rate suppression near a cosmological horizon.

These functions do not claim that redshift is a new quantum-information
mechanism. They test which information-theoretic statements follow from
standard coherent propagation and loss models.
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import cumulative_trapezoid

C_KM_S = 299_792.458
MPC_M = 3.085677581491367e22


def _normalize_mode(grid: np.ndarray, amplitude: np.ndarray) -> np.ndarray:
    grid = np.asarray(grid, dtype=float)
    amplitude = np.asarray(amplitude, dtype=complex)
    if grid.ndim != 1 or amplitude.shape != grid.shape:
        raise ValueError("grid and amplitude must be same-shape 1D arrays")
    norm = np.trapezoid(np.abs(amplitude) ** 2, grid)
    if not np.isfinite(norm) or norm <= 0:
        raise ValueError("mode has non-positive norm")
    return amplitude / np.sqrt(norm)


def gaussian_spectral_mode(frequency, center: float, sigma: float):
    """Normalized Gaussian single-photon spectral amplitude.

    ``sigma`` is the standard deviation of the probability density |f|^2.
    Frequencies may be dimensionless or expressed in any consistent unit.
    """
    frequency = np.asarray(frequency, dtype=float)
    if center <= 0 or sigma <= 0:
        raise ValueError("center and sigma must be positive")
    amp = np.exp(-((frequency - center) ** 2) / (4.0 * sigma**2))
    return _normalize_mode(frequency, amp)


def redshifted_gaussian_mode(frequency, center: float, sigma: float, z: float):
    """Coherently redshifted Gaussian mode.

    The dilation map is f_z(nu)=sqrt(1+z) f((1+z)nu), which preserves the
    continuum norm. For a Gaussian this moves both center and bandwidth by
    1/(1+z). Numerical normalization removes finite-grid truncation error.
    """
    if z < 0:
        raise ValueError("redshift must be non-negative")
    scale = 1.0 + z
    frequency = np.asarray(frequency, dtype=float)
    initial = gaussian_spectral_mode(scale * frequency, center, sigma)
    return _normalize_mode(frequency, np.sqrt(scale) * initial)


def mode_overlap(grid, mode_a, mode_b) -> complex:
    """Inner product between two normalized spectral modes."""
    grid = np.asarray(grid, dtype=float)
    a = _normalize_mode(grid, np.asarray(mode_a, dtype=complex))
    b = _normalize_mode(grid, np.asarray(mode_b, dtype=complex))
    return np.trapezoid(np.conjugate(a) * b, grid)


def fixed_detector_capture_probability(frequency, center: float, sigma: float, z: float) -> float:
    """Probability that a redshifted photon projects onto the unshifted mode."""
    original = gaussian_spectral_mode(frequency, center, sigma)
    shifted = redshifted_gaussian_mode(frequency, center, sigma, z)
    return float(np.abs(mode_overlap(frequency, original, shifted)) ** 2)


def matched_detector_capture_probability(frequency, center: float, sigma: float, z: float) -> float:
    """Capture probability for a detector exactly matched to the shifted mode."""
    shifted = redshifted_gaussian_mode(frequency, center, sigma, z)
    return float(np.abs(mode_overlap(frequency, shifted, shifted)) ** 2)


def gaussian_time_probability(time, sigma_t: float, z: float = 0.0):
    """Normalized temporal probability density of a redshift-stretched packet.

    A coherent frequency dilation by s=1+z stretches the temporal standard
    deviation to s*sigma_t and lowers the peak density by 1/s.
    """
    time = np.asarray(time, dtype=float)
    if sigma_t <= 0 or z < 0:
        raise ValueError("sigma_t must be positive and z non-negative")
    width = sigma_t * (1.0 + z)
    density = np.exp(-(time**2) / (2.0 * width**2)) / (np.sqrt(2.0 * np.pi) * width)
    return density


def distribution_std(grid, density) -> float:
    """Standard deviation of a normalized numerical probability density."""
    grid = np.asarray(grid, dtype=float)
    density = np.asarray(density, dtype=float)
    norm = np.trapezoid(density, grid)
    if norm <= 0:
        raise ValueError("density must have positive integral")
    p = density / norm
    mean = np.trapezoid(grid * p, grid)
    var = np.trapezoid((grid - mean) ** 2 * p, grid)
    return float(np.sqrt(max(var, 0.0)))


def cycles_in_observation_window(emitted_frequency_hz: float, z: float, duration_s: float) -> float:
    """Number of carrier cycles within a finite observation interval."""
    if emitted_frequency_hz <= 0 or duration_s <= 0 or z < 0:
        raise ValueError("frequency/duration must be positive and z non-negative")
    return emitted_frequency_hz * duration_s / (1.0 + z)


def one_cycle_redshift(emitted_frequency_hz: float, duration_s: float) -> float:
    """Redshift at which a fixed observation window contains exactly one cycle."""
    if emitted_frequency_hz <= 0 or duration_s <= 0:
        raise ValueError("frequency and duration must be positive")
    return emitted_frequency_hz * duration_s - 1.0


def bosonic_entropy_g(x):
    """Entropy g(x)=(x+1)log2(x+1)-x log2(x), with g(0)=0."""
    x = np.asarray(x, dtype=float)
    if np.any(x < 0):
        raise ValueError("x must be non-negative")
    out = np.zeros_like(x)
    mask = x > 0
    xm = x[mask]
    out[mask] = (xm + 1.0) * np.log2(xm + 1.0) - xm * np.log2(xm)
    return out


def pure_loss_classical_capacity(transmissivity, mean_input_photons: float = 1.0):
    """Classical capacity g(eta*N) bits/mode of an ideal pure-loss bosonic channel."""
    eta = np.asarray(transmissivity, dtype=float)
    if np.any((eta < 0) | (eta > 1)) or mean_input_photons < 0:
        raise ValueError("eta must be in [0,1] and photon number non-negative")
    return bosonic_entropy_g(eta * mean_input_photons)


def single_photon_erasure_classical_information(transmissivity):
    """Classical bits/use for an orthogonal single-photon alphabet with erasure flag."""
    eta = np.asarray(transmissivity, dtype=float)
    if np.any((eta < 0) | (eta > 1)):
        raise ValueError("transmissivity must be in [0,1]")
    return eta


def single_photon_erasure_quantum_capacity(transmissivity):
    """Quantum capacity max(0,2 eta-1) qubits/use of the qubit erasure model."""
    eta = np.asarray(transmissivity, dtype=float)
    if np.any((eta < 0) | (eta > 1)):
        raise ValueError("transmissivity must be in [0,1]")
    return np.maximum(0.0, 2.0 * eta - 1.0)


def accessible_information_rate(
    source_uses_per_second: float,
    z,
    geometric_transmissivity,
    detector_efficiency: float = 1.0,
    mode_capture=1.0,
):
    """Detected orthogonal-symbol information rate in bits/s.

    One source use carries one ideal bit. Redshift slows the received use rate
    by 1/(1+z); loss and mode mismatch act as erasures.
    """
    if source_uses_per_second < 0 or not (0 <= detector_efficiency <= 1):
        raise ValueError("invalid source rate or detector efficiency")
    z = np.asarray(z, dtype=float)
    eta = np.asarray(geometric_transmissivity, dtype=float)
    capture = np.asarray(mode_capture, dtype=float)
    if np.any(z < 0) or np.any((eta < 0) | (eta > 1)) or np.any((capture < 0) | (capture > 1)):
        raise ValueError("invalid redshift/transmissivity/capture")
    return source_uses_per_second * eta * detector_efficiency * capture / (1.0 + z)


def flat_lcdm_comoving_distance(z, H0: float = 70.0, omega_m: float = 0.3):
    """Flat-LambdaCDM line-of-sight/transverse comoving distance in Mpc."""
    z = np.asarray(z, dtype=float)
    if np.any(z < 0) or H0 <= 0 or not (0 < omega_m < 1):
        raise ValueError("invalid cosmology")
    order = np.argsort(z)
    zs = z[order]
    grid = np.unique(np.r_[0.0, zs])
    ez = np.sqrt(omega_m * (1.0 + grid) ** 3 + (1.0 - omega_m))
    dc_grid = (C_KM_S / H0) * cumulative_trapezoid(1.0 / ez, grid, initial=0.0)
    dc_sorted = np.interp(zs, grid, dc_grid)
    out = np.empty_like(dc_sorted)
    out[order] = dc_sorted
    return out


def isotropic_telescope_transmissivity(distance_mpc, aperture_area_m2: float):
    """Fraction of an isotropic photon wavefront intercepted by an aperture."""
    d = np.asarray(distance_mpc, dtype=float) * MPC_M
    if aperture_area_m2 <= 0 or np.any(d <= 0):
        raise ValueError("distance and area must be positive")
    return np.minimum(1.0, aperture_area_m2 / (4.0 * np.pi * d**2))


def lcdm_detected_photon_rate(
    z,
    emitted_photons_per_second: float,
    aperture_area_m2: float,
    detector_efficiency: float = 1.0,
    H0: float = 70.0,
    omega_m: float = 0.3,
):
    """Photon count rate from an isotropic source in flat LambdaCDM.

    Geometry uses the present-area sphere 4*pi*D_M^2. Arrival times are
    dilated by 1+z. This is a count rate, not an energy flux.
    """
    z = np.asarray(z, dtype=float)
    dm = flat_lcdm_comoving_distance(z, H0=H0, omega_m=omega_m)
    eta = isotropic_telescope_transmissivity(dm, aperture_area_m2)
    return accessible_information_rate(
        emitted_photons_per_second,
        z,
        eta,
        detector_efficiency=detector_efficiency,
        mode_capture=1.0,
    )


def de_sitter_horizon_scaling(epsilon):
    """Asymptotic redshift/information scaling near a de Sitter event horizon.

    Let epsilon=(exp(-H t_emit)-H chi/c)/(H chi/c)>0 measure how close an
    emission event is to the latest event that can ever reach the observer.
    Then 1+z=(1+epsilon)/epsilon and the received use-rate fraction is its
    inverse epsilon/(1+epsilon). Both remain finite for epsilon>0; as
    epsilon->0, z->infinity and the rate tends to zero only asymptotically.
    """
    eps = np.asarray(epsilon, dtype=float)
    if np.any(eps <= 0):
        raise ValueError("epsilon must be positive")
    one_plus_z = (1.0 + eps) / eps
    rate_fraction = eps / (1.0 + eps)
    return one_plus_z - 1.0, rate_fraction
