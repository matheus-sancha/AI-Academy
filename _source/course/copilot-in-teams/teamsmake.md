## TL;DR

In Teams, Copilot works on messages you've already written. Type your message, then select **Rewrite
with Copilot**. **Rewrite** suggests other versions, and **Adjust** changes the length or tone. It can
also translate. Because the facts are yours before Copilot starts, it's the safe habit from mail
built into the compose box. What's left to check is what a rewrite changed: a tone adjustment can turn
a hope into a promise.

## Why it matters

A channel post reaches a whole team at once, and people act on it. A scrappy note is a nuisance. A
polished note that says something you didn't mean is worse, because nobody questions it.

## How it works

### Your words first

Microsoft's page is about rewriting: *"The compose box now includes Copilot to help you rewrite and
edit chat and channel messages, adjusting tone and length."* You write the message, and Copilot
reworks it. That's the order {{topic:mailmake}} recommends for mail, and Teams builds it in.

If you need a first draft from nothing, ask Copilot Chat ({{topic:m365chat}}) and give it the facts.
Then paste the result into Teams and read it as if a colleague wrote it.

### Rewrite and Adjust

<!-- verified tenant=2026-10 -->
1. Write your message in the compose box.
2. Select **Rewrite with Copilot** beneath the box, then choose **Rewrite** or **Adjust**.
   - **Rewrite** offers other versions, and you move between them with the arrows.
   - **Adjust**: **Make it** concise or longer; **Make it sound** casual, professional, confident
     or enthusiastic.
3. Select **Replace** to use the new version, or **X** to keep your own. Then select **Send**.

To rework a message you've already sent, hover over it, select **Edit**, then **Rewrite with
Copilot**. Select **Done** to save it.
<!-- /verified -->

You can also select part of a message and rework only that. Use it when one sentence is clumsy and the
rest is right.

<!-- verified tenant=2026-10 -->
Microsoft's FAQ describes a **Custom Tone** option where you can *"fine-tune the tone, translate the
message, or add additional context"*.
<!-- /verified -->

### What to check

A rewrite keeps your facts most of the time. The risk is in the words that carry weight: *should*
against *will*, *about* against *by*, a condition against a statement. Read the new version against
your own before you select **Replace**.

## In practice at Technik

Revision C of `SWI70000318`, *Cladding Preparation and Inspection*, is nearly ready, and
`ECN70000042` is waiting on it. A quality engineer types a quick note to the manufacturing engineering
channel:

> *rev C of SWI70000318 shld be released next wk if UT inspector confirmed. sec 4 adds UT check before
> cladding, sec 5 porosity limit tighter. XT bores already in the queue still go to rev B. ECN70000042*

The facts are right, but the note is hard to read. The engineer selects **Rewrite with Copilot** >
**Adjust** > **Make it sound** professional:

> *Revision C of SWI70000318 is expected to be released next week, subject to confirmation of an
> ultrasonic (UT) inspector. Section 4 adds a UT check before cladding, and section 5 tightens the
> porosity limit. XT bores already in the queue will continue to follow revision B. This change is
> tracked under ECN70000042.*

That's better, and every fact survived. Out of curiosity, the engineer tries **confident** too:

> *Revision C of SWI70000318 will be released next week. …*

The condition is gone. *Should, if* became *will*. The confident version would tell the shop floor a
date that depends on an inspector nobody has confirmed. The engineer picks the professional version,
reads it once more against their own note, and posts it.

A colleague at the plant asks for it in Portuguese. The engineer uses the custom option to translate
it. Before sending, they check the two document numbers and the ECN number came through unchanged.
<!-- verified tenant=2026-10 -->
Microsoft's pages don't say whether a translation keeps identifiers and technical terms intact.
<!-- /verified -->

## Using it well

- **Write the facts first**, then let Copilot change how they read.
- **Compare the rewrite with your own**, looking hardest at dates, conditions and *should* against *will*.
- **Rework only the clumsy sentence** by selecting it, and leave the rest alone.
- **Keep your own version** with **X** when no suggestion is better.
- **Check numbers and names** in a translation before you send it.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A condition disappeared | A tone adjustment rewrote it as a statement | Compare with your own before **Replace** |
| A shorter version lost a fact | **Concise** cuts what looks least important | Use it on a selection, or trim by hand |
| You can't get a message out of a blank box | The compose box rewrites what you typed | Type the facts first, or draft in Copilot Chat |
| A sent post now says something different | **Edit** > **Rewrite with Copilot** changed more than intended | Read it before **Done** |

## Key terms

**Compose box**: the box at the bottom of a chat or channel where you type a message.

**Rewrite**: a Copilot option that suggests other versions of what you wrote.

**Adjust**: a Copilot option that changes the length or tone of what you wrote.
