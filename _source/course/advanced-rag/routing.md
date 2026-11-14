## TL;DR

Retrieval comes in three kinds: an aggregate over rows, passages from documents, and one record found by its key. A
good agent sends each question to the right kind, or combines them, because a wrong route fails politely: search
returns paragraphs where a number was wanted, and a text-to-SQL tool has nothing to say about a document. The two
platforms in this module route differently. A Cortex Agent plans, picks a tool per subtask and reflects. Copilot Studio
searches its knowledge sources, and says it filters them with a model above 25. Neither page measures how well it routes,
so you do, and where a wrong route is silent and costly, the route belongs in code.

## Why it matters

{{topic:cortexanalyst}} answers a question about rows and {{topic:cortexsearch}} and {{topic:hybrid}} answer a question
about text. A real question does not say which it is. The risk is not an error message. It is a plausible answer from
the wrong tool, in the same confident tone as a right one, so routing is where a retrieval system quietly loses trust.

## How it works

### Three kinds of question

| Kind | Technik example | Right tool | A wrong tool returns |
|---|---|---|---|
| Aggregate over rows | *What is welding efficiency at Plant 1 this month?* | Text-to-SQL over a semantic view | Paragraphs about efficiency, and no sum |
| Passages | *What does `SWI70000318` allow on a sealing surface?* | Document search | No answer, since Analyst resolves only what SQL can |
| One record by key | *Is revision C of `SWI70000318` released?* | A lookup on the identifier | A passage that mentions revision C and says nothing of its status |

The roadmap's pair of structured and unstructured leaves out the third. It is the capstone's whole design: its three
tools are all keyed lookups, and none of them aggregates or searches.

### How a Cortex Agent routes

<!-- volatile verified=2026-11 -->
A Cortex Agent is a schema-level object that bundles a model, tools and orchestration instructions. Each request runs a
loop of three steps. It plans, which can mean disambiguating a vague question, splitting a complex one into subtasks and
choosing a tool for each. It uses the tools, Cortex Analyst for structured data and Cortex Search for unstructured. It
reflects on the results, then asks a clarifying question, calls another tool or answers. You shape the planning with
natural-language instructions, and Snowflake recommends the `auto` model. A preview analytical-search tool answers counts
and trends over large document collections, which is a fourth kind. Orchestration is billed on tokens, Analyst per token
on this path, and Search by the size of its index, so every route has a price, and an orchestration budget caps a run.
<!-- /volatile -->

The page is plain about limits. Snowflake does not guarantee the accuracy of the responses or of the citations, and says
to review answers before serving them. And if the caller's role cannot use every configured tool, the run can still
continue with the tools it can reach.

<!-- unknown since=2026-11 -->
A run that continues without a tool is a silent downgrade only if nothing tells the user. The page says the run
continues and does not say what the response shows. It links a section on inaccessible tool handling that was not
read for this lesson. Test it with a role that lacks one grant.
<!-- /unknown -->

### How Copilot Studio routes

<!-- volatile verified=2026-11 -->
Copilot Studio grounds an agent in knowledge sources: public websites, uploaded documents, SharePoint, Dataverse and
connector data. SharePoint, Dataverse and connector sources run as the asking user, so the agent surfaces only what that
person can open. With generative orchestration, an internal GPT model filters the sources when an agent has more than 25
of them, and the page points to *authoring descriptions* for how to steer it. Uploaded files do not count towards the
25. Dataverse, the one table-based source, is retrieved with a technique the page names and does not describe.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
The page says when the filtering starts and not how a source is chosen at or below 25, nor how well the filter picks.
Nothing on it describes a question that needs a sum over a source.
<!-- /unknown -->

### Where the route is decided

There are three places, in rising order of certainty. The platform's planner decides from the descriptions you wrote
({{topic:tooldesc}}), which is cheap and probabilistic. Your instructions can state the rule, as Technik's
`<knowledge_routing>` block does ({{topic:citations}}). And code can decide before any model runs: an identifier shaped
like a document number goes to the lookup. The capstone's instructions already check an identifier's format before a tool
is called ({{topic:stageagent}}). This course's position, which neither page states, is to route in code where a
wrong route is silent and costly, and to leave the rest to the planner, where a bad route is visible and cheap.

## In practice at Technik

*Work order `100004521` has not moved. What is holding it, and what does the work instruction say about the porosity?*
That is three questions. The first reads SAP: the order is released, its current operation is `0020` Cladding,
`INPROC`, and open QN `300001234` names it, so it is blocked. The second needs a key lookup, since revision B of
`SWI70000318` is released and revision C is a draft. The third is a passage, section 5's porosity limit in revision B.
No single tool answers all three, and a planner that sends the whole question to document search can return the limit
and never mention the QN.

In the Production Assistant, routing is a Copilot Studio matter: fixed-query tools and two SharePoint sources, steered by
descriptions and a routing block. In a pro-code build the Snowflake half could be a Cortex Agent that a Microsoft agent
reaches ({{topic:sfintegrate}}), with the lookups beside it. The question is where each mis-route would hide. A planner
that skips the lookup answers *is revision C released?* from a passage, which says what the text says and not what the
record says, and that is the costly one. So route identifiers in code and leave the planner the open questions.

<!-- unknown since=2026-11 -->
Nobody ran any of this. The capstone has no search and no Snowflake agent, and the routes above are the course's own
reading of the pages. The invented `V_QUALITY_NOTIFICATIONS` view in {{topic:cortexsearch}} is the same kind of
assumption.
<!-- /unknown -->

## Design guidance

- **Name the kind of each question first**: aggregate, passage or key.
- **Write each tool's description** around the question it answers and the one it does not.
- **Route in code where a wrong route is silent**, such as anything keyed on an identifier.
- **Put the expected route on every evaluation case**, and score routing apart from the answer ({{topic:rageval}}).
- **Test with a role that lacks one grant**, to see what the user is told.
- **Cap the planner** with an orchestration budget, and count a planning call in the cost of every question.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A sum question returns paragraphs | The planner chose document search | Describe the aggregate tool by the questions it answers |
| A lookup question quotes a draft | The planner skipped the key lookup | Route identifiers in code |
| An answer covers half the question | One tool was reachable and the other was not | Test each role, and report a skipped tool |
| Every question is slower | A planning call runs on each request | Send simple questions straight to a tool |
| A filtering model drops the right source | More than 25 sources, with weak descriptions | Write descriptions, or cut sources |
| Confident, uncited answers | Snowflake does not guarantee accuracy or citations | Add a grounding check ({{topic:grounded}}) |

## Key terms

**Routing**: choosing, per question or per subtask, which retrieval tool answers it.

**Orchestration**: the plan, use tools, reflect loop a Cortex Agent runs on each request.

**Knowledge source**: a Copilot Studio definition of searchable content.

**Keyed lookup**: retrieval of one record by its identifier, which needs no search.
