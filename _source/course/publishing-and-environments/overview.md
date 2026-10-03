## What this module is for

Everything so far happened in one place, as one person. This module is about the move out of that: from your
developer environment to a test environment and production, from the preview pane to Teams and Microsoft
Copilot, and from you to the people the agent was built for.

The recurring theme is *it worked for me*. Each lesson finds a different reason an agent that passed every test
can still fail its first real user: a connection that didn't cross environments, a version that hadn't reached
the user's session yet, a channel that renders differently, a knowledge source the user can't open. None of them
is a bug in the agent. They are differences between where it was tested and where it runs, and the module's
job is to make those differences deliberate.

## Before you start

You want {{topic:devenv}}, because this module starts from the developer environment it describes, and
{{topic:connauth}}, because connections are the first thing that fails to travel. {{topic:agentauth}} decides
which channels and sharing options you have, and {{topic:dlp}} explains why a channel or a publish can be
blocked. {{module:testing-and-evaluation}} comes first in the path: publishing is what happens *after* the
evaluation passes, and analytics is where the evaluation set's next cases come from.

Some of this needs an administrator: creating test and production environments, approving an agent for the
organisation's app store, granting transcript access. The lessons say where. Allow about 90 minutes.

## What you will be able to do

By the end of this module you should be able to:

- explain what an environment contains, and lay out development, test and production environments for an agent;
- package an agent in a custom solution with your own publisher, and say why that has to happen on day one;
- publish an agent, write its description as user-facing copy, and know when users see a new version;
- choose channels for an agent, and predict what each will change about authentication and rendering;
- share an agent with security groups, and name the three things sharing does not share;
- read the Monitor tab and turn what it shows into the next fix and the next test cases.

## The thread through this module

One agent, the Technik Production Assistant, on its way to its users.

{{topic:envs}} lays out its three environments and finds, in test, that the agent's Snowflake role was missing a
grant the engineer's own login had hidden. {{topic:solutions}} creates a publisher and a custom solution before
the agent exists, and shows a second agent built without one. {{topic:publish}} rewrites a description that told
a planner nothing, and meets a fix that hadn't reached an open conversation. {{topic:channels}} publishes to
Teams and Microsoft Copilot only, simplifies the QN list for Teams, and keeps the agent out of the shift team's
channel, where SharePoint knowledge can't work. {{topic:share}} shares with three security groups and watches a
planner get *"nothing found"* for a document the engineer could see. {{topic:analytics}} finds lead-time
questions landing on the efficiency tool, in transcripts no evaluation case had predicted.

## Self-check

<details>
<summary>1. An engineer built an agent in the tenant's default environment because "everyone already has access there". What is wrong with that, and what would you suggest?</summary>

The default environment is shared by every licensed user, all of whom are makers there. Microsoft describes it as
for experimentation, with no backup guarantees, and says it shouldn't be used for production workloads. Anyone
can change things next to the agent, and nothing there is meant to be relied on.

Build in a developer environment, test in a sandbox shaped like production, and deploy to a production
environment, moving the agent as a solution each time ({{topic:envs}}, {{topic:solutions}}).
</details>

<details>
<summary>2. Three months in, an agent built in the default solution needs to reach production. Why is that harder than it sounds?</summary>

The default solution isn't exported. The agent has to be put into a custom solution after the fact, with every
component it depends on found and added by hand: flows, connection references, environment variables. And
anything already created carries the default publisher's prefix, which can't be changed once components exist.
Creating the publisher and a custom solution, and setting it as preferred before building, avoids all of it
({{topic:solutions}}).
</details>

<details>
<summary>3. You publish a fix and ask the agent again in Teams, in the conversation you already had open. The old behaviour comes back. Is the fix broken?</summary>

Probably not. A published change reaches users only in a new session, so a conversation that started before the
publish can keep the old version. On the standard harness, *start over* in Teams starts a new session at once;
otherwise it can take up to an hour. Test every publish in a new conversation before concluding anything
({{topic:publish}}).
</details>

<details>
<summary>4. A supervisor wants the Production Assistant in the shift team's Teams channel so everyone sees the answers. What do you tell them?</summary>

Work order answers will work there, but document answers won't. In Teams group chats and channels, agents can't
use knowledge sources that need the user's own sign-in, such as SharePoint. Microsoft built it that way to
prevent unintended data exposure, so those agents are supported only in 1:1 chats. Either keep the agent in 1:1
chats, or design a separate channel agent that doesn't depend on SharePoint, and record the decision in the brief
({{topic:channels}}).
</details>

<details>
<summary>5. The agent answers document questions perfectly for you and says "nothing in my sources covers that" to a planner. Nothing has changed in the agent. Where do you look, and in what order?</summary>

At what sharing doesn't share. First knowledge permissions: SharePoint answers each user from what they can open,
so check the planner's access to the site. Then connections: a tool connection tied to each user can fail for
them. Then, on the standard harness, flows, which sharing doesn't share and the test panel runs anyway. The
abstention is the agent doing the right thing; the fix is access, or a deliberate shared identity for data
everyone may see ({{topic:share}}).
</details>
