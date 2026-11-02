## TL;DR

History is the only line item that grows while you do nothing. It also degrades quality in a way
volume alone does not explain: Liu et al. found a **U-shaped performance curve**, where models use
information best at the start and end of a context and worst in the middle, and that
extended-context models are "not necessarily better than their non-extended counterparts at using
their input context". A bigger window is not a strategy. The strategies are reduction — truncation
and summarization — plus **compaction**, which restarts the window from a summary, and **notes kept
outside the context**.

## Why it matters

Intermediate told you history is re-sent on every turn ({{topic:contextcost}}), and {{topic:budget}}
made it a line item with an owner. What makes it unlike the others is that nobody has to add
anything for it to grow: instructions change when you edit them, but history grows because the user
asked a second question.

So any agent that holds a conversation needs a reduction policy *before* it ships — the first long
session is when you find out you have none. And what degrades is not only recall but position: a
constraint stated on turn two sits, by turn twenty, in the region of the window the model handles
worst.

## How it works

### Position, not just volume

*Lost in the Middle* (Liu et al., TACL 2023) tested multi-document question answering and key-value
retrieval while moving the relevant information around the context. Performance "is often highest
when relevant information occurs at the beginning or end of the input context, and significantly
degrades when models must access relevant information in the middle of long contexts, even for
explicitly long-context models." The paper calls the two ends **primacy bias** and **recency bias**.

The effect is large: multi-document QA performance "can drop by more than 20%", and in the worst
positions one model scored below its own closed-book baseline of 56.1% — worse with the documents
than with none. Nor does more context buy more answer: 50 documents instead of 20 "only marginally
improves performance (∼1.5%…)". And where a context fitted both a model and its extended-context
version, "performance between them is nearly identical" — so you cannot buy your way out of history
management with a 128k window ({{topic:tokenbudget}}).

### Four ways to make it smaller

Microsoft's RAG guidance names four strategies for when "the total token count exceeds the context
window", and they are not interchangeable. **Truncation** removes the lowest-ranked content until the
prompt fits, so whatever went is gone. **Summarization** condenses it first, which "introduces an
extra inference call and risks information loss". **Map-reduce** and **iterative refinement** answer
in batches and combine — chunk strategies, not history ones.

For conversation the guidance is concrete: include "the recent conversation history (typically two to
five turns)", and "Summarize older turns if you need to preserve context beyond the recent window".
It also gives the step people forget — before retrieval runs, "Rewrite the current user query as a
self-contained query that resolves all coreferences". *"And the other one?"* is not a search query.

### Compaction, and how to tune it

Compaction is the agent-shaped version of summarization: "taking a conversation nearing the context
window limit, summarizing its contents, and reinitiating a new context window with the summary." The
summariser is told what to value — it "preserves architectural decisions, unresolved bugs, and
implementation details while discarding redundant tool outputs or messages".

The risk is named: "overly aggressive compaction can result in the loss of subtle but critical
context whose importance only becomes apparent later." So the tuning advice is to "Start by
maximizing recall… then iterate to improve precision" — recall first, precision second, which is the
opposite of how most summariser prompts get written.

There is also a cheaper intervention to reach for first. "One of the safest lightest touch forms of
compaction is tool result clearing": once a tool has been called far back in the history, the raw
result rarely needs to be there ({{topic:toolshaping}}).

### Notes outside the window

The third technique moves state out of the conversation entirely. **Structured note-taking**, "or
agentic memory, is a technique where the agent regularly writes notes persisted to memory outside of
the context window", which "get pulled back into the context window at later times" — a to-do list,
or a notes file. Its value is surviving a reset: the agent reads its own notes and carries on. This
is session working state, not remembered facts about a person ({{topic:memory}}).

The three are not ranked. Compaction "maintains conversational flow"; note-taking "excels for
iterative development with clear milestones"; and sub-agents suit parallel exploration, each
returning "only a condensed, distilled summary of its work (often 1,000-2,000 tokens)"
({{topic:multiagent}}).

### What the runtime gives you

<!-- volatile verified=2026-11 -->
Agent Framework's packaged Harness does some of this for you. Its chat pipeline "adds function
invocation, message injection, per-service-call history persistence, and optional compaction", and
compaction is "Enabled when token limits or a custom strategy are supplied in .NET and Python" — Go
"requires explicit provider composition". The toggle is `disable_compaction`, and the page's example
passes `max_context_window_tokens=128_000`.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
What the Harness page does not document: the default compaction strategy, what a compacted history
keeps, whether compaction runs when nothing is configured, and whether that token option is the
"token limit" that enables it. Truncation and trimming are not mentioned at all. So do not assume
the runtime protects you; check what your configuration produced.
<!-- /unknown -->

## In practice at Technik

The capstone's history budget is zero, by decision rather than omission:

*From [`agent/main.py`, lines 57–64](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/agent/main.py#L57-L64):*

```python
async def ask(question):
    from agent_framework.foundry import FoundryChatClient
    from azure.identity.aio import AzureCliCredential

    async with AzureCliCredential() as credential, teamcenter_server() as server:
        client = FoundryChatClient(credential=credential, function_invocation_configuration=TOOL_LOOP)
        agent = build_agent(client, server)
        print((await agent.run(question)).text)
```

One question, one process, no session — so there is no earlier turn to compact, and no middle of the
context for a constraint to get lost in. The three tools take explicit identifiers, which is what
makes that viable: every question carries its own `SWI70000318` or `100004521`, so nothing resolves
*"that drawing"* against a previous turn.

Two things change the day a session is added. The query rewrite stops being optional, because a
planner reading *"and revision C?"* without the previous turn will look up a document called
"revision C". And the groundedness guard needs re-reading: it refuses any answer with no
`function_result` in the response, and a compaction summary is not a tool result — so summarise a
turn whose answer came from a tool, ask a follow-up the summary already answers, and a correct answer
becomes the refusal ({{topic:loop}}, {{topic:stageagent}}). Compaction does not only shorten the
history; it changes what downstream checks can see.

## Design guidance

- **Decide the policy before launch.** *Keep the last N turns, summarise beyond that* is a policy;
  *the window is big* is not.
- **Put durable constraints last**, where recency bias helps them.
- **Rewrite the question before retrieval.** The cheapest fix a multi-turn agent has.
- **Clear tool results before summarising.** The lowest-risk reduction available.
- **Tune the summariser for recall, then prune.** A summary that drops the constraint that mattered
  is worse than a long history.
- **Keep working state in notes.** A to-do list survives a reset; turn fourteen does not.
- **Test after reduction.** Run the eval set on a compacted session, because that is the session
  your users have ({{topic:evalstrategy}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent forgets a constraint set earlier in the chat | It now sits mid-context, where recall is worst | Re-state durable constraints near the end of the context |
| Quality drops off a cliff at a predictable point | Compaction ran and dropped something load-bearing | Tune the compaction prompt for recall; log what it kept |
| Retrieval returns nothing sensible on a follow-up | The query still contains *it*, *that one*, *the same* | Rewrite the query as self-contained before searching |
| A correct answer becomes a refusal after compaction | A downstream check wants a tool result the summary lacks | Re-check guards that inspect the message history |
| Two sessions answer the same question differently | One had been compacted and the other had not | Make compaction deterministic; record it in the trace ({{topic:tracing}}) |

## Key terms

**Compaction** — summarising a conversation nearing the window limit and reinitiating a new context
window from that summary.

**Tool result clearing** — dropping the raw results of earlier tool calls; the lightest-touch form
of compaction.

**Structured note-taking** — the agent writing notes outside the context window and reading them
back later.

**Primacy and recency bias** — the measured tendency to use information at a context's start and end
better than information in its middle.

**Query rewriting** — restating the question as a self-contained one, resolving references to earlier
turns, before retrieval runs.
