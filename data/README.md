# Data

Drop OPUS (COA Estimated Cost / invoice) exports as CSV into `data/actual/`. If that folder has CSVs the pipeline uses them; otherwise it falls back to `data/sample/` (**synthetic SAMPLE data**, reports are watermarked).

Required columns (one row per accrual line):

| column | meaning |
|---|---|
| period | accounting month `YYYY-MM` |
| voyage | voyage / reference |
| lane | trade / service lane |
| module | COA, PSO, TES, TRS, JOO |
| cost_category | Bunker, Port Service, Terminal, Transport, Canal, Joint Operation, Slot Charter |
| vendor | supplier / partner |
| accrual_usd | accrued amount |
| actual_usd | invoiced amount; blank if not yet invoiced |
| invoice_date | `YYYY-MM-DD`; blank if not invoiced |

Rename columns in your export to match, or tell Claude the mapping and it will be added to `scripts/analyze.py`.
