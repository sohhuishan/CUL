# CUL — Cost Control workspace

Owner: Cost Controller, container shipping. Work here = accrual vs actual cost analysis, dashboards, PPT.

## Session rules (every session)
1. **Before analysing**, read `docs/FINDINGS.md` (index) and any relevant file in `docs/findings/`. Do not re-derive or re-ask what is already recorded; build on it.
2. **Before finishing**, write each new finding to `docs/findings/<YYYY-MM-DD>-<topic>.md` (copy `docs/findings/_TEMPLATE.md`) and add one line to `docs/FINDINGS.md`. A Stop hook enforces this and auto-commits/pushes findings.
3. Mark Status honestly: Confirmed / Hypothesis / Superseded. Never present a hypothesis as fact.
4. Data in `data/sample/` is SAMPLE (synthetic). Never present sample numbers as real. Real exports go in `data/actual/` (see `data/README.md`).

## Definitions
- **Variance = Actual − Accrual.** Positive = under-accrued (unfavourable, P&L hit). Negative = over-accrued.
- **Accrual accuracy** = 1 − Σ|Actual − Accrual| / Σ Actual, on invoiced lines only.
- **Unbilled accrual** = accrual line with no actual invoice yet. Aged by period; >90 days = reversal/review candidate.
- **Material variance** = |variance| ≥ 10% and ≥ USD 10k (tune in `scripts/config.py`).
- Cost categories map to OPUS modules: Bunker/Port Service (PSO)/Terminal (TES)/Transport (TRS)/Canal (PSO)/Joint Operation (JOO)/Slot Charter (COA).

## Commands
- `bash scripts/run_daily.sh` — analyse, rebuild dashboard (`reports/dashboard.html`) and deck (`reports/daily_cost_review.pptx`).
- `python3 scripts/analyze.py` — KPIs only (JSON to stdout).
