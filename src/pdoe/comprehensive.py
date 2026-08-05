"""Comprehensive falsification diagnostics for optical-redshift theories.

The module is deliberately model-class based.  A failed diagnostic applies only
when its assumptions match the proposed completion.  The aim is to prevent a
phenomenological distance-redshift curve from being mistaken for a complete
physical theory.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import math
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import minimize

C_M_S = 299_792_458.0
C_KM_S = 299_792.458
MPC_KM = 3.0856775814913673e19
SECONDS_PER_YEAR = 365.25 * 86400.0
H_PLANCK_EV_S = 4.135667696e-15
K_B_EV_K = 8.617333262e-5
E_PLANCK_EV = 1.220890e28


@dataclass(frozen=True)
class AuditResult:
    test: str
    model_class: str
    status: str
    metric: float | str
    limit_or_target: float | str
    interpretation: str

    def to_dict(self):
        return asdict(self)


def hubble_s(H0_km_s_mpc: float = 70.0) -> float:
    if H0_km_s_mpc <= 0:
        raise ValueError("H0 must be positive")
    return H0_km_s_mpc / MPC_KM


def hubble_fraction_per_year(H0_km_s_mpc: float = 70.0) -> float:
    """Fractional evolution rate H0 expressed per Julian year."""
    return hubble_s(H0_km_s_mpc) * SECONDS_PER_YEAR


def cmb_temperature_prediction(z, T0: float = 2.72548, beta: float = 0.0):
    z = np.asarray(z, dtype=float)
    if np.any(z < 0) or T0 <= 0:
        raise ValueError("valid non-negative z and positive T0 required")
    return T0 * (1.0 + z) ** (1.0 - beta)


def cmb_temperature_measurement_test(
    z: float = 0.89,
    observed_K: float = 5.13,
    sigma_K: float = 0.06,
    T0_K: float = 2.72548,
):
    """Compare standard adiabatic and constant-temperature static histories.

    This tests the *local radiation bath* at the absorber epoch.  It rules out a
    model in which the past CMB was physically at today's temperature and all
    redshift occurred only after emission.  A globally evolving optical field
    can match the measurement, but then the radiation field itself evolves.
    """
    if z <= 0 or observed_K <= 0 or sigma_K <= 0 or T0_K <= 0:
        raise ValueError("positive inputs required")
    standard = float(cmb_temperature_prediction(z, T0_K, 0.0))
    static_sigma = (observed_K - T0_K) / sigma_K
    standard_pull = (observed_K - standard) / sigma_K
    beta = 1.0 - math.log(observed_K / T0_K) / math.log1p(z)
    beta_sigma = sigma_K / (observed_K * math.log1p(z))
    return {
        "z": z,
        "observed_K": observed_K,
        "sigma_K": sigma_K,
        "standard_prediction_K": standard,
        "standard_pull_sigma": standard_pull,
        "constant_temperature_pull_sigma": static_sigma,
        "inferred_beta": beta,
        "inferred_beta_sigma": beta_sigma,
    }


def planck_occupation(x):
    """Photon occupation number 1/(exp(x)-1), stable for small x."""
    x = np.asarray(x, dtype=float)
    if np.any(x <= 0):
        raise ValueError("x must be positive")
    return 1.0 / np.expm1(x)


def blackbody_shape(x):
    """Dimensionless specific intensity proportional to x^3/(exp(x)-1)."""
    x = np.asarray(x, dtype=float)
    return x**3 * planck_occupation(x)


def liouville_redshift_blackbody_residual(z: float, points: int = 2000) -> float:
    """RMS fractional residual after coherent metric-like redshift.

    In Liouville transport I_nu/nu^3 is invariant.  An emitted blackbody at
    T_emit=(1+z)T0 is therefore observed as an exact blackbody at T0.
    """
    if z < 0 or points < 100:
        raise ValueError("invalid z or grid")
    x_obs = np.logspace(-3, 2, points)
    x_emit = x_obs  # h[(1+z)nu]/k[(1+z)T0] = h nu/kT0
    transported = blackbody_shape(x_emit)
    target = blackbody_shape(x_obs)
    mask = target > target.max() * 1e-12
    return float(np.sqrt(np.mean(((transported[mask] - target[mask]) / target[mask]) ** 2)))


def naive_energy_loss_blackbody_residual(z: float, points: int = 2000) -> float:
    """Best-fit blackbody residual for a specified naive energy-loss mapping.

    The toy mapping reduces each photon's energy but does not include the
    Liouville nu^3 phase-space Jacobian.  We allow a free amplitude and
    temperature when fitting, making this a conservative shape test.
    """
    if z <= 0 or points < 100:
        raise ValueError("positive z and sufficient grid required")
    x = np.logspace(-2.5, 1.7, points)
    # Emission temperature is (1+z) in units where T0=1.  Evaluate emission
    # intensity at emitted frequency (1+z)nu, then reduce photon energy only.
    emitted_x = x
    naive = blackbody_shape(emitted_x) / (1.0 + z)

    def objective(params):
        log_amp, log_temp = params
        amp = math.exp(log_amp)
        temp = math.exp(log_temp)
        model = amp * blackbody_shape(x / temp)
        mask = naive > naive.max() * 1e-8
        return float(np.mean((np.log(model[mask]) - np.log(naive[mask])) ** 2))

    fit = minimize(objective, x0=np.array([0.0, 0.0]), method="Nelder-Mead")
    amp, temp = np.exp(fit.x)
    model = amp * blackbody_shape(x / temp)
    mask = naive > naive.max() * 1e-8
    return float(np.sqrt(np.mean(((model[mask] - naive[mask]) / naive[mask]) ** 2)))


def firas_fractional_energy_injection_limit(mu_limit: float = 47e-6) -> float:
    """Approximate small-distortion energy-injection limit Delta rho/rho≈mu/1.401."""
    if mu_limit <= 0:
        raise ValueError("mu_limit must be positive")
    return mu_limit / 1.401


def static_ap_parameter(z):
    """Alcock-Paczynski F=D_A H_eff/c for exponential static redshift.

    For D=(c/H0)ln(1+z), H_eff=(dD/dz)^-1 c=H0(1+z), and D_A=D.
    """
    z = np.asarray(z, dtype=float)
    if np.any(z < 0):
        raise ValueError("z must be non-negative")
    return (1.0 + z) * np.log1p(z)


def lcdm_ap_parameter(z, omega_m: float = 0.3):
    """Flat-LCDM Alcock-Paczynski parameter D_M(z)H(z)/c."""
    z = np.asarray(z, dtype=float)
    if np.any(z < 0) or not 0 < omega_m < 1:
        raise ValueError("invalid z or omega_m")
    order = np.argsort(z)
    zs = z[order]
    grid = np.r_[0.0, zs]
    E = np.sqrt(omega_m * (1.0 + grid) ** 3 + 1.0 - omega_m)
    chi = cumulative_trapezoid(1.0 / E, grid, initial=0.0)[1:]
    F = chi * E[1:]
    out = np.empty_like(F)
    out[order] = F
    return out


def ap_relative_difference(z, omega_m: float = 0.3):
    z = np.asarray(z, dtype=float)
    ref = lcdm_ap_parameter(z, omega_m)
    out = np.zeros_like(ref)
    mask = ref != 0
    out[mask] = static_ap_parameter(z[mask]) / ref[mask] - 1.0
    return out


def static_optical_redshift_drift(z, H0_km_s_mpc: float = 70.0):
    """dz/dt_obs and spectroscopic velocity drift for n(t)=exp(H0 t)."""
    z = np.asarray(z, dtype=float)
    if np.any(z < 0):
        raise ValueError("z must be non-negative")
    dz_per_year = hubble_fraction_per_year(H0_km_s_mpc) * z
    dv_m_s_year = C_M_S * dz_per_year / (1.0 + z)
    return dz_per_year, dv_m_s_year


def lcdm_redshift_drift(z, H0_km_s_mpc: float = 70.0, omega_m: float = 0.3):
    """Sandage-Loeb drift in flat LCDM."""
    z = np.asarray(z, dtype=float)
    if np.any(z < 0):
        raise ValueError("z must be non-negative")
    E = np.sqrt(omega_m * (1.0 + z) ** 3 + 1.0 - omega_m)
    dz_per_year = hubble_fraction_per_year(H0_km_s_mpc) * ((1.0 + z) - E)
    dv_m_s_year = C_M_S * dz_per_year / (1.0 + z)
    return dz_per_year, dv_m_s_year


def linear_liv_fractional_speed_bound(energy_ev, scale_in_planck: float = 5.9):
    """|delta v/c| ≲ E/E_QG for a linear LIV scale bound."""
    E = np.asarray(energy_ev, dtype=float)
    if np.any(E < 0) or scale_in_planck <= 0:
        raise ValueError("valid energy and scale required")
    return E / (scale_in_planck * E_PLANCK_EV)


def photon_mass_speed_deficit(energy_ev, mass_kg: float = 7.1e-51):
    """Relativistic massive-photon speed deficit 1-v/c≈(mc²/E)²/2."""
    E = np.asarray(energy_ev, dtype=float)
    if np.any(E <= 0) or mass_kg < 0:
        raise ValueError("positive energy and non-negative mass required")
    mc2_ev = mass_kg * C_M_S**2 / 1.602176634e-19
    return 0.5 * (mc2_ev / E) ** 2


def conditional_clock_drift_mismatch(
    H0_km_s_mpc: float = 70.0,
    alpha_drift_limit_per_year: float = 1.1e-18,
):
    """Conditional mismatch if optical-index evolution directly drives alpha.

    This is not a model-independent constraint: a purely disformal cone change
    need not vary alpha.  It applies to gauge-kinetic completions tying the same
    scalar evolution to the electromagnetic coupling.
    """
    if alpha_drift_limit_per_year <= 0:
        raise ValueError("limit must be positive")
    rate = hubble_fraction_per_year(H0_km_s_mpc)
    return {
        "required_fractional_rate_per_year": rate,
        "alpha_clock_limit_per_year": alpha_drift_limit_per_year,
        "mismatch_factor": rate / alpha_drift_limit_per_year,
    }


def comprehensive_audit_results():
    """Return a compact model-class survival matrix with numerical diagnostics."""
    cmb = cmb_temperature_measurement_test()
    clock = conditional_clock_drift_mismatch()
    ap_z = np.array([0.5, 1.0, 2.33])
    ap_diff = ap_relative_difference(ap_z)
    _, drift_static = static_optical_redshift_drift(3.962)
    _, drift_lcdm = lcdm_redshift_drift(3.962)
    return [
        AuditResult(
            "CMB local temperature at z=0.89",
            "post-emission path-only redshift with static radiation bath",
            "FAIL",
            f"{cmb['constant_temperature_pull_sigma']:.1f} sigma",
            "T=5.13±0.06 K versus static 2.725 K",
            "The past radiation bath was physically hotter; redshift cannot occur only after emission.",
        ),
        AuditResult(
            "CMB local temperature scaling",
            "globally evolving optical field",
            "PASS_KINEMATIC",
            f"beta={cmb['inferred_beta']:.3f}±{cmb['inferred_beta_sigma']:.3f}",
            "beta=0",
            "Can pass only by making photon energies evolve everywhere, not merely with traveled circumference.",
        ),
        AuditResult(
            "CMB blackbody preservation",
            "metric-like Liouville transport",
            "PASS",
            f"RMS={liouville_redshift_blackbody_residual(2.0):.2e}",
            "near zero",
            "A coherent achromatic effective metric maps blackbodies to blackbodies.",
        ),
        AuditResult(
            "FIRAS spectral distortion",
            "dissipative/scattering redshift",
            "STRONGLY_CONSTRAINED",
            f"Delta rho/rho≲{firas_fractional_energy_injection_limit():.2e}",
            "|mu|<47e-6",
            "Generic energy exchange or photon conversion must be tiny; a Liouville-preserving branch is the loophole.",
        ),
        AuditResult(
            "BAO Alcock-Paczynski geometry",
            "static exponential Euclidean mapping",
            "FAIL_LIKELY",
            ", ".join(f"z={zz:g}: {dd:+.1%}" for zz, dd in zip(ap_z, ap_diff)),
            "DESI DR2 percent-level distance measurements",
            "The one-function static mapping cannot freely match radial and transverse BAO geometry.",
        ),
        AuditResult(
            "Redshift drift",
            "smooth optical index n(t)=exp(H0t)",
            "FUTURE_DISCRIMINANT",
            f"at z=3.962: {float(drift_static):+.3e} vs LCDM {float(drift_lcdm):+.3e} m/s/yr",
            "current ESPRESSO uncertainty ~3.6 m/s/yr",
            "Current data are far too weak, but the predicted sign differs from LCDM at high redshift.",
        ),
        AuditResult(
            "Energy-dependent dispersion",
            "linear dispersive constitutive law",
            "STRONGLY_CONSTRAINED",
            f"|delta v/c|(1 eV)≲{float(linear_liv_fractional_speed_bound(1.0)):.2e}",
            "E_QG>5.9 E_Pl",
            "Any optical-redshift mechanism relying on appreciable energy dependence is excluded; achromatic models remain.",
        ),
        AuditResult(
            "Massive-photon completion",
            "Proca-like photon mass",
            "FAIL_AS_COSMOLOGICAL_MECHANISM",
            f"1-v/c at 1 eV≲{float(photon_mass_speed_deficit(1.0)):.2e}",
            "m_gamma<7.1e-51 kg",
            "The permitted mass is far too small to generate cosmological optical redshift.",
        ),
        AuditResult(
            "Atomic-clock drift",
            "gauge-kinetic scalar tied to alpha",
            "FAIL_CONDITIONAL",
            f"mismatch {clock['mismatch_factor']:.2e}",
            "|dot alpha/alpha|~1.1e-18/yr",
            "Applies only when the optical background also changes the electromagnetic coupling.",
        ),
        AuditResult(
            "Cosmic birefringence",
            "parity-even disformal metric",
            "PASS_NULL",
            "predicts zero rotation",
            "ACT DR6 tentative beta=0.215±0.074 deg with unresolved systematics",
            "A parity-even model is not excluded; parity-odd constitutive terms are separately testable.",
        ),
        AuditResult(
            "Universal effective metric",
            "all matter, photons and GWs share one evolving geometry",
            "OPEN_BUT_REINTERPRETED",
            "evades differential-speed and WEP tests",
            "must fit CMB+BAO+SN+lensing+growth",
            "This is no longer light stretching in static space; operationally it is metric cosmology.",
        ),
    ]
