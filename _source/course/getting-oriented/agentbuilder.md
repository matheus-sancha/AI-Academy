## TL;DR

Agent Builder, inside Microsoft Copilot, is where most people build their first agent: describe it in
plain language, give it instructions and knowledge, test it, share it. Spend an hour there before you
open Copilot Studio, because it shows you the entire shape of an agent with almost nothing to
configure. Its ceiling is also the reason this level exists — no actions into external systems, no
connectors, no workflows, no evaluation, no environments.

## Why it matters

The shape of an agent is the same everywhere: standing instructions, knowledge it answers from, a test
pane, and someone you share it with. Meeting that shape once, at the smallest possible scale, turns
Copilot Studio into a larger version of something familiar rather than an unfamiliar product with
forty panels.

There is a second reason, and it is the more practical one. Knowing exactly where Agent Builder stops
is what prevents you from building the wrong thing twice — and it also stops the opposite mistake, of
opening Copilot Studio for a job that a fifteen-minute question-and-answer agent would have solved.

## How it works

### Where it is and what you configure

<!-- volatile verified=2026-09 -->
Agent Builder is reached from the Microsoft 365 Copilot app at microsoft365.com/chat, from
office.com/chat, and from the Teams desktop and web clients. It is available on both the **Work** and
**Web** options on the Copilot app toolbar, and it is not available on mobile.

You describe the agent in natural language and it drafts the rest. Then you refine the instructions,
attach knowledge — SharePoint content, Microsoft 365 Copilot connectors, or web content — and test the
agent in its own pane before sharing it with colleagues.
<!-- /volatile -->

### What you are actually building

Agent Builder produces a **declarative agent**: your instructions, your knowledge and your actions
running on *Copilot's* orchestrator and *Copilot's* foundation models. Nothing extra is hosted, and
the agent inherits Microsoft 365's security, compliance and Responsible AI posture rather than
establishing its own ({{topic:stack}}).

That is an architectural fact rather than a simplification, and it explains both the speed and the
ceiling. You are not building an agent so much as configuring Copilot for a scenario.

### Governance, which is better than people expect

Agent Builder is not a loophole. Its governance rests on one principle worth stating in full:

> **No new privileges.** Agents respect existing Microsoft 365 permissions. If a user cannot access a
> SharePoint site, a Teams channel or a mailbox, the agent does not surface content from it.

This is the same rule the reader met as a Copilot user in {{topic:visibility}}, and it holds for
everything they build from here on. Standard audit logs, activity reports and DLP and retention
policies all apply; administrators see an inventory in the Microsoft 365 admin center under
**Copilot** → **Agents**, and can enable, disable, block or remove agents, configure pay-as-you-go
billing, and enforce compliance through Microsoft Purview. Agents built this way do not consume the
tenant's Dataverse storage.

It is worth being precise about what the principle does *not* promise. It governs *permissions*, not
*judgement*: an agent that can legitimately read a document can still summarise it into a channel
where it does not belong, and nothing about "no new privileges" changes what is safe to paste
({{topic:sensitive}}).

### Licensing

Agent Builder is included with a Microsoft 365 Copilot licence. Without one you can reach it through
Copilot Credits or pay-as-you-go — and you can use it **free** for agents grounded on web knowledge
only, which is a genuinely useful way to try the tool with nothing at stake ({{topic:licensing}}).

### The ceiling, precisely

<!-- volatile verified=2026-09 -->
| Limit | Consequence |
|---|---|
| No actions integrating external services | Anything beyond Microsoft 365 content needs Copilot Studio. The documentation says so directly |
| Agents built here **cannot be used in Teams Chat** | A published-to-Teams requirement fails outright |
| Target audience is individuals or small teams | Department-wide or external rollout belongs in Copilot Studio |
| Customer Managed Keys are not supported | A blocker in some regulated tenants |
| Auto-sharing SharePoint files works only with specific security groups, not everyone in the organisation | You may have to fix file and folder permissions by hand for the agent to return anything |
| If tenant policy blocks web search, the **Web content** toggle still appears enabled | A known UI limitation: the policy wins, and the interface does not admit it |
<!-- /volatile -->

The last row deserves its own sentence. An interface that shows a setting as available when policy has
overridden it is the exact situation in which a careful engineer concludes they have misconfigured
something. They have not.

### The way out

An agent built in Microsoft 365 Copilot can be **copied to Copilot Studio**, preserving its core
configuration and instructions. So outgrowing Agent Builder costs you a copy, not a rebuild — which
makes it a safe place to start something you suspect will grow. The documented path runs upward only.

## In practice at Technik

Build one slice of the Production Assistant here, in an hour, and let it succeed.

Take the *engineering questions* capability: *"which document covers weld prep inspection, and what
does it say about acceptance criteria?"* Attach the Technik standards in SharePoint and the controlled
documents. Write instructions that tell it to answer only from those sources, to cite the document
number, and to say plainly when it has nothing rather than reasoning its way to an answer. Test it.
It works — and that is one of the assistant's seven capability areas, genuinely delivered, with no
connector, no flow and no environment.

Then ask it the status of work order `100004521`.

It fails completely, and instructively. Not because the instructions are weak or the model is poor,
but because the answer lives in `SAP_WORK_ORDERS` in Snowflake and Agent Builder has no way to reach
it. There is no setting to find. That is the ceiling, met deliberately, and it is the cleanest
motivation for everything that follows in this level.

> [!TIP]
> Do this before the guided build, not instead of it. An hour spent watching one capability succeed
> and another fail is worth more than an hour reading about the difference.

## Design guidance

- **Build one on purpose, early.** The shape transfers; the hour does not come back later.
- **Use it as the free test of a real question:** is this problem solved by knowledge alone? If yes,
  you may be finished.
- **Check the ceiling against your hardest requirement**, not your first one ({{topic:stack}}).
- **Read "no new privileges" as a statement about permissions only.** It is not a sensitivity policy.
- **When you outgrow it, copy rather than rebuild** — and record why you moved.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent returns nothing from a SharePoint site | The user lacks access; agents add no privileges | Fix the permissions, not the instructions |
| You shared it and colleagues see nothing | Auto-sharing files works only with specific security groups | Set the file and folder permissions manually |
| Web content is toggled on but no web answers appear | Tenant policy blocks web search; the toggle is not disabled | The policy wins — ask your administrator |
| The agent cannot be used in Teams Chat | A known limitation of agents built here | Build in Copilot Studio if Teams Chat is required |
| You need to read or write another system | No actions into external services | Copy the agent to Copilot Studio ({{topic:stack}}) |
| Answers are confident and uncited | Attaching knowledge is not the same as being grounded in it | Instruct it to answer from the source and to say when it cannot ({{topic:citations}}) |
| It is rolling out department-wide and creaking | Designed for individuals and small teams | Move to Copilot Studio before the rollout, not after |

## Key terms

**Agent Builder** — the natural-language agent builder inside Microsoft Copilot, for lightweight
question-and-answer agents over organisational content.

**Declarative agent** — instructions, knowledge and actions running on Copilot's own orchestrator and
models, with no additional hosting ({{topic:stack}}).

**No new privileges** — the governance principle that an agent surfaces only content its user could
already open ({{topic:visibility}}).

**Copy to Copilot Studio** — the documented upgrade path, preserving core configuration and
instructions.
