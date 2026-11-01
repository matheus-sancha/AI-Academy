## TL;DR

A capable harness breaks a goal into steps, notices when a step fails, retries and tries another path.
Almost none of that is the model's doing, and almost all of it is yours. You improve planning from
outside: a goal narrow enough to finish, tool errors written so the model can act on them, checkpoints
that let a run resume instead of restart, and deterministic code for the steps that must never vary.
Copilot Studio makes this a harness choice — one harness "Retries and finds alternative paths
automatically" while another "Follows the paths you built". In your own code it is a design choice.

## Why it matters

Planning is where agents look most impressive and fail most expensively. The failure is rarely a wrong
answer; it is a run that spends twenty minutes bouncing between two tools, or one that quietly gives up
halfway and reports success.

It also decides what you can safely automate. An agent that recovers from a bad identifier can be given
a whole task; one that stops dead needs someone watching, which turns a background job back into a
conversation ({{topic:autonomous}}).

And it is the first place pro-code beats configuration. Azure's guidance is explicit: some patterns
route deterministically, others let agents choose their own routes, and "If your agents are defined in
a no-code or low-code environment, you might not control those behaviors."

## How it works

### Choosing how much planning you want

Copilot Studio settles planning by picking a harness. Its GitHub Copilot harness takes "a goal, break
it into steps, call the right tools across connectors, knowledge, MCP, and connected agents, and
adjust when a step fails or a request changes", and recovers by retrying and finding alternative paths.
The Customer Conversation harness recovers by escalating to a human through a defined path. The
standard harness follows the paths you built. And the choice is not free: "The harness you use affects the billing, features, and capabilities of what you build"
({{topic:chooseharness}}).

In code the equivalent decision is a complexity ladder. If prompt engineering solves the problem you
do not need an agent. A single agent with tools is "Often the right default for enterprise use cases"
— and even there, "To guard against infinite tool-call loops, set iteration limits". Multi-agent
orchestration "Adds coordination overhead, latency, and failure modes". The rule: "Use the lowest
level of complexity that reliably meets your requirements."

### Planning as an artifact

The orchestration pattern built for open-ended work, **magentic**, makes the plan a thing you can
inspect. A manager agent "builds a task ledger to develop the approach plan with goals and subgoals,
which is eventually finalized, followed, and tracked", then "regularly checks whether the original
request is satisfied or stalled and updates the ledger to adjust the plan". A documented plan "can be
presented to a user before allowing the agents to follow the tasks". Avoid it when work is
time-sensitive: it "focuses on building and debating viable plans, not optimizing for speed", and its
cost is the hardest to predict.

The **maker-checker** loop is the cheap version: one agent produces, another evaluates against clear
acceptance criteria. The instruction that matters is "Set an iteration cap to prevent infinite
refinement loops, and define fallback behavior for when the cap is reached" — escalation to a human
reviewer, or the best available result with a quality warning. Agent Framework provides this and the
other four patterns as built-in orchestrations, with human-in-the-loop support for approvals and
feedback ({{topic:mafworkflows}}).

### Recovery, concretely

Azure's reliability guidance treats an orchestration as a distributed system, with node failures,
message loss and cascading errors. The measures it asks for:

- implement timeout and retry mechanisms, and graceful degradation when an agent faults;
- "Surface errors instead of hiding them," so downstream logic can respond;
- "Validate agent output before you pass it to the next agent" — then retry, request clarification,
  or halt rather than let bad input propagate;
- "Consider circuit breaker patterns for agent dependencies";
- isolate agents so they do not share a single point of failure, including a shared model endpoint
  that rate-limits when several agents run at once;
- use your SDK's checkpoint features to recover from an interrupted run, "such as from a fault or a
  new code deployment".

Human gates are part of recovery, not an exception to it. "Mandatory gates make the orchestration
synchronous at that step, so persist state at these checkpoints to resume operation without a replay
of prior agent work." And they can be narrowed: gates can be scoped "to specific tool invocations
rather than full agent outputs so that the orchestration can proceed autonomously for low-risk
actions" ({{topic:hitl}}).

## In practice at Technik

The capstone's agent has no retry policy and does not need one, because its recovery is carried by its
tool errors. When an operation has no linked items, the server does not say *not found*:

*From [`server/teamcenter.py`, lines 116–127](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/server/teamcenter.py#L116-L127):*

```python
def no_items(work_order, operation_seq):
    """Say why an operation has no linked items: it has none, or the operation does not exist."""
    ops = rows("""SELECT OPERATION_SEQ, OPERATION FROM V_WORK_ORDER_OPERATIONS
                  WHERE WORK_ORDER = %(wo)s ORDER BY OPERATION_SEQ""", wo=work_order)
    if not ops:
        raise ToolError(f"No released work order {work_order}. Check the number with the user.")
    for op in ops:
        if op["OPERATION_SEQ"] == operation_seq:
            return f"{work_order} operation {operation_seq} ({op['OPERATION']}) uses no drawing, " \
                   "CNC program or work instruction in Teamcenter."
    listed = ", ".join(f"{op['OPERATION_SEQ']} {op['OPERATION']}" for op in ops)
    raise ToolError(f"Work order {work_order} has no operation {operation_seq}. Its operations are: {listed}.")
```

Three distinct outcomes, each actionable. An operation that genuinely links nothing is a normal answer.
A work order that does not exist tells the model to check the number with the user rather than guess.
And an operation sequence that is wrong comes back with the sequences that exist, so the agent recovers
on its next pass instead of trying `0020`, `0030`, `0040` in turn. This is planning improved entirely
from the tool's side ({{topic:tooldesc}}).

The deterministic half is just as deliberate. Technik's operations data has confirmations posted
twice, and welding at Plant 1 reads 110.9% efficient until the stale postings are dropped. That rule
is not something an agent should rediscover per run: it lives in `V_WORK_ORDER_OPERATIONS`, which the
agent's role reads instead of the table ({{topic:qualify}}, {{topic:sfviews}}).

Where the agent must stop rather than recover is also fixed in advance. Drafting a revision of
`SWI70000318` belongs to the document's owner, so the instruction layer tells the agent to look the
owner up, decline, and name them — and a middleware guard makes the refusal true whatever the model
decides ({{topic:loop}}, {{topic:stageagent}}).

## Design guidance

- **Write tool errors for the model as a reader.** Say what was wrong and what exists; an error that
  only says *not found* forces a guess.
- **Cap the refinement loop and define the fallback.** A cap without a fallback is a silent failure.
- **Keep judgement-free steps out of the plan.** A business rule in a view or a flow runs identically
  every time ({{topic:detvsagentic}}).
- **Treat a mandatory human gate as synchronous** and persist state at it, so an approval that arrives
  tomorrow does not replay today's work.
- **Scope approvals to the risky tool call**, not to whole answers, so low-risk steps keep running.
- **Give the agent a goal narrow enough to be finishable** — and a way to say it cannot.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent tries variations of a failing call | The error text named no alternative | Return the valid options in the error ({{topic:errors}}) |
| A run reports success having skipped a step | Errors were swallowed rather than surfaced | Surface errors; validate output before passing it on |
| Two agents keep handing work back and forth | A handoff topology with no completion test | Route deterministically when the right specialist is known from the input |
| An approval arrives and the run starts over | No state persisted at the gate | Checkpoint at every mandatory gate |
| A long run dies on a deployment | Nothing persisted outside the process | Use the SDK's checkpoints; store progress durably |
| The plan is good and the result varies anyway | A deterministic rule was left to the model | Move it into SQL, a view or a flow |
| Planning is slow on a simple request | A plan-building pattern used where a single agent would do | Drop a rung down the complexity ladder |

## Key terms

**Task ledger** — a written plan of goals and subgoals that a manager agent maintains, tracks and
revises as a run proceeds.

**Maker-checker** — a loop in which one agent produces and another evaluates against acceptance
criteria, bounded by an iteration cap.

**Circuit breaker** — stopping calls to a dependency that keeps failing, instead of retrying into it.

**Checkpoint** — persisted progress a run can resume from after a fault, a deployment or a human gate.

**Stall** — a run that is neither finished nor progressing, which a planner has to detect explicitly.
