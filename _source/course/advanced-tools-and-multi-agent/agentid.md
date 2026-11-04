## TL;DR

Microsoft Entra Agent ID is "an identity and security framework that extends Microsoft Entra
capabilities to AI agents", and agent identities "are identity accounts within Microsoft Entra ID".
Read the design as subtractive rather than empowering. An agent gets its own identity mainly so it
can be *denied* things a person could hold: "Only lower privileged roles (such as a reader role) can
be assigned to an agent", four Microsoft Graph permissions are refused outright, and because "Agents
can't satisfy interactive controls like MFA", Conditional Access has to grip somewhere else.

## Why it matters

Every lesson in this module has ended at the same question — whose authority runs this? A custom
connector's credential, a connection reference's owner, a computer-use run's stored password, an A2A
caller's header. Agent ID is the first answer that treats the agent as the principal rather than
borrowing someone's.

The problem it names is specific: organizations "need purpose-built identity constructs to
authenticate, authorize, govern, and protect these nonhuman identities", because "Traditional
identity types (like standard app registrations or user accounts) aren't ideal for autonomous
agents." Of the four pressures listed, the last two are the interesting ones — "Preventing AI agents
from gaining access to the most critical security roles and systems", and "Scaling identity
management to large numbers of AI agents that might be quickly created and destroyed."

## How it works

### Four objects, and the one that holds the credentials

Agent identities "are built on the same service principal infrastructure that applications use
throughout Microsoft Entra, but they're a distinct object type" — "modeled as single-tenant service
principals with a new 'agent' subtype classification". There are four object types: an **agent
identity blueprint**, a **blueprint principal**, an **agent identity**, and an **agent user**.

The shape is familiar. The audit-log documentation spells out the analogy: a blueprint is "Analogous
to an app registration", an agent identity "Analogous to a service principal". What differs is the
cardinality and the credential. "Standard applications have a one-to-one relationship between
application and service principal. The agent app model is one-to-many", and a blueprint "can perform
exactly one operation in the tenant: provision or deprovision agent identities."

Then the twist worth remembering: "Agent identities don't manage credentials. The blueprint holds all
credentials and uses them to impersonate each agent identity", so "the agent identity appears as the
client in the resulting token and in audit logs, even though the blueprint performed the actual token
exchange." One consequence follows immediately — "OAuth permissions granted to a agent identity
blueprint are granted to all agent identities created from that blueprint." The blueprint is a blast
radius, not just a template.

### Where identities come from

<!-- volatile verified=2026-11 -->
Five channels: the Entra admin center, the Microsoft Graph API, CLI and PowerShell and
infrastructure-as-code, Microsoft product integrations, and the consent experience — where signing in
to a third-party agent shows a page that "allows the employee to add the agent to their tenant". Of
the integrations, Copilot Studio records the creator "as its sponsor", and Foundry "automatically
provisions and manages agent identities throughout the agent lifecycle", with "Publishing an agent"
creating a dedicated blueprint and identity. By hand, over Graph:
<!-- /volatile -->

```json
POST https://graph.microsoft.com/beta/serviceprincipals/Microsoft.Graph.AgentIdentity
{ "agentIdentityBlueprintId": "<your-blueprint-id>" }
```

Two inventory problems come with that. "some Microsoft applications, including earlier versions of
Microsoft Copilot Studio and Azure AI Foundry, used standard application service principals to secure
their agents", so a tenant holds agents that are not agent identities — which is why the admin list
at **Entra ID** > **Agents** > **Agent identities** carries a **Uses agent identity** column. And
principals "are limited to a maximum of 250 agent identity creations".

### What an agent may not have

The permission model is where the design shows itself. Lower-privileged roles only: "Roles such as
Global Administrator, Privileged Role Administrator, or User Administrator can't be assigned to agent
identities", though "Custom roles can be assigned to agents." Four Graph permissions are blocked —
`Application.ReadWrite.All`, `RoleManagement.ReadWrite.All`, `User.ReadWrite.All` and
`Directory.AccessAsUser.All` — and the reasoning is unusually direct: this "Ensures that an agent
can't circumvent security by asking for sweeping Microsoft Graph access – even an administrator can't
consent to give an agent those permissions."

Access comes in two modes: **autonomous**, on rights held by the agent identity itself, and
**delegated**, on-behalf-of a signed-in user. Conditional Access applies, and it inherits the
blueprint's reach — "A policy that targets a blueprint applies to all agent identities created from
that blueprint, including agent identities created later." But the control surface is different,
because an agent cannot be challenged: with MFA unavailable, you "create separate policies that use
identity filters, risk signals, and named locations as control points."

Accountability is split deliberately: "Owners are technical administrators who can manage the
configuration and operations of an agent. Sponsors are business owners who are accountable for the
agent's purpose, lifecycle decisions, and access reviews."

<!-- unknown since=2026-11 -->
Three gaps. The pages disagree on Copilot Studio: one says every new agent "gets an agent identity",
another that it "can be configured to automatically be assigned" once a setting is enabled — so do
not assume it is on. Agent Framework is never mentioned, so whether code you write yourself gets an
identity automatically is unstated. And regional availability is given nowhere.
<!-- /unknown -->

Licensing is split too, which matters for planning: "Agent ID is available for all Microsoft Entra
customers", but "Extending Microsoft Entra security features to agents requires Microsoft Agent 365"
({{topic:agent365}}, {{topic:costs}}).

## In practice at Technik

The capstone's agent already has one of these. Deployed as a Foundry hosted agent, it reaches its MCP
server through a toolbox whose connection authenticates as the agent's own Entra Agent ID
({{topic:stageship}}). What the scenario adds is that this is not the agent's only identity: inside
Snowflake it is `TECHNIK_AGENT_SVC`, a service user holding the single read-only role
`TECHNIK_AGENT_RO`. Two identities, one agent, meeting at a secret in Key Vault.

That is not duplication to be tidied away — it is the boundary. The Entra Agent ID governs whether
the agent may reach the server at all; `TECHNIK_AGENT_SVC` governs which rows come back. Neither
answers the other's question, and the read-only ceiling on the Snowflake side happens to match the
role ceiling Entra would impose anyway.

Three practices follow. Name it so it reads as an agent in a log — the documented convention is
"prefixing display names with the department or function", so `Agent-TechnikProduction`, nothing
resembling a person. Give it a sponsor accountable for *why it exists*, which at Technik is the
Production Assistant's owner rather than whoever deployed it. And drop client secrets, since the
guidance is to "prefer federated identity credentials (managed identities) or certificates", which
also removes something {{topic:connrefs}} would have to rotate.

## Design guidance

- **One identity per agent instance**, and never improvise: "Don't create AI agents as plain app
  registrations or service principals outside the Agent ID framework."
- **Treat the blueprint as a blast radius.** Permissions granted there reach every identity it has
  made, and every one it makes later.
- **Design Conditional Access without MFA.** Identity filters, risk and named locations are the
  controls you have.
- **Give every agent a sponsor and an owner**, and make the sponsor answer for its purpose.
- **Prefer managed identities or certificates** to client secrets, and keep what remains in Key
  Vault.
- **Audit by `agentType`**, not by name, so agents on legacy service principals are not missed.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A role assignment is refused | It is a privileged role, barred for agents | Use a lower-privileged or custom role |
| An admin cannot consent to a permission | It is one of the four blocked Graph permissions | Redesign the access; no consent will unblock it |
| A Conditional Access policy does not bite | It targets the agent identity, not the agent's user account, or vice versa | Write a policy for each object |
| Every agent from one blueprint gains access nobody asked for | A grant was made on the blueprint | Move the grant to the individual agent identity |
| An agent is missing from the inventory | It runs on a legacy application service principal | Filter the list by **Uses agent identity** |

## Key terms

**Agent identity blueprint** — the template that provisions agent identities, holds their credentials
and impersonates them. Analogous to an app registration, but one-to-many.

**Agent's user account** — the optional user-subtype object that lets an agent act where a user
identity is required. Governed separately from the agent identity.

**Sponsor** — the business owner accountable for an agent's purpose and lifecycle, distinct from the
owner who administers it.
