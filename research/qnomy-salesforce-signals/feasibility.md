# Feasibility: "Salesforce migration" signals for Qnomy

## Hit rate

| Stage | Count |
|---|---|
| Distinct candidate organisations examined | 15 (CA DMV, Rush, BCU, PenFed, Sunnyvale, Austin, Texas Tech, TAMU Mays, VA, SF BCDC, Victoria DGS, NSW DCJ, WV DMV, NC DMV, Sacramento County 311) |
| Passed "Salesforce scope + named SI" | 6 (CA DMV, Rush, BCU, PenFed, Sunnyvale, SF BCDC) |
| Also in segment, with two sources (one dated) | 3 (CA DMV, Rush, BCU) |
| **Of those, booking/queue status classified with evidence** | **1 (CA DMV, Qmatic; currency unconfirmed)**. Rush is partially classified (Epic MyChart booking, no queue vendor seen). BCU is unclassified. |
| Clean "first move onto Salesforce in 2026" | **0**. All three are 2020–2025 programmes expanding or entering a new phase in 2026. |
| ANZ | 0 verified (2 planning-stage leads without an SI) |

Verified yield is about 20% of candidates (3/15). Fully complete (classified) yield is about 7% (1/15). Run time was roughly 2.5 hours, search-only.

## What worked
- **SI and vendor case studies** (PwC, Glance, Salesforce customer stories). These are the fastest way to get "org + SI + scope" in one hit, and the SI's own page is a genuinely independent second source.
- **State budget documents** (CA Dept. of Finance BCPs). Dated, specific, and they name the phase, the budget and the problems (cancelled DL solicitation). This is the best "planning or in process" evidence type, and partners rarely read them.
- **Old procurement news on the incumbent** (Qmatic CCFMAS). Pairing the "new CRM" signal with the "old queue contract" signal is where the actual insight comes from.
- **Third-party vendor press releases** (Glance + BCU). They date the move and corroborate it without relying on Salesforce marketing.

## What didn't work
- **Generic searches** ("credit union selects Salesforce 2026", "health system goes live Health Cloud"). They return partner listicles and SEO content, not named organisations.
- **Procurement aggregators** (HigherGov, govly, starbridge, govdash). Good for **RFPs**, which name the org but not the SI, because there's no award yet. Awards that name SIs are scattered across council minutes (Legistar), which were blocked here.
- **ANZ.** AusTender, Buy NSW and Buying for Victoria surface licence contracts with Salesforce itself, not SI awards. Search engines index the content poorly.
- **Booking-vendor classification by search.** Search engines don't expose page source, and vendors rarely publish named customer logos in this category. **This step needs page-source or Wayback access**, which this environment blocked. With that access it's a few minutes per org: view the source of the "book an appointment" page and grep for qmatic, jrni, engageware or timetrade.
- **Event verification for 2027.** Most exhibitor and speaker lists for Nov 2026 – Jun 2027 are not published yet. Only 1 of 6 events could show the prospect as listed.

## Main failure modes
1. **The "2026 move" definition is too narrow for this market.** Public-sector, health and credit-union Salesforce programmes are multi-year and phased. Hardly anyone does a press-released switch in a single year the way Shopify replatforms do. The workable signal is "**a new phase or new customer-facing scope starting**," not "migrated."
2. **The SI is usually invisible until the award**, and awards sit in council minutes, state contract registers and case studies published 6–18 months after go-live. So the signal is either early (RFP, no SI) or late (case study, the decision has already been made).
3. **The classification step needs live-site access.** Without it, two of three signals can't say whether they are whitespace, displacement or a Salesforce Scheduler play, and that is the part that makes the pitch specific.
4. **Salesforce marketing inflates the "new."** Customer stories don't date themselves and are often re-skins of older projects.
5. **Exclusion checks need the Qnomy, ACF and Infina customer pages**, which were blocked. Exclusion was only checked by search (it surfaced BECU and Texas Tech FCU as Qnomy customers).

## Repeatability (monthly, per territory?)
- **US: yes, as a semi-automated monthly sweep, if you have web access.** Feeds that would work:
  - (a) state budget and IT project-tracking portals for DMV and agency CRM phases (CA, TX, NY ITS, etc.);
  - (b) Legistar and BoardDocs searches for "Salesforce" plus "agreement," which give city and county awards with the SI named;
  - (c) new Salesforce customer stories filtered by industry;
  - (d) case-study pages of about 15 SIs (Deloitte, Accenture/NeuraFlash, PwC, Slalom, Huron, Coastal Cloud, Cloud for Good, Catalyst, HCLTech…);
  - (e) a page-source check on each hit.

  Realistic yield: 2–4 qualified signals per month in the US, mostly "phase or expansion" signals.
- **ANZ: weak.** It needs direct tender-portal scraping (within terms of service) and LinkedIn/job-post corroboration. Expect perhaps 0–1 a month.
- **Effort:** about 3–4 hours per territory per month once the source list is set up. Classification and event checks are the manual part.

## Verdict: is "we find what partners don't see" defensible?

**Partly, and not with this sample as it stands.**

- **Defensible:** the *combination* is the edge. In CA DMV, a Salesforce programme whose next phase (driver licences) is being re-procured sits on top of a roughly 10-year-old Qmatic queue contract. That link is only visible by reading a state budget document alongside an old procurement article. Neither is a press release. ACF probably knows CA DMV exists, but probably doesn't know the timing or that Deloitte is the door.
- **Not defensible yet:**
  - (1) None of the three is a clean "2026 replacement."
  - (2) Two of three lack an evidenced booking/queue status, which is the piece that makes a signal actionable for Qnomy.
  - (3) BCU and Rush come from Salesforce/SI marketing, which *is* visible to everyone, including ACF and Infina.
  - (4) No event is verified for BCU or Rush.

**Recommendation for the call:** don't promise "opportunities your partners don't see" as a volume claim. Promise a **method with one worked example**: CA DMV (Salesforce DL phase + Qmatic incumbent + Deloitte as SI + an event where the DMV is a listed speaker). Before the call:
- re-run the classification step for BCU, PenFed and Rush with live-site access (about 30 minutes);
- confirm Qmatic is still in place at CA DMV.

If two of the three come back as displacement or whitespace with evidence, the claim stands up at "2–3 a month."

## Notes
- The "attached HTML" method reference was not present in the repo, so this report follows the method as described in the brief.
- The optional one-page HTML summary was skipped. With only one fully classified signal, a polished summary would overstate the result.
