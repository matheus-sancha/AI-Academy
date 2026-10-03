## TL;DR

Analytics show how the published agent is actually used: sessions and users, how sessions end, thumbs up and
down, which tools ran, failures, and what it all cost. On the GitHub Copilot harness this is the **Monitor**
tab; on the standard harness, the **Monitor** page. Use it for two jobs: deciding **what to improve next**, and
finding the **questions your evaluation set does not contain**. The numbers point; the session transcripts
explain.

## Why it matters

Evaluation tells you how the agent does on the questions you thought of ({{topic:whyeval}}). Users ask the
others. A planner phrases a lead-time question in a way nobody tested; a supervisor asks for something the brief
ruled out; a whole user group stops coming back after the first week. None of that appears in an evaluation
run, because none of it was in the set.

Analytics is the only view of the agent people are really using. It is also easy to misread: a high session
count says people opened it, not that it helped them, and a thumbs-up rate from the few who click says little
about the many who don't.

## How it works

### The GitHub Copilot harness's Monitor tab

<!-- volatile verified=2026-10 -->
Microsoft describes it as *an in-context view of an agent's production health*. It holds:

| Section | What it shows |
|---|---|
| **Overview** | Total sessions, users, autonomous runs, average duration, success rate and fail rate, each compared with the previous period |
| **Reactions** | How often users chose thumbs up or thumbs down on responses |
| **Total estimated credits used** | Credits consumed in the period, with a breakdown by experience such as production use, preview testing and evaluations |
| **Capabilities** | **Tool use**: which tools the agent invoked |
| **Sessions** | Each session's status, duration, messages, channel, tools used and credits; the last **28 days** |

Selecting a session opens its **full transcript**: the user's messages, the agent's responses, and details of
tool calls and knowledge sources used. Sessions can be filtered by status, including **Failed** and
**Rejected**. Transcripts can be downloaded for any period in the last **29 days**, and data can take up to an
hour to appear. You can open Monitor before publishing, but production data arrives only once people use the
published agent.
<!-- /volatile -->

The credits figure is worth knowing about. Unlike the estimates in Preview and Evaluate, Microsoft says the
Monitor number *is the final, source-of-truth number used for billing* ({{topic:licensing}}).

### The standard harness's Monitor page

<!-- volatile verified=2026-10 -->
Richer and older: data for up to **360 days**, session details and transcripts for **28**, all times in UTC. It
adds an AI-generated **summary** of insights, **active users** (daily and monthly, only if the agent requires
authentication), session **outcomes** (resolved, escalated, abandoned), **satisfaction**, and **themes**
(preview), which group users' questions by subject and can seed an evaluation set. Activity in the **test
panel** is excluded.
<!-- /volatile -->

### Who can see it

On the standard harness, the **Analytics viewer** sharing role gives read-only access to the Monitor page
without access to the agent. Drilling into anything that comes from a transcript also needs the **Bot
Transcript Viewer** security role, which by default only admins hold. Transcripts are users' own words, so
Microsoft suggests granting that role only to people with appropriate privacy training ({{topic:share}}).

### Reading it

Each number is a question, not an answer:

| Signal | Question it raises | Where you look |
|---|---|---|
| Fail rate rising | What broke, and since when? | Failed sessions; a recent publish ({{topic:publish}}) |
| Thumbs down clustered | On which kind of question? | Those sessions' transcripts |
| A tool never used | Is it unnecessary, or is its description never matched? | {{topic:tooldesc}} |
| A tool used where it shouldn't be | Near-twin descriptions | The tool's transcript calls |
| Few sessions per user | Did people try it once and leave? | The first sessions of new users |
| Credits up with sessions flat | Longer sessions, or more tool calls per turn? | Session credits and tools used |

The transcript is where every row ends. Read sessions, not just charts, and turn what you find into test cases:
{{topic:feedback}} is that loop.

## In practice at Technik

Two weeks after the Production Assistant reached all three user groups, its Monitor tab showed:

- **Sessions and users**: steady, with planners making most of them.
- **Reactions**: mostly positive, with a cluster of thumbs down in the second week.
- **Tool use**: `Get work order lead time` almost never invoked, `Get operation efficiency` invoked far more
  than the efficiency questions in the evaluation set would predict.

Opening the thumbs-down sessions explained both. Planners were asking *"how long are cladding jobs taking on
2031?"* and meaning **lead time**, calendar days from release to completion. The efficiency tool's description
claimed *"how long work is taking"*, so it won the match, and the answer arrived as a percentage nobody had asked
for.

None of the evaluation set's lead-time cases phrased the question that way, so the set had passed. The fix went
into the tool descriptions ({{topic:tooldesc}}), and three of the planners' own sentences went into the
evaluation set unchanged. On the next run, those were the cases that told the engineer the fix worked.

Who reads what was decided too. The engineer and the team lead review the Monitor tab weekly. Transcript access
went only to them, because transcripts include work order discussions and quality engineers' notes on
nonconformances.

## Design guidance

- **Read the Monitor tab on a schedule**, weekly at first, not only when someone complains.
- **Open the transcripts** behind every cluster of thumbs down or failures before changing anything.
- **Treat tool-use counts as a description check.** Unexpected counts usually mean a description is matching
  the wrong questions.
- **Turn real users' phrasings into test cases**, unchanged.
- **Limit transcript access** to people who need it and know how to handle it.
- **Watch credits per session**, not only in total.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Monitor is empty | The agent isn't published, or nobody has used it yet | Production data appears after use; check the period filter |
| The evaluation passes and users complain | Users ask what the set doesn't contain | Mine transcripts for new cases ({{topic:feedback}}) |
| High satisfaction, low use | The few who react aren't the many who left | Look at users and sessions per user |
| A colleague can see charts but not transcripts | Transcript drill-downs need Bot Transcript Viewer | Grant it deliberately, to the right people |
| Last quarter's sessions are gone | Sessions and transcripts are kept for 28–29 days | Download transcripts you need to keep |

## Key terms

**Monitor**: the tab (GitHub Copilot harness) or page (standard harness) where published-agent analytics live.

**Session**: one conversation with the agent, with its status, duration, channel and credits.

**Reactions**: users' thumbs up and thumbs down on responses.

**Tool use**: how often each tool was invoked, a check on whether descriptions match real questions.

**Transcript**: the full record of a session, including tool calls and knowledge used.
