## TL;DR

Turning a stack of documents into one table you can sort and filter is a common job. Decide the
columns first, make them an Excel table, and fill the first rows by hand: they're Copilot's pattern and
your check. Then let Copilot fill the rest, a few documents at a time, and check every row it adds
against its document.

## Why it matters

A table built from documents is only as good as its worst row, and nothing in the table tells you which
row that is. A value copied from the wrong line of a certificate looks just like a right one. Fixing the
shape in advance is what keeps every row Copilot adds checkable.

## How it works

### Decide the columns first

Write the headers before you ask for anything: one column per value, one row per document, and a column
naming the source document. Put the unit in the header (*Yield strength (MPa)*) and only the number in
the cell, so the column sorts and calculates.

### Make it a table

<!-- verified tenant=2026-10 -->
Select the headers and the first rows, then select **Home** > **Format as Table**, choose a style, and
make sure **My table has headers** is ticked.
<!-- /verified -->

An Excel table gives every column a sort and filter control, and a formula entered in one cell fills
the whole column. Those are the controls you'll check Copilot's rows with.

### Fill two rows by hand

Type the first two documents' values in yourself. It gives Copilot a pattern ({{topic:fewshot}}), and
shows you where each value sits on the document, which is what checking a row involves.

### Let Copilot fill the rest

<!-- verified tenant=2026-10 -->
Copilot in Excel can draw on your work documents. Use **Select sources** in the chat field to turn on
**Work**. Copilot then asks you to confirm which documents it may use for the answer. Your approvals last
for the current chat, and a new chat asks again.
<!-- /verified -->

<!-- verified tenant=2026-10 -->
Microsoft doesn't say how reliably Copilot in Excel reads values from a PDF, and in particular from a
scanned certificate where the values are part of an image. Treat every value it
copies from a PDF as unchecked.
<!-- /verified -->

Ask for a few documents per prompt, so a bad batch is small enough to see. Without the Work source,
use Copilot Chat ({{topic:m365chat}}): one certificate at a time, each value quoted, and you type them in.

## In practice at Technik

You have ten supplier material certificates as PDFs, one per heat of bar for XT valve bodies.

**Columns:** *Certificate*, *Heat number*, *Grade*, *Yield strength (MPa)*, *Tensile strength (MPa)*,
*Hardness (HBW)*. Make it a table and type in the first two certificates yourself.

Then, in Edit mode with Work turned on:

> *Add one row to this table for each of these certificates: MC-0413, MC-0414 and MC-0415. Fill every
> column the way rows 1 and 2 are filled. Copy each value exactly as printed on the certificate. If a
> value isn't on the certificate or isn't in MPa, leave the cell empty and say which.*

Approve the three certificates when asked, then check every cell of the new rows against their PDFs
before asking for the next three. Ten certificates are sixty values: a quarter of an hour, and far
cheaper than accepting the wrong heat.

The prompt's last sentence does real work. One supplier reports strength in ksi. Without it, Copilot
might convert the value, or copy it as MPa. With it, you get an empty cell and a note, and you decide.

## Using it well

- **Write the headers before the first prompt.** Units go in the header, numbers in the cell.
- **Fill the first rows yourself.** They're the pattern, and they tell you what checking a row involves.
- **A few documents per prompt.** Check each batch before the next.
- **Ask for an empty cell, not a guess**, wherever a value is missing or in another unit.
- **Approve only the documents you mean.** Approved content can end up in a workbook other people open.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A value that's on the certificate, but in the wrong column | Two values sit close together on the document | Check each new row against its document before going on |
| Numbers that won't sort or add up | The cell holds *"520 MPa"*, not *520* | Units in the header, numbers in the cell |
| A strength that looks too low | The certificate gave ksi and the value was copied as MPa | Tell Copilot to leave other units empty, and convert them yourself |
| Copilot can't find a certificate | Work isn't on, or you didn't approve that document | Check **Select sources**, then approve it |

## Key terms

**Excel table**: a range Excel treats as one object, with a header row, a sort and filter control on
each column, and formulas that fill a whole column.

**Work source**: the setting that lets Copilot in Excel use your work documents once you approve them.

**Pattern rows**: the first rows you fill by hand, which show Copilot the shape and give you a check.
