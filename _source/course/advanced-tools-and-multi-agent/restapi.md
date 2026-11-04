## TL;DR

Upload an OpenAPI file, pick an authentication type, choose which operations to expose, and the agent
has tools — no connector portal to visit. It is the shortest route from an API to an agent, and it is
in preview: "Preview features aren't meant for production use and may have restricted
functionality." The catch is not the preview label. It is that the page never says whether what it
builds is a connector, and {{topic:mcpcs}} showed how much rides on that answer.

## What it actually takes

<!-- volatile verified=2026-11 -->
From the agent's **Overview** page: **Add tool** → **New tool** → **REST API**, then drag in the
spec. The format is strict — "The OpenAPI specification must be a JSON file in v2 format" — though
"If you submit a v3 specification, the creation process automatically translates it to a v2
specification." Next a description and an optional **Solution**, then **Authentication**: **None**,
**API key** (where "The user of the agent provides the API key", prompted at runtime), or OAuth 2.0
with client ID, secret and three URLs. Then select operations, describe each, and connect.
<!-- /volatile -->

Everything here is "powered by the standard harness", so {{topic:chooseharness}} decides whether it
is available to you.

The descriptions are the work. "Provide a detailed description, because your agent orchestration uses
the description to determine when to use the particular tool." They arrive "initially prepopulated
from the descriptions in the API specification", and the product will not let you skip them: "If any
of the descriptions are blank, you must complete them before you can move forward." That is
{{topic:tooldesc}}'s rule enforced by a form — the only place in this module where it is.

## The question the page does not answer

<!-- unknown since=2026-11 -->
Nothing on the page says whether a REST API tool is a Power Platform connector. Its own solution text
leaks the word — "your selected connector is already in the solution" — but connection references,
data policies and DLP are never mentioned. So whether {{topic:dlp}} governs these tools as
{{topic:mcpcs}} found it governs MCP is unverified. Assume connector rules apply until an
administrator proves otherwise.
<!-- /unknown -->

The page also offers no comparison with {{topic:customconn}} and no when-to-use guidance, so the
choice is yours to argue. And its OAuth section is headed "Auth 2.0" and reads "if your MCP server
uses OAuth 2.0" — copied from the MCP page, which measures how settled this surface is.

## At Technik

The Teamcenter live-status endpoint {{topic:customconn}} wraps could be added this way in minutes.
Technik should not, and the reason is reuse rather than preview status: the document revision flow in
{{module:automation-and-workflows}} needs that call too, and a tool defined inside one agent helps
only that agent. Reach for this when exactly one agent will ever call the API.

## Key terms

**REST API tool** — an agent tool generated from an uploaded OpenAPI v2 specification, configured per
agent rather than registered tenant-wide.

**Tool description** — the sentence the orchestration reads to decide whether to call an operation.
Prepopulated from the spec, and the one field the form will not let you leave empty.
