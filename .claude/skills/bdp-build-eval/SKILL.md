---
name: bdp-build-eval
description: Decide whether BD Partners should build a given tool, automation, script, app, artifact, integration, dashboard, scraper, Claude skill, board or website feature — or buy off-the-shelf, make it a skill or template, defer it, or skip it entirely. Use this skill WHENEVER anyone proposes, considers or is offered a "build" for BD Partners, or asks "should we build X", "is it worth making Y", "do we need a tool for Z", talks about automating a workflow, wiring up an integration, standing up a CRM, tracker, scraper or dashboard, adopting a new SaaS platform, or spending time or money on any piece of software or infrastructure. Trigger even when the word "build" never appears — any time the real question is whether to invest effort into a technical artifact, evaluate it here first. Also use it to re-evaluate a previously deferred build when the trigger it was parked on has fired.
---

# BDP Build-Eval: Build / Buy / Skill-It / Defer / No-Build

A tachles go/no-go on any proposed build. Produces a 60-second verdict grounded in BD Partners' real constraints and live engagements — not a generic feasibility rubric. The bias is deliberately conservative: for a two-operator practice racing to revenue, the honest answer to most "let's build X" is not "build".

Read `bdp-model.md`, the live engagement file and `engine-method.md` before answering, so the pipeline anchor is current rather than remembered.

## Two gates before any analysis

**Gate 1 — Revenue proximity.** Does it generate revenue, or materially support a live or closing engagement, within roughly 1–2 months? If it cannot touch the current revenue window, the default is DEFER, however clever, cheap or fun it is. Most builds die here, and that is correct.

**Gate 2 — Engine asset.** Does it leave behind a reusable method asset — a skill, template, taxonomy or schema that makes the next client cheaper to serve? A build that passes Gate 1 but leaves nothing behind is a one-off cost; a build that passes both is the business model. A build that passes only Gate 2 is deferred until a live engagement needs it (build-on-demand, not on spec).

## Standing context — apply every time
- **No dedicated engineer.** Two operators: a commercial lead (BD, partnerships, origination) and a technical lead (core and banking systems, integrations, regulation). Both are the delivery capacity and the sales capacity. Build hours come straight out of selling and delivery hours — measure cost in **operator-hours diverted**, not calendar days.
- **Weak hardware on at least one machine.** A 4GB Windows 11 Home laptop: no local models, no heavy local data crunching, no Docker-heavy development. Anything needing local horsepower is disqualified or must move to a hosted substrate. Agentic desktop tooling that runs a local VM (~1.8GB RAM) is at the edge of what this machine supports; verify before depending on it.
- **Stack in hand.** Claude Team (two seats, shared projects, org-level skills, Claude Code, desktop agentic tooling), a private GitHub repo as the method library, Cloudflare (Pages and Workers — already the host, generous free tier), Google Workspace (Drive and Sheets as a light store, Gemini Deep Research, NotebookLM). No cloud credits in hand; a credits track is being pursued and must not be assumed. [VERIFY status before relying on it]
- **Money is tight.** A recurring cost that looks trivial to a funded startup is real here. Weigh every monthly charge against actual engagement revenue.
- **The product is the deliverable.** BDP sells fractional corpdev and market-entry engagements plus referral fees. The highest-leverage builds either upgrade the deliverables that are the product, or move a named live engagement.

**Preferred substrates, cheapest first** — push every build down this ladder before accepting it:
1. **A skill, prompt asset or template** in the shared workspace — hardware-independent, near-zero maintenance, upgrades the actual product. This is the default meaning of "build" here.
2. **A shared knowledge file or schema** — sometimes the whole answer is a documented convention.
3. **Off-the-shelf SaaS on a free or cheap tier**, ideally one that already connects to the workspace.
4. **A thin Cloudflare Worker or Pages function plus a Sheet or board as the store.**
5. **Bespoke, maintained code** — last resort. Someone must own it forever, and nobody is spare.

## Kill screen (any one TRUE ⇒ default NO-BUILD or DEFER)
1. No credible revenue or live-engagement impact within ~1–2 months.
2. Needs a dedicated engineer, or ongoing maintenance nobody can sustain.
3. A mature off-the-shelf tool covers ~80% at trivial cost and a low learning curve → **BUY**.
4. Needs local heavy compute, or assumes credits or infrastructure not actually in hand.
5. It is infrastructure for a business model not yet proven by paying clients (premature scaling).
6. It duplicates a layer already paid for — a second AI layer, a second tracker, a second source of truth.

## The five-point evaluation
Keep each to a few lines.

**1. Complexity.** v1 in operator-hours diverted; recurring cost; who owns it when it breaks; any skills gap.

**2. Impact.** Direct (bills a client, earns a fee, closes a deal) · Strong support (lifts close odds or delivery quality on a named live engagement) · Weak (generic capability) · None. Tie it to a named line and say when it lands.

**3. Off-the-shelf alternative.** Name the actual tool, real monthly cost, seat minimums, and the learning curve for a non-developer. Always include the skill-or-template option and the no-code option.

**4. Alignment.** Does it fit the model, the current priority order, the hard constraints (hardware, two operators, tight budget, existing stack), and the three-layer architecture in `engine-method.md`? Separate "moves a live engagement or upgrades the product" from "generic infrastructure".

**5. Final call.** BUILD (minimal) · BUY · SKILL-IT · DEFER (with the trigger that flips it) · NO-BUILD.

## Output template — always use this structure
```
VERDICT: <BUILD (minimal) | BUY | SKILL-IT | DEFER | NO-BUILD> — <one-line why>

What it is: <1–2 lines>

Scorecard:
| Dimension        | Rating                   | One-line note                          |
| Build complexity | Low/Med/High             | <operator-hours + recurring cost>      |
| Revenue impact   | Direct/Support/Weak/None | <named engagement + when>              |
| Engine asset     | Yes/No                   | <what reusable asset it leaves behind> |
| Off-the-shelf    | Yes(<tool, cost>)/No     | <effort for a non-developer>           |
| Pipeline fit     | Strong/Weak              | <moves a live deal? or generic infra?> |

Minimal version (if not NO-BUILD): <smallest thing that ships in days, on which substrate>
Off-the-shelf pick: <tool — cost — setup effort>   (or "none good")
Revisit trigger (if DEFER): <the event that flips this>
Pre-registered test: <how we will know in 2 weeks whether it worked>
Confidence: <Low/Med/High> — biggest risk to this call: <one line>
```

## Calibration and failure modes
- **Coolness ≠ revenue.** "We could build this in an afternoon" explains the cost, not the value.
- **Buying is winning** when a cheap tool plus thirty minutes does 80%.
- **Push builds down the substrate ladder** before accepting them.
- **Rate learning curves honestly** for a non-developer on weak hardware.
- **Apply the 2–4× optimism correction.** If a build looks like an obvious yes, check whether speculative future revenue is being booked as live pipeline.
- **Every DEFER gets a trigger**, so parked ideas resurface at the right moment.
- **Every adopted tool gets a pre-registered pass/fail test** with a date, and something that fails it gets dropped rather than tolerated.
- **When two builds compete for the same scarce hours, rank them.** The real choice is rarely "build or not", it is "this or the thing it displaces".
