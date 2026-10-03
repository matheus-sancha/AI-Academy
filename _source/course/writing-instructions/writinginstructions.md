## TL;DR

Instructions that hold up are specific, structured and tested against real questions. Two rules do most of
the work. **Write every rule as must or must-never with its reason attached**, because a rule whose reason
is missing gets reasoned around. And **treat size as economics**: everything in the instructions is paid
for on every turn, so when they grow too long, move reference material into a skill or a knowledge source.
Never cut the role, tone, rules or routing to fit. If they cannot fit without that, the agent is doing too
much and should be split.

## Why it matters

Most instructions are written once, read with satisfaction and never tested. They look complete because
they cover every concern, and they fail because covering a concern is not the same as changing behaviour.

The failures are predictable. A rule says *never* and the model finds a case where *never* seems
unreasonable. A line is vague enough to agree with whatever the model was going to do anyway. The text
grows each time someone hits a problem, until a model change or a new tool shifts the balance and nobody
can say which line was doing what. This lesson is about writing instructions that survive all three.

## How it works

### Be specific, and say what to do

Microsoft's guidance for agent instructions comes down to removing interpretation:

- **Use precise verbs** — *ask*, *search*, *check*, *call*, *quote* — rather than *handle* or *process*.
- **Say what to do**, not only what to avoid. A must-never with nothing in its place leaves the model to
  invent the alternative.
- **Define your own terms.** If *efficiency* means routing hours over actual hours, say so once.
- **Make each step atomic.** *"Extract the metrics and summarise them"* is two steps.
- **Always specify tone, length and format**, or the model infers them, differently on different models.
- **Give the model an out.** Say what to answer when the sources have nothing, so it does not invent.

### Rules carry their reasons

A bare rule is a string the model has to apply to cases you did not imagine. Given only *"Never quote a
revision from a document's text"*, a model faced with a user saying *"the SWI in my hand says rev B"* has
to guess whether that counts. Given the reason — *"because printed copies go stale and work is built to the
released revision"* — it can see that the user's copy is exactly the case the rule exists for.

The reason also tells **you** whether the rule still earns its place. A rule nobody can explain is either
obsolete or misplaced, and both are reasons to remove it.

So each line in `<rules>` has the same shape: *must* or *must never*, the behaviour, *because*, the
consequence. Add what to do instead wherever the model would otherwise improvise.

### Size is economic

<!-- volatile verified=2026-09 -->
Microsoft documents an **8,000-character** limit on instructions for agents that extend Microsoft 365
Copilot — on its Copilot Studio limits page, which is written for the standard harness, and on its
declarative agent guidance.
<!-- /volatile -->

<!-- unknown since=2026-10 -->
No Microsoft page states an instruction limit for the **GitHub Copilot harness**. Treat 8,000 characters
as a safety margin, not a known wall, until it is checked in a tenant.
<!-- /unknown -->

The field limit is not the real constraint anyway. The instructions share the model's input with the
history, tool definitions and retrieved content on **every turn** ({{topic:contextcost}}), so a long
instruction set costs you on the question about PPE as much as on the one it was written for.

When the text grows too long, there are two ways down, in this order:

1. **Move reference material out.** Anything the agent *consults* rather than *obeys* — a long template, a
   code table, a policy extract — goes into a skill or a knowledge source. This frees context on every turn
   instead of losing content.
2. **Trim the lowest-value sections**: `<examples>`, then `<out_of_scope>`, then `<data_handling>`.

Never trim `<role>`, `<tone>`, `<rules>`, `<tool_use>` or `<knowledge_routing>` to fit. They decide what
the agent does and where its answers come from, and cutting them produces a shorter agent that is wrong.
If the instructions cannot fit without cutting them, the agent is doing too much: split it.

Note what moves out: **reference, not directives.** Microsoft warns, for declarative agents, against
keeping instructions in a SharePoint document to get around the limit. Knowledge content is not trusted as
instructions, so directive-like text there can be blocked, truncated or sanitised at runtime — and anyone
who can edit the document can change the agent.

### Tested, not admired

Every line should have a question that fails without it and passes with it. Microsoft's iteration loop is
create, test, change, test again, and its RAG guidance adds two disciplines worth keeping: change **one**
thing at a time, and keep each version with what it scored. Instructions interact, so re-run the whole set
after any change, not only the case you were fixing. And re-run it when the model changes
({{topic:model}}): Microsoft says outright that a model update can change how an agent reads its
instructions.

## In practice at Technik

Three rules from early drafts of the Technik Production Assistant's instructions, and what they became:

| Draft | Rewritten |
|---|---|
| Be careful with revisions. | Never call a revision current unless its status is **Released**, because work is built to whatever the answer says. If only In Work or In Review revisions exist, say so. |
| Don't make up data. | Answer only from your knowledge sources and tools, because engineers act on the answer. If nothing covers the question, say *"I could not find that in my sources"* and stop. |
| Don't give torque values. | Never state a torque, pressure or dimension unless it is quoted from a released document, because a remembered value can be from the wrong revision. Name the document and revision with the value. |

The size problem arrived when the QN write-up format was pasted into `<instructions>`: a 40-line template
read on every work order question. Moving it into the QN write-up skill ({{module:agent-skills}}) took the
instructions from about 9,600 characters to about 4,100, and the only line left about it is *"Use the QN
write-up skill for QN write-ups."*

The two definitions from the scenario — *efficiency* is routing hours over actual hours, *lead time* is
calendar days from release to technical completion — stayed. They are two lines, and they change how every
answer about efficiency is read.

## Design guidance

- **Write every rule as must or must-never, plus *because***, plus what to do instead.
- **Use precise verbs and define your own terms.**
- **Move reference out before trimming anything**, and never move directives into a knowledge source.
- **Never trim role, tone, rules or routing.** Split the agent instead.
- **Keep one test question per line**, and re-run all of them after any change.
- **Re-test after a model change**, even if you changed nothing.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A rule is broken in a case nobody foresaw | The rule had no reason, so the model guessed its scope | Add the reason and the alternative |
| The agent obeys a vague line and nothing changes | The line agrees with what it would do anyway | Delete it, or make it specific and testable |
| Instructions near the limit, and growing | Reference material kept in them | Move templates and tables to a skill or knowledge |
| Behaviour from a SharePoint "instructions" page is unreliable | Directives placed in knowledge | Move them back into the instructions |
| Fixing one case broke another | Instructions interact | Re-run the full set after every change |
| Behaviour shifted with no edit | The model changed | Re-run the set; adjust where precision matters |

## Key terms

**Must / must-never rule** — a rule stated as an absolute, with its reason and what to do instead.

**Reference material** — content the agent consults rather than obeys. Belongs in a skill or knowledge.

**Directive** — content the agent must obey. Belongs in the instructions.

**Split** — dividing an agent whose essential sections cannot fit, rather than cutting them.
