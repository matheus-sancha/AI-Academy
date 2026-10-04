## TL;DR

An aggregate function "takes multiple rows (actually, zero, one, or more rows) as input and produces a single
output": `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`. `GROUP BY` produces one output row per group, and `HAVING`
filters those groups as `WHERE` filters rows. A metric that is a ratio is **a ratio of sums**, never an
average of per-row ratios. And an aggregate is only as right as the rows under it, so check their grain
first.

## Why it matters

Most questions the Production Assistant answers are metrics: efficiency, lead time, open QNs per project.
Each one ends as an aggregation, and an aggregation hides its inputs. Forty-one rows go in and one number
comes out, with nothing in that number to show that two of the rows were the same operation. The agent sees
only the output, so the aggregation is where wrong data stops being visible.

## How it works

### From rows to one row

Without `GROUP BY`, an aggregate collapses the whole result to one row:

```sql
SELECT COUNT(*), SUM(ACTUAL_HOURS), AVG(ACTUAL_HOURS), MIN(CONFIRMED_AT), MAX(CONFIRMED_AT)
FROM ...
```

Two rules about `NULL` decide what these return:

- **`NULL`s are skipped.** Snowflake's example: the average of `1`, `5` and `NULL` is `3`, because "only the
  two non-NULL values are used" in numerator and denominator. So `COUNT(*)` counts rows and
  `COUNT(ACTUAL_HOURS)` counts rows where hours are present. The difference is your unconfirmed operations.
- **No rows still means one row.** Aggregates "always return exactly one row, even when the input contains
  zero rows", and "typically, if the input contains zero rows, the output is NULL." A filter that matches
  nothing gives a `NULL` total, not a zero.

### GROUP BY

`GROUP BY` "groups rows with the same group-by-item expressions and computes aggregate functions for the
resulting group". Every column in the `SELECT` list is either aggregated or grouped. `GROUP BY ALL` groups by
every non-aggregated item in the `SELECT` list, which keeps the two in step when columns change.

### HAVING

`HAVING` filters groups after aggregation, so it can test an aggregate, which `WHERE` cannot. Snowflake
evaluates `WHERE` before `GROUP BY` and `HAVING` after it ({{topic:sfwindow}}). Filter rows in `WHERE`,
since fewer rows are cheaper to group, and keep `HAVING` for conditions on the groups themselves.

### Ratios: sum first, then divide

*Efficiency %* is routing hours ÷ actual hours × 100. There are two ways to write it, and only one is the
definition:

```sql
SUM(ROUTING_HOURS) / SUM(ACTUAL_HOURS) * 100     -- ratio of sums: the definition
AVG(ROUTING_HOURS / ACTUAL_HOURS) * 100          -- average of ratios: a different metric
```

The second gives a two-hour operation the same weight as a forty-hour one, so a few short operations that
ran fast can lift it far above the true figure. It also divides by zero on any row booked with no actual
hours.

## In practice at Technik

**Welding efficiency by plant for September**, over the rows {{topic:sfjoins}} established:

```sql
SELECT w.PLANT,
       COUNT(*)                                                   AS ROWS_USED,
       SUM(o.ROUTING_HOURS)                                       AS ROUTING_HOURS,
       SUM(o.ACTUAL_HOURS)                                        AS ACTUAL_HOURS,
       ROUND(SUM(o.ROUTING_HOURS) / SUM(o.ACTUAL_HOURS) * 100, 1) AS EFFICIENCY_PCT
FROM TECHNIK_DW.OPS.SAP_WO_OPERATIONS o
JOIN TECHNIK_DW.OPS.SAP_WORK_ORDERS w ON w.WO_NO = o.WO_NO
WHERE o.OPERATION = 'Welding'
  AND o.CONFIRMED_AT >= '2026-09-01' AND o.CONFIRMED_AT < '2026-10-01'
GROUP BY ALL
ORDER BY w.PLANT;
```

| `PLANT` | `ROWS_USED` | `ROUTING_HOURS` | `ACTUAL_HOURS` | `EFFICIENCY_PCT` |
|---|---|---|---|---|
| Plant 1 | 26 | 416.0 | 375.0 | 110.9 |
| Plant 2 | 15 | 240.0 | 250.0 | 96.0 |

The rows add up to the 41 {{topic:sfselect}} counted, so the join lost nothing. The query is correct SQL, and
an agent would report *welding at Plant 1 ran at 110.9% efficiency in September*.

It is wrong. A whole operation type beating its routing by 11% for a month is the kind of number that should
send you back to the rows, and one more aggregate shows why:

```sql
SELECT COUNT(*) AS ROWS_USED, COUNT(DISTINCT o.WO_NO, o.OP_SEQ) AS OPERATIONS
-- same FROM, JOIN and WHERE, plus AND w.PLANT = 'Plant 1'
-- ROWS_USED 26, OPERATIONS 20
```

Twenty-six rows describe twenty operations, so some operations appear more than once, and their hours were
summed more than once. Which row of each to keep is a different kind of question, one `GROUP BY` cannot
answer, because it merges rows rather than choosing between them. {{topic:sfwindow}} answers it and the
figure falls to 88.9%. Keep `ROWS_USED` in the output anyway: it is the number that made the problem
visible.

**Lead time by part, where it means something.** Lead time is calendar days from release to technical
completion. An average over one work order is an anecdote, so `HAVING` keeps parts with at least three:

```sql
SELECT PART_NO,
       COUNT(*)                                          AS WORK_ORDERS,
       ROUND(AVG(DATEDIFF('day', RELEASED_AT, COMPLETED_AT)), 1) AS AVG_LEAD_TIME_DAYS
FROM TECHNIK_DW.OPS.SAP_WORK_ORDERS
WHERE STATUS = 'TECO'
GROUP BY ALL
HAVING COUNT(*) >= 3
ORDER BY AVG_LEAD_TIME_DAYS DESC;
```

The `WHERE` keeps completed work orders, since an open one has no completion date. The `HAVING` drops thin
groups. Returning `WORK_ORDERS` beside the average lets the agent say *across 7 work orders* instead of
presenting the figure as if it were a law.

## Design guidance

- **Check the grain before you aggregate**: `COUNT(*)` against `COUNT(DISTINCT <key>)`.
- **Write ratios as a ratio of sums**, exactly as the metric is defined.
- **Return the count with every average and ratio**, so the agent can say how much evidence it rests on.
- **Filter rows in `WHERE`, groups in `HAVING`.**
- **Prefer `GROUP BY ALL`** so grouping cannot drift from the `SELECT` list.
- **Decide what an empty result means**, and make the tool say *no data* rather than return a bare `NULL`.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Efficiency above 100% for a whole operation type | Rows repeat: duplicate confirmations or a fan-out join | Compare `COUNT(*)` with distinct operations; deduplicate ({{topic:sfwindow}}) |
| Efficiency far higher as `AVG` than as a ratio of totals | Average of per-row ratios | Divide the sums |
| A tool returns `NULL` and the agent says efficiency is zero | No rows matched, and an aggregate over zero rows is `NULL` | Return the row count; describe `NULL` as *no data* |
| An error naming a column "not in GROUP BY" | A non-aggregated column is missing from the grouping | Add it, or use `GROUP BY ALL` |
| A `WHERE SUM(...) > ...` fails | Aggregates are not available in `WHERE` | Move the condition to `HAVING` |

## Key terms

**Aggregate function** — takes zero or more rows, returns one value.

**Grain** — what one row of a table or result represents, such as one operation or one confirmation.

**`GROUP BY`** — one output row per distinct combination of the grouped expressions.

**`HAVING`** — filters groups after aggregation.

**Ratio of sums** — total numerator divided by total denominator; the definition of a rate over many rows.
