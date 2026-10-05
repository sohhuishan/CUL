from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
ACTUAL_DIR = ROOT / "data" / "actual"
SAMPLE_FILE = ROOT / "data" / "sample" / "accrual_vs_actual.csv"
REPORTS = ROOT / "reports"
MATERIAL_PCT = 0.10
MATERIAL_USD = 10_000
AGED_DAYS = 90
