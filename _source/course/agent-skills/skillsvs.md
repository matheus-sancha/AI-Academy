## TL;DR

**Tools** perform an action. **Skills** hold know-how about how to carry out a kind of task. **Topics** are
scripted conversation paths, and they exist only on the standard harness. A skill may call several tools; a
topic fixes the exact steps. Most of the real decisions, though, are between a skill and plain
**instructions**, and they come down to one test: a task earns a skill when it needs bundled reference
material, follows a fixed procedure, produces an output with its own conventions, or is needed only
sometimes. Otherwise it belongs in the instructions.

## Why it matters

From a requirements list the options look interchangeable. *Draft a quality notification* could be a
paragraph in the instructions, a skill, a topic or a tool that calls a flow, and every one of them can be
made to work in a demo. They fail differently and at different times. An instruction that should have been
a skill bloats every turn and gets half-followed. A skill that should have been a sentence in the
instructions fires unpredictably, because something that should always apply now applies only when a
description matches. A topic that should have been a skill turns a judgement into a rigid script that breaks
on the first unusual case.

This is also the distinction {{topic:triage}} builds on when it sorts a whole design into its parts. Get the
three-way split straight here and the four-way one later is mostly bookkeeping.

## How it works

### Three components, three jobs

Microsoft's own comparison puts each component in its lane: instructions for general behaviour, knowledge
for data the agent references, tools for actions through external services, skills for reusable
task-specific capabilities. Adding topics from the standard harness gives the full picture:

| | Does what | What is fixed | Who decides when | Harness |
|---|---|---|---|---|
| **Tool** | One action: a query, an API call, a flow | The action itself | The orchestrator, from the tool's description | Both |
| **Skill** | Follows a written procedure, calling tools as needed | The procedure; not the wording or the decisions | The orchestrator, from the skill's description | GitHub Copilot |
| **Topic** | Runs a designed conversation, node by node | Almost everything: you drew the path | Its trigger | Standard |

**A skill uses tools; it does not replace them.** The skills overview gives the example itself: a skill
might instruct the agent to use a specific tool in a particular way. A skill holds *how*; a tool does
*one thing*. A skill that writes its own SQL has swallowed a tool's job, and a tool whose description runs to
a procedure is a skill in the wrong place.

**A topic fixes the steps; a skill does not.** A topic is the right answer when the exact path matters
more than the result reading naturally: a structured intake, a confirmation, a check that must happen in
order. On the GitHub Copilot harness there are no topics, so the same need is met by a tool's input
contract, a workflow, or a rule in the instructions ({{topic:topics}}, {{topic:chooseharness}}).

### The earns-a-skill test

Tools and topics are usually easy to spot: one is an action, the other is a script. The harder line, and
the one you will draw most often, is between a skill and the instructions. A task earns a skill when at
least one of these is true:

1. **It needs bundled reference material**: a template, a lookup table, a list of codes. A skill carries
   files; the instructions do not.
2. **It follows a fixed procedure** that must run the same way every time: steps in order, checks that
   cannot be skipped.
3. **It produces an output format with its own conventions**: headings, field order, wording rules that
   would take a page to state.
4. **It is needed only sometimes.** Progressive disclosure means a skill's body costs nothing on the turns
   that do not need it ({{topic:skill}}).

If none holds, it belongs in the instructions. *Always cite the document number and revision* is needed on
every answer, has no procedure and no template, and is one sentence. Making it a skill would make a rule
that should always apply depend on a description match, which is strictly worse.

The fourth criterion is the one that settles close calls. Something needed on most turns is cheaper in the
instructions, where it is always present; something needed rarely is cheaper as a skill, where it is
present only when asked for.

## In practice at Technik

Run the assistant's candidate behaviours through the split:

| Behaviour | Where it goes | Why |
|---|---|---|
| Look up work order status | **Tool** | One action, one shape of answer |
| Draft a QN write-up | **Skill** | All four criteria: a template, a procedure from `SOP70000101`, its own format, needed a few times a week |
| Cite the document number and revision | **Instructions** | Needed on every answer; one sentence |
| Ask which measure is meant when "how long" is ambiguous | **Instructions** | A rule, needed whenever the question arises ({{topic:tooldesc}}) |
| Check a work order number's format before using it | **Tool input contract** | On the standard harness this would be a topic; here there are none ({{topic:chooseharness}}) |
| Explain what `SWI70000318` says about porosity | **Knowledge** | Retrieval, not procedure ({{topic:triage}}) |

Two rows are worth arguing with.

**Why is the write-up not just instructions?** It could be: a long `<output_format>` section describing
the QN layout. But it would be re-sent on the hundreds of turns that are about status and lead time, it
would need the template pasted inline, and the procedure from `SOP70000101` would be competing for attention
with the rules every answer needs. Three of the four criteria hold strongly; one would be enough.

**Why is the citation rule not a skill?** Because a skill only applies when its description matches. A rule
that must hold on every answer cannot depend on whether this particular request looked like a citation
request. It belongs where it is always read.

## Design guidance

- **Ask the four questions in order** before creating any skill. If none is a clear yes, write a sentence
  in the instructions instead.
- **Keep rules that apply everywhere in the instructions.** A skill is conditional by design.
- **Let skills call tools; never make a tool carry a procedure.** Each owns one thing.
- **Keep one owner per behaviour.** The same procedure in a skill and in the instructions will drift, and
  nobody can say afterwards which version the agent followed.
- **On the GitHub Copilot harness, stop reaching for topics.** Ask what the topic was for, and put that in a
  tool's inputs, a workflow or a rule.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A rule is followed on some answers but not others | It was made a skill, so it applies only when the description matches | Move it to the instructions |
| The instructions are long and half-followed | Procedures and templates live in them | Move each occasional procedure into a skill |
| A skill generates its own queries | There is no tool for the data it needs | Add the tool; have the skill call it |
| A skill and the instructions both describe the write-up | Two owners | Keep the procedure in the skill and delete it from the instructions |
| The design calls for a topic and there is no Topics area | The agent is on the GitHub Copilot harness | Move the need into a tool's inputs, a workflow or a rule |

## Key terms

**Tool**: one action the agent can call, chosen by its description.

**Skill**: a written procedure the agent follows when its description matches, calling tools as it goes.

**Topic**: a designed conversation path on the standard harness.

**Earns-a-skill test**: bundled material, a fixed procedure, an output with its own conventions, or occasional
need. If none applies, it belongs in the instructions.
