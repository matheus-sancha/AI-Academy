## TL;DR

{{topic:topicsvsflows}} decided which home a requirement gets. This lesson decides what happens **inside** one: for each step of a process, does code or a model do it? Anthropic and Microsoft draw the line in different places. Anthropic's *workflows* are fixed code paths, and they may call a model at every step. Microsoft's are rules-based automation that hands one step to an agent, or that an agent calls as a tool. The lesson follows Microsoft's usage, because that is what Copilot Studio builds. The working rule is the same on both pages: start with the simplest design, and give a model only the steps whose path you cannot draw in advance.

## Why it matters

A pipeline's cost is paid step by step. A step written as code is tested once and then trusted. A step given to a model costs credits ({{topic:aibuilder}}), adds latency, and can come back different next time. Making the whole pipeline an agent chooses that cost for every step, even those whose rule fits on an index card.

The opposite choice has a price too: a pile of `if` branches written to imitate judgement. The skill is placing the boundary one step at a time.

## How it works

### Two vocabularies

| | Anthropic | Microsoft |
|---|---|---|
| **Workflow** | LLMs and tools "orchestrated through predefined code paths" | Rules-based automation that "drive[s] process execution with consistency and speed", including an audit trail |
| **Agent** | A system where the LLM "dynamically direct[s]" its own process and tool use | A flexible solution that acts, shares knowledge and handles tasks |
| **Between them** | Both are *agentic systems* | A workflow calls an agent at one step, or an agent calls a workflow as a tool |

The definitions of *workflow* disagree. Anthropic's is model calls arranged by code, so it would call a Microsoft workflow with an agent node agentic. Microsoft's is deterministic except where it hands a step over. When one page says workflows trade latency for accuracy and the other says they bring speed, they mean different things.

Anthropic's page also dates from December 2024 and carries a note that much of its tooling description has since changed. Its design reasoning is the part worth keeping.

### Five shapes between a single call and an agent

Anthropic names five workflow patterns, and the lesson's step audit borrows them as a vocabulary:

| Shape | Use it when (Anthropic's test) |
|---|---|
| **Prompt chaining** | The task decomposes cleanly into fixed subtasks, with a programmatic check between steps if needed |
| **Routing** | Distinct categories are better handled separately. The classifier can be a model or "a more traditional classification model/algorithm" |
| **Parallelization** | Subtasks can run side by side for speed, or several attempts are needed for confidence |
| **Orchestrator-workers** | You can't predict the subtasks in advance, so a model chooses them at run time |
| **Evaluator-optimizer** | There are clear evaluation criteria, and iterating measurably improves the result |

Past these sits the autonomous agent, for open-ended problems where the steps can't be predicted. The page's advice is to find the simplest solution and add complexity only when it demonstrably helps, which "might mean not building agentic systems at all". Agentic systems trade latency and cost for performance, and autonomy brings compounding errors, so it recommends sandbox testing and stopping conditions such as a maximum number of iterations.

### Two directions of combining

Microsoft's post names both. A **workflow calls an agent** at a step that can't be captured in simple if-then logic. An **agent calls a workflow** where it needs to run a repeatable process reliably, and the post says to give the agent explicit instructions on when to use it. An agent node can also carry an option to contact a designated person when it needs clarification ({{topic:wfagentnodes}}).

<!-- volatile verified=2026-11 -->
The post says agent nodes are available now in all regions. It labels no feature generally available or in preview, and it is dated 10 April with no year in the text.
<!-- /volatile -->

### Auditing a process, step by step

Walk the process and put three questions to each step. **Can you write the rule down?** If yes, it is code. **What would a different answer on the second run cost?** If the answer is a wrong record, the step needs a check after it. **Who sees the result before it acts?** Wherever the answer is *nobody* and the action is hard to undo, put a person there ({{topic:hitl}}).

## In practice at Technik

Supplier material certificates are the module's running example. This is the intake process from {{topic:docproc}}, audited step by step:

| Step | Done by | Why |
|---|---|---|
| A file lands in *Incoming certificates* | Trigger | An event, not a decision |
| Is it a certificate? | The library and the file name | A rule. A model joins only if suppliers start mixing delivery notes into the library |
| Read the fields | A document model | The one step that has to cope with a different layout per supplier |
| Convert strength to MPa | Code | One supplier reports in ksi. 1 ksi is 6.894757 MPa, a constant |
| Check grade, the 485 MPa yield minimum and tensile above yield | Code | The purchase specification is the rule |
| Draft the query to the supplier when a check fails | An agent step | Drafting from the failed checks is the judgement |
| Accept, or send the query | A quality inspector | Material for pressure-containing equipment. The agent drafts and never sends |
| Write to the *Certificate register* | Code | A fixed row, written once a person has decided |

Two of eight steps use a model, and neither can accept a certificate. If the extraction misreads 72.1 ksi as 7.21, the conversion and the minimum check, which are code, flag it. The point of the split is that a model's mistake lands on a step that can be tested.

Take the conversion out and it shows. 72.1 ksi is 497 MPa and conforms, and 68.0 ksi is 469 MPa and does not. A validator that compares 72.1 with 485 rejects both. As code, the answer is the same every time.

<!-- unknown since=2026-11 -->
Neither source gives a measurement. Anthropic and Microsoft both call workflows consistent and agents flexible, and neither says how much an agent's runs vary, what either style costs, or how long a model step adds. The cost claims in this lesson are Anthropic's general statement plus the credit rates in {{topic:aibuilder}}. Nothing here was run.
<!-- /unknown -->

## Design guidance

- **Start with no model**, and add one for the step that fails without it.
- **Audit every step with the three questions**, and write down who owns each answer.
- **Keep the model's output a draft or a field**, and keep acceptance and writing in code or with a person.
- **Put a check after every model step**, written as code you can test.
- **Use Microsoft's two directions on purpose.** A workflow that calls an agent for one step, or an agent that calls a workflow for a fixed process, and tell the agent when to use it.
- **Set a stop** on anything that loops: a maximum number of iterations.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The same certificate passes on Monday and fails on Tuesday | The compliance check was given to a model | Write the rule as code |
| Every step is a model call and the bill is a surprise | No step was ever asked whether it needs one | Run the three-question audit |
| A branch for every phrasing of an exception | Judgement imitated with rules | Hand that step to an agent and check its output |
| The agent calls the workflow at the wrong moment | Its instructions never say when to use it | Write the trigger condition into the instructions |
| A loop runs on | No stopping condition | Add a maximum iteration count |

## Key terms

**Workflow**: a fixed path, which Microsoft builds from rules-based steps and Anthropic from model calls arranged by code.

**Agent**: a system in which the model decides its own steps and tool use.

**Handover**: the point where a step passes between code, a model and a person.
