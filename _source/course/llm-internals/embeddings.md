## TL;DR

An embedding is a vector, a long array of numbers, that captures the meaning of a piece of text, so that
pieces with similar meaning sit near each other. Search then becomes arithmetic: embed the query, find the
nearest vectors. That is the whole idea, and the curated sources are thin on everything around it. Neither says
how similarity is measured in the product, that the query and the index must use the same model, or what to do
when you change it. This lesson teaches the documented parts, shows the limits and costs, and marks the rest
unknown, with a test for each. The index side belongs to {{topic:vector}}.

## Why it matters

You call an embedding model, store what it returns, and everything built on top inherits its choices: what
counts as near, which content it handles, how long an input may be. The choice is cheap to make and may be
expensive to reverse. It is also easy to over-credit. A vector search always returns something, and it returns
the nearest things whether or not any of them answers the question.

## How it works

### What an embedding is

The .NET page defines embeddings as the way LLMs capture semantic meaning: numeric representations of
non-numeric data that a model uses to find relationships between concepts. The training module explains the
mechanism one level down. Each token has a vector, a real transformer's vectors have thousands of elements, and
the module measures how alike two of them are with **cosine similarity** ({{topic:transformers}}).

<!-- unknown since=2026-11 -->
That module is about the vectors inside a language model. The .NET page names no similarity measure and gives
no dimension counts, and the Azure AI Search page covers neither metrics, dimensions nor index algorithms. So
neither says which measure your index uses or how many dimensions your model produces. Read both from the
model's and the index's own documentation.
<!-- /unknown -->

### What they are used for

The .NET page lists use with your own data (it ties this to retrieval-augmented generation), fitting more text
into a prompt without adding tokens, classification and summarization, audio, images and code. The Azure AI
Search page lists six scenarios: similarity, hybrid, multimodal, multilingual and filtered search, and a pure
vector index used as long-term memory or to ground answers. Its examples are "dog" and "canine" as
conceptually similar, and text matching images of a dog.

<!-- unknown since=2026-11 -->
The roadmap's other uses, clustering, deduplication and semantic caching, are in neither page, and search is
not among the .NET page's named use cases either. They are plausible, and unchecked here.
<!-- /unknown -->

### Choosing the model

<!-- volatile verified=2026-11 -->
The .NET page names `text-embedding-3-small` and `text-embedding-3-large` as the recommended embedding models,
replacing `text-embedding-ada-002`. The Azure AI Search page says its demos and samples target
`text-embedding-ada-002`, and recommends an Azure OpenAI model for text. The pages point at different models,
so check the list for your region.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
Neither page says that vectors from different embedding models are incomparable, that the query and the
indexed content must use the same model, or that changing the model means re-embedding everything. The
roadmap's "pick your model once per index" is that claim, unsourced. Treat it as true while you test it:
embed the same texts with two models and check whether a query from one finds the other's vectors.
<!-- /unknown -->

### Where vectors are made, and what it costs

<!-- volatile verified=2026-11 -->
Azure AI Search can make them for you. **Integrated vectorization** runs in an indexer pipeline, which needs a
data source and a skillset that drives chunking and embedding, and calls your Azure OpenAI endpoint. The
alternative is to push vectors you made yourself. At query time a vectorizer can encode the input, or your
client can. Vector search is available in all regions and tiers at no extra charge, but generating embeddings
or enrichment may incur charges from the model provider.

The Azure OpenAI quota page sets limits on the embeddings endpoint: 2,048 inputs in an array and 300,000 tokens
per request, summed across all inputs. At Tier 1 on Global Standard it lists `text-embedding-3-small` at
1,000,000 TPM.
<!-- /volatile -->

The .NET page says to break a large text into pieces small enough to fit one input, with no sizes or token
limit given ({{topic:chunking}}).

### Hybrid, and what a query returns

Azure AI Search defines **hybrid search** as vector and keyword search in the same request, run in parallel
and merged into one ranked response. It claims this often beats either alone, with no benchmark, and it needs
both vector and nonvector content in the same index ({{topic:hybrid}}). A vector query returns the requested
*k* nearest neighbours. By definition, *k* results come back, near or not.

## In practice at Technik

The capstone has no embeddings. Its three tools look up an identifier through a view, and a question that
names `DU700001042` needs the row, not the nearest thing to it. Embeddings earn their place on questions that
have no identifier. *Has this porosity been seen before?* is one. The open QN `300001234` records porosity in
the bore overlay, and `300001211` and `300001219` are its near-duplicates, the same defect raised twice. A
keyword search for "porosity" misses a QN that says "gas pits"; a vector search should place it near. Similar
QNs inside Snowflake are the job of {{module:snowflake-cortex}}.

Do the cost arithmetic, with its assumptions. Say the QN history holds 1,000 notifications of about 300
tokens each, invented for the example. That is 300,000 tokens, right at the per-request limit, so send it in
several requests, and well under a minute of the 1,000,000 TPM Tier 1 pool. The one-off cost is small. The
recurring one is the query embedding on every question, and a full re-embed if a model change needs one.

Two consequences hold whichever model you pick. The injected QNs `300001267` and `300001270` embed like any
other text, so indexing them makes them retrievable, and a retrieved description enters the prompt as
data that may carry an instruction ({{topic:ctxsecurity}}). And because a vector query always returns *k*
results, the capstone's rule "if a lookup finds nothing, say so" has no counterpart: you must decide what
distance counts as no match, and test it ({{topic:evalstrategy}}).

<!-- unknown since=2026-11 -->
Nobody has checked how an embedding ranks near-identical identifiers. Run it yourself: query with
`DU700001042` and see whether a different drawing's number lands among the nearest results.
<!-- /unknown -->

## Design guidance

- **Record the embedding model and version with the index.** Treat them as one thing until you have tested
  otherwise.
- **Send identifiers to an exact lookup**, and reserve vectors for questions with no key.
- **Decide what "no match" means.** Set a threshold or add a check, because *k* results always return.
- **Batch below both limits**, 2,048 inputs and 300,000 tokens per request.
- **Use hybrid search** when queries mix words and codes ({{topic:hybrid}}).
- **Evaluate retrieval separately from the answer** ({{topic:evalstrategy}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Results look unrelated after a model change | Query and index were embedded by different models, which the pages do not forbid or confirm | Re-embed with one model and test |
| A confident answer built on an irrelevant neighbour | A vector query always returns *k* results | Add a distance threshold and a no-match path |
| A batch embedding call fails | It exceeded 2,048 inputs or 300,000 tokens | Split the batch |
| Part numbers retrieve the wrong document | Vectors rank by meaning, not by exact string | Use a key lookup or hybrid search |
| The bill grows after launch | Every query is embedded, and generation can be charged | Meter query embeddings separately |
| A retrieved description gives the agent an order | Indexed text is retrievable whatever it says | Treat it as data ({{topic:ctxsecurity}}) |
| A tutorial's model name is retired | The sources disagree on the current model | Check your region's model list |

## Key terms

**Embedding**: a vector that represents the meaning of an input, comparable with others from the same model.

**Vector**: a long array of numbers.

**Cosine similarity**: a measure of how alike two vectors are, used in the training module's examples.

**Nearest neighbours (kNN)**: the *k* stored vectors closest to the query vector.

**Integrated vectorization**: Azure AI Search calling an embedding model for you, inside an indexer.

**Hybrid search**: vector and keyword search in one request, with merged results.
