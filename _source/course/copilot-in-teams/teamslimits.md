## TL;DR

Teams is the one app where what Copilot can do depends on a setting somebody else chose. You can use
Copilot during a meeting without a transcript. But asking about the meeting **afterwards** needs a
transcript, and whether there is one is up to the organiser's meeting options. So two meetings on the
same day can give you a full recap and nothing at all. A transcript can also mishear, and everything
built on it inherits the error.

## Why it matters

People assume Copilot remembers every meeting. It remembers the ones that were transcribed. Finding
that out the morning after, when you need the decision, is too late.

## How it works

### The organiser's setting

<!-- verified tenant=2026-10 -->
The organiser sets **Allow Copilot and Facilitator** under **Online meeting options** > **Copilot and
other AI**. There are three choices:

| Setting | During the meeting | After it |
|---|---|---|
| **During and after the meeting** | Copilot starts when transcription starts | Ask about it, and see the recap |
| **Only during the meeting** | Copilot works without a transcript | *"Speech-to-text data that wasn't transcribed and interactions with Copilot will no longer be available"* |
| **Off** | No Copilot. Recording and transcription are off too | Nothing |
<!-- /verified -->

Microsoft's FAQ: *"After the meeting, Copilot will answer questions using the most recent available
transcript. If there is no transcript available, Copilot will only be available for the meeting chat."*
If someone starts transcribing partway through, Copilot covers only the transcribed part.

### Who can start a transcript

<!-- verified tenant=2026-10 -->
In the meeting, **More actions** > **Record and transcribe** > **Start transcription**, then confirm
the spoken language. Recording starts transcription automatically. Who may do it is a meeting option
the organiser sets: organisers and co-organisers, presenters as well, or no one.
<!-- /verified -->

So if a meeting matters, ask the organiser beforehand. If you're the organiser, decide before people
join. Everyone sees a notice when a meeting is being transcribed.

### Other meetings and other content

- **Meetings outside Technik.** Microsoft: *"Copilot won't work in meetings that are hosted outside
  the participant's organization."* A supplier's meeting is outside its reach.
- **Shared content.** In chats, Copilot can't read images, Loop components or shared files
  ({{topic:teamsask}}).
- **Languages.** Microsoft lists English, Spanish, Japanese, French, German, Portuguese, Italian and
  Simplified Chinese.

### When the transcript is wrong

Copilot names people by *"the first string in the attendee's display name"*. Two attendees with the
same first name look the same in its answers. People can also hide their identity in transcripts.

<!-- verified tenant=2026-10 -->
Microsoft's pages don't say how well transcription handles document and part numbers, names, or two
people talking at once.
<!-- /verified -->

Assume it can get them wrong. A recap is built on the transcript, so it repeats what it misheard.

## In practice at Technik

Two meetings on the same day, both about revision C of `SWI70000318`, *Cladding Preparation and
Inspection*.

**The morning design review** is set to *During and after the meeting* and is transcribed. The quality
engineer gets a recap, checks its tasks ({{topic:teamsrecap}}), and asks Copilot what was decided
about section 5.

**The afternoon call with the cladding cell** was set up by someone else, with Copilot *Only during
the meeting*. The engineer used Copilot during the call, to catch up after joining late. The next
morning they ask it what the cell agreed about the queue of XT bores. There's no transcript, so
Copilot has only the meeting chat, which says nothing useful. The engineer writes down what they
remember, posts it in the chat, and asks the cell to correct it.

Back in the morning recap, one line reads *"Revision C of SWI70000381 to be released after
qualification."* The transcript had misheard *318* as *381*, and the recap repeated it. `SWI70000381`
is a different document. The engineer corrects the number before the notes go anywhere.

## Using it well

- **Decide on transcription before the meeting**, or ask the organiser to.
- **Write your own notes** when a meeting isn't transcribed.
- **Check every document number and name** in a recap against what you know was said.
- **Don't expect Copilot** in meetings hosted by another organisation.
- **Watch for shared first names** in tasks and answers.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Copilot knows nothing about yesterday's meeting | It was set to *Only during the meeting*, or not transcribed | Write notes; transcribe next time |
| Copilot covers only the second half | Transcription started partway through | Fill in the first half yourself |
| No Copilot in a supplier's meeting | It's hosted outside your organisation | Take your own notes |
| A wrong document number in the recap | The transcript misheard it | Check identifiers against the source |
| A task under the wrong person | Two attendees share a first name | Check the transcript's speaker |

## Key terms

**Organiser**: the person who scheduled the meeting and controls its options.

**Meeting options**: the settings for one meeting, including Copilot and who can record and transcribe.

**Live transcription**: Teams turning speech into text with speakers' names and timestamps as the
meeting runs.
