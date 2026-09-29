# Outreach sprint #2 — prompt sequence for claude.ai/code

Paste the prompts one at a time. Each one ends by stopping for your answer, so nothing runs past a decision that's yours to make.

Before prompt 0:
- Put the exports into the Drive folder **roster-inputs**:
  - LinkedIn archive (`Connections.csv`, `messages.csv`)
  - Google Contacts CSV (~4K)
  - "Other contacts" CSV (~5.8K)
- Connect Google Calendar in claude.ai's connector settings.

---

## Prompt 0 — Setup and connector check

```
First, find "bdp-code-pack.zip" in my Google Drive (search by title), download it, unzip it into the repo root (it contains CLAUDE.md, PROMPTS.md, sprint/, .claude/skills/, .gitignore), and commit it with the message "Add BDP context pack". Then read CLAUDE.md and:
1. List the MCP servers/tools available in this session (/mcp). Confirm Google Drive, Gmail and Google Calendar are usable by making one read-only call to each (Drive: list recent files; Gmail: search "in:sent newer_than:3d"; Calendar: list events for the last 7 days). Report what works and which Google account each one is authenticated as.
2. Pull the six knowledge files listed in CLAUDE.md (bdp-model, engine-method, target-profile, house-style, track-record, roles-and-cadence) from Drive into context/ as .md files, unchanged. Do NOT pull cal-engagement.md into the repo.
3. Find the Drive folder "roster-inputs" and list its files with sizes. Tell me which of these are present: LinkedIn Connections, LinkedIn messages, Google Contacts, Google Other contacts.
4. Commit context/ with message "Add BDP knowledge mirrors". Commit nothing from roster-inputs.
Stop and report. Keep it short.
```

## Prompt 1 — Stage 0: build the warm roster (one-off script, not a system)

```
Stage 0 of the outreach sprint (see sprint/spec.md). Goal: one table of my real relationships, where warmth = evidence, not connection.

Build scripts/build_roster.py (stdlib + pandas only) that runs on files in data/ (gitignored):
- Download from Drive "roster-inputs": LinkedIn Connections.csv (it has a 3-line notes preamble before the header), LinkedIn messages.csv, Google Contacts CSV, Google Other contacts CSV. Decode any base64 tool-result files into data/.
- LinkedIn messages: per counterpart (key = profile URL, fall back to name), compute msgs_from_me, msgs_from_them, two_way (both > 0), first_date, last_date. Never write message content to any output.
- Join messages to Connections on profile URL. Keep people who message me but aren't connections.
- Google Contacts: saved contact (Y/N), has_phone (Y/N), emails. Other contacts: emailed at least once (Y/N). Match to LinkedIn by email first, then by normalized full name (handle Hebrew/English variants, casing, middle names). Record match_method and match_confidence. Never auto-merge low-confidence matches; list them separately.
- Calendar (Calendar connector, primary calendar, last 24 months): per attendee email, meetings_count and last_meeting.
- Aug 31 contact set (Drive ID in CLAUDE.md): carry over my hand tags (warm/hot).

Warmth score, transparent and additive, breakdown shown per row:
- LinkedIn two-way conversation with last message ≤24 months = 2; two-way but older = 1; one-way = 0
- Saved Google contact with phone = 2; saved without phone = 1; Other contacts only = 1
- Calendar meeting in the last 24 months = 2
- My Aug 31 tag warm/hot = 2
- Tier:
  - WARM: score ≥3, including at least one of (two-way LinkedIn, phone saved, meeting, my tag)
  - KNOWN: score 1–2
  - COLD: score 0

Output:
- data/roster.csv with columns: name, company, title, linkedin_url, emails (masked in any printout), each evidence field, score + breakdown, tier.
- Upload a Google Sheet "Warm roster — <today>" to the "customers and pipeline" folder with the same columns, minus emails.

Report back:
- counts per tier, and how many people each source contributed
- match rates
- the 15 warmest people at fintech, payments or financial-services companies
- a calibration sample: 10 random WARM and 10 random KNOWN rows (name, company, breakdown)

I'll correct the thresholds before anything uses them. Stop after the report.
```

## Prompt 2 — Stages 1–3: re-diagnose, re-score directions, set the hypothesis

```
Rerun stages 1–3 of sprint/spec.md. Run #1 (Sep 27) is logged there. Its direction scores were within one point of each other (10/10/9/8/6), and the "doors" line was estimated by hand. This rerun replaces estimates with roster evidence.

1. Diagnose.
   - Read the newest entries of the strategy log, the pipeline sheet tabs sep26-pipe and sep26-connectors, and Gmail since Sep 27 (in:sent and inbound from people, not newsletters).
   - Check the run #1 sheet's Stage column and find any replies to those 14 people.
   - Ask me at most 4 closed questions, including: did the Cal call on Oct 6 happen and what was decided, and which run #1 messages did I actually send.
   - Output: the stuck type, plus pipeline math against my end-of-December test (Cal signed + one similar deal close to signing). State the assumptions explicitly.
2. Directions.
   - Re-score, on the 7-line card in the spec (0–2 each): second Cal with the buyer choosing the market; second Cal US-only; selling Israel to foreign fintech infrastructure; Israeli incumbents' new units; Singapore/India; plus any direction the evidence now suggests.
   - The "doors" line must be computed from the roster: the number of WARM and KNOWN-senior people at companies that fit each direction. Show the counts and name up to 3 examples each.
   - Add a sensitivity table: does the winner change if any single judgment line moves by ±1?
   - Pre-registered tie-break: within 1 point, the direction with more WARM doors wins.
   - Give a verdict.
3. Hypothesis.
   - Use the spec's template: smallest first yes, a test with dates, pass/fail thresholds set from the actual warm/known mix, how to read a failure, and the US sub-test.
Stop for my approval before building the list.
```

## Prompt 3 — Stages 4–5: persona, signals, and the list

```
Build the sprint #2 list for the approved hypothesis.
- Persona and signals: buyer titles, company filter, and ranked signals from context/target-profile.md.
- Exclusions:
  - people already in motion (per the pipeline sheet and logs)
  - anyone already messaged in run #1
  - competitors of an active client (Cal: Isracard, Max, and acquirers in Israel)
  - companies in M&A or sale processes
  - Micha's accounts (Airwallex, Bridgewise, Jeen, D4, Qiz)
- Universe:
  - roster companies that fit the direction
  - dated signals from the last 12 months (funding, launches, licences, executive hires, event participation), each with a source URL and date
  - use bdp-target-screen logic for the company layer
- 15–20 rows, WARM first. Every row needs a named door and an opening line (hard gate). Anyone who fails the gate goes to a "no route yet" list, with what would open the door.
- Row score = fit + signal age + door (from roster tier) + role, 0–2 each, with the breakdown shown.
- Drafts: ≤90 words. Open with their dated signal, one line on BD Partners, one question about their next market, and ask for 20 minutes or a pointer to the right person. Don't name Thunes or Cal. English by default; Hebrew if I've messaged them in Hebrew before (you can tell from the language in the messages; don't quote any content).
- Channel: WhatsApp if a phone number is saved, email if there's a Gmail thread, otherwise LinkedIn.
- Output: a Google Sheet "Outreach sprint #2 — <date>" in "customers and pipeline", with the same columns as the run #1 sheet plus warmth evidence. Report the top 10 in chat.
Stop.
```

## Prompt 4 — Turn it into a skill (run #2 = second use, so extract now)

```
Extract the skill from runs #1 and #2. Use the skill-creator conventions if you have them.
- Create .claude/skills/bdp-outreach-sprint/:
  - SKILL.md: frontmatter with name and a description that triggers on "I'm stuck", "pipeline is thin", "waiting on a deal", "who should I reach out to", "new direction". The body gives the stages, gates, scorecards and exclusions from sprint/spec.md, updated with what runs #1–2 taught.
  - references/: warmth-rubric.md, direction-scorecard.md, hypothesis-template.md, message-rules.md
  - scripts/build_roster.py: the script from prompt 1, parameterised
- Keep it under ~500 lines of SKILL.md. No personal or client data anywhere in the skill.
- Dry-run the skill against today's state and show me the first two stages it would produce. Fix anything that misfires.
- Append the run #2 results to the run log in sprint/spec.md.
- Commit, and produce a zip of the skill folder that I can upload to claude.ai as well.
Stop.
```

## Prompt 5 — Agent: evaluate before building

```
Run bdp-build-eval on "turn bdp-outreach-sprint into an agent".
- Candidates:
  - (a) a day-10 review that checks Gmail/Calendar for replies to sprint rows and updates the Stage column
  - (b) a monthly roster refresh reminder
  - (c) a weekly signal sweep for roster companies
- Use evidence from runs #1–2 and the deferral trigger in the spec (3 completed sprints).
- Give a verdict per candidate using the skill's template.
- Build only what gets BUILD (minimal), and only as a scheduled task that calls the skill. For everything deferred, write the trigger into sprint/spec.md.
```
