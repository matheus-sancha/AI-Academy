## TL;DR

Pipelines are Power Platform's built-in way to promote a solution. An administrator defines the stages once
in a **host** environment. A maker presses **Deploy** from an unmanaged solution in development, and the
platform exports it once, checks it against the target, asks for connections and variable values up front,
and imports that same sealed artifact stage by stage. What it moves is a solution: not Dataverse data, and
not code. It is the simplest route Microsoft documents and not the only one. A pro-code team uses it for the
low-code half of an agent and builds the rest of the release itself ({{topic:cicd}}).

## Why it matters

Promoting by hand means exporting, downloading, importing, remaking connections and filling in a settings
file, and each step is a place to import the wrong file. A manual process also cannot show that what reached
production is what passed test. Pipelines can, and that is the reason to prefer them to a hand-written
workflow. Microsoft's own advice is to use pipelines for core deployment and extend them with other CI/CD
tools where needed, which keeps those workflows smaller.

## How it works

### Three parts

**The host.** An environment that holds the pipeline definitions, the run history and a stored copy of every
artifact. It should be a production environment, though it need not be managed. It cannot be the same
environment as a development one. An environment belongs to one host, and can sit in several pipelines of
that host. Pipelines cannot deploy to a different tenant.

**The pipeline.** It links one or more development environments to an ordered list of stages, each with a
target environment. A stage names its previous stage, which is how the order is enforced.

**The run.** A maker starts it from an *unmanaged* solution in a linked development environment. It cannot
be started from the default solution, from a managed solution or from a target.

<!-- volatile verified=2026-11 -->
Setup is done in the host's **Deployment Pipeline Configuration** app. The second link walks it through:
create the pipeline, tick the option that allows redeploying older versions, link the development
environment, then add a test stage and a production stage whose **Previous Deployment Stage** is the test
one.
<!-- /volatile -->

### What the platform guarantees

- **One artifact.** The solution is exported when the maker selects Deploy and is not exported again for
  later stages. It cannot be altered, so a change cannot skip QA or an approval.
- **Checked before it moves.** Missing dependencies are found before the import, and connections and
  variable values are supplied and validated first ({{topic:solutionsdeep}}).
- **A stored copy.** Managed and unmanaged versions are kept in the host for every deployment.
- **Approvals.** Delegated deployments route a stage through an approver.
- **An owner.** Deployed objects belong to the deploying identity: the requesting maker, or for a delegated
  deployment the service principal or user it names. A connection reference's owner cannot be transferred
  later ({{topic:connrefs}}), so choose that identity before the first import.
- **Rollback, if enabled.** With the older-versions setting on, a previous version can be redeployed from
  run history. Without it only higher versions go in.

### What it does not do

| Limit | What the page says |
|---|---|
| Data | Solutions and pipelines do not carry Dataverse table data |
| Import mode | Fixed at upgrade without overwriting customisations; update is not offered |
| Batch | One solution per deployment |
| Developers | One development environment per solution, so parallel work goes through Git ({{topic:gitintegration}}) |
| Unsaved work | Unmanaged customisations are not published before export, so publish as you save |
| Connection references | One with no value in the solution or target cannot be updated during a deployment |
| Unmanaged solutions | Cannot be deployed: managed only |

<!-- volatile verified=2026-11 -->
Every environment except the developer ones and the host must be a **managed environment**, and managed
environments need licences with premium use rights ({{topic:managedenvs}}). Since October 2026 the admin
deployment page warns when a pipeline targets an unmanaged environment. Admins then have 30 days to approve
enabling it, and one 30-day extension, before deployments to it are blocked.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
The pipelines overview never mentions agents or Copilot Studio. The Copilot Studio guidance lists the items
that are not solution-aware and says they need steps afterwards. Neither page says whether a pipeline run
reminds you of them, or whether an agent's settings are validated before deployment as a flow's
connections are. Run one deployment to a test environment and look.
<!-- /unknown -->

## In practice at Technik

Technik's *Production Assistant* promotes through one pipeline.

| Part | Setting |
|---|---|
| Host | *Technik Pipelines Host*, a production environment used for nothing else |
| Development | Each engineer's own developer environment, linked to the pipeline |
| Stage 1 | *Technik Agents Test*, a sandbox, no approval |
| Stage 2 | *Technik Agents*, with a delegated deployment approved by a manufacturing engineer other than the one deploying |
| Deploying identity | A service principal, so the owner of the connection references is not a person who may leave |
| Licensing | The test and production environments are managed |

Two things in the solution are not simple. The Teamcenter server is fronted by a custom connector, and
{{topic:connrefs}} found that a custom connector must be imported in a separate solution before the
flows that use it. A pipeline deploys one solution at a time, so the connector solution is a deployment of
its own, run first. The pages do not say whether a single run can sequence two solutions.

The second is what the pipeline never sees. The capstone's agent and server are code. They ship through the
release workflow in {{topic:stageship}}, and no pipeline here deploys them. A release of the low-code
assistant and a release of the server behind it are two events, and someone has to decide which goes first.

Technik's one manual rule: nothing is promoted to production until the evaluation set from
{{topic:testsets}} has been run in *Technik Agents Test* by hand, because no pipeline stage runs it.

## Design guidance

- **Pick the deploying identity first**, and make it a service principal where a person might leave.
- **Use one pipeline per solution**, so run information stays in one place.
- **Treat the host as infrastructure**: a production environment used for nothing else.
- **Turn on older-version redeployment** before you need it, not after a bad release.
- **Deploy a custom connector's solution before the agent's**, as its own run.
- **Publish objects as you save them.** The pipeline will not publish unmanaged customisations for you.
- **Run the evaluation set yourself before the production stage**, since no stage runs it.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The pipeline does not appear | Run from a managed or default solution, or the environment is not linked as development | Open the unmanaged solution in a linked development environment |
| A change is missing after deployment | It was saved but not published | Publish individual objects as you save |
| A deployment to test is blocked | The target is not a managed environment | Enable managed environments for it |
| A connection reference cannot be updated | It has no value in the solution or the target | Give it a value in the target first |
| Deployed objects belong to a departed maker | A standard deployment is owned by the requester | Use a delegated service principal |
| Rollback offers only newer versions | Older-version redeployment was never enabled | Enable it in the pipeline's settings |

## Key terms

**Pipeline**: an ordered path of stages that promotes one solution from development to production.

**Host**: the environment that stores pipeline definitions, history and artifacts.

**Stage**: one target environment in a pipeline, with a named previous stage.

**Delegated deployment**: a deployment run under another identity, with an approval step.

**Managed environment**: an environment with governance features turned on, required for pipeline targets.
