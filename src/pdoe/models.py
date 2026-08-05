"""Core phenomenological and first-principles diagnostics for PDOE.

The package deliberately distinguishes:
1. ordinary geometric spreading,
2. phenomenological redshift laws,
3. gauge-kinetic scalar couplings, and
4. effective-metric (disformal) photon propagation.
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import cumulative_trapezoid

C_KM_S = 299_792.458


def lcdm_luminosity_distance(z, H0: float = 70.0, omega_m: float = 0.3):
    """Flat-LambdaCDM luminosity distance in Mpc."""
    z = np.asarray(z, dtype=float)
    if np.any(z < 0):
        raise ValueError("redshift must be non-negative")
    order = np.argsort(z)
    zs = z[order]
    grid = np.r_[0.0, zs]
    ez = np.sqrt(omega_m * (1.0 + grid) ** 3 + (1.0 - omega_m))
    dc = (C_KM_S / H0) * cumulative_trapezoid(1.0 / ez, grid, initial=0.0)[1:]
    dl = (1.0 + zs) * dc
    out = np.empty_like(dl)
    out[order] = dl
    return out


def exponential_path_redshift(distance_mpc, gamma_per_mpc):
    """Phenomenological ansatz 1+z = exp(gamma D); not a derived local theory."""
    distance_mpc = np.asarray(distance_mpc, dtype=float)
    return np.expm1(gamma_per_mpc * distance_mpc)


def static_path_distance(z, H0: float = 70.0):
    """Distance implied by exponential cumulative redshift in static Euclidean space."""
    z = np.asarray(z, dtype=float)
    if np.any(z < 0):
        raise ValueError("redshift must be non-negative")
    return (C_KM_S / H0) * np.log1p(z)


def static_luminosity_distance(z, p: float = 1.0, H0: float = 70.0):
    """Diagnostic static model d_L=r(1+z)^p.

    p=1/2: photon-energy loss only.
    p=1: additionally inserts an arrival-rate/time-dilation factor.
    This is a shape diagnostic, not a covariant completion.
    """
    z = np.asarray(z, dtype=float)
    return static_path_distance(z, H0) * (1.0 + z) ** p


def calibrated_distance_modulus_residual(model_dl, reference_dl):
    """Remove the absolute-magnitude/H0 intercept and return shape residuals."""
    model = np.asarray(model_dl, dtype=float)
    reference = np.asarray(reference_dl, dtype=float)
    if np.any(model <= 0) or np.any(reference <= 0):
        raise ValueError("luminosity distances must be positive")
    residual = 5.0 * np.log10(model / reference)
    return residual - np.mean(residual)


def beam_expansion_redshift(r, r0, alpha):
    """Rejected beam-circumference law: 1+z=(r/r0)^(2 alpha)."""
    r = np.asarray(r, dtype=float)
    if r0 <= 0 or np.any(r <= 0):
        raise ValueError("r and r0 must be positive")
    return (r / r0) ** (2.0 * alpha) - 1.0


def spherical_wave(r, t=0.0, wavelength=1.0, amplitude=1.0, speed=1.0):
    """Outgoing spherical wave A sin(kr-wt)/r."""
    r = np.asarray(r, dtype=float)
    if np.any(r <= 0) or wavelength <= 0 or speed <= 0:
        raise ValueError("r, wavelength and speed must be positive")
    k = 2.0 * np.pi / wavelength
    omega = speed * k
    return amplitude * np.sin(k * r - omega * t) / r


def measured_crest_spacing(r, field):
    """Estimate crest spacing after removing the 1/r spherical envelope."""
    r = np.asarray(r, dtype=float)
    field = np.asarray(field, dtype=float)
    if r.shape != field.shape or r.ndim != 1:
        raise ValueError("r and field must be same-shape 1D arrays")
    signal = r * field
    peaks = np.where((signal[1:-1] > signal[:-2]) & (signal[1:-1] > signal[2:]))[0] + 1
    if peaks.size < 2:
        raise ValueError("not enough peaks")
    return np.diff(r[peaks])


def gauge_kinetic_wkb_amplitude(B, initial_amplitude=1.0):
    """Leading WKB amplitude for L=-B(x)F^2/4: A proportional B^(-1/2).

    The leading eikonal remains k^2=0; this scalar prefactor does not create
    an independent frequency drift in geometric optics.
    """
    B = np.asarray(B, dtype=float)
    if np.any(B <= 0):
        raise ValueError("B must remain positive")
    return initial_amplitude * np.sqrt(B.flat[0] / B)


def conformal_photon_speed(conformal_factor):
    """Pure conformal rescaling leaves the photon null cone unchanged in 4D."""
    C = np.asarray(conformal_factor, dtype=float)
    if np.any(C <= 0):
        raise ValueError("conformal factor must be positive")
    return np.ones_like(C)


def disformal_photon_speed(q):
    """Matter-frame photon speed for q=(D/C) phidot^2 in homogeneous FRW.

    For ds_gamma^2=-(C-D phidot^2)dt^2 + C a^2 dx^2,
    c_gamma/c = sqrt(1-q). Lorentzian signature requires q<1.
    """
    q = np.asarray(q, dtype=float)
    if np.any(q >= 1.0):
        raise ValueError("q must be < 1 for a Lorentzian photon metric")
    return np.sqrt(1.0 - q)


def disformal_redshift(a_emit, a_obs, c_emit, c_obs):
    """Photon redshift in a homogeneous disformal optical metric.

    1+z_gamma = (a_obs/a_emit)*(c_emit/c_obs).
    The extra factor is an endpoint/evolving-background effect, not beam area.
    """
    vals = np.asarray([a_emit, a_obs, c_emit, c_obs], dtype=float)
    if np.any(vals <= 0):
        raise ValueError("scale factors and speeds must be positive")
    return (a_obs / a_emit) * (c_emit / c_obs) - 1.0


def required_static_speed_ratio(z):
    """In a=constant disformal model, c_emit/c_obs must equal 1+z."""
    z = np.asarray(z, dtype=float)
    if np.any(z < 0):
        raise ValueError("redshift must be non-negative")
    return 1.0 + z


def arrival_delay_seconds(distance_mpc, fractional_speed_difference):
    """Small-delta propagation delay |delta| D/c in seconds."""
    mpc_m = 3.085677581491367e22
    c_m_s = 299_792_458.0
    return np.abs(np.asarray(fractional_speed_difference, dtype=float)) * np.asarray(
        distance_mpc, dtype=float
    ) * mpc_m / c_m_s


def stationary_frequency(initial_frequency, affine_parameter):
    """No-go benchmark: stationary conservative propagation conserves k_t.

    In a time-independent Hamiltonian/effective metric, dk_t/dlambda=0.
    """
    lam = np.asarray(affine_parameter, dtype=float)
    return np.full_like(lam, float(initial_frequency), dtype=float)
