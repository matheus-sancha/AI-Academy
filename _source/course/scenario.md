# Scenario: Technik Production Assistant

> This is the single running scenario for every worked example, exercise and lab in both tracks.
>
> Technik is a **fictional company**. All projects, clients, fields, people, part/drawing/program numbers and data values are invented, and any resemblance to real companies or projects is coincidental. Don't add real client names, field names, drawings, procedures or data exports.

## The company

Technik designs and manufactures **subsea production equipment** for offshore oil and gas projects:

- **Subsea trees (XTs):** valve assemblies installed on a subsea wellhead to control flow from the well.
- **Manifolds:** seabed structures that gather flow from several XTs and route it to a flowline.

Every unit is **engineered to order** for a client project. Parts are made through a sequence of manufacturing operations:

**Machining → Cladding → Welding → Bending → Coating → Assembly & Testing**

Factory Acceptance Testing (FAT) is part of **Assembly & Testing**. Not every part goes through every operation.

## Systems

Technik runs engineering in Teamcenter and manufacturing in SAP. Both are replicated nightly into **Snowflake**, which is where the agent reads them. Standards and supporting documents live in SharePoint.

| System | Owns | Snowflake tables |
|---|---|---|
| **Teamcenter** (TcE) | Parts and revisions, drawings, controlled documents, CNC programs, Engineering Change Notifications (ECNs) | `TC_*` |
| **SAP** (ERP) | Projects, serialised units, BOMs, work orders and operations (routing and actual hours), Quality Notifications (QNs) | `SAP_*` |
| **SharePoint** | Standards and supporting documents that engineers consult alongside Teamcenter documents | Knowledge source (not in Snowflake) |

## Identifiers

Every Teamcenter number is **11 characters**: the code, then `7` padded with zeros, then a 5-digit sequence.

| Thing | Format | Example | Source |
|---|---|---|---|
| Part number | `P70000XXXXX` | `P7000001042` | Teamcenter / SAP |
| Drawing | `DU7000XXXXX` | `DU700001042` | Teamcenter |
| CNC program | `T70000XXXXX` | `T7000000217` | Teamcenter |
| Document | `<code>700XXXXX` | `SWI70000318` | Teamcenter |
| ECN | `ECN700XXXXX` | `ECN70000042` | Teamcenter |
| Work order | SAP number | `100004521` | SAP |
| Quality Notification (QN) | SAP number | `300001234` | SAP |
| Project | `PRJ-####` | `PRJ-2031` | SAP |
| Serial number | `<XT\|MF>-<model>-####` | `XT-V2-1042` | SAP |
| Solution checkpoint | `TechnikAssistant_<module>_end.zip` | `TechnikAssistant_B7_end.zip` | labs |

### Controlled document types

| Code | Meaning |
|---|---|
| SWI | Standard Work Instruction |
| LWI | Local Work Instruction |
| GWI | Global Work Instruction |
| SOP | Standard Operating Procedure |
| DCP | Data Collection Point |
| TDS | Technical Datasheet |
| MFG | Manufacturing Document |
| LST | Document List |
| DGL | Design Guidelines |
| DRM | Design Review Meeting |

## The problem

Planners, manufacturing engineers, quality engineers and supervisors spend hours answering the same questions by searching SAP, Teamcenter, SharePoint, spreadsheets and email:

- "What's the status of work order `100004521`? Which operation is it at?"
- "What's the efficiency of welding work orders at Plant 1 this month?"
- "What's the average lead time for `P7000001042` work orders?"
- "What's the latest released revision of drawing `DU700001042`, and which ECN changed it?"
- "Which CNC program revision should machining use for `P7000001042`?"
- "Show open QNs on cladding for project `PRJ-2031`."
- "Which document covers weld prep inspection, and what does it say about acceptance criteria?"
- "Draft a new revision of `SWI70000318` that includes the change from `ECN70000042`."

## The agent

The **Technik Production Assistant** is an internal agent in Microsoft Teams. It covers seven capability areas:

| Capability | Example | Data |
|---|---|---|
| Work order information | Status, current operation, blocked reason | `SAP_WORK_ORDERS`, `SAP_WO_OPERATIONS` |
| Work order efficiency | Routing hours ÷ actual hours by operation, work centre, period | `SAP_WO_OPERATIONS` |
| Work order lead time | Release → completion, by part, operation or plant | `SAP_WORK_ORDERS` |
| Quality Notifications | Find, summarise and draft QNs | `SAP_QUALITY_NOTIFICATIONS` |
| Engineering questions | Answer engineers' everyday questions about procedures, documents and standards, with citations | Teamcenter documents + SharePoint |
| Teamcenter revision information | Latest released revision of parts, drawings, documents and CNC programs; ECN history | `TC_*` |
| Document revision & creation | Draft a new document or revision in Technik's template, then route it for approval | Documents + `TC_DOCUMENTS` |

> **Definitions:** *Efficiency %* = routing hours ÷ actual hours × 100. *Lead time* = calendar days from work order release to technical completion.

The agent grows module by module. Every lab ships a checkpoint, so no module depends on the learner having finished the previous one.

### Beginner track: built in Copilot Studio

| Module | What learners do with the scenario |
|---|---|
| B1 LLM Fundamentals | Exercise: count tokens in an SWI, compare outputs at different temperatures, catch a hallucinated part number |
| B2 Prompt Engineering | Exercise: turn a vague "summarise this QN" prompt into a structured, XML-tagged one |
| B4 Agent Fundamentals | Exercise: map the assistant's seven capabilities onto knowledge, tools, topics and flows |
| B5 Copilot Studio Basics | Lab: create the assistant with instructions and a *Work order status* topic |
| B6 Knowledge & RAG | Lab: ground it in SOPs and work instructions (documents) plus Snowflake work-order data |
| B7 Tools, Connectors & MCP | Lab: query Teamcenter revision data in Snowflake through a connector tool; add an existing MCP server |
| B8 Skills | Lab: add a *QN write-up* skill that drafts QNs in Technik's format |
| B9 Workflows & AI Builder | Lab: document revision approval flow; extract fields from supplier material certificates |
| B10 SQL in Snowflake | Lab: work order efficiency and lead-time queries; a clean view for the agent |
| B11 Safety & Responsible AI | Lab: moderation settings; test prompt injection hidden in a QN description |
| B12 Environments & Publishing | Lab: move the assistant into a solution and publish it to Teams |
| B13 Testing & Evaluation | Lab: build and run an evaluation set across the seven capabilities |

### Advanced track: the same company, deeper engineering

| Module | What learners do with the scenario |
|---|---|
| A2 Context Engineering | Redesign the assistant's context budget: instructions, tool results, long SAP result sets |
| A4 Agent Skills | Author a *document revision* skill package: template, change-summary script, ECN cross-check |
| A5 MCP | Build an MCP server over Teamcenter revision data and QNs; connect it to VS Code and Copilot Studio |
| A6 Multi-Agent | Split into a production agent (SAP) and an engineering agent (Teamcenter, documents, standards) with handoff |
| A7 Pro-Code Agents | Rebuild the assistant in Microsoft Agent Framework |
| A8 Advanced RAG | Chunk and index controlled documents; Cortex Search vs. Azure AI Search; route between SQL and documents |
| A9 Snowflake & Cortex | FAT bench data as JSON (`VARIANT`); classify QNs and find similar past QNs with Cortex AI SQL; secure views for the agent role |
| A10 Intelligent Automation | Material certificate processing pipeline with validation and human review |
| A11 Models | Decide whether QN classification needs fine-tuning; prepare training data |
| A12 Evaluation | Eval harness with regression gates for the Agent Framework build |
| A13 Security | Threat-model the assistant; data exfiltration through tools; DLP design |
| A14 ALM & Operations | Pipelines, Git integration and CI/CD with evaluation gates |

## People (personas)

| Persona | Role | Typical question |
|---|---|---|
| Ana | Production planner, Plant 1 | "Which work orders are late to start Coating this week?" |
| Bruno | Quality engineer | "Show open QNs on Welding older than 30 days." |
| Carla | Manufacturing engineer | "Draft revision C of `SWI70000318` for `ECN70000042`." |
| Diego | Machining supervisor, Plant 2 | "What was machining efficiency last month, by work centre?" |

## Data model (Snowflake)

One schema per learner (`SANDBOX_<user>`), seeded and reset by `labs/_setup/snowflake/`. The data is small, deterministic and fully synthetic: 251 rows across 13 tables, two plants, four projects and about three months of manufacturing history.

| Table | Rows | Key columns | Used in |
|---|--:|---|---|
| `SAP_PROJECTS` | 4 | `PROJECT_ID`, `PROJECT_NAME`, `CLIENT_NAME` (invented), `FIELD_NAME` (invented), `FAT_DUE_DATE`, `STATUS` | B10 joins |
| `SAP_UNITS` | 10 | `SERIAL_NO`, `PRODUCT_TYPE` (XT / MANIFOLD), `MODEL`, `PROJECT_ID`, `PLANT`, `STATUS` | B5, B10 |
| `SAP_BOM_LINES` | 13 | `PARENT_PART_NO`, `COMPONENT_PART_NO`, `QTY` | B10 joins |
| `SAP_WORK_ORDERS` | 27 | `WO_NO`, `PART_NO`, `SERIAL_NO`, `PROJECT_ID`, `PLANT`, `RELEASED_AT`, `COMPLETED_AT`, `STATUS` | B5–B7, lead time |
| `SAP_WO_OPERATIONS` | 85 | `WO_NO`, `OP_SEQ`, `OPERATION`, `WORK_CENTER`, `ROUTING_HOURS`, `ACTUAL_HOURS`, `PLANNED_START`, `ACTUAL_START`, `ACTUAL_END`, `STATUS`, `DRAWING_NO`, `DRAWING_REV`, `CNC_PROGRAM_NO`, `CNC_PROGRAM_REV`, `WORK_INSTRUCTION_NO`, `CONFIRMATION_NO`, `CONFIRMED_AT` | Efficiency, B10 windows |
| `SAP_QUALITY_NOTIFICATIONS` | 18 | `QN_NO`, `WO_NO`, `SERIAL_NO`, `PART_NO`, `OPERATION`, `DEFECT_TYPE`, `DESCRIPTION`, `PRIORITY`, `STATUS`, `CREATED_AT`, `CLOSED_AT` | B8, B11, A5, A9 |
| `TC_PARTS` | 22 | `PART_NO`, `REVISION`, `DESCRIPTION`, `RELEASE_STATUS`, `RELEASED_AT` | B7 revision tool |
| `TC_DRAWINGS` | 19 | `DRAWING_NO`, `REVISION`, `PART_NO`, `TITLE`, `RELEASE_STATUS`, `RELEASED_AT` | B7, A5 |
| `TC_DOCUMENTS` | 17 | `DOC_NO`, `DOC_TYPE`, `REVISION`, `TITLE`, `OWNER`, `STATUS` (In Work / In Review / Released / Obsolete), `RELEASED_AT`, `NEXT_REVIEW_DATE` | B9 revision flow, A4 |
| `TC_CNC_PROGRAMS` | 8 | `PROGRAM_NO`, `REVISION`, `PART_NO`, `MACHINE`, `RELEASE_STATUS`, `RELEASED_AT` | B7, A5 |
| `TC_ECNS` | 6 | `ECN_NO`, `TITLE`, `REASON`, `STATUS`, `CREATED_AT`, `RELEASED_AT` | Revision history |
| `TC_ECN_AFFECTED_ITEMS` | 12 | `ECN_NO`, `ITEM_NO`, `ITEM_TYPE` (Part / Drawing / Document / CNC Program), `FROM_REV`, `TO_REV` | Revision history |
| `FAT_RESULTS` | 10 | `SERIAL_NO`, `TEST_ID`, `TEST_NAME`, `RESULT`, `TESTED_AT`, `RAW` (`VARIANT`: bench readings as JSON) | A4, A9 |

Conventions the data follows:

- **Work order status** uses the SAP codes `CRTD`, `REL`, `PCNF`, `CNF` and `TECO`; operation status uses `OPEN`, `INPROC` and `CNF`. Everything else — project, unit, notification, revision status — is spelled out in words. Turning the codes into something a user can read is one of the jobs of the view built in B10.
- **`SAP_WO_OPERATIONS` has one row per confirmation**, not per operation. An operation should have exactly one; where it has two, the higher `CONFIRMATION_NO` is the posting that counts.
- **A work order is "blocked" when its current operation is `INPROC` and an open notification names that work order.** There is no blocked flag; the agent works it out by joining.
- **Dates are relative.** Every date is stored as a fixed number of days from the first day of the month the sandbox was reset, so "this month" and "older than 30 days" always mean something. Gaps between dates never change.

Deliberate "teaching defects" in the data:
- **Operations confirmed twice** — a partial posting that was never reversed, then the full re-posting. Hours and operation counts are double-counted, and welding at Plant 1 reads about **111% efficiency** until the stale postings are dropped with `QUALIFY`, at which point it is about **89%** (B10, A9).
- **Work orders on superseded revisions**: work orders `100004510` and `100004513` reference a drawing or CNC program revision that a released ECN has replaced. Found by joining SAP with Teamcenter.
- **Documents past their review date**: `SOP70000114`, `SWI70000318` and `TDS70000044`, for document-revision prompts.
- **Near-duplicate QNs** `300001211` and `300001219`, raised for the same overlay porosity, for similarity search (A9).
- **QN descriptions containing injected instructions**, `300001267` and `300001270`, for the prompt-injection lab (B11, A13).

`ECN70000042` is released and still waiting for revision C of `SWI70000318`. That is not a defect — it is the change Carla drafts in B9 and A4.

The scripts that create all of this, the two-role model and the reset procedure are in [`labs/_setup/snowflake/`](../../labs/_setup/snowflake/README.md). `python _build/check_seed.py` validates the data without needing a Snowflake account.

## Documents (knowledge sources)

All documents are invented, short, and marked *Fictional — for training only*.

| Document | Type | Used in |
|---|---|---|
| `SOP70000101` Quality Notification Handling | SOP | B6, B8, A8 |
| `SOP70000114` Engineering Change Notification Process | SOP | B6, A4 |
| `SWI70000318` Cladding Preparation and Inspection | SWI | B6, B9 revision flow, A4 |
| `SWI70000402` Hydrostatic Test During Assembly & Testing | SWI | B6 citations, A8 |
| `GWI70000027` Controlled Document Authoring Template | GWI | B8, A4 document creation |
| `DGL70000009` Cladding Design Guidelines | DGL (Teamcenter) | Engineering questions, A8 |
| Technik internal standards (e.g. weld overlay acceptance criteria) | SharePoint | B6 SharePoint knowledge, engineering questions |
| Supplier material certificates (10 samples) | PDF | B9, A10 document extraction |
| Plant safety and PPE rules | Web page (SharePoint) | B6 website/SharePoint knowledge |

> Industry standards may be **referenced by title and number** only. Never copy their text into the repo; they're copyrighted.
