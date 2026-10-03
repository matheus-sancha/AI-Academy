## TL;DR

An agent flow is the **standard harness's** deterministic automation, built inside Copilot Studio with the
same trigger-and-action model as Power Automate. Its job is to give an agent a process it can call as
**one tool**, with defined inputs and outputs, so that the steps run identically every time. To be callable
it needs the **When an agent calls the flow** trigger and a **Respond to the agent** action. It must be
published and answer within **100 seconds**. Every action it runs consumes Copilot Studio capacity. On the
GitHub Copilot harness the same job belongs to a workflow ({{topic:workflows}}).

## Why it matters

The orchestrator decides what to call, in what order, with what arguments. That is the right design for
open questions and the wrong one for a process. If an answer depends on running query A, then query B only
when A returns something, and then combining them by a rule, leaving that sequence to the model means it
will sometimes run one step, sometimes both and sometimes combine them differently.

An agent flow moves the sequence out of the model's hands. The agent decides *whether* to call the
process. The flow decides *how* it runs. This is the mechanism {{topic:triage}} relies on when it sends a
fixed multi-step process out of the instructions, and the one {{topic:hitl}} relies on for out-of-band
approvals.

## How it works

### What a flow is for, before what it does

| Designer | Lives in | Called by | For |
|---|---|---|---|
| Cloud flow | Power Automate | Events, schedules, buttons | Work with nobody in a conversation ({{topic:cloudflows}}) |
| **Agent flow** | Copilot Studio, standard harness | An agent, a topic, a schedule or an event | A fixed process an agent hands off to |
| Workflow | Copilot Studio, GitHub Copilot harness | The same | The same job, with AI steps built in ({{topic:workflows}}) |

Agent flows are made of the same parts as cloud flows: a trigger and at least one action. The action
catalogue covers **AI capabilities** (run a prompt, process a document, call an agent), **human in the loop**
(approvals, requests for information), **built-in tools** (conditions, loops, data operations, child
flows) and **connectors**. Microsoft describes them as deterministic: "the same input always produces the
same output." Strictly, that holds for the non-AI steps. A prompt inside a flow is still a model.

### What makes a flow callable as a tool

| Requirement | Why |
|---|---|
| **When an agent calls the flow** trigger | Declares the inputs the agent must supply |
| **Respond to the agent** action | Declares the outputs the agent gets back |
| **Asynchronous response** off | The agent waits for the answer in the same turn |
| **Published** | Only published flows appear in the tool list |
| **Under 100 seconds** | The action limit. Return only the fields the agent needs |

A flow can be added at the **agent level**, where the orchestrator may call it whenever its description
fits, or to a **single topic** as an action node, where it runs only at that point in the script. The
description you write when adding it is the routing signal ({{topic:tooldesc}}).

### What it costs

Every action a flow executes consumes Copilot Studio capacity, on top of what triggered it:

| Run from | Consumes |
|---|---|
| A topic | One classic answer, plus the flow's actions |
| Generative orchestration | One autonomous action, plus the flow's actions |
| The test chat or the flow designer | Nothing for the flow's actions |

<!-- volatile verified=2026-10 -->
When an environment's prepaid capacity runs out, **new** runs are blocked until capacity returns, while runs
already under way finish. Microsoft 365 Copilot licensed users and test runs are not affected.
Pay-as-you-go billing is the documented way to avoid the interruption.
<!-- /volatile -->

The free test does not extend to AI steps inside the flow. Prompts and models in agent flows always consume
Copilot Credits, even from the test panel ({{topic:aibuilder}}).

Agent flows live in solutions, which give them drafts, versions, export and import ({{topic:solutions}}).
An existing cloud flow can be converted into one, one-way.

## In practice at Technik

The Production Assistant runs on the GitHub Copilot harness ({{topic:chooseharness}}), so its own flows are
workflows. The agent-flow version below is the standard-harness design, behind the *Work order status*
topic from {{topic:topics}}.

**The problem.** A work order is *blocked* when its current operation is `INPROC` and an open quality
notification names that work order. There is no blocked flag, so the answer needs two reads and a rule.
Given two connector actions, the orchestrator sometimes ran only the first and reported `100004521` as
*in process* while QN `300001234` was holding it up.

**The flow.** *Get work order status*:

| Step | Action |
|---|---|
| Trigger | **When an agent calls the flow**, input `WorkOrderNumber` (text) |
| 1 | Query `V_WORK_ORDER_OPERATIONS` for that work order's current operation and status |
| 2 | If the operation is *In progress* (`INPROC` in SAP), query `SAP_QUALITY_NOTIFICATIONS` for open QNs on the work order |
| 3 | Compose: status in words, current operation, and `BlockedBy` set to the QN numbers, or empty |
| Respond | `Status`, `CurrentOperation`, `BlockedBy` |

Both queries run as `TECHNIK_AGENT_RO`. The flow returns three fields, not the rows behind them, which keeps
it far inside 100 seconds and keeps the agent's context small. Added to the topic, each status question costs
one classic answer plus about five actions. Added at agent level, the same question costs one autonomous
action plus the same actions.

The rule now runs the same way on every call. The agent's remaining job is the one it is good at: explaining
to a planner what *blocked by `300001234`* means for their day.

## Design guidance

- **Use an agent flow when the sequence is the requirement.** If the steps or the rule must not vary, they
  do not belong to the orchestrator.
- **Design the inputs and outputs first.** They are the tool's contract with the agent.
- **Return fields, not rows**, and stay well under 100 seconds.
- **Describe the flow for routing**, the same way you would describe any tool.
- **Count actions when you cost it.** Every action is capacity, on every call.
- **Build it on the harness the agent is on.** On the GitHub Copilot harness, build a workflow.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The flow is not in the agent's tool list | Missing trigger or response action, or not published | Add both, publish, then add the tool |
| The agent's call times out | The flow takes over 100 seconds, or responds asynchronously | Trim queries and outputs; set *Asynchronous response* off |
| The agent sometimes skips a step of the process | The steps are separate tools the orchestrator chains | Wrap them in one flow |
| Flows stop running mid-month | Prepaid Copilot Studio capacity exhausted | Monitor capacity; enable pay-as-you-go |
| Testing a flow with a prompt in it used credits | AI steps in agent flows always consume Copilot Credits | Budget test runs of AI steps |
| The flow cannot be found from a GitHub Copilot harness agent | Agent flows belong to the standard harness | Build it as a workflow |

## Key terms

**Agent flow** — a deterministic automation built in Copilot Studio on the standard harness, callable by an
agent as one tool.

**When an agent calls the flow** — the trigger that makes a flow callable, and declares its inputs.

**Respond to the agent** — the action that returns the flow's outputs to the agent.

**Agent-level tool** — a flow the orchestrator may call whenever it fits.

**Topic-level tool** — a flow that runs only at a fixed point in one topic.

**Copilot Studio capacity** — the prepaid or pay-as-you-go allowance that flow actions consume.
