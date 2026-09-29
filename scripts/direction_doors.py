#!/usr/bin/env python3
"""Stage 2 of the outreach sprint: count doors per direction from the warm roster.

Door = WARM person, or KNOWN person with a senior title, at a company that fits the direction.
Excluded as "in motion": partner, clients, referral partners, Cal competitors (spec exclusions).
Company fit is a keyword map over company name, title and email domain: a heuristic, listed per row
in data/direction_doors.csv so every door can be checked by hand.

Doors line (pre-registered): 2 = >=15 doors incl. >=5 WARM; 1 = >=5 doors; 0 = <5.

Usage: python scripts/direction_doors.py   (reads data/roster.csv)
"""
import os
import re

import pandas as pd

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

SENIOR = re.compile(r"\b(ceo|cfo|coo|cto|cmo|cro|cbo|cso|cpo|chief|founder|co-founder|president|vp|vice president|"
                    r"svp|evp|head|director|gm|general manager|managing|partner|chairman|owner|board)\b", re.I)

IN_MOTION = re.compile(r"micha motlis|\bcal[- ]platform|\bcal\b|isracard|ישראכרט|\bmax\b|max\.co\.il|max it|"
                       r"thunes|transferto|bridgerpay|melodicapital|melodi|xenaris|\beko\b|eko\.co\.in", re.I)

DIRECTIONS = {
    # Israel-HQ fintech / payments / FS scale-ups and platform units that sell abroad (buyer picks the market)
    "D1 Second Cal, buyer picks market": r"payoneer|rapyd|nayax|tipalti|papaya global|melio|sunbit|biocatch|thetaray|"
        r"riskified|pagaya|lemonade|wiserpay|okoora|payem|pontera|justt|nilus|candex|sapiens|actimize|global-e|"
        r"etoro|plus500|au10tix|personetics|earnix|fundbox|bluevine|forter|fireblocks|pomvom|be the bank|"
        r"lucid financials|kolleno|cedar money|next insurance|passportcard|davidshield|mera-fintech|"
        r"getneema|neema|dokka|trafix|withvayu|vayu",
    # same buyer pool, US as the only market: no separate company set
    "D2 Second Cal, US only": None,
    # foreign fintech / payments infrastructure without a big Israeli operation (sell them Israel)
    "D3 Sell Israel to foreign fintech infra": r"payroc|terrapay|moneythor|salt ?edge|riverty|adyen|checkout\.com|"
        r"wise\.com|wise payments|unipaas|flagright|lido finance|amara exchange|chainalysis|iserveu|revolut|airwallex|"
        r"visionaryarc|traild|nuvei|simplex|valley bank|state bank of india|dbs bank|bank of singapore",
    # Israeli incumbents (banks, insurers, investment houses) and big-co units in Israel (Aug 31 universe)
    "D4 Israeli incumbents' new units": r"leumi|hapoalim|poalim|discount|mizrahi|shva|automated banking|tefahot|fibi|first international|"
        r"one zero|\besh\b|paybox|migdal|clal|harel insurance|menora|phoenix|meitav|altshuler|psagot|\bibi\b|"
        r"more investment|tafnit|check point|hibob|fiverr|intuit|citi|mastercard|visa\b|j\.?p\.? ?morgan|jpmorgan|"
        r"paypal|barclays|stripe|bankleumi|dcapital|wix",
    # Singapore / India based organisations (Amos's APAC network)
    "D5 Singapore / India": r"\bpte\b|singapore|\bsg\b|india|private limited|\bnus\b|\bsmu\b|\bntu\b|nanyang|\bedb\b|"
        r"govtech|temasek|\bgrab\b|iserveu|\bdbs\b|ocbc|\buob\b|\.sg$|\.in$|\.co\.in$",
    # evidence-suggested: Big-4 / advisory / law as referral channel for market-entry mandates
    "E1 Big-4 & advisory referral channel": r"\bpwc\b|\bey\b|ernst|kpmg|deloitte|\bbdo\b|dun & bradstreet|"
        r"law firm|\blaw\b|\badv\b|advocates|pollak|matalon|herzog|kyprianou|shibolet|gornitzky|"
        r"meitar|fischer|barnea|goldfarb|amit, pollak|apm\.law|roland berger|gartner|mckinsey|\bbcg\b|bain",
    # evidence-suggested: Israeli cyber / AI-infra scale-ups going international (target-profile sector 2)
    "E2 Israeli cyber & AI-infra scale-ups": r"cyber|security|\bsec\b|bindsec|guardz|silverfort|check point|"
        r"xm cyber|cyberpro|legion|valence|zenyard|\.ai\b|\bai\b|faros|aerospike|datasnipper|camunda|emerix|"
        r"darrow|tenjin|melingo|conifers|metriko|opeak|arc analytics",
}


def main():
    d = pd.read_csv(os.path.join(DATA, "roster.csv"), dtype=str).fillna("")
    d["senior"] = d.title.map(lambda t: bool(SENIOR.search(t)))
    d["domain"] = d.emails.map(lambda e: ";".join(sorted({x.split("@")[1] for x in e.split(";") if "@" in x})))
    pool = d[(d.tier == "WARM") | ((d.tier == "KNOWN") & d.senior)].copy()
    # current employer = company field; email domains are only a fallback (merged contacts carry stale domains)
    hay = pool.company.where(pool.company != "", pool.domain)
    pool["in_motion"] = (hay + " | " + pool.name).str.contains(IN_MOTION)
    pool["s"] = pool.score.astype(int)
    pool["last_ev"] = pool[["li_last_msg", "cal_last_meeting"]].max(axis=1)
    rows, summary = [], []
    for name, pat in DIRECTIONS.items():
        src = DIRECTIONS["D1 Second Cal, buyer picks market"] if pat is None else pat
        fit = pool[hay.str.contains(src, flags=re.I, regex=True)]
        doors = fit[~fit.in_motion].sort_values(["s", "last_ev"], ascending=False)
        w, k = int((doors.tier == "WARM").sum()), int((doors.tier == "KNOWN").sum())
        line = 2 if w + k >= 15 and w >= 5 else 1 if w + k >= 5 else 0
        summary.append({"direction": name, "warm": w, "known_senior": k, "doors": w + k, "doors_line": line,
                        "in_motion_excluded": int(fit.in_motion.sum()),
                        "warm_examples": "; ".join(f"{r['name']} ({r.company})" for _, r in doors[doors.tier == "WARM"].head(3).iterrows()),
                        "known_examples": "; ".join(f"{r['name']} ({r.company}, {r.title[:40]})" for _, r in doors[doors.tier == "KNOWN"].head(3).iterrows())})
        for _, r in doors.iterrows():
            rows.append({"direction": name, "name": r["name"], "company": r.company, "title": r.title, "tier": r.tier,
                         "score": r.score, "breakdown": r.breakdown})
    pd.DataFrame(rows).to_csv(os.path.join(DATA, "direction_doors.csv"), index=False)
    out = pd.DataFrame(summary)
    out.to_csv(os.path.join(DATA, "direction_doors_summary.csv"), index=False)
    print(out[["direction", "warm", "known_senior", "doors", "doors_line", "in_motion_excluded"]].to_string(index=False))


if __name__ == "__main__":
    main()
