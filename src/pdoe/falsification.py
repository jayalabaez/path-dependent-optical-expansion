"""High-leverage falsification tests for optical-redshift models.

The functions here isolate one concrete completion: a static matter spacetime with
an isotropic, homogeneous, time-varying optical index n(t). Photons see
c_gamma=c/n while gravitational waves remain on the matter metric.

This is not the most general constitutive theory. It is the minimal smooth
photon-only completion capable of turning endpoint index evolution into a
cosmological redshift. Its failure therefore falsifies that branch, not every
possible universal or nonlocal effective geometry.
"""
from __future__ import annotations

import numpy as np

MPC_KM = 3.0856775814913673e19
SECONDS_PER_YEAR = 365.25 * 86400.0


def hubble_per_second(H0_km_s_mpc: float = 70.0) -> float:
    """Convert H0 from km s^-1 Mpc^-1 to s^-1."""
    if H0_km_s_mpc <= 0:
        raise ValueError("H0 must be positive")
    return H0_km_s_mpc / MPC_KM


def static_optical_hubble_times(z, H0_km_s_mpc: float = 70.0):
    """Travel times in the minimal homogeneous static optical-Hubble model.

    Choose n(t)=exp[H0(t-t0)] with n(t0)=1. Then
        1+z = n0/ne = exp(H0 tau_gamma)
    and the static coordinate distance is
        D = integral c/n dt = (c/H0) z.

    A gravitational wave on the matter metric traverses the same D in z/H0,
    whereas the photon takes ln(1+z)/H0.

    Returns photon time, GW time, and GW-minus-photon arrival time in seconds.
    Positive delay means the photon arrives earlier than the GW.
    """
    z = np.asarray(z, dtype=float)
    if np.any(z < 0):
        raise ValueError("redshift must be non-negative")
    H0 = hubble_per_second(H0_km_s_mpc)
    photon = np.log1p(z) / H0
    gw = z / H0
    return photon, gw, gw - photon


def effective_average_photon_speed_excess(z):
    """Average c_gamma/c - 1 for the minimal static optical-Hubble model."""
    z = np.asarray(z, dtype=float)
    if np.any(z < 0):
        raise ValueError("redshift must be non-negative")
    out = np.zeros_like(z, dtype=float)
    mask = z > 0
    out[mask] = z[mask] / np.log1p(z[mask]) - 1.0
    return out


def gw170817_falsification(
    z_host: float = 0.0098,
    H0_km_s_mpc: float = 70.0,
    observed_delay_seconds: float = 1.74,
    speed_bound: float = 3e-15,
):
    """Numerical verdict for a photon-only smooth optical explanation.

    ``speed_bound`` is the conservative magnitude of the published GW170817
    bound on the fractional GW-photon propagation-speed difference.
    """
    photon, gw, advance = static_optical_hubble_times(z_host, H0_km_s_mpc)
    avg_excess = float(effective_average_photon_speed_excess(z_host))
    # In the small optical-fraction limit, avg speed excess ~= z_opt/2.
    max_optical_fraction = 2.0 * speed_bound / z_host
    return {
        "z_host": z_host,
        "H0_km_s_mpc": H0_km_s_mpc,
        "photon_travel_years": float(photon / SECONDS_PER_YEAR),
        "gw_travel_years": float(gw / SECONDS_PER_YEAR),
        "predicted_photon_advance_years": float(advance / SECONDS_PER_YEAR),
        "observed_gw_to_gamma_delay_seconds": observed_delay_seconds,
        "timing_mismatch_factor": float(advance / observed_delay_seconds),
        "effective_average_cgamma_over_c_minus_1": avg_excess,
        "published_fractional_speed_bound_used": speed_bound,
        "speed_bound_mismatch_factor": avg_excess / speed_bound,
        "max_smooth_local_optical_fraction_of_redshift": max_optical_fraction,
    }


def static_euclidean_distance_duality_eta(z):
    """CDDR eta for photon-number-conserving static Euclidean optical redshift.

    Energy redshift plus arrival-rate dilation gives D_L=r(1+z), while static
    Euclidean angular geometry gives D_A=r. Therefore
        eta = D_L / [(1+z)^2 D_A] = 1/(1+z).
    """
    z = np.asarray(z, dtype=float)
    if np.any(z < 0):
        raise ValueError("redshift must be non-negative")
    return 1.0 / (1.0 + z)


def homogeneous_index_time_dilation(z):
    """Pulse-duration stretch predicted by a homogeneous time-varying index.

    Differentiating the null-path integral for two adjacent pulses gives
    dt_obs/dt_emit = n_obs/n_emit = 1+z. This branch therefore passes the
    supernova time-dilation relation at the kinematic level.
    """
    z = np.asarray(z, dtype=float)
    if np.any(z < 0):
        raise ValueError("redshift must be non-negative")
    return 1.0 + z
