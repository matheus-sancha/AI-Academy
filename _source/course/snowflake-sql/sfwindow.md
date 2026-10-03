## TL;DR

An aggregate function collapses a group of rows into one. A **window function** keeps every row and adds
a value computed across related rows. In Snowflake's words, "the input is each row within a partition,
and the output is one row *per input row*." Three of them cover most of what an agent's queries need:
**`ROW_NUMBER`** for *the latest record per X*, **`RANK`** for league tables, and a **running `SUM`**. To
filter on their result, use **`QUALIFY`**.

## Why it matters

Technik's most important data flaw is a *latest record per X* problem. `SAP_WO_OPERATIONS` holds one row
per **confirmation**, not per operation. Where a partial posting was never reversed, an operation has two
rows, and only the one with the higher `CONFIRMATION_NO` counts. Sum the table as it stands and welding at
Plant 1 reads about **111%** efficiency. Keep the right row per operation and it reads about **89%**.

`GROUP BY` cannot fix this: it would merge the two rows, not choose between them. Choosing one row per
group while keeping its columns intact is what a window function is for. It is the step that every
efficiency figure the Production Assistant reports depends on.

## How it works

### The OVER clause

A window function is an ordinary function followed by `OVER (...)`, which has up to three parts:

```sql
ROW_NUMBER() OVER (
    PARTITION BY WO_NO, OP_SEQ      -- which rows belong together
    ORDER BY CONFIRMATION_NO DESC   -- their order inside the group
)                                   -- (plus an optional window frame)
```

- **`PARTITION BY`** splits the rows into groups. The function starts again in each group.
- **`ORDER BY`** orders rows within a group. Ranking functions require it.
- **The window frame** says which rows around the current one take part, for functions such as `SUM`.

### Three functions

| Function | Returns | Ties |
|---|---|---|
| `ROW_NUMBER()` | 1, 2, 3, … within each partition | Broken arbitrarily: tied rows still get different numbers |
| `RANK()` | Position, with ties sharing a rank | Leaves gaps: 1, 2, 2, 4 |
| `SUM(x) OVER (...)` | A total over the frame, such as a running total | — |

Snowflake's example of `RANK` gives seven days only five distinct ranks, "1, 2, 3, 5, 6", because two
pairs tied. And it warns about ties in general: "If multiple rows have the same value for the ORDER BY
columns, add additional columns as tiebreakers to ensure consistent, predictable results." A
`ROW_NUMBER` with a tied `ORDER BY` can pick a different row on each run, and an agent's answer then
changes for no visible reason.

### Frames: say what you mean

For a running total, give the frame explicitly:

```sql
SUM(ACTUAL_HOURS) OVER (ORDER BY OP_SEQ
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

`ROWS` counts physical rows. `RANGE` groups rows that share an `ORDER BY` value, so tied rows land in the
same step of the total. Snowflake cautions that "for some window functions, an ORDER BY clause implies a
window frame", and "recommends declaring window frames explicitly". Follow that advice. An implied frame
is a rule a reviewer has to remember.

### Filtering on a window: QUALIFY

A window function cannot go in `WHERE`, because `WHERE` runs first. Snowflake evaluates `FROM`, `WHERE`,
`GROUP BY`, `HAVING`, then the window functions, then `QUALIFY`. "QUALIFY does with window functions what
HAVING does with aggregate functions."

That order has a consequence worth knowing. **A `WHERE` filter decides which rows the window sees.**
`WHERE CONFIRMED_AT >= '2026-09-01'` followed by "keep the latest confirmation" keeps the latest of the
rows *inside the period*. If an operation's full re-posting landed in October and its partial posting in
September, the September row survives as if it were final. Deduplicate first, in its own step, and filter
afterwards.

## In practice at Technik

**Welding efficiency at Plant 1 for September.** *Efficiency %* is routing hours ÷ actual hours × 100. The
routing hours repeat on every confirmation row. The actual hours on a partial posting are only what was
posted at the time. So the duplicates inflate routing hours far more than actual hours:

| | Routing hours | Actual hours | Efficiency |
|---|---|---|---|
| Every row, as stored | 416.0 | 375.0 | 110.9% |
| One row per operation | 320.0 | 360.0 | 88.9% |

The query that produces the second row deduplicates in a CTE, then filters ({{topic:sfcte}}):

```sql
WITH confirmed AS (
    SELECT WO_NO, OP_SEQ, ROUTING_HOURS, ACTUAL_HOURS, CONFIRMED_AT
    FROM SAP_WO_OPERATIONS
    WHERE OPERATION = 'Welding'
      AND CONFIRMATION_NO IS NOT NULL
    QUALIFY ROW_NUMBER() OVER (PARTITION BY WO_NO, OP_SEQ
                               ORDER BY CONFIRMATION_NO DESC) = 1
)
SELECT ROUND(SUM(c.ROUTING_HOURS) / SUM(c.ACTUAL_HOURS) * 100, 1) AS EFFICIENCY_PCT
FROM confirmed c
JOIN SAP_WORK_ORDERS w ON w.WO_NO = c.WO_NO
WHERE w.PLANT = 'Plant 1'
  AND c.CONFIRMED_AT >= '2026-09-01' AND c.CONFIRMED_AT < '2026-10-01';
```

Three details carry the correctness. The partition is `WO_NO, OP_SEQ`, which identifies one operation.
The order is on `CONFIRMATION_NO`, which is unique, so there are no ties to break. And the
`OPERATION = 'Welding'` filter is safe before the window because both confirmations of an operation share
it. The date filter, which could split them, waits until after.

**Hours consumed so far on work order `100004521`**, with each operation still on its own row. This one
reads the deduplicated view that {{topic:sfviews}} builds:

```sql
SELECT OPERATION_SEQ, OPERATION, ACTUAL_HOURS,
       SUM(ACTUAL_HOURS) OVER (ORDER BY OPERATION_SEQ
                               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS HOURS_TO_DATE
FROM V_WORK_ORDER_OPERATIONS     -- already one row per operation
WHERE WORK_ORDER = '100004521'
ORDER BY OPERATION_SEQ;
```

**Parts with the most open quality notifications.** Rank the counts with `RANK()`. If two parts tie on
nine, both are second and nobody is third. An agent asked for "the top three" should be told that, which
is why the rank column belongs in the result, not just the order.

The deduplication step is the one to put in a view ({{topic:sfviews}}), once, so no tool or knowledge
query ever sums the raw table again.

## Design guidance

- **Partition by the key that identifies one thing**, here the work order and operation sequence.
- **Order by something unique**, or add a tiebreaker column.
- **Deduplicate in its own step, before any filter that could split a group.**
- **Write window frames out in full.**
- **Use `QUALIFY` to keep the top row**, rather than nesting a subquery to filter on a row number.
- **Return the rank, not just the order**, when ties are possible.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Efficiency above 100% for a whole operation type | Duplicate confirmations summed | Keep one row per operation with `ROW_NUMBER` and `QUALIFY` |
| The "latest" row changes between runs | Tied `ORDER BY` values in `ROW_NUMBER` | Add a unique tiebreaker |
| A partial posting survives deduplication | A `WHERE` date filter ran before the window and dropped the later row | Deduplicate first, filter after |
| An error as soon as a window function appears in `WHERE` | `WHERE` runs before window functions | Use `QUALIFY` |
| A running total jumps two rows at once | An implied or `RANGE` frame over tied values | Declare `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` |
| "Top three" returns four parts | `RANK` ties | Decide whether the answer is ranks or rows, and say so |

## Key terms

**Window function** — returns one value per input row, computed over a set of related rows.

**Partition** — the group of rows a window function works within, set by `PARTITION BY`.

**Window frame** — which rows around the current one take part, set with `ROWS` or `RANGE`.

**`QUALIFY`** — filters on window function results, as `HAVING` does for aggregates.

**Latest record per X** — `ROW_NUMBER()` partitioned by X, ordered newest first, kept where it equals 1.
