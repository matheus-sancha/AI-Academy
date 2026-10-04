## TL;DR

Every requirement in the brief lands in exactly one of four places, and the triage is learnable. Reads live
data or writes into another system: a **tool**, and a fixed multi-step process with branching or approvals is
a tool too, built as a flow. Content the agent answers from: **knowledge**. Produces a document, follows
a procedure or applies bundled reference material: a **skill**. Everything else: **instructions**. People reach
for connectors when what they need is a sentence in the instructions, and every unnecessary tool is paid for on
every turn.

## Why it matters

None of the brief's slots says *build a tool here*. The triage turns a design record into a parts list, and
it is where most avoidable cost enters an agent.

A requirement in the wrong place still works in a demo, and fails later in a way that points somewhere else.
A rule made into a skill holds only when its description matches. Reference tables pasted into the
instructions are re-sent on every turn and half-followed. Live rows set up as a knowledge source come back as
passages to summarise instead of values to report. And a tool built for something the instructions could have
said adds a definition every unrelated question pays for ({{topic:contextcost}}).

## How it works

### Four places, four jobs

Microsoft's comparison for the GitHub Copilot harness gives each component one purpose: instructions for
general agent behaviour, knowledge for data the agent can reference, tools for actions via external services,
skills for reusable task-specific capabilities. As a triage, asked in this order:

| Ask | If yes | Because |
|---|---|---|
| Does it read live data, or write into another system? | **Tool** | Tools are how an agent interacts with external systems. Rows are values to report, not passages to summarise |
| Is it a fixed multi-step process, with branching or approvals? | **Tool**, built as a **flow** | One tool that runs the same way every time: a workflow on this harness ({{topic:tools}}) |
| Is it content the agent should answer from? | **Knowledge** | Knowledge grounds answers in documents, pages and indexed data, per user |
| Does it produce a document, follow a procedure, or apply bundled material? | **Skill** | The earns-a-skill test ({{topic:skillsvs}}); a skill uses tools, it does not replace them |
| None of the above | **Instructions** | Behaviour, tone, rules and routing: what applies to every turn |

A flow is not a fifth place. Copilot Studio lists it among the tool types, beside connectors and MCP servers, and the orchestrator chooses it by its description like any other tool.

### Exactly one place, after splitting

A requirement that seems to need two places is two requirements. *"Draft the next revision of a controlled
document from a released ECN"* is a procedure with a template (a skill), a read of the ECN and its affected
items (a tool), and a must-never about unreleased ECNs (instructions). Split it, then place each part once.

The *once* matters as much as the place. A procedure described in a skill and again in the instructions will
drift, and nobody can say afterwards which version the agent followed.

### What each place costs

| Place | Paid on every turn | Paid only when used |
|---|---|---|
| Instructions | All of it | Nothing |
| Tool | Name, description, input descriptions | The call and its result |
| Knowledge | Its description, for routing | The search and the passages returned |
| Skill | Its description | Its body and files, once activated |

Tools are the expensive default. Microsoft recommends keeping an agent to **25 to 30 tools** for best results on
the standard harness, and its multi-agent guidance expects routing to degrade past 30 to 40 choices, sooner if
descriptions are similar. Two questions catch most unnecessary tools before they exist:

- **Could a sentence do it?** Formatting, wording, what to say when something is missing: instructions.
- **Could an existing tool return it?** A column added to a query is free on every turn that does not use it. A
  new tool is not.

## In practice at Technik

The Production Assistant's brief, triaged:

| Requirement (from the brief) | Place | Why |
|---|---|---|
| Report a work order's status and current operation | Tool | Live rows from `SAP_WORK_ORDERS` and `SAP_WO_OPERATIONS` |
| Report efficiency for an operation and period | Tool | An aggregation over `V_WORK_ORDER_OPERATIONS` ({{topic:sfviews}}) |
| Report lead time for a period | Tool | Calendar days from `SAP_WORK_ORDERS`; kept apart from efficiency by its description ({{topic:tooldesc}}) |
| List open QNs on a project | Tool | Live rows from `SAP_QUALITY_NOTIFICATIONS` |
| Report the latest released revision and its ECN | Tool | Live rows from `TC_*` |
| Say what `SWI70000318` requires for acceptance | Knowledge | A controlled document to answer from, read as the asking user |
| Draft the next revision in the `GWI70000027` template | Skill | A procedure, a template, its own format, needed a few times a week |
| Never call a revision current unless it is Released | Instructions | A rule on every revision answer |
| Plain answer first, codes explained after | Instructions | Tone, for every answer |
| Say the data is as of last night's replication | Instructions | One sentence, whenever SAP data is shown |
| Name the document owner when sources conflict | The revision tool, plus instructions | `TC_DOCUMENTS.OWNER` added to an existing query; the escalation itself is a rule |

Three rows are worth arguing with.

**Work order data is not knowledge.** Snowflake can be added as a knowledge source on the standard harness,
but it runs as the asking user and returns passages to generate from ({{topic:snowflakeknowledge}}). A status
question wants a value from one row, read as `TECHNIK_AGENT_RO`. That is a tool.

**The escalation recipient is not a new tool.** The first draft added *Get document owner*. The owner is one
column of the table the revision tool already reads, so the tool returns it and every unrelated question is
spared another definition.

**The status codes are not a tool either.** A planner asked for *"a connector to the SAP status code list"*.
There are five work order codes and three operation codes. They fit in four lines of the instructions, which is
less than one tool's description.

Release approval is missing from the table on purpose. The drafting task ends *ready for the document owner to
submit for review* ({{topic:tasks}}), so the approval flow belongs to the owner's submission
({{topic:approvals}}), not to the agent. Triage places only the agent's own requirements.

## Design guidance

- **Triage the brief, not the wish list.** Every part should trace back to a slot.
- **Ask the questions in order**, and stop at the first yes.
- **Split compound requirements first**, then place each part exactly once.
- **Before adding a tool, ask whether a sentence or an existing tool would do.**
- **Live rows go to a tool, documents to knowledge**, whatever the source can technically do.
- **Leave out what the agent does not own.** A step after the task's finished state belongs to someone else.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Routing slips after the tenth tool | Tools built for things a sentence could say | Move them to the instructions; merge near-twins |
| A rule holds on some answers and not others | It was made a skill, so it fires on a description match | Move it to the instructions |
| Status answers summarise instead of reporting a value | Live data set up as knowledge | Read it through a tool |
| The same procedure behaves two ways | It lives in a skill and in the instructions | Keep it in one place |
| A tool returns one field another tool already reads | A new tool where a column would do | Extend the existing query |
| The agent tries to run another person's step | A requirement placed that the agent does not own | Check it against the task's finished state |

## Key terms

**Triage**: placing each requirement from the brief in exactly one of instructions, knowledge, tool or skill.

**Flow**: a deterministic multi-step process the agent calls as one tool; on this harness, a workflow.

**Compound requirement**: a requirement that is really several, each with its own place.

**Standing charge**: what a component costs on every turn, whether or not it is used ({{topic:contextcost}}).
