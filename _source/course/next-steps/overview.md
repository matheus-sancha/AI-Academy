## What this module is for

The guided build is the end of what this level teaches. This module is where you find out what stayed with
you. It holds one lesson, {{topic:checkpoint}}: seven tasks, each with a test you run on an agent of your own
and a module to reread if it fails.

It teaches nothing new. Every check is drawn from a module you have already read, and the page after this one
is the next roadmap, where the knowledge that level takes for granted is listed.

## Before you start

The checkpoint assumes the whole core path, and it is most honest after {{module:guided-build}}, once you have
built one agent with the toolchain's help. You also need an agent of your own to sit it against, an
environment you can build in, a second one to publish into, and a colleague willing to read a brief and try a
second account.

Reading the lesson takes about fifteen minutes. Sitting the checkpoint takes a day or two, most of it check 7.

## What you will be able to do

By the end of this module you should be able to:

- say which of the seven capabilities you can show without a guide, and which you can only describe;
- run each check on your own agent rather than on the course's example;
- name the module to reread for each check you fail;
- read Exam AB-620's skills list as a map of what comes after this level, not a second checkpoint.

## The thread through this module

One engineer, just finished with the Technik Production Assistant, sits the checkpoint against a smaller agent
they built the same month: a FAT checklist helper. Its brief has a task that is really an area, its Snowflake
connection runs as the engineer who made it, and it lives in the default solution. Each failure sends them to
one module, and they sit the checkpoint again on the rebuilt helper.

## Self-check

<details>
<summary>1. You finished the guided build, every stage passed its finished-when test and the agent is published. Are you ready to go on?</summary>

Not on that evidence alone. The route carried you: the router handed out each stage's instructions, and each
skill checked its own output. A finished build shows the route works. The checkpoint asks whether you could do
the same work without it, which is what the next level assumes ({{topic:checkpoint}}). The build is still the
best preparation for sitting it.
</details>

<details>
<summary>2. You sit all seven checks against the Production Assistant and pass them in an hour. What does that tell you?</summary>

Mostly that you remember the course. Every example in this level is that agent, so its brief, its triage table
and its solution are things you have read, not things you have produced. Sit the checkpoint again against an
agent of your own, where no worked example tells you what the answer looks like ({{topic:checkpoint}}).
</details>

<details>
<summary>3. Your ten evaluation cases all pass. A colleague in another user group asks the agent about a work order and gets nothing. Which two checks does this touch?</summary>

Checks 5 and 6. On the GitHub Copilot harness an evaluation runs only as the signed-in user, so all ten cases
passed with your identity ({{topic:testidentity}}). If the tool's connection runs as the end user, your
colleague needs a connection of their own, and sharing the agent did not give them one. Or they have one, and
their own permissions do not reach the data ({{topic:connauth}}).

So the report of that run should have said which account it ran as, and the identity sentence from check 5
should have predicted what a second account would see.
</details>

<details>
<summary>4. You can explain exactly how to move an agent from the default solution into a custom one, but you have never done it. Do you pass check 7?</summary>

No. The check is the publish, not the explanation: export, import into an environment you did not build in,
bind the connection references and publish, then see a colleague get an answer ({{topic:solutions}}).

If your agent is on the GitHub Copilot harness there is a second reason to do it rather than describe it.
Solutions are documented only for the standard harness, so whether such an agent travels in one is something
you find out by trying.
</details>

<details>
<summary>5. Exam AB-620's study guide lists Microsoft Foundry, the Agent2Agent protocol and Power Platform Pipelines. You have touched none of them. Did this level leave a gap?</summary>

No. The guide describes a professional developer or advanced builder, and those items sit beyond this level.
The part that overlaps is *Test and manage agents*: test sets, evaluation methods, reviewing results, solutions
and environment variables, which this level does teach ({{module:testing-and-evaluation}},
{{module:publishing-and-environments}}). Read the rest as a map of what comes next.
</details>
