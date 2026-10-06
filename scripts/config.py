"""Settings. Folders come from env vars or config.local.json (git-ignored); defaults keep everything inside the repo."""
import os, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
_f = ROOT / "config.local.json"
CFG = json.loads(_f.read_text(encoding="utf-8-sig")) if _f.exists() else {}

def _pick(key, default):
    v = os.environ.get(key) or CFG.get(key)
    return Path(v).expanduser() if v else default

ACTUAL_DIR = _pick("CUL_DATA_DIR", ROOT / "data" / "actual")          # real OPUS exports (CSV)
REPORTS = _pick("CUL_REPORTS_DIR", ROOT / "reports")                  # dashboard, deck, findings page
FINDINGS_DIR = _pick("CUL_FINDINGS_DIR", ROOT / "docs" / "findings")  # one .md per finding
EMAIL_TO = os.environ.get("CUL_EMAIL_TO") or CFG.get("CUL_EMAIL_TO") or ""
EXTERNAL = FINDINGS_DIR != ROOT / "docs" / "findings"                 # true on the company PC: no git, no push
SAMPLE_FILE = ROOT / "data" / "sample" / "accrual_vs_actual.csv"
MATERIAL_PCT = 0.10
MATERIAL_USD = 10_000
AGED_DAYS = 90
