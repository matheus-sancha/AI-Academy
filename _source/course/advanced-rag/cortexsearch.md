## TL;DR

Cortex Search is Snowflake's managed search over text that already sits in Snowflake. One `CREATE CORTEX SEARCH SERVICE`
statement builds a hybrid index, keyword plus vector, with a semantic rerank, and keeps it fresh as the source table
changes, with no embedding code and no index to run. That is the appeal and the trade: you choose from four
embedding models and a few scoring controls, and the rest is Snowflake's. Two facts matter most for an agent.
The service searches with its owner's rights, so the source query is the access boundary. And a refreshing index has a
lag, a cost that runs while idle and a rate limit that returns 429.

## Why it matters

{{topic:hybrid}} showed what an Azure AI Search index asks of you: fields, semantic configuration, a pipeline. For
data already in Snowflake, such as quality notifications, Cortex Search offers the same shape of retrieval with the
work taken out, and some control with it. Choosing between them is a design decision, and so is which rows a service
may expose, and to whom.

## How it works

### One statement

<!-- volatile verified=2026-11 -->
The page's example creates a service on a text column, with `ATTRIBUTES` for the other columns to index so they can be
returned and used as filters, a `WAREHOUSE` that builds and refreshes it, a `TARGET_LAG` for how often it checks the
source, an `EMBEDDING_MODEL` and a source query. The index is built during the statement, which can take up to several
hours on a large table, and Snowflake recommends a dedicated warehouse no larger than MEDIUM per service. A query then
goes to the service, in SQL or the REST API, with optional filters on the attribute columns.
<!-- /volatile -->

Under the hood each query uses vector search, keyword search and a semantic rerank of the best results. The page says
you can customise scoring with numeric boosts, time decays, component weights, or by disabling reranking.

### The embedding choice

<!-- volatile verified=2026-11 -->
Four hosted models are listed. The default, `snowflake-arctic-embed-m-v1.5`, is English-only with 768 dimensions and a
512-token context window. `snowflake-arctic-embed-l-v2.0` is multilingual with 1,024 dimensions and 512 tokens, its
`-8k` variant takes 8,192 tokens, and `voyage-multilingual-2` takes 32,000. Availability differs by cloud region. When
a value exceeds the model's window, Cortex Search truncates it before embedding, but the keyword side uses the full
text. Snowflake recommends splitting text into chunks of at most 512 tokens, about 385 English words, and offers
`SPLIT_TEXT_RECURSIVE_CHARACTER` and `COUNT_TOKENS` to do it.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
The 512-token advice rests on research the page does not cite ("research shows" a smaller chunk typically helps). It is
the only chunk-size recommendation in this module's sources, and it is for this service and these models
({{topic:chunking}}).
<!-- /unknown -->

### Refresh, cost and limits

<!-- volatile verified=2026-11 -->
A service is refreshed like a dynamic table, and its source query must be a candidate for incremental refresh, which
guards against runaway embedding cost. An optional primary key on text columns lets each refresh process only changed
rows instead of re-embedding everything, with periodic full rebuilds that do not re-embed unchanged data. Embedding is
billed per token for each inserted or updated row. Serving is billed per gigabyte of indexed data per month, including
the embeddings, while the service is available, even with no queries. Warehouse compute, storage and cloud services
add to it. Indexing suspends itself after five consecutive refresh failures. The optional `AUTO_SUSPEND`, a preview
feature with a 30-minute minimum, stops serving after inactivity. The first query then waits for the resume, and
concurrent queries during it get HTTP 429 with a `Retry-After` header.

Limits include fewer than 400 million rows, about 20 queries a second per service and 140 across an account, no
cloning, no zero data retention, and a stale service must be recreated. The source tables must not be modified or dropped
while it runs, so stop the service first.
<!-- /volatile -->

### Rights

<!-- volatile verified=2026-11 -->
The creator needs a Cortex database role (`CORTEX_USER` or `CORTEX_EMBED_USER`), the create privilege on the schema,
`SELECT` on the sources and `USAGE` on the warehouse, and change tracking must be on for every underlying object. A
caller needs only `USAGE` on the service, its database and its schema. The page's important note is that a service
searches with owner's rights, the same security model as other Snowflake objects that run with owner's rights.
<!-- /volatile -->

The consequence is direct. A caller does not need `SELECT` on the source, since it is the service that reads it.
Whatever the source query selects, any role with `USAGE` can retrieve.

## In practice at Technik

Quality notifications are data that already lives in Snowflake, and *has this porosity been seen before?* is a question a
keyword search misses when the earlier QN says "gas pits" ({{topic:embeddings}}). The scenario's `300001234`,
`300001211` and `300001219` are the near-duplicates a search should group. A service for them:

*Adapted from the create and grant examples on the Cortex Search page, for `SAP_QUALITY_NOTIFICATIONS` through a view:*

```sql
CREATE OR REPLACE CORTEX SEARCH SERVICE qn_search
  ON DESCRIPTION
  ATTRIBUTES STATUS, OPERATION, PRIORITY
  PRIMARY KEY (QN_NO)
  WAREHOUSE = <your-refresh-warehouse>
  TARGET_LAG = '1 day'
AS (
  SELECT QN_NO, DESCRIPTION, STATUS, OPERATION, PRIORITY
  FROM V_QUALITY_NOTIFICATIONS
);

GRANT USAGE ON CORTEX SEARCH SERVICE qn_search TO ROLE TECHNIK_AGENT_RO;
```

The agent role already holds `USAGE` on `TECHNIK_DW` and `OPS`, and `SELECT` on the QN table, so here the grant adds a
way of finding rows and no new access. For a role without that `SELECT`, the same grant opens a back door. Owner's
rights makes the source query the place a rule lives, as the views do elsewhere in the capstone. Whatever
`V_QUALITY_NOTIFICATIONS` returns is what any grantee can retrieve: which plants, which statuses, which text. The
injected descriptions on `300001267` and `300001270` are rows like any other: indexing them makes them retrievable, and
they come back as data that may carry an instruction ({{topic:ctxsecurity}}). A view can drop them, which is a
decision about the corpus and not a defence.

The rest are choices. `OPERATION`, `STATUS` and `PRIORITY` are attributes so the agent can ask only for open cladding
QNs. A day of `TARGET_LAG` hides a QN raised this morning until the next refresh, which suits a similar-QN question and
not a status one. And the 429 is a client duty: the agent needs backoff.

The scenario's controlled documents are not in Snowflake, only their metadata in `TC_DOCUMENTS`. For SharePoint
documents that points to Azure AI Search ({{topic:vector}}). For QN text, Cortex Search is the shorter path.

<!-- unknown since=2026-11 -->
`V_QUALITY_NOTIFICATIONS` is not one of the capstone's views, and nobody ran the statement. The page does not say whether
a view over `SAP_QUALITY_NOTIFICATIONS` qualifies for incremental refresh, nor whether `QN_NO` is the text type a primary key
requires. Check both, and measure retrieval on your own labelled questions before you trust it ({{topic:rageval}}).
<!-- /unknown -->

## Design guidance

- **Treat the source query as the access boundary.** Owner's rights expose whatever it returns.
- **Build services over views** that hold the rules, not over raw tables.
- **Split long text to 512 tokens or fewer**, and count tokens with the model's own tooling.
- **Set a primary key** to get incremental refresh, and keep it unique.
- **Choose `TARGET_LAG` from the question's freshness need**, and note the idle serving cost.
- **Add backoff for 429** on the client, and on resume if you use `AUTO_SUSPEND`.
- **Stop the service before changing its source tables.**

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A role reads rows it could not query directly | The service runs with owner's rights | Narrow the source query |
| A long document matches on words it never embedded | The embedding is truncated, and the keyword side is not | Split to 512 tokens |
| `CREATE` takes hours | The index is built during the statement | Use a dedicated, modest warehouse |
| A new QN is not found | The service refreshes on `TARGET_LAG` | Shorten the lag, or use a tool for fresh rows |
| Refreshes stop, with no new rows | Five consecutive failures suspend indexing | Read `INDEXING_ERROR`, fix the query and resume |
| Queries return 429 | The rate limit, or a resume in progress | Retry with backoff |

## Key terms

**Cortex Search service**: a Snowflake object that builds and serves a hybrid index over a source query.

**Owner's rights**: the security model in which a service acts with its owner's privileges, not the caller's.

**Target lag**: how far behind its source a service may fall before it refreshes.

**Attribute**: an indexed column that can be returned and used as a filter.
