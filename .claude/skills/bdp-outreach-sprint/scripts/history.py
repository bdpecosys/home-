"""Relationship-history layer for the warm roster (called by build_roster.py --history).

Warmth says how well the founder knows someone. History says what happened the last time business
came up: a stalled pitch or a dead partnership talk is not a fresh warm door. For every WARM and
KNOWN person this derives:

  last_business_date, last_business_topic   date + topic label of the last pitch/discussion, if any
  outcome                                   active | stalled | closed-lost | referral-only |
                                            never-pitched | personal-only
  outcome_intent                            "low" when the thread is live but unlikely to buy
  outcome_source, outcome_confidence        which evidence decided (confirmed > high > medium >
                                            low > inherited)
  company_status                            the company-level outcome, when there is one
  history_tier                              WARM-fresh | WARM-stalled | WARM-other | KNOWN | COLD
  geo, geo_source                           region and the signal that decided it

Message content never reaches an output. Subjects, meeting titles, pipeline statuses and log lines
are classified in memory into a label; only the label, a date and the source name are written.

Sources (all read from the gitignored data dir; see roster_config.example.json "history"):
  pipeline workbook(s) .xlsx     every tab; rows with a status are classified
  sprint workbooks .xlsx         rows whose status says sent / reached out = active since that date
  gmail/*.json                   search_threads pages (in:sent), classified per counterpart email
  calendar/*.json                via build_roster.py: business meetings per attendee
  LinkedIn messages              via build_roster.py: who spoke last and unanswered count
  history_seeds.csv              founder facts and labels read from the logs
  history_overrides.csv          the founder's corrections; always wins
  company_hq.csv                 optional company -> region map for geography

Seed/override columns: key_type (company|name|email|url), key, outcome, intent, date, topic, source.
A company key is a regex matched against the company field.
"""
import os
import re
from collections import defaultdict
from datetime import timedelta

import pandas as pd

OUTCOMES = ("active", "stalled", "closed-lost", "referral-only", "never-pitched", "personal-only")
CONF_RANK = {"confirmed": 5, "high": 4, "medium": 3, "low": 2, "inherited": 1, "": 0}
SEVERITY = {"closed-lost": 4, "stalled": 3, "active": 2, "referral-only": 1}

# topic labels for the "what was pitched or discussed" field (first match wins)
TOPICS = [
    ("salesforce-co-sell", r"salesforce|appexchange|netsuite|co-?sell|go-?live|\bisv\b|oracle"),
    ("signal-platform", r"signal|alpha|platform demo|\bdemo\b|monitor"),
    ("market-entry", r"market[- ]entry|expansion|international|origination|italy|salone|cross-border|global"),
    ("fractional-bd", r"fractional|retainer|\bbd\b support"),
    ("corpdev-m&a", r"m&a|corp ?dev|acquisi|merger|pmi"),
    ("proposal", r"proposal|agreement|contract|הצעה|הסכם"),
    ("referral-partnership", r"referr|partner|שת\"?פ|שיתוף|intro|connect|<>|\bx\b"),
    ("discovery-call", r"discovery|intro call|pitch|catch ?up|meeting|call|sync|zoom|meet|פגישה|שיחה"),
]
PERSONAL = re.compile(r"birthday|b-?day|יום הולדת|dinner|wedding|חתונה|family|משפחה|kids|ילדים|doctor|רופא|"
                      r"dentist|gym|yoga|holiday|חג|vacation|חופש|party|מסיבה|brit|ברית|funeral|הלוויה", re.I)
PITCH_TOPICS = {"salesforce-co-sell", "signal-platform", "market-entry", "fractional-bd", "corpdev-m&a", "proposal",
                "discovery-call"}

# pipeline status vocabulary (checked in this order)
ST_LOST = re.compile(r"said no|replied no|^\s*no\s*$|proposal - no|not interested|prob(ably|\.)? dead|likely dead|"
                     r"\bdead\b|halting|bad (call|mtg)|discovery - no|no budget|not comm?itted|no need|\blost\b|"
                     r"declin|disqualif", re.I)
ST_STALL = re.compile(r"no response|no reply|\bnr\b|2nd follow|3 fu|fu's|last try|waiting|waitng|maybe later|"
                      r"^later|to fu\b|follow[- ]?up|following up|proposal sent|sent proposal|propose sent|"
                      r"proposal - maybe|reach(ed)?[- ]out|\bsent\b|to sched|to set|to schedule|speak in two|"
                      r"deferred|to renew|to finalize|to confrim|to confirm", re.I)
ST_REF = re.compile(r"referr|to connect|connected|he will connect|asked for intros|suggest(ed)? (general|intos|intros)|"
                    r"open to meet and help|advisor", re.I)
ST_ACTIVE = re.compile(r"schedu|meeting set|call set|call booked|call sched|kick-?off|weekly|catching up|catchup|"
                       r"\bmet\b|spoke|closed|\bclose\b|customer|signed|offer pilot|interested|open to|"
                       r"want to hear|generally accepted|discovery|intro call|pitch call|first call|second call|"
                       r"1st call|interact|propose\b", re.I)
DATE_DMY = re.compile(r"\b(\d{1,2})\.(\d{1,2})\.(\d{2})\b")

GENERIC_MAIL = re.compile(r"@(gmail|googlemail|yahoo|hotmail|outlook|live|icloud|me|walla|proton(mail)?|aol|"
                          r"msn|zahav\.net)\.", re.I)

# geography
REGIONS = ("Israel", "US", "UK", "DACH", "rest of EU", "Singapore/SEA", "India", "GCC", "other")
CC = {"972": "Israel", "1": "US", "44": "UK", "49": "DACH", "43": "DACH", "41": "DACH", "91": "India",
      "971": "GCC", "966": "GCC", "974": "GCC", "973": "GCC", "965": "GCC", "968": "GCC",
      "65": "Singapore/SEA", "60": "Singapore/SEA", "62": "Singapore/SEA", "66": "Singapore/SEA",
      "63": "Singapore/SEA", "84": "Singapore/SEA", "95": "Singapore/SEA", "855": "Singapore/SEA",
      "856": "Singapore/SEA", "673": "Singapore/SEA"}
# every 1- and 2-digit calling code; anything else is read as a 3-digit code
CALLING_CODES_SHORT = {"1", "7", "20", "27", "30", "31", "32", "33", "34", "36", "39", "40", "41", "43", "44", "45",
                       "46", "47", "48", "49", "51", "52", "53", "54", "55", "56", "57", "58", "60", "61", "62", "63",
                       "64", "65", "66", "81", "82", "84", "86", "90", "91", "92", "93", "94", "95", "98"}
EU_CC = {"33", "34", "39", "31", "32", "351", "353", "30", "46", "45", "358", "48", "420", "36", "40", "359", "385",
         "386", "421", "370", "371", "372", "352", "356", "357"}
TLD = {"il": "Israel", "uk": "UK", "de": "DACH", "at": "DACH", "ch": "DACH", "sg": "Singapore/SEA",
       "my": "Singapore/SEA", "id": "Singapore/SEA", "th": "Singapore/SEA", "ph": "Singapore/SEA",
       "vn": "Singapore/SEA", "in": "India", "ae": "GCC", "sa": "GCC", "qa": "GCC", "bh": "GCC", "kw": "GCC",
       "om": "GCC", "us": "US"}
EU_TLD = {"fr", "es", "it", "nl", "be", "pt", "ie", "gr", "se", "dk", "fi", "pl", "cz", "hu", "ro", "bg", "hr", "si",
          "sk", "lt", "lv", "ee", "lu", "mt", "cy", "eu"}
TEXT_GEO = [
    ("Singapore/SEA", r"singapore|\bpte\b|\bsea\b|south ?east asia|apac|malaysia|indonesia|jakarta|thailand|"
                      r"bangkok|vietnam|philippines|manila|kuala lumpur"),
    ("India", r"\bindia\b|private limited|\bpvt\b|mumbai|bangalore|bengaluru|delhi|gurgaon|hyderabad|pune|chennai"),
    ("GCC", r"dubai|abu dhabi|\buae\b|saudi|riyadh|qatar|doha|bahrain|kuwait|oman|\bgcc\b|\bdifc\b|\badgm\b"),
    ("DACH", r"germany|deutschland|gmbh|\bag\b|berlin|munich|münchen|frankfurt|hamburg|austria|vienna|wien|"
             r"switzerland|zurich|zürich|geneva|\bdach\b"),
    ("UK", r"\buk\b|united kingdom|london|england|scotland|manchester|\bplc\b"),
    ("rest of EU", r"europe|\beu\b|emea|france|paris|spain|madrid|barcelona|italy|milan|rome|netherlands|amsterdam|"
                   r"belgium|brussels|ireland|dublin|portugal|lisbon|poland|warsaw|sweden|stockholm|denmark|"
                   r"copenhagen|finland|cyprus|lithuania|vilnius|estonia|tallinn|czech|prague|greece|athens"),
    ("US", r"\busa\b|\bus\b|united states|new york|\bnyc\b|san francisco|silicon valley|boston|chicago|"
           r"los angeles|miami|texas|austin|seattle|delaware"),
    ("Israel", r"israel|ישראל|tel aviv|תל אביב|herzliya|הרצליה|jerusalem|ירושלים|haifa|חיפה|ramat gan|רמת גן|"
               r"petah tikva|פתח תקווה|\bltd\.? \(?il|בע\"?מ"),
]
HEB = re.compile(r"[֐-׿]")
VANITY_TLD = {"io", "ai", "co", "me", "tv", "cc", "vc", "ly", "so", "to", "gg", "fm", "sh", "ws", "la",
              "am", "xyz"}


def topic_of(text):
    t = str(text or "")
    for label, pat in TOPICS:
        if re.search(pat, t, re.I):
            return label
    return "other-business"


def meeting_kind(title):
    """'personal' or 'business' for a calendar title (the title itself is never stored)."""
    return "personal" if PERSONAL.search(str(title or "")) else "business"


def norm(s):
    s = re.sub(r"\(.*?\)", " ", str(s or "").lower())
    s = re.sub(r"[^\w֐-׿@.\- ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def phone_cc(raw):
    """Country calling code from a phone string, or ''. Israeli local numbers (0x...) map to 972."""
    s = re.sub(r"[^\d+]", "", str(raw or ""))
    if s.startswith("00"):
        s = "+" + s[2:]
    if s.startswith("+0"):
        s = s[1:]  # "+05x..." is a local number typed with a plus
    elif s.startswith("+"):
        d = s[1:]
        for n in (1, 2, 3):
            if d[:n] in CALLING_CODES_SHORT or (n == 3 and len(d) > 6):
                return d[:n]
        return ""
    if re.match(r"^0(5\d|[2-4]|[89]|7\d)\d{6,8}$", s):
        return "972"
    return ""


def ev_date(s):
    return str(s)[:10] if s and str(s) not in ("nan", "NaT") else ""


# ---------------------------------------------------------------- evidence collection


class Evidence:
    def __init__(self):
        self.person = defaultdict(list)  # key -> [ev]; keys: "email:x", "url:x", "name:x"
        self.company = []  # [(regex, ev)]

    def add(self, key_type, key, **ev):
        ev.setdefault("intent", "")
        ev.setdefault("topic", "")
        ev.setdefault("date", "")
        ev.setdefault("confidence", "medium")
        if key_type == "company":
            self.company.append((re.compile(key, re.I), ev))
        else:
            k = norm(key) if key_type == "name" else str(key).strip().lower()
            if k:
                self.person[f"{key_type}:{k}"].append(ev)


def load_seed_file(path, ev, source_default, confidence):
    if not os.path.exists(path):
        return 0
    df = pd.read_csv(path, dtype=str).fillna("")
    for _, r in df.iterrows():
        if not r["key"] or r["outcome"] not in OUTCOMES:
            continue
        ev.add(r["key_type"], r["key"], outcome=r["outcome"], intent=r.get("intent", ""), date=r.get("date", ""),
               topic=r.get("topic", ""), source=r.get("source", "") or source_default,
               confidence=r.get("confidence", "") or confidence, asof=r.get("asof", "") or r.get("date", ""))
    return len(df)


def classify_status(text, current):
    t = str(text or "").strip()
    if not t or t in ("-", "x", "v", "?"):
        return None
    if ST_LOST.search(t):
        return "closed-lost"
    if ST_REF.search(t):
        return "referral-only"
    if ST_STALL.search(t):
        return "active" if current else "stalled"
    if ST_ACTIVE.search(t):
        return "active" if current else "stalled"  # an old pitch with nothing newer has gone quiet
    return None


def header_row(d):
    for i in range(min(4, len(d))):
        cells = [str(v).lower() for v in d.iloc[i].tolist()]
        if any(re.search(r"compan|prospect|partner|\bname\b|person|contact", c) for c in cells):
            return i
    return None


def load_pipeline(paths, cfg, ev, today):
    tab_dates = {k.lower(): v for k, v in cfg.get("tab_dates", {}).items()}
    referral_tabs = {t.lower() for t in cfg.get("referral_tabs", [])}
    skip_tabs = {t.lower() for t in cfg.get("skip_tabs", [])}
    n = 0
    for path in paths:
        for tab, d in pd.read_excel(path, sheet_name=None, dtype=str, header=None).items():
            if tab.lower() in skip_tabs:
                continue
            h = header_row(d.fillna(""))
            if h is None:
                continue
            cols = [str(c).strip().lower() for c in d.iloc[h].fillna("")]
            body = d.iloc[h + 1:].fillna("")
            ci = next((i for i, c in enumerate(cols) if re.search(r"^(company|prospect|partner|target company)$", c)), None)
            pi = next((i for i, c in enumerate(cols) if re.search(r"^(person|contact|point of contact|name|"
                                                                   r"contact name|budget owner)$", c)), None)
            si = [i for i, c in enumerate(cols) if re.search(r"status|response|stage|^channel$", c)]
            for _, r in body.iterrows():
                vals = [str(v) for v in r.tolist()]
                row_txt = " ".join(vals)
                status = " | ".join(vals[i] for i in si if i < len(vals) and vals[i].strip())
                is_ref_tab = tab.lower() in referral_tabs
                dmy = [f"20{y}-{int(m):02d}-{int(dd):02d}" for dd, m, y in DATE_DMY.findall(row_txt)
                       if 1 <= int(m) <= 12 and 1 <= int(dd) <= 31]
                date = max(dmy) if dmy else tab_dates.get(tab.lower(), "")
                current = bool(date) and pd.Timestamp(date, tz="UTC") >= today - timedelta(days=cfg.get("current_days", 30))
                outcome = "referral-only" if is_ref_tab and status and not ST_LOST.search(status) \
                    else classify_status(status, current)
                if outcome is None:
                    continue
                company = vals[ci].strip() if ci is not None and ci < len(vals) else ""
                person = vals[pi].strip() if pi is not None and pi < len(vals) else ""
                e = dict(outcome=outcome, date=date, topic=topic_of(row_txt), source=f"pipeline:{tab}",
                         confidence="high" if date else "low")
                if person and len(person.split()) >= 2 and len(person) < 40:
                    ev.add("name", person, **e, company_hint=company)
                    n += 1
                if company and len(company) >= 3 and not is_ref_tab:
                    ev.add("company", r"(?<![a-z])" + re.escape(norm(company).split(" (")[0]) + r"(?![a-z])", **e)
                    n += 1
    return n


def load_sprints(paths, ev):
    """Rows whose status says sent / reached out / commented -> active since that date (person and company)."""
    n = 0
    for path in paths:
        d = pd.read_excel(path, dtype=str).fillna("")
        cols = {c.lower(): c for c in d.columns}
        sc = next((cols[c] for c in cols if c == "status"), None)
        pc = next((cols[c] for c in cols if c in ("person", "name")), None)
        cc = next((cols[c] for c in cols if c == "company"), None)
        if not sc:
            continue
        for _, r in d.iterrows():
            st = r[sc]
            if not re.search(r"sent|reached out|comment", st, re.I):
                continue
            m = DATE_DMY.search(st)
            date = f"20{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}" if m else ""
            src = f"sprint:{os.path.basename(path)}"
            kind = "comment" if re.search(r"comment", st, re.I) and not re.search(r"sent", st, re.I) else "send"
            only = re.search(r"\bto (\w+)\s*$", st, re.I)  # "sent on ld to miri": one of the named people
            if kind == "send":
                for nm in re.split(r"\s*(?:/|\+|,| and )\s*", r[pc]):
                    if only and not nm.lower().startswith(only.group(1).lower()):
                        continue
                    if len(nm.split()) >= 2:
                        ev.add("name", nm, outcome="active", date=date, topic="market-entry", source=src,
                               confidence="high", company_hint=r[cc])
                        n += 1
            ev.add("company", r"(?<![a-z])" + re.escape(norm(r[cc])) + r"(?![a-z])", outcome="active", date=date,
                   topic="market-entry", source=src + (" (post comment)" if kind == "comment" else ""),
                   confidence="high")
    return n


def load_gmail(gdir, is_self, ev, today):
    """Per counterpart email: last activity, who spoke last, whether they ever replied, topic."""
    per = defaultdict(lambda: {"threads": 0, "last": "", "last_from_me": False, "replied": False,
                               "my_last": "", "topics": [], "first": ""})
    seen = set()
    import glob as _g
    import json as _j
    for f in sorted(_g.glob(os.path.join(gdir, "*.json"))):
        for th in _j.load(open(f)).get("threads", []):
            if th.get("id") in seen:
                continue
            seen.add(th.get("id"))
            msgs = sorted(th.get("messages", []), key=lambda m: m.get("date", ""))
            if not any(is_self(m.get("sender", "")) for m in msgs):
                continue  # only threads the founder wrote in are business attempts
            parties = set()
            for m in msgs:
                for a in [m.get("sender", "")] + m.get("toRecipients", []) + m.get("ccRecipients", []):
                    a = a.lower().strip()
                    if a and "@" in a and not is_self(a):
                        parties.add(a)
            topic = topic_of(" ".join(m.get("subject", "") for m in msgs))  # classified in memory, not stored
            for a in parties:
                s = per[a]
                s["threads"] += 1
                s["topics"].append(topic)
                for m in msgs:
                    d = m.get("date", "")[:10]
                    snd = m.get("sender", "").lower()
                    if snd == a:
                        s["replied"] = True
                    if d >= s["last"]:
                        s["last"], s["last_from_me"] = d, is_self(snd)
                    if is_self(snd) and d > s["my_last"]:
                        s["my_last"] = d
                    s["first"] = min(filter(None, [s["first"], d])) if s["first"] else d
    for a, s in per.items():
        age = (today - pd.Timestamp(s["last"], tz="UTC")).days if s["last"] else 9999
        topic = next((t for t in reversed(s["topics"]) if t in PITCH_TOPICS), s["topics"][-1])
        if not s["replied"]:
            outcome = "active" if age <= 21 else "stalled"
        elif age <= 45 or (age <= 60 and not s["last_from_me"]):
            outcome = "active"
        elif topic == "referral-partnership":
            outcome = "referral-only"
        elif topic in PITCH_TOPICS:
            outcome = "stalled"
        else:
            outcome = None
        if outcome:
            ev.add("email", a, outcome=outcome, date=s["last"], topic=topic, confidence="medium",
                   source=f"gmail:{s['threads']} thread(s), last {'from me' if s['last_from_me'] else 'from them'}"
                          f"{'' if s['replied'] else ', never replied'}")
    return len(per)


# ---------------------------------------------------------------- resolution


def pick(evs):
    """Latest evidence wins; undated sorts oldest; ties go to the more severe outcome, then confidence.
    A founder-confirmed fact counts as of the day it was stated ("asof"), so only newer evidence beats it."""
    eff = lambda e: max(e["date"] or "0000", e.get("asof") or "0000") if e["confidence"] == "confirmed" \
        else (e["date"] or "0000")
    return max(evs, key=lambda e: (eff(e), SEVERITY.get(e["outcome"], 0), CONF_RANK[e["confidence"]]))


def geo_of(r, hq, cc):
    comp = str(r.get("company", ""))
    if cc:
        if cc in CC:
            return CC[cc], f"phone +{cc}"
        return ("rest of EU" if cc in EU_CC else "other"), f"phone +{cc}"
    for region, pat in TEXT_GEO:
        if re.search(pat, comp, re.I):
            return region, "company text"
    for e in str(r.get("emails", "")).split(";"):
        if "@" in e and not GENERIC_MAIL.search(e):
            tld = e.rsplit(".", 1)[-1].lower()
            if tld in TLD:
                return TLD[tld], f"email .{tld}"
            if tld in EU_TLD:
                return "rest of EU", f"email .{tld}"
            if len(tld) == 2 and tld not in VANITY_TLD:
                return "other", f"email .{tld}"
    for pat, region in hq:
        if pat.search(comp):
            return region, "company HQ"
    if HEB.search(str(r.get("name", ""))) or HEB.search(comp):
        return "Israel", "Hebrew script"
    return "unknown", ""


def apply(df, data_dir, hcfg, today, is_self):
    """Add the history columns to df (the roster) and return (df, ambiguous, summary)."""
    ev = Evidence()
    p = lambda f: os.path.join(data_dir, f)
    counts = {
        "seeds": load_seed_file(p(hcfg.get("seeds", "history_seeds.csv")), ev, "seed", "confirmed"),
        "overrides": load_seed_file(p(hcfg.get("overrides", "history_overrides.csv")), ev, "founder correction",
                                    "confirmed"),
        "pipeline_rows": load_pipeline([p(x) for x in hcfg.get("pipeline_workbooks", []) if os.path.exists(p(x))],
                                       hcfg, ev, today),
        "sprint_sends": load_sprints([p(x) for x in hcfg.get("sprint_workbooks", []) if os.path.exists(p(x))], ev),
        "gmail_counterparts": load_gmail(p(hcfg.get("gmail_dir", "gmail")), is_self, ev, today),
    }
    overrides, notes = set(), {}
    if os.path.exists(p(hcfg.get("overrides", "history_overrides.csv"))):
        o = pd.read_csv(p(hcfg.get("overrides", "history_overrides.csv")), dtype=str).fillna("")
        overrides = {f"{t}:{norm(k) if t == 'name' else k.lower()}" for t, k in zip(o.key_type, o.key)}
        # optional columns: "company" (the person moved; replaces the export's company) and "note" (e.g. a route)
        for _, x in o[o.key_type == "name"].iterrows():
            notes[norm(x.key)] = (x.get("company", ""), x.get("note", ""))
        df = df.copy()
        moved = df["name"].map(lambda n: notes.get(norm(n), ("", ""))[0])
        df.loc[moved != "", "company"] = moved[moved != ""]
    hq = []
    if os.path.exists(p(hcfg.get("company_hq", "company_hq.csv"))):
        for _, r in pd.read_csv(p(hcfg.get("company_hq", "company_hq.csv")), dtype=str).fillna("").iterrows():
            hq.append((re.compile(r"(?<![a-z])(?:" + r["company_regex"] + r")(?![a-z])", re.I), r["region"]))
    no_inherit = re.compile(hcfg["no_inherit_regex"], re.I) if hcfg.get("no_inherit_regex") else None
    max_inherit = hcfg.get("max_inherit", 30)
    era = hcfg.get("bdp_era_start", "")
    company_size = df[df.tier.isin(["WARM", "KNOWN"])].company.str.lower().value_counts()

    out = []
    for _, r in df.iterrows():
        x = {k: (v if isinstance(v, str) or pd.notna(v) else "") for k, v in r.items()}
        cc = str(x.get("phone_cc", "") or "")
        geo, geo_src = geo_of(r, hq, cc)
        row = {"phone_cc": cc, "geo": geo, "geo_source": geo_src, "history_note": notes.get(norm(r["name"]), ("", ""))[1]}
        if r.tier not in ("WARM", "KNOWN"):
            row.update(outcome="", history_tier=r.tier)
            out.append(row)
            continue
        comp = norm(r.company)
        keys = [f"email:{e.lower()}" for e in str(r.emails).split(";") if e] + \
               ([f"url:{r.linkedin_url.lower()}"] if r.linkedin_url else []) + [f"name:{norm(r['name'])}"]
        evs = []
        for k in keys:
            for e in ev.person.get(k, []):
                hint = norm(e.get("company_hint", ""))
                if k.startswith("name:") and hint and (not comp or (hint.split()[0] not in comp
                                                                     and comp.split()[0] not in hint)):
                    continue  # same name at another (or an unknown) company
                # a founder correction, or a founder-confirmed fact about this person, stands until changed
                evs.append(dict(e, override=k in overrides or e["confidence"] == "confirmed"))
        # calendar (business meetings) and LinkedIn metadata from build_roster
        if x.get("cal_next"):
            evs.append(dict(outcome="active", date=x["cal_next"], topic=x.get("cal_topic", "discovery-call"),
                            source="calendar: upcoming meeting", confidence="high", intent=""))
        elif x.get("cal_biz_last"):
            age = (today - pd.Timestamp(x["cal_biz_last"], tz="UTC")).days
            later = max([e["date"] for e in evs if e["date"]], default="")
            if age <= 30:
                evs.append(dict(outcome="active", date=x["cal_biz_last"], topic=x.get("cal_topic", ""),
                                source="calendar: recent meeting", confidence="medium", intent=""))
            elif x.get("cal_topic") in PITCH_TOPICS and later <= x["cal_biz_last"] and \
                    str(r.li_last_msg or "") <= x["cal_biz_last"]:
                evs.append(dict(outcome="stalled", date=x["cal_biz_last"], topic=x.get("cal_topic", ""),
                                source="calendar: meeting, nothing after", confidence="low", intent=""))
        li_last = str(r.li_last_msg or "")
        if int(x.get("li_unanswered") or 0) >= 2 and era and li_last >= era and \
                (today - pd.Timestamp(li_last, tz="UTC")).days > 21:
            evs.append(dict(outcome="stalled", date=li_last, topic="", source=f"linkedin: {x['li_unanswered']} "
                            "unanswered from me", confidence="low", intent=""))
        # company-level evidence
        cevs = [e for pat, e in ev.company if comp and pat.search(comp)]
        cbest = pick(cevs) if cevs else None
        row["company_status"] = f"{cbest['outcome']} ({cbest['source']}, {cbest['date'] or 'undated'})" if cbest else ""

        # company-level evidence joins the person's own when it is strong: founder-confirmed, or dated and high
        # confidence and protective (a stalled/lost pitch or a referral-only relationship), at a company small
        # enough that one thread speaks for it
        inheritable = cbest is not None and (
            cbest["confidence"] == "confirmed" or (
                cbest["confidence"] == "high" and cbest["date"]
                and cbest["outcome"] in ("stalled", "closed-lost", "referral-only")
                and not (no_inherit and no_inherit.search(comp))
                and company_size.get(r.company.lower(), 0) <= max_inherit))
        cands = evs + ([dict(cbest, source=f"company: {cbest['source']}", inherited=True)] if inheritable else [])
        forced = [e for e in cands if e.get("override")]
        if cands:
            best = pick(forced or cands)
            conf = ("confirmed" if best.get("override") else
                    "confirmed" if best["confidence"] == "confirmed" else
                    "inherited" if best.get("inherited") else best["confidence"])
        else:
            personal = int(x.get("cal_personal") or 0) > 0 and not x.get("cal_biz_last")
            bare = r.g_has_phone == "Y" and not str(r.company).strip() and not str(r.title).strip()
            label = "personal-only" if personal or bare else "never-pitched"
            best, conf = dict(outcome=label, date="", topic="", intent="",
                              source="no business evidence" + (" (personal meetings only)" if personal else
                                                               " (saved phone, no company)" if bare else "")), \
                "medium" if personal else "low" if bare else "medium"
        biz = [e for e in evs + ([cbest] if cbest and conf == "inherited" else []) if e.get("date")]
        lb = max(biz, key=lambda e: e["date"]) if biz else None
        row.update(outcome=best["outcome"], outcome_intent=best.get("intent", ""), outcome_source=best["source"],
                   outcome_date=best.get("date", ""), outcome_confidence=conf,
                   last_business_date=lb["date"] if lb else "", last_business_topic=(lb.get("topic") or "other-business") if lb else "",
                   evidence_outcomes=";".join(sorted({e["outcome"] for e in evs})),
                   n_evidence=len(evs))
        if r.tier == "WARM":
            o, intent = best["outcome"], best.get("intent", "")
            row["history_tier"] = ("WARM-stalled" if o in ("stalled", "closed-lost") else
                                   "WARM-other" if o == "referral-only" or (o == "active" and intent == "low") else
                                   "WARM-fresh")
        else:
            row["history_tier"] = r.tier
        out.append(row)
    h = pd.DataFrame(out, index=df.index)
    df = pd.concat([df, h], axis=1)

    # the outcome labels most worth a human check: WARM first, low confidence, conflicting evidence
    w = df[df.tier.isin(["WARM", "KNOWN"])].copy()
    cstat = w.company_status.fillna("").str.split(" ").str[0]
    w["amb"] = (
        (w.tier == "WARM") * 4 + (w.fs_company == "Y") * 2
        + w.outcome_confidence.map({"low": 3, "inherited": 1, "medium": 1}).fillna(0)
        + w.evidence_outcomes.fillna("").str.count(";") * 2
        + ((w.outcome_date.fillna("") == "") & ~w.outcome.isin(["never-pitched", "personal-only"])) * 2
        + ((cstat != "") & (cstat != w.outcome)) * 2
        - (w.outcome_confidence == "confirmed") * 20
        - ((w.outcome == "never-pitched") & (w.company_status.fillna("") == "") & (w.n_evidence == 0)) * 5
    )
    amb = w.sort_values(["amb", "score"], ascending=False).head(hcfg.get("ambiguous_n", 30))
    summary = {
        "inputs": counts,
        "history_tiers": df.history_tier.value_counts().to_dict(),
        "outcomes_warm": df[df.tier == "WARM"].outcome.value_counts().to_dict(),
        "outcomes_known": df[df.tier == "KNOWN"].outcome.value_counts().to_dict(),
        "geo_by_tier": {t: df[df.history_tier == t].geo.value_counts().reindex(list(REGIONS) + ["unknown"],
                                                                             fill_value=0).to_dict()
                        for t in ("WARM-fresh", "WARM-stalled", "WARM-other", "KNOWN")},
        "geo_sources_warm_known": df[df.tier.isin(["WARM", "KNOWN"])].geo_source.replace("", "none")
                                    .value_counts().to_dict(),
    }
    return df, amb, summary
