## TL;DR

A custom engine agent is how an agent with its own orchestration and models reaches Teams and
Microsoft 365 Copilot. The Microsoft 365 Agents SDK is not that engine. It "isn't an AI model, an
orchestration engine, or a no-code builder". The docs call it "the plumbing layer between a user
sending a message ... and whatever logic you built to respond". You bring the engine, the SDK carries
messages, state and channels, and everything a declarative agent inherited is now yours to provide.

## Why it matters

The capstone ends as a Foundry hosted agent that no user can talk to, which {{topic:harnessvssdk}}
named as the price of the rebuild. Paying it back is a decision of its own, with three documented
routes that differ in what you host, which identity answers, and what you have to rebuild. Pick by
habit and you can quietly undo the identity design the capstone was built around.

## How it works

### What "custom engine" buys, and costs

Custom engine agents "provide full control over orchestration, AI models, and data integrations",
plus proactive automation: they can "Programmatically trigger workflows and take actions". The page
also counts Copilot Studio as a low-code way to build one, so the line {{topic:stack}} drew is about
who owns the engine, not about writing code. Custom engine agents need app manifest version 1.21 or
later.

The bill arrives as things you no longer get for free. Copilot Studio agents "have native access to
Microsoft 365 and Copilot connector content". Pro-code agents "can access the same data via Microsoft
Graph APIs and use the Retrieval API", which means you build that retrieval yourself. You still
inherit storage, though: prompts and responses in Copilot Chat and Teams are kept under Microsoft 365's
terms, and administrators reach them with Content Search or Purview ({{topic:purview}}).

### The SDK is plumbing

The SDK overview names three problems it solves. Channels: "You write your agent logic once, and the
SDK translates incoming and outgoing messages to and from the format each channel expects." Vendor
lock-in: it "is AI-agnostic by design". And state: it tracks a **turn**, "a single unit of work in a
conversation", across messages without a persistence layer of your own.

Mechanically, every incoming message is normalised into an `Activity`, routed to the handler you
wrote for that activity type, and answered through the same channel. The SDK "doesn't decide what an
agent says". Your orchestration does. That is the seam where Agent Framework plugs in
({{topic:maf}}).

<!-- volatile verified=2026-11 -->
The overview lists C# on .NET 8.0, JavaScript on Node.js 18 and later, and "Python using version 3.9
to 3.11".
<!-- /volatile -->

### Three ways in

For an agent that already lives in Foundry, the custom engine page documents two routes, and the SDK
is the third.

| Route | What you build | Documented as ideal for |
|---|---|---|
| Publish from Foundry | Nothing: it "Automatically provisions Azure Bot Service and Entra ID and packages your agent" | "Rapid deployment and testing with minimal code changes" |
| Agents Toolkit proxy app | A proxy in front of the Foundry agent | "Scenarios requiring custom logic, SSO, or managed infrastructure" |
| Agents SDK | Your own process, any orchestration behind it | "full-stack, multi-channel agents", with "10+ channels" |

Both Foundry routes reach Microsoft 365 "through a bot or proxy layer". A fourth option, the Teams
SDK, has a built-in planner and suits agents for Teams channels and meetings. For store publishing,
only Teams SDK, Agents SDK or Foundry agents can go to the Commercial Store through the Agents Toolkit.

### Streaming has rules here

Teams and Copilot order messages by server timestamps and activity IDs, so a turn that mixes streams
and plain messages "can appear out of sequence". The rules are strict: "Use a single streaming
sequence per user turn", finalise it with `endStream()` before sending anything else, attach media
with `setAttachments()` inside the stream, serialise outgoing messages, and never send updates after
`endStream()`. A follow-up uses `replyToId`.

### Read the page for structure, not names

The custom engine page lags its own products. It names Semantic Kernel and LangChain as example
orchestrators, calls Agent Framework "the Agent Framework SDK (formerly Semantic Kernel)" where
{{topic:maf}} presents it as the successor to Semantic Kernel *and* AutoGen, and heads a comparison
column "Teams AI" over prose about the Teams SDK. Take the routes and constraints from it, and take
product names from each product's own documentation.

## In practice at Technik

Getting the capstone into Teams for the four user groups runs straight into its identity design. The
agent reaches the MCP server through a Foundry toolbox signed in as its **Entra Agent ID**, and the
server admits only callers holding `Teamcenter.Read` ({{topic:stageship}}, {{topic:agentid}}).

The fastest route provisions "Entra ID" of its own. That may be harmless, a bot's identity in front
of an agent that still calls tools as itself, or it may put a second identity in the call path.

<!-- unknown since=2026-11 -->
The page never mentions hosted agents. Whether **Publish from Foundry** covers a hosted agent, and how
the identity it provisions relates to the agent's Entra Agent ID, are both undocumented. Check both
in a test tenant before choosing this route for the capstone.
<!-- /unknown -->

The SDK route carries a constraint the capstone has met before. Its documented Python range stops at
3.11, and both of the capstone's projects declare `requires-python = ">=3.12"`, so an SDK front end
cannot share their environment. It runs as its own process and calls the hosted agent over the wire,
the same answer the Agent Framework `mcp<2` pin forced in {{topic:localenv}}. Owning the plumbing
means owning its dependency graph too.

Streaming matters for the same reason. The capstone's refusal guard also covers streamed answers
({{topic:stageship}}). In Teams, a refusal sent as a second message after the stream may render
before the answer it replaces, so the guard's output has to travel inside the one stream.

## Design guidance

- **Choose the route by identity first.** Know which identity calls your tools before you pick the
  fastest path.
- **Keep the SDK layer thin.** Activities, state and channels go in it. Reasoning stays in the
  orchestration you already test.
- **Budget for retrieval you used to get free.** Microsoft 365 content now comes through Graph and the
  Retrieval API.
- **One stream per turn.** Put refusals, attachments and corrections inside it.
- **Isolate the front end's runtime** when its supported language versions differ from your agent's.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Messages in Teams appear in the wrong order | Streaming mixed with separate activities in one turn | One stream per turn; `setAttachments()`; `replyToId` for follow-ups |
| Tools fail after publishing from Foundry | A provisioned identity lacks the role the server requires | Check which identity calls the tools; assign the role or change route |
| The SDK will not install beside the agent | Its documented Python range ends at 3.11 | Run the SDK front end as a separate process |
| The agent cannot see SharePoint content Copilot Studio reached | Pro-code agents get no native Microsoft 365 knowledge | Ground through Graph or the Retrieval API |
| Advice names Semantic Kernel as the orchestrator | The custom engine page predates Agent Framework | Take names from each product's own documentation |

## Key terms

**Custom engine agent** — an agent with its own orchestration and models, surfaced in Microsoft 365
Copilot and Teams. Built low-code in Copilot Studio or pro-code with an SDK.

**Microsoft 365 Agents SDK** — the channel, activity and state layer between users' messages and your
agent logic. It makes no AI choices of its own.

**Activity** — the SDK's normalised form of anything a channel sends, routed to a handler by type.

**Turn** — one unit of work in a conversation, the boundary the SDK tracks state across.
