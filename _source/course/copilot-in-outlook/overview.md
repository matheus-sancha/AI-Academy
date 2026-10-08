## What this module is for

Mail is where most people meet Copilot first. The button is at the top of every long thread, and it sits
in the toolbar of every message you write. It's also where a bad draft does the most damage. A slide or
a paragraph gets read again before anyone acts on it. An email is sent, and a sent email is a
commitment with your name on it.

Copilot in Outlook does four useful things: it summarises a thread, drafts a message, coaches a draft
you wrote, and marks which incoming mail looks important. Microsoft gives the same caution for all of
them: what it generates *"may contain inaccuracies or sensitive material. Be sure to review and verify
the information that it generates."*

The five app modules share a shape (ask, make, one speciality, limits). Outlook's speciality is the
inbox: catching up after time away, where Copilot can suggest what needs you but can't know.

## Before you start

{{module:prompting}} applies to every request in this module, especially {{topic:clarity}} (say what
you need from a thread) and {{topic:iterate}} (adjust a draft rather than accept it).
{{topic:visibility}} explains why Copilot sees your own mailbox and nothing more.
{{topic:wordmake}} teaches the habit this module leans on most: the more of the content is yours before
Copilot starts, the less it invents.

Allow about 40 minutes.

## What you will be able to do

By the end of this module you should be able to:

- read a thread summary for what was decided, what is still open and who owes what, and check each
  point against the message it cites;
- write the facts of a reply yourself, then use coaching to change how it lands, and check what
  *Apply all suggestions* rewrote;
- set up inbox prioritisation before you need it, teach it what matters to you, and treat its marks
  as a starting point;
- name what Copilot in Outlook can't reach (shared, archive and group mailboxes, encrypted mail) and
  what a summary or a draft can lose;
- read every draft in full before you send it.

## The thread through this module

Every example comes from Technik, the fictional manufacturer this course is built around. See the
[scenario](../scenario/index.html) for the company and its documents.

One job carries the module. Three controlled documents are past their review date: `SOP70000114`
*Engineering Change Notification Process*, `SWI70000318` *Cladding Preparation and Inspection* and
`TDS70000044`, a technical datasheet. Technik's document controller has to get each one reviewed. A
reply-all thread about them has run to twenty-three messages. The controller summarises it, writes to
the owners, catches up after a week away, and finds where Copilot's reach ends. Only the documents and
the mail about them are used. No system data is involved.

## Self-check

Answer these before moving on. Each answer explains the reasoning, not just the verdict.

<details>
<summary>1. Copilot's summary of a long thread says "all three documents will be re-reviewed by the end of the month". How do you check it before you act on it?</summary>

Open the numbered citation behind that line, and read the last few messages yourself. Threads change
direction late, and a summary weighs the whole thread. Here, two messages from the end, the datasheet's
owner proposed withdrawing `TDS70000044` instead of reviewing it. Read the summary for decisions, open
questions and owners, not for the story. Reread {{topic:mailask}}.
</details>

<details>
<summary>2. You ask Copilot to draft "a reminder to the owners of the three overdue documents". The draft is polite, clear and offers a 30-day extension. What went wrong?</summary>

Nothing told it the facts, so it supplied likely ones, and an extension is a commitment you can't make.
Write the facts yourself: which document, which date, what you need from each owner. Then use
**Coaching by Copilot** to improve the tone and clarity. If you choose *Apply all suggestions*, read
what it rewrote, because it regenerates the text. Reread {{topic:mailmake}}.
</details>

<details>
<summary>3. You're back from a week away. You turned on Prioritize the morning you returned, and no mail from last week is marked. Is it broken?</summary>

No. Copilot only prioritises mail that arrives after the feature is turned on. It doesn't go back over
older messages. Turn it on before you need it, and teach it in its settings with phrases such as
*"It's about a controlled document past its review date"*. Reread {{topic:mailtriage}}.
</details>

<details>
<summary>4. Technik's document control team shares a mailbox. Copilot's summary button doesn't appear there. Why not, and what do you do?</summary>

Microsoft says Copilot in Outlook works only on your primary mailbox, not on shared, delegate, group or
archive mailboxes. It also can't read mail encrypted with S/MIME or Double Key Encryption. Read those
threads yourself. Reread {{topic:maillimits}}.
</details>

<details>
<summary>5. The thread summary is accurate, and your reply is ready to send. One early message said the datasheet is cited in a supplier specification. Neither the summary nor your reply mentions it. Whose problem is that?</summary>

Yours. A summary keeps what the thread repeats and drops what was said once. A caveat that nobody
answered is exactly what goes. Before a reply that commits anyone to anything, skim the thread for
conditions and warnings, and read the whole draft before you send it. Reread {{topic:maillimits}}.
</details>
