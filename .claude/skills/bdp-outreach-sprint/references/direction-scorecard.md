# Direction scorecard (7 lines, 0–2 each, total /14)

Score up to 5 directions. Always include the incumbent thesis, the one already being worked, so the new directions have to beat it with numbers.

| Line | 2 | 1 | 0 |
|---|---|---|---|
| **1. Right to win** | Named track record with this buyer type (past deals, employer, domain) | Adjacent credibility | None the buyer would recognise |
| **2. Doors (computed)** | ≥15 doors incl. ≥5 WARM | ≥5 doors | <5 doors |
| **3. First yes before the decision date** | A priced first yes plausible within ~30 days | Within the quarter | Needs a long cycle or procurement |
| **4. Deal size vs the reference deal** | ≥ reference deal | 30–99% of it | <30% of it, or unpriced |
| **5. Dated why-now** | Several dated triggers in the segment in the last 6 months | Some, older or generic | None found |
| **6. Fit with active client work** | Reuses or strengthens the active engagement, no conflict | Neutral | Competes with or distracts from a client |
| **7. Founder pull** | The founder wants it (ask, don't assume) | Indifferent | Reluctant |

## Doors line (pre-registered, set before counting)
Run `scripts/count_doors.py`, which removes in-motion and held accounts first. Then:
1. Read the "top matched companies" line for each direction and fix false positives in the regex. Examples:
   - substring hits;
   - stale email domains;
   - cyber firms caught by "security";
   - "& co".
2. Rerun and report W and K per direction.

A direction with 0 doors can still score high elsewhere. It becomes a research track, not the sprint.

**Gate:** can you name 15 doors this week? If not, the direction isn't the sprint.

**Yield:** gates and signal search cut doors hard (runs 1–2: 102 doors → 13 draft rows → 8 sendable after the full in-motion scan). Before choosing, say how many rows the door count realistically yields.

## Sensitivity table
For each direction, show:
- the total as scored;
- the total with doors ±30%, re-bucketed;
- the total with the most uncertain judgment line moved ±1.

If the ranking flips inside plausible error, say so. The tie-break then decides it, not a gut call.

## Tie-break (pre-registered)
Within 1 point, the direction with more **WARM** doors wins, because warm doors convert several times better than known ones.

## Combining directions
Two directions can be run together when:
- their company sets don't overlap (check that the regexes are disjoint);
- one message skeleton fits both buyers.

Report the combined pool as one W/K count.
