## TL;DR

Copilot in Excel answers questions about the workbook in front of you: which rows stand out, how one
group compares with another, what a column adds up to. Because the answer is about data you can see,
Excel is the easiest place in Office to catch Copilot being wrong. The number either matches the sheet
or it doesn't. Ask in **Chat only** mode, name the columns, and check the answer against the cells
before you repeat it.

## Why it matters

In Word, checking a paraphrase means rereading a section. In Excel you check an answer in seconds:
sort the column, look at the cell. That makes Excel the best place to build the course's central habit,
treating an answer as a claim to check against its source ({{topic:hallucination}}). An answer naming
the wrong row reads exactly as confidently as one naming the right row.

## How it works

### Where you find it, and which mode to use

<!-- verified tenant=2026-10 -->
Select the **Copilot** icon in the lower-right corner of Excel. The pane opens in one of three modes:

- **Edit** (the default) changes the workbook directly to carry out what you ask.
- **Plan** proposes the steps first, so you can review them before anything changes.
- **Chat only** analyses the data and answers in the pane, without changing the workbook.

On a phone, Copilot in Excel may offer only Chat mode.
<!-- /verified -->

For a question, use **Chat only**. In Edit mode, a question can come back as a new sheet, a new
column or a reformatted range.

### What it answers with

Microsoft lists the forms an answer can take: a **summary**, a **trend**, an **outlier**, a **chart** or
a **PivotTable**. If you want a particular one, say so in the prompt. For columns of free text, such as
inspection remarks, it can summarise themes, and you can hover over the small superscript number in the
answer to see which rows it used.

Microsoft's own tips are short. **Be specific**, and **name the columns** you want analysed, because
naming them gives more accurate results. Start broad, then refine with follow-ups ({{topic:iterate}}).

### Three kinds of question

| You ask | You get | How to check it |
|---|---|---|
| **Find:** *"Which heat has the lowest yield strength?"* | A row | Sort the column yourself |
| **Compare:** *"Average tensile strength by supplier"* | A summary or PivotTable | Filter one supplier and look at the status bar |
| **Judge:** *"Are any of these unacceptable?"* | A verdict | Weakest. Ask it to list the rows, then decide against the requirement yourself |

## In practice at Technik

A sheet holds one row for each of ten supplier material certificates. The columns are *Certificate*,
*Heat number*, *Grade*, *Yield strength (MPa)*, *Tensile strength (MPa)* and *Hardness (HBW)*. The
purchase specification calls for a minimum yield strength of 485 MPa.

In Chat only mode, ask the narrow question:

> *Using the Yield strength (MPa) column, list every certificate whose value is below 495, with its heat
> number, lowest first.*

Copilot lists two rows. Now sort *Yield strength (MPa)* ascending and look at the top of the sheet. If
a third row sits at 490 and Copilot missed it, you found out in ten seconds, before forwarding it.

Then ask the judging question the careful way:

> *Which certificates have a yield strength below 485 MPa? Name the rows. Don't say whether they are
> acceptable.*

The second sentence matters. Whether a certificate is accepted depends on the specification, the
certificate's own statements and whoever signs off incoming material. Copilot can find the row. Deciding
about it is your job.

## Using it well

- **Use Chat only for questions.** Switch to Edit only when you want the workbook changed.
- **Name the columns**, exactly as their headers read.
- **Ask for rows, not verdicts.** *"List the certificates below…"* is checkable; *"are these OK?"* is not.
- **Ask for the form you want**: a list, a chart, a PivotTable.
- **Check every number against the cells** with a sort, a filter or the status bar. It's quicker
  than rereading the answer.
- **Follow up rather than starting again.** *"Now only grade TK-A"* builds on the last answer.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A question added a sheet or reformatted the data | The pane was in Edit mode | Undo, then switch to **Chat only** |
| The answer used the wrong column | Two headers were similar and the prompt didn't say which | Name the column exactly as its header reads |
| A list that's almost right | Nothing in Excel forces the answer to match the sheet | Sort or filter the column and compare |
| *"These certificates are acceptable"* | You asked it to judge | Ask for the rows; apply the requirement yourself |
| A long, general answer | The question was broad | Name the columns and the comparison you want |

## Key terms

**Chat only**: the mode of Copilot in Excel that answers in the pane without changing the workbook.

**Edit mode**: the default mode, in which Copilot changes the workbook to carry out a request.

**Insight**: Copilot's answer about your data, as a summary, trend, outlier, chart or PivotTable.
