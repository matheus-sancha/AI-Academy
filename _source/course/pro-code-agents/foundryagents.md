## TL;DR

Foundry Agent Service is where you hand the runtime back. It is "a managed platform for building,
deploying, and scaling AI agents", and it offers three agent types whose difference is "how much you
build versus how much Foundry manages". A **hosted agent** is the one that takes your code: you ship
a container, and the platform "owns the endpoint, identity, scaling, and session state around it".
You still own everything inside the sandbox, and one thing outside it that looks pinned and is not.

## Why it matters

{{topic:maf}} left you with an agent that runs on a laptop. Between that and production sits the
list the hosted agents page opens with: "containerization, web server setup, security, memory
persistence, scaling, instrumentation, and version rollbacks". {{topic:harnessvssdk}} called a
platform service the third answer to where the loop lives. This lesson is what that answer contains.

## How it works

### Three types and a fourth path

| Path | What you supply | What Foundry runs |
|---|---|---|
| Prompt agent | Instructions, a model and tools | Everything: "no code or infrastructure to manage" |
| Voice-based prompt agent | The same, plus audio settings | The voice orchestration too (parts are in preview) |
| Hosted agent | "your own code and framework" as a container | "a managed endpoint, scaling, and identity" |
| Responses API, called from your code | The whole agent, in your application | Models and tools only |

The fourth row is not an agent type. The overview calls it an *ephemeral agent*: the definition
"lives in your application code instead of as a persisted resource in Foundry", so there is "no
agent to create, update, or delete".

The overview's reason for choosing a hosted agent is narrower than "pro-code". Hosted agents are
best for "Agents that call into your own custom code; secondarily, custom orchestration logic". If
nothing of yours has to run, a prompt agent is the documented starting point.

### What a hosted agent is

"You package your agent as a container image and push it to Azure Container Registry. When you
deploy, Agent Service pulls the image, assigns a dedicated Microsoft Entra ID (agent identity), and
exposes a dedicated endpoint for the agent." Each session then runs in its own VM-isolated sandbox.
Python and C# are supported.

The container speaks one or more protocols. **Responses** is the default advice, "Not sure? Start
with Responses", because the platform then manages conversation history, streaming events and the
session lifecycle. **Invocations** takes arbitrary JSON and leaves sessions to you. When a Responses
agent is published to Teams, "the platform automatically bridges Responses to the Activity protocol
for channel delivery".

### Two identities

| Identity | Purpose |
|---|---|
| Agent identity, per agent, "Created automatically at deploy time" | "The identity the agent container authenticates with at runtime" |
| Project managed identity | Infrastructure operations. "Not the agent's runtime identity" |

The agent identity reaches model inference and session storage by default. For anything else you
"assign RBAC roles manually to the agent's Microsoft Entra ID" ({{topic:agentid}}). Reached through
Teams, an agent can act on behalf of the user when a user token is present, and as itself otherwise.

<!-- unknown since=2026-11 -->
The two pages do not read the same way on identity. The hosted agents page gives every hosted agent
its own identity at deploy. The overview says published agents "inherit the enterprise identity and
access controls configured for your project", and lists the project's managed identity as an option
for tool connections. The capstone never ran live, so which identity its server actually sees is
unverified ({{topic:stageship}}).
<!-- /unknown -->

### Sessions, conversations and the state store

Three things hold state, and they have different lifetimes. A **session** is compute plus a
filesystem: `$HOME` and uploaded files persist "across turns and across idle periods". A
**conversation** is "a durable record of conversation history" stored in Foundry, which "persists
independently of compute state". The **state store** is a key-value store for your own application
state, and it can hold "framework checkpoints" for Agent Framework ({{topic:mafworkflows}}). With
the Responses protocol, "conversation ID is the primary concept".

<!-- volatile verified=2026-11 -->
The idle timeout is configurable "from 2 through 240 minutes (4 hours), with a 15-minute default",
and a session is deleted "after 30 days of inactivity".
<!-- /volatile -->

### Toolboxes

A toolbox "groups those tools into a single, reusable unit" behind "one managed MCP-compatible
endpoint". It centralises "authentication, governance, and versioning": you "Create a new version,
test it, and promote it to default". Hosted agents take their tools this way "rather than by adding
them directly to the agent definition", and an Agent Framework agent uses `FoundryToolbox` "instead
of a generic MCP client".

### Versions, and what they do not pin

Each deployment creates "an **immutable agent version**", a "snapshot of the container image,
resource allocation, environment variables, and protocol configuration". Then the constraint that
shapes a release: "An agent endpoint serves one version at a time and routes 100% of its traffic to
that version. Traffic splitting between versions isn't supported." There is no canary. Whatever
decides that a version is good has to run before the deployment ({{topic:cicd}}).

The snapshot lists four things, and tools are not among them. A toolbox has versions of its own and
a default that someone can promote.

<!-- unknown since=2026-11 -->
Neither page says whether an agent version can pin a toolbox version. The capstone builds its
toolbox address from the toolbox's name, so it should follow whichever version is the default. If
so, promoting a toolbox version changes what a deployed, immutable agent can call. That is the
propagation {{topic:mcpcs}} warned about, one layer up.
<!-- /unknown -->

### Cost follows sessions

"Hosted agents scale per session, not per replica." The CPU and memory you set "describe a *single
session*", and billing covers every active one, so "oversizing multiplies cost by your concurrency".

## In practice at Technik

The capstone is a hosted agent because of one function. Its refusal guard must run on every answer
({{topic:loop}}), and a prompt agent has no place for code of yours. An ephemeral agent on Technik's
own compute would run the guard too, but it is never deployed, and the identity that holds the
server's `Teamcenter.Read` role is created at deploy.

*From [`azure.yaml`, lines 52–71](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/azure.yaml#L52-L71):*

```yaml
  technik-agent:
    host: azure.ai.agent
    project: agent
    language: docker
    uses:
      - ai-project
      - teamcenter
      - technik-tools
    toolboxes:
      - technik-tools
    kind: hosted
    name: technik-production-assistant
    description: Answers questions about Technik's controlled documents and revisions from Teamcenter.
    protocols:
      - protocol: responses
        version: 2.0.0
    env:
      MICROSOFT_FOUNDRY_MODEL_DEPLOYMENT_NAME: gpt-4.1-mini
      TOOLBOX_NAME: technik-tools
    startupCommand: python hosted.py
```

Read it against the page. One protocol, Responses, so Foundry keeps the conversation and the code
stores nothing. Two environment variables and neither is a secret, which follows the page's rule:
"Don't put secrets in container images or environment variables". The Snowflake key stays in Key
Vault, behind the server. The file goes on to request the smallest sandbox, because each planner's
session gets its own.

The page's third security rule is one the capstone meets by layout. Uploads land in `$HOME`, and you
should not "automatically load code, configuration, or trusted instructions from upload-writable
paths". The image keeps `instructions.md` in `/app`, beside the code.

## Design guidance

- **Start from a prompt agent and justify leaving it.** Name the code that has to run.
- **Gate before you deploy.** With no traffic splitting, the evaluation run is the canary.
- **Treat a toolbox promotion as a release** of every agent that uses it.
- **Size for one session**, then multiply by the concurrency you expect.
- **Grant the agent identity each role by hand**, and record the grant with the deployment.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A new version takes all traffic at once | One version per endpoint, no splitting | Gate on evaluations before deploying; keep the last version ready to redeploy |
| The agent's tools changed with no new agent version | A toolbox version was promoted to default | Review toolbox promotions like deployments |
| The server rejects the agent's calls | The role was never assigned to the agent identity | Assign it after the first deploy ({{topic:stageship}}) |
| The bill grows faster than usage | CPU and memory are per session | Right-size from Application Insights, then retest |

## Key terms

**Hosted agent** — your own agent code in a container, run by Foundry with a managed endpoint,
identity, scaling and session state.

**Agent identity** — the Microsoft Entra identity created for a hosted agent at deploy, which its
container uses at runtime.

**Toolbox** — a versioned set of tools behind one managed MCP endpoint, shared across agents.

**Session** — a hosted agent's compute and persistent filesystem for one user's exchange. Distinct
from the **conversation**, the durable message history Foundry stores.
