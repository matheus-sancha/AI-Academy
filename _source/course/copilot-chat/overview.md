## What this module is for

The app modules that follow each put Copilot inside one document: the report in Word, the table in
Excel, the thread in Outlook. This module is about the assistant that isn't inside any of them.
Microsoft Copilot Chat is where you go when you don't know which document holds the answer, or when the
answer is spread across your week: which procedure covers a step, what happened on a job, what you
missed.

It's one lesson, because Chat itself is simple. What takes judgement is knowing what it's answering
*from*, and that depends on something most people never check: which Copilot they have.

## If you have Copilot Chat only

Everyone with a work account has Copilot Chat. Without a **Microsoft 365 Copilot licence**, it answers
from the web and from what you give it: text you paste, files you upload or select, and the mail or
chat you have open in Outlook or Teams. It doesn't search your organisation's documents, so a question
like *"which document covers weld prep inspection?"* gets a general answer from the web, not Technik's
procedure. The fix is to attach the document you mean. The lesson starts by showing how to tell which
one you have, and marks each step that needs the licence.

## Before you start

{{module:how-copilot-sees-your-work}}. This module assumes you know that a licensed Copilot searches
your work content within your permissions, and that you read citations as part of the answer.
{{module:prompting}} applies to every question you ask in Chat.

Allow about 20 minutes.

## What you will be able to do

By the end of this module you should be able to:

- find Copilot Chat, and tell whether yours searches your work content or only the web;
- choose Chat rather than an app for questions that span several documents or conversations;
- ask Chat which document covers a procedure, and check the citation before using the answer;
- recognise a web-only answer to a work question, and fix it by attaching the document;
- use Chat to pull a job together across mail and chats, and treat the result as a map, not a record.

## The thread through this module

Every example comes from Technik, the fictional manufacturer this course is built around. See the
[scenario](../scenario/index.html) for the company and its documents.

The worked example is one question: *which document covers weld preparation and inspection for
cladding?* With a licence, Chat finds work instruction `SWI70000318` and a summary page on the Standards
site, and the lesson shows how the citation tells you which one to use. Without one, the same question
shows what a convincing web answer to a work question looks like.

## Self-check

Answer these before moving on. Each answer explains the reasoning, not just the verdict.

<details>
<summary>1. You need to know which procedure covers the hydrostatic test, but you don't know its number. Do you open Word and ask Copilot there, or use Copilot Chat? Why?</summary>

Copilot Chat. Copilot in Word works on the document you have open, and you don't yet know which
document that should be. Chat is for questions that span more than one file: finding which document
covers something, then checking it. Once you know it's `SWI70000402`, you can open it and work on it in
Word. Reread {{topic:m365chat}}.
</details>

<details>
<summary>2. Chat gives you a clear, well-structured answer about weld preparation that never mentions a Technik document. What are the two likely explanations, and how do you tell them apart?</summary>

Either you have Copilot Chat without a Microsoft 365 Copilot licence, so it can't search your
organisation's documents and answered from the web; or you have the licence and the search found
nothing useful. Check which one you have from the label the product shows. Either way, the fix is the
same: attach the document and ask about the file. A fluent answer is not a grounded one. Reread
{{topic:m365chat}}, and {{topic:missingcontent}} for the second case.
</details>

<details>
<summary>3. A colleague says Copilot Chat "can't see their files", and yours clearly can. Is theirs broken?</summary>

Not necessarily. Everyone with a work account has Copilot Chat, but only a licensed Chat searches work
content. Without the licence it answers from the web and from what you paste, upload or have open. Their
answer depends on which one they have, and on whether work grounding is switched on. They can check the
label Copilot shows. Reread {{topic:m365chat}}.
</details>

<details>
<summary>4. Chat answers *"which document covers weld prep inspection?"* by citing both `SWI70000318` and the Weld Overlay Acceptance Criteria page. Which do you use, and how do you know?</summary>

The work instruction. You know because you opened the citations: the Standards page says the work
instruction governs where the two differ, which makes it a summary of the procedure, not the procedure.
Then check you're looking at the released revision and that sections 4 and 5 say what the answer
claims. Without opening the citations, the two look equally authoritative. Reread {{topic:m365chat}},
and {{topic:tenantgrounding}} for why grounded answers go wrong this way.
</details>

<details>
<summary>5. You ask Chat what's happened on PRJ-2031 this week, and it lists four open questions with names. Can you forward that list to the project manager as it is?</summary>

Not yet. The list is a map of where to look: each item came from a mail or chat it cites, and a summary
can merge, drop or misattribute what was said. Open the cited messages, check each item and who raised
it, then send it as your own summary. You're accountable for what you forward, not Copilot. Reread
{{topic:m365chat}}, and {{topic:rai}} for accountability.
</details>
