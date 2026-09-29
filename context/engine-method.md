# The market-entry engine — method and conventions

*Last updated: 2026-09-22. Internal shared knowledge. This is the method BD Partners is building while delivering it; every engagement must leave it better.*

## The vision, in one line

An agent-based working tool for business development and international market entry — from research, through pipeline building, conference-centred meetings and follow-ups — built on a unified methodology, technology, AI and automation: efficient from day one and replicable for other clients.

## The rule that makes it real

**Every task produces two things: the client output, and a reusable method asset.** If a task leaves nothing behind, it was consulting, not engine-building. Assets are extracted from a run that worked — a prompt plus an output template first, a skill on the second use — never designed before the first run.

## The six stages (per engagement)

1. **Onboarding and product immersion** → positioning and use-case brief for the target market.
2. **Market and regulatory map** → prioritised map with named organisations and dated intent signals.
3. **Targets and first outreach** → scored universe (buyers and channels) plus live outreach.
4. **Meeting programme** → booked meetings with named decision-makers, confirmed and scheduled.
5. **Anchor event** → the delivered meeting programme, plus any speaking or exhibition presence.
6. **Conversion** → follow-ups, second sessions, handover into the client's technical and commercial process, and the plan for the next market.

Stages overlap deliberately: research does not precede market contact, it runs alongside it and deepens on live targets.

## Three layers — one home per artifact

* **Method layer —** Skills, templates, schemas, taxonomies, prompts, scripts. English. **No client data, ever.** This is the intellectual property that makes the next client cheaper to serve.
* **Client layer — a shared Drive folder per client.** Client materials, market maps, pipeline, meeting notes, deliverables. Any language.
* **Work layer — a project per client in the shared workspace**, with its instructions and the relevant knowledge files.

The repository is the source of truth; anything uploaded into a project is a mirror. Edit in the repository, then re-upload. No shadow copies: one home per artifact.

## Pipeline schema (the contract every output writes into)

One row per organisation:

`organisation · role (buyer/channel/competitor/influencer) · segment · country · fit score with breakdown · why-now signal · signal source URL · signal date · use case or channel motive · event presence · access (warm/known/cold) · door (named person) · owner · stage · next step · next-step date · confidence · source of record`

Agent outputs are produced as rows in this schema. If a field cannot be sourced, it is left blank and flagged — never filled with a guess.

## Signal taxonomy

Each signal type is defined by: what it is, where it is detected, how it is verified, and its weight. The current set is in `target-profile.md`. Signals are stored with source and date; the taxonomy is versioned in the repository and updated when a signal type proves or disproves itself in a live engagement.

## Quality rules for agent output

* Source URL and date on every factual claim.
* Verified against a primary source vs unverified is marked per row.
* Access and relationships are human-filled; the engine may surface hints only.
* Every output states what it could not find, not only what it found.

## Measuring replicability

Log **actual hours** per task. The claim that the engine is replicable is only credible if the second market or the second client demonstrably costs a fraction of the first. That log is also the evidence base for pricing the next engagement.

## Tooling in use

Shared workspace with projects and org-level skills; the GitHub method repository; Drive for the client layer; Deep Research for longlist building; a source-grounded notebook tool for regulatory and document-heavy research; a design tool for client-facing one-pagers. Anything beyond this is evaluated with the `bdp-build-eval` skill before adoption, with a pre-registered pass/fail test and a date.

