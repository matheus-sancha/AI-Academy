## TL;DR

Adding an existing MCP server to a Copilot Studio agent gives it that server's whole tool set at
once, and keeps giving it whatever the server adds later. That is the convenience and the risk in
the same sentence. The work is not the adding — it is the review beforehand and the routing test
afterwards.

## Why it matters

A connector tool is one operation you configured and described yourself. An MCP server can
contribute a dozen tools you did not write, whose descriptions you did not choose, that your agent
will call with your agent's identity, and whose list can change without you touching the agent.

Everything about that is fine when the server is one your organisation has reviewed. None of it is
fine when someone found a server online and enabled it because the demo looked good.

## How it works

<!-- volatile verified=2026-09 -->
In Copilot Studio, an MCP server is added from the agent's **Tools** area as a tool of its own kind:
you give it the server's address and whatever authentication it needs, the server is queried for
what it offers, and its tools appear in the agent. Which harnesses support it, what transports and
authentication methods are accepted, and how individual tools are enabled or disabled all change
between releases — follow the linked documentation for the current steps rather than a remembered
screen.
<!-- /volatile -->

Three properties are stable whatever the screens look like.

**The server must be reachable from the cloud.** A server running on your laptop over standard input
and output is fine for VS Code and useless to Copilot Studio. Remote means an address, a supported
transport and an authentication story.

**Tools arrive as a set.** You are not adding one capability; you are adding the server's catalogue,
and it lands in the same list the orchestrator chooses from.

**Discovery is ongoing.** When the server publishes a new tool, connected agents can pick it up. This
is the feature. It is also the reason the review is not a one-off.

### The review, before you enable anything

Answer these in writing. If you cannot answer one, that is the finding.

1. **Who publishes it?** Certified by Microsoft, published by the system vendor, built internally, or
   none of the above?
2. **What is the full tool list, and what does each tool do?** Read it. Not the summary — the list.
3. **Which of them can change something?** A server described as read-only can expose a write; the
   description is marketing, the tool list is the contract.
4. **What identity does it act with**, and what can that identity reach?
5. **Where does it run, and what does it see?** Everything you send a remote server, it has.
6. **How is it versioned, and how will you learn it changed?**

Then enable **only the tools you need**, if the platform lets you, and re-run the review when the
server updates.

### After you enable it

Adding several tools at once changes the orchestrator's choices for every tool that was already
there. So:

- re-run the routing tests for your existing tools, not just the new ones;
- watch for overlap — if the server offers a revision lookup and you built one, one of them has to go;
- check the activity map on a few real questions to see which tool is actually being chosen.

## In practice at Technik

In the lab you add an MCP server to the Technik Production Assistant alongside the
`Get released revision` tool you built by hand, and the exercise is deliberately a comparison rather
than a build.

Three things are worth noticing when you do it.

**The orchestrator treats them identically.** Your connector tool and the server's tools sit in one
catalogue, and the same description-matching decides between them. Nothing about MCP changes how
routing works.

**The authoring effort is completely different.** Your tool took a view, a query, four input
decisions and three pieces of description. The server took an address. That asymmetry is the argument
for MCP — and the reason to be careful about what you point at.

**The security questions are unchanged.** The server reaches a system with some identity, and that
identity bounds what any prompt injection can achieve. A5 builds Technik's own server and connects
it to `ACADEMY_AGENT_<you>` for exactly this reason.

> [!IMPORTANT]
> A hostile or careless MCP server sits inside your agent's trust boundary: it sees what the agent
> sends it, and its tool descriptions influence what the orchestrator decides to do. A tool
> description is text the model reads — a server can write descriptions that steer routing. Enable
> servers you have reviewed, from publishers you trust, and nothing else. A13 treats this properly as
> a supply-chain question.

## Design guidance

- **Prefer certified or internally approved servers.** Treat an unreviewed one as an unreviewed
  dependency.
- **Read the tool list before enabling**, and enable the minimum.
- **Write down the review.** Publisher, tools, identity, where it runs, how you will hear about
  changes.
- **Re-test routing after adding a server**, across your existing tools too.
- **Avoid duplicate capability.** Two tools that do the same thing make the orchestrator worse at
  both.
- **Know how you will find out it changed.** If the answer is "we would not", pin a version or do not
  use it.
- **Keep the identity least-privilege.** MCP does not change who the agent is when it reaches your
  data.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The server cannot be added | It is local-only, or uses a transport the client does not accept | Deploy remotely with a supported transport |
| Authentication fails | The server expects a method the client cannot supply | Check what the client supports before choosing a server |
| New tools appeared unannounced | Tool discovery did its job | Review on update; pin versions; enable selectively |
| The agent stopped calling your own tool | An MCP tool's description matches better | Remove the overlap, or sharpen your description |
| Routing got noticeably worse | The catalogue grew by several tools at once | Enable fewer tools; consider a connected agent to hold them (A6) |
| A server returns far more data than expected | No control over its result size | Check result sizes in testing; prefer servers with bounded output |
| Nobody can say what the server is allowed to do | No review was done | Do it now, before anyone shares the agent |

## Key terms

**Tool discovery** — the client asking the server what it offers, so new tools appear without
re-authoring the agent.

**Remote MCP server** — one reachable over HTTP, which is what a cloud client needs.

**Certified connector or server** — one Microsoft has validated for use in the platform.

**Trust boundary** — the line inside which components are assumed not to be hostile. An enabled MCP
server is inside yours.

**Supply-chain risk** — risk inherited from a dependency you did not write (A13).
