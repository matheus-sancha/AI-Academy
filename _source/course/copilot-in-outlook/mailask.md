## TL;DR

Copilot in Outlook summarises a long thread in one click, with numbered citations that open the message
each point came from. Read the summary for what you actually need: what was decided, what is still open
and who owes what. Check each point against its citation, and read the last few messages yourself,
because that's where threads change direction.

## Why it matters

Nobody wants to read twenty-three messages to find one decision. But a thread isn't a document. It's
a conversation that changes its mind. The decision that holds is usually near the end, and a summary
can give it the same weight as everything said before it.

## How it works

### Where you find it

<!-- volatile verified=2026-10 -->
Open the conversation and select **Summary by Copilot** (or **Summarize**) at the top of the thread.
Copilot scans the thread for key points and shows a summary above the messages. On a phone, open the
conversation and select the **Copilot** icon in the toolbar.
<!-- /volatile -->

Microsoft says the summary can include *"numbered citations that, when selected, take you to the
corresponding email in the thread"*. Those numbers make a summary checkable. A point without one is
the summary's own wording.

### Attachments

<!-- volatile verified=2026-10 -->
For a PDF, PowerPoint or Word file attached to a message, select **Summarize a file**.
<!-- /volatile -->

A thread summary covers the messages. If the decision lives in an attached document, summarise the
file, or better, open it ({{topic:wordask}}).

### Asking for what you need

The button gives you Copilot's choice of key points. You choose what to read for:

| Read for | Why |
|---|---|
| **What was decided** | The thing you'll act on. Check it against its citation and the last messages |
| **What is still open** | Questions nobody answered. A summary tends to drop them, because nobody repeated them |
| **Who owes what** | Names and dates. A wrong name is a commitment someone never made |

If the summary doesn't answer one of the three, that doesn't mean the thread has no answer. Scroll to
the messages near the end and read them.

<!-- volatile verified=2026-10 -->
In the new Outlook for Windows and Outlook on the web, the **Copilot** icon in the navigation header
also opens a chat pane, where you can ask in your own words ({{topic:clarity}}).
<!-- /volatile -->

<!-- unknown since=2026-10 -->
Microsoft's pages don't say whether the chat pane reads the thread you have open, or how far back into
a long thread the summary reads.
<!-- /unknown -->

## In practice at Technik

Three controlled documents are past their review date: `SOP70000114` *Engineering Change Notification
Process*, `SWI70000318` *Cladding Preparation and Inspection* and `TDS70000044`, a technical datasheet.
Technik's document controller started a thread about them. It has run to twenty-three messages.

The controller selects **Summary by Copilot**. It reads well:

> *The owners agreed that all three documents will be re-reviewed by the end of the month. The SWI
> owner noted that revision C is in progress under ECN70000042. [1] [2]*

The controller reads it for the three things.

**Decided.** Citation [1] opens message 6, where the owners did agree to re-review all three. But
message 21, from the datasheet's owner, proposes something else: `TDS70000044` describes a coating
Technik no longer buys, so it should be withdrawn, not reviewed. Message 22 agrees. The summary's
decision was true a fortnight ago.

**Open.** Message 14 asked whether `SOP70000114` needs a full review or only a date change. Nobody
answered it, and the summary doesn't mention it.

**Who owes what.** Citation [2] checks out: revision C of `SWI70000318` is with its owner, waiting on
`ECN70000042`.

So the controller's note reads: SWI, waiting on the ECN; TDS, proposed for withdrawal; SOP, an open
question. The summary saved reading twenty-three messages. The last three changed what it meant.

## Using it well

- **Read the summary for three things**: decided, open, who owes what.
- **Open the citation** behind any point you'll act on.
- **Read the last few messages yourself.** That's where a thread changes direction.
- **Treat a point with no citation** as the summary's wording, not the thread's.
- **Summarise or open the attachment** when the decision lives in a file, not in the mail.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The summary's decision was later reversed | A summary weighs the whole thread, not the latest message | Read the last few messages before acting |
| An unanswered question is missing | Nobody repeated it, so it didn't look like a key point | Ask what is still open, or skim for questions |
| A point you can't find in any message | No citation, or it was inferred | Open the citation; if there is none, don't rely on it |
| The decision is in the attachment, not the mail | The thread summary covers messages | Use **Summarize a file**, or open the file |

## Key terms

**Thread**: a conversation in Outlook, the original message and every reply to it.

**Citation**: a numbered link in a Copilot summary that opens the message a point came from.

**Reply-all thread**: a thread where everyone answers everyone, which is why it grows long and
changes direction.
