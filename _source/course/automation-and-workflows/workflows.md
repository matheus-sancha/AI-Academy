## TL;DR

Workflows are the **GitHub Copilot harness's** automation designer, and the kind of flow its agents call
as tools. Underneath, they are the same trigger-and-action model as agent flows. What they add is AI as a
first-class step. **Classify** and **extract** actions are built in, and an **agent node** hands a single
step to an agent that can reason, use tools and read knowledge, then returns text or a structured object
the rest of the workflow can branch on. Each node can be tested on its own. Use a workflow to mix fixed
business logic and judgement in one process, with the judgement confined to the step that needs it.

## Why it matters

The Production Assistant runs on the GitHub Copilot harness ({{topic:chooseharness}}). Its tool list offers
three kinds of tool: connectors, MCP servers and workflows. Agent flows are not among them. So every fixed
process the assistant hands off, which {{topic:triage}} sends out of the instructions, is built here. On
this harness, "make it a flow" means "make it a workflow".

The second reason is design. A process that needs one judgement in the middle (*is this notification
really a cladding defect?*) used to force a choice. Either the whole thing became an agent and lost its
determinism, or the judgement was squeezed into a prompt with its output parsed by hand. A workflow keeps the
process deterministic and gives the judgement a node with a declared output shape.

## How it works

### Same skeleton, more node types

A workflow is a trigger and at least one action, triggered manually, on a schedule, by an event or by an
agent. The node types are:

| Node | Does |
|---|---|
| **Connectors** | Read and write external systems, as in any flow |
| **Built-in tools** | Conditions, loops, data operations, child workflows |
| **AI actions** | Run a prompt, process a document, classify, extract, call an agent |
| **Human in the loop** | Stop and ask a person for information |

Conditions take several branches rather than only *yes* and *no*. Each publish is saved to the version
history, so an earlier version can be compared or restored.

### The agent node

The agent node is the feature that defines the designer. It calls either an **existing published agent**
or an **inline agent** built inside the node:

| | Existing agent | Inline agent |
|---|---|---|
| Configured | On the agent, elsewhere | In the node: instructions, model, tools, knowledge, output |
| Per-run prompt | A **Message** field with dynamic content | The **Instructions** field doubles as the prompt |
| Reuse | Shared across workflows and channels | Scoped to this workflow only |

Tools are MCP servers and connector actions. Knowledge is SharePoint or public websites. **Work IQ** can be
switched on to ground the agent in the running user's mail, Teams and files ({{topic:workiq}}).

The **Output** setting decides how the rest of the workflow uses the answer:

| Output | Returns | Use when |
|---|---|---|
| Text response | One string | The next step only inserts it into a message |
| Structured output | Named fields | Consistent fields without writing a schema |
| Custom structured output | An object matching your JSON schema | Later steps branch on a field, write it to a column or send it to an API |

Each structured field becomes its own dynamic-content token, so a condition can test `priority` directly.
**Request human assistance when unsure** lets the agent email the connection owner and wait for a reply
before continuing.

### Testing a node, not the run

Select a node and run it from its **Test** tab, with typed inputs or inputs from a previous run, without
running the workflow around it. Inline agent nodes can then be **evaluated**: describe what a good response
looks like as test methods, and each one returns pass or fail with its reasoning. The documented limits are
five generated test methods and 20 evaluations per node per day.

### As a tool

<!-- volatile verified=2026-10 -->
Adding a workflow to a GitHub Copilot harness agent is documented as a preview. The requirements match agent
flows ({{topic:agentflows}}): a **When an agent calls the flow** trigger, a **Respond to the agent** action,
asynchronous response off, published, and an answer within **100 seconds**. A published workflow is listed
on the **Workflows** page and can be used by other agents.
<!-- /volatile -->

Workflow actions consume Copilot Studio capacity, and on this harness building and testing consume Copilot
Credits too ({{topic:licensing}}). A Power Automate flow **cannot be converted** into a workflow. It is
rebuilt.

<!-- unknown since=2026-10 -->
Whether AI actions and agent nodes inside a workflow are billed like prompts in agent flows, which always
consume Copilot Credits even in a test. The licensing page names agent flows only.
<!-- /unknown -->

## In practice at Technik

The quality lead wants a morning list of yesterday's new quality notifications, with any whose priority
looks wrong for the defect pulled out for review. Most of that is fixed logic. One step is judgement.

| Node | Kind | Detail |
|---|---|---|
| Trigger | Schedule | Weekdays, 06:30, after the nightly replication |
| `Get yesterday's QNs` | Connector | Snowflake, as `TECHNIK_AGENT_RO`: `SAP_QUALITY_NOTIFICATIONS` created since the last run |
| `For each QN` | Loop | Over the returned rows |
| `Check priority` | Agent node, inline | Grounded in `SOP70000101`; **no tools**; custom structured output |
| `Route` | Condition | `priority_matches` false → the review list; true → the digest |
| `Post the digest` | Connector | Teams, one message to the quality channel |

The inline agent's instructions say what it receives (one QN's defect type, operation, priority and
description), what to judge (whether the priority fits the rules in `SOP70000101`) and what to return:

```json
{ "qn": "300001234", "priority_matches": false,
  "suggested_priority": "High", "reason": "Through-wall porosity on cladding; SOP section 4 rates it High." }
```

Three choices in that design are deliberate.

**The agent node has no tools.** QN descriptions are free text from the shop floor, and `300001267` carries
an injected instruction ({{topic:injection}}). With nothing to call, the worst it can do is return a wrong
field. That field lands on a review list a person reads.

**The output is a schema, not prose.** The condition tests a boolean. Nothing downstream parses a sentence.

**The judgement suggests and the quality lead decides.** The workflow never changes a priority in SAP.

The assistant's own process tools are workflows for the same harness reason. *Get work order status* from
{{topic:agentflows}} is rebuilt here, node for node.

## Design guidance

- **On the GitHub Copilot harness, a process tool is a workflow.**
- **Keep the judgement to one node.** Gather inputs before it, act on its output after it.
- **Use custom structured output wherever a later step branches.**
- **Give an agent node the fewest tools that will do**, and none when it reads untrusted text.
- **Inline agents for one-off judgement**, existing agents for reused ones.
- **Test nodes as you build**, and evaluate the agent node before you publish.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The workflow is not offered as a tool | Missing trigger or response node, or not published | Add both and publish |
| A condition on the agent's answer never matches | Text output being compared as if it were a field | Switch to custom structured output and test the field |
| An agent node follows instructions found in the data | It holds tools and reads untrusted text | Remove the tools; route its output to a person |
| The same inline agent appears in several workflows | Inline agents cannot be shared | Publish it as an agent and call that |
| Evaluations stop for the day | 20 evaluations per node per day | Plan evaluation runs; fix several things between runs |
| A colleague's Power Automate flow cannot be brought across | No conversion to the workflow format | Rebuild it as a workflow |

## Key terms

**Workflow** — the GitHub Copilot harness's automation, built in Copilot Studio's redesigned designer.

**Agent node** — a workflow step that hands one task to an existing or inline agent.

**Inline agent** — an agent configured inside a node and scoped to that workflow.

**Custom structured output** — an agent node's answer shaped by a JSON schema you define.

**Node-level testing** — running one node with chosen inputs, without running the whole workflow.
