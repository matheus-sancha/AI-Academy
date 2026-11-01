## TL;DR

The window is one allowance shared by everything: system instructions, tool definitions, retrieved
knowledge, conversation history, tool results — and the answer. Microsoft's docs are explicit that
output competes with input, because the limit "is often expressed as a combined maximum context
window that covers both input and output tokens together". There are two ceilings, not one. The
hard ceiling is the window; the soft one arrives much earlier, because the attention budget means
"Every new token introduced depletes this budget by some amount". So treat the window as a budget
with named line items, measure each one, and spend against evaluation scores rather than against
the limit.

## Why it matters

Intermediate established what everything costs on a turn: instructions and every tool definition
are re-sent each time, with knowledge results and history on top ({{topic:contextcost}}). That was
a fact to work around. Here it becomes an allocation you own and defend.

Three things depend on it. **Cost**, because "Generative AI services often use token-based pricing"
and "The cost of each request depends on the number of input and output tokens. Pricing might
differ between input and output." **Throughput**, because services "also enforce a maximum number
of tokens per minute (TPM)", so a bloated context reduces how many questions you answer per minute
as well as what each one costs. And **quality**, because a context near its limit is already past
the point where recall holds up ({{topic:fromprompt}}).

The upshot: an agent that answers correctly on a clean first turn and badly on turn twelve usually
has a budget problem, not a prompt problem.

## How it works

### One window, shared with the output

"LLMs have a maximum number of tokens for input and output", and the usual expression of it is
combined. Microsoft's worked example uses a hypothetical model "with a maximum context window of
100 tokens": tokenised by word the input "is nine tokens. This leaves 91 word tokens available for
the output", while the same sentence tokenised by character "is 34 tokens (including spaces). This
leaves only 66 character tokens available for the output."

The numbers are illustrative; the shape is the lesson. Reserve room for the answer before you budget
anything else. An agent asked for a twenty-line summary needs that reservation; one that emits a
one-line verdict does not.

### A character budget is not a token budget

"The specific tokenization method varies by LLM." GPT models use "a type of subword tokenization
that's known as Byte-Pair Encoding (BPE)", and the trade-offs run in both directions: smaller
tokens mean "A given text is broken into more tokens, requiring additional computational resources
while processing", while with larger tokens, "Given the same token limit, the maximum size of the
model's input and output is larger."

Two consequences. You cannot carry a token count across a model change, so a budget is pinned to a
deployment. And you have to count rather than estimate — the mechanics are {{topic:tokenbudget}},
and the docs point at OpenAI's tokenizer tool for seeing the split.

### The soft ceiling is the one that bites

The hard ceiling produces an error you can see. The soft ceiling produces a worse answer that looks
fine. Context must be "treated as a finite resource with diminishing marginal returns", and models
"may show reduced precision for information retrieval and long-range reasoning" well before they
run out of room.

So the budget you hold yourself to sits below the limit, and what justifies it is an evaluation
score, not a token count. The loop: name the segments, measure each, cut the largest, re-run the
eval set ({{topic:evalstrategy}}, {{topic:mafeval}}). A cut that does not move the score is a cut
you keep.

### The line items

| Segment | Paid when | Shrunk by |
|---|---|---|
| System instructions | Every turn | Layering and pruning ({{topic:sysprompt}}) |
| Tool definitions | Every turn, for every tool | Fewer, narrower tools ({{topic:toolshaping}}) |
| Retrieved knowledge | When retrieval runs | Fetching on demand instead of preloading ({{topic:jit}}) |
| Conversation history | Every turn, growing | Compaction and truncation ({{topic:history}}) |
| Tool results | Per call, and they persist | Shaping the result at the source ({{topic:toolshaping}}) |
| Long-term memory | Every turn it is injected | Deciding what may be remembered ({{topic:memory}}) |
| The answer | Every turn | Asking for the format you need ({{topic:structured}}) |

Caching does not shrink any of these, but it changes what the stable ones cost — which is why the
stable parts go first ({{topic:caching}}).

## In practice at Technik

The capstone's per-turn context is short enough to enumerate. Fixed: `agent/instructions.md` at 37
lines and 1,836 characters; three tool definitions, each a docstring of roughly 250 characters plus
five typed parameter patterns; and the server's one-sentence `instructions` string. Variable: the
question, up to six tool results, and the answer.

Four decisions in the code hold the variable half down. The first is the result format. Tools return
assembled lines rather than rows, so a column name is written once instead of once per row:

*From [`server/teamcenter.py`, lines 88–94](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/server/teamcenter.py#L88-L94):*

```python
    first = revisions[0]
    lines = [f"{doc_no}: {first['TITLE']} ({first['DOC_TYPE']}), owner {first['OWNER']}"]
    for r in revisions:
        released = f", released {day(r['RELEASED_AT'])}, next review {day(r['NEXT_REVIEW_DATE'])}" \
            if r["STATUS"] == "Released" else ""
        lines.append(f"  rev {r['REVISION']}: {r['STATUS']}{released}")
    return "\n".join(lines)
```

That matches Microsoft's own space-efficiency advice for prompts, which prefers a tabular layout
"rather than preceding every field with a name (such as with JSON)". The second: a superseded
revision's release date is left out entirely — columns of a row that is not the answer. The third is
`day()`, which truncates a Snowflake timestamp to ten characters, because `2026-09-14` answers every
question asked of it and `2026-09-14 03:11:52.000` answers no more. The fourth is the cap: six tool
calls, so at most six results accumulate behind one answer ({{topic:loop}}).

<!-- unknown since=2026-11 -->
The capstone's context has never been measured in tokens. It never ran against a live model
deployment, so the figures above are lines and characters, which are not tokens. Count your own
with the tokenizer of the model you deploy before you rely on any of them as a budget.
<!-- /unknown -->

## Design guidance

- **Reserve the output first.** Decide the longest answer you will accept, subtract it, then budget
  the input against what is left.
- **Pin the budget to a deployment.** Record the model and tokenizer beside the numbers; a model
  change invalidates them.
- **Count, don't estimate.** Characters and words both mislead, in different directions, for
  identifiers and code.
- **Give every segment an owner.** A line item nobody owns only ever grows.
- **Spend against evals, not the limit.** Cut, re-run the set, keep the cut if the score holds.
- **Watch the per-tool multiplier.** One more tool is paid on every turn, including the turns
  needing none of them.
- **Trim at the source.** A result shaped in the tool costs less than the same result trimmed after
  it has entered the window.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The answer is cut off mid-sentence | Input filled the combined window; nothing was reserved for output | Reserve output tokens and cap the input segments |
| A budget that fitted last month overflows now | The model changed, so the tokenizer changed | Re-measure per deployment; keep the figures with the model name |
| Cost per answer rises while questions stay the same | History accumulating, or tool results persisting across turns | Compact ({{topic:history}}); cap tool calls |
| Requests start failing under load, not individually | A tokens-per-minute limit, not a window limit | Shrink per-request context; check the TPM quota |
| Quality degrades long before the limit is reached | The attention budget, not the window | Hold a working budget below the limit and verify with evals |
| Trimming the instructions barely helped | Instructions were never the largest line item | Measure every segment before cutting any of them |
| A JSON tool result dwarfs the answer it supports | Keys repeated per row, timestamps and nulls included | Return assembled lines; drop fields nothing reads |

## Key terms

**Context window** — the maximum number of tokens a model can process in one request, usually
covering input and output together.

**Token** — the unit text is broken into before the model reads it: "words, character sets, or
combinations of words and punctuation".

**Byte-Pair Encoding (BPE)** — the subword tokenization that GPT models use; the reason a token
count is a property of the model, not of the text.

**Tokens per minute (TPM)** — a throughput quota enforced alongside the per-request limit, which
large contexts consume faster.

**Line item** — one named segment of the budget (instructions, tool definitions, history, results)
with a measured size and an owner.
