## TL;DR

A Copilot Studio agent can draw on public websites, SharePoint and OneDrive, uploaded files, Dataverse
tables, and enterprise systems through connectors. Three things separate them, and they decide the choice:
**whose permissions** apply, **how fresh** the content is, and **what limits** you hit. Choose on those,
not on which is quickest to set up. On the GitHub Copilot harness the list is a little different from the
standard harness's, so check which harness a page describes before you rely on it.

## Why it matters

Adding a knowledge source takes minutes. Its consequences last as long as the agent does, and the two that
hurt are permissions and freshness. Upload a controlled document as a file, and everyone who can use the
agent can now get answers from it, at whatever revision it was on the day you uploaded it. Point the agent
at the SharePoint library instead, and each user gets only what they can already open, at the current
revision.

Nothing in the product warns you about this. It is a design decision that looks like a configuration step.

## How it works

<!-- volatile verified=2026-10 -->
| Source | Whose permissions | Freshness | Limits worth knowing |
|---|---|---|---|
| **Uploaded files** | None. Microsoft lists their authentication as *None*, so anyone who can use the agent gets answers from them | Frozen at upload | Stored in Dataverse; files up to 512 MB |
| **SharePoint / OneDrive** | **The person asking**, through their Microsoft Entra ID sign-in | Live, once Microsoft Search has indexed the change | Uses the top three results per question. Files over 7 MB are skipped without a Microsoft 365 Copilot licence in the tenant (200 MB with one) |
| **Public websites** | None; public content only | As fresh as Bing's index | Generative orchestration: up to 25 sites |
| **Dataverse tables** | The person asking | Live | Structured records already in Power Platform |
| **Connectors** | Depends on the kind ({{topic:connectorknowledge}}) | Indexed or live, depending on the kind | Some are preview |

On the standard harness, generative orchestration searches up to 25 knowledge sources before it starts
filtering them with a model, and uploaded files do not count toward that 25.
<!-- /volatile -->

**Permissions belong to the source, not the agent.** No instruction can make an uploaded file respect
access rules, and no wording gets around SharePoint's. When SharePoint denies access it does so silently:
the user just gets no answer, exactly as if the document did not exist ({{topic:visibility}}). Choosing
the source *is* choosing the access model.

**Live is not the same as correct.** SharePoint fixes the *copy* problem, not the *content* problem. A
document nobody revised is as stale in SharePoint as it would be as an upload.

**Every source costs something on every question.** Each one's description is part of what the agent
weighs when it decides where to look ({{topic:orchestration}}), and each extra source is one more place
an irrelevant passage can come from.

### On the GitHub Copilot harness

The Technik Production Assistant is built on this harness. Microsoft says it supports "the same categories
of knowledge sources as the standard harness" with two differences: there is **no general-knowledge
switch**, and a drag-and-drop file upload is always available. Sources are added from **Build →
Knowledge**.

<!-- volatile verified=2026-10 -->
The **Add knowledge** dialog lists **Featured** sources (Public websites, SharePoint, OneDrive for
Business, Salesforce, ServiceNow, Azure SQL) and **Advanced** ones (Azure DevOps Wiki, Azure DevOps Work
Items, Custom Connector, Enterprise websites). Dataverse and Copilot connectors may also appear, depending
on environment and licensing. Sources show as chips, with no table of types and statuses. Web search is a
**Search all websites** option under Public websites.
<!-- /volatile -->

Two GitHub Copilot harness facts change how you prepare content. Microsoft says a **SharePoint document's
title is one of the signals** the agent uses to choose what to reference, so `Document1` is hard to find.
And changes to the underlying content, such as a revised document in SharePoint, "are reflected
automatically" with no change to the agent.

A knowledge source is something the *maker* provides, so every user gets the same grounding. A file a user
drops into one conversation is an *attachment*, which is a different feature.

## In practice at Technik

The Production Assistant has two knowledge sources, and both are SharePoint:

| Content | Source | Why |
|---|---|---|
| Released controlled documents: `SOP70000101`, `SOP70000114`, `SWI70000318`, `SWI70000402`, `DGL70000009` | The **Controlled Documents** library, where released Teamcenter documents are published as PDFs | Per-user permissions, because not everyone may read every controlled document; and a new revision replaces the old one in place |
| Internal standards: *Weld Overlay Acceptance Criteria*, *Plant Safety and PPE* | The Technik **Standards** site | Changes more often than a controlled document; maintained by its owners in SharePoint |

What it does **not** have matters as much. Work order, notification and revision data stay in Snowflake
and reach the assistant through tools ({{topic:tools}}), because the questions about them can be named in
advance. Nothing is uploaded as a file: an upload would be a second copy of a controlled document, with
nobody's permissions and a revision that never changes.

Before the library was attached, someone fixed the titles. PDFs exported from Teamcenter had titles like
`export_0412.pdf`. Renamed to `SWI70000318 Cladding Preparation and Inspection`, they carry both the number
an engineer types and the words they use.

> [!TIP]
> Before you add a knowledge source, write one sentence: *who may see this content, and how stale may the
> answer be?* If that sentence is hard to write, you do not yet know the content well enough to index it.

## Design guidance

- **Choose on permissions first**, freshness second, effort last.
- **Never upload a document that has access rules.** That is what SharePoint is for.
- **One source per body of content.** The same document as an upload *and* in SharePoint gives retrieval
  two chances to return the older one.
- **Fix titles before you attach a library.** On the GitHub Copilot harness they are a retrieval signal.
- **Write a description that says what the source holds and what it does not.** Orchestration reads it.
- **Check the harness of every page you follow.** Several of Microsoft's knowledge pages describe the
  standard harness only.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A colleague gets no answer from SharePoint content | They cannot open the file. Permissions are working | Confirm their access, not the agent |
| Everyone can get answers from a restricted document | It was uploaded as a file | Move it to SharePoint and delete the upload |
| A large PDF is never cited | Over 7 MB, with no Microsoft 365 Copilot licence in the tenant | Split it, or check the licensing situation |
| A revised document still answers with old text | An uploaded copy is indexed beside the live one | One source per body of content |
| A document that exists is never found | A generic title such as `Document1` | Give it a descriptive title in SharePoint |
| There is no *use general knowledge* switch | The agent is on the GitHub Copilot harness | Grounding is an instruction you test ({{topic:genai}}) |

## Key terms

**Knowledge source** — content the maker makes available to an agent at design time.

**End-user authentication** — the source is queried as the person asking, so answers respect their access.

**Attachment** — a file a user brings into one conversation. Not a knowledge source.

**Indexing** — preparing content so it can be retrieved. It takes time.

**Source description** — the text orchestration reads to decide whether to search a source.
