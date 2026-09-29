#!/usr/bin/env python3
"""In-motion gate for the outreach sprint: scan EVERY tab of the pipeline workbook(s) and earlier
sprint sheets for each candidate's company and surname.

Why a script: the Drive text reader returns only a sample row per tab, so a visual check misses
live threads (run 2 listed 5 people whose companies already had meetings set or outreach logged).
Export each sheet as .xlsx (download_file_content with the xlsx export type), decode it into data/,
then run:

  python in_motion_scan.py --candidates data/list.csv --workbooks data/pipeline.xlsx data/sprint1.xlsx
                           [--company-col company] [--name-col name] [--out data/in_motion_hits.csv]

Every hit is printed with its tab and a truncated row, for a human decision: a status like
"meeting set", "reached out", "proposal" or "call scheduled" means in motion; an idea-only row
(no contact, no status) usually doesn't. Nothing is excluded automatically.
"""
import argparse
import re

import pandas as pd

STOP = {"group", "ltd", "inc", "bank", "the", "israel", "global", "capital", "insurance", "money", "financial"}


def keys(company, name):
    """Search keys: the company's distinctive tokens and the person's surname (>=4 letters)."""
    toks = [t for t in re.split(r"[^a-z0-9\-]+", company.lower()) if len(t) >= 3 and t not in STOP]
    out = {" ".join(toks[:2])} if toks else set()
    parts = [p for p in re.split(r"\s+", re.sub(r"\(.*?\)", "", name.lower()).strip()) if p]
    if len(parts) >= 2 and len(parts[-1]) >= 4:
        out.add(parts[-1])
    return {k for k in out if k}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--workbooks", nargs="+", required=True)
    ap.add_argument("--company-col", default="company")
    ap.add_argument("--name-col", default="name")
    ap.add_argument("--out", default="data/in_motion_hits.csv")
    args = ap.parse_args()
    cand = pd.read_csv(args.candidates, dtype=str).fillna("")
    lines = []
    for wb in args.workbooks:
        for tab, d in pd.read_excel(wb, sheet_name=None, dtype=str, header=None).items():
            for _, r in d.fillna("").astype(str).iterrows():
                line = " | ".join(v for v in r if v).lower()
                if line:
                    lines.append((wb, tab, line))
    hits = []
    for _, c in cand.iterrows():
        for k in keys(c[args.company_col], c[args.name_col]):
            pat = re.compile(r"(?<![a-z])" + re.escape(k) + r"(?![a-z])")
            for wb, tab, line in lines:
                if pat.search(line):
                    hits.append({"name": c[args.name_col], "company": c[args.company_col], "key": k,
                                 "workbook": wb, "tab": tab, "row": line[:140]})
    out = pd.DataFrame(hits).drop_duplicates() if hits else pd.DataFrame(
        columns=["name", "company", "key", "workbook", "tab", "row"])
    out.to_csv(args.out, index=False)
    print(f"{out['company'].nunique() if len(out) else 0} of {cand[args.company_col].nunique()} companies have hits "
          f"across {len(lines)} rows. Review each:")
    for _, h in out.iterrows():
        print(f"- {h['company']} [{h['key']}] {h['tab']}: {h['row']}")


if __name__ == "__main__":
    main()
