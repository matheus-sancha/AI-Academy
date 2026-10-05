## TL;DR

Before you paste a document into an assistant, ask three things. **Which assistant is this?** Copilot
signed in with your work account keeps your content under your organisation's protections; a consumer
AI site, including personal Copilot, doesn't. **What label does the file carry?** A sensitivity label
says how your organisation classifies it, and Copilot honours its protection. **Is it covered by an
agreement?** Customer and supplier documents can come with terms. Check first, not after.

## Why it matters

Pasting is the one step where *you* move content, not Copilot. {{topic:visibility}} is about Copilot
staying inside permissions; a paste goes wherever you put it. The usual risk isn't a dramatic leak. It's
a customer specification summarised in a personal chatbot on a phone: easy to do, hard to undo.

## How it works

### Which assistant you're in

- **Copilot signed in with your work account** runs under **enterprise data protection**: Microsoft
  says prompts and responses get the same contractual protection as your organisation's mail and
  files, and aren't used to train the underlying models.
- **A consumer AI site** is a different product with different terms. Microsoft's own compliance tools
  group consumer Microsoft Copilot with ChatGPT and Google Gemini, as AI apps outside your organisation.

<!-- volatile verified=2026-10 -->
The Copilot app, Copilot in Edge, and Copilot in Outlook and Teams can all be signed in with a personal
Microsoft account as well as a work one. Before you paste anything from work, check which account it
shows.
<!-- /volatile -->

What you type into work Copilot is kept, too: prompts and responses are stored in your activity history,
under your organisation's retention rules, and its compliance team can search them, like mail.

### What a sensitivity label means

A **sensitivity label** is a stamp your organisation defines, such as *General* or *Confidential*,
that stays with a file wherever it goes. You see it in the app's title bar or **Sensitivity** button,
sometimes as a header or watermark. Some labels **encrypt** the file, limiting who can open it and
whether they may copy from it.

Copilot works with labels in three ways:

- **It respects encryption.** If a label encrypts a file, Copilot only uses content from it if you're
  allowed to **copy** from that file, not just view it.
- **It shows you the label.** When an answer in Copilot Chat draws on several files, you see the most
  restrictive label among them.
- **New content can inherit it.** What Copilot creates from labelled files can carry the most
  restrictive label.

A label doesn't stop *you* pasting text you're allowed to copy somewhere else. That judgement is yours.

> [!WARNING]
> Never lower or remove a label to get Copilot to work with a file. Your organisation usually asks for
> a reason when a label is lowered, and it can see the change.

### What agreements cover

Customer specifications, supplier certificates and anything under a non-disclosure agreement can carry
terms about where they may be processed. Those terms are in the contract, and no setting can tell you
what they say. If a document came from a customer or supplier, ask its owner before putting it into any
AI tool.

## In practice at Technik

You're preparing for a review on project `PRJ-2031` and have three things to summarise:

| Document | Label | Where | Verdict |
|---|---|---|---|
| Work instruction `SWI70000318` | *General* | Work Copilot | Fine |
| The customer's specification for `PRJ-2031` | *Confidential* | Work Copilot | Check the customer agreement first; if it's allowed, the label goes with the summary |
| A supplier's material certificate | None | A free AI site on your phone | No: wrong assistant, whatever the label |

People get the second row wrong in the other direction. Work Copilot is the *right* tool for a
confidential file, if the agreement allows it. Copying the text into a personal tool to "avoid" the
label is the mistake.

## Using it well

- **Check the account before the first paste.** Work account, work Copilot.
- **Read the label before summarising.** It's in the title bar; it takes a second.
- **Treat "no label" as "not yet classified"**, not as "public".
- **Ask before putting customer or supplier documents into any AI tool**, including work Copilot.
- **Remember that text inside a document can try to instruct Copilot** ({{topic:anatomy}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Copilot won't use a file you can open | An encrypting label lets you view it but not copy from it | Expected; ask the owner if you need more rights |
| A summary you made carries a label you didn't choose | It inherited the most restrictive label of its sources | Keep it; it's describing what went in |
| You pasted work content into a personal chatbot | Same app, personal account | Stop; tell your manager or IT what was shared |

## Key terms

**Enterprise data protection**: the terms under which work Copilot handles your prompts and responses,
the same as your organisation's mail and files.

**Sensitivity label**: an organisation-defined classification stamped on a file or email, which can
also apply protection such as encryption.

**Encryption (in a label)**: protection that limits who can open a file and what they may do with it.
