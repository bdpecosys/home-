# Qnomy: customer-facing operations moving onto Salesforce (2026 signals)

**Version 2, 7 Oct 2026.** This version uses direct web access. Pages were fetched with curl or a headless Chromium browser, and vendor signatures were read from the live page source and network calls. Public data only, at a low request rate, and no one was contacted.

**Limits:** the Internet Archive refused connections from this environment (connection reset / HTTP 429), so no switch could be dated from snapshots. qnomy.com returned 403, so the exclusion check used ACF and Infina pages plus search.

| # | Organisation | Segment / lane | Stage | Implementing SI | Today's booking/queue | Class | Confidence |
|---|---|---|---|---|---|---|---|
| 1 | **California DMV** | State gov service centres / **ACF** | **In process.** Driver-licence phase starts in FY2026-27, and the replacement of Qmatic is in scope | Deloitte (OL and VR phases); Infinite Solutions (Salesforce/MuleSoft dev, 2025–27); DL SI not yet awarded | **Qmatic Cloud** (appointments and "Get in Line"), live 7 Oct 2026 | **Displacement (Qmatic)** | **High** |
| 2 | **BCU (Baxter Credit Union)** | Credit union, branches / **Infina** (ACF if enterprise) | Moved 2026. AI agent and member service on Salesforce, launched 2026 | NeuraFlash (part of Accenture) | **Salesforce Lightning Scheduler** on help.bcu.org, live 7 Oct 2026 | **Salesforce Scheduler (AppExchange play)** | **High** |
| 3 | **City of San José** | City service centres (311, permit center) / **ACF** or **Infina** | **In process.** Enterprise Salesforce CRM build, Oct 2025 – 2028 | Infinite Solutions, Inc. | Permit Center ticket kiosk (since June 2018) plus web appointment forms; **kiosk vendor not found** | Displacement (unnamed ~8-year-old incumbent); weaker | **Medium-High** |

---

## Signal 1 — California DMV: Salesforce programme set to replace the Qmatic queuing system

**Segment:** state government, about 170+ field offices, California. **Lane:** ACF Technologies, which already has US DMV references (South Carolina DMV uses Q-Flow via ACF).

**Salesforce scope and date**
- The Digital eXperience Platform (DXP) replaces DMV's legacy core systems on Salesforce, in phases:
  - Occupational licensing went live Oct 2022.
  - Disabled-person placards went live Aug 2023.
  - Vehicle registration, control cashiering and inventory are in development.
  - **The driver-licence/ID phase starts in FY2026-27.**
- The FY2026-27 budget request asks for **$94.1M and 109 positions** to "start the Driver Licensing (DL) phase." The total project cost is $414.7M. The request was signed 30 Dec 2025 and submitted to the Legislature **9 Jan 2026**.
- After the single bid at the second DL tender came in 56% over estimate, DMV is splitting DL into **small/medium modules**, explicitly to let **smaller companies** bid. The phase will be piloted in **field offices statewide**.
- **The key line:** DXP's scope covers "**Customer Flow Management functions** for the public." The Special Project Report lists **CCFMAS (Centralized Customer Flow Management and Appointment System)**, the Qmatic system, among the legacy systems to be replaced. Its objectives are:
  - 9.1: "coordinate and manage customer flow based on DMV staff availability";
  - 9.2: "automate customers flow based on service request complexity and staff expertise";
  - 9.3: cut manual staff-scheduling time.

**Implementing SI**
- **Deloitte Consulting LLP**: OL SI (2021–23, $7.8M) and VR SI (Aug 2022 award; $46.7M, raised to $58.1M). Named in the SPR's contract table.
- **Infinite Solutions, Inc. (Sacramento)**: Salesforce, MuleSoft and application-development services contract with DMV, 26 Jun 2025 – 26 Jun 2027 (up to $4.34M with options). Contract TC23-103 is extended to 28 Jun 2026. *Source is a contract aggregator and search index, not the state register, so treat as Medium.*
- **DL phase SI: not awarded** (the "DL Pilot vendor" is unnamed). This is the procurement to watch.

**Current booking/queue: Qmatic, verified live.** On 7 Oct 2026, dmv.ca.gov/portal/appointments/select-appointment-type/ carried `data-qmatic-url="https://mt-cadmvoas.us.qmatic.cloud/branches"`, and its "Get in Line Now" link goes to `https://mt-cadmvoas-secondary.us.qmatic.cloud/`. → **Displacement (Qmatic)**, with the replacement already written into the Salesforce programme.

**Evidence**

| Source | Date | What it proves |
|---|---|---|
| [CA DoF Budget Change Proposal FY2026-27, DXP (2740-016-BCP-2026-GB)](https://bcp.dof.ca.gov/2627/FY2627_ORG2740_BCP8680.pdf) | Signed 30 Dec 2025; to Legislature 9 Jan 2026 | DL phase starts 2026-27 ($94.1M); "Customer Flow Management functions" in DXP scope; modular procurement open to smaller firms; field-office pilots; Salesforce front end |
| [CDT Special Project Report, DXP v3.3 (project 2740-227)](https://projecttracking.technology.ca.gov/Home/Download?documentid=7b01f806-b5a9-4b35-b1aa-1a67348050cf&projectid=2740-227) | Submitted 29 Mar 2024 | CCFMAS listed for replacement; customer-flow objectives 9.1–9.3; Deloitte contracts and values |
| dmv.ca.gov appointment page (live source) | Observed 7 Oct 2026 | Qmatic Cloud tenant `mt-cadmvoas` powers appointments and "Get in Line" today |
| [Techwire: Qmatic $12.7M CCFMAS award](https://insider.govtech.com/california/www-techwire-net/state-awards-127m-contract-for-centralized-customer-management-system-at-dmv.html) | c. 2016–17 | Qmatic is the contracted CCFMAS vendor; queue-flow in field offices since 1999 |
| [Salesforce customer story: CA DMV](https://www.salesforce.com/customer-stories/california-department-of-motor-vehicles/) | Undated | DXP is built on Salesforce Public Sector / Experience Cloud / MuleSoft |
| Search-indexed contract summaries (Starbridge DMV contract catalog) | 2025–26 | Infinite Solutions' DMV Salesforce/MuleSoft contract and TC23-103 extension |

**Confidence: High.** Two dated primary state documents, plus a live-site signature on the same day as this report.

**Why it's an opening:** the largest DMV in the US has written the replacement of its Qmatic customer-flow system into a Salesforce programme. The phase that touches field offices (DL) is being re-procured in smaller modules in 2026-27, and DMV has said it wants smaller bidders. A Salesforce-native Q-Flow, delivered through ACF and teamed with the DXP integrator, fits that procurement exactly. ACF's South Carolina DMV reference is the proof point.

---

## Signal 2 — BCU (Baxter Credit Union): member service moved onto Salesforce, booking on Salesforce Scheduler

**Segment:** credit union, about $6.5B in assets, about 360–370k members, branches in IL, WI and Puerto Rico. **Lane:** Infina (credit unions). ACF if positioned as a multi-region enterprise rollout.

**Salesforce scope and date (2026)**
- **13 May 2026:** the Salesforce blog "How BCU Is Transforming Banking Service with Agentforce" names **NeuraFlash** as BCU's partner. BCU launched "Freeda," an Agentforce assistant on Financial Services Cloud data.
- Salesforce customer story: BCU uses Agentforce, Agentforce 360 for Financial Services, Service Cloud, Sales Cloud and Marketing Cloud. Its old bot "couldn't take action — like … scheduling an appointment." Its agent now "schedules time directly on the loan officer's calendar."
- **27 May 2026:** Glance/PR Newswire. BCU builds cobrowse into Salesforce and plans to extend it to its new member application experience.
- **15 Sept 2026:** Salesforce Koa announcement lists BCU in customer pilots.

**Implementing SI:** **NeuraFlash** (part of Accenture), named by Salesforce.

**Current booking/queue: Salesforce Scheduler, verified live.** On 7 Oct 2026, bcu.org's "Schedule an Appointment" button linked to `https://help.bcu.org/s/schedule`, an Experience Cloud site on `baxtercreditunion.my.site.com`. Rendering it loaded Salesforce Lightning Scheduler components and objects (`lightningscheduler`, `ServiceAppointment`, `WorkTypeGroup`, `ServiceTerritory`). Appointment reasons include accounts, home equity, loans (US and Puerto Rico), medallion, new membership, notary and home purchase.

A leftover allow-list entry for `nc1stage01.timetradesystems.com` in bcu.org's page code suggests an earlier **TimeTrade/Engageware** setup. The switch could not be dated (the Internet Archive was unreachable).

→ **Salesforce Scheduler.** No dedicated queue or lobby product was seen. Walk-ins and arrivals appear unmanaged by any digital tool.

**Evidence**

| Source | Date | What it proves |
|---|---|---|
| [Salesforce blog: How BCU Is Transforming Banking Service with Agentforce](https://www.salesforce.com/blog/how-bcu-is-transforming-banking-service-with-agentforce/) | 13 May 2026 | NeuraFlash is the partner; Agentforce launch on FSC data |
| [Salesforce customer story: BCU](https://www.salesforce.com/customer-stories/bcu/) | Undated (live Oct 2026) | Clouds in use; agent books loan-officer appointments |
| [PR Newswire / Glance: BCU and Salesforce](https://www.prnewswire.com/news-releases/bcu-achieves-faster-human-centered-digital-support-with-glance-and-salesforce-302782183.html) | 27 May 2026 | Independent vendor confirms member support being rebuilt in Salesforce, and expanding |
| [Salesforce: Announcing Koa](https://www.salesforce.com/news/press-releases/2026/09/15/koa-reasoning-model/) | 15 Sept 2026 | BCU in Koa customer pilots; the relationship is deepening |
| help.bcu.org/s/schedule (rendered live) | Observed 7 Oct 2026 | Branch booking runs on Salesforce Lightning Scheduler |
| bcu.org page source | Observed 7 Oct 2026 | Leftover TimeTrade host reference (earlier vendor, undated) |

**Confidence: High** for the Salesforce scope, the SI, 2026 timing and classification. The exact date of the move to Scheduler is unknown.

**Why it's an opening:** BCU has standardised member engagement on Salesforce and books appointments in Salesforce Scheduler, which does not run branch lobbies (walk-in queueing, arrival, routing to the next free banker). Q-Flow's AppExchange app slots in alongside Scheduler without asking BCU to leave Salesforce. NeuraFlash/Accenture is the integrator to pitch it with.

---

## Signal 3 — City of San José: enterprise customer service migrating to Salesforce (2025–2028)

**Segment:** city government. The SJ311 service centre, plus the Development Services Permit Center at City Hall (about 126k counter customers a year as of 2018). **Lane:** ACF (large city) or Infina (municipal mid-market).

**Salesforce scope and date**
- City Council, 30 Sept 2025 (file 25-1027): award to **Infinite Solutions, Inc.** to implement an **enterprise-wide Salesforce CRM**, up to $2,095,800 plus $526,950 contingency, from about 15 Oct 2025.
  - It "will replace the existing SJ311 platform" and consolidate "multiple fragmented customer service platforms."
  - Implementation runs **24–34 months**, so through about 2028.
  - Infinite Solutions beat Accenture and Guidehouse, with CA DMV, DWR and Caltrans as references.
  - Salesforce licences were bought through Carahsoft (file 25-683, Jun 2025).
- **16 Mar 2026:** the city opened a "Customer Experience (CX) Transformation Manager" post (job 202601485). The role is "business product owner for the City's CRM implementation," running stand-ups and coordinating "system design, development, testing, and implementation." The migration was in progress in 2026.

**Implementing SI:** **Infinite Solutions, Inc.** (the same Sacramento firm on CA DMV's Salesforce work).

**Current booking/queue:** the Permit Center uses a "highly programmed ticketing kiosk" plus online appointment scheduling, introduced June 2018. Current pages route appointments through web forms, sjpermits.org and a Freshdesk ticket portal. **The kiosk/queue vendor was not found** (no vendor signature on sanjoseca.gov; not named in council records or the 2018 announcement). → Displacement of an unnamed, roughly 8-year-old incumbent. Classification is **Medium/Low**.

**Evidence**

| Source | Date | What it proves |
|---|---|---|
| [San José Council memo, file 25-1027 (Legistar)](https://legistar.granicus.com/sanjose/attachments/ec940727-52ba-43b0-934f-b7b6bc547bee.pdf) | 8 Sept 2025; approved 30 Sept 2025 | SI = Infinite Solutions; scope; SJ311 replacement; 24–34-month timeline; bidders scored |
| [San José job posting 202601485: CX Transformation Manager](https://www.governmentjobs.com/careers/sanjoseca/jobs/newprint/5272722) | Opened 16 Mar 2026 | CRM implementation actively under way in 2026 |
| Legistar file 25-683 (Carahsoft, Salesforce licences) | Jun 2025 | Platform purchase |
| [The Registry: "San José Announces Faster Service at Permit Center through New Appointment and Ticketing System"](https://news.theregistrysf.com/san-jose-announces-faster-service-at-permit-center-through-new-appointment-and-ticketing-system/) | 11 Jun 2018 | Age of the current kiosk/appointment system |
| [sanjoseca.gov Permit Center pages](https://www.sanjoseca.gov/business/development-services-permit-center) | Observed 7 Oct 2026 | Ticket kiosk still in use; appointment routing |

**Confidence: Medium-High.** Scope, SI and the 2026 in-process status are High. The incumbent vendor is unknown.

**Why it's an opening:** San José is mid-build on a citywide Salesforce customer-service platform. Its walk-in counters still run on a 2018 kiosk that sits outside Salesforce. The same SI (Infinite Solutions) is also inside CA DMV's Salesforce programme, so one partner conversation covers two prospects.

---

## Exclusion check
None of the three appears on the ACF or Infina sites, nor in search of qnomy.com. qnomy.com itself returned 403. Known Qnomy customers surfaced along the way and were excluded: BECU, Texas Tech FCU, and South Carolina DMV (ACF).

## Watchlist (not upgraded)
- **Rush University System for Health**: Salesforce/Agentforce Health with **PwC**. It started in 2025, has no source dated 2026, and its booking runs on Epic MyChart. Medium-Low.
- **PenFed**: Salesforce in its branches, HCLTech as partner. The booking page wasn't checked in this pass (penfed.org returned a bot-wall stub).
- **Sunnyvale, CA**: Catalyst Consulting Group, Salesforce PSS CRM, approved 30 Sept 2025. Booking not checked.
- **Victoria DGS Salesforce Panel (ANZ)**: closes 19 Oct 2026. Re-check after award.
