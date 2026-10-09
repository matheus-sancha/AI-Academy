## TL;DR

Copilot in Word answers questions about the document you have open: what it covers, where a
requirement is stated, what a section asks of you. It reads the whole file, but it answers in its own
words, and a paraphrase of a procedure is not the procedure. Ask narrow questions, ask it to quote the
passage and name the section, and read that passage yourself before you act on it.

## Why it matters

Controlled documents are long, and you usually need one step of them. Copilot in Word gets you to the
right page fast. It is less good, and less obviously so, at telling you exactly what that page says. A summary that drops *"at every measurement point"* from an acceptance criterion still
reads perfectly well, and it changes what gets accepted.

## How it works

### Where you find it

<!-- verified tenant=2026-10 -->
Open the document and select the **Copilot** button in the corner of the page. Copilot opens in a pane
beside the document, in a mode that can edit it; select **Chat only** when you want answers without
changes. Some documents also open with a summary at the top: depending on your organisation's
settings, Word makes one automatically for files of at least 200 words saved in OneDrive or SharePoint.
Select **View more** to read all of it, or **Summary** to make one yourself.
<!-- /verified -->

### What it answers from

The open document is the context ({{topic:context}}), and unless you bring in another file it is all
Copilot reads. Microsoft says it takes the whole document into account, but **doesn't always cite later
content**, so a point near the end can arrive without a pointer back to where it came from.

### Three kinds of question

| You ask | You get | How far to trust it |
|---|---|---|
| **Summarise:** *"Summarise this in five bullets."* | The gist | Enough to decide what to read. Never enough to act on |
| **Locate:** *"Which section covers this? Quote the sentence."* | A pointer and a quote | Good, because you can check it in seconds |
| **Judge:** *"Is a 2.8 mm reading acceptable?"* | A verdict | Weakest. Get the quote and decide yourself |

Asking for a quote rather than a paraphrase is the habit from {{topic:hallucination}}: a quote is
either in the document or it isn't.

## In practice at Technik

### Summarising `SWI70000318`

You open the Word copy of work instruction `SWI70000318`, *Cladding Preparation and Inspection*. The
summary at the top gives five bullets, one of which says *"Check finished overlay thickness against the
minimum in section 5."* That tells you where to look, and nothing more.

Now ask the narrow question, in Chat only:

> *Which section gives the minimum overlay thickness on XT valve body bores? Quote the sentence exactly
> and give the section number.*

Copilot names section 5 and quotes: *"not less than 3.0 mm at every measurement point."* Go to section
5 and read the sentence in place. *At every measurement point* is the requirement: a bore whose readings
average 3.1 mm with one at 2.8 mm does not pass. An answer saying *"minimum thickness 3.0 mm"* wasn't
wrong. It just wasn't enough to sign against. Copilot found the rule; applying it is yours, because you sign
the inspection record.

### Which revision is this?

Ask *"is this the current revision?"* and Copilot can only read the revision letter printed in the
file. An old saved copy says revision B long after revision C is released. Check where documents are
released, not in Copilot.

## Using it well

- **Open the document you mean.** Copilot in Word answers from that file, so you choose the source.
- **Use Chat only for questions.** Leave editing on only when you mean to change the document.
- **Ask for the section number and the exact words.** Then read them in place.
- **One question at a time.** Follow up with *"and in section 4?"*.
- **Read the summary as a table of contents.** It tells you where to go, not what it says.
- **Check the revision outside Copilot.** The file's own word for it is not proof.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The summary barely mentions the last sections | It doesn't always cite later content | Ask about that section by name |
| The answer is right in spirit and wrong in detail | A paraphrase dropped a qualifier | Ask for the exact sentence, then read it in place |
| No summary at the top | The file is short, not in OneDrive or SharePoint, or your settings don't allow it | Select **Summary**, or ask in the pane |
| Copilot changed the document when you only asked something | The pane was in its editing mode | Undo, then switch to **Chat only** |
| *"Yes, this is the current revision"* | It read the revision letter in the file | Check the released revision |

## Key terms

**Summary**: Copilot's short overview of the open document, shown at the top or made on request.

**Chat only**: a mode of the Copilot pane in Word that answers without editing the document.

**Quote**: the document's own words, as opposed to Copilot's paraphrase of them. Quotes can be checked.
