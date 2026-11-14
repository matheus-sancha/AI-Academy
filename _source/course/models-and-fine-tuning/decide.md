## TL;DR

Microsoft calls prompt engineering, RAG and fine-tuning "not mutually exclusive but … complementary", so *which one?* is the wrong question. Ask what the failing cases need, and answer it with an experiment: fix an evaluation set and a pass mark, score the best prompt, read the failures, add one technique, score the same set again, and price what the addition costs per request. The pages put prompt engineering first and call fine-tuning an advanced capability, and they disagree about whether it can teach facts, so that part is a test and not a rule. At Technik's volume, the quality-notification classifier fails the cost test before it reaches the quality one.

## Why it matters

{{topic:training}} gave you the escalation order and a table of what each technique is good at. Both are arguments, and an argument loses to "we tried it, and here are the numbers". This lesson turns the order into an experiment you can run, repeat when the model changes, and defend to the person paying for the hosting.

## How it works

### What each page says each technique is for

The classic customisation page calls **prompt engineering** "the starting point". **RAG** grounds answers in private or recent data and reduces fabrication. **Fine-tuning** adapts a model "to improve performance, teach the model new skills, or reduce latency", and the page's good cases are steering style, tone or format, and tasks whose steering information is too long for the prompt window. The current overview adds that it can improve tool use and the use of retrieved context. It also says "held-out evaluation helps you compare the fine-tuned model with your baseline."

### Where the pages disagree about facts

The classic page says fine-tuning "enhances LLM with after-cutoff-date knowledge and/or domain specific knowledge". It also sends questions about recent or private data to RAG. The current overview says fine-tuning "doesn't replace retrieval for current information". The Intermediate lesson argued from mechanism: a fine-tuned model cannot cite, it is a snapshot, and it is shared by every user. Those are good arguments, and no curated page makes them.

<!-- unknown since=2026-11 -->
No curated page measures how well a fine-tuned model recalls a fact it saw in training, or says fine-tuning fails to learn facts "reliably". Test it instead of asserting it: hold out questions whose answers changed after the training data was cut, and score a fine-tuned model on them.
<!-- /unknown -->

The rule that survives either reading is about the answer. If it must be current, citable or limited by who may see it, it needs retrieval, whatever a fine-tune could recall.

### The experiment

1. **Write the evaluation set and the pass mark first** ({{topic:evalstrategy}}). Keep a part of it as a final test that nothing is ever tuned against.
2. **Score the baseline.** The classic page: "Having a baseline for performance without fine-tuning is essential", because "fine-tuning with bad data makes the base model worse", and without a baseline you cannot see it. The baseline is the best prompt you can write, examples included.
3. **Read the failures and sort them by cause.** Missing or stale knowledge points to retrieval. A wrong format or inconsistent style points to the prompt, structured output ({{topic:structured}}) and examples. Labels people disagree on point to the task, which no technique fixes. Only what is left is a candidate for training.
4. **Add one technique and score the same set again.**
5. **Price it per request.**
6. **Repeat when the model, the data or the prompt changes** ({{topic:modellifecycle}}).

### What it costs

The classic page names two ways fine-tuning cuts cost: fewer tokens per task, and a smaller model that matches a larger one on one task. Against that stand an upfront training cost and an hourly charge to host the deployed model. The current page says a Standard deployment bills per token plus "applicable fine-tuned-model hosting charges", while a **Developer** deployment has no hourly hosting fee, is for evaluation only, and lasts 24 hours. Score a candidate there before you commit to hosting it. For the other deployment types, see {{topic:deploytypes}}.

Neither page gives a price or a break-even point, so the saving is arithmetic you do yourself, in tokens first.

## In practice at Technik

The candidate is the classifier from {{topic:lifecycle}}: read a quality notification's description and fill its defect type, for reports and filters. The label is a reading and never a disposition, which belongs to the assigned quality engineer ({{topic:aisql}}). The figures below are invented for the example.

Say the two plants raise about 40 QNs a week, so three months of history holds about 520 closed QNs, each with a defect type a person chose. Technik's own pass mark, set by the quality lead, is agreement with an engineer on 95 of every 100 notifications. Hold 100 QNs back as the test set. That leaves 420 to train and tune on.

**Baseline.** Write a prompt that lists the six labels, includes a way to decline (`other`) and carries examples. Run it, or `AI_CLASSIFY` in Snowflake, which takes examples too. A label is right or wrong, so an exact-match check grades it and no judge is needed ({{topic:llmjudge}}).

**Failures.** Suppose a QN describing "gas pits in the overlay" comes back as `other`. That is vocabulary, and one more example in the prompt fixes it. Suppose `porosity` and `lack of fusion` are swapped on a dozen QNs where two engineers disagree. That is a taxonomy problem, so fix the definitions and relabel before any run.

**Cost.** Twelve examples of about 100 tokens put 1,200 tokens on every call. At about 173 notifications a month, that is roughly 208,000 tokens of overhead a month. A fine-tuned model with an empty prompt saves at most that, and the hosting charge is owed whether or not anyone asks. At Technik's volume, fine-tuning does not win on cost.

**Quality.** It could still win on accuracy, but only if the best prompt misses the pass mark. And 420 examples sit below the classic overview's guidance of 500 or more for production ({{topic:dataprep}}).

So the answer is *not yet*, and the experiment explains why. The method, thresholds and arithmetic are this course's position. The pages supply the baseline advice and the cost components.

## Design guidance

- **Write the evaluation set and the pass mark before any technique.**
- **Keep a final test set that nothing is tuned against.** Prompt tuning overfits too.
- **Sort the failures by cause.** Only the leftover is a case for fine-tuning.
- **Combine rather than choose.** Retrieval for what changes, training for how it is said.
- **Price a call, not a run.** Count tokens saved against the hosting charge.
- **Evaluate a candidate on a Developer deployment** before paying to host it.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| "97% accuracy", and nobody can say against what | No baseline was scored | Score the best prompt on the same set first |
| The fine-tune passes and the pilot disappoints | The prompt was tuned on the evaluation set | Keep a final test set no one has seen |
| The model is confidently wrong about this week's change | A fact that changes was put in training | Move it to retrieval and test recall of changed facts |
| The hosting bill outlives the pilot | A deployed fine-tune charges whether or not it is used | Evaluate on a Developer deployment, and delete what you do not use |
| Two engineers keep scoring the same QN differently | The labels, not the model, are inconsistent | Fix the taxonomy before comparing methods |

## Key terms

**Baseline**: the score of the best prompt-only approach on your evaluation set.

**Final test set**: examples kept out of training, validation and prompt tuning.

**Pass mark**: the score someone with authority agrees is good enough.

**Developer deployment**: a 24-hour, evaluation-only deployment type for fine-tuned models.
