## TL;DR

Distillation trains a smaller model on answers written by a larger one. Foundry has no separate method for it. The current overview lists it as "distillation through teacher-generated SFT data" under Managed Training, so a distilled model is an SFT job ({{topic:finetune}}) whose desired responses came from a teacher. The pitch is the overview's: a smaller model that meets requirements "at lower cost and latency", though benefits "aren't guaranteed". The catch is where the labels come from. A student learns only what the teacher says, so the test of whether it worked needs answers from people.

## How it works

<!-- volatile verified=2026-11 -->
The current overview names the idea twice: *Specialize a smaller model* is one of its six reasons to fine-tune, and *Distill a larger model* is an example use case for Managed Training. The classic page adds a model choice: for focused tasks such as classification, or "when distilling knowledge from a more sophisticated model", start with `gpt-4.1-mini`. Whichever student you pick must appear in the support table in {{topic:lifecycle}} for the method.

A synthetic-data page (preview) is the closest thing to a tool. A generator reads one reference file, a document under 20 MB or an OpenAPI specification, and writes 50 to 1,000 question-and-answer or tool-use examples with a model you choose, as JSONL ready for a job. That is new examples derived from a document, which is not the same as a teacher labelling your own inputs. The page advises starting small and mixing in real-world data.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
Neither page describes the procedure: collecting teacher answers, how many to keep, or filtering them. What follows is this course's position. Run representative inputs through the teacher, review a sample of its answers, write the rest as `messages` lines ({{topic:dataprep}}), train the student, and score both models on the same held-out set.
<!-- /unknown -->

A distilled model is still a fine-tuned model, with its training and hosting costs, its base's retirement clock ({{topic:modellifecycle}}) and the baseline test ({{topic:decide}}). Distillation changes only who wrote the answers.

## In practice at Technik

The classifier from {{topic:decide}} failed on volume: about 40 quality notifications a week, too few for a shorter prompt to repay hosting. Distillation replaces the labeller and not the volume, and Technik already has about 520 closed notifications labelled by engineers, so a teacher adds nothing those labels lack. The answer stays *not yet*. The figures are invented.

It would be worth pricing with plentiful inputs and scarce labels. Suppose Technik wanted a defect type on every operator note from both plants, thousands a month and none labelled. A large model could label them, engineers could relabel a 100-note sample, and a `gpt-4.1-mini` student could carry the volume. The score that counts is then the student's agreement with the engineers' sample. Agreement with the teacher says only that it copied it.

## Key terms

**Distillation**: training a smaller model on a larger model's outputs for a narrow task.

**Teacher**: the larger model whose answers become the training data.

**Student**: the smaller model fine-tuned on them.
