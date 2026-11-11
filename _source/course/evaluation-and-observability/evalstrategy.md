## TL;DR

An evaluation strategy answers three questions before any harness exists: what you measure, when
you run it, and what a failure tells you. Microsoft's checklist gives four stages, from a small
"must pass" set to a continuous operation, and four categories of test, so that a red result points
at a cause rather than a number. Foundry adds a split between grading the outcome and grading the
steps. Neither source decides what "good" means for your agent. That part is yours, and it comes first.

## Why it matters

{{topic:runeval}} ended on a warning: a score says how many cases passed, not whether the agent is
finished. At pro-code scale the warning sharpens, because the things that change an agent multiply.
A prompt edit, a model swap, a new tool, a knowledge update and a compacted history each move the
answers ({{topic:budget}}, {{topic:history}}), and you do not pick when most of them arrive. A
strategy decides which change starts which run, so "did that break something?" gets a result.

## How it works

### Four stages

The agent evaluation checklist describes "an iterative process starting from the agent envisioning
and design phase". That is the source of *define metrics before you build*: the test prompts "should
be closely coordinated with the development of agent instructions".

| Stage | Goal | What you hold at the end |
|---|---|---|
| 1. Foundational set | Cover the core scenarios | One prompt per key scenario, each with acceptance criteria |
| 2. Baseline and improve | Run it, record it, fix | Pass or fail per case, the pass rate, the agent version, the date |
| 3. Systematic expansion | Broaden by quality category | Suites for robustness, architecture and edge cases |
| 4. Continuous operation | Hold quality as things change | A cadence, and triggers that start a full run |

### A case is more than a question

A test case is a prompt, "an optional expected response (assertion)", an acceptance criterion and a
test method. The criterion is the part people skip. The checklist's own example asks the same
question, how many sick leave days an employee gets, in two cases. One expects the policy answer with
a citation. The other expects a route to human HR, because that scenario is to stay inside the
policy article. The criterion tells the grader which behaviour the case is about.
{{topic:testsets}} and {{topic:advtests}} cover writing the questions. This lesson is about reading
what comes back.

### The baseline, and two places a failure can live

Stage 2 records a run; it does not chase a score. For each failure the checklist asks whether the
prompt, expected answer or criterion caused it, or whether it shows "unclear agent instruction, or
flaws in knowledge or tool configuration". It also names a result to distrust: a *false positive* is
"an answer marked as passing but should fail based on human judgment". Because "agents
can produce varying responses to the same prompt", it advises running each set several times and
averaging, aiming for "a realistic pass rate of 80-90%, based on your business needs". Foundry's
example is "an 85% task adherence passing rate", set before release.

### Four categories, four meanings of red

Stage 3 sorts suites by what a failure means.

| Category | Tests | When it fails |
|---|---|---|
| Foundational core | The "must pass" set | "Something is broken or isn't working. Investigate recent changes." |
| Robustness | The same intent in other words, rich context, several intents in one prompt | "Agent is too strict", overfocused on specific phrasings |
| Architecture | Tool calls, retrieval and citation, routing, handoffs | A specific component or workflow needs debugging |
| Edge cases | Boundaries, not-allowed and out-of-scope behaviour | Guardrails need improvement |

Intermediate sorted cases by scenario type. These sort by diagnosis. An 87% is the same number
whether the core suite or the edge suite lost the points, and only one sends you to the
instructions' boundaries.

### Outcome and steps

Foundry's agent evaluators split the question in two ({{topic:foundryevals}}). *System evaluation*
examines "the end-to-end outcomes"; *process evaluation* verifies "the step-by-step execution". An
agent can reach the right answer through the wrong tool, and it can call every tool correctly and
still misstate the result. A strategy that grades one half cannot tell those apart.

### What starts a run

Stage 4 lists the triggers for a full suite: "Model change", "Major knowledge setup update", "New
tool or connector integrations" and "Production incident", on top of a regular cadence. Its test of
success is a sentence you can say: compliance is at 98%, personalization fell to 87% because
tenure-based policies are not applied, and the cause is found.

<!-- unknown since=2026-11 -->
The two curated pages describe the pre-release half in detail and the production half in one line.
Foundry's evaluate-agent page says production monitoring uses "continuous evaluation" and links
elsewhere for setup, so this lesson does not teach it. {{topic:prodfeedback}} and {{topic:tracing}}
carry what the course can source.
<!-- /unknown -->

## In practice at Technik

The capstone's set has eight cases. Sorted by the checklist's categories ({{topic:stageevals}}):

| Category | Capstone cases |
|---|---|
| Foundational core | `rev-01`, `rev-02`, `doc-01` |
| Architecture | `op-01`, the one case that needs two tool calls in order |
| Edge cases | `rev-03`, a tempting wrong answer; `doc-02` and `abstain-01`, abstentions; `scope-01`, out of scope |
| Robustness | none |

Every question appears in one phrasing. A prompt change that overfits those eight sentences would
pass, which is the failure the robustness row exists to catch. The set is the right size to read in
a pull request and the wrong size to claim robustness. Before the next prompt change, add
rephrasings of `rev-01`, one with a typo and one asking two things at once, as a suite of their own.

Each case carries its acceptance criterion in the file: `ground_truth` says what a correct answer
contains, and `must_include` is the code check that enforces it. For `doc-02` the truth is the
refusal, word for word. And `evals/baseline.json` is stage 2 as a committed file, a pass or fail per
case. It records `rev-03` as a failure on purpose. The checklist's word for that is a *true
negative*, "an answer correctly identified as a failure", and keeping it in the baseline means a red
result in a later run is a change and not a constant.

*From [`.github/workflows/evals.yml`, lines 4–11](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/.github/workflows/evals.yml#L4-L11):*

```yaml
on:
  pull_request:
    paths: ["agent/**", "server/**", "evals/**", "seed/data/**", "tests/**", "infra/**", "azure.yaml",
            "pyproject.toml", "uv.lock", ".github/workflows/*.yml"]
  push:
    branches: [main]
  workflow_dispatch:
  workflow_call:  # stage 5: the release workflow runs this as its gate
```

Read it against stage 4. A new tool is `server/**`. A model change is `azure.yaml` or `agent/**`.
A knowledge update is `seed/data/**`. Nothing here is a schedule, and no path filter sees a model
that changes on the platform's side. {{topic:declarative}} made the same point about configured
agents: behaviour moves with no commit, so only a regular run notices.

## Design guidance

- **Write the acceptance criterion with the case**, not after the first failure.
- **Label each case with a category**, so a drop in score names its cause.
- **Give robustness its own suite.** One phrasing per question can never test it.
- **Keep known failures in the baseline**, marked, so that red means changed.
- **List your triggers.** Each of model, prompt, tool, knowledge and platform gets a path or a schedule.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The score is steady and users still complain | One phrasing per question, so nothing tests robustness | Add rephrasings, typos and multi-intent cases as a suite |
| A fix "didn't work" and the case still fails | The case was wrong: prompt, expected answer or criterion | Ask the checklist's first question before editing instructions |
| A score swings with no change | Nondeterminism, and one run | Run the set several times and compare averages |
| Behaviour changed with no commit | A model or platform update that no path filter sees | Add a scheduled run |
| The target is met, and the failing case mattered most | A pass rate weighs every case equally | Mark must-pass cases and block on each |

## Key terms

**Acceptance criterion** — the written statement of what passes and what does not for one case.

**Baseline** — a recorded pass or fail per case, tied to an agent version and a date, that later runs
are compared with.

**False positive / true negative** — a wrongly passed answer, and a correctly failed one.

**System and process evaluation** — grading the end-to-end outcome, and grading each step and tool
call that produced it.
