## What this module is for

{{module:snowflake-sql}} taught you to write the SQL an agent runs. This module is for what comes after that. An efficiency
figure is wrong because a window function kept the wrong row. An agent's first answer after a quiet spell is slow and its
warehouse bill is not. A planner sees notifications from a plant they do not work in. A classification column has gaps,
and a budget that nobody checked has doubled. Each of those is a Snowflake problem before it is an agent problem, and each
has a mechanism you can read.

It is a reference module, not a read-through. Come here with a symptom. Eight lessons cover the ground in two halves.
The first four are about SQL that an agent depends on: `QUALIFY` and window frames, semi-structured data, query
performance and the policies that put a rule where Snowflake enforces it. The second four are about AI inside
Snowflake: the SQL functions that call a model per row, the managed agent object, the three ways a Microsoft agent
reaches all of it, and what it costs.

The capstone is the running example only where it can be. Its views, role and warehouse are real, and its three tools
are keyed lookups, so it calls no AI function and has no Cortex service. The capstone's code was tested offline only
({{module:capstone-build}}), and nothing in this module was run. Each lesson says so in a visible *Not yet verified*
block where it matters.

## Before you start

You need {{module:snowflake-sql}}, and in particular {{topic:sfroles}} and {{topic:sfviews}}, which give the agent a role
and a clean view, and {{topic:sfwindow}}, which introduced `QUALIFY`. {{topic:sfconnector}} and
{{topic:snowflakeknowledge}} are the Microsoft-side routes that {{topic:sfintegrate}} sets against a third.
{{topic:sfmcp}} explains the managed MCP server, and {{module:advanced-rag}} supplies {{topic:cortexanalyst}} and
{{topic:routing}}, which the Cortex Agents lesson builds on. For the security habits in the AI lessons you need
{{topic:ctxsecurity}}, and for the cost of the Microsoft side, {{topic:costs}}.

Allow about three hours to read it end to end, though you are not meant to.

## What you will be able to do

By the end of this module you should be able to:

- audit a deduplicating view with the clause that built it, and say where `ROWS` and `RANGE` disagree;
- say what `FLATTEN` does to a row that lacks a path, and why a view should do the extracting;
- read a Query Profile and Grouped Queries, and say what a warehouse's auto-suspend costs an assistant used in bursts;
- choose between a secure view, a row access policy and a masking policy, and name what none of them can do for a single-identity agent;
- say which AI function fits a closed set, a boolean, a score or free text, and what each does with a row it cannot process;
- explain why text a person wrote reaches the model through these functions, and where its output may and may not be used;
- say whose privileges a Cortex Agent's tools run with, and what `tool_not_accessible` does when one is missing;
- choose among knowledge, the connector and managed MCP by who writes the SQL and whose identity Snowflake sees;
- say which cost control watches which meter, and why a resource monitor leaves AI spend uncapped.

## The thread through this module

From the query, through the policy, to the model, and then to the bill.

{{topic:qualify}} is the rule that decides which row counts, and it can list the rows it hid. {{topic:semistructured}}
is how bench readings fit in a column, and what the extracting must do about a missing key. {{topic:performance}} measures
what each call costs, and {{topic:sfgov}} puts the access rule where the database enforces it.

{{topic:aisql}} then calls a model on every row. {{topic:cortexagents}} is the managed agent that runs with the caller's
rights, {{topic:sfintegrate}} chooses how a Microsoft agent reaches Snowflake, and {{topic:sfcost}} says what each of
them bills and which control can stop it.

Two ideas run through all eight. The first is that **a rule which must hold has to live where Snowflake enforces it**, and
not in a prompt: the clause in a view, the role of the session, a policy on a table, a privilege on a tool, a setting that
rejects a run, a revoked role. Each moves the rule from a request that a model may ignore to a condition the database checks.
It is also why one service identity cannot be told apart from another by any policy.

The second is a habit, **count before you scale**. The pages give no numbers where you most want one: nothing on how a
classifier behaves on text that states nothing, nothing on how the cost of a similarity join grows, and nothing on what a
Microsoft client shows of a warning. So the lessons use the seed's twelve notifications as an answer key, count the `NULL`
rows, put a figure on the instructions an `AI_CLASSIFY` call repeats, and mark the rest in an `unknown` block.

Four dated facts will have moved by the time you read this, so check them first. Snowflake as a Copilot Studio knowledge source
is preview. Analytical search in Cortex Agents is public preview. The page for AI functions labels no function generally
available. And the two Snowflake cost pages name the AI usage view differently.

## Self-check

<details>
<summary>1. Welding efficiency at Plant 1 for September reads 110.9% over the operations table, and the report says 88.9%. Where does the difference come from, and how do you prove it?</summary>

From operations confirmed twice. A partial posting was never reversed and the full one followed, so 20 operations
appear as 26 rows and the hours count double. The fix is a rule, not a prompt: keep the posting with the highest
`CONFIRMATION_NO` per operation, in a view that the agent reads.

To prove it, run the clause that builds the view in the other direction. `QUALIFY` filters after window functions are
computed, so the same expression, inverted, lists exactly the stale rows the view hides. Count them and the 6 extra rows
appear. A frame over timestamps that tie is the second place this goes wrong, because `RANGE` treats tied values as peers
and `ROWS` counts physical rows ({{topic:qualify}}).
</details>

<details>
<summary>2. The first question after a quiet spell is slow, and the warehouse's credits are mostly idle minutes. What do you check, and what can this module not tell you?</summary>

Check the gaps against `AUTO_SUSPEND`. Each resume bills a 60-second minimum and drops the cache, so a warehouse that
suspends after 60 seconds and is used in bursts a few minutes apart is billed for resuming again and again, and each
resume is also a slower first answer. Then open the Query Profile of one tool's statement and look at partitions scanned
against total, and watch the statement as a group, since an agent repeats the same ones.

What the module cannot tell you is the right value. The warehouse page gives no absolute numbers, the capstone's traffic
was never measured, and the seed has 133 rows, so every plan is trivial ({{topic:performance}}). The capstone also sets
no `QUERY_TAG`, so its three tools can be told apart only by their SQL text.
</details>

<details>
<summary>3. Plant 2's quality team gets its own agent and must see only Plant 2's notifications. Which tool do you use, and what can it not do?</summary>

A row access policy on the table is the rule that holds on every path, because a secure view can be bypassed by a grant
on the table underneath it. A secure view suits a view that exists for privacy, at the cost of speed and a hidden profile,
and a plain convenience view should stay plain. Name the administrator roles in the policy, since it binds owners too,
and remember that row access needs Enterprise Edition.

What neither can do is tell one caller from another when the agent runs as one identity. The policy decides from the
session's role, and the capstone chose a single role for every question. A per-person answer needs the person's own role,
or a rule outside Snowflake ({{topic:sfgov}}).
</details>

<details>
<summary>4. A nightly job classifies every notification's description. The warehouse's resource monitor sits at 12% of its quota, yet the month's bill has doubled and some labels are empty. What happened?</summary>

Two separate things. The bill is in the other meter. A resource monitor watches warehouse credits and, by the page's own
words, cannot track AI services, so the model's tokens are invisible to it. Each record also repeats the labels and the
task description, which for the seed's notifications is about as many tokens as the text itself. A budget notifies and a
per-user quota can block, and neither exists until you set one ({{topic:sfcost}}).

The empty labels are rows that failed. A function that cannot process its input returns `NULL` and the query carries on,
so the job succeeded. Count the `NULL`s and read the error details. Then look at notifications `300001267` and
`300001270`, which carry text aimed at an assistant. A label there is derived from untrusted text and must not decide
anything ({{topic:aisql}}).
</details>

<details>
<summary>5. A planner asks a Cortex Agent for welding efficiency and gets a confident answer built only from documents. Nobody saw an error. Why, and what do you change?</summary>

The agent's role could not reach the semantic view's tables, and the default `tool_not_accessible` mode, `accept`, carries
on with the tools the role can reach and reports the rest as a warning. The capstone's agent role is denied the raw
operations table on purpose, so an Analyst tool over it is exactly that case. Whether the client displays the warning is
untested, so the downgrade can look like an answer.

Set `reject` where a missing tool changes the answer, so the run fails loudly. Grant per tool, since `USAGE` on the agent
alone is not enough, and test as the caller's role. Then ask whether this route is the right one at all. A named question
belongs in a connector tool over a view, and a mixed one in an agent behind MCP, whose identity is the engineer's own role
({{topic:cortexagents}}, {{topic:sfintegrate}}).
</details>
