## TL;DR

A **common table expression** (CTE) is a named query defined in a `WITH` clause and then used by the
query that follows. Snowflake's own definition: the `WITH` clause "defines one or more CTEs (common table
expressions) that can be used later in the statement." A **subquery** is a query nested inside another.
Use CTEs to break a question into steps you can name, read and run one at a time. Use an `EXISTS`
subquery when you need to know only *whether* a matching row exists.

## Why it matters

The SQL behind an agent's tool is reviewed by people who did not write it, often months later, and is
increasingly explained or edited by GitHub Copilot. A question that needs four joins and two filters,
written as one block, is hard to review and easy to break. You cannot see which filter belongs to which
step, and you cannot run half of it to check.

A CTE gives each step a name. *Replaced revisions*, then *open operations*, then the comparison. A
reviewer reads the names first and the SQL second, and anyone checking the query can run each step on its
own to see whether its rows look right. That is the habit {{topic:sfselect}} teaches about row counts,
applied one step at a time.

## How it works

### The WITH clause

```sql
WITH step_one AS (
    SELECT ...
),
step_two AS (
    SELECT ... FROM step_one ...
)
SELECT ... FROM step_two;
```

The rules that matter in practice, from Snowflake's reference:

- **A CTE can use the CTEs defined before it** in the same `WITH` clause, but not the ones after it. Write
  the steps in the order the reasoning runs.
- **It exists only for that one statement.** It is not stored, and the next query cannot see it. When the
  same steps are needed by many queries, that is a view ({{topic:sfviews}}).
- **A column list is optional** for an ordinary CTE: `WITH replaced (ITEM_NO, OLD_REV) AS (...)`. Aliasing
  inside the `SELECT` usually reads better.
- **Recursive CTEs exist**, for walking hierarchies such as a bill of materials. Snowflake recommends the
  `RECURSIVE` keyword only when one is actually recursive, and "strongly recommends omitting the keyword if
  none of the CTEs are recursive". A recursive CTE must use `UNION ALL` and can loop forever without a stop
  condition. You will not need one in this level.

### Subqueries

Snowflake classifies a subquery two ways. It is **correlated** if it "refers to one or more columns from
outside of the subquery", and **uncorrelated** if it is "an independent query". It is **scalar** if it
"returns a single value (one column of one row)", and **non-scalar** otherwise.

Three forms cover most needs:

| Form | Where | Example use |
|---|---|---|
| `EXISTS (...)` | `WHERE` | Work orders that have at least one open QN |
| `IN (...)` | `WHERE` | Parts that appear on a released ECN |
| Scalar `(SELECT ...)` | Anywhere a value goes (uncorrelated); `WHERE` (correlated) | A single threshold or reference value |

One rule bites: **"If a scalar subquery returns more than one row, a runtime error is generated."** A
correlated scalar subquery must also be one that Snowflake can tell will return one row.

### Which to reach for

Use a **CTE** when a step produces rows you will join, or when you want the step named and checkable. Use
**`EXISTS`** when you only need a yes or no per row. Unlike a join, it never multiplies rows, which is the
problem {{topic:sfjoins}} warns about. Avoid scalar subqueries over data you have not checked for
duplicates.

## In practice at Technik

**Which work orders are still running on a revision that a released ECN has replaced?** The scenario
contains two: `100004510` and `100004513`. Finding them means joining SAP operations to Teamcenter change
history. That is three steps, so it is three named parts.

```sql
WITH replaced AS (            -- revisions a released ECN has superseded
    SELECT a.ITEM_NO, a.FROM_REV AS OLD_REV, a.TO_REV AS NEW_REV, e.ECN_NO
    FROM TC_ECN_AFFECTED_ITEMS a
    JOIN TC_ECNS e ON e.ECN_NO = a.ECN_NO
    WHERE e.STATUS = 'Released'
      AND a.ITEM_TYPE IN ('Drawing', 'CNC Program')
),
open_ops AS (                 -- operations not yet confirmed
    SELECT WO_NO, OP_SEQ, OPERATION,
           DRAWING_NO, DRAWING_REV, CNC_PROGRAM_NO, CNC_PROGRAM_REV
    FROM SAP_WO_OPERATIONS
    WHERE STATUS IN ('OPEN', 'INPROC')
)
SELECT DISTINCT o.WO_NO, o.OPERATION, r.ITEM_NO,
       r.OLD_REV AS REV_ON_WORK_ORDER, r.NEW_REV AS CURRENT_REV, r.ECN_NO
FROM open_ops o
JOIN replaced r
  ON (r.ITEM_NO = o.DRAWING_NO     AND r.OLD_REV = o.DRAWING_REV)
  OR (r.ITEM_NO = o.CNC_PROGRAM_NO AND r.OLD_REV = o.CNC_PROGRAM_REV)
ORDER BY o.WO_NO;
```

| WO_NO | OPERATION | ITEM_NO | REV_ON_WORK_ORDER | CURRENT_REV | ECN_NO |
|---|---|---|---|---|---|
| `100004510` | Machining | `DU700001042` | B | C | `ECN70000051` |
| `100004513` | Machining | `T7000000217` | A | B | `ECN70000051` |

Each CTE can be checked alone. Run `replaced` by itself and you should see every revision change on a
released ECN. If `ECN70000051` is missing, the problem is upstream of the join. Run `open_ops` and compare
its count with what planners expect. Only then run the whole query. When it returns two rows, you know
why.

`DISTINCT` is there for a reason the scenario documents: `SAP_WO_OPERATIONS` has one row per
confirmation, so an operation can appear twice. {{topic:sfwindow}} removes those properly.

**Which work orders on `PRJ-2031` are blocked?** Technik has no blocked flag. A work order is blocked when
its current operation is `INPROC` and an open notification names that work order. *Whether one exists* is
exactly what `EXISTS` asks:

```sql
SELECT w.WO_NO, w.PART_NO, o.OPERATION
FROM SAP_WORK_ORDERS w
JOIN SAP_WO_OPERATIONS o
  ON o.WO_NO = w.WO_NO AND o.STATUS = 'INPROC'
WHERE w.PROJECT_ID = 'PRJ-2031'
  AND EXISTS (
      SELECT 1 FROM SAP_QUALITY_NOTIFICATIONS q
      WHERE q.WO_NO = w.WO_NO AND q.STATUS = 'Open'
  );
```

Write it as a join to the notifications table instead, and a work order with two open QNs is listed twice.
An agent counting the rows would then report one more blocked work order than there is.

## Design guidance

- **Name each step after what it holds**: `replaced`, `open_ops`, not `cte1`, `t2`.
- **One idea per CTE.** If a step needs a comment explaining two things, it is two steps.
- **Check each step's rows before the next one joins it.**
- **Use `EXISTS` for "has at least one"**, never a join followed by `DISTINCT` to undo the damage.
- **Keep scalar subqueries to values you know are unique**, or the query fails at run time.
- **Promote a CTE to a view** once a second query needs the same step.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| "Single-row subquery returns more than one row" | A scalar subquery hit duplicate rows, such as two confirmations of one operation | Deduplicate first ({{topic:sfwindow}}), or use `EXISTS` / `IN` |
| A work order appears twice in the result | A join to a table with several matches per key | Use `EXISTS`, or aggregate the other side first |
| A CTE "cannot be found" | It refers to a CTE defined after it | Reorder the `WITH` list |
| A recursive query runs until it times out | No stop condition in the recursive part | Add a depth limit such as `WHERE level < 10` |
| The same 30-line CTE is pasted into three tools | A shared step kept inside each query | Make it a view and query the view |

## Key terms

**CTE (common table expression)** — a named query in a `WITH` clause, visible only to its statement.

**Subquery** — a query nested inside another query.

**Correlated subquery** — one that refers to columns of the outer query, so it is evaluated per outer row.

**Scalar subquery** — one that returns exactly one value. More than one row is a runtime error.

**`EXISTS`** — true when the subquery returns at least one row. Never multiplies the outer rows.
