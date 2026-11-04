## What this module is for

You have added tools to an agent and built a server of your own. This module covers everything that
is left when the easy integration does not exist: wrapping an API nobody has wrapped, sharing a
credential safely across environments, driving a system that has no API at all, and coordinating
agents — yours and other people's.

Two questions run through all seven lessons, and the product answers neither for you. **How is this
described?** A connector's operation description, a REST tool's mandatory description, a computer-use
instruction, an A2A agent's card, the sentence a main agent reads before delegating — each is the
interface, and each decides what gets chosen. **Whose authority does it run as?** A connection's
owner, a service principal, a maker's stored password, a header on an HTTP request, an Entra Agent
ID. Get the description wrong and the right thing never fires; get the identity wrong and the wrong
thing succeeds.

The second thing to expect is that nothing here is the first choice. You build a connector because
none exists, use computer use because there is no API, add a second agent because one "can't reliably
handle" the task. The documentation is unusually honest about this — "Use the lowest level of
complexity that reliably meets your requirements" — and unusually honest, too, about how little its
guardrails promise. Computer use's access control "doesn't stop the model from opening" a blocked
site, its human supervision is not "a safety fail-safe", and three of the five orchestration
patterns list a loop as their documented failure. The boundaries you can rely on are the ones you
build: a narrow tool, a least-privileged identity, a hard iteration cap.

## Before you start

From Intermediate, {{topic:connectors}} and {{topic:connauth}} are the ground this module stands on —
particularly the warning that a connection's identity is the most common reason a shared agent
breaks. {{topic:tools}} and {{topic:tooldesc}} carry the description rule in its original form, and
{{topic:addconnector}} is the habit of verifying that the orchestrator actually chooses what you
expect. {{topic:connected}} introduced child and connected agents, {{topic:computeruse}} introduced
computer use as a last resort, and {{topic:dlp}} and {{topic:agentauth}} matter more than they look:
two of this module's integrations turn out to be connectors underneath, so connector policy governs
them. {{topic:envs}} and {{topic:solutions}} stop being administrative detail here.

From this level, {{module:building-mcp-servers}} is the comparison half of the first two lessons —
especially {{topic:mcpcs}}, where handing a server to a platform took three things away, and
{{topic:mcpsec}}, whose attack classes reappear almost verbatim in A2A's webhook rules.
{{topic:toolshaping}} and {{topic:budget}} are the arithmetic behind every multi-agent context
decision, and {{topic:ctxsecurity}} already covered indirect prompt injection, so the lessons here
deal only with what a new surface adds. {{topic:permissions}} set the expectation that a feature
which looks like a boundary may not be sold as one.

Nothing here needs to be run. The capstone repository is public and tested offline only
({{module:capstone-build}}).

Allow about two and a half hours.

## What you will be able to do

By the end of this module you should be able to:

- decide between a custom connector, a REST API tool and an MCP server by asking who the consumers
  are, not which is more sophisticated;
- plan a connector's second year — the update that does not propagate, and the platform change that
  breaks it without a commit;
- say what a REST API tool leaves undocumented, and why that uncertainty is a governance question;
- bind a solution to a credential per environment, and name the one documented route to letting a
  service principal activate it;
- separate a connector's credential from a secret your logic reads, and set up each correctly;
- harden computer use where the hardening actually lives, and state plainly what its guardrails do
  not promise;
- name the five orchestration patterns, pick one from the problem, and argue the harder case that no
  pattern is needed;
- justify a multi-agent split with one of the three documented reasons, and recognise a split that
  follows your systems rather than your questions;
- connect to an agent you do not own over A2A, read its card, handle its interrupted task states, and
  decide what leaves your tenant with the thread;
- give an agent its own identity, and explain why that identity is designed to be denied things a
  person could hold.

## The thread through this module

Outward from the integration to the identity. {{topic:customconn}} wraps an API the platform does not
know and finds that your updates reach nobody until every consumer rebuilds. {{topic:restapi}} offers
the same thing in minutes and will not say whether it is a connector. {{topic:connrefs}} separates
what ships from what authenticates, then runs into the fact that someone human still has to switch it
on. {{topic:cuaadv}} takes the integration of last resort into production and finds that every
documented safeguard is hedged.

Then coordination. {{topic:multiagent}} lays out five patterns and spends its best material arguing
against using any of them. {{topic:a2a}} crosses the tenant boundary to an agent described as
*opaque*, where identity sits outside the message and Copilot Studio sends the whole conversation.
{{topic:agentid}} closes the module by giving the agent a principal of its own — and the design turns
out to be mostly a list of things it may not have.

## Self-check

<details>
<summary>1. A colleague wants Teamcenter's REST API available to the Production Assistant. They have found three ways to do it and want to know which is "most advanced". How do you redirect the question?</summary>

By asking who else will call it. A custom connector is "a wrapper around a REST API" registered in
the tenant, so it serves Copilot Studio, Power Automate and Power Apps alike — which matters here,
because the document revision flow needs the same call. A REST API tool is configured inside one
agent and helps only that agent. An MCP server is code you own and deploy, reaching MCP clients.
None is more advanced; they differ in who can reach them.

Two costs belong in the answer. The connector's updates do not propagate: when a field changes you
republish, then "Remove any connection / data source in any app that used that connector" and re-add
it — the exact inverse of {{topic:mcpcs}}, where edits reach every agent with no release step. And
the REST API tool's documentation never says whether it is a Power Platform connector, so whether
data policies govern it is unverified. Assume they do ({{topic:customconn}}, {{topic:restapi}}).
</details>

<details>
<summary>2. The assistant is getting large, so a colleague proposes splitting it in two: a production agent over SAP and an engineering agent over Teamcenter and the documents, with handoff between them. What is wrong with that, and what would make it right?</summary>

The split follows Technik's systems, and its questions do not. The sharpest question the assistant
answers is whether a work order is running against a superseded revision — `100004510` still names
drawing `DU700001042` revision B after `ECN70000051` released C — and answering it means joining SAP
operations to the Teamcenter revision view in one query. Under a handoff that question crosses the
boundary mid-thought, and neither agent can perform the join.

The documented default is also against them: a single agent with tools is "Often the right default
for enterprise use cases", and multi-agent orchestration "Adds coordination overhead, latency, and
failure modes". Three reasons justify the split — prompt complexity, tool overload, or a security
requirement — and only the third applies at Technik, where Snowflake is read by one service role
while the SharePoint documents are read with each user's own permissions. That is the real seam, and
the superseded-revision query stays whole on one side of it ({{topic:multiagent}},
{{topic:connrefs}}).
</details>

<details>
<summary>3. A manager read that computer use "adapts to interface changes" and wants it running unattended against the supplier portal, with an allow list so it cannot wander. What do you tell them?</summary>

That both halves of their plan are weaker than they sound. The adaptability claim is contradicted by
the product's own FAQ — "Sensitive to interface and timing changes. Layout changes, loading delays,
or unexpected dialogs can produce different outcomes for the same task" — so treat the run as
fragile, not self-healing. And the allow list governs actions rather than reach: it "only prevents
the model from taking actions on websites or applications that aren't in the allow list", with the
docs' own example being the model reaching Bing from the Edge search bar.

Unattended is the part to refuse outright. Human supervision is model-triggered and probabilistic —
you "shouldn't rely on clarification requests as a safety fail-safe" — and it is not optional either,
because "If you don't configure reviewers, these requests have nowhere to be routed, so the session
fails when the agent pauses." So configure a reviewer, run it on a dedicated machine under a
least-privileged account, and price it: five Copilot Credits per step adds up fast enough to fund the
connector instead ({{topic:cuaadv}}, {{topic:customconn}}).
</details>

<details>
<summary>4. An EPC contractor offers an A2A endpoint so the assistant can ask about their scope directly. Name the two things to settle before the connection is made.</summary>

What leaves, and who the far side is. Copilot Studio's A2A payload carries "Full chat history, not
just the latest user utterance", so one question exports a whole thread — work order numbers, part
and drawing numbers, and quality notification text. Two of Technik's QNs, `300001267` and
`300001270`, carry injected instructions in their descriptions, so forwarding the thread also
forwards hostile text into a system with its own tools and none of your supervision.

Identity is the second, and the protocol deliberately leaves it to you: "A2A protocol payloads ...
don't carry user or client identity information directly. Identity is established at the
transport/HTTP layer." Neither Copilot Studio page says which identity the called agent runs as, so
it is whatever the connection was configured with — OAuth, not an API key, and not **None**. Two
practical notes: read their Agent Card and its skills first, and remember that "A2A connections use
the custom connector infrastructure", so this traffic is governed as a connector ({{topic:a2a}},
{{topic:ctxsecurity}}).
</details>

<details>
<summary>5. The capstone agent already has an Entra Agent ID. Why does it still need the Snowflake service user `TECHNIK_AGENT_SVC`, and what would you check about the Entra side?</summary>

Because they answer different questions. The Entra Agent ID is who the agent is to Azure: it governs
whether the agent may reach its MCP server at all, through the toolbox connection at
{{topic:stageship}}. `TECHNIK_AGENT_SVC`, holding the single read-only role `TECHNIK_AGENT_RO`, is
who it is to the data, and governs which rows come back. Neither can answer the other's question, and
the read-only ceiling happens to match the role ceiling Entra would impose anyway — "Only lower
privileged roles (such as a reader role) can be assigned to an agent."

Three things to check on the Entra side. The blueprint, because "OAuth permissions granted to a agent
identity blueprint are granted to all agent identities created from that blueprint" — it is a blast
radius, not a template. Conditional Access, which cannot use MFA here, since "Agents can't satisfy
interactive controls like MFA"; use identity filters, risk and named locations instead. And the
credential: prefer managed identities or certificates to client secrets, which removes one thing
{{topic:connrefs}} would otherwise have to rotate ({{topic:agentid}}).
</details>
