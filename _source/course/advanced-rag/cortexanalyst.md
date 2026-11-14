## TL;DR

Cortex Analyst turns a business question into SQL, runs it in your warehouse and returns the answer. What makes it
accurate is the **semantic view** it reads: a Snowflake object that holds your business definitions once, with synonyms
and verified example queries. A bare schema has no definition of *efficiency* or *released*, and the model guesses one.
Snowflake's page now recommends moving to Cortex Agents, so the semantic view is the part that lasts. The pages
describe a semantic view as sitting over physical tables, and nothing on them says a rule living in a database view
carries over, which matters for Technik's views. And Analyst answers only what SQL can answer.

## Why it matters

{{topic:snowflakeknowledge}} showed the other way to ask Snowflake a free question: Microsoft indexes the table and
column names and writes the SQL itself, and anything a person will act on belongs in a view or a tool you wrote.
Cortex Analyst is Snowflake's answer to the long tail of questions nobody wrote a tool for, and it differs in where the
meaning lives. A column called `ACTUAL_HOURS` says nothing about efficiency, so a model has to guess the formula. A
definition written once, in one governed object, makes every question about efficiency use the same arithmetic. The
risk is the mirror image: a wrong definition is wrong everywhere.

## How it works

### What the model reads

A semantic view is a schema-level object. Over your tables it defines **logical
tables** for business entities, **relationships** that join them on shared keys, **facts** that are row-level
quantities, **dimensions** that give categorical context such as plant or operation, and **metrics** that aggregate
facts into the numbers people ask for. The overview page's example defines net revenue once, as a sum of gross revenue
after discount, so *net revenue by region* aggregates the same way in every report. The Cortex Analyst page adds
descriptions and synonyms, verified examples (sample questions with their SQL answers), public or private access
modifiers, and custom instructions for writing SQL and categorising a question.

<!-- volatile verified=2026-11 -->
You can create one with Semantic View Autopilot, an AI-assisted wizard that also accepts a YAML, Tableau or Power BI
file, in Semantic Studio, or with `CREATE SEMANTIC VIEW`, and query it with a plain `SELECT`. The older semantic
model, a YAML file on a stage, still works, and Snowflake recommends semantic views for new work, starting from a simple
star schema.
<!-- /volatile -->

At question time the model sees only metadata from the definition, meaning table and column names, value types and
descriptions. The SQL it writes then runs in your warehouse.

### Under whose rights it runs

The page says the SQL Analyst generates and executes adheres to role-based access control. Its privilege table lists
what the requesting role needs: the `SNOWFLAKE.CORTEX_USER` or `SNOWFLAKE.CORTEX_ANALYST_USER` database role, and
`SELECT` on the tables the semantic model mentions. That is the opposite shape to a Cortex Search service
({{topic:cortexsearch}}), which reads with its owner's rights. Here the asking role needs access to the data.

Two traps sit on the page. `CORTEX_USER` is granted to `PUBLIC` by default, so every role can call Analyst until
someone revokes it and grants the narrower `CORTEX_ANALYST_USER` to named roles. And a legacy YAML file on a stage is
governed by access to the stage: a role that can read the file sees the table and column names, even without `SELECT`
on the tables.

### What it can and cannot answer

<!-- volatile verified=2026-11 -->
Analyst answers only what SQL can resolve, and the page's example of what it will not do is broad insight, such as
trends. The model keeps
no state, so you pass the conversation in `messages` and the whole history is processed again each turn, with compute
rising each round. It cannot see earlier results, so a follow-up that refers to a list it returned fails, and after many
turns or a change of intent the page says to reset. You cannot choose its model. It assigns one from an ordered
preference list, headed by Claude Sonnet 4.6, by region, cross-region setting and model-level restrictions, and says
the behaviour may change. Different models produce different results. Billing is per message processed, successful
responses only, plus the warehouse time of the SQL. Tokens matter to cost only when Analyst is called through Cortex
Agents.
<!-- /volatile -->

The page also says to run a semantic view's verified queries through Analyst and count how accurately it writes the
SQL. Because the model can change under you, that set is how you notice a change you did not make.

### The banner

The page opens by recommending a move to Cortex Agents, which Snowflake says supports every Analyst capability with
higher answer quality. A semantic view can be an agent's tool ({{topic:cortexagents}}), so the view is the durable
investment, and {{topic:routing}} covers how an agent chooses between Analyst and search.

## In practice at Technik

The Production Assistant answers efficiency through a fixed tool, `Get operation efficiency`. A planner who asks about
welding at Plant 2 last week has no tool, and that is the long tail. A semantic view over the `OPS` data could serve it:
logical tables for work orders, operations and projects joined on `WO_NO` and `PROJECT_ID`, plant and operation as
dimensions, and efficiency as a metric in the scenario's definition, routing hours divided by actual hours times 100,
written in the shape of the page's net-revenue metric. Synonyms map a planner's *technically complete* to SAP's
`TECO` and *released* to `REL`.

The trap is a number. Welding at Plant 1 in September reads **110.9%** over `SAP_WO_OPERATIONS`, because operations
confirmed twice are counted twice (26 rows for 20 operations), and **88.9%** once the stale postings are dropped with
`QUALIFY` ({{topic:qualify}}). The rule behind 88.9% lives in the view `V_WORK_ORDER_OPERATIONS`. The Snowflake pages
describe a semantic view as sitting over physical tables, and Technik's agent role is deliberately denied the raw
table, since `TECHNIK_AGENT_RO` reads views wherever a rule lives. The two designs collide. Analyst needs `SELECT` on
what the model names, and the role reaches operations only through the view. Grant the raw table to make Analyst work and the flaw returns
as an answer with a definition's confidence.

<!-- unknown since=2026-11 -->
The pages do not say whether a logical table can be defined over a view, or whether a verified query's SQL can carry a
rule like the `QUALIFY`. Build the view and ask the welding question. The right answer is 88.9%, and any other number
means the rule did not carry. The capstone has no Cortex Analyst, and nobody ran any of this.
<!-- /unknown -->

## Design guidance

- **Define each business term once**, in the semantic view, and check where the dedupe or status rule lives.
- **Test the grain before you ship** with a question whose right answer you know, such as 88.9%.
- **Prefer semantic views** to staged YAML, and keep verified queries as a regression set.
- **Revoke `CORTEX_USER` from `PUBLIC`**, and grant `CORTEX_ANALYST_USER` to the roles that need it.
- **Treat granting a raw table as a design decision**, not a fix for a permission error.
- **Make each question self-contained**, and reset the conversation when the intent changes.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A metric is off by a double count | The logical table sits over a raw table and the rule lived in a view | Test with a known answer before trusting it |
| Every role can ask Analyst | `CORTEX_USER` is granted to `PUBLIC` by default | Revoke it, and grant `CORTEX_ANALYST_USER` to named roles |
| A role without table access sees their names | A staged YAML file is governed by stage access | Use a semantic view, or restrict the stage |
| A follow-up about an earlier result fails | Analyst cannot see earlier results | Restate the question in full |
| Answers change with no edit to the view | The model depends on region and settings, and can change | Keep one configuration and rerun the verified queries |
| A trends question gets no useful answer | Analyst resolves only what SQL can | Route it to another tool |

## Key terms

**Cortex Analyst**: Snowflake's managed text-to-SQL service, called through a REST API.

**Semantic view**: a schema-level object that defines business tables, relationships, facts, dimensions and metrics.

**Metric**: an aggregation of facts into a business number, defined once and reused by every question.

**Verified query**: a sample question stored with its SQL answer, used to guide generation and to measure accuracy.
