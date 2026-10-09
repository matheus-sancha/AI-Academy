# Reference scenario: Technik

> The single reference behind every worked example in all three levels. It is a set of **shapes** —
> systems, identifiers, documents and data — not a story. No example depends on an earlier module.
>
> Technik is a **fictional company**. All projects, clients, fields, part/drawing/program numbers and
> data values are invented, and any resemblance to real companies or projects is coincidental. Don't
> add real client names, field names, drawings, procedures or data exports.

## What Technik makes

Technik is a fictional manufacturer of engineered-to-order equipment. Two product types appear in the
data:

- **Subsea tree (`XT`)** — a valve assembly that controls flow from a well.
- **Manifold (`MANIFOLD`)** — a structure that gathers flow from several trees.

Parts are made through a sequence of manufacturing operations, and operation names appear throughout
the data:

**Machining → Cladding → Welding → Bending → Coating → Assembly & Testing**

Factory Acceptance Testing (FAT) is part of **Assembly & Testing**. Not every part goes through every
operation.

## Systems

Technik runs engineering in Teamcenter and manufacturing in SAP. Both are replicated nightly into
**Snowflake**, which is where the agent reads them. Standards and supporting documents live in
SharePoint.

| System | Owns | Snowflake tables |
|---|---|---|
| **Teamcenter** (TcE) | Parts and revisions, drawings, controlled documents, CNC programs, Engineering Change Notifications (ECNs) | `TC_*` |
| **SAP** (ERP) | Projects, serialised units, BOMs, work orders and operations (routing and actual hours), Quality Notifications (QNs) | `SAP_*` |
| **SharePoint** | Standards and supporting documents that engineers consult alongside Teamcenter documents, and PDF copies of released Teamcenter documents | Knowledge source (not in Snowflake) |

## Identifiers

Every Teamcenter number is **11 characters**: the code, then `7` padded with zeros, then a 5-digit
sequence.

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

## The agent

The **Technik Production Assistant** is an internal agent in Microsoft Teams, and the target of both
guided builds. It is built on Copilot Studio's **GitHub Copilot harness**, because the guided build
packages a capability as a skill, so it has no topics. It covers seven capability areas:

| Capability | Example question | Data |
|---|---|---|
| Work order information | *What's the status of work order `100004521`? Which operation is it at?* | `SAP_WORK_ORDERS`, `SAP_WO_OPERATIONS` |
| Work order efficiency | *What's the efficiency of welding work orders at Plant 1 this month?* | `SAP_WO_OPERATIONS` |
| Work order lead time | *What's the average lead time for `P7000001042` work orders?* | `SAP_WORK_ORDERS` |
| Quality Notifications | *Show open QNs on cladding for project `PRJ-2031`.* | `SAP_QUALITY_NOTIFICATIONS` |
| Engineering questions | *Which document covers weld prep inspection, and what does it say about acceptance criteria?* | Teamcenter documents + SharePoint |
| Teamcenter revision information | *What's the latest released revision of drawing `DU700001042`, and which ECN changed it?* | `TC_*` |
| Document revision & creation | *Draft a new revision of `SWI70000318` that includes the change from `ECN70000042`.* | Documents + `TC_DOCUMENTS` |

> **Definitions:** *Efficiency %* = routing hours ÷ actual hours × 100. *Lead time* = calendar days
> from work order release to technical completion.

Capability areas are not tasks: a brief rewrites each one as tasks with a trigger and a finished state.
What the Intermediate examples give the assistant:

| Part | What it is |
|---|---|
| Users | Four groups, all internal, each asking as an individual in Teams: **production planners** (fluent in SAP codes), **quality engineers** (own QNs and their disposition), **manufacturing engineers** (drawings, programs, revisions), **supervisors** (need every code spelled out). Shared through one security group per user group |
| Knowledge | Two SharePoint sources: the **Controlled Documents** library, where released Teamcenter documents are published as PDFs, and the Technik **Standards** site |
| Tools | `Get work order status`, `Find quality notifications`, `Get released revision`, `Get operation efficiency`, `Get work order lead time` — each a fixed query over Snowflake |
| Skills | `qn-write-up`, which drafts a QN write-up in Technik's format; `agent-skills` adds `wo-delay-note`, a five-line delay note on one work order |
| Will not | Disposition a nonconformance (the assigned quality engineer decides); write anything to SAP or Teamcenter. Its description in Teams tells users both |
| Escalates to | The document's owner, from `TC_DOCUMENTS.OWNER` |

One more agent appears: a small **FAT checklist helper** that tells a test lead which tests a unit still
needs before its project's `FAT_DUE_DATE`. It exists to be the reader's *other* agent, built carelessly
(`publishing-and-environments`, `next-steps`). Standard-harness designs such as a *Work order status*
topic are illustrations of what Technik would build on that harness, not parts of either agent.

## Which part of this each level uses

The same reference, at two depths.

| Level | Draws on |
|---|---|
| **Basic** | The **documents only** — work instructions, SOPs, quality notification text, supplier certificates, the plant safety page |
| **Intermediate**, **Advanced** | The documents **and** the Snowflake data model |

Basic teaches *using* Copilot in Chat and the Office apps. Its examples are documents a reader opens,
summarises, drafts from or asks about. **A Basic lesson never reaches for a table**: the data model
below is for the two levels that build against it.

## Worked examples by module

Each module draws its examples from one slice of the assistant. Every example stands on its own, so a
lesson found through search makes sense by itself. Lists are indicative where a module's topics are
not yet written. Basic's rows describe what was written.

### Basic — documents only

| Module | Worked examples |
|---|---|
| `how-copilot-works` | A summary of a QN that was never attached; a long chat about `SWI70000318` losing an earlier turn; auditing an answer about section 5.2 claim by claim (a misread limit, an invented appendix, an unsupported "current revision") |
| `prompting` | One summary prompt for QN `300001234`, improved lesson by lesson, then tested on `300001211`, `300001219` and `300001267` |
| `how-copilot-sees-your-work` | Revision C of `SWI70000318` in a site production can't open; `SWI70000402` not found; the *Confidential* customer specification for `PRJ-2031`; a chat summary that ranks people |
| `copilot-chat` | Finding which document covers weld prep inspection, and checking the citation; what happened on `PRJ-2031` this week |
| `copilot-in-word` | Asking `SWI70000318` for a quote rather than a summary; drafting a note from the file; filling `GWI70000027` for a new LWI; reviewing revision C with tracked changes |
| `copilot-in-excel` | A table of the ten supplier material certificates: asking, filling, a formula against the 485 MPa minimum, and a messy supplier spreadsheet |
| `copilot-in-powerpoint` | An old QN training deck that disagrees with `SOP70000101`; a six-slide supervisor briefing built from the SOP, put on the corporate template and edited down |
| `copilot-in-outlook` | The document controller's thread about the three documents past their review date: summary, drafted reminders, Prioritize, and what the summary missed |
| `copilot-in-teams` | The channel thread on `ECN70000042` and revision C; a rewritten status post; a design review recap with a misheard document number |
| `using-agents-others-built` | Asking the Production Assistant about work order `100004521` and auditing the cited half and the looked-up half; asking it outside its job |
| `finishing-basic` | A week of the habits: the QN prompt, the Chat question about weld prep inspection, the certificate table, the overdue-documents reminder, an agent answering outside its job |

### Intermediate — built in Copilot Studio

| Module | Worked examples |
|---|---|
| `getting-oriented` | Where the Production Assistant sits in the Microsoft AI stack |
| `how-models-behave` | Counting tokens in an SWI; the same summary at different temperatures |
| `agent-fundamentals` | Mapping the assistant's seven capabilities onto knowledge, tools, topics and flows |
| `copilot-studio-basics` | Reading the activity trace for a revision question; a *Work order status* topic, as a standard-harness design the assistant does not have |
| `writing-instructions` | The assistant's instructions; an XML-tagged QN summary prompt |
| `knowledge-and-rag` | Grounding in SOPs and work instructions plus Snowflake work-order data |
| `tools-connectors-mcp` | A connector tool over Teamcenter revision data in Snowflake; adding an existing MCP server |
| `agent-skills` | A *QN write-up* skill that drafts QNs in Technik's format |
| `safety-and-moderation` | Moderation settings; prompt injection hidden in a QN description |
| `designing-an-agent` | The thirteen slots, filled in for the Production Assistant |
| `testing-and-evaluation` | An evaluation set across the seven capabilities |
| `publishing-and-environments` | Moving the assistant into a solution and publishing it to Teams |
| `the-six-skills` | What each skill in the toolchain produces for this agent |
| `guided-build` | What you must have ready before the route starts |
| `snowflake-sql` *(reference)* | Work order efficiency and lead-time queries; a clean view for the agent |
| `automation-and-workflows` *(reference)* | A document revision approval flow; extracting fields from supplier material certificates |
| `next-steps` | The checkpoint, sat on the FAT checklist helper rather than the assistant |

### Advanced — the same company, pro-code

| Module | Worked examples |
|---|---|
| `developer-tooling` | The repo layout for the Production Assistant rebuild |
| `agent-harness` | Watching the agent loop run against a Teamcenter lookup |
| `context-engineering` | Redesigning the context budget: instructions, tool results, long SAP result sets |
| `authoring-skills` | A *document revision* skill package: template, change-summary script, ECN cross-check |
| `building-mcp-servers` | An MCP server over Teamcenter revision data and QNs, connected to VS Code and Copilot Studio |
| `advanced-tools-and-multi-agent` | Splitting into a production agent (SAP) and an engineering agent (Teamcenter, documents, standards) with handoff |
| `pro-code-agents` | Rebuilding the assistant in Microsoft Agent Framework |
| `evaluation-and-observability` | An eval harness with regression gates for the Agent Framework build |
| `security-advanced` | Threat-modelling the assistant; data exfiltration through tools; DLP design |
| `alm-and-governance` | Pipelines, Git integration and CI/CD with evaluation gates |
| `capstone-build` | Scaffold → MCP server over Teamcenter data → agent → evals → ship |
| `llm-internals` *(reference)* | — |
| `advanced-rag` *(reference)* | Chunking and indexing controlled documents; Cortex Search vs. Azure AI Search; routing between SQL and documents |
| `snowflake-cortex` *(reference)* | FAT bench data as JSON (`VARIANT`); classifying QNs and finding similar past QNs with Cortex AI SQL; secure views for the agent role |
| `automation-advanced` *(reference)* | A material certificate processing pipeline with validation and human review |
| `models-and-fine-tuning` *(reference)* | Deciding whether QN classification needs fine-tuning; preparing training data |

## Data model (Snowflake)

Technik's replicated data lives in `TECHNIK_DW.OPS`. It exists only on paper: lessons quote rows from
it, and the course provides no database to run against. It is small — two plants, four projects and
about three months of manufacturing history.

| Table | Key columns | Used in |
|---|---|---|
| `SAP_PROJECTS` | `PROJECT_ID`, `PROJECT_NAME`, `CLIENT_NAME` (invented), `FIELD_NAME` (invented), `FAT_DUE_DATE`, `STATUS` | `snowflake-sql`, `next-steps` |
| `SAP_UNITS` | `SERIAL_NO`, `PRODUCT_TYPE` (XT / MANIFOLD), `MODEL`, `PROJECT_ID`, `PLANT`, `STATUS` | Not yet used |
| `SAP_BOM_LINES` | `PARENT_PART_NO`, `COMPONENT_PART_NO`, `QTY` | Not yet used |
| `SAP_WORK_ORDERS` | `WO_NO`, `PART_NO`, `SERIAL_NO`, `PROJECT_ID`, `PLANT`, `RELEASED_AT`, `COMPLETED_AT`, `STATUS` | Work order status, lead time, `knowledge-and-rag`, `snowflake-sql` |
| `SAP_WO_OPERATIONS` | `WO_NO`, `OP_SEQ`, `OPERATION`, `WORK_CENTER`, `ROUTING_HOURS`, `ACTUAL_HOURS`, `PLANNED_START`, `ACTUAL_START`, `ACTUAL_END`, `STATUS`, `DRAWING_NO`, `DRAWING_REV`, `CNC_PROGRAM_NO`, `CNC_PROGRAM_REV`, `WORK_INSTRUCTION_NO`, `CONFIRMATION_NO`, `CONFIRMED_AT` | Efficiency, superseded revisions, `snowflake-sql` |
| `SAP_QUALITY_NOTIFICATIONS` | `QN_NO`, `WO_NO`, `SERIAL_NO`, `PART_NO`, `OPERATION`, `DEFECT_TYPE`, `DESCRIPTION`, `PRIORITY`, `STATUS`, `CREATED_AT`, `CLOSED_AT` | `agent-skills`, `safety-and-moderation`, `automation-and-workflows`, `building-mcp-servers`, `snowflake-cortex` |
| `TC_PARTS` | `PART_NO`, `REVISION`, `DESCRIPTION`, `RELEASE_STATUS`, `RELEASED_AT` | `tools-connectors-mcp` revision view |
| `TC_DRAWINGS` | `DRAWING_NO`, `REVISION`, `PART_NO`, `TITLE`, `RELEASE_STATUS`, `RELEASED_AT` | `tools-connectors-mcp`, `building-mcp-servers` |
| `TC_DOCUMENTS` | `DOC_NO`, `DOC_TYPE`, `REVISION`, `TITLE`, `OWNER`, `STATUS` (In Work / In Review / Released / Obsolete), `RELEASED_AT`, `NEXT_REVIEW_DATE` | `automation-and-workflows` revision flow, the escalation owner, `authoring-skills` |
| `TC_CNC_PROGRAMS` | `PROGRAM_NO`, `REVISION`, `PART_NO`, `MACHINE`, `RELEASE_STATUS`, `RELEASED_AT` | `tools-connectors-mcp`, `building-mcp-servers` |
| `TC_ECNS` | `ECN_NO`, `TITLE`, `REASON`, `STATUS`, `CREATED_AT`, `RELEASED_AT` | Revision history, superseded revisions |
| `TC_ECN_AFFECTED_ITEMS` | `ECN_NO`, `ITEM_NO`, `ITEM_TYPE` (Part / Drawing / Document / CNC Program), `FROM_REV`, `TO_REV` | Revision history, superseded revisions |
| `FAT_RESULTS` | `SERIAL_NO`, `TEST_ID`, `TEST_NAME`, `RESULT`, `TESTED_AT`, `RAW` (`VARIANT`: bench readings as JSON) | `authoring-skills`, `snowflake-cortex` |

Conventions the data follows:

- **Work order status** uses the SAP codes `CRTD`, `REL`, `PCNF`, `CNF` and `TECO`; operation status
  uses `OPEN`, `INPROC` and `CNF`. Everything else — project, unit, notification, revision status — is
  spelled out in words (a QN's status is `'Open'`, a revision's `'Released'`), and so are plants
  (`'Plant 1'`, `'Plant 2'`). Turning the codes into something a user can read is one of the jobs of
  the view in `snowflake-sql`.
- **`SAP_WO_OPERATIONS` has one row per confirmation**, not per operation. An operation should have
  exactly one; where it has two, the higher `CONFIRMATION_NO` is the posting that counts.
- **A work order is "blocked" when its current operation is `INPROC` and an open notification names
  that work order.** There is no blocked flag; the agent works it out by joining.
- **Dates in examples are illustrative.** Where an example depends on elapsed time ("older than 30
  days"), it says what it assumes.

Deliberate flaws in the data, which lessons use as examples:

- **Operations confirmed twice** — a partial posting that was never reversed, then the full
  re-posting. Hours and operation counts are double-counted, and welding at Plant 1 in September reads
  **110.9% efficiency** (26 rows for 20 operations) until the stale postings are dropped with
  `QUALIFY`, at which point it is **88.9%** (`snowflake-sql`, `snowflake-cortex`).
- **Work orders on superseded revisions**: at Machining, work order `100004510` still references
  drawing `DU700001042` revision B and `100004513` CNC program `T7000000217` revision A, after
  `ECN70000051` released drawing C, program B and part `P7000001042` C. Found by joining SAP with
  Teamcenter (`snowflake-sql`, `building-mcp-servers`). Revision D of `DU700001042` is In Work, which
  is what an agent that picks the highest letter gets wrong (`copilot-studio-basics`,
  `testing-and-evaluation`).
- **Documents past their review date**: `SOP70000114`, `SWI70000318` and `TDS70000044`, for
  document-revision prompts (`copilot-in-outlook`, `automation-and-workflows`).
- **Near-duplicate QNs** `300001211` and `300001219`, raised for the same overlay porosity, for
  similarity search (`snowflake-cortex`).
- **QN descriptions containing injected instructions**, `300001267` and `300001270`, for the
  prompt-injection examples (`safety-and-moderation`, `security-advanced`).

Two states that are not defects, and that many examples lean on:

- **`100004521` is blocked.** It is released (`REL`), its current operation is `0020` Cladding,
  `INPROC`, and open QN `300001234` (porosity in the overlay) names it. Asked for its status, a correct
  answer says so.
- **`ECN70000042` is released and still waiting for revision C of `SWI70000318`.** Revision B is the
  released one. Revision C adds an ultrasonic check before cladding (section 4) and tightens the
  porosity limit (section 5). It is the change drafted in `automation-and-workflows` and
  `authoring-skills`.

**Agent identity.** Technik's agents and MCP servers read Snowflake as `TECHNIK_AGENT_RO`, a read-only
role, on warehouse `TECHNIK_AGENT_WH`. The Production Assistant connects through a service principal as
the service user `TECHNIK_AGENT_SVC`, which holds that one role and nothing else. The role reads a view
wherever a rule lives: `V_WORK_ORDER_OPERATIONS` (one row per operation, duplicates removed) and
`V_RELEASED_REVISIONS` (the latest released revision of each part, drawing and program, with its ECN). The
only tables it reads directly are `SAP_QUALITY_NOTIFICATIONS` and `TC_DOCUMENTS`.
People query with their own roles; agents never borrow them.

## Documents (knowledge sources)

All documents are invented, short, and marked *Fictional — for training only*. This is the layer
**Basic** draws on in full. A controlled document is written in Word: drafts circulate as Word files,
and the released revision is published as a PDF to the Controlled Documents library, which everyone
can read. A Word copy someone saved shows only the revision letter printed in it.

| Document | Type | Used in |
|---|---|---|
| `SOP70000101` Quality Notification Handling. Sections *Purpose, Scope, Definitions, Raising a QN, Recording the defect, Priority, Disposition, Closure, References*. A QN is raised no later than the end of the shift, at one of three priority levels. The disposition belongs to **the quality engineer assigned to the QN** | SOP | `copilot-in-powerpoint`, `knowledge-and-rag`, `agent-skills`, `advanced-rag` |
| `SOP70000114` Engineering Change Notification Process. Past its review date | SOP | `copilot-in-outlook`, `knowledge-and-rag`, `authoring-skills` |
| `SWI70000318` Cladding Preparation and Inspection. Section 4, preparation; section 5, inspection: finished overlay on XT valve body bores not less than 3.0 mm at every measurement point. Section 5.2, visual and dye-penetrant inspection of clad surfaces: indications up to 0.8 mm on sealing surfaces, 1.5 mm on non-sealing surfaces, in two tables. No appendix B. Revision B released, and past its review date; revision C is in draft (see below) | SWI | `how-copilot-works`, `how-copilot-sees-your-work`, `copilot-chat`, `copilot-in-word`, `copilot-in-outlook`, `copilot-in-teams`, `using-agents-others-built`, `knowledge-and-rag`, `automation-and-workflows`, `authoring-skills`, and most Intermediate modules |
| `SWI70000402` Hydrostatic Test During Assembly & Testing. Gives the test's hold time | SWI | `how-copilot-sees-your-work`, `copilot-chat`, `knowledge-and-rag` citations, `advanced-rag` |
| `GWI70000027` Controlled Document Authoring Template. Headings *Purpose, Scope, References, Safety, Procedure, Records, Revision history* | GWI | `copilot-in-word`, `agent-skills`, `authoring-skills` |
| `TDS70000044`, a technical datasheet for a coating Technik no longer buys. Past its review date, and cited in the cladding supplier's purchase specification | TDS | `copilot-in-outlook`, `automation-and-workflows` |
| `DGL70000009` Cladding Design Guidelines. Section 3 explains the 3.0 mm: 0.5 mm dilution + 1.0 mm machining + 1.5 mm service. It explains, it does not set the requirement | DGL (Teamcenter) | Engineering questions, `knowledge-and-rag`, `advanced-rag` |
| *Weld Overlay Acceptance Criteria*, on the Technik Standards site: a summary table, which says the work instruction governs where the two differ | SharePoint | `how-copilot-sees-your-work`, `copilot-chat`, `using-agents-others-built`, `knowledge-and-rag`, `testing-and-evaluation` |
| Supplier material certificates (10 samples), one per heat of bar for XT valve bodies, numbered like `MC-0413`. Each gives supplier, certificate number, heat number, grade (such as `TK-A`), yield and tensile strength, elongation and hardness (HBW). One supplier reports strength in ksi. Technik's purchase specification for the bar sets a minimum yield strength of **485 MPa** | PDF | `copilot-in-excel`, `automation-and-workflows`, `automation-advanced` |
| The customer specification for `PRJ-2031`, labelled *Confidential* | Customer document | `how-copilot-sees-your-work` |
| Plant safety and PPE rules | Web page (SharePoint) | `copilot-chat`, `knowledge-and-rag` |
| Quality notification text, as a user pastes it or the assistant returns it (see below) | QN | `prompting`, `using-agents-others-built`, `safety-and-moderation`, `snowflake-cortex` |

### What Basic's examples share

Basic's lessons each stand alone, but several of them share these details. Keep a new example
consistent with them.

**QN `300001234`.** A dye-penetrant check after cladding found porosity in the bore overlay of
`XT-V2-1042` (`P7000001042`, `PRJ-2031`), on work order `100004521` at operation `0020` Cladding. The
area is marked and the unit held. The disposition is pending with the quality engineer. No cause and
no release date are recorded. `300001211` and `300001219` are its near-duplicates, the same porosity
raised twice. `300001267`'s description carries an injected instruction, quoted word for word from
`safety-and-moderation`.

**Revision C of `SWI70000318`.** The manufacturing engineering team drafts it in Word, in their own
SharePoint site and Teams channel. Production staff can't open either. It adds an ultrasonic (UT)
check before cladding (section 4) and tightens the porosity limit (section 5). The channel thread on
`ECN70000042` and revision C runs six weeks and about sixty replies, and agreed the new limit about
five weeks in. The draft circulates for review with tracked changes, and goes through a design review.
Its release waits on a qualified UT inspector, which the cladding supervisor is qualifying for. XT bores
already in the queue stay on revision B. Lessons catch revision C at different points short of
release, from early draft to ready for release. None has it released. **There is no `SWI70000381`.** A
lesson uses that number as a mishearing of `318`, so it must not become a real document.

**The documents past their review date.** Technik's document controller runs a reply-all thread of
twenty-three messages about `SOP70000114`, `SWI70000318` and `TDS70000044`. In message 4, purchasing
says the datasheet is cited in the cladding supplier's purchase specification. In message 6, everyone
agrees to re-review all three. Message 14 asks whether `SOP70000114` needs a full review or only a
date change, and nobody answers. In messages 21–22, the datasheet's owner proposes withdrawing it, and
someone agrees.

**Roles.** Basic names roles, never people: production and shift supervisors, the quality engineer
assigned to a QN, the quality lead, the document controller, manufacturing engineers, a production
planner, the NDT lead and the cladding supervisor.

**Places.** The Controlled Documents library and the Standards site are indexed and open to everyone.
The manufacturing engineering team's site isn't open to production. The plant's shared mailbox and the
*Document Control* shared mailbox are shared mailboxes, so Copilot reaches neither. Technik's
sensitivity labels include *General* (work instructions) and *Confidential* (customer documents).

> Industry standards may be **referenced by title and number** only. Never copy their text into the
> repo; they're copyrighted.
