## TL;DR

Variables hold information during a conversation. **Topic variables** live inside one topic; **global
variables** are shared across the whole conversation. **Power Fx** is the Excel-like formula language
you use to transform values, build conditions and format output. Together they are how a standard
harness agent remembers anything — because the model itself remembers nothing.

## Why it matters

[B1 established that the model is stateless](../B1/llm.html). Everything that feels like memory is
built around it, and in the standard harness variables are that machinery. A work order number Ana
gave three turns ago exists because a topic put it in a variable, not because the agent
"remembered".

Power Fx matters for a less obvious reason: it is where you put the small deterministic bits —
format checks, trimming, uppercasing, date arithmetic — that you should never ask a model to do.

## How it works

### Scope

| Kind | Lives | Use for |
|---|---|---|
| **Topic variable** | One topic, one run | Working values inside a path |
| **Global variable** | The whole conversation, across topics | Things the user said once that later turns need |
| **System variable** | Provided by the platform | User identity, channel, conversation id |
| **Environment variable** | Per environment, set at deployment | Configuration that differs between dev, test and production (B12) |

That last row is the one people miss. A schema name or a site URL that changes between environments
is **not** a variable in your topic; it is an environment variable, and getting that right in B5
saves a deployment problem in B12.

### Power Fx

Power Fx is the same formula language as Power Apps. You will use a small subset constantly:

| Need | Looks like |
|---|---|
| Trim and uppercase what the user typed | `Upper(Trim(Topic.Answer))` |
| Check a format | `IsMatch(Topic.Answer, "\d{9}")` |
| Default when empty | `Coalesce(Global.Plant, "Plant 1")` |
| Build a message | `"Work order " & Global.WorkOrderNo & " at " & Global.Plant` |
| Date arithmetic | `DateDiff(Global.ReleasedAt, Now(), TimeUnit.Days)` |

<!-- volatile verified=2026-09 -->
Which Power Fx functions are available inside Copilot Studio differs from Power Apps and changes
between releases. Check the linked documentation before relying on a function you know from
elsewhere.
<!-- /volatile -->

### The trap

A variable persists; **meaning does not**. `Global.WorkOrderNo` is still set ten turns later when
the user has moved to a different work order entirely, and nothing clears it. Worse, nothing
guarantees the model *uses* it — with generative orchestration the variable is available, not
compulsory.

So: set them deliberately, clear them deliberately, and never assume a set variable is a current
one.

## In practice at Technik

The *Work order status* topic uses three:

| Variable | Scope | Why |
|---|---|---|
| `Topic.Answer` | Topic | What the user typed at the question node |
| `Global.WorkOrderNo` | Global | Ana asks follow-ups about the same work order. Re-asking each time is the fastest way to make an agent annoying |
| `Global.Plant` | Global | Set when a user mentions a plant, used to scope later queries |

And one piece of Power Fx that earns its keep:

```
IsMatch(Trim(Topic.Answer), "^\d{9}$")
```

Technik work order numbers are nine digits. Part numbers are eleven characters starting `P70000`,
and people type them into the wrong field constantly. Catching that here, deterministically, is
worth more than any instruction: the model will usually notice, and "usually" is not a validation
strategy.

Note what this is doing in course terms. It is the same principle as B7's *"put the constraint in
the query, not the prompt"* and B6's *"deduplicate in a view, not in a description"*. Three
different modules, one idea: **when something must be true, use the mechanism that makes it true.**

> [!WARNING]
> `Global.WorkOrderNo` surviving into an unrelated question is a real failure mode, and it looks like
> the agent hallucinating a work order number. Clear globals when the subject changes, and when
> debugging a wrong number, check the variable before blaming the model.

## Design guidance

- **Global only when more than one topic needs it.** Everything else is a topic variable.
- **Clear globals when the subject changes.**
- **Validate at capture**, with Power Fx, not with an instruction.
- **Put per-environment values in environment variables**, not in topics (B12).
- **Name variables for what they hold**, not for where they came from.
- **Never ask the model to do arithmetic or format-checking** that Power Fx can do.
- **Check variables first** when a wrong value appears in an answer.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent re-asks for something it was told | The value was a topic variable | Make it global |
| An old value appears in an unrelated answer | A global was never cleared | Clear on subject change |
| A part number was accepted as a work order | No validation at capture | `IsMatch` in the topic |
| The agent ignores a set variable | With generative orchestration it is available, not compulsory | Use the variable explicitly in the topic path |
| It works in dev and breaks in production | Environment-specific values hard-coded | Environment variables (B12) |
| A Power Fx function from Power Apps does not exist | The subset differs | Check the current documentation |

## Key terms

**Topic variable** — scoped to one topic run.

**Global variable** — shared across topics for the conversation.

**System variable** — supplied by the platform: user, channel, conversation.

**Environment variable** — configuration that differs per environment, set at deployment (B12).

**Power Fx** — the Excel-like formula language for transforming values and building conditions.

**`IsMatch`** — Power Fx pattern matching. The cheapest validation you have.
