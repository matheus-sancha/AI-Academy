## What this module is for

Word is where Technik's long documents live: work instructions, SOPs, reports, the notes people write
about them. It's also where Copilot's summarising is worth the most, because the cost of reading twenty
pages to find one step is real.

This module is about using Copilot *inside* the document you have open. Copilot Chat helps when you
don't know which document holds the answer. Copilot in Word helps once you do: asking about it,
drafting from it, reworking it, and starting a new controlled document from the template.

The five app modules share a shape (ask, make, one speciality, limits). Word's speciality is the
controlled template, where a required structure meets a generative draft.

## Before you start

{{module:prompting}} applies to every request in this module, especially {{topic:clarity}} and
{{topic:decompose}}. {{topic:hallucination}} explains why the lessons keep asking for a quote rather
than a paraphrase. {{module:copilot-chat}} is the place to start when you don't yet know which
document you need.

Allow about 40 minutes.

## What you will be able to do

By the end of this module you should be able to:

- ask Copilot about the open document, and get a quote and a section number you can check;
- tell a summary you can act on from one that only tells you where to look;
- draft from a referenced file rather than a description, and rework text without losing a qualifier;
- fill a controlled template one section at a time, keeping its structure, and treat the result as a
  draft, not a released revision;
- name where Copilot in Word gets thin (length, language, formatting, tracked changes) and check
  those places yourself.

## The thread through this module

Every example comes from Technik, the fictional manufacturer this course is built around. See the
[scenario](../scenario/index.html) for the company and its documents.

Two documents carry the module. Work instruction `SWI70000318`, *Cladding Preparation and Inspection*,
is summarised, questioned, drafted from and reviewed: its section 5 requires an overlay *"not less than
3.0 mm at every measurement point"*, and the last four words are the kind of detail a paraphrase drops.
`GWI70000027`, the *Controlled Document Authoring Template*, is where a new Local Work Instruction
starts, filled one section at a time.

## Self-check

Answer these before moving on. Each answer explains the reasoning, not just the verdict.

<details>
<summary>1. The summary at the top of SWI70000318 says "minimum overlay thickness 3.0 mm". A bore's readings average 3.1 mm, with one at 2.8 mm. Can you pass it on the strength of the summary?</summary>

No. The summary is a pointer, not the requirement. Section 5 says *"not less than 3.0 mm at every
measurement point"*, so one reading at 2.8 mm fails, whatever the average. The summary wasn't wrong; it
paraphrased and dropped the qualifier that decides this case. Ask Copilot to quote the sentence and
name the section, then read it in place. Reread {{topic:wordask}}.
</details>

<details>
<summary>2. You ask Copilot in Word "is this the current revision?" and it says yes, revision B. What has it actually told you?</summary>

Only what the file says about itself. Copilot reads the revision letter printed in the document you
have open. If that's an old saved copy, it will still say revision B after revision C is released.
Which revision is released is a fact about the release record, not about this file. Check it there.
Reread {{topic:wordask}}.
</details>

<details>
<summary>3. A colleague drafted a note for new operators with "write a note about cladding inspection", and it gives a minimum thickness of 2.5 mm. What went wrong, and what's the better prompt?</summary>

Nothing grounded the draft, so the model wrote a likely number rather than Technik's. Draft from the
source instead: reference `SWI70000318` with **/**, name the sections, and say *keep every number as
written and add no requirements*. Then check each number against the document anyway. Reworking text
you supplied is stronger still, because the content is already yours. Reread {{topic:wordmake}}.
</details>

<details>
<summary>4. You open GWI70000027 and ask Copilot to "write a Local Work Instruction for recording overlay thickness". It looks finished. What's wrong with it, even if every sentence is accurate?</summary>

Two things. You asked for the whole document, so Copilot chose the headings and order, and reviewers
read against the template's structure. Fill one section per prompt and tell it to keep the headings.
And it *looks* finished, but it's a draft: no document number, no revision letter, no approval. It goes
through the same review as anything you typed, and its *References* and *Revision history* need
checking or leaving blank. Reread {{topic:wordtemplate}}.
</details>

<details>
<summary>5. You're reviewing a draft of SWI70000318 revision C with tracked changes on. Should you ask Copilot "what changed in this revision?"</summary>

Not as your answer to that question. Microsoft doesn't document how Copilot in Word treats tracked
changes, so you can't tell whether it read a deletion as gone, as still present, or not at all. Use
Word's own review tools to see what changed, ask Copilot about one section at a time, and read the
changed limits yourself. Reread {{topic:wordlimits}}.
</details>
