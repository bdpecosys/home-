#!/usr/bin/env python3
"""Stage 0 of the outreach sprint: build the warm roster (one-off script, not a system).

Warmth = evidence, not connection. Reads raw exports from the data dir (keep it gitignored),
writes roster.csv, roster_sheet.csv (no emails), match_review.csv and roster_summary.json,
and prints counts only. Message content is dropped on load and never reaches any output.

Inputs (in --data-dir; only Connections.csv is required, missing sources are reported):
  Connections.csv            LinkedIn export (3-line notes preamble before the header)
  messages.csv|messages.zip  LinkedIn messages export (zip holds messages.csv)
  contacts.csv               Google Contacts export
  other_contacts.csv         Google "Other contacts" export
  <tags_file>                optional hand-tagged contact set (see config "tags")
  calendar/*.json            Calendar connector list_events pages (primary calendar)

Config (--config, default <data-dir>/roster_config.json; copy roster_config.example.json):
  self_emails         your own addresses (excluded as counterparts)
  self_email_regex    catches your other/old addresses, e.g. "^you[^@]*@(yourco\\.|oldco\\.com)"
  self_names          your name in every script you use (drops your own rows)
  sector_extra_regex  company names that should count as in-sector (fs_company = Y)
  sector_exclude_regex  words that veto the sector flag (VCs, cyber firms)
  tags                {"file", "url_col", "tag_col", "name_col", "company_cols", "title_col", "warm_values"}

Usage: python build_roster.py --data-dir data [--config FILE] [--today YYYY-MM-DD]
                              [--lookback-days 730] [--max-attendees 8]
"""
import argparse
import glob
import io
import itertools
import json
import os
import re
import unicodedata
import zipfile
from collections import defaultdict
from datetime import datetime, timedelta, timezone

import pandas as pd

# Set from CLI/config in main(); module-level so the helpers stay simple.
DATA = "data"
MY_EMAILS, SELF_NAMES, SELF_RE = set(), set(), None
LOOKBACK_DAYS = 730  # "recent" evidence window (24 months)
MAX_MEETING_ATTENDEES = 8  # larger invites (webinars, all-hands) are not relationship evidence
TAGS = {"file": "", "url_col": "LinkedIn", "tag_col": "Tag", "name_col": "Contact name",
        "company_cols": ["Company"], "title_col": "Title", "warm_values": ["warm", "hot"]}
# Generic sector keywords only; named companies go in config "sector_extra_regex".
FS_BASE = (
    r"bank|banc|pay|fintech|financ|credit|card|insur|invest|securities|trading|lending|loan|"
    r"wallet|remit|acquir|clearing|forex|\bfx\b|crypto|blockchain|wealth|asset management|"
    r"brokerage|exchange|"
    r"בנק|פיננס|אשראי|ביטוח|השקעות|תשלומים"
)
FS_PATTERN = re.compile(FS_BASE, re.I)
FS_EXCLUDE = re.compile(r"venture|\bvc\b|cyber|security\b", re.I)  # VCs and cyber firms are not FS buyers

# ---------------------------------------------------------------- normalisation

HEB = re.compile(r"[֐-׿]")
NOISE = re.compile(
    r"\b(dr|mr|mrs|ms|prof|adv|cpa|mba|phd|jr|sr|ii|iii|cfa|pmp|llm|esq|ceo|cto|cfo|rn|md)\b\.?", re.I
)


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm_name(s):
    """Lowercase, strip accents/titles/emoji/parentheticals; keep Latin and Hebrew letters."""
    if not isinstance(s, str):
        return ""
    s = re.sub(r"\(.*?\)|\[.*?\]", " ", s)
    s = s.split(",")[0].split("|")[0]
    s = strip_accents(s).lower()
    s = NOISE.sub(" ", s)
    s = s.replace("-", " ").replace("'", "").replace("׳", "").replace("\"", "").replace("״", "")
    s = re.sub(r"[^a-zא-ת ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def first_last(n):
    t = n.split()
    if len(t) < 2:
        return None
    return t[0], t[-1]


EN_RULES = [("sch", "S"), ("ch", "K"), ("kh", "K"), ("sh", "S"), ("tz", "S"), ("ts", "S"), ("ph", "P"),
            ("th", "T"), ("ck", "K"), ("x", "KS")]
EN_MAP = {"q": "K", "c": "K", "k": "K", "z": "S", "s": "S", "f": "P", "p": "P", "v": "B", "w": "B",
          "b": "B", "j": "G", "g": "G", "t": "T", "d": "D", "l": "L", "m": "M", "n": "N", "r": "R"}
HE_MAP = {"א": [""], "ב": ["B"], "ג": ["G"], "ד": ["D"], "ה": [""], "ו": ["B", ""], "ז": ["S"],
          "ח": ["K", ""], "ט": ["T"], "י": [""], "כ": ["K"], "ך": ["K"], "ל": ["L"], "מ": ["M"],
          "ם": ["M"], "נ": ["N"], "ן": ["N"], "ס": ["S"], "ע": [""], "פ": ["P"], "ף": ["P"],
          "צ": ["S"], "ץ": ["S"], "ק": ["K"], "ר": ["R"], "ש": ["S"], "ת": ["T"]}


def dedupe(s):
    return re.sub(r"(.)\1+", r"\1", s)


def skeletons(token):
    """Consonant skeletons shared by Hebrew and Latin spellings (Hebrew yields several candidates)."""
    if HEB.search(token):
        # vav is a consonant (V) only word-initially or doubled; elsewhere it is a vowel
        t = token.replace("וו", "ב")
        t = ("ב" + t[1:] if t.startswith("ו") else t).replace("ו", "")
        opts = [HE_MAP.get(ch, [""]) for ch in t][:12]
        head = "^" if token[0] in "אע" else ""
        tail = "$" if token[-1] in "יאהוע" else ""
        return {head + dedupe("".join(p)) + tail for p in itertools.product(*opts)}
    s = token
    for a, b in EN_RULES:
        s = s.replace(a, b)
    head = "^" if token[0] in "aeiou" else ""
    tail = "$" if token.rstrip("h")[-1:] in tuple("aeiouy") else ""
    return {head + dedupe("".join(EN_MAP.get(ch, ch if ch.isupper() else "") for ch in s)) + tail}


def norm_url(u):
    if not isinstance(u, str) or "linkedin.com" not in u:
        return ""
    u = u.strip().lower().split("?")[0].rstrip("/")
    return "https://www.linkedin.com/" + u.split("linkedin.com/", 1)[1]


def emails_of(row, cols):
    out = set()
    for c in cols:
        v = row.get(c)
        if isinstance(v, str):
            for e in re.split(r"[;,:\s]+", v):
                e = e.strip().lower()
                if "@" in e:
                    out.add(e)
    return out


# ---------------------------------------------------------------- sources


def read_opt(fname):
    path = os.path.join(DATA, fname)
    if not os.path.exists(path):
        MISSING.append(fname)
        return None
    return pd.read_csv(path, dtype=str)


MISSING = []


def load_connections():
    df = pd.read_csv(os.path.join(DATA, "Connections.csv"), skiprows=3, dtype=str)
    df = df[df["URL"].notna()]
    people = []
    for _, r in df.iterrows():
        name = f"{r['First Name'] or ''} {r['Last Name'] or ''}".strip()
        people.append({
            "name": name, "company": r.get("Company") or "", "title": r.get("Position") or "",
            "linkedin_url": norm_url(r["URL"]), "emails": emails_of(r, ["Email Address"]),
            "li_connected_on": pd.to_datetime(r["Connected On"], format="%d %b %Y", errors="coerce"),
            "is_connection": True,
        })
    return people


def open_messages():
    p = os.path.join(DATA, "messages.csv")
    if os.path.exists(p):
        return pd.read_csv(p, dtype=str)
    z = os.path.join(DATA, "messages.zip")
    if os.path.exists(z):
        with zipfile.ZipFile(z) as zf:
            name = next(n for n in zf.namelist() if n.lower().endswith("messages.csv"))
            return pd.read_csv(io.BytesIO(zf.read(name)), dtype=str)
    MISSING.append("messages.csv|messages.zip")
    return None


def load_messages():
    """Per counterpart: msgs_from_me, msgs_from_them, first/last date. Content columns are dropped on load."""
    df = open_messages()
    if df is None:
        return None, {}
    df = df.drop(columns=[c for c in df.columns if c.strip().upper() in ("CONTENT", "SUBJECT")])
    df.columns = [c.strip().upper() for c in df.columns]
    if "FOLDER" in df.columns:
        df = df[df["FOLDER"].str.upper() != "SPAM"]
    df["SENDER PROFILE URL"] = df["SENDER PROFILE URL"].map(norm_url)
    me = df["SENDER PROFILE URL"].value_counts().idxmax()
    df["DATE"] = pd.to_datetime(df["DATE"].str.replace(" UTC", ""), errors="coerce")
    stats = defaultdict(lambda: {"from_me": 0, "from_them": 0, "first": None, "last": None, "name": ""})
    skipped_group = 0
    for conv, g in df.groupby("CONVERSATION ID"):
        parts = {}
        for _, r in g.iterrows():
            if r["SENDER PROFILE URL"]:
                parts[r["SENDER PROFILE URL"]] = r.get("FROM") or ""
            urls = str(r.get("RECIPIENT PROFILE URLS") or "").split(",")
            names = str(r.get("TO") or "").split(",")
            for i, u in enumerate(urls):
                u = norm_url(u)
                if u:
                    parts.setdefault(u, names[i].strip() if i < len(names) and len(urls) == len(names) else "")
        others = {u: n for u, n in parts.items() if u != me}
        if len(others) != 1:
            skipped_group += 1  # group threads and sender-less system messages are not 1:1 evidence
            continue
        (url, nm), = others.items()
        s = stats[url]
        s["name"] = s["name"] or nm
        for _, r in g.iterrows():
            s["from_me" if r["SENDER PROFILE URL"] == me else "from_them"] += 1
            d = r["DATE"]
            if pd.notna(d):
                s["first"] = d if s["first"] is None or d < s["first"] else s["first"]
                s["last"] = d if s["last"] is None or d > s["last"] else s["last"]
    meta = {"my_url": me, "conversations": int(df["CONVERSATION ID"].nunique()),
            "skipped_group_or_system": skipped_group}
    return meta, dict(stats)


def load_google():
    """Google Contacts + Other contacts, merged with each other by email."""
    persons = []
    for fname, saved in (("contacts.csv", True), ("other_contacts.csv", False)):
        df = read_opt(fname)
        if df is None:
            continue
        ecols = [c for c in df.columns if c.startswith("E-mail") and c.endswith("Value")]
        pcols = [c for c in df.columns if c.startswith("Phone") and c.endswith("Value")]
        for _, r in df.iterrows():
            name = " ".join(x for x in (r.get("First Name"), r.get("Middle Name"), r.get("Last Name"))
                            if isinstance(x, str)).strip()
            raw = emails_of(r, ecols)
            emails = {e for e in raw if not is_self(e)}
            if raw and not emails:
                continue  # a contact card for one of my own addresses
            if not name and not emails:
                continue
            persons.append({
                "name": name or (label_for(sorted(emails)[0]) if emails else ""),
                "company": r.get("Organization Name") if isinstance(r.get("Organization Name"), str)
                else ("" if name or not emails else sorted(emails)[0].split("@")[1]),
                "title": r.get("Organization Title") if isinstance(r.get("Organization Title"), str) else "",
                "emails": emails, "g_saved": saved,
                "g_phone": saved and any(isinstance(r.get(c), str) and r.get(c).strip() for c in pcols),
                "g_other": not saved, "named": bool(name),
            })
    # merge rows sharing an email (a person can sit in both lists)
    by_email, merged = {}, []
    for p in persons:
        hit = next((by_email[e] for e in p["emails"] if e in by_email), None)
        if hit is None:
            merged.append(p)
            hit = p
        else:
            hit["g_saved"] |= p["g_saved"]
            hit["g_phone"] |= p["g_phone"]
            hit["g_other"] |= p["g_other"]
            hit["emails"] |= p["emails"]
            if not hit["named"] and p["named"]:
                hit["name"], hit["named"] = p["name"], True
            hit["company"] = hit["company"] or p["company"]
        for e in p["emails"]:
            by_email[e] = hit
    return merged


def load_calendar(today):
    since = today - timedelta(days=LOOKBACK_DAYS)
    per = defaultdict(lambda: {"count": 0, "last": None, "display": ""})
    events = 0
    seen = set()
    for f in sorted(glob.glob(os.path.join(DATA, "calendar", "*.json"))):
        for e in json.load(open(f)).get("events", []):
            if e.get("id") in seen or e.get("status") == "cancelled":
                continue
            seen.add(e.get("id"))
            att = [a for a in e.get("attendees", []) if not a.get("resource")]
            mine = [a for a in att if a.get("self") or is_self(a.get("email", ""))]
            if any(a.get("responseStatus") == "declined" for a in mine):
                continue
            others = [a for a in att if not a.get("self") and not is_self(a.get("email", ""))]
            if not others or len(att) > MAX_MEETING_ATTENDEES:
                continue
            st = e.get("start", {})
            d = pd.to_datetime(st.get("dateTime") or st.get("date"), utc=True, errors="coerce")
            if pd.isna(d) or d.to_pydatetime() < since or d.to_pydatetime() > today + timedelta(days=1):
                continue
            events += 1
            for a in others:
                if a.get("responseStatus") == "declined":
                    continue
                s = per[a["email"].lower()]
                s["count"] += 1
                s["display"] = s["display"] or a.get("displayName", "")
                s["last"] = d if s["last"] is None or d > s["last"] else s["last"]
    return events, dict(per)


def load_tags():
    """Optional hand-tagged set keyed by LinkedIn URL (column names come from config "tags")."""
    df = read_opt(TAGS["file"]) if TAGS.get("file") else None
    out = {}
    if df is None:
        return out
    txt = lambda r, c: r.get(c).strip() if c and isinstance(r.get(c), str) else ""
    for _, r in df.iterrows():
        u = norm_url(r.get(TAGS["url_col"]))
        if u:
            out[u] = {"tag": txt(r, TAGS["tag_col"]).lower(), "name": txt(r, TAGS["name_col"]),
                      "company": next((txt(r, c) for c in TAGS["company_cols"] if txt(r, c)), ""),
                      "title": txt(r, TAGS["title_col"])}
    return out


# ---------------------------------------------------------------- matching


class NameIndex:
    """Index of LinkedIn people by exact first|last and by cross-script consonant skeleton."""

    def __init__(self, people):
        self.exact, self.swap, self.skel = defaultdict(set), defaultdict(set), defaultdict(set)
        self.full = {}
        for i, p in enumerate(people):
            n = norm_name(p["name"])
            fl = first_last(n)
            if not fl:
                continue
            self.full[i] = n
            self.exact[fl].add(i)
            self.swap[(fl[1], fl[0])].add(i)
            for a in skeletons(fl[0]):
                for b in skeletons(fl[1]):
                    if a and b:
                        self.skel[(a, b)].add(i)

    def match(self, name):
        """Return (ids, method, confidence). Only high/medium are merged by the caller."""
        n = norm_name(name)
        fl = first_last(n)
        if not fl:
            return [], "", ""
        hits = self.exact.get(fl, set())
        if len(hits) == 1:
            i = next(iter(hits))
            same = self.full[i] == n
            return [i], "name_exact" if same else "name_middle_dropped", "high" if same else "medium"
        if len(hits) > 1:
            return sorted(hits), "name_ambiguous", "low"
        hits = self.swap.get(fl, set())
        if len(hits) == 1:
            return sorted(hits), "name_swapped", "medium"
        cand = set()
        for a in skeletons(fl[0]):
            for b in skeletons(fl[1]):
                cand |= self.skel.get((a, b), set())
        if not cand:
            return [], "", ""
        hebrew = bool(HEB.search(n)) and len(n.split()) <= 3
        core = lambda t: max((x.strip("^$") for x in skeletons(t)), key=len)
        short = min(len(core(fl[0])), len(core(fl[1]))) < 2
        two_words = len(cand) == 1 and len(self.full[next(iter(cand))].split()) == 2
        if two_words:  # Hebrew spelling runs ~50-120% of the Latin length (Ran != Ronen)
            other = self.full[next(iter(cand))].split()
            two_words = all(0.5 <= len(h) / max(len(e), 1) <= 1.2 for h, e in zip(fl, other))
        if len(cand) == 1 and hebrew and not short and two_words:
            return sorted(cand), "name_transliterated", "medium"
        return sorted(cand)[:5], "name_skeleton" if len(cand) == 1 else "name_skeleton_ambiguous", "low"


# ---------------------------------------------------------------- scoring


def score(p, today):
    parts, strong = [], False
    cutoff = today - timedelta(days=LOOKBACK_DAYS)
    if p["li_two_way"] == "Y":
        recent = p["li_last_msg"] is not None and p["li_last_msg"].to_pydatetime().replace(tzinfo=timezone.utc) >= cutoff
        parts.append(("li_2way" if recent else "li_2way_old", 2 if recent else 1))
        strong = True
    if p["g_saved_contact"] == "Y":
        parts.append(("phone_saved", 2) if p["g_has_phone"] == "Y" else ("saved_no_phone", 1))
        strong |= p["g_has_phone"] == "Y"
    elif p["g_other_contact"] == "Y":
        parts.append(("other_contact", 1))
    if p["cal_meetings"]:
        parts.append(("meeting", 2))
        strong = True
    if p["tag"] in TAGS["warm_values"]:
        parts.append(("tag_" + p["tag"], 2))
        strong = True
    total = sum(v for _, v in parts)
    breakdown = f"{total} = " + " + ".join(f"{k}{v}" for k, v in parts) if parts else "0"
    tier = "WARM" if total >= 3 and strong else "KNOWN" if total >= 1 else "COLD"
    return total, breakdown, tier


def is_self(e):
    e = e.lower()
    return e in MY_EMAILS or bool(SELF_RE and SELF_RE.search(e))


def handle_name(e):
    """'jane.doe@x' -> 'Jane Doe'; '' when the handle is not clearly first+last."""
    toks = [t for t in re.split(r"[._\-]+", re.sub(r"\d+", "", e.split("@")[0])) if len(t) >= 2]
    return " ".join(t.capitalize() for t in toks) if len(toks) >= 2 else ""


def label_for(e):
    """Display label for a person known only by email: a name if the handle spells one, else masked."""
    local, _, dom = e.partition("@")
    return handle_name(e) or f"{local[:1]}*** @{dom}"


def mask(e):
    u, _, d = e.partition("@")
    return (u[:1] + "***@" + d) if d else "***"


# ---------------------------------------------------------------- main


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--config", default="")
    ap.add_argument("--today", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    ap.add_argument("--lookback-days", type=int, default=730)
    ap.add_argument("--max-attendees", type=int, default=8)
    args = ap.parse_args()
    global DATA, MY_EMAILS, SELF_NAMES, SELF_RE, LOOKBACK_DAYS, MAX_MEETING_ATTENDEES, FS_PATTERN, FS_EXCLUDE
    DATA, LOOKBACK_DAYS, MAX_MEETING_ATTENDEES = args.data_dir, args.lookback_days, args.max_attendees
    cfg_path = args.config or os.path.join(DATA, "roster_config.json")
    cfg = json.load(open(cfg_path, encoding="utf-8")) if os.path.exists(cfg_path) else {}
    if not cfg:
        print(f"WARNING: no config at {cfg_path}: your own rows will not be filtered")
    MY_EMAILS = {e.lower() for e in cfg.get("self_emails", [])}
    SELF_NAMES = {norm_name(n) for n in cfg.get("self_names", [])}
    SELF_RE = re.compile(cfg["self_email_regex"], re.I) if cfg.get("self_email_regex") else None
    TAGS.update(cfg.get("tags", {}))
    if cfg.get("sector_extra_regex"):
        FS_PATTERN = re.compile(FS_BASE + "|" + cfg["sector_extra_regex"], re.I)
    if cfg.get("sector_exclude_regex"):
        FS_EXCLUDE = re.compile(cfg["sector_exclude_regex"], re.I)
    today = datetime.strptime(args.today, "%Y-%m-%d").replace(tzinfo=timezone.utc)

    # 1. LinkedIn people = connections + message counterparts
    people = load_connections()
    for p in people:
        p["src"] = {"li_connection"}
    by_url = {p["linkedin_url"]: p for p in people}
    msg_meta, msg = load_messages()
    for url, s in msg.items():
        p = by_url.get(url)
        if p is None:
            p = {"name": s["name"], "company": "", "title": "", "linkedin_url": url, "emails": set(),
                 "li_connected_on": None, "is_connection": False, "src": set()}
            people.append(p)
            by_url[url] = p
        p["src"].add("li_messages")
        p["li_msgs_from_me"], p["li_msgs_from_them"] = s["from_me"], s["from_them"]
        p["li_first_msg"], p["li_last_msg"] = s["first"], s["last"]

    # 2. Hand tags (keyed by LinkedIn URL)
    aug = load_tags()
    aug_unmatched = 0
    for url, a in aug.items():
        p = by_url.get(url)
        if p is None:
            aug_unmatched += 1
            p = {"name": a["name"], "company": a["company"], "title": a["title"], "linkedin_url": url,
                 "emails": set(), "li_connected_on": None, "is_connection": False, "src": set()}
            people.append(p)
            by_url[url] = p
        p["src"].add("tags")
        p["tag"] = a["tag"]

    n_linkedin = len(people)
    email_to_li = {e: i for i, p in enumerate(people) for e in p["emails"]}
    idx = NameIndex(people)
    review = []
    stats = defaultdict(int)

    # 3. Google people -> LinkedIn by email, then by name
    google = load_google()
    for g in google:
        hit = next((email_to_li[e] for e in g["emails"] if e in email_to_li), None)
        method, conf, ids = ("email", "high", [hit]) if hit is not None else (None, None, [])
        if hit is None and g["named"]:
            ids, method, conf = idx.match(g["name"])
        elif hit is None and handle_name(sorted(g["emails"])[0]):
            ids, method, conf = idx.match(handle_name(sorted(g["emails"])[0]))
            if conf == "high":  # a name spelled by an email handle is never better than medium
                method, conf = "email_handle_name", "medium"
            elif conf == "medium":
                method, conf = "email_handle_name", "low"
        stats[f"google_{conf or 'none'}"] += 1
        if conf in ("high", "medium"):
            p = people[ids[0]]
            if conf == "medium":
                review.append({"source": "google", "source_name": g["name"], "source_emails": ";".join(sorted(g["emails"])),
                               "method": method, "merged": "Y", "candidates": f"{p['name']} ({p['company']}) {p['linkedin_url']}"})
        else:
            if conf == "low":
                review.append({"source": "google", "source_name": g["name"], "source_emails": ";".join(sorted(g["emails"])),
                               "method": method, "merged": "N", "candidates": " || ".join(f"{people[i]['name']} ({people[i]['company']}) {people[i]['linkedin_url']}" for i in ids)})
            p = {"name": g["name"], "company": g["company"], "title": g["title"], "linkedin_url": "",
                 "emails": set(), "li_connected_on": None, "is_connection": False, "src": set()}
            people.append(p)
            method, conf = "", ""
        p["src"].add("g_contacts" if g["g_saved"] else "g_other")
        if g["g_saved"] and g["g_other"]:
            p["src"].add("g_other")
        p["emails"] |= g["emails"]
        p["g_saved"] = p.get("g_saved", False) or g["g_saved"]
        p["g_phone"] = p.get("g_phone", False) or g["g_phone"]
        p["g_other"] = p.get("g_other", False) or g["g_other"]
        if method and not p.get("match_method"):
            p["match_method"], p["match_confidence"] = method, conf
        p["company"] = p["company"] or g["company"]

    # 4. Calendar attendees -> people by email, then by display name (LinkedIn only)
    n_events, cal = load_calendar(today)
    email_to_p = {e: p for p in people for e in p["emails"]}
    for e, c in cal.items():
        p = email_to_p.get(e)
        how = "email"
        # try the display name (and each side of "עברית - English"), then a name spelled by the email handle
        tries = [(d.strip(), False) for d in re.split(r"\s+-\s+", c["display"]) if d.strip()] if c["display"] else []
        tries += [(handle_name(e), True)] if handle_name(e) else []
        low = None
        for cand, from_handle in tries if p is None else []:
            ids, method, conf = idx.match(cand)
            if from_handle:
                method, conf = "email_handle_name", {"high": "medium", "medium": "low"}.get(conf, conf)
            if conf in ("high", "medium"):
                p, how = people[ids[0]], method
                p.setdefault("match_method", method)
                p.setdefault("match_confidence", conf)
                break
            if conf == "low" and low is None:
                low = (cand, method, ids)
        if p is None and low:
            review.append({"source": "calendar", "source_name": low[0], "source_emails": e, "method": low[1], "merged": "N",
                           "candidates": " || ".join(f"{people[i]['name']} ({people[i]['company']}) {people[i]['linkedin_url']}" for i in low[2])})
        if p is None:
            how = "new"
            p = {"name": c["display"] or label_for(e), "company": e.split("@")[1], "title": "", "linkedin_url": "",
                 "emails": {e}, "li_connected_on": None, "is_connection": False, "src": set()}
            people.append(p)
            email_to_p[e] = p
        stats[f"cal_{how}"] += 1
        p["emails"].add(e)
        p["src"].add("calendar")
        p["cal_meetings"] = p.get("cal_meetings", 0) + c["count"]
        p["cal_last"] = max(filter(None, [p.get("cal_last"), c["last"]]))

    # 5. Flatten, score, write
    rows = []
    for p in people:
        fm, ft = p.get("li_msgs_from_me", 0), p.get("li_msgs_from_them", 0)
        r = {
            "name": p["name"], "company": p["company"], "title": p["title"], "linkedin_url": p["linkedin_url"],
            "emails": ";".join(sorted(p["emails"])),
            "li_connection": "Y" if p.get("is_connection") else "N",
            "li_connected_on": p["li_connected_on"].strftime("%Y-%m-%d") if p.get("li_connected_on") is not None and pd.notna(p["li_connected_on"]) else "",
            "li_msgs_from_me": fm, "li_msgs_from_them": ft, "li_two_way": "Y" if fm and ft else "N",
            "li_first_msg": p.get("li_first_msg"), "li_last_msg": p.get("li_last_msg"),
            "g_saved_contact": "Y" if p.get("g_saved") else "N", "g_has_phone": "Y" if p.get("g_phone") else "N",
            "g_other_contact": "Y" if p.get("g_other") else "N",
            "cal_meetings": p.get("cal_meetings", 0), "cal_last_meeting": p.get("cal_last"),
            "tag": p.get("tag", ""), "sources": ";".join(sorted(p["src"])),
            "match_method": p.get("match_method", ""), "match_confidence": p.get("match_confidence", ""),
            "fs_company": "Y" if isinstance(p["company"], str) and FS_PATTERN.search(p["company"])
                                and not FS_EXCLUDE.search(p["company"]) else "N",
        }
        r["score"], r["breakdown"], r["tier"] = score(r, today)
        for k in ("li_first_msg", "li_last_msg", "cal_last_meeting"):
            r[k] = r[k].strftime("%Y-%m-%d") if r[k] is not None and pd.notna(r[k]) else ""
        rows.append(r)
    df = pd.DataFrame(rows)
    my_url = (msg_meta or {}).get("my_url", "")
    df = df[~df["name"].map(norm_name).isin(SELF_NAMES) & ((df["linkedin_url"] != my_url) | (my_url == ""))]
    df["last_evidence"] = df[["li_last_msg", "cal_last_meeting"]].max(axis=1)
    df = df.sort_values(["score", "last_evidence"], ascending=False).drop(columns="last_evidence")
    df.to_csv(os.path.join(DATA, "roster.csv"), index=False)
    df.drop(columns=["emails"]).to_csv(os.path.join(DATA, "roster_sheet.csv"), index=False)
    pd.DataFrame(review).to_csv(os.path.join(DATA, "match_review.csv"), index=False)

    summary = {
        "people": len(df), "tiers": df["tier"].value_counts().to_dict(),
        "linkedin_people": n_linkedin, "messages": msg_meta or "MISSING (data/messages.csv or .zip not found)",
        "message_counterparts": len(msg), "tag_rows": len(aug), "tags_not_in_connections": aug_unmatched,
        "missing_inputs": MISSING,
        # freshness: the newest evidence each source carries (file dates are only download dates)
        "latest_evidence": {"li_connected_on": df["li_connected_on"].max(), "li_last_msg": df["li_last_msg"].max(),
                            "cal_last_meeting": df["cal_last_meeting"].max()},
        "google_people": len(google), "google_match": {k[7:]: v for k, v in stats.items() if k.startswith("google_")},
        "calendar_events_counted": n_events, "calendar_attendees": len(cal),
        "calendar_match": {k[4:]: v for k, v in stats.items() if k.startswith("cal_")},
        "low_confidence_listed": sum(r["merged"] == "N" for r in review),
        "medium_merged_listed": sum(r["merged"] == "Y" for r in review),
        "source_contribution": {s: int(df["sources"].str.contains(s).sum()) for s in
                                ("li_connection", "li_messages", "g_contacts", "g_other", "calendar", "tags")},
    }
    json.dump(summary, open(os.path.join(DATA, "roster_summary.json"), "w"), indent=1, default=str)
    print(json.dumps(summary, indent=1, default=str))


if __name__ == "__main__":
    main()
