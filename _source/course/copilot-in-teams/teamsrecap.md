## TL;DR

After a recorded or transcribed meeting, its **Recap** holds the transcript, AI-generated notes and
follow-up tasks, plus the moments your name came up. It's the most useful thing Copilot does for most
people, because otherwise nobody writes the meeting down. It's also the costliest when it's wrong. A
task under the wrong name is a commitment that person never made. So check every task against the
transcript before you send the notes on.

## Why it matters

A meeting ends, and everyone walks away remembering a slightly different version of who agreed to do
what. A recap fixes that, as long as it's right. Microsoft says plainly that recap content *"is based
on the event transcript"* and *"might be inaccurate, incomplete, or inappropriate"*. The recap is only
as good as the transcript under it, and it hides that transcript one click away.

## How it works

### Where you find it

<!-- volatile verified=2026-10 -->
After the meeting, open the meeting chat and select the **Recap** tab, or **View recap** on the
meeting's thumbnail. The recap has tabs including **Recording**, **Transcript**, **AI notes**
(notes and follow-up tasks), **Mentions** (where your name was spoken), **Speakers** (who spoke when)
and **Chapters**.
<!-- /volatile -->

### What it needs

| Needs | Because |
|---|---|
| **Recording or transcription** | Microsoft: recaps *"are available after Teams events… that were recorded or transcribed"* |
| **A meeting longer than five minutes** | For the AI-generated notes |
| **An invitation** | *"People in your org can access an event's intelligent recap if they were invited"* |

No transcript, no recap. Who turns transcription on, and why that differs from meeting to meeting, is
{{topic:teamslimits}}.

AI notes and tasks don't last forever: Microsoft says they *"will expire according to your org's
policies"*. Copy the tasks somewhere permanent.

### Asking about the meeting

You can also ask Copilot about the meeting, from the meeting chat or the **Recap** tab, in your own
words. Microsoft's examples include *"What ideas were discussed?"* and *"Where do we disagree on this
topic?"* After the meeting, Copilot answers from the transcript and the meeting chat. Ask the
question you actually have: *"What did we decide about X, and who is doing Y?"*

### Checking a task

The **Speakers** view and the transcript's speaker names and timestamps are how you check a task.
Find the moment the task was agreed. Read who said *"I'll do it"*, not just who raised it.

## In practice at Technik

A design review meeting walks through revision C of `SWI70000318`, *Cladding Preparation and
Inspection*: the new ultrasonic check before cladding, and the tighter porosity limit. It's
transcribed. Afterwards, the quality engineer who organised it opens **Recap** > **AI notes**. The
follow-up tasks read:

> - *NDT lead to arrange ultrasonic inspector qualification for the cladding cell.*
> - *Quality engineer to update section 5 of SWI70000318 with the revised porosity limit.*
> - *Cladding supervisor to confirm which XT bores in the queue still follow revision B.*

Before forwarding them, the engineer checks each one in the transcript.

The first is wrong. At 34:10 the NDT lead says *"someone needs to sort out UT qualification for that
cell"*. At 34:25 the cladding supervisor says *"I'll take that, it's my people"*. The recap gave the
task to the person who raised it. The NDT lead never agreed to it.

The second and third check out. The engineer corrects the first, puts the three tasks in the meeting
chat under the right names, and asks each owner to reply *"agreed"*. It takes five minutes. Without
the recap there'd be no list at all. Without the check, the qualification would wait on someone who
doesn't know it's theirs.

<!-- unknown since=2026-10 -->
Microsoft's pages don't say whether AI-generated notes and tasks can be edited in the recap itself.
<!-- /unknown -->

## Using it well

- **Check every task** against the transcript before you pass it on.
- **Look for who agreed**, not who raised it.
- **Post the corrected tasks** where the owners will see and confirm them.
- **Ask the question you have** rather than reading a general summary.
- **Make sure the meeting is transcribed** if you'll need the recap ({{topic:teamslimits}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A task under the wrong name | The recap linked it to whoever raised it | Find the moment in the transcript and correct it |
| No recap at all | The meeting wasn't recorded or transcribed | Write the notes yourself, and transcribe next time |
| No AI notes for a short meeting | AI notes need a meeting longer than five minutes | Write them, it was short |
| A colleague can't open the recap | They weren't invited | Share the corrected notes in the chat |

## Key terms

**Recap**: the page after a Teams meeting that gathers its recording, transcript, notes and tasks.

**AI notes**: the notes and follow-up tasks Copilot generates from the transcript.

**Transcript**: the written record of what was said, with each speaker's name and a timestamp.

**Follow-up task**: an action the recap thinks someone agreed to. Treat it as a claim to check.
