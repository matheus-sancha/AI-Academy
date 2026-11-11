## TL;DR

A judge is a model asked to score another model's answer. Foundry's AI-assisted evaluators all work
that way: they "use a judge model to score responses and can provide explanations". That makes a
judge the only grader that can read an open-ended answer, and the one with the most ways to be wrong.
Intermediate's {{topic:judge}} showed what a grader without an answer key cannot know. This lesson is
about owning one: pick the cheapest grader that can decide, write the rubric before the judge sees an
answer, and measure the judge against a person before its pass rate means anything. The two curated
pages say little about how judges fail, and the lesson says so where it matters.

## Why it matters

Every grader in {{topic:evalharness}} is cheaper and steadier than a judge, so a judge has to earn its
place. It earns it where no code can decide. The capstone's `abstain-01` expects the agent to say a
document does not exist. A check can find the words "no document" in the answer. It cannot tell
whether the next sentence invents a section number for the document. That gap is the judge's job, and
the judge brings its own errors, a bill, and a model version that can change under the pass rate.

## How it works

### A ladder of graders

Foundry's reference lists several graders for the same kind of question, which makes the trade-off
visible.

| Rung | Foundry examples | Decides | Cost and repeatability |
|---|---|---|---|
| Code check | String Checker, your own function | A pattern, a field, a tool call | Free, same answer every time |
| Overlap metric | F1, BLEU, ROUGE, METEOR | N-gram overlap with the ground truth | Cheap, blind to meaning |
| A service check | Groundedness Pro (preview) | Whether the answer is grounded, as pass or fail, "without requiring a model deployment" | Calls the Azure AI Content Safety service |
| A fixed-question judge | Groundedness, Similarity, Task Adherence | One quality, scored by a model; Groundedness returns "a score from 1–5" | A model call per case |
| Your own judge | Rubric (preview), Model Labeler, Model Scorer | Criteria and labels you write | A model call per case, and your design |

Groundedness appears twice, once as a model's judgement and once as a service's binary verdict. That is
the ladder in miniature. Climb it only as far as the question needs.

### What a judge hands back

An AI-assisted evaluator can return an explanation with its score, and the Rubric evaluator returns "a
weighted average score normalized to 0–1 with per-dimension reasoning". Pass or fail then comes from a
threshold ({{topic:foundryevals}}). The explanation is the same judge's account of its own score. Read
it to see what the judge saw, and check a sample of passes against the transcript.

### Writing the rubric

A rubric evaluator scores against "custom, weighted criteria". The craft is in the criteria, and it is
the same craft as an acceptance criterion ({{topic:evalstrategy}}): each one is a statement a person
could mark true or false from the answer alone. Weights say which failures matter. Equal weights let
a polite answer that invents a section number outscore a curt one that is right.

### Calibrating the judge

A pass rate from a judge is a measurement, and the instrument has to be checked. Have a person label a
sample, run the judge on the same answers, and put the two verdicts in a table. The number that
matters is not the overall agreement but the answers the judge passed and the person failed. Those are
the checklist's false positives ({{topic:evalstrategy}}), and each one is a criterion the rubric is
missing or a case that needs a code check.

<!-- unknown since=2026-11 -->
The roadmap lists three judge biases: a preference for its own style, for longer answers, and for an
answer by its position. Neither curated page names any of them, or says how to correct for one. The
calibration above does not depend on naming the cause. It finds disagreement wherever it comes from.
Neither page shows how a rubric is entered either.
<!-- /unknown -->

### What a judge costs

One judge cost arrives without anyone scheduling it.

<!-- volatile verified=2026-11 -->
"Evaluations in the agents playground are enabled by default for all Foundry projects and are included
in consumption-based billing." To turn them off, select metrics in the upper right of the agents
playground and unselect all evaluators.
<!-- /volatile -->

## In practice at Technik

`abstain-01` asks what `SWI70000381` says about weld prep. There is no such document, since the number
is a mishearing of `318`. Its `must_include` list accepts any of four phrasings of "not found" next to
the number, so an answer that says "No document `SWI70000381` was found. It covers weld prep in
section 4, where…" passes the check and fails a person. A rubric for it, weights being Technik's
choice:

| Criterion | Weight | True when |
|---|---|---|
| Says the document was not found | 0.4 | The answer states that no document `SWI70000381` exists in Teamcenter |
| Invents nothing about it | 0.4 | No section, limit or text is attributed to `SWI70000381` |
| Stays inside its tools | 0.2 | Any suggestion of `SWI70000318` is a question, not an answer given as if asked |

Suppose the document controller labels twenty answers to cases like it, and the judge scores the same
twenty.

| | Judge passes | Judge fails |
|---|---|---|
| **Person passes** | 11 | 1 |
| **Person fails** | 4 | 4 |

The judge passes 15 and the person 12, so the judge is generous by three, and the four answers in the
corner are the finding. Read them. If each invents a section number, the second criterion is too
loosely worded or the judge is not reading for it, and a code check for "section" next to the number
would catch them for free.

The capstone's live run keeps the code checks as the gate and adds three Foundry judges, Intent
Resolution, Task Adherence and Tool Call Accuracy, built on the agent's own chat client.

*From [`evals/run.py`, lines 65–66](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/evals/run.py#L65-L66):*

```python
        graders.append(FoundryEvals(client=client, evaluators=[
            FoundryEvals.INTENT_RESOLUTION, FoundryEvals.TASK_ADHERENCE, FoundryEvals.TOOL_CALL_ACCURACY]))
```

So the judge is the agent's own model deployment, because that is the one in reach. A separate judge
deployment would remove the question of a model grading itself, at the price of a second deployment
to pin. The capstone has no human labels, no calibration table and no rubric, and it never ran live.
Its judges report, and its code checks block.

## Design guidance

- **Climb the ladder only as far as the question needs.** Pattern, then overlap, then service, then judge.
- **Write the rubric before the first run**, as true-or-false criteria with weights.
- **Calibrate on a labelled sample** before a judge's pass rate is quoted, and read the false positives.
- **Fold every false positive back**: a sharper criterion, or a code check that makes the judge unnecessary.
- **Let the judge report and the code gate**, until the judge has a calibration table.
- **Pin the judge's model** and re-baseline when it moves ({{topic:foundryevals}}).
- **Decide whether the judge may be the agent's own deployment**, and write the decision down.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The judge passes what a person fails | A missing criterion, or a judge not reading for it | Calibrate, read the disagreements and add a code check |
| The pass rate moves and nothing in the agent did | The judge model or its version changed | Pin it, and re-baseline on purpose |
| A convincing reason beside a wrong verdict | The explanation comes from the same judge as the score | Check a sample of passes against the transcript |
| An evaluation bill nobody scheduled | Playground evaluations are on by default | Unselect the evaluators in the playground |
| An overlap metric fails a correct answer | It measures n-gram overlap, not meaning | Use a check on the fact, or a judge |

## Key terms

**Judge** — a model that scores another model's answer against a question or a rubric.

**Rubric** — weighted, true-or-false criteria a judge scores an answer against.

**Calibration** — comparing a judge's verdicts with a person's on the same answers, to learn where it differs.

**False positive** — an answer the judge passed and a person would fail.
