#!/usr/bin/env python3
"""Weekly reconnection batch: pool, gates, ranking and supply per geography, from the warm roster sheet.

Reconnection is not a pitch. The goal is to restart real relationships so needs surface on their own,
so there is no signal gate: a dated signal, if one exists, is only the hook.

Input: the "Warm roster" Google Sheet exported as .xlsx into the gitignored data dir
(download_file_content with the xlsx export type, base64-decoded). Do not rebuild the roster for this.

Pool:  WARM-fresh (priority groups "1 fresh·sector" and "2 fresh·other")
       + KNOWN in-sector rows ("3 known·sector") whose title is senior.
Gates (in this order; each removed row keeps its reason):
  roster outcome active / company status active / referral partner  -> in motion
  company matches micha_regex or the row note names Micha           -> partner's account
  company matches client_competitor_regex                           -> client competitor
  person in exclude_names (runs #1-N contacted, or excluded there)  -> earlier runs
  company matches listed_company_regex (run LIST companies)         -> company already in a run
  outcome stalled / closed-lost                                     -> WARM-stalled
The 90-day Gmail-sent check is per person and runs through the connector on the shortlist only;
record it in the log, not here.

Rank: warmth + seniority (0-3), ties broken by FS/connector relevance, then warmth.
Batch: the top `foreign_slots` rows from the non-Israel geography with the most supply, then the rest
by rank. Evidence type, language and channel come from the raw exports for the shortlist only.

Config (data/reconnection_config.json; never committed, it holds names):
  {"exclude_names": [...], "micha_regex": "...", "client_competitor_regex": "...",
   "listed_company_regex": "...", "batch_size": 10, "foreign_slots": 3}

Run:
  python reconnection_pool.py --roster data/roster.xlsx --config data/reconnection_config.json
Prints pool size and weeks of supply per geography; writes data/reconnection_ranked.csv.
"""
import argparse
import json
import re

import pandas as pd

SENIOR = re.compile(r"\b(?:chief|ceo|cfo|coo|cto|cro|cmo|cbo|vp|vice president|head|director|gm|general manager|"
                    r"founder|co-founder|partner|managing|president|owner|svp|evp|principal|board|chairman|"
                    r"country manager|lead)\b", re.I)
NOT_SENIOR = re.compile(r"business partner|partner solution|partner manager|partnerships? (manager|lead)", re.I)
RELEVANT = re.compile(r"pay|fin|bank|insur|wealth|chain|crypto|lend|credit|money|\bfx\b|treasury|trading|securities|"
                      r"asset|capital|invest|venture|fund|angel|kpmg|pwc|deloitte|\bey\b|law|grants|hub|embassy|"
                      r"accelerat|chamber|trade", re.I)


def seniority(title):
    t = NOT_SENIOR.sub("", str(title).lower())
    if re.search(r"\b(chief|ceo|cfo|coo|cto|cro|cmo|cbo|founder|co-founder|partner|managing director|"
                 r"general manager|\bgm\b|owner|president|chairman|board member|country manager)\b", t):
        return 3
    if re.search(r"\b(svp|evp|vp|vice president)\b", t):
        return 2
    if re.search(r"\b(head|director|lead|principal)\b", t):
        return 1
    return 0


def norm(name):
    p = re.sub(r"[^a-z ]", "", str(name).lower().replace("-", " ")).split()
    return (p[0], p[-1]) if len(p) >= 2 else tuple(p)


def load_roster(path):
    df = pd.read_excel(path, dtype=str).fillna("")
    df = df[[c for c in df.columns if not str(c).startswith("Unnamed")]]
    df = df[df["name"].str.strip() != ""]
    df["warmth"] = pd.to_numeric(df["warmth"], errors="coerce").fillna(0)
    return df


def gate(r, cfg, excluded):
    company, note = str(r["company"]), str(r.get("note", ""))
    if r["outcome"] == "active" or str(r.get("company_status", "")).lower().startswith("active"):
        return "in motion"
    if r["outcome"] == "referral-only":
        return "referral partner (in motion)"
    if cfg.get("micha_regex") and (re.search(cfg["micha_regex"], company, re.I) or "micha" in note.lower()):
        return "partner's account"
    if cfg.get("client_competitor_regex") and re.search(cfg["client_competitor_regex"], company, re.I):
        return "client competitor"
    if norm(r["name"]) in excluded:
        return "earlier runs"
    if cfg.get("listed_company_regex") and re.search(cfg["listed_company_regex"], company, re.I):
        return "company already in a run"
    if r["outcome"] in ("stalled", "closed-lost"):
        return "WARM-stalled"
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roster", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", default="data/reconnection_ranked.csv")
    args = ap.parse_args()
    cfg = json.load(open(args.config))
    excluded = {norm(n) for n in cfg.get("exclude_names", [])}
    df = load_roster(args.roster)
    grp = df["priority_group"]
    df["sen"] = df["title"].map(seniority)
    senior = df["title"].str.contains(SENIOR) & (df["sen"] > 0)
    pool = df[grp.str.startswith("1") | grp.str.startswith("2") | (grp.str.startswith("3") & senior)].copy()
    pool["excl"] = pool.apply(gate, axis=1, cfg=cfg, excluded=excluded)
    print("Removed by gate:", pool[pool.excl != ""].excl.value_counts().to_dict())
    el = pool[pool.excl == ""].copy()
    el["rel"] = (el["in_sector"] == "Y") | el["company"].str.contains(RELEVANT) | el["title"].str.contains(RELEVANT)
    el["rank_score"] = el["warmth"] + el["sen"]
    el = el.sort_values(["rank_score", "rel", "warmth"], ascending=False)
    per = cfg.get("batch_size", 10)
    sup = el.groupby("geo").agg(pool=("name", "size"), fs_or_connector=("rel", "sum"))
    sup["weeks_at_batch"] = (sup["pool"] / per).round(1)
    print(f"Eligible pool: {len(el)} ({int(el.rel.sum())} FS/connector)")
    print(sup.sort_values("pool", ascending=False).to_string())
    el[["name", "company", "title", "geo", "priority_group", "warmth", "sen", "rel", "rank_score"]].to_csv(
        args.out, index=False)
    print(f"Ranked pool written to {args.out}")


if __name__ == "__main__":
    main()
