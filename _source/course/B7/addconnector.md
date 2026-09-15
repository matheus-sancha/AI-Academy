## TL;DR

Adding a connector action as a tool is four decisions, not one: **which action**, **which inputs the
model fills and which you fix**, **what the description says**, and **what the result looks like when
it comes back**. Get those right and the orchestrator calls the tool at the right moment with the
right values. Get the second one wrong and the model is writing your SQL for you.

## Why it matters

The four decisions above are where nearly every problem with a tool comes from. A tool that works perfectly when you test the action directly can still be called at the
wrong time, with a part number the model invented, returning three hundred rows nobody needed.

## How it works

### 1. Choose the action

One action, one job. If the thing you want takes two calls — submit a statement, then fetch its
result — wrap them in an agent flow and expose *that* as the tool, rather than hoping the
orchestrator sequences two tools correctly. It sometimes will. You do not want to depend on it.

### 2. Decide what the model fills in

Every input is either **model-filled** or **fixed**. The rule is simple and worth applying strictly:

> The model fills in what the *user* said. Everything else is configuration.

| Input | Who supplies it | Why |
|---|---|---|
| Part number | Model | It came from the question |
| Item type (part, drawing, document, CNC program) | Model | It came from the question |
| Snowflake role, warehouse, database, schema | Fixed | Nothing the user says should change these |
| Row limit | Fixed | A bound is a bound |
| The SQL statement itself | **Fixed** | See below |

Leaving the statement model-filled is the mistake worth naming explicitly. It turns the tool into
"run arbitrary SQL as the agent's role", which means the blast radius of a prompt injection is now
everything that role can do. It is also unpredictable in the boring case: the model writes slightly
different SQL each time and you cannot reason about the results. Fix the statement; parameterise the
values it takes.

<!-- volatile verified=2026-09 -->
In Copilot Studio, after choosing the connector and action you can mark each input as filled by the
model or set to a fixed value, and give each one a description. The labels and layout change between
releases; the distinction itself does not. Follow the linked documentation for the current screen.
<!-- /volatile -->

### 3. Write the description

Three pieces of text matter, in this order of impact:

**Tool name** — a verb phrase in the user's vocabulary. `Get released revision`, not `SnowflakeQuery3`.

**Tool description** — what it returns, when to use it, when not to. Two or three sentences.

**Input descriptions** — what a good value looks like, with an example. These are how the model knows
that a part number is `P7000001042` and not "the valve block". Skipping them is the most common cause
of a tool called with nonsense.

### 4. Shape the result

The result is read by the model as text. So:

- return few columns, with names a human would use;
- return few rows — filter and aggregate in SQL;
- return the *answer*, not the raw material for it. If the question is "which revision is released",
  return one row, not the whole revision history and a hope.

## In practice at Technik

Carla asks which CNC program revision machining should use for `P7000001042`. The tool that answers
it is `Get released revision`. Here it is as a specification.

**Fixed SQL**, parameterised on two values:

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

Three things about that specification are worth spelling out.

**It queries a view, not a table.** `V_RELEASED_REVISIONS` filters to released revisions and unions
the four item types behind business-friendly column names. The rule "only released revisions" is
therefore enforced by the database on every call. Written into the tool description instead, it would
be a preference the model usually honours — and
[Hallucinations & Grounding](../B1/hallucination.html#auditing-an-answer-claim-by-claim) shows what
"usually" looks like when it fails.

```sql
CREATE OR REPLACE VIEW V_RELEASED_REVISIONS
COMMENT = 'Current released revision of every Teamcenter item, with the ECN that introduced it. One row per item.'
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
ever comes back as revision A, the filter is wrong, and the view is the place to fix it, not anywhere
downstream. The view's `COMMENT` travels with it, so anyone reading the schema — including the agent
role — sees what it is for.

**The input description forbids inventing a number.** Without that sentence, a user asking about
"the valve block" gets a plausible eleven-character part number that does not exist. With it, the
agent is far more likely to ask which part they mean. Instructions in an input description are read
at exactly the moment the model is filling that input, which makes them unusually effective.

**It says what it is not for.** The assistant will eventually have tools for work orders,
efficiency, lead time and notifications. Exclusions are what keep six tools from blurring into each
other.

### Testing the routing, not just the tool

A tool that works but is never chosen looks identical, from the outside, to a tool that is broken. So
test the orchestrator's choice separately, with a fixed set of questions, and check the activity map
for every one rather than reading the answers.

| # | Question | Expected |
|---|---|---|
| 1 | Which CNC program revision should machining use for `P7000001042`? | Calls the tool |
| 2 | What is the latest released revision of drawing `DU700001042`? | Calls the tool |
| 3 | Is `SWI70000318` up to date? | Calls the tool |
| 4 | Why did `T7000000217` change? | Calls the tool |
| 5 | What revision is `P7000001088` at? | Calls the tool |
| 6 | What is the status of work order `100004521`? | Does **not** call it; says it cannot look that up |
| 7 | Show me open quality notifications on cladding. | Does **not** call it |
| 8 | What does `SWI70000318` say about surface preparation? | Knowledge, not the tool |
| 9 | Who owns `SOP70000101`? | Knowledge, not the tool |
| 10 | What is our overtime policy? | Out of scope entirely |
| 11 | Which revision should I use for the valve block? | **Asks which part** — never invents a number |

The failures point straight at their cause. If 1–5 miss the tool, the description is the problem. If
6–10 call it, the exclusions are. If 11 produces a part number, the input description is. Keep the set
and re-run it whenever a tool is added, because every new tool changes the choices for the old ones.

### Making the answer useful

Answering the question asked is not the same as being useful. Carla's real risk is the one she did
not ask about: shop paperwork still showing a superseded revision. A sentence in the agent's
instructions covers it:

```
When you report a released revision for a part, drawing or CNC program, and the conversation is
about manufacturing that item, say plainly that shop paperwork may still show an older revision and
that the operator should check before starting. Never state which work orders are affected unless a
tool has returned that information.
```

> [!IMPORTANT]
> The last sentence is doing real work. An instruction that *mentions* work orders invites the model
> to produce one, and it will produce a plausible, invented work order number. Until the agent has a
> tool that returns work order data, the honest answer is a caution, not a list.

## Design guidance

- **Fix everything the user did not say.**
- **Never let the model supply a whole query.**
- **Write an input description for every input, with an example.**
- **Point the tool at a view.** Constraints belong in SQL.
- **Return the answer, not the source material.**
- **Have the agent confirm before acting**, for anything that changes state.
- **Re-test routing after adding the next tool.** Adding a tool changes the choices for all the others.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The tool is never chosen | Description does not match the user's words | Rewrite using real questions from real users |
| It is chosen for unrelated questions | No exclusions; description too broad | Add "do not use for…" |
| Called with an invented part number | No input description, or no instruction against inventing | Describe the input, give an example, forbid invention; have the agent ask |
| Returns the superseded revision | Query not filtered on release status | Fix the view. Not the prompt |
| Enormous results, slow answers | No limit, all columns | Limit and project in SQL |
| Works in test, silently empty when shared | Connection identity | See [Connections & Authentication](connauth.html) |
| A newly created view returns nothing to the agent, with no error | The agent's role has no `SELECT` on it | Run the tool's query in a worksheet *as the agent role* before involving Copilot Studio; grant on the schema's future views so new ones are covered |
| The answer mentions work orders nobody looked up | An instruction talks about work orders the agent has no tool for | Say explicitly that it must not name records a tool has not returned |
| The agent calls it twice for one question | Two actions where one flow was needed | Wrap the sequence in an agent flow and expose one tool (B9) |

## Key terms

**Model-filled input** — a parameter the orchestrator supplies from the conversation.

**Fixed input** — a parameter set at configuration time and not visible to the model.

**Input description** — the guidance the model reads while filling a parameter. High leverage.

**Activity map** — Copilot Studio's view of what an agent did in a turn: which tools, which inputs,
which results (B5).

**View** — a named query in Snowflake. Where constraints belong (B10).
