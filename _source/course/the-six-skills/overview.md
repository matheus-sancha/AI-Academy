## What this module is for

The six skills come from an upstream repository, `copilot-studio-skills`, and this course is written against its
{{skills-version}} release. They are not six features. They are one route for building one agent, and each skill
owns a stage of it. This module covers which skill owns what, how to get the six onto an agent and off it again,
and the one product behaviour the whole route is designed around.

The stage-by-stage instructions stay upstream, where they are versioned, so there is one copy and it cannot
drift. Come back here when you need to know what one of the six does, or why the route insists on something that
looks unnecessary.

## Before you start

You want {{module:agent-skills}}, because the six are ordinary skills: they activate on their descriptions,
they fail load-time checks silently, and one of them is a package. {{topic:conversation}} is essential. It
establishes that a skill does not reach a running conversation, and this module's last lesson builds the
whole route's logic on that fact.

The six skills write the documents the earlier modules taught you to judge: the brief ({{module:designing-an-agent}}),
the instructions ({{module:writing-instructions}}), the tool plan ({{module:tools-connectors-mcp}}) and the
evaluation set ({{module:testing-and-evaluation}}). You do not need to have written them yourself, but you need
to be able to tell a good one from a plausible one.

Nothing here needs a tenant to read. Allow about 45 minutes.

## What you will be able to do

By the end of this module you should be able to:

- name the skill that owns each stage of the route, and reach it by asking for what it does;
- answer the router's placement question honestly, and say what a thin brief costs;
- say what each skill refuses to do, and why that refusal protects the build;
- install the six from the pinned release, and confirm they are live;
- explain why no `copilot-*` skill belongs on a published agent, and where in the route they come off;
- explain why the build keeps one conversation and still needs a new chat before testing;
- recover a build whose conversation was lost, and say which output cannot be recovered.

## The thread through this module

One build, the Technik Production Assistant, seen through the toolchain instead of stage by stage.

{{topic:sixoverview}} sets out what each of the six produces for the assistant: a brief with the supervisors'
words in it, a tool plan with a **Check** line on the Snowflake connector, `qn-write-up` as a package, and 25
evaluation cases including a tempting attempt to call an unreleased revision current. {{topic:installing}} puts
the six on a GitHub Copilot harness agent from the {{skills-version}} release, and shows what a published
assistant does if they are never taken off. {{topic:notrunning}} uploads `qn-write-up` halfway through the
build to see it work, and loses the build conversation as a result.

## Self-check

<details>
<summary>1. At stage 3 the tool plan says your tenant has no Snowflake connector. Which skill do you go back to, and which do you not?</summary>

Go back to `copilot-find-skills-and-tools`, the stage 3 owner, with what the **Check** line found. The plan is its
output, and an alternative (an MCP server, a workflow, or dropping the need) is its decision ({{topic:sixoverview}}).

Do not fix it by editing the instructions draft. The instructions are revised at stage 5 precisely so they can
name the tools that actually exist. Patching them now means they describe a plan nobody made.
</details>

<details>
<summary>2. You worked through the designing-an-agent module and have a brief, but the Connected agents slot says "TBD". What do you answer the router?</summary>

**A**, nothing yet. The router places you at the earliest stage you have not genuinely completed, and a brief
with an undecided slot has not completed stage 1. Answering **B** skips the interview and sends an undecided slot
into the instructions, the tool plan and the test set, which all read the brief ({{topic:sixoverview}}).

The interview will not accept "TBD" either. It re-asks a slot that fails its acceptance test, so that is where
the decision gets made.
</details>

<details>
<summary>3. A colleague says the six skills are harmless to leave on the published agent, since users will never ask to build an agent. Why are they wrong?</summary>

Because users do not have to ask to build an agent. A skill fires when a request matches its **description**, and
the descriptions are broad. The router's covers users who ask what to do next, and the skill creator's covers
producing a document in a fixed format, which competes with `qn-write-up` ({{topic:installing}}).

Every description also sits in the catalogue on every turn, so the six cost context even when they never fire.
Stage 7's first step deletes them, and the components panel should show no `copilot-*` row before any publish.
</details>

<details>
<summary>4. Microsoft's testing page says Build edits reach the next turn and you don't need a new conversation. Why does the route still insist on one before testing?</summary>

Because the page lists tools, the model and Memory, not skills. An uploaded skill was observed **not** to reach a
running conversation ({{topic:notrunning}}). At stage 7 you upload the skills the build produced, so the build
conversation cannot see them.

It also carries the whole build's history, which steers every answer. A test in that conversation tests the agent
as it was, under the influence of weeks of design talk. One new chat costs nothing.
</details>

<details>
<summary>5. Your build conversation is lost after stage 4. What do you do, and what do you lose?</summary>

Re-upload `agent-brief.md` in a new chat and tell the router which stages you finished. The brief is the recovery
file, and the other outputs you saved (`tool-plan.md`, the skill packages) are still yours.

What is lost is stage 2's draft. It was only ever in the conversation and never became a file, so expect to redo
it ({{topic:notrunning}}). With no brief at all, start again at stage 1. A brief rebuilt from memory is one nobody
checked.
</details>
