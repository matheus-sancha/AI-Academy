## TL;DR

Microsoft Purview governs the data an agent touches, not what the agent does. It brings sensitivity
labels, data loss prevention, auditing and posture management to Copilot and to agents, and its
documentation says that "where these AI apps support agents, they inherit the same security and
compliance capabilities as their parent AI app." Three limits shape how much it can do for a pro-code
agent. Coverage differs by agent type. Policy enforcement can depend on how the call is
authenticated. And every control assumes the data is something Purview can see, which for an agent
that reads a warehouse is only part of it.

## Why it matters

Everything so far in this module is about what an agent may do. Purview is about what the
organisation can say afterwards: which labelled file reached an answer, who asked, whether a policy
stopped a prompt, what a retention rule keeps. Those are the questions a security review or an
audit asks. An agent that works perfectly and leaves no record cannot answer them, and an agent
that reads data its sources never labelled cannot be held to labels that were never applied.

## How it works

### Access first, then labels

The documentation's baseline is that AI apps "use existing controls to ensure that data stored in
your tenant is never returned" to a user without access to it. Labels add a layer. The label name and
its content markings show in Office apps, and for encrypted content the rule is explicit: "users must
have the EXTRACT usage right, as well as VIEW, for the AI apps to return the data." A response in
Copilot Chat shows the highest-priority label among the data it used, and Copilot in Word,
PowerPoint and Outlook gives new content the highest-priority label of its source file.

Three caveats are stated. "S/MIME protected emails won't be returned by Copilot". "Password-protected
documents can't be accessed by AI apps unless they're already opened by the user in the same app".
And the recommendation to enable sensitivity labels for SharePoint and OneDrive, because without it
the encrypted files that Copilot and agents can reach "are limited to data in use from Office apps on
Windows."

### Policies on prompts and files

Data loss prevention has a policy location for **Microsoft 365 Copilot and Copilot Chat**. A policy
there can restrict the processing of prompts that contain sensitive information types, and the
processing of files and emails that carry specific sensitivity labels. Insider Risk Management has a
*Risky AI usage* policy template for prompt injection attempts and access to protected materials.
Communication compliance covers prompts and responses. Each is a policy over a population of users
and content, written in the Purview portal, and none of them asks the model anything.

### What is recorded

<!-- volatile verified=2026-11 -->
"Prompts and responses are captured in the unified audit log", and an audit record for an AI
interaction carries properties such as `AgentId`, `AgentName`, `AccessedResources` (with a file's
`SensitivityLabelId` and an `XPIADetected` flag), `Messages` (with `JailbreakDetected`) and
`ModelTransparencyDetails`. Copilot interactions are also stored in the user's mailbox, which is
what eDiscovery searches, and retention policies choose *Microsoft Copilot Experiences* for
Copilot Studio agents and *Enterprise AI apps* for Foundry.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
The audit page's own example of `Messages` holds only an ID and a prompt-or-response flag, and the
pages disagree about where the text lives: the unified audit log, the user's mailbox and the
activity explorer are each named. None of the audit pages read mentions tool calls.
<!-- /unknown -->

### Coverage by agent type

The agents page has one table for what each kind of agent gets.

<!-- volatile verified=2026-11 -->
Copilot Studio agents and Foundry agents are supported for data classification, sensitivity labels,
data loss prevention and Insider Risk Management, and for compliance management. Entra-registered
agents are supported for both columns. Foundry's page adds a condition: policies "apply to API calls
that use Microsoft Entra ID authentication with a user-context token", and "for all other
authentication scenarios, user interactions are displayed in Microsoft Purview Audit". Turning it
on takes one of two routes, Purview Data Security in the Foundry Control Plane or in Defender for
Cloud, while Copilot Studio asks you to activate Purview Audit from DSPM for AI. Managing these
interactions "might require you to enable pay-as-you-go billing". The curated page names no licence,
so check the Purview service description before promising a capability to a security team.
<!-- /volatile -->

## In practice at Technik

The Production Assistant reads three kinds of data, and Purview's reach differs for each.

| Data path | Who it runs as | Purview's part |
|---|---|---|
| Controlled Documents and Standards sites | The asking user | Access trimming, labels such as *Confidential* on the `PRJ-2031` customer specification, DLP, audit |
| Teamcenter and SAP data in Snowflake | `TECHNIK_AGENT_SVC`, one read-only role | Unclear, see below. The boundary is the role and the views |
| The conversation itself | The user, in Teams | Audit, retention, eDiscovery, communication compliance |

That table is the practical finding. A label stops the *Confidential* customer specification
reaching a user without access to it, and shows its label in the answer. The pages describe labels
on files and Dataverse content, and none describes one on a warehouse row. For the Snowflake half the
controls are the ones the course has already built:
a view, a role and a narrow tool ({{topic:threats}}).

The capstone adds two uncertainties.

<!-- unknown since=2026-11 -->
Whether the hosted agent's calls meet Foundry's condition of a user-context token depends on how a
client calls it, and the capstone never ran live, so nobody has seen which of its interactions
would be policy-covered and which only audited. The pages read also do not say whether Purview
classifies what a tool returns from outside Microsoft 365, such as Snowflake rows, or whether
anything it does reaches the traces in Application Insights.
<!-- /unknown -->

What to decide is therefore small and concrete. Write down, per data path, which control governs it
and who can read the record afterwards. The traces are the case in point: they hold tool results,
and every document result names its owner, such as the person who owns `SOP70000114`
({{topic:tracing}}). The access control on them is a Log Analytics role assignment, and no Purview
label applies to them that the documentation shows.

## Design guidance

- **Map every data path to the control that governs it**, and write down the ones Purview does not.
- **Enable labels for SharePoint and OneDrive**, or encrypted files fall out of reach.
- **Label the sources before blaming the agent.** An unlabelled file carries no restriction.
- **Know the authentication condition** on policies, and test which interactions each covers.
- **Turn on audit before you need it**, and decide who may search it.
- **Treat an agent's identity as a data-access decision**, not only a security one ({{topic:agentid}}).
- **Name the licence and billing model** a capability needs before a review depends on it.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| An answer cites a document the user cannot open | The user could reach it, or the agent ran as a service identity | Check whose authority the retrieval used |
| An encrypted file never appears in answers | Missing EXTRACT, or labels not enabled for SharePoint | Grant the right, or enable labels |
| A policy never fires for a pro-code agent | The call lacked a user-context token | Read the audit record and the authentication path |
| Audit has the interaction but not the text | The record holds message IDs and flags | Find where your tenant stores the text before promising it |
| A summary of labelled data carries no label | Inheritance is documented for Copilot in Word, PowerPoint and Outlook, not for a tool's result | Say so, and bound the data at the source |

## Key terms

**Sensitivity label** — a classification on content that can add encryption and markings Copilot honours.

**EXTRACT usage right** — the right, with VIEW, a user needs for AI apps to return encrypted content.

**DLP policy location** — where a data loss prevention rule applies; *Microsoft 365 Copilot and Copilot Chat* is one.

**Unified audit log** — Purview's record of interactions with AI apps, including the files they accessed.
