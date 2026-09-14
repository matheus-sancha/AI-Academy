## What this module is for

The agent you built in B5 can hold a conversation and follow a script. It cannot answer a single
question about Technik, because it has never seen anything Technik wrote.

This module fixes that. You give the agent documents and data, and it starts answering from them
instead of from whatever the model absorbed during training. That change — from *plausible* to
*grounded and citable* — is the single largest jump in usefulness anywhere in this course, and it is
the whole reason [B1's lesson on hallucination](../B1/hallucination.html) came first.

It is also where most agents quietly go wrong. Knowledge that returns nothing, answers built from the
wrong source, citations that point at the right document and the wrong clause: none of these produce
an error message. They produce a confident answer.

## Before you start

Conceptually you want [B5 Copilot Studio Basics](../../beginner.html#B5), because this module assumes
you can create an agent, write its instructions and read the test pane.

The lab ships its own starter, so you do not need to have finished B5 to do it.

You will need:

- your Power Platform developer environment and Copilot Studio;
- a SharePoint site you can upload two pages to — a personal or team site is fine;
- your Snowflake sandbox, with `ACADEMY_AGENT_<you>` working;
- the Technik documents from `labs/_setup/documents/`, as PDFs;
- about 75 minutes for the lessons and 90 for the lab.

## What you will be able to do

By the end of this module you should be able to:

- explain what retrieval-augmented generation actually does to a request, and what it does not fix;
- choose between an uploaded file, SharePoint, a public website, Dataverse and a connector for a
  given body of knowledge, and say what each costs in freshness and permissions;
- explain the difference between a Copilot connector and a Power Platform connector used as
  knowledge, and pick correctly;
- add Snowflake tables as a knowledge source and describe when that is the right answer rather than
  a tool;
- write instructions that make an agent cite, abstain, and prefer the right source when two
  disagree;
- diagnose knowledge that returns nothing, which is the most common failure in this module and has
  five usual causes.

## The thread through this module

Bruno is a quality engineer. He asks the questions everyone asks:

> *"What is the minimum overlay thickness, and why is it that?"*

The answer is in three places at once. `SWI70000318` says **what** — 3.0 mm at every measurement
point. `DGL70000009` says **why** — it is a dilution layer, a machining allowance and a service
allowance added together. The intranet page `TS-014` summarises both and says explicitly that where
it differs from the work instruction, the work instruction wins.

An agent that finds one of the three gives an answer that is true and incomplete. An agent that
finds all three, and knows which one governs, is doing the job. Building that is the lab.

## Self-check

<details>
<summary>1. Someone asks why you cannot just paste all of Technik's documents into the agent's instructions.</summary>

Two reasons, and the second is the interesting one. The **size**: the five documents in this module
alone are around 12,000 tokens, the full controlled document set would be far beyond any context
window, and every request would carry all of it (see [Tokens](../B1/tokens.html)). And the
**quality**: irrelevant context does not sit harmlessly, it competes — a question about hydrostatic
testing is answered *worse* when the cladding instruction is also in the window, because there is
more plausible-looking material to blend. Retrieval exists to put three relevant passages in the
context instead of thirty irrelevant ones.
</details>

<details>
<summary>2. Your agent answers questions about SharePoint documents perfectly for you, and returns nothing for a colleague. What happened, and is it a bug?</summary>

It is almost certainly permissions, and it is not a bug — it is the feature working. SharePoint
knowledge is queried with each user's own permissions, so a colleague who cannot open the document
gets no answer built from it. That is exactly what you want for controlled documents, and it is why
this module uses SharePoint for the standards pages rather than uploading them as files. Uploaded
files have no per-user permissions at all: everyone who can use the agent can see everything in
them.
</details>

<details>
<summary>3. When should Snowflake be a knowledge source rather than a tool?</summary>

When the questions are open-ended and you cannot enumerate them in advance. Knowledge lets the agent
turn a question into a query itself, which covers a long tail you would never write tools for, at
the cost of predictability — you do not know what query it will write. A tool is the opposite: one
fixed statement, known cost, known shape, testable. The rule that works in practice is that the
questions you can name become tools, and the ones you cannot become knowledge. Technik's revision
lookups are named questions, so B7 makes them a tool. "Something about work orders last month" is
not, so this module makes it knowledge.
</details>

<details>
<summary>4. An answer cites the right document but the quoted criterion is wrong. Which of the three usual causes is it, and how would you tell?</summary>

Three candidates. **Retrieval** brought back the wrong passage of the right document — check what
was actually retrieved in the test pane; this is the most common. **The model paraphrased** a
passage it did retrieve correctly, which is an instruction problem: tell it to quote acceptance
criteria rather than summarise them. Or **the source is genuinely out of date or contradicted** by
another source — at Technik, `TS-014` is a summary of `SWI70000318`, and if the work instruction is
revised the summary can be wrong while remaining perfectly retrievable. The activity map
distinguishes the first from the other two; only reading the source distinguishes the second from
the third.
</details>

<details>
<summary>5. Why does an agent that never says "I could not find that" make you nervous?</summary>

Because abstention has to be asked for. The training bias is towards answering, so a model with no
relevant passage in context will produce a plausible one rather than stopping — the gap-filling
mechanism from [B1](../B1/hallucination.html). An agent that always answers is not well-grounded, it
is untested: you have not yet asked it something its sources do not cover. Put such questions in the
evaluation set deliberately (B13), and instruct the agent to answer only from its sources and to say
plainly when they do not reach.
</details>
