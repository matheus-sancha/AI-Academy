## TL;DR

Copilot in PowerPoint can summarise a deck someone sent you and answer questions about what is in it.
Ask for the slide,
not just the answer, then go to that slide and read it. And remember what a deck is: someone's
presentation of a document, not the document itself.

## Why it matters

Decks travel. A training deck is still forwarded to new starters long after the procedure behind it
changed, and Copilot answers from it fluently, with no sign that it's out of date. Microsoft's FAQ is plain about the limit: Copilot *"can't
understand meaning or evaluate accuracy"*. So an answer about a deck is a claim about what the deck
says. Whether the deck is right is a separate question, and it's yours ({{topic:hallucination}}).

## How it works

### Where you find it

<!-- volatile verified=2026-10 -->
Open the deck and select the **Copilot** icon. The Copilot pane opens beside the slides. Type a
request: *"Summarise this presentation"*, or a question about its content.
<!-- /volatile -->

For a deck you already have, Microsoft lists two things: a **summary** of the presentation, and
**answers to questions** about its content. Both arrive as chat in the pane.

### What it reads

<!-- unknown since=2026-10 -->
Microsoft's pages on Copilot in PowerPoint don't say whether it reads **speaker notes**, the text
inside **charts and tables**, or anything shown only in a **picture**, such as a screenshot of a
form. They also don't say how a very long deck is handled, beyond a limit on how many words Copilot
can process per prompt.
<!-- /unknown -->

Until that's checked, treat the slide text as what Copilot surely read. If the point you're after
might live in a chart, a screenshot or the notes, look there yourself.

### Three ways to ask

| You ask | You get | How to check it |
|---|---|---|
| *"Summarise this presentation"* | A short overview | Weakest. A summary decides for you what mattered |
| *"Which slide covers X? Give the slide number and title"* | A pointer | Go to the slide and read it |
| *"What does the deck say about X? Quote it and give the slide"* | A quote and a place | Find the quote on the slide; compare it word for word |

Use the second and third. They turn Copilot into a way of finding a slide, and the slide either says
it or doesn't. The same habit served you in Word
({{topic:wordask}}): ask for the quote, not the gist.

## In practice at Technik

A new supervisor is sent the quality team's training deck on handling quality notifications, 38 slides
long, and wants one thing: who decides what happens to a nonconforming part.

The quick question:

> *Who decides the disposition of a QN?*

Copilot answers *"the production supervisor, after review with the quality engineer"*. It sounds
reasonable.

The better question asks where:

> *Which slide says who decides the disposition of a QN? Give the slide number and title, and quote the
> sentence.*

Copilot points to slide 23, *Roles*. The quoted sentence is there. Now look at the deck's title slide:
it's dated three years ago. The controlled document is `SOP70000101` *Quality Notification Handling*,
and its current revision gives the disposition to **the quality engineer assigned to the QN**. The
deck has drifted from the procedure. Copilot read the deck faithfully. The deck was the problem.

So the supervisor follows `SOP70000101` and tells the deck's owner that slide 23 is out of date.
Copilot found the slide in seconds. It couldn't have known the deck was stale.

## Using it well

- **Ask for the slide number and a quote**, not only an answer. Then go and read the slide.
- **Look at the deck's date and owner.** A deck is a copy of someone's understanding at one moment.
- **Check the governing document** when the answer matters. A deck about a procedure is not the
  procedure.
- **Look at charts, pictures and speaker notes yourself** when the answer might be there.
- **Ask "is it in the deck?"** before asking what it says. *"Does this deck mention concessions? If
  not, say so"* makes a missing topic visible instead of filled in.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A confident answer that the procedure contradicts | The deck is out of date, and Copilot can't know that | Check the controlled document; tell the deck's owner |
| A summary that skips the one point you needed | A summary decides what mattered | Ask the specific question, and ask for the slide |
| *"The deck doesn't say"* about a value you can see on a chart | Microsoft doesn't document whether chart contents are read | Read the chart yourself |
| An answer you can't find on any slide | It came from the notes, or it was invented | Ask for the slide and a quote; if neither exists, don't use it |

## Key terms

**Deck**: a PowerPoint presentation, the file of slides.

**Speaker notes**: the text under each slide that the presenter sees and the audience doesn't.

**Governing document**: the controlled document a deck summarises, such as an SOP. Where the two
differ, it wins.
