## TL;DR

A reasoning model generates a chain of thought before it answers. That thinking is made of tokens: billed as
output, held in the context window, and never shown in the message. The result is a dial and a failure mode.
The dial is reasoning effort, from `none` to `max`, with defaults that vary by model. The failure mode is a
response that stops as `incomplete` before any visible output, with the thinking already billed. In an agent
loop the model's reasoning items must also travel with the tool results. The curated page has no guidance on
routing between models, so this lesson claims none.

## Why it matters

{{topic:models}} told you to use a reasoning model knowingly, for the step that needs it. This lesson is what
"knowingly" costs in mechanics. A reasoning model changes the bill, the latency, the output cap and what you
must resend. An agent multiplies all four, because each tool call is another inference that may think.

## How it works

### What the model does differently

The Agent Framework page explains where the behaviour comes from. Reinforcement learning teaches a model to
break a problem into sub-steps, explore alternatives and check its work before it answers. It names gains in
math, logic, coding and multi-step problems, and says the approach works best in verifiable domains. The price
is higher latency and token usage, because the reasoning steps are generated as tokens too. The reasoning page
lists complex code generation, document comparison and instruction following as uses, and says these models do
not need you to prescribe every intermediate step.

### Where the thinking goes

<!-- volatile verified=2026-11 -->
Reasoning tokens never appear in the message content. They occupy space in the context window and are billed
as output tokens, so a request that thinks longer costs more even when the visible answer is short. The count
is in the usage object, as `reasoning_tokens` under `completion_tokens_details` or `output_tokens_details`. A
request can use from a few hundred to tens of thousands of them. Both output caps, `max_completion_tokens` and
`max_output_tokens`, cover reasoning, visible output and formatting together.

You can ask for a **summary** of the reasoning with `reasoning.summary` set to `auto`, `concise` or `detailed`.
The GPT-5 series does not support `concise`, and a summary is not guaranteed for every request. The raw
reasoning is not returned, and the page tells you not to extract it another way.
<!-- /volatile -->

<!-- volatile verified=2026-11 -->
*Adapted from the Responses API sample on the reasoning models page:*

```python
response = client.responses.create(
    input="<your question>",
    model="gpt-5",  # your deployment name
    reasoning={"effort": "medium", "summary": "auto"},
    text={"verbosity": "low"},
)
```
<!-- /volatile -->

### The effort dial

<!-- volatile verified=2026-11 -->
The values are `none`, `minimal`, `low`, `medium`, `high`, `xhigh` and `max`, and not every model takes all of
them: `minimal` is for the original GPT-5 models, and `max` for GPT-6 and GPT-5.6 on the Responses API. The
default varies by model: `gpt-5.1` defaults to `none`, `gpt-5-pro` takes only `high`, and GPT-5.6 defaults to
`medium`. The page's suggested uses:

| Effort | Suggested for |
|---|---|
| `none` | Latency-critical work that gains nothing from reasoning: voice, fast retrieval, classification |
| `low` | Modest extra latency, for tool use, planning, search and multi-step decisions where speed and cost count |
| `medium` | A balanced starting point for most workloads |
| `high` | Hard reasoning, complex debugging, deep planning, where quality beats latency |
| `xhigh` | Deep research and long agentic runs, only when evaluations show a gain worth the cost |
<!-- /volatile -->

The page calls effort a tuning knob, to reach for after you have fixed the task statement, the constraints and
the output format. It also says the models adapt within a setting, spending fewer tokens on simple tasks.

### The failure: incomplete

<!-- volatile verified=2026-11 -->
When generation hits the context window or your cap, the response comes back with `status` set to
`incomplete` and the reason `max_output_tokens`. That can happen before the model produces any visible output,
so you pay for input and thinking and receive nothing. Check `status` on every response. While you
learn a workload, the page advises reserving at least 25,000 tokens.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
The page shows this signal for the Responses API only. It gives no Chat Completions `finish_reason` for the
same case, so a Chat Completions caller has no documented signal to check.
<!-- /unknown -->

### Inside an agent loop

<!-- volatile verified=2026-11 -->
The page says to use the Responses API when you combine reasoning with function tools. Pass the previous response's reasoning items back with your function output, and after several calls in a row
send every reasoning item, call and output since the last user message. The model then continues its line of
reasoning "instead of starting over" and gets there in fewer tokens. The simplest method is to pass all output
items back. With `store` off, reasoning items carry encrypted content that you replay yourself. A setting,
`reasoning.context`, chooses how much earlier reasoning is kept, with defaults that differ by model.
<!-- /volatile -->

## In practice at Technik

The capstone does not use a reasoning model. Its deployment is `gpt-4.1-mini` ({{topic:tokenbudget}}), and its
three tools are lookups: a controlled document, the documents an operation uses, a released revision. By the
page's own table those sit with `none`, the row for fast retrieval. A reasoning model would make each of the
up to six calls in a turn an inference that may think, so effort multiplies by the loop.

Suppose Technik wanted to test one for harder questions. Here is a starting set, each a hypothesis for an
evaluation to confirm, with the page's rows as the only guide:

| Technik task | Starting point |
|---|---|
| Status of `SWI70000318` | No reasoning |
| Documents that cover Cladding at operation `0020` | `low` |
| Find open work orders still on revisions `ECN70000051` superseded | `medium` |
| Draft revision C's change summary against its ECN | `medium`, then `high` if reviews find misses |

<!-- unknown since=2026-11 -->
Nobody has run these against the capstone. Whether Agent Framework replays a reasoning model's items between
tool calls when the hosted agent sets `store` to `False` is not in the cited pages. Verify it before you move
the capstone to a reasoning deployment.
<!-- /unknown -->

The roadmap's "route simple requests to faster models" is not in the page, whose nearest statements are effort
`none` and a model that thinks less on easy tasks. Routing between deployments is a design choice
({{topic:models}}), and a router is one more component to evaluate ({{topic:evalstrategy}}).

## Design guidance

- **Start at the lowest effort the task tolerates**, and raise it when an evaluation shows the gain.
- **Reserve room before you cap.** Budget thinking and answer together ({{topic:tokenbudget}}).
- **Check `status` on every response**, and treat `incomplete` as an error.
- **Use the Responses API for tools**, and carry reasoning items forward.
- **Write the task, not the steps.**
- **Re-evaluate on a model change** ({{topic:mafeval}}).
- **Log reasoning tokens** so cost per question can be computed ({{topic:costs}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| An empty answer and a full bill | The cap was spent on thinking | Raise the cap, reserve headroom, check `status` |
| Tool calls fail on a newer model through Chat Completions | GPT-5.6 rejects `tools` unless effort is `none` | Move to the Responses API |
| Agent cost per question jumps after a model swap | Each loop step now thinks | Cap tool calls, lower effort on lookups |
| Quality drops, and you raise effort first | Effort is a knob, not the first fix | Fix the task statement first |
| The agent restarts its reasoning after each tool result | Reasoning items were not passed back | Replay every item since the last user message |
| You cannot see why it answered that way | Raw reasoning is not returned | Use a summary, and trace the calls ({{topic:tracing}}) |
| A latency-critical path got slower | The default effort is not `none` | Set effort explicitly |

## Key terms

**Reasoning model**: a model trained to generate a chain of thought before its answer.

**Reasoning tokens**: the thinking tokens, billed as output and held in the window, never shown in the message.

**Reasoning effort**: the setting that scales how much a model thinks.

**Reasoning item**: a unit of reasoning returned by the Responses API, to be passed back across tool calls.

**Incomplete response**: a response that stopped at a token cap, possibly before any visible output.

**Reasoning summary**: an optional, non-guaranteed digest of the thinking.
