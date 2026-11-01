## What this module is for

You have already shipped an agent that ran a loop. You just could not see it. Copilot Studio chose
knowledge, tools and topics from the descriptions you wrote, decided when to stop and when to ask, and
none of that was yours to change. This module opens the lid.

The surprise is how little of it is about the model. A harness is the runtime around the model, and
nearly everything you tune lives in that runtime: how many tool calls one request may make, whether
the model ever sees why a tool failed, what runs without asking, which files the agent reads before it
starts, and who owns the whole loop in the first place. Six lessons, six places to put a decision
that a prompt cannot hold.

It is also where this level's honesty about boundaries begins. The documentation you will read is
unusually blunt — an LLM judge approving tool calls is "not a security boundary", sandboxing is "an
added layer", and verifying an instruction file "verifies discovery, but not whether the instructions
are followed". Take those at face value. Three of the six lessons end up in the same place: if a rule
must hold every time, it goes in code or in an identity, not in a dialog or a prompt.

## Before you start

You need {{topic:harness}}, which named the thing this module takes apart, and
{{topic:orchestration}}, whose loop was deliberately not explained there. {{topic:chooseharness}} made
this choice once inside Copilot Studio; {{topic:harnessvssdk}} makes it again with your own code as an
option. {{topic:hitl}} said where a person has to confirm, and {{topic:permissions}} is the mechanics
of that confirmation on a surface that holds your shell. {{topic:agentmode}} set up the editor's agent
and its approvals, so this module does not repeat them.

Nothing here needs to be run. The capstone repository is public, so the code the lessons quote can be
read alongside them, and it is tested offline only ({{module:capstone-build}}). One lesson's worked
example uses Copilot CLI, which is worth installing if you want to follow it.

Allow about two hours.

## What you will be able to do

By the end of this module you should be able to:

- describe the agent loop as read, decide, call, observe, repeat — and say what has to be true at each
  step for the next one to be worth running;
- set a stop condition deliberately, and defend the number you chose;
- say why a rule in the instructions and the same rule in middleware are not equivalent;
- write a tool error a model can act on, and explain why *not found* is the worst thing to return;
- place a human gate without stalling a run, and say what has to be persisted at one;
- name the two things VS Code's documentation refuses to call security boundaries, and what you would
  use instead;
- pick a Copilot surface by the review point you intend to use, rather than by convenience;
- choose between `AGENTS.md`, a targeted instruction file, a prompt file and a custom agent — and say
  which one does not travel between harnesses;
- decide between a managed harness, an SDK and a platform runtime, naming the requirement that settles
  it.

## The thread through this module

From the inside out: the loop, then what steers it, then what bounds it, then who owns it.

{{topic:loop}} sets the loop running and finds two levers on it — six tool calls and detailed tool
errors, two lines of configuration — then puts the groundedness rule in middleware, where the loop's
exit is, because that is the only place it can be made true. {{topic:planning}} asks what happens when
a step fails, and answers mostly from outside the model: an error that lists the operations that do
exist, a business rule kept in a Snowflake view instead of in the agent's plan, and a stop that was
decided in advance. {{topic:permissions}} works out what the agent may do unasked, and arrives at
identity rather than approval dialogs — a role that cannot write beats any setting that asks politely.
{{topic:ghharness}} takes the same agent across the editor, the terminal and the cloud, and shows the
review point moving with the autonomy, plus two limits that shape what you can delegate at all.
{{topic:customize}} commits the repository's own context as files, and finds that the one thing people
reach for first — a prompt file — runs on exactly one harness. {{topic:harnessvssdk}} closes the module
with the question the other five were evidence for: which layer do you actually need to own, and what
can you hand back.

## Self-check

<details>
<summary>1. An agent answers a question about a drawing revision confidently and correctly, with no tool call in the run. Is anything wrong?</summary>

Yes, and the fact that it was right this time is the problem. An answer no tool result backs came from
the model's memory of training data, not from Teamcenter — so it is a coincidence, and the next one
will be a confident invention. This is why the capstone inspects the finished run for a
`function_result` and replaces an ungrounded answer with a fixed refusal.

Note *where* that check lives. The instructions already say to answer only from tool results, and the
instruction layer is doing useful work. But instructions are followed, not enforced, so the guarantee
is middleware wrapped around the loop. The general rule for the whole module: if it must hold every
time, it is code ({{topic:loop}}, {{topic:stageagent}}).
</details>

<details>
<summary>2. A tool cannot find operation <code>0015</code> on a work order. What should it return, and what will the agent do with each option?</summary>

It should return the operations that **do** exist. Given a bare *not found*, the model has no
information to plan with and will usually guess — trying `0010`, `0020`, `0030` in turn, spending
passes against the iteration limit, and possibly answering about the wrong operation. Given *"Work
order 100004510 has no operation 0015. Its operations are: 0010 Machining, 0020 Cladding…"*, it
recovers on the next pass or asks the user a precise question.

This is the cheapest planning improvement available, and it happens in the server rather than in the
agent. It depends on one framework setting: Agent Framework hides tool errors from the model by
default, so a carefully written error arrives as `Error: Function failed.` unless detailed errors are
turned on ({{topic:planning}}, {{topic:tooldesc}}).
</details>

<details>
<summary>3. A colleague proposes running the editor's agent with auto-approval on everything, arguing that sandboxing will contain any damage. What is wrong with the argument?</summary>

Both halves. Sandboxing is documented as "an added layer" and explicitly "not a virtual machine or
user-account boundary, a standalone security boundary" — and injected credentials, allowed paths,
unrestricted network access and unsandboxed fallbacks all weaken it further. It is also narrower than
people assume: sandboxing a local MCP server is macOS and Linux only, so on Windows that stdio server
runs with your account's access.

The answer is not a better setting. It is capability and identity: a tool that cannot write, a
read-only Snowflake role, an app role checked before a request reaches the server, a dev container
when a real boundary is needed. Approvals are for the decisions a person should make, not for the ones
that must never be possible ({{topic:permissions}}, {{topic:sfroles}}).
</details>

<details>
<summary>4. You want to delegate "update the eval baseline and the behaviour it measures" to the cloud agent. Why is that one task a problem?</summary>

Because Copilot "can only work on one branch at a time and can open one pull request per task", and
because the two changes want different review. A baseline moves *because* behaviour moved, so bundling
them means the artefact that would have detected a regression changes in the same reviewed unit as the
cause — the reviewer has nothing to compare against.

Two other limits shape delegation on the same surface: an Actions-based session has a maximum
execution time of 59 minutes, which "cannot be extended or bypassed", and an Actions session can only
change the repository you named when you started the task. Sizing tasks to one branch, one pull
request and well under an hour is not a quota workaround; it is how the surface is meant to be used
({{topic:ghharness}}, {{topic:evalharness}}).
</details>

<details>
<summary>5. Your repository is worked on from more than one harness. Where do you put a reusable "draft the change summary for an ECN" task, and where do you put "this repo is two dependency projects on purpose"?</summary>

The reusable task goes in a **skill**, not a prompt file. Prompt files run only in Local harness
sessions in the Chat view, and authoring one in a Copilot session does not make it runnable there —
the documented alternative is to create a skill or convert the prompt file into one
({{module:authoring-skills}}).

The dependency fact goes in an **always-on** file at the repository root, `AGENTS.md` or
`.github/copilot-instructions.md`, because an agent that does not know it will helpfully reconcile the
two `mcp` pins and break the build. Targeted `*.instructions.md` files with an `applyTo` glob are for
context that only matters when particular files are touched, such as the seed data whose rows
reproduce figures quoted in lessons. And remember what none of it is: discovery is verifiable,
compliance is not, and there is no general precedence order between these files — so never let two of
them disagree ({{topic:customize}}, {{topic:localenv}}).
</details>
