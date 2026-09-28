## TL;DR

An agent is a model, plus instructions, plus knowledge and tools, plus a **loop that decides what to do
next**. It can answer, search, call a system, run an automation, ask a clarifying question, or hand over
to a person — and it chooses which, each turn, within the limits you set. A chatbot follows a path you
drew. An agent picks its own, which is why it covers requests you never anticipated and why you cannot
fully enumerate what it will do.

## Why it matters

The word is used for everything, which makes it useless as a specification. What is not vague is the
consequence: once something decides its own next step, the questions that matter change.

- With a workflow you ask *"is the logic right?"*
- With an agent you ask *"what could it decide to do, and what is the worst of those?"*

That second question is the origin of least-privilege tool identities ({{topic:connauth}}), of approvals
({{topic:hitl}}), of moderation and injection handling ({{module:safety-and-moderation}}), and of
evaluation ({{module:testing-and-evaluation}}). All of it follows from the loop.

## How it works

```mermaid
flowchart TB
  A[User message] --> B[Orchestrator]
  B --> C{"What should<br/>happen next?"}
  C -->|Answer| D["Reply from instructions<br/>and context"]
  C -->|Search| E[Knowledge]
  C -->|Act| F[Tool, flow or another agent]
  C -->|Ask| G[Clarifying question]
  C -->|Escalate| H[Human]
  E --> B
  F --> B
  D --> I[Response]
  G --> I
```

The parts:

| Part | Is |
|---|---|
| **Model** | The language ability. Reads, writes, decides ({{topic:models}}) |
| **Instructions** | Identity, scope, rules, tone. Read every turn ({{module:writing-instructions}}) |
| **Knowledge** | Content it can retrieve from ({{module:knowledge-and-rag}}) |
| **Tools** | Things it can do ({{module:tools-connectors-mcp}}) |
| **Skills** | Written procedures for kinds of task, on harnesses that support them ({{module:agent-skills}}) |
| **Orchestrator** | The thing that decides. The subject of {{topic:orchestration}} |
| **Harness** | The runtime all of this sits in ({{topic:harness}}) |

Three properties follow, and each one surprises somebody.

**It is not deterministic.** The same question can take a different route twice. Anything that must be
identical every time belongs in a flow or a query, not in the agent's judgement.

**Its reach is exactly its tools.** An agent cannot do anything it has no tool for, and it can do
anything it has a tool for. There is no middle ground and no instruction that creates one.

**It is only as good as what it is given.** The loop is the same in a useless agent and an excellent
one. The difference is the instructions, the knowledge, the tools and their descriptions — and all of
that is re-sent on every turn, which has a cost you will meet in {{topic:contextcost}}.

### Agent, chatbot, workflow

| | Decides its next step | Handles the unanticipated | Predictable |
|---|---|---|---|
| **Chatbot** | No — you drew the path | No | Yes |
| **Workflow** | No — you wrote the logic | No | Yes |
| **Agent** | Yes | Yes | No, not fully |

None of these is better. Real systems use all three, and the skill is putting each where it belongs —
which is what {{topic:skillsvs}} and {{topic:triage}} are about.

## In practice at Technik

The Technik Production Assistant is an agent because its users will not stay on a path.

Someone in production control starts with *"which work orders are late to start Coating this week?"*,
narrows to Plant 1, points at one of them, asks what is holding it up, and asks for a note to the
supervisor. Nobody drew that path. A chatbot would need every branch enumerated; the agent needs a query
tool, notification data, and instructions about what to do when something is blocked.

That third question is worth pausing on. *"What is holding it up"* has no field to read: a work order is
blocked when its current operation is `INPROC` **and** an open notification names that work order, and
the agent works it out by joining. Deciding to make that join is the loop doing its job.

But look at what is *not* left to judgement, because this is the part people get wrong:

| Part of that conversation | Mechanism | Why not judgement |
|---|---|---|
| Validating the work order number's format | **The tool's own input contract** | The check must happen every time, identically. On the standard harness a topic would guarantee it; on this harness the tool has to ({{topic:chooseharness}}) |
| The query behind "late to start Coating" | **A tool over a view** ({{topic:sfviews}}) | The definition of "late" must not vary between answers |
| Which document governs an acceptance criterion | **An instruction** | Source precedence is a rule, not a preference |
| Creating a record in SAP | **A flow with an approval** ({{topic:approvals}}) | Irreversible |

The agent decides *what to do*. It does not decide *what the numbers mean*. Keeping that line clear is
most of what separates an assistant people trust from one they check by hand.

> [!TIP]
> When someone proposes "an agent for X", ask what it would be allowed to *do*, not what it would be
> able to answer. The tool list is the design; everything else is wrapping.

## Design guidance

- **Give it the smallest set of tools that covers the job.** Reach is exactly the tool list.
- **Write descriptions as carefully as instructions.** They are what the loop decides with
  ({{topic:tooldesc}}).
- **Put anything that must be identical every time outside the agent's judgement.**
- **Assume it will be asked things you did not plan for.** That is the reason you chose an agent.
- **Design the failure case.** What it says when it cannot help is part of the product.
- **Decide early what it may do without asking**, and build the confirmation ({{topic:hitl}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Inconsistent answers to the same question | It is an agent; the route varies | Move the part that must be consistent into a tool, a view or a flow |
| "It should just know that" | The knowledge or tool does not exist | Reach is exactly what you gave it |
| It does something nobody wanted | A tool existed for it | Remove the tool, or gate it behind a confirmation |
| Impossible to say what it will do | That is the nature of the loop | Constrain with tools; evaluate with a fixed set ({{topic:testsets}}) |
| Built as an agent, behaves like a bad chatbot | Everything was forced into scripted paths | Let the orchestrator do its job ({{topic:orchestration}}) |
| Built as an agent, should have been a flow | The task never needed judgement | Use a flow: cheaper, testable, auditable ({{topic:agentflows}}) |

## Key terms

**Agent** — model, instructions, knowledge and tools, plus a loop that decides the next step.

**Orchestrator** — the component that makes that decision ({{topic:orchestration}}).

**Harness** — the runtime the whole thing runs in ({{topic:harness}}).

**Tool** — something the agent can do. Its reach ({{topic:tools}}).

**Autonomous agent** — one started by an event rather than a person ({{topic:autonomous}}).
