## TL;DR

You need one language, well enough to do four specific jobs: call a model's API, write an MCP
server, script an evaluation, and use an agent SDK. That is a much smaller target than "learn
Python" — it is async calls, types, packaging, tests and JSON, and almost no algorithms. **Pick one
language for the team and stay with it.** The reason is not that one is better; it is that every
sample, every dependency pin, every reviewer and every debugging session is cheaper when there is
one answer. This course and its capstone are Python throughout, and where .NET exists it is named
rather than shown.

## Why it matters

The question *"do I need to be a programmer for this?"* has a precise answer at this level, and it
is neither yes nor no. Nothing in the rest of this level asks you to design an algorithm. It asks
you to glue well-documented services together carefully, handle their failures honestly, and prove
the result works. That is a narrow and learnable slice of a language.

The more consequential half is the choice itself. A team that writes some agents in Python and some
in C# does not have two skill sets; it has two dependency graphs, two sets of version pins, two CI
configurations and two review populations, for the same number of agents. The cost shows up in the
unglamorous places — the day an SDK's minor release moves a class and only half the team has seen
it before.

## How it works

### What "enough" actually means

| You need | Because |
|---|---|
| **Async calls** (`async`/`await`) | Model and agent SDK calls are asynchronous; the samples are written that way |
| **Types and data shapes** | Tool arguments and results are structured; a tool contract is a schema ({{topic:structured}}) |
| **Packaging and environments** | One project, pinned dependencies, a lock file ({{topic:localenv}}) |
| **Tests** | The capstone's offline suites are how each stage is proved ({{topic:evalharness}}) |
| **JSON and dictionaries** | Everything crossing a protocol boundary is JSON |
| **Decorators or attributes** | How a function is registered as a tool in most SDKs ({{topic:buildmcp}}) |
| **Environment variables and files** | Configuration and credentials ({{topic:localenv}}) |
| **Errors as values** | A tool's error message is read by a model, so it is part of the interface ({{topic:tooldesc}}) |

What is *not* on the list is as useful: no data structures beyond lists and dictionaries, no
concurrency beyond awaiting calls, no performance work, and no machine learning. If you can write a
tested script that calls an HTTP service and handles its failures, you can do this level.

### The SDK landscape, in one paragraph each

**Agent Framework** is the SDK this level builds on. Its own getting-started documentation is
pivoted by language and currently covers **C#, Python and Go** — so "Python or C#" understates the
choice slightly.

<!-- volatile verified=2026-11 -->
The install commands differ in a way that tells you something. Python is
`pip install agent-framework-foundry azure-identity`, where `agent-framework-foundry` brings in
`agent-framework-core` plus the Foundry integration, and a broader `agent-framework` metapackage
pulls in many optional integrations as well. .NET is
`dotnet add package Microsoft.Agents.AI.Foundry --prerelease` — note the flag. The documentation
states a minimum version only for Go (1.26 or later); it gives none for Python or .NET.

Authentication differs too: the Python sample signs in with the Azure CLI credential after
`az login`, while the .NET sample uses the default credential chain and carries an explicit warning
that this is convenient for development and needs thought in production.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
Whether the Python and .NET implementations are at feature parity is **not stated** anywhere in
this topic's curated documentation. Do not assume a sample in one language has an equivalent in the
other; check before committing a team to the language with fewer examples in the area you need.
<!-- /unknown -->

### Why Python here

The choice for this course was made on the ground rather than on principle. The capstone needs an
MCP server, a Snowflake driver, an agent framework and an evaluation runner to coexist and be
pinned together, and Python is where those four currently meet with the least friction. The
decision then propagates: lessons show Python, the conventions assume it, and a reader gets one
consistent example rather than two half-examples.

<!-- volatile verified=2026-11 -->
A minimal agent is genuinely about this long — a client pointed at a model deployment, instructions,
and a call:

```python
import asyncio
import os
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

async def main() -> None:
    agent = Agent(
        client=FoundryChatClient(
            project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
            model=os.environ["FOUNDRY_MODEL"],
            credential=AzureCliCredential(),
        ),
        instructions="You are a friendly assistant. Keep your answers brief.",
    )
    print(await agent.run("What is the largest city of France?"))

asyncio.run(main())
```

Adapted from the Agent Framework quickstart, with the endpoint and model read from the environment
rather than hardcoded, per this level's code conventions. The framework does **not** load a `.env`
file by itself ({{topic:localenv}}).
<!-- /volatile -->

If your organisation is a .NET shop, the C# path exists and the C# guide in *Go deeper* is the
reference for the language itself. What you lose by taking it is this course's worked examples;
what you keep is your team's existing review capacity, which may well be the better trade.

## In practice at Technik

Technik's capstone is Python end to end, and the most instructive thing about it is not the code
but a dependency constraint ({{topic:localenv}}): Agent Framework requires an MCP SDK older than the
one the server uses, so the repository holds **two** projects — the server on the current MCP SDK,
the agent on the older one. They talk over the protocol, so the mismatch is invisible at runtime.

Two further details from building it are worth carrying into your own choice. The broad
`agent-framework` metapackage would not resolve without allowing pre-releases, so the capstone pins
`agent-framework-core` and `agent-framework-foundry` individually — exactly the situation the
documentation hints at when it distinguishes the metapackage from the targeted package. And the
current MCP SDK moved its server class between major versions, with the old import path raising an
error that points at the migration guide. Neither is a Python problem. Both are what *young SDK*
means, and they are the strongest practical argument for one language, exact pins and a committed
lock file.

## Design guidance

- **Choose once, for the team, and write the choice down** with its reason.
- **Learn the four jobs, not the language's whole surface.** Async, types, packaging, tests.
- **Pin exact versions and commit the lock file.** Preview SDKs move.
- **Prefer the targeted package over the broad metapackage** when the broad one drags in
  everything.
- **Let processes that talk over a protocol differ in their dependencies.** It is a feature, not
  debt.
- **Read errors as part of your interface.** A model reads your tool's failure text
  ({{topic:tooldesc}}).
- **Check parity before assuming it**, in whichever language has fewer samples for your area.
- **Keep credentials out of code in every language.** The mechanism differs; the rule does not.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A broad SDK metapackage will not resolve | It pulls optional integrations, some pre-release | Install the targeted package and pin it |
| Two SDKs cannot share one environment | A shared transitive pin across a major version | Two projects, talking over the protocol ({{topic:localenv}}) |
| An import that matches the docs raises an error | The SDK moved the class in a major version | Read the error; it usually names the migration guide. Pin exactly |
| Configuration is empty at runtime | The framework does not load `.env` automatically | Load it explicitly, or set the variables in the shell |
| A sample for your language does not exist | Parity between languages is undocumented | Check before committing; prototype the risky part first |
| The team maintains two stacks for one agent estate | No language decision was ever made | Make it now; migrating one agent is cheaper than carrying two toolchains |
| Credentials work locally and fail when deployed | A development credential chain was used in production | Use a deployment identity ({{topic:agentid}}, {{topic:stageship}}) |

## Key terms

**Agent Framework** — the SDK this level's pro-code agents are built on
({{topic:maf}}).

**MCP SDK** — the library for writing and calling Model Context Protocol servers
({{topic:buildmcp}}).

**Metapackage** — a package whose purpose is to pull in others; convenient until it pulls in
something unresolvable.

**Pre-release** — a package version not considered stable, which some SDKs still require.

**Credential chain** — the ordered set of ways an SDK tries to authenticate; convenient in
development, deliberate in production.

**Parity** — whether two language implementations of one SDK offer the same features. Not
documented here; check it.
