## TL;DR

Agent Framework's evaluation is three types and one function. An `EvalItem` is one interaction, an
evaluator scores items, and `EvalResults` holds the counts and the per-item detail. `evaluate_agent`
runs your agent once per query and hands the batch to each evaluator you give it. Two kinds of
evaluator mix in one call: `LocalEvaluator` runs functions you write, with no model call, and
`FoundryEvals` calls Foundry's judges. This is the runner and most of the graders that
{{topic:evalharness}} said the framework supplies. The page documents the aggregate result well and
the per-case result lightly, and a harness that gates case by case has to read the second.

## Why it matters

{{topic:evalharness}} split a harness into a dataset, a runner, graders and a report, and left the
runner and graders to this lesson. The framework earns its place because of how {{topic:maf}} told you
to build the agent: the client is a parameter, so the same agent runs against a scripted model in CI
and the real one in a live run, and evaluation attaches from the outside. You do not rewrite the agent
to evaluate it. You do need to know which part of a run each grader can see, because a check can only
decide what the run recorded.

## How it works

### Three types, one function

| Type | Purpose |
|---|---|
| `EvalItem` | "A single item to evaluate", the full conversation, with query and response derived by a split strategy |
| `Evaluator` | "A provider that scores items": local checks, Foundry, or your own |
| `EvalResults` | Pass and fail counts, per-item detail and optional portal links |

In Python these live in the core `agent_framework` package, evaluators follow an `Evaluator` protocol,
and `evaluate_agent()` and `evaluate_workflow()` orchestrate. .NET builds on
`Microsoft.Extensions.AI.Evaluation` with its own method names. The course shows Python only.

### Local checks

`LocalEvaluator` "runs checks locally without API calls", which the page recommends for inner-loop
development and CI smoke tests. Four checks ship with it.

| Check | Passes when |
|---|---|
| `keyword_check(*keywords)` | The response contains all of them |
| `tool_called_check(*names)` | The agent called those tools |
| `tool_calls_present` | Every expected call's name appears, "unordered, extras OK" |
| `tool_call_args_match` | Expected calls match on name and arguments, as a subset |

Your own check is a function with the `@evaluator` decorator. Its parameter names decide what it
receives: `query`, `response`, `expected_output`, `expected_tool_calls`, `conversation`, `tools` and
`context`. It may return a `bool`, a `float` where 0.5 or more passes, a dict with `score` or `passed`,
or a `CheckResult`, and async functions work as they are.

### Judges in the same call

`FoundryEvals` is "cloud-based LLM-as-judge evaluation", with results in the Foundry portal. It runs
relevance, coherence and task adherence by default and adds tool call accuracy when items carry tool
definitions. The page lists constants for the agent, tool, quality and safety evaluators, and needs a
Foundry project with a model deployment, which "specifies which model to use as the LLM judge". The
catalog is {{topic:foundryevals}}, and what a judge can and cannot be trusted with is
{{topic:llmjudge}}.

### Running it

`evaluate_agent` "runs the agent once per query, converts each interaction to an `EvalItem`, and passes
the batch to the evaluator". It returns one `EvalResults` per evaluator provider, so a local and a
Foundry evaluator in one call give two. The arguments that matter:

- **`expected_output`** is paired with queries by position, and **`expected_tool_calls`** takes
  `ExpectedToolCall(name, arguments)` for each.
- **`num_repetitions`** runs each query several times, "to detect non-deterministic behavior".
- **`responses=`** evaluates answers you already have, from logs or an earlier run, without calling
  the agent again. The response keeps schema-only snapshots of the tools it saw, and `tools=` overrides
  them.
- **`conversation_split`** decides which half is the query. The default splits at the last user
  message, `FULL` takes the first message as the query and everything after as the response, and a
  custom splitter is any callable. `EvalItem.per_turn_items` builds items that score each exchange
  with cumulative context.

For a workflow, `evaluate_workflow` evaluates each sub-agent and the final output, with the per-agent
counts in `sub_results`.

## In practice at Technik

The capstone's graders are one custom check and two built-in ones. `facts_present` reads each case's
`must_include` list from the dataset, where `"a|b"` accepts either wording.

*From [`evals/run.py`, lines 32–38](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/evals/run.py#L32-L38):*

```python
@evaluator
def facts_present(query: str, response: str) -> CheckResult:
    """Every must_include entry appears in the answer; "a|b" accepts either wording."""
    missing = [want for want in BY_QUERY[query]["must_include"]
               if not any(alt.lower() in response.lower() for alt in want.split("|"))]
    return CheckResult(passed=not missing, check_name="facts_present",
                       reason=f"missing {missing}" if missing else "all facts present")
```

The reason string is what makes a red case readable in the report. The run itself is one call.

*From [`evals/run.py`, lines 55–73](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/evals/run.py#L55-L73):*

```python
async def run(offline, scripts=None):
    graders = [LocalEvaluator(tool_calls_present, tool_call_args_match, facts_present)]
    if offline:
        client = ReplayChatClient(scripts, function_invocation_configuration=TOOL_LOOP)
        server = teamcenter_server(args=("run", "--directory", str(ROOT), "tests/fake_server.py"))
    else:
        from agent_framework.foundry import FoundryChatClient, FoundryEvals
        from azure.identity.aio import AzureCliCredential
        client = FoundryChatClient(credential=AzureCliCredential(), function_invocation_configuration=TOOL_LOOP)
        server = teamcenter_server()
        graders.append(FoundryEvals(client=client, evaluators=[
            FoundryEvals.INTENT_RESOLUTION, FoundryEvals.TASK_ADHERENCE, FoundryEvals.TOOL_CALL_ACCURACY]))
    async with server:
        return await evaluate_agent(
            agent=build_agent(client, server), queries=[c["query"] for c in CASES],
            expected_output=[c["ground_truth"] for c in CASES],
            expected_tool_calls=[[ExpectedToolCall(t["name"], t["arguments"]) for t in c["expected_tool_calls"]]
                                 for c in CASES],
            evaluators=graders, eval_name="technik-production-assistant")
```

The offline branch swaps the model for a replayed one and the server for a fake. The live branch adds
three judges to the same list. The agent and the `evaluate_agent` call are identical either way.

The page shows `raise_for_status()` as the way to fail on any failed item. The capstone cannot use it,
because `rev-03` fails on purpose, so `outcomes` reads each provider's `items` instead and groups them
by case. The page's concepts table promises "per-item detail", and the attributes read here (`is_passed`,
`is_error`, `input_text`, `scores`) are not on it. The offline tests exercise them against real local
results.

<!-- unknown since=2026-11 -->
The page constructs `FoundryEvals` with `project_client` and `model`. The capstone passes the agent's
own chat client as `client`, and passes an `eval_name` to `evaluate_agent` that the page never shows.
The live branch never ran. The library also raised an `ExperimentalWarning` on the evaluation API, and
the page carries no preview label.
<!-- /unknown -->

<!-- unknown since=2026-11 -->
`op-01` expects two tool calls, the second needing the document number the first returns. Both
`tool_calls_present` and `tool_call_args_match` are documented by name and arguments, and the first is
documented as unordered with extras allowed. Nothing documents whether the second checks order, so the
capstone does not check it. The capstone also never sets `num_repetitions`, and nothing tests how
`outcomes` treats three items for one case. Reading the code, a case passes only if every repetition does.
<!-- /unknown -->

## Design guidance

- **Make the agent a function of its client**, so one agent runs against a replay and a real model.
- **Give every custom check a reason.** A `CheckResult` with a reason is a diagnosis. A bare `False` is a number.
- **Read results per case**, not as a pass count, whenever a known failure sits in the set.
- **Check order yourself** with a custom evaluator over `conversation` when order is the requirement.
- **Evaluate logged responses with `responses=`** before building a second runner for production.
- **Choose the split for the question**: last turn for an answer, full for a task, per turn for a drift.
- **Pin the framework version.** The evaluation API warns that it is experimental.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Every check passes and the answer is wrong | A check decides only what its assertion names | Assert the fact, not just that a tool ran |
| A tool check passes with calls in the wrong order | `tool_calls_present` is unordered and allows extras | Write an ordering check |
| The gate fails on a case that fails on purpose | `raise_for_status()` raises on any failed item | Read the items and compare with a baseline |
| A multi-turn score grades the wrong turn | The default split is the last user message | Choose the split that matches the question |
| Logged responses raise `ValueError` | One tool name appeared with two input schemas | Use distinct names, split the segments or pass `tools=` |
| A framework upgrade breaks the runner | The evaluation API is experimental | Pin the version and read its warnings |

## Key terms

**`EvalItem`** — one interaction to score, holding the whole conversation.

**`LocalEvaluator`** — a set of checks that run in the process, with no model call.

**`EvalResults`** — what one evaluator provider returned for a run: counts and per-item detail.

**Split strategy** — the rule that divides a conversation into the query and the response a grader sees.
