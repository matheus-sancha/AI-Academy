## TL;DR

Copilot Studio's evaluation does more than one General quality run, in two places. In the product,
the standard harness offers seven more test methods, one of them a custom method you define with
instructions and labels. Beside it, the Copilot Agent Kit runs richer tests: multi-turn conversations
with critical and noncritical steps, plan validation, and attachment checks. The methods page says
outright that it describes the standard harness, and the Technik Production Assistant is not on it.
So this lesson is about choosing well when you are, and what the capstone does instead.

## Why it matters

{{topic:judge}} ended on a grader with no answer key: it cannot see your facts, and it can mark a
correct refusal down. The standard harness has methods that fix both, and they go unused
because General quality is the default and asks nothing of you. {{topic:testsets}} and
{{topic:runeval}} showed how to build and read a set. Here you choose how each case is graded.

## How it works

### The methods

<!-- volatile verified=2026-11 -->

| Method | Checks | You supply | Result |
|---|---|---|---|
| General quality | Quality against fixed criteria | Nothing | Scored out of 100% |
| Content safety | Harmful content, per content type | Content type and permitted level | Pass or fail |
| Compare meaning | Meaning against an expected answer | Pass score (default 50) and expected answers | Scored out of 100% |
| Tool use | Whether the expected tools or topics were used | Expected capabilities | Pass or fail |
| Keyword match | Whether the answer contains the keywords | Keywords, and *Any* or *All* | Pass or fail |
| Text similarity | Wording against an expected answer | Pass score and expected answers | Scored |
| Exact match | Character-for-character equality | Expected answers | Pass or fail |
| Custom | Your own criteria | A name, instructions and labels | The label's pass or fail |

<!-- /volatile -->

A set can use several methods. Content safety takes a severity threshold from level 0, "the
strictest", to level 7, which "allows graphic or extreme content to pass", with one method per
content type. It does not "guarantee that an agent is safe".

<!-- unknown since=2026-11 -->
The page contradicts itself on text similarity: its table says out of 100%, its text says a cosine
score "ranges from 0 to 1". Which scale the pass score uses is not stated, so check the field in
the product before choosing a value.
<!-- /unknown -->

### Match the method to the answer's shape

The page gives each method a job. Compare meaning is for an answer that "can be phrased in different
correct ways" but must carry the same meaning. Text similarity is for text that must match "exactly,
or almost exactly", such as a generated legal document, and it "is typically used alongside" Compare
meaning, since it cannot check meaning. Exact match suits "numbers, codes, or fixed phrases". Keyword
match checks that terms are present, not how the sentence is built. Tool use checks behaviour, not
text. The mistake is reaching for the strictest method because it feels rigorous. A rigorous check of the
wrong thing fails correct answers.

### Custom: the method for what the others cannot say

A custom method has instructions and labels. Good instructions "be goal oriented" and use headings
and bullets. Each label has a name, a description and a pass or fail assignment, and you add at least
two, as in the page's *Compliant* and *Non-Compliant*.

Its main use is the refusal. General quality's abstention criterion asks whether the agent attempted
an answer, so a correct refusal can be flagged. The page's remedy is a custom method whose labels
define the expected refusal.

### The Agent Kit's test types

<!-- volatile verified=2026-11 -->

| Test type | Checks | Needs |
|---|---|---|
| Response Match | The reply against an expected one, by an operator such as equals or contains | An expected response |
| Attachments | The attachment JSON, such as an Adaptive Card | Expected JSON; an "AI Validation" operator exists |
| Topic Match | That the expected topic fired | Dataverse enrichment |
| Generative Answers | A generated answer against a sample or instructions | AI Builder enrichment |
| Multi-turn | Child tests run in one conversation, in order | Child tests, each with an order and a criticality |
| Plan Validation | That the dynamic plan included the expected tools | Expected tools and a pass threshold |

<!-- /volatile -->

Two of these change how you write cases. In a multi-turn test a failed *critical* child stops the run
and fails it. *Noncritical* children "feed" information to the agent, so later steps have something
to act on. Plan Validation is "a deterministic test" of the share of expected tools present in the
plan. Extra tools "don't affect the test result", so it shows that the agent reached for what it
needed and never that it stayed away from the rest. Topic Match, Generative
Answers and Plan Validation are all evaluated after the run, as enrichment steps.

<!-- unknown since=2026-11 -->
Neither page documents generating cases from analytics, or starting a run through an API or a
connector. The kit page does not say which harness its tests target, or whether they can test an
agent on the GitHub Copilot harness. {{topic:agentkit}} covers the kit as a product.
<!-- /unknown -->

## In practice at Technik

The Production Assistant is on the GitHub Copilot harness, so none of the tables above reaches it.
Take its work-order capability built as a standard-harness design, an illustration in the scenario's
sense. Each case gets the method that fits its answer.

| Case | Method | Why |
|---|---|---|
| "What's the status of work order `100004521`?" | Keyword match, *All*: `0020`, `300001234` | A correct answer names the blocked operation and the open QN, however worded |
| "wo 100004521 whats blocking it" | Plan Validation: the work-order tool and the QN tool, threshold 100% | "Blocked" joins the two, so a plan with one cannot be right |
| That question, after "Status of 100004521?" | Multi-turn, the first step noncritical | The second turn needs the first |
| "Draft revision C of `SWI70000318` and submit it." | Custom: *Declined and named the owner* passes; *Declined only* and *Attempted* fail | General quality would flag the refusal |

The capstone makes the same choices in code, because its agent is not a Copilot Studio agent
({{topic:stageevals}}). `must_include` is Keyword match with alternatives, `expected_tool_calls` is
Plan Validation, and `scope-01` is the custom refusal. One check goes past the documented ones:
`tool_call_args_match` also compares each call's arguments, which neither the Tool use method nor
Plan Validation does. An agent that calls the right tool with revision D instead of C
would satisfy both product checks, as the pages describe them, and fail the capstone's.

## Design guidance

- **Pick the method from the answer's shape**, and say why in the case.
- **Combine methods**: one for what the answer says, one for how it got there.
- **Give every refusal a custom method**, with labels that define the right one.
- **Mark feeding turns noncritical**, and the asserting turn critical.
- **Read a Plan Validation pass as recall.** It never penalises an extra tool.
- **Check the harness before planning around a method.** These pages describe the standard one.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A correct refusal scores low | General quality's abstention criterion | A custom method with a refusal label |
| One method shows *Invalid* on some cases | They lack its expected answers, keywords or tools | Fill the field for every case, or drop the method |
| A correct, reworded answer fails | Text similarity compares wording | Pair it with Compare meaning, or use Compare meaning alone |
| A multi-turn test ends at step one | A critical child failed | Mark steps that only feed information noncritical |
| Topic Match is not offered | It exists only when Dataverse enrichment is configured | Configure the enrichment first |

## Key terms

**Test method** — how a set grades its cases: a judgement, a comparison or a check.

**Custom method** — a test method defined by instructions and labels, each label passing or failing.

**Plan Validation** — a deterministic check that the agent's dynamic plan included the expected tools.

**Criticality** — whether a failed child step stops a multi-turn test.
