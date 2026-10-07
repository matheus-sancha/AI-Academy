## TL;DR

A controlled document has a required structure, and a draft that ignores it costs more to fix than it
saved. So start from the template, keep its headings, and use Copilot to **fill sections one at a
time** from a source, not to invent the shape. And say it plainly: a Copilot draft is **not a released
revision**. It has no number and no approval, and it goes through the same review as anything you typed.

## Why it matters

At Technik, every new controlled document starts from `GWI70000027`, the *Controlled Document Authoring
Template*. Reviewers read a draft against that structure. Ask Copilot for *"a work instruction for
recording overlay thickness"* and you get something that looks like a work instruction: its own
headings, its own order, sections the template doesn't have and none of the ones it requires. Now you're
fixing the shape before anyone can review the content.

The second risk is quieter. A draft that Copilot has made look finished gets treated as finished.

## How it works

### Two ways to start from a template

<!-- volatile verified=2026-10 -->
**In Word:** open the template, then ask Copilot to draft into it. Microsoft lists this among Copilot in
Word's abilities: start from a template or an existing document and draft new content *while keeping
its formatting and structure*.

**From the Microsoft Copilot app:** select **Apps and more**, then **Create**. In *What do you want to
create?*, choose **Browse all templates**, or **Browse brand templates** for your organisation's own,
which appear only if your organisation has set them up.
<!-- /volatile -->

<!-- unknown since=2026-10 -->
Whether `GWI70000027` appears under **Browse brand templates** at Technik hasn't been checked. If it
doesn't, open it from wherever your team takes controlled templates from.
<!-- /unknown -->

### Fill, don't shape

| You ask | What Copilot decides |
|---|---|
| *"Write a work instruction for…"* | The headings, the order and the content |
| *"Fill the Scope section of this document from…"* | The content of one section, inside a structure that's already right |

The second is the request you want. It's {{topic:decompose}} applied to a document: one section, one
source, one prompt, checked before the next.

### What a draft is, and what it isn't

| | Released revision | Copilot draft |
|---|---|---|
| Has a document number and revision letter | Yes | No |
| Reviewed and approved | Yes | No |
| What work is done to | Yes | Never |

Copilot can't release anything, and it doesn't know what is released. Everything it writes into the
template is a proposal, exactly like text you typed yourself.

## In practice at Technik

### A new Local Work Instruction

The cladding cell needs a Local Work Instruction (LWI) for recording overlay thickness readings. You
open `GWI70000027`. Its headings are *Purpose*, *Scope*, *References*, *Safety*, *Procedure*,
*Records* and *Revision history*. Don't ask Copilot for the whole document. Fill one section:

> *Fill the Procedure section of this document from /SWI70000318, section 5. Use numbered steps.
> Keep this document's headings, and don't add any. Where the source doesn't say something, write
> [TO CONFIRM] instead of guessing.*

Read the steps against section 5. Is the limit still *"not less than 3.0 mm at every measurement
point"*? Each `[TO CONFIRM]` is a question for the cell lead, not a gap to fill with whatever sounds
right. Then move on to *Records*, with its own prompt.

### The sections to keep away from Copilot

- **References.** Check every document number Copilot writes. A number in the right format that
  doesn't exist is exactly the gap-filling of {{topic:hallucination}}.
- **Revision history and approvals.** Leave them empty. The release process fills them, and an
  invented approver or date is worse than a blank.

The finished draft goes into review like any other. Copilot doesn't shorten that path.

## Using it well

- **Start from the template, never from a blank page**, for anything controlled.
- **One section per prompt**, each with its source named.
- **Tell it to keep the headings** and to add none.
- **Ask for a placeholder, not a guess**, where the source is silent.
- **Never let it fill numbers, revision letters, approvers or dates.**
- **Mark the file as a draft** until it's released, and review it as your own work.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Headings renamed, reordered or added | You asked for the whole document | Fill one section at a time, and say *keep the headings* |
| *References* lists a document that doesn't exist | It filled a gap with a likely number | Check every number where documents are released |
| A draft circulates as if it were approved | It looks finished | Mark it as a draft and send it through review |
| The template isn't under **Browse brand templates** | Your organisation hasn't set it up there | Open the template from its usual location |

## Key terms

**Controlled document**: a document whose structure, review and release are governed. At Technik,
work instructions, SOPs and the rest of the document set.

**Template**: the document a new controlled document starts from. At Technik, `GWI70000027`.

**Released revision**: the approved version with a number and revision letter. Work is done to this,
never to a draft.
