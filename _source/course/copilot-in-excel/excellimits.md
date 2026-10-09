## TL;DR

Copilot in Excel's default mode **changes your workbook directly**, and in a shared file others see
the changes. Microsoft says it makes mistakes and shouldn't be used for sensitive decisions. Some files
it won't work in at all, and how it copes with messy layouts isn't documented. Keep sheets tidy, work on
a copy when it matters, and decide for yourself.

## Why it matters

In Word, a bad answer stays in the pane until you use it. In Excel's default mode Copilot acts first:
it adds sheets, fills columns, reformats ranges. So a mistake can be in the file, in front of your
colleagues, before you've read it. And results from a messy sheet aren't flagged as unreliable.

## How it works

### It edits the file

Edit mode is the default. When you save Copilot's changes, **anyone with access to the file sees them**,
including people co-authoring it at the same moment. You can undo, or go back to an earlier version.

<!-- verified tenant=2026-10 -->
Copilot in Excel works with AutoSave on or off. To try something without saving it into the workbook,
turn **AutoSave** off first. Use **Plan** mode to see the steps before anything changes, and **Chat
only** when you want no changes at all.
<!-- /verified -->

### It can be wrong, fluently

Microsoft's FAQ says Copilot *"can sometimes make mistakes, misinterpret information, or produce
inaccurate results"*, explains itself fluently even when wrong, and should be avoided *"for decisions in
sensitive areas such as finance, legal, or medical topics."* Accepting material or passing an inspection
belongs on that list. Copilot can sort, count and flag; whoever signs decides.

### Files it won't work in

<!-- verified tenant=2026-10 -->
- **Calculation set to manual.** Copilot only edits when **Calculation Options** are **Automatic**.
- **A file checked out in SharePoint.** You get *"Unsupported file state"*. Check the file back in,
  or open it in Excel for the web. If a site requires check-out for editing, Copilot in desktop Excel
  won't work on its files.
- **An unsupported format**, such as Strict Open XML. Save as an ordinary Excel Workbook (`.xlsx`).
<!-- /verified -->

### Messy layouts

<!-- verified tenant=2026-10 -->
Microsoft's pages on Copilot in Excel don't say how it handles **merged cells**, **blank rows** inside
the data, **several tables on one sheet**, or **numbers stored as text**. Don't
assume it reads such a sheet the way you do.
<!-- /verified -->

Microsoft's tips say naming the columns gives better results, and a column needs a header to be named.
A tidy sheet (one table, one header row, one kind of value per column, units in the header, no blank
rows) keeps Copilot's work checkable, and the sheet needed it anyway.

### Language

Microsoft says Copilot in Excel was trained mostly on English sources and may do less well when the
prompt **or the data** is in another language. Portuguese headers are data too.

## In practice at Technik

A supplier sends a summary spreadsheet with its material certificates. The top row is a merged title. The
headers are on row 3. There's a blank row between heats, and the strengths read *"520 MPa"*.

Before asking Copilot anything:

1. **Copy it.** Work on your own copy, not a shared file.
2. **Tidy it.** One header row. Delete the title and the blank rows. Move the units into the headers
   and keep only numbers in the cells. Then **Format as Table**.
3. **Check the calculation setting** if Copilot refuses to edit.

Then ask, in Chat only, *"Which heats have a yield strength below 485 MPa?"* and check by sorting. A
flagged heat is a reason to read the certificate, not a rejection. Rejecting is the decision Microsoft
says not to hand to Copilot.

## Using it well

- **Work on a copy** of any shared or important workbook, or turn AutoSave off first.
- **Use Plan or Chat only** when you're not sure what you want changed.
- **Tidy before you ask.** One header row, no blank rows, units in the header.
- **Read every change** Copilot makes before you save it.
- **Keep decisions with people.** Copilot flags; someone accountable decides.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Colleagues see changes you didn't mean to make | Edit mode changed a shared file, and it was saved | Undo or restore a previous version; work on a copy next time |
| Copilot won't edit the workbook | Calculation is set to manual | Set **Calculation Options** to **Automatic** |
| *"Unsupported file state"* | The file is checked out, or in an old format | Check it in, use Excel for the web, or save as `.xlsx` |
| Odd results from a supplier's sheet | Merged cells, blank rows or text numbers, which Microsoft doesn't document | Tidy it into one table, then ask again |
| A confident answer used for an acceptance decision | The decision was handed to Copilot | Use the answer to find rows; decide against the requirement |

## Key terms

**Edit mode**: the default mode, in which Copilot changes the workbook directly.

**Calculation Options**: Excel's setting for when formulas recalculate. Copilot only edits when it is
Automatic.

**Tidy sheet**: one table, one header row, one kind of value per column, no blank rows.
