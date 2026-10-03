## TL;DR

Skills are a GitHub Copilot harness feature, so an agent on the **standard harness** has no Skills area, and the
harness is fixed when the agent is created. Reuse there comes from other parts. **Component collections** share
topics, tools, knowledge, flows and child agents between agents in an environment. **Connected agents** let one
agent hand work to another, which can be reused by several. **Child agents** split one agent's job but are not
meant for reuse. Pick the pattern that fits the harness you are on. The usual mistake is forcing a skill-shaped
design onto an agent that cannot hold one.

## Why it matters

Not every agent in a company is on the GitHub Copilot harness, and not every one should be. A help desk that
must ask the same three questions in the same order every time is a standard-harness design, because only
topics guarantee a path ({{topic:chooseharness}}). Those agents still need to share behaviour, and the reasons are
the same: one copy of a procedure, one owner, no drift between agents that are meant to agree.

Rebuilding an agent on another harness to gain skills is a project, not a setting: new agent, new tools, new
connections, new tests. Knowing the reuse options that exist without skills is usually the cheaper answer.

## How it works

### Component collections: shared parts

<!-- volatile verified=2026-10 -->
A **component collection** is a named set of agent components that several agents can use. Microsoft's page
for it is a standard-harness page, and the components it lists are topics, knowledge, tools, child agents,
MCP servers, connectors, flows and entities. You create one from an agent's **Settings** > **Component
collections**, or at environment level from the side bar.
<!-- /volatile -->

The important detail is how sharing works. When you add components from an agent to a collection, they are
**moved** into the collection and the agent **references** them there. Other agents connected to the collection
use the same components, and their authors cannot change them; only the collection's creator, or someone with
the system customizer or administrator role, can edit it. Within one environment, that is one copy shared, not
copies that drift.

Two refinements matter in practice:

- **A primary agent** restricts a collection to one agent, for when the point is modularity rather than sharing.
- **Across environments, a collection travels as a solution.** Export makes it a managed solution, imported into
  the target environment ({{topic:solutions}}). The source environment stays the place to change it.

One trap is on the page itself: adding *uploaded files* used as knowledge to a collection **removes them from the
agent they came from**.

### Connected agents: delegate the whole job

A **connected agent** is a separate agent that another agent hands work to ({{topic:connected}}). Microsoft's
guidance points to connected agents, rather than child agents, when an agent should be reusable by more than
one other agent, when different teams own the parts, or when parts need their own settings, model or release
cycle.

The cost is the same as any handoff: an extra orchestration hop of latency, context that has to be carried
across deliberately, and more to test and govern. Citations might not survive the trip back to the calling agent.
And one structural limit: an agent that has connected agents cannot itself be connected to a second main agent.

<!-- unknown since=2026-10 -->
Whether a standard-harness agent can connect to an agent on the GitHub Copilot harness, which would let the
skill live on one and the topics on the other, is not stated on Microsoft's page and has not been tested.
<!-- /unknown -->

### Child agents: split, not share

A **child agent** groups instructions, tools and knowledge inside one parent. Microsoft lists *you don't need to
reuse the agent across multiple agents* among the reasons to choose one. A child agent is how one agent stays
organised, not how two agents share. Put it in a component collection if it has to travel.

### Choosing

| You want to share | Pattern | What it costs |
|---|---|---|
| A tool, topic or flow | **Component collection** | Only collection owners can change it |
| A whole capability, with its own settings or owner | **Connected agent** | A hop of latency and a handoff to design |
| Structure inside one large agent | **Child agent** | Nothing reusable |
| A written procedure | A prompt, a flow, or a connected agent ({{topic:prompts}}) | Not a skill file, so not portable |

The last row is the honest gap. A skill is a portable Markdown procedure. On the standard harness, the nearest
equivalents are a prompt, which the standard harness can draw from a prompt library, or a flow. Neither is the
open format, and neither moves to VS Code ({{topic:openformat}}).

## In practice at Technik

The Technik Production Assistant is on the GitHub Copilot harness and holds `qn-write-up` as a skill. Technik
also runs a **shop-floor help desk** on the standard harness, because its *Report a defect* conversation must
collect the serial number, the operation and a photo in that order before anything else happens.

The help desk now wants to offer a QN write-up at the end of that conversation. Three options:

| Option | Result |
|---|---|
| Rebuild the help desk on the GitHub Copilot harness | Loses the scripted intake, which is why it is on the standard harness |
| Copy the write-up procedure into an AI Builder prompt | Works today; two copies of the procedure from then on |
| Connect the help desk to the Production Assistant | One copy; depends on the unknown above |

Technik's choice: test the third. If a standard-harness agent cannot connect to a GitHub Copilot harness agent,
fall back to the second, generate the prompt's text from the skill's `SKILL.md` in the repository, and record
the duplication where the next maintainer will see it.

The help desk's own *Report a defect* topic and its `Find quality notifications` tool go into a component
collection, so the plant's second help desk uses the same intake rather than a lookalike.

> [!TIP]
> When you create an agent, write down why you chose its harness. "It needs a fixed intake" takes ten seconds
> to record. Reconstructing it in six months, when someone asks why this agent cannot have skills, takes an
> afternoon.

## Design guidance

- **Choose the pattern by the harness you are on**, not by the one you wish you were on.
- **Share parts through a collection; delegate whole jobs to a connected agent.**
- **Use child agents to organise, not to reuse.**
- **Keep one source for any duplicated procedure**, and generate the copy from it.
- **Design the handoff explicitly** and test multi-turn conversations across it.
- **Record why each agent is on its harness.**

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| No Skills area on the agent | It is on the standard harness | Use a collection, a connected agent or a prompt |
| "We'll just switch harness" | The harness is fixed at creation | Plan a rebuild, or delegate instead |
| A file used as knowledge vanished from an agent | It was added to a collection, which moves it | Move it back, or keep files out of collections |
| Another author cannot edit a shared topic | Collection components are editable only by their owners | Ask the owner; that is the point |
| The help desk and the assistant word a QN differently | The procedure was copied, then one copy was edited | One source; regenerate the copy from it |
| A constraint from earlier in the chat is lost after a handoff | Context did not cross the boundary | Carry it explicitly; test multi-turn |

## Key terms

**Component collection**: a set of agent components shared by reference among agents in an environment.

**Primary agent**: the one agent a collection is restricted to, when it is not meant to be shared.

**Connected agent**: a standalone agent another agent hands work to, reusable by several.

**Child agent**: a specialised part inside one agent, not intended for reuse.
