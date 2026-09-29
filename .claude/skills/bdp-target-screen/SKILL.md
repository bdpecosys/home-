---
name: bdp-target-screen
description: Score, rank and group a UNIVERSE of organisations for BD Partners — either the target map for a client's market-entry engagement (buyers and channel partners in a target market, often anchored to a conference) or BD Partners' own prospect universe. Turns a raw longlist (Deep Research run, exhibitor or speaker list, association directory) into a prioritised, role-tagged, reachability-gated target map with transparent additive scoring. Use WHENEVER there is a LIST of organisations to screen, score, rank, prioritise or segment — e.g. "score this target list", "screen these companies", "rank the Italian universe", "build the target map", "who from this exhibitor list should we meet" — or right after a Deep Research run returns a longlist. This is the MANY-organisations triage engine, NOT deep intel on one named prospect (bdp-call-prep), NOT a prospect-facing pitch (bdp-pitch-teaser), NOT the paid deliverable (bdp-market-entry-paths). Trigger even if someone only pastes a list and asks to prioritise it.
---

# BDP Target-Screen: the triage engine

Turns a raw universe into a ranked, role-tagged shortlist that feeds real conversations. It does the triage; it does not do the selling, and it does not invent access.

Before scoring, read the shared knowledge files for live context: `target-profile.md` (ICP, gates, warm-path definition, signal preferences), `engine-method.md` (pipeline schema and signal taxonomy), and, for a client engagement, that client's engagement file. Never hard-code pipeline facts into this skill; they go stale.

## Two modes — declare which one is running

**Mode A — Client market-entry universe.** Screening organisations in a target market on behalf of a client. The universe splits into **buyers** (who could buy the client's product), **channel partners** (systems integrators, consultancies, distributors, platform vendors, associations who reach the buyers), **competitors** and **influencers** (regulators, industry bodies, event organisers). Channel targets are scored on reach, not on their own appetite to buy.

**Mode B — BD Partners' own prospect universe.** Screening companies that could become BDP clients. Same machinery, different fit axis (see below).

## Where it sits in the flow
Longlist built (Deep Research, exhibitor/speaker lists, association directories, filings) → **this skill scores, groups and ranks it** → the human owner fills reachability → pick the few to take into conversation → outreach → meeting prep runs per named target (`bdp-call-prep`). Enrichment tools, if any, come after the pick, never before.

## Input expectations
A list of organisations with, ideally: segment, size, country, ownership, source link, and any observed signal with its date. Tiers usually arrive together — strict matches and partial matches. Keep the tiers; they carry information. If fields are missing, score what is present and flag the gap. Never invent a value to complete a row.

## Three axes — keep them separate
Collapsing these into one number hides the answer.
1. **Fit** — how good a target, given the mandate.
2. **Role and use case** — buyer / channel / competitor / influencer, and which pitch they would hear.
3. **Access** — is there a named door and an opening line.

The pick is the intersection: strong fit × a use case you can actually demonstrate × a real door.

## Axis 1 — Fit score (transparent, additive, interrogable)
No black-box number. Every point traces to evidence, shown as a breakdown.

**Mode A (market entry), each 0–2:**
- **Segment fit** — does the client's product solve a problem this organisation demonstrably has.
- **Capacity to buy** — budget, procurement route, tender history, prior spend on comparable systems.
- **Why-now signal** — a dated, named signal from the taxonomy (regulatory deadline, core-system replacement, published tender, new executive with the mandate, funding or programme allocation, event participation). Unknown scores 0 and is flagged; never round intent upward.
- **Access at the anchor event** — attending, exhibiting or speaking at the event the engagement is anchored to. This is both a signal and a bookable route.
- **(Channel targets only) Reach** — installed base or client base among the buyer segment, replacing segment fit.

**Mode B (BDP's own prospects), each 0–2:** new business unit standing up with revenue ambition and no BD muscle · parent size and pre-scale unit · employment signals (business-side roles posted recently, no senior BD in seat) · live why-now signal (new market entity, new global exec, conference presence, partnership announcements).

Fit = sum (0–8 or 0–10). Always show it inline: `Fit 6 = segment2 + capacity1 + why-now2 + event1`. That line is the point.

## Axis 2 — Role and use case
Tag every row: buyer / channel / competitor / influencer. For buyers, tag the use case the client's product serves them. For channels, tag what they would actually do (resell, integrate, refer, co-sell, host) and what they get out of it. A channel with no stated reason to cooperate is a wish, not a target.

## Axis 3 — Access (human column, never fabricated)
Warm / known / cold, filled by the person who owns the relationship. A warm path is a real prior conversation, shared work history or a live thread — a connection on a social network is not a warm path. The engine may surface a **hint** ("ex-colleague plausibly there", "spoke at the same event"), explicitly labelled as a hint to check, never as a claimed relationship. **No named door and no opening line is a hard gate, not a scoring column**: such rows go to a separate "no route yet" list rather than the shortlist.

## Output
One table, ranked by fit, matching the pipeline schema in `engine-method.md`, offered as CSV:

```
Organisation | Role | Segment | Tier | Fit (with breakdown) | Why-now signal + source + date | Use case / channel motive | Event presence | Access (warm/known/cold) | Door (named person, if any) | Confidence | Notes
```

Then a short read, not a data dump:
- Top 8–10 by fit, one line each on why.
- **The 5 to approach now** — the intersection pick. For each: the use case, the door, and the opening line.
- The "no route yet" list, with what would open it.
- Gaps in the universe worth a second research pass.

## Guardrails
- **Transparent score or no score.** If the breakdown is not shown, it is not done.
- **Observable, dated signals only.** "They probably need this" is a motivation, not a field.
- **Confidence flags on the data.** Deep Research figures are often stale or second-hand; mark verified against a primary source vs unverified, and never let an unverified figure top the list.
- **Apply the standing 2–4× optimism correction** to signal strength and to assumed readiness.
- **Access is human.** Hints only; no invented relationships.
- **The score triages, it does not decide.** A high score is a reason to call, not evidence anyone will buy.
- **Stay lean.** A scored table, not infrastructure.

## Failure modes
- A blended rank that hides why an organisation is there.
- Scoring inferred enthusiasm instead of evidenced signals.
- An invented warm path that embarrasses the operator on the first call.
- Screening buyers only, and discovering in week 6 that the market buys through channels.
- Polishing the universe into a product when its only job is to source a handful of good conversations.
