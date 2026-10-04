## TL;DR

Say exactly what shape the answer should take: a bullet list, a table with named columns, fixed headings, one
paragraph, an email you can send. A named shape makes the answer usable without editing. It also makes a
wrong answer easier to spot, because a missing column is obvious in a way a missing sentence is not. Ask
for a place to put *"not stated"* and a citation per claim, and the shape starts checking the answer for
you.

## Why it matters

Much of the time spent on a Copilot answer goes on reshaping it: paragraph into bullets, prose into a
table. Asking for the shape up front skips that.

The bigger reason is checking. A paragraph can leave something out smoothly. A table with a *Status*
column can't: the cell says something or is visibly empty. Microsoft's guidance adds that specifying the
output structure can significantly affect the quality of results, not just their look.

## How it works

The shapes worth knowing by name:

| Shape | Use it when |
|---|---|
| **Bullet list** | The points are separate and order matters little |
| **Numbered list** | Order matters: steps, priorities |
| **Table with named columns** | You're comparing several things on the same points |
| **Fixed headings** | Every answer of this kind should be laid out the same way |
| **One paragraph, N words** | It'll be read in passing, or pasted somewhere |
| **A finished email or message** | It's going straight to someone. Name the recipient and the tone |

Three refinements make a shape do more than look tidy:

1. **Name every column or heading.** *"A table"* leaves the columns to Copilot. *"A table with columns QN,
   unit, operation, defect, status"* doesn't.
2. **Give gaps a place.** A *Not stated* heading, or the instruction *"write 'not stated' in any cell the
   source doesn't support"*. Without one, a shape with ten cells tends to get ten answers.
3. **Ask for citations, close to the claim.** Microsoft's guidance is that asking for citations makes
   statements more likely to be grounded, because a wrong statement now needs a wrong citation too, and
   that a citation next to the statement works better than a list at the end. In Copilot, citations to
   files it found are links you can open. For pasted text, ask it to quote the sentence it used.

A format the source can't fill invites invention: ask for a column the QN has no information for, and
you're asking to have it filled.

## In practice at Technik

**One QN, fixed headings.** The summary of quality notification `300001234` goes to the same team leads every
time, so give it the same headings every time:

> Use exactly these headings: **Found**, **Where**, **Done so far**, **Still open**, **Not stated**. One line
> under each. Put anything the QN doesn't cover under *Not stated*.

People learn to read *Not stated* first. When it says *"cause; disposition; release date"*, the team leads
know what not to ask.

**Several QNs, one table.** A week later you have `300001234`, `300001211` and `300001219`, all about porosity
in overlay cladding, and the question is whether they are the same problem:

> Put the three QNs below in one table, one row per QN, with these columns: **QN**, **Unit**, **Operation**,
> **What was found**, **Status**, **Source sentence**. In *Source sentence*, quote the sentence from that QN
> each row is based on. Write "not stated" in any cell its QN doesn't support.

The *Source sentence* column makes this checkable in a minute. If a row's *What was found* doesn't match
its quote, that row is wrong. And a *not stated* cell isn't a failure: you've learnt something about that
QN.

> [!TIP]
> If you'll paste the result somewhere, ask for that destination's shape: *"as a Teams message under 50
> words"*, *"as a table I can paste into Excel"*. Reshaping afterwards is where errors creep in.

## Using it well

- **Name the shape and every part of it**: columns, headings, word count.
- **Pick the shape for the check you'll make**: a table to compare, headings to spot what's missing.
- **Always give gaps a place.**
- **Ask for a quote or citation per claim** when you'll act on the answer.
- **Show it** when naming isn't enough. One example of the layout fixes most drift ({{topic:fewshot}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Every cell is filled, some with things the source doesn't say | No place for gaps | Add *"write 'not stated'"*, or a *Not stated* heading |
| The format drifts after the first answers | The request is far back in a long chat | Restate it; start a new chat per task ({{topic:context}}) |
| You always get bullets, whatever you ask | A custom instruction sets the format ({{topic:anatomy}}) | Override it in the message, or change the setting |
| A neat table that's wrong in one row | A tidy shape looks trustworthy | Add a source column and spot-check rows against it |

## Key terms

**Output format**: the shape you ask the answer to take.

**Fixed headings**: the same named sections in the same order, every time.

**Source column**: a column quoting the passage each row is based on, so each row can be checked.
