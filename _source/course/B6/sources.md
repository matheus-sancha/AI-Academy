## TL;DR

Copilot Studio agents can draw knowledge from public websites, SharePoint and OneDrive, uploaded
files, Dataverse tables, and enterprise systems through connectors. They differ in three ways that
decide the choice for you: **how fresh** the content is, **whose permissions** apply, and **what
limits** you hit. Pick on those three, not on which is easiest to set up.

## Why it matters

The setup cost of every knowledge source is roughly an afternoon. The consequences last for the life
of the agent, and the two that bite are permissions and freshness. Upload a controlled document as a
file and you have just given everyone who can use the agent a copy of it, permanently, at the
revision it was on the day you uploaded it. Point at SharePoint instead and both problems go away.

Nothing in the product warns you about this. It is a design decision that looks like a
configuration step.

## How it works

<!-- volatile verified=2026-09 -->
The set of knowledge sources, their size and count limits, and which are available in which harness
all change between releases. Learn the trade-offs below — they are stable — and check the linked
documentation for the current list and limits before you design around a number.
<!-- /volatile -->

| Source | Freshness | Whose permissions | Good for |
|---|---|---|---|
| **Uploaded files** | Frozen at upload | None — everyone using the agent sees everything | Small, stable reference content you control |
| **SharePoint / OneDrive** | Live, subject to indexing | **The end user's** | Controlled documents, anything with real access rules |
| **Public website** | Live, subject to crawl | Public | Product and vendor documentation |
| **Dataverse tables** | Live | Dataverse security, row level | Structured business data already in Power Platform |
| **Connectors** (Snowflake, ServiceNow, SAP…) | Live, queried per request | Whatever the connection uses | Systems of record that are not in Microsoft 365 |

Three properties matter more than the table suggests.

**Permissions are a property of the source, not of the agent.** You cannot make an uploaded file
respect permissions by writing an instruction, and you cannot bypass SharePoint's permissions by
asking nicely. Choosing the source *is* choosing the access model.

**Freshness is not the same as correctness.** SharePoint is live, but a document nobody revised is
just as stale as a file you uploaded. Live sources fix the *copy* problem, not the *content*
problem.

**Every source costs context.** Passages from each are carried on requests where they are retrieved.
A third source does not make the agent a third more capable; it makes retrieval a third more likely
to return something irrelevant.

### Websites

A public website is the least effort and the least control. It is right for vendor documentation you
do not own and wrong for anything internal — an internal site that requires sign-in cannot be
crawled as a public website, and the answer is SharePoint knowledge instead.

### Uploaded files

Convenient, and the default people reach for. Use them when the content is small, stable, and may be
seen by everyone who can use the agent. Their honest place at Technik is training material and
templates, not controlled documents — and in this module's lab you will upload controlled documents
anyway, deliberately, so that the difference between doing that and pointing at SharePoint is
something you have seen rather than read.

### Dataverse and connectors

Both reach structured data. Dataverse is the right answer when the data already lives in Power
Platform. Connectors are the right answer when it lives elsewhere — and they bring the whole
identity question with them, which is why [Copilot Connectors vs. Power Platform
Connectors](connectorknowledge.html) and [Snowflake as a Knowledge Source](snowflakeknowledge.html)
are separate lessons.

## In practice at Technik

The Technik Production Assistant ends up with three kinds of knowledge, each chosen for a different
reason:

| Content | Source | Why |
|---|---|---|
| Controlled documents: `SOP70000101`, `SOP70000114`, `SWI70000318`, `SWI70000402`, `DGL70000009` | Uploaded files, in this module | Small, fixed set, and it makes the lab independent of your tenant's SharePoint. In a real deployment these belong in SharePoint |
| Intranet standards: `TS-014` weld overlay acceptance, plant safety and PPE | SharePoint | They change more often, and per-user permissions matter for some intranet content |
| Work orders and operations | Snowflake connector | Millions of rows, live, and nobody is going to export them |

Note the honest compromise in the first row. Uploading controlled documents is not what Technik
would do; it is what makes a lab work on any tenant. The lab says so, and the
[lab](lab.html) asks you to write down what would change in a real deployment. Being
able to name the compromise is worth more than avoiding it.

> [!TIP]
> Before adding a knowledge source, write one sentence: *who may see this content, and how stale may
> the answer be?* If the sentence is hard to write, you do not yet know enough about the content to
> index it.

## Design guidance

- **Choose on permissions first**, freshness second, effort last.
- **Never upload a document that has access rules.** SharePoint exists for that.
- **Curate rather than accumulate.** Five relevant documents beat fifty.
- **One source per body of content.** The same document in SharePoint *and* as an upload gives
  retrieval two chances to return the older one.
- **Check the format is supported** before building a lab, a demo or a promise around it.
- **Write down what you would do differently in production** whenever you take a shortcut for
  convenience. That note is the one people thank you for later.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A colleague gets no answer from SharePoint content | They cannot open the file; permissions are working | Confirm the permission, not the agent |
| Everyone can see a restricted document | It was uploaded as a file, which has no permissions | Move it to SharePoint and delete the upload |
| Newly added content is not found | Indexing has not finished | Wait, then re-test. Indexing is not instant |
| An internal site returns nothing as a website source | It requires sign-in, so it cannot be crawled | Use SharePoint knowledge instead |
| A revised document still answers with old text | An uploaded copy is still indexed alongside the live one | One source per body of content |
| Answers degraded as sources were added | Retrieval competition | Remove sources; narrow scope; route (A8) |

## Key terms

**Knowledge source** — a body of content an agent can retrieve from.

**Indexing** — preparing content so it can be retrieved. Not instantaneous.

**End-user permissions** — the source is queried as the person asking, so answers respect their
access.

**Crawl** — how a public website source is read and refreshed.

**Dataverse** — Power Platform's own data store, with row-level security.

**Curation** — deciding what *not* to index. The most undervalued step in this module.
