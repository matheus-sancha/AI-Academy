## TL;DR

Everything the agent is made of is re-sent to the model **on every single turn**: the instructions, the
conversation history, every tool's definition, and any tool results. The ceiling you actually hit is the
model's total input size, not any per-field character limit — which is why an agent with fifteen tools pays
for fifteen tools on every question, including the ones that need none of them. When a turn fails for this
reason it has a name: `CONTEXT_LENGTH_EXCEEDED`.

## Why it matters

Most people meet this as a mystery. An agent that worked fine grows a few more tools, or a conversation
runs long, and turns start failing — or worse, do not fail but quietly lose the earlier part of the
conversation.

The instinct is to trim the instructions, because that is the field you can see and the one with a number
next to it. That is sometimes right and often the most expensive choice available, because the instructions
are where the role, the rules and the routing live, and those are earning their keep on every turn. What is
*not* earning its keep is reference material sitting in a field that gets re-sent whether or not anyone
asked for it.

## How it works

Microsoft's own description of the failure is the clearest statement of the mechanism:

> The combined size of the agent's instructions, the conversation history, the tool definitions, and any
> tool results is larger than the model can process in a single turn. Long conversations and large numbers
> of tools are the most common causes.

Four contributors, one shared budget.

| Contributor | Grows with | Paid |
|---|---|---|
| **Instructions** | What you wrote | Every turn, in full |
| **Tool definitions** | How many tools, and how long their descriptions are | Every turn, for every tool, used or not |
| **Conversation history** | How long the conversation has run | Every turn, until it is truncated |
| **Tool and knowledge results** | How much a call returned | The turn it arrives and while it stays in history |

The second row is the one that surprises people. The runtime has to show the model the catalogue in order
for the model to choose from it ({{topic:orchestration}}), so every tool's name, description and input
descriptions are present on every turn — including on a question that needs no tool at all. Tools are not
free when idle. They are a standing charge.

### Why the ceiling is not the field limit

A Copilot agent's instructions cap at 8,000 characters, and it is tempting to treat that as *the* limit. It
is not. It is one field's limit inside a much larger shared budget, and you can be comfortably inside it
and still exceed the model's input size because history and fifteen tool definitions are sitting alongside
it.

This is also why the same agent can fail on the twentieth turn of a conversation and succeed on the first.
Nothing changed about your configuration. The budget filled up.

### The four documented remedies, and which to reach for

The documentation lists four responses to `CONTEXT_LENGTH_EXCEEDED`:

1. Shorten the instructions.
2. Reduce the number of tools attached to the agent.
3. Start a new conversation to clear the history.
4. Choose a model with a larger context window.

All four work. The judgement is *which*, and it depends on what is actually large:

- **If the conversation is long**, start a new one — and notice that this is the same first move as most
  other apparent failures ({{topic:conversation}}).
- **If the tool list has grown**, cut it. Two narrow tools with sharp descriptions beat five overlapping
  ones, and the orchestrator routes better with fewer choices anyway ({{topic:tooldesc}}).
- **If the instructions are long**, cut *reference material*, never the role, tone, rules or routing.
  Move it into a knowledge source, or into a **skill** — which exists partly for this reason. Skills
  implement a progressive-disclosure pattern so an agent "loads only the context it needs, when it needs
  it": until the runtime activates a skill, only its description is in play, not its body
  ({{topic:skill}}).
- **A larger model** is a real option, not a cop-out — but it treats the symptom, and it changes cost and
  behaviour, so re-evaluate afterwards ({{topic:models}}).

> [!IMPORTANT]
> If instructions cannot fit without cutting the role, rules or routing, the agent is doing too much. That
> is a design signal, not a formatting problem: split it ({{topic:connected}}).

### The neighbouring failures

Two other codes look similar in the moment and are not the same thing. `QUOTA_EXCEEDED` means your
organisation's longer-running AI quota is exhausted — schedule large evaluation runs off-peak, as the
documentation advises. `RATE_LIMIT_REACHED` is a short-lived burst limit that clears in seconds. Neither is
about your agent's size ({{topic:licensing}}).

Error codes surface in the **Preview** tab, in preview history, in the activity trace and in **Evaluate**
results — the activity trace being the GitHub Copilot harness's window into a turn, the counterpart of the
standard harness's activity map ({{topic:test}}).

## In practice at Technik

The Production Assistant covers seven capability areas, and a naive build gives each one its own tool:
work order status, efficiency, lead time, notifications, revisions, document lookup, document drafting.
Seven tools, plus knowledge over the standards and controlled documents, plus a skill.

Now price a question that needs none of them — *"what does this level expect me to know about cladding?"*
Seven tool definitions, their input descriptions, the knowledge source descriptions and the full
instructions all travel to the model anyway. The reader asked a one-line question and paid for the whole
catalogue.

The fix is not to delete capabilities. It is to notice which of them are not tools at all:

| Naive | Better | Why |
|---|---|---|
| Document lookup as a tool | A knowledge source | Retrieval over documents is what knowledge does, and its description costs less than a tool's ({{topic:sources}}) |
| Document drafting as a tool | A skill | It is a procedure with bundled reference material, loaded only when it fires ({{topic:skillsvs}}) |
| The Technik document conventions pasted into the instructions | The same text inside that skill | Re-sent every turn versus loaded on demand |

That last row is the whole lesson in one line. The document-authoring conventions are several hundred words
that matter on the rare turn someone drafts a revision, and are dead weight on every other turn.

## Design guidance

- **Count the standing charge.** Before adding a tool, ask what every unrelated question will now pay.
- **Cut reference material out of instructions, not structure.** Role, tone, rules and routing stay.
- **Prefer a skill or a knowledge source for anything bulky and occasional.** That is what progressive
  disclosure is for.
- **Bound every tool result.** Row limits and selected columns; an unbounded result is a context problem
  as well as a cost one ({{topic:tools}}).
- **Treat a long conversation as a variable**, not a constant. Test a twentieth turn, not just a first.
- **Read the error code** rather than guessing which contributor grew.
- **Split the agent when it will not fit.** Too much to fit is too much to be one agent.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `CONTEXT_LENGTH_EXCEEDED` on a turn that used to work | Combined instructions, history, tool definitions and results exceeded the model's input | Identify which grew; do not reflexively trim instructions |
| Fails late in a conversation, fine in a new one | History filled the budget | Start a new conversation; expect this in long Teams threads |
| The agent forgot something said earlier | History was truncated rather than exceeded | Restate key facts periodically; keep conversations shorter |
| Adding the tenth tool slowed and worsened everything | Every tool is paid for on every turn, and the choice got harder | Merge, remove, or split ({{topic:connected}}) |
| Instructions were trimmed and behaviour degraded | The rules or routing were cut, not the reference material | Restore them; move bulk into a skill instead |
| Evaluation runs fail at busy times | `QUOTA_EXCEEDED`, not agent size | Run them off-peak ({{topic:licensing}}) |

## Key terms

**`CONTEXT_LENGTH_EXCEEDED`** — the request exceeded the model's maximum input size. The maker's problem to
fix.

**Progressive disclosure** — loading only the context needed, when it is needed. The mechanism behind
skills ({{topic:skill}}).

**Activity trace** — the GitHub Copilot harness's per-turn record, where a failed step shows its error code
({{topic:test}}).
