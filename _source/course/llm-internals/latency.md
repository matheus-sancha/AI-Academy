## TL;DR

Two questions get mixed up. *Latency* is how long one call takes. *Throughput* is how much a deployment processes in
a minute. One formula covers the first: the time to the last token is the time to the first token plus the time
between tokens multiplied by the tokens generated. Output length usually dominates it, so most levers cut output or
take work off the path the user waits on. Capacity levers, such as quota and provisioned throughput, set throughput
and how much latency varies. The capstone's waiting time is set by a guard that holds the stream. Neither curated
page publishes a figure for any model.

## Why it matters

A slow agent and an expensive one usually share a cause: more tokens than the question needed. A latency number alone
does not say which kind of slow you have, so the page's main advice is to read it beside a token count. A deployment
can also be slow because of what else is using its capacity, and the fix differs.

## How it works

### Per call and per deployment

The page separates **system-level throughput**, the tokens per minute a deployment handles, from **per-call
latency**. On a Standard deployment, quota is admission logic and does not enforce throughput, so you may not reach
it. On a provisioned deployment you reserve capacity, and what it delivers depends on the workload's shape: input
tokens, output tokens, call rate and cache match rate.

### The latency formula

<!-- volatile verified=2026-11 -->
The page gives `TTLT = TTFT + (TBT × tokens generated)`. TTFT is the time to the first token, TBT the average time
between tokens, and TTLT the time to the last. Generation is sequential, one token at a time, which the page
compares to a loop of *n* iterations for *n* tokens. Each prompt token adds little beside each generated one,
though a large prompt raises TTFT. Latency depends on the model, the prompt tokens, the generated tokens and the load
on the deployment, and the model and the generated tokens often count most. So a rise in TTLT is often fully
explained by longer output, and the page says to check token counts before calling it a regression.
<!-- /volatile -->

Its ten-minute check follows. Chart the last-token time with the generated-token count. If they rise together, the
change is expected. If the time rises alone, look for capacity pressure: a provisioned deployment's utilisation, or
429s and concurrency on a pay-as-you-go one. For a streamed call, a first-token time that rises with a flat prompt
points at utilisation, and a rising time between tokens at load.

### The levers the page lists

<!-- volatile verified=2026-11 -->
- **Model.** Latency differs by model for an identical request. The page recommends GPT-4o mini for the lowest latency.
- **Generation size.** Set the cap as low as the task allows, add stop sequences, and leave `n` at 1, since more
  outputs per request add latency. The requested size is reserved as compute while the request runs, so a higher cap
  adds latency even when the same number of tokens is generated.
- **Streaming.** Tokens return as they are ready. The total time is the same, but the first response comes sooner,
  which suits chat, and long calls survive client timeouts. For bulk work it matters little.
- **Content filtering.** It adds safety and latency, and the page calls the trade-off one to evaluate.
- **Separate workloads.** Mixed workloads on one endpoint are batched together, so short calls wait on long ones
  and cache hits fall. Use a deployment per workload.
- **Prompt size and batching.** A smaller prompt helps less than a shorter answer. Several requests in one call may
  help, and the page says to test it.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
The roadmap listed caching, parallel tool calls and model routing as levers. This page covers none. The first two are
documented elsewhere ({{topic:caching}}, {{topic:functioncalling}}), and neither curated page mentions model routing.
The page also uses `max_tokens`, which reasoning models do not support ({{topic:params}}), and names GPT-4o mini with
no latency figure for it or any other model.
<!-- /unknown -->

### Capacity, and what it costs

<!-- volatile verified=2026-11 -->
Standard deployments are pay per token with no latency target. Provisioned deployments reserve capacity in
provisioned throughput units (PTUs), billed per PTU per hour whether or not requests arrive, with a defined latency
target per model. Reservations of one month or one year discount the rate, are bought apart from the deployment and
do not guarantee capacity, so create the deployment first. Having PTU quota does not guarantee that PTUs are
available, and a deployment you scale down may not come back, so do not scale one up and down with traffic.

Three factors size a deployment: the request shape, the output-to-input ratio (output tokens need more capacity than
input) and the cache rate. The page's example for GPT-4o mini is 800 prompt tokens, 150 generated and 30 requests a
minute: 28,500 tokens a minute and 15 PTUs, scaling about linearly with call rate. Spillover can send a full
provisioned deployment's overflow to a Standard deployment in the same resource, set for the deployment or per
request by a header. Priority processing is a pay-per-token option with a latency target.
<!-- /volatile -->

{{topic:deploytypes}} lays these types out. One word needs care: *batching* in the page's lever list means several
requests in one call, while a Batch deployment is asynchronous, with a 24-hour target and no real-time promise.

## In practice at Technik

One question to the capstone can make up to six model calls ({{topic:loop}}), run in sequence, so their latencies
add. Suppose, with assumed figures, that TTFT is 0.6 s and TBT is 20 ms. A first call
that returns a 40-token tool call takes 0.6 + 40 × 0.02 = 1.4 s. After the tool runs, a second call that writes a
120-token answer takes 3.0 s, so the question takes about 4.4 s plus the tool's own time. If the instructions let the
answer run to 400 tokens, the second call takes 8.6 s and the question about 10 s. The extra 280 tokens cost 5.6 s.

Streaming is the lever the capstone chooses not to use. The hosted server always streams, and the guard holds the
updates until the answer can be checked:

*From [`agent/main.py`, lines 38–41](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/agent/main.py#L38-L41):*

```python
    # The hosted server always streams. Hold the updates until the answer is final, check it,
    # and release only what passed: the answer, or the refusal in its place.
    context.result = context.result.with_result_transform(refuse_unless_grounded).buffer_updates(
        result_to_updates=lambda r: [AgentResponseUpdate(role=m.role, contents=m.contents) for m in r.messages])
```

So the user sees the first word only at the last token, and the benefit the page describes is gone. The trade is
deliberate, since an answer shown and then replaced by a refusal is worse than a wait. The levers on tokens and calls
remain. Nothing in the capstone caps output, and its one deployment is `GlobalStandard`, a type with no latency
target ({{topic:deploytypes}}).

<!-- unknown since=2026-11 -->
No latency was measured. The capstone never ran against a live deployment, and the arithmetic above is the page's
formula with invented inputs. Measure TTFT, TBT and generated tokens on your own deployment first.
<!-- /unknown -->

## Design guidance

- **Read latency beside tokens.** Generated tokens explain most changes.
- **Cap output on purpose**, low enough to save time and high enough to keep answers whole.
- **Count the calls in a loop.** Each tool round adds a model call ({{topic:functioncalling}}).
- **Stream where a person watches**, and note when a check has to hold the stream.
- **Keep batch and interactive work on separate deployments.**
- **Set a latency target only from your own measurements.**

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Latency doubled after a prompt change | The answer got longer | Compare generated tokens before you suspect the platform |
| Streaming is on and users still wait | A guard holds the stream, or a large input delays the first token | Decide which, and shorten the input ({{topic:transformers}}) |
| Time to last token rises and tokens do not | Capacity pressure | Check provisioned utilisation, or 429s and concurrency |
| Short calls queue behind long ones | Mixed workloads share an endpoint | Give each workload its own deployment |
| A "batched" job takes a day | Batch deployment, not request batching | Use Batch only when nobody waits |

## Key terms

**TTFT and TBT**: the time to the first token and the average time between tokens.

**TTLT**: the time to the last token, the whole call.

**Throughput**: the tokens per minute a deployment processes, not the latency of one call.

**PTU**: the unit of provisioned throughput, a fixed amount of reserved capacity.

**Spillover**: routing a full provisioned deployment's overflow to Standard.
