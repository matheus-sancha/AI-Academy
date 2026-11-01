## TL;DR

Every agent runs the same loop: read the goal and the context, decide on an action, call a tool, read
what came back, repeat. The **harness** is the code that runs that loop — and almost everything you
tune is outside the model. Two things matter most. The loop needs **ground truth** at every step, which
means a real tool result rather than the model's own account of what it did; and it needs an explicit
**stop condition**, because nothing else will end it. A loop with no cap is a bill, and a loop whose
steps aren't grounded is a confident story. Microsoft's Agent Framework ships an opinionated harness
with both: a configurable per-request iteration limit, and middleware you can hang your own rule on.

## Why it matters

You have already shipped an agent that ran a loop you could not see. Copilot Studio's generative
orchestration chose knowledge, tools and topics from the descriptions you wrote
({{topic:orchestration}}), and the loop underneath was the platform's business. Pro-code moves that
loop into your repository. You now own the thing that decides when to stop.

That ownership is mostly about cost and compounding. Anthropic's guidance is blunt about the trade:
"The autonomous nature of agents means higher costs, and the potential for compounding errors." Each
pass through the loop spends tokens on the whole accumulated context ({{topic:budget}}), and each
ungrounded step becomes the input to the next one. An agent that misread a revision letter on pass two
will happily reason about it for four more passes.

It also matters because the loop is where enforcement actually lands. Instructions ask; code decides.
If a rule must hold every time — never answer without a tool result, never exceed six tool calls — the
place to put it is the loop, not the prompt.

## How it works

### The loop itself

Anthropic describes an autonomous agent plainly: they are "typically just LLMs using tools based on
environmental feedback in a loop." The feedback is the point. The guidance is that "it's crucial for
the agents to gain 'ground truth' from the environment at each step (such as tool call results or code
execution) to assess its progress," and that agents "can then pause for human feedback at checkpoints
or when encountering blockers."

Termination has two forms: "The task often terminates upon completion, but it's also common to include
stopping conditions (such as a maximum number of iterations) to maintain control." No number is
recommended: the right number is a property of your task.

The same guidance draws a line worth keeping: a **workflow** is a system where models and tools "are
orchestrated through predefined code paths", while an **agent** is one where models "dynamically
direct their own processes and tool usage". Both are agentic systems. Only one of them has a loop whose
length you cannot predict ({{topic:detvsagentic}}).

### What a harness adds around it

Agent Framework documents a harness as "the runtime scaffolding that turns a language model into an
agent that can perform work" — it drives model and tool calls, manages conversation state and context,
applies approval policies, and keeps the agent progressing through a multistep task. Its architecture
is five layers, and they are a useful map of everything this module covers:

1. the **chat client**, which connects the agent to a model;
2. the **chat pipeline**, adding function invocation, message injection, history persistence and
   optional compaction;
3. the **agent and context providers** — session instructions, tools, memory, todo state and operating
   modes;
4. **middleware and decorators**, for approval handling, observability and optional bounded looping;
5. the **application UX**, which streams responses and collects input such as tool approvals.

<!-- volatile verified=2026-11 -->
The harness composes existing building blocks rather than defining a separate runtime, so what you get
back is an ordinary agent:

```python
from agent_framework import create_harness_agent

agent = create_harness_agent(client=client, harness_instructions="...", max_output_tokens=16_384)
session = agent.create_session()
response = await agent.run("Draft the change summary for ECN70000042.", session=session)
```

Several capabilities are on by default: todo tracking, plan and execute modes, session file memory,
standing approvals and auto-approval rules, and OpenTelemetry. Each has a `disable_` parameter.
Harness instructions are placed **before** your own agent instructions. Background agents, file access
and looping are documented as experimental.
<!-- /volatile -->

Two mechanisms bound the loop. Function invocation is "Enabled with a configurable per-request
iteration limit", and looping is "Optional bounded re-invocation driven by evaluators or predicates" —
which is the maker-checker shape from {{topic:planning}}. Neither has a documented default number.

## In practice at Technik

The capstone's agent is a plain Agent Framework agent rather than the packaged harness, so its loop
controls are two lines of configuration:

*From [`agent/main.py`, lines 19–20](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/agent/main.py#L19-L20):*

```python
# Pass the server's ToolError messages to the model; by default it sees only "Error: Function failed."
TOOL_LOOP = {"include_detailed_errors": True, "max_function_calls": 6}
```

Six is not a round number. Walk the loop for a real question — *which drawing does operation 0010 of
work order 100004510 use, and is that revision still released?* Pass one calls
`list_operation_documents` and gets the drawing with the revision the operation was released against.
Pass two calls `get_revision_status` for that drawing and learns revision B is not the released one.
Pass three answers. That is two tool calls; six leaves room for a mistyped identifier, a retry, and the
third tool, without leaving room for a wander.

`include_detailed_errors` is the ground-truth half, and it was a surprise: without it the framework
hands the model `Error: Function failed.` and the server's carefully written error text never arrives
({{topic:planning}}).

The second control sits at the loop's exit rather than inside it:

*From [`agent/main.py`, lines 30–41](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/agent/main.py#L30-L41):*

```python
@agent_middleware
async def grounded_or_refuse(context: AgentContext, call_next):
    await call_next()
    if context.result is None:
        return
    if not context.stream:
        refuse_unless_grounded(context.result)
        return
    # The hosted server always streams. Hold the updates until the answer is final, check it,
    # and release only what passed: the answer, or the refusal in its place.
    context.result = context.result.with_result_transform(refuse_unless_grounded).buffer_updates(
        result_to_updates=lambda r: [AgentResponseUpdate(role=m.role, contents=m.contents) for m in r.messages])
```

`call_next()` is the whole loop. What follows it inspects the finished run, and if no message carries a
`function_result`, the answer came from the model's memory and is replaced with a fixed refusal. The
instructions ask for the same behaviour; this makes it true. Note the streaming branch: the first
version skipped streamed runs, and the hosted deployment streams every answer, so the guard silently
stopped firing ({{topic:stageship}}).

## Design guidance

- **Decide the stop condition before you need one.** Cap tool calls at the longest legitimate chain
  plus one retry, and write down why that number.
- **Give every step ground truth.** A tool result, an exit code, a test run — not the model's summary
  of its own work.
- **Pass tool errors through to the model.** A framework that hides them turns a recoverable step into
  a dead end.
- **Put invariants in the loop, not only in the prompt.** Middleware runs every time; instructions
  are followed most of the time.
- **Check your guard against streaming.** A rule written for a buffered response can disappear the
  day you deploy.
- **Keep the agent's steps visible.** Transparency about planning steps is a design principle, not a
  debugging luxury.
- **Start at the lowest complexity that works.** A single agent with good tools beats a loop you
  cannot predict ({{topic:multiagent}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Costs scale with nothing visible | No iteration limit; each pass re-sends the accumulated context | Set a per-request call limit; compact history ({{topic:history}}) |
| The agent insists it did something it did not do | A step with no ground truth — the model's own account was taken as the result | Require a tool result or an exit code per step |
| The model keeps retrying the same failing call | It never saw why the call failed | Turn on detailed tool errors; make error text actionable |
| A rule in the instructions holds in testing and fails in production | Instructions are followed, not enforced | Move the rule into middleware at the loop's edge |
| A guard stopped working after deployment | The deployed surface streams; the guard only handled buffered results | Buffer streamed updates and check the final result |
| The loop ends with a plausible answer and no citations | Nothing checked groundedness at exit | Inspect the finished run for tool results before releasing it |
| The loop runs long on an easy question | Tool descriptions overlap, so selection churns | Fewer, more distinct tools ({{topic:toolshaping}}) |

## Key terms

**Agent loop** — the repeating cycle of deciding, calling a tool, reading the result and deciding
again, until the task completes or a stop condition fires.

**Harness** — the runtime scaffolding around the model that drives the loop, manages state and context
and applies approval policies.

**Ground truth** — evidence from the environment, such as a tool result or a command's output, that
tells the agent where it actually is.

**Stop condition** — the explicit rule that ends a run: completion, a maximum number of iterations, or
a predicate.

**Middleware** — code wrapped around the loop that can inspect or replace what it produces.
