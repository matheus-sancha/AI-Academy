## TL;DR

A **managed environment** is an ordinary environment with a set of premium governance features switched on and
licences enforced. Any environment type can be managed. Three things make it an engineer's concern. A pipeline
may deploy only to managed target environments. Developer environments can no longer stay unmanaged: creation
of new ones ends on 15 November 2026, suspension starts on 15 December and deletion on 15 January 2027. And
from February 2027 a user without the right licence is blocked from opening apps there. Nothing on the overview
page mentions an agent, so the work here is to know what the switch costs and what it is for, not what it adds
to your agent.

## Why it matters

The first sign is usually a blocked deployment: a pipeline run that worked into the sandbox is refused at the
next stage, because the target is not managed ({{topic:pipelines}}). The second is a developer environment
that disappears from a maker's list.

The third arrives as a bill. Managed environments are included as an entitlement with standalone Power Apps,
Power Automate, Copilot Studio, Power Pages and Dynamics 365 licences, and then they enforce those licences.
Turning one on is a licensing decision too.

## How it works

### What the switch turns on

<!-- volatile verified=2026-11 -->
Microsoft calls managed environments "a suite of premium capabilities" for managing the platform at scale, and
its overview names 21 of them, adding that the list "encompasses, but isn't limited to" these. The page names
them and describes none. Grouped by what they touch, which is this lesson's grouping and not the page's:

| Touches | Named features |
|---|---|
| Makers | Limit sharing, maker welcome content, environment groups, default environment routing |
| Delivery | Pipelines in Power Platform, solution checker, administer the catalog |
| Data and network | Data policies, data policies for desktop flow, IP Firewall, IP cookie binding, virtual network support, customer-managed key, Lockbox, extended backup, masking rules |
| Insight | Weekly usage insights, export data to Application Insights |
| Apps | Control which apps are allowed, conditional access on individual apps (preview), app descriptions with Copilot (preview) |
<!-- /volatile -->

<!-- unknown since=2026-11 -->
Not one of the 21 names mentions an agent. Whether sharing limits, solution checker or usage insights act on a
Copilot Studio agent is not stated by the overview, and {{topic:agent365}}'s Copilot Studio page does not use
the term "managed environment" at all. Check each feature's page before assuming it covers agents.
<!-- /unknown -->

### Turning it on

<!-- volatile verified=2026-11 -->
Enabling or editing the property needs the Power Platform Administrator or Dynamics 365 Administrator role. The
Delegated Admin and Environment Admin roles "can't change" it. In the Power Platform admin center, choose
**Manage** > **Environments**, open the ellipsis beside the environment and choose **Enable Managed
Environments**, or **Edit Managed Environments** if it is already managed. Production, sandbox and trial
environments need a Dataverse database to be managed. Developer environments do not.

The property must match in the source and destination of a copy or restore. Disabling is documented through
PowerShell only, by setting the governance configuration's protection level back to basic, and the page warns
you to be sure none of the capabilities is in use first.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
Devaney's environment guide shows a **Make This A Managed Environment** option in the New environment
dialog. Microsoft's enabling page describes only the ellipsis route on an existing environment, so whether the
dialog option is still there is unchecked.
<!-- /unknown -->

### Who needs a licence

<!-- volatile verified=2026-11 -->
Every user who runs an app in a managed environment needs Power Apps Premium, Power Automate Premium or a
Dynamics 365 Enterprise licence with premium Power Apps rights. The same set applies to a user who runs a cloud
flow. A user who does both needs only one. Flows triggered within apps, or in the context of agents, are covered
by the Power Apps or Copilot Studio standalone licence. Capacity works as an alternative: allocate per-app or
per-flow plans to the environment itself.

The timeline on Microsoft's licensing page: admin notifications began in March 2026, in-app notices for users
in June, and from **February 2027** a user without a qualifying licence cannot open apps in the environment.
Apps are not removed, and access resumes when a licence is detected.
<!-- /volatile -->

Devaney's guide says every user in a managed environment needs a premium licence. Microsoft's page limits it to
users who run apps or cloud flows there.

<!-- unknown since=2026-11 -->
The February 2027 block is described for apps. The licensing page does not say what happens to a person who
talks to an agent in an environment where they hold no Power Apps licence, or to a flow that the agent calls.
Ask before enabling.
<!-- /unknown -->

### Pipelines and developer environments

<!-- volatile verified=2026-11 -->
The platform host page requires that "all target environments" in a pipeline are managed, with a Dataverse
database. The default environment, Dataverse for Teams environments and environments without Dataverse cannot
be targets. Devaney's guide builds exactly that layout: a sandbox for development left unmanaged, a sandbox for
test and a production environment, both managed.

The Developer type changes this. Microsoft's deprecation page says unmanaged developer environments are
deprecated, that a developer environment now exists only as a managed one, one per user, and that a user needs
a premium licence to run apps and flows in it. Export any solution you need before suspension begins.
<!-- /volatile -->

{{topic:pipelines}} records the admin deployment page's 30-day warning for unmanaged targets. The pages this
lesson reads give no date for it.

## In practice at Technik

| Environment | Type | Managed | Reason |
|---|---|---|---|
| Each engineer's own | Developer | Yes | An unmanaged developer environment is suspended from 15 December 2026 |
| *Technik Pipelines Host* | Production | Not required by the page | It runs pipelines and nothing else |
| *Technik Agents Test* | Sandbox | Yes | A pipeline target |
| *Technik Agents* | Production | Yes | A pipeline target |

Read the licence question first. The Production Assistant's users reach it through Teams, and the Copilot Studio
licence is an entitlement for managed environments. The page covers flows in the context of agents. A
manufacturing engineer who also opens a canvas app in *Technik Agents* is a Power Apps user and needs a premium
licence.

The capstone has no Power Platform environment. Its server and agent are code on Container Apps and Foundry, so
nothing in this lesson governs it. The environment that does matter is the one holding the custom connector
that fronts the server ({{topic:mcpcs}}).

## Design guidance

- **Manage every pipeline target**, and decide the licence plan before the first deployment.
- **Keep developer environments managed**, since the unmanaged kind is going away.
- **Count licences by who runs apps and cloud flows**, not by everyone with access.
- **Use the right role to change the property**, a Power Platform or Dynamics 365 administrator.
- **Check each feature's page** before relying on it for an agent.
- **Check what is in use before disabling**, because features stop with it.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A deployment is refused at a stage | The target is not a managed environment | Enable it, with a Dataverse database |
| A maker's developer environment vanishes | It was unmanaged past the deprecation dates | Enable before 15 December 2026, or export first |
| An administrator cannot find the enable option | The role is Delegated Admin or Environment Admin | Use a Power Platform or Dynamics 365 administrator |
| Copy or restore fails | The property differs between source and destination | Match them first |
| Users see "You need a Power Apps license to use this app" | No qualifying licence in a managed environment | Assign one, or request it through the admin center |
| A feature stopped working after disabling | It depended on the managed property | Check what is in use before turning it off |

## Key terms

**Managed environment**: an environment with premium governance features enabled and licences enforced.

**Target environment**: the environment a pipeline deploys into.

**Dataverse database**: the data store a production, sandbox or trial environment needs before it can be managed.

**Premium licence**: Power Apps Premium, Power Automate Premium or a qualifying Dynamics 365 Enterprise licence.
