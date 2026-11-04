## TL;DR

A Snowflake-managed MCP server is a **schema object**, not a program: `CREATE MCP SERVER … FROM
SPECIFICATION` takes a YAML list of tools and Snowflake hosts the endpoint, "without needing to
deploy separate infrastructure". You write no transport, no authorization code and no SQL plumbing.
What you give up is the thing you spent the last five lessons controlling. Access runs through
OAuth as the **connecting user**, so the role your tools execute under is theirs, not yours. And the
privileges split in two: "Access to the MCP Server does not give access to the tools. Permission
needs to be granted for each tool."

## Why it matters

Technik's Teamcenter and SAP data is already replicated into Snowflake ({{module:snowflake-sql}}), so
before writing another line of server code there is a question worth asking: why write a server at
all? The answer is not "because ours is better". It is that the two designs answer *who is asking*
differently, and that decides which one your organization can govern.

This is also the first managed MCP server you have met, and the pattern generalises. When a platform
hosts the protocol for you, the protocol stops being where your decisions live. They move into
grants, parameters and a YAML block.

## How it works

### The server is a database object

You create it in a database and schema, and inspect it like anything else — `SHOW MCP SERVERS IN
SCHEMA`, `DESCRIBE MCP SERVER`, `DROP MCP SERVER`. Clients reach it at a URL built from the object's
path:

```text
https://<account_url>/api/v2/databases/<database>/schemas/<schema>/mcp-servers/<name>
```

Six tool types are supported today: `CORTEX_AGENT_RUN`, `CODING_AGENT`,
`CORTEX_SEARCH_SERVICE_QUERY`, `CORTEX_ANALYST_MESSAGE`, `SYSTEM_EXECUTE_SQL` and `GENERIC` for UDFs
and stored procedures. For anything resembling a business question, Snowflake's recommendation is to
expose one Cortex Agent rather than its parts: "This configuration gives the external MCP client one
governed interface and lets the agent select the appropriate resources for each request"
({{topic:cortexagents}}).

*Adapted from the Snowflake specification sample:*

```sql
CREATE OR REPLACE MCP SERVER TECHNIK_DW.OPS.PRODUCTION_MCP
  FROM SPECIFICATION $$
  tools:
    - title: "Governed production data agent"
      name: "production_data_agent"
      type: "CORTEX_AGENT_RUN"
      identifier: "TECHNIK_DW.OPS.PRODUCTION_AGENT"
      description: "Answers governed questions about work orders, operations and quality notifications."
      annotations:
        openWorldHint: false
  $$;
```

### Two layers of permission

`USAGE` on the MCP server lets a role "connect with the MCP server and discover tools". Invoking one
needs a second grant on whatever sits underneath it — `USAGE` on a Cortex Search service or an agent,
`SELECT` on a semantic view, `USAGE` on a function or procedure. The two-layer design produces a
distinctive symptom: a tool the client can see and cannot call. Snowflake's own troubleshooting table
names it — "A visible tool can't be invoked" → "The default role is missing an underlying object
privilege".

### Who the tools run as

This is the part that is not yours. Snowflake OAuth is the default, with External OAuth available to
bind an identity provider such as Okta or Entra ID. In either case, "the OAuth session uses the
connecting user's `DEFAULT_ROLE` as the primary role". Scopes can advertise other roles, but two
things blunt that. The default scope is named misleadingly: "`session:role:all`: Use the user's
`DEFAULT_ROLE` as the primary role. Despite the name, this doesn't activate every role or secondary
roles." And several clients cannot ask for a role at all — Snowflake names Claude as one that
"request[s] `session:role:all` instead".

The recommended configuration is therefore least privilege by subtraction: leave
`OAUTH_USE_SECONDARY_ROLES = NONE`, restrict `ALLOWED_ROLES_LIST` to the MCP access role, and set
each user's `DEFAULT_ROLE` and `DEFAULT_WAREHOUSE` ({{topic:sfroles}}). A session with no default
warehouse "fail[s] to initialize". And when per-user differences genuinely matter, the answer is
structural, not scope-based: "use separate MCP servers with dedicated roles."

### The limits worth knowing before you design around it

Snowflake "supports Model Context Protocol revision 2025-11-25" — one revision behind the
`2026-07-28` that {{topic:mcparch}} describes — and "only supports tool capabilities". Resources,
prompts, roots, notifications, version negotiations, lifecycle phases and sampling are all
unsupported. Dynamic client registration is not supported either, which rules out the one Copilot
Studio path that needs it ({{topic:mcpcs}}).

Three numbers shape the design. A server holds **at most 50 tools**, and "Higher tool counts can
degrade tool-selection accuracy". Generic and SQL-execution responses are **truncated at 250 KB** —
the explicit answer to a question VS Code's documentation leaves silent ({{topic:budget}}) — while an
agent tool's reply "includes all intermediate steps by design" and "can result in large response
payloads (200 KB or more)". And recursion is capped at **10 invocations**, because an agent reachable
through MCP can be configured to call back into itself.

One warning deserves repeating, because it is the module's recurring shape. Tool annotations —
`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint` — "are client-facing hints, not
security controls. Snowflake doesn't validate that a tool behaves as its annotations claim." Worse,
the defaults are pessimistic rather than safe: `GENERIC` and `CORTEX_AGENT_RUN` tools default to
`readOnlyHint: false` and `destructiveHint: true`, so a read-only tool advertises itself as
destructive until you say otherwise.

## In practice at Technik

Set the capstone's server beside a managed one and the trade is clear.

The capstone exposes three narrow tools over three curated views, with bound parameters and typed
identifiers, running as `TECHNIK_AGENT_SVC` — a `TYPE = SERVICE` user holding only `TECHNIK_AGENT_RO`
({{topic:stagemcp}}). Every question any engineer asks reaches Snowflake as the same identity, and
the read-only role is the boundary.

A managed server cannot reproduce that. A service user cannot complete a browser OAuth flow, so the
session would run as each engineer's own default role — which is {{topic:connauth}}'s question
arriving in a new place, and a real decision rather than an oversight. Exposing `SYSTEM_EXECUTE_SQL`
would also hand the model arbitrary SQL under that role, where the capstone hands it three
statements it cannot rewrite.

Where the managed server wins outright is the half Technik's server cannot do at all: Cortex Search
over the controlled documents and Cortex Analyst over the semantic model ({{module:advanced-rag}}).
The sensible end state is both — Technik's server for the narrow, audited Teamcenter lookups, a
managed server for the governed analytical questions, each with its own role.

<!-- unknown since=2026-11 -->
Neither has been run. Whether an Agent Framework agent can hold a Snowflake-managed server and an
Entra-protected server at once, and present an acceptable identity to each, is untested here.
<!-- /unknown -->

## Design guidance

- **Expose an agent, not its parts**, when the client should not be choosing between search and SQL.
- **Grant the server and the tools separately**, and expect "visible but not callable" while you get
  it wrong.
- **Set `DEFAULT_ROLE` and `DEFAULT_WAREHOUSE`** on every user who will connect. Scopes will not
  rescue you.
- **Split servers before you split scopes** when two audiences need different data.
- **Never read an annotation as a guarantee.** It is a hint to a client, and the default says
  destructive.
- **Keep tool counts far below 50**, for selection accuracy rather than for the limit.
- **Design for 250 KB**, by returning narrower rows rather than hoping a result fits.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Tools are listed but every call fails | No grant on the underlying object | Grant per tool, not just `USAGE` on the server |
| The session sees the wrong data | The user's `DEFAULT_ROLE` is not the MCP role | Set it explicitly; the client may not send a scope |
| The session never initialises | No default warehouse on the user | Set `DEFAULT_WAREHOUSE` and grant `USAGE` on it |
| A client cannot resolve the host | Underscores in the account hostname | Use hyphens instead |
| `invalid_client` with correct credentials | A network policy blocked the client's IPs | Allow the client provider's outbound addresses |
| Results arrive incomplete | The 250 KB truncation | Return fewer columns or rows per call |
| The server is missing after failover | MCP server objects are not replicated | Recreate them on the secondary account |

## Key terms

**Snowflake-managed MCP server** — an MCP endpoint declared as a schema object from a YAML
specification, hosted by Snowflake, exposing Cortex and custom tools.

**Tool annotation** — a client-facing hint (`readOnlyHint`, `destructiveHint`, `idempotentHint`,
`openWorldHint`) describing how a tool behaves. Unvalidated, and not a security control.

**MCP access role** — the dedicated Snowflake role granted `USAGE` on the server plus the privileges
its tools need, and set as the connecting user's default role.
