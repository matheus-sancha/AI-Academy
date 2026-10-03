## TL;DR

A Power Platform **environment** is a container for agents, flows, apps, connections and data, with its own
security, its own region and at most one Dataverse database. Nothing in one environment can reach the data
sources of another. That boundary is what makes separate **development, test and production** environments
worth having: an experiment in development cannot touch what real users rely on. Build in your own developer
environment, prove the agent in a test environment that looks like production, and only then let users near it.

## Why it matters

Every *it worked for me* failure in this module has the same shape: the agent ran in one place, with one
person's access, and then met a different place or a different person. Environments are the first of those
differences, and the only one you choose deliberately.

The tempting shortcut is to build where everyone already is. Every tenant has a **default environment**, and
everyone with a licence is automatically a maker in it. Microsoft describes it as intended for experimentation
and lightweight trial development, with no backup guarantees, and says it shouldn't be used for production
workloads. An agent built there is one person's experiment sitting in a space shared by the whole company,
next to everyone else's.

## How it works

### What an environment holds

<!-- volatile verified=2026-10 -->
Microsoft's definition: a space to store, manage and share an organisation's business data, apps, agents and
flows, and a container to separate apps with different roles, security requirements or audiences. Each one:

- belongs to one Microsoft Entra tenant, and only that tenant's users can reach it;
- is bound to a **geographic region**, and everything created in it (agents, connections, flows) stays there;
- has **zero or one Dataverse database**, which is where Copilot Studio stores agents;
- can only connect to data sources deployed **in the same environment**: an agent in Test cannot use a
  connection made in Dev.
<!-- /volatile -->

That last point is why moving an agent is a real operation, not a copy. Its connections stay behind and have to
be made again on the other side ({{topic:connauth}}).

### The types

| Type | Meant for | Worth knowing |
|---|---|---|
| **Default** | Experimentation | One per tenant, shared by everyone, every licensed user is a maker, no manual backup |
| **Developer** | One owner's own work | Only the owner; security groups can't be assigned ({{topic:devenv}}) |
| **Sandbox** | Development and testing | Non-production, with copy and reset |
| **Trial** | Short-term testing | Expires after 30 days; one per user |
| **Production** | Anything you depend on | Full control; the type to use for real users |
| **Dataverse for Teams** | Apps built inside a team | Created automatically; little admin control |

### Who can do what in one

Two built-in roles govern an environment: **Environment Admin**, who manages everything in it including data
policies, and **Environment Maker**, who can create resources. Neither role grants access to the environment's
database by itself. Copilot Studio adds its own rules on top, for example that people need a role carrying the
*ChatBotReaders* privilege to chat with agents in an environment ({{topic:share}}).

### Development, test, production

The pattern Microsoft's solution guidance assumes has three stages:

1. **Development.** Your own developer environment. You change things freely; the agent lives in an
   *unmanaged* solution ({{topic:solutions}}).
2. **Test.** A sandbox shaped like production: the same data policies, the same kind of connections, test
   accounts with users' access. The agent arrives as a *managed* solution, exactly as it will in production.
3. **Production.** Where users meet the agent. Nobody edits here; changes arrive from development through test.

Each move is an export and an import, never a rebuild. And each environment answers a different question:
*does it work?*, *does it work somewhere that isn't mine?*, *is it working for users?*

<!-- volatile verified=2026-10 -->
Environments are created and managed in the **Power Platform admin center** (**Manage** > **Environments**),
which also keeps an environment's **history**: who created, copied, reset or edited it. Creating production and
sandbox environments can be restricted to admins, so in most tenants the test and production environments
are an administrator's to provide.
<!-- /volatile -->

## In practice at Technik

The Production Assistant's three environments:

| Stage | Environment | Type | Who is in it |
|---|---|---|---|
| Development | The engineer's own developer environment | Developer | The engineer |
| Test | *Technik Agents Test* | Sandbox | The engineer; a planner, a supervisor and a quality engineer as testers |
| Production | *Technik Agents* | Production | Users, through Teams; makers only through the admin |

The test environment is the one people want to skip, and the one that earns its place first. The agent's
Snowflake tool reads as `TECHNIK_AGENT_RO` on `TECHNIK_AGENT_WH`. In development it was connected with the
engineer's own Snowflake login, which can read every `TC_*` and `SAP_*` table. In *Technik Agents Test* the
connection had to be made again, this time with the agent's role, and the first revision question failed:
nobody had granted `TECHNIK_AGENT_RO` `SELECT` on `V_RELEASED_REVISIONS`, the view the tool queries, so the tool
found nothing and the agent said it could not look the revision up.

Development could never have shown that, because the engineer's login could see everything. The grant was fixed
before a single user saw the agent.

## Design guidance

- **Never build in the default environment.** It is shared, unbacked and not for production workloads.
- **Develop in your own developer environment**, and treat it as yours alone.
- **Ask your admin for a test sandbox shaped like production**: same policies, same identities for connections.
- **Never edit in production.** Changes travel development → test → production as solutions.
- **Expect connections to be remade** in every environment; plan who makes them, and as which identity.
- **Check the region** of an environment that holds sensitive data. Its contents stay there.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent breaks the day it is moved | Connections don't cross environments | Recreate them in the target, as the right identity ({{topic:connauth}}) |
| Works in development, fails in test with access errors | Development used your broader permissions | Test with the agent's real identity before users arrive |
| A colleague edited your agent | It lives in the default environment, where everyone is a maker | Move work to a developer environment |
| You can't create a test environment | Creation is restricted to admins | Ask the admin; that is the intended route |
| An agent disappeared with its environment | A trial expired after 30 days | Never put anything you need in a trial |

## Key terms

**Environment**: a container for agents, flows, connections and data, with its own security, region and database.

**Default environment**: the tenant's shared environment, where every licensed user is a maker.

**Sandbox**: a non-production environment for development and testing.

**Production environment**: the environment users rely on.

**Environment Maker / Environment Admin**: the two built-in roles that govern who can create and who can manage.
