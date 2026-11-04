## TL;DR

A custom connector is "a wrapper around a REST API that allows Logic Apps, Power Automate, Power
Apps, or Copilot Studio to communicate with that REST or SOAP API". You write no server: you describe
someone else's API in OpenAPI, choose an authentication method — "Microsoft Entra ID is recommended"
— and the platform builds the connector. What you gain is reach, since one connector serves every
maker in the tenant. What you take on is the inverse of {{topic:mcpcs}}'s problem: there your edits
ship themselves; here they reach nobody until each consumer rebuilds its connection.

## Why it matters

{{topic:connectors}} told you to search your environment rather than trust that a connector exists.
This is what you do when the search comes back empty: "Custom connectors address this scenario by
allowing you to create (and even share) a connector with its own triggers and actions."

It is also the second of this level's two answers to the same question, and the comparison is the
point. An MCP server is code you own, deployed where you choose, speaking a protocol
({{module:building-mcp-servers}}). A connector is a definition you register, hosted by the platform,
usable by Power Automate and Power Apps as well as by agents. Neither is the advanced choice; the one
that fits is the one whose *consumers* match.

## How it works

### The lifecycle, and where the work actually is

The documentation walks six numbered steps: build the API, secure it, describe it and define the
connector, use it, share it, certify it. Only the third is connector work. The API is yours to build
and host, "Public (visible on the public internet)" or "Private (visible only to your network)" —
and for a private one, "Microsoft offers on-premises data connectivity through an on-premises data
gateway."

Three ways to produce the definition: an OpenAPI definition, "A Postman collection", or "Start from
scratch using the custom connector portal (Power Automate and Power Apps only)". The last is no
different underneath — "Behind the scenes, Logic Apps, Power Automate, Power Apps, and Copilot Studio
use OpenAPI to define connectors."

<!-- volatile verified=2026-11 -->
Built from blank, the portal asks for a **Scheme**, a **Host** and a **Base URL**, then an
authentication type, then one or more actions. An action takes a **summary**, a **description** and
an **operation ID**, which "must be a text string with no spaces". **Import from sample** turns a
request URL into a parameter list, and **Add default response** turns a sample JSON body into an
output schema.
<!-- /volatile -->

### Authentication, and the maintenance event that proves the connector is not only yours

Four standard methods are offered: generic OAuth 2.0, "OAuth 2.0 for specific services, including
Microsoft Entra ID, Dropbox, GitHub, and SalesForce", basic authentication, and API key. The
recommendation saves you writing code: "You can set up Microsoft Entra ID authentication for your API
in the Azure portal so you don't have to implement authentication."

Then read the sentence that tells you what owning a connector costs. "If you have older custom
connectors created before February 2024 that were using the global redirect URI, those connectors
were updated or stopped working for new connections after the per-connector redirect URI was
enforced." A platform decision, applied to connectors nobody had touched, breaking *new* connections
rather than existing ones — so the symptom arrives weeks later, for one person. The fix is a checkbox
(**Update to unique redirect URL**) or `"redirectMode": "GlobalPerConnector"` through the CLI, then
registering the new URL on the OAuth app.

### Why your updates do not propagate

"You need to create a connection to your API in order to use that connection to call any operations
that you expose in your custom connector." That connection is the problem. When a field changes, the
documented procedure has three steps: republish the connector, "Remove any connection / data source
in any app that used that connector", then re-add it.

So a connector's blast radius is wide and its propagation is nil — the exact inverse of
{{topic:mcpcs}}, where a reworded docstring reaches every agent with no release step. Reach is
asymmetric too: a connector built in Power Automate or Power Apps is available in both and in Copilot
Studio, but "This availability isn't true for connectors created in Logic Apps." Certification is for
breadth only — needed to "share your connector with all users", never to use your own, which is where
{{topic:mcpcert}} landed from the other side.

### The descriptions, and what nobody documents

{{topic:tooldesc}} established that a description is an interface, and {{topic:mcpcs}} found a second
description living outside your repository. A connector has three naming fields, and the only
guidance on them addresses the wrong readers: the summary and description "will be show in Power
Automate to identify the action whereas Operation ID will be used in Power Apps".

<!-- unknown since=2026-11 -->
Neither source says which of those fields a Copilot Studio orchestrator reads when it chooses an
operation, or how to write them for a model rather than for a maker. Neither covers **policy
templates**, the request- and response-shaping rules a definition can carry. And neither settles
licensing: the overview omits it, and the blog's only statement is a four-year-old comment reply.
<!-- /unknown -->

So write them to {{topic:tooldesc}}'s rule — what the operation is *for* — and verify by watching the
orchestrator choose, the way {{topic:addconnector}} does.

## In practice at Technik

Technik's agents read Teamcenter through Snowflake, where it lands overnight, and the capstone's MCP
server queries exactly that replica ({{topic:stagemcp}}). So a connector's job here is the question
the replica cannot answer: *was this revision released today?* A drawing released this morning misses
`V_RELEASED_REVISIONS` until tonight, and an agent answering from the replica is confidently a day
stale.

Teamcenter has a REST API and no prebuilt connector, the stated trigger for building one. A `Technik
Teamcenter Live` connector with one operation — `GetItemRevisionStatus`, taking an 11-character
Teamcenter number and returning its current release status — gives the Production Assistant a
same-day answer beside its replica tools, and gives the document revision flow in
{{module:automation-and-workflows}} the same check from Power Automate with no second integration.
That shared reach is the whole argument for a connector over a second MCP server.

Secure it with Entra ID in front of the API rather than an API key, because an API key here is
supplied per connection and Technik's agents run as one service identity ({{topic:agentid}}). And
since Teamcenter sits on Technik's own network, this is the gateway case — with the caveat the
overview spells out: "OAuth and token requests do not transit the linked Virtual Network."

## Design guidance

- **Choose by consumer, not by sophistication.** A connector if Power Automate and Power Apps need it
  too; an MCP server if only MCP clients will call it.
- **Keep the operation list short and each operation narrow** ({{topic:toolshaping}}). A connector you
  cannot change cheaply deserves few commitments.
- **Put authentication in front of the API, not inside it.** Entra ID in the portal is the recommended
  path and the one that composes with {{topic:agentid}}.
- **Write the operation description for the orchestrator** even though nothing documents that it is
  read. Being right is free; being terse can cost a wrong call.
- **Version the API and add operations rather than change them**, because a changed field makes every
  consumer rebuild its connection. Expect platform-side maintenance too: February 2024's
  redirect-URI change is the model, a connector breaking without a commit.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| New connections fail while existing ones work | The pre-2024 global redirect URI | Apply **Update to unique redirect URL**, then register the new URL on the OAuth app |
| The connector returns fresh data; the agent answers stale | It chose a replica tool instead | Make the operation description say *live* and *today* |
| An app breaks after a connector update | Its connection still holds the old definition | Remove and re-add the connection in every consumer |
| The connector is missing in Power Automate | It was created in Logic Apps | Recreate it from the same OpenAPI definition |

## Key terms

**Custom connector** — a wrapper around a REST or SOAP API, defined in OpenAPI and registered in the
tenant, that Copilot Studio, Power Automate, Power Apps and Logic Apps can all call.

**Operation ID** — a space-free identifier for one action in the definition, used in Power Apps. Its
siblings, summary and description, are what a maker sees.

**Per-connector redirect URI** — the OAuth callback now issued per connector, enforced after February
2024, replacing a global URI every custom connector once shared.
