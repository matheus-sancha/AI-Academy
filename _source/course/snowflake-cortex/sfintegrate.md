## TL;DR

Microsoft agents reach Snowflake by three routes, and they differ in who writes the SQL and whose identity Snowflake sees.
**Knowledge** has Copilot Studio index table and column names and generate the query at question time, as the asking user.
It is preview, and documented for the standard harness only. The **connector** runs SQL that you wrote, as one service
principal or as each signed-in person. A **Snowflake-managed MCP server** exposes Snowflake's own tools, Analyst, Search,
agents, SQL and procedures, and runs as the connecting user's default role. The choice is made per class of question, by how
much control, governance and reasoning it needs. Neither company's pages describe how Copilot Studio and Cortex fit
together, and the capstone uses none of the three.

## Why it matters

Each route was taught somewhere else in this course. {{topic:snowflakeknowledge}} and {{topic:sfconnector}} are in
Intermediate, and {{topic:sfmcp}} is in this level. Set side by side, the question that separates them is not capability.
It is identity and determinism: who is Snowflake talking to, and will the same question run the same statement twice? Pick
wrongly and the cost arrives months later, as a user who gets an authentication error, a number that differs between runs,
or a role nobody meant to widen.

## How it works

### Route 1: knowledge

<!-- volatile verified=2026-11 -->
Microsoft's page is titled *preview* and says it describes features "powered by the standard harness", naming no other. You
choose **Add knowledge**, pick the Snowflake connector, sign in, select tables and give the source a name. The page says
Microsoft "only indexes metadata, such as table names and column names", that each request is "executed against the target
system", and that every runtime call uses the user's own token, so the source system's access controls hold. The same data
policies govern the connection. It lists fourteen connectors, and synonyms and glossary terms work only for two of them,
ServiceNow and Zendesk.
<!-- /volatile -->

The page says nothing about how a question becomes a query, how accurate that is, or any limit on tables or rows.

### Route 2: the connector tool

<!-- volatile verified=2026-11 -->
The connector reference lists three actions: submit a statement, check its status and get results, and cancel. It is a
Premium connector, and the prerequisites say users "must have a premium Power Apps license". The service principal and
delegated connection types are the ones {{topic:sfconnector}} compares. Two limits apply to a shared connection, 900 calls
per 60 seconds and 50 concurrent requests. The submit action also accepts a `query_tag`, which matters in
{{topic:sfcost}}.
<!-- /volatile -->

### Route 3: the managed MCP server

{{topic:sfmcp}} covers what it is. What decides the choice is the Snowflake page's own advice. Expose one Cortex Agent as
the client-facing tool, and expose Analyst or Search directly only when the client should choose between them. Keep
`SYSTEM_EXECUTE_SQL` off the server that holds a governed agent, because a client can use it to bypass semantic views and
verified queries, and put direct SQL on a separate server under a least-privileged role.

<!-- volatile verified=2026-11 -->
Authentication is a security integration. It is a custom OAuth client that allows only the MCP access role and sets
secondary roles to `NONE`. The page splits clients into confidential ones, which can keep a secret, with VS Code and Cursor
as examples, and public ones that use PKCE, with Claude Desktop as the example. One integration can serve every user, who
still signs in individually, and several servers in the same account. Copilot Studio is not named in the text read for this
lesson.
<!-- /volatile -->

### The three side by side

| | Knowledge | Connector tool | Managed MCP |
|---|---|---|---|
| Who writes the SQL | Copilot Studio, at question time | You, once | Snowflake's tools, or your procedures |
| Identity Snowflake sees | The asking user | A service principal, or each user | The connecting user's default role |
| Where the rule lives | The user's role and your table choice | Your view and the connection's role | Grants on the server and each tool |
| Same question, same statement | No | Yes | Depends on the tool |
| Status | Preview, standard harness | Premium connector | Not labelled in the text read |

The pages never compare the routes, and neither company mentions the other's AI features. The two Microsoft pages do not
mention Cortex or MCP, and no Microsoft client is named among the clients on the Snowflake page.

## In practice at Technik

Three questions from the Production Assistant's users go to three different routes.

**"What is the status of work order `100004521`?"** is a named question, so it goes to a connector tool over a view. It needs
one read-only identity, because most users have no Snowflake account ({{topic:connauth}}). Knowledge would generate the
query each time, and MCP would run it as each person's role.

**"What was welding efficiency at Plant 2 last week?"** is long tail. Knowledge over the raw operations table is the trap
from {{topic:snowflakeknowledge}}, where operations confirmed twice give 110.9% against a true 88.9%. The managed route
fixes the definition in a semantic view, and it collides with the agent role's denied table ({{topic:cortexanalyst}}). The
connector fits only once someone names the question and writes the view.

**"What is holding `100004521`, and what does the work instruction say about the porosity?"** mixes rows and passages, which
is the case for one Cortex Agent behind MCP ({{topic:routing}}). It also means the engineer's own role is the identity,
and the capstone's service user cannot connect that way.

The capstone uses none of the three. Its server talks to Snowflake with the Python connector as `TECHNIK_AGENT_SVC`, which
is a fourth route open only to code you host. The three here are the Copilot Studio-facing ones, and the identity of the
caller decides before the question does. If callers have no Snowflake users, knowledge and managed MCP are closed as
designed.

<!-- unknown since=2026-11 -->
Nobody ran any route against a Technik account. The pages do not say whether the GitHub Copilot harness offers Snowflake as
knowledge, whether the generated SQL can be seen, what a knowledge query costs the Snowflake account, or how a Copilot
Studio connection to a managed MCP server is set up. The last question includes the dynamic client registration that
{{topic:mcpcs}} showed Snowflake does not support. The ordering of questions above is this course's position.
<!-- /unknown -->

## Design guidance

- **Decide the identity first.** If callers have no Snowflake users, two of the three routes are closed.
- **Route a named question to a connector tool**, over a view, with the role fixed in the connection.
- **Use knowledge only for exploration**, among users who already hold Snowflake roles, and treat it as preview.
- **Reach for managed MCP when Snowflake should do the reasoning**, and expose an agent, not its parts.
- **Never put `SYSTEM_EXECUTE_SQL` beside a governed agent.** Give it its own server and role.
- **Promote a frequent knowledge question** to a tool with a fixed statement.
- **Write the choice down per question class.** The routes can coexist in one agent.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A user gets an authentication error | Delegated or knowledge route, and the user has no Snowflake login | Create the login, or use a service principal |
| The same question returns different numbers | Knowledge generates a new query each time | Move it to a tool |
| An MCP client sees the wrong data | The session ran as the user's default role | Set the default role and the integration's allowed roles |
| A governed agent is bypassed | `SYSTEM_EXECUTE_SQL` shares its server | Split the servers |
| The connector fails at busy times | One shared connection hit 900 calls a minute | Cut calls per question |
| The preview feature is missing | Wrong harness or tenant | Check both before designing around it |

## Key terms

**Knowledge route**: Snowflake tables added as a Copilot Studio knowledge source, with metadata indexed and queries generated
at runtime.

**Connector route**: SQL you write, run through the Snowflake connector under a connection you choose.

**Managed MCP route**: Snowflake's hosted MCP server, which exposes Snowflake tools to an MCP client.

**Security integration**: the Snowflake object that sets how OAuth clients sign in and which roles they may use.
