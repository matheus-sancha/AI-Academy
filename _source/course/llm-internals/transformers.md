## TL;DR

A transformer turns tokens into vectors, adds each token's position, and runs **attention**: a step that lets
every token's vector be shaped by the tokens around it. The model then predicts one next token, appends it,
and runs again. Two consequences are documented. Every generated token is computed with the whole sequence in
view, and longer prompts cost more. Two consequences the roadmap used to promise are in neither curated source:
that cost grows faster than length, and that evidence in the middle of a long prompt is used less. This lesson
teaches the mechanism, marks those two as unknown, and tells you to test position instead of assuming it.

## Why it matters

{{topic:tokens}} and {{topic:inference}} gave you the outside view: tokens in, tokens out, a pause before the
first word. This lesson is one level down, for the day a result needs an explanation rather than a guess. A
mechanism lets you ask the right first question, and that question is almost always *what was in the
sequence*. "The model forgot" usually means the context never held the fact.

## How it works

### From text to vectors

A tokenizer splits text into sub-word units, and each unit has an integer ID. Microsoft's training module
describes the next step: each token gets a **vector**, and a real transformer's vectors have thousands of
elements. The token vectors go in together with a **positional encoding** that says where each token sits,
because order changes how tokens relate to one another.

### What attention does

The module describes the attention layer as examining each token in turn and working out how it is influenced
by the tokens around it. Its worked example is a sentence ending in "bark": "heard" and "dog" weigh more than
"I" or "a" when the layer considers "bark". It adds that attention is multi-headed, evaluating several elements
of a token in parallel, and tells the reader not to worry about the details. Neither curated page shows a way
for you to read the weights.

<!-- unknown since=2026-11 -->
The module describes an encoder block that builds the embeddings with attention and a decoder block that
predicts the next token, with masked attention ignoring tokens after the current one. It also calls its
transformer greatly simplified. Neither curated page says which blocks the models you deploy use. The Agent
Framework page says only that an LLM is weights plus architecture code, "typically a Transformer".
<!-- /unknown -->

### The loop

The Agent Framework page lists five steps. The whole prompt is tokenized and fed in. The model produces a
probability for every token in its vocabulary. One token is chosen, influenced by temperature and other sampling
settings. It is appended and the whole updated sequence is fed back in. This repeats until a stop token or a
length limit. A tip on the same page explains the shortcut engines take: a **KV-cache** keeps intermediate
computations from tokens already processed, so each new token does not reprocess the sequence from scratch.
Generation then has two phases. **Prefill** processes all input tokens, and the first token takes longer for it.
**Decode** produces one token at a time from the cache.

Two lines on that page bear on cost. Longer prompts use more tokens, cost more and leave less room for the
response. And longer responses take proportionally longer, because each token needs a full forward pass. The
API is a stateless request and response, so nothing carries over between calls unless you send it again.

### What is sourced and what is not

| Claim | Status | Where |
|---|---|---|
| Each generated token is computed with the entire sequence in view | Documented | Agent Framework, inference steps |
| Longer prompts cost more and leave less room for the answer | Documented | Agent Framework, tokens |
| Latency grows with output length | Documented | Agent Framework, response-length callout |
| The first token is slower than later ones | Documented | Agent Framework, KV-cache tip |
| First-token latency grows with input length | Not stated | Neither page says it |
| Cost grows faster than linearly with length | Not stated | Neither page says it |
| Evidence in the middle of a long prompt is used less | Not stated | Neither page says it |

<!-- unknown since=2026-11 -->
Neither curated page says how compute grows with input length, or that a model uses evidence in the middle of a
long input less than evidence at the ends. {{topic:budget}} cites a different source for the softer point that
context has diminishing returns, and that source does not say where in the window the loss falls. Treat
position as an empirical question for your own deployment.
<!-- /unknown -->

## In practice at Technik

Take the question *"What is the acceptance limit for indications on sealing surfaces in `SWI70000318`?"* After
retrieval, the sequence holds the agent's instructions, its tool definitions, the question and the passage from
section 5.2, which gives 0.8 mm on sealing surfaces and 1.5 mm on non-sealing ones. Borrow the module's
example. When the layer works on the token "limit", the useful neighbours are "indications", "sealing" and the
figure beside them, and the risk is the 1.5 mm sitting one table cell away. That illustrates what attention is
for. It is not a measurement.

Now the failure you will meet. The capstone's agent answers a revision question correctly in a one-turn test and
wrongly after six tool calls. The tempting explanation is that attention drifted. The first thing to check is
the sequence: is the released revision still in it, and what else arrived behind it? Every tool result joins
the same stream as the instructions. The sequence holds no field that marks one part as trusted, which is why a
quality notification description carrying an instruction, such as `300001270`, is a context-security problem and
not a prompt-wording one ({{topic:ctxsecurity}}).

The capstone makes the one move this lesson supports without a measurement: it keeps the sequence short.
Tools return assembled lines, not rows, and a loop cap of six calls bounds what accumulates
({{topic:budget}}, {{topic:toolshaping}}). To learn whether position matters for your agent, build the test
the sources lack: one evaluation question asked twice, with the same evidence first and then last, both scored
({{topic:evalstrategy}}).

## Design guidance

- **Debug the sequence before the model.** Print or trace what the model was given, then reason about it.
- **Do not rely on position.** Where you put a fact is a variable to test, not a rule to assume.
- **Keep trust out of the stream.** The model attends to a tool result as it does to your instructions, so
  treat everything that enters as data to be shaped and constrained.
- **Cap output as well as input.** Latency tracks output length, and a cap bounds it.
- **Keep the stable prefix first** so a cache can reuse it ({{topic:caching}}).
- **Resend what must persist.** The API is stateless, so memory is whatever you put back in the sequence.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| "The model ignored the rule" | The rule was never in the sequence, or a later tool result outweighed it | Inspect the sequence first, then test moving the rule |
| Correct on short tests, wrong in real sessions | The real sequence is longer and holds more competing text | Test at production length, not on a clean first turn |
| Long pause before the first word | Prefill over a large input | Shrink the input; streaming does not shorten this wait ({{topic:inference}}) |
| An explanation that blames attention | Attention weights are not visible, so the claim cannot be checked | Replace it with a test that moves the evidence |
| The agent "remembers" an earlier turn | The history was resent, not stored in the model | Check what your harness replays ({{topic:history}}) |
| A claim that cost grows quadratically | Neither curated page says so | Measure cost against length on your deployment |

## Key terms

**Transformer**: the neural network architecture behind current LLMs.

**Attention**: the step that lets each token's vector be influenced by the tokens around it.

**Positional encoding**: the signal added to token vectors so the model knows their order.

**Autoregressive**: generating one token, appending it, and generating the next from the longer sequence.

**KV-cache**: stored intermediate computations from tokens already processed, reused for each new token.

**Prefill and decode**: the two generation phases. Prefill reads the whole input, and decode emits one token
at a time.
