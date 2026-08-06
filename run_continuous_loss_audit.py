from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from pdoe.continuous_loss import run_audit

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

report = run_audit()
(RESULTS / "v7_continuous_loss_audit.json").write_text(
    json.dumps(report, indent=2) + "\n", encoding="utf-8"
)
pd.DataFrame(report["tests"]).to_csv(
    RESULTS / "v7_continuous_loss_test_matrix.csv", index=False
)
pd.DataFrame(report["diagnostics"]["bao"]).to_csv(
    RESULTS / "v7_continuous_loss_bao_geometry.csv", index=False
)
print(json.dumps(report, indent=2))
