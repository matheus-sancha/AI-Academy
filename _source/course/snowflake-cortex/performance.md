## TL;DR

An agent's queries are small, repeated and many, so the cost is rarely one slow query. It is the warehouse seconds that
every call buys. The two curated pages give three habits: read one query in its profile, watch all of an agent's queries
as a group, and size the warehouse from what it runs. They give no numbers on purpose, since the warehouse page says it
"does not provide specific or absolute numbers", so this lesson teaches what to measure. The capstone's own warehouse
setting is where it shows.

## Why it matters

The capstone's warehouse, `TECHNIK_AGENT_WH`, is X-Small with `AUTO_SUSPEND = 60`. The warehouse page bills a minimum of
60 seconds each time compute resources start, and it drops a warehouse's cache when it suspends. Its own example of
the trap is a workload with gaps of two or three minutes between queries and an auto-suspend of one or two: the warehouse
is "in a continual state of suspending and resuming", and each resume is billed the minimum. An assistant is used at a
person's pace, which is bursts of a few queries and then quiet. The setting may be right. But nothing in the capstone
checks it, and slow SQL, a cold cache and a churning warehouse look the same to the user: a slow answer.

## How it works

### Reading one query

<!-- volatile verified=2026-11 -->
Query History, under Monitoring in Snowsight, lists the last 14 days of queries. You always see your own. To see others
you need `ACCOUNTADMIN`, or `MONITOR` or `OPERATE` on the warehouse they used, or `IMPORTED PRIVILEGES` on the
`SNOWFLAKE` database. Filters include warehouse, duration, SQL text and query tag, which is whatever the `QUERY_TAG`
session parameter held. Details and profile are unavailable once a query is older than 14 days, and the page calls their
depth "best-effort".
<!-- /volatile -->

The Query Profile shows the plan as operator nodes, each with its share of the run time. Four panes help: where time
went (processing, disk and network waits), query insights, statistics for I/O, pruning and spilling, and the most
expensive nodes, those over 1% of the time. The page names four problems and their signs:

- **An exploding join**: a `Join` node produces orders of magnitude more rows than it consumes.
- **`UNION` without `ALL`**: an extra `Aggregate` sits on top of the `UnionAll`.
- **Spilling**: intermediate results overflow memory to local and then remote disk. The remedies are a larger warehouse or
  smaller batches.
- **Inefficient pruning**: *Partitions scanned* is a large share of *Partitions total*. Pruning needs the table's storage
  order to correlate with the filtered columns.

Nodes from earlier lessons appear by name: `WindowFunction` computes the window, `Flatten` processes a `VARIANT`, and a
`TableScan` lists its "extracted variant paths".

### Watching the group

<!-- volatile verified=2026-11 -->
Grouped Queries, a tab of the same page, groups statements by a parameterized query hash and shows, per group, the
executions, failures, latency at p50, p90 and p99, and executions a minute. It covers 14 days, a query can take up to
180 minutes to appear, and seeing it needs `ACCOUNTADMIN`, `IMPORTED PRIVILEGES` on `SNOWFLAKE` or the
`GOVERNANCE_VIEWER` database role. The page aims it at workloads of thousands of near-identical statements, and says it
includes every query. The `AGGREGATE_QUERY_HISTORY` view holds the same data for SQL.
<!-- /volatile -->

### Sizing the warehouse

<!-- volatile verified=2026-11 -->
Credits follow warehouse size, the number of clusters and run time. X-Small bills 1 credit per full hour, each size up
generally doubles that, the first 60 seconds are the minimum, and billing is per second after. Resizing a running
warehouse changes nothing for queries already running. It helps larger, more complex queries and queued ones, but "larger
is not necessarily faster" for small simple ones, and it is not the fix for concurrency: that is more warehouses, or a
multi-cluster warehouse on Enterprise Edition.
<!-- /volatile -->

Each running warehouse caches the table data it reads, and suspending it, or shrinking it, drops the cache. So
auto-suspend is a trade of credits against warm reads. Snowflake recommends a low value, "5 or 10 minutes or less", that
still matches the gaps in the workload. It also advises running homogeneous queries on one warehouse, because mixed
complexity makes the load hard to read. Table size matters more than row count, and filters and joins count too.

## In practice at Technik

*From [`seed/03_access.sql`, lines 5–7](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/seed/03_access.sql#L5-L7):*

```sql
CREATE WAREHOUSE IF NOT EXISTS TECHNIK_AGENT_WH
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Used only by agents and MCP servers.';
```

The comment is the good part. A warehouse used only by agents matches the page's advice on homogeneous work, and it means
the *Warehouse* filter in history is an agent filter. The tag filter is not available, because the server sets no
`QUERY_TAG`, so the three tools can be told apart only by their SQL text. {{topic:sfcost}} returns to tags.

To read the efficiency tool's query, open its profile and expect a `TableScan` of `SAP_WO_OPERATIONS`, a `Join` to
`SAP_WORK_ORDERS`, and a `WindowFunction` for the view's {{topic:qualify}}. The question the pages do not answer is
whether the tool's `PLANT`, `OPERATION` and period filters cut rows before that window or after it. The profile
does. Look at the scan's partitions scanned against total, and at whether a `Filter` sits above the `TableScan`. The
page's reading of a high scanned share with a `Filter` above it is that a different data organisation might help.

The seed has 133 rows, so every plan is trivial and nothing here can be measured on it. This is method, for the volume the
reader's own tables reach.

<!-- unknown since=2026-11 -->
Nobody measured the capstone's traffic, its resumes per hour or any profile. Whether Grouped Queries counts a tool's
statements as one group is also open: the page describes statements that "vary only by user ID", and says nothing of
SQL a model generates or of how the connector fills in parameters.
<!-- /unknown -->

## Design guidance

- **Start from the profile, not the SQL text.** The scanned-to-total ratio and the biggest node say where the time went.
- **Watch the group.** For repeated tool SQL, p99 latency and executions a minute are the figures, not any one query.
- **Keep agents on their own warehouse, and tag their queries**, so history can isolate them.
- **Match `AUTO_SUSPEND` to the real gaps**, and change it only after counting resumes.
- **Resize for query size, not for concurrency.** Concurrency needs more warehouses.
- **Check pruning before blaming the warehouse.** A big warehouse cannot prune a table that is stored the wrong way.
- **Capture the profile while you tune.** It is gone after 14 days.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Idle minutes dominate an assistant's credits | Each resume bills 60 seconds, and auto-suspend is shorter than the gaps | Set it from measured gaps |
| The first question after a quiet spell is slow | The suspend dropped the cache and the resume takes time | Accept it, or trade credits for warmth |
| A resize did not help concurrent queries | It affects only queued and new queries, and is not for concurrency | Add warehouses, or go multi-cluster |
| Grouped Queries shows nothing for the agent | It lags up to 180 minutes, or the role lacks the privilege | Wait, or use a privileged role |
| A query's profile is gone | It is older than 14 days | Capture it while tuning |
| A secure view's profile is empty inside | Its internals are hidden, even from the owner | Profile the same `SELECT` on the base tables |

## Key terms

**Query Profile**: the plan of one executed query as operator nodes, with the time each took.

**Pruning**: skipping parts of a table that a filter rules out, seen as partitions scanned against total.

**Parameterized query hash**: the identifier that groups statements differing only in values.

**Auto-suspend**: the idle time after which a warehouse stops, which also drops its cache.

**Scaling up and out**: resizing a warehouse, or adding clusters to a multi-cluster one.
