## TL;DR

Models trade four things against each other: **quality**, **speed**, **cost** and **reasoning depth**.
There is no best model, only a best fit for a task, and the fit changes as providers ship new
versions. Copilot Studio lets you pick the primary model for an agent. Pick a sensible default,
build the thing, measure it against a fixed set of questions, and only then decide whether a
different model is worth the difference — because "it felt better" is not a finding.

## Why it matters

Model choice is the most visible decision and rarely the most consequential one. Teams spend weeks on
it and minutes on the query that returns 300 rows, when the second is what actually made the agent
slow, expensive and wrong. Worse, a model change invalidates every test you ran before it: behaviour
shifts even when your instructions do not.

Getting this in proportion is the point of the lesson. Choose deliberately, change rarely, and
re-measure whenever you do.

## How it works

Four axes, and they genuinely trade off.

**Quality** — how well the model follows complex instructions, handles nuance and stays consistent
over a long context. Bigger models are generally better; the gap on simple tasks is small and on hard
ones large.

**Speed** — how fast the answer arrives. Smaller models are faster. For an assistant people use
dozens of times a day, latency is a feature.

**Cost** — charged per token, input and output separately. A model several times the price only
matters at volume, but agents are volume.

**Reasoning depth** — *reasoning* models generate internal thinking tokens before answering. They are
markedly better at multi-step problems and markedly slower and more expensive at everything else.
Using one for "what is the status of work order 100004521" is paying for deliberation about a lookup.

A useful way to choose:

| The task is | Choose |
|---|---|
| A lookup, or reading one row back to a user | The fastest model that gets it right |
| Summarising or drafting from supplied text | A mid-range general model |
| Deciding between many tools, or multi-step work | A stronger general model; consider reasoning |
| Genuinely hard analysis over messy input | A reasoning model, knowingly, for that step only |
| Classification at high volume | The smallest model that passes your evaluation set |

<!-- volatile verified=2026-09 -->
Copilot Studio exposes the model choice when you create an agent and in its settings afterwards, and
the list spans providers — OpenAI GPT models and Anthropic Claude models among them. Which models
appear depends on your tenant, your region and your harness, and the list changes regularly. Rather
than learning a list that will be out of date, learn where the setting lives and check the linked
documentation for what is currently offered and what each one costs in Copilot Credits.
<!-- /volatile -->

Two constraints are easy to miss and expensive to discover late. Availability varies by **region and
tenant**, so a model a colleague used may simply not be there for you. And the **harness** you choose
when you create the agent shapes what is available and cannot be changed afterwards (B4).

## In practice at Technik

The Technik Production Assistant does seven quite different jobs. If you were free to choose per
capability:

| Capability | Sensible choice | Why |
|---|---|---|
| Work order information | Fast general model | A lookup, read back plainly. Latency is what users notice |
| Work order efficiency | Fast general model | Snowflake does the arithmetic; the model formats a result |
| Lead time | Fast general model | As above |
| Quality notifications: find and summarise | Mid-range general model | Summarising free text well, in a fixed format |
| Engineering questions from documents | Mid-range general model | Retrieval does the finding; the model must read carefully and cite |
| Teamcenter revision information | Fast general model | A tool call and a careful reading of a few rows |
| Document revision drafting | Stronger model | Long output, a template to honour, an ECN to cross-check |

In Copilot Studio's standard harness the agent has one primary model, so in practice you pick for
the hardest thing it does routinely and accept that lookups are slightly over-served. That is a
reasonable trade — until the day drafting becomes a large share of usage, at which point splitting
into connected agents (B7) lets each half have its own.

> [!TIP]
> Before changing model, write down what you expect to improve and how you will know. Then run your
> evaluation set on both. Half the time the expected improvement does not appear, and finding that
> out in ten minutes is worth far more than the change would have been.

## Design guidance

- **Start with a capable default** and make the agent work. Model choice is not where an agent
  becomes good.
- **Change one thing at a time** and re-run the same questions. B13 is what makes this possible.
- **Do not use a reasoning model as a default.** Use it for the step that needs it.
- **Watch cost per conversation, not per token.** An agent that needs three turns on a cheap model
  can cost more than one turn on an expensive one.
- **Record which model produced which results.** An evaluation run whose model you cannot
  reconstruct is not evidence.
- **Re-check when a provider ships a new version.** Yesterday's right answer may now be the slow,
  expensive one.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent got better or worse after a model change, and nobody can say by how much | No fixed test set | Build one first (B13). Ten to twenty realistic questions is enough to start |
| A colleague's model is not in your list | Region, tenant or harness differences | Check availability for your environment rather than assuming |
| Costs jumped after switching model | Different per-token price, or a reasoning model generating thinking tokens | Compare cost per conversation on the same test set |
| Answers are slower with no quality gain | A reasoning model on routine work | Use it only for the hard step |
| The same instructions behave differently on the new model | Models differ in how they follow instructions | Re-test and adjust instructions per model. There is no portable prompt |
| The harness turns out to be wrong for the job | It is chosen at creation and cannot be changed | Decide the harness deliberately (B4) before you build |

## Key terms

**Primary model** — the model an agent uses by default.

**Reasoning model** — one that generates internal thinking tokens before answering. Better at
multi-step problems, slower and dearer.

**Small language model (SLM)** — a compact model, fast and cheap, good for narrow tasks.

**Harness** — the runtime between your agent and the model. Chosen at creation, not changeable
afterwards (B4).

**Copilot Credits** — the consumption unit Copilot Studio usage is billed in. Different models
consume at different rates (B0).

**Model version** — providers ship updates under new version identifiers. Pin and re-evaluate rather
than following changes silently.
