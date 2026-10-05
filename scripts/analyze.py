"""Accrual vs actual analysis. `python3 analyze.py` prints KPI JSON; import `analyse()` for reuse."""
import json, datetime as dt
import pandas as pd
from config import *

def load():
    files = sorted(ACTUAL_DIR.glob("*.csv")) if ACTUAL_DIR.exists() else []
    if files:
        df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True); sample = False
    else:
        df = pd.read_csv(SAMPLE_FILE); sample = True
    for c in ("accrual_usd", "actual_usd"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["period_end"] = pd.to_datetime(df["period"] + "-01") + pd.offsets.MonthEnd(0)
    return df, sample

def summ(g):
    inv = g[g.actual_usd.notna()]
    var = (inv.actual_usd - inv.accrual_usd).sum()
    acc = 1 - (inv.actual_usd - inv.accrual_usd).abs().sum() / inv.actual_usd.sum() if len(inv) and inv.actual_usd.sum() else None
    return pd.Series({"accrued": g.accrual_usd.sum(), "invoiced_accrual": inv.accrual_usd.sum(),
                      "actual": inv.actual_usd.sum(), "variance": var,
                      "variance_pct": var / inv.actual_usd.sum() if inv.actual_usd.sum() else None,
                      "accuracy": acc, "unbilled": g[g.actual_usd.isna()].accrual_usd.sum()})

def analyse(asof=None):
    df, sample = load()
    asof = pd.Timestamp(asof or dt.date.today())
    inv = df[df.actual_usd.notna()].copy()
    inv["variance"] = inv.actual_usd - inv.accrual_usd
    inv["var_pct"] = inv.variance / inv.actual_usd
    inv["material"] = (inv.var_pct.abs() >= MATERIAL_PCT) & (inv.variance.abs() >= MATERIAL_USD)
    ub = df[df.actual_usd.isna()].copy()
    ub["age_days"] = (asof - ub.period_end).dt.days
    ub["aged"] = ub.age_days > AGED_DAYS
    by = lambda col: df.groupby(col).apply(summ, include_groups=False).sort_values("variance", key=abs, ascending=False)
    tot = summ(df)
    heat = inv.pivot_table(index="lane", columns="cost_category", values="variance", aggfunc="sum").fillna(0)
    return dict(sample=sample, asof=asof, df=df, inv=inv, unbilled=ub, total=tot,
                by_period=df.groupby("period").apply(summ, include_groups=False),
                by_cat=by("cost_category"), by_lane=by("lane"), by_vendor=by("vendor"),
                heat=heat, top=inv.reindex(inv.variance.abs().sort_values(ascending=False).index).head(10),
                aged=ub[ub.aged].sort_values("accrual_usd", ascending=False),
                material=inv[inv.material])

def headlines(r):
    t, ub = r["total"], r["unbilled"]
    out = [f"Accrual accuracy {t.accuracy:.1%} on invoiced lines; net variance USD {t.variance/1e6:+.2f}M ({t.variance_pct:+.1%} of actual) — positive = under-accrued.",
           f"{len(r['material'])} material variances (≥{MATERIAL_PCT:.0%} and ≥USD {MATERIAL_USD//1000}k), USD {r['material'].variance.sum()/1e6:+.2f}M net."]
    bc = r["by_cat"]; w = bc.index[0]
    out.append(f"Largest driver: {w} at USD {bc.loc[w,'variance']/1e6:+.2f}M ({bc.loc[w,'variance_pct']:+.1%}).")
    a = r["aged"]
    out.append(f"Unbilled accruals USD {ub.accrual_usd.sum()/1e6:.1f}M; {len(a)} lines aged >{AGED_DAYS}d worth USD {a.accrual_usd.sum()/1e6:.1f}M — review for reversal/chase.")
    return out

if __name__ == "__main__":
    r = analyse()
    print(json.dumps({"sample": r["sample"], "headlines": headlines(r),
                      "by_cat": json.loads(r["by_cat"].round(3).to_json(orient="index"))}, indent=1))
