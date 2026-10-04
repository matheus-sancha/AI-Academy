## TL;DR

Showing Copilot an example of the answer you want often works better than describing it. One example is
*one-shot*, several are *few-shot*, none is *zero-shot*. The model picks up length, layout, tone and level
of detail from the example in a way a paragraph of description rarely conveys. It also picks up things you
didn't mean it to copy, so keep examples short, realistic and clearly labelled.

## Why it matters

Some things are hard to describe and easy to show. *"Short, plain, no codes, headings in this order"* still
leaves a dozen choices open: how short, which headings, full sentences or fragments. One finished
summary settles all of them at once.

Examples also hold a shape steady. Team leads who get a QN summary every morning want each one laid out the
same way.

## How it works

The model continues the text in front of it in whatever way is most likely ({{topic:llm}}). Put a finished
input and output in that text and the most likely continuation is *another one like it*. Microsoft's
guidance stresses that this isn't learning in the lasting sense. The model isn't changed. The example
shapes this one answer and is gone when the chat ends.

Microsoft's guidance shows this with a classifying task: with no examples the model guesses; with three,
it follows the pattern exactly, even for a label no example used.

That cuts both ways. The model copies everything that looks like part of the pattern:

- **Length and layout**, which is usually what you wanted.
- **Wording and specific details**, which usually isn't. A serial number or a phrase from the example can
  turn up in the new answer.
- **Order.** Models give extra weight to what comes last, so with several examples the final one has the
  most pull.

So the rules for a good example are few and strict: **short, realistic, consistent with the output you
want, and clearly marked as an example.** Keep examples together, rather than scattered among your
instructions.

## In practice at Technik

You once wrote a summary of quality notification `300001211` by hand, and everyone liked it. Show that
shape instead of describing it:

> Summarise the new quality notification for the team leads in exactly the same layout as the example.
> The example is about a **different** QN. Use its layout only, never its facts.
>
> **Example (QN 300001211):**
> **Found:** porosity in the cladding on a valve body bore
> **Where:** subsea tree unit, at the cladding step
> **Done so far:** area marked, unit held
> **Still open:** whether to repair or scrap; no decision recorded
> **Not stated:** cause
>
> **New QN:**
> \---
> *(QN 300001234 text)*
> \---

The answer arrives in the same five headings, at the same length and level of plainness. Read it against the
QN anyway. One run's *Where* line reads *"subsea tree unit, at the cladding step"*, word for word from the
example, when the new QN names its unit, `XT-V2-1042`. The example had no serial number, so neither did the
answer.

There are two fixes. Either make the example carry the detail you want, giving it a serial number of its own
so the answer does the same, or say so in words: *"always give the serial number."* Describing and showing
work together. Use the example for the shape and a sentence for any rule the example doesn't make obvious.

> [!IMPORTANT]
> Never paste a real past answer as an example without reading it first. Whatever it got wrong, it will
> teach.

## Using it well

- **Show the shape when describing it would take more than a sentence.** Headings, a table layout, a tone.
- **Use one good example before several.** Add a second only if the first is being copied too literally,
  and make the two differ in their content.
- **Label it** as an example and say what to take from it: layout, length, tone.
- **Keep it short.** An example longer than the answer you want also teaches *long*.
- **Keep good examples somewhere you can find them.** A summary everyone liked is worth saving as the
  pattern for the next one ({{topic:iterate}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A detail from the example appears in the new answer | The model copied content as well as pattern | Label the example as a different case; check the answer for leaked details |
| Answers follow the example too literally | One example, read as a template for wording | Add a second example that differs in content |
| A detail you need is always missing | The example didn't show it | Put it in the example, or state it as a rule |
| The format drifts after a few answers | The example has scrolled far back in a long chat | Repeat it, or start a new chat ({{topic:context}}) |

## Key terms

**Zero-shot**: a prompt with no examples, only instructions.

**One-shot / few-shot**: a prompt with one, or several, examples of the input and the answer you want.

**Example leakage**: content from an example, not just its pattern, showing up in the answer.
