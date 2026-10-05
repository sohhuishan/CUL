#!/usr/bin/env bash
# Rebuild analysis, dashboard, deck and email summary. Usage: bash scripts/run_daily.sh
set -euo pipefail
cd "$(dirname "$0")"
python3 -c "import pptx, pandas" 2>/dev/null || pip install -q python-pptx pandas
python3 build_dashboard.py && python3 build_ppt.py && python3 build_email.py
