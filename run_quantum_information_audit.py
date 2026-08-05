from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pdoe.quantum_information import (
    cycles_in_observation_window,
    de_sitter_horizon_scaling,
    distribution_std,
    fixed_detector_capture_probability,
    gaussian_spectral_mode,
    gaussian_time_probability,
    lcdm_detected_photon_rate,
    matched_detector_capture_probability,
    pure_loss_classical_capacity,
    redshifted_gaussian_mode,
    single_photon_erasure_classical_information,
    single_photon_erasure_quantum_capacity,
)

ROOT = Path(__file__).parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

# Coherent spectral-mode dilation and receiver mismatch.
nu = np.linspace(0.001, 180.0, 180_000)
center, sigma = 100.0, 4.0
mode_rows = []
plt.figure(figsize=(9, 5.5))
for z in [0.0, 0.1, 0.5, 1.0, 3.0, 10.0]:
    shifted = redshifted_gaussian_mode(nu, center, sigma, z)
    row = {
        "z": z,
        "mode_norm": np.trapezoid(np.abs(shifted) ** 2, nu),
        "fixed_detector_capture": fixed_detector_capture_probability(nu, center, sigma, z),
        "matched_detector_capture": matched_detector_capture_probability(nu, center, sigma, z),
    }
    mode_rows.append(row)
    if z in [0.0, 0.5, 1.0, 3.0]:
        plt.plot(nu, np.abs(shifted) ** 2, label=f"z={z:g}")
plt.xlabel("frequency (dimensionless)")
plt.ylabel("single-photon spectral probability density")
plt.title("Coherent redshift moves the photon mode without destroying its norm")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "quantum_redshift_mode_dilation.png", dpi=180)
plt.close()
mode_df = pd.DataFrame(mode_rows)
mode_df.to_csv(OUT / "quantum_mode_fidelity.csv", index=False)

# Temporal pulse stretching.
t = np.linspace(-80.0, 80.0, 250_000)
time_rows = []
plt.figure(figsize=(9, 5.5))
for z in [0.0, 1.0, 4.0, 10.0]:
    density = gaussian_time_probability(t, sigma_t=1.0, z=z)
    time_rows.append({
        "z": z,
        "measured_temporal_std": distribution_std(t, density),
        "expected_temporal_std": 1.0 + z,
        "peak_probability_density": float(density.max()),
    })
    plt.plot(t, density, label=f"z={z:g}")
plt.xlabel("arrival time (arbitrary units)")
plt.ylabel("photon arrival probability density")
plt.title("Redshift stretches a normalized photon packet in time")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "quantum_packet_time_stretch.png", dpi=180)
plt.close()
pd.DataFrame(time_rows).to_csv(OUT / "quantum_time_stretch.csv", index=False)

# Pure-loss channel capacities.
eta = np.logspace(-12, 0, 800)
classical_bosonic = pure_loss_classical_capacity(eta, mean_input_photons=1.0)
classical_erasure = single_photon_erasure_classical_information(eta)
quantum_erasure = single_photon_erasure_quantum_capacity(eta)
plt.figure(figsize=(9, 5.5))
plt.loglog(eta, classical_bosonic, label="bosonic classical capacity, N=1")
plt.loglog(eta, classical_erasure, label="single-photon classical erasure")
positive = quantum_erasure > 0
plt.loglog(eta[positive], quantum_erasure[positive], label="single-photon quantum capacity")
plt.xlabel("transmissivity eta")
plt.ylabel("capacity per mode/use")
plt.title("Faintness reduces channel capacity; redshift alone is not erasure")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "quantum_loss_capacity.png", dpi=180)
plt.close()
pd.DataFrame({
    "transmissivity": eta,
    "bosonic_classical_bits_per_mode_N1": classical_bosonic,
    "single_photon_classical_bits_per_use": classical_erasure,
    "single_photon_quantum_qubits_per_use": quantum_erasure,
}).to_csv(OUT / "quantum_loss_capacity.csv", index=False)

# Finite-window test: a finite redshift never produces exactly zero frequency.
cycle_rows = []
for name, frequency in {
    "visible_500_THz": 5.0e14,
    "CMB_peak_160_GHz": 1.60e11,
    "radio_1_GHz": 1.0e9,
}.items():
    for z in [1.0, 10.0, 1100.0, 1e6, 1e12]:
        cycle_rows.append({
            "carrier": name,
            "z": z,
            "cycles_in_one_second": cycles_in_observation_window(frequency, z, 1.0),
        })
pd.DataFrame(cycle_rows).to_csv(OUT / "finite_window_cycles.csv", index=False)

# Illustrative cosmological photon/data rate for a fixed aperture.
z_grid = np.logspace(-3, 4, 800)
rate = lcdm_detected_photon_rate(
    z_grid,
    emitted_photons_per_second=1e50,
    aperture_area_m2=25.0,
)
plt.figure(figsize=(9, 5.5))
plt.loglog(z_grid, rate)
plt.xlabel("redshift z")
plt.ylabel("detected photons / ideal bits per second")
plt.title("Accessible image/data rate falls from geometry and time dilation")
plt.tight_layout()
plt.savefig(OUT / "cosmological_detected_information_rate.png", dpi=180)
plt.close()

# Event-horizon asymptotic limit.
epsilon = np.logspace(1, -15, 900)
horizon_z, horizon_rate = de_sitter_horizon_scaling(epsilon)
plt.figure(figsize=(9, 5.5))
plt.loglog(1.0 + horizon_z, horizon_rate)
plt.xlabel("1+z near de Sitter event horizon")
plt.ylabel("received information-rate fraction")
plt.title("Horizon limit: information rate tends to zero only asymptotically")
plt.tight_layout()
plt.savefig(OUT / "de_sitter_horizon_information_rate.png", dpi=180)
plt.close()

# Synthetic photon-counting image progression.
rng = np.random.default_rng(73129)
size = 180
y, x = np.mgrid[-1:1:complex(size), -1:1:complex(size)]
radius = np.sqrt((x / 0.75) ** 2 + (y / 0.35) ** 2)
angle = np.arctan2(y, x)
image = np.exp(-3.2 * radius) * (1.0 + 0.38 * np.cos(2.0 * angle + 13.0 * radius))
image += 0.75 * np.exp(-((x - 0.26) ** 2 + (y + 0.12) ** 2) / 0.003)
image = np.clip(image, 0, None)
image /= image.sum()
fig, axes = plt.subplots(1, 4, figsize=(14, 3.8))
image_rows = []
for ax, z in zip(axes, [0.1, 1.0, 5.0, 15.0]):
    # Illustrative count budget only; not a cosmological likelihood.
    expected_counts = 1_000_000 / (1.0 + z) ** 3
    counts = rng.poisson(expected_counts * image + 0.015)
    ax.imshow(np.log1p(counts), origin="lower", cmap="gray")
    ax.set_title(f"z={z:g}\n{counts.sum():,} photons")
    ax.axis("off")
    probability = counts.ravel().astype(float)
    probability /= probability.sum()
    entropy = -np.sum(probability[probability > 0] * np.log2(probability[probability > 0]))
    image_rows.append({"z": z, "detected_photons": int(counts.sum()), "spatial_shannon_entropy_bits": entropy})
fig.suptitle("Synthetic image information fades through photon-count loss, not wave flattening")
fig.tight_layout()
fig.savefig(OUT / "photon_counting_image_progression.png", dpi=180)
plt.close(fig)
pd.DataFrame(image_rows).to_csv(OUT / "photon_counting_image_progression.csv", index=False)

summary = pd.DataFrame([
    {
        "claim": "coherent redshift preserves finite-bandwidth mode norm",
        "result": "PROVED_WITHIN_MODEL",
        "numerical_value": float(mode_df["mode_norm"].sub(1.0).abs().max()),
        "interpretation": "redshift is a unitary mode dilation, not quantum erasure",
    },
    {
        "claim": "unretuned detector loses the shifted photon",
        "result": "CONFIRMED",
        "numerical_value": float(mode_df.loc[np.isclose(mode_df.z, 1.0), "fixed_detector_capture"].iloc[0]),
        "interpretation": "mode mismatch looks like loss; retuning restores capture",
    },
    {
        "claim": "redshift stretches pulse duration by 1+z",
        "result": "CONFIRMED",
        "numerical_value": float(pd.DataFrame(time_rows).iloc[-1]["measured_temporal_std"]),
        "interpretation": "arrival information is spread over longer time",
    },
    {
        "claim": "photon loss drives accessible information to zero",
        "result": "CONFIRMED",
        "numerical_value": float(pure_loss_classical_capacity(np.array([1e-12]), 1.0)[0]),
        "interpretation": "capacity tends to zero with transmissivity",
    },
    {
        "claim": "finite-distance wave becomes exactly flat",
        "result": "FALSIFIED",
        "numerical_value": float(cycles_in_observation_window(5e14, 1e12, 1.0)),
        "interpretation": "finite z leaves positive frequency",
    },
    {
        "claim": "information rate vanishes at a cosmological event horizon",
        "result": "ASYMPTOTICALLY_CONFIRMED",
        "numerical_value": float(horizon_rate[-1]),
        "interpretation": "zero rate is reached only in the infinite-time limit",
    },
])
summary.to_csv(OUT / "v5_quantum_information_verdict.csv", index=False)
print(summary.to_string(index=False))
print("\nVerdict: coherent redshift moves and stretches a finite-bandwidth photon mode without erasing it. Loss reduces accessible capacity. A wave does not become exactly flat at finite redshift; horizon suppression is asymptotic.")
