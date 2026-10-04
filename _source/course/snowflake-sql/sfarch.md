## TL;DR

Snowflake keeps **storage**, **compute** and **cloud services** in separate layers. Data sits in
**databases** and **schemas**, and every query runs on a **virtual warehouse**, a compute cluster that
consumes credits while it runs and can suspend itself when idle. The Production Assistant reads
`TECHNIK_DW.OPS` on its own warehouse, `TECHNIK_AGENT_WH`, so its queries neither slow anyone else down nor
hide inside anyone else's bill.

## Why it matters

An agent's tool sends SQL to Snowflake on every question that needs data. Each of those queries needs
somewhere to run, and that somewhere costs money while it is awake. Which warehouse a tool uses, how big it
is and how fast it goes back to sleep are design decisions, and they are made once, when the tool is wired
up ({{topic:sfconnector}}).

The layers also explain two things you will meet in the rest of this module. Data is stored in columns,
which is why selecting only the columns you need is more than tidiness ({{topic:sfselect}}). And access is
checked by a separate services layer before any query runs, which is why a role, not a person, is the unit
an agent is given ({{topic:sfroles}}).

## How it works

### Three layers

Snowflake describes its architecture as "a hybrid of traditional shared-disk and shared-nothing database
architectures", built from three components:

| Layer | What it does | What you control |
|---|---|---|
| **Database storage** | Holds the data. Snowflake reorganises loaded data "into its internally optimized, compressed, columnar format" and divides every table into micro-partitions | Nothing about the physical layout; Snowflake manages it |
| **Compute** | Runs queries on virtual warehouses, massively parallel clusters | Which warehouse, its size, when it suspends |
| **Cloud services** | Coordinates everything "from sign-in to query dispatch": authentication and access control, metadata, query parsing and optimisation | Roles and grants ({{topic:sfroles}}) |

Storage is shared by every warehouse. Compute is not: "Each virtual warehouse is an independent compute
cluster that doesn't share compute resources with other virtual warehouses. As a result, each virtual
warehouse has no effect on the performance of other virtual warehouses."

### Databases, schemas and names

Data is organised as database → schema → table or view. A fully qualified name gives all three, such as
`TECHNIK_DW.OPS.SAP_WORK_ORDERS`. A shorter name is resolved against the session's current database and
schema, which you can inspect with `SELECT CURRENT_DATABASE(), CURRENT_SCHEMA();`. Every database has a
default schema, `PUBLIC`.

### Warehouses

Snowflake's tutorial creates its warehouse like this:

```sql
CREATE OR REPLACE WAREHOUSE sf_tuts_wh WITH
   WAREHOUSE_SIZE='X-SMALL'
   AUTO_SUSPEND = 180
   AUTO_RESUME = TRUE
   INITIALLY_SUSPENDED=TRUE;
```

`AUTO_SUSPEND` is the number of idle seconds before the warehouse stops, and `AUTO_RESUME` restarts it when a
query arrives. The tutorial is plain about the cost: "A running virtual warehouse consumes Snowflake
credits." A suspended one does not run, so it consumes none. Storage is billed separately, for the data
held.

<!-- unknown since=2026-10 -->
The curated pages do not give Snowflake's credit rates per warehouse size, or the minimum time a resumed
warehouse is billed for. Both decide what one agent question costs. Check them with whoever owns Technik's
Snowflake account before sizing a warehouse for an agent.
<!-- /unknown -->

## In practice at Technik

Technik's SAP and Teamcenter data is replicated nightly into one database and one schema:

| Thing | Technik's | Notes |
|---|---|---|
| Database | `TECHNIK_DW` | The replicated warehouse data |
| Schema | `OPS` | All 13 tables, `SAP_*`, `TC_*` and `FAT_RESULTS` |
| Agent warehouse | `TECHNIK_AGENT_WH` | Used only by agents and MCP servers |
| Engineers' warehouse | `TECHNIK_DEV_WH` | Where engineers explore the data with their own roles |

The separate agent warehouse earns its keep three ways. An engineer running a heavy exploratory join on
`TECHNIK_DEV_WH` cannot make the assistant slow, because the two clusters share nothing. The assistant's
credit consumption shows up under one warehouse name, so its running cost is a number someone can report.
And the agent's role can be granted usage of that warehouse alone ({{topic:sfroles}}).

The assistant's traffic is bursty: a planner asks three questions in a minute, then nobody asks anything
for half an hour. That shape favours an extra-small warehouse with auto-resume on and a short auto-suspend.
A tool's queries are narrow and filtered, so they rarely need a larger one. If answers get slow, look at
the query first ({{topic:sfselect}}); a bigger warehouse makes a bad query finish sooner, not cost less.

The nightly replication has one consequence an agent must not hide. Everything in `TECHNIK_DW.OPS` is as
of last night, so an operation confirmed this morning is not there yet. The assistant's instructions say so
whenever it reports work order status.

## Design guidance

- **Give agents their own warehouse.** Isolation, a cost you can read, and a grant you can scope.
- **Start at the smallest size** with auto-resume on and a short auto-suspend. Resize only on evidence.
- **Use fully qualified names** in a tool's fixed SQL, so it does not depend on the session's defaults.
- **Fix the query before resizing the warehouse.** Size buys speed, not efficiency.
- **Say how fresh the data is.** Replicated data has an age, and the agent's answer should carry it.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A tool fails with an object-not-found error that works in your worksheet | The tool's SQL uses a short name, and the connection's default database or schema differs from yours | Fully qualify every name in the tool's SQL |
| The assistant slows down whenever engineers run reports | Agents and people share one warehouse | Give agents their own warehouse |
| The agent warehouse's credit use is far above what its traffic suggests | Auto-suspend set long, so the cluster idles between bursts | Shorten `AUTO_SUSPEND` |
| Someone proposes a larger warehouse because a tool is slow | A query scanning far more than it returns | Narrow the columns and filters first |
| The agent reports a work order as still in welding after it was confirmed this morning | The data is replicated nightly | State the data's age in the answer |

## Key terms

**Virtual warehouse** — a compute cluster that runs queries and consumes credits while it runs.

**Auto-suspend / auto-resume** — stopping a warehouse after idle seconds, and restarting it when a query
arrives.

**Cloud services layer** — the layer that handles sign-in, access control, metadata and query optimisation.

**Fully qualified name** — `database.schema.object`, independent of the session's current context.

**Micro-partition** — the unit Snowflake divides every table into, in a compressed, columnar format.
