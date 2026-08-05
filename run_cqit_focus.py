from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pdoe.cqit import (
    candidate_new_physics_flag,
    conditional_bell_fidelity,
    novelty_classification,
    standard_channel_budget,
)

ROOT = Path(__file__).parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

# Receiver-relative information budget across redshift and loss.
z_values = np.array([0.0, 0.1, 1.0, 3.0, 10.0])
eta_values = np.array([1.0, 0.5, 0.1, 1e-3])
rows = []
for z in z_values:
    for eta in eta_values:
        budget = standard_channel_budget(1e6, z, eta)
        rows.append(budget.as_dict())
pd.DataFrame(rows).to_csv(OUT / "v6_cqit_channel_budget.csv", index=False)

# Plot classical accessible rate; this is receiver-resource dependent.
plt.figure(figsize=(9, 5))
for eta in eta_values:
    z = np.logspace(-3, 2, 500)
    rate = np.array([standard_channel_budget(1e6, float(zi), float(eta)).classical_bits_per_second for zi in z])
    plt.loglog(1 + z, rate, label=f"eta={eta:g}")
plt.xlabel("1+z")
plt.ylabel("accessible classical rate [bits/s]")
plt.title("CQIT null model: redshift slows modes; loss erases detections")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "v6_cqit_accessible_rate.png", dpi=180)
plt.close()

# Polarization residual target: common redshift does nothing, differential
# rotation/dephasing creates a measurable conditional-state anomaly.
angles = np.linspace(0, np.pi / 2, 400)
fidelity = np.array([conditional_bell_fidelity(a) for a in angles])
plt.figure(figsize=(9, 5))
plt.plot(angles, fidelity)
plt.xlabel("differential polarization rotation [rad]")
plt.ylabel("conditional Bell-state fidelity")
plt.title("New-physics target: polarization-dependent residual after calibration")
plt.tight_layout()
plt.savefig(OUT / "v6_cqit_bell_fidelity_residual.png", dpi=180)
plt.close()

novelty = pd.DataFrame(novelty_classification())
novelty.to_csv(OUT / "v6_novelty_map.csv", index=False)

# Demonstrate conservative triage behavior, not a discovery claim.
examples = pd.DataFrame(
    [
        {"case": "standard_null", "significances": "0.2,-0.4,1.1", "flag": candidate_new_physics_flag([0.2, -0.4, 1.1])},
        {"case": "single_outlier", "significances": "5.4,0.3,-0.8", "flag": candidate_new_physics_flag([5.4, 0.3, -0.8])},
        {"case": "two_independent_residuals", "significances": "5.4,-6.2,0.4", "flag": candidate_new_physics_flag([5.4, -6.2, 0.4])},
    ]
)
examples.to_csv(OUT / "v6_candidate_residual_screen.csv", index=False)

print("CQIT v6 focus audit")
print("===================")
print(novelty.to_string(index=False))
print("\nVerdict: the redshift-information effect is real but established physics. The new focus is a null-test framework for residuals beyond coherent dilation, loss, detector mismatch, and known noise.")
