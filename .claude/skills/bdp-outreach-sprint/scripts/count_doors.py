#!/usr/bin/env python3
"""Stage 2 of the outreach sprint: count doors per direction from the warm roster.

Door = WARM person, or KNOWN person with a senior title, at a company that fits the direction.
People already in motion (partner, clients, referral partners, client competitors, live deals)
are removed first. Company fit is a keyword map, so the script prints the top companies it matched
per direction: read them before trusting any count (substring hits like "ntu" inside "Intuit",
or "wise" inside an unrelated firm, are the usual failure).

Doors line (pre-registered): 2 = >= 15 doors incl. >= 5 WARM; 1 = >= 5 doors; 0 = < 5.

Directions config (JSON, keep client names out of the skill; store it next to the run log):
  {
    "in_motion_regex": "partner name|client|client competitor|referral partner|...",
    "hold_regex": "optional: accounts held back this sprint",
    "senior_regex": "optional override of SENIOR below",
    "directions": {"D1 name": "regex of fitting companies", "D2 name": null, ...}
  }
A direction set to null reuses the first direction's company set (same pool, different market).

Usage: python count_doors.py --roster data/roster.csv --config sprint/directions.json [--out-dir data]
Outputs: direction_doors.csv (every door, for hand checks) and direction_doors_summary.csv.
"""
import argparse
import json
import os
import re

import pandas as pd

SENIOR = (r"\b(ceo|cfo|coo|cto|cmo|cro|cbo|cso|cpo|chief|founder|co-founder|president|vp|vice president|"
          r"svp|evp|head|director|gm|general manager|managing|partner|chairman|owner|board)\b")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roster", default="data/roster.csv")
    ap.add_argument("--config", required=True)
    ap.add_argument("--out-dir", default="data")
    args = ap.parse_args()
    cfg = json.load(open(args.config, encoding="utf-8"))
    senior = re.compile(cfg.get("senior_regex") or SENIOR, re.I)
    in_motion = re.compile(cfg["in_motion_regex"], re.I)
    hold = re.compile(cfg["hold_regex"], re.I) if cfg.get("hold_regex") else None
    directions = cfg["directions"]
    first = next(v for v in directions.values() if v)

    d = pd.read_csv(args.roster, dtype=str).fillna("")
    d["senior"] = d.title.map(lambda t: bool(senior.search(t)))
    d["domain"] = d.emails.map(lambda e: ";".join(sorted({x.split("@")[1] for x in e.split(";") if "@" in x})))
    pool = d[(d.tier == "WARM") | ((d.tier == "KNOWN") & d.senior)].copy()
    # current employer = company field; email domains only as a fallback (merged contacts carry stale domains)
    hay = pool.company.where(pool.company != "", pool.domain)
    pool["in_motion"] = (hay + " | " + pool.name).str.contains(in_motion)
    pool["held"] = hay.str.contains(hold) if hold else False
    pool["s"] = pool.score.astype(int)
    pool["last_ev"] = pool[["li_last_msg", "cal_last_meeting"]].max(axis=1)

    rows, summary = [], []
    for name, pat in directions.items():
        fit = pool[hay.str.contains(pat or first, flags=re.I, regex=True)]
        doors = fit[~fit.in_motion & ~fit.held].sort_values(["s", "last_ev"], ascending=False)
        w, k = int((doors.tier == "WARM").sum()), int((doors.tier == "KNOWN").sum())
        line = 2 if w + k >= 15 and w >= 5 else 1 if w + k >= 5 else 0
        summary.append({"direction": name, "warm": w, "known_senior": k, "doors": w + k, "doors_line": line,
                        "in_motion_excluded": int(fit.in_motion.sum()), "held": int(fit.held.sum()),
                        "top_companies": "; ".join(f"{c} ({n})" for c, n in doors.company.value_counts().head(8).items())})
        for _, r in doors.iterrows():
            rows.append({"direction": name, "name": r["name"], "company": r.company, "title": r.title, "tier": r.tier,
                         "score": r.score, "breakdown": r.breakdown, "linkedin_url": r.linkedin_url,
                         "li_last_msg": r.li_last_msg, "cal_last_meeting": r.cal_last_meeting})
    pd.DataFrame(rows).to_csv(os.path.join(args.out_dir, "direction_doors.csv"), index=False)
    out = pd.DataFrame(summary)
    out.to_csv(os.path.join(args.out_dir, "direction_doors_summary.csv"), index=False)
    print(out[["direction", "warm", "known_senior", "doors", "doors_line", "in_motion_excluded", "held"]].to_string(index=False))
    print("\nTop matched companies per direction (check for keyword false positives):")
    for s in summary:
        print(f"- {s['direction']}: {s['top_companies']}")


if __name__ == "__main__":
    main()
