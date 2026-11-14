## TL;DR

A RAG answer can fail in two places, and a metric that cannot say which one is a guess. Foundry names the halves
*process* evaluation, which asks whether retrieval fetched the right chunks, and *system* evaluation, which asks whether
the answer used them well. Retrieval can be scored precisely against human relevance labels, or roughly by a judge with
no labels. The answer is scored on groundedness, completeness and relevance, and the Azure architecture page adds
utilization and correctness. The metrics diagnose in pairs. Model answers vary, so score against a range.

## Why it matters

Without the split, every bad answer gets the same treatment: tune the prompt. The architecture page's order is the
opposite. It has you evaluate chunking, embedding and search first, and be confident the system returns relevant
grounding data before you judge the model's call. {{topic:chunking}} and {{topic:cortexsearch}} each ended with
*measure on your own labelled questions*. This lesson is how, and it protects a choice the chunking page calls
semipermanent.

## How it works

### Two halves

| Half | Evaluator | Needs | Returns |
|---|---|---|---|
| Retrieval | Document Retrieval | Human relevance labels and the search system's scores | Fidelity, NDCG, XDCG, max relevance and Holes, each with pass or fail |
| Retrieval | Retrieval | The query and the retrieved context, no labels | A judge's 1–5 score |
| Answer | Groundedness | The response and the context | A judge's 1–5 score |
| Answer | Relevance | The query and the response | A judge's 1–5 score |
| Answer | Response Completeness (preview) | The response and the expected answer | A judge's 1–5 score |

<!-- volatile verified=2026-11 -->
The Foundry page's reasoning is that retrieval sits upstream: if it is poor and the answer needs corpus-specific
knowledge, a model has little chance. Its judge-based evaluators pass at a default threshold of 3.
<!-- /volatile -->

### The labelled set

<!-- volatile verified=2026-11 -->
Document Retrieval compares what the search returned with what a person said it should return. The labels, one per
document, are the page's `retrieval_ground_truth`, and by SDK default run from 0 to 4. The results are
`retrieved_documents`, each with the search system's own score. Fidelity is the share of the known good documents that
came back. NDCG asks whether they came in a good order. XDCG scores the top results. Holes counts retrieved documents
that have no label, a check on the label set itself. The page's use for all this is a **parameter sweep**: generate
retrieval results for each search algorithm, `top_k` and chunk size you want to try, and keep the combination that
scores best.
<!-- /volatile -->

*Adapted from the document retrieval example on the RAG evaluators page, for one Technik question:*

```python
# Written by a person: 0 = irrelevant, 4 = the answer.
retrieval_ground_truth = [
    {"document_id": "SWI70000318-s5", "query_relevance_label": 4},
    {"document_id": "DGL70000009-s3", "query_relevance_label": 2},
    {"document_id": "WOAC-summary", "query_relevance_label": 1},
]

# What the search returned, best first, with its own score.
retrieved_documents = [
    {"document_id": "WOAC-summary", "relevance_score": 3.1},
    {"document_id": "SWI70000318-s5", "relevance_score": 2.7},
    {"document_id": "SOP70000101-s3", "relevance_score": 0.9},
]
```

The last result has no label, so it is a hole. Label every result you expect to see, irrelevant ones as 0.

### Reading the metrics in pairs

The architecture page's advice is that no single metric explains a result, and it pairs them.

| Pattern | Reads as | Look first at |
|---|---|---|
| High groundedness, low correctness | The answer used the context faithfully, and the context or the conclusion is wrong | The source data, then the prompt |
| High utilization, low completeness | Retrieval is accurate and incomplete | More chunks, ranking, the prompt |
| Low utilization, high completeness | Irrelevant chunks come back too | A lower `top_k` |
| Low on both | The chunks do not carry the answer | Chunking, `top_k`, the prompt |

Two warnings. *Completeness* has two definitions. Foundry's compares the response with an expected answer, which is
recall. The architecture page checks whether each intent in the query is answered by the retrieved documents, and
squares the ratio. Name the one you use. And for low groundedness the architecture page lists retrieval-side remedies,
adding data and adjusting chunking, so read a generation metric beside a retrieval one before you act.

### Variation and upkeep

Model responses are nondeterministic, and the page says to aim for a target range, not a single figure. For correctness
it suggests a model other than the one that wrote the answer. It says to record every run's hyperparameters with its
results and to automate it, since a real sweep means hundreds of runs, and to revisit the work as documents and
questions change. For agentic retrieval it adds tool selection accuracy, tool calls per request and latency, in an
article this lesson does not cover. Its responsible-AI section adds content safety, protected material, indirect prompt
injection and privacy ({{topic:ctxsecurity}}).

## In practice at Technik

Build the set in three groups: questions with a governing document, questions where near neighbours compete, and
questions with no answer. Four rows from the scenario:

| Question | Relevant | Competing | A pass |
|---|---|---|---|
| Minimum overlay thickness on an XT bore? | `SWI70000318` section 5 | `DGL70000009` section 3 explains it, and a Standards summary repeats it | The work instruction ranks first and is cited |
| Hold time for the hydrostatic test? | `SWI70000402` | None | Found and quoted exactly |
| What does revision C of `SWI70000318` change? (a production user) | No released revision C | The draft, in a site production cannot open | Nothing from the draft comes back, and revision B is named |
| Minimum overlay for Inconel on a manifold header? | None | `SWI70000318`, the closest | The agent abstains and names the nearest document |

Suppose, with invented figures, that the first question returns the Standards summary at rank one and the work
instruction at rank two. The answer cites the summary and is right today, because the two say the same thing. Every
system metric passes. Document Retrieval does not, since NDCG falls when the document labelled 4 is not on top. Only the
split shows this failure: a right answer from the wrong rank, waiting for the day revision C is released and the
summary is not updated ({{topic:grounded}}). The sweep is then plain. Compare vector-only with hybrid and the semantic
ranker ({{topic:hybrid}}), and section-based chunks with fixed ones ({{topic:chunking}}), one change per run.

<!-- unknown since=2026-11 -->
Nobody ran this. The document ids above name sections, and the page says only *documents*, so check whether the
evaluator treats a section or a whole file as the unit, and label at the level you retrieve. The capstone has no
retrieval step to score. Its eight cases grade tool calls, and the figures here only illustrate.
<!-- /unknown -->

## Design guidance

- **Score retrieval and the answer apart**, and read the metrics in pairs.
- **Write the labelled set before you tune**, with neighbour, absent and permission cases in it.
- **Label every result you expect to see**, irrelevant ones included, so Holes stays at zero.
- **Change one thing per run** in a sweep, and keep the settings beside the scores.
- **Aim for a range**, repeat runs, and judge correctness with a different model.
- **Add a case for every production failure** ({{topic:prodfeedback}}), and review the set as documents change.
- **Score the route as well**, because a right answer from the wrong tool is luck ({{topic:routing}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The answer is right and the retrieval metric is low | The right document ranks below a summary | Fix the ranking before the summary goes stale |
| A re-chunk moved the score and nobody knows why | Several settings changed in one run | Change one thing at a time |
| Groundedness is high and the answer is wrong | The source is wrong or stale | Correct the source, and add a correctness case |
| Holes is above zero | Results came back with no label | Label them, irrelevant ones as 0 |
| The same case scores differently across runs | A judge is not deterministic | Use a range, and repeat the run |
| Two tools disagree on completeness | The definitions differ | Name the one you use |

## Key terms

**Process evaluation**: scoring the retrieval step against the query or against labelled documents.

**System evaluation**: scoring the final answer for groundedness, relevance and completeness.

**Query relevance labels**: human judgements of how well each document answers a query, the ground truth for retrieval.

**Utilization**: how much of the retrieved context the answer actually uses.

**Parameter sweep**: comparing retrieval settings, one change at a time, on a fixed question set.
