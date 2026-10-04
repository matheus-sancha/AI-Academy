## TL;DR

You create an agent by describing it in plain language, and Copilot Studio drafts a first configuration
from what you typed. Then comes the part that matters: **rewrite what it drafted**, add one knowledge
source, test in Preview, and add tools only once the plain answers are right. Two things are fixed at the
moment of creation and cannot be changed afterwards — the **harness**, and on the standard harness the
**primary language** — so those are decided before you type anything.

## Why it matters

Creating an agent takes two minutes, and that is the problem. The two minutes produce something that
answers plausibly, and it is tempting to treat plausible as done and start bolting on tools. Agents built
that way are the ones that misbehave three modules later, because nobody went back and made the
foundation specific — and by then there are six components that could be responsible.

The order in this lesson is deliberate: identity, then instructions, then **one** source, then a test.
Each step is cheap to debug on its own and expensive to debug together.

## How it works

### Before you type: where, and on what

<!-- volatile verified=2026-09 -->
The home page shows an **environment picker**, filtered to environments where you are allowed to create.
If the one you expect is missing, it is inactive or you lack permission there — an administrator question,
not a bug ({{topic:envs}}). The home page's cards create agents on the **GitHub Copilot harness**; the
standard harness is under **Other ways to build**, or reached by turning off **New experience**.
<!-- /volatile -->

Both choices stick. An agent cannot be moved to the other harness ({{topic:chooseharness}}), and an agent
created in a scratch environment has to be moved through a solution to get anywhere else
({{topic:solutions}}). Decide both on purpose.

### Describing it

On either harness you can start by describing what you want. The two harnesses do different things with
the description:

<!-- volatile verified=2026-09 -->
| | GitHub Copilot harness | Standard harness |
|---|---|---|
| **What you type into** | The text box on the home page (preview) | The description box on the home or Agents page, up to 1,024 characters |
| **What you get** | Copilot Studio suggests, builds and guides you through the agent — and can propose workflows alongside it | A drafted name, description and instructions, plus *suggested* triggers, channels, knowledge and tools |
| **Also fixed at creation** | The harness | The harness and the primary language (its region can change; secondary languages can be added) |
<!-- /volatile -->

On the standard harness the suggestions are offers, not configuration: you add or dismiss each one, and
they do not persist beyond the current session. Whatever the harness, you can also start blank.

<!-- volatile verified=2026-09 -->
The fields you will edit have hard limits on the standard harness: a name of up to 42 characters with no
angle brackets, a description of up to 1,024, and instructions of up to 8,000.
<!-- /volatile -->

### What to put in the description

The description is the raw material for the drafted instructions, so it is worth more than a sentence.
Say:

- **who it is for** — roles, not a department;
- **what it covers** — the actual questions;
- **what it must not do** — and what to say instead;
- **how it should sound**.

A vague description produces vague instructions, and vague instructions produce an agent that answers
everything with equal confidence.

### What to fix in the draft

The draft will be polite, generic and unbounded, because it was written knowing nothing about your work.
Three things to change every time:

1. **Scope.** Add what the agent does *not* cover, and where to send people instead.
2. **Grounding posture.** Whether it may answer from general knowledge or only from its sources. For an
   internal assistant over company data it is *only from its sources*, and that line belongs in the
   instructions before there are any sources ({{topic:genai}}).
3. **Tone.** *Helpful and friendly* is the default and wrong for most engineering tools.

Instructions have a format of their own, which the next module teaches ({{module:writing-instructions}}).
For now the aim is a draft that is specific, not one that is finished.

### Then stop

Add **one** knowledge source. Ask five real questions in Preview, starting a new chat before you do
({{topic:conversation}}). Read the activity trace. Only then add a tool. An agent with one source and five
tested questions is a baseline; an agent with four sources and three tools on day one is a debugging
problem with no baseline.

## In practice at Technik

The description that starts the Technik Production Assistant:

```
An internal assistant for Technik manufacturing and engineering staff: production planners,
quality engineers, manufacturing engineers and supervisors. It answers questions about work orders,
manufacturing operations, quality notifications, controlled documents and Teamcenter revisions.

It answers only from the knowledge and tools it has been given, and says plainly when it cannot
find something rather than guessing. It never invents a part, drawing, work order or QN number.

It is concise and factual and writes in British English. It is a tool people use dozens of times
a day, so it does not greet, apologise or use exclamation marks.

It does not answer questions about pay, HR policy or anything outside manufacturing and
engineering. When asked, it says so and points to the HR portal.
```

Four things earn their place:

- **The roles are named.** *Manufacturing staff* would have produced instructions written for nobody.
- **The grounding rule comes before the knowledge.** Once work order data arrives
  ({{module:tools-connectors-mcp}}) it is load-bearing; written now, it is never retrofitted.
- **The tone is specific and negative.** *Does not greet or apologise* changes output; *professional*
  does not.
- **The boundary has an action.** Not just *does not cover HR*, but what to say instead.

The first source is `SOP70000101` *Quality Notification Handling*: one document, with questions whose
answers you can check by reading it. Five questions against it, each in a new chat, tell you whether the
grounding rule holds before a single table is connected.

> [!TIP]
> Keep the description you typed, somewhere outside the agent. When behaviour drifts three modules from
> now, the fastest way to see what changed is to compare today's instructions with what you originally
> meant.

## Design guidance

- **Decide the environment and the harness before creating.** Neither is an edit later.
- **Write the description as a briefing for a new starter**, including what not to do.
- **Treat the draft as raw material.** It is generic by construction.
- **Put the grounding rule in on day one.**
- **One source, five questions, a new chat each time.** Then add the next thing.
- **Name the agent as users will say it.** The name appears in Teams, in sharing and in analytics.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent answers everything, including what it should refuse | No boundary in the instructions | State what it does not cover and what to say instead |
| It sounds like a marketing chatbot | The drafted tone was never changed | Be specific and negative about tone |
| It answers company questions from general knowledge | No grounding rule | Add it now, before there is knowledge to ground in |
| It worked, then four additions later nothing works | No tested baseline | Remove back to one source; add one thing at a time |
| The environment you need is not in the picker | Inactive, or you cannot create there | Ask an administrator ({{topic:tenantvaries}}) |
| The suggested knowledge and tools vanished | Standard-harness suggestions last only for the session | Add the ones you want before leaving |
| The agent is on the wrong harness or in the wrong language | Chosen by default | Neither can be changed. Recreate it |

## Key terms

**Agent description** — what you type at creation; the raw material for the drafted instructions.

**Drafted instructions** — what Copilot Studio generates from the description. A starting point.

**Grounding posture** — whether the agent may answer from general knowledge or only from its sources.

**Environment** — the container an agent is created in, and where its data and connections live
({{topic:envs}}).

**Baseline** — a small set of questions you have tested and know the answers to. What makes the next
change debuggable.
