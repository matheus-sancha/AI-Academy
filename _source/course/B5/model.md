## TL;DR

Each agent has a primary model, and you can change it to trade speed, cost and reasoning ability.
The important part is not the choice but what follows it: **behaviour shifts when the model changes,
even with identical instructions**, so a model change invalidates every test you ran before it.
Choose a sensible default, build, measure, and change models only with an evaluation set to hand.

## Why it matters

Model choice is the most visible knob and rarely the most consequential one — [B1 made that
case](../B1/models.html) in general. What is specific to Copilot Studio is the discipline around
changing it: an agent is a system of instructions, tool descriptions and knowledge tuned against one
model's tendencies, and swapping the model perturbs all of it at once.

Teams that change model casually end up with agents nobody can reason about, because no two
behaviours can be attributed to a single cause.

## How it works

<!-- volatile verified=2026-09 -->
The primary model is set when you create an agent and can be changed in its settings afterwards.
Which models are offered depends on your tenant, your region and your harness, and the list changes
regularly — it spans providers, including OpenAI GPT and Anthropic Claude models. Check the linked
documentation for what is currently available and what each consumes in Copilot Credits, rather than
learning a list.
<!-- /volatile -->

What is stable is how to think about it:

| The agent mostly | Choose |
|---|---|
| Looks things up and reads a few rows back | The fastest model that gets it right |
| Summarises and drafts from supplied text | A mid-range general model |
| Chooses between many tools, or works multi-step | A stronger general model |
| Does genuinely hard analysis over messy input | A reasoning model, knowingly, for that work |

Three things bite in practice.

**One model per agent.** In the standard harness the agent has one primary model, so you choose for
the hardest thing it does routinely and accept that lookups are over-served. When drafting becomes a
large share of usage, that is an argument for splitting into connected agents (B7), not for
compromising.

**Reasoning models are not a free upgrade.** They generate thinking tokens before answering — billed,
timed, invisible. Excellent for a hard decision, pure waste for "what is the status of work order
`100004521`".

**Availability varies.** A model a colleague used may not exist for your tenant or region. Check
before designing around one.

## In practice at Technik

The Technik Production Assistant does seven things of quite different difficulty — the full mapping
is in [B1](../B1/models.html). In the standard harness it gets one model, so:

- the hardest routine work is **choosing between tools and knowledge** once B6 and B7 land, and
  **drafting** once B8 does;
- lookups are the most frequent and most latency-sensitive;
- so a capable general model, not a reasoning model, is the right default.

The sequence that matters is what you do *around* the choice:

1. Build with a sensible default.
2. Get the instructions, knowledge and tools right. This is where the quality is.
3. Build an evaluation set (B13) — ten to twenty real questions with known answers.
4. Only then try a different model, and run the same set on both.

Step 4 without step 3 is an opinion.

> [!WARNING]
> Changing the model invalidates prior testing. Not "might affect" — the same instructions produce
> different phrasing, different willingness to call a tool, and different willingness to say "I could
> not find that". If you change it, re-run everything.

## Design guidance

- **Start with a capable default.** Model choice is not where an agent becomes good.
- **Do not use a reasoning model as a default.** Use it where the work is genuinely hard.
- **Record which model produced which results.** A test run whose model you cannot reconstruct is
  not evidence.
- **Change one thing at a time**, and re-run the whole evaluation set.
- **Compare cost per conversation, not per token.** Three turns on a cheap model can cost more than
  one on a dear one.
- **Check availability for your tenant** before designing around a model.
- **Re-check when a provider ships a new version.** Yesterday's right answer may now be the slow one.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent changed behaviour and nobody knows why | The model was changed without re-testing | Re-run the evaluation set; record the model with results |
| Costs jumped | A different per-token price, or a reasoning model generating thinking tokens | Compare cost per conversation on the same test set |
| Slower with no quality gain | A reasoning model doing routine work | Use the faster model; reserve reasoning for hard steps |
| A model in the documentation is not in your list | Tenant, region or harness | Check availability rather than assuming |
| The same instructions behave differently after a switch | Models differ in how they follow instructions | Re-tune per model. There is no portable prompt |
| "It felt better" is the only evidence | No evaluation set | Build one (B13). Ten questions is enough to start |

## Key terms

**Primary model** — the model the agent uses by default.

**Reasoning model** — generates internal thinking tokens before answering. Better at multi-step work,
slower and dearer.

**Copilot Credits** — the consumption unit Copilot Studio is billed in; models consume at different
rates (B0).

**Evaluation set** — a fixed set of questions with known answers, run before and after a change
(B13).
