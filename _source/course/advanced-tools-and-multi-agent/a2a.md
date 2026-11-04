## TL;DR

A2A is "an open protocol enabling communication and interoperability between opaque agentic
applications", and *opaque* is the whole design. You cannot see inside the other agent, so the
protocol standardises only its outside: a card that advertises it, a task with a lifecycle, and a
transport. Two facts decide whether to use it. Identity is deliberately not in the payload, and
Copilot Studio hands the other agent your "Full chat history, not just the latest user utterance".

## Why it matters

{{topic:connected}} delegated to agents inside your own tenant and {{topic:multiagent}} asked whether
you should delegate at all. A2A answers a different question: what if the other agent is not yours?
Version `1.0.0` is "the first stable, production-ready version", and the governance says to take it
seriously — donated by Google to the Linux Foundation, steered by AWS, Cisco, Google, IBM Research,
Microsoft, Salesforce, SAP and ServiceNow, and accepted in August 2026 into the Agentic AI
Foundation, the same home as MCP.

That shared home matters, because the two protocols are explicitly not rivals: "MCP is for
agent-to-tool communication ... A2A is for agent-to-agent communication", or in the release post,
"MCP inside agents, A2A between agents." A2A is equally clear about what it refuses
to be: "Not a sub-agent or tool-call protocol."

## How it works

### The card is the interface

Discovery works like MCP's docstrings one level up. An Agent Card is "a JSON document that serves as
a digital 'business card' for an A2A Server", served at a well-known path, and its required fields
are the agent's name, description, supported interfaces, version, capabilities, default input and
output modes, and **skills**. A skill is "a more focused set of behaviors that the agent is likely to
succeed at", with its own id, description, tags, examples and security requirements.

So the card is both advertisement and contract, and {{topic:tooldesc}}'s rule applies unchanged —
except the consumer is a system you have never met.

<!-- unknown since=2026-11 -->
The path does not line up. The specification serves the card at `/.well-known/agent-card.json`, while
Copilot Studio's page says to check `/.well-known/agent.json` — so one is wrong, and it is the first
thing to test when autofill fails. The field names disagree too, snake_case in the protocol
definitions against camelCase on the discovery page. Read the card your counterparty serves.
<!-- /unknown -->

### A task, not a request

The unit of work is a **Task** — "the core unit of action for A2A. It has a current status and when
results are created for the task they are stored in the artifact." Its states are the vocabulary of
every failure you will debug: `SUBMITTED`, `WORKING`, then the terminal four `COMPLETED`, `FAILED`,
`CANCELED` and `REJECTED` — the last meaning "the agent has decided to not perform the task" — plus
two *interrupted* states, `INPUT_REQUIRED` and `AUTH_REQUIRED`. Those two are the interesting ones: a
remote agent can stop and ask for more input, or demand credentials you never supplied, and your side
needs somewhere for that to go ({{topic:hitl}}).

Three transports are official — "The core ones officially supported are `JSONRPC`, `GRPC` and
`HTTP+JSON`" — and the operations are few: send a message, get, list, cancel or subscribe to a task.
Long work has two shapes, each declared in the card: streaming over server-sent events
(`capabilities.streaming`), resumable after a dropped connection, and a webhook
(`capabilities.pushNotifications`) for tasks "lasting minutes, hours, or even days".

### Identity sits outside the message

This is the design decision to carry away. "A2A protocol payloads, such as `JSON-RPC` messages, don't
carry user or client identity information directly. Identity is established at the transport/HTTP
layer", credentials "**must** be transmitted in standard HTTP headers", and the server "**must**
authenticate every incoming request". Rejections are ordinary HTTP: `401` with a `WWW-Authenticate`
header, `403` when the caller is known but unauthorised. Authorisation can be per skill, with
"specific OAuth scopes" granting "access to invoke certain skills but not others", and production
traffic "must occur over `HTTPS`".

The webhook is where the spec gets sharpest, echoing {{topic:mcpsec}} almost word for word. "Servers
SHOULD NOT blindly trust and send POST requests to any URL provided by a client", because a malicious
one could point "to internal services or unrelated third-party systems, leading to Server-Side
Request Forgery (SSRF) attacks". Both directions must authenticate, and notifications "SHOULD include
a timestamp" so the receiver can reject stale ones.

### What Copilot Studio actually does

<!-- volatile verified=2026-11 -->
From the main agent's **Agents** page: **Add agent** → **A2A agent**, then the endpoint URL — and
note the warning, the opposite of what the spec's discovery mechanism trains you to expect: "The
endpoint URL should be the endpoint for communication with the agent and not the URL for the agent
card." Authentication is **None**, **API key** or **OAuth 2.0**; name and description autofill from
the card when one is found. Delegation is description-driven: "The description should describe the
purpose of your agent, so that your main agent can understand when [it] should be used."
<!-- /volatile -->

Two details change the design. First, "Because A2A connections use the custom connector
infrastructure, you can also use them to connect to A2A agents running on-premises or within a
virtual network" — so everything {{topic:customconn}} and {{topic:dlp}} say about connectors now
governs your agent-to-agent traffic. Second, the payload carries a `contextId`, message ids, locale,
message parts and "Full chat history, not just the latest user utterance".

<!-- unknown since=2026-11 -->
Neither Copilot Studio page says which identity the called agent runs as. The connection offers no
*as the signed-in user* option, and the payload carries no identity because the protocol puts none
there — so what the remote agent acts as is set entirely by the connection you
configured.
<!-- /unknown -->

## In practice at Technik

The capstone's agent reaches its own server through a Foundry toolbox ({{topic:stageship}}), not over
A2A, and nothing inside Technik needs A2A at all: both halves of the split {{topic:multiagent}}
considered live in one tenant. A2A is the exit the design keeps open, for the first counterparty
outside it — an EPC contractor's or a supplier's agent answering about their own scope.

Before that connection is made, the full-chat-history fact becomes a governance decision rather than
a protocol detail. A Production Assistant thread holds work order numbers, part and drawing numbers
and quality notification text — and two of Technik's QNs, `300001267` and `300001270`, carry injected
instructions in their descriptions. Forwarding a whole thread exports Technik's manufacturing detail
to another company *and* forwards hostile text to a system with its own tools and nobody's
supervision ({{topic:ctxsecurity}}, {{topic:threats}}).

So Technik's rule is narrow: an external A2A agent is added only with OAuth, only after its card has
been read, and only for a question whose context can be stated without the thread. Where that is
impossible, the right integration is a tool, not an agent.

## Design guidance

- **Read the counterparty's card before trusting its description.** It is the only machine-readable
  statement of what the agent claims to do.
- **Write your own card for a stranger**, with skills narrow enough to scope authorisation.
- **Handle the interrupted states.** `INPUT_REQUIRED` and `AUTH_REQUIRED` need a route to a human.
- **Treat a client-supplied webhook URL as hostile** until allow-listed and verified; the spec names
  SSRF outright.
- **Decide what leaves with the thread**, since full chat history is the default and the far side is
  outside your tenant — and govern the connection as a connector, because that is what it is.
- **Reach for a tool first.** A2A earns its place when the other side is genuinely an agent you do
  not own.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Name and description do not autofill | No card, or it is not on the path Copilot Studio checks | Open the endpoint plus `/.well-known/…` in a browser and compare both spellings |
| The remote agent is never called | A vague description on the connection | Rewrite it as what the agent is *for* |
| A long task appears to hang | Streaming or push notifications were never declared | Check the card's capabilities, then subscribe or register a webhook |
| Citations vanish across the hop | A documented Copilot Studio limitation | Expect it, and carry sources in the answer text |

## Key terms

**Agent Card** — the JSON document advertising an A2A server's identity, capabilities, skills and
security schemes, served at a well-known path.

**Task** — A2A's unit of work, with eight states: two in-flight, four terminal, and two interrupted
ones that need an answer from your side.

**Opaque agentic application** — the protocol's term for the other agent: addressable and described,
with no visibility into how it works.
