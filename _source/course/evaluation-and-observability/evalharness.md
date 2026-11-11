## TL;DR

An eval harness has four parts: a versioned dataset, a runner that calls the agent, graders, and a
report that compares the run with something. Where a platform ships one you configure it. Where you
write the agent in code you own it. Foundry gives you two pieces for a pipeline: a GitHub Action that
runs the evaluation and reports with statistics, and an Azure Developer CLI extension that fails the
build below a pass rate. Neither checks a case-by-case baseline you committed. For that you write the
comparison yourself, and the capstone's takes three lines.

## Why it matters

Four earlier lessons lean on this one. {{topic:lowvspro}} found that `wiqd agent eval` stops at the
declarative boundary, so a custom engine agent's harness is yours to build. {{topic:skilltest}}
found no product way to test what a skill produces, and sent that test to a harness you own.
{{topic:foundryagents}} found that a hosted agent has no canary, which makes the evaluation run the
only check before a version takes all the traffic. And {{topic:ghharness}} said a suite must stay
fast enough to delegate. All four assume the same thing: that fixed inputs, graded outputs and a
comparison run on every relevant change, without a person remembering to.

## How it works

### Four parts, in two places

| Part | What it is | Foundry's Action | The capstone |
|---|---|---|---|
| Dataset | A versioned file of cases | A JSON file: `name`, `evaluators`, and `data` with a `query` and optional fields such as `ground_truth` | `evals/eval_set.jsonl`, eight cases |
| Runner | Calls the agent for each case | "invokes your agents with the queries", by `agent-name:version` | `evaluate_agent` in `evals/run.py` |
| Graders | Code checks and judges | Any evaluator in the catalog, graders, or custom evaluators in Python or as a judge | Three code checks, plus three Foundry judges on a live run |
| Report | A comparison, not a score | Per-metric scores with confidence intervals, and for two agents a pairwise significance test | A table against `evals/baseline.json` |

The decomposition is this course's. The right-hand columns show it holds on both sides.

### What the Action gives you

The Action's inputs are five: the project endpoint, the judge model's deployment, the data file, one
or more `agent-ids`, and an optional `baseline-agent-id`. List two versions and it compares them,
with "confidence intervals and test for statistical significance to determine if changes are
meaningful and not due to random variation". That statistics layer is what a single pass rate cannot
give you for a nondeterministic agent. The page is marked preview, and it warns: "To minimize costs,
don't run evaluation on every commit."

<!-- unknown since=2026-11 -->
The Action's prerequisites say "a Foundry agent". The evaluate-agent page says an evaluation works
"against a Foundry agent or hosted agent". Neither Action page says its `agent-ids` accept a hosted
agent's version, which is how the capstone's release workflow uses it, and the capstone never ran live.
<!-- /unknown -->

The Action's input table has no threshold. It writes its report to the run summary, and the
documented inputs give it no way to stop a merge.

### What blocks: the azd gate

The same page documents a gate. The Azure Developer CLI evaluation extension registers an evaluation,
starts a run and then fails the job below a pass rate.

<!-- volatile verified=2026-11 -->
The commands are `azd ai eval run start`, then `azd ai eval run show <run-id> --eval <name> --wait
--fail-on pass-rate=0.8`. It needs `azd` 1.33.0 or later and the `azure.ai.evaluations` extension,
which the `microsoft.foundry` package does not include. Pass rate is "passed test cases divided by
total test cases", and failed, errored and skipped rows all count against it.
<!-- /volatile -->

Two details matter in a pipeline. The command exits 1 for a quality breach and for an operational
failure alike, because the CLI "collapses an extension's exit code". Only the message "evaluation
quality gate not met" separates them. And the identity is a federated credential with no client
secret, given Foundry User on the project and little else, in a protected `live-evaluation` environment that a
same-repository pull request can enter and a fork cannot. The page says the workflow "must not use
`pull_request_target`".

### Two questions a gate can ask

A pass-rate gate asks *is it good enough?* A baseline gate asks *is it no worse than before?* They
disagree more often than they sound. Suppose a set of eight has one case that fails on purpose, so
seven pass. A change breaks one passing case and happens to fix the failing one. The pass rate is
still 0.875 and an 0.8 gate stays green. A per-case baseline sees a case that passed and now does not.
Use the pass rate for the standard you hold the agent to, and the baseline for what moved. It
automates the case-by-case read {{topic:runeval}} taught by eye.

## In practice at Technik

The capstone writes its own comparison because its set holds a case that fails on purpose.

*From [`evals/run.py`, lines 89–91](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/evals/run.py#L89-L91):*

```python
def compare(found, baseline):
    """A regression is a case the baseline passes that this run doesn't."""
    return [case for case, then in baseline.items() if then == "pass" and found.get(case, {}).get("status") != "pass"]
```

`rev-03`, a tempting wrong answer, is recorded as a failure in `baseline.json`, so it is red in every
report and blocks nothing. The runner exits 1 only when this function returns a case. It also writes
the table to the run summary, which is the Action's job done by hand. Agent Framework supplies the
runner and most of the graders ({{topic:mafeval}}). The dataset, the baseline and this comparison
are Technik's.

The release workflow then uses the Action the way the page's inputs invite: the version being
replaced against the new one.

*From [`.github/workflows/release.yml`, lines 53–61](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/.github/workflows/release.yml#L53-L61):*

```yaml
      - name: Compare the new version with the one it replaced
        # Foundry's judges on the deployed agent, in the run summary. It reports; the gate above blocks.
        uses: microsoft/ai-agent-evals@v3-beta
        with:
          azure-ai-project-endpoint: ${{ env.PROJECT }}
          deployment-name: gpt-4.1-mini
          data-path: ${{ github.workspace }}/evals/action_dataset.json
          agent-ids: technik-production-assistant:${{ env.BEFORE }},technik-production-assistant:${{ env.AFTER }}
          baseline-agent-id: technik-production-assistant:${{ env.BEFORE }}
```

Two limits are worth saying plainly. The offline job that runs on every pull request replays a
scripted model against a fake Snowflake, so it returns the same result every time. That proves the
dataset loads, the runner calls the agent, the graders grade and the gate fires, and a test checks
that it catches `rev-03`. It cannot show that a real model's answers are good. That is the live job's
work, and the live job is off until a repository variable is set. And the live path runs each case
once, so a case that passes eight times in ten can trip the baseline gate on a bad draw. The
checklist's advice to run a set several times ({{topic:evalstrategy}}) is one the capstone does not
follow.

## Design guidance

- **Grade with code first.** A judge is for what a check cannot decide ({{topic:llmjudge}}).
- **Review the dataset and baseline like code.** A new baseline is a diff someone approves.
- **Split by cost.** A free deterministic job on every relevant change, a paid live run on a trigger.
- **Ask both gate questions.** A pass rate for the bar, a baseline for the movement.
- **Gate before the deploy** wherever the platform has no canary.
- **Keep the pipeline's identity small**, and out of reach of forks.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| CI is green and the agent got worse | The offline run replays the model | Treat it as a test of the harness, and schedule a live run |
| The Action's run is green after a drop | It reports; its inputs have no threshold | Gate with `--fail-on`, or compare against your own baseline |
| The job exits 1 and nobody knows why | One exit code for quality and operational failures | Read the message before the exit code |
| The pass rate holds and a case regressed | One case fixed, another broken | Compare case by case |
| The evaluation bill follows the commit count | Judges and agent calls run every time | Filter by path, and run live on a trigger |
| A fork's pull request reaches the cloud identity | No same-repository check, or `pull_request_target` | Skip forks in the job that holds the identity |

## Key terms

**Eval harness** — a dataset, a runner, graders and a report, run as one repeatable step.

**Baseline** — a committed record of what each case did last time, or an earlier agent version that
a new one is compared with.

**Quality gate** — a pipeline step that fails the build when the evaluation falls below a bar.

**Regression** — a case the baseline passed that the new run does not.
