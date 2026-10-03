## TL;DR

A **solution** is the package an agent travels in between environments: the agent, its flows, its connection
references and its environment variables, exported from one environment and imported into the next. You build
in an **unmanaged** solution and deploy a **managed** one. Every agent starts life in the **default** solution,
which can't be moved, so create a **custom solution with your own publisher** and make it your **preferred
solution** before you build anything. Retrofitting one later is real work.

## Why it matters

Nobody thinks about packaging on the first day, because on the first day nothing needs to move. The agent is
built, tested in the preview pane and shown to a colleague, all in one environment. The question arrives weeks
later, when the agent has to reach a test environment and then production ({{topic:envs}}), and by then
everything it is made of was created wherever Copilot Studio put it by default.

That is the trap. The default solution is not something you export. Getting an agent out of it means building
a custom solution after the fact and finding every component the agent depends on, and some decisions made on
day one, like the prefix on every name, can no longer be changed.

## How it works

### What a solution is

<!-- volatile verified=2026-10 -->
Microsoft calls solutions the mechanism for application lifecycle management in Power Platform. In Copilot
Studio, *when you create an agent, the agent is created within a Power Platform solution*: automatically, the
**default solution**. *To export, import, and manage agents between environments, you need to create and use a
custom solution.* A solution acts as a *carrier* for the agent, and you can open it from the agent's settings
with **View solution**, or from the solution explorer under **…** > **Solutions**.
<!-- /volatile -->

Everything that can go in a solution is a **component**. For an agent, the ones that matter are:

| Component | Why it has to travel |
|---|---|
| The agent | Its instructions, knowledge, tools and settings |
| Agent flows | Tools built as flows ({{module:automation-and-workflows}}) |
| **Connection references** | Pointers to connections, re-bound in each environment, because connections themselves don't move ({{topic:connauth}}) |
| **Environment variables** | Values that differ per environment: a site URL, a warehouse name |

A solution can be up to 95 MB.

### Unmanaged and managed

| | Unmanaged | Managed |
|---|---|---|
| Where | The development environment | Test, production: anywhere downstream |
| Purpose | Developed: you change things | Deployed: a build artifact |
| Editable | Yes | No; components can't be edited directly |
| When deleted | Only the container goes; customisations stay | Everything it brought is removed |

Microsoft's guidance: unmanaged solutions are your **source**, and the exported unmanaged copy belongs in source
control. Managed solutions are produced by exporting the unmanaged one *as* managed. You can't import a managed
solution into the environment that holds its unmanaged original, which is one more reason the test environment
exists.

### Publisher and prefix

Every solution has a **publisher**, and every publisher has a **prefix** that is stamped on the names of
components created under it. Create your own publisher rather than using the default one. Microsoft is blunt
about timing: change a prefix *before you create any new apps or metadata items because you can't change the
names of metadata items after they're created*. A component's publisher is its owner, and ownership can move
between solutions of the same publisher but not across publishers. One publisher per organisation or team keeps
that simple.

### Preferred solution: the day-one switch

In the solution explorer, **Set preferred solution** chooses the solution in which new agents are created by
default. Set it to your custom solution before creating the agent, and everything you build afterwards lands
in the right place with the right prefix. That one setting is the whole of *create every agent inside a custom
solution from day one*.

<!-- unknown since=2026-10 -->
Microsoft documents solutions only for the standard harness. Whether an agent on the GitHub Copilot harness is
created in, can be added to, and travels in a custom solution the same way has not been checked. Check it in
your developer environment before you build an agent that has to reach production.
<!-- /unknown -->

## In practice at Technik

Before creating the Production Assistant, the engineer creates a publisher, *Technik Engineering* with the
prefix `tke`, then a custom solution, *Technik Production Assistant*, and sets it as the preferred solution.

The solution ends up holding:

| Component | Notes |
|---|---|
| The Production Assistant | — |
| Connection reference: Snowflake | Bound in each environment to a connection made as `TECHNIK_AGENT_RO` |
| Connection reference: SharePoint | Bound per environment |
| Environment variable: `tke_SnowflakeWarehouse` | `TECHNIK_AGENT_WH` in every environment today, but named so it can differ |
| The document revision approval flow | Added when the drafting task got its approval ({{topic:approvals}}) |

The unmanaged solution is exported to source control after every change worth keeping, and exported **as
managed** for *Technik Agents Test*.

A second agent built the same month, a small FAT checklist helper, went the other way: built in the default
solution as *"just a prototype"*. Moving it meant creating a solution afterwards, adding the agent, finding the
flow and its connection by hand, and living with the default publisher's prefix on the flow it had created.

## Design guidance

- **Create a publisher with a meaningful name and prefix** before anything else.
- **Create the custom solution and set it as preferred** before creating the agent.
- **Develop unmanaged, deploy managed.** Never import an unmanaged solution into production.
- **Use connection references and environment variables** for anything that differs per environment.
- **Export the unmanaged solution to source control** as your record of the agent.
- **Check the harness**: confirm that your agent travels in a solution before relying on it.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent can't be exported to test | It lives in the default solution | **Create every agent inside a custom solution from day one**, set as preferred |
| Component names carry the default prefix | Built before a publisher was created | Create the publisher first; names can't be changed later |
| A component is missing after import | It was never added to the solution | Add components and their dependencies before exporting |
| Production can't be edited | It was deployed managed, as intended | Change it in development and redeploy |
| The agent arrives and its tools fail | Connections don't travel; references weren't bound | Bind each connection reference in the target environment |

## Key terms

**Solution**: the package that carries an agent and its components between environments.

**Default solution**: where agents are created unless told otherwise. Not for export.

**Unmanaged / managed**: the editable source in development, and the locked build deployed downstream.

**Publisher prefix**: the prefix stamped on component names, fixed once components exist.

**Preferred solution**: the solution new agents are created in by default.
