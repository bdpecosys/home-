# Warmth rubric

Warmth means **evidence of a real relationship**: a two-way conversation, a meeting, a saved phone number, shared work history, or a hand tag the founder set. A LinkedIn connection on its own is *known*, never *warm*. Presenting a connection as warm destroys the credibility of the whole list.

## Evidence points (additive; `scripts/build_roster.py` implements this)
| Signal | Points | Strong? |
|---|---|---|
| Two-way LinkedIn 1:1 thread, last message ≤24 months | 2 | yes |
| Two-way LinkedIn thread, older | 1 | yes |
| Saved Google contact with phone | 2 | yes |
| Saved contact without phone | 1 | no |
| Only in "Other contacts" (auto-collected) | 1 | no |
| Calendar meeting ≤24 months (≤8 attendees, not declined) | 2 | yes |
| Hand tag warm/hot | 2 | yes |

**Tier:** WARM = ≥3 including at least one strong signal · KNOWN = 1–2 · COLD = 0.
Breakdown is always shown: `5 = li_2way2 + other_contact1 + tag_warm2`.

Not evidence:
- one-way messages;
- group threads;
- webinars and large invites;
- endorsements;
- "we're connected".

## Door
A **door** is a WARM person, or a KNOWN person with a senior title (C-level, VP, head, director, GM, founder, partner, managing), at a company that fits the direction and isn't excluded. The door count is computed. The founder's feeling that "I know people there" doesn't count.

Door score in a list row: WARM = 2, KNOWN-senior = 1, junior or indirect = 0.

## Recency flags
- **Met in the last ~21 days:** it may be a live thread, which would mean the person is in motion. Ask the founder before listing them.
- **Last evidence older than 5 years:** still counts toward the tier, but the message needs a reintroduction line.

## Channel choice
| Evidence | Channel |
|---|---|
| Saved phone + meeting or recent thread | WhatsApp (Hebrew for Israelis) |
| Two-way LinkedIn thread | LinkedIn DM in the existing thread |
| Hand tag only, no thread on file | LinkedIn DM; flag "no thread on file" |
| KNOWN with old thread | LinkedIn DM, reintroduce in one clause |
| Email-only contact | Email from the business address |

## Calibration
Before anything downstream uses the tiers, show the founder about 10 WARM and 10 KNOWN rows with their breakdowns. Change a threshold only with a logged reason. Reference result (runs 1–2): about 21K people gave about 450 WARM (2%), about 10.4K KNOWN and about 10K COLD.
