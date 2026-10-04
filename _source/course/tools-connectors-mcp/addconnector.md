## TL;DR

Adding a connector action as a tool is four decisions: **which action**, **which inputs the model
fills and which you fix**, **what the description says** and **what the result looks like**. Get the
second one wrong and the model is writing your SQL for you.

## Why it matters

Nearly every problem with a tool comes from one of those four. A tool that works when you test the
action directly can still be called at the wrong time, with a part number the model invented, returning three
hundred rows nobody needed.

## How it works

### 1. Choose the action

One action, one job. If the thing you want takes two calls — submit a statement, then fetch its
result — wrap them in an agent flow and expose *that* as the tool, rather than depending on the
orchestrator to sequence two tools correctly.

### 2. Decide what the model fills in

Every input is either **model-filled** or **fixed**, and the rule is worth applying strictly:

> The model fills in what the *user* said. Everything else is configuration.

A part number came from the question, so the model fills it. The Snowflake role, warehouse, database
and schema, the row limit and **the SQL statement itself** are fixed. A model-filled statement turns the
tool into "run arbitrary SQL as the agent's role", so the blast radius of a prompt injection is
everything that role can do. It is also unpredictable in the boring case: the model writes slightly
different SQL each time. Fix the statement; parameterise its values.

<!-- volatile verified=2026-09 -->
In Copilot Studio, after choosing the action you mark each input as model-filled or fixed and give it
a description. The screen changes between releases; the distinction does not.
<!-- /volatile -->

### 3. Write the description

The tool name, the tool description and each input description; the rules for writing them are in
{{topic:tooldesc}}. For a connector action the one most often skipped is the **input description**:
what a good value looks like, with an example. It is how the model knows a part number is `P7000001042`
and not "the valve block".

### 4. Shape the result

The model reads the result as text, so return few columns with names a human would use, few rows
(filter and aggregate in SQL), and the *answer* rather than the raw material for it: one released
revision, not the whole history.

## In practice at Technik

Which CNC program revision should machining use for `P7000001042`? The tool that answers it is
`Get released revision`, specified here.

**Fixed SQL**, parameterised on one value:

```sql
SELECT ITEM_NO, ITEM_TYPE, TITLE, REVISION, RELEASED_AT, ECN_NO, ECN_TITLE
FROM V_RELEASED_REVISIONS
WHERE ITEM_NO = :item_no
LIMIT 5
```

**Inputs:**

| Input | Mode | Description given to the model |
|---|---|---|
| `item_no` | Model-filled | The Teamcenter number to look up. Eleven characters, for example `P7000001042` for a part, `DU700001042` for a drawing, `T7000000217` for a CNC program or `SWI70000318` for a controlled document. Use exactly what the user gave; never invent or reformat one. |
| role, warehouse, database, schema | Fixed | — |

**Tool description:**

> Returns the current released revision of a Teamcenter item — a part, drawing, controlled document
> or CNC program — with the date it was released and the Engineering Change Notification that
> introduced it. Use when the user asks which revision to use, whether something is up to date, or
> why a revision changed. Do not use for work order status or for quality notifications.

**It queries a view, not a table.** `V_RELEASED_REVISIONS` filters to released revisions and unions
the four item types behind business-friendly column names, so "only released revisions" is enforced by
the database on every call. Written into the tool description instead, it would be a preference the
model usually honours ({{topic:hallucination#auditing-an-answer-claim-by-claim}} shows what "usually"
looks like when it fails).

```sql
CREATE OR REPLACE VIEW V_RELEASED_REVISIONS
AS
WITH items AS (
    SELECT PART_NO    AS ITEM_NO, 'Part'        AS ITEM_TYPE, DESCRIPTION AS TITLE, REVISION, RELEASED_AT
      FROM TC_PARTS        WHERE RELEASE_STATUS = 'Released'
    UNION ALL
    SELECT DRAWING_NO,           'Drawing',                   TITLE,                REVISION, RELEASED_AT
      FROM TC_DRAWINGS     WHERE RELEASE_STATUS = 'Released'
    UNION ALL
    SELECT PROGRAM_NO,           'CNC Program', 'CNC program for ' || PART_NO || ' on ' || MACHINE, REVISION, RELEASED_AT
      FROM TC_CNC_PROGRAMS WHERE RELEASE_STATUS = 'Released'
    UNION ALL
    SELECT DOC_NO,               'Document',                  TITLE,                REVISION, RELEASED_AT
      FROM TC_DOCUMENTS    WHERE STATUS = 'Released'
)
SELECT i.ITEM_NO, i.ITEM_TYPE, i.TITLE, i.REVISION, i.RELEASED_AT,
       e.ECN_NO, e.TITLE AS ECN_TITLE
FROM items i
LEFT JOIN TC_ECN_AFFECTED_ITEMS a ON a.ITEM_NO = i.ITEM_NO AND a.TO_REV = i.REVISION
LEFT JOIN TC_ECNS e               ON e.ECN_NO = a.ECN_NO AND e.STATUS = 'Released';
```

Looking up `P7000001042`, `T7000000217` and `DU700001042` in this view returns exactly three rows —
part revision C, program revision B, drawing revision C — each citing `ECN70000051`. If the program
ever comes back as revision A, fix the view, not anything downstream.

**The input description forbids inventing a number.** Without that sentence, "the valve block" gets a
plausible part number that does not exist; with it, the agent is far more likely to ask which part. The
model reads an input description at the moment it fills that input, which makes it unusually effective.

**It says what it is not for.** Exclusions keep it apart from the tools for work orders, efficiency,
lead time and notifications that follow.

### Testing the routing, not just the tool

A tool that is never chosen looks identical to a broken one, so test the orchestrator's choice
separately: a fixed set of questions, reading the activity map for each rather than the answers.

| # | Question | Expected |
|---|---|---|
| 1 | Which CNC program revision should machining use for `P7000001042`? | Calls the tool |
| 2 | Is `SWI70000318` up to date? | Calls the tool |
| 3 | Why did `T7000000217` change? | Calls the tool |
| 4 | What is the status of work order `100004521`? | Does **not** call it; says it cannot look that up |
| 5 | What does `SWI70000318` say about surface preparation? | Knowledge, not the tool |
| 6 | Which revision should I use for the valve block? | **Asks which part**; never invents a number |

Each failure points at its cause: 1–3 missing the tool means the description; 4–5 calling it means the
exclusions; 6 producing a part number means the input description. Re-run the set whenever a
tool is added: every new tool changes the choices for the old ones.

### Making the answer useful

The risk nobody asked about is shop paperwork still showing a superseded revision. One sentence in the
instructions covers it. Its second half matters most: an instruction that *mentions* work orders invites
the model to invent one.

```
When you report a released revision for an item being manufactured, say that shop paperwork may still
show an older revision and the operator should check before starting. Never name affected work orders
unless a tool has returned them.
```

## Design guidance

- **Fix everything the user did not say**, and never let the model supply a whole query.
- **Write an input description for every input, with an example.**
- **Point the tool at a view** and return the answer, not the source material.
- **Re-run the routing set after adding the next tool.**

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The tool is never chosen | Description does not match the user's words | Rewrite it in real users' words |
| It is chosen for unrelated questions | No exclusions; description too broad | Add "do not use for…" |
| Called with an invented part number | No input description forbidding invention | Describe the input with an example; forbid invention |
| Works in test, silently empty when shared | Connection identity | See {{topic:connauth}} |
| A new view returns nothing to the agent, with no error | The agent's role has no `SELECT` on it | Run the query in a worksheet *as the agent role* first; grant on the schema's future views |
| The agent calls it twice for one question | Two actions where one flow was needed | Wrap the sequence in an agent flow and expose one tool ({{module:automation-and-workflows}}) |

## Key terms

**Model-filled input** — a parameter the orchestrator supplies from the conversation.

**Fixed input** — a parameter set at configuration time; the model never sees it.

**Input description** — the guidance the model reads while filling a parameter.

**View** — a named query in Snowflake, and where constraints belong ({{topic:sfviews}}).
