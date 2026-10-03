## TL;DR

You can add selected Snowflake tables to an agent as a knowledge source. Nobody writes SQL, the data never
leaves Snowflake, and the agent can answer questions nobody listed in advance. It is a **preview** feature,
documented for the **standard harness** only. Microsoft indexes just the table and column names, and runs
every question **as the asking user's own Snowflake identity**. What you give up is knowing what query will
run, so anything someone will act on belongs in a view or a tool you wrote.

## Why it matters

Questions about Technik's manufacturing data have a long tail. *Which work orders are late to start
Coating this week? How many operations did Plant 2 confirm last month? Which parts have the most open
notifications?* Nobody will build a tool for each one, and planners will never stop inventing new ones.

Knowledge over Snowflake covers that tail. It is also where the difference between a raw table and a
well-named view shows most clearly. That is why the Snowflake reference module ({{module:snowflake-sql}})
exists, and why this lesson keeps sending you to it.

## How it works

<!-- volatile verified=2026-10 -->
On the standard harness: **Add knowledge → Snowflake** (under **Advanced** if it is not Featured), sign in,
choose the target, select the tables, then name and describe the source. While Copilot Studio indexes the
metadata, the status shows **In progress**; when it changes to **Ready** you can test. Synonyms and glossary
definitions are supported only for ServiceNow and Zendesk, not Snowflake. Power Platform connectors as
knowledge are preview, and Microsoft says preview features "aren't meant for production use".
<!-- /volatile -->

<!-- unknown since=2026-10 -->
Whether Snowflake can be added as knowledge on the **GitHub Copilot harness**. Its **Add knowledge** dialog
does not list it, but it does offer a *Custom Connector* option and says the available sources vary by
environment. Check your own tenant before designing around it.
<!-- /unknown -->

What Microsoft documents is short: it indexes **only metadata, such as table names and column names**; there
is **no data movement**; each request "is processed at runtime and executed against the target system";
and every runtime call is authenticated with **the user's token**, so Snowflake's own access controls
apply. Three consequences follow.

**The names are most of what the agent has.** It is turning a question into a query over tables it knows
by their names and their columns. `SAP_WO_OPERATIONS.ACTUAL_HOURS` gives it something to work with; a
column called `AH` gives it nothing.

<!-- unknown since=2026-10 -->
Whether the agent also reads Snowflake **column and table comments**, and whether you can see the query it
generated. Microsoft names table and column names only. Write good comments anyway, because people and
other tools read them, but do not count on the agent reading them.
<!-- /unknown -->

**You do not know what query will run.** It can differ between runs, like any generated text. It may join
in a way you would not, or leave out a filter you thought was obvious. For an exploratory question that
is acceptable. For a number someone reports upwards, it is not.

**Each user's own role is the boundary.** The Snowflake connector's user-delegated authentication maps a
person's Microsoft Entra sign-in to a Snowflake user with a matching login name. A user with no Snowflake
account gets nothing, and a user with broad access can reach everything their role can read, whichever
tables you selected. This is the opposite of Technik's rule for agents, which read as `TECHNIK_AGENT_RO`
({{topic:connauth}}).

### Knowledge or tool?

| | Knowledge over Snowflake | A connector tool ({{topic:addconnector}}) |
|---|---|---|
| Question shape | Open-ended, unpredictable | Named, listable in advance |
| SQL | Generated per question | Fixed by you |
| Repeatability | Varies | Identical every time |
| Identity | The asking user, always | Your choice: user, maker or service identity |
| Testable | Only by the outcome | Directly |
| Right for | The long tail | Anything anyone acts on |

The rule that holds up in practice: **questions you can name become tools, and questions you cannot name
become knowledge.** When a knowledge question turns out to be asked every day, promote it to a tool.

## In practice at Technik

The Production Assistant does not use Snowflake as knowledge. It is on the GitHub Copilot harness, and most
of its users have no Snowflake account. Its work order questions are named ones, so they are tools
({{topic:tools}}).

Picture instead a planning agent on the standard harness, used only by planners, who already query
Snowflake with their own roles. Give it `SAP_WORK_ORDERS` and `SAP_WO_OPERATIONS` as knowledge and ask two
questions.

**"What is the status of work order `100004521`, and which operation is it at?"** works well. It is a
lookup with an obvious filter, and the answer is a couple of rows. It returns `REL`, though, and only a
planner knows what that means.

**"What was welding efficiency at Plant 1 this month?"** goes wrong, and how it goes wrong is the lesson.
The natural reading of the column names is `SUM(ROUTING_HOURS) / SUM(ACTUAL_HOURS)` over the operations
table. But `SAP_WO_OPERATIONS` holds one row per *confirmation*, and some operations were confirmed twice:
a partial posting that was never reversed, then the full one. The hours are double-counted. The agent
reports about **111%**. With the stale postings removed (keep the highest `CONFIRMATION_NO` per operation)
the answer is about **89%**. The wrong figure is plausible, flattering and drawn from a real table.

Nothing in the table names says so. The fix is not a better prompt. It is a **view** that deduplicates
before the agent ever sees the rows and spells out the status codes ({{topic:sfviews}}). That is the same
view the assistant's efficiency tool queries.

> [!WARNING]
> A wrong generated query does not look wrong. It returns a number, in the right units, from a real table.
> Any metric that leaves the room should come from a view or a tool you wrote, never from a query invented
> at question time.

## Design guidance

- **Use business words in names.** `V_WORK_ORDER_STATUS.CURRENT_OPERATION` beats `SWO.OP_CUR`, because the
  name may be all the agent reads.
- **Point it at the fewest objects that answer the questions.** Every extra table is another way to join
  wrongly.
- **Put deduplication and code translation in SQL**, where they are enforced, not in a description.
- **Check the users' roles, not the agent's.** Live knowledge has no agent identity to restrict.
- **Promote frequent questions to tools.** If planners ask it daily, it deserves a fixed query.
- **Treat it as preview.** Pilot it; do not hang a production promise on it.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Plausible metrics that are subtly wrong | A generated query over data with a known quirk | Deduplicate in a view; promote the metric to a tool |
| The same question gives different numbers | A different query on each run | Fix the query in a tool |
| Answers for the maker, nothing for colleagues | They have no Snowflake user mapped to their sign-in | Map them, or use a tool with a service identity |
| An answer mixes two plants or two months | The query left out a filter the user assumed | Put the grain in the view's name; have the answer state its filters |
| Snowflake is not in the **Add knowledge** dialog | The GitHub Copilot harness, or the preview has not reached the tenant | Check the harness and the tenant first |

## Key terms

**Real-time knowledge** — a connector queried live at question time, as the asking user, with no data
copied.

**Metadata indexing** — Copilot Studio storing table and column names, not rows.

**User-delegated authentication** — the connector acting as the signed-in user, mapped to their own
Snowflake login.

**View** — a named, fixed query; where deduplication and business rules belong ({{topic:sfviews}}).

**Promotion** — turning a frequently asked knowledge question into a tool with a fixed query.
