## TL;DR

{{topic:embeddings}} covered the vector. This lesson covers where vectors live: a search index. Its design decides
what an agent can find: which fields hold text, which hold vectors, which hold metadata you can filter on, and how
content gets in. Azure AI Search keeps vector fields beside ordinary ones, so one index serves keyword, vector and
filtered queries. One rule carries the lesson. A vector field cannot be filtered, so every condition that must always
hold, such as *released revisions only*, needs a metadata field of its own.

## Why it matters

Poor retrieval gets blamed on the embedding model, and a good share belongs to the index: a field never added, a
filter never applied, content that never arrived or arrived stale. The model can only rank what the index holds, so
for an agent whose answer a person acts on, that is the first design decision.

## How it works

### An index of fields

The Azure AI Search page says vector support is implemented at the field level. An index can contain vector and
nonvector fields, and a query can target both. Internally the service builds a vector index for each vector field,
using a nearest-neighbours algorithm that places similar vectors close together. The service also stores the data
you query over, which the page calls using it as a vector database: long-term memory, a knowledge base, or grounding
data for retrieval-augmented generation.

<!-- unknown since=2026-11 -->
The roadmap says the index design, the embedding model and the filters decide what the agent can find. The page
documents the filters and says little about the index design. It gives no guidance on field layout, dimension
limits or index size, and names no index algorithm. The hybrid page names two ways vectors are ranked, HNSW and
exhaustive nearest-neighbour search, and leaves their trade-off to other pages.
<!-- /unknown -->

### Getting content in

<!-- volatile verified=2026-11 -->
There are two routes. With internal processing, an indexer pipeline chunks and embeds the content itself. That
needs an indexer, a supported data source and a skillset, and Azure AI Search then calls your embedding endpoint.
With external processing, you generate embeddings yourself and push the prevectorized content into the index's
vector fields. The route you pick decides who owns freshness. An indexer can automate ingestion from a data
platform such as Blob Storage or OneLake. A pushed index is only as fresh as the code that pushes it, and the page
says nothing about how to schedule either.
<!-- /volatile -->

At query time the same choice appears again. Your client can encode the question, or a vectorizer in the service can.
Either way the service returns the requested *k* nearest neighbours.

### Filtered vector search

<!-- volatile verified=2026-11 -->
A query can carry a vector query and a filter expression together. Filters apply to text and numeric fields, which
makes them the tool for metadata and for including or excluding results. A vector field itself is not filterable, so
you add a filterable text or numeric field beside it. The search engine can process the filter before or after
the vector query. The hybrid page adds that with the semantic ranker you probably want post-filtering as the last
step, and that you should test which is better for your queries ({{topic:hybrid}}).
<!-- /volatile -->

<!-- unknown since=2026-11 -->
Neither page says what each mode does to the number of results. A filter applied after the *k* nearest neighbours
are found can leave fewer than *k* results, or none, and a filter applied before cannot. That follows from the
description, but nothing documents it. Test a filter that excludes most of the index.
<!-- /unknown -->

### How an index reaches an agent

<!-- volatile verified=2026-11 -->
For Foundry agents the page describes a chain. You create an indexed knowledge source that points to a search index
with vector fields and a vectorizer, parent it to a knowledge base, and connect the knowledge base to Foundry
Agent Service. {{topic:agentic}} covers what the knowledge base does with a question. Vector search is available in
all regions and tiers at no extra charge, though embedding and enrichment calls can bill from the model provider.
Some services created before 1 January 2019 do not support vector fields: adding one fails, and the fix is a new service.
Services created after 3 April 2024 have higher vector quotas.
<!-- /volatile -->

## In practice at Technik

The capstone has no search index. Its server declares that it "holds metadata, not document text", and
`get_document` returns a document's title, owner and the status of each revision, and never what it says. Questions about what a
document says need an index. Technik's engineering questions, such as *which document covers weld prep inspection,
and what does it say about acceptance criteria?*, are the ones that do.

Suppose the controlled-documents index holds one row per chunk:

| Field | Example | Kind |
|---|---|---|
| `doc_no` | `SWI70000318` | Filterable text |
| `doc_type` | `SWI` | Filterable text |
| `revision`, `status` | `B`, `Released` | Filterable text |
| `section` | `5.2 Visual and dye-penetrant inspection` | Searchable text |
| `content` | The chunk's text | Searchable text |
| `content_vector` | The chunk's embedding | Vector |

The filter earns its row. Revision B of `SWI70000318` is released, and revision C is in draft, with a tightened
porosity limit in section 5. A question about the limit is conceptual, which is exactly what vector search is for, and
revision C's sentence can be the closest match to a question about a stricter limit. With no filter on `status`, the agent
can quote a limit the shop is not yet inspecting to. The two controls are layers: index only
released content, and filter on `status` anyway. The second still holds on the day someone indexes a draft by mistake.

Where the content comes from is part of the design. Released revisions are published as PDFs to the Controlled
Documents library. Drafts live in the manufacturing engineering team's own site, which production cannot open, so an
index built from that site would show production users text they could never have opened themselves. Permission trimming
is {{topic:agentic}}'s subject, and this page documents nothing on it.

<!-- unknown since=2026-11 -->
The scenario does not say whether a superseded PDF leaves the library when the next revision is published. If it
stays, an index built from the library holds revision A beside revision B, and only the `status` filter or a delete in
the pipeline keeps revision A out of answers.
<!-- /unknown -->

## Design guidance

- **Decide the fields before the model.** List which are searchable, which are vectors and which are filterable.
- **Put every must-hold condition in a filterable field.** Status, document type and revision belong there.
- **Do not index what a user may not see**, and do not rely on a filter alone to hide it.
- **Choose who owns freshness.** A push is as fresh as your code.
- **Test a filter that removes most of the index**, and count the results.
- **Keep identifiers searchable as text.** An exact number is a keyword job ({{topic:embeddings}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| An answer quotes a limit from a draft | Draft text is indexed and no filter excludes it | Index released content only, and filter on `status` |
| A filter on the vector field is rejected | A vector field is not filterable | Add a filterable text or numeric field |
| Adding a vector field fails | The service predates 2019 | Create a new search service |
| Answers quote a superseded revision | The old PDF stayed in the source, or the push never ran | Delete on supersession, and filter on `status` |
| A production user is shown text they cannot open | The index was built from a restricted source | Index only what the audience may read |

## Key terms

**Search index**: the store Azure AI Search queries, with fields of several kinds.

**Vector field**: an index field holding embeddings, searched by similarity and not filterable.

**Filterable field**: a text or numeric field that a query can use to include or exclude results.

**Vectorizer**: the component that turns query text into a vector inside the search service.

**Knowledge source**: a definition of searchable content, which can point to an index with vector fields.
