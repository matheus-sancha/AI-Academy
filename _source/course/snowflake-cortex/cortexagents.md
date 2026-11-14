## TL;DR

A Cortex Agent is a schema-level object that bundles a model, tools, orchestration settings and instructions, and Snowflake
runs the planning loop for you. {{topic:routing}} covered how it plans. This lesson covers the object around the loop, which
is where the decisions are. The tools run with the **caller's** session roles, and that role needs privileges on every
object a tool uses. By default a run **continues without** any tool the caller cannot reach and reports a warning, which is
a silent downgrade unless you set `reject`. A per-run **budget** caps seconds and tokens. And Snowflake does not guarantee
the accuracy of the answers or their citations, so the object does not replace checking.

## Why it matters

{{topic:sfmcp}} showed how an agent becomes one governed tool for a Microsoft client, and {{topic:routing}} showed the
loop that chooses between tools. Neither says what to set in the object, and the settings carry the rules. The capstone's
rule is one read-only identity for every question. A Cortex Agent has no such shape, since it runs as whoever calls it. So
the first question is the identity, and the second is what a missing grant does to an answer.

## How it works

### The object

<!-- volatile verified=2026-11 -->
The page defines an agent as a schema-level object that bundles the model, tools, orchestration settings and instructions.
You create one in Snowsight, with SQL or through the REST API, and run it through `agent:run`. A thread keeps the
conversation context, so the client does not carry it. An agent with no tools answers from the model's general knowledge
and can query nothing. The tools the page lists are Cortex Analyst over a semantic view, Cortex Search, analytical search
(public preview), a Python code sandbox, data-to-chart, stored procedures and functions as custom tools, skills, MCP
connectors to remote servers, other agents' toolsets, and web search, which must be enabled for the account. Custom tools
cannot take a parameter of type object.
<!-- /volatile -->

The specification is YAML inside `CREATE AGENT … FROM SPECIFICATION`, and `ALTER AGENT … MODIFY LIVE VERSION SET
SPECIFICATION` replaces the whole of it, so a partial edit deletes the rest. The inaccessible-tool page warns that a
specification holds three keys named `orchestration`. The top-level one sets `tool_not_accessible`, `budget` and
`capabilities`. The one under `models` picks the model, and Snowflake recommends `auto`. The one under `instructions`
steers tool choice.

### Whose rights

Calling an agent takes the `SNOWFLAKE.CORTEX_USER` or `SNOWFLAKE.CORTEX_AGENT_USER` database role, privileges on the agent,
and privileges on the objects its tools use. `CORTEX_USER` is granted to `PUBLIC` by default and covers every covered AI
feature. `CORTEX_AGENT_USER` covers agents only and leaves out Cortex Analyst, which needs `CORTEX_ANALYST_USER` as well.
`USAGE` on the agent is not enough alone. Because the agent uses the caller's session roles, those roles need privileges on
the tools' objects. A REST call sets the primary role with the `X-Snowflake-Role` header, or falls back to the user's
default role. Tools run on the warehouses the specification names.

### When the role cannot reach a tool

<!-- volatile verified=2026-11 -->
`orchestration.tool_not_accessible` has three modes. Under `accept`, the default, the run continues with the tools the role
can reach and reports the others as warnings. Under `reject`, one 4XX response lists every inaccessible tool. Under
`legacy`, the run fails at the first one. There is no account-level setting. Search, Analyst, MCP and skill tools are
checked when the run starts, but custom tools, SQL execution and code execution are not, and one of those fails at
execution time while the agent keeps reasoning. A resource you name produces a warning, but items Snowflake enumerates, such
as an MCP connector set to `selection: all`, are omitted with no warning.

A streaming client receives a `response.warning` event before the first model call, and a non-streaming response carries a
top-level `warnings` array. The message does not tell a missing object from an unauthorized one, and the warning is
recorded in `SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS`. None of this bypasses a privilege. It decides only whether a
missing one aborts the run.
<!-- /volatile -->

### Spend and visibility

<!-- volatile verified=2026-11 -->
A `budget` of `seconds` and `tokens` limits one run, and the page's example sets 30 and 16,000. Orchestration is billed in
tokens, Cortex Analyst per token and Cortex Search by index size and time. A custom tool costs warehouse time, and web
search, code execution, connectors and skills can add more. Spend limits across runs are separate features, and
{{topic:sfcost}} covers them.

Observability shows live threads and traces. A thread has a `thread_id`, a turn is one `agent:run` request, and a trace is
one turn made of spans such as planning or SQL execution. Viewing needs `OWNERSHIP` or `MONITOR` on the agent and the
`CORTEX_USER` role. Without a separate account privilege, a role sees metadata only, and inputs, outputs and feedback text
are redacted.
<!-- /volatile -->

The page's note is plain: the accuracy of the model's responses, and of the citations it gives, "is not guaranteed".

## In practice at Technik

Say Technik wants a Snowflake-side agent for governed questions, the `PRODUCTION_AGENT` that {{topic:sfmcp}} exposed through
MCP. The specification below sets the two rules this lesson is about.

*Adapted from the specification example on the manage-agents page, with the tool blocks elided:*

```sql
CREATE OR REPLACE AGENT TECHNIK_DW.OPS.PRODUCTION_AGENT
  COMMENT = 'Governed questions about work orders, operations and quality notifications.'
  FROM SPECIFICATION
  $$
  orchestration:
    tool_not_accessible: reject
    budget:
      seconds: 30
      tokens: 16000
  instructions:
    orchestration: "Efficiency and counts: use the analyst tool. Document wording: use search."
    response: "Quote identifiers exactly. Say so when a tool returned nothing."
  # tools: and tool_resources: elided
  $$;
```

**Why `reject`.** The capstone's agent role is denied `SAP_WO_OPERATIONS` on purpose, and reads the deduplicated view
instead ({{topic:cortexanalyst}}). A semantic view over the raw table is therefore a tool that role cannot reach. Under
`accept`, a planner asking about welding efficiency gets a run that continues, and the answer comes from whatever else the
agent can reach. The warning exists, but nothing guarantees that the client shows it. Under `reject`, the planner gets an
error, which is the honest result when the question's main tool is missing. `accept` fits only where a partial answer is
useful and the interface shows the warning.

**Whose role runs it.** Through a managed MCP server the session runs as the connecting user's default role, so each
engineer's reach differs, and the capstone's `TYPE = SERVICE` identity cannot connect that way. Grant `CORTEX_AGENT_USER`
and `USAGE` on the agent to the role that engineers use, and test as that role with the header.

<!-- unknown since=2026-11 -->
Nobody ran this. The pages do not say how an agent behaves when two people with different roles share a thread, or what
makes `IS_AGENT_ACTIVATED()` true, which the row access page uses. They do not say how a user's spend is attributed to a
run or how to pin the model version. Whether a warning survives the MCP layer into a Microsoft client's tool result is also
untested. The specification's analyst and search blocks, and its budget numbers, are Technik's design, not tested values.
<!-- /unknown -->

## Design guidance

- **Set `tool_not_accessible: reject`** when a missing tool changes the answer, and `accept` only where a partial answer helps.
- **Grant per tool, then test as the caller's role.** `USAGE` on the agent alone never makes a run work.
- **Put a `budget` in every specification.** A loop with no ceiling is the expensive failure.
- **Send the whole specification on every update.** `ALTER` replaces it.
- **Keep `MONITOR` narrow.** It exposes traces, and traces hold what tools returned.
- **Grant `CORTEX_AGENT_USER`, not `CORTEX_USER`,** when a role needs agents and nothing else.
- **Verify answers and citations yourself.** The accuracy statement is Snowflake's own.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| An answer ignores half the question | A tool was inaccessible, and `accept` carried on | Use `reject`, or surface `warnings` |
| The agent can be called but fails at a tool | `USAGE` on the agent is not enough | Grant privileges on each tool's objects |
| A custom tool fails mid-run | Custom tools are not checked at run start | Test the role against each one |
| An update removed the tools | `ALTER` replaced the whole specification | Resend it in full |
| An Analyst tool errors for a role | `CORTEX_AGENT_USER` leaves out Analyst | Add `CORTEX_ANALYST_USER` |
| A reviewer sees no inputs in a trace | Redaction without the extra account privilege | Grant it only where needed |

## Key terms

**Cortex Agent**: a schema-level object that bundles a model, tools, orchestration settings and instructions.

**Thread**: the stored conversation context an agent keeps across turns.

**`tool_not_accessible`**: the setting that decides whether a missing tool privilege aborts a run.

**Orchestration budget**: the seconds and tokens one run may use.

**Trace**: one turn of an agent, recorded as spans such as planning and tool calls.
