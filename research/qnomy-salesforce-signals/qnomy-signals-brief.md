# Qnomy one-pager: signal-test brief

*Prepared 7 Oct 2026 for the thread drafting BD Partners' one-pager to Qnomy. All findings come from public sources and were checked on live sites the same day. No one was contacted.*

---

## 1. Why we ran this

The one-pager will claim that **BD Partners finds opportunities Qnomy's partners don't see, because press releases are visible to everyone.** Before promising that on a call, we tested whether we could back it with a real sample.

**What Qnomy told us (VP Global Sales):**
- The category is crowded, and many prospects already run a competitor.
- The best entry window is when a prospect replaces its CRM or ERP.
- Q-Flow has a Salesforce AppExchange app.
- Tenders are a main channel, with a sales cycle of about 6 months.

**Partners:**
- US: ACF Technologies (enterprise and state) and Infina (mid-market, credit unions and counties).
- ANZ: NEXA.

**Test definition:** an organisation in Qnomy's segments that in 2026 is moving, planning to move, or in the middle of moving its customer-facing operations onto Salesforce. The implementing partner (SI) must be named, with at least two independent public sources, one of them dated. For each, we classify what it uses today for booking and queueing:
- **whitespace** (nothing visible);
- **displacement** (a named competitor);
- **Salesforce Scheduler** (an AppExchange play for Q-Flow);
- **existing Qnomy customer** (excluded).

---

## 2. The logic: how we got here

The method mirrors the one used for an e-commerce client: find a platform change, name the implementer, verify the incumbent on the live site, and reach the buyer through the implementer and an event.

**Pass 1 (search engine only; direct page access was blocked).**
- Searched Salesforce customer stories, SI case studies, procurement aggregators and news.
- Result: 3 candidates with Salesforce and a named SI. **None** had a verified booking/queue vendor, and none was a clean 2026 move.
- Lesson: **marketing sources (Salesforce, SIs, press) give you the "who," but they are visible to everyone and are usually undated.** They can't show the incumbent, so they can't support the claim.

**Pass 2 (direct web access).** We switched to sources partners rarely read:
1. **Government budget and IT-oversight documents** (California budget change proposals, Department of Technology project reports). These are dated, signed and specific, and they list *which legacy systems will be replaced*.
2. **Council records via the Legistar API.** Staff memos name the SI, budget, scope and timeline at award.
3. **Live-site inspection with a headless browser.** We rendered each organisation's "book an appointment" page and read the vendor from its code and network calls (Qmatic, Engageware/TimeTrade, JRNI, Qminder, QLess, Wavetec, Salesforce Lightning Scheduler, and others).
4. **Job posts.** These date an implementation that is actually under way.
5. **Following the SI.** Once an implementer turns up, look for its other public-sector clients.
6. **Event speaker pages**, checked live for the Nov 2026 – Jun 2027 window.

**Hit rate:** 18 organisations examined, of which **2 are high confidence and 1 is medium-high**. Both high-confidence signals have their booking/queue system verified live. ANZ produced nothing usable (no equivalent public documents found).

---

## 3. Findings

### Signal 1: California DMV (state government, ACF's lane). Confidence: high. Migration in progress.

**What's happening:**
- DMV is rebuilding its core systems on **Salesforce** in phases (the Digital eXperience Platform, DXP).
- The FY2026-27 budget request asks for **$94.1M to start the driver-licence phase**, the phase that touches the field-office counters. It was signed 30 Dec 2025 and submitted to the Legislature 9 Jan 2026. Total project cost is $414.7M.

**The non-obvious part:**
- DXP's scope explicitly includes "**Customer Flow Management functions**."
- The state IT oversight report lists **CCFMAS (DMV's Qmatic queue and appointment system) among the legacy systems Salesforce will replace**. Its objectives include "coordinate and manage customer flow based on DMV staff availability."
- **The incumbent is live today:** DMV's appointment page and "Get in Line" both run on DMV's Qmatic Cloud instance (`mt-cadmvoas.us.qmatic.cloud`), checked 7 Oct 2026.

**The window:**
- The previous driver-licence tender drew a single bid at 56% over estimate and was not awarded.
- DMV is now splitting the work into **small/medium modules**, explicitly so that **smaller companies** can bid, and will pilot it in field offices statewide.

**Implementers:**
- **Deloitte**: system integrator on earlier phases ($58M vehicle-registration contract).
- **Infinite Solutions (Sacramento)**: Salesforce/MuleSoft development contract with DMV running to Jun 2027 (medium confidence; the source is a contract aggregator).
- No partner has been awarded the driver-licence phase yet.

**Classification:** displacement (Qmatic), with the replacement already written into the Salesforce programme.

**Proof point for the pitch:** ACF already delivers Q-Flow to **South Carolina DMV**.

**Sources:**
- CA Department of Finance BCP FY2026-27 (DXP): https://bcp.dof.ca.gov/2627/FY2627_ORG2740_BCP8680.pdf
- CA Department of Technology Special Project Report, DXP v3.3 (29 Mar 2024)
- Live page source of dmv.ca.gov/portal/appointments/
- Salesforce CA DMV customer story

### Signal 2: BCU (Baxter Credit Union; credit union, Infina's lane). Confidence: high. Moved in 2026.

**What's happening:**
- About $6.5B in assets, roughly 360–370k members, branches in IL, WI and Puerto Rico.
- BCU moved member service onto Salesforce in 2026, launching an AI assistant with **NeuraFlash (part of Accenture)**. Salesforce blog, **13 May 2026**: https://www.salesforce.com/blog/how-bcu-is-transforming-banking-service-with-agentforce/
- Corroborated by Glance (PR Newswire, **27 May 2026**) and Salesforce's Koa pilot list (**15 Sept 2026**).

**Booking:**
- BCU's "Schedule an Appointment" runs on **Salesforce Lightning Scheduler**, verified on the live page.
- Leftover code points to an earlier TimeTrade/Engageware setup (the switch could not be dated).

**Classification:** Salesforce Scheduler, the AppExchange play. Scheduler books appointments but doesn't run the branch lobby: walk-ins, arrival, routing to the next free banker. Q-Flow's Salesforce app fills that gap without asking BCU to leave Salesforce.

**Caveat:** BCU's Salesforce move is public on Salesforce's own blog. The non-obvious part is only the Scheduler gap.

### Signal 3: City of San José (city government, ACF or Infina). Confidence: medium-high. Migration in progress, 2025–2028.

**What's happening:**
- The council awarded **Infinite Solutions** a 24–34-month build of a **citywide Salesforce customer-service platform** replacing SJ311 (30 Sept 2025; up to $2.1M plus contingency). Infinite Solutions beat Accenture and Guidehouse.
- A city job post opened **16 Mar 2026** hires the product owner for the CRM implementation, which confirms the build is under way.

**Booking:** the Permit Center (about 126k counter customers a year) still uses a **ticket kiosk installed in 2018**. The vendor couldn't be identified.

**Why it matters beyond itself:** **the same SI, Infinite Solutions, is inside CA DMV's Salesforce work.** One partner conversation reaches two prospects, which is the same warm-path pattern as in our reference case.

### Exclusions and watchlist
- **Exclusion check:** none of the three appears on the ACF or Infina sites, nor in search of qnomy.com. Known Qnomy customers we hit and excluded: BECU, Texas Tech FCU and South Carolina DMV.
- **Watchlist** (not strong enough yet):
  - Rush University System for Health: Salesforce with PwC, but started in 2025.
  - PenFed: Salesforce with HCLTech; booking not checked.
  - Sunnyvale, CA: Catalyst Consulting.
  - Victoria's whole-of-government Salesforce panel (ANZ): closes 19 Oct 2026.

---

## 4. Events in the window (Nov 2026 – Jun 2027)

| Event | Date / place | Listed | Status |
|---|---|---|---|
| **Government Innovation California 2027** (Public Sector Network) | **2 Mar 2027**, Sacramento (the 2026 venue; the 2027 page doesn't show one) | **CA DMV:** Chief Digital Transformation Officer (Ajay Gupta) and **Deputy Director, Customer Services Division** (Sonia Huestis, field offices). **Salesforce:** Sr Director Solution Engineering | **Verified on the speaker page, 7 Oct 2026.** Sponsor packages are still open. |
| AAMVA Region IV Conference (motor-vehicle administrators) | 15–17 Jun 2027, Anaheim, CA | CA DMV's own region, hosted in-state | Date verified; speakers and exhibitors not yet published |
| America's Credit Unions GAC | 28 Feb – 4 Mar 2027, Washington DC | — | Not yet published (weak fit for BCU) |

There is no verified event for BCU or San José yet. For BCU, the realistic route is through NeuraFlash/Accenture's own financial-services events.

---

## 5. Implications for the one-pager

**1. The claim holds, but as a method, not as volume.**
- Don't promise "a stream of hidden opportunities."
- Do promise: *"We read what your partners don't — government budget and IT-oversight filings, council records and live-site code — to find the moment a buyer commits to replacing its customer-flow stack, which incumbent is there, which integrator holds the keys, and which room they'll be in."*

**2. Lead with CA DMV as the worked example.** Every element of the claim is in it:
- the CRM/platform-replacement window Qnomy's VP described;
- a named competitor (Qmatic) scheduled for replacement, found in a state oversight report rather than a press release;
- a procurement opening now, deliberately sized for smaller bidders;
- a named integrator path (Deloitte and Infinite Solutions);
- a partner proof point (ACF at South Carolina DMV);
- a verified event, 2 Mar 2027, where both DMV buyers are speaking.

**3. Use BCU to show the Salesforce/AppExchange angle.** Q-Flow's AppExchange app is a wedge whenever a Salesforce customer books on Scheduler, because Scheduler leaves the branch lobby and walk-ins unmanaged. That turns Qnomy's Salesforce app from a feature into a pipeline source.

**4. Use San José to show repeatability and the integrator lever.**
- Council records show in-flight migrations with the SI named, months before any case study.
- Following one regional SI (Infinite Solutions) surfaced two prospects.

**5. Offer it as a recurring service.** In the US it can run monthly:
- council-records sweep;
- state budget and IT trackers;
- following each SI to its other clients;
- live-site incumbent check;
- event check.

Expected yield: about 2–4 high-confidence US signals a month. **Be honest about ANZ:** public sources there are thinner, so NEXA's territory needs a different source mix, still to be tested.

**6. Mention partner fit by lane:**
- state and large-city government → ACF;
- credit unions and municipal mid-market → Infina.

The signals arrive pre-routed to the right partner.

## 6. Caveats to respect in the one-pager
- Don't state that DMV "will buy Q-Flow" or that Qmatic "is being removed" as a decision. The documents show replacement is *in scope* of the Salesforce programme. The vendor approach is not decided.
- Infinite Solutions' DMV contract comes from an aggregator listing, not the state register. Phrase it as "also works on DMV's Salesforce programme."
- BCU's TimeTrade history is inferred from leftover code and is undated.
- The two 2027 conferences are not yet confirmed as attended by Deloitte, Infinite Solutions or NeuraFlash.

## 7. Suggested proof-point line (draft)
> *"Example: California DMV's 2026-27 budget launches the driver-licence phase of its Salesforce programme, and the state's own IT oversight report lists its Qmatic queuing system among the systems to be replaced. The phase is being re-procured in smaller modules open to smaller bidders, and both of DMV's buyers for it are speaking in Sacramento on 2 March 2027. None of this was in a press release."*
