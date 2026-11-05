## TL;DR

The decision is made per component, not per project. Microsoft's own guide says "A plugin can use
more than one tool" and tells you to choose "based on the components, target experiences, authoring
approach, lifecycle requirements, and current product support". Agent Builder, Copilot Studio, the
pro-code declarative routes and a custom engine agent are not a ladder to climb. Each component (an
agent, an action, a server) goes on the route whose ceiling its hardest requirement fits under, and a
working system usually spans more than one.

## Why it matters

{{topic:stack}} drew the map and {{topic:harnessvssdk}} asked where the loop lives. Neither tells you
what to do when the requirement list is concrete and the routes overlap. The overlap is the trap:
three routes can produce a declarative agent, and the difference between them shows up in the second
month, when you need a staging environment, a pipeline or an evaluation run and find your route has
none.

The guide is also explicit that its matrix is partial: "If a combination isn't listed, check the
current product documentation instead of inferring that it's supported or unsupported." A missing
row is not a no. It is not a yes either.

## How it works

### One word, two meanings

The guide is written around a **plugin**, and the word has moved. Here it means the whole Microsoft
365 app package (agent, skills, connectors, MCP-based capabilities) that ships together. In
{{topic:plugins}} the same word means only an MCP or API action inside a declarative agent, and that
page says so twice. When a colleague says "plugin", ask which one.

### The filter

Read the guide's starting points as a filter on requirements rather than on job titles.

- **Agent Builder** gives "natural-language configuration and a test pane without requiring a
  source-code project". Its exit is written into the guide: "If your scenario requires workflow logic
  or integrations beyond its supported configuration, compare Copilot Studio or a pro-code route"
  ({{topic:agentbuilder}}).
- **Copilot Studio** fits when the solution needs "managed integrations, workflow logic,
  environments, governance, analytics, or enterprise lifecycle capabilities", and the harness you
  chose decides the rest ({{topic:chooseharness}}).
- **A pro-code declarative agent**: "Choose a source-controlled pro-code workflow when you need
  direct manifest and API integration control." Two tools compete for it. Work IQ Dev Tools (`wiqd`)
  is in preview. The Microsoft 365 Agents Toolkit used directly gives "lower-level control of a
  supported Microsoft 365 app package or capabilities outside the supported Work IQ Dev Tools scope"
  ({{topic:declarative}}).
- **A custom engine agent** is built with the "Microsoft 365 Agents SDK or another supported
  custom-engine stack". The guide stops at that row. Agent Framework and Foundry appear nowhere on it.
  They answer the runtime question, and {{topic:customengine}} is how they reach a Microsoft 365 user.

### Lifecycle is where the routes really differ

Most requirement lists describe what the agent should do. The ones that decide the route describe how
it changes. For declarative agents the guide credits Work IQ Dev Tools with "Named development,
staging, and production environments", offline validation, and "Terminal, JSON-output, or continuous
integration workflows". Three details belong in the decision rather than the footnotes:

<!-- volatile verified=2026-11 -->
- **Evaluation stops at the declarative boundary.** `wiqd agent eval` "Applies to deployed
  declarative agents, not custom engine agents." Choose a custom engine and the evaluation harness is
  yours to build ({{topic:evalharness}}).
- **Pipeline identity covers less than it sounds.** WIQD's trusted-pipeline authentication "applies
  only to core lifecycle operations such as provision, publish, and share. It doesn't authenticate
  Work IQ monitoring, evaluations, or other extensions." A CI job that evaluates needs another
  credential ({{topic:cicd}}).
- **The editor extension is not a gate.** It is "Inner-loop static validation only; keep CLI
  validation in continuous integration."
<!-- /volatile -->

Agent Builder has none of these, by design. Copilot Studio has its own, in environments, solutions
and pipelines ({{module:alm-and-governance}}), which is why it is a route and not a stepping stone.

<!-- unknown since=2026-11 -->
The guide never says whether an agent built in Agent Builder can be brought into a source-controlled
project. WIQD can "Create or import" a Microsoft 365 app package, which is not the same thing, and
the one documented move out of Agent Builder runs to Copilot Studio ({{topic:stack}}). Assume an
Agent Builder agent that needs a pipeline is rebuilt, not exported.
<!-- /unknown -->

### GitHub Copilot is not a route

It appears in the guide because people expect it there. It "assists the selected authoring route; it
doesn't own the Microsoft 365 package, publishing, or runtime." Using it to write a manifest does not
decide how that manifest ships.

### Ownership is a requirement too

The guide ends on a table with nothing technical in it: per component, build or reuse, tool, owner,
prerequisites. "For each component, identify the system of record, the owning team, and the tool
that produces the artifact used in the plugin." Its readiness checklist adds that "Teams understand
which tool and repository are the system of record." Two routes that both work become one wrong
answer when nobody owns the second.

## In practice at Technik

Run Technik's assets through the filter and they land on three routes, which is the normal result.

| Component | Hardest requirement | Route | System of record |
|---|---|---|---|
| Production Assistant (Intermediate) | Teams for four user groups, skills, Snowflake tools, evaluation sets | Copilot Studio, GitHub Copilot harness | Its Copilot Studio solution |
| Teamcenter MCP server (capstone) | A tool over `V_OPERATION_DOCUMENTS` that connects as one read-only role | Code, on Container Apps | `technik-capstone` |
| A standards agent in Word | The Standards site and the Controlled Documents library, beside an open draft | Pro-code declarative agent | Its own repository |

The third row is hypothetical, and it makes the point. A manufacturing engineer drafting revision C of
`SWI70000318` in Word wants the acceptance criteria next to the draft. That is retrieval over
Microsoft 365 content with nothing to orchestrate, so it is a declarative agent. Technik wants it
reviewed and promoted through staging like everything else, so it takes the source-controlled route,
not Agent Builder. The MCP server is not rebuilt for it. It is reused as an action
({{topic:plugins}}), and its owner stays the capstone team.

Notice what never happened: no component moved up a route because it felt more serious. The server
is code because no configuration could express its connection identity. The assistant stays in Copilot
Studio because nothing on its requirement list exceeds it.

## Design guidance

- **Decide per component.** Fill in the guide's summary table (component, build or reuse, tool,
  owner, prerequisites) before choosing anything.
- **Let the hardest requirement pick the route**, and write down which requirement it was.
- **Ask the lifecycle questions first**: environments, pipeline, evaluation, who promotes. They
  separate routes that look identical on features.
- **Treat a missing row as unknown.** Check the product documentation rather than reading support
  into silence.
- **Name one system of record per artifact.** Two repositories describing one agent is a bug.
- **Read status labels as constraints.** A preview CLI decides what you can promise in production.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A declarative agent cannot be promoted through staging | Built in Agent Builder, which has no environments | Rebuild on a source-controlled route before it has users |
| Evaluations stopped working after a rebuild | Moved to a custom engine agent, which `wiqd agent eval` does not cover | Build your own harness ({{topic:evalharness}}) |
| CI provisions fine, then evaluation fails to authenticate | Trusted-pipeline auth covers provision, publish and share only | Give the evaluation step its own credential |
| Two teams argue about a "plugin" | One means the package, the other an MCP or API action | Name the component, not the word |
| A combination was assumed to be supported | Inferred from the matrix's silence | Check the current docs; the matrix says it is not exhaustive |
| Nobody can say where the agent's instructions live | Two tools each produced an artifact | Record one system of record per artifact |

## Key terms

**Plugin (package sense)** — in the tool guide, the Microsoft 365 app package that composes agents,
skills, connectors and MCP-based capabilities. Elsewhere, an MCP or API action alone.

**Work IQ Dev Tools (`wiqd`)** — a preview command-line and VS Code workflow for the declarative-agent
lifecycle, with environments, validation, evaluation and CI support.

**System of record** — the one tool and repository whose artifact is authoritative for a component.
