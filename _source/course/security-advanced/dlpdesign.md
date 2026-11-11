## TL;DR

Intermediate taught how to read a data policy someone else wrote ({{topic:dlp}}). This lesson is about
writing one. A Power Platform data policy sorts connectors into **Business**, **Non-business** and
**Blocked**, forbids sharing between groups, and applies to environments you choose. For agents it
also governs Copilot Studio's own features, and, because an MCP server reaches Copilot Studio through
a connector, "blocking Power Platform connectors also blocks access to tools in connected MCP
servers." A good design decides the group of each thing, what a new connector does by default,
and how a change reaches published agents. It also knows what a data policy does not reach.

## Why it matters

A data policy is the one control an administrator can apply to every agent in a tenant without
reading any of them. That is its strength, and it makes a poor policy expensive in both directions:
too loose and any maker can join a business system to a consumer one in an afternoon, too tight and
finished agents stop working for reasons their makers cannot see. Pro-code teams meet it late. A
server that works in VS Code becomes a connector the first time Copilot Studio calls it, and the
policy applies from then on ({{topic:mcpcs}}).

## How it works

### Groups, scope and the default

"The three data groups are the Business data group, the Non-Business data group, and the Blocked data
group." Connectors "can't share data" across groups and "can reside in only one data group at a time."
For a new policy, "all connectors are placed in the Non-Business group by default", and Microsoft
advises against changing the default group. That interacts with the fact the Copilot Studio page
states: connectors introduced after 2019 are likely to land in Non-business, and "in many
organizations" that group "is automatically blocked", so a new feature can arrive already blocked.

Scope is the other axis. "Tenant-level policies can be defined to include or exclude specific
environments", and "Environment-level data policies can't override tenant-wide data policies", so a
maker's environment admin cannot loosen your tenant baseline.

<!-- unknown since=2026-11 -->
None of the pages read says how two policies that apply to the same environment combine. Test a
connector against the environment, and read the violation, before relying on a rule you cannot see.
<!-- /unknown -->

### The places a policy fails open

**Custom connectors.** An unclassified custom connector goes into the default group. Tenant admins can
classify them by host URL, using "an ordered list of Allow and Deny URL patterns", with the wildcard
rule as the last entry. "By default, the pattern is set as Ignore for new data policies", and with no
specific rule "an Ignore * rule allows custom connectors to be used with both Business and Non-Business
connector groupings." That is the opposite of a default-deny, and an MCP server added as a custom
connector sits under it.

**Connectors you cannot block.** "To ensure core user scenarios remain fully functional", Dataverse,
Approvals and Notifications cannot be blocked. Microsoft says "many of the nonblockable connectors ...
now support MCP", and that you "manage and restrict these connectors and their MCP servers" through
advanced connector policies. Custom connectors and HTTP are "not yet supported" there.

**Endpoint filtering (preview).** It lets an administrator allow or deny specific endpoints for
HTTP, SQL Server, Azure Blob Storage, SMTP and a few others, with ordered rules and a last rule of
`* Allow` or `* Deny`, where Allow is the default. It has a hard limit: "Only static endpoints that are
known and selected when building an app, flow, or chatbot during design time are enforced", and rules
"don't apply to environment variables, custom inputs, or any endpoint dynamically created at
runtime."

### What a change does to something already published

<!-- volatile verified=2026-11 -->
"Copilot Studio supports data policy enforcement in real time", though the platform page says "for the
most extreme cases, the latency for full enforcement is 24 hours. In most cases, it's within an hour."
A maker sees an error banner and an unavailable **Publish** button. A user of a published agent sees
"Sorry, something unexpected happened", with the code `DataLossPreventionViolation`. Agents "can't
be exempted from data policy enforcement" any more. Microsoft warns that "misaligned configurations,
such as data policies blocking new connectors by default, could result in production outages."
<!-- /volatile -->

<!-- unknown since=2026-11 -->
No page read describes a grace period for a published agent, and the two pages disagree about whether
blocking the *Microsoft Copilot Studio* connector is possible: one says it stops event triggers, the
other lists it among connectors that cannot be blocked. Whether endpoint filtering reaches SharePoint
or public-website knowledge is also stated by one page and absent from the other's list.
<!-- /unknown -->

## In practice at Technik

Technik's Teamcenter server is a custom connector to Copilot Studio and a Foundry toolbox target for
the capstone's agent. Two doors, and two different governors. Design the policy for the first.

| Decision | Setting | Why |
|---|---|---|
| Tenant baseline scope | All environments | Environment admins cannot override it |
| Business group | Snowflake, SharePoint knowledge, the Teams and Microsoft 365 channel, *Microsoft Copilot Studio*, *Application Insights in Copilot Studio* | The assistant's footprint ({{topic:dlp}}); Application Insights is what {{topic:tracing}} depends on |
| Blocked | *Chat without Microsoft Entra ID authentication in Copilot Studio*, the Direct Line, Facebook and WhatsApp channels | Nobody at Technik should publish an unauthenticated or external agent |
| Custom connectors | Allow the server's host, `<your-server-host>/*`, and end with `*` as Deny rather than the default Ignore | Every new custom connector is then a decision |
| HTTP | Blocked in production; endpoint-filtered in development | Child flows share a dependency with HTTP, so test them first |
| Roll-out | Scope the policy to development and test, read every violation, then add production | A policy change can break a published agent |

Then the part the table cannot cover. The capstone's server runs on Azure Container Apps, and its
agent reaches it through a Foundry toolbox with its own Entra identity ({{topic:stageship}}).

<!-- unknown since=2026-11 -->
The data-policy pages describe Power Platform connectors and Copilot Studio features. None says a
data policy reaches a server that a Foundry toolbox calls. The capstone's own controls on that path
are an Entra app role, `Teamcenter.Read`, that the server requires of its caller, and a host header
check. They are good controls and the policy does not stand in for them.
<!-- /unknown -->

So one server has two governors: a data policy when Copilot Studio calls it, and an app role when
the Foundry agent does. A review that finds the policy and stops has checked half of it.

## Design guidance

- **Write the policy from the agent's footprint**, group by group, and agree it with the administrator before building.
- **End the custom connector list with a deny**, so a new one needs a decision.
- **Scope a new policy to development and test first.** Read violations before touching production.
- **Know the connectors you cannot block** and use advanced connector policies for them.
- **Use endpoint filtering where HTTP is allowed**, and remember it only sees static endpoints.
- **Keep Application Insights allowed** wherever you rely on traces.
- **Pair a data policy with an identity control** on every server it cannot see.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A new Copilot Studio feature is blocked on day one | It landed in the default group, which is often blocked | Classify it deliberately and tell makers |
| A custom connector is allowed beside a business one | The `*` rule is Ignore by default | Allow your hosts, deny the rest |
| A published agent starts failing with `DataLossPreventionViolation` | A policy change after publication | Test the policy on a scoped environment first |
| An HTTP rule seems ignored | The endpoint came from a variable or was built at runtime | Use a static endpoint, or block HTTP |
| An MCP tool disappears for a connector you did not touch | Its connector is blocked, and tools go with it | Check the connector's group |

## Key terms

**Data policy** — a rule that sorts connectors into groups and stops agents combining them.

**Default group** — where a connector lands when nobody has classified it, usually Non-business.

**Endpoint filtering** — ordered allow and deny rules on the addresses a connector may call.

**Advanced connector policy** — the control for connectors that cannot be blocked outright.
