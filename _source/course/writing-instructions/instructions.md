## TL;DR

An agent's **instructions** are its standing brief: who it is, what it covers, how it answers and what it
must never do. They do two jobs at once. They describe the agent, and they bias every choice the agent
makes about which knowledge, tool or skill to reach for. They are read on **every turn**, a saved edit
reaches a conversation already running, and they are a strong request rather than a guarantee. Most of
writing good instructions is knowing what belongs in them and what belongs somewhere else.

## Why it matters

Instructions are the only part of an agent that touches every answer. A knowledge source is consulted when
it is relevant and a tool runs when it is called, but the instructions are present on the question about
weld prep, the question about PPE and the question the agent should refuse.

That makes them the artifact you will rewrite most. It also makes them the place people put everything
they cannot think where else to put. A 300-word brief turns into 1,500 words, and the agent gets slower,
more expensive and worse at the thing it used to do well. The skill is placement: keep in the instructions
what has to be true of every turn, and move the rest somewhere it is only read when it matters.

## How it works

### What the harness does with them

<!-- volatile verified=2026-09 -->
On the GitHub Copilot harness you type instructions into the **Instructions** section of the **Build**
tab and select **Save**.
<!-- /volatile -->

Microsoft describes the harnesses differently, and the difference is worth knowing:

| Harness | What the instructions do, per Microsoft |
|---|---|
| **GitHub Copilot harness** | *"The primary mechanism for controlling agent behavior."* The runtime interprets them to decide what to do, how to respond and what to avoid |
| **Standard harness**, with generative orchestration | Decide which resources to call — tools, knowledge, topics, other agents — fill tool inputs from context, and shape the response |

On both, descriptions do the other half of the routing. The orchestrator picks a tool or topic mainly
from its name and description ({{topic:orchestration}}), so the instructions say *when and why* to use
something, and the description says *what it is*. Neither can carry the other's job.

### What follows from being read every turn

**Everything is paid for continuously.** The instructions sit in the model's input beside the history,
the tool definitions and whatever was retrieved ({{topic:contextcost}}). A rule about drafting QN
write-ups is read when someone asks about a work order. At 300 words that is fine; at 1,500 it is a
standing tax on every answer.

**Edits land immediately.** A saved change reaches the very next reply, including in a chat that is
already running ({{topic:conversation}}). That is useful when you are iterating, and a trap when you are
halfway through a test you were relying on.

**They are not enforcement.** An instruction is followed *usually*. Anything that must be true every time
belongs in something that runs deterministically — a tool's input contract, a query filter, a flow, or on
the standard harness a topic. This distinction runs through the whole level.

### What Microsoft says to include

The GitHub Copilot harness documentation suggests five things:

- the agent's primary role and purpose;
- the tone and style;
- subjects or tasks it should decline or redirect;
- how to handle unclear or ambiguous input;
- escalation or hand-off triggers.

That is a sensible checklist and a poor structure. {{topic:xml}} turns it into fixed sections, and
{{topic:tasksvsinstr}} separates the two kinds of line people most often blur.

### What belongs here, and what does not

| Put it in the instructions | Put it elsewhere |
|---|---|
| Role, users, tone | A procedure used for one kind of request → a **skill** ({{module:agent-skills}}) |
| Scope, and what to say when out of it | What one tool does → its **description** ({{topic:tooldesc}}) |
| Grounding: answer from sources, cite, say when there is nothing | Facts the agent looks up → **knowledge** ({{module:knowledge-and-rag}}) |
| Which source wins when two disagree | A value that must be checked → a **tool input** or a flow |
| When to use which tool, skill or other agent | A long template or glossary → a **skill** or **knowledge** |

The left column is everything that applies to every turn and has nowhere else to live. Source precedence
is the clearest case: it governs every answer that touches two documents, and no single tool or source
could hold it.

## In practice at Technik

The Technik Production Assistant got its first instructions as a by-product of creating it
({{topic:create}}): a polite, generic draft that answered anything. Three things were fixed before any
knowledge was added — scope, grounding posture and tone. Since then, every addition has been forced by
something going wrong:

| Added | Line | What went wrong without it |
|---|---|---|
| At creation | Covers work orders, QNs, revisions and controlled documents; nothing else | It offered to plan a holiday rota |
| First knowledge source | Answer only from sources; name the document and revision; say *"I could not find that in my sources"* | An Inconel question got a confident, invented thickness ({{topic:genai}}) |
| `Get released revision` tool | Use it for any question about which revision is current; never infer a revision from a document's text | It quoted the revision printed on an old SWI copy |
| QN write-up skill | Use the skill for QN write-ups; do not restate its format here | Someone pasted the 40-line template into the instructions |

Two lines from the same agent show the difference between an instruction that works and one that reads
well:

> Answer only from your knowledge sources and tools. If they do not cover the question, say *"I could not
> find that in my sources"* and stop.

That changes behaviour, and you can write a question that proves it.

> Be accurate and helpful.

That changes nothing. The model is already trying to be both.

> [!TIP]
> Before adding a line, name the question that fails today and passes afterwards. If you cannot, the line
> is decoration, and you will pay for it on every turn from now on.

## Design guidance

- **Keep only what applies to every turn.** Everything else has a cheaper home.
- **Be specific.** *"Never state a torque value"* beats *"be careful with numbers"*.
- **Name your tools, skills and sources in the instructions** when you say when to use them, and keep
  what each one *is* in its own description.
- **Never use instructions for a guarantee.** If it must hold every time, enforce it.
- **Do not edit instructions in a chat you are relying on.** The edit lands mid-test.
- **Keep the text outside the portal**, somewhere you can diff it and say why each line is there.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A rule is followed most of the time | It is an instruction, not a guarantee | Move the guarantee into a tool input, a query or a flow |
| Answers got slower and vaguer over weeks | Lines accumulated and none were removed | Move procedures to skills and facts to knowledge ({{topic:writinginstructions}}) |
| The right tool exists but the agent does not use it | The instructions never say when it applies, or its description is vague | Say when in the instructions; say what in the description |
| Behaviour changed in the middle of a test | Someone saved an instruction edit | Expected. Start a new chat and re-run |
| Nobody knows why a line is there | No record of the failure it fixed | Keep the source copy with a note per line |

## Key terms

**Instructions** — the agent's standing brief, read on every turn.

**Placement** — deciding whether a requirement belongs in instructions, a description, a skill, knowledge
or something that enforces it.

**Guarantee** — a behaviour that must hold every time. Never an instruction alone.

**Source precedence** — which source wins when two disagree. An instruction-level rule.
