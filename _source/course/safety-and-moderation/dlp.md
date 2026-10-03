## TL;DR

**Data policies** (Power Platform's DLP) are rules your administrator sets that put every connector into one of
three groups: **Business**, **Non-business** or **Blocked**. An agent cannot combine connectors from different
groups, and cannot use a blocked one at all. Copilot Studio exposes its own features as connectors too:
knowledge sources, channels, HTTP requests, skills, even *chat without sign-in*. So a data policy decides much
more than which tools you may add. When something will not add or will not publish, suspect a policy before a
bug. Copilot Studio does say so, but in places makers rarely look.

## Why it matters

You design an agent as a combination: these knowledge sources, these tools, this channel. A data policy decides
whether that combination is allowed, and it was written by someone who has never seen your design. Finding out
at publish time means redesigning a finished agent.

The policy is also the organisation's answer to a question you should be able to answer yourself before
publishing anything: **what data does this agent move, and where to?** Every connector is a route data can
travel. The policy exists because, without one, a maker can join a business system to a consumer service in an
afternoon.

## How it works

### Groups, and the rule that joins them

Administrators configure data policies in the Power Platform admin center, scoped to some or all environments.
Each connector sits in one data group, and **connectors in different groups cannot share data**. Two business
connectors are fine together. A business connector and a non-business one in the same agent is a violation,
even if neither is blocked.

New connectors land in the policy's **default group**. Microsoft notes that connectors introduced after 2019,
including several of Copilot Studio's own, are likely to default to **Non-business**, and that many
organisations block that group automatically. A feature can therefore be blocked in your tenant without anyone
having decided to block it.

Enforcement applies to every tenant since early 2025, and agents can no longer be exempted.

### Copilot Studio's features are connectors

| To control | The policy blocks |
|---|---|
| Agents anyone can chat with, without signing in | *Chat without Microsoft Entra ID authentication in Copilot Studio* |
| SharePoint and OneDrive knowledge | *Knowledge source with SharePoint and OneDrive in Copilot Studio* |
| Uploaded files, public websites as knowledge | Two further *Knowledge source with …* connectors |
| Tools built on Power Platform connectors | The connector itself. This also blocks MCP servers that connect through one |
| HTTP requests from topics | *HTTP* |
| Skills | *Skills with Copilot Studio* |
| Publishing to Teams and Microsoft 365 | *Microsoft Teams + Microsoft 365 Channel in Copilot Studio* |
| Event triggers, and automated evaluations run with an authenticated account | *Microsoft Copilot Studio* |

For SharePoint, public websites and HTTP, an administrator can use **endpoint filtering** instead of a block:
specific sites allowed, others denied. So *SharePoint knowledge is allowed* does not mean *your* site is.

### How a policy shows itself

The explanation exists. It is just easy to miss:

- a blocked connector appears **disabled** when you add a tool, with the reason in its **hover text**;
- a blocked channel appears disabled when you add it at publish time;
- a violation already in the agent raises an **error banner** with a **Details** button, and the detail is a
  file you **download** from the **Channels** page, one row per violation;
- the **Publish** button becomes unavailable.

Administrators can add a contact email and a *Learn more* link to these messages, which applies across Power
Platform. If your tenant's errors name a person, that is who wrote the policy.

<!-- unknown since=2026-10 -->
The data-policy pages do not distinguish between harnesses. That GitHub Copilot harness agents surface
violations the same way is not documented. Nor is whether *Skills with Copilot Studio* governs the Agent Skills
this level teaches. The page's own link for *skills* points at an older Copilot Studio feature of the same name.
<!-- /unknown -->

### Where the data goes

Data policies govern combinations. Two other controls govern geography. Copilot Studio documents geographic
data residency, and an administrator can disable data movement across geographies for generative AI features.
On the GitHub Copilot harness, a request the residency settings forbid fails with `CROSS_GEO_NOT_ALLOWED`, and
the documented fix is an administrator setting or a model deployed in your region. For SharePoint knowledge,
users see the highest sensitivity label among the sources an answer used.

## In practice at Technik

Before building anything, write the Technik Production Assistant's **policy footprint**: every connector its
design touches, and the group each must be in. Then hand it to the administrator.

| Part of the design | Connector in the policy | Must be |
|---|---|---|
| Published to Teams | Microsoft Teams + Microsoft 365 Channel in Copilot Studio | Business |
| Two SharePoint knowledge sources ({{topic:sources}}) | Knowledge source with SharePoint and OneDrive in Copilot Studio | Business, with both sites allowed if endpoints are filtered |
| Work order, QN and revision tools | Snowflake | Business |
| `qn-write-up` and the other skills | Skills with Copilot Studio, if it applies to this harness | Not blocked |
| Evaluation runs as a test account ({{module:testing-and-evaluation}}) | Microsoft Copilot Studio | Not blocked |
| Sign-in required | Chat without Microsoft Entra ID authentication in Copilot Studio | **Blocked**, and that is what you want |

The last row is the one to ask for. A policy that blocks unauthenticated chat stops anyone, you included, from
publishing a Technik agent that needs no sign-in ({{topic:agentauth}}).

Then the data-movement question, in one paragraph: the agent reads replicated SAP and Teamcenter data from
Snowflake as `TECHNIK_AGENT_RO`, and controlled documents from SharePoint as the asking user. Both reach the
model's context and then a Teams chat. Nothing is written back. The model must be deployed somewhere Technik's
residency settings allow. If the administrator can read that paragraph and the table and say yes, the
conversation took ten minutes instead of a failed publish.

> [!TIP]
> When Publish is greyed out, open **Channels**, expand the error and download the details before changing
> anything. One row per violation is a faster diagnosis than guessing which connector it was.

## Design guidance

- **Write the policy footprint before you build**, and agree it with your administrator.
- **Suspect a policy first** when something will not add, will not publish, or worked in another environment.
- **Read the hover text and download the details.** The reason is there.
- **Keep every connector in one group.** A mix is a violation even when nothing is blocked.
- **Ask for unauthenticated chat to be blocked** in any environment holding company data.
- **Be able to say where the data goes**, source by source, in a paragraph.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A connector is greyed out in **Add a tool** | A data policy blocks it | Read the hover text; ask the administrator |
| **Publish** is unavailable with an error banner | A policy violation somewhere in the agent | **Channels** → expand the error → download the details |
| Every part is allowed, and the agent still violates the policy | Two connectors sit in different data groups | Ask for both in the same group, or drop one |
| A Copilot Studio feature is blocked that nobody blocked | It defaulted to Non-business, which the tenant blocks | Ask for it to be classified deliberately |
| An MCP server's tools stopped working | The connector it connects through was blocked | Same fix as any blocked connector |
| SharePoint knowledge works for one site and not another | Endpoint filtering allows only some sites | Ask for the site to be allowed |
| `CROSS_GEO_NOT_ALLOWED` | Residency forbids the model's region | An in-region model, or an administrator change |

## Key terms

**Data policy (DLP)**: administrator rules deciding which connectors an agent may use, and which together.

**Data group**: Business, Non-business or Blocked. Connectors in different groups cannot share data.

**Endpoint filtering**: allowing or denying specific SharePoint sites, websites or HTTP endpoints rather than a
whole connector.

**Policy footprint**: the list of connectors a design touches, and the group each needs.

**Data residency**: where Copilot Studio may process an agent's data geographically.
