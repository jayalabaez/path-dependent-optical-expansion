from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / "src"))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pdoe.comprehensive import (
    ap_relative_difference,
    blackbody_shape,
    cmb_temperature_measurement_test,
    comprehensive_audit_results,
    lcdm_redshift_drift,
    static_optical_redshift_drift,
)

ROOT = Path(__file__).parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

matrix = pd.DataFrame([r.to_dict() for r in comprehensive_audit_results()])
matrix.to_csv(OUT / "v4_comprehensive_matrix.csv", index=False)

cmb = pd.DataFrame([cmb_temperature_measurement_test()])
cmb.to_csv(OUT / "cmb_temperature_test.csv", index=False)

z = np.linspace(0.01, 2.5, 600)
plt.figure(figsize=(9, 5))
plt.plot(z, 100 * ap_relative_difference(z))
plt.axhline(0, linewidth=1)
plt.xlabel("redshift z")
plt.ylabel("static AP difference from flat LCDM [%]")
plt.title("Static exponential mapping: radial/transverse BAO consistency test")
plt.tight_layout()
plt.savefig(OUT / "bao_ap_static_vs_lcdm.png", dpi=180)
plt.close()

z_drift = np.linspace(0.01, 5.0, 700)
_, v_opt = static_optical_redshift_drift(z_drift)
_, v_lcdm = lcdm_redshift_drift(z_drift)
plt.figure(figsize=(9, 5))
plt.plot(z_drift, v_opt, label="smooth optical-index static model")
plt.plot(z_drift, v_lcdm, label="flat LCDM")
plt.axhline(0, linewidth=1)
plt.xlabel("redshift z")
plt.ylabel("spectroscopic velocity drift [m/s/year]")
plt.title("Redshift drift: future sign test")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "redshift_drift_discriminator.png", dpi=180)
plt.close()

x = np.logspace(-2.5, 1.7, 1000)
plt.figure(figsize=(9, 5))
plt.loglog(x, blackbody_shape(x))
plt.xlabel("dimensionless frequency hν/kT")
plt.ylabel("dimensionless spectral intensity")
plt.title("Metric-like Liouville redshift preserves the Planck spectrum")
plt.tight_layout()
plt.savefig(OUT / "blackbody_liouville_invariance.png", dpi=180)
plt.close()

print(matrix[["test", "model_class", "status"]].to_string(index=False))
print("\nOverall verdict:")
print("1. Circumference and smooth photon-only static branches remain falsified.")
print("2. Dispersive, massive-photon, dissipative, and gauge-kinetic variants are strongly constrained or excluded.")
print("3. Only a coherent achromatic universal effective metric remains broadly viable; that is operationally an evolving geometry, not light stretching through static space.")
