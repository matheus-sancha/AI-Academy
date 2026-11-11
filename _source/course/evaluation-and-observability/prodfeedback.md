## TL;DR

Intermediate taught the loop on Copilot Studio's Monitor tab: harvest what users did, read the
transcript, write the case in their words, fix one thing, run the whole set. A pro-code agent changes
three things. The signals come from Application Insights and Foundry's monitoring, not from a tab you
share. Production can be graded as well as read, by evaluations that run on a sample of live traffic
or on a schedule. And a new case has to fit the harness you own: a dataset line, a replay script and a
baseline entry. The first question is where the failure lived, because that decides where its test
goes. Neither curated page describes the route from a conversation to a case, so the loop is this course's.

## Why it matters

{{topic:evalstrategy}} listed what starts a full run: a model change, a new tool, a knowledge update
and a production incident, on top of a regular cadence. Only the last arrives from outside the repo,
and the capstone's eight cases give each question one phrasing, so the first real user's wording will
not be among them. The reason to read production is that it holds the cases you did not think of. The
reason to be careful is that a case copied in carelessly protects nothing, or blocks nothing, or
copies a person into a repository. {{topic:analytics}} and {{topic:feedback}} taught the reading. This
lesson is about the pipeline behind it.

## How it works

### What production gives you

Foundry's observability page describes post-production monitoring as five things: operational metrics,
continuous evaluation ("quality and safety evaluation of production traffic at a sampled rate"),
scheduled evaluation ("using test datasets to detect system drift"), scheduled red teaming, and Azure
Monitor alerts "when outputs fail quality thresholds or produce harmful content". Integrated with
Application Insights, its dashboards track "operational metrics, token consumption, latency, error
rates, and quality scores".

Two of those answer different questions from a trace ({{topic:tracing}}). A trace explains one
conversation you already know about. Sampled evaluation grades conversations nobody reported, so it
finds the failure before the complaint. Scheduled evaluation re-runs your own dataset, which is the
only thing that notices a model that changed on the platform's side with no commit in your repository
({{topic:evalstrategy}}).

<!-- unknown since=2026-11 -->
The page points to a Monitor agents dashboard page for setup, and the course does not curate it. Neither
curated page says how a sampled evaluation's results are read case by case, or describes any route from
a production conversation to a test case.
<!-- /unknown -->

### Copilot Studio's side

For an agent on Copilot Studio the signals are the Monitor page, already covered in {{topic:analytics}}.
What matters to a pipeline is its limits.

<!-- volatile verified=2026-11 -->
Monitor data is kept for up to 360 days and session details and transcripts for 28. Activity in the
test panel is excluded. The Analytics Viewer role can be shared only with individuals, not groups, and
reading a transcript also needs the Bot Transcript Viewer role. Outcomes are Resolved, Escalated and
Abandoned, and active-user counts need an agent that requires authentication.
<!-- /volatile -->

A transcript you want in a test set has to be taken inside that window. The page documents no export
route into a dataset.

### Where did the failure live?

Before writing the case, ask what produced the failure, because the answer decides where its test goes.

| It lived in | Example | Where the test goes |
|---|---|---|
| The model | A right tool result, misread | A live case, graded by a check or a judge |
| Your code, tools or data | The guard let an ungrounded answer through, or a view returned the wrong row | An offline test with a scripted turn |

The distinction comes from how the capstone's two runs differ ({{topic:evalharness}}). The offline run
replays a scripted model, so it can show that code and tools behave and cannot show that a model does.
A case in the live set guards a model failure and a test with a scripted bad turn guards a code failure.

### Writing the case into the harness

In the capstone, a new case is four edits that belong in one reviewed change.

1. **A line in `evals/eval_set.jsonl`**, with the user's wording as the `query`.
2. **A script in `evals/replay.jsonl`** for its `id`. The replayed client looks the script up by id, so
   without one the offline run fails on the new case.
3. **An entry in `evals/baseline.json`.** `compare` walks the baseline, so a case missing from it shows
   as `new` and can never be flagged as a regression.
4. **A regenerated `evals/action_dataset.json`**, because a test fails when it drifts from the set.

## In practice at Technik

Suppose a manufacturing engineer asks the assistant "Can I use rev C of SWI70000318 on the next bore?"
and it says yes. The trace shows `get_revision_status` called with the right document and revision, and
a result saying revision C is In Work. A tool result backed the answer, so the refusal guard let it
through. This is `rev-03` in a phrasing the set does not have, and it lived in the model.

| Field | New case |
|---|---|
| `id` | `rev-04` |
| `category` | `trap`, like `rev-03` |
| `query` | The engineer's sentence, without the engineer |
| `ground_truth` | No. Revision B is the released revision. Revision C is In Work, waiting on `ECN70000042`. |
| `expected_tool_calls` | `get_revision_status` for `SWI70000318`, revision `C`, as in the trace |
| `must_include` | `rev B\|revision B` and `not released\|in work` |

Because it lived in the model, the case guards a live run. Offline, its replay script holds the correct
turn, so it passes every time and proves only that the plumbing accepts the new line. And the committed
`baseline.json` holds an offline baseline only, so a live run has nothing to compare with until someone
runs `--update-baseline` and the diff is reviewed. A failure in the guard would go the other way: a test in
[`agent/tests/test_evals.py`](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/agent/tests/test_evals.py)
already feeds the replay an answer from memory and checks that it becomes the refusal.

The capstone has no sampled evaluation, no scheduled evaluation and no alert. Its workflow runs on pull
requests, on pushes to `main` and on request. Everything in this lesson beyond the harness is a
decision it leaves to the reader.

## Design guidance

- **Decide where the failure lived**, then put the test in the live set or in an offline test.
- **Keep the user's words and drop the user.** Redact names and identifiers before a transcript becomes a case ({{topic:tracing}}).
- **Make the case, its replay script, its baseline entry and the Action dataset one reviewed change.**
- **Schedule a run**, because only a schedule notices a platform change.
- **Grade a sample of live traffic** if the platform offers it, and read the failures as you would a complaint.
- **Set alerts on the thresholds the agent was released against**, not on new ones.
- **Take transcripts inside their retention window.**

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The new case passes offline forever | The replay script holds a good turn | Put model failures in the live set and code failures in offline tests |
| A new case never blocks anything | It is not in the baseline | Update the baseline in the same change |
| The offline run fails on the new case | No replay script for its id | Add the script |
| The release report disagrees with the set | `action_dataset.json` was not regenerated | Run the generator |
| Quality dropped and nothing deployed | The model or platform changed, and no run is scheduled | Add a scheduled evaluation |
| A person's name sits in the repository | A transcript was pasted whole | Redact before it becomes a case |

## Key terms

**Continuous evaluation** — grading a sampled share of production traffic as it arrives.

**Scheduled evaluation** — re-running a fixed dataset on a timetable to detect drift.

**Replay script** — the scripted model turn an offline run uses in place of a real model.

**Where the failure lived** — the layer that produced a fault: the model, or your code, tools and data.
