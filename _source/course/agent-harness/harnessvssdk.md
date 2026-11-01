## TL;DR

There are three answers to *where does the loop live*. A **managed harness** owns the loop and you
configure it. An **SDK** gives you the loop as code you compile, test and host. A **platform service**
runs your code as a managed agent, with identity, scaling, session state and tracing supplied. They
are not rungs on a quality ladder; they are different things to own. Microsoft Agent Framework reached
1.0 in April 2026, "bringing the convergence of AutoGen and Semantic Kernel into a single, supported
platform", and now ships both a packaged harness and a hosted deployment target — so you can take the
SDK and still hand the runtime away. Choose by what you must control, and give away the rest.

## Why it matters

The expensive mistake is reaching for an SDK to get something configuration already gave you. Copilot
Studio's GitHub Copilot harness already plans, retries, calls MCP servers and runs in a governed
sandbox; rebuilding that in code to gain one tool you could have added is weeks of work and a runtime
to operate forever ({{topic:lowvspro}}).

The opposite mistake is quieter. Some requirements are simply not expressible as configuration — a
guard that must run on every answer, a release that must fail on an evaluation regression, a server
over data the platform cannot reach. Those are code, and discovering it three months into a low-code
build is worse than starting there.

And the choice is rarely all-or-nothing. The same agent can be SDK code on a managed runtime, or a
managed harness calling a server you wrote. The useful question is which layer you need to own.

## How it works

### The SDK, and the harness inside it

Agent Framework is "our open-source SDK and runtime for building AI agents and multi-agent workflows",
with "the same concepts and APIs across .NET and Python" ({{topic:maf}}). Since BUILD 2026 it includes
three things worth knowing about by name.

**Agent Harness** is a packaged loop: "the layer where model reasoning meets real execution: shell and
filesystem access, human-in-the-loop approval flows, and context management". It brings automatic
context compaction, todo and planning providers, file memory, skills, web search and tool-approval
middleware, with harness instructions merged ahead of your own ({{topic:loop}}). You reach for it when
you want the SDK's control over a loop you did not want to write.

**Hosted Agents** is the platform answer: a container deployed onto Foundry-managed infrastructure
"with built-in identity, automatic scaling, managed session state, observability, and versioning". It
scales to zero and resumes with the filesystem intact, gives each session a VM-isolated sandbox, and
flows the SDK's OpenTelemetry traces into Application Insights. The blog's own framing is the
recommendation: it "is the easiest way to give that agent a production home"
({{topic:foundryagents}}, {{topic:tracing}}).

**CodeAct** is a different shape of loop. Instead of one tool call per pass, the model writes "a single
short Python program that calls your tools", run once in a sandbox — because "Many agents aren't
bottlenecked by model quality, they're bottlenecked by orchestration overhead". On a benchmark needing
dozens of tool calls it cut a 27.81-second, 6,890-token run to 13.23 seconds and 2,489 tokens. It
ships in an **alpha** package and is Python-only, which is the whole story about whether it can carry
production today.

Two features graduated to 1.0 alongside them: the GitHub Copilot SDK integration, which brings that
agent's shell, file and MCP capabilities into Agent Framework code, and Handoff orchestration, where
"Topology and guardrails stay with the developer; routing decisions stay with the agents"
({{topic:multiagent}}).

### The Microsoft 365 question is a different question

Microsoft's own tool comparison for Microsoft 365 Copilot answers *how does this reach a user* rather
than *where does the loop live*, and names neither Agent Framework nor Foundry. Its routes run from
Agent Builder (no-code) through Copilot Studio — "Choose Copilot Studio when you need its managed
workflows, connectors, and application lifecycle capabilities" — and the Microsoft 365 Agents Toolkit
for manifest and package control, to the Microsoft 365 Agents SDK for a **custom engine agent**, which
is where you "Build and host custom orchestration, models, integrations, and multi-channel agent
experiences" ({{topic:declarative}}, {{topic:customengine}}).

Read the status labels as part of the comparison: Work IQ Dev Tools is in preview with an alpha plugin
command tree and no publish command, and GitHub Copilot appears as "Development assistance, not a
Microsoft 365 packaging route."

So a complete decision has two axes. Runtime ownership picks harness, SDK or platform. Reach picks the
channel and the packaging route — and a custom engine agent is how an SDK-built agent gets into Teams
and Microsoft 365 Copilot at all.

## In practice at Technik

The Production Assistant exists twice, and the second build is justified by exactly three things that
configuration could not give it.

Intermediate's version runs on Copilot Studio's GitHub Copilot harness. Nothing is hosted, the
capability ships as a skill, Teams is the channel, and the bill is Copilot Credits. For the seven
capability areas as originally scoped, that is the right answer and still is.

The capstone rebuilds it on Agent Framework because it needed an MCP server over Teamcenter views
connecting as a specific read-only role, a refusal guard that runs on every answer including streamed
ones, and an evaluation gate in CI that blocks a release on a regression against a baseline. Each is
code, not configuration ({{topic:stageagent}}, {{topic:evalharness}}).

Then it gives the runtime straight back. Stage 5 deploys the agent as a Foundry hosted agent reaching
the server through a toolbox, so the identity, the scaling and the tracing are Foundry's problem rather
than Technik's ({{topic:stageship}}, {{topic:agentid}}). What the rebuild gave up is the Teams channel
and the low-code publishing path — which is why `customengine` is a topic of its own and not a
footnote here.

One detail is worth carrying forward as a general lesson. Choosing the SDK dragged a constraint with
it: Agent Framework requires an MCP SDK below version 2, so the capstone is two dependency projects
rather than one ({{topic:localenv}}). Owning a loop means owning its dependency graph.

## Design guidance

- **Name the requirement that configuration cannot meet**, and if you cannot, stay in the managed
  harness.
- **Give away the runtime even when you own the loop.** Identity, scaling and tracing are the cheapest
  things to buy.
- **Treat preview and alpha labels as answers, not caveats.** An alpha package decides the question
  for production.
- **Count the operating cost, not the build cost.** Credits versus tokens versus compute is part of
  the comparison, and so is who is on call ({{topic:costs}}).
- **Decide reach separately from runtime.** A channel requirement can override a runtime preference
  outright.
- **One language per team**, because an SDK's loop is code someone else has to read
  ({{topic:language}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A pro-code rebuild delivers what the low-code version already did | No requirement that needed code | Name the three things it unlocks, or stop |
| An agent works and nobody can tell what it did | An SDK loop deployed without the platform's observability | Host it where tracing is built in ({{topic:tracing}}) |
| A capability is demoed and cannot ship | It depends on an alpha or preview package | Check status labels before designing around a feature |
| The agent is finished and reaches no users | Runtime was chosen, reach was not | Pick the packaging route and channel explicitly |
| The SDK choice forced an awkward dependency split | A framework pinned a transitive SDK version | Separate the processes; a protocol boundary lets versions differ |
| Costs appear in three places at once | Credits, model tokens and compute are billed separately | Model the whole bill per agent before committing |
| A multi-agent design went in because the SDK offered it | Patterns adopted for availability rather than need | Use the lowest complexity that meets the requirement ({{topic:planning}}) |

## Key terms

**Managed harness** — a runtime someone else owns, configured rather than coded; Copilot Studio's
harnesses are the example you have used.

**SDK** — a library for building the loop as code you compile, test and host; Agent Framework here.

**Platform service** — a managed runtime for your agent code, supplying identity, scaling, session
state and observability.

**Hosted agent** — an agent container deployed onto Foundry-managed infrastructure.

**Custom engine agent** — an agent with your own orchestration and models, brought into Teams and
Microsoft 365 Copilot through the Microsoft 365 Agents SDK.
