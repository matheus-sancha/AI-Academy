## TL;DR

The orchestrator never sees what a tool does, only what you **said** it does: a name, a description,
and the names and descriptions of its inputs and outputs. Microsoft ranks the description first. So
those lines are the tool's interface, and you write them like instructions: plain words, the user's
vocabulary, a clear boundary. The two failures that matter are a **vague** description, which leaves a
tool unused, and **near-twins**, two descriptions so alike that the choice between them is
unpredictable.

## Why it matters

When an agent calls the wrong tool it looks like a model mistake. Usually the model did exactly what
the text in front of it suggested, and the text was yours, or was never written at all.

A tool usually arrives with a description already filled in. The standard harness calls it "often
prepopulated", and the GitHub Copilot harness shows one when you add a tool and tells you to review it.
Whoever built the connector wrote that text to describe the connector in a catalogue. It knows nothing
about your agent, your users or your other tools. Leave it in place and your routing logic was written
by a stranger.

## How it works

### What the orchestrator reads

In Microsoft's order: the description first, then the name, then the input and output parameters with
*their* names and descriptions. The GitHub Copilot harness adds that the instructions also influence
when tools are used. The instructions say *when and why*; the description says *what*
({{topic:instructions}}).

On the standard harness the description has a second job: the orchestrator uses it to phrase the
question it asks when an input is missing. Never say what a part number looks like, and the follow-up
question will be vague.

<!-- volatile verified=2026-10 -->
**Where you edit it.** On both harnesses the tool's **Details** panel holds the name and description.
An MCP server's tool descriptions are the server's: you can switch individual tools off, not rewrite them
({{topic:mcpadd}}).
<!-- /volatile -->

<!-- verified tenant=2026-10 -->
Each input can have its own description on both harnesses. The GitHub Copilot harness's documentation
describes only configuring input *values*, but its Inputs panel lets you rewrite an input's description too.
<!-- /verified -->

### What a good description says

Four things, in this order:

1. **What it returns**: the thing itself, not the system behind it. "Efficiency % by operation" beats
   "Queries SAP data".
2. **When to use it, in the user's words**: *taking longer than planned*, *overrunning*, not your
   column names.
3. **When not to, naming the neighbour**: "Do not use for calendar time; use `Get work order lead
   time`." This is the sentence that keeps similar tools apart.
4. **What it needs**: identifiers and their format, if the inputs do not make it obvious.

Under that sit Microsoft's style rules: active voice, present tense, plain words, jargon spelled out.
A name is a short, unique phrase: *Create support ticket*, not *Ticket tool*.
Microsoft suggests one or two sentences; the exclusion usually makes it three. Six is too many, because
the description is in context on every turn ({{topic:contextcost}}).

### Near-twins

When descriptions are similar, the agent picks **one**, and the overlap makes *which* one
unpredictable ({{topic:orchestration}}). No error, just a different answer on different days. Tools
rarely overlap in purpose; they overlap in *words*: both mention work orders, parts and time. Say what
makes each one different, and write the boundary into **both** descriptions, not just the one in front
of you.

### Keep the list short

The standard harness supports up to 128 tools per agent and recommends 25 to 30 for the best results.
The gap is the point: every definition is re-sent each turn, used or not, and every one is another
option to choose between.

<!-- unknown since=2026-10 -->
The GitHub Copilot harness says MCP servers count against "the total number of tools an agent can
host" but does not state that number. Treat the standard harness's 25–30 as the working ceiling until
it is published.
<!-- /unknown -->

Turning a tool off keeps it attached but out of the choice; removing it detaches it. Either beats
leaving an unused tool in the list.

## In practice at Technik

The assistant's two performance tools are the pair most likely to blur. *Efficiency* is routing hours
÷ actual hours × 100, per operation. *Lead time* is calendar days from release to technical completion,
per work order. With descriptions left vague, they read:

> **`Query efficiency`**: Returns work order performance data from Snowflake.
>
> **`Query lead time`**: Returns work order timing data from Snowflake.

Ask *"How long are `P7000001042` work orders taking?"* and either is a reasonable match, so over a day
of testing both get chosen. Rewritten:

> **`Get operation efficiency`**: Returns efficiency % (routing hours ÷ actual hours × 100) by
> operation, work centre or plant for a period, from confirmed operations. Use when the user asks
> whether work is taking longer or shorter than planned, about overruns, or about efficiency of welding,
> machining or another operation. Do not use for calendar time from release to completion; use
> `Get work order lead time`.
>
> **`Get work order lead time`**: Returns lead time in calendar days, from work order release to
> technical completion, averaged by part number, project or plant for a period. Use when the user asks
> how long work orders take end to end, or how long until something is finished. Do not use for hours
> against plan; use `Get operation efficiency`.

Each name now states its measure, each description defines its number and names its twin, and the
boundary is *calendar days versus hours against plan*, a real difference, rather than *performance
versus timing*, which is not. The original question is still ambiguous, because the user has not
decided either. No description settles that. The instructions do:

```
<rules>
If a question about how long work orders take could mean either lead time or efficiency, ask which
the user means before calling a tool.
</rules>
```

Then test the pair together, reading the activity trace rather than the answers:

| Question | Expected |
|---|---|
| What's the efficiency of welding at Plant 1 this month? | `Get operation efficiency` |
| Is machining overrunning on `PRJ-2031`? | `Get operation efficiency` |
| What's the average lead time for `P7000001042` work orders? | `Get work order lead time` |
| How long until work order `100004521` is finished? | Neither; that is status, so `Get work order status` |
| How long are `P7000001042` work orders taking? | Asks which is meant |

The fourth row is the one people forget: rewriting two tools changes the choice for a third, so the
whole routing set is re-run, not just the two you edited ({{topic:addconnector}}).

## Design guidance

- **Rewrite every description you inherit.** The prepopulated text describes a connector, not your
  agent.
- **Name the measure or the object, then the verb.** `Get work order lead time`, not `Query lead
  time`.
- **Define your terms inside the description.** If a number has a formula, the formula belongs there.
- **Name the neighbour in every exclusion**, and write the boundary into both descriptions.
- **Hold the list near 25 to 30 at most.** Past that, merge, remove, or split the agent
  ({{topic:connected}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A connector tool is never chosen | The prepopulated description is still there | Rewrite it for this agent, in the user's words |
| Two tools take turns answering the same question | Near-twin descriptions; the pick is unpredictable | Define each one's measure; name the twin in both exclusions |
| Fixing one tool broke a third | Descriptions are compared against each other | Re-run the routing set for every tool |
| The agent asks a vague follow-up for an input | The description never says what the input looks like | State the format and an example |
| An MCP tool keeps winning over yours | Its description, written by the server author, matches better | Sharpen yours or turn that MCP tool off ({{topic:mcpadd}}) |

## Key terms

**Tool description**: the text the orchestrator matches a request against, and the strongest factor in
the choice.

**Near-twin**: two tools whose descriptions overlap enough that the choice between them is
unpredictable.

**Routing set**: the fixed list of questions, with the tool each should reach, re-run after every
change.
