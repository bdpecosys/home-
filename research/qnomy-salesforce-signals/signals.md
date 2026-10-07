# Qnomy — "customer-facing operations moving onto Salesforce" signals

Feasibility sample, compiled 7 Oct 2026. Public data only. No one was contacted.

**Research constraint (read first):** this run had **search-engine access only**. Direct page fetches were blocked by the environment's network policy. That covered qnomy.com, salesforce.com, govtech.com, legistar, dallascityhall.com and the Internet Archive, and the shell had no outbound web access at all. So:
- every fact below comes from search-result text (titles, snippets and the engine's page extracts), not from reading the full page;
- **no page-source vendor signatures and no Wayback snapshots were checked.** The booking/queue classification step of the method therefore could not be run as designed. Where a vendor is named, it comes from a published document, not the live site.

**Headline:** 3 signals meet the "Salesforce scope + named SI + two independent sources, one dated" bar. **None is a clean "new to Salesforce in 2026" migration.** All three are multi-phase programmes that started in 2020–2025 and are going live, expanding or entering a new phase in 2026. Treat them as "in the process of moving," which the brief allows, not as fresh replacements.

---

## Signal 1 — California Department of Motor Vehicles (CA DMV)

| Field | Detail |
|---|---|
| Segment / territory | State government service centres (approx. 170+ field offices), California, US |
| Qnomy partner lane | **ACF Technologies** (state government, national scale) |
| Salesforce scope | Digital eXperience Platform (DxP): legacy core systems are being replaced, phase by phase, on Salesforce (Customer 360 for Public Sector, Experience Cloud, Public Sector Solutions, MuleSoft). Phase 1 was occupational licensing. Phase 2 is vehicle registration, control cashiering and inventory (planned to go live around Nov 2025, with completion in FY2025-26). **Phase 3, driver licences, is still in planning:** the DL solicitation was cancelled because bids came in over budget, and about $295M is estimated to finish DL plus M&O. For FY2026-27, DMV requested $1.5M to continue implementation and knowledge transfer. |
| Date | Multi-year programme. The 2026 status is "VR phase landing, DL phase being re-planned and re-procured." That second step is the opening. |
| Implementing SI | **Deloitte Consulting**: SI for phase 1 and the $46M VR phase contract. |
| Current booking/queue | **Qmatic.** In the CCFMAS (Centralized Customer Flow Management and Appointment System) procurement, Qmatic Corp. won a $12.7M contract for a new queuing and appointment system. Qmatic's older queue-flow system had run since 1999 in most field offices. The award year is not shown in the search text (the procurement began in 2014; the award is likely around 2016–17). DMV also runs its own "Get in Line" virtual queue (sa.dmv.ca.gov). |
| Classification | **Displacement (Qmatic)**, confidence Med. The incumbent is documented, but its 2026 status was **not** re-confirmed on the live site. |
| Exclusion check | No evidence found that CA DMV is a Qnomy/ACF/Infina customer. The ACF and Qnomy customer pages could not be opened directly, so this check is incomplete. |
| Confidence | **Medium-High** that the Salesforce programme and SI are real. **Medium** on the 2026 timing. **Low-Medium** that Qmatic is still in place. |

**Evidence**
1. Salesforce customer story, "The CA Department of Motor Vehicles scales service, drives innovation." Proves that CA DMV is a Salesforce Public Sector customer and that DxP runs on Salesforce. https://www.salesforce.com/customer-stories/california-department-of-motor-vehicles/
2. Industry Insider California (GovTech), "Deloitte Wins $46M DMV Contract for Work on Vehicle Registration Project." The article date was not visible in the search text (SCPRS start date 30 Aug, year not shown), so this source is treated as undated. Proves that Deloitte is the SI, gives the value, and confirms all phases are on Salesforce. https://insider.govtech.com/california/news/deloitte-wins-dmv-46m-contract-for-work-on-vehicle-licensing-project (mirror: https://www.govreport.net/deloitte-secures-46m-california-dmv-modernization-contract/)
3. CA Dept. of Finance BCP FY2025-26 (ORG2740, BCP8281). **Dated** state budget document. Proves the VR/CC/IM go-live target (Nov 2025), the $295M still to finish DL, and that the DL solicitation was cancelled. https://bcp.dof.ca.gov/2526/FY2526_ORG2740_BCP8281.pdf
4. CA Dept. of Finance BCP FY2026-27 (ORG2740, BCP8680). **Dated**. Proves that DMV is still funding DxP implementation in 2026-27. https://bcp.dof.ca.gov/2627/FY2627_ORG2740_BCP8680.pdf
5. Techwire/Industry Insider, "State awards $12.7M contract for centralized customer management system at DMV." Proves Qmatic as the queue/appointment incumbent (CCFMAS). https://insider.govtech.com/california/www-techwire-net/state-awards-127m-contract-for-centralized-customer-management-system-at-dmv.html
6. Techwire, "State RFP opens foundational modernization phase." Proves the phased plan (OL → VR/CC → DL) and its scale (8,000 users, 50M transactions a year). https://www.techwire.net/news/state-rfp-opens-foundational-modernization-phase

**Why it's an opening:** the Qmatic CCFMAS contract is about 10 years old. Meanwhile the DL phase, which is the field-office counter transaction, is being re-scoped on Salesforce. This is the CRM-replacement moment Qnomy's VP described, in the single largest DMV in the US. Deloitte is the gatekeeper.

---

## Signal 2 — Rush University System for Health (Chicago)

| Field | Detail |
|---|---|
| Segment / territory | Academic health system: 3 hospitals plus outpatient clinics, Illinois, US |
| Qnomy partner lane | **ACF Technologies** (health systems) |
| Salesforce scope | Patient access and contact centre rebuilt on Salesforce: Health Cloud / Agentforce Health, Data Cloud (Data 360), Marketing Cloud, and MuleSoft integration with Epic. Agentforce on the Rush website handles clinic hours, finding the nearest clinic and prescription refills. Rush moved from IVR to intent-based telephony. PwC's case study says the scope runs "from booking appointments to refilling prescriptions." |
| Date | Launched 2025 (Rush was featured at Dreamforce 2025 and described as "the first healthcare provider to use agentic AI to support patients"). 2026 is scale-out: results published (15% fewer routine calls, 25% more digital self-service). **No source with a 2026 date confirms the timing**; the case-study pages carried no visible date. |
| Implementing SI | **PwC**. |
| Current booking/queue | Online scheduling runs on **Epic MyChart**. Rush was the first Connexient customer to combine MediNav indoor wayfinding with MyChart appointment scheduling. Contact centre: Genesys. **No queue-management/lobby vendor found** (Qmatic, JRNI, Qminder, QLess, Wavetec or Engageware not seen in any public source). |
| Classification | **Whitespace for in-clinic queue/flow**, not confirmed. The page source was not inspected. Booking is Epic-native rather than a Qnomy competitor. |
| Exclusion check | Not found among Qnomy/ACF customers. The check is incomplete for the same reason as above. |
| Confidence | **Medium-Low**. SI and scope High (Salesforce plus PwC, independently). "2026 move" Low: it started in 2025, and the only dated item is the Dreamforce 2025 feature. Classification Low. This signal meets the two-source rule only if the Dreamforce 2025 reference counts as the dated source. |

**Evidence**
1. Salesforce customer story, "Rush leads the way in agent-first patient support with Agentforce." Proves the scope (Agentforce on rush.edu, refills, clinic lookup) and that **PwC is the implementation partner**. https://www.salesforce.com/customer-stories/rush/
2. PwC case study, "AI agents improve patient care access, Rush University System for Health." An independent source (the SI's own). Proves PwC's role, the stack (Agentforce Health, Data 360), the IVR → intent-based telephony change, booking in scope, and published results. https://www.pwc.com/us/en/library/case-studies/rush-university-health-ai-patient-access.html
3. Salesforce blog, "Rush University System for Health Creates A New Standard for Patient Care." Proves Health Cloud, Data Cloud and Marketing Cloud plus MuleSoft–Epic integration. https://www.salesforce.com/blog/rush-salesforce-patient-care-ai/
4. PwC "Salesforce Dreamforce 2026" alliance page. **Dated (2026)**. It was returned for a Rush + PwC + Agentforce query, but I could not confirm Rush is named on it (the page could not be opened). Weak corroboration only. https://www.pwc.com/us/en/technology/alliances/salesforce/dreamforce.html
5. Connexient/MyChart sources (HIT Consultant; mychart.org "Emmie at Rush"). Prove that booking runs on Epic MyChart with MediNav wayfinding. https://hitconsultant.net/?p=45348
6. Genesys customer story. Proves the contact-centre platform. https://www.genesys.com/customer-stories/rush-university-system-for-health

**Why it's an opening:** Rush has digitised the front door (Salesforce/Epic). It has no visible arrival and lobby-flow layer for its outpatient clinics, the gap between "booked in MyChart" and "seen in clinic." PwC already owns the patient-access roadmap. Note: Epic-native check-in (Welcome kiosks) may already cover part of this. Verify before pitching.

---

## Signal 3 — BCU (Baxter Credit Union)

| Field | Detail |
|---|---|
| Segment / territory | Credit union, about $6.5B in assets, about 370k members, branches in Illinois, Wisconsin and elsewhere, US |
| Qnomy partner lane | **Infina** (credit unions); **ACF** if pitched as an enterprise multi-state deployment |
| Salesforce scope | Member service moved onto Agentforce Financial Services: "Freeda," an autonomous virtual assistant (82–84% of inquiries resolved without a human, 27% lower AHT). Glance co-browse built into Salesforce for agents, with plans to extend it to the new member application experience. The help centre runs on Salesforce Experience Cloud (help.bcu.org/s/…). BCU is in customer pilots of Salesforce's Koa reasoning model (Sept 2026). |
| Date | **2026**: Salesforce story and blog (Agentforce with NeuraFlash, around May 2026); Glance press release **27 May 2026**; Koa pilot announced **15 Sept 2026**. BCU used Salesforce before 2026, so this is an expansion into member-facing service, not a first-time move. |
| Implementing SI | **NeuraFlash** (part of Accenture). |
| Current booking/queue | bcu.org has a "Schedule Appointment" flow (phone or in-person, chosen through the location finder). **Vendor not found**: the page source could not be inspected, and no vendor case study names BCU. |
| Classification | **Not determined**. It could be whitespace, Salesforce Scheduler or a competitor. A two-minute check of the booking page source would settle it. |
| Exclusion check | Not found among Qnomy/Infina customers. Incomplete. Note: BECU and Texas Tech FCU *are* Qnomy customers (qnomy.com case studies), so the credit-union lane is well covered by Qnomy references. |
| Confidence | **Medium**. Salesforce scope plus SI plus 2026 date are High (three independent dated sources). Classification is missing. |

**Evidence**
1. Salesforce customer story, "BCU delivers human-centered service on demand with Agentforce," and the Salesforce blog "How BCU Is Transforming Banking Service with Agentforce." Prove the Agentforce member-service scope and **NeuraFlash as the partner**. https://www.salesforce.com/customer-stories/bcu/ · https://www.salesforce.com/blog/how-bcu-is-transforming-banking-service-with-agentforce/
2. PR Newswire / Glance, "BCU Achieves Faster, Human-Centered Digital Support with Glance and Salesforce." **Dated 27 May 2026**. An independent vendor source. Proves member-support workflows are being rebuilt in Salesforce in 2026 and expanding. https://www.prnewswire.com/news-releases/bcu-achieves-faster-human-centered-digital-support-with-glance-and-salesforce-302782183.html
3. Salesforce press release, "Announcing Koa." **Dated 15 Sept 2026**. Lists BCU in Koa customer pilots. https://www.salesforce.com/news/press-releases/2026/09/15/koa-reasoning-model/
4. help.bcu.org/s/topic/… (Salesforce Experience Cloud URL pattern). Proves the member help centre is on Salesforce. https://help.bcu.org/s/topic/0TOf2000000xCJXGA2/contacting-bcu
5. bcu.org contact/locations pages. Prove that in-person and phone appointment booking exists (vendor not visible). https://www.bcu.org/contact-and-help

**Why it's an opening:** BCU is rebuilding the member front door around Salesforce, and its integrator (NeuraFlash/Accenture) is the #1 Agentforce partner. Branch appointment and lobby flow is the obvious next piece. If BCU is on Salesforce Scheduler or a non-native tool, Q-Flow's AppExchange app is the entry point.

---

## Candidates checked but not verified (for the hit-rate count)

| Candidate | Why it failed the bar |
|---|---|
| PenFed (Pentagon FCU) | Salesforce/Agentforce is real (Jan 2026 story; Salesforce used in branches). The SI is HCLTech per a Jan 2025 HCLTech release. The booking vendor was not found. Close to verified; it needs a booking-page check. |
| City of Sunnyvale, CA | Catalyst Consulting Group is the SI for Salesforce PSS CRM ($801k implementation). Council action dates to 2025, the go-live date was not found, and its fit to service-centre queueing is unclear. |
| City of Austin, TX | $19.5M Salesforce amendment (10 Sept 2026) via Carahsoft, who is the reseller, not an SI. No SI named. |
| Texas Tech University | RFP to consolidate multi-org Salesforce into Education Cloud (due Jul 2026). No award or SI found. |
| Texas A&M Mays Business School | Education Cloud RFP (due 30 Sept 2026). Scope is grad recruitment/admissions, not student services. |
| US Dept. of Veterans Affairs | $1.6B Salesforce AELA (24 Jul 2026) including appointment scheduling. Salesforce is the direct contractor and no SI is named. Federal, outside the defined lanes, and too large to "sample." Worth a separate look for ACF. |
| SF Bay Conservation & Development Commission | Notice of intent to award to StackNexus (Apr 2026). Regulatory system, not in segment. |
| Victoria DGS Salesforce Panel (ANZ) | Whole-of-government panel to deliver Salesforce platforms (closes 19 Oct 2026). Planning signal, no agency or SI yet. Re-check after award. |
| NSW Dept. of Communities & Justice (ANZ) | ~A$85M Salesforce/MuleSoft/Tableau licences. No SI or date found in search. |
| West Virginia DMV, NC DMV | Modernisation projects, but not on Salesforce (NC = Kyndryl), or the platform is unknown. |
