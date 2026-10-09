## TL;DR

**Microsoft Copilot Chat** is the assistant that isn't inside any one document, and everyone with a
work account has it. It answers from your **work content**, the **web** and whatever you give it. Use it
for questions that span more than one file, and check which of those an answer came from.

## Why it matters

Copilot in Word knows the document you have open. Chat is where you go when you don't know which
document holds the answer, or when it's spread across several.

It's also where the source matters most. The same question can come back grounded in Technik's own
procedures, or as a fluent summary of what the internet says. Only one is about your company, and the
citations tell you which you got.

## How it works

### Where you find it

<!-- verified tenant=2026-10 -->
Microsoft lists these ways in: the web at `copilot.cloud.microsoft`, the Microsoft Copilot app on
desktop and mobile, the Copilot icon in the Edge browser, and Copilot Chat in Teams and Outlook. Sign in
with your **work** account, not a personal one ({{topic:sensitive}}).
<!-- /verified -->

### What it answers from

<!-- verified tenant=2026-10 -->
Signed in with your work account, Chat answers from:

- a search of your documents, mail, chats and meetings, within your permissions ({{topic:tenantgrounding}});
- the web;
- files you paste, upload or select, and the mail or chat you have open in Outlook or Teams.

Searching your work content is what makes it a work assistant. If it's switched off, Chat answers from
the web and your files only.
<!-- /verified -->

All of it comes with the same enterprise data protection, as long as you're signed in with your work
account.

### Is yours searching your work?

A quick test, in the browser or the Copilot app: ask *"Which documents on our SharePoint sites mention
PRJ-2031?"*. It should list and cite files. If it says it can't, or answers in general terms, check
that work grounding is on and that you're signed in with your work account. (Not in Outlook: Copilot
there sees your own mailbox either way.)

### Choosing a model

<!-- verified tenant=2026-10 -->
Chat offers three modes: **Auto**, which picks for you, **Quick Response** and **Think deeper**.
Nothing in this course depends on which one answered: the habits are the same.
<!-- /verified -->

### What to ask it

Questions that aren't about one open file: *which document covers…?*, *what's happened on… this
week?*, *what did I miss in…?*, or a draft from several sources. Everything in {{module:prompting}}
applies unchanged.

## In practice at Technik

### Which document covers weld prep inspection?

You ask:

> *Which document covers weld preparation and inspection for cladding on XT valve bodies? Give me the
> document number and section, and cite it.*

The answer names work instruction `SWI70000318`, *Cladding Preparation and Inspection*: section 4 for
preparation, section 5 for inspection. It cites the PDF in the Controlled Documents library, and also
mentions the *Weld Overlay Acceptance Criteria* page on the Standards site.

Now **check the citations**, the step that makes the answer usable. Open `SWI70000318`: is it the
released revision, and do sections 4 and 5 say what the answer claims? Open the Standards page: it says
the work instruction governs where the two differ, so it's a summary. Use the work instruction.

If the answer names no Technik document at all, it came from the web, however much it sounds like a
procedure. Attach `SWI70000318` and ask about the file.

### Pulling a job together

> *What's happened on PRJ-2031 this week? Use my mail and Teams chats, and list open questions with who
> raised them.*

Read the answer as a map of where to look, and open the messages it
cites before acting on any of them.

## Using it well

- **Check where an answer came from** before you trust it about your own work.
- **Ask for the document number and section**, and open the citation.
- **Attach the file when you know which one it is.** Searching is for when you don't.
- **Start a new chat for a new topic.** Old turns stay in the context ({{topic:context}}).
- **Treat a web-only answer to a work question as a guess**, however well written.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A polished answer that never mentions Technik's documents | It answered from the web | Attach the document, or ask again naming it |
| "I can't access your files" | Work grounding off, or a personal account | See *Is yours searching your work?* |
| The answer cites a summary page, not the procedure | Both were found; the summary ranked well | Ask again naming the governing document |

## Key terms

**Microsoft Copilot Chat**: Microsoft's work chat assistant, for everyone with a work account.

**Auto**: Chat choosing the model for you.

**Web grounding**: answering from a web search, not your organisation's content.
