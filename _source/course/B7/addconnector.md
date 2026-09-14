## TL;DR

Adding a connector action as a tool is four decisions, not one: **which action**, **which inputs the
model fills and which you fix**, **what the description says**, and **what the result looks like when
it comes back**. Get those right and the orchestrator calls the tool at the right moment with the
right values. Get the second one wrong and the model is writing your SQL for you.

## Why it matters

This is the lesson the lab is built on, and the four decisions above are where nearly every problem
comes from. A tool that works perfectly when you test the action directly can still be called at the
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

The lab builds `Get released revision`. Here it is as a specification.

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
be a preference the model usually honours — and the B1 exercise showed you what "usually" looks like
when it fails.

**The input description forbids inventing a number.** Without that sentence, a user asking about
"the valve block" gets a plausible eleven-character part number that does not exist. With it, the
agent is far more likely to ask which part they mean. Instructions in an input description are read
at exactly the moment the model is filling that input, which makes them unusually effective.

**It says what it is not for.** The assistant will eventually have tools for work orders,
efficiency, lead time and notifications. Exclusions are what keep six tools from blurring into each
other.

> [!TIP]
> Test the routing separately from the tool. Ask five questions that *should* call it, five that
> should not, and one deliberately ambiguous. The activity map tells you what the orchestrator
> actually did. A tool that works but is never chosen looks identical, from the outside, to a tool
> that is broken.

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
| The agent calls it twice for one question | Two actions where one flow was needed | Wrap the sequence in an agent flow and expose one tool (B9) |

## Key terms

**Model-filled input** — a parameter the orchestrator supplies from the conversation.

**Fixed input** — a parameter set at configuration time and not visible to the model.

**Input description** — the guidance the model reads while filling a parameter. High leverage.

**Activity map** — Copilot Studio's view of what an agent did in a turn: which tools, which inputs,
which results (B5).

**View** — a named query in Snowflake. Where constraints belong (B10).
