## TL;DR

Copilot in Word does two kinds of writing: it **drafts** from a description, and it **reworks** a
passage you already have, making it shorter, plainer, more formal or into a table. Reworking is the
stronger of the two, because the content is already yours. Drafting from a description is the weaker,
because nothing constrains what it writes. Either way you choose what stays, and you're answerable for
it.

## Why it matters

A blank page and a dense paragraph are where people lose an afternoon in Word. Copilot helps with both. The risk is different in each. A rework can quietly drop a word that mattered. A draft
from a description can fill a note for new operators with numbers that look right and aren't
Technik's, because the model writes what is *likely* ({{topic:llm}}), and a likely thickness is not your
thickness.

## How it works

### Drafting

<!-- volatile verified=2026-10 -->
Place the cursor where the new text should go, or open a blank document, then open Copilot and
describe what you want: topic, audience, tone, format and length. Select **Generate**. You can keep
the result, discard it, regenerate it, or refine it with a follow-up prompt. To draft from a particular
file, type **/** and choose it, if it's available.
<!-- /volatile -->

### Reworking

<!-- volatile verified=2026-10 -->
Select the text, then open Copilot from the small toolbar that appears beside the selection, or from
the document. Use **Auto Rewrite**, or ask for what you want: *"shorter"*, *"plainer, for new
operators"*, *"turn this into a table with columns step, check and limit"*. Then choose **Replace**,
**Insert below** or **Regenerate**.
<!-- /volatile -->

### What the content comes from

| You start from | What fills the page | Typical failure |
|---|---|---|
| A description only | The model's sense of what is likely | Invented specifics: limits, steps, document numbers |
| A file you reference with **/** | That file, as far as the prompt holds it there | Things added that the file never said |
| Text you selected | Your own text | A qualifier dropped or softened in the rewording |

Read down the table and the risk shrinks. The more of the content is yours before Copilot starts, the
less it has to invent. That is grounding ({{topic:hallucination}}) applied to writing.

## In practice at Technik

### A note for new cladding operators

You need a one-page note that walks new operators through cladding inspection. The quick version:

> *Write a one-page note for new operators about cladding inspection.*

It comes back well organised, and says the minimum overlay thickness is **2.5 mm**.
Nothing told it Technik's number, so it wrote a plausible one. Discard it.

The grounded version names the source and the limits on it:

> *Draft a one-page note for new cladding operators from /SWI70000318, sections 4 and 5. Keep every
> number and limit exactly as written in the document. Don't add any requirement it doesn't contain.
> End with: "Section 5 of SWI70000318 governs."*

Now the minimum reads *"not less than 3.0 mm at every measurement point"*, because it came from the
document. Check it anyway, and check every other number against the source.

### Reworking a dense paragraph

One paragraph of the note lists four checks in a single long sentence. Select it and ask: *"Turn this
into a table with columns step, check, limit and record."* Choose **Insert below** rather than
**Replace**, so the original sits under the table and you can compare them row by row. Then delete the
paragraph yourself.

The note isn't a controlled document, and it shouldn't pretend to be one. That's why its last line
sends the reader back to the work instruction.

## Using it well

- **Draft from a file, not a description**, whenever the content exists somewhere.
- **Say what not to add.** *"Don't add requirements"* and *"keep every number as written"* are
  constraints a draft needs ({{topic:clarity}}).
- **Prefer a rework to a draft.** Write the rough content yourself and let Copilot fix the shape.
- **Use Insert below when the wording matters**, and compare before you delete anything.
- **Check every number, name and document reference** against the source. Microsoft's own guidance
  says the same: you decide what to keep, revise or remove.
- **Iterate in follow-ups** rather than regenerating and hoping ({{topic:iterate}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Plausible limits that aren't Technik's | Drafted from a description, with nothing to ground it | Reference the document with **/**, or write the numbers in yourself |
| *"Not less than 3.0 mm"* became *"about 3 mm"* | A plainer rewrite softened a qualifier | Insert below, compare, keep the original wording for limits |
| A colleague's draft reads almost word for word like yours | Similar prompts give similar text | Add your specifics: source, audience, purpose |
| **/** doesn't offer the file | It isn't available to Copilot from where you are | Open the file, or paste the section in ({{topic:sensitive}}) |

## Key terms

**Draft**: new text Copilot writes from a prompt, optionally from a file you reference.

**Rework**: Copilot rewriting text you selected: shorter, plainer, another tone, or a table.

**Insert below**: keeps your original and puts Copilot's version underneath, so you can compare.
