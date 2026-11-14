## TL;DR

Hybrid search sends one request that carries both a keyword query and a vector query. The two run in parallel and a
merge step, Reciprocal Rank Fusion, produces one ranked list. A semantic ranker can then re-score the top of that list
with a language model. Each layer covers a gap in the one before it: keywords catch the exact code a vector blurs,
vectors catch the paraphrase a keyword misses, and the ranker sorts what both found. Each also has a boundary the
pages state plainly, and the boundaries are what you design around: the ranker sees only the top 50 results, only text,
and only as much of each document as fits its input.

## Why it matters

{{topic:embeddings}} showed that a vector query always returns *k* results, near or not, and that an identifier
such as `DU700001042` wants an exact match. Hybrid search is the product answer to both. It is also where a good
index quietly loses quality, through a truncated field, a sort order that overrides relevance or a threshold set too
fine. The rest of this lesson is those places.

## How it works

### One request, two retrievals

<!-- volatile verified=2026-11 -->
A hybrid query is a single request with `search` for the full-text query and `vectorQueries` for one or more vector
queries. The text side is ranked with BM25 and the vector side with HNSW or exhaustive nearest-neighbour search. Reciprocal
Rank Fusion merges the two lists into one. The same request can use filters, facets, sorting, scoring profiles and the
semantic ranker on its text fields. The page names what keyword search is better at, which is product codes,
specialised jargon, dates and people's names, and says benchmark testing shows hybrid retrieval with the semantic
ranker gives significant relevance gains.
<!-- /volatile -->

Four notes from the page's sample query bear on design. If you use the semantic ranker, set `k` to 50 to maximise its
inputs. Return only human-readable text fields in `select`, since those are what a person or a model will read. Filters
can run at the start or the end of query processing, and with the semantic ranker you probably want the end, though you
should test. And leave out `orderby`: an explicit sort overrides relevance ranking.

<!-- unknown since=2026-11 -->
The roadmap says hybrid beats vector-only search for most enterprise content. The page's claim is narrower: benchmark
tests on real and benchmark datasets show benefits for hybrid with the ranker, with no dataset named and no figure.
It does not say that vector-only search loses on most content, and it does not say how a keyword analyzer treats a
code such as `SWI70000318`.
<!-- /unknown -->

### What the semantic ranker does

<!-- volatile verified=2026-11 -->
The ranker is a second pass. It takes a result already ranked by BM25 or RRF and re-scores it with language models
adapted from Bing. It reranks text only, and only the top 50 results go in. It cannot rerun the query over the whole
corpus, so a good chunk ranked 51st never reaches it. Each document is summarised before scoring: up to 2,000 tokens
in, drawn from the `title`, `keywords` and `content` fields of the semantic configuration. `title` and `keywords` each
take at most 128 tokens and `content` gets the rest. Text beyond the limit is ignored, which is why you list fields in
priority order. The summary string passed to the ranker is capped at 2,048 tokens.
<!-- /volatile -->

<!-- volatile verified=2026-11 -->
Each result gets a `@search.rerankerScore` from 4 to 0, where 4 means highly relevant and complete, 3 relevant but
lacking detail, 2 partly relevant, 1 relevant to a small part and 0 irrelevant. The page warns that the distribution
varies slightly with infrastructure and model updates, so a minimum threshold should not be too granular. The ranker can
also return captions and answers, which are always verbatim text from your index, because no generative model is
involved. It works best on information-rich prose. It is a premium feature billed by use, with a free allowance, and
it is charged when `queryType` is `semantic` and the search string is not empty. A preview query-rewrite feature
expands a query into up to ten variants.
<!-- /volatile -->

## In practice at Technik

Take a question that mixes an identifier and an idea: *what did `ECN70000042` change about preparation before
cladding?* The code is an exact term, and the change is a concept. A vector query alone may rank a chunk about
cladding preparation from any revision, and a keyword query alone matches the ECN number and nothing about the change.
Hybrid search brings both, and a filter keeps the draft out:

<!-- volatile verified=2026-11 -->
*Adapted from the hybrid query on the hybrid search page, for the controlled-documents index of {{topic:vector}}:*

```json
{
  "search": "ECN70000042 preparation before cladding",
  "select": "doc_no, revision, section, content",
  "filter": "status eq 'Released'",
  "vectorFilterMode": "postFilter",
  "vectorQueries": [
    { "kind": "vector", "vector": [ <array of embeddings> ],
      "k": 50, "fields": "content_vector" }
  ],
  "top": 10,
  "queryType": "semantic",
  "semanticConfiguration": "controlled-docs"
}
```
<!-- /volatile -->

<!-- unknown since=2026-11 -->
Nobody ran this query. The page's sample filters on a geographic distance, so the `eq` filter on `status` is the
course's own, written in the filter language's usual form and not checked against a service. The index and the
configuration name are invented.
<!-- /unknown -->

Three of the page's limits show up at once. The semantic configuration should put `section` in the title slot and `content` after it, and the chunk has to fit the 2,000-token input, so {{topic:chunking}}'s chunks must be small enough that nothing
is cut. The top 50 is a hard cut, and Technik has near neighbours that compete for it: `SWI70000318`, `DGL70000009`
and the Standards site's *Weld Overlay Acceptance Criteria* summary all discuss overlay limits. Document type and
precedence are the agent's job to say aloud, because the ranker will score all three as relevant.

The reranker score also gives a coarse answer to a problem {{topic:embeddings}} left open: what counts as no match. A
result scoring below 2 answers at most a small part of the question on the page's own scale, so an agent can say it found nothing solid.
Where to draw that line is a choice to test, and the page's warning applies, so set a band and not a decimal.

## Design guidance

- **Use hybrid when queries mix identifiers and ideas**, and keep an exact lookup for a pure identifier.
- **Set `k` to 50 with the semantic ranker**, and expect nothing beyond it to be reranked.
- **List semantic fields in priority order**, with chunks small enough to fit the ranker's input.
- **Do not sort.** An explicit order replaces relevance.
- **Treat reranker scores as coarse.** Draw a no-match line by band, and recheck it after model updates.
- **Test filter placement** with the ranker on, as the page advises.
- **Evaluate with and without the ranker** on your own labelled questions ({{topic:rageval}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The right chunk never appears, though it exists | It ranked below 50 before reranking | Raise `k` to 50, or tighten the query and filters |
| Relevance looks random after adding a sort | `orderby` overrides ranking | Remove the sort |
| A long section is judged on its first half | The ranker's input limit cut the rest | Chunk below the limit, and order fields by priority |
| An exact code is not found | Keyword matching on the code is unchecked | Test it, and use an exact lookup for codes |
| A threshold flips results after an update | Score distributions shift | Use coarse bands, not fine cut-offs |
| A cost line appears for semantic queries | It is billed per query with a non-empty search | Watch the allowance, and skip it where it does not help |

## Key terms

**Hybrid search**: one request with a text query and vector queries, merged into one ranking.

**Reciprocal Rank Fusion (RRF)**: the method that merges the ranked lists into one.

**Semantic ranker**: a second pass that re-scores the top 50 results with language models.

**Reranker score**: the 0 to 4 relevance score the semantic ranker assigns.
