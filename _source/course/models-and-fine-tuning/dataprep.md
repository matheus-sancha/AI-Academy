## TL;DR

A fine-tuning file is a list of examples, one per line, in the shape the method expects. For SFT each line is a `messages` conversation ending in the answer you want, and you upload a `training.jsonl` and a `validation.jsonl`. The shape is the easy part. Microsoft's guidance on the hard part is short: examples must be **accurate, consistent and representative**, duplicates, gaps, bias and sensitive information are inspected before upload, and the final test set stays out of training entirely. Most of what makes a Technik file safe, such as splitting by event, auditing labels and leaving out text that gives orders, is this course's position and is marked as one.

## Why it matters

The training run is the cheap part. The classic page's warning is the reason to spend the effort on the data: fine-tuning with bad data "makes the base model worse", and without a baseline that is hard to see ({{topic:decide}}). A model also has no way to know that a label was a rushed guess. It learns whatever the file says, so the quality of the file is the quality ceiling of the model.

## How it works

### The shape of a line

*Adapted from the SFT page's example, which has a system, a user and an assistant message:*

```json
{"messages": [{"role": "system", "content": "Classify the quality notification's defect type."}, {"role": "user", "content": "Dye-penetrant check after cladding found porosity in the bore overlay. Area marked, unit held."}, {"role": "assistant", "content": "porosity"}]}
```

Save one conversation per line in `training.jsonl` and a second file, `validation.jsonl`. The page says to check the data-format, file-size and minimum-example requirements for your selected model, and it does not state them. Tool-calling and vision examples have their own formats on separate pages. A DPO line holds an `input`, a `preferred_output` and a `non_preferred_output` to the same prompt. An RFT line ends in a user message and carries whatever fields its grader reads, such as a reference answer. Both are detailed in the guides {{topic:finetune}} links.

### How much

The classic overview advises starting with 50 to 100 high-quality examples for initial testing, and scaling to 500 or more for production models. The counts are a guide and not a requirement, and the pages give no minimum that applies to every model.

### What "quality" means

The current overview's list of challenges gives the doc-backed checks:

- **Data quality and coverage.** Use accurate, consistent, representative examples. Look for missing scenarios, duplicates, bias and sensitive information before uploading.
- **Overfitting and evaluation leakage.** Keep training, validation and final test data separate, and compare checkpoints on held-out tasks, not on training loss.

Three roles follow. The **training** file is what the model learns from. The **validation** file is uploaded with the job, and the job reports loss on it. The **test** set is yours: never uploaded, never used to tune a prompt, kept for the end. The SFT page says only to keep validation and final test examples out of the training set.

<!-- unknown since=2026-11 -->
The pages stop at the checks above, so what follows is this course's position. Split by event, not by row, so near-duplicate records land on the same side. Audit the labels by having a second person relabel a sample. Remove personal data you do not need. Keep a record of where each example came from. Leave out text that is addressed to a model. The pages say nothing about whether extra fields beside `messages` are accepted, so a provenance record is safest kept in a separate file keyed by line number.
<!-- /unknown -->

## In practice at Technik

The set for the classifier in {{topic:decide}} comes from about 520 closed quality notifications, with a description and a defect type a person chose. The figure is invented. Here is what each rule does to it.

**Split by event.** Notifications `300001211` and `300001219` describe the same porosity as `300001234` in different words. If one twin trains the model and another sits in the test set, the model has seen the answer and the score is overstated. Group them, and put each group wholly on one side. A row-by-row random split cannot see that they are one defect.

**Audit the labels.** A defect type that engineers filled in from a pick list is noisy where two categories overlap, such as `porosity` and `lack of fusion`. Have a second engineer relabel 50 notifications. If they disagree on more than a few, the model will learn the disagreement, and the fix is to sharpen the definitions, not to add rows.

**Remove what is not needed.** A description may name the inspector who found the defect. The classifier needs the defect, so drop the name. Whether to keep identifiers such as the serial number `XT-V2-1042` is a choice to test, since a defect type does not depend on them.

**Leave out text aimed at a model.** Notifications `300001267` and `300001270` carry sentences addressed to an assistant ({{topic:ctxsecurity}}). They teach nothing about defects, and a shared model should not be trained on instructions. A screen that looks for such text beats listing two numbers by hand, because the next one will have different words.

Then split what is left, say 340 to train and 80 to validate, a ratio the pages do not set. The 420 sit under the classic guidance of 500 or more for production, which is one more reason the answer in {{topic:decide}} was *not yet*.

The candidate set starts as one query:

```sql
SELECT QN_NO, DESCRIPTION, DEFECT_TYPE
FROM TECHNIK_DW.OPS.SAP_QUALITY_NOTIFICATIONS
WHERE CLOSED_AT IS NOT NULL
  AND DEFECT_TYPE IS NOT NULL;
```

<!-- unknown since=2026-11 -->
Nobody ran this query. A person runs it under their own role, because agents never borrow people's roles and building a training set is not an agent's task.
<!-- /unknown -->

Order matters: this runs first, and the screens above run over its result.

## Design guidance

- **Split before you clean, and by event.** A duplicate across the line is leakage, not a detail.
- **Hold the test set out of everything**, including prompt tuning.
- **Audit the labels** before counting the examples.
- **Use the system message you will run with**, so the model is trained on the input it will see.
- **Inspect for sensitive information** and drop what the task does not need.
- **Keep provenance beside the file**, not inside it.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A fine-tune scores far above the baseline on the test set and not in use | Near-duplicates sit on both sides of the split | Group by event and re-split |
| The model reproduces one engineer's labelling habits | The labels were never audited | Relabel a sample with a second person, then fix the definitions |
| The model is trained on instruction-shaped text | A notification carried words addressed to an assistant | Screen for them before extracting, and review what is left |
| Names turn up in outputs | Personal data stayed in the descriptions | Remove what the task does not need before upload |
| The job rejects the file | The format differs by method or model | Check the format and size requirements for the selected model |

## Key terms

**JSONL**: one JSON object per line, the format of every fine-tuning file.

**Validation set**: examples uploaded with the job, on which it reports loss.

**Test set**: examples held out of training and tuning, used once at the end.

**Evaluation leakage**: a test example, or its near-duplicate, that the model trained on.
