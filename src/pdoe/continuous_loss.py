from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Literal

from scipy.integrate import quad

C = 299_792_458.0
MPC_M = 3.085677581491367e22
YEAR_S = 365.25 * 86400.0
T_CMB0_K = 2.72548


@dataclass(frozen=True)
class TestResult:
    name: str
    status: Literal["FALSIFIED", "CONSTRAINED", "PASS", "OPEN", "FUTURE_TEST"]
    statistic: float
    unit: str
    threshold: float | None
    note: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def h0_si(h0_km_s_mpc: float = 70.0) -> float:
    return h0_km_s_mpc * 1000.0 / MPC_M


def loss_coefficient_per_m(h0_km_s_mpc: float = 70.0) -> float:
    return h0_si(h0_km_s_mpc) / C


def redshift_from_distance(distance_m: float, h0_km_s_mpc: float = 70.0) -> float:
    if distance_m < 0:
        raise ValueError("distance_m must be non-negative")
    return math.expm1(loss_coefficient_per_m(h0_km_s_mpc) * distance_m)


def distance_from_redshift(z: float, h0_km_s_mpc: float = 70.0) -> float:
    if z < 0:
        raise ValueError("z must be non-negative")
    return math.log1p(z) / loss_coefficient_per_m(h0_km_s_mpc)


def photon_energy_ratio(z: float) -> float:
    if z < 0:
        raise ValueError("z must be non-negative")
    return 1.0 / (1.0 + z)


def static_luminosity_distance(
    distance_m: float, z: float, time_dilation_exponent: float
) -> float:
    """Static Euclidean D_L from energy loss and optional rate stretching."""
    return distance_m * (1.0 + z) ** ((1.0 + time_dilation_exponent) / 2.0)


def distance_duality_eta(z: float, time_dilation_exponent: float) -> float:
    """D_L / [(1+z)^2 D_A] for static Euclidean D_A=r."""
    return (1.0 + z) ** ((time_dilation_exponent - 3.0) / 2.0)


def tolman_surface_brightness_ratio(z: float, time_dilation_exponent: float) -> float:
    return (1.0 + z) ** (-(1.0 + time_dilation_exponent))


def time_dilation_significance(
    predicted_b: float,
    observed_b: float = 1.003,
    statistical_sigma: float = 0.005,
    systematic_sigma: float = 0.010,
) -> float:
    return abs(predicted_b - observed_b) / math.hypot(
        statistical_sigma, systematic_sigma
    )


def cmb_temperature_significance(
    predicted_k: float, observed_k: float = 5.13, sigma_k: float = 0.06
) -> float:
    return abs(predicted_k - observed_k) / sigma_k


def equivalent_linear_eta0_at_z1(time_dilation_exponent: float) -> float:
    return distance_duality_eta(1.0, time_dilation_exponent) - 1.0


def eta0_significance(
    predicted_eta0: float, observed_eta0: float = 0.022, sigma_eta0: float = 0.025
) -> float:
    """Single-point P1 diagnostic, not a replacement for a full likelihood."""
    return abs(predicted_eta0 - observed_eta0) / sigma_eta0


def required_stochastic_events(z: float, max_sigma_ln_energy: float) -> float:
    """Minimum Poisson events for a fixed mean logarithmic energy loss."""
    if z <= 0 or max_sigma_ln_energy <= 0:
        raise ValueError("z and max_sigma_ln_energy must be positive")
    return (math.log1p(z) / max_sigma_ln_energy) ** 2


def per_event_log_loss(z: float, n_events: float) -> float:
    if z <= 0 or n_events <= 0:
        raise ValueError("z and n_events must be positive")
    return math.log1p(z) / n_events


def lcdm_e(z: float, omega_m: float = 0.3) -> float:
    return math.sqrt(omega_m * (1.0 + z) ** 3 + 1.0 - omega_m)


def lcdm_dimensionless_comoving_distance(z: float, omega_m: float = 0.3) -> float:
    return quad(lambda x: 1.0 / lcdm_e(x, omega_m), 0.0, z, epsabs=1e-12)[0]


def f_ap_static_loss(z: float) -> float:
    return (1.0 + z) * math.log1p(z)


def f_ap_lcdm(z: float, omega_m: float = 0.3) -> float:
    return lcdm_dimensionless_comoving_distance(z, omega_m) * lcdm_e(z, omega_m)


def static_loss_redshift_drift_per_year(z: float) -> float:
    if z < 0:
        raise ValueError("z must be non-negative")
    return 0.0


def lcdm_redshift_drift_per_year(
    z: float, h0_km_s_mpc: float = 70.0, omega_m: float = 0.3
) -> float:
    return h0_si(h0_km_s_mpc) * ((1.0 + z) - lcdm_e(z, omega_m)) * YEAR_S


def velocity_drift_m_s_per_year(z: float, dz_per_year: float) -> float:
    return C * dz_per_year / (1.0 + z)


def local_fractional_shift(distance_m: float, h0_km_s_mpc: float = 70.0) -> float:
    return redshift_from_distance(distance_m, h0_km_s_mpc)


def run_audit() -> dict[str, object]:
    pure_b = 0.0
    engineered_b = 1.0
    time_sigma = time_dilation_significance(pure_b)
    engineered_time_sigma = time_dilation_significance(engineered_b)

    static_cmb_sigma = cmb_temperature_significance(T_CMB0_K)
    expected_cmb = T_CMB0_K * 1.89
    evolving_cmb_sigma = cmb_temperature_significance(expected_cmb)

    eta_sigma_pure = eta0_significance(equivalent_linear_eta0_at_z1(pure_b))
    eta_sigma_engineered = eta0_significance(
        equivalent_linear_eta0_at_z1(engineered_b)
    )

    resolution = 140_000.0
    n_events = required_stochastic_events(1.0, 1.0 / resolution)
    event_loss = per_event_log_loss(1.0, n_events)

    bao_rows = []
    for z in (0.5, 1.0, 2.33):
        static = f_ap_static_loss(z)
        lcdm = f_ap_lcdm(z)
        bao_rows.append(
            {
                "z": z,
                "f_ap_static": static,
                "f_ap_lcdm": lcdm,
                "fractional_difference": static / lcdm - 1.0,
            }
        )

    z_drift = 3.962
    lcdm_dz = lcdm_redshift_drift_per_year(z_drift)
    lcdm_dv = velocity_drift_m_s_per_year(z_drift, lcdm_dz)

    tests = [
        TestResult(
            "DES supernova time dilation: pure energy-loss model",
            "FALSIFIED",
            time_sigma,
            "sigma",
            5.0,
            "Pure energy loss predicts b=0; DES measures b=1.003±0.005(stat)±0.010(sys).",
        ),
        TestResult(
            "DES time dilation: engineered pulse-stretch variant",
            "PASS",
            engineered_time_sigma,
            "sigma",
            2.0,
            "An independent (1+z) pulse stretch passes this observable but is not pure energy loss.",
        ),
        TestResult(
            "CMB temperature at z=0.89: path-only static bath",
            "FALSIFIED",
            static_cmb_sigma,
            "sigma",
            5.0,
            "A path-only model predicts T0; ALMA measures 5.13±0.06 K.",
        ),
        TestResult(
            "CMB temperature: globally evolving radiation field",
            "PASS",
            evolving_cmb_sigma,
            "sigma",
            2.0,
            "T(z)=T0(1+z) passes but requires global evolution rather than distance-only loss.",
        ),
        TestResult(
            "Distance duality: pure energy-loss static geometry",
            "FALSIFIED",
            eta_sigma_pure,
            "sigma diagnostic",
            5.0,
            "At z=1 eta=2^-3/2, far from PantheonPlus+BAO eta≈1.",
        ),
        TestResult(
            "Distance duality: energy loss plus pulse stretch",
            "FALSIFIED",
            eta_sigma_engineered,
            "sigma diagnostic",
            5.0,
            "Adding time dilation gives eta(z=1)=1/2; focusing/geometry must also evolve.",
        ),
        TestResult(
            "Stochastic collision broadening at z=1",
            "CONSTRAINED",
            n_events,
            "minimum events",
            1.0e9,
            "At R=140,000, a Poisson collision model needs about 10^10 tiny events.",
        ),
        TestResult(
            "Stationary redshift drift",
            "FUTURE_TEST",
            0.0,
            "dz/yr",
            None,
            "A stationary path-loss law predicts zero drift; current ESPRESSO precision is insufficient.",
        ),
        TestResult(
            "BAO Alcock-Paczynski geometry at z=2.33",
            "FALSIFIED",
            abs(bao_rows[-1]["fractional_difference"]),
            "fraction",
            0.02,
            "Static r∝ln(1+z) differs by about 11%, above percent-level Ly-alpha BAO precision.",
        ),
    ]

    fatal = [test.name for test in tests if test.status == "FALSIFIED"]
    return {
        "model": {
            "name": "stationary continuous fractional photon-energy loss",
            "law": "dE/dr=-(H0/c)E",
            "distance_redshift": "1+z=exp(H0 r/c)",
            "photon_speed_changed": False,
            "pure_model_time_dilation_exponent": pure_b,
        },
        "constants": {
            "H0_km_s_Mpc": 70.0,
            "loss_coefficient_per_m": loss_coefficient_per_m(),
            "loss_length_Gpc": 1.0 / loss_coefficient_per_m() / (1e3 * MPC_M),
            "one_AU_fractional_shift": local_fractional_shift(149_597_870_700.0),
        },
        "diagnostics": {
            "time_dilation_sigma_pure": time_sigma,
            "time_dilation_sigma_engineered": engineered_time_sigma,
            "cmb_static_sigma": static_cmb_sigma,
            "cmb_evolving_sigma": evolving_cmb_sigma,
            "distance_duality_eta_z1_pure": distance_duality_eta(1.0, pure_b),
            "distance_duality_eta_z1_engineered": distance_duality_eta(
                1.0, engineered_b
            ),
            "distance_duality_sigma_pure": eta_sigma_pure,
            "distance_duality_sigma_engineered": eta_sigma_engineered,
            "stochastic_min_events_z1_R140k": n_events,
            "stochastic_max_log_loss_per_event": event_loss,
            "bao": bao_rows,
            "redshift_drift_z3p962": {
                "static_loss_dz_per_year": 0.0,
                "lcdm_dz_per_year": lcdm_dz,
                "lcdm_velocity_drift_m_s_per_year": lcdm_dv,
                "current_espresso_velocity_m_s_per_year": -3.5,
                "current_espresso_sigma_m_s_per_year": 3.6,
            },
        },
        "tests": [test.to_dict() for test in tests],
        "n_tests": len(tests),
        "n_falsified": len(fatal),
        "fatal_tests": fatal,
        "verdict": (
            "The pure stationary continuous photon-energy-loss model is falsified. "
            "Repairing it requires pulse stretching, global radiation-temperature "
            "evolution, and evolving focusing/geometry, which turns it into an "
            "effective metric cosmology rather than simple tired light."
        ),
        "whole_new_physics_confirmed": False,
    }
