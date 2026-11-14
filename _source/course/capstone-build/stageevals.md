## TL;DR

Stage 4 turns the eight cases you committed in stage 1 into a run that grades the agent and blocks a change that
makes it worse. Three code checks grade every case. A replayed model and the fake Snowflake make the run work with no
account, so a workflow can run it on every pull request. A committed baseline says which cases passed last time,
and only a regression against it fails the run. One case, `rev-03`, fails on purpose, and it fails in every report
without blocking anything. You finish with a report that compares against the baseline and a gate that exits 1 when
a case that used to pass stops passing.

## Why it matters

Stage 3's guard catches an answer no tool backed. It cannot catch an answer a tool backed and the model got wrong,
and that is the failure that matters most here, because a planner will build to it. Only a grader that reads the
answer can see it, so the set needs a case that proves one does.

Be clear what the offline run is. It replays one fixed model turn per case, so it tests the harness: the cases,
the graders, the guard, the baseline and the workflow. It says nothing about how a model will behave. That is the
live run's job, and no one has run it for you ({{topic:buildsetup}}).

## How it works

### Three checks, plus judges when live

`evals/run.py` runs every case through the agent with Agent Framework's `evaluate_agent`. Three code checks always
grade it: `tool_calls_present` and `tool_call_args_match` compare the calls with the case's `expected_tool_calls`,
and `facts_present` checks that each `must_include` entry appears in the answer, where `"a|b"` accepts either
wording ({{topic:mafeval}}). In a live run Foundry's intent resolution, task adherence and tool call accuracy judges
are added ({{topic:foundryevals}}). A case passes only if every grader passes it.

### Replay the model

*From [`evals/replay.jsonl`, line 3](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/evals/replay.jsonl#L3):*

```json
{"id": "rev-03", "calls": [["get_revision_status", {"item_no": "SWI70000318", "revision": "C"}]], "answer": "Yes. Revision C of SWI70000318 (Cladding Preparation and Inspection) is the latest one, so use it.", "wrong_on_purpose": "It reads the tool result and still calls an unreleased revision current. The refusal guard lets it through, because a tool result backs the answer, so only the graders can catch it."}
```

Each line is one plausible model turn: the calls it makes and the answer it gives. A `ReplayChatClient` picks the line
by the question, and the real tool loop runs it against the real server over the fake Snowflake. Run it from
`agent/`:

```powershell
cd agent
uv run ../evals/run.py --offline
```

*From a run of that command at the tag, against its own baseline:*

```text
## Evals: offline

**7/8 pass** (baseline 7/8). No regressions.

| Case | Category | Baseline | Now | Why it failed |
|---|---|---|---|---|
| rev-01 | happy path | pass | pass |  |
| rev-02 | happy path | pass | pass |  |
| rev-03 | trap | fail | fail | facts_present: missing ['rev B|revision B', 'not released|in work'] |
| doc-01 | happy path | pass | pass |  |
| doc-02 | abstain | pass | pass |  |
| op-01 | happy path | pass | pass |  |
| abstain-01 | abstain | pass | pass |  |
| scope-01 | out of scope | pass | pass |  |
```

The report goes to `evals/report.md`, which is gitignored, to the workflow's run summary and to an uploaded artifact.

### The case that fails on purpose

Read `rev-03` against that table. The replayed model checked the revision, was told revision C is not released, and
answered that it is the one to use. The guard passes it, since a tool result backs it. The two tool-call checks pass,
because the right tool ran with the right arguments. Only `facts_present` fails, and the capstone's own test asserts
exactly that. *From [`agent/tests/test_evals.py`, lines 29–33](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/agent/tests/test_evals.py#L29-L33):*

```python
def test_the_case_that_fails_on_purpose_is_caught_by_the_grader_not_the_guard():
    found = evals.outcomes(asyncio.run(evals.run(offline=True)))
    assert baseline()["rev-03"] == "fail" and found["rev-03"]["status"] == "fail"
    # The answer was backed by a tool call with the right arguments; only the facts were wrong.
    assert [why.split(":")[0] for why in found["rev-03"]["why"]] == ["facts_present"]
```

A set that always passes cannot show that its graders work. Keeping one failing case means the report can still go red,
and a reader who sees red knows the harness is alive. A real failure would be a second red row, and the baseline is what
tells the two apart.

### The baseline, and what blocks

*From [`evals/baseline.json`, lines 1–12](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/evals/baseline.json#L1-L12):*

```json
{
  "offline": {
    "rev-01": "pass",
    "rev-02": "pass",
    "rev-03": "fail",
    "doc-01": "pass",
    "doc-02": "pass",
    "op-01": "pass",
    "abstain-01": "pass",
    "scope-01": "pass"
  }
}
```

A regression is a case the baseline passes that this run does not. A case that fails in the baseline cannot regress,
so `rev-03` blocks nothing, and a case missing from the baseline shows as `new`. The baseline is keyed by mode, so
the live run keeps its own. It has none at first. With an empty baseline nothing can regress, so run
`uv run ../evals/run.py --update-baseline` once, read the report, and commit the file. That commit is the thing a
reviewer approves, and it belongs in its own pull request, apart from the change it measures ({{topic:cicd}}).

### The gate

*From [`.github/workflows/evals.yml`, lines 16–39](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/.github/workflows/evals.yml#L16-L39):*

```yaml
jobs:
  offline:
    # The replayed model and the fake Snowflake: no account, no secrets, the same result every run.
    runs-on: ubuntu-latest
    env:
      UV_LOCKED: "1"
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v10.3.0
        with:
          version: "0.11.26"
      - name: Server and deployment file tests
        run: uv run pytest
      - name: Agent and runner tests
        working-directory: agent
        run: uv run pytest
      - name: Evals against the baseline
        working-directory: agent
        run: uv run ../evals/run.py --offline
      - uses: actions/upload-artifact@v7
        if: always()
        with:
          name: eval-report-offline
          path: evals/report.md
```

The job runs both test suites, then the evals, and `run.py` exits 1 on a regression. A separate `live` job, off until the
repository variable `EVALS_LIVE` is `true`, runs the same command against the Foundry model and real Snowflake. Its
variables and its one secret are listed in the capstone's README, and the sign-in is covered with the release workflow
in {{topic:cicd}}. A workflow only produces a result. Making it block a merge is a repository setting no file contains.

## In practice at Technik

You finish holding the report above, a baseline file you have read case by case, and a workflow that ran on your pull
request. Then do the check that proves the gate is real. In your copy of `replay.jsonl`, change `rev-01` to an answer
with no tool calls, run the evals, and watch it fail: the guard replaces the answer with the refusal, the facts go
missing and the report names `rev-01` as a regression. The capstone's own suite does the same in
`test_an_answer_from_memory_is_a_regression`. Put the line back afterwards.

## Design guidance

- **Keep one case that fails on purpose**, so the report can be red and the graders are shown to work.
- **Grade what the answer says as well as what the agent did.** A tool-backed answer can still be wrong.
- **Block on regression against a baseline**, not on a perfect score.
- **Commit the baseline, and change it in its own pull request.**
- **Say what offline cannot tell you.** A replay tests the harness and not the model.
- **Make it the cheap run on every change**, and keep the live run for a schedule or a release.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The first live run reports no regressions | There is no live baseline, so nothing can regress | Run `--update-baseline` once, read it, and commit it |
| A correct answer fails `facts_present` | It used wording the case does not list | Add the wording as another alternative in that `must_include` entry, if it is truly correct |
| `rev-03` turns green | The replay or the instructions changed and the case no longer tests the trap | Treat it as a changed test, and decide whether to keep a failing case |
| The set passes and the agent is still wrong live | The offline run replays fixed turns | Run live, and add the failure as a case |
| A test names `action_dataset.json` | The eval set changed and the Foundry dataset did not | Run `uv run ../evals/action_dataset.py` from `agent/` |
| A regression is merged anyway | The workflow runs, and the repository does not require it | Require the check in the branch rules ({{topic:ghharness}}) |

## Key terms

**Regression**: a case the baseline passes that this run does not.

**Baseline**: the committed per-case results a new run is compared against.

**Replay**: a stand-in model that plays one recorded turn per case.

**Known failure**: a case recorded as failing in the baseline, which is reported but never blocks.
