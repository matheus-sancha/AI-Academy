## TL;DR

On the **standard harness**, a variable holds a value during a conversation so later steps can use it. A
**topic variable** lives inside one topic; a **global variable** is shared across the agent; **system** and
**environment** variables are supplied for you. **Power Fx** is the Excel-like formula language you use to
check, transform and combine those values. Together they are where a topic puts the small deterministic
work — a format check, a date calculation — that you should never hand to a model. The GitHub Copilot
harness has no topics, so it has none of this.

## Why it matters

A model remembers nothing between requests ({{topic:llm}}). Everything that looks like memory in a
standard-harness agent is built around it, and inside a topic, variables are that machinery. A work order
number the user gave three turns ago is still available because a Question node stored it, not because
the agent "remembered".

Power Fx matters for a less obvious reason. It is the one place in a topic where a value is computed
rather than generated. `IsMatch` on a work order number is right every time; an instruction asking the
model to check the number is right most of the time. When something must be true, use the mechanism that
makes it true.

On the GitHub Copilot harness you still need the vocabulary: half the pages you will read assume it, and
its guarantees have to live somewhere else on yours ({{topic:chooseharness}}).

## How it works

### Where variables come from

Any node that returns an output creates a variable of the right type automatically — a **Question** node
creates one for the answer, a tool call creates one for each output. A **Set variable value** node sets
one yourself, from a literal, another variable of the same type, or a Power Fx formula. A new variable's
type is **unknown** until it is given a value.

<!-- volatile verified=2026-09 -->
The **Variables** panel on a topic's menu bar lists every variable available to that topic. Selecting one
opens **Variable properties**, where you rename it, see where it is used, choose whether it can receive
values from other topics or return values to them, and convert it to a global variable. That conversion is
one way: a global variable cannot be turned back into a topic variable.
<!-- /volatile -->

### Scope

In a formula, a prefix names the scope:

| Prefix | Scope | Use for |
|---|---|---|
| `Topic.` | One topic | Working values inside one path |
| `Global.` | The whole agent, for the session | A value more than one topic needs |
| `System.` | Supplied by the platform | The conversation, the user, the channel — for example `System.Conversation.Id` |
| `Environment.` | Set per environment | Configuration that differs between development, test and production |

Before reaching for a global, check whether you need one. Topics can **pass** variables to the topic they
redirect to, and **return** them to the topic that called them, so a value one topic collects can reach
the next without being shared agent-wide. Microsoft presents this as the way to reduce global variables.
Three entity types cannot be passed this way: Date and time, Duration and Multiple choice options, and
nor can custom entities.

The environment row matters more than it looks. A site URL or a schema name that changes between
environments is not a topic variable; it is an environment variable, set when the solution is deployed
({{topic:solutions}}). An environment variable can also reference an **Azure Key Vault secret** — but
anyone who can edit the agent can add a Message node that prints it, so a secret in an agent is only as
private as the agent's editor list.

### Power Fx

<!-- volatile verified=2026-09 -->
Power Fx goes wherever a node accepts a value: the **Formula** tab of a Set variable value node, or a
Condition node switched to **Change to formula**. Copilot Studio uses **US-style numbers** — a dot is the
decimal separator and a comma separates parameters, whatever your locale.
<!-- /volatile -->

The subset you will use constantly:

| Need | Formula |
|---|---|
| Check a format | `IsMatch(Topic.WorkOrderNo, "\d{9}")` |
| Clean what was typed | `Upper(Trim(Topic.Answer))` |
| Default when empty | `Coalesce(Global.Plant, "Plant 1")` |
| Build a message | `"Work order " & Global.WorkOrderNo & " is at " & Topic.Operation` |
| Date arithmetic | `DateDiff(Topic.ReleasedAt, Now(), TimeUnit.Days)` |

`IsMatch` tests the whole value by default, so `"\d{9}"` rejects ten digits as well as eight. A **Parse
value** node handles the other common need: turning a JSON string from a flow or API into a typed
**Record** your formulas can read.

### The trap

A global variable persists; its **meaning** does not. `Global.WorkOrderNo` is still set when the user has
moved on to a different work order, and nothing clears it for you. Worse, a set variable is not a used
one: under generative orchestration the value is available to the orchestrator, not compulsory for it.

The **Reset Conversation** system topic clears global variables for the session, but not the conversation
history the orchestrator reads ({{topic:conversation}}). Clearing that takes a **Clear variable values**
node with *Conversation history for the current session*.

## In practice at Technik

The Technik Production Assistant is on the GitHub Copilot harness and has no topics, so this is the
standard-harness design: the *Work order status* topic from {{topic:topics}}, with its variables.

| Variable | Scope | Why |
|---|---|---|
| `Topic.Answer` | Topic | What the user typed at the Question node, before it is checked |
| `Global.WorkOrderNo` | Global | The follow-up *"which operation is it at?"* must not ask again |
| `Global.Plant` | Global | Set when a user names a plant; scopes later questions |

The check that earns its keep:

```
IsMatch(Trim(Topic.Answer), "\d{9}")
```

SAP work orders are nine digits — `100004521`; part numbers are eleven characters — `P7000001042` — and
people type one for the other constantly. Caught here, every later node can
trust `Global.WorkOrderNo`.

The second decision is when to clear it. If the user asks about `100004513` after `100004521`, the Question
node overwrites the value. If they ask *"how many QNs are open on cladding?"*, the old work order is still
set, and an answer that mentions `100004521` looks exactly like a hallucinated number. The topic that
changes the subject clears the global.

On the GitHub Copilot harness the same check moves into the lookup tool's input contract, which rejects
anything that is not nine digits. Nothing stores the number between turns except the conversation itself.

## Design guidance

- **Topic variable by default.** Pass or return values between topics before making one global.
- **Validate at capture with Power Fx**, never with an instruction.
- **Clear globals when the subject changes.**
- **Put per-environment values in environment variables**, and treat a Key Vault reference as visible to
  every editor.
- **Rename every variable** for what it holds. `Var1` is unreadable in a trace.
- **Never ask the model** to do arithmetic, date maths or format checks Power Fx can do.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent re-asks for something it was told | The value was a topic variable nobody passed on | Pass it on redirect, or make it global |
| An old work order number appears in an unrelated answer | A global was never cleared | Clear it when the subject changes; check variables before blaming the model |
| A part number was accepted as a work order | No check at capture | `IsMatch` in a Condition node |
| A formula fails in a comma-decimal locale | Copilot Studio uses US-style numbers | Dot for decimals, comma between parameters |
| Reset Conversation did not clear the context | It clears globals, not history | Clear variable values → conversation history |
| There is no Variables panel | The agent is on the GitHub Copilot harness | Put the check in the tool's input contract |

## Key terms

**Topic variable** — scoped to one topic; can be passed to or returned from another.

**Global variable** — shared across the agent for the session. Cannot be converted back.

**System variable** — supplied by the platform, such as `System.Conversation.Id`.

**Environment variable** — configuration set per environment, optionally a Key Vault secret.

**Power Fx** — the Excel-like formula language for checking, transforming and combining values.

