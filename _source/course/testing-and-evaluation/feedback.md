## TL;DR

Real user questions, thumbs up and down, comments and transcripts are the best source of new test cases, because
they are the cases you did not think of. **Close the loop**: a failed conversation becomes a new case in the
user's exact words, then a fix, then a run of the whole set. Do it on a schedule, because transcripts expire.
An evaluation set that never grows stops being evidence about the agent people are actually using.

## Why it matters

Every case in a set written before launch comes from the brief and from the team's imagination. That is the
right place to start, and it has a ceiling. The team cannot write the question nobody on it would ask, in
wording nobody on it would use.

Users write those cases every day, by asking. Most of them succeed and are never seen again. The ones that fail
show up as a thumbs down, a comment, a session that ended in an error, or a complaint in a corridor. Each of
those is a test case that already failed once in production, which makes it worth more than any case you could
invent. And without a loop, each failure is found once, fixed by hand, and free to come back with the next
change.

## How it works

### Where the signal is on the GitHub Copilot harness

<!-- volatile verified=2026-10 -->
The **Monitor** tab shows an agent's production health, and it fills only after the agent is published and
people use it. Three parts of it feed the loop:

- **Reactions**: the count of thumbs up and thumbs down on agent responses. *See details* lists them, filtered
  by reaction or by whether the user left a **comment**, and opens each response in its conversation context.
  Users can react only if **User feedback** is on, under *Settings → Safety & access*.
- **Sessions**: every conversation, with its status, messages, tools used and credits. Filter by **Failed** or
  **Rejected** status, and open a session for its full transcript, including tool invocations and knowledge
  source usage.
- **Download**: session transcripts can be downloaded for any period in the last 29 days. The sessions list
  itself shows the past **28 days** only.

Whether response text and session details are visible to you depends on your permissions and your
administrator's data-access settings.
<!-- /volatile -->

Reading the dashboards themselves, on both harnesses, is {{topic:analytics}}. The standard harness adds
**themes**, which group real user questions and can seed a test set directly ({{topic:testsets}}). This lesson
is about what to do with what the dashboards show you.

<!-- unknown since=2026-10 -->
The GitHub Copilot harness's pages describe no route from a Monitor session or reaction to a new evaluation
case. Copying the user's turns into a conversation by hand, or into the CSV, is the documented path.
<!-- /unknown -->

### The loop

1. **Harvest.** On a fixed day, list the thumbs down, the comments and the failed sessions since the last
   harvest. Weekly is safe against a 28-day window. Monthly is not.
2. **Read the transcript.** The reaction says the user was unhappy. The transcript says with what, and the tool
   and knowledge entries say what the agent did.
3. **Reproduce.** Replay the user's exact turns in a new preview chat, three times, and classify the fault
   ({{topic:manual}}).
4. **Write the case.** Keep the user's wording: their typos are the robustness case you could not invent
   ({{topic:advtests}}). Add the expected response, and name the brief slot it belongs to.
5. **Fix one thing, run the whole set.** Not just the new case ({{topic:runeval}}).
6. **Keep the case.** It stays in the set for good, so the same failure cannot come back unseen.

### Reading the signal honestly

Reactions are sparse and lopsided. Most users never press either thumb, and the ones who do are mostly unhappy.
So a thumbs-up rate is not a quality score, and a quiet week is not a good one. Treat each reaction as a pointer
to a conversation worth reading, not as a measurement.

Three kinds of signal deserve more than a case:

- **A question no category covers.** That is a gap in the brief, not just the set. Send it back to the
  people who own the brief ({{topic:brief}}).
- **The same complaint from several users.** Check whether it is one failure or a missing task.
- **A failed session with no reaction.** Errors the user gave up on are the ones that never get reported.

## In practice at Technik

The Production Assistant's team harvests every Monday. One week's list held four thumbs down, two with
comments, and three failed sessions.

One comment read *"wrong, this is the old one"*. The transcript showed a supervisor asking *"drawing for
cladding on 4513?"*. The agent had answered with the drawing revision recorded on work order `100004513`'s
cladding operation in SAP, and stopped there. A released ECN had since replaced that revision in Teamcenter.
The supervisor knew; the agent never checked. Reproduced three times out of three, and the trace classified it:
the right tool, the right inputs, and an **instructions** fault. Nothing told the agent that a revision read
from a work order is a claim to verify, not an answer.

It became case 31, in the supervisor's words:

| Field | Content |
|---|---|
| **Conversation** | *drawing for cladding on 4513?* |
| **Category** | Edge case: work order on a superseded revision |
| **Expected response** | Must give the revision the work order references *and* the latest released revision. Must say they differ. Must not present the work order's revision as current |

The fix was one sentence in the instructions: when a revision comes from a work order, check it against the
latest released revision and say if they differ. Then the whole set ran again, and case 31 stayed in it.

The three failed sessions were tool timeouts during one night's Snowflake maintenance. That is an operations
problem, not a behaviour one, so they went to the error review in {{topic:analytics}} and got no case. Not
every signal belongs in the set.

## Design guidance

- **Turn on User feedback** before you publish, so reactions can arrive at all.
- **Harvest on a fixed day, inside the 28-day window**, and download what you need to keep.
- **Read transcripts, not reaction counts.** A reaction is a pointer, not a score.
- **Keep the user's exact words** in the new case, typos included.
- **Fix one thing, then run the whole set**, and keep the case for good.
- **Send uncovered questions to the brief**, not only to the set.
- **Look at failed sessions with no reaction.** Silent failures are the ones nobody reports.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The set scores well and users keep complaining | Its cases come from the team, not from use | Add a case for every reproduced production failure |
| The same failure comes back two releases later | Fixed by hand, never added to the set | Every fixed failure becomes a permanent case |
| A reported failure cannot be found | The 28-day sessions window passed | Harvest weekly; download transcripts you need |
| The Monitor tab shows no reactions | User feedback is off, or the agent is unpublished | Turn it on under *Safety & access*; publish |
| A new case passes immediately | It was rewritten in polished wording | Keep the user's own words |
| Thumbs-up rate treated as quality | Reactions are sparse and lopsided | Use reactions to find conversations; measure with the set |

## Key terms

**Feedback loop**: production failure → transcript → reproduction → new case → fix → full run → kept case.

**Reaction**: a user's thumbs up or thumbs down on one agent response, optionally with a comment.

**Harvest**: the scheduled review of reactions, comments and failed sessions since the last one.

**Transcript**: the full record of a session, including the tools and knowledge the agent used.
