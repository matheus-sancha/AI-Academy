## TL;DR

Copilot in PowerPoint can't tell which slide matters. Microsoft says it *"can't understand meaning or
evaluate accuracy"*, so its slides come out evenly weighted, often wordy, and unchecked against each
other. Its rewrite tools work on whole text boxes and skip shapes. It does best in English. Treat a
generated deck as a draft to edit down, never as a deck to present.

## Why it matters

A paragraph that's slightly off in a Word document gets reread; a slide that's slightly off gets said
out loud to a room, often by someone who didn't write it. Every limit below ends in the same place: someone who understands the
content has to decide what the deck is for, and cut it to that.

## How it works

### It doesn't know what matters

Microsoft's FAQ: Copilot gives you *"a head start"*, but what it generates *"can be inaccurate or
inappropriate. It can't understand meaning or evaluate accuracy, so be sure to read over what it
writes, and use your judgment."*

In a deck, that shows up in three ways:

- **Even weight.** The slide your audience must remember gets the same six bullets as the slide they
  can skip.
- **Wordiness.** Slides carry more text than anyone can read while listening.
- **No cross-checking.** Nothing tells you when one slide contradicts another, or when a diagram
  disagrees with the text beside it.

<!-- verified tenant=2026-10 -->
Microsoft doesn't say whether Copilot reads the contents of charts, diagrams or pictures when it
writes or answers about a deck.
<!-- /verified -->

### The rewrite tools have edges

<!-- verified tenant=2026-10 -->
Select a text box and Copilot offers **Auto-rewrite**, **Condense** and **Make professional**. They work
on **text boxes only, not shapes**, and on the **whole box**: you can't rewrite one bullet inside it.
<!-- /verified -->

So a process diagram drawn from shapes is left alone, and *Condense* on a box of six bullets rewrites
all six, including the one with the limit in it. Check what changed before you keep it.

### Other limits worth knowing

- **Length.** Copilot can process only so many words per prompt. Microsoft doesn't give the figure.
- **One file.** A deck is built from a single source file.
- **Overflow.** Generated text isn't shrunk to fit its box ({{topic:pptbrand}}).
- **Language.** Microsoft says quality is highest in English and varies in other languages. A
  Portuguese source document may give a weaker draft.

## In practice at Technik

The `SOP70000101` briefing for shift supervisors is built and on-brand ({{topic:pptmake}},
{{topic:pptbrand}}). Before anyone presents it, the quality lead edits it down.

**Find the one slide.** The briefing exists to say who decides a disposition. That slide has six
bullets, like every other. Cut it to one sentence, the SOP's own: the disposition belongs to the
quality engineer assigned to the QN. Make it the slide people remember.

**Cut the words.** *Condense* on slide 2, *When to raise a QN*, shortens all five bullets, and *"not later than the end of the
shift"* becomes *"promptly"*. That's the same softening a Word rewrite can do. Undo, and cut by hand,
keeping the SOP's wording for the deadline.

**Read across slides.** Slide 3 lists three priority levels. The flowchart on slide 5, drawn in shapes,
still shows four, from an older draft the quality lead pasted in. Copilot flagged nothing. A person
reading the deck end to end catches it.

**Rehearse once.** Read the speaker notes aloud. A sentence that wouldn't survive *"says who?"* goes.

## Using it well

- **Decide what the deck is for** before you edit it, and give that slide the weight.
- **Cut, don't shrink.** Fewer words, not a smaller font.
- **Check what a rewrite changed**, especially limits, deadlines and names.
- **Read the deck end to end** for slides, diagrams and notes that disagree.
- **Edit diagrams yourself.** Copilot's rewrite tools skip shapes.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Every slide looks equally important | Copilot can't judge meaning | Pick the key slide and give it the weight |
| *"Not later than the end of the shift"* became *"promptly"* | *Condense* rewrote the whole box | Undo; cut by hand, keeping the source wording |
| A diagram disagrees with the text | Nothing cross-checks slides, and rewrite skips shapes | Read the deck end to end; fix the diagram yourself |
| A weak draft from a Portuguese document | Quality is highest in English | Expect more editing, or work from an English source if there is one |

## Key terms

**Condense**: a Copilot rewrite that shortens the text in a selected text box.

**Text box versus shape**: Copilot's rewrite works on text boxes, not on text inside shapes such as
flowchart boxes.

**Even weight**: every slide given the same amount of text and emphasis, whatever it matters.
