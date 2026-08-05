from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

from pdoe.audit import branch_audit
from pdoe.models import (
    arrival_delay_seconds,
    beam_expansion_redshift,
    calibrated_distance_modulus_residual,
    conformal_photon_speed,
    disformal_photon_speed,
    gauge_kinetic_wkb_amplitude,
    lcdm_luminosity_distance,
    measured_crest_spacing,
    required_static_speed_ratio,
    spherical_wave,
    static_luminosity_distance,
    stationary_frequency,
)

ROOT = Path(__file__).parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

# 1. Standard spherical propagation: amplitude changes, wavelength does not.
r = np.linspace(1.0, 50.0, 20_000)
wave = spherical_wave(r, wavelength=1.0)
spacing = measured_crest_spacing(r, wave)
plt.figure(figsize=(9, 5))
plt.plot(r, r * wave)
plt.xlabel("radius r")
plt.ylabel("envelope-compensated field rE")
plt.title("Ordinary spherical propagation: constant radial crest spacing")
plt.tight_layout()
plt.savefig(OUT / "spherical_wave_constant_wavelength.png", dpi=180)
plt.close()

# 2. Rejected circumference branch: arbitrary reference radius.
r_beam = np.logspace(0, 25, 600)
plt.figure(figsize=(9, 5))
for r0 in [1.0, 1e6, 1e12]:
    plt.loglog(r_beam, 1 + beam_expansion_redshift(r_beam, r0, 0.012), label=f"r0={r0:g}")
plt.xlabel("radius in common units")
plt.ylabel("1+z")
plt.title("Rejected beam-expansion law depends on arbitrary launch radius")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "arbitrary_origin_failure.png", dpi=180)
plt.close()

# 3. Gauge-kinetic scalar prefactor: amplitude responds, phase spacing does not.
x = np.linspace(0.0, 100.0, 2000)
B = 1.0 + 0.5 * (1.0 + np.tanh((x - 50.0) / 8.0))
amp = gauge_kinetic_wkb_amplitude(B)
phase = 2.0 * np.pi * x / 5.0
field = amp * np.cos(phase)
plt.figure(figsize=(9, 5))
plt.plot(x, field, label="WKB field")
plt.plot(x, amp, linestyle="--", label="amplitude envelope")
plt.plot(x, -amp, linestyle="--")
plt.xlabel("propagation coordinate")
plt.ylabel("field")
plt.title("B(phi)F^2 coupling: amplitude changes while wavelength stays fixed")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "gauge_kinetic_amplitude_only.png", dpi=180)
plt.close()

# 4. Stationary conservative no-go benchmark.
lam = np.linspace(0.0, 10.0, 300)
omega = stationary_frequency(1.0, lam)
plt.figure(figsize=(9, 5))
plt.plot(lam, omega)
plt.xlabel("affine parameter")
plt.ylabel("normalized frequency")
plt.ylim(0.95, 1.05)
plt.title("Stationary local conservative propagation: k_t is conserved")
plt.tight_layout()
plt.savefig(OUT / "stationary_no_go.png", dpi=180)
plt.close()

# 5. Disformal branch: quantify the speed evolution needed in a static universe.
z_req = np.linspace(0.0, 2.5, 500)
ratio = required_static_speed_ratio(z_req)
plt.figure(figsize=(9, 5))
plt.plot(z_req, ratio - 1.0)
plt.yscale("log")
plt.xlim(0.001, 2.5)
plt.ylim(1e-4, 3)
plt.xlabel("redshift z")
plt.ylabel("required fractional endpoint speed change")
plt.title("Static disformal explanation requires c_emit/c_obs - 1 = z")
plt.tight_layout()
plt.savefig(OUT / "disformal_static_requirement.png", dpi=180)
plt.close()

# Illustrative multimessenger delay for persistent speed differences.
distances = np.array([40.0, 100.0, 1000.0])
deltas = np.array([1e-15, 1e-9, 1e-3])
delay_rows = []
for d in distances:
    for delta in deltas:
        delay_rows.append(
            {
                "distance_mpc": d,
                "fractional_speed_difference": delta,
                "arrival_delay_seconds": float(arrival_delay_seconds(d, delta)),
            }
        )
pd.DataFrame(delay_rows).to_csv(OUT / "multimessenger_delay_scale.csv", index=False)

# 6. Hubble-shape diagnostic only (not an observational likelihood).
z = np.linspace(0.01, 2.26, 700)
ref = lcdm_luminosity_distance(z)


def score(p):
    residual = calibrated_distance_modulus_residual(static_luminosity_distance(z, p), ref)
    return float(np.mean(residual**2))


fit = minimize_scalar(score, bounds=(-1.0, 3.0), method="bounded")
shape_rows = []
plt.figure(figsize=(9, 5))
for name, p in [("energy-only", 0.5), ("inserted-time-factor", 1.0), ("best-shape", fit.x)]:
    residual = calibrated_distance_modulus_residual(static_luminosity_distance(z, p), ref)
    shape_rows.append(
        {
            "model": name,
            "p": p,
            "rms_mag_vs_LCDM_shape": np.sqrt(np.mean(residual**2)),
            "max_abs_mag_vs_LCDM_shape": np.max(np.abs(residual)),
            "warning": "benchmark-curve comparison, not a fit to supernova data",
        }
    )
    plt.plot(z, residual, label=f"{name}, p={p:.4f}")
plt.axhline(0.0, linewidth=1)
plt.xlabel("redshift z")
plt.ylabel("intercept-calibrated residual vs flat LCDM [mag]")
plt.title("Phenomenological shape degeneracy only—not an observational fit")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "hubble_shape_diagnostic.png", dpi=180)
plt.close()

# 7. Summary artifacts.
pd.DataFrame(shape_rows).to_csv(OUT / "shape_diagnostic.csv", index=False)
pd.DataFrame(branch_audit()).to_csv(OUT / "branch_audit.csv", index=False)
summary = pd.DataFrame(
    [
        {"diagnostic": "mean_spherical_crest_spacing", "value": spacing.mean(), "expected": 1.0},
        {"diagnostic": "std_spherical_crest_spacing", "value": spacing.std(), "expected": 0.0},
        {"diagnostic": "pure_conformal_speed", "value": float(conformal_photon_speed(3.0)), "expected": 1.0},
        {"diagnostic": "disformal_speed_q_0p1", "value": float(disformal_photon_speed(0.1)), "expected": np.sqrt(0.9)},
        {"diagnostic": "best_static_shape_p", "value": fit.x, "expected": "diagnostic only"},
    ]
)
summary.to_csv(OUT / "summary.csv", index=False)

print(summary.to_string(index=False))
print("\nBranch audit:")
print(pd.DataFrame(branch_audit())[["branch", "status"]].to_string(index=False))
print("\nVerdict: distance-only redshift in a static, stationary, local conservative vacuum is ruled out by the symmetry/no-go assumptions. The only retained core branch is an evolving disformal/constitutive optical background, which is no longer circumference-driven and is strongly constrained.")
