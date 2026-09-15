## TL;DR

Describe the agent in plain language and Copilot Studio drafts a name, a description and
instructions for you. Then do the part that matters: **refine what it drafted**, add one knowledge
source, test, and only then add anything else. The drafted instructions are a starting point, not a
result — they are generic because they were written without knowing anything about your work.

## Why it matters

Creating an agent takes two minutes, which is the problem. The two minutes produce something that
answers plausibly, and it is tempting to treat that as done and start adding tools. Agents built
that way are the ones that behave unpredictably three modules later, because nobody ever went back
and made the foundation specific.

The order below is deliberate: identity, then instructions, then **one** source, then test. Each step
is cheap to debug alone and expensive to debug together.

## How it works

<!-- volatile verified=2026-09 -->
Copilot Studio's creation flow asks you to describe the agent, drafts an identity and instructions,
and lets you refine them before or after creating. Where the harness choice appears in that flow
changes between releases — find it before you finish creating, because it cannot be changed
afterwards. Follow the linked documentation for the current steps.
<!-- /volatile -->

### The description you type

The description you give during creation becomes the draft instructions, so it is worth more than a
sentence. Include:

- **who it is for** — the people, not the department;
- **what it covers** — the actual questions;
- **what it must not do** — the boundary;
- **how it should sound** — tone and language.

A vague description produces vague instructions, which produce an agent that answers everything with
equal confidence.

### What to fix in the draft

The draft will usually be polite, generic and unbounded. Three things to change every time:

1. **Scope.** Add what the agent does *not* cover, and what it should do when asked — say so, and
   suggest where to go instead.
2. **Grounding posture.** Whether it may answer from general knowledge or only from its sources. For
   an internal assistant over company data, the answer is only from its sources, and it belongs in
   the instructions from day one even before there are any.
3. **Tone.** "Helpful and friendly" is the default and is wrong for most engineering tools. Concise
   and factual is usually what people want.

### Then stop

Add **one** knowledge source, ask five real questions, read the activity map. Resist adding tools.
An agent with one source and five tested questions is a foundation; an agent with four sources and
three tools on day one is a debugging problem with no baseline.

## In practice at Technik

The description that creates the Technik Production Assistant:

```
An internal assistant for Technik manufacturing and engineering staff: production planners,
quality engineers, manufacturing engineers and supervisors. It answers questions about work orders,
manufacturing operations, quality notifications, controlled documents and Teamcenter revisions.

It answers only from the knowledge and tools it has been given, and says plainly when it cannot
find something rather than guessing. It never invents a part number, drawing number, work order
number or measurement.

It is concise and factual, writes in British English, and does not use exclamation marks or
enthusiasm. It is a tool people use dozens of times a day.

It does not answer questions about pay, HR policy, or anything outside manufacturing and
engineering. When asked, it says so and suggests the intranet.
```

Four things in there earn their place:

- **The personas are named.** "Manufacturing staff" would have produced instructions written for
  nobody in particular.
- **The grounding rule is present before there is any knowledge.** By B6 it is load-bearing; putting
  it in now means it is never retrofitted.
- **The tone is specific and negative.** "Does not use exclamation marks" changes output in a way
  "professional" does not.
- **The boundary has an action.** Not just "does not cover HR" but what to say instead.

> [!TIP]
> Keep the description you typed. When the agent behaves oddly in three modules' time, the first
> useful question is "is this in the instructions, and does it still say what I meant?" — and the
> original description is the fastest way to see what has drifted.

## Design guidance

- **Write the description as if briefing a new starter**, including what not to do.
- **Choose the harness before you finish creating.** It is irreversible ([Copilot Studio Tour](tour.html)).
- **Create inside a custom solution.**
- **Refine the drafted instructions.** They are generic by construction.
- **One knowledge source, five questions, read the activity map.** Then continue.
- **Name it as users will say it.** The name appears in Teams and in sharing.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent answers everything, including things it should refuse | No boundary in the instructions | State what it does not cover and what to say instead |
| It sounds like a marketing chatbot | The drafted tone was never changed | Be specific and negative: concise, factual, no enthusiasm |
| It answers company questions from general knowledge | No grounding rule | Add it now, before there is knowledge to ground in |
| It worked, then four additions later nothing works | No tested baseline | One source, five questions, then add |
| The agent cannot be deployed | Created outside a solution | Create in a solution from the start |
| The wrong harness | Chosen by default, not decided | It cannot be changed. Rebuild |

## Key terms

**Agent description** — what you type at creation; becomes the draft instructions and is shown to
users in some channels.

**Drafted instructions** — what Copilot Studio generates from your description. A starting point.

**Grounding posture** — whether the agent may answer from general knowledge or only from its sources
([B6](../B6/rag.html)).

**Baseline** — a small set of questions you have tested and know the answers to. What makes the next
change debuggable.
