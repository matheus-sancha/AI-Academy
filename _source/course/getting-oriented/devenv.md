## TL;DR

Build in your own Power Platform **developer environment** — never the tenant's default environment,
and never production. It is free, it is where premium and custom connectors behave predictably, and it
has limits you want to know before they surprise you: a 2 GB database, 750 flow runs a month, the
tightest generative-AI rate limit of any tier, no AI Builder, and automatic disablement after 30 days
of inactivity. Pair it with Copilot Studio access, VS Code with GitHub Copilot, and a Snowflake role
of your own — and give the agent a separate, read-only role from the first day.

## Why it matters

The tenant's default environment is shared with everyone in the organisation and is explicitly not
where premium and custom connectors belong. Production is where your half-finished experiment meets
real users. A developer environment is the answer to both, and it is free, so there is no reason to
work anywhere else.

The subtler point is that a developer environment is **not a smaller production environment**. Some
things are reduced — storage, flow runs, throughput — but other things are simply *absent*, and no
amount of capacity fixes them. Knowing which is which saves you from debugging an entitlement as
though it were a bug.

## How it works

### Getting one

Anyone with a work or school account backed by Microsoft Entra ID can sign up for the **Power Apps
Developer Plan**; personal accounts cannot. Signing up provisions one developer environment
automatically, named after you, and you can create up to **three** in the Power Platform admin center.
Provisioning takes a couple of minutes, and progress is visible there.

The licence is a *viral* or *internal* licence, which means the tenant has to permit it. If sign-up is
blocked, that is a policy decision rather than an error — an administrator can allow the consent plan,
or block developer-environment creation outright. If yours is blocked, the documented alternatives are
to ask your administrator or to use a separate test tenant.

### What you get, and what you do not

This is the table worth reading twice, because the right-hand column is where the surprises live.

<!-- volatile verified=2026-09 -->
| Included | Not included |
|---|---|
| Premium connectors | AI Builder use rights |
| Custom connectors | Power Automate RPA use rights |
| On-premises data gateway | Dataverse dataflows |
| Dataverse, and your own data schema | Dynamics 365 apps |
| Cloud flows | Managed-environment use rights |
| Sharing with colleagues for development and testing | Production use of any kind |

| Capacity | Limit |
|---|---|
| Database size | 2 GB |
| Flow runs per month | 750 |
| Generative AI messages | 10 per minute, 200 per hour |
<!-- /volatile -->

Capacity add-ons cannot be applied to a developer environment — if you need more, you need a plan that
supports production. The flip side is that the environment's entitlements do not count against your
company's overall quota, so nobody is paying for your experiments.

Two behaviours follow from "not for production" and both are visible: apps display a banner reminding
you where they are running, and **an environment inactive for 30 days is automatically disabled**. A
long holiday is enough.

### The rest of the toolchain

The environment is one of four things you want before the guided build:

1. **A developer environment**, as above.
2. **Copilot Studio access** — a licence or the authors role, and enough credits to spend
   ({{topic:licensing}}).
3. **VS Code with GitHub Copilot.** Not needed to build in Copilot Studio, but it is where the same
   Agent Skills format runs ({{topic:openformat}}), and it is Advanced's home
   ({{module:developer-tooling}}).
4. **Snowflake access through your own development role** — for exploring the data model, writing
   queries and checking your assumptions about the tables.

### The role rule

Your Snowflake development role is *yours*. The agent gets a different one: a dedicated, least
privilege, read-only role, and so does every connector and flow you build.

This is not tidiness. Everything an agent reads is potentially attacker-controlled — a quality
notification description is free text typed by anyone on the shop floor — and text the agent reads can
try to reach the tools it holds. If the only role available to the agent cannot write, the worst case
is bounded by the platform instead of by a sentence in your instructions. {{topic:connauth}} covers who
a connection runs as, {{topic:sfroles}} covers how the roles are built, and
{{module:safety-and-moderation}} shows the attempt being made.

### Getting work out again

Anything you want to move to a test or production environment travels in a **solution**, so create
every agent inside a custom solution from day one. Retrofitting one later is real work, and
{{topic:solutions}} explains why.

## In practice at Technik

The engineer building the Production Assistant works in their own developer environment. They explore
`SAP_WORK_ORDERS` and the `TC_*` tables in Snowflake using their own role, because understanding the
data means querying it freely. The agent they build reads the same data as `TECHNIK_AGENT_RO` on
`TECHNIK_AGENT_WH`, and never with the engineer's role.

Two limits are worth predicting for this build. The 2 GB Dataverse database never bites, because
Technik's data lives in Snowflake and the agent queries it live rather than importing it. The 750
monthly flow runs *do* bite, once the document-revision approval flow is being tested — a flow under
development is run far more often than a flow in production, and each test is a run. And AI Builder is
absent outright, so the supplier-certificate extraction in {{module:automation-and-workflows}} needs a
separate AI Builder trial rather than a bigger environment.

## Design guidance

- **One environment per engineer.** Never the default, never production, and never a colleague's.
- **Ask what is absent, not just what is smaller.** Capacity you can plan around; a missing
  entitlement you cannot.
- **Give the agent its own least-privilege identity on day one.** Retrofitting an identity means
  re-testing every tool.
- **Put everything in a custom solution immediately.**
- **Touch the environment at least monthly**, or it will be disabled for you.
- **Treat a blocked sign-up as a policy question.** The answer lives with your administrator, not in
  the documentation.
- **Do not benchmark anything here.** Throughput in a developer environment says nothing about
  production.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A premium or custom connector is missing or behaves oddly | Building in the tenant's default environment | Build in your developer environment instead |
| Developer Plan sign-up is refused | The tenant does not permit viral or internal licences, or environment creation is restricted | Ask your administrator to allow it, or use a test tenant |
| The environment has vanished | Inactive for 30 days, so it was automatically disabled | Keep it in use; recreate if necessary |
| An AI Builder step cannot be completed | AI Builder use rights are not part of the Developer Plan | Start an AI Builder trial |
| Flows stopped running partway through the month | The 750 flow runs per month were consumed by testing | Space the tests, or move to a plan that supports production |
| A long evaluation run throttles | 200 generative AI requests per hour in this tier | Expected; space the runs ({{topic:licensing}}) |
| The agent works only for you | Its connection authenticates as you | Decide who it runs as ({{topic:connauth}}) |
| The agent cannot be moved to a test environment | It was never in a solution | Create it inside one from the start ({{topic:solutions}}) |
| Colleagues need a licence to run your app here | Managed-environment use rights are not included | Move the work to an environment that supports it |

## Key terms

**Developer environment** — a free Power Platform environment for development and test use only, with
its own capacity limits and no production rights.

**Default environment** — the environment every tenant gets, shared by all users; not where premium
connectors or agents belong.

**Power Apps Developer Plan** — the free plan that provisions a developer environment; requires a work
or school account.

**Viral or internal licence** — a licence a user can assign themselves if the tenant permits it; an
administrator can block it.

**Solution** — the package that moves agents, flows and connection references between environments
({{topic:solutions}}).

**Least-privilege role** — the smallest set of permissions that still does the job; what every agent
and connector gets, instead of yours.
