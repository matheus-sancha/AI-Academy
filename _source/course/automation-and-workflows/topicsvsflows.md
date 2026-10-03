## TL;DR

Three kinds of logic, three homes. A **scripted conversation**, which must ask, confirm and branch the same way
every time, is a **topic**. A **business process**, which must run the same steps every time and often has
nobody in a conversation, is a **flow**: a cloud flow, an agent flow or a workflow. An **open-ended request** that
needs judgement belongs to the **agent**. Real solutions combine all three, in both directions: agents call
flows as tools, and flows call agents for one step. One harness detail changes the map. The GitHub Copilot
harness has no topics, so a scripted path there becomes a rule in the instructions, enforced by a tool.

## Why it matters

Each of the earlier lessons in this module explains one designer. This one decides between them, and the triage
that started in {{topic:triage}} ends here. Once a requirement is known to be a tool, the remaining question is
what kind of logic sits behind it.

Most of the mistakes run in one direction: giving judgement work that should be fixed. A status rule left to the
orchestrator is applied differently on different turns. A weekly reminder built as an agent conversation adds a
model, and a bill, to something a schedule could do. The opposite mistake is rarer but real: a topic that tries
to script a question with a thousand phrasings.

## How it works

### Microsoft's distinction

Microsoft's FAQ treats topics and agent flows as the same kind of thing with different jobs. Both are
deterministic: "given the same inputs, they'll always produce the same output." **Topics are optimised for
conversations**, and can call actions behind the scenes. **Agent flows are optimised for business processes**,
with fuller automation for work that is not a conversation. The agent is the third option, and the only one that
is not deterministic. Use it where the path cannot be drawn in advance.

### Four questions, in order

| Ask | If yes | Built as |
|---|---|---|
| Does it run with nobody in a conversation, on a schedule or an event? | **Flow** | A cloud flow, unless an agent will also call it |
| Must its steps or its rule run identically every time? | **Flow**, called as one tool | An agent flow on the standard harness, a workflow on the GitHub Copilot harness |
| Must the *conversation* follow a fixed path: collect, confirm, branch? | **Topic** | Standard harness only. On the GitHub Copilot harness, an instruction plus a tool that checks the value |
| None of the above: the request needs interpretation | **Agent** | Instructions, knowledge and tools, chosen by the orchestrator |

A flow can still contain judgement. A workflow's agent node, or a prompt inside any flow, handles one step that
needs a model ({{topic:workflows}}, {{topic:prompts}}). The process around it stays fixed.

### Which flow

| | Cloud flow | Agent flow | Workflow |
|---|---|---|---|
| Built in | Power Automate | Copilot Studio | Copilot Studio |
| Harness | — | Standard | GitHub Copilot |
| Paid by | A Power Automate licence | Copilot Studio consumption | Copilot Studio consumption |
| Sharing | Copy, share, co-owners, run-only users | None of those four | Usable by other agents once published |
| Shown on Copilot Studio's Flows page | No, managed in Power Automate | Yes | On the Workflows page |

To be added to an agent, an agent flow must be a **solution flow** with the **When an agent calls the flow**
trigger and **Respond to the agent**. Agent flows can use premium connectors, and cannot call desktop flows. A
cloud flow can be converted into an agent flow one way, and never into a workflow ({{topic:cloudflows}}).

### Combining them

| Direction | Mechanism |
|---|---|
| Agent → flow | The flow is a tool, chosen by its description ({{topic:agentflows}}) |
| Topic → flow | The flow is an action node at one point in the script |
| Flow → agent | A workflow's agent node, or a *call an agent* action |
| Flow → person | An approval or a request for information ({{topic:approvals}}) |

## In practice at Technik

Six requirements, one per row:

| Requirement | Home | Why |
|---|---|---|
| Remind owners that `SOP70000114`, `SWI70000318` and `TDS70000044` are past review | **Cloud flow** | A schedule, and nobody asks anything |
| *What's the status of `100004521`?* | **Workflow** tool + instructions | Two reads and the blocked rule must run identically. On the standard harness, a topic calling an agent flow |
| *Why is `PRJ-2031` behind?* | **Agent** | No fixed path: work orders, operations and QNs, weighed together |
| A morning list of new QNs, with doubtful priorities pulled out | **Workflow** with one agent node | A fixed process with one judgement in it |
| Revision C of `SWI70000318` | **Agent**, then **cloud flow**, then a **person** | The skill drafts, the owner's flow gets approval, the owner releases |
| Supplier certificates | **Cloud flow** with a document model | Extraction, validation and review. No conversation, no agent ({{topic:docproc}}) |

Three rows are worth arguing with.

**The status question has no topic.** On the standard harness, the *Work order status* topic asks for a valid
work order number before anything runs ({{topic:topics}}). The Production Assistant is on the GitHub Copilot
harness, so the guarantee moves. The instructions say to ask for the number, and the workflow refuses an
invalid one and says why. The check still always happens, but at the point the value is used rather than in
the conversation.

**The certificates have no agent at all.** Every step is AI or fixed logic, and nobody chats with it. Adding the
assistant would add a conversation nobody needs and a model call that decides nothing.

**The revision uses all three, and the boundaries are the design.** The agent's judgement ends at a draft. The
process starts when the owner submits it. The irreversible release stays with a person in Teamcenter. Each
handover is a point where someone can see the work before it moves on.

## Design guidance

- **Give judgement only the steps that need it.** Everything that can be drawn in advance is a flow.
- **No conversation, no agent.** A schedule or an event is a cloud flow.
- **On the GitHub Copilot harness, a scripted path is an instruction plus a tool that checks.**
- **Pick the flow designer by the harness and by who pays.**
- **Put judgement inside a process as one node**, with a structured output.
- **Draw the handovers.** Where the agent stops, where a flow starts, where a person decides.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A rule is applied differently on different turns | Process logic left to the orchestrator | Move the steps into one flow and call it as a tool |
| A scheduled job runs as an agent conversation | Built in the wrong designer | Rebuild it as a cloud flow |
| A topic grows a branch for every phrasing | Judgement scripted as a conversation | Hand that path to the agent |
| A flow made in Power Automate is missing from Copilot Studio | The Flows page shows only agent flows | Convert it, or manage it in Power Automate |
| A colleague cannot co-own an agent flow | Agent flows cannot be shared or co-owned | Put it in a solution and manage access there ({{topic:solutions}}) |
| The assistant cannot find a flow to call | It is an agent flow, and the assistant is on the GitHub Copilot harness | Rebuild it as a workflow |

## Key terms

**Topic** — a scripted conversation path on the standard harness.

**Flow** — a deterministic process: a cloud flow, an agent flow or a workflow.

**Agent** — the orchestrator, given instructions, knowledge and tools, for requests that need judgement.

**Handover** — the point where work passes from an agent to a flow, or from a flow to a person.
