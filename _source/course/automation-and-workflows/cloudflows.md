## TL;DR

A Power Automate cloud flow is a **trigger** followed by **actions**. The trigger is an event, a schedule or a
button. The actions are connector calls, conditions, loops and expressions. A cloud flow is for work that has
to happen whether or not anyone is talking to an agent: nobody asks it anything, and it never has to answer
one. It is the oldest of the three automation designers in this module and the one with the most templates
and connectors. It is also the only one that does not live in Copilot Studio.

## Why it matters

Plenty of the work around an agent should not involve one. A reminder that a document is overdue for
review, a nightly export, a notification when a record changes: each runs on a timetable or an event, with
the same steps every time, and nobody types a question. Building that as an agent conversation adds a model
where none is needed, and a model can be wrong.

The cost of picking the wrong designer is mostly paid later. Cloud flows are licensed and billed through
Power Automate, while agent flows and workflows consume Copilot Studio capacity
({{topic:agentflows}}, {{topic:workflows}}). A flow built in one designer does not simply move to another,
so the choice is worth making on purpose. {{topic:topicsvsflows}} settles where each kind of logic belongs.
This lesson covers what a cloud flow is for.

## How it works

### Trigger, then actions

Every cloud flow starts with exactly one trigger:

| Trigger | Starts the flow when | Example |
|---|---|---|
| **Automated** | An event happens in a connected service | A file is added to a SharePoint library |
| **Scheduled** | A recurrence comes round | Every Monday at 06:00 |
| **Instant** | Someone presses a button, in the portal, an app or Teams | Run this report now |

After the trigger come **actions**: steps that call a connector (send an email, query a database, post to
Teams) or shape the run. **Conditions** branch, **Apply to each** loops over a list, and **expressions**
compute values such as `addDays(utcNow(), -7)` or a formatted date. Each action can use the outputs of the
steps before it.

Flows live in an **environment** and are invisible from any other. Microsoft's guidance is to check you are
in the right environment *before* building, because components do not move between environments easily.

### What makes a flow maintainable

A cloud flow that works is not the same as one that someone else can support. The coding standards in
*Go deeper* come down to a handful of habits:

- **Build inside a solution**, so the flow can be exported, versioned and moved ({{topic:solutions}}).
- **Use connection references, not connections**, and have a **service account own them**. Then the flow
  survives its author changing roles.
- **Name every action** for what it does. `Get documents past review` reads in run history; `Submit SQL
  Statement 2` does not.
- **Wrap the work in a scope and catch failures.** A second scope set to run only *after failure* tells the
  process owner what failed, with a link to the run, and ends the flow as **Failed** rather than silently
  succeeding.
- **Filter at the source.** Ask the connector for the rows you need instead of looping over everything and
  checking each one.

<!-- volatile verified=2026-10 -->
Flows are built at make.powerautomate.com, from a template, from a description given to Copilot, or from a
blank canvas. The home page's navigation and the Copilot entry point move between releases. The *Go
deeper* home-page tour shows the current layout.
<!-- /volatile -->

### The licensing line

Cloud flows run on Power Automate licensing. Some connectors are **premium**, which changes the licence a
flow needs, and the Snowflake connector is one ({{topic:connectors}}). A cloud flow can be **converted
to an agent flow** if it is in a solution and the environment has Copilot Studio capacity. Conversion moves
its billing to Copilot Studio, and it is **one-way**. A cloud flow cannot be converted to the new workflow
format at all.

## In practice at Technik

Three documents are past their review date: `SOP70000114`, `SWI70000318` and `TDS70000044`. Nobody asks an
agent about them. A weekly reminder to each owner is the right shape, and it is a cloud flow:

| Step | Action | Detail |
|---|---|---|
| Trigger | **Recurrence** | Mondays, 06:00 plant time |
| 1 | `Get documents past review` | Snowflake *Submit SQL Statement*: `TC_DOCUMENTS` where `STATUS = 'Released'` and `NEXT_REVIEW_DATE < CURRENT_DATE` |
| 2 | `For each overdue document` | Apply to each over the returned rows |
| 3 | `Email the owner` | Outlook, to `OWNER`: the document number, title and how many days it is overdue |
| 4 | `Post the weekly summary` | Teams, one message to the document control channel listing all three |
| Catch | `Notify on failure` | Runs only if steps 1–4 fail; emails the flow's owner with the run link |

A few decisions in that table are worth explaining.

**The query filters in Snowflake.** Step 1 returns three rows, not every document Technik has. The loop
then has nothing to check, only work to do.

**The connection reads as the read-only role.** The flow uses a connection reference to the same service
principal connection the agent's Snowflake tools use, so it reads as `TECHNIK_AGENT_RO` on
`TECHNIK_AGENT_WH`. A reminder flow has no business writing to anything, so least privilege applies here
just as it does to the agent ({{topic:connauth}}).

**There is no model in it.** Every step is deterministic, so the reminder is identical every week and its
run history is an audit trail. Asking an agent to "remind owners about overdue documents" would add a step
that can paraphrase a document number.

Drafting revision C of `SWI70000318` is a different job, and it does not belong in this flow. It needs a
person, a template and judgement, which makes it the Production Assistant's work ({{topic:skill}}). The
approval that follows the draft is covered in {{topic:approvals}}.

## Design guidance

- **Reach for a cloud flow when nobody is in the conversation.** A schedule or an event, fixed steps and
  no question to answer.
- **Choose the designer before you build.** Conversion to an agent flow is one-way, and to a workflow is
  impossible.
- **Solution, connection references and a service account from the first save.**
- **Name actions for what they do**, and catch failures where the process owner will see them.
- **Filter at the source**, not in a loop.
- **Give a flow the same least-privilege identity thinking as an agent.**

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Every flow a colleague built stops when they leave | Connections owned by a person | Connection references owned by a service account |
| The flow "succeeded" but nobody got an email | A failed step was skipped and nothing caught it | A catch scope that notifies and ends the run as Failed |
| The flow is missing in the test environment | It was built outside a solution, or in another environment | Build in a solution; check the environment before creating |
| A loop runs for minutes over thousands of rows | Filtering inside the flow instead of in the query | Filter in the connector call |
| A flow with the Snowflake connector will not run for its owner | Premium connector, and the licence does not cover it | Check the licence before designing around a premium connector |
| Run history is unreadable | Default action names | Rename every action for its purpose |

## Key terms

**Cloud flow** — a Power Automate automation that runs in the cloud from a trigger.

**Trigger** — the event, schedule or button press that starts a flow.

**Action** — one step of a flow: a connector call, a condition, a loop or a data operation.

**Expression** — a formula that computes a value inside a flow.

**Connection reference** — a solution component that points to a connection, so the flow is not bound to
one person's sign-in.

**Premium connector** — a connector that requires a premium Power Automate licence to use.
