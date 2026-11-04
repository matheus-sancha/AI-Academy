## TL;DR

Copilot Studio does not talk to your server directly. Access "relies on Power Platform connectors
for connectivity", so your server arrives in the tenant as a connector and inherits everything that
governs one. Three things stop being yours the moment you register it. The **server description** is
what the orchestrator reads: "The agent orchestrator uses this information to identify whether to
call your server at runtime." Your **edits ship themselves** — Copilot Studio "dynamically reflects
these changes" and "removes obsolete tools and resources", with no version to pin. And a **data
policy** you do not own decides whether anyone can reach you at all.

## Why it matters

{{topic:mcpadd}} taught the consuming side, and noted in passing that an added server's tool surface
can change without you touching the agent. You are now on the other end of that sentence. The
convenience belongs to the maker; the obligation is yours.

What changes is the shape of a mistake. In the editor a wrong description is a five-second edit
({{topic:mcpvscode}}). Here it is a wrong tool call inside an agent you have never seen, made for a
user you cannot identify, produced by text you wrote weeks earlier. Microsoft states the division
plainly: "When you connect to a non-Microsoft product, including an
external MCP server, you're responsible for the tools and resources you access from within Copilot
Studio."

## How it works

### What reaches your server, and over what

<!-- volatile verified=2026-11 -->
Two routes. The **MCP onboarding wizard** is the recommended one — on the agent's **Tools** page,
**Add a tool** → **New tool** → **Model Context Protocol** — and it asks for a server name, a server
description, a server URL and an authentication type. The second route is a **custom connector in
Power Apps**, built by importing an OpenAPI definition that declares the protocol on the operation:
`x-ms-agentic-protocol: mcp-streamable-1.0`.

Transport is settled for you: "Currently, Copilot Studio supports the Streamable transport type", and
"Copilot Studio no longer supports SSE for MCP after August 2025" — the deprecation
{{topic:transports}} describes. Of the three primitives, "Copilot Studio currently supports MCP tools
and resources", so a server whose value is in its prompts has nothing to offer here. Generative
orchestration must be turned on.
<!-- /volatile -->

### Two descriptions now, not one

{{topic:tooldesc}} taught that a tool's description is its interface, and {{topic:buildmcp}} made it
a docstring. Registration adds a second description a level up, written in Copilot Studio rather than
in your code: "Write a brief, but clear description of what your MCP server does." The orchestrator
uses it to decide whether to come to you at all, before it looks at any tool. So the server sentence
is routing and the docstrings are selection — and only one of the two lives in your repository.

### Your edits are the release

There is no publish step and no version. Tools you add appear, tools you remove disappear, and a
docstring you reword reaches every agent holding the server. For a well-run server that is pure
upside. It is also the mechanism {{topic:mcpsec}} calls a rug pull, which Microsoft describes as
"hosted MCP server scenarios, where tool definitions can be dynamically amended to include malicious
content later". Nothing distinguishes your careless Tuesday from an attack, because the propagation
path is the same one.

### Authentication, and where it stops matching the spec

<!-- volatile verified=2026-11 -->
The wizard offers **None**, **API key** — sent as a header or a query parameter, where "The user of
the agent provides the API key" — and **OAuth 2.0** in three flavours: **Dynamic discovery**,
**Dynamic** and **Manual**. Manual takes a client ID, client secret, authorization and token URLs, a
refresh URL and optional scopes, then hands back a callback URL you must add to your app
registration.
<!-- /volatile -->

Note what the simplest option rests on. Dynamic discovery requires that your server support "the
OAuth 2.0 dynamic client registration (DCR) with discovery mechanism" — and DCR is the mechanism the
authorization specification now marks deprecated ({{topic:mcpauth}}). The convenient path here is the
one the protocol is moving away from.

### The governance you inherit

Because MCP rides on connectors, connector policy *is* MCP policy: "Blocking Power Platform
connectors also blocks access to tools in connected MCP servers, which rely on Power Platform
connectors for connectivity." Data policies sort connectors into **Business**, **Non-business** and
**Blocked** ({{topic:dlp}}), and two details decide whether your server is usable at all. Connectors
"introduced after 2019 … are likely to be part of the default 'Non-business' group", and "In many
organizations, connectors in the 'Non-business' group are automatically blocked." Within one policy,
connectors "must be in the same data group because data can't be shared among connectors that are in
different groups" — so an agent combining your server with a Business connector can fail on
classification alone.

Enforcement is real time, exemptions are gone, and a tenant-scoped policy "appl[ies] to all agents in
all environments across the tenant". A maker sees a blocked connector "disabled when a maker adds
tools to an agent"; a violation makes **Publish** unavailable, with a downloadable file carrying one
row per violation.

<!-- volatile verified=2026-11 -->
Every page in this flow is marked "features used in agents or agent flows powered by the standard
harness". Adding an MCP server as a tool on the GitHub Copilot harness shipped separately, in
preview, in July 2026 — so {{topic:chooseharness}} decides which set of instructions applies to you.
<!-- /volatile -->

## In practice at Technik

The capstone's server ships to Foundry, not Copilot Studio ({{topic:stageship}}), and what handing it
over would need shows where the two models disagree.

Two requirements it already meets: a public HTTPS endpoint, and stateless streamable HTTP, which
Container Apps needed anyway. The third is where it breaks. The deployed server authenticates callers
through Entra built-in authentication and a required `Teamcenter.Read` app role, with the agent
presenting its own Entra Agent ID — one machine identity for every question. None of the wizard's
three options expresses that: **API key** would make the secret per-user, and **OAuth 2.0** would
have every Technik engineer consent individually to a server whose Snowflake role is a single
read-only service identity ({{topic:connauth}}).

So Technik's server is built for one caller it trusts, and Copilot Studio expects a server built for
many callers it does not. The conversation to have first is with whoever owns the tenant's data
policies — because a connector landing in **Non-business** in an organization that blocks that group
means a server that works perfectly and is unreachable.

*A minimal OpenAPI stub for the Power Apps route, adapted from the Copilot Studio sample:*

```yaml
swagger: '2.0'
info:
  title: Technik Teamcenter
  description: Teamcenter revisions and controlled documents
  version: 1.0.0
host: <your-server-host>
basePath: /
schemes: [https]
paths:
  /mcp:
    post:
      summary: Technik Teamcenter MCP server
      x-ms-agentic-protocol: mcp-streamable-1.0
      operationId: InvokeMCP
      responses:
        '200':
          description: Success
```

## Design guidance

- **Write the server description as routing copy.** It decides whether the orchestrator considers you
  at all, and it is the one description you cannot change by committing.
- **Treat every edit as a release.** There is no pin, so your review gate is the only gate.
- **Ask about data policies before you build the connector.** Classification is a tenant decision,
  and for your server it is binary.
- **Keep the tool set narrow.** Each tool costs context in every agent that holds your server.
- **Pick the OAuth flavour the spec still endorses**, even when dynamic discovery is fewer clicks.
- **Say which harness you support** in your own documentation, because the product's pages do.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The orchestrator never calls your server | A vague server-level description | Rewrite it as what the server is for, not what it is |
| A tool vanishes from live agents | A rename propagated with no version step | Treat renames as breaking, and announce them |
| The connector appears disabled to makers | A data policy blocks its group | Get it classified with the connectors it must work beside |
| An agent cannot publish | Connectors split across data groups | Move them into one group with the admin |
| OAuth works nowhere | The callback URL was never registered | Copy it from Copilot Studio into the app registration |
| Prompts you expose are ignored | Only tools and resources are supported | Move the logic into a tool |

## Key terms

**MCP onboarding wizard** — the Copilot Studio flow that registers a server from a name, description,
URL and authentication type, and writes the connector for you.

**Server description** — the sentence the orchestrator reads to decide whether to route to your
server. It lives in Copilot Studio, not in your code.

**Data policy** — the Power Platform rule sorting connectors into Business, Non-business and Blocked.
It governs your MCP tools because MCP reaches them through a connector.
