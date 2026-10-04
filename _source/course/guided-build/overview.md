## What this module is for

Everything before this module taught what goes into an agent. This one is where you build one, end to end,
using the six-skill toolchain against a task of your own. The build itself does not happen on these pages. It
happens in a conversation with the router, `copilot-studio-agent-creator`, which hands you each stage's
instructions from the release you installed. This course is written against {{skills-version}}. One copy of the
route, kept where it is versioned, cannot drift from what you downloaded.

So these three lessons are what you read around the build: what to have before it starts, the map of the
route, and what to do when a stage stalls. Read all three before stage 1. Come back to the map when you lose
your place.

## Before you start

{{module:the-six-skills}} is essential. It covers which skill owns which stage, how to install the six and
take them off again, and why the route keeps one conversation and still needs a new chat before testing.
This module assumes all of it.

Beyond that, the route assumes the whole core path of this level, a module per stage:
{{module:designing-an-agent}} for the interview, {{module:writing-instructions}} for both instruction passes,
{{module:tools-connectors-mcp}} for the tool plan, {{module:agent-skills}} for the skills you package,
{{module:testing-and-evaluation}} for the test set, and {{module:publishing-and-environments}} for the last
step. You do not need to have mastered them. You need to be able to judge what each stage hands back.

Reading the module takes about 45 minutes. The build takes days. It needs a tenant, a developer environment,
Copilot Credits and, most of all, a real task with someone who will use the agent.

## What you will be able to do

By the end of this module you should be able to:

- say what you need before stage 1, and why an idea is not enough to start with;
- spot the licence and credit gaps that only show at the end of the build;
- name what each stage leaves you holding, and the test that says it is finished;
- name the module of this level that taught what each stage assumes;
- work stage 7's checklist in order, including the knowledge step it leaves out;
- tell which stage you reached from the files you hold;
- tell a missing connector from a blocked one, and send each to the right person;
- judge a stage's output by its shape rather than by resemblance to the course's example.

## The thread through this module

One build, the Technik Production Assistant, from the morning before stage 1 to its first published answer.

{{topic:whatyouneed}} lays out the build's prerequisites: an agent on the right harness, a user licence rather
than a trial, an administrator who knows where the credits come from, and a folder of real artifacts with a
supervisor and a quality engineer booked for the interview. {{topic:theroute}} follows the files as they arrive,
adds the two SharePoint knowledge sources the stage 7 checklist leaves out, and recovers the build when the
conversation is lost after stage 4. {{topic:whenitstalls}} finds the Snowflake connector blocked by a data
policy at stage 3, carries on through stages 4 to 6 while the administrator decides, and shows a shift-handover
agent whose brief looks nothing like Technik's and is finished anyway.

## Self-check

<details>
<summary>1. You have a Copilot Studio trial licence, six skills installed and a well-defined task. What will stop you, and when?</summary>

The trial licence, at the very end. Microsoft documents that a trial lets you create and test agents but not
publish them, so the build runs through every stage and fails at stage 7's last step ({{topic:whatyouneed}}).
That limit is stated on the standard harness's licensing page and unverified for the GitHub Copilot harness,
which is the reason to ask your administrator before stage 1 rather than after.
</details>

<details>
<summary>2. You return to a build after two weeks. Your folder holds agent-brief.md and tool-plan.md, and the build conversation is gone. Where are you, and what do you redo?</summary>

Stage 3 is the last one finished, so stage 4 is next, or stage 5 if the plan names no skills. Re-upload the
brief in a new chat and tell the router that stages 1 and 3 are done ({{topic:theroute}}).

You redo stage 2. Its draft was only ever in the lost conversation, and stage 5 revises that draft, so it has
to exist again first.
</details>

<details>
<summary>3. You finish stage 7's checklist exactly as given, and the agent answers procedure questions from general knowledge, ignoring its knowledge routing. What went wrong?</summary>

The checklist at {{skills-version}} has no step for knowledge sources, and no earlier stage adds them. The brief
named the sources and `<knowledge_routing>` routes to them, but nothing put them on the agent
({{topic:theroute}}). Add them in **Build** > **Knowledge** and open a new chat. Then run the evaluation again,
because the earlier run graded an agent with no knowledge.
</details>

<details>
<summary>4. At stage 3 the Snowflake connector appears disabled in Add a tool. Do you go back to the tool finder?</summary>

No. Disabled with a reason in the hover text means a data policy is blocking it, and that is a policy question
for your administrator. Nothing about the design is wrong ({{topic:whenitstalls}}). Go back to the tool finder
only if the connector does not appear at all.

Meanwhile the route continues. Stages 4 to 6 only need the tool named, not added, so only stage 7 waits for the
policy.
</details>

<details>
<summary>5. Your brief has two tasks, no tools and no knowledge, and the course's example has seven capability areas. Should you redo the interview?</summary>

Not on that evidence. A stage is finished when its output passes the stage's test, not when it resembles the
example ({{topic:theroute}}). If every slot passed its acceptance test and you confirmed the summary, the brief
is finished. Stages 3 and 4 are skipped, and stage 5 just confirms the draft ({{topic:whenitstalls}}).

Redo it if a slot only passed because you accepted a vague answer. That is a failed test, not a small agent.
</details>
