## What this module is for

Sooner or later a colleague will send you a link, or you'll find a name in the Teams app store: an agent
someone at your company built for one job. It answers questions about work orders, or a policy, or a
product range, from a set of documents its publisher chose.

This module is about meeting one from the user's side. It's one lesson, because nothing about an agent
needs new technique. It needs the habits you already have, applied to an assistant that looks more
official than Copilot and is wrong for the same reasons.

## Before you start

{{module:how-copilot-sees-your-work}}, especially {{topic:visibility}}: an agent that searches
SharePoint does it with your permissions. {{topic:m365chat}} shows how to check a citation, and this
module does the same thing with an agent's.

Allow about 15 minutes.

## What you will be able to do

By the end of this module you should be able to:

- find an agent your organisation published, in Teams or in Microsoft Copilot;
- read an agent's description and say what it was and wasn't built to answer;
- audit an answer that mixes a cited document with something the agent looked up;
- recognise a question outside an agent's job, and what a good agent does with it;
- report a wrong answer to the right person, with enough detail to fix it.

## The thread through this module

Every example comes from Technik, the fictional manufacturer this course is built around. See the
[scenario](../scenario/index.html) for the company and its documents.

The agent is the **Technik Production Assistant**, in Teams. You ask it about work order `100004521`,
held up by a quality notification, and about the inspection that applies. The answer cites work
instruction `SWI70000318` for one half and has nothing to cite for the other. Then you ask it something
it was told not to decide.

## Self-check

Answer these before moving on. Each answer explains the reasoning, not just the verdict.

<details>
<summary>1. An agent was built by your company's quality team and approved by an admin. Can you use its answers without checking them?</summary>

No. Approval means an admin agreed it may be offered to the organisation. It doesn't check the answers,
and nobody could: they're generated fresh for each question. The agent runs on the same kind of model as
Copilot and is wrong for the same reasons, so read what it cites. Reread {{topic:usingagents}}, and
{{topic:hallucination}} for why.
</details>

<details>
<summary>2. The Production Assistant tells you work order 100004521 is held up by QN 300001234 and cites SWI70000318 for the inspection. Which part can you check by opening the citation?</summary>

Only the inspection. The citation is the work instruction, so open it, check it's the released revision,
and check section 5 says what the answer claims. The status and the QN were looked up, not cited, so
there's no document to open. Check them in the record if you have access, or with the planner, before
you act on them. Reread {{topic:usingagents}}.
</details>

<details>
<summary>3. You ask the assistant whether the porosity can be accepted and the unit released. It gives you a confident yes. What's wrong, and what do you do?</summary>

The question was outside its job. Deciding what happens to a nonconforming part is the assigned
quality engineer's call, and the agent's description says it won't make it. A confident yes, with
nothing cited, is the agent answering from general knowledge. Don't act on it, and report it to the
publisher with the question and the answer, because the next person may not notice. Reread
{{topic:usingagents}}.
</details>

<details>
<summary>4. The assistant quotes SWI70000318 accurately, but you know the procedure itself is out of date. Who do you tell: the agent's publisher or the document's owner?</summary>

The document's owner. The agent did its job: it found the right document and quoted it correctly. The
fix belongs in the document, and once it's released the agent will answer from the new revision. Tell
the publisher when the answer doesn't match what the document says. Reread {{topic:usingagents}}.
</details>

<details>
<summary>5. The assistant gives you good answers in a one-to-one chat. Your team adds it to a channel, and there it can't find any procedures. Is it broken?</summary>

No. In Teams channels and group chats, an agent built in Copilot Studio can't use knowledge that needs
your own sign-in, such as SharePoint, so the documents it answers from aren't available there. Ask it
in a one-to-one chat. (A colleague asking the same agent and getting a citation you don't is a
different thing: permissions, not a fault.) Reread {{topic:usingagents}}, and {{topic:visibility}}.
</details>
