## TL;DR

Prompt caching reuses the processed form of a stable prompt *prefix* across calls, cutting latency
and cost with no other effect on the answer. It is free money for a context already laid out well —
stable parts first, variable parts last ({{topic:xmltemplates}}) — and worth nothing to one that is
not. The threshold: **1,024 tokens**, and the first 1,024 must be identical.

## How it works

<!-- volatile verified=2026-11 -->
Azure OpenAI retains "a temporary cache of processed input token computations" rather than
reprocessing an identical prefix. It "has no impact on the output content returned in the model
response beyond a reduction in latency and cost", and is enabled by default for supported models.

Two strict requirements: "A minimum of 1,024 tokens in length" and "The first 1,024 tokens in the
prompt must be identical." Miss either and you pay in full — "A single character difference in the
first 1,024 tokens results in a cache miss." On GPT-5.5 and earlier, hits beyond the first 1,024
tokens land "in 128-token increments".

What participates is more than the system message: "The complete messages array", tool definitions
and images. Hence the layout advice — "Place stable or repeated content at the beginning of the
prompt and dynamic content at the end. Keep conversation context append-only."

Cache reads are "billed at a discount on input token pricing for Standard deployment types and up to
100% discount on input tokens for Provisioned deployment types", and on GPT-5.6 and later, cache
*writes* can be charged too. Entries are short-lived: the in-memory cache clears "within 5 to 10
minutes of inactivity" and always "within one hour of the cache's last use", while extended
retention holds a prefix "up to a maximum of 24 hours". Caches are not shared between subscriptions.

Measure it rather than assume it: hits "show up as `cached_tokens` under `prompt_tokens_details` in
the chat completions response". In VS Code, the Cache Explorer serves the same purpose, "to check
prompt cache hit rates and token usage".
<!-- /volatile -->

## Where it fits at Technik

The capstone's prefix is already in the right order: the instructions file, the three tool
definitions, then the server's own description, with only the question varying per call. Nothing has
to change.

<!-- unknown since=2026-11 -->
Whether it *is* cacheable is unmeasured. The capstone never ran live ({{module:capstone-build}}),
and its instructions file is 1,836 characters — characters, not tokens, and plausibly short of the
1,024-token floor even with the tool definitions added. Count your own prefix before claiming a
cache benefit.
<!-- /unknown -->

Two traps follow from *append-only*. Anything that rewrites history instead of appending to it —
compaction above all — invalidates what it touches ({{topic:history}}). And a greeting or timestamp
injected at the top of the context destroys every hit, for a line nobody reads.

## Key terms

**Prompt prefix** — the leading, identical portion of a request: the stable part a cache can match.

**Cache hit** — a match between the prefix and the cache's content, reported as `cached_tokens`.

**Append-only context** — adding to the end of the message array rather than editing earlier
messages, which is what keeps a prefix matchable.
