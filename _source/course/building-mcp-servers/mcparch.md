## TL;DR

An MCP **host** is the AI application; it creates one **client** per **server**, and each server
offers **tools**, **resources** and **prompts** over JSON-RPC 2.0. The fact that reorganises
everything else: as of protocol revision `2026-07-28`, **MCP is stateless**. Every request carries
its own protocol version, capabilities and client identity, the server "infer[s] nothing from
previous requests", and `server/discover` is a convenience rather than a handshake. Sampling and
logging are deprecated in this revision; elicitation is not.

## Why it matters

In Intermediate you added someone else's server and the protocol stayed invisible
({{topic:mcpadd}}). Owning one makes it visible, and statelessness is the part that changes your
design rather than your vocabulary.

A stateful protocol lets a server hold things between calls: who you are, what you asked last, a
cursor, a cached permission. A stateless one does not. Anything your server needs on the second call
has to arrive on the second call, or be derivable from the data it reads. That one constraint is why
the capstone's server is three independent lookups rather than a conversation, why it runs on several
replicas without a sticky session ({{topic:stageship}}), and why a crashed stdio server can simply be
restarted under you.

It also bounds what MCP is for: it "focuses solely on the protocol for context exchange—it does not
dictate how AI applications use LLMs or manage the provided context" ({{topic:harnessvssdk}}).

## How it works

### Three participants, and the one that is not a participant

> "MCP follows a client-server architecture where an MCP host — an AI application […] — establishes
> connections to one or more MCP servers. The MCP host accomplishes this by creating one MCP client
> for each MCP server."

| Participant | The documentation's definition |
|---|---|
| **Host** | "The AI application that coordinates and manages one or multiple MCP clients" |
| **Client** | "A component that maintains a connection to an MCP server and obtains context from an MCP server for the MCP host to use" |
| **Server** | "A program that provides context to MCP clients" |

The model is not in that list, and Microsoft's curriculum says so outright: "The AI model is not
itself an MCP client." The host holds the clients and calls the model; the two never meet directly.

Where a server runs is not part of what it is — "MCP servers can execute locally or remotely" — and
the transport is what differs ({{topic:transports}}). One asymmetry follows: "Local MCP servers that
use the STDIO transport typically serve a single MCP client, whereas remote MCP servers that use the
Streamable HTTP transport will typically serve many MCP clients."

> [!NOTE]
> The text says one client per server, while the same page's diagram shows two clients on one remote
> server, unexplained. Read *one client per connection* as the rule.

### Two layers

The **data layer** "defines the JSON-RPC based protocol for client-server communication, including
capability and version discovery, and core primitives". The **transport layer** "defines the
communication mechanisms and channels", including "connection establishment, message framing, and
authorization". The same JSON-RPC 2.0 format rides every transport, which is why
{{topic:transports}} is a separate decision.

### Stateless, and what replaces the handshake

> "MCP is a stateless protocol (Every request contains all the information needed to process it, so
> servers infer nothing from previous requests)."

Each request carries three fields in `_meta`: `io.modelcontextprotocol/protocolVersion`,
`io.modelcontextprotocol/clientCapabilities` and `io.modelcontextprotocol/clientInfo`. Capability
negotiation is therefore per request, not per connection: "The client declares its capabilities […]
on every request, and the server returns its own `capabilities` object from `server/discover`."

`server/discover` returns `supportedVersions`, a `capabilities` object, `serverInfo` and cache hints
(`ttlMs`, `cacheScope`). Servers must answer it, and the documentation is explicit that clients may
skip it: "Calling `server/discover` is optional. Because every request carries the same `_meta`
fields, a client is free to send any request directly and handle a version error if one comes back."
A version the server does not speak returns an `UnsupportedProtocolVersionError` listing the ones it
does.

### The primitives, and their method names

"MCP defines three core primitives that *servers* can expose": **tools** ("Executable functions that
AI applications can invoke"), **resources** ("Data sources that provide contextual information") and
**prompts** ("Reusable templates that help structure interactions with language models"). The naming
rule is mechanical — discovery `*/list`, retrieval `*/get`, execution `tools/call` — so a client
lists before it calls, and "This design allows listings to be dynamic."

<!-- unknown since=2026-11 -->
The rule and the examples disagree on one method. The page states retrieval is `*/get`, then names
the resource methods as `resources/list` and `resources/read`. It never writes `prompts/list`,
`prompts/get` or `resources/get` at all. Read method names out of your SDK rather than inferring
them from the pattern.
<!-- /unknown -->

Clients expose primitives too. **Elicitation** lets a server "request additional information from
users […] or ask for confirmation of an action", through `elicitation/create`, delivered by the
Multi Round-Trip Requests pattern rather than as a server-initiated request. Two others are
**deprecated as of `2026-07-28`**: **sampling** (`sampling/createMessage`), where "New
implementations should integrate directly with LLM provider APIs", and **logging**, where "New
implementations should log to `stderr` (stdio transport) or use OpenTelemetry". Microsoft's
curriculum records the same shift, listing the "deprecation of Roots, Sampling, and Logging".

### Notifications are opt-in

A changed tool list does not simply arrive. "Change notifications are opt-in: the client opens a
long-lived `subscriptions/listen` stream naming the notification types it wants", the server
acknowledges with `notifications/subscriptions/acknowledged` reflecting only the types it agreed to,
and then sends `notifications/tools/list_changed`. Two properties bind a server author: the
notification is only available "from servers that declared `"listChanged": true` in their tools
capability", and delivery is **best effort** — "There are no guarantees that every notification will
be sent or received […] Clients should also rely on polling."

## In practice at Technik

The capstone's Teamcenter server is one `MCPServer` object with three tools and no session state at
all. Its constructor carries the one thing a client reads before any tool:

*From [`server/teamcenter.py`, lines 30–32](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/server/teamcenter.py#L30-L32):*

```python
mcp = MCPServer("technik-teamcenter", instructions=(
    "Read-only lookups in Technik's Teamcenter: controlled documents, the items each work order "
    "operation uses, and whether a revision is the released one. It holds metadata, not document text."))
```

Three tools, three independent questions, none depending on a previous call — which is what makes
them safe under a stateless protocol. When the agent needs two facts about work order `100004510` —
which drawing operation `0010` uses, and whether that revision is still the released one — it makes
two calls and joins them itself ({{topic:stagemcp}}).

The only state in the process is a cached Snowflake connection, and that is performance rather than
protocol state: lose it and the next call reopens it. Nothing about the conversation lives in the
server, so VS Code starting it over stdio and Container Apps running several replicas of it are the
same server with the same guarantees ({{topic:stageship}}).

## Design guidance

- **Make every tool answerable alone.** A tool that only makes sense after another one ran is state
  the protocol will not keep for you.
- **Validate each request on its own merits.** You cannot rely on having seen the caller before.
- **Put the server's purpose in `instructions`**, so a client knows what it is for before listing.
- **Declare `listChanged` only if you really change.** Clients subscribe on the strength of it, and
  polling is their only backstop.
- **Pick the primitive by who acts.** The model calls a tool; the host reads a resource; a person
  chooses a prompt ({{topic:tooldesc}}).
- **Do not build on sampling or logging.** Both are deprecated here; integrate a model directly and
  log to `stderr`.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The second call behaves as though the first never happened | It didn't — the protocol is stateless | Pass what the call needs; derive the rest from data |
| A tool works for one client and not another | A capability the other client never declared | Read `clientCapabilities` per request rather than assuming |
| Clients never notice a new tool | `listChanged` not declared, or the client never subscribed | Declare it, and expect clients to poll anyway |
| A client rejects every request | Protocol version mismatch | Read `supportedVersions` from `server/discover` |
| A per-user cache answers wrongly behind a load balancer | Process state under a stateless protocol | Keep caches derivable, not authoritative |

## Key terms

**Host** — the AI application that manages one or more MCP clients and calls the model; the model is
not itself a client.

**`server/discover`** — the request returning supported versions, capabilities, identity and cache
hints. Servers must answer it; clients may skip it.

**`_meta`** — the per-request field carrying protocol version, client capabilities and client
identity. It is what makes the protocol stateless.

**Primitive** — a tool, resource or prompt (server side), or elicitation (client side).
