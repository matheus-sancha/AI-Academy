## TL;DR

Copilot explains a formula you don't understand and proposes one for a result you describe, its most
useful work in Excel. Both need checking. Read the formula against what you asked
for, and test it on rows where you already know the answer, including one that sits exactly on a limit.
A formula that's wrong the same way on every row looks perfectly right in a chart.

## Why it matters

A wrong answer in a chat is one wrong answer. A wrong formula is wrong on every row it fills, including
rows added later, and a column of tidy results looks more trustworthy than prose. Most formula mistakes
raise no error. They answer a different question: `>` where you needed `>=`, the tensile column instead
of the yield column, a limit typed into the formula that nobody updates.

## How it works

### Three ways Copilot writes formulas

<!-- volatile verified=2026-10 -->
- **In the Copilot pane.** Describe the column you want (*"add a column that…"*), and Copilot adds it
  and explains how the formula works. It can also build a lookup from another sheet, typically with
  `XLOOKUP`.
- **Formula completion.** Type `=` in a cell and Copilot suggests a whole formula from the headers,
  nearby cells and tables, with a preview of the result and a short explanation.
- **Formula by example.** Type a few values that follow a pattern and Copilot suggests one formula to
  fill the rest of the column.

Both suggestion features can be turned off: in Excel for Windows, **File** > **Options** > **Copilot**;
on the web, **File** > **Options** > **Copilot Settings**.
<!-- /volatile -->

### Explaining a formula

Select a cell and ask *"Explain the formula in the selected cell"*, or name it: *"Explain the formula
in D3."* This is the low-risk use: the formula already exists, and the formula bar shows it in full to
check the explanation against.

### Reading a formula

Every formula starts with `=` and holds up to four kinds of thing: **functions** (`IF`, `SUM`),
**references** to cells or columns, **constants** (`485`) and **operators** (`>=`). Check three:

1. **The references.** Is it reading the column you meant?
2. **The operators.** Does *"at least"* appear as `>=`, not `>`?
3. **The constants.** Is the limit right, and should it be in the formula at all?

Microsoft advises putting a constant in its own cell and referring to it, rather than typing it into
the formula. Then there's one place to read a limit and one place to change it.

### Testing a formula

Then test it on rows whose answer you already know:

- one row clearly passing,
- one clearly failing,
- one **exactly on the limit**,
- one with a **blank** cell.

Most wrong formulas fail one of those four.

## In practice at Technik

A table holds ten supplier material certificates, with a *Yield strength (MPa)* column. The purchase
specification calls for at least 485 MPa. You ask Copilot:

> *Add a column called Yield check that says OK if Yield strength (MPa) meets the minimum in cell J1,
> and CHECK if it doesn't or if the cell is blank.*

Cell J1 holds `485`, labelled *Minimum yield (MPa)*. Copilot adds the column and explains it. Now read
the formula. Suppose part of it is `[@[Yield strength (MPa)]]>J1`. *Meets the minimum* means `>=`, so a
certificate at exactly 485 MPa gets CHECK. That error is cautious. Reading the tensile column instead
would mark weak heats OK.

Then test it. Type `485` into a spare row: OK? Clear it: CHECK? Try a known failing value. Only then
delete the test row and trust the column, for what it checks. *OK* means one number meets one limit, not
that the certificate is accepted.

## Using it well

- **Describe the result, the columns and the limit** in the prompt, by name ({{topic:clarity}}).
- **Keep limits in their own labelled cells**, and ask Copilot to refer to them.
- **Read the formula before you read the results**: references, operators, constants.
- **Test on four known rows**: pass, fail, exactly on the limit, blank.
- **Ask for an explanation** of any formula you inherit, and check it against the formula bar.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A value exactly on the limit is flagged | `>` where *at least* needed `>=` | Read the operators; test a value on the limit |
| Every result looks plausible, and some are wrong | The formula reads the wrong column | Read the references; test a row you know |
| The limit changed and the column didn't | The limit was typed into the formula | Keep it in a labelled cell and refer to it |
| Blanks pass the check | The formula never tested for an empty cell | Say what blanks should give, then test one |
| A suggested formula went in unread | Formula completion offers formulas as you type | Read it like any other formula, or turn suggestions off |

## Key terms

**Formula**: a calculation in a cell, starting with `=`, built from functions, references, constants
and operators.

**Formula completion**: Copilot suggesting a whole formula as you type `=`.

**Formula by example**: Copilot turning a few typed example values into one formula for the column.
