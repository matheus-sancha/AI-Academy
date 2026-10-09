## What this module is for

Copilot is genuinely useful, and it is sometimes confidently wrong. Both come out of the same
mechanism, and three ideas explain nearly all of it: what the thing inside Copilot actually does,
what it is working from when it answers, and why it sometimes writes something that was never true.

You need no technical background for any of this. What you should have afterwards is the ability to
read a Copilot answer and hold a sensible opinion about whether to trust it.

## Before you start

Nothing. This is where the course starts. Everything after it — prompting, Copilot in the Office
apps, agents your colleagues published — assumes this module and nothing else.

Allow about half an hour.

## What you will be able to do

By the end of this module you should be able to:

- explain, to a colleague who has never used it, what Copilot is doing when it answers;
- say why the same question can come back with two different answers;
- describe what Copilot is working from at any point in a conversation, and what happens to that as
  the conversation gets long;
- recognise an invented detail in an answer about your own work, and name the mechanism behind it;
- decide when an answer needs checking against the source document, and check it quickly.

## The thread through this module

Every example comes from Technik, the fictional manufacturer this course is built around. See the
[scenario](../scenario/index.html) for the company, its documents and how it works.

You will meet one document here — the work instruction `SWI70000318` — and one wrong answer about
it: a limit taken from the wrong table, an appendix the document doesn't have, and a claim to be the
current revision that nothing supports. The rest of the module explains how fluent, confident, wrong
sentences like those come to be written, and what you do about them.

## Self-check

Answer these before moving on. Each answer explains the reasoning, not just the verdict.

<details>
<summary>1. You ask Copilot about the work instruction for weld prep inspection and it answers confidently with something wrong. What are the three candidate causes, in the order you should check them?</summary>

First, **it never saw the document** — it was not attached, or it sits somewhere Copilot cannot reach
for you, and the model filled the gap with something plausible. Second, **it saw the wrong document** —
an old copy, a superseded revision, or a different document with a similar name. Third, and least
likely, **it saw the right one and misread it** — usually because you asked it to summarise when you
needed it to quote. Concluding "Copilot is bad at this" before checking the first two is the most
common reason people give up on it too early, and opening the citation settles both in seconds.
</details>

<details>
<summary>2. Copilot gives good answers about cladding but now and then invents a document number. Which fixes it: a better model, rewording the question, or pointing it at the real documents?</summary>

Pointing it at the real documents. A better model invents less often but still invents. Rewording
usually makes the answer tidier without giving it anything new to work from — and a tidier wrong
answer is worse, because it is more convincing. Only putting the actual documents in front of it, and
then reading what it cites, changes the mechanism that produced the invented number. Everything else
is tuning something that was never the cause.
</details>
