# Hypothesis template

> [Segment] with [dated trigger] and [gap] will take a [20-minute call] about [smallest first yes], because [right to win].

The **smallest first yes** is the smallest paid or committed step a buyer can say yes to in one call, for example a 3-week target-market map at a fixed fee. "A meeting" isn't a first yes.

## Record with it
- **Test:** N sends between [start] and [end]. Five working days; skip holiday weeks.
- **Pass:** by [end + 14 days], at least R replies and at least C calls. By [end + ~30 days], at least 1 proposal requested.
- **Thresholds come from the actual mix of the final list**, not from wishes:
  - R = round(0.4 × W + 0.1 × K)
  - C = round(0.25 × W + 0.05 × K)
  - Here W and K are the numbers of WARM and KNOWN rows actually sent.
  - The rates are priors from run 1–2 planning. Replace them with observed rates after 3 sprints.
- **Revisions:** allowed only before the first send, with the reason logged. For example, rows added from "No dated signal" mean recompute with the same formula.

## If it fails
| Result | Diagnosis | Next move |
|---|---|---|
| No replies | The door or the opener is wrong | Check that the signal was theirs and fresh; move up to owner-level doors |
| Replies, no calls | The offer is too big or vague | Shrink the first yes; name the price |
| Calls, no proposal | Wrong target profile or timing | Revisit the segment or the why-now |
| Replies are mostly pointers | The doors sit below the owner (role 0) | Use the pointers as doors in the next batch |

## Sub-tests (optional, pre-registered)
One cheap question can decide the next sprint's direction. For example: "if ≥40% of calls name market X as their next market, the next sprint goes X-first". Write the threshold and the consequence before sending, and count it at the day-10 review.
