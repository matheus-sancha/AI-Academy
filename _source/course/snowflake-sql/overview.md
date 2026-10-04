## What this module is for

Every number the Technik Production Assistant reports about work orders comes out of Snowflake, through SQL
someone wrote. That SQL decides whether the number is right before any model sees it. An agent cannot
notice that an operation was confirmed twice, or that a join doubled the rows. It reports what the query
returned, fluently and with confidence. This module is the SQL an engineer needs to make sure the query
returns the truth, and the connector setup that decides as whom it runs.

These are the level's only lessons sourced from Snowflake's own documentation rather than Microsoft's. The
last lesson returns to Power Platform. Every example queries Technik's model in `TECHNIK_DW.OPS`, described
on the scenario page, which exists on paper only. The course provides no database, so the queries are for
reading and adapting, not running.

## Before you start

{{topic:snowflakeknowledge}} and {{topic:addconnector}} are the two lessons that send readers here. The
first shows an agent getting a metric wrong from raw tables, and the second puts a fixed query behind a
tool. {{topic:connauth}} is the identity question that `sfroles` and `sfconnector` make concrete, and
{{topic:devenv}} is where your own Snowflake development role comes from.

No SQL is assumed beyond knowing that a table has rows and columns. If you already write SQL daily, skip to
`sfwindow` and `sfviews`, which hold the parts specific to agents. Read straight through, it takes about
three hours.

## What you will be able to do

By the end of this module you should be able to:

- explain how Snowflake separates storage from compute, and what a warehouse costs while it runs;
- set up a dedicated, read-only role for an agent, and say why it is never a person's role;
- write a filtered, bounded query and check its row count before anyone relies on it;
- choose between an inner and a left join, and spot a join that multiplies rows and inflates totals;
- turn detailed rows into a metric with `GROUP BY` and filter groups with `HAVING`;
- break a question into named steps with CTEs, and use `EXISTS` to ask "has at least one";
- keep the latest record per operation with `ROW_NUMBER` and `QUALIFY`, and write a running total;
- build a view an agent can safely read: fixed grain, business names, translated codes, comments, grants;
- choose how the Snowflake connector authenticates for an agent shared with many users.

## The thread through this module

One question runs through all nine lessons: *what was welding efficiency at Plant 1 last month?*

{{topic:sfarch}} places the data in a database, a schema and a warehouse the agent's queries run on.
{{topic:sfroles}} gives the agent its own read-only role. {{topic:sfselect}} writes the first query over
the operations table and checks how many rows it returns. {{topic:sfjoins}} joins operations to work orders
to filter by plant, and meets the join that quietly duplicates rows. {{topic:sfagg}} turns the operations
into one percentage.

The answer is still wrong, and the second half finds out why. {{topic:sfcte}} breaks the question into
named steps and shows how to ask about blocked work orders without listing one twice. {{topic:sfwindow}}
finds that some operations were confirmed twice, and keeps the latest confirmation of each: the figure
drops from about 111% to about 89%. {{topic:sfviews}} puts that fix, readable names and translated status
codes in one view, granted to the agent's role, so no tool can return 111% again. {{topic:sfconnector}}
connects the view to the agent as a service principal and settles who owns the secret.

## Self-check

<details>
<summary>1. An agent's tool reports welding efficiency at Plant 1 as 111%. The SQL is a correct SUM over a real table. What do you check first?</summary>

The grain of the table. `SAP_WO_OPERATIONS` holds one row per confirmation, not per operation, and some
operations were confirmed twice. The routing hours repeat on both rows, so the sum overstates them. Keep one
row per operation, the one with the highest `CONFIRMATION_NO`, using `ROW_NUMBER` and `QUALIFY`, and the
figure becomes about 89%. Then move that step into a view so no other query repeats the mistake
({{topic:sfwindow}}, {{topic:sfviews}}).
</details>

<details>
<summary>2. You deduplicate with ROW_NUMBER, but put the month filter in the WHERE clause of the same query. Why can a partial posting still survive?</summary>

`WHERE` runs before window functions. If an operation's partial posting falls inside the month and its full
re-posting falls after it, the filter removes the later row before `ROW_NUMBER` sees it. The partial posting
is then the latest row left, and it counts. Deduplicate in its own step first, and filter on the result
({{topic:sfwindow}}).
</details>

<details>
<summary>3. Your query lists blocked work orders by joining work orders to open quality notifications, and an agent reports one more blocked work order than the planners count. What happened?</summary>

A work order with two open QNs matches twice, so the join lists it twice, and a count of rows counts it
twice. Ask *whether* an open QN exists with `EXISTS` instead, which never multiplies the outer rows. The same
fan-out inflates sums, which is why a join's row count is worth checking before aggregating
({{topic:sfcte}}, {{topic:sfjoins}}).
</details>

<details>
<summary>4. Why should the agent's role be granted a view rather than the tables behind it?</summary>

A view is where the rules live: the grain, the deduplication, the translated codes and the columns the agent
should not see. A role that can read the tables can bypass all of it. Snowflake lets a role query a view
without any grant on the underlying tables, as long as the view's owner can read them. So the grant on the
view is the agent's whole reach, and anything left out of the view cannot leak through it
({{topic:sfviews}}, {{topic:sfroles}}).
</details>

<details>
<summary>5. The assistant is shared with four user groups, and most of its users have no Snowflake account. Which Snowflake connection type do you choose, and what do you plan for before launch?</summary>

A service principal connection, with a read-only role such as `TECHNIK_AGENT_RO`. Delegated authentication
would need a Snowflake user mapped to every person's sign-in, and users without one would get errors. Before
launch, plan the Entra app registrations and the Snowflake security integration, keep high-privilege roles
out of it, give the client secret an owner and an expiry reminder, and check that one shared connection's
throttling limit covers the expected traffic ({{topic:sfconnector}}).
</details>
