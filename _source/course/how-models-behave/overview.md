## What this module is for

Basic explained what a model is doing when it answers. This module is about the consequences you have
to hold as a builder: what a request costs, how long it takes, which settings change the answer, and
which model to put behind the agent. You do not need the mathematics. You do need to be able to
answer, about any agent you build:

- What is this costing, and what happens to that as the conversation gets long?
- Why did it answer differently the second time, and which setting decides that?
- Which of these models should be behind this agent, and what did choosing it commit me to?
- Is this a problem for better instructions, better grounding, or — very rarely — fine-tuning?

Engineers who skip this module can still build an agent. They cannot debug one.

## Before you start

{{module:how-copilot-works}} in Basic, which this module builds directly on: what a model is, what it
sees, and why it invents things are not repeated here. {{module:getting-oriented}} is worth ten
minutes first, but nothing here depends on it.

Allow about 90 minutes. Nothing here needs a Copilot Studio environment or Snowflake access; the
module is concepts, with worked examples from Technik.

## What you will be able to do

By the end of this module you should be able to:

- estimate the token cost of a document before you put it in a prompt, and say what that costs in
  speed and money;
- read an agent's per-turn cost and say which part of it is the agent's own configuration rather than
  the question;
- predict whether a change to temperature will help or hurt a given task, and recognise the tasks
  where it is the wrong dial entirely;
- choose a primary model for an agent and defend the choice on quality, latency and cost together;
- tell the difference between a problem that needs better instructions, one that needs grounding, and
  the rare one that needs fine-tuning;
- say what a multimodal model buys you over a purpose-built extraction pipeline, and when it does not.

## The thread through this module

Every example uses Technik, the fictional manufacturer the whole course is built around. See the
[scenario](../scenario/index.html) for the company, its systems, documents and data.

You are not building anything yet. You are sizing the raw material the Technik Production Assistant
will be made of: counting the tokens in a work instruction before it goes anywhere near a prompt, and
watching the same quality-notification summary come back differently at different temperatures.

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
not evidence that an agent works, and why {{module:testing-and-evaluation}} spends a whole module on
it. It is also why low temperature is the right default for anything that has to be repeatable, such
as reading a work order status back to a planner.
</details>

<details>
<summary>3. When is fine-tuning the right answer to a business problem?</summary>

Rarely, and almost never as a first move. Fine-tuning teaches a model a *style*, a *format* or a
narrow *classification* — not facts, which change. If Technik wants quality notifications classified
into its own defect taxonomy, thousands of times a day, with labelled history to learn from, that is
a genuine fine-tuning candidate, and {{module:models-and-fine-tuning}} works through exactly that
decision. If Technik wants answers about its current documents, fine-tuning is the wrong tool: the
documents change, and a fine-tuned model cannot cite.
</details>
