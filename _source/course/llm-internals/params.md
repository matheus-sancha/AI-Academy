## TL;DR

An inference parameter is not portable. The same intent has a different name on Chat Completions and on the
Responses API, and a reasoning model does not support some settings that a chat model accepts. {{topic:temperature}}
taught the sampling pair. This lesson teaches the rest by intent: limit the output, shape it, spend thinking,
keep state. For each it gives the name on each surface, and then it does something the roadmap did not: it
lists what the curated pages never document. `seed`, stop sequences and `tool_choice` are in neither, so they
are marked unknown. The capstone sets two options on its model calls and leaves the rest to the defaults.

## Why it matters

Parameters are where a working call breaks on a model change. The request that ran on one deployment returns an
error on the next because a parameter was renamed or is no longer accepted, or it runs and silently does
something different. They are also the part of a configuration least likely to be written down. An evaluation
score reported without the settings behind it cannot be reproduced, which is the point of the last section.

## How it works

### One intent, several spellings

| Intent | Chat Completions | Responses API |
|---|---|---|
| Cap generation, thinking included | `max_completion_tokens` | `max_output_tokens` |
| Constrain the answer to a schema | `response_format` | `text.format` |
| Spend more or less thinking | `reasoning_effort` | `reasoning` with an `effort` field |
| Carry a conversation on | Resend the messages | `previous_response_id`, or resend items |
| Keep or drop stored output | Not on the page | `store` |

The reasoning page covers the caps and effort for both APIs. The Responses page says the schema goes in
`text.format` and that Chat Completions uses `response_format` instead. The older `max_tokens` is on the
unsupported list for reasoning models. A hand-written call that uses the left-hand column against a deployment
that expects the right is the commonest breakage. Both caps cover reasoning, visible output and formatting
tokens ({{topic:reasoning}}).

<!-- volatile verified=2026-11 -->
*Adapted from the Chat Completions sample on the reasoning models page:*

```python
response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user", "content": "<your question>"},
    ],
    max_completion_tokens=5000,
    reasoning_effort="medium",
)
```
<!-- /volatile -->

A developer message is functionally a system message. The page warns against sending both in one request, and
for the o-series it treats a system message as a developer one.

### What a reasoning model does not support

<!-- volatile verified=2026-11 -->
The page's unsupported-parameters list covers every reasoning model except GPT-6 Astra: `temperature`, `top_p`,
`presence_penalty`, `frequency_penalty`, `logprobs`, `top_logprobs`, `logit_bias` and `max_tokens`. Two more
limits sit in its feature tables. Parallel tool calls are unsupported on the o-series, and at `minimal` effort.
And the GPT-5.6 models reject a Chat Completions request that carries `tools` unless `reasoning_effort` is
`none`, even when you never set it, because their default is `medium`. The page's fix is to use the Responses
API for tools.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
The page contradicts itself. Its GPT-6 table marks `temperature`, `top_p` and `logprobs` as supported for all
five GPT-6 models, while its unsupported list excludes only GPT-6 Astra. It does not say which statement wins.
It also never says whether an unsupported parameter is rejected with an error or ignored, though
{{topic:temperature}} says some surfaces ignore temperature. Test the exact deployment, and do not rely on
either statement.
<!-- /unknown -->

### State and retention

<!-- volatile verified=2026-11 -->
The Responses API keeps response data for 30 days by default. With `store=false` the response is stateless, and
a reasoning model's output then carries encrypted reasoning that you replay yourself on the next call. The page
warns against `previous_response_id` for a response that was never stored.
<!-- /volatile -->

### What the curated pages do not document

The Responses page, the other source for this topic, lists none of the parameters this topic's roadmap entry
named. It covers `stream`, `store`, `include`, `previous_response_id`, `text.format` and `tools`, and refers
the reader to a separate parameter reference for the rest.

<!-- unknown since=2026-11 -->
Neither curated page mentions `seed` or stop sequences. Neither describes `tool_choice` or
`parallel_tool_calls` for non-reasoning models, or `temperature` and `top_p` on the Responses API. The
roadmap's "best-effort reproducibility" for `seed` is therefore unsourced. The Agent Framework page says only
that even at temperature 0 a model is not fully deterministic ({{topic:temperature}}).
<!-- /unknown -->

## In practice at Technik

The capstone sets two things on its model calls and nothing else. The loop options go on the client:

*From [`agent/main.py`, lines 19–20](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/agent/main.py#L19-L20):*

```python
# Pass the server's ToolError messages to the model; by default it sees only "Error: Function failed."
TOOL_LOOP = {"include_detailed_errors": True, "max_function_calls": 6}
```

Those are Agent Framework options, not parameters of the model API. They bound the loop and decide what the
model sees of an error. The only API-level setting is in the hosted entry point:

*From [`agent/hosted.py`, lines 18–20](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/agent/hosted.py#L18-L20):*

```python
def host(client, tools):
    # Foundry keeps the conversation, so the model call stores nothing.
    return ResponsesHostServer(build_agent(client, tools, default_options={"store": False}))
```

`store: False` is the Responses API's `store`, set because Foundry already holds the conversation. Nothing
sets a temperature, a token cap, a tool choice or a seed, so the deployment's defaults apply, and the curated
pages do not state them.

This matters for the evals. The eight cases in the capstone's set are graded against a baseline file, and a
regression is a difference from it ({{topic:mafeval}}). If a default shifts when the model version changes,
the baseline moves for a reason nobody wrote down. The fix costs one line per run: record the model, version
and every option beside the score. Set a cap on purpose before you move to a reasoning model, because there it
bounds thinking as well as the answer.

## Design guidance

- **Name parameters by intent in your own code**, and translate to the API's spelling in one place.
- **Check the deployment, not the table.** Send a test call with each setting you rely on.
- **Set an output cap deliberately.** On a reasoning model it bounds thinking too.
- **Prefer a schema to a request for JSON** where the platform offers one ({{topic:structured}}).
- **Choose `store` on purpose.** It decides what is retained, and for how long.
- **Record the settings with every evaluation result**, defaults included.
- **Do not build on `seed`** until you have verified it on your deployment.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A call fails, or a setting stops having an effect, after a model upgrade | The new model family does not support a setting you pass | Remove it, or branch by model family |
| `max_tokens` has no effect or fails | It is on the reasoning models' unsupported list | Use `max_completion_tokens`, or `max_output_tokens` on Responses |
| Tools stop working on a newer model through Chat Completions | The model rejects `tools` unless effort is `none` | Move the tool path to the Responses API |
| The answer shape changes between APIs | `response_format` and `text.format` are different fields | Set the one the API expects |
| Reproduction fails on re-run | `seed` is unsourced, and temperature 0 is not deterministic | Evaluate over a set, not one run ({{topic:evalstrategy}}) |
| `previous_response_id` fails or finds nothing | The earlier response was never stored | Keep `store` on, or resend the items |
| You tune a setting and nothing changes | The model may not support it, and the page does not say what happens then | Check the model's supported list before tuning |

## Key terms

**Inference parameter**: a setting on a model call that changes how it generates, as opposed to what it is
asked.

**Output cap**: the maximum tokens a response may generate, which on a reasoning model includes thinking.

**Response format**: the field that constrains an answer to a schema, spelled differently on each API.

**Store**: the Responses API setting that keeps response data, by default for 30 days.

**Developer message**: a message role that works like a system message on reasoning models.
