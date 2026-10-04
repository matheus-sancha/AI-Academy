## TL;DR

`SELECT` names the columns, `FROM` the table, `WHERE` the rows, `ORDER BY` their order and `LIMIT` how many
come back. Name only the columns you need, filter as early as you can, and **count the rows before anyone
relies on them**. Without `ORDER BY`, Snowflake returns "an unordered set", so a `LIMIT` on its own returns
an arbitrary few. An agent cannot tell a truncated answer from a complete one.

## Why it matters

A tool behind the Production Assistant is a fixed query with a few parameters ({{topic:addconnector}}).
Whatever that query returns is all the model knows. If the query quietly returns ten rows of forty-one, the
agent reports ten, fluently. If a filter matches nothing because a value is spelled differently, it reports
that there is nothing. Neither looks like an error. The only defence is knowing, before the tool ships, how
many rows the query *should* return, and checking that it does.

## How it works

### The clauses, in the order you write them

```sql
SELECT   <columns>          -- what comes back
FROM     <table or view>    -- where from
WHERE    <condition>        -- which rows
ORDER BY <columns>          -- in what order
LIMIT    <n>;               -- how many at most
```

Snowflake's query syntax page lists many more clauses (`WITH`, `JOIN`, `GROUP BY`, `HAVING`, `QUALIFY` and
others), and the rest of this module adds them one at a time. These five are enough to read a table.

### Choose the columns

`SELECT *` returns every column. Snowflake also accepts `SELECT * EXCLUDE (...)` to drop a few, and `RENAME`
to rename them. For a tool, name the columns. Storage is columnar ({{topic:sfarch}}), the model reads every
column it is given, and a column added to the table next month will not appear in a tool's output unasked.

An alias, `ACTUAL_HOURS AS HOURS_BOOKED`, becomes the column's name in the result. Snowflake warns: "Do not
assign a column alias that is the same as the name of another column referenced in the query." Aliases and
unquoted identifiers are case-insensitive; double quotes preserve case.

### Filter with WHERE

`WHERE` keeps the rows whose condition is true, combined with `AND`, `OR` and `NOT`. Two habits prevent most
wrong answers:

- **Use half-open date ranges.** `CONFIRMED_AT >= '2026-09-01' AND CONFIRMED_AT < '2026-10-01'` includes all
  of 30 September. `BETWEEN '2026-09-01' AND '2026-09-30'` stops at midnight on the 30th when the column
  holds a time.
- **Filter on values you have seen.** Run `SELECT DISTINCT OPERATION FROM SAP_WO_OPERATIONS` once and copy the
  value, rather than typing what you expect it to be.

### Order, then limit

"Without an ORDER BY clause, the results returned by SELECT are an unordered set. Running the same query
repeatedly against the same tables might result in a different output order every time." So `LIMIT 10`
without `ORDER BY` means *any ten*, and the ten can change between runs. With `ORDER BY`, it means *the
first ten by that order*, which is a question someone can actually ask.

### Count before you trust

Before a result is shared or wired into a tool, run the same `FROM` and `WHERE` with `COUNT(*)`:

```sql
SELECT COUNT(*) FROM ... WHERE ...;
```

Then compare it with something you know: the planners' count, last month's, the number of work orders on
the project. A count of zero is a filter problem until proven otherwise. A count far above what you expected
is the sign of a duplicating join ({{topic:sfjoins}}) or a table whose grain you have misread.

## In practice at Technik

The welding-efficiency question starts here: *which welding operations were confirmed in September?*

```sql
SELECT WO_NO, OP_SEQ, WORK_CENTER, ROUTING_HOURS, ACTUAL_HOURS, CONFIRMED_AT
FROM TECHNIK_DW.OPS.SAP_WO_OPERATIONS
WHERE OPERATION = 'Welding'
  AND CONFIRMED_AT >= '2026-09-01' AND CONFIRMED_AT < '2026-10-01'
ORDER BY CONFIRMED_AT DESC
LIMIT 50;
```

Six columns of seventeen, filtered on operation and month, newest first, at most fifty rows. Before trusting
it, count:

```sql
SELECT COUNT(*)
FROM TECHNIK_DW.OPS.SAP_WO_OPERATIONS
WHERE OPERATION = 'Welding'
  AND CONFIRMED_AT >= '2026-09-01' AND CONFIRMED_AT < '2026-10-01';
-- 41
```

Forty-one rows across both plants, so `LIMIT 50` returns them all. Had the limit been 10, an agent asked
"how many welding confirmations were there in September?" would have counted the rows it was given and
answered ten. The table has no plant column; filtering to Plant 1 needs `SAP_WORK_ORDERS`, which is the next
lesson ({{topic:sfjoins}}).

Write the count down. Every later step in this module is checked against it, and the welding question will
turn out to have more than one way of being wrong.

The same discipline applies to a tool's parameters. A *Work order status* tool that filters on
`WO_NO = :work_order` should return one row per operation of that work order. Test it on `100004521` and
count the rows against the routing before giving it to the agent.

## Design guidance

- **Name the columns** in every tool query. No `SELECT *`.
- **Pair every `LIMIT` with an `ORDER BY`**, and make the limit larger than any answer you expect.
- **Tell the agent when a result is capped**: return the total count alongside the rows, or say in the
  tool's description that the list is the top *n*.
- **Use half-open ranges for dates and times.**
- **Copy filter values from the data**, not from memory.
- **Count, then compare** with a number you trust, before the query is shared or shipped.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent reports exactly ten of something, every time | A `LIMIT 10` truncated the result | Raise the limit and return the total, or say the list is capped |
| The same question returns a different "top five" each run | `LIMIT` without `ORDER BY` | Order by a column that defines "top" |
| The agent says there were no welding operations last month | The filter value does not match the data's spelling | Copy the value from `SELECT DISTINCT` |
| September's totals miss the last day | `BETWEEN` on a timestamp ends at midnight | Use `>=` the first day and `<` the next month |
| A tool's output gains a column nobody reviewed | `SELECT *` picked up a new column | Name the columns |

## Key terms

**Projection** — the `SELECT` list: the columns a query returns.

**Predicate** — a condition in `WHERE` that a row must satisfy to be kept.

**Half-open range** — a range that includes its start and excludes its end, as in `>= start AND < end`.

**Row count check** — `COUNT(*)` over the same `FROM` and `WHERE`, compared with a number you trust.
