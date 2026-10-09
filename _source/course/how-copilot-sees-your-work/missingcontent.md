## TL;DR

"It didn't find the obvious file" is the most common complaint about Copilot, and it's rarely the
model's fault. Before the model writes anything, Copilot searches, and a search only returns what it
can reach. Four causes cover nearly every miss: **permissions** (can you open it?), **location** (does
it live somewhere Copilot searches?), **format** (could it be indexed?) and **age** (has it been indexed
yet?). Work through them in that order.

## Why it matters

When a search misses a document, the answer doesn't say *"I couldn't find it"*. It answers fluently
from whatever it did find: thinner, older or more generic than it should be. Rewording rarely helps,
because the problem isn't the question.

## How it works

Copilot searches Microsoft's **semantic index** of your organisation's content
({{topic:tenantgrounding}}). Each cause is a way a file can be missing from that index, or missing for
you.

**1. Permissions.** Copilot only uses what you could open yourself ({{topic:visibility}}). Check by
clicking the link.

**2. Location.** The index covers files in SharePoint and OneDrive, and your own mailbox. Microsoft
lists places it does **not** cover, including shared mailboxes, mailboxes you open on someone else's
behalf, and archived mail or SharePoint content. A file kept only on your computer or a network drive
isn't in Microsoft 365, so it isn't in the index. An administrator can also exclude a sensitive
SharePoint site from search, and that excludes it from Copilot too.

**3. Format.** The index is built from **text**. Microsoft lists Word documents, PowerPoint decks, PDFs,
SharePoint pages and OneNote files among the supported types.
<!-- verified tenant=2026-10 -->
How the index treats a scanned PDF that is only a picture of a page, with no text in it, isn't stated in
the linked documentation. Treat scans as unlikely to be found by content.
<!-- /verified -->

**4. Age.** Indexing takes time, and the delay differs by place.
<!-- verified tenant=2026-10 -->
Microsoft says mail is indexed in near real time, and changes to an already-indexed document are picked
up immediately. A **new** document in a SharePoint site that two or more people can reach is indexed
**daily**, so a procedure uploaded this morning may not be found until tomorrow.
<!-- /verified -->

A fifth case isn't a miss: the file was found, but something else ranked higher. Naming the document
in your prompt usually fixes it.

## In practice at Technik

You ask Copilot Chat:

> *Which procedure covers the hydrostatic test during Assembly & Testing, and what does it say about
> hold time?*

The answer describes hydrostatic testing in general terms and cites nothing from Technik. You know work
instruction `SWI70000402` exists. Work through the shortlist:

| Cause | Check | What you find |
|---|---|---|
| Permissions | Can you open it? | Yes, from the Controlled Documents library |
| Location | Where does it live? | The library, which is indexed. (The copy you usually use, in the plant's **shared mailbox**, never would be.) |
| Format | Is it a real PDF? | Yes, text you can select |
| Age | When was it published? | **This morning**, as a new file |

So it's age. Wait until tomorrow, or give Copilot the file now:

> *Using the attached `SWI70000402`, what does it say about hold time for the hydrostatic test?*

Attaching the document skips the search. When you know which file answers the question, point Copilot
at it. Searching is for when you don't.

## Using it well

- **Notice a missing citation.** A generic, uncited answer about your own work usually means the search
  found nothing useful.
- **Name or attach the document** when you know it. That removes all four causes.
- **Check the shortlist in order.** Permissions takes ten seconds.
- **Report a site that should be searchable and isn't** to its owner, rather than working around it.

<!-- verified tenant=2026-10 -->
In Copilot Chat on the web, you can also point a question at a SharePoint **library or
folder**, by attaching it or pasting its link. Copilot then searches that place.
<!-- /verified -->

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Generic answer, no Technik citation | The search found nothing relevant | Name or attach the document |
| Nothing from the plant mailbox is ever found | Shared mailboxes aren't indexed | Save the file to a library, or attach it |
| A document published today isn't found | Not indexed yet | Attach it, or ask tomorrow |
| A scanned certificate is never found by its contents | Nothing readable to index | Open it and ask about it directly |
| A whole site never appears | Excluded from search, or no access | Ask the site owner which |

## Key terms

**Index**: the searchable map of your organisation's content that Copilot searches before it answers.

**Indexed**: added to that map. Content that isn't indexed can't be found by searching, even if you
can open it.
