## What this module is for

Excel is where Technik's lists live: readings, certificates, schedules, anything with one row per thing.
It's also where Copilot's answers are easiest to check, because the data is on the screen. Sort a
column and you know whether Copilot found the right row.

That makes Excel the place to practise the course's central habit: treat an answer as a claim and check
it against the source. It also has a risk the other apps don't share as much. Copilot in Excel changes
the workbook by default, so a mistake can be in the file before you've read it.

The five app modules share a shape (ask, make, one speciality, limits). Excel's speciality is the
formula: the most useful thing Copilot writes here, and the one most worth testing.

## Before you start

{{module:prompting}} applies to every request in this module, especially {{topic:clarity}} (name the
columns) and {{topic:fewshot}} (pattern rows). {{topic:hallucination}} explains why every answer gets
checked against the cells. {{topic:visibility}} covers which work documents Copilot can draw on.

Allow about 40 minutes.

## What you will be able to do

By the end of this module you should be able to:

- ask Copilot about a table in Chat only mode, and check its answer with a sort or a filter;
- build a table from a set of documents: columns first, two rows by hand, then a few documents per
  prompt, each row checked against its source;
- read a formula Copilot writes for its references, operators and constants, and test it on rows whose
  answer you know;
- keep limits in their own cells rather than inside formulas;
- name where Copilot in Excel needs care (direct edits, manual calculation, checked-out files, messy
  layouts, sensitive decisions) and work around each.

## The thread through this module

Every example comes from Technik, the fictional manufacturer this course is built around. See the
[scenario](../scenario/index.html) for the company and its documents.

One set of documents carries the module: **ten supplier material certificates**, one per heat of bar for
XT valve bodies. They're turned into a table, questioned, given a yield check against the purchase
specification's 485 MPa minimum, and in the last lesson they arrive as a supplier's untidy spreadsheet.
Only the documents are used. No system data is involved.

## Self-check

Answer these before moving on. Each answer explains the reasoning, not just the verdict.

<details>
<summary>1. You ask Copilot "which certificates have a yield strength below 485 MPa?" and it names two. What do you do before you tell anyone?</summary>

Sort the *Yield strength (MPa)* column and look. It takes ten seconds and it's the whole advantage of
Excel: the answer is about data on your screen, so you can check it directly. If a third row is below 485,
Copilot missed it, and you've caught it before anyone acted on the list. Ask in **Chat only** too, so
the question doesn't change the workbook. Reread {{topic:excelask}}.
</details>

<details>
<summary>2. You want a table of all ten certificates. Why type the first two rows yourself, when Copilot could do all ten?</summary>

Two reasons. The rows show Copilot the shape to follow: which value goes in which column, in which unit.
And typing them shows you where each value sits on a certificate, which is what checking Copilot's rows
will involve. Then ask for a few certificates per prompt, check each batch against its PDFs, and tell
Copilot to leave a cell empty rather than guess when a value is missing or in ksi. Reread
{{topic:excelmake}}.
</details>

<details>
<summary>3. Copilot adds a Yield check column using the formula [@[Yield strength (MPa)]]>J1, where J1 holds 485. The specification says "at least 485 MPa". Is the column right?</summary>

No. *At least* is `>=`, so a certificate at exactly 485 MPa will be marked CHECK. This mistake errs on
the cautious side; reading the wrong column would not. You catch both the same way: read the
references, operators and constants, then test on four rows you know (pass, fail, exactly on the limit,
blank). Keeping the limit in J1 rather than in the formula was right. Reread {{topic:excelformula}}.
</details>

<details>
<summary>4. Copilot adds a summary sheet to the team's shared certificate log while you're trying something out. Is that a problem?</summary>

It can be. Edit mode is the default and changes the file directly. Once the change is saved, everyone with
access sees it, including anyone co-authoring at that moment. Undo it or restore a previous version. Next
time, work on a copy, turn AutoSave off, or use **Plan** or **Chat only**. Reread {{topic:excellimits}}.
</details>

<details>
<summary>5. A supplier's spreadsheet has a merged title row, headers on row 3, a blank row between heats, and strengths like "520 MPa". Copilot's answer about it looks odd. Why, and what do you do?</summary>

Microsoft doesn't document how Copilot in Excel handles merged cells, blank rows or numbers stored as
text, so you can't rely on it reading the sheet the way you do. Copy the file, then tidy the copy: one
header row, no blank rows, units in the headers and numbers in the cells, then **Format as Table**. Ask
again and check the answer with a sort. If it flags a heat, read the certificate. Accepting or rejecting
material isn't Copilot's decision. Reread {{topic:excellimits}}.
</details>
