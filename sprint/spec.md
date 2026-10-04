# Outreach sprint — process spec v0

*Created 2026-09-27 from run #1. Extracted into `.claude/skills/bdp-outreach-sprint/` on 2026-09-29, after run #2. The skill is now the method; this file keeps the run log and the build-eval verdicts. Directions config for runs 1–2: `sprint/directions_2026-09.json`.*

## Purpose
- **Trigger:** a waiting moment (one deal gates the thesis), a thin pipeline, or the urge to build instead of sell.
- **Output:** a closed list of 15–20 people to contact now. Each row has a named door, a dated why-now, a draft message and a channel.
- **Success metric:** messages actually sent to real doors within 5 working days. Artifacts don't count.

## Hard rules
- **Warmth means evidence:** a real conversation, email thread, meeting, saved number or shared work history. A LinkedIn connection alone counts as "known", not warm.
- **Reachability is a hard gate.** No named door and no opening line means the row goes to "No route yet".
- **Dated, sourced signals only.** Each row carries a signal URL and date. An undated signal is a hypothesis.
- **Exclusions:**
  - people already in motion
  - anyone who competes with an active client (Cal: Isracard, Max, acquirers in Israel)
  - companies in an M&A or sale process
  - partner-owned accounts, when the sprint is solo
- **Investor route:** map at least 3 relevant portfolio companies and a real mandate before asking for intros.
- **Don't name** referral partners (e.g. Thunes) or pre-signature clients (Cal) in outreach without their permission.
- **Pass/fail criteria are set before sending.** They may be revised only before the first send, and the reason must be logged.

## Stages
| # | Stage | Output | Time (Amos) | Sources |
|---|---|---|---|---|
| 0 | Warm roster | One sheet with person, company, evidence type + last date, warmth, tags. Refreshed each sprint, never synced | ~50 min | LinkedIn export (Connections + Messages), Google Contacts incl. "Other contacts", phone, calendar, earlier contact sets |
| 1 | Diagnose | Stuck type (dependency-wait, thin funnel, no sized first yes, wrong channel, energy) and pipeline math against the current decision criterion | ~45 min | Memory, Drive logs, pipeline sheet, Gmail 30–45 days, market scan, ≤4 closed questions |
| 2 | Directions | Up to 5 directions scored 0–2 on 7 lines. The incumbent thesis is always included | ~30 min | Scorecard below |
| 3 | Hypothesis | One direction, smallest first yes, pass/fail with dates and failure diagnostics | ~15 min | Template below |
| 4 | Persona + signals | Buyer titles, company filter, ranked signals, channel and message rules | — | target-profile.md, engine-method.md |
| 5 | The list | 15–20 ranked rows in a Drive sheet | ~90 min review + send | Connections export × dated signals (funding lists, press releases, licences, event lists) |
| 6 | Send + learn | Warmest first, rest in a second batch; day-10 review against the criteria; update the roster and memory | ~10 min/day | Pipeline sheet, Gmail, scheduled review |

## Direction scorecard (0–2 per line, total out of 14)
1. Right to win
2. Doors (solo / new people)
3. First yes before the decision date
4. Deal size vs the reference deal
5. Dated why-now
6. Fit with active client work
7. Founder pull

**Gate:** could you name 15 doors this week? If not, the direction becomes a research track, not the sprint.

## Row score (0–2 each, total out of 8)
Fit (new market or new unit, in the ICP) + signal age (≤6 months = 2, 6–12 = 1, >12 = 0) + door (warm-tagged = 2, senior and known = 1, junior or indirect = 0) + role (owns expansion/partnerships = 2, other C-level = 1, other = 0). Always show the breakdown.

## Hypothesis template
> [Segment] with [dated trigger] and [gap] will take a [20-min call] about [smallest first yes], because [right to win].

Record with it:
- **Test:** N sends by [date].
- **Pass:** ≥X replies and ≥Y calls by [date + 14 days], plus ≥1 proposal requested by [date + ~30 days].
- **If it fails:**
  - no replies → door or opener is wrong
  - replies but no calls → the offer is too big or vague
  - calls but no proposal → the target profile or timing is wrong

## Message rules
- ≤90 words.
- Open with their dated signal.
- One line on what BD Partners does.
- One question about their next market.
- Ask for 20 minutes or a pointer to the right person.
- English by default; Hebrew for Israeli WhatsApp contacts.
- No unverifiable claims, no naming partners or clients.

## Build-eval verdicts (2026-09-27)
- **Sprint as a skill:** make it a skill, after run 2. Pass test: run 1 gets ≥15 sends in 5 days and ≥3 calls booked in 14 days.
- **Skill as an agent:** defer. Trigger: 3 completed sprints. The first automation candidate is the day-10 reply check, as a scheduled task.
- **"Living" contacts database:** don't build. Build a one-off warm roster instead. Fallback if monthly re-exports get painful: trial Dex ($12–20/mo according to the vendor) rather than build. Merge with Micha's tool only after the partnership agreement is signed, as who-knows-whom lookups rather than pooled records.
- **Set aside:** Anthropic Sales plugin (overlaps the bdp skills); Apollo / Clay / Lusha (only if finding cold signals becomes the bottleneck); folk (from $30/user/mo).

## Run log
### Run #1 — 2026-09-27
- **Constraints:** solo, new people only, done in 2–3 days, ~5 hours of Amos's time.
- **Diagnosis:** short of commitments, not conversations. 10 meetings are booked Sep 30–Oct 8, but none carries a sized ask. It's a dependency-wait on the Cal go-call (Oct 6). Connector work (5 intros in 45 days) is unpriced.
- **Scorecard:**
  - Second Cal, buyer chooses the market: 10
  - Second Cal, US only: 10
  - Selling Israel to foreign fintech infrastructure: 9 (0 doors)
  - Israeli incumbents' new units: 8
  - Singapore / India: 6

  Chosen: second Cal with the market chosen by the buyer. The US is tested, not bet on.
- **Hypothesis:** Israel-HQ fintech/payments/FS companies setting 2027 international targets, with no BD muscle in the target market, will take a call about a 3-week target-market map (NIS 30K).
- **List:** 14 rows passed the gates (2 warm-tagged, 12 known), plus 2 "no route yet" and 6 excluded. Sheet: "Outreach sprint #1 — 2026-09-27" in Drive › customers and pipeline.
- **Pass/fail:** originally ≥6 replies / ≥4 calls, which assumed warm doors. Revised before any send: if Amos marks ≥7 rows warm, keep 6/4; otherwise ≥4 replies and ≥3 calls by Oct 14, and ≥1 proposal requested by Oct 31.
- **US test:** if ≥40% of calls name the US as their 2027 market, the mid-October sprint goes US-first (Melodi / Dror for US doors).
- **Parked direction:** selling Israel to foreign fintechs becomes the mid-October sprint if partners (Thunes, Salt Edge, Eko) produce ≥5 warm intros to people who own Israel at foreign fintechs by Oct 14.
- **Open items:** cross-check doors against the LinkedIn Messages export; Google Contacts export; add the persona and signal rules to target-profile.md (needs Amos's OK).

### Run #2 — 2026-09-29
- **Direction:** D1 (Israel-HQ fintech/payments that sell abroad) and D4 (incumbents' new units) combined. Discount-group doors held. Founder pull accepted.
- **Pool:** 102 roster doors (41 WARM, 61 KNOWN-senior). Web-checked for a dated signal and the M&A gate.
- **List:**
  - 13 rows passed the gates (7 WARM, 6 KNOWN), 2 short of the 15-row floor. Not padded.
  - 11 rows are in "No dated signal / No route yet", mostly WARM connectors and investors with no dated trigger.
  - 14 groups are excluded or held.
  - Sheet: "Outreach sprint #2 — 2026-09-29" in Drive › customers and pipeline.
- **Top rows:**
  - Global-e 8 = fit2 + signal2 + door2 + role2
  - ThetaRay 7 = 2+1+2+2
  - Mastercard IL 7 = 1+2+2+2
  - Riskified 7 = 2+2+1+2
- **Gate kills this run:**
  - M&A: Payoneer (Nuvei, 2026-06-15), BioCatch (Visa, 2026-08-03), Papaya (sale talks).
  - Cal competitor plus M&A: esh (Isracard).
  - Held: Leumi (Micha overlap), until Amos decides.
- **Pass/fail (set before the first send):**
  - Sends Oct 4–8.
  - By Oct 22: replies ≥ round(0.4·7 + 0.1·6) = **3**; calls ≥ round(0.25·7 + 0.05·6) = **2**.
  - By Nov 12: ≥1 proposal requested.
  - If rows are added from "No dated signal" before the first send, recompute the thresholds with the same formula and log the reason.
- **US test (carried over):** if ≥40% of calls name the US as the 2027 market, the next sprint goes US-first via Dror.
- **Lesson:** 5 of 13 rows have role 0. The WARM doors in this segment sit below the expansion owner, so most sends are pointer asks. If replies arrive with no calls, the door is wrong, not the opener.
- **Revision before the first send (2026-09-29, logged per the hard rule):**
  - **What happened:** a full scan of every pipeline tab (xlsx export, `in_motion_scan.py`) found 5 listed companies already in motion: Justt (meeting set), Vayu (1st meeting set), Pontera, Mastercard IL (reached out) and Nayax (reached out). It also moved 4 "No dated signal" people to Excluded, because their threads are live (PassportCard, Wiserpay, Intuit, Meitav).
  - **Cause:** the Drive text reader returns one sample row per tab, and run #2 trusted it.
  - **List now:** **8 rows (4 WARM, 4 KNOWN)**.
  - **Thresholds recomputed** with the same formula: replies ≥ round(0.4·4 + 0.1·4) = **2**; calls ≥ round(0.25·4 + 0.05·4) = **1**, by Oct 22. Still ≥1 proposal requested by Nov 12.
  - **Sheets:** the sheet of record is "Outreach sprint #2 — 2026-09-29 (v2)". The original is renamed "SUPERSEDED, do not send".
- **Run #2 results:**
  - direction D1+D4, 102 doors → 13 draft rows → 8 sendable;
  - gate kills: 4 M&A or client-competitor, 9 in motion found late, plus the held groups;
  - 0 sends as of 2026-09-29 (holiday week; window Oct 4–8).
- **Lessons folded into the skill:**
  - scan the whole pipeline workbook before any research;
  - yield is about 1 sendable row per 13 doors;
  - WARM doors often sit below the expansion owner, so ask for a pointer;
  - check M&A before drafting.
- **Skill extraction ahead of its pass test:** the build-eval pass test (run #1 ≥15 sends in 5 days, ≥3 calls in 14) is unmet and still open: 3 sends so far. Extracted on the founder's explicit request, 2026-09-29. Re-check at the run #1 day-10 review, Oct 9. If run #1 fails, the skill stays, but the failure diagnostic is logged against it.

### Run #3 — 2026-10-04
- **Direction:** CONNECTORS, fixed by the founder. The roster was rebuilt with the relationship-history layer: 388 WARM-fresh, 38 WARM-stalled, 19 WARM-other. Details are in `sprint/run-03.md`.
- **Funnel:** 78 persona matches → 67 passed the door gate → 22 researched → 5 passed the book and need-signal gates (3 IL, 2 SG/SEA). The foreign geography is SG/SEA, the only one with ≥5 WARM-fresh connectors.
- **Pass/fail (pre-registered):** 10–15 sends Oct 11–15. By Oct 29: ≥5 replies, ≥3 conversations, ≥4 companies offered. By Nov 14: ≥1 discovery meeting. The IL and SEA slices have separate thresholds.
- **Result:** 5 rows is below the 10-send floor, so the test cannot run as registered. Re-open bucket: 1 (news only). Doors to build: US, UK, DACH, GCC.
- **Lesson:** the binding constraint is need-signal companies (4 IL, 3 SG sourced), not doors. Supply of warm, not-in-motion, signal-backed doors is under 10 per sprint, so outreach moves to three instruments: weekly reconnection, signal alerts, one-to-many.
