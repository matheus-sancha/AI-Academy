## TL;DR

The best use of Copilot in PowerPoint is a first draft built **from a document you already have**,
not from a one-line description. The document constrains the content, so there is far less to invent.
Copilot shows you an **outline** before it makes any slides, and that's the cheapest place to cut.
Expect to cut: a draft deck is generous with slides and short on judgement about which ones matter.

## Why it matters

A deck from a description has the same problem as a Word draft from a description
({{topic:wordmake}}): the model writes what is *likely* ({{topic:llm}}), and a likely procedure is
not Technik's procedure. Starting from the document fixes most of that. What's left is subtler:
slides compress, and compression is where a qualifier or a name quietly disappears.

## How it works

### Starting a deck

<!-- verified tenant=2026-10 -->
In PowerPoint for the desktop, open a new presentation (ideally from your organisation's template,
see {{topic:pptbrand}}) and select the **Copilot** icon. Choose **Add content**, then **Agent Mode**,
and describe the presentation you want, or reference the file to build it from. Copilot may ask
questions first, such as who the audience is and what style you want. It then shows an **outline**,
which you can refine in the chat. Only when you approve it does it generate the slides.
<!-- /verified -->

### From a file

Microsoft names what it can build from: a **Word** document and, where it's offered, a **PDF**. Its
notes on doing it well:

<!-- verified tenant=2026-10 -->
- **One file at a time.** A deck is built from a single file.
- **Word documents work best under 24 MB.**
- **Headings help.** A document that uses Word's heading styles gives Copilot its structure.
- **When you reference a file, you can't add more instructions in the same prompt.** Give the
  audience, length and emphasis afterwards, while refining the outline.
- **You need permission to open the file** yourself.
<!-- /verified -->

### The outline is the checkpoint

| Stage | What you can change | Cost of a change |
|---|---|---|
| Outline | Which slides exist, their order, their titles | One sentence in the chat |
| Slides | Wording, layout, images | Slide by slide |
| Presented | Nothing | Whatever the audience believed |

Cut at the outline, before there's anything to unpick.

## In practice at Technik

The quality lead asks for a short briefing for shift supervisors on `SOP70000101` *Quality
Notification Handling*: when to raise a QN, how its priority is set, and who decides what happens to
the part. Supervisors don't need the rest.

Open a new deck from Technik's template, open Copilot, and reference `SOP70000101`. Copilot asks who the
deck is for. Answer in the chat:

> *Shift supervisors. Six slides at most: when to raise a QN, how priority is set, who decides the
> disposition, and where to find the full SOP. Keep the SOP's wording for roles and priorities.*

The first outline has eleven slides, one per section of the SOP, *Purpose*, *Scope* and *References*
included. Cut them in the chat: *"Remove Purpose, Scope, Definitions and References. Merge Raising a QN
and Recording the defect."* Six titles remain. Approve them.

Now read every slide against the SOP. Slide 4 reads *"Disposition: agreed between the supervisor and
quality"*. The SOP says the disposition belongs to **the quality engineer assigned to the QN**. The
bullet kept the topic and lost the person, the very point the briefing exists to make. Fix it by hand,
in the SOP's words. Then check the speaker notes too. Someone will read them aloud.

The last slide sends people to the source: *"`SOP70000101` governs. This briefing doesn't replace it."*

## Using it well

- **Build from the document**, not from a description, whenever the document exists.
- **Give the audience and length in the chat**, right after referencing the file.
- **Cut at the outline**, before any slides exist.
- **Read each slide against the source**: names, roles, numbers and limits first.
- **Read the speaker notes.** Copilot can write them, and a presenter may say them word for word.
- **End with the governing document.** A briefing summarises; the SOP rules.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A deck full of plausible content that isn't Technik's | It was built from a description | Build it from the document instead |
| One slide per section, *Scope* and *References* included | The outline mirrors the document's structure | Cut and merge in the chat before approving |
| *"Agreed between the supervisor and quality"* | Compression dropped who decides | Restore the source wording for roles and limits |
| Your instructions were ignored | They were in the same prompt as the file reference | Reference the file, then give instructions in a follow-up |

## Key terms

**Outline**: the list of slide titles Copilot proposes before it generates any slides.

**Agent Mode**: the Copilot mode in PowerPoint that plans a deck with you, outline first, then builds
it.

**Briefing deck**: a short presentation that summarises a document for one audience, and points back
to it.
