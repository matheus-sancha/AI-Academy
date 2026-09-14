## TL;DR

**Pre-training** teaches a model language from an enormous unlabelled corpus. **Instruction tuning**
and preference training turn that text predictor into something that follows requests. **Fine-tuning**
takes an already-trained model and trains it further on your own examples, to specialise its style,
its format or a narrow classification. Almost every business problem you will meet is solved by
prompting and grounding, not by training — but you need the vocabulary, because the question "should
we fine-tune this?" will be asked, and the answer is usually a well-argued no.

## Why it matters

"Train it on our data" is the most common suggestion from people outside the team, and it is
usually the wrong shape for the problem. It sounds like it would teach the model Technik's facts.
It would not: fine-tuning adjusts behaviour, not a retrievable store of facts, and the facts in
question change every day. Being able to explain that clearly, without dismissing the question, is a
genuinely useful skill.

The reverse mistake matters too. There are real fine-tuning cases, and refusing to consider any of
them is as unhelpful as proposing it for everything.

## How it works

**Pre-training.** Vast amounts of text, one objective: predict the next token. Enormously expensive,
done by model providers, not by you. The result is a model that has absorbed language and, along the
way, a great deal about the world, frozen as of a cut-off date.

**Instruction tuning.** A much smaller, curated set of instruction-and-response examples teaches the
model to behave like an assistant rather than continuing your text.

**Preference training.** People compare candidate responses and the model is adjusted towards the
preferred ones. This is where tone, helpfulness and refusal behaviour largely come from.

**Fine-tuning.** You take a released model and continue training it on your own examples. What it can
and cannot do is the crux:

| Fine-tuning is good at | Fine-tuning is bad at |
|---|---|
| Consistent output **format** without a long prompt | Teaching **facts** that change |
| A house **style** or tone | Making answers **citable** |
| Narrow **classification** with labelled history | Anything needing **fresh** data |
| Cutting prompt length, and so cost, at high volume | **Small** datasets — hundreds of examples, not tens |

Two properties decide most arguments. First, a fine-tuned model **cannot cite**, because it has no
source to point at — it has absorbed your examples into its parameters. Second, it is a **snapshot**:
the day the data changes, the model is stale, and updating it means another training run.

**Retrieval-augmented generation** is the alternative for facts, and the comparison is worth
memorising:

| | Fine-tuning | Grounding / RAG |
|---|---|---|
| Teaches | behaviour, style, format | facts, current content |
| Updates when data changes | retrain | immediately |
| Can cite sources | no | yes |
| Respects per-user permissions | no | yes |
| Cost to set up | high | moderate |
| Cost per request | lower (shorter prompts) | higher (passages in context) |

The permissions row decides more real projects than any other. Fine-tuning bakes whatever it was
trained on into a model every user shares. Retrieval can apply each user's own access rights at query
time.

## In practice at Technik

**Should Technik fine-tune a model on its controlled documents?** No. The documents are revised
continuously — `SWI70000318` is waiting on revision C right now — a fine-tuned model could not cite
the clause it used, and an engineer who cannot check the source will not trust the answer. This is a
grounding problem, and B6 solves it.

**Should Technik fine-tune to classify quality notifications?** Possibly, and A11 works through the
decision properly. The shape fits: a fixed taxonomy of defect types, years of labelled history, high
volume, no citation needed, and the mapping is a judgement about language rather than a fact that
changes. Even then the honest first step is to try a well-written prompt with a few examples and
measure it. Fine-tuning is what you reach for when prompting has been measured and found wanting —
not before.

**Should Technik fine-tune so the assistant writes notifications in the house format?** Probably not.
A skill containing the template and the rules does the same job (B8), costs nothing to change, and
can be read and reviewed by a human. Fine-tuning becomes attractive only if the prompt is long, the
volume is very high, and the token saving genuinely matters.

> [!NOTE]
> A useful order of escalation: **prompt → few-shot examples → grounding → skill or tool → fine-tune.**
> Work down it, and measure at each step. Most problems stop at grounding, and the ones that do not
> are much better understood by the time you get to the end.

## Design guidance

- **Reach for grounding first**, always, for anything factual.
- **Ask what would change if the data changed tomorrow.** If the answer is "we would retrain",
  fine-tuning is the wrong tool.
- **Ask whether the answer must be citable.** If yes, fine-tuning is out.
- **Ask who is allowed to see what.** Per-user permissions and fine-tuning do not mix.
- **Measure the prompt-based baseline before proposing training.** Without it you cannot show a
  benefit, and you will be asked to.
- **Budget for the data, not the training.** The expensive part of fine-tuning is assembling and
  cleaning consistent, correctly labelled examples. The training run is the easy bit.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| "Train it on our documents" is proposed as the plan | Fine-tuning is assumed to store facts | Explain the split: behaviour versus facts. Demonstrate a grounded answer with citations |
| A fine-tuned model gives outdated answers | It is a snapshot of its training data | Move facts to retrieval; keep fine-tuning for style and format |
| A fine-tuning run makes the model worse at everything else | Over-fitting to a narrow dataset | More varied data, fewer epochs, and a held-out evaluation set |
| The fine-tuned model cannot show where an answer came from | There is no source to point at, by construction | If citations are required, do not fine-tune |
| Fine-tuning is proposed to reduce hallucination | It reduces some, but the mechanism is unchanged | Ground it |
| Everyone can now see data they should not | Training data was baked into a shared model | Retrieval with per-user permissions instead |

## Key terms

**Pre-training** — learning language from a very large unlabelled corpus. Done by model providers.

**Instruction tuning** — teaching a text predictor to follow instructions.

**Preference training** — adjusting the model towards responses people prefer.

**Fine-tuning** — continuing training on your own examples to specialise behaviour.

**Base model** — the model you fine-tune from.

**Catastrophic forgetting** — losing general ability while over-specialising on a narrow dataset.

**Distillation** — training a smaller model to imitate a larger one, to cut cost and latency.
