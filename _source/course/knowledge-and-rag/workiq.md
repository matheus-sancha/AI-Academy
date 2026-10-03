## TL;DR

**Work IQ** gives agents organisational context from Microsoft 365: mail, calendar, files, people, chats
and sites. **Foundry IQ** gives agents shared, permission-aware knowledge bases built in Microsoft Foundry.
Both treat knowledge as infrastructure many agents share, rather than something each agent configures for
itself. Know what they are now; {{module:pro-code-agents}} and {{module:advanced-rag}} cover using them.

## What they are

<!-- volatile verified=2026-10 -->
**Work IQ** is what Microsoft calls a "workplace intelligence layer". Agents reach it through A2A, a
remote MCP server or a REST API. The Work IQ MCP server collapses hundreds of operations into ten generic
tools over Microsoft 365 data. Every request is **user scoped**: it runs as a specific user and sees only
what that user may see. Access is independent of Microsoft 365 Copilot licensing and is billed by usage.

**Foundry IQ** is a "managed knowledge layer". A *knowledge base* groups knowledge sources (Azure Blob
Storage, SharePoint, OneLake, the public web) and uses agentic retrieval ({{topic:rag}}) to plan queries,
run them in parallel and return extractive results with citations. Several agents can share one knowledge
base, and queries can run under the caller's Microsoft Entra identity. Azure AI Search does the indexing.
Some features are generally available and others are preview, depending on the API version.
<!-- /volatile -->

## Why they are worth knowing now

Everything else in this module treats knowledge as something *you point one agent at*: this library, that
site. Both IQ layers push the other way. When you find yourself attaching the same library with the same
description to a third agent, you are hand-building what a shared knowledge base is for.

The questions do not change. Who may see it? How stale may it be? Which source governs? A shared layer is
one more layer, and staleness compounds across layers ({{topic:connectorknowledge}}).

## Where they would fit at Technik

**Work IQ** fits the questions the Production Assistant cannot answer because they are not about documents
or data at all: *"Has anyone replied in Teams about the concession on `300001234`?"* That context lives in
mail and chat, so per-user permissions are essential, and Work IQ's user scoping provides them.

**Foundry IQ** fits the day Technik has more than one agent. Once the assistant is split into a production
agent and an engineering agent ({{module:advanced-tools-and-multi-agent}}), both need the controlled
documents. Configuring that retrieval twice is how two agents drift apart.

## Key terms

**Work IQ** — organisational context from Microsoft 365, offered to agents as user-scoped tools and APIs.

**Foundry IQ** — reusable knowledge bases in Microsoft Foundry, shared across agents.

**Knowledge base** — in Foundry IQ, a set of knowledge sources plus the settings that control retrieval.
