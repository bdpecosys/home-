---
name: bdp-call-prep
description: Prepare an evidence-based internal memo before a call or meeting with a prospect company (Israeli or foreign, public or private) for BD Partners. Use this skill whenever Amos mentions an upcoming call/meeting with a company or executive, uploads a financial report or annual report ahead of a meeting, asks to "analyze company X", "prep for my call with Y", "who is [person] at [company]", or asks for why-now signals, growth engines, or what to offer a specific prospect. Trigger even if he only names the company and contact without asking for a memo explicitly.
---

# BDP Call-Prep: Prospect Analysis & Memo

Produces a tachles internal memo before a prospect call, built from primary sources (filings, annual reports, news) plus BDP updated business context. 

## Inputs to collect (ask only for what's missing)
1. Company name + contact person (name, title, career background)
2. Relationship history (how they know each other, anything sent/done before — this often defines the natural offer)
3. Meeting date and how it came about (who initiated matters)
4. Any uploaded documents (financial report, deck); otherwise rely on web + filings

## Workflow

### Step 1 — Primary-source extraction
For Hebrew TASE filings and reports, read `references/hebrew_filings.md` for extraction recipes and keyword anchors. For any filing:
- Business structure, segments, controlling shareholders, key officers
- Financial trajectory: revenue, net profit, ROE/portfolio/backlog growth — find the **tension** (e.g., growth vs. profitability, targets vs. actuals)
- Strategy & targets section: published targets, **recent revisions and their dates** (a board cutting or changing a target in the last 6 months is usually the strongest why-now in the document)
- Risk factors and segment concentration

### Step 2 — Map the person (decisive step)
Search the filing for the contact by name:
- Exact role, subsidiary, committees (credit/investment/executive)
- Compensation structure — variable comp tied to what? Commissions for client acquisition? **Personal incentives predict what they'll say yes to.**
- Authority check: is the contact the approval body, near it, or an authority gap away? (BDP pattern: deals die at unowned approval steps.)
- Career background sets the register: never pitch process to someone who ran that process professionally (ex-bankers, ex-M&A heads). Talk deals, boxes, structures — not decks.
- Note without asserting: if their unit was just downsized/refocused, the person may have personal motives for the meeting. Let discovery reveal it.

### Step 3 — Fresh signals
Web search for news after the filing date. Verify the entity is who you think it is — same-name companies in wrong geographies are a known failure mode.

### Step 4 — Why-now signals (theirs, not ours)
List 3-6 signals grounded in evidence, each implying a need BDP can serve.

### Step 5 — Classify buyer and rank the plays
Match the company to BDP's product lanes — do not force the wrong product.

### Step 6 — Calibrate honestly
Distinguish: paying-client odds vs. partnership odds vs. network value ("who else should I talk to" is always worth something). Never inflate.

### Step 7 — Write the memo
Use the exact structure in `references/memo_template.md`. Style: tachles, dense, numbers first, no padding. Front-load a 60-second read. Include 4-6 discovery questions ordered from informed-open to commitment-close, 2-3 credibility facts max (dropping many reads as showing off), and one hygiene/conflict note if fees could flow from both sides. Save as `[Company]_call_memo_[date].md` and present the file with a short chat summary of the headline finding — especially anything that reframes the call away from the assumed pitch.

