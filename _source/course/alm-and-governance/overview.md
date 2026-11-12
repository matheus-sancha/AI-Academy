## What this module is for

Every module before this one is about building an agent that behaves. This one is about the part that
happens afterwards and mostly to other people: moving the agent between environments, keeping its source,
deciding what may reach production, and living under an administrator's controls and a monthly bill. The
first four lessons are the route to production for the two halves of an agent. A Power Platform solution
moves by pipeline, with Git integration for its source ({{topic:solutionsdeep}}, {{topic:pipelines}},
{{topic:gitintegration}}). Code moves by workflows you write, behind a gate you wrote too ({{topic:cicd}}).
The last four are the controls that apply once it is there: managed environments, Agent 365, the Copilot
Agent Kit and the cost meters ({{topic:managedenvs}}, {{topic:agent365}}, {{topic:agentkit}}, {{topic:costs}}).

Two ideas run through it. The first half's is **promote the artifact that was tested, and know what the
package does not carry.** A solution carries the definition of an environment variable but not its value, and
leaves Application Insights, authentication, channels and sharing behind. No documented action runs an
agent's evaluation, so the gate that blocks a release is yours. The second half's is **governance is a set of
switches someone else holds.** An administrator can block an agent, a pipeline can refuse a target, a hard stop
can turn the agent off and a licence can lock users out. None of those is a bug, and each one has a failure
mode that looks like one.

Expect the pages to describe features and be quiet about agents. The pipelines and Git pages never mention
one, the managed-environment overview names 21 features and describes none, and the Copilot Agent Kit's pages
do not say whether it can test an agent on the GitHub Copilot harness. The lessons mark each gap as
*Not yet verified* rather than guess, and the capstone, which has never run live, cannot settle them.

## Before you start

From Intermediate, {{topic:solutions}} and {{topic:envs}} are what a solution and an environment are, and
{{topic:connrefs}} is why a connection reference needs a value in the target. {{topic:licensing}} is what an
environment is billed on, and {{topic:testsets}} is the evaluation set that a gate should run.

From this level, {{topic:evalharness}} and {{topic:stageship}} supply the gate and the release the capstone
uses, and {{topic:foundryagents}} explains why a hosted agent has no canary. {{topic:agentid}} is the identity
that {{topic:agent365}} governs, {{topic:tracing}} is where a per-conversation cost figure would come from, and
{{topic:dlpdesign}} is the data-policy half of the same governance story.

Nothing here needs to be run. The capstone, public and tested offline only ({{module:capstone-build}}), has a
gate workflow and a release workflow, and no Power Platform environment.

Allow about two and a half hours. {{topic:agentkit}} is optional on a first pass.

## What you will be able to do

By the end of this module you should be able to:

- list what a solution carries and what it leaves for a checklist, and say how an environment variable's
  definition and value travel;
- design a pipeline for a low-code agent, choosing the deploying identity first, and say what it will not
  promote;
- keep a solution's source in Git, review it in a pull request and pull accepted changes into other
  development environments;
- write a gate for a pro-code release that blocks on regression, and keep a change to its baseline in its own
  reviewed pull request;
- decide which environments to manage and what that costs in licences, and say what the developer
  environment deadlines change;
- register and instrument a pro-code agent so Agent 365 can see it, and say what an administrator can do to it;
- say which meter an agent will hit, what happens when it does, and where a cost figure comes from.

## The thread through this module

{{topic:solutionsdeep}} comes first because everything else moves a solution and must know what is in it.
{{topic:pipelines}} automates the move, with approvals and a deploying identity chosen before the first import.
{{topic:gitintegration}} is the other direction: source files, pull requests and a way to keep several
developers' environments in step. {{topic:cicd}} adds what none of them does, the evaluation gate, and shows
where the capstone's lives.

{{topic:managedenvs}} turns from the route to the places on it. A pipeline's targets must be managed, a
developer environment must be too, and the switch brings licence enforcement with it. {{topic:agent365}} goes
a level up, to the agent as an object an administrator can govern wherever it was built. {{topic:agentkit}} is
the one tool in the module that tests an agent and documents a gate in a pipeline, with a sign-in that
changes production. {{topic:costs}} closes with the bill, because every limit in it is a switch of the second
kind, and because the pages that explain them give no cost per conversation.

## Self-check

<details>
<summary>1. A solution imports cleanly into *Technik Agents*, but nobody can open the Production Assistant and its traces never reach Application Insights. What did the deployment leave behind, and where is the list?</summary>

Parts of a Copilot Studio agent are not solution-aware: Application Insights settings, authentication,
channels and sharing. Each needs a step by hand after the import, and the deployment's checklist is the other
half of the release ({{topic:solutionsdeep}}). Check the environment variables too. A definition travels with the
solution, and the value belongs to the target, so an import without a current value asks for one.

The pipelines do not do these steps, and neither the pipelines nor the Git pages mention agents
({{topic:pipelines}}, {{topic:gitintegration}}).
</details>

<details>
<summary>2. A deployment into *Technik Agents Test* is refused, and in January an engineer's developer environment has been deleted. Are those two problems or one?</summary>

One cause, two routes. A pipeline's target environments must be managed and have a Dataverse database. Microsoft also
deprecates unmanaged developer environments: creation ends on 15 November 2026, suspension starts on
15 December and deletion on 15 January 2027. Enabling managed environments fixes both, and it brings licences:
from February 2027 a user without a qualifying licence cannot open apps there ({{topic:managedenvs}}).

The pages do not say what that block does to a person who only talks to an agent. That is worth asking before
you enable it.
</details>

<details>
<summary>3. The capstone's `Evals` workflow and the Copilot Agent Kit both claim to test before a release. Which one gates the Production Assistant, and which gates the capstone's agent?</summary>

No Power Platform action runs an agent evaluation, so the gate for the capstone is a workflow you write:
`Evals` runs on any change to behaviour, including the workflow files, blocks on a regression against
`evals/baseline.json`, and is made binding by a repository rule no file can contain ({{topic:cicd}}). The Foundry
action after deployment only reports.

For the Production Assistant, the kit is the one documented route: a pre-deployment step in a pipeline that
runs its tests and decides whether to proceed. It states no pass mark, and its sign-in changes the agent's
production authentication ({{topic:agentkit}}).
</details>

<details>
<summary>4. A pro-code Agent Framework rebuild is in Teams, but the administrator cannot find it in the registry and Defender shows no spans from it. What do you check?</summary>

Registration and telemetry are separate steps. Registering creates a blueprint and an agent identity in Entra and
gives catalogue visibility. Instrumentation adds the telemetry, and it needs a root `invoke_agent` span. A
licensed user must also exist in the tenant, or the spans are dropped silently. A Copilot Studio agent would
have joined automatically in an onboarded tenant, and a pro-code one does not ({{topic:agent365}}).

What the administrator can then do to it includes blocking it, so plan what users see when that happens.
</details>

<details>
<summary>5. On the 20th the Production Assistant stops answering. A week earlier a flow it calls began failing while the agent still replied. Name the two meters, and say how you find the cost of one conversation.</summary>

The first is the environment's credits: with none left, new agent flow runs are blocked and the parent
agent keeps working. The second is the per-agent monthly limit, whose hard stop turns the agent off. A
limit does not stop its flows, it is not applied instantly, and its notifications go to administrators, not
to the owner ({{topic:costs}}).

Copilot Studio's reports are by environment, agent and user, with no single conversation and no token counts.
For a code agent the trace records tokens ({{topic:tracing}}), and you multiply by the model's price.
</details>
