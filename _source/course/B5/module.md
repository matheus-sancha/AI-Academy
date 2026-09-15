## What this module is for

This is where you build something. B1 to B4 were ideas; from here on there is an agent in front of
you, and every module adds to the same one.

The module covers the parts of Copilot Studio you touch on every agent you will ever build:
instructions, the model, topics, variables, the generative AI settings, and the test pane. None of
it is difficult. The difficulty is that two decisions made in the first ten minutes — **which
harness** and **what the instructions say** — shape everything afterwards, and one of them cannot be
undone.

> [!IMPORTANT]
> The harness you choose when you create an agent **cannot be changed later**. It decides whether
> the agent can have topics, whether it can have skills, and how it orchestrates. The Technik
> Production Assistant is built on the **standard harness** in this module, deliberately, and
> [B8](../B8/index.html) is where that decision comes due. Read
> [Copilot Studio Tour](tour.html) before you create anything.

## Before you start

[B4 Agent Fundamentals](../../beginner.html#B4), conceptually — this module assumes you know what
an agent, an orchestrator and a harness are.

You will need:

- your Power Platform developer environment and Copilot Studio;
- about 80 minutes for the lessons and 75 for the lab;
- a small number of Copilot Credits.

You do **not** need Snowflake for this module. The agent gets its first data in B6.

## What you will be able to do

By the end of this module you should be able to:

- find your way around Copilot Studio and say what each area is for;
- create an agent, choose its harness deliberately, and say why;
- write agent instructions that are specific enough to change behaviour and short enough not to
  crowd out the answer;
- choose a primary model, and know to re-test after changing it;
- build a topic with trigger phrases, questions, conditions and variables;
- read the generative AI settings and change the ones that matter;
- use the test pane and the activity map to find out *why* an agent answered as it did, rather than
  guessing.

## The thread through this module

You create the Technik Production Assistant, and it answers its first question — badly, and for
instructive reasons.

Ana, a production planner, asks about work order `100004521`. The agent has no data, no tools and no
knowledge, so all it can honestly do is take the work order number, confirm it back, and say it
cannot look anything up yet. That is what you build: a scripted, predictable exchange that is
useless on its own and becomes the front end of a real capability in B6 and B7.

Building the useless version first is not busywork. It is how you see the difference between what a
topic does and what knowledge and tools do, at the point where the difference is still visible.

## Self-check

<details>
<summary>1. Why does this module build an agent on the standard harness, when the GitHub Copilot harness is newer and can do more?</summary>

Because the assistant needs **topics**, and topics are standard-harness only. The *Work order
status* topic in this lab is a scripted exchange with a fixed path, which is exactly what topics are
for. The cost is real and arrives in B8: standard-harness agents cannot have skills, so the write-up
skill has to live on a second agent. That is a defensible trade, and the point of the lesson is that
it is a *trade*, chosen knowingly, and recorded — not a default you discover later.
</details>

<details>
<summary>2. Instructions and a topic can both make an agent ask for a work order number. What is the difference?</summary>

A topic **guarantees** the exchange: you drew the path, so the question is asked, the answer is
stored in a variable, and the next node runs. Instructions **influence** it: the model usually
complies, and occasionally does something reasonable but different. Use a topic when the steps must
be identical every time — a compliance check, a structured intake, a confirmation before an action.
Use instructions for the behaviour you want everywhere, in every conversation, regardless of path.
</details>

<details>
<summary>3. Your agent gives a wrong answer. Why is the activity map the first place to look, not the instructions?</summary>

Because the instructions are the *last* thing you can usefully change and the first thing everyone
reaches for. The activity map tells you what actually happened: which topic triggered, which
knowledge was searched, which tool ran with which inputs, what came back. That distinguishes "it
never had the data" from "it had the data and misread it" — two problems with completely different
fixes, from [B1](../B1/hallucination.html). Rewriting instructions before you know which one you
have is guessing.
</details>

<details>
<summary>4. You change the primary model and the agent still passes your manual spot-checks. Is it safe to ship?</summary>

No, and not because the model is worse. Behaviour shifts when the model changes even with identical
instructions — different phrasing, different tool-calling tendencies, different willingness to
abstain. Manual spot-checks confirm the cases you happened to think of, which are the cases you
already knew worked. This is the whole argument of B13: a fixed set of questions, run before and
after, is the only thing that makes "still fine" a statement rather than an impression.
</details>

<details>
<summary>5. What is a global variable for, and what is the trap?</summary>

It holds a value across topics for the whole conversation — a work order number the user gave once,
a plant they said they were working in. The trap is that it is **conversation-scoped state in a
system whose other half is a stateless model**: the variable persists, but nothing guarantees the
model *uses* it, and nothing clears it when the user moves on to a different work order. Set them
deliberately, clear them deliberately, and never assume a value is still meaningful ten turns later
just because it is still set.
</details>
