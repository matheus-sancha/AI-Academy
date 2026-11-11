## What this module is for

Intermediate ran one evaluation by hand, in a product, graded by a model you could not choose. This
module takes the same work and makes it a system you own: a strategy that says what to measure and what
starts a run, a harness that runs it without a person remembering to, the graders inside it, and the
traces and production signals that show what the agent did once someone else was using it.

The idea that runs through all eight lessons is **a measurement is only as good as what it can see.**
A check decides what its assertion names. A judge sees what the conversation holds. A pass rate sees
the cases you wrote, in the phrasings you wrote them, and an offline run sees a scripted model. A trace
sees the agent and may not see the server behind it. Each lesson ends by saying what its instrument
cannot see, and the module's habit is to put a cheaper, steadier instrument in front of a dearer one
and to read the result case by case.

Expect the documentation to be uneven. Foundry's pages describe the pre-release half of evaluation in
detail and the production half in a line. Most of Foundry's system evaluators, its rubric evaluator and its custom evaluators are preview. Both
Copilot Studio pages describe the standard harness, not the one the Production Assistant is on. Where a
lesson could not source a claim, it says so in a *Not yet verified* block and does not guess.

## Before you start

From Intermediate, {{topic:whyeval}}, {{topic:testsets}} and {{topic:advtests}} are how a case is
written, {{topic:runeval}} is reading a run by eye, and {{topic:judge}} is what a grader with no answer
key cannot know. {{topic:analytics}} and {{topic:feedback}} are the Copilot Studio half of the last two
lessons here.

From this level, {{topic:maf}} built the agent that {{topic:mafeval}} evaluates, with its client as a
parameter. {{topic:foundryagents}} found that a hosted agent has no canary, which is why the evaluation
gate runs before the deploy. {{topic:lowvspro}} and {{topic:skilltest}} each found something a product
cannot test and sent it to the harness built here.

Nothing here needs to be run. The capstone repository is public and tested offline only
({{module:capstone-build}}), and the lessons that quote its code say what an offline run can and cannot
show.

Allow about two and a half hours.

## What you will be able to do

By the end of this module you should be able to:

- write an acceptance criterion with each case, label it with a category, and list what starts a run;
- describe an eval harness as a dataset, a runner, graders and a report, and say what a pipeline gate
  can and cannot ask;
- tell a pass-rate gate from a per-case baseline, and keep a known failure in the baseline so that red
  means changed;
- choose a Copilot Studio test method from the answer's shape, and know when the harness rules it out;
- pick Foundry evaluators by the question, outcome or step, and check each one's preview label and the
  tools it can read before it enters a gate;
- build an Agent Framework evaluation from local checks and judges in one call, and read results case by
  case;
- write a rubric, calibrate a judge against a person, and decide what a judge may gate;
- connect tracing, read a conversation in it, and decide who may read it;
- put a production failure into the harness as a case, and say where its test belongs.

## The thread through this module

The first four lessons are the instruments and the plan. {{topic:evalstrategy}} decides what to
measure, when to run it and what a failure means. {{topic:evalharness}} gives the parts and the two
questions a gate can ask. {{topic:csevaladv}} and {{topic:foundryevals}} are the two catalogs, the first
for Copilot Studio and the second for Foundry, and both turn out to have blind spots that depend on the
harness and the tools.

The second half puts them to use. {{topic:mafeval}} is the API that runs the graders and the one part of
the harness you do not write. {{topic:llmjudge}} is the grader you cannot trust until you have checked
it. {{topic:tracing}} is the record of one run, and {{topic:prodfeedback}} closes the loop by turning what
production shows into the next case. The capstone's {{topic:stageevals}} and {{topic:stageship}} are
where all of it lands, and {{topic:cicd}} is where a pipeline carries the gate.

## Self-check

<details>
<summary>1. The capstone's CI is green on a pull request that changes the agent's instructions. A colleague says that proves the change is safe. What does it prove?</summary>

That the harness works, and that the code around the model still behaves. The offline run replays a
scripted model against a fake Snowflake, so it returns the same result every time. It shows that the
dataset loads, the runner calls the agent, the graders grade and the gate fires. It cannot show that a
real model answers well under the new instructions. That is the live job's work, and the live job is
off until a repository variable is set ({{topic:evalharness}}).

Add that the green check compares each case with a baseline. A baseline that passes seven of eight is a
statement about the cases written, and every question appears in one phrasing, so an overfit prompt
would pass ({{topic:evalstrategy}}).
</details>

<details>
<summary>2. A teammate wants Copilot Studio's extra test methods, with a custom method that passes a correct refusal, for the Production Assistant. What do you check first, and what does the capstone do for the same case?</summary>

The harness first. The methods page describes the standard harness, and the Production Assistant is on
the GitHub Copilot harness, which offers one test method. The method you planned around may not exist
for it ({{topic:csevaladv}}).

For the capstone, the refusal case is a code check. `doc-02` expects the refusal word for word and calls
no tool, and `facts_present` enforces it. That runs offline, needs no model and gives the same answer
every time. A Foundry evaluator is the choice only for what no check can decide, and its preview label
and the tools it can read come first ({{topic:foundryevals}}).
</details>

<details>
<summary>3. The capstone cannot end its eval run with `raise_for_status()`. Why not, and what does it read instead?</summary>

Because `raise_for_status()` raises when any item failed, and `rev-03` is a case that fails on purpose.
The run would fail on the case that is meant to be red. Instead the capstone's `outcomes` reads each
provider's items, groups them by case, and `compare` flags only a case the baseline passed that this
run does not. The page documents the aggregate result and the concept of per-item detail, and not the
attributes the capstone reads, which its offline tests exercise ({{topic:mafeval}}).

The same check cannot enforce the order of `op-01`'s two tool calls. `tool_calls_present` is documented
as unordered and allowing extras, so order needs a check of its own ({{topic:mafeval}}).
</details>

<details>
<summary>4. You label twenty answers by hand and score the same twenty with a judge. The judge passes 15 and you pass 12. Is the judge fit to gate the build?</summary>

Not on that number. The overall agreement hides the direction. What matters is the answers the judge
passed and you failed, because each is a false positive the gate would let through. Read them. If they
share a fault, such as inventing a section number, either a criterion is missing or the judge is not
reading for it, and a code check for the fault is better than a better judge. Until a calibration table
exists the judge reports and the code checks gate, and the judge's model is pinned so that a change to
it is a change you chose ({{topic:llmjudge}}, {{topic:foundryevals}}).
</details>

<details>
<summary>5. A manufacturing engineer reports that the hosted assistant said revision C of a work instruction was usable. What do you open first, and where does the new test go?</summary>

The conversation in the Traces tab, from the Response ID in the report. The ordered tool calls show what
the agent asked, and the results show what it was told. If `get_revision_status` returned In Work and
the answer said yes, the fault is in the model, and the refusal guard let it through because a tool
result backed it ({{topic:tracing}}).

A model failure goes in the live set as a new case in the engineer's wording, without the engineer. It
needs its replay script, a baseline entry and a regenerated release dataset in one reviewed change. A
code failure would be an offline test with a scripted bad turn instead. Remember that the trace holds
tool results, document owners' names included, so redact before the question becomes a case, and keep
the reader role to named people ({{topic:prodfeedback}}, {{topic:tracing}}).
</details>
