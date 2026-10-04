## TL;DR

A join "combines rows from two tables to create a new combined row". An **inner join** keeps only rows that
match; a **left join** keeps every row of the left table and fills the missing side with `NULL`. Before
joining, know how many rows on each side share a key. Joining *many* to *one* keeps the row count. Joining
*many* to *many* multiplies it, and every `SUM` over the result is inflated with no error to warn you.

## Why it matters

Most questions the Production Assistant answers cross a table boundary. Plant lives on the work order, hours
on its operations, defects on its quality notifications. So nearly every tool's SQL contains a join, and a
join is where a correct-looking query starts returning a wrong number.

The failure is quiet. A join that duplicates rows produces a result with the right columns, plausible values
and a few more rows than it should. Summed, those rows give a total that is simply too high. The agent
reports it with confidence, because nothing in the result says *these rows repeat*. Only a row count
compared before and after the join says so.

## How it works

### Inner and left

```sql
FROM SAP_WO_OPERATIONS o
JOIN SAP_WORK_ORDERS w ON w.WO_NO = o.WO_NO          -- inner: matching rows only
```

Snowflake's reference defines it row by row: "For each row of o1, a row is produced for each row of o2 that
matches according to the ON condition." A row with no match produces nothing.

```sql
FROM SAP_WORK_ORDERS w
LEFT JOIN SAP_QUALITY_NOTIFICATIONS q ON q.WO_NO = w.WO_NO   -- left: every work order
```

A left join returns the inner join's rows plus one "for each row of o1 that has no matches in o2", with the
columns from the right table set to `NULL`. Use it when *none* is a valid answer: work orders with no QN
still belong in a list of work orders. Right and full outer joins exist too; a left join with the tables in
the order you think about them covers nearly every case.

A cross join pairs every row with every row, a *Cartesian product*: "If the first table has N rows and the
second table has M rows, then the result is N x M rows." You will rarely write one on purpose. A join whose
condition matches far more than intended behaves like a partial one.

### Conditions on a left join belong in ON

Filter the right-hand table in `ON`, not in `WHERE`. Snowflake: "Specifying the predicate in the ON subclause
avoids the problem of accidentally filtering rows with NULL values when using a WHERE clause". A `WHERE
q.STATUS = 'Open'` after a left join discards every work order without a QN, because their `STATUS` is
`NULL`, and the left join silently becomes an inner one.

### Cardinality decides the row count

Before writing a join, say how many rows on each side share the key:

| Left → right | Example | Rows after the join |
|---|---|---|
| Many → one | Operations → their work order | Unchanged |
| One → many | Work order → its operations | One per operation |
| Many → many | Operations → QNs, both on `WO_NO` | Each operation row repeated once per QN |

The first two are safe if you meant them. The third is almost never what anyone meant, because the two
sides are related only through the work order they share.

## In practice at Technik

**Filtering by plant.** {{topic:sfselect}} counted 41 welding confirmations in September across both
plants. `SAP_WO_OPERATIONS` has no plant column, so join to the work order:

```sql
SELECT o.WO_NO, o.OP_SEQ, o.ROUTING_HOURS, o.ACTUAL_HOURS, o.CONFIRMED_AT
FROM TECHNIK_DW.OPS.SAP_WO_OPERATIONS o
JOIN TECHNIK_DW.OPS.SAP_WORK_ORDERS w ON w.WO_NO = o.WO_NO
WHERE o.OPERATION = 'Welding'
  AND o.CONFIRMED_AT >= '2026-09-01' AND o.CONFIRMED_AT < '2026-10-01'
  AND w.PLANT = 'Plant 1';
-- 26 rows
```

Many operations to one work order, so no row is repeated. Count without the plant filter and you get 41
again, which proves the join neither added nor lost rows. Those 26 rows feed {{topic:sfagg}}.

**The join that duplicates.** Someone then asks for *welding hours on work orders that have a quality
notification*, and adds the QNs:

```sql
SELECT o.WO_NO, o.OP_SEQ, o.ROUTING_HOURS, o.ACTUAL_HOURS, q.QN_NO
FROM TECHNIK_DW.OPS.SAP_WO_OPERATIONS o
JOIN TECHNIK_DW.OPS.SAP_WORK_ORDERS w ON w.WO_NO = o.WO_NO
LEFT JOIN TECHNIK_DW.OPS.SAP_QUALITY_NOTIFICATIONS q ON q.WO_NO = o.WO_NO
WHERE o.OPERATION = 'Welding'
  AND o.CONFIRMED_AT >= '2026-09-01' AND o.CONFIRMED_AT < '2026-10-01'
  AND w.PLANT = 'Plant 1';
-- 31 rows
```

Twenty-six became thirty-one. Work order `100004527` has three welding rows and two QNs, `300001241` and
`300001248`, so its three rows became six. Work order `100004533` has two rows and two QNs, so its two
became four. Every hour on those work orders is now counted twice, and a `SUM(ACTUAL_HOURS)` over this
result is wrong by exactly those hours.

The fix depends on the question. To flag operations whose work order has a QN, ask *whether* one exists
with `EXISTS`, which never multiplies rows ({{topic:sfcte}}). To show QN counts beside hours, count QNs per
work order first and join that one-row-per-work-order result. Either way, the count goes back to 26.

## Design guidance

- **State each join's cardinality** in a comment, `-- many ops : one work order`, before you run it.
- **Count before and after every join.** An unexplained change is a bug until you can explain it.
- **Never join two "many" tables on a shared parent.** Reduce one side to one row per key first.
- **Use a left join when "none" is an answer**, and put conditions on the right-hand table in `ON`.
- **Join on keys**, not on descriptions or names that happen to match.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Hours or counts rise when a column is added from another table | A many-to-many join repeated rows | Aggregate or test with `EXISTS` before joining |
| Work orders with no QN vanish from a "QNs per work order" list | Inner join, or a `WHERE` on the right table after a left join | Left join, condition in `ON` |
| A count of work orders exceeds the number of work orders | Counting rows of a one-to-many join | Count distinct keys, or join after aggregating |
| A query returns millions of rows from two small tables | A missing or wrong join condition, effectively a cross join | Check every table has a correct `ON` |
| `NULL` hours appear in a joined result | The left join found no match on the right | Expected for a left join; decide whether `NULL` means zero |

## Key terms

**Inner join** — returns only rows with a match on both sides.

**Left outer join** — returns every left-hand row, with `NULL` where the right side has no match.

**Cardinality** — how many rows on each side share a key: one-to-one, one-to-many, many-to-many.

**Fan-out** — the multiplication of rows when one row matches several, inflating sums and counts.

**Cartesian product** — every row paired with every row; N × M rows.
