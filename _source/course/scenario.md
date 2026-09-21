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
| **SharePoint** | Standards and supporting documents that engineers consult alongside Teamcenter documents | Knowledge source (not in Snowflake) |

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
guided builds. It covers seven capability areas:

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
not yet written.

### Basic — documents only

| Module | Worked examples |
|---|---|
| `how-copilot-works` | An answer citing a revision of `SWI70000318` that does not exist |
| `prompting` | Turning a vague *summarise this QN* prompt into a specific, structured one |
| `how-copilot-sees-your-work` | Why a document in a SharePoint site the reader cannot open never appears in an answer |
| `copilot-chat` | Finding which document covers weld prep inspection, and checking the citation |
| `copilot-in-word` | Summarising `SWI70000318`; starting a document from the `GWI70000027` template |
| `copilot-in-excel` | Tabulating values from ten supplier material certificates |
| `copilot-in-powerpoint` | Turning `SOP70000101` into a short briefing deck |
| `copilot-in-outlook` | Drafting a note about documents past their review date |
| `copilot-in-teams` | Catching up on a thread about `ECN70000042` |
| `using-agents-others-built` | Asking the Production Assistant a work order question and auditing what it cites |

### Intermediate — built in Copilot Studio

| Module | Worked examples |
|---|---|
| `getting-oriented` | Where the Production Assistant sits in the Microsoft AI stack |
| `how-models-behave` | Counting tokens in an SWI; the same summary at different temperatures |
| `agent-fundamentals` | Mapping the assistant's seven capabilities onto knowledge, tools, topics and flows |
| `copilot-studio-basics` | A *Work order status* topic |
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

### Advanced — the same company, pro-code

| Module | Worked examples |
|---|---|
| `developer-tooling` | The repo layout for the Production Assistant rebuild |
| `agent-harness` | Watching the agent loop run against a Teamcenter lookup |
| `context-engineering` | Redesigning the context budget: instructions, tool results, long SAP result sets |
| `authoring-skills` | A *document revision* skill package: template, change-summary script, ECN cross-check |
| `mcp` | An MCP server over Teamcenter revision data and QNs, connected to VS Code and Copilot Studio |
| `advanced-tools-and-multi-agent` | Splitting into a production agent (SAP) and an engineering agent (Teamcenter, documents, standards) with handoff |
| `pro-code-agents` | Rebuilding the assistant in Microsoft Agent Framework |
| `evaluation-and-observability` | An eval harness with regression gates for the Agent Framework build |
| `security-advanced` | Threat-modelling the assistant; data exfiltration through tools; DLP design |
| `alm-and-governance` | Pipelines, Git integration and CI/CD with evaluation gates |
| `guided-build` *(capstone)* | Scaffold → MCP server over Teamcenter data → agent → evals → ship |
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
| `SAP_PROJECTS` | `PROJECT_ID`, `PROJECT_NAME`, `CLIENT_NAME` (invented), `FIELD_NAME` (invented), `FAT_DUE_DATE`, `STATUS` | `snowflake-sql` joins |
| `SAP_UNITS` | `SERIAL_NO`, `PRODUCT_TYPE` (XT / MANIFOLD), `MODEL`, `PROJECT_ID`, `PLANT`, `STATUS` | `copilot-studio-basics`, `snowflake-sql` |
| `SAP_BOM_LINES` | `PARENT_PART_NO`, `COMPONENT_PART_NO`, `QTY` | `snowflake-sql` joins |
| `SAP_WORK_ORDERS` | `WO_NO`, `PART_NO`, `SERIAL_NO`, `PROJECT_ID`, `PLANT`, `RELEASED_AT`, `COMPLETED_AT`, `STATUS` | `copilot-studio-basics`, `knowledge-and-rag`, `tools-connectors-mcp`, lead time |
| `SAP_WO_OPERATIONS` | `WO_NO`, `OP_SEQ`, `OPERATION`, `WORK_CENTER`, `ROUTING_HOURS`, `ACTUAL_HOURS`, `PLANNED_START`, `ACTUAL_START`, `ACTUAL_END`, `STATUS`, `DRAWING_NO`, `DRAWING_REV`, `CNC_PROGRAM_NO`, `CNC_PROGRAM_REV`, `WORK_INSTRUCTION_NO`, `CONFIRMATION_NO`, `CONFIRMED_AT` | Efficiency, `snowflake-sql` windows |
| `SAP_QUALITY_NOTIFICATIONS` | `QN_NO`, `WO_NO`, `SERIAL_NO`, `PART_NO`, `OPERATION`, `DEFECT_TYPE`, `DESCRIPTION`, `PRIORITY`, `STATUS`, `CREATED_AT`, `CLOSED_AT` | `agent-skills`, `safety-and-moderation`, `mcp`, `snowflake-cortex` |
| `TC_PARTS` | `PART_NO`, `REVISION`, `DESCRIPTION`, `RELEASE_STATUS`, `RELEASED_AT` | `tools-connectors-mcp` revision tool |
| `TC_DRAWINGS` | `DRAWING_NO`, `REVISION`, `PART_NO`, `TITLE`, `RELEASE_STATUS`, `RELEASED_AT` | `tools-connectors-mcp`, `mcp` |
| `TC_DOCUMENTS` | `DOC_NO`, `DOC_TYPE`, `REVISION`, `TITLE`, `OWNER`, `STATUS` (In Work / In Review / Released / Obsolete), `RELEASED_AT`, `NEXT_REVIEW_DATE` | `automation-and-workflows` revision flow, `authoring-skills` |
| `TC_CNC_PROGRAMS` | `PROGRAM_NO`, `REVISION`, `PART_NO`, `MACHINE`, `RELEASE_STATUS`, `RELEASED_AT` | `tools-connectors-mcp`, `mcp` |
| `TC_ECNS` | `ECN_NO`, `TITLE`, `REASON`, `STATUS`, `CREATED_AT`, `RELEASED_AT` | Revision history |
| `TC_ECN_AFFECTED_ITEMS` | `ECN_NO`, `ITEM_NO`, `ITEM_TYPE` (Part / Drawing / Document / CNC Program), `FROM_REV`, `TO_REV` | Revision history |
| `FAT_RESULTS` | `SERIAL_NO`, `TEST_ID`, `TEST_NAME`, `RESULT`, `TESTED_AT`, `RAW` (`VARIANT`: bench readings as JSON) | `authoring-skills`, `snowflake-cortex` |

Conventions the data follows:

- **Work order status** uses the SAP codes `CRTD`, `REL`, `PCNF`, `CNF` and `TECO`; operation status
  uses `OPEN`, `INPROC` and `CNF`. Everything else — project, unit, notification, revision status — is
  spelled out in words. Turning the codes into something a user can read is one of the jobs of the
  view in `snowflake-sql`.
- **`SAP_WO_OPERATIONS` has one row per confirmation**, not per operation. An operation should have
  exactly one; where it has two, the higher `CONFIRMATION_NO` is the posting that counts.
- **A work order is "blocked" when its current operation is `INPROC` and an open notification names
  that work order.** There is no blocked flag; the agent works it out by joining.
- **Dates in examples are illustrative.** Where an example depends on elapsed time ("older than 30
  days"), it says what it assumes.

Deliberate flaws in the data, which lessons use as examples:

- **Operations confirmed twice** — a partial posting that was never reversed, then the full
  re-posting. Hours and operation counts are double-counted, and welding at Plant 1 reads about
  **111% efficiency** until the stale postings are dropped with `QUALIFY`, at which point it is about
  **89%** (`snowflake-sql`, `snowflake-cortex`).
- **Work orders on superseded revisions**: work orders `100004510` and `100004513` reference a drawing
  or CNC program revision that a released ECN has replaced. Found by joining SAP with Teamcenter
  (`snowflake-sql`, `mcp`).
- **Documents past their review date**: `SOP70000114`, `SWI70000318` and `TDS70000044`, for
  document-revision prompts (`copilot-in-outlook`, `automation-and-workflows`).
- **Near-duplicate QNs** `300001211` and `300001219`, raised for the same overlay porosity, for
  similarity search (`snowflake-cortex`).
- **QN descriptions containing injected instructions**, `300001267` and `300001270`, for the
  prompt-injection examples (`safety-and-moderation`, `security-advanced`).

`ECN70000042` is released and still waiting for revision C of `SWI70000318`. That is not a defect — it
is the change drafted in `automation-and-workflows` and `authoring-skills`.

**Agent identity.** Technik's agents and MCP servers read Snowflake as `TECHNIK_AGENT_RO`, a read-only
role, on warehouse `TECHNIK_AGENT_WH`. People query with their own roles; agents never borrow them.

## Documents (knowledge sources)

All documents are invented, short, and marked *Fictional — for training only*. This is the layer
**Basic** draws on in full.

| Document | Type | Used in |
|---|---|---|
| `SOP70000101` Quality Notification Handling | SOP | `copilot-in-powerpoint`, `knowledge-and-rag`, `agent-skills`, `advanced-rag` |
| `SOP70000114` Engineering Change Notification Process | SOP | `knowledge-and-rag`, `authoring-skills` |
| `SWI70000318` Cladding Preparation and Inspection | SWI | `copilot-in-word`, `knowledge-and-rag`, `automation-and-workflows`, `authoring-skills` |
| `SWI70000402` Hydrostatic Test During Assembly & Testing | SWI | `knowledge-and-rag` citations, `advanced-rag` |
| `GWI70000027` Controlled Document Authoring Template | GWI | `copilot-in-word`, `agent-skills`, `authoring-skills` |
| `DGL70000009` Cladding Design Guidelines | DGL (Teamcenter) | Engineering questions, `advanced-rag` |
| Technik internal standards (e.g. weld overlay acceptance criteria) | SharePoint | `knowledge-and-rag` |
| Supplier material certificates (10 samples) | PDF | `copilot-in-excel`, `automation-and-workflows`, `automation-advanced` |
| Plant safety and PPE rules | Web page (SharePoint) | `copilot-chat`, `knowledge-and-rag` |

> Industry standards may be **referenced by title and number** only. Never copy their text into the
> repo; they're copyrighted.
