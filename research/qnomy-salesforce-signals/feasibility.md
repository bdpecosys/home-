# Feasibility: "Salesforce migration" signals for Qnomy

Version 2, 7 Oct 2026. The first pass was search-only. This pass had direct web access: curl, headless Chromium and the Legistar Web API.

## Hit rate

| Stage | Pass 1 (search only) | Pass 2 (web access) |
|---|---|---|
| Organisations examined | 15 | 18 (adds San José, Sunnyvale and Infinite Solutions' DMV work via Legistar and contract records) |
| Salesforce scope + named SI | 6 | 7 |
| + 2026-dated source + in segment | 3 | 4 (CA DMV, BCU, San José, Rush on the margin) |
| + booking/queue status **verified on the live site** | 0 | **2** (CA DMV = Qmatic; BCU = Salesforce Scheduler) |
| **High confidence** | 0 | **2**, plus 1 Medium-High (San José) |
| Migration in process | — | **2** (CA DMV DL phase, FY2026-27; San José CRM build, 2025–28) |

Strict yield is 2 high-confidence signals out of 18 examined (about 11%), or 3 counting San José. ANZ is still 0.

## What worked
1. **State budget and IT-oversight documents** (CA Department of Finance BCPs, CDT Special Project Reports). These were the best single source. They are dated and signed, and they name the phase, budget, SIs, procurement strategy and **the legacy systems to be replaced**. That is how CCFMAS/Qmatic was found inside the CA DMV Salesforce scope.
2. **Live page-source and rendered-page checks.** These settled the booking/queue question in seconds where they worked:
   - `qmatic.cloud` tenant at CA DMV;
   - Lightning Scheduler objects on BCU's booking page.

   A static curl is not enough for Salesforce Experience Cloud pages. A headless browser that logs network responses is needed.
3. **Legistar Web API** (`webapi.legistar.com/v1/{client}/matters`, filtered on "Salesforce" in the title). It surfaced council awards that name the SI, with the full staff memo attached: San José and Sunnyvale. Coverage is partial, because many clients don't expose the API.
4. **Following the SI.** Infinite Solutions appeared in both San José and CA DMV. Mapping an SI's public-sector clients is a cheap way to find adjacent signals, and it gives a single warm path to several prospects, as the Shopify-agency method did.
5. **Job posts.** One posting (San José CX Transformation Manager, Mar 2026) was enough to date an in-process build.

## What didn't work
- **The Internet Archive** refused connections from this environment (connection reset / 429), so no switch could be dated from snapshots. Retrying from another network, at a polite rate, should fix this.
- **qnomy.com** returns 403 to scripts, so the exclusion check relied on the ACF and Infina sites and search.
- **Some city sites are behind bot walls** (penfed.org returned a stub to curl). A rendered browser usually got through. When it didn't, I stopped rather than work around it.
- **Contract aggregators** (Starbridge, HigherGov) render client-side and cover only a sample. They are useful for leads but weak as evidence.
- **ANZ.** No equivalent of BCP/SPR documents or Legistar was found in the time available. AusTender lists licence contracts with Salesforce itself, not SI awards.

## Main failure modes
1. **Unnamed incumbents.** Cities often buy queue kiosks as small purchases that never reach council (San José). The site shows a kiosk but no vendor.
2. **SI not yet chosen.** The best "planning" signals (CA DMV's DL phase) don't yet have an SI. That's an opening, but it means naming the *previous* SI as the warm path.
3. **Signal age.** Salesforce stories and case studies are undated or lag go-live by 6–18 months. Budget documents and job posts are the reliable dated sources.
4. **Coverage.** The Legistar API only covers clients that expose it. Other councils use BoardDocs, CivicClerk or Granicus video archives, which need separate handling.

## Repeatability (monthly, per territory)
**US: yes.** This version of the method is repeatable and partly automatable:
1. **Monthly Legistar API sweep** (about 100 large cities and counties) for "Salesforce", "CRM", "311", "queue" and "appointment" in matter titles. Pull the staff memos and extract the SI, scope and timeline.
2. **State budget/IT trackers**: CA (BCP and CDT project tracking), TX DIR, NY ITS, WA OCIO, and similar. Search for "Salesforce" and "customer flow" / "appointment" / "queue" in new documents. Budget cycles concentrate these in Jan–Feb and May–June.
3. **SI follow-the-thread**: for each SI found, search its other public-sector and credit-union clients.
4. **Live-site classification** with a headless browser and a regex for qmatic, jrni, engageware, timetrade, qminder, qless, wavetec, qflow, `lightningscheduler`/`ServiceAppointment`, calendly and bookings.
5. **Event check** against the PSN, GovTech, AAMVA and league speaker pages.

Expected yield is 2–4 high-confidence US signals a month, with about 4–6 hours of analyst time once scripted. **ANZ: not yet.** It needs a source equivalent to Legistar and BCPs (state budget papers, council meeting minutes), which this pass didn't find.

## Verdict: is "we find what partners don't see" defensible?

**Yes, now with a concrete example, but phrase it as a method, not as volume.**

- **CA DMV is the proof.** The fact that Qmatic's customer-flow system (CCFMAS) is scheduled for replacement inside a Salesforce programme is in a 54-page state IT oversight report and a budget request, not in any press release. The DL phase that carries it is being re-procured in smaller modules in 2026-27, so the window is open now. Pair that with a live Qmatic signature and an event in the window where both DMV owners are speakers.
- **BCU shows the classification step works**: Salesforce Scheduler is confirmed from the live booking page, which leads straight to an AppExchange pitch.
- **San José shows the "in-process" pipeline works** (council memo plus job post), and the shared SI (Infinite Solutions) shows the warm-path angle.

**Caveat for the call:** Salesforce and SI press (BCU, Rush) *is* visible to ACF and Infina. The defensible claim is the **combination**: a dated government document, plus the live-site incumbent, plus the SI path, plus a verified event. Lead with CA DMV.

## Notes
- The "attached HTML" method reference wasn't in the repo, so the method follows the brief's description.
- Optional HTML summary: not produced yet. CA DMV is now strong enough to support a one-page version if wanted.
