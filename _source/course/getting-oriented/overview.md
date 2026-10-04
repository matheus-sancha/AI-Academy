## What this module is for

You have used Copilot. You know what a model does, why it invents things, and how to ask it for
something useful. None of that told you where to *build*.

This module is the orientation: what the job is, which of Microsoft's several build surfaces fits which
problem, what any of it costs, where you are supposed to work, and — the one that saves the most
time — why nothing here can tell you what your own environment actually contains.

Nothing is built in this module. It exists so that the first real decision you make in
{{module:copilot-studio-basics}} is an informed one, because two of the choices ahead of you cannot be
undone afterwards.

## Before you start

The Basic topics listed in {{module:what-you-already-know}} are assumed, and most of this module leans
on just two of them: that a model predicts rather than looks up ({{topic:llm}}), and that Copilot only
ever shows you what you could already open ({{topic:visibility}}). The second becomes a governance
principle here rather than a convenience.

You do not need an environment yet, and you do not need to have built anything. Allow about 75 minutes.

## What you will be able to do

By the end of this module you should be able to:

- describe what an AI engineer produces, and how it differs from what a data scientist, a solution
  architect or a maker produces;
- place a requirement on the right build surface — Agent Builder, Copilot Studio or pro-code — and
  defend the choice against its hardest requirement;
- name the two decisions that cannot be reversed later, and say when each is made;
- explain what a Copilot Credit is, what exhausts capacity, and what an agent looks like when it runs
  out;
- set yourself up properly: your own developer environment, what it includes, what it simply does not
  have, and why the agent gets a different identity from you;
- build a small agent in Agent Builder and state precisely where its ceiling is;
- tell the difference between *broken*, *switched off*, *unlicensed* and *blocked by policy* — and know
  where to look for each.

## The thread through this module

One question runs through all six lessons: **where does the Technik Production Assistant belong, and
what do you need before you can build it?**

The assistant has to answer questions about work orders from SAP data in Snowflake, answer engineering
questions from controlled documents, and draft document revisions for their owners to submit — then live in Teams
for a whole department. {{topic:role}} works out which of those decisions are yours rather than the
model's. {{topic:stack}} takes the requirements one at a time and lets the hardest one pick the
platform. {{topic:licensing}} prices the evaluation runs that will prove it works. {{topic:devenv}} is
where you will build it, and where the agent gets a read-only role of its own.

Then {{topic:agentbuilder}} does something the rest of the module cannot: it builds one real slice of
the assistant — the engineering-questions capability — in about an hour, and it works. Ask that same
agent for the status of a work order and it fails completely, with no setting to fix. That is the
ceiling, met on purpose, and it is the argument for the remaining sixteen modules.

{{topic:tenantvaries}} closes the module by taking back a little of what the others promised: every
feature named here might be absent from your tenant, and the difference between a bug and an
entitlement is something you now know how to check.

## Self-check

<details>
<summary>1. You built an agent in Agent Builder that answers engineering questions from SharePoint, and it works well. You now need it to report the status of a work order from Snowflake. What are your options, and which one is right?</summary>

Agent Builder cannot integrate external services through actions, so there is no configuration that
makes this work — this is a ceiling, not a setting. Your options are to rebuild in Copilot Studio, or
to **copy the agent to Copilot Studio**, which is documented and preserves the core configuration and
instructions. Copy, then add the connector there. What you should *not* do is keep looking for the
setting, or split the work across two agents so that users have to know which one to ask. Note the
direction of the door: agents copy upward from Microsoft 365 Copilot to Copilot Studio, not back
({{topic:stack}}).
</details>

<details>
<summary>2. A Microsoft page describes a connector you need. You cannot find it in your environment. What are the possibilities, in the order you should check them?</summary>

Four, and "broken" is not among them. **Not licensed** — it may be premium, and your plan or
environment may not include it. **Blocked by a data policy** — DLP decides which connectors may be
used together, and the reason shows up where makers rarely look. **Switched off or in preview** — an administrator may not
have enabled it. **Wrong environment** — the tenant's default environment is not where premium and
custom connectors belong; a developer environment is.

Underneath all four is the distinction that matters: Microsoft publishes the full catalogue of
connectors that *exist*, but nothing publishes which ones **your** environment offers after licence,
policy and administrator decisions. The catalogue tells you what could exist; only your own
environment's connector list tells you what does ({{topic:tenantvaries}}).
</details>

<details>
<summary>3. Your evaluation run stalls partway through, repeatedly, in your developer environment — and then runs fine an hour later. What do you check first?</summary>

The rate limit, not your agent. Generative AI messages are capped at roughly 10 requests per minute
and 200 per hour on trial and developer environments — an order of magnitude below a pay-as-you-go
environment's 100 per minute and 2,000 per hour. A twenty-five case evaluation set is a real fraction
of that hourly allowance, and two runs back to back will throttle.

The tell is the recovery: a defect does not fix itself after an hour, and a quota does. Check the
quota before you touch the instructions, because "it worked later" is otherwise the most misleading
evidence you will ever collect ({{topic:licensing}}, {{topic:devenv}}).
</details>

<details>
<summary>4. Why should the Technik agent read Snowflake as <code>TECHNIK_AGENT_RO</code> rather than through your own development role, which already works?</summary>

Because a read-only role cannot be talked into writing. Everything the agent reads is potentially
attacker-controlled — a quality notification description is free text typed by anyone on the shop
floor — and text the agent reads can attempt to reach the tools the agent holds. If the only role
available to it cannot update or drop anything, the worst case is bounded by the platform rather than
by a sentence in your instructions, which a model trying to be helpful can reason around.

There is a second, duller reason: a connection that authenticates as you stops working, or silently
returns *your* data, the moment someone else uses the agent. Your role is for exploring the data
model. The agent gets its own ({{topic:devenv}}, {{topic:connauth}}).
</details>

<details>
<summary>5. Your agent answers questions normally, but a flow it is supposed to call does nothing at all, and there is no error message. What is the most likely cause?</summary>

Exhausted prepaid capacity. When an environment runs out, **new agent flow runs are blocked while the
parent agent carries on answering everything that does not need a flow** — so the agent looks healthy
and merely appears to have forgotten one of its capabilities. Flow authors also see a design-time
warning in the designer, which is the confirmation to look for.

The fix is capacity rather than configuration: reallocate credits to the environment, purchase more, or
enable pay-as-you-go. And the lesson generalises — capacity exhaustion presents as partial, silent
misbehaviour rather than as a billing message, which is why "it stopped doing one thing late in the
month" should always be a capacity hypothesis first ({{topic:licensing}}).
</details>
