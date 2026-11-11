## What this module is for

Up to here you have configured agents and built the pieces around them: an editor agent, a context
budget, skills, an MCP server. This module is about the agent itself as code. It covers the four
routes to a Microsoft 365 agent, the framework you write an agent in, the workflows that put steps
in a fixed order, and the service that runs the result.

One idea runs through all eight lessons: **what you configure versus what you own.** Every route
either runs your configuration on Microsoft's engine or makes you supply the engine. Supplying it is
not a promotion. Each thing you take ownership of is a thing the platform used to provide, and the
lessons keep a list: retrieval over Microsoft 365 content, a channel, evaluation, safety filters, a
runtime, an identity.

So the choice is made **per component, by its hardest requirement**, and a working system spans
several routes. Technik's does. The Production Assistant stays in Copilot Studio, its Teamcenter
server is code, and the capstone agent is Agent Framework on a Foundry hosted agent. The second half
of the module shows the trade running the other way too. Having taken the engine, you hand the
runtime back to Foundry, and in the last lesson you keep a configured platform and bring it one
model of your own.

Expect the documentation to be uneven. One page still calls Agent Framework "formerly Semantic
Kernel". Two of the workflow pages are indexes, with one line per capability. Where a lesson could
not source a claim, it says so in a *Not yet verified* block and does not guess.

## Before you start

From Intermediate, {{topic:stack}} is the map this module fills in, and {{topic:chooseharness}} and
{{topic:agentbuilder}} are the two low-code routes it compares against. {{topic:model}} and
{{topic:prompts}} matter for the last lesson, and {{topic:hitl}} for the workflow one.

From this level, {{topic:harnessvssdk}} asked where the loop lives, and this module is the long
answer. {{topic:loop}} showed the capstone's tool loop and its refusal guard, which three lessons
here lean on. {{module:building-mcp-servers}} supplies the server every route reuses, and
{{topic:mcpcs}} supplies the warning about tools that change without a release. {{topic:multiagent}}
argued against adding agents, which {{topic:mafworkflows}} assumes. {{topic:agentid}} introduced the
identity a hosted agent is given.

Nothing here needs to be run. The capstone repository is public and tested offline only
({{module:capstone-build}}).

Allow about two and a half hours.

## What you will be able to do

By the end of this module you should be able to:

- place each component of a system on a route by its hardest requirement, and name its system of
  record;
- say what a declarative agent's configuration cannot promise, and move those requirements to code
  or to a flow;
- scope a declarative agent's knowledge and pin its plugin's tools, knowing both fail open;
- choose between the three routes that bring a Foundry agent to Teams, starting from which identity
  calls the tools;
- describe an Agent Framework agent as a client, instructions, tools and middleware, and explain why
  the client should be a parameter;
- apply the framework's own order of preference: a function, then an agent, then a workflow;
- choose between the functional and graph workflow APIs, and design the pause for a person before
  anything else;
- choose between a prompt agent, a hosted agent and the Responses API, and plan a release around an
  endpoint that serves one version at a time;
- connect a Foundry model to a Copilot Studio prompt, and list the limits that decide whether you
  can.

## The thread through this module

The first half goes outward from configuration. {{topic:lowvspro}} replaces the ladder with a
filter: each component goes where its hardest requirement fits. {{topic:declarative}} takes the
route that owns least, and finds the line configuration cannot cross. {{topic:plugins}} gives that
agent actions, and shows that both scoping and tool discovery are permissive unless you say
otherwise. {{topic:customengine}} crosses the line. The Agents SDK turns out to be plumbing, and the
engine is still missing.

The second half supplies the engine and then gives parts of it back. {{topic:maf}} is the engine: a
few lines to start, and a notice that safety is now yours. {{topic:mafworkflows}} adds the paths you
refuse to leave to a model. {{topic:foundryagents}} returns the runtime to a platform, and finds one
thing an immutable version does not pin. {{topic:byom}} closes the module with the smallest move of
all, one owned model inside a configured product.

## Self-check

<details>
<summary>1. A manager wants the revision summaries in the document approval flow to come from a model Technik has deployed in Foundry. A colleague proposes rebuilding the Production Assistant in Agent Framework to get it. What do you say?</summary>

That the requirement belongs to one component, and the route is chosen per component by its hardest
requirement. The summaries come from one prompt in the submission flow. Nothing on the assistant's
own list exceeds Copilot Studio, so the assistant does not move, and a rebuild would give up Teams,
skills and knowledge to gain a model ({{topic:lowvspro}}).

The model can come to the prompt. A Foundry deployment connects to a prompt, and "Each time this
prompt runs, it uses the selected model". Check the limits before promising it: the endpoint must be
a chat completions endpoint, "The GPT-5 family and later models ... aren't currently supported", and
the page is written for the standard harness. The connection is a Power Platform connector holding
an API key, so data policy and secret handling apply. And it is still a model change, so the
prompt's test cases run again ({{topic:byom}}).
</details>

<details>
<summary>2. A declarative agent for manufacturing engineers is given OneDrive and SharePoint knowledge and the capstone's MCP server as a plugin. In review you find no `ItemsByUrl` and no tool list in the manifest. Why does that matter?</summary>

Because both defaults are permissive. Without `ItemsByUrl` the agent reaches "all OneDrive and
SharePoint content in your Microsoft 365 organization that the signed-in user can access", which for
an engineer includes the drafting team's site and its unreleased revisions. Scope is something you
opt into, and Teams messages, connectors and web search behave the same way.

The missing tool list means the plugin resolves its tools "dynamically at runtime by default",
straight from the server. A change to the server then reaches the agent with no release on the
agent's side, the propagation {{topic:mcpcs}} found Microsoft calling a rug pull. Pin the three
tools in the manifest. Do not count the documented validation of "new or changed tools" as a review,
because the page never says what it checks ({{topic:plugins}}, {{topic:declarative}}).
</details>

<details>
<summary>3. Technik wants the capstone agent in Teams by Friday, and the fastest route is to publish it from Foundry. What do you check first, and what do you check second?</summary>

Identity first. The agent reaches its MCP server as its own Entra identity, and the server admits
only callers holding `Teamcenter.Read`. The publish route "Automatically provisions Azure Bot
Service and Entra ID". Whether that identity sits in front of the agent's, or in the call path to
the tools, is not documented, so it is a test in a non-production tenant before it is a plan. The
hosted agents page adds a second case: reached through Teams with a user token present, an agent can
act on behalf of the user ({{topic:customengine}}, {{topic:foundryagents}}).

Streaming second. Teams orders messages by server timestamp, and the rule is one streaming sequence
per turn. The capstone's refusal guard replaces an ungrounded answer, and a refusal sent as a second
message can render before the answer it replaces. The guard's output has to travel inside the one
stream. The hosted server always streams, so this is the normal path and not an edge case
({{topic:stageship}}).
</details>

<details>
<summary>4. After an ECN is released, Technik wants open work orders on superseded revisions found and their planners told, with a manufacturing engineer approving each notice. Agent, workflow or function?</summary>

All three, in the framework's order of preference. "If you can write a function to handle the task,
do that instead of using an AI agent." Reading the ECN's affected items and finding the operations
still on the old revisions are queries, so they are functions. After `ECN70000051` they return work
orders `100004510` and `100004513` with no model involved. Drafting a notice a planner can act on is
the one step that suits a model.

The whole is a workflow, because the process "has well-defined steps" and the order has to be
enforced. It is a fixed graph with a fan-out and one pause, which is what the graph API is for, and
the functional API is experimental. Design the pause first. An approval can outlast the process that
asked for it, so the run needs a checkpoint, and these pages do not say what a resumed run repeats.
Then ask whether an agent flow with an approval would do the same job with less to own
({{topic:maf}}, {{topic:mafworkflows}}).
</details>

<details>
<summary>5. For the next release of the capstone agent, a colleague plans to send a tenth of the traffic to the new version and watch it for a day. Why will that not work, and what replaces it?</summary>

"An agent endpoint serves one version at a time and routes 100% of its traffic to that version.
Traffic splitting between versions isn't supported." There is no canary on a hosted agent. A version
is an immutable snapshot of image, resources, environment variables and protocols, and deploying one
moves everyone to it.

So the judgement runs before the deployment. The capstone's release gates on its evaluation run,
then deploys, and keeps the previous version available to redeploy. One more thing belongs in the
release plan. The snapshot does not include tools. They come from a toolbox with versions of its
own, and promoting a toolbox version may change what a deployed agent can call. Whether an agent
version can pin a toolbox version is not documented, so treat a toolbox promotion as a release of
every agent that uses it ({{topic:foundryagents}}, {{topic:cicd}}).
</details>
