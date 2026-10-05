"""Build reports/dashboard.html (self-contained, light/dark, hover tooltips via <title>)."""
import html, datetime as dt
from analyze import analyse, headlines
from config import REPORTS, AGED_DAYS

BLUE, ORANGE = "#2a78d6", "#eb6834"
M = lambda v: f"{v/1e6:+.2f}M" if abs(v) >= 1e5 else f"{v/1e3:+.0f}k"
Mp = lambda v: f"{v/1e6:.1f}M"

def hbars(series, title, fmt=M):
    """Diverging horizontal bars: orange = under-accrued (+), blue = over-accrued (-)."""
    mx = max(abs(series).max(), 1); W, H, mid = 600, 28 * len(series) + 8, 300
    s = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(title)}">']
    for i, (k, v) in enumerate(series.items()):
        w = abs(v) / mx * 170; x = mid if v >= 0 else mid - w; y = 4 + i * 28
        s.append(f'<text x="{mid-198}" y="{y+15}" class="lbl" text-anchor="end">{html.escape(str(k))}</text>')
        s.append(f'<rect x="{x:.1f}" y="{y}" width="{max(w,1):.1f}" height="20" rx="3" fill="{ORANGE if v>=0 else BLUE}"><title>{html.escape(str(k))}: USD {fmt(v)}</title></rect>')
        s.append(f'<text x="{(x+w+6) if v>=0 else (x-6):.1f}" y="{y+15}" class="val" text-anchor="{"start" if v>=0 else "end"}">{fmt(v)}</text>')
    s.append(f'<line x1="{mid}" x2="{mid}" y1="0" y2="{H}" class="axis"/></svg>')
    return "".join(s)

def trend(bp):
    """Single series: accuracy % by period (period-end partial billing makes absolute USD misleading)."""
    W, H, pad = 600, 190, 48; v = bp.accuracy; n = len(v)
    lo, hi = min(v.min(), 0.9) - 0.01, min(max(v.max(), 0.95) + 0.01, 1.0)
    xs = [pad + i * (W - 2 * pad) / max(n - 1, 1) for i in range(n)]
    y = lambda a: H - 28 - (a - lo) / (hi - lo) * (H - 56)
    s = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Accrual accuracy by period">']
    for g in (lo + (hi - lo) * k / 3 for k in range(4)):
        s.append(f'<line x1="{pad-8}" x2="{W-pad+8}" y1="{y(g):.1f}" y2="{y(g):.1f}" class="axis"/><text x="{pad-12}" y="{y(g)+4:.1f}" class="lbl" text-anchor="end">{g:.0%}</text>')
    pts = " ".join(f"{x:.1f},{y(a):.1f}" for x, a in zip(xs, v))
    s.append(f'<polyline points="{pts}" fill="none" stroke="{BLUE}" stroke-width="2"/>')
    for x, (p, a) in zip(xs, v.items()):
        s.append(f'<circle cx="{x:.1f}" cy="{y(a):.1f}" r="5" fill="{BLUE}" stroke="var(--surface)" stroke-width="2"><title>{p}: {a:.1%} accuracy, {bp.loc[p,"unbilled"]/1e6:.1f}M still unbilled</title></circle>')
        s.append(f'<text x="{x:.1f}" y="{y(a)-10:.1f}" class="val" text-anchor="middle">{a:.1%}</text><text x="{x:.1f}" y="{H-8}" class="lbl" text-anchor="middle">{p}</text>')
    s.append("</svg>")
    return "".join(s)

def table(df, cols, fmts):
    h = "".join(f"<th>{c}</th>" for c in cols)
    b = "".join("<tr>" + "".join(f"<td>{f(r[c]) if f else html.escape(str(r[c]))}</td>" for c, f in zip(cols, fmts)) + "</tr>" for _, r in df.iterrows())
    return f"<table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>"

def build():
    r = analyse(); t = r["total"]; REPORTS.mkdir(exist_ok=True)
    kpis = [("Accrual accuracy", f"{t.accuracy:.1%}", "invoiced lines"), ("Net variance", f"USD {M(t.variance)}", f"{t.variance_pct:+.1%} of actual · + = under-accrued"),
            ("Unbilled accruals", f"USD {Mp(t.unbilled)}", f"{len(r['aged'])} lines > {AGED_DAYS}d (USD {Mp(r['aged'].accrual_usd.sum())})"),
            ("Material variances", str(len(r["material"])), f"USD {M(r['material'].variance.sum())} net")]
    kp = "".join(f'<div class="kpi"><div class="k">{a}</div><div class="v">{b}</div><div class="s">{c}</div></div>' for a, b, c in kpis)
    top = r["top"].assign(var=lambda d: d.variance, pct=lambda d: d.var_pct)
    aged = r["aged"].head(10)
    wm = '<div class="wm">SAMPLE DATA — synthetic, not real figures</div>' if r["sample"] else ""
    hl = "".join(f"<li>{html.escape(h)}</li>" for h in headlines(r))
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cost Control Dashboard</title><style>
:root{{--bg:#f6f6f4;--surface:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--line:#e3e2dc}}
@media(prefers-color-scheme:dark){{:root{{--bg:#111110;--surface:#1a1a19;--ink:#fff;--ink2:#c3c2b7;--line:#33322f}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 system-ui,sans-serif}}
main{{max-width:1100px;margin:0 auto;padding:16px}}h1{{font-size:20px;margin:4px 0}}h2{{font-size:14px;margin:0 0 8px;color:var(--ink2);font-weight:600}}
.sub{{color:var(--ink2);margin-bottom:12px}}.wm{{background:#fff3cd;color:#664d03;padding:6px 10px;border-radius:6px;margin-bottom:12px;font-weight:600}}
.grid{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));margin-bottom:12px}}
.card{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px;overflow-x:auto}}
.two{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));margin-bottom:12px}}
.kpi .k{{color:var(--ink2);font-size:12px}}.kpi .v{{font-size:26px;font-weight:700}}.kpi .s{{color:var(--ink2);font-size:12px}}
svg{{width:100%;height:auto}}.lbl{{font-size:11px;fill:var(--ink2)}}.val{{font-size:11px;fill:var(--ink)}}.axis{{stroke:var(--line)}}
table{{border-collapse:collapse;width:100%;font-size:12px}}th,td{{text-align:left;padding:5px 8px;border-bottom:1px solid var(--line);white-space:nowrap}}th{{color:var(--ink2)}}
.key i{{display:inline-block;width:10px;height:10px;border-radius:2px;margin:0 4px 0 10px}}ul{{margin:0;padding-left:18px}}
</style></head><body><main>{wm}
<h1>Cost Control — Accrual vs Actual</h1><div class="sub">As of {r['asof']:%d %b %Y} · variance = actual − accrual</div>
<div class="grid">{kp}</div>
<div class="card" style="margin-bottom:12px"><h2>Headlines</h2><ul>{hl}</ul></div>
<div class="two"><div class="card"><h2>Accrual accuracy by period (invoiced lines)</h2>{trend(r['by_period'])}</div>
<div class="card"><h2>Variance by cost category</h2><div class="key"><i style="background:{ORANGE}"></i>under-accrued<i style="background:{BLUE}"></i>over-accrued</div>{hbars(r['by_cat'].variance,'Variance by category')}</div></div>
<div class="two"><div class="card"><h2>Variance by lane</h2>{hbars(r['by_lane'].variance,'Variance by lane')}</div>
<div class="card"><h2>Variance by vendor</h2>{hbars(r['by_vendor'].variance.head(8),'Variance by vendor')}</div></div>
<div class="card" style="margin-bottom:12px"><h2>Top 10 variances</h2>{table(top,['period','voyage','lane','cost_category','vendor','accrual_usd','actual_usd','var','pct'],[None]*5+[lambda v:f'{v:,.0f}']*3+[lambda v:f'{v:+.1%}'])}</div>
<div class="card"><h2>Aged unbilled accruals (&gt;{AGED_DAYS} days) — reversal / chase candidates</h2>{table(aged,['period','voyage','lane','cost_category','vendor','accrual_usd','age_days'],[None]*5+[lambda v:f'{v:,.0f}',None])}</div>
</main></body></html>"""
    (REPORTS / "dashboard.html").write_text(page)
    return REPORTS / "dashboard.html"

if __name__ == "__main__":
    print(build())
