## What this module is for

Everything later in this program — prompts, agents, knowledge, tools, evaluation — is built on a
handful of ideas about how a large language model actually behaves. You do not need the
mathematics. You do need to be able to answer, about any agent you build:

- What did the model see when it produced this?
- Why did it answer differently the second time?
- Why did it invent that part number, and what stops it happening again?
- What is this costing, and what happens when the conversation gets long?

Engineers who skip this module can still build an agent. They cannot debug one.

## Before you start

Nothing. This is the first technical module in the Beginner track.
[B0 Getting Oriented](../../beginner.html#B0) is worth ten minutes first, but nothing here depends
on it.

You will need about 90 minutes for the lessons and 30 minutes for the exercise. No Copilot Studio
environment and no Snowflake access are needed — this module is concepts and one paper exercise.

## What you will be able to do

By the end of this module you should be able to:

- explain, to a colleague who has not used AI, what a language model is doing when it answers;
- estimate the token cost of a document before you put it in a prompt, and say what that costs in
  speed and money;
- describe what is in the context window at any point in a conversation, and what gets dropped
  first when it fills;
- predict whether a change to temperature will help or hurt a given task;
- tell the difference between a problem that needs better prompting, one that needs grounding, and
  the rare one that needs fine-tuning;
- recognise a hallucination in an answer about your own domain, and name the mechanism that
  produced it.

## The thread through this module

Every example uses Technik, the fictional subsea equipment manufacturer the whole course is built
around. See the [scenario](../scenario/index.html) for the company, its systems and its people.

In this module you are not building anything yet. You are looking at the raw material the Technik
Production Assistant will be made of: a work instruction that has to fit in a prompt, a quality
notification that has to be summarised, a part number the model must not invent.

## Self-check

Answer these before moving on. Each answer explains the reasoning, not just the verdict.

<details>
<summary>1. You paste a 12-page work instruction into a prompt and ask for a summary. Someone says "that will use about 3,000 tokens". Are they in the right range?</summary>

Roughly, yes. Twelve pages of prose is perhaps 6,000 words, and in English a token averages about
three quarters of a word, so 6,000 words is around 8,000 tokens. "3,000" is low by more than a
factor of two — close enough to be a plausible guess, far enough off to matter if you are sizing a
context budget. The lesson is not the arithmetic but the habit: **estimate before you paste**, and
remember that tables, part numbers like `P7000001042` and anything non-English cost more tokens per
character than plain prose.
</details>

<details>
<summary>2. The same prompt, run twice against the same model, returns two different answers. Is the model broken?</summary>

No. Generation samples from a probability distribution over the next token, so unless sampling is
effectively switched off the output varies run to run. This is why "I tested it and it worked" is
not evidence that an agent works, and why B13 spends a whole module on evaluation. It is also why
low temperature is the right default for anything that has to be repeatable, such as reading a work
order status back to a planner.
</details>

<details>
<summary>3. An agent is asked about work order <code>100004521</code> and answers confidently with a status that is wrong. What are the three candidate causes, in the order you should check them?</summary>

First, **it never saw the data** — no tool was called, or the tool returned nothing, and the model
filled the gap with something plausible. Second, **it saw the wrong data** — the tool ran, but
against the wrong table, the wrong filter or a stale copy. Third, and least likely, **it saw the
right data and misread it** — usually a formatting or units problem, or an instruction that told it
to summarise when it should have quoted. Reaching for "the model is bad" before checking the first
two is the most common waste of time in agent debugging. The activity map in Copilot Studio (B5)
exists to answer this question.
</details>

<details>
<summary>4. Your agent gives good answers about cladding but occasionally invents a document number. Which fixes the problem: a better model, a lower temperature, or grounding?</summary>

Grounding. A better model invents less often but still invents; a lower temperature makes it invent
the *same* thing more consistently. Only supplying the real document list in context, and
instructing the model to answer from it and cite what it used, changes the mechanism. Temperature
and model choice are worth tuning afterwards — they are not the cause.
</details>

<details>
<summary>5. When is fine-tuning the right answer to a business problem?</summary>

Rarely, and almost never as a first move. Fine-tuning teaches a model a *style*, a *format* or a
narrow *classification* — not facts, which change. If Technik wants quality notifications classified
into its own defect taxonomy, thousands of times a day, with labelled history to learn from, that is
a genuine fine-tuning candidate (and A11 works through exactly that decision). If Technik wants
answers about its current documents, fine-tuning is the wrong tool: the documents change, and a
fine-tuned model cannot cite.
</details>
