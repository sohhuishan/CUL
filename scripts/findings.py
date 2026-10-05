"""Findings lookup + searchable page.
  python3 scripts/findings.py search bunker     # terminal search (what Claude uses before re-analysing)
  python3 scripts/findings.py build             # writes reports/findings.html
"""
import sys, re, html, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "docs" / "findings"

def load():
    out = []
    for f in sorted(DIR.glob("*.md"), reverse=True):
        if f.name.startswith("_"): continue
        t = f.read_text()
        title = (re.search(r"^#\s+(.+)", t, re.M) or [None, f.stem])[1]
        status = (re.search(r"\*\*Status:\*\*\s*([A-Za-z]+)", t) or [None, "Unknown"])[1]
        date = (re.search(r"\*\*Date:\*\*\s*(\S+)", t) or [None, f.stem[:10]])[1]
        out.append(dict(file=f.name, title=title, status=status, date=date, text=t))
    return out

def search(q):
    for e in load():
        hits = [l.strip() for l in e["text"].splitlines() if q.lower() in l.lower()]
        if hits:
            print(f"\n## {e['date']} [{e['status']}] {e['title']}  ({e['file']})")
            for h in hits[:6]: print("  -", h[:200])

def build():
    es = load()
    cards = "".join(f'<article data-s="{html.escape(e["status"])}" data-t="{html.escape(e["text"].lower())}"><h2>{html.escape(e["title"])}</h2>'
                    f'<p class="m">{e["date"]} · <b class="st {e["status"]}">{e["status"]}</b></p><pre>{html.escape(e["text"])}</pre></article>' for e in es)
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Findings</title><style>
:root{{--bg:#f6f6f4;--s:#fcfcfb;--ink:#0b0b0b;--i2:#52514e;--l:#e3e2dc}}@media(prefers-color-scheme:dark){{:root{{--bg:#111110;--s:#1a1a19;--ink:#fff;--i2:#c3c2b7;--l:#33322f}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 system-ui,sans-serif}}main{{max-width:860px;margin:0 auto;padding:16px}}
input,select{{font:inherit;padding:8px;border:1px solid var(--l);border-radius:6px;background:var(--s);color:var(--ink)}}input{{width:100%;margin-bottom:8px}}
article{{background:var(--s);border:1px solid var(--l);border-radius:10px;padding:12px 14px;margin:10px 0}}h2{{font-size:16px;margin:0}}.m{{color:var(--i2);margin:2px 0 6px}}
pre{{white-space:pre-wrap;font:13px/1.5 inherit;margin:0;max-height:0;overflow:hidden}}article.open pre{{max-height:none}}h2{{cursor:pointer}}
.st{{padding:1px 8px;border-radius:99px;background:var(--l)}}.Hypothesis{{background:#fff3cd;color:#664d03}}.Confirmed{{background:#d1e7dd;color:#0a3622}}</style></head><body><main>
<h1 style="font-size:20px">Findings ({len(es)})</h1><input id="q" placeholder="Search findings (e.g. bunker, Asia-Europe, aged)…" autofocus>
<select id="f"><option value="">All statuses</option><option>Confirmed</option><option>Hypothesis</option><option>Superseded</option></select><div id="n" class="m"></div>{cards}
<script>const A=[...document.querySelectorAll('article')],q=document.getElementById('q'),f=document.getElementById('f');
function r(){{let c=0;A.forEach(a=>{{const ok=a.dataset.t.includes(q.value.toLowerCase())&&(!f.value||a.dataset.s===f.value);a.hidden=!ok;c+=ok;if(q.value)a.classList.toggle('open',ok)}});document.getElementById('n').textContent=c+' shown'}}
q.oninput=f.onchange=r;A.forEach(a=>a.querySelector('h2').onclick=()=>a.classList.toggle('open'));r()</script></main></body></html>"""
    (ROOT / "reports").mkdir(exist_ok=True); (ROOT / "reports" / "findings.html").write_text(page); print(ROOT / "reports" / "findings.html")

if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "build"
    search(" ".join(sys.argv[2:])) if c == "search" else build()
