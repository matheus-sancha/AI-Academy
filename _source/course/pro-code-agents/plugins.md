## TL;DR

A plugin is a declarative agent's action: an MCP server, or a REST API with an OpenAPI description.
Plugins "aren't enabled as standalone experiences", so they exist only inside an agent. Copilot reads
the plugin manifest, decides when to call, asks the user before sending data, and calls a service
"hosted outside of Microsoft 365". TypeSpec writes the agent and its manifests from one typed source,
and its quietest default is its most dangerous one.

## How a plugin gets chosen

With up to five plugins, the agent "always injects the plugins into the prompt". With more, it uses
semantic matching, "based on the plugin's description, not on any of the individual functions or
tools within the plugin itself", and every tool of a matched plugin comes along. Quality "might
degrade if more than 10 functions or tools are included". So the plugin's description does the
routing, as Copilot Studio's server-level description did in {{topic:mcpcs}}, and a narrow server
beats a broad one ({{topic:toolshaping}}).

## Discovery and consent

An MCP plugin resolves its tools "dynamically at runtime by default", straight from the server. That
is the propagation {{topic:mcpcs}} found Microsoft calling a rug pull. You can pin a fixed tool set in
the manifest instead; REST plugins always use the manifest's.

<!-- unknown since=2026-11 -->
The page says the agent "validates any new or changed tools before using them" and never says what
that validation checks. Don't count it as a review step.
<!-- /unknown -->

Copilot asks before sending data to a plugin the first time. After that, tools that only read need no
confirmation and tools that modify data do, but "Plugin developers can override these defaults."

## TypeSpec

TypeSpec declares the agent with decorators and capabilities, and **Provision** writes them into the
manifest:

*Adapted from the TypeSpec tutorial's sample:*

```typespec
@instructions("""
  Answer from Technik's standards and released controlled documents only.
""")
namespace StandardsAgent {
  op od_sp is AgentCapabilities.OneDriveAndSharePoint<ItemsByUrl = [
    { url: "https://<your-tenant>.sharepoint.com/sites/<your-standards-site>" }
  ]>;
}
```

The scoping array carries all the risk. Leave `ItemsByUrl` out and the agent reaches "all OneDrive
and SharePoint content in your Microsoft 365 organization that the signed-in user can access". Teams
messages, Copilot connectors and web search fail open the same way. Scope is something you opt into.

## At Technik

The standards agent from {{topic:declarative}} reuses the capstone's MCP server as one plugin with
three tools, well inside both thresholds. Pin those three, so a server change reaches the agent
through a release rather than at runtime. Name each SharePoint source explicitly. Left unscoped, the
agent could reach anything an engineer can open, the drafting team's site included.

<!-- unknown since=2026-11 -->
The server only admits callers holding its `Teamcenter.Read` role ({{topic:stageship}}). The page
says a plugin gets "a token or API key from the token store" and says nothing about app roles, so
whether a user's token can pass that check is a tenant test.
<!-- /unknown -->

## Key terms

**Plugin (action sense)** — an MCP or API action inside a declarative agent, described by a plugin
manifest. Not to be confused with the package sense in {{topic:lowvspro}}.

**Dynamic tool discovery** — resolving an MCP plugin's tools from the server at runtime instead of
from the manifest.
