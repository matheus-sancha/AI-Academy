## TL;DR

{{topic:workflows}} taught the parts: the agent node, its output modes and the Test tab. This lesson is about the **skeleton around them**. A workflow is a deterministic path with model steps hung on it, and its behaviour is decided by where the rules sit, what each agent node is shown, and where branches rejoin. A third-party build in the course's sources keeps the rules as data in an array, gives each judgement its own agent node, runs a rules branch and an agent branch side by side, and lets the last node write only after both finish. Microsoft's overview page adds three facts that bear on the design: every action consumes capacity, AI results can vary, and the harness decides what you get. Two roadmap claims, approvals and sample inputs for node tests, are in neither source.

## Why it matters

A workflow with one agent node is easy to reason about. A pipeline with three is where a wrong rule hides: the rule sits in a prompt, the node reads a field the previous node named differently, or a message is written from half the facts. None of that shows in a single node's test.

The sources are also uneven. Microsoft's page is a short overview, and almost everything about a multi-agent build comes from one community article, so what follows is a pattern to adapt and check, not documented behaviour.

## How it works

### The skeleton

Microsoft describes a workflow as a trigger and at least one action. The trigger runs on demand, on a schedule or on an event. Actions come in four kinds:

| Kind | What the page says |
|---|---|
| **AI capabilities** | Generate text, process documents, run a prompt, call an agent, write a natural-language reply to a calling agent |
| **Human in the loop** | Actions that require human intervention, "such as requesting information" |
| **Built-in tools** | Looping and branching, data operations, date and time functions, child workflows |
| **Connectors** | Microsoft 365, third-party and custom |

No approval action is named anywhere on the page, and the community article never mentions one. A workflow that needs a named approver is a question for {{topic:approvals}}, not an assumption.

### Rules as data, judgement as a node

The community article builds a loan-application reviewer with three agent nodes, and its structure transfers:

1. A SharePoint file arrives. One agent node reads the PDF and returns each field **as it is**, with blanks left blank, as structured output.
2. A variable holds the **rules as an array**, each entry an expression returning true or false, with a field name and an error message. A **Filter array** keeps the entries that came out false.
3. A second agent node judges the one field a rule cannot: a free-text purpose, classified against a list attached to the agent as knowledge.
4. Both branches are wired off the first node, so they **run in parallel**. A third agent node writes the reply, and the article says it runs only once every parallel branch has finished.

Three things carry over. The rules live in data that a person can read and test, not in a prompt. Each agent does one judgement. And the writer sees only the filtered failures and the category, never the raw document.

The article's gotchas are as useful as the pattern. Downstream expressions read an agent's output through the node's auto-generated name and a `structuredOutput/` prefix, so renaming a node breaks every rule that reads it. The article's own two agents disagree on a label, *Approved or Flagged* against *Allowed*. The knowledge list has to be attached to the agent. And the author tests whole runs, republishing and re-uploading a file each time.

*Adapted from the article's expression for one field of an agent node's structured output:*

```text
body('Agent__Extract_Certificate_Fields')?['structuredOutput/Heat_No']
```

### What the overview page adds

<!-- volatile verified=2026-11 -->
Every action a workflow runs consumes Copilot Studio capacity. When prepaid capacity is used up, **new runs are blocked** and running ones complete, and pay-as-you-go is the suggested way round it. An administrator reviews the actions a workflow used in the Power Platform admin center under Licensing, then Copilot Studio. The Workflows page has a *Credit usage (last 30 days)* column, and classic workflows show **N/A**, which the page says does not mean no credits were used.
<!-- /volatile -->

The page's one caution about AI: results can vary when actions use AI or retrieve changing data. It also says the harness affects billing, features and capabilities.

<!-- unknown since=2026-11 -->
Naming. The overview calls its harness the **Microsoft Copilot harness** and its title reads *Workflows overview (Microsoft Copilot)*, where the rest of this course says GitHub Copilot harness. Whether that is a rename or a second harness the page does not say, so check which one your agent is on ({{topic:chooseharness}}).
<!-- /unknown -->

## In practice at Technik

Supplier certificates, as the module's example, rebuilt as a workflow instead of the AI Builder flow in {{topic:docproc}}:

| Node | Kind | Detail |
|---|---|---|
| Trigger | Connector | A file is created in *Incoming certificates* |
| `Get file content` | Connector | The PDF |
| `Extract certificate fields` | Agent node, **no tools** | Structured output: supplier, certificate number, heat number, grade, strength with its unit |
| `Rules` | Variable, array | Convert ksi to MPa, grade, yield of at least 485 MPa, tensile above yield |
| `Failed rules` | Filter array | Entries that came out false |
| `Any failures?` | Condition | None → register row **Ready for sign-off**. Some → next |
| `Draft supplier query` | Agent node, **no tools** | Input: the failed rules only. Output: a short note |
| `Send to inspector` | Connector | To the quality inspector for that supplier, who sends or discards it |

The agents have no tools because a certificate is a file a supplier wrote, and {{topic:injection}} treats text from outside as untrusted. The worst a manipulated PDF can do is produce a wrong field or an odd draft, and the rules and the inspector see both.

The comparison with the AI Builder version is plain. A document model returns a confidence score for each field, which the earlier flow used to say where to look first. Neither source mentions a score on an agent node's output, so the inspector gets every field with no hint of which ones the agent was unsure of.

<!-- unknown since=2026-11 -->
Whether an agent node's output can carry a confidence value, and what a failed node does to the run. The overview names neither, and the article's only testing advice is to compare predictions with real results. The failure path in {{topic:errors}} has to be built around that gap.
<!-- /unknown -->

Use the document model when layouts repeat and a per-field score helps. Use an agent node when the reading itself needs judgement, and accept the loss of the score.

## Design guidance

- **Keep the rules in data**, an array or a table, never in an agent's instructions.
- **One agent node per judgement**, with the smallest input it can do the job with.
- **Give agent nodes no tools** when they read text from outside.
- **Wire independent work in parallel**, and make the node that depends on both wait for both.
- **Never rename a node** that later expressions read, and make labels match across agents.
- **Test one node, then the whole run**, with a failing case first.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Every rule fails after a tidy-up | A node was renamed, so the expression path is stale | Re-point the expressions, and leave names alone afterwards |
| The writer ignores a category | Two agents use different words for it | Fix the labels in one place |
| The judging agent finds nothing in its list | The list exists but is not attached as knowledge | Attach it to the agent |
| The reply goes out half-written | The writer was wired to one branch | Wire it after both |
| New runs stop mid-month | Prepaid capacity was used up | Watch usage, and consider pay-as-you-go |

## Key terms

**Rules array**: the checks held as data, each an expression with a field name and a message.

**Parallel branch**: two paths wired off one node that run at the same time.

**Structured output**: an agent node's answer as named fields, readable by later steps.
