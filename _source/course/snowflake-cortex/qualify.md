## TL;DR

{{topic:sfwindow}} used `QUALIFY` for one job, keeping the latest row per key. The two curated pages say more.
`QUALIFY` runs after aggregates and window functions, so it filters on both and can use select-list aliases. It also
works as an audit: the clause that hides stale rows can list them. A window frame either counts rows (`ROWS`) or
measures values (`RANGE`), and the two disagree exactly where timestamps tie. A window's own `ORDER BY` takes no column
numbers. And `QUALIFY` is Snowflake's syntax, not ANSI's.

## Why it matters

`V_WORK_ORDER_OPERATIONS` hides Technik's double-confirmation flaw with one `QUALIFY` clause, and the efficiency tool
reads 88.9% and not 110.9% because of it. Two things follow. Something has to check that the view still hides what it
should, because a view that quietly handles a flaw also hides when the flaw changes. And agents are often asked for more
than one row: hours to date, a recent average, a share. Those depend on a frame and on how ties fall, and a wrong choice
returns a plausible number, not an error.

## How it works

### Where QUALIFY sits

The `QUALIFY` page lists the evaluation order: `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `WINDOW`, `QUALIFY`, `DISTINCT`,
`ORDER BY`, `LIMIT`. From that list and the page's usage notes:

- **`QUALIFY` is to window functions what `HAVING` is to aggregates.** Both can sit in one query: `HAVING` filters the
  groups, then `QUALIFY` filters what the windows computed.
- **It needs a window function**, in the select list or in its own predicate. The predicate can also hold aggregates and
  subqueries, under `HAVING`'s rules.
- **It can use select-list aliases.** Put `ROW_NUMBER() OVER (...) AS row_num` in the select list and write
  `QUALIFY row_num = 1`. The row number comes back with the row, which is how {{topic:sfwindow}} advised returning ranks.
- **`DISTINCT`, `ORDER BY` and `LIMIT` come after it**, so none can stand in for it. `LIMIT 1` keeps one row of the
  result, and `QUALIFY` keeps one per partition.
- **It is a reserved word, and not ANSI.** Nothing on the page says another engine will accept it.

### The window's own ORDER BY

The `ORDER BY` inside `OVER` orders only the rows that function processes. The usage page calls it "separate and
distinct" from the query's. It takes no column numbers: in `OVER (PARTITION BY 1 ORDER BY 2)` the 2 is "interpreted as
the constant 2", not the second column. Ordinals work in the outer `ORDER BY`, so this is a slip that generated SQL can
carry, and a window ordered by a constant leaves nothing to decide which row is latest.

Two kinds of function need the clause: ranking functions such as `RANK`, `DENSE_RANK` and `CUME_DIST`, and any function
with an explicit frame. For some functions an `ORDER BY` also implies a frame, and Snowflake recommends declaring frames
explicitly for that reason.

### Frames: rows count, ranges measure

A `ROWS` frame is a physical offset: `2 PRECEDING` is the two rows before this one. A `RANGE` frame is a distance in
the `ORDER BY` value, a number or an interval, so `INTERVAL '3 hours' FOLLOWING` takes the rows stamped within three
hours after this one. Under `RANGE`, `CURRENT ROW` means every row with the same `ORDER BY` value.

The usage page shows what that does to tied values. For prices of 2.00, 3.00, 3.00 and 3.50, a `ROWS` running sum climbs
2.00, 5.00, 8.00, 11.50, while the `RANGE` version gives both tied rows the same 8.00. Frames are also cut off at the
partition's edge: the page's moving average over a short history has a window "only 3 rows wide" on the third day.

A partition plus a frame gives a running total that resets in each group. An empty `OVER ()` is valid and puts one
total on every row, and `RATIO_TO_REPORT(x) OVER (PARTITION BY ...)` divides each value by its partition's sum.

## In practice at Technik

**Auditing what the view hides.** Run against the raw table, this lists every operation that was confirmed more than
once:

*Adapted from the aggregate-in-the-predicate pattern on the `QUALIFY` page, for `SAP_WO_OPERATIONS`:*

```sql
SELECT WO_NO, OP_SEQ, CONFIRMATION_NO, ACTUAL_HOURS, CONFIRMED_AT
FROM SAP_WO_OPERATIONS
QUALIFY COUNT(*) OVER (PARTITION BY WO_NO, OP_SEQ) > 1
ORDER BY WO_NO, OP_SEQ, CONFIRMATION_NO;
```

The seed holds 133 rows for 127 operations, and the query returns 12: six operations with two postings each, all
welding at Plant 1. An evaluation set or a pipeline can pin that number. Zero means the flaw has left the replica. More
means new duplicates that the view will handle without saying so.

**Hours to date, and the last few.** Welding at Plant 1 in September is 20 confirmed operations once the view has
deduplicated them, 360.0 actual hours, the figure behind 88.9%. This query computes two running totals and two averages,
so each frame can be compared with its twin:

*Adapted from the frame examples on the window functions page, for `V_WORK_ORDER_OPERATIONS`:*

```sql
SELECT WORK_ORDER, OPERATION_SEQ, CONFIRMED_AT, ACTUAL_HOURS,
  SUM(ACTUAL_HOURS) OVER (ORDER BY CONFIRMED_AT, WORK_ORDER, OPERATION_SEQ
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS HOURS_TO_DATE_ROWS,
  SUM(ACTUAL_HOURS) OVER (ORDER BY CONFIRMED_AT
    RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS HOURS_TO_DATE_RANGE,
  AVG(ACTUAL_HOURS) OVER (ORDER BY CONFIRMED_AT, WORK_ORDER, OPERATION_SEQ
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS AVG_LAST_3_OPS,
  AVG(ACTUAL_HOURS) OVER (ORDER BY CONFIRMED_AT
    RANGE BETWEEN INTERVAL '2 days' PRECEDING AND CURRENT ROW) AS AVG_LAST_2_DAYS
FROM V_WORK_ORDER_OPERATIONS
WHERE PLANT = 'Plant 1' AND OPERATION = 'Welding' AND OPERATION_STATUS = 'Confirmed'
  AND CONFIRMED_AT >= '2026-09-01' AND CONFIRMED_AT < '2026-10-01'
ORDER BY CONFIRMED_AT, WORK_ORDER, OPERATION_SEQ;
```

Four of its rows tell the story:

| Operation | Hours | To date, `ROWS` | To date, `RANGE` | Last 3 ops | Last 2 days |
|---|---|---|---|---|---|
| `100004528` / `0020`, 4 Sep | 20.0 | 20.0 | 20.0 | 20.0 | 20.0 |
| `100004527` / `0020`, 5 Sep | 17.5 | 37.5 | 53.5 | 18.75 | 17.83 |
| `100004527` / `0030`, 5 Sep | 16.0 | 53.5 | 53.5 | 17.83 | 17.83 |
| `100004535` / `0020`, 21 Sep | 15.5 | 285.5 | 285.5 | 17.83 | 16.75 |

The first row shows the edge: its "last three" is one row. The two 5 September rows were confirmed at the same minute,
so `RANGE` gives both 53.5, while `ROWS` needs the tiebreaker to say which comes first. Here `WORK_ORDER, OPERATION_SEQ`
puts 17.5 before 16.0. Without it the middle value could be 37.5 or 36.0, the unstable ordering the usage page warns
about. On 21 September the last three operations reach back to the 18th, because nothing was confirmed on the 20th, and
the last two days do not. "The last three confirmations" is `ROWS`, and "the last two days" is `RANGE`.

<!-- unknown since=2026-11 -->
Nobody ran these two queries on Snowflake. They are adapted from the pages' examples, and the figures are worked out
by hand from the seed's rows. The page shows `RANGE` with an interval only in the `FOLLOWING` direction, so `PRECEDING`
is that form read backwards. It does not say whether a row exactly two days back is inside the frame. Here it is, and the
16.75 depends on it.
<!-- /unknown -->

## Design guidance

- **Audit with the clause you filter with.** A `QUALIFY COUNT(*) OVER (...) > 1` over the raw table pins what a
  deduplicating view hides.
- **End every window `ORDER BY` in a unique key**, and never use a column number.
- **Choose `ROWS` for "the last N things" and `RANGE` for a span of time**, and put the unit in the column name.
- **Write the frame out**, rather than relying on the one an `ORDER BY` implies.
- **Keep `QUALIFY` in views and tools you own.** It is not ANSI, so SQL that leaves Snowflake needs rewriting.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A running total changes between runs | Tied values in the window `ORDER BY` under `ROWS` | End the `ORDER BY` in a unique key |
| Tied rows show the same running total | `RANGE` treats every row with the same value as the current row | Use `ROWS` when each row is a thing |
| An ordering has no effect | A column number in the window's `ORDER BY` is read as a constant | Name the column |
| `QUALIFY` on an aggregate alone is rejected | It needs a window function | Use `HAVING` for aggregates |
| The first rows of a moving average look low | The frame is cut off at the partition's edge | Leave those rows out when the window must be full |
| A view's duplicates grow and nothing complains | The view's `QUALIFY` handles them silently | Pin the audit query's row count |

## Key terms

**`QUALIFY`**: the clause that filters on window function results, evaluated after `HAVING` and before `DISTINCT`.

**`ROWS` frame**: a frame measured in physical rows from the current one.

**`RANGE` frame**: a frame measured in distance of the `ORDER BY` value, which keeps tied rows together.

**Tiebreaker**: a further `ORDER BY` column that makes the order, and so the result, repeatable.

**Moving average**: an average over a sliding frame, which is smaller at the partition's start.
