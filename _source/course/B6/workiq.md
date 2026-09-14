Two newer pieces of Microsoft's knowledge story are worth knowing by name before you meet them.

<!-- volatile verified=2026-09 -->
**Work IQ** gives agents organisational context from Microsoft 365 — mail, calendar, files, Teams
messages, and the relationships between people and the work they do. The idea is that an agent
should know what you know by virtue of working somewhere, rather than only what you explicitly
indexed.

**Foundry IQ** gives agents ready-made knowledge bases assembled in Microsoft Foundry, so retrieval
is configured once, centrally, and reused by many agents rather than rebuilt per agent.

Both are moving quickly, and details here may be out of date by the time you read this. Check the
linked documentation rather than these two paragraphs.
<!-- /volatile -->

## Why they are worth knowing now

Everything in this module treats knowledge as *something you point an agent at*: these documents,
that site, those tables. Both of these push in the same direction — that retrieval is infrastructure
shared across agents, rather than configuration owned by each one.

That distinction matters even before you use either. When you find yourself adding the same
SharePoint site and the same five documents to a third agent, you are hand-building what a shared
knowledge base exists to provide, and the questions to ask are the same ones this module has already
raised: who may see it, how fresh is it, which source governs.

## Where they would fit at Technik

**Work IQ** is a good fit for the questions the Production Assistant currently cannot answer because
they are not about data at all: *"who raised this notification and what did they say about it in
Teams?"*, *"has the project engineer already replied about this concession?"*. That context lives in
mail and chat, and per-user permissions are not optional for it.

**Foundry IQ** is a good fit for the moment Technik has more than one agent — which the Advanced
track reaches in A6, when the assistant splits into a production agent and an engineering agent. Both
need the controlled documents. Configuring that retrieval twice is how the two drift apart.

## What does not change

The reasoning in the rest of this module applies unchanged to both:

- permissions are a property of the source, not of the agent;
- freshness compounds across layers, and a shared knowledge base is another layer;
- an answer an engineer may act on still needs a citation;
- an agent that never abstains still has not been tested honestly.

Treat a new knowledge capability as a new source with the same three questions — **who may see it,
how stale may it be, which source governs** — rather than as something that makes those questions go
away.

## Key terms

**Work IQ** — organisational context from Microsoft 365 made available to agents.

**Foundry IQ** — reusable knowledge bases built in Microsoft Foundry and shared across agents.

**Preview feature** — available for evaluation, not covered by general availability commitments, and
subject to change. Everything on this page is one.
