## TL;DR

Copilot Studio is Microsoft's low-code platform for building agents. The areas you will use are the
build surface (instructions, knowledge, tools, skills), topics, the test pane, evaluation, publish
and channels, and analytics. Before any of that matters you make one irreversible choice: **the
harness**. Learn the map first, and make that choice deliberately.

## Why it matters

Copilot Studio changes often, and screenshots age badly. What does not change is the shape: an agent
is instructions plus knowledge plus tools plus, on some harnesses, skills and topics; you test it;
you publish it to channels; you watch how it is used. Knowing the shape means a renamed menu is an
inconvenience rather than a blocker.

The harness matters more than anything else on the page because it is the one decision you cannot
revisit.

## How it works

<!-- volatile verified=2026-09 -->
Copilot Studio's navigation, the names of its areas, and which areas appear for which harness all
change between releases — this part of the product has been reorganised more than once. Use the map
below for what each area *is for*, and the linked documentation for where it currently lives.
<!-- /volatile -->

| Area | What it is for |
|---|---|
| **Overview / build** | The agent's identity, instructions, knowledge, tools and skills. Where most authoring happens |
| **Topics** | Designed conversation paths, node by node. **Standard harness only** |
| **Test / preview** | Chat with the draft agent and see what it did. Where debugging happens |
| **Evaluate** | Run a fixed set of questions and review the results (B13) |
| **Publish and channels** | Make the agent available in Teams, a website, Microsoft 365 Copilot (B12) |
| **Analytics / monitor** | Sessions, engagement, resolution, which knowledge and tools were used, errors (B12) |
| **Settings** | Generative AI settings, authentication, security |

### The harness, first

Copilot Studio offers three harnesses, covered in [B4](../B4/index.html):

| Harness | Has | Does not have |
|---|---|---|
| **Standard** | Topics, tools, agent flows, knowledge | Skills |
| **GitHub Copilot** | Skills, memory, files, tools, knowledge | Topics |
| **Copilot chat** | Extends Microsoft 365 Copilot Chat with enterprise knowledge | — |

You choose during creation. **You cannot change it afterwards.** Changing your mind means creating a
new agent and rebuilding everything in it, then re-publishing and asking users to move.

So before you click create, answer one question: **does this agent need a conversation path that
must run exactly as drawn?** If yes, it needs topics, and that means the standard harness. If no,
and it needs to hold written procedures, the GitHub Copilot harness. If you genuinely do not know,
the answer is usually the standard harness, because a scripted exchange somewhere is more common
than you expect.

### Solutions, from day one

An agent created outside a solution is an agent that cannot cleanly move to another environment.
Create it **inside a custom solution** from the start — B12 covers why in full, and retrofitting is
real work. This is the single cheapest habit in the whole course: it costs one extra step now.

## In practice at Technik

The Technik Production Assistant is built on the **standard harness**, and the reasoning is worth
recording because someone will ask:

- Ana's work order question needs a scripted intake — ask for the number, confirm it, then act. That
  is a topic.
- The assistant is the front door for four personas in Teams. It is the agent people learn to go to,
  which means it should be stable, not rebuilt.
- The one thing the standard harness cannot do — hold a skill — is handled in B8 by putting the
  skill on a second agent and delegating to it.

That trade is fine. What would not be fine is discovering it in B8 without having chosen it.

> [!TIP]
> Write the harness reasoning into the agent's own description, not only into a document. In six
> months the person asking "why can't this one have skills?" will be looking at the agent, not at
> your notes.

## Design guidance

- **Decide the harness before you create anything**, and write down why.
- **Create inside a custom solution**, always.
- **Name the agent as users will refer to it.** It appears in Teams, in analytics and in sharing
  dialogs.
- **Learn the areas, not the layout.** The layout will change.
- **Do not add tools before the basic answers are good.** Every addition makes the next problem
  harder to isolate.
- **Open the test pane early and keep it open.** It is the only place that tells you what happened.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| There is no Topics area | The agent is on the GitHub Copilot harness | Topics are standard-harness only. Rebuild, or use a different pattern |
| There is no Skills area | The agent is on the standard harness | [B8](../B8/reuse.html). Skills are not coming to it |
| The agent cannot be moved to test or production | It was created outside a solution | Create it in a solution from the start; moving it later is real work |
| A menu is not where the documentation says | The product changed | Check the current docs. Learn the shape, not the path |
| Two people built two agents for the same job | No naming or ownership convention | Agree names and owners before building, not after |

## Key terms

**Harness** — the runtime between your agent and the model. Chosen at creation, not changeable (B4).

**Solution** — the container that lets an agent and its dependencies move between environments (B12).

**Topic** — a designed conversation path. Standard harness only.

**Test pane** — the chat-with-your-draft surface, and the activity map that shows what it did.

**Channel** — where users meet the agent: Teams, a website, Microsoft 365 Copilot (B12).
