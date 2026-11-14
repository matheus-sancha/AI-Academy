## TL;DR

{{topic:tokens}} taught estimates and {{topic:budget}} taught the window as a budget with named line items. This
lesson is the measurement and quota half. A budget made of estimates fails on identifiers and on any model you
did not calibrate against, so you count with the model's own tokenizer and read the counts the service returns.
Some of the bill is never in your prompt text: tool definitions, retrieved chunks and reasoning tokens. And
limits act before the window does. Quota is a tokens-per-minute pool shared across a subscription, and a 429 can
arrive while your own metrics look fine.

## Why it matters

An estimate that is off by 20% rarely matters. One that is off by a factor of three does, and it is most likely
to be on exactly the content an engineering agent handles: part numbers, JSON and tables. The second reason is
that the failures arrive in a different form. A full window is an error you can read. A spent quota is a 429, a
slowdown, or a reasoning answer that comes back empty, and each needs a different fix.

## How it works

### Counting: what the sources give you

The token count is a property of the model, not the text. The tokenization method varies by LLM, and GPT models
use a subword method called Byte-Pair Encoding. Both the .NET page and the Agent Framework page point to
OpenAI's online tokenizer to see how text splits, and the Agent Framework page shows a split of "Tokenization"
into pieces with an integer ID each. That tool shows the split for text you author.

For what a call actually used, you read the usage object the service returns. The reasoning-models page names
its reasoning-token fields (`completion_tokens_details.reasoning_tokens` on Chat Completions,
`output_tokens_details.reasoning_tokens` on the Responses API) and says the object reports the exact count.

<!-- unknown since=2026-11 -->
Neither curated page documents counting in code, or the names of the other usage fields. Both are silent on
counting a prompt before you send it. Until you verify a method for your model, the documented options are the
tokenizer view for authored text and the usage object after a call.
<!-- /unknown -->

### The meters outside your prompt text

| Meter | How it is counted | Source |
|---|---|---|
| Tool definitions | They are part of the prompt and consume context tokens, so more tools leave less for history and answer | Agent Framework, tool use |
| Retrieved and injected context | It must fit in the window with everything else | Agent Framework, context window |
| History | Resent on every turn of a multi-turn workload | Reasoning page, control costs |
| Reasoning tokens | Billed as output, share the window, never shown in the message | Reasoning page |
| The response | Output tokens, billed apart from input | .NET tokens page |

The tokens page adds that pricing may differ between input and output, and that no figures are given. It sends
you to the pricing page for them.

### Limits that act before the window

<!-- volatile verified=2026-11 -->
Quota is scoped to the Azure subscription, not the tenant. Since 7 May 2026 it is tracked per subscription:
all resources and regions share one pool, and Global Standard deployments of the same model and version share
one pool across regions. Standard, Data Zone Standard and Global Standard sit in usage tiers numbered 0 to 6,
each with a requests-per-minute and a tokens-per-minute figure per model. At Tier 1 on Global Standard the
page lists `gpt-4.1` at 1,000 RPM and 1,000,000 TPM, `gpt-4.1-mini` at 5,000 RPM and 5,000,000 TPM, and
`gpt-5` at 2,500 RPM and 250,000 TPM. Provisioned and global batch deployments are outside the tiers, and batch
counts enqueued tokens against its limit until the job ends.

Hard counts hold whatever your quota: 128 tools or functions and 2,048 messages per chat request, 50 images per
request, 1,048,576 characters in a message, and for embeddings 2,048 inputs per array and 300,000 tokens per
request, summed across inputs ({{topic:embeddings}}).
<!-- /volatile -->

The page says a 429 can come back "even when token usage metrics appear below your quota". It describes
exceeding a tier as latency, sometimes more than double, and its advice is to add retry logic and avoid sharp
changes in load.

<!-- unknown since=2026-11 -->
The quota page does not say how a request is counted against tokens per minute before it finishes, including
whether the output cap you set counts. It gives no context window or maximum output per model, only "varies per
model" with a link. Its usage-tier table is headed per month while its text calls the tier a maximum in tokens
per minute, and nothing here resolves the two.
<!-- /unknown -->

## In practice at Technik

The capstone's deployment is one block of `azure.yaml`:

*From [`azure.yaml`, lines 14–22](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/azure.yaml#L14-L22):*

```yaml
    deployments:
      - name: gpt-4.1-mini
        model:
          format: OpenAI
          name: gpt-4.1-mini
          version: "2025-04-14"
        sku:
          name: GlobalStandard
          capacity: 10
```

The pages this lesson cites do not say what unit `capacity` is in, so read it in your own deployment rather than
from here. The context has never been counted in tokens either. The capstone never ran against a live
deployment, so the figures in {{topic:budget}} are lines and characters.

Do the arithmetic the tiers invite, with its assumption stated. Suppose one question reads about 7,100 input
tokens (the illustrative table in {{topic:tokens}}) and writes about 300, and suppose both count against the
pool. At the Tier 1 figure for `gpt-4.1-mini`, 5,000,000 TPM allows about 675 single-call turns a minute, and
that is below the 5,000 RPM, so tokens bind first. Now the capstone's loop. A question that makes six tool
calls re-reads the context six times, about 44,000 tokens with output, before the context grows, so the same pool allows
roughly 110 such questions a minute. On `gpt-4.1`, whose pool is a fifth the size, the figure is about 22. The
cap of six calls in `TOOL_LOOP` is therefore a quota decision as well as a safety one.

## Design guidance

- **Count per deployment.** Record the model, version and tokenizer beside every number.
- **Read the usage object** on every call and store it with the trace ({{topic:tracing}}), so a budget is
  checked against reality.
- **Treat each tool definition as a per-turn multiplier**, and each loop step as a multiplier on the input.
- **Reserve headroom for reasoning and output** before budgeting input ({{topic:reasoning}}).
- **Size quota from calls per question times context per call**, not from questions per minute.
- **Retry with backoff**, and do not read a 429 as proof you are over quota.
- **Keep batch work on its own deployment**, since its quota is counted differently.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A prompt estimated at 4,000 tokens is billed at 9,000 | The estimate used word counts on identifiers and JSON | Count with the model's tokenizer, on real tool output |
| 429s under light traffic | Quota is a shared pool, and the metrics may not show it | Check the subscription's usage, add backoff, spread load |
| A reasoning call returns no answer and a bill | The cap was spent on thinking | Raise the cap and check status ({{topic:reasoning}}) |
| A budget that held last month breaks | The model or version changed, so the tokenizer did | Re-measure and keep figures with the deployment name |
| Embedding a corpus fails in one request | It exceeded 300,000 tokens or 2,048 inputs | Split into batches below both limits |
| Throughput halves after adding a tool-heavy agent | Each question now reads the context several times | Cap tool calls and shape results ({{topic:toolshaping}}) |
| A cost forecast per conversation is unavailable | The reports give tokens, not conversations | Compute it from stored usage and the model's price ({{topic:costs}}) |

## Key terms

**Tokenizer**: the model-specific component that splits text into tokens and IDs.

**Usage object**: the counts a response returns for the tokens it consumed.

**TPM and RPM**: quota in tokens per minute and requests per minute.

**Quota pool**: the allowance shared across a subscription's resources, per model.

**Usage tier**: a numbered quota level for Standard-family deployments.

**Enqueued tokens**: the batch measure, counted from submission until the job finishes.
