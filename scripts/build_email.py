"""Write reports/email_summary.html (inline-styled; the daily routine sends this as the email body)."""
import html
from analyze import analyse, headlines
from config import REPORTS, EXTERNAL

def build(link=None):
    link = link or (REPORTS.as_uri() if EXTERNAL else "https://github.com/sohhuishan/CUL/blob/reports/reports")
    r = analyse(); t = r["total"]
    sm = "<p style='background:#fff3cd;padding:8px'><b>SAMPLE DATA — synthetic, not real figures.</b> Drop real exports into data/actual/.</p>" if r["sample"] else ""
    rows = "".join(f"<tr><td>{html.escape(k)}</td><td align=right>{v.variance:+,.0f}</td><td align=right>{v.variance_pct:+.1%}</td><td align=right>{v.accuracy:.1%}</td></tr>" for k, v in r["by_cat"].iterrows())
    body = f"""<div style="font-family:Arial,sans-serif;max-width:640px">{sm}
<h2 style="margin:0">Cost Control — daily review, {r['asof']:%d %b %Y}</h2>
<p style="color:#555">Variance = actual − accrual (+ = under-accrued)</p>
<ul>{''.join(f'<li>{html.escape(h)}</li>' for h in headlines(r))}</ul>
<table cellpadding=5 style="border-collapse:collapse;border:1px solid #ddd;font-size:13px"><tr style="background:#f3f3f3"><th align=left>Category</th><th>Variance USD</th><th>%</th><th>Accuracy</th></tr>{rows}</table>
<p><a href="{link}/daily_cost_review.pptx">Download the deck (PPTX)</a> · <a href="{link}/dashboard.html">Dashboard (HTML)</a> · <a href="{link}/findings.html">All findings (searchable)</a></p></div>"""
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "email_subject.txt").write_text(f"Cost Control Daily Review - {r['asof']:%d %b %Y}" + (" [SAMPLE DATA]" if r["sample"] else ""), encoding="utf-8")
    (REPORTS / "email_summary.html").write_text(body, encoding="utf-8"); return REPORTS / "email_summary.html"
if __name__ == "__main__": print(build())
