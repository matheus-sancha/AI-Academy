## TL;DR

**Microsoft Copilot Chat** is the assistant that isn't inside any one document, and everyone with a
work account has it. What it *answers from* depends on your licence: on its own, the **web** and
whatever you give it; with a **Microsoft 365 Copilot licence**, your **work content** too. Use it for
questions that span more than one file, and know which of the two you have.

## Why it matters

Copilot in Word knows the document you have open. Chat is where you go when you don't know which
document holds the answer, or when it's spread across several.

It's also where the licence difference bites hardest. The same question can come back grounded in
Technik's own procedures, or as a fluent summary of what the internet says. Only one is about your
company.

## How it works

### Where you find it

<!-- volatile verified=2026-10 -->
Microsoft lists these ways in: the web at `copilot.cloud.microsoft`, the Microsoft Copilot app on
desktop and mobile, the Copilot icon in the Edge browser, and Copilot Chat in Teams and Outlook. Sign in
with your **work** account, not a personal one ({{topic:sensitive}}).
<!-- /volatile -->

### What it answers from

| | Copilot Chat on its own | With a Microsoft 365 Copilot licence |
|---|---|---|
| The web | Yes | Yes |
| Files you paste, upload or select | Yes | Yes |
| The mail or chat you have open in Outlook or Teams | Yes | Yes |
| A search of your documents, mail, chats and meetings | **No** | Yes, within your permissions ({{topic:tenantgrounding}}) |

Signed in with your work account, both get the same enterprise data protection. The difference is
reach, not safety.

### Which one do you have?

<!-- volatile verified=2026-10 -->
Microsoft shows an in-product label naming your experience, in the Copilot app and in Word, Excel,
PowerPoint and OneNote. **Copilot Chat (Basic)** means Chat on its own. **Microsoft 365 Copilot
(Basic)** adds Copilot in the Office apps, but Chat still answers from the web and your files only.
**Microsoft 365 Copilot (Premium)** is the licence this course means: Chat also searches your work
content. Microsoft's support site also has a page called *Check your Copilot license*.
<!-- /volatile -->

A quick test, in the browser or the Copilot app: ask *"Which documents on our SharePoint sites mention
PRJ-2031?"*. A licensed Chat lists and cites files. Chat on its own says it can't, or answers in general
terms. (Not in Outlook: Copilot there sees your own mailbox either way.)

### What to ask it

Questions that aren't about one open file: *which document covers…?*, *what's happened on… this
week?*, *what did I miss in…?*, or a draft from several sources. Everything in {{module:prompting}}
applies unchanged.

## In practice at Technik

### Which document covers weld prep inspection?

With a licence, you ask:

> *Which document covers weld preparation and inspection for cladding on XT valve bodies? Give me the
> document number and section, and cite it.*

The answer names work instruction `SWI70000318`, *Cladding Preparation and Inspection*: section 4 for
preparation, section 5 for inspection. It cites the PDF in the Controlled Documents library, and also
mentions the *Weld Overlay Acceptance Criteria* page on the Standards site.

Now **check the citations**, the step that makes the answer usable. Open `SWI70000318`: is it the
released revision, and do sections 4 and 5 say what the answer claims? Open the Standards page: it says
the work instruction governs where the two differ, so it's a summary. Use the work instruction.

> [!NOTE]
> With Copilot Chat on its own, this question can't search Technik's libraries. You'll get a general
> web answer that may sound exactly like a procedure. Attach `SWI70000318` and ask about the file.

### Pulling a job together

> *What's happened on PRJ-2031 this week? Use my mail and Teams chats, and list open questions with who
> raised them.*

A licence makes this possible. Read the answer as a map of where to look, and open the messages it
cites before acting on any of them.

## Using it well

- **Know which Chat you have** before you trust an answer about your own work.
- **Ask for the document number and section**, and open the citation.
- **Attach the file when you know which one it is.** Searching is for when you don't.
- **Start a new chat for a new topic.** Old turns stay in the context ({{topic:context}}).
- **Treat a web-only answer to a work question as a guess**, however well written.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A polished answer that never mentions Technik's documents | Chat on its own answers from the web | Attach the document, or check your licence |
| "I can't access your files" | No licence, or work grounding off | See *Which one do you have?* |
| The answer cites a summary page, not the procedure | Both were found; the summary ranked well | Ask again naming the governing document |

## Key terms

**Microsoft Copilot Chat**: Microsoft's work chat assistant, for everyone with a work account.

**Microsoft 365 Copilot licence**: the paid licence that lets Copilot search your work content. Shown
in the product as *Microsoft 365 Copilot (Premium)*.

**Web grounding**: answering from a web search, not your organisation's content.
