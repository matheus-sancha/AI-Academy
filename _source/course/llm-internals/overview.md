## What this module is for

Intermediate told you what a token is, what temperature does and why a reasoning model is slower. This module opens
the box one level further, for the day a number needs an explanation. The agent got slower, the bill went up, a call
that worked on one model fails on the next, or a reply arrived in the right shape with the wrong value. In each case
a guess is cheap and a mechanism is what fixes it.

It is a reference module, not a read-through. Come here with a symptom and read the lesson that explains it. The
capstone is the running example, and its model is a small chat model that does no reasoning. So a lesson often
says what would change if it did.

One thread runs through all nine lessons: **a token is the unit of everything you pay in**. Input tokens fill the
window and spend quota. Output tokens are what the user waits for. Thinking tokens are billed as output and share the
window. A tool definition is tokens, and so is every tool result, resent on every call of the loop. Once you count in
tokens, time, money, quota and context stop being four problems.

The second thread is a habit. The documentation for these mechanisms is thinner than the roadmap assumed. Where a
curated page is silent, the lesson says so in a visible *Not yet verified* block, such as the claim that evidence in
the middle of a prompt is used less, what `seed` guarantees, or how requests count against quota. Each block tells
you what to test on your own deployment. Treat those as open questions with a test attached, not as facts.

## Before you start

You need {{topic:tokens}}, {{topic:inference}} and {{topic:temperature}}, which this module deepens rather than
repeats, and {{topic:models}} for choosing between a chat and a reasoning model. {{topic:contextcost}} established
what is resent on every turn, and {{topic:tools}} and {{topic:mcp}} are the tool side that {{topic:functioncalling}}
takes apart. {{topic:prompts}} showed one product's version of a locked JSON format, the starting point for
{{topic:structured}}.

From this level, {{topic:budget}} and {{topic:caching}} in {{module:context-engineering}} treat the window as a
budget, and {{topic:loop}} in {{module:agent-harness}} is the loop that several lessons price. The capstone's code,
quoted at the tag `v1.0.0`, was tested offline only ({{module:capstone-build}}), so no lesson here reports a
measurement from it.

Allow about three hours to read it end to end, though you are not meant to.

## What you will be able to do

By the end of this module you should be able to:

- explain from the mechanism why a longer prompt costs more and a longer answer takes longer, and say which
  further claims the sources do not support;
- count tokens with the deployment's own tokenizer, and say which limit, window, quota or hard count, you will meet
  first;
- name each inference parameter by intent on both APIs, and say which behaviours the pages never document;
- set reasoning effort and an output cap on purpose, check for an incomplete response, and say what must travel between
  tool calls;
- say what an embedding is, what to record beside an index, and what a similarity search can never tell you;
- walk through a function call step by step and name the parts that are yours to validate;
- declare a schema for a reply, and name what it cannot check;
- split a latency figure into its parts, and tell a longer answer from a slower platform;
- choose a deployment type for a workload, and give the reason.

## The thread through this module

From the model outward, then to what it costs to run.

{{topic:transformers}} gives the mechanism: attention shapes each token by its neighbours, and generation runs one
token at a time. It marks two familiar claims, that cost grows faster than length and that the middle of a prompt is
used less, as unsupported by its sources. {{topic:tokenbudget}} turns tokens into something you count and budget, and
finds the limits that act before the window does. {{topic:params}} lists what you can set and what each API calls it.
{{topic:reasoning}} is the one setting that changes the bill, the latency and the cap together.

{{topic:embeddings}} leaves generation for the other thing a model produces, a vector, and the cost of keeping
vectors comparable. {{topic:functioncalling}} is the mechanism under every tool in this course: the model returns a
request, your code runs it. {{topic:structured}} is the same idea applied to the answer, a shape the platform holds
to, with the checks that a shape cannot do.

{{topic:latency}} puts the module's numbers to work: one formula, the levers on it and the capacity beneath it.
{{topic:deploytypes}} closes the module with the choice of where prompts are processed and how you pay.

## Self-check

<details>
<summary>1. The assistant takes about twice as long to answer after someone edits its instructions. The platform status is green. Where do you look first, and what would show a platform problem instead?</summary>

At generated tokens, before anything else. A call's time to the last token is the time to the first token plus the
time between tokens multiplied by the tokens generated, and generation is sequential. So a doubling is often fully
explained by an answer that got longer, and an edit to the instructions can do exactly that. Chart the last-token
time beside the generated-token count. If they rise together, the change is expected and the fix is a shorter answer
and a cap on purpose.

If the time rises with the tokens flat, suspect capacity: a provisioned deployment's utilisation, or 429s and
concurrency on a pay-as-you-go one. Also count the model calls in a turn, because the capstone's loop can make six in
sequence and their latencies add ({{topic:latency}}, {{topic:transformers}}).
</details>

<details>
<summary>2. Someone proposes moving the capstone from its chat model to a reasoning model "for better answers", and points out that the code sets no temperature or token cap. Is it a one-line change?</summary>

No, and the missing settings are part of why. A reasoning model does not accept several parameters a chat model does,
and the capstone sets none of them, so that part happens to be safe. What changes instead is everything the defaults
were hiding. Thinking is billed as output and shares the window, and an output cap, which the capstone does not set,
now bounds thinking as well as the answer. A response can end as `incomplete` before any visible output, so
`status` has to be checked. The effort default varies by model and may be higher than a lookup needs, and each of up to
six calls in a turn is an inference that may think.

Two more questions the sources leave open. Whether Agent Framework replays reasoning items between tool calls when
the hosted agent sets `store` to false is not documented. And the evaluation baseline moves, so the model, version and
effort belong beside every score ({{topic:reasoning}}, {{topic:params}}).
</details>

<details>
<summary>3. A log line shows a call to <code>get_document</code> with the argument <code>quality handling</code>. Did the model query Teamcenter, and what protects the system if it keeps sending calls like that?</summary>

The model queried nothing. It returned a request naming a function and a string of JSON arguments, and the harness
decided to run it. Everything that happens next is code you own, which is why the page's advice is a list of checks:
validate the function, the arguments and the intent, grant the least access the function needs, and confirm before
any action. The capstone's tool is read-only through one role, so a malformed or hostile call cannot write.

The argument has the wrong shape for a document number, so the useful questions are where it was rejected and what
the model then saw. The server's error text is shown to the model so it can ask the user, and the grounding guard
refuses any answer no tool result backs. Be honest about one gap: the course's tests do not isolate whether the
`pattern` constraints are enforced before the tool body runs ({{topic:functioncalling}}).
</details>

<details>
<summary>4. A strict-schema extraction of a supplier material certificate returns <code>"yield_strength": 72</code> with <code>"yield_unit": "MPa"</code>, and the certificate prints 72 ksi. Is the schema broken, and what do you change?</summary>

The schema is working as designed. A structured output guarantees shape: every field present, the unit one of
the allowed values, no extra keys. It cannot guarantee that a value is true, and 72 against the unit `MPa` fits the
schema exactly. The supported subset has no `minimum`, so the platform cannot hold a range either, and a threshold
such as the 485 MPa minimum is a business rule that belongs in code anyway.

So the change is in the code around it. Check plausibility, since 72 MPa is far below any yield figure Technik
buys against. Convert ksi to MPa when the unit says so. Route a reading that fails, or that the model could not
read, to a person. Check for a refusal or an incomplete response before reading the parsed value, and add this
certificate to the evaluation set ({{topic:structured}}).
</details>

<details>
<summary>5. The nightly certificate job and the daytime assistant share one deployment. At 10 a.m. the assistant returns 429s although its own traffic is light. What do you suspect, and what do you change?</summary>

Suspect the shared pool. Quota is a tokens-per-minute pool across a subscription, and a 429 can arrive while your
own usage metrics look below it, so the job's tokens and the assistant's compete. Mixed workloads on one endpoint
also hurt latency, because short calls queue behind long ones and cache hits fall.

Move the job to its own deployment, and nothing about it needs a person waiting: that is what Batch is for. A Batch
deployment is asynchronous, with a 24-hour target, half the price and its own enqueued-token quota, so it does not
disturb the online workload. Meanwhile add backoff to the assistant's retries, and do not read a 429 as proof that the
deployment is too small. A larger quota is the last fix, not the first ({{topic:tokenbudget}}, {{topic:deploytypes}},
{{topic:latency}}).
</details>
