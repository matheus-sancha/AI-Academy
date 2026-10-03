## TL;DR

An agent does not give the same answer twice, and it changes whenever you change its instructions,
knowledge, tools or model, sometimes in places you did not touch. *"It worked when I tried it"* is one
sample of a moving target. Evaluation means running a **fixed set of cases** after every change and
comparing the results with the last run. The comparison between runs is the signal. A single score on its
own tells you very little.

## Why it matters

Ordinary software gives the same output for the same input, so a test that passed once keeps passing until
someone changes the code. An agent breaks both halves of that.

**The same input gives different output.** The model samples its answer ({{topic:temperature}}), so a
question that was answered well once may be answered badly the next time. You saw the consequence in
{{topic:test}}: one success in the preview pane is not a pass, and one failure is only a hypothesis.

**Changes reach further than you meant them to.** Instructions, tool descriptions and knowledge sources
are all read together on every turn, so an edit made to fix one capability can move another. Some changes
are not even yours: a default model upgrade changes behaviour with nobody touching the agent
({{topic:model}}).

Put those together and manual spot checks stop working. You fix the case in front of you, and whatever
broke elsewhere goes unnoticed until a user finds it. Microsoft's own summary of the problem is the one to
remember. You want to answer a stakeholder with specifics, not with *"the agent seems okay"*.

## How it works

### Test chat and evaluation do different jobs

Microsoft draws the line between the two clearly:

| | Preview / test chat | Evaluation |
|---|---|---|
| Cases per run | One question at a time | A whole test set at once |
| Repeatable | Hard to repeat the same test exactly | The same set, re-run after every change |
| Control | Full: you steer every turn | Less: the cases run without you |
| Good for | Reproducing and diagnosing one problem ({{topic:manual}}) | Measuring the agent, and catching regressions |

You need both. The test chat tells you *why* one case fails. Evaluation tells you *whether* the agent got
better or worse overall.

### The run, and what you compare

On the GitHub Copilot harness the **Evaluate** tab holds your evaluations. Each one is a named set of test
conversations plus a test method, and every run of it is **saved separately** so you can compare runs over
time. Microsoft's own workflow ends in a loop: adjust the instructions, knowledge or tools, then run the
evaluation again to measure the impact. The standard harness has an equivalent Evaluation page and adds
automated runs through REST APIs and connectors.

What you compare is not just the headline score:

- **Which cases changed result.** A run that holds at 80% while two cases swap from pass to fail is a
  regression *and* a fix, and the score hides both.
- **Which category moved.** Microsoft's checklist reads a failing category as a diagnosis. Core cases
  failing means something is broken. Robustness failing means the agent is too strict about phrasing. An
  architecture case failing points at one tool or route. Edge cases failing means a guardrail needs work.

### Baseline first, then every change

Microsoft's evaluation checklist runs in four stages. You build a foundational set from the agent's key
scenarios, run it to set a **baseline**, expand it across quality categories, and keep running it once the
agent is in production. The baseline step is the one people skip. It means recording the pass rate together
with the **agent version and date**, because a later score means nothing without the one it is compared to.

Two practical points come straight from the checklist:

- **Run each set more than once and average.** Responses vary, so a single run can pass or fail a case by
  chance. Microsoft suggests aiming for a realistic **80–90%** pass rate set by business need, not 100%.
- **Re-run the full suite on specific triggers**: a model change, a major knowledge update, a new tool or
  connector, and any production incident.

<!-- volatile verified=2026-10 -->
### Evaluation costs credits

On the GitHub Copilot harness the Evaluate tab marks the actions that use Copilot Credits with a badge, and
every run reports its estimated credits, split into credits used to *generate* the agent's responses and
credits used to *grade* them, with a per-case figure as well ({{topic:licensing}}). Running a set three times
costs three runs. Budget for that before the first baseline.
<!-- /volatile -->

<!-- verified tenant=2026-10 -->
The standard harness does not charge for this: its test panel and its evaluation runs consume no Copilot
Credits.
<!-- /verified -->

## In practice at Technik

The Production Assistant has two near-twin tools, `Get operation efficiency` and
`Get work order lead time`, separated by their descriptions ({{topic:tooldesc}}). A planner reports that
*"how long is welding taking at Plant 1"* gives a lead time in days when they wanted efficiency. The fix is
a sentence in the efficiency tool's description naming overruns and *"taking longer than planned"*.

In the preview pane the fix works: three new chats, three efficiency answers. Then the evaluation set runs:

| Case | Before the fix | After the fix |
|---|---|---|
| *How long is welding taking at Plant 1 this month?* | Fail (lead time) | Pass |
| *What's the average lead time for `P7000001042` work orders?* | Pass | **Fail (efficiency)** |
| *How long until work order `100004521` is finished?* | Pass | Pass |
| Other cases across the seven capabilities | 22 of 22 pass | 22 of 22 pass |
| **Score** | 24 of 25 | 24 of 25 |

The score did not move, and the agent got worse at something a user had not complained about. The new
wording, *"how long work is taking"*, was close enough to the lead-time question to pull it across. Only
the case-by-case comparison shows it. The second fix, *"for calendar days from release to completion, use
`Get work order lead time`"*, goes into the efficiency description, and the set runs again: 25 of 25,
then 24 and 25 on two more runs.

That last line is the result worth recording, with the agent version and the date, as the new baseline.

## Design guidance

- **Build the set before the second change**, not after the tenth. The first change is your baseline.
- **Run the whole set after every change**, not just the case you were fixing.
- **Compare runs case by case.** Read which results flipped before reading the score.
- **Run a set two or three times** before you trust a result, and average.
- **Record the agent version, model and date** with every run you mean to rely on.
- **Re-run on the checklist's triggers**: model change, knowledge update, new tool, incident.
- **Expect 80–90%, not 100%.** Hunting the last case usually means fixing variance.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A fix works in preview, and users report something else broke | Only the fixed case was retested | Re-run the whole set after every change |
| The score is unchanged, so the change "did nothing" | Two cases flipped in opposite directions | Compare runs case by case |
| A case passes, then fails, with no change to the agent | Response variance | Run the set several times; average |
| Nobody can say whether the agent improved this quarter | No baseline was recorded | Record pass rate, version and date on the first run |
| Behaviour changed and nobody edited the agent | Default model upgrade | Re-run the suite on every model change ({{topic:model}}) |
| The evaluation budget runs out mid-build | Repeated runs consume credits | Check the run's estimated credits early ({{topic:licensing}}) |

## Key terms

**Evaluation**: running a fixed set of test cases against the agent and scoring the responses, after
every change.

**Test set**: the fixed group of test cases an evaluation runs. On the GitHub Copilot harness, each case is
a conversation.

**Baseline**: the first recorded run, with its pass rate, agent version and date, that later runs are
compared against.

**Regression**: a case that passed before a change and fails after it.

**Run**: one execution of a test set. Each is saved separately, so runs can be compared.
