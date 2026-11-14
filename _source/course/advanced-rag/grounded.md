## TL;DR

*Grounded* now means three things in this course, and a system has to know which one it is buying. A **presence** check
asks whether a source was used at all, which is what the capstone's guard does. An **agreement** check asks whether each
claim matches the source, which is what groundedness detection and Foundry's Groundedness evaluator do, using a model.
**Truth** is checked by nobody, since an answer can agree with a stale source. So enforce grounding in layers: instruct,
guard, detect and review. One date shapes the build. The runtime detection API retires on 30 April 2027, so the check
you rely on should be one you own.

## Why it matters

Stage 3 of the capstone replaces any answer no tool backed with a fixed refusal, and its own page says that the guard
checks a tool was used, which is not the same as the answer being right. `rev-03` is the proof. The agent reads a tool
result that says revision C is unreleased and still calls it the latest, and the guard lets it through
({{topic:stageagent}}). {{topic:contentsafety}} raised the same word problem from the safety side. This lesson is the
layer above the guard: how to check what an answer says against what it was given, and what to do with the verdict.

## How it works

### Four layers

| Layer | Its question | Catches | Misses |
|---|---|---|---|
| Instruct | Does the prompt say to answer from sources, cite and refuse? ({{topic:citations}}) | Most answers from memory | Whatever the model ignores, since a system message does not guarantee compliance ({{topic:sysprompt}}) |
| Guard | Did the run use a source? | An answer from memory | A source misread |
| Detect | Does each claim agree with the source? | A claim outside or against the source | A wrong source, and the judge's own errors |
| Review | Does a person agree? ({{topic:prodfeedback}}) | What the layers above pass | Scale |

### What the two Azure pages offer

<!-- volatile verified=2026-11 -->
Groundedness detection in Azure AI Content Safety takes the text, the grounding sources and, for question answering, the
query. It reports whether the text is ungrounded. A fast mode returns a binary verdict for online use, and a reasoning
mode explains each ungrounded segment, which the page recommends for development. You pick a domain, medical or generic,
and a task, summarisation or question answering. An optional correction feature, in preview, returns text rewritten to
match the sources. It is optimised for English, and the page's best practice is to use grounding sources taken straight
from official documentation and kept current. The page also says it retires on 30 April 2027, and suggests Foundry's
evaluation tooling or your own validation with a model or a system prompt.
<!-- /volatile -->

<!-- volatile verified=2026-11 -->
Foundry's Groundedness evaluator is a model judge. It scores how well a response sticks to its context from 1 to 5,
passes at a default threshold of 3, and returns a label and a reason. It needs the response and, recommended, the
context as one string, with chunks joined by a separator such as a blank line. The query is optional. For an agent it
can read the context from tool call results in the response, and supplying tool definitions helps. Groundedness Pro, in
preview, uses the Content Safety service and returns a strict true or false. Foundry frames groundedness as precision,
nothing in the answer outside the context, and completeness as recall ({{topic:rageval}}).
<!-- /volatile -->

<!-- unknown since=2026-11 -->
Foundry says Groundedness Pro uses the Content Safety service, and the Content Safety page says its groundedness
detection retires. Neither page says whether Groundedness Pro survives that date.
<!-- /unknown -->

### Flag, block or correct

A verdict changes nothing until code acts on it ({{topic:contentsafety}}). There are three actions. You can **flag**: log
it and let the answer through. You can **block**: replace the answer with a refusal, as the capstone's guard does. Or
you can **correct**, which is the preview feature. The page's own examples correct *5%* to *4.5%* from the source. For a
revision letter or a limit that someone will act on, this course's position is to block or send it to a person, because
a silent rewrite hides the very discrepancy an evaluation set exists to find.

<!-- volatile verified=2026-11 -->
*Adapted from the question-answering example on the groundedness detection page, for `SWI70000318` section 5.2:*

```json
{
  "domain": "Generic",
  "task": "QnA",
  "qna": { "query": "What is the largest indication allowed on a sealing surface?" },
  "text": "Up to 1.5 mm on sealing surfaces.",
  "groundingSources": [
    "5.2 Indications on sealing surfaces are acceptable up to 0.8 mm; on non-sealing surfaces, up to 1.5 mm."
  ]
}
```
<!-- /volatile -->

## In practice at Technik

An engineering agent answers from the chunk above, whose 0.8 mm and 1.5 mm are the scenario's invented figures. Four
answers show what each layer sees:

| Answer | Presence | Agreement | Truth |
|---|---|---|---|
| Up to 0.8 mm on sealing surfaces, 1.5 mm on the rest | Pass | Grounded | Right |
| Up to 1.5 mm on sealing surfaces | Pass | Ungrounded, the limits are swapped | Wrong |
| 0.8 mm, with exceptions in appendix B | Pass | Ungrounded, there is no appendix B | Wrong |
| The figure the Standards summary table gives, if revision C tightens section 5 and the table is not updated | Pass | Grounded in the summary | Wrong |

The first row passes everything. The last passes every automated check, because the source itself is stale. That is
{{topic:citations}}'s lagging summary again, and it is why the page's advice to keep sources current belongs in the
pipeline and not on a checklist.

The capstone holds the presence layer, which is the guard, and a hand-written check. Its live judges are intent
resolution, task adherence and tool call accuracy, and none is Groundedness. The offline run catches `rev-03` with a code
check that looks for *not released* or *in work*, which works only because someone wrote the facts the answer must include
({{topic:stageevals}}). So the capstone has no agreement layer. It was tested offline only ({{module:capstone-build}}).
Add one by running the Groundedness evaluator over the cases, with the tool results as the context.

<!-- unknown since=2026-11 -->
Nobody ran either service on Technik text. Whether a judge flags `rev-03`'s sentence, whether a threshold of 3 is the
right one for revision questions, and whether the evaluator reads the capstone's tool results as context are all
untested. Label a sample of answers by hand first, and compare ({{topic:llmjudge}}).
<!-- /unknown -->

## Design guidance

- **Say which grounded you mean**: presence, agreement or truth.
- **Layer the checks**, so each catches what the one before it passes.
- **Decide what a verdict does** before you wire it: flag, block or a person.
- **Do not auto-correct** a figure, a revision or an identifier that someone acts on.
- **Own a check** built on an evaluator or on your own judge, since the runtime API retires.
- **Keep sources current**, because agreement with a stale source passes.
- **Test your own language** against a service optimised for English.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A right answer became the refusal | No tool result was in the run, so the guard did its job | Fix the tool or the instruction, never the guard |
| A grounded answer is wrong | The source was stale or wrong | Add a correctness case, and retire the summary |
| A verdict changed nothing | No code acts on it | Wire flag, block or review |
| Detection stops working in 2027 | The API retires on 30 April 2027 | Move to evaluation tooling or your own judge |
| The same answer scores differently | A model judge is not deterministic | Use a threshold and several runs |
| A corrected answer hid a defect | Correction rewrote a figure silently | Block it, or send it to a person |

## Key terms

**Groundedness**: how well an answer's claims agree with the sources it was given.

**Grounding source**: the text an answer is checked against.

**Presence check**: a test that a source was used at all, blind to what the answer says.

**Correction**: a preview feature that rewrites ungrounded text to match its sources.
