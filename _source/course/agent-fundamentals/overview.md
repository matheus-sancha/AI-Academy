## What this module is for

{{module:getting-oriented}} decided *where* you will build. This module decides *what you are building* —
and it contains the one choice in the level you cannot take back.

An agent is not a chatbot with better language. It is a loop that decides its own next step, and almost
everything that makes agent engineering different from software engineering follows from that: you cannot
enumerate what it will do, its reach is exactly the tools you gave it, and the text you write to describe
those tools *is* the routing logic rather than documentation of it.

The module also does something the roadmap cannot: it puts a price on the design. Every tool, every
instruction and every turn of conversation is re-sent to the model on each request, out of one shared
budget — so "add another tool" is never free, and the failure it eventually causes has a name.

## Before you start

You want {{module:getting-oriented}} first, mainly for {{topic:stack}} — this module assumes you know that
Copilot Studio is the build surface and roughly why. {{topic:llm}} and {{topic:context}} from Basic carry
more weight here than anywhere else in the level, because a model that is stateless and reads a bounded
context window is the whole explanation for {{topic:contextcost}}.

Nothing here requires a built agent, though {{topic:chooseharness}} is worth reading *before* you create
one. Allow about 90 minutes.

## What you will be able to do

By the end of this module you should be able to:

- say what makes something an agent rather than a chatbot or a workflow, and choose between the three for a
  given requirement;
- explain what a harness is, and attribute a behaviour to the harness, the context, the tools or the model
  in that order;
- choose a Copilot Studio harness deliberately, state what you gave up, and name the workaround — knowing
  that the choice cannot be transferred in either direction;
- explain how the runtime decides what to do, and write a tool or skill description that wins the selection
  it should and loses the ones it should not;
- account for what every turn costs, diagnose `CONTEXT_LENGTH_EXCEEDED`, and choose the right remedy rather
  than the visible one;
- design where a person belongs in the path, and tell the difference between a problem approvals solve and
  one only privilege solves;
- say what disappears when an agent becomes autonomous, and what has to be built to replace it.

## The thread through this module

The Technik Production Assistant stops being an idea and becomes an architecture.

{{topic:agent}} establishes why it has to be an agent at all: someone in production control asks about late
Coating work orders, narrows to a plant, points at one and asks what is holding it up — a path nobody drew,
and an answer that requires a join no field contains. Then it draws the line that matters, listing what is
deliberately *not* left to the agent's judgement.

{{topic:harness}} and {{topic:chooseharness}} make the permanent decision: the GitHub Copilot harness,
because the write-up has to ship as a skill and because a revision question takes two calls and a
comparison the runtime must recover from. The cost is topics, and the module says plainly what that costs
and where the guarantee goes instead.

{{topic:orchestration}} is the load-bearing lesson. Four exclusion clauses — *"do not use for work order
status"* and its siblings — are the difference between an assistant that routes well and the same agent,
same model, same data, routing badly. {{topic:contextcost}} then prices the catalogue those clauses live in,
and finds several hundred words of document conventions being re-sent on every turn to no purpose.

{{topic:hitl}} places the people: nothing gating reads, because a read-only role already bounds them;
nothing gating drafts, because a draft is not an action; a confirmation before a record others act on; a
real approval before a document revision changes what the shop floor works to. {{topic:autonomous}} closes
by asking what would break if nobody were watching at all.

## Self-check

<details>
<summary>1. An agent that worked fine starts failing turns with <code>CONTEXT_LENGTH_EXCEEDED</code> shortly after you added three tools. Why is "shorten the instructions" often the wrong first move?</summary>

Because four things share one budget — the instructions, the conversation history, **every** tool
definition, and any tool results — and the instructions are the only one with a visible number next to it.
The contributor that actually grew is the tool definitions, which are re-sent on every turn for every tool
whether or not the question needs them. Tools are a standing charge, not a cost you pay when they fire.

Cutting instructions is also the most expensive option available, because that is where the role, rules and
routing live and those earn their keep every turn. If instructions genuinely are the problem, cut
*reference material* rather than structure, and move it into a knowledge source or a skill — skills use
progressive disclosure, so until one activates only its description is in play, not its body. The other two
documented remedies are cheaper here: reduce the tool count, or start a new conversation. And if nothing
fits without cutting rules, the agent is doing too much and should be split
({{topic:contextcost}}).
</details>

<details>
<summary>2. You built your agent on the GitHub Copilot harness. A new requirement arrives: a structured intake that must run exactly as drawn, every time. What are your options?</summary>

Not "switch the harness" — the documentation is explicit that an agent created on the GitHub Copilot harness
cannot be transferred to the standard harness, or the other way round. Topics live only on the standard
harness and they are the only way to *guarantee* a conversation path.

So: put the guarantee somewhere other than a conversation — in the tool's input contract, or in a flow,
which is where a format check or a fixed sequence can be enforced rather than requested. Or delegate that
piece to a connected agent on the standard harness. Or rebuild, if the scripted path is genuinely central
to the product.

The real lesson is upstream: this is why the harness is chosen before creation and the reasoning written
into the agent's description. An instruction usually catches a badly formatted value; a topic always would
({{topic:chooseharness}}).
</details>

<details>
<summary>3. You rewrite a tool's description to fix misrouting, test the same question again, and the agent behaves exactly as before. What do you check before concluding the description is still wrong?</summary>

Start a new chat. The runtime uses recent conversation history when it decides what to call, so the same
question can route differently in a fresh conversation than in one that has been running — Microsoft names
this comparison directly and calls the behaviour expected, because it is what lets an agent handle
follow-ups. Your previous attempts are still steering it.

Two related checks. If you changed the model, re-test routing and not just answers, because models differ
in how they select. And read the activity trace rather than inferring from the answer — it tells you what
was actually chosen and why, which is a different question from whether the answer was good
({{topic:orchestration}}).
</details>

<details>
<summary>4. In the Technik design, releasing a document revision needs an approval but reading Snowflake data needs nothing at all. Why is that not inconsistent?</summary>

Because they are different problems. Reading is bounded by **privilege**: the assistant reads as
`TECHNIK_AGENT_RO`, a read-only role, so there is nothing to approve because nothing can be changed. Asking
a person to approve reads would be theatre — and it would be weak theatre, because the Technik data contains
notification descriptions that try to talk the agent into doing more than reading, and a privilege boundary
holds against that where an approval does not.

Releasing a revision is different: it is irreversible and it changes what the shop floor works to the same
day. That earns a real approval, placed between the draft and the release — the last point where reversing
is still cheap — with the draft, the ECN and the diff in the request so the approver can actually judge it.

Note what is *also* ungated: the draft itself. A draft is not an action, and gating it would teach people
that approvals are noise, which is exactly how the one that matters stops being read
({{topic:hitl}}).
</details>

<details>
<summary>5. Someone proposes making the assistant autonomous — triggered whenever a new quality notification appears. What disappears, and what has to be built to replace it?</summary>

What disappears is the user, and with them a lot of free safety: they noticed wrong answers, rephrased
misunderstood requests, and abandoned conversations that went strange. None of that was designed, and all
of it now has to be.

Five things replace it. A **trigger** specific enough that it does not fire on everything — the most common
autonomous failure, in both directions, since too narrow means it silently never runs. **Tighter
instructions**, because ambiguity a person would resolve in a second becomes a systematic error repeated
across every item. A named **failure path**, decided before go-live. **Monitoring that alerts on silence**,
because an agent doing nothing looks identical to an agent with nothing to do. And a **cost cap**, because
consumption is now bounded by the trigger rather than by demand.

The sound version also shrinks the model's job: deterministic validation around one narrow model task,
with anything low-confidence going to a review queue rather than being guessed
({{topic:autonomous}}).
</details>
