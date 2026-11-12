## TL;DR

Microsoft Agent 365 is a control plane that sits above where an agent was built. It lists agents in a registry,
puts identity and access controls on them, and gives administrators actions to install, activate, block, delete
and, for Foundry agents, start and stop. Microsoft's pages organise it as **Observe, Govern, Secure**. It has
been generally available since 1 May 2026, licensed per user. Copilot Studio agents join it automatically in an
onboarded tenant. A pro-code agent joins only if you do the work: register it, give it an identity and instrument
it. The lesson for an engineer is that an administrator now holds switches over your agent, so build it to
survive each one being thrown.

## Why it matters

Until now every control in this module acted on a solution or an environment. Agent 365 acts on the agent
itself, wherever it was built, and the person using it is a tenant administrator who never opened your
repository. They can block the agent, delete it or reassign its owner. An agent that was not built with that in
mind loses its telemetry, its owner or its users without a deployment having happened.

## How it works

### Three pillars, one registry

<!-- volatile verified=2026-11 -->
The overview says that "as of May 1, 2026", Agent 365 is generally available for the Commercial segment, per
user. Its **registry** in the Microsoft 365 admin center lists every agent available to the organisation, from
four publisher types: Microsoft, external partners, your organisation and shared by a creator. It can filter by
platform and channel, and it counts **unmanaged** agents separately: those created outside Agent 365, with no
risk protection or observability. A Risks column draws on Microsoft Purview, Entra and Defender.
<!-- /volatile -->

Each pillar maps onto a product you may already use. **Observe** is activity dashboards and telemetry. **Govern**
is the lifecycle actions below. **Secure** is Entra for identity, Purview for data and audit, and Defender for
threats. Defender's real-time blocking is in preview, as are the registry's Graph API and the Work IQ tools.

### How an agent gets in

<!-- volatile verified=2026-11 -->
For **Copilot Studio**, Microsoft's builder page says the agent gets an identity, a registry entry and
observability "automatically", and is pre-approved through Power Platform policies. Copilot Studio's own page
frames Agent 365 as something for "organizations that onboard" it, so read *automatic* as *automatic once the
tenant is onboarded*. A custom-engine agent published only in Copilot Studio "might not" appear. Sharing it with
the whole organisation and submitting it for admin approval creates a *Published by your org* entry.

For a **pro-code** agent in Python, Node.js or .NET, the quickstart works through coding-assistant skills. The
`a365-setup` skill writes a generated configuration file. `make-a365-agent` registers a blueprint in Entra,
creates an agent identity from it and requests the permissions it needs. `instrument-observability` adds the
telemetry. The quickstart separates the two: "Registration provides catalog visibility; the observability step
adds telemetry." You need a Global Administrator, or an Agent ID Developer with one on hand for consent grants.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
Telemetry is "dropped silently" if no user in the tenant holds an E7 or Agent 365 licence, and spans do not
reach Defender, Purview or the admin center without a root `invoke_agent` span. Whether Agent Framework's own
tracing ({{topic:tracing}}) produces that span is not stated by this topic's pages.
<!-- /unknown -->

The identity half is {{topic:agentid}}'s blueprint. The two pages that lesson reads disagree about whether a
Copilot Studio agent always gets an identity, and the builder page here says it does. Treat that as one more
reason to check an agent's identity in the admin center rather than infer it.

### What an administrator can do

<!-- volatile verified=2026-11 -->
Under **Agents** > **All agents** in the Microsoft 365 admin center, the governance actions page lists these.

| Action | Effect | Note |
|---|---|---|
| Install, uninstall | For everyone, or chosen users and groups | Consent is granted at install |
| Activate | Gates a new agent: a user's request needs AI admin approval | Admins can also activate directly |
| Block, unblock | Stops an agent org-wide | A Copilot Studio or Agent Builder agent is blocked in Microsoft Copilot and other hosts. A SharePoint or Foundry agent is blocked only in Copilot Chat |
| Delete, restore | Soft delete, 30 days, audited | Copilot Studio agents are deleted by a Power Platform environment admin |
| Start, stop | Foundry agents only: deallocate or provision the compute | Needs the Azure AI Owner role |
| Assign owner | Shared Agent Builder and Copilot Studio agents only | A creator who is deleted leaves the agent ownerless |
<!-- /volatile -->

If a Power Platform environment enforces its IP Firewall, these admin center actions are not applied, and the
page sends you to the Power Platform API.

### The Copilot Studio controls under it

<!-- volatile verified=2026-11 -->
Copilot Studio's security and governance page is a table of controls, most set in the Power Platform admin
center. Data policies govern authentication, knowledge sources, actions, HTTP requests, channels, Application
Insights and triggers. Environment routing sends makers to a safe environment. Maker audit logs go to Purview,
and audit events can go to Microsoft Sentinel. Tenant switches can turn off publishing of agents that use
generative AI, or stop data moving across geographies. The page says no tenant policy blocks conversations on
admin-defined topics, which makes moderation a design matter ({{topic:modtuning}}).
<!-- /volatile -->

<!-- unknown since=2026-11 -->
VS Code lets "your organization" restrict MCP servers ({{topic:mcpvscode}}). Whether Agent 365 governs which MCP
servers an agent may reach is not stated by this topic's pages. Nor is whether the capstone's hosted agent
appears in the registry, although the registry does list Foundry agents.
<!-- /unknown -->

## In practice at Technik

| Agent | How it reaches the registry | What an administrator can do to it |
|---|---|---|
| Production Assistant (Copilot Studio) | Automatically, once the tenant is onboarded | Block, delete, reassign the owner |
| A pro-code Agent Framework rebuild in Teams | The SDK route: blueprint, identity, instrumentation | Block, and see its telemetry only if a licensed user exists |
| The capstone's hosted agent | Unstated | If it is listed: start, stop and block, as a Foundry agent |

Name an owner and a sponsor for each ({{topic:agentid}}). The dashboard counts agents without owners, and a
shared agent becomes ownerless when its creator is deleted.

## Design guidance

- **Give every agent an owner**, because deleting a creator leaves it ownerless.
- **Register and instrument a pro-code agent** and confirm both appear, since they are separate steps.
- **Ensure a licensed user exists** before relying on telemetry.
- **Plan for being blocked.** Decide what users see and who is told.
- **Check which surfaces a block reaches**, because the effect differs by platform.
- **Use the right role.** An AI Administrator cannot configure Conditional Access.
- **Keep the agent's own controls**, since the registry reports and does not replace data policy or identity.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent is missing from the registry | A custom-engine agent published only in Copilot Studio | Share it organisation-wide and submit it for approval |
| No spans reach Defender or Purview | No licensed user, or no root `invoke_agent` span | License a user and check the span |
| A block does not stop the agent everywhere | A Foundry or SharePoint agent is blocked only in Copilot Chat | Block it at its own platform too |
| An admin center action has no effect | The environment's IP Firewall is enforcing | Use the Power Platform API |
| An agent cannot be reassigned | Its creator was deleted | Assign an owner first |
| Deletion fails for a Copilot Studio agent | It needs a Power Platform environment admin | Ask that role |

## Key terms

**Control plane**: the layer that governs agents without running them.

**Registry**: the admin center's inventory of agents.

**Blueprint**: the Entra object that holds an agent identity's credentials.

**Unmanaged agent**: one created outside Agent 365, with no risk protection or observability.

**Activation**: admin approval that lets users create instances of an agent.
