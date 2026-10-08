## TL;DR

After time away, the useful question isn't *"summarise my mail"* but *"what needs me?"*. Copilot's
**Prioritize** feature marks incoming mail as high, normal or low priority and says why. You can teach
it what matters to you. Two things limit it: it only marks mail that arrives after you turn it on, and
it can't know which of your threads actually matters. Its marks are where triage starts, not where it
ends.

## Why it matters

A week away can leave hundreds of messages. Most can wait, a few can't, and the few that can't don't
always look urgent. A two-line *"can you confirm?"* from the right person matters more than a long
newsletter. Copilot can sort the pile by what *looks* important. Whether it is important depends on
what you're responsible for, and only you know that in full.

## How it works

### What Prioritize does

Microsoft: Copilot *"reviews your emails as they arrive in your inbox and assigns a priority (high,
low, normal) to them based on a list of factors—like people on the thread, their job titles, email
content and more."* It *"will lean towards marking emails where action is required from you as more
important."*

<!-- volatile verified=2026-10 -->
High-priority mail shows an **up arrow** in the message list. Open one and Copilot shows a few lines
explaining why it thinks the message matters to you. You can filter and sort the list by priority.
<!-- /volatile -->

The explanation is the useful part. It lets you disagree with a mark in seconds, rather than taking it
on trust.

### Teaching it what matters

<!-- volatile verified=2026-10 -->
Go to **Settings** > **Copilot** > **Prioritize** and describe what matters to you. Microsoft's
examples include *"It's from my manager"* and *"It's about a customer complaint"*. Turned on in one
place, it works in every Outlook you use.
<!-- /volatile -->

Microsoft advises phrases (*"it's from…"*, *"mentions…"*, *"contains…"*) rather than single words. Write
them the way you'd brief a colleague covering your inbox ({{topic:clarity}}).

### What it doesn't mark

Microsoft lists what Prioritize leaves alone:

- mail in any folder other than the inbox, including mail your own rules move;
- messages the sender marked as low importance;
- out-of-office replies and meeting invitations;
- encrypted messages, and very short messages;
- **anything that arrived before you turned it on.** It doesn't go back over older mail.

The last one decides how you use it. Prioritize helps after time away only if it was on while you were
away. Turn it on before you go, not the morning you return.

## In practice at Technik

Technik's document controller is back after a week away. They switched Prioritize on a month ago and
taught it two phrases: *"It's about a controlled document past its review date"* and *"It mentions
SOP70000114, SWI70000318 or TDS70000044"*.

**The marks.** Six messages have an up arrow. Four make sense: the reply about `SOP70000114`, a
question from an auditor, and two messages with clear asks. One is a newsletter from engineering that
happens to mention `SWI70000318`. The explanation shows it matched the phrase and nothing more. It
can wait. The sixth is a meeting follow-up that names the controller in an action list. That one
earns its arrow.

**What has no arrow.** The controller knows two things Copilot doesn't:

- The datasheet's owner was going to confirm the withdrawal of `TDS70000044`. Their reply is two words,
  *"Confirmed, withdraw."* A very short message isn't marked. Searching for the owner's name finds it.
- Teamcenter's workflow notices go to a folder by the controller's own rule. Prioritize doesn't look
  there. The controller opens the folder and finds that revision C of `SWI70000318` is ready for
  release.

Copilot cut the pile to a short list worth reading first. The two messages that closed two of the
three documents weren't on it.

## Using it well

- **Turn Prioritize on before you need it.** It only marks mail that arrives afterwards.
- **Teach it with phrases** about people, documents and asks, not single words.
- **Read the explanation** before you trust or dismiss a mark.
- **Search for the replies you're waiting on**, whatever their mark.
- **Check the folders your rules fill.** Prioritize only looks at the inbox.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Nothing from last week is marked | It only marks mail received after it was turned on | Turn it on before time away |
| A two-word reply you needed isn't marked | Very short messages are skipped | Search for the people you're waiting on |
| Important mail in a folder has no mark | Only the inbox is prioritised | Check the folders your rules fill |
| A newsletter is marked high | It matched a phrase you taught | Read the explanation; tighten the phrase |
| An encrypted message has no mark | Encrypted mail is skipped | Open encrypted mail yourself |

## Key terms

**Prioritize**: the Copilot feature that marks incoming mail high, normal or low priority and explains
why.

**Triage**: deciding what to deal with now, what later, and what not at all.

**Rule**: an Outlook setting that acts on incoming mail automatically, for example moving it to a
folder.
