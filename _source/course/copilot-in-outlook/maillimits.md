## TL;DR

Mail has two traps of its own. A summary flattens a thread, so a caveat someone raised once and nobody
answered can disappear. And a drafted reply is fluent enough to send without reading, which is how a
wrong commitment leaves the building with your name on it. Copilot's reach also ends at your own
mailbox: shared, archive and group mailboxes, and some encrypted mail, are out of its sight.

## Why it matters

Microsoft says it directly: *"Review, edit, and verify anything it creates for you."* Its privacy page
adds that generated responses *"aren't guaranteed to be 100% factual"*, and that Copilot provides drafts
and summaries *"giving you a chance to review"* them *"rather than fully automating these tasks"*. In
mail, that review is the last step before something reaches another person.

## How it works

### A summary keeps what was repeated

A summary picks the key points of a thread ({{topic:mailask}}). What makes a point look key is that
people return to it. A warning raised once, in message 4, and never answered, looks like noise. Yet
it may be the most important thing in the thread. You can't ask Copilot to find what it didn't think
mattered. Before a reply that commits anyone to anything, skim the thread for conditions, warnings
and unanswered questions.

### A draft sounds finished

A generated draft has no rough edges to make you stop and read it. That's the trap. The fix is the habit
from {{topic:mailmake}}: write the facts yourself, and read every message in full before you send it.
Coaching changes how it lands. Checking what it says is still your job.

### What Copilot can't reach

<!-- verified tenant=2026-10 -->
Microsoft's FAQ: Copilot's features are *"only available on a user's primary mailbox. They are not
available on a user's archive mailbox, group mailboxes, or shared and delegate mailboxes."* Copilot
also can't read mail encrypted with **S/MIME** or **Double Key Encryption**. The chat pane needs a work
account and the new Outlook for Windows or Outlook on the web.
<!-- /verified -->

For other protected mail, Copilot honours the rights you hold. And it only ever sees what you could
already open ({{topic:visibility}}). Microsoft also says prompts, responses and the data Copilot reads
*"aren't used to train foundation LLMs"*.

### Smaller limits

- **Language.** Many languages are supported. Prioritising mail supports fewer (Microsoft's *Tier 1*
  languages).
- **Meeting preparation.** When little has been shared about a meeting, Microsoft says the result can
  be generic.

<!-- verified tenant=2026-10 -->
Microsoft doesn't say how far back Copilot reaches into an old thread in your primary mailbox, or
whether it reads attachment types beyond PDF, Word and PowerPoint.
<!-- /verified -->

## In practice at Technik

The document controller is ready to close out the three overdue documents.

**The caveat that went missing.** The datasheet's owner has confirmed the withdrawal of `TDS70000044`
({{topic:mailtriage}}). The controller drafts the reply that makes it obsolete. Before sending, they
skim the original thread for conditions, and find message 4, from purchasing: *"TDS70000044 is cited
in our cladding supplier's purchase specification. Please tell us before it's withdrawn."* Nobody
answered it. The summary didn't include it, and the reply didn't either. The controller adds
purchasing to the reply and asks them to update the specification first. If the reply had gone out
as drafted, Technik's supplier would have been left citing a withdrawn datasheet.

**The mailbox Copilot can't see.** Owners' questions about reviews also arrive in Technik's shared
*Document Control* mailbox. There's no summary button there. Microsoft says Copilot works only on the
primary mailbox. So the controller reads that thread the old way. It's short, and that's fine.

**The reply, read once.** The controller reads the final message top to bottom, checks the three
document numbers against the thread, and sends it.

## Using it well

- **Skim the thread for warnings and unanswered questions** before any reply that commits someone.
- **Read every draft in full before you send it**, however finished it sounds.
- **Know where Copilot can't help**: shared, delegate, group and archive mailboxes, and S/MIME or
  Double Key encrypted mail.
- **Check names and document numbers** in the final message against their source.
- **Expect weaker results** in languages Microsoft supports less well.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A warning from early in the thread is missing | Raised once and unanswered, so not a key point | Skim for conditions and questions before replying |
| A wrong commitment went out | A fluent draft was sent unread | Read every message in full before sending |
| No Copilot in a shared mailbox | Copilot works only on your primary mailbox | Read it yourself |
| *"Can't summarise"* on an encrypted message | S/MIME and Double Key Encryption are out of reach | Read the message yourself |
| A generic meeting brief | Little was shared about the meeting | Add the documents yourself, or prepare without it |

## Key terms

**Primary mailbox**: your own mailbox, the one Outlook opens with your account. Shared, delegate,
group and archive mailboxes are separate.

**Shared mailbox**: one mailbox that several people read and send from, such as a team address.

**S/MIME, Double Key Encryption**: two ways of encrypting mail so that Copilot can't read it.
