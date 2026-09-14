## What this module is for

By B7 the Technik Production Assistant has knowledge and tools. It can find things and it can call
things. What it does not have is **know-how**: a written, reusable account of *how Technik does a
particular kind of task*.

A skill is that. Name, description, Markdown instructions, and optionally files it carries with it.
The orchestrator loads it only when a request matches its description, so an agent can hold a great
deal of know-how without paying for it on every question.

This module also contains the course's first hard platform constraint, and it is worth meeting
head-on rather than discovering it in the lab.

> [!IMPORTANT]
> **The Technik Production Assistant cannot have skills.** It was created on the standard harness in
> B5, skills belong to the GitHub Copilot harness, and the harness is chosen at creation and cannot
> be changed. This is not a gap in the course; it is the decision from
> [B4](../../beginner.html#B4) coming due. The lab builds the skill where skills live, then brings
> the capability back to the assistant the way the standard harness allows — which is exactly what
> [Reuse in the Standard Harness](reuse.html) is about.

## Before you start

[B7 Tools, Connectors & MCP](../B7/index.html), conceptually — the lab adds a tool, and assumes you
know what a tool description does. As always the lab ships its own starter.

You will need:

- your Power Platform developer environment and Copilot Studio;
- your Snowflake sandbox with `ACADEMY_AGENT_<you>` working;
- about 65 minutes for the lessons and 90 for the lab;
- a modest number of Copilot Credits. Skills are reasoning-heavy, so budget a little more than B7.

## What you will be able to do

By the end of this module you should be able to:

- say what a skill is, what it is made of, and when the orchestrator loads it;
- decide, for a given behaviour, whether it should be a tool, a skill, a topic or a flow — and
  defend the choice;
- add an existing skill from a `SKILL.md` file or a bundle, and say what you checked first;
- write a skill from blank whose description triggers on the right requests and not on others;
- explain why a standard-harness agent cannot hold a skill, and implement the same capability
  there anyway;
- recognise that a skill which reads user-written text inherits every risk that text carries.

## The thread through this module

Bruno raises three or four quality notifications a week, and every one of them takes twenty minutes
he would rather spend on the shop floor. The findings are in his head and in his measurements; what
takes the time is writing them up in the form `SOP70000101` and `GWI70000027` require, with the
readings, the acceptance criterion, the immediate action and the disposition requested, in that
order, every time.

That is exactly the shape a skill fits: a task done often, the same way, where the *how* is written
down but nobody remembers all of it. You will build it, discover it cannot live on the assistant,
and connect it instead.

## Self-check

<details>
<summary>1. An agent has a tool that queries notifications and a skill that writes them up. What is the difference, in one sentence each?</summary>

The **tool** performs an action: it runs a fixed query and returns rows. The **skill** holds
know-how: how Technik words a write-up, in what order, quoting which criterion, requesting which
disposition. A tool is a verb the agent can do; a skill is a procedure it can follow — and a skill
frequently *uses* tools, which is the relationship that makes the two easy to confuse.
</details>

<details>
<summary>2. Why does a skill cost nothing on questions that do not match it?</summary>

Because only its **description** is in the catalogue the orchestrator reads. The instructions and
any bundled files are loaded when the description matches the request, not before. That is the whole
economic argument for skills over long agent instructions: instructions are read on every single
turn (see [Context](../B1/context.html)), a skill's body is read on the turns that need it. It also
means the description is doing all the routing work, exactly as a tool description does.
</details>

<details>
<summary>3. Your new skill never triggers. Where do you look, and in what order?</summary>

The description, first and usually last. It is matched against how users actually phrase the
request, so "Drafts quality notification write-ups in Technik's format. Use when someone describes a
defect they have found and wants it written up" beats "QN helper". Then check for **overlap** — if a
tool or another skill already claims that territory, one of them wins and it may not be the one you
want. Only then consider whether the agent is on a harness that supports skills at all, which in
this course is a real possibility. What almost never helps is rewriting the skill's instructions:
they are not read until it triggers.
</details>

<details>
<summary>4. Technik wants the same write-up behaviour in the standard-harness assistant. Name two ways, and say what each costs.</summary>

A **connected or child agent** on a harness that does support skills, which the assistant hands the
task to: the know-how stays in one place, and the cost is an extra hop of latency and a handoff that
has to carry the context. Or **rebuild it in standard-harness parts** — a topic that gathers the
findings and an agent flow or AI Builder prompt that writes them up: no extra hop, and now the same
know-how exists twice and will drift. The first is usually right; the second is right when the
behaviour is small and the latency matters.
</details>

<details>
<summary>5. The write-up skill reads a quality notification description from Snowflake. What risk have you just taken on?</summary>

Notification descriptions are free text typed by people on the shop floor, and the seeded Technik
data contains two that address the agent directly and tell it to do something else. A skill that
reads that text is reading attacker-controlled input with the agent's tools in hand. Nothing in this
module defends against it; B11 and A13 do. What this module can do is keep the blast radius small —
the agent's Snowflake role is read-only, so the worst case is a bad write-up rather than a changed
record.
</details>
