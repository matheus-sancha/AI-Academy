## TL;DR

Copilot in Outlook can draft a message from a few words, and it can coach a message you wrote,
commenting on tone, clarity and how the reader is likely to take it. Coaching is the safer habit: your
facts and your commitments stay yours, and only the way they land changes. Whichever you use, read the
whole message before you send it.

## Why it matters

A drafted email is fluent and polite, which is exactly why it gets sent unread. Once it's sent, a
date it offered or a promise it made is yours, with your name under it. The facts in a message should come from you, not from
what a model thinks is likely ({{topic:llm}}).

## How it works

### Drafting

<!-- volatile verified=2026-10 -->
Start a new message, select the **Copilot** icon in the toolbar, then **Draft** (in classic Outlook,
**Draft with Copilot**). Type what you want and select **Generate**. You can change the length or tone,
try again, or give a new prompt. When you're happy, select **Keep it**, then edit and send. Replying
works the same way, from **Help me write** or **Help me reply**. Drafting doesn't work on messages
written in plain text, only HTML.
<!-- /volatile -->

Microsoft notes one more thing: when you keep a draft, the message's sensitivity label may rise if the
generated content carries a higher one. Check the label before you send.

### Coaching

<!-- volatile verified=2026-10 -->
Write the message yourself, select the **Copilot** icon, then **Coaching by Copilot**. Copilot comments on
**tone**, **clarity** and **reader sentiment**. You can work suggestions in by hand, or select **Apply
all suggestions**.
<!-- /volatile -->

**Apply all suggestions** regenerates your text, so the message is a rewrite again, with the same
risk as any rewrite: a date softened, a condition dropped. Read what changed.

### Which to use

| You start from | What fills the message | Typical failure |
|---|---|---|
| A few words to Copilot | Copilot's sense of what such a message says | Invented specifics: dates, offers, promises |
| Your own draft, coached | Your facts, Copilot's suggestions on how they land | A qualifier lost if you *Apply all* without reading |
| Your own draft, sent as written | Your facts and your tone | Only what you'd risk without Copilot |

It's the same table as in Word ({{topic:wordmake}}): the more of the content is yours before Copilot
starts, the less it can invent.

## In practice at Technik

The thread is summarised ({{topic:mailask}}), and Technik's document controller now writes to the three
owners.

**The quick draft.** *"Remind the owners of SOP70000114, SWI70000318 and TDS70000044 that their review
is overdue."* The draft is courteous and clear. It also asks all three owners to *"complete the review
by the end of the month"*. That was already out of date: the datasheet is proposed for withdrawal, not
review. And it closes: *"If you need more time, a 30-day extension can be arranged."* Nobody offered
that, and the controller can't grant it. Copilot wrote what reminders like this usually say. Discard it.

**Your facts, coached.** The controller writes three short paragraphs, one per document:

- `SOP70000114`: please confirm whether this needs a full review or only a new review date, by Friday.
- `SWI70000318`: no action until revision C is released under `ECN70000042`; the review is then
  complete.
- `TDS70000044`: please confirm the withdrawal you proposed, so it can be made obsolete.

Then **Coaching by Copilot**. It says the opening reads as blunt, and suggests saying why the dates
matter. Fair. The controller works that in by hand.

**Apply all, read once.** Trying **Apply all suggestions** on a copy, the controller finds
*"by Friday"* has become *"at your earliest convenience"*. That's softer, and it means nobody has to
answer. The controller keeps the hand-edited version, with the date.

## Using it well

- **Write the facts yourself**: the document numbers, dates and asks.
- **Use coaching for how it lands**, not for what it says.
- **Read what *Apply all suggestions* changed**, especially dates, names and conditions.
- **Never send a commitment you didn't write**: an extension, an approval, a date.
- **Check the sensitivity label** after you keep a draft.
- **Read the whole message before you send it.** A fluent draft is the easiest one to send unread.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The draft offers something you can't give | Nothing told it the facts, so it wrote what is likely | Discard; write the facts yourself, then coach |
| *"By Friday"* became *"at your earliest convenience"* | *Apply all suggestions* regenerated the text | Work suggestions in by hand, or restore the date |
| **Draft** isn't offered | The message is in plain text | Switch the message to HTML |
| The sensitivity label changed | Generated content can raise it | Check the label before you send |

## Key terms

**Draft with Copilot**: Copilot writes a message from your prompt, which you keep, adjust or discard.

**Coaching by Copilot**: Copilot comments on a message you wrote, on tone, clarity and reader sentiment.

**Sensitivity label**: a marking on a message or file that says how confidential it is.
