## What this module is for

You have met models, prompts and assistants. An agent is what you get when you wrap a model in a
loop that can **decide what to do next** and **act** — call a system, run an automation, hand over to
a person — within limits you set.

This module is the last one before you build. It covers what an agent is, how it decides, what runs
it, and where a human has to stay in the loop. It also contains the decision that shapes everything
afterwards: **which harness**, chosen once, at creation, permanently.

> [!IMPORTANT]
> Read [Choosing a Harness](chooseharness.html) before you create your first agent in B5. The
> harness decides whether an agent can have topics, whether it can have skills, and how it
> orchestrates. It cannot be changed afterwards, and in this course it comes due twice: B5 chooses
> the standard harness for the Technik assistant, and [B8](../B8/index.html) pays for it.

## Before you start

Nothing beyond [B1](../B1/index.html). B2 and B3 help but nothing here depends on them.

About 70 minutes for the lessons and 30 for the exercise. No environment needed — this module is
concepts and one mapping exercise you do on paper.

## What you will be able to do

By the end of this module you should be able to:

- say what distinguishes an agent from a chatbot and from a workflow, without reaching for
  marketing words;
- explain the orchestration loop, and why names and descriptions are the thing that makes it work;
- say what a harness is and why the same model behaves differently in two of them;
- choose a harness for a given job and defend the choice, knowing what it forecloses;
- identify where a human must stay in the loop, and design the confirmation rather than bolting it
  on;
- take a set of business capabilities and map each one onto knowledge, a tool, a topic or a flow.

## The thread through this module

The Technik Production Assistant has seven capability areas, listed in the
[scenario](../scenario/index.html). They look similar from a distance — they are all "answer
questions about manufacturing" — and they are built from four completely different mechanisms.

The exercise is that mapping. Doing it on paper, before B5, is the difference between building an
assistant and assembling one feature at a time until it stops working.

## Self-check

<details>
<summary>1. What actually distinguishes an agent from a well-written chatbot?</summary>

The loop, and the ability to act. A chatbot follows a path someone drew: the designer decided, in
advance, what happens after each thing the user might say. An agent is given instructions, knowledge
and tools, and **decides its own next step** each turn — which knowledge to search, which tool to
call, whether to ask a question or answer. Both can be useful; the agent is the one that handles
requests nobody anticipated, and the one whose behaviour you therefore cannot fully enumerate in
advance. That trade — coverage for predictability — is the whole design conversation.
</details>

<details>
<summary>2. Why do tool and knowledge descriptions matter so much more in an agent than in a workflow?</summary>

Because in a workflow *you* decided what runs; in an agent the orchestrator decides, and the only
thing it has to decide with is the names and descriptions you wrote. A tool called `Run query`
described as "runs a query" is unroutable — the orchestrator has nothing to match a user's words
against. This is why B7 spends most of a lab on writing three pieces of text, and why "the agent
doesn't use my tool" is nearly always a writing problem rather than a configuration one.
</details>

<details>
<summary>3. Two teams use the same model and get very different behaviour. Give three reasons that are not the model.</summary>

The **harness** — what it sends, when it calls the model, how it reads the reply, which tools it may
run. The **context** — instructions, retrieved passages, tool results, history; the model only ever
sees what it is given ([B1](../B1/context.html)). And the **tools and their descriptions** — an agent
that can reach a database and one that cannot are different systems regardless of the model inside
them. "Which model?" is usually the third or fourth most useful question about an agent's behaviour.
</details>

<details>
<summary>4. An autonomous agent processes supplier certificates overnight. What changes compared with the same work done conversationally?</summary>

Nobody is watching. So: the trigger has to be right, because nothing will notice a spurious run; the
instructions have to be tighter, because nobody will rephrase a misunderstood request; failures need
somewhere to go, because there is no user to see an error; and anything irreversible needs an
approval step, because "the user would have noticed" is no longer true. The work is the same; the
supervision is the thing that disappeared, and it has to be rebuilt as design.
</details>

<details>
<summary>5. Where would you put a human in the loop for Technik's document revision flow, and why there?</summary>

Between the draft and the release. Drafting a revision is judgement the agent can do and a human can
check cheaply; releasing it changes what the shop floor works to, and is expensive to undo. The
general rule is to put the human at the last point where reversing costs little — not at the start,
where they rubber-stamp an empty request, and not at the end, where they are approving something
already in effect. B9 builds exactly that approval.
</details>
