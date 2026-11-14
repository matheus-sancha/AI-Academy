## TL;DR

Agentic retrieval replaces one query with a small pipeline. A knowledge base takes a question and the conversation so
far, can ask a model to break it into subqueries, runs them in parallel over one or more knowledge sources, reranks each
result and merges them. Foundry IQ is the managed form: a knowledge base several agents can share, with permissions
enforced at query time. Two facts shape every decision. The planning step that makes it *agentic* is in preview, and
the generally available path skips it. And it adds latency and a token-based bill, so it is for questions a single
query cannot answer.

## Why it matters

A single hybrid query ({{topic:hybrid}}) serves a question with one ask. Real questions carry several, or lean on the
last turn, or contain a typo. {{topic:jit}} treated retrieval as a budget decision. This lesson is the mechanism behind
it: what the pipeline does, which parts are production-ready, and what it costs per question rather than per query.

## How it works

### The pipeline

<!-- volatile verified=2026-11 -->
Your application calls a knowledge base with a `retrieve` action, passing the query and the conversation history. At
`low` and `medium` retrieval reasoning effort the knowledge base sends both to a model, which writes focused subqueries.
At `minimal` that step is skipped and the query goes straight to the knowledge sources. The default is `low`, set on the
knowledge base. The subqueries run at the same time, and each can be keyword, vector or hybrid. Each is semantically
reranked ({{topic:hybrid}}), and the references are kept for citation. The merged content always comes back. The
source references and an activity log of what ran are optional.
<!-- /volatile -->

A **knowledge base** orchestrates the pipeline. A **knowledge source** defines the content and is either indexed,
backed by a search index on your service, or remote, fetched at query time from an external platform. A model from Azure
OpenAI can plan queries, choose sources, summarise web results and write a cited answer. The page says the pipeline
suits questions with several asks, questions that depend on earlier turns, and queries that gain from rewriting or have
spelling mistakes. It also says agentic retrieval adds latency compared with a single query.

### Generally available and preview

<!-- volatile verified=2026-11 -->
Two REST versions split the feature. The `2026-04-01` version is for production workloads that use generally available
knowledge source types with minimal, extractive retrieval. The `2026-08-01-preview` version adds LLM query planning,
answer synthesis, non-minimal reasoning effort and multi-turn messages. The page states that preview features have no
service-level agreement, are not recommended for production and can change. Both portals give preview-only access to
everything, and objects created there may need migrating to the generally available version.
<!-- /volatile -->

So the part that plans queries, which is the *agent* in agentic, is the preview part. The production-supported path
runs the parallel searches and reranking with no planning.

### What it costs

<!-- volatile verified=2026-11 -->
Two services bill. Azure AI Search charges for retrieval tokens consumed by subquery execution and semantic ranking,
and Azure OpenAI charges for the tokens in planning and answer synthesis. Against the classic pipeline, which bills per
query, agentic retrieval bills per token, at a variable cost that depends on reasoning effort. The page's tips for
control are to read the activity log, reduce the number of knowledge sources to cut fan-out, lower the effort, and
organise content so fewer sources and documents are needed.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
The page's worked example uses a "hypothetical price of 0.022 per token" and gets $3.30 for 150 million tokens, which
works only if the price is per million. Its other figures, 2,000 retrievals, three subqueries, 50 chunks of 500 tokens
and a $4.32 total, check out arithmetically. Take the shape of the estimate, and read current prices from the pricing
pages.
<!-- /unknown -->

### Foundry IQ

<!-- volatile verified=2026-11 -->
Several agents can share one Foundry IQ knowledge base, and it can be called from Foundry Agent Service, Microsoft Agent
Framework or any application, through the knowledge base REST API or an SDK. Sources include Azure Blob Storage,
SharePoint, OneLake and public web data. For indexed sources it automates chunking, embedding and metadata extraction,
with scheduled indexer runs for refresh. It can synchronise access control lists, honour Microsoft Purview sensitivity
labels and run a query under the caller's Microsoft Entra identity, so an agent returns only what that person may read.
A Copilot Studio agent can connect only on the GitHub Copilot harness, with one Foundry IQ connection per agent. The
end user's identity is passed with every request.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
The Foundry IQ page says a knowledge base returns "grounded answers with citations" and, a few lines on, extractive
data with citations. Answer synthesis is a preview feature on the other page, so what a setup returns depends on the
API version. The page also says end-user tokens are used for sources that support them, and does not list which source
kinds enforce which permission mechanism.
<!-- /unknown -->

## In practice at Technik

Technik's capstone does not use agentic retrieval. Its three tools are narrow lookups, and a planning step would add
latency and tokens to a question that needs one view. The case for it appears in the engineering agent that
{{module:advanced-tools-and-multi-agent}} splits out. A question like *which document covers weld prep inspection, what
does it say about sealing surfaces, and has revision C changed it?* has three asks. A knowledge base can plan three
subqueries, search them in parallel and merge them with references, where one hybrid query would blur them together.

The identity half matters more. Revision C of `SWI70000318` is drafted in the manufacturing engineering team's site,
which production cannot open. A knowledge base that answers as the caller returns the released revision to a production
user and the draft to a member of the team. One that answers as a shared service identity returns the same to both,
the failure {{topic:vector}} warned about from the index side. Run it as the caller.

The cost scales with how the content was cut. Suppose, with invented figures, that the engineering agent takes 1,000
questions a day, each planned into three subqueries that rerank 50 chunks of 500 tokens. That is 75 million reranked
tokens a day, and planning adds roughly 2,000 input tokens a question on the page's assumptions. Chunk size is
a direct multiplier on retrieval cost ({{topic:chunking}}), as well as on quality.

<!-- unknown since=2026-11 -->
Nobody has run this. Whether a knowledge base can serve the capstone's hosted agent, as a tool beside the three
Teamcenter tools, is covered by neither the capstone nor either page.
<!-- /unknown -->

## Design guidance

- **Use it for multi-part or context-dependent questions**, and keep a single hybrid query for the rest.
- **Choose the API version on purpose.** Planning and synthesis are preview.
- **Start at `minimal` or `low` effort**, and raise it only where an evaluation shows a gain.
- **Read the activity log** as a trace of the subqueries ({{topic:tracing}}).
- **Prefer fewer knowledge sources.** Each adds fan-out and tokens.
- **Run permission-bound content as the caller**, and test with a user who lacks access.
- **Require references**, and pass them on as citations ({{topic:grounded}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The pipeline does not plan queries | The generally available path is `minimal` effort | Use the preview version, knowing its terms |
| Simple questions got slower | Planning runs on every question | Route simple questions to a single query |
| The bill tracks question difficulty | Billing is per token, not per query | Estimate tokens, and cap effort |
| A production user sees draft text | The knowledge base ran as a shared identity | Pass the caller's identity, and test it |
| A portal-built object fails in code | The portal used a preview schema | Migrate to the generally available version |
| A Copilot Studio agent cannot connect | Foundry IQ needs the GitHub Copilot harness | Check the harness and the one-connection limit |

## Key terms

**Agentic retrieval**: a multi-query pipeline that plans subqueries, runs them in parallel and merges the results.

**Knowledge base**: the resource that orchestrates retrieval across knowledge sources.

**Knowledge source**: a definition of searchable content, indexed or remote.

**Retrieval reasoning effort**: the setting, `minimal`, `low` or `medium`, that controls LLM planning.

**Foundry IQ**: Microsoft's managed knowledge layer, built on agentic retrieval and shared across agents.
