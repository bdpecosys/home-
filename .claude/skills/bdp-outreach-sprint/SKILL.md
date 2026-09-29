---
name: bdp-outreach-sprint
description: Run a BD Partners outreach sprint that turns a stuck moment into 8–20 real people to contact this week. Each row gets a named door, a dated and sourced why-now, a draft message and a channel. The sprint builds a warm roster from contact exports, diagnoses the stall, scores directions with doors counted from the roster, sets a pass/fail hypothesis and builds the gated list. Use WHENEVER the founder says "I'm stuck", "pipeline is thin", "waiting on a deal", "waiting for X to sign", "who should I reach out to", "who do I call this week", "new direction", "what should I sell next", or feels the urge to build instead of sell. Also for rerunning a sprint ("next sprint", "build the list", "day-10 review"). Decides WHO to contact and WHY NOW from the founder's own network; NOT for scoring a handed-over org list (bdp-target-screen), one named call (bdp-call-prep) or build decisions (bdp-build-eval).
---

# BDP Outreach Sprint

A sprint turns a waiting moment into sends. It succeeds when messages go to real doors within 5 working days. A good-looking sheet doesn't count. Everything below exists to stop three failures seen in real runs:
- presenting a LinkedIn connection as a warm path;
- drafting to companies that are about to be sold;
- padding the list to hit a number.

Before starting, read the live context. Don't hard-code it here, because it goes stale:
- `bdp-model.md`: what is sold, the reference deal and prices.
- `target-profile.md`: ICP, gates, the warm-path definition.
- `engine-method.md`: signal taxonomy.
- The pipeline sheet and the previous sprint sheets, which tell you who is in motion.
- The run log (in this repo, `sprint/spec.md`), which holds earlier runs, their thresholds and what they taught.

## Working mode
- Give verdicts with explicit reasoning, not menus. Numbers come first.
- Scoring is additive, with the breakdown shown inline: `7 = fit2 + signal1 + door2 + role2`.
- Every factual claim carries a source URL and a date. An unknown scores 0 and is flagged. Never round an assumption up.
- Personal contact data stays in a gitignored `data/` folder. Outputs carry counts, dates and names, never message content, and never emails in anything shared.
- Stop for the founder's approval after stage 3 (the hypothesis). Don't build the list on an unapproved direction.

## Stages

| # | Stage | Output | Stop? |
|---|---|---|---|
| 0 | Warm roster | `roster.csv` plus a summary. Rebuild only when `latest_evidence` in the summary is more than 30 days old, or new exports arrived | Report counts, stop if thresholds are new |
| 1 | Diagnose | Stuck type plus pipeline math | — |
| 2 | Directions | Up to 5 directions on the 7-line card, doors computed, sensitivity table, verdict | — |
| 3 | Hypothesis | One testable sentence, test dates, pass/fail from the actual W/K mix | **Stop for approval** |
| 4 | The list | Ranked, gated rows in a Drive sheet, plus "No dated signal / No route yet" and "Excluded / Held" sections | Report |
| 5 | Send + learn | Warmest first. Day-10 review against pass/fail. Log the run | — |

### Stage 0: Warm roster
Run `scripts/build_roster.py`. It merges these sources in a gitignored data dir:
- LinkedIn Connections and Messages;
- Google Contacts and "Other contacts";
- calendar pages;
- an optional hand-tagged set.

1. Get the exports:
   - Ask the founder for the LinkedIn data export (Connections plus Messages) and the Google Contacts CSVs.
   - Pull the calendar with the connector: 24 months back, one JSON file per page, into `data/calendar/`.
   - Large Drive files come back as base64. Decode them into `data/`.
   - If a big download keeps expiring, ask for a zip. `messages.zip` works as-is.
2. Create `data/roster_config.json` from `scripts/roster_config.example.json`. It holds:
   - your own addresses and names, so you don't appear as your own contact;
   - the named companies that count as in-sector;
   - the tag file's columns.
3. Run it:
   ```
   python scripts/build_roster.py --data-dir data --today YYYY-MM-DD
   ```
   It prints a JSON summary. Check `missing_inputs` first, then check the tier counts against the last run.
4. Report back:
   - the counts per tier;
   - the source contribution;
   - the match rates;
   - the 30 warmest people in the sector;
   - a calibration sample of about 10 WARM and 10 KNOWN rows.

   The founder corrects thresholds before anything downstream uses them. Scoring and tiers are in `references/warmth-rubric.md`.
5. Upload a copy without emails (`roster_sheet.csv`) as a Google Sheet, split into parts if large.

Matching rules that held up in runs 1–2 (the script enforces them):
- Never auto-merge a low-confidence match. List it in `match_review.csv`.
- Hebrew↔Latin name matching uses consonant skeletons with vowel head/tail markers. An unconstrained version was wrong about 25% of the time.
- A name taken from an email handle is at most medium confidence.
- The company field beats email domains, because merged contacts carry stale domains.
- Calendar events with more than 8 attendees, declined events and group message threads are not relationship evidence.

### Stage 1: Diagnose
**Check for open sprints first.** Read the run log and the last sprint sheet. The diagnosis is "finish sprint N" if either:
- sprint N's sends haven't gone out;
- its day-10 review is less than 10 days away.

In that case, give the send plan and the review date, and stop. A new sprint on top of an unsent one only adds artifacts.

Pull the calendar for the next 14 days (the stage 0 pull only looks back), and read the pipeline sheet tabs.

Name the stuck type, and back it with numbers from the pipeline sheet, the calendar for the next 14 days, and 30–45 days of email subjects. Never quote email bodies. The stuck types:
- **dependency-wait:** one pending decision gates the thesis;
- **thin funnel:** too few live threads;
- **no sized first yes:** meetings exist but none carries a priced ask;
- **wrong channel;**
- **energy.**

Then do the pipeline math against the current decision date: live threads × historical conversion ≥ the commitments needed. Ask at most 4 closed questions, and only where the data can't answer. The verdict is one line: "Stuck type = X, because [numbers]. The sprint must produce [Y] by [date]." See the output format below.

### Stage 2: Directions
Score up to 5 directions on the 7-line card in `references/direction-scorecard.md`. Always include the incumbent thesis.
- The doors line is **computed from the roster, not guessed**:
  ```
  python scripts/count_doors.py --roster data/roster.csv --config <directions.json>
  ```
- Keep the directions config (company regexes, the in-motion regex, held accounts) next to the run log, not in this skill.
- Read the "top matched companies" the script prints before trusting a count. Keyword regexes misfire:
  - "ntu" inside Intuit;
  - "wise" catching unrelated firms;
  - "& co" catching banks;
  - cyber firms landing in a fintech bucket.
- Include:
  - a sensitivity table: each total with door counts ±30%, and with the most uncertain line moved ±1;
  - the pre-registered tie-break: within 1 point, more WARM doors wins.
- Give a verdict. A combination of two directions is allowed when their company sets don't overlap and they share a buyer message.
- **Yield check.** In runs 1–2, about 1 in 8 doors became a draft row and 1 in 13 became a sendable row once the gates and signal search ran (102 doors gave 13 draft rows, and 8 once the full in-motion scan ran). If a direction has fewer than ~200 doors, say up front that 15 rows is unlikely. Don't discover it at the end.

### Stage 3: Hypothesis
Use `references/hypothesis-template.md`: the smallest first yes, a test with send dates, and pass/fail thresholds computed from the expected W/K mix. Stop and ask for approval.

### Stage 4: The list
Work company by company, cheapest gates first, so no research is spent on rows that will die:
1. **In motion.** Scan every tab of the pipeline workbook and the earlier sprint sheets with `scripts/in_motion_scan.py`:
   - export each sheet as .xlsx and decode it into `data/`;
   - run the scan, then decide each hit by hand.

   The Drive text reader shows only one sample row per tab. In run 2, trusting it put 5 in-motion companies on the list ("meeting set", "reached out"); the full scan caught them before any send. Company-level status counts: a second pitch to a different person at a company with a live thread confuses both threads.

   Exclude:
   - anyone whose company has a live status in the pipeline or an earlier sprint sheet (sent, drafted, reached out, meeting set, proposal). An idea-only row with no contact doesn't count;
   - anyone with a meeting booked in the next 14 days;
   - anyone met in the last ~21 days: flag them for the founder instead, since it may already be a live thread.
2. **Active-client competitors**, which the client file names.
3. **Partner-owned or held accounts.** A partner's former employer counts as a likely overlap: hold it, and let the founder decide.
4. **M&A or sale process.** Run one web search per company: "<company> acquisition 2026" or "<company> sale talks". In run 2 this gate killed 4 companies that had WARM doors: two definitive acquisitions, one company in sale talks, and one being bought by a client's competitor. IPO preparation is not a sale, and an acquirer is not being sold.
5. **Signal.** Find a dated, sourced why-now: a funding round, new market, licence, partnership, results with an international line, an executive move or an event.
   - Age scores ≤6 months = 2, 6–12 months = 1, older = 0.
   - A row with an old but real signal can stay, scoring 0 on age.
   - A row with no dated signal goes to "No dated signal / No route yet". Don't invent one.
6. **Door and role.** Pick the best door at the company, and name one alternate door in notes. When the WARM door doesn't own expansion (role 0), the message asks for a pointer, not a meeting. Run 2 had 5 of 13 draft rows like this, which is normal for warm networks: they sit one level below the expansion owner.
7. **Investor or connector routes.** First map ≥3 relevant portfolio companies and a real mandate. Until then the row goes to "No route yet".
8. **Score and draft.**
   - Row score = fit + signal age + door + role, 0–2 each, with the breakdown shown. Anchors are in `references/message-rules.md`.
   - Draft per `references/message-rules.md`: ≤90 words, count them, and use Hebrew for Israeli WhatsApp contacts.

**Don't pad.** The target is 15–20 rows. If fewer pass, ship what passed, say how many short it is, and list the cheapest way to promote rows from "No dated signal", for example "a dated signal for any 2 of these 3 WARM founders gets you to 15".

Sheet columns, one sheet with a `section` column:

`section, rank, name, company, title, tier, row_score, breakdown, why_now, signal_date, source_url, channel, draft, draft_words, notes`

- The sections are `LIST`, `NO DATED SIGNAL / NO ROUTE YET` and `EXCLUDED / HELD`.
- An excluded row states its reason and its source URL.
- Title it "Outreach sprint #N — YYYY-MM-DD" and put it in the pipeline output folder.
- Upload with Drive `create_file` using `text/csv`, which converts to a Sheet.
- Read it back to confirm the row count. The `fileSize` in the create response is not reliable.

### Stage 5: Send + learn
- Send the warmest first, and the rest in a second batch.
- Record each send's date in the sheet.
- Day-10 review:
  - count replies and calls against the thresholds;
  - check the failure diagnostic in the hypothesis template;
  - update the roster tags (a new real conversation makes the person WARM).
- Log the run in the run log: direction, pool, rows (W/K), gate kills, thresholds, lesson.
- The first automation candidate is the day-10 reply check as a scheduled task, and only after 3 completed sprints.

## Output format for stages 1–3
```
## Stage 1: Diagnosis
Stuck type: <type>. <2–4 lines of numbers, each with its source and date>
The sprint must produce: <commitment> by <date>.

## Stage 2: Directions
| Direction | Right to win | Doors (W/K) | First yes | Deal size | Why-now | Client fit | Founder pull | Total |
Sensitivity: <table>. Tie-break: <applied or not>.
Verdict: <direction>, because <reason>. Yield check: <doors → expected rows>.

## Stage 3: Hypothesis
<template sentence> | Test | Pass | If it fails
```

## Tooling notes from real runs
- **Web fetches of news sites are often blocked by the proxy.**
  - Use search-result snippets, plus URLs that carry the date in their path.
  - When only the month is known, write "YYYY-MM (day unverified)".
- **A quota or rate error on a Drive upload:**
  - commit the local work first;
  - retry once;
  - read the file back.
- **Sheets:** the Drive text reader samples one row per tab; export as .xlsx for anything that must be complete. Reading .xlsx needs `openpyxl`.
- **Heavy work** runs in the cloud session, not on the founder's machine. Never commit anything from `data/`.

## Files
- `references/warmth-rubric.md`: evidence scoring, tiers, what a door is, choosing the channel.
- `references/direction-scorecard.md`: the 7 lines with 0/1/2 anchors, the doors line, sensitivity, tie-break.
- `references/hypothesis-template.md`: the sentence, the test, the pass/fail formula, failure diagnostics, sub-tests.
- `references/message-rules.md`: row-score anchors, message rules, draft skeletons in English and Hebrew.
- `scripts/build_roster.py`: stage 0. `--data-dir`, `--config`, `--today`, `--lookback-days`, `--max-attendees`.
- `scripts/count_doors.py`: stage 2 doors line from the roster and a directions config.
- `scripts/in_motion_scan.py`: stage 4 gate 1, candidate companies and surnames against every tab of the pipeline and sprint workbooks.
- `scripts/roster_config.example.json`: copy it to `data/roster_config.json` and fill it in.
