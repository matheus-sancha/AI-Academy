## TL;DR

Chunking decides what a retrieval system can return, because a chunk is the smallest thing it can hand back. The
Azure Architecture Center's page defines it as breaking documents into chunks that each hold semantically relevant
content, and calls it crucial. Its guidance is a menu, not a recipe: approaches from fixed-size splitting to prebuilt
models, matched to how much structure a document has. It gives no chunk size and no overlap amount, and it says to
experiment. This lesson uses the menu on Technik's controlled documents, where the structure is numbered sections
and the risk is a number separated from the sentence that gives it meaning.

## Why it matters

A retrieval system answers from chunks, so a fact that is split across two chunks may never reach the model whole,
and a chunk that carries the right number without its condition is worse than none. The page names both failures.
Chunks that are too small lack the context to answer, and relevant context spread over several chunks may not be
captured. Oversized chunks are expensive, can overwhelm the model's token limits and dilute the answer. The page
also warns that the choice is semipermanent: changing strategy can affect everything downstream.

## How it works

### The menu

<!-- volatile verified=2026-11 -->
The page matches approaches to document structure, from structured to unstructured:

| Approach | Suits | Effort | Cost |
|---|---|---|---|
| Prebuilt or custom model | Structured forms and invoices | Low to high | Medium to high |
| Document layout analysis | Semi-structured pages | Medium | Medium |
| Custom code, such as regular expressions | Structure you can infer | Medium | Low |
| Fixed-size with overlap | Prose with little structure | Low | Low |
| Sentence-based | Unstructured prose, as a fallback | Low | Low |
| Semantic chunking, by embeddings | Content with topical overlap | High | High |
| Language model augmentation | Images and tables turned into text | Medium | High |
| Graph-based | Unplanned quantitative queries | High | High |

Effort and cost are the page's own relative ratings and are labelled subjective. It lists Azure Content Understanding
and Document Intelligence as managed options, and both require uploading your documents, so check your
compliance rules first. For fixed-size chunking it advises BERT tokens over character counts and a chunk visualiser
for exploring where the splits fall.
<!-- /volatile -->

### Structure picks the approach

The page sorts documents into four kinds. **Structured** documents have fixed layouts, and models suit them.
**Semi-structured** ones share a schema but vary in layout, such as invoices. **Inferred** structure exists in the text
without markup, such as numbered clauses, and the page's advice is custom code, or a custom model if you have many
documents of the type. **Unstructured** text takes sentence-based or fixed-size splitting. It lists manufacturing
specifications among its examples of inferred structure. It then undercuts its own table: in practice any approach
might suit any document type, so test each and compare.

### Loading, combining and cost

Chunking first needs the document in memory. The page recommends starting with loading and chunking combined, and
separating them when you need to, for instance to keep a cleaned copy while you try several chunkers. If you separate
them, avoid an intermediate format, which can lose data. The economics are a count: how many distinct chunking
implementations you maintain, the per-document cost of each, and the numbers of initial and incremental documents. An
image or a table described by a language model adds cost per item. The page's savers are to classify first and cache
results by the image's hash.

<!-- unknown since=2026-11 -->
The roadmap says chunking that follows headings, tables and pages, with some overlap, usually works best. The page
says no such thing. It names overlap only for fixed-size chunking, gives no overlap amount and no chunk size, and states
there are no specific rules. {{topic:cortexsearch}} carries the one chunk-size recommendation in this module's sources, for a
single product. For everything else you measure ({{topic:rageval}}).
<!-- /unknown -->

## In practice at Technik

Technik's controlled documents have **inferred structure**. They are written in Word from a template, and the
released revision is published as a PDF with numbered sections. `SWI70000318` has section 4 for preparation and
section 5 for inspection, and section 5.2 holds two tables: indications up to 0.8 mm on sealing surfaces and 1.5 mm on
non-sealing ones. By the page's own table, the match for this structure is custom code.

A chunker for it splits at numbered headings and keeps three things together. The first is a section's heading with its
text, so a chunk knows it is *5.2 Visual and dye-penetrant inspection*. The second is a table with the sentence that
introduces it, because *0.8 mm* without *sealing surfaces* is a number with no meaning. The third is a chunk's own
document number, revision and type, kept as fields beside the text ({{topic:vector}}). The type matters more than it
looks. `DGL70000009` section 3 explains the 3.0 mm overlay thickness as 0.5 mm of dilution, 1.0 mm of machining and
1.5 mm of service, and it explains where `SWI70000318` section 5 sets it. A chunk that quotes the explanation without
saying it came from a design guideline lets the agent present a rationale as a requirement.

The economic question is how many chunkers to write. Technik has ten controlled document types. Suppose, as an
assumption, that the work instructions and procedures share the authoring template's headings, so one heading-based
chunker serves them. Datasheets and document lists may be different shapes, and each would cost another chunker. The page's advice is
to count: each implementation carries engineering and maintenance costs, so write the second only when the first
fails on a measured question.

<!-- unknown since=2026-11 -->
Nothing here was run. The capstone has no index, the scenario holds no document text beyond summaries, and no
chunker was tested against a retrieval set. The 0.8 mm and 1.5 mm limits are the scenario's invented figures. Build a
small labelled question set before you choose, and keep it for the day you change strategy.
<!-- /unknown -->

## Design guidance

- **Start from the document's structure**, then pick the cheapest approach that respects it.
- **Keep a table with its heading and introducing sentence**, and a heading with its text.
- **Store document number, revision and type with every chunk**, and never in the chunk text alone.
- **Count implementations before writing a second.** Each one is a maintenance cost.
- **Treat the strategy as semipermanent.** Evaluate a candidate on a labelled set before you replace one.
- **Check your compliance rules** before sending documents to a managed extraction service.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Right document, wrong clause | A boundary cut the answer from its heading | Split at structure, not at a count |
| A limit is quoted with no condition | A table was split from its introduction | Chunk the table with its sentence |
| A rationale is presented as a requirement | The chunk lost its document type | Carry the type as a field |
| Answers ignore a table or figure | Nothing turned it into text | Describe it first, and chunk the description |
| Quality drops after a strategy change | The new chunks changed every downstream step | Evaluate on a labelled set first |
| Cost grows with each document type | A chunker was written for every type | Share one where the structure matches |

## Key terms

**Chunk**: the unit of a document that is indexed and retrieved.

**Overlap**: text repeated across neighbouring fixed-size chunks so an idea is not cut at a boundary.

**Inferred structure**: structure that exists in a document's text, such as numbered clauses, without markup.

**Language model augmentation**: using a model to turn images or tables into text that can be chunked.

**Layout analysis**: extracting a document's headings, tables and figures with OCR and models.
