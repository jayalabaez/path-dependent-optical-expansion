from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pdoe.falsification import (
    gw170817_falsification,
    static_euclidean_distance_duality_eta,
    static_optical_hubble_times,
)

ROOT = Path(__file__).parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

result = gw170817_falsification()
pd.DataFrame([result]).to_csv(OUT / "gw170817_falsification.csv", index=False)

z = np.linspace(1e-4, 2.0, 800)
_, _, advance = static_optical_hubble_times(z)
advance_years = advance / (365.25 * 86400.0)

plt.figure(figsize=(9, 5))
plt.loglog(z, advance_years)
plt.scatter([result["z_host"]], [result["predicted_photon_advance_years"]], label="GW170817 host")
plt.xlabel("optical redshift z")
plt.ylabel("predicted photon advance over standard-metric GW [years]")
plt.title("Minimal static photon-only optical-redshift model")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "gw170817_predicted_advance.png", dpi=180)
plt.close()

eta = static_euclidean_distance_duality_eta(z)
plt.figure(figsize=(9, 5))
plt.plot(z, eta, label=r"static Euclidean $\eta=1/(1+z)$")
plt.axhline(1.0, linestyle="--", label="Etherington relation")
plt.xlabel("redshift z")
plt.ylabel(r"$\eta=D_L/[(1+z)^2D_A]$")
plt.title("Static Euclidean optical redshift violates distance duality")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "distance_duality_failure.png", dpi=180)
plt.close()

checks = pd.DataFrame(
    [
        {
            "test": "GW170817 propagation timing",
            "branch": "smooth homogeneous photon-only static optical redshift",
            "result": "FALSIFIED",
            "reason": f"predicts photon advance of {result['predicted_photon_advance_years']:.0f} years vs 1.74 s observed GW-to-gamma lag",
        },
        {
            "test": "GW170817 speed bound",
            "branch": "smooth photon-only optical contribution at z~0.0098",
            "result": "CONSTRAINED",
            "reason": f"local smooth optical fraction < {result['max_smooth_local_optical_fraction_of_redshift']:.2e} under the linearized shared-history assumption",
        },
        {
            "test": "supernova time dilation",
            "branch": "homogeneous time-varying index",
            "result": "PASSES KINEMATICALLY",
            "reason": "null-path mapping gives dt_obs/dt_emit=1+z",
        },
        {
            "test": "cosmic distance duality",
            "branch": "static Euclidean photon-number-conserving optical redshift",
            "result": "FALSIFIED UNLESS FOCUSING IS MODIFIED",
            "reason": "predicts eta=1/(1+z), not eta=1",
        },
        {
            "test": "universal shared optical metric",
            "branch": "photons and GWs couple identically",
            "result": "NOT FALSIFIED BY GW170817",
            "reason": "but the model is no longer photon-specific and behaves like an evolving effective metric",
        },
    ]
)
checks.to_csv(OUT / "v3_falsification_matrix.csv", index=False)

print(pd.DataFrame([result]).T.to_string(header=False))
print("\n", checks.to_string(index=False))
