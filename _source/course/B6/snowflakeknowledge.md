## TL;DR

You can add selected Snowflake tables as a knowledge source, and the agent turns natural-language
questions into queries itself. Nobody writes SQL, and the data never leaves Snowflake. What you gain
is coverage of questions you could never enumerate in advance. What you give up is knowing what
query will run. Both matter, and the deciding factor is almost always the quality of the table names,
column names and comments you point it at.

## Why it matters

Technik's manufacturing questions have a very long tail. "Which work orders are late to start
Coating this week", "how many operations did Plant 2 confirm last month", "which parts have the most
open notifications" — you will never build a tool for each, and a planner will never stop inventing
new ones.

Knowledge over Snowflake covers that tail. It is also the place where the difference between a raw
table and a well-named, commented view shows up most dramatically, which is why this lesson sits
next to [B10](../../beginner.html#B10) in spirit even though it comes first in reading order.

## How it works

<!-- volatile verified=2026-09 -->
Snowflake is added through the Power Platform connector, selected as a knowledge source rather than
as a tool, and you choose which tables the agent may reach. Exactly where that lives in the maker
portal, and which harnesses support it, changes between releases — check the linked documentation for
the current path.
<!-- /volatile -->

At question time the agent has the **schema** — table names, column names, types and comments — and
the user's question. It writes a query, runs it through the connection, and answers from the rows
that come back.

Three consequences follow directly.

**The schema is the prompt.** The model has nothing else to go on. `SAP_WO_OPERATIONS.ACTUAL_HOURS`
with the comment *"Hours actually booked. Null until the operation is confirmed"* is a far better
input than an uncommented `AH` column. This is not a nicety; it is the single largest lever you have
over answer quality here.

**You do not know what query will run.** It varies between runs, like any generated text. It may
join in a way you would not have, or miss a filter you consider obvious. For an exploratory question
that is fine. For a number someone reports upward, it is not.

**Everything the role can read is reachable.** Not "everything you selected" in a security sense —
the connection's role is the boundary. This is why the course uses `ACADEMY_AGENT_<you>`, read-only,
from the first lab.

### Knowledge or tool?

| | Knowledge over Snowflake | A connector tool (B7) |
|---|---|---|
| Question shape | Open-ended, unpredictable | Named, enumerable |
| SQL | Written by the model, per question | Fixed by you |
| Repeatability | Varies | Identical every time |
| Cost and result size | Unpredictable | Bounded by your query |
| Testable | Only by outcome | Directly |
| Right for | The long tail | Anything anyone will act on |

The rule that survives contact with reality: **questions you can name become tools; questions you
cannot become knowledge.** And when a knowledge question turns out to be asked every day, promote it
to a tool.

## In practice at Technik

In this module's lab you give the agent `SAP_WORK_ORDERS` and `SAP_WO_OPERATIONS` as knowledge, and
then ask it two questions that behave very differently.

**"What is the status of work order `100004521`, and which operation is it at?"** works well. It is a
lookup with an obvious filter, the column comments carry the status codes, and the answer is a couple
of rows.

**"What was machining efficiency last month?"** does not, and the reason is the point of the exercise.
The agent will write something like `SUM(ROUTING_HOURS) / SUM(ACTUAL_HOURS)` over the operations
table — which is the natural reading of the column names and comments, and which is **wrong**,
because six operations in the seeded data carry two confirmations each. Hours are double-counted. The
number that comes back is plausible, wrong in the direction of flattering, and cited to a real table.

Nothing in the schema tells the model that. The comment on `SAP_WO_OPERATIONS` warns that duplicates
exist, and even so the model has to invent the `QUALIFY` that removes them and choose the right
ordering key. Sometimes it does. That is worse than never doing it, because it means testing once
proves nothing.

The fix is not a better prompt. It is a **view** that deduplicates before the model ever sees the
rows — which is exactly what B10 builds, and why B7's lab points its tool at a view rather than at
tables.

> [!WARNING]
> A generated query that is wrong does not look wrong. It returns a number, with a citation to a real
> table, in the right units. Any metric that leaves the room should come from a view or a tool you
> wrote, never from a query invented at question time.

## Design guidance

- **Point it at views, not raw tables**, wherever the question involves a metric.
- **Comment every column you expose.** The comment is read by the model on every question; it is the
  cheapest quality improvement available.
- **Use business words in names.** `V_WORK_ORDER_STATUS.CURRENT_OPERATION` beats `SWO.OP_CUR`.
- **Expose the fewest objects that answer the questions.** Every extra table is another way to join
  wrongly.
- **Read-only role, always.** The agent cannot be talked into a write it has no privilege for.
- **Promote frequent questions to tools.** If planners ask it daily, it deserves a fixed query.
- **Watch result size.** A question that matches ten thousand rows will try to bring them back.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Plausible metrics that are subtly wrong | The model invented a query over data with a known quirk | Deduplicate in a view; do not rely on the model finding `QUALIFY` |
| The same question gives different numbers | A different query each run | Fix the query: promote it to a tool |
| "I could not find that" for data that exists | The role cannot see the object, or the name gave the model nothing to match | Check grants as the agent role; rename or comment the columns |
| Very slow answers | A generated query scanning more than it needs | Expose narrower views; add filters into the view |
| Costs rising in Snowflake | Unbounded generated queries on an always-on warehouse | Auto-suspend, a resource monitor, and bounded views |
| An answer mixes two plants or two months | The model omitted a filter the user assumed | Put the grain in the view name and comment; confirm the filter in the answer |

## Key terms

**Knowledge over a connector** — the agent generating and running a query against a live source at
question time.

**Schema** — the table names, column names, types and comments the model sees. Its only guide.

**`COMMENT`** — Snowflake's column and table documentation. Read by the model on every question.

**View** — a named, fixed query. Where constraints and deduplication belong (B10).

**`QUALIFY`** — the Snowflake clause that filters on a window function, used to keep one row per
operation.

**Least privilege** — the read-only role the agent connects with, which bounds everything it can
reach.
