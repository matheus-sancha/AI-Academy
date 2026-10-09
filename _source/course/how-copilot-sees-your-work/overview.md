## What this module is for

The previous modules treated Copilot as a model working from what's in front of it. This one is about
*what gets in front of it* at work: what Copilot can reach inside the company, what it can't, and what
you should never hand it. Every app module after this one rests on it, because Copilot in Word, Excel,
PowerPoint, Outlook and Teams all reach your content the same way.

It covers five things: how Copilot answers from your organisation's own content, the permissions rule
that limits what it can see, why it sometimes misses a file you were sure it would find, what not to
paste in, and a short checklist for using what it gives you responsibly.

## Before you start

{{module:how-copilot-works}}, especially {{topic:hallucination}}: this module is what grounding looks
like when Copilot does the searching for you. {{module:prompting}} helps but isn't required;
{{topic:sensitive}} builds on the prompt-injection example in {{topic:anatomy}}.

Allow about 45 minutes.

## What you will be able to do

By the end of this module you should be able to:

- explain where Copilot's answer about your work comes from, and read its citations to check
  it used the right document;
- say why two colleagues can get different answers to the same question, and what that means about
  access;
- recognise over-sharing when Copilot surfaces it, and know what to do about it;
- work through the four causes when Copilot misses a file, and get the answer anyway;
- decide whether a document may go into an assistant, and which assistant;
- use six principles as a check on answers about people, decisions, or anything that leaves your hands.

## The thread through this module

Every example comes from Technik, the fictional manufacturer this course is built around. See the
[scenario](../scenario/index.html) for the company and its documents.

Most examples turn on one work instruction, `SWI70000318`, *Cladding Preparation and Inspection*. It's
published as a PDF in the Controlled Documents library, summarised on a separate Standards page, and
revised in an engineering site that production staff can't open. Who can open which of those, and which
one an answer came from, is most of what this module teaches.

## Self-check

Answer these before moving on. Each answer explains the reasoning, not just the verdict.

<details>
<summary>1. Copilot answers your question about overlay thickness with a figure and a correct citation to the Standards site's summary table. Every word is real. Why might you still not use it?</summary>

Because the summary isn't the governing document. The Standards page itself says the work instruction
governs where the two differ, so the figure is only right if the summary is up to date, and the answer
can't tell you that. A grounded answer is only as good as the document it found. Open the citation,
then ask again naming `SWI70000318`. Reread {{topic:tenantgrounding}}.
</details>

<details>
<summary>2. A colleague's answer to the same question cites a document yours never mentions. Is one of you getting a broken answer?</summary>

Probably neither. Copilot only uses what each person could open themselves, so each search reached
different content. Compare the citations rather than the wording. If the document theirs cites is one
you need for your work, ask them or its owner for it. Copilot never widens anyone's access. Reread
{{topic:visibility}}.
</details>

<details>
<summary>3. Copilot quotes a draft salary review from another department, with a citation. You can open the file. What do you do?</summary>

Don't use it, don't forward it, and tell the file or site owner it's over-shared. Copilot didn't break
anything: the file was already open to you, and Copilot found it because it searches everything you can
open. That makes it the quickest way your organisation has to discover sharing mistakes. Being able to
open something doesn't mean it was meant for you. Reread {{topic:visibility}}.
</details>

<details>
<summary>4. A procedure you know exists isn't found. You can open it, and it's a normal PDF in the Controlled Documents library. What's the likeliest remaining cause, and what do you do now?</summary>

Age. Permissions and format are ruled out, and the library is a place Copilot searches, so the remaining
cause on the shortlist is that the file is too new to have been indexed yet. New documents in a shared
site are indexed daily. Attach the file, or name it in the prompt: that skips the search and gives you
an answer you can check. Reread {{topic:missingcontent}}.
</details>

<details>
<summary>5. You want a summary of a customer's specification labelled *Confidential*. A colleague suggests a free AI site, "so the label doesn't get in the way". What's wrong with that, and what's the better route?</summary>

The label isn't in the way. It's telling you how your organisation classifies the file, and a consumer
site is outside your organisation's protections entirely. The better route is work Copilot, signed in
with your work account, where the summary can inherit the label. First check whether the customer's
agreement allows the document to go into an AI tool at all, by asking its owner. Reread
{{topic:sensitive}}, and {{topic:rai}} for owning what you then send.
</details>
