## TL;DR

Preloading every document an agent might need is a bet that you can predict relevance before the
question is understood. The alternative, which Anthropic's engineering team calls "just in time"
context, is to hold **lightweight identifiers** and resolve them with tools at runtime. Most capable
agents end up hybrid: a small core loaded up front for speed, the rest fetched on demand. The
trade-off is stated plainly — "runtime exploration is slower than retrieving pre-computed data", and
an unguided agent "can waste context by misusing tools, chasing dead-ends, or failing to identify
key information".

## Why it matters

Intermediate attached knowledge sources and let the orchestrator decide what to pull in
({{topic:sources}}, {{topic:rag}}). The question you answered was *which library*; the platform
answered *when*. Pro-code hands you the *when*, the largest lever on the budget, because retrieved
knowledge is the line item that can arrive in arbitrary quantity ({{topic:budget}}).

It is also the lever most often pulled the wrong way. Stuffing feels safe — the document is
*there*, so the model cannot miss it. But a window near its limit is already past the point where
recall holds up, so the document that is *there* is also the document competing for attention
({{topic:fromprompt}}). Preloading trades a certainty you do not have (this will be needed) for a
cost you certainly pay (every turn, for every token).

## How it works

### Pre-inference retrieval, and what it assumes

The established pattern is to retrieve before the model runs: "many AI-native applications employ
some form of embedding-based pre-inference time retrieval to surface important context for the agent
to reason over." For a narrow, well-understood question set it is still the right answer. What it
assumes is that the question is answerable by similarity to an embedded chunk, decided before the
agent has reasoned at all — which is what breaks on compound questions, and why the same problem
gets attacked by planning the queries instead of the chunks ({{topic:agentic}}, {{topic:hybrid}}).

### Identifiers instead of payloads

The just-in-time move is to keep the pointer and leave the payload where it is. "Rather than
pre-processing all relevant data up front, agents built with the 'just in time' approach maintain
lightweight identifiers (file paths, stored queries, web links, etc.) and use these references to
dynamically load data into context at runtime using tools."

Two things follow, and the second is the one people miss.

First, a pointer costs a fraction of what it points at, and it does not go stale the way an index
does. Anthropic's own coding agent analyses large databases by writing targeted queries and using
shell commands like `head` and `tail`, "without ever loading the full data objects into context."

Second, the *names* are information. Hierarchies, naming conventions and timestamps "all provide
important signals that help both humans and agents understand how and when to utilize information",
which is what enables **progressive disclosure**, where agents "incrementally discover relevant
context through exploration": "file sizes suggest complexity; naming conventions hint at purpose;
timestamps can be a proxy for relevance." So your identifier scheme is a context design decision. An
opaque surrogate key tells the model nothing; `DU700001042` tells it what it is looking at before any
tool runs.

### The managed middle

Between a static index and an agent with a shell sits Azure AI Search's agentic retrieval, "a
multi-query pipeline designed for complex questions", where an LLM plans subqueries from your query
and conversation history, runs them in parallel and merges the reranked results. {{topic:agentic}}
covers the mechanism; three facts about it belong to the budget decision here.

<!-- volatile verified=2026-11 -->
Planning is a dial, not a fixed cost: at `minimal` retrieval reasoning effort "this step is skipped
and queries are issued directly to knowledge sources", and "Reasoning effort defaults to `low`".
Billing changes shape — the classic pipeline has a "Uniform cost per query", while agentic retrieval
is token-based with a "Variable cost per token (depends on reasoning effort)", so retrieval scales
with how hard the question is, not how often it is asked. And the cost is not only money: "Agentic
retrieval adds latency compared to a single-query pipeline, but it handles query complexity that a
single query can't."
<!-- /volatile -->

### The hybrid default

The recommendation is not purity. "In certain settings, the most effective agents might employ a
hybrid strategy, retrieving some data up front for speed, and pursuing further autonomous
exploration at its discretion. The decision boundary for the 'right' level of autonomy depends on
the task." Anthropic's own example preloads project context files while leaving `glob` and `grep`
for everything else, "effectively bypassing the issues of stale indexing".

The hybrid approach suits "contexts with less dynamic content, such as legal or finance work", and
as models improve, "the level of autonomy of agents can scale" — so the boundary you set today is a
property of your current model, not a permanent design.

## In practice at Technik

The capstone is just-in-time by construction, and the clearest evidence is what its MCP server
refuses to carry. The server's own description tells the model: "It holds metadata, not document
text." No document body ever enters the window — not `SWI70000318`'s section 5 tables, not one
revision's text. The agent gets enough to answer the question asked, plus the numbers it needs to
ask the next one.

The pointer-then-resolve pattern is written into a tool description:

*From [`server/teamcenter.py`, lines 97–103](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/server/teamcenter.py#L97-L103):*

```python
@mcp.tool()
def list_operation_documents(work_order: WorkOrder, operation_seq: OperationSeq) -> str:
    """List the drawing, CNC program and work instruction one work order operation uses.

    Drawings and CNC programs come with the revision the operation was released against. Check
    whether that revision is still the released one with get_revision_status.
    """
```

Two hops, on purpose. The first returns identifiers — `DU700001042`, rev B — and the second resolves
one against `V_RELEASED_REVISIONS`. A stuffing design would return the operation's documents *and*
every revision of each, which is how work order `100004510` sitting on a superseded drawing becomes
dozens of rows instead of two. The agent also cannot explore indefinitely: the loop caps
function calls at six, bounding the one real risk of runtime exploration ({{topic:loop}}).

Compare the SAP side, which the capstone deliberately does not expose. Technik's operation history
holds one row per confirmation, not per operation, so *"show me this work order's operations"* has a
result set nobody can predict from the question — the case for a narrow tool over a view, and for
leaving the aggregation in Snowflake, where it costs no context at all ({{topic:sfviews}}).

## Design guidance

- **Default to the pointer.** Preload what every question needs; make the rest reachable.
- **Make identifiers legible.** A naming scheme the model can reason about is retrieval guidance you
  never have to write.
- **Bound the exploration.** Just-in-time without a call cap trades a context problem for a cost
  problem.
- **Preload the map, not the territory.** An index of what exists beats one of the documents it
  lists.
- **Measure retrieval per question.** Token-billed retrieval scales with difficulty, not usage.
- **Re-check the boundary when the model changes.** A more capable model justifies less preloading.
- **Never preload to cover a weak tool.** Fix the tool; a document stuffed in to close a gap is
  paid for on every turn.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent ignores a document you preloaded | It arrived with everything else, with nothing marking it relevant | Retrieve it on demand, labelled ({{topic:xmltemplates}}) |
| Answers get worse as you add knowledge sources | Preloaded context is displacing the question and the tool results | Move sources behind tools; measure per question |
| The agent searches repeatedly and never answers | Runtime exploration with no stop condition | Cap function calls; on a miss, return what does exist ({{topic:planning}}) |
| Retrieval cost rises with no new users | Token-based billing, at a reasoning effort the questions do not need | Lower the effort; reserve planning for compound questions |
| A pointer the agent resolves returns nothing | The identifier was invented or reformatted | Type and pattern the parameter, and say so in the description ({{topic:toolshaping}}) |
| First answers are fast, later ones slow | Results accumulating behind one answer | Cap the calls; clear results nothing reads any more ({{topic:history}}) |
| Fresh data, stale answers | A pre-built index behind the retrieval step | Query the source at runtime, or re-check the index's refresh |

## Key terms

**Just-in-time context** — holding lightweight identifiers and loading the data they point to at
runtime, rather than pre-processing it up front.

**Pre-inference retrieval** — embedding-based retrieval run before the model, to surface context for
it to reason over.

**Progressive disclosure** — discovering relevant context incrementally through exploration, using
names, sizes and timestamps as signals.

**Hybrid strategy** — preloading some data for speed while leaving the agent free to explore
further.

**Agentic retrieval** — a multi-query pipeline that plans subqueries, runs them in parallel and
merges the reranked results.
