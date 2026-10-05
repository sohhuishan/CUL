"""Build reports/daily_cost_review.pptx with native (editable) charts."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from analyze import analyse, headlines
from config import REPORTS, AGED_DAYS

BLUE, ORANGE, INK, GREY = RGBColor(0x2a,0x78,0xd6), RGBColor(0xeb,0x68,0x34), RGBColor(0x1b,0x1b,0x1a), RGBColor(0x6b,0x6a,0x66)
M = lambda v: f"{v/1e6:+.2f}M" if abs(v) >= 1e5 else f"{v/1e3:+.0f}k"

def text(sl, x, y, w, h, s, size=14, bold=False, color=INK):
    tb = sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = tb.text_frame; tf.word_wrap = True
    for i, line in enumerate(s if isinstance(s, list) else [s]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line; p.font.size = Pt(size); p.font.bold = bold; p.font.color.rgb = color; p.space_after = Pt(6)
    return tb

def slide(prs, title, sample):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    text(sl, 0.5, 0.3, 12.3, 0.9, title, 26, True)       # action title = the takeaway
    if sample: text(sl, 9.3, 7.0, 3.8, 0.3, "SAMPLE DATA — synthetic", 10, True, ORANGE)
    return sl

def bar(sl, series, x, y, w, h, fmt='#,##0,"k"'):
    cd = CategoryChartData(); cd.categories = list(series.index); cd.add_series("Variance (USD)", [float(v) for v in series])
    ch = sl.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(x), Inches(y), Inches(w), Inches(h), cd).chart
    ch.has_legend = False; ch.category_axis.reverse_order = True; ch.value_axis.visible = False
    ch.value_axis.has_major_gridlines = False; ch.category_axis.tick_labels.font.size = Pt(12)
    pl = ch.plots[0]; pl.gap_width = 60; pl.has_data_labels = True
    pl.data_labels.number_format = fmt; pl.data_labels.number_format_is_linked = False; pl.data_labels.font.size = Pt(11)
    s = pl.series[0]; s.invert_if_negative = False
    for i, v in enumerate(series):
        pt = s.points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = ORANGE if v >= 0 else BLUE

def table(sl, df, cols, heads, x, y, w, rowh=0.32, size=11):
    t = sl.shapes.add_table(len(df) + 1, len(cols), Inches(x), Inches(y), Inches(w), Inches(rowh * (len(df) + 1))).table
    for j, h in enumerate(heads):
        c = t.cell(0, j); c.text = h; c.text_frame.paragraphs[0].font.size = Pt(size); c.text_frame.paragraphs[0].font.bold = True
    for i, (_, r) in enumerate(df.iterrows(), 1):
        for j, col in enumerate(cols):
            v = r[col]; c = t.cell(i, j); c.text = f"{v:,.0f}" if isinstance(v, float) and abs(v) > 5 else (f"{v:+.1%}" if isinstance(v, float) else str(v))
            c.text_frame.paragraphs[0].font.size = Pt(size)

def build():
    r = analyse(); t = r["total"]; REPORTS.mkdir(exist_ok=True); sm = r["sample"]
    prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    bc, a = r["by_cat"], r["aged"]; top = bc.index[0]

    sl = slide(prs, f"Accruals were {t.accuracy:.1%} accurate; {top} drives USD {M(bc.loc[top,'variance'])} under-accrual", sm)
    text(sl, 0.5, 1.4, 12.3, 0.4, f"Daily cost review · as of {r['asof']:%d %b %Y} · variance = actual − accrual (+ = under-accrued)", 13, False, GREY)
    for i, (k, v) in enumerate([("Accrual accuracy", f"{t.accuracy:.1%}"), ("Net variance", f"USD {M(t.variance)}"),
                                ("Unbilled accruals", f"USD {t.unbilled/1e6:.1f}M"), ("Material variances", str(len(r['material'])))]):
        text(sl, 0.5 + i * 3.1, 2.0, 3, 0.4, k, 13, False, GREY); text(sl, 0.5 + i * 3.1, 2.4, 3, 0.8, v, 30, True)
    text(sl, 0.5, 3.6, 12.3, 3.2, ["• " + h for h in headlines(r)], 16)

    sl = slide(prs, f"Accuracy is {'slipping' if r['by_period'].accuracy.iloc[-1] < r['by_period'].accuracy.iloc[0] else 'stable'}: "
                    f"{r['by_period'].accuracy.iloc[0]:.1%} → {r['by_period'].accuracy.iloc[-1]:.1%} over six periods", sm)
    bp = r["by_period"]; cd = CategoryChartData(); cd.categories = list(bp.index); cd.add_series("Accrual accuracy", [float(v) for v in bp.accuracy])
    ch = sl.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(0.5), Inches(1.5), Inches(8.2), Inches(5.2), cd).chart
    ch.has_legend = False; ch.value_axis.minimum_scale = 0.9; ch.value_axis.maximum_scale = 1.0; ch.value_axis.tick_labels.number_format = '0%'; ch.value_axis.tick_labels.number_format_is_linked = False
    ch.plots[0].has_data_labels = True; ch.plots[0].data_labels.number_format = '0.0%'; ch.plots[0].data_labels.number_format_is_linked = False; ch.plots[0].data_labels.position = XL_LABEL_POSITION.ABOVE
    ch.plots[0].series[0].format.line.color.rgb = BLUE
    text(sl, 9.0, 1.7, 4, 4, ["Reading this", "Latest period is partly un-invoiced, so its accuracy is provisional and will move as invoices land.", f"Unbilled accruals: USD {t.unbilled/1e6:.1f}M."], 14)

    sl = slide(prs, f"{top} and Joint Operation account for most of the under-accrual", sm)
    bar(sl, bc.variance, 0.5, 1.4, 7.6, 5.3)
    text(sl, 8.5, 1.5, 4.4, 5, ["Variance by cost category (USD)", "Orange = under-accrued (actual > accrual); blue = over-accrued.",
         *[f"{k}: {M(v.variance)} ({v.variance_pct:+.1%})" for k, v in bc.head(3).iterrows()]], 14)

    lane = r["by_lane"]; w = lane.index[0]
    sl = slide(prs, f"{w} is the hot lane: USD {M(lane.loc[w,'variance'])} of net variance", sm)
    bar(sl, lane.variance, 0.5, 1.4, 6.0, 3.0); vend = r["by_vendor"].variance.head(8); bar(sl, vend, 6.8, 1.4, 6.0, 5.3)
    text(sl, 0.5, 4.6, 6, 2, ["By lane (left) · by vendor, top 8 (right)", "Use lane × category detail in the dashboard to pinpoint the rate or surcharge being missed in the accrual."], 13, False, GREY)

    sl = slide(prs, "Ten line items explain the largest variances — start the follow-up here", sm)
    table(sl, r["top"], ["period", "voyage", "lane", "cost_category", "vendor", "accrual_usd", "actual_usd", "variance", "var_pct"],
          ["Period", "Voyage", "Lane", "Category", "Vendor", "Accrual", "Actual", "Variance", "%"], 0.5, 1.5, 12.3)

    sl = slide(prs, f"USD {a.accrual_usd.sum()/1e6:.1f}M of accruals are >{AGED_DAYS} days unbilled — chase or reverse", sm)
    table(sl, a.head(10), ["period", "voyage", "lane", "cost_category", "vendor", "accrual_usd", "age_days"],
          ["Period", "Voyage", "Lane", "Category", "Vendor", "Accrual", "Age (days)"], 0.5, 1.5, 12.3)
    text(sl, 0.5, 5.4, 12.3, 1.5, [f"{len(a)} lines in total. Proposed: confirm with vendor/ops whether service was performed; if not, reverse; if yes, request invoice."], 14, False, GREY)

    sl = slide(prs, "Proposed actions", sm)
    text(sl, 0.5, 1.5, 12.3, 5, ["1. Re-base the " + top + " accrual rate for the worst lane; monitor next period's variance.",
         "2. Review aged unbilled items with Ops/Procurement; reverse the stale ones before month-end.",
         "3. Investigate material variances (≥10% and ≥USD 10k) — confirm cause (rate, volume, surcharge, timing).",
         "4. Reduce systematic over-accrual where the variance is consistently negative (e.g. tariff-based port costs)."], 18)
    out = REPORTS / "daily_cost_review.pptx"; prs.save(out); return out

if __name__ == "__main__":
    print(build())
