"""Generate SYNTHETIC sample data with realistic patterns. Not real figures."""
import random, csv, datetime as dt
from config import SAMPLE_FILE
random.seed(7)
lanes = ["Asia-Europe","Transpacific","Intra-Asia","Asia-Med","Transatlantic"]
cats = {"Bunker":("COA",["Vendor B1","Vendor B2"]),"Port Service":("PSO",["PortCo SG","PortCo RTM","PortCo LA"]),
        "Terminal":("TES",["TermOp A","TermOp B"]),"Transport":("TRS",["HaulCo","RailCo"]),
        "Canal":("PSO",["Suez Auth","Panama Auth"]),"Joint Operation":("JOO",["Partner X","Partner Y"]),
        "Slot Charter":("COA",["Partner X","Partner Z"])}
base = {"Bunker":900e3,"Port Service":120e3,"Terminal":220e3,"Transport":160e3,"Canal":300e3,"Joint Operation":400e3,"Slot Charter":250e3}
months = ["2026-04","2026-05","2026-06","2026-07","2026-08","2026-09"]
rows=[]
for mi,p in enumerate(months):
    for lane in lanes:
        for cat,(mod,vends) in cats.items():
            if cat=="Canal" and lane not in ("Asia-Europe","Asia-Med","Transpacific"): continue
            for k in range(2):
                acc = base[cat]*random.uniform(.5,1.4)*(1.25 if lane in("Asia-Europe","Transpacific") else .8)/ (2)
                bias=random.gauss(0,.04)
                if cat=="Bunker" and lane=="Asia-Europe": bias+=.09 + .01*mi   # under-accrued, worsening
                if cat=="Canal" and lane=="Asia-Europe": bias+=.12             # rerouting surcharges
                if cat=="Port Service": bias-=.07                              # over-accrued tariff
                if cat=="Joint Operation": bias+=random.choice([0,0,.15])      # late settlement
                act = acc*(1+bias)
                age = len(months)-1-mi
                billed = random.random() > (0.55 if age==0 else .22 if age==1 else .06)
                if cat=="Joint Operation" and age>=3 and random.random()<.5: billed=False  # stale
                inv = (dt.date(int(p[:4]),int(p[5:]),28)+dt.timedelta(days=random.randint(10,45))).isoformat() if billed else ""
                rows.append([p,f"{lane[:3].upper()}{mi}{k}{cat[:2].upper()}",lane,mod,cat,random.choice(vends),round(acc),round(act) if billed else "",inv])
with open(SAMPLE_FILE,"w",newline="") as f:
    w=csv.writer(f);w.writerow(["period","voyage","lane","module","cost_category","vendor","accrual_usd","actual_usd","invoice_date"]);w.writerows(rows)
print(len(rows),"rows")
