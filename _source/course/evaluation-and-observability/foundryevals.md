## TL;DR

Foundry's built-in evaluators are grouped by what they grade: general quality, text similarity,
retrieval, safety, agent behaviour, and your own criteria. For an agent the split that matters is
the one {{topic:evalstrategy}} introduced. *System* evaluators grade the outcome, *process*
evaluators grade each tool call, and almost all of them are a model's judgement returned as pass or
fail against a threshold. Two things decide whether an evaluator is usable for you: its preview
label, and whether it can read the tools your agent calls.

## Why it matters

The strategy lesson said to grade the outcome and the steps. This lesson is the instruments. They
are not free: an AI-assisted evaluator is another model call per case and per evaluator, and Foundry
ships composites for that reason. They are also not uniformly mature, and a few cannot see the
tools some agents use. Choosing them by name from a long list is how a harness ends up grading with
something that is retired, in preview, or blind to its own agent.

## How it works

### The catalog

| Family | Examples | Grades |
|---|---|---|
| General purpose | Coherence, Fluency | Flow and readability |
| Textual similarity | Similarity, F1, BLEU, GLEU, ROUGE, METEOR | Overlap with a ground-truth answer |
| RAG | Retrieval, Document Retrieval, Groundedness, Relevance | Whether the right material was found and used |
| Risk and safety | Violence, Self-Harm, Indirect Attack, Prohibited Actions, Sensitive Data Leakage | Harm, and what an agent should never do |
| Agent | Task Adherence, Intent Resolution, Tool Call Accuracy | Below |
| Rubric (preview) | One evaluator | A response against weighted criteria you write |
| Graders | String Checker, Model Labeler, Model Scorer | Your own check or label |

Custom evaluators (preview) are the last resort: they "define unique scoring logic, validation
rules, and quality metrics". For an agent the page recommends combining "Output Quality + Tool Use
Quality + Rubric + Content Safety", with risk and safety evaluators added to everything.

### Outcome and steps

Agent evaluators "function like unit tests for agentic systems": they take agent messages and
return pass or fail, or a scaled score converted by a threshold.

| Kind | Evaluators | The question |
|---|---|---|
| System | Task Completion, Task Adherence, Intent Resolution, Task Navigation Efficiency, Customer Satisfaction | Did it finish the job, follow its rules, understand the request? |
| Process | Tool Call Accuracy, Tool Selection, Tool Input Accuracy, Tool Output Utilization, Tool Call Success | Right tool, right parameters, result understood, call succeeded? |

In a multi-agent system the system evaluators apply to "the main orchestrator or the final agent".
Task Navigation Efficiency needs expected steps as ground truth. Tool Input Accuracy is the strict
one, checking six criteria including type, format and "no unexpected parameters".

<!-- volatile verified=2026-11 -->
Two composites batch several evaluators into one judge call. Output Quality covers Fluency,
Coherence, Intent Resolution, Task Adherence, Groundedness and Task Completion. Tool Use Quality
covers the five process evaluators. The primary result "passes only when every applicable component
passes", a component that does not apply is skipped, and each component returns its own score and
reason, so a failure names its cause. They call for a judge model from the GPT-5.6 family, and the
page names `gpt-5.6-luna` as the lowest-cost option.
<!-- /volatile -->

Preview matters here. Four of the five system evaluators are marked preview and none of the process
evaluators is, and the page's warning applies: Microsoft "doesn't recommend it for production
workloads".

### Configuring one

An evaluator is a testing criterion: a name, the judge model, and a mapping from its inputs to your
dataset's fields.

*Adapted from the agent evaluators page's configuration sample:*

```python
testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "task_adherence",
        "evaluator_name": "builtin.task_adherence",
        "initialization_parameters": {"deployment_name": model_deployment},
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{item.response}}",
        },
    },
]
```

Evaluators that need the full interaction, such as Task Adherence and Tool Call Accuracy, read the
agent's structured output with its tool calls. Those that expect a string, such as Coherence, read
its plain text. Turn level grades each response and conversation level grades the whole exchange.
Conversation level needs the `messages` format, and it "skips turn-only evaluators".

### What an evaluator cannot read

The page lists the tools agent evaluators support: File Search, user-defined functions, MCP and
knowledge-based MCP. For Azure AI Search, Bing Grounding, SharePoint Grounding, Code Interpreter,
Fabric Data Agent and Web Search, support is "limited", and the page says to avoid four of the
process evaluators and Groundedness when a conversation includes them.

<!-- unknown since=2026-11 -->
The two curated pages disagree about Quality Grader. The reference lists it as a preview evaluator.
The agent evaluators page calls it deprecated and says it "can no longer be run in an evaluation".
This lesson follows the page that gives the specific answer, but the reference has not been checked
in a project.
<!-- /unknown -->

## In practice at Technik

On a live run the capstone adds three Foundry judges to its code checks: Intent Resolution and Task
Adherence, both system evaluators marked preview, and Tool Call Accuracy, a process evaluator that
is not. The offline job runs none of them, so by default no preview evaluator sits in the merge gate.
The live job adds them, and there an evaluator that errors counts against its case: `outcomes`
marks the case an error, and `compare` reads anything but a pass as a regression. The capstone's
tools reach it over MCP, which is on the supported list. An agent that took the Controlled Documents
library through SharePoint grounding would find its tool-call and Groundedness evaluators limited.

The domain rule lives in code. `facts_present` checks that each case's required facts appear in the
answer, such as the released revision's letter and the ECN. It could have been a Foundry custom
evaluator, which is a preview feature. A local check runs offline, needs no model and gives the same
answer every time.

<!-- unknown since=2026-11 -->
`rev-03` is the case that fails on purpose: the replay checks revision C, then calls it the one to
use although it is not released. The `facts_present` check fails it, and a test confirms that.
Tool Output Utilization measures whether the agent "correctly understood and used tool call results",
which describes this fault, but the capstone does not run it, and none of the three live judges was
observed on `rev-03`. The capstone never ran live.
<!-- /unknown -->

## Design guidance

- **Pick by the question.** Outcome failed: system evaluators. A step failed: process evaluators.
- **Put a check before a judge** wherever the answer is decidable.
- **Start from the composites** when cost matters, and read the components to diagnose.
- **Check the preview label and the tool list** before an evaluator enters a gate.
- **Treat a judge-model change as a change to the measurement.** Re-baseline when it moves.
- **Add the safety evaluators to every set**, as the catalog's combinations advise.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| An evaluator never reports on some runs | Conversation level skips turn-only evaluators | Use `messages` data, and check each evaluator's supported levels |
| Tool evaluators are unreliable on a search-based agent | Limited support for that tool | Leave those evaluators out, and grade with a code check |
| A composite fails with no obvious cause | It passes only if every applicable component does | Read the component reasons |
| Scores moved and nothing in the agent changed | The judge model or its version changed | Pin the judge, and re-baseline on purpose |
| A gate broke when an evaluator changed state | It was preview or deprecated | Gate on code checks, and let the judges report |

## Key terms

**System evaluation** — grading an agent's end-to-end outcome.

**Process evaluation** — grading each step, mainly each tool call and its use.

**Composite evaluator** — one judge call that returns several evaluators' scores.

**Evaluation level** — whether an evaluator scores a single turn or a whole conversation.
