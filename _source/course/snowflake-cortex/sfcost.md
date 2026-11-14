## TL;DR

An agent on Snowflake spends credits through two meters, and they have different controls. **Warehouse credits** are what a
resource monitor watches and can suspend. **AI credits**, from Cortex AI functions and Cortex Agents, are billed in tokens
and are outside a resource monitor's reach: the page says plainly that it cannot track "serverless features and AI
services". A **budget** watches them and only notifies. A **per-user quota** can block, and revoking the right database role
is the older lever. Attribution depends on a `QUERY_TAG` and on usage views. The capstone as shipped sets no monitor, no tag
and no revocation, so none of these controls exists until the reader adds them.

## Why it matters

{{topic:performance}} ended on a warehouse that bills a minimum of 60 seconds each time it resumes. That is the smaller
bill. A single `AI_CLASSIFY` over a table or a long Cortex Agent run can cost more than the warehouse that hosts the
statement, and the tool built to stop a runaway warehouse does not see it. A team that sets a resource monitor and
considers the spend capped has capped one meter of two.

## How it works

### Warehouse credits: the resource monitor

<!-- volatile verified=2026-11 -->
A resource monitor controls credit use by warehouses and the cloud services behind them. It has a credit quota, a schedule
that resets at 12:00 AM UTC, and triggers at percentages of the quota. A trigger does one of three things: `NOTIFY`,
`SUSPEND`, which lets running statements finish, or `SUSPEND_IMMEDIATE`, which cancels them. A monitor may have one of each
suspending action and five notifications, and thresholds above 100% are allowed. An account-level monitor covers every
warehouse, but a warehouse below it can have one monitor of its own, and whichever reaches its suspend threshold first
wins. Only `ACCOUNTADMIN` creates one. Notifications are off until someone enables them.
<!-- /volatile -->

The page says a monitor is not for "precise limits". A query that starts before a threshold can finish after the suspend,
so it recommends a 90% threshold and, for tight control, one warehouse per monitor. And a suspended warehouse stays
suspended until the interval resets or someone raises the quota, which turns a spending control into an outage.

### AI credits: tokens

<!-- volatile verified=2026-11 -->
The functions bill credits from tokens, with a token about four characters, and the rates sit in a Service Consumption
Table that this lesson did not read. A generative function pays for input and output. The embedding functions, which
include `AI_SIMILARITY`, pay for input only. `AI_CLASSIFY`, `AI_FILTER` and several others add a prompt of their own, so the
bill is larger than your text. For `AI_CLASSIFY`, the labels, descriptions and examples count "as input tokens for each
record processed". The warehouse bills too, and Snowflake recommends one no larger than `MEDIUM`. Cortex Agent orchestration
is billed in tokens, and Cortex Search by index size and time ({{topic:cortexagents}}).
<!-- /volatile -->

A count makes the second point. The seed's notification `300001234` has a description of 143 characters, roughly 36
tokens. The call in {{topic:aisql}} attaches four labels and a task description of about 123 characters, roughly 31
tokens, to every row. So the instructions cost about as much as the text, before the function's own prompt. That is
arithmetic on the page's four-characters rule, not a measured bill.

### Seeing it, and tagging it

<!-- volatile verified=2026-11 -->
The usage view lists function, model, credits, query, user, role names, query tag and warehouse, with up to five minutes of
latency and one row per hour of a long query. The page advises setting `QUERY_TAG` to attribute cost by project or team.
Requests through the REST API are not itemized.
<!-- /volatile -->

*Adapted from the daily-credits query on the Managing AI Function costs page:*

```sql
SELECT DATE_TRUNC('day', START_TIME) AS usage_date,
       FUNCTION_NAME, MODEL_NAME,
       SUM(CREDITS) AS total_credits,
       COUNT(DISTINCT QUERY_ID) AS query_count
FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AI_FUNCTIONS_USAGE_HISTORY
WHERE START_TIME >= DATEADD('day', -30, CURRENT_TIMESTAMP())
GROUP BY 1, 2, 3
ORDER BY usage_date DESC, total_credits DESC;
```

### Capping it: budgets, quotas and roles

<!-- volatile verified=2026-11 -->
A budget is a monthly credit limit for the account, or for a custom group of objects chosen by tag or one by one. It "is
used for alerting and notification purposes only", and it can call a stored procedure of yours at a threshold. Its supported
services include Cortex Agents, listed as orchestration and tool usage. The table does not list AI functions, though the
account budget is described as covering all credit usage. A budget can lag by up to 6.5 hours, and the hourly option raises
the budget's own compute cost twelvefold.

A **per-user quota** can block. Once a user reaches the limit, Snowflake stops new AI requests from them, counted within
minutes. No enforcement happens until a limit is set, and one quota covers warehouse compute or AI domains, never both.
<!-- /volatile -->

The older lever is the role. `USE AI FUNCTIONS` and `CORTEX_USER` are both granted to `PUBLIC` by default, so every role can
call the functions until someone revokes them and grants a narrower role. `AI_FUNCTIONS_USER` is not granted to `PUBLIC`, and
it covers the scalar functions but not `AI_AGG` and `AI_SUMMARIZE_AGG`. The management page's per-user limit works by revoking
such a role from users over their limit, and warns that any other role carrying `CORTEX_USER` bypasses it.

## In practice at Technik

*From [`seed/03_access.sql`, lines 13–21](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/seed/03_access.sql#L13-L21):*

```sql
GRANT USAGE ON WAREHOUSE TECHNIK_AGENT_WH TO ROLE TECHNIK_AGENT_RO;
GRANT USAGE ON DATABASE  TECHNIK_DW       TO ROLE TECHNIK_AGENT_RO;
GRANT USAGE ON SCHEMA    TECHNIK_DW.OPS   TO ROLE TECHNIK_AGENT_RO;

GRANT SELECT ON VIEW  TECHNIK_DW.OPS.V_WORK_ORDER_OPERATIONS   TO ROLE TECHNIK_AGENT_RO;
GRANT SELECT ON VIEW  TECHNIK_DW.OPS.V_RELEASED_REVISIONS      TO ROLE TECHNIK_AGENT_RO;
GRANT SELECT ON VIEW  TECHNIK_DW.OPS.V_OPERATION_DOCUMENTS     TO ROLE TECHNIK_AGENT_RO;   -- stage 2: the MCP server
GRANT SELECT ON TABLE TECHNIK_DW.OPS.SAP_QUALITY_NOTIFICATIONS TO ROLE TECHNIK_AGENT_RO;
GRANT SELECT ON TABLE TECHNIK_DW.OPS.TC_DOCUMENTS              TO ROLE TECHNIK_AGENT_RO;
```

Nothing here, and nothing else in the seed, mentions an AI function, a monitor or a tag. So the role holds `CORTEX_USER`
through `PUBLIC`, and read-only describes its data and not its spend. The capstone's fixed statements never call a function.
A managed server that exposes `SYSTEM_EXECUTE_SQL` would hand the model that choice ({{topic:sfmcp}}). The warehouse has no
monitor, and the server sets no `QUERY_TAG`, though the connector's submit action accepts one ({{topic:sfintegrate}}).

*Adapted from the create-and-assign example on the resource monitors page. The quota is Technik's choice:*

```sql
USE ROLE ACCOUNTADMIN;
CREATE OR REPLACE RESOURCE MONITOR TECHNIK_AGENT_RM WITH CREDIT_QUOTA = 20
  TRIGGERS ON 90 PERCENT DO NOTIFY
           ON 100 PERCENT DO SUSPEND;
ALTER WAREHOUSE TECHNIK_AGENT_WH SET RESOURCE_MONITOR = TECHNIK_AGENT_RM;
```

At 100% every tool fails until the interval resets, so the agent must say that data is unavailable and not answer from
memory ({{topic:stagemcp}}). Pair it with a custom budget on the agent and a quota on the AI domain, and revoke `CORTEX_USER`
from `PUBLIC`. The model cost of the capstone's Foundry deployment sits outside Snowflake ({{topic:costs}}).

<!-- unknown since=2026-11 -->
Nobody measured a bill. The two pages name the usage view differently, `CORTEX_FUNCTIONS_USAGE_HISTORY` on the cost page and
`CORTEX_AI_FUNCTIONS_USAGE_HISTORY` on the management page, so check the account's own view list. Whether a budget counts
`AI_CLASSIFY` calls, and whether a quota can block Cortex Agent use, are not stated. The budget's custom actions, the credit
rates and the effect of caching were not read. Whether a trial account allows any of this is unchecked.
<!-- /unknown -->

## Design guidance

- **Match the control to the meter.** Monitors for warehouses, budgets and quotas for AI credits.
- **Put agents on their own warehouse, with its own monitor**, and set the threshold at 90%.
- **Revoke `CORTEX_USER` from `PUBLIC`**, and grant a role to those who need it.
- **Set a `QUERY_TAG` per tool**, so the view can split one agent's spend by tool.
- **Count tokens, not rows.** Labels, descriptions and examples repeat on every record.
- **Treat a suspending monitor as an outage**, and test the agent's message when it fires.
- **Read the usage view before trusting a budget.** Both lag.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| AI spend rises with a monitor in place | Monitors cannot track AI services | Add a budget or a quota |
| The monitor fired and the agent answers oddly | A suspended warehouse fails every tool | Return a clear error and alert the owner |
| Usage cannot be split by tool | No `QUERY_TAG` is set | Set one per tool |
| A per-user limit does not hold | Another role carries `CORTEX_USER` | Revoke it from `PUBLIC` and every other role |
| A budget alert arrives hours late | Refresh takes up to 6.5 hours | Use a quota where blocking matters |
| A classification bill is larger than the text | Instructions repeat on each record | Shorten labels, or batch fewer rows |

## Key terms

**Resource monitor**: a quota on warehouse credits, with triggers that notify or suspend.

**Budget**: a monthly credit limit that notifies and does not cap.

**Per-user quota**: a limit on one user's spend that can block new AI requests.

**Query tag**: the `QUERY_TAG` session value that lets usage views attribute cost.

**Token**: the unit AI functions bill in, about four characters.
