## TL;DR

SFT, DPO and RFT share one job shape: upload a training file and a validation file, create a job that names the method, watch its metrics and checkpoints, choose a checkpoint on held-out results, and deploy it through the portal. They differ in what the file holds and what you have to trust: SFT trusts your examples, DPO your preference labels and RFT your grader. Each method also reports a metric that is **not** task quality, and all three pages warn against reading it as such. Start with SFT, default settings and your model's supported values, and judge the result on your own test set.

## Why it matters

A job is easy to submit and easy to misjudge. The three Foundry guides read alike because the work is alike, and they repeat one warning: a number the job reports about itself does not say the model solves your task. This lesson gives you the common shape once, then the part of each method where a careless job goes wrong.

A source note. The roadmap's older wording, "serverless or managed compute", belongs to the classic portal. The current guides call the job **Managed Training**, and use serverless and managed compute for how you later *serve* the result ({{topic:lifecycle}}).

## How it works

### One job shape

1. **Prepare** `training.jsonl` and `validation.jsonl`, one example per line ({{topic:dataprep}}).
2. **Upload** both with purpose `fine-tune` and wait for them to finish processing.
3. **Create** the job: a supported model identifier, the two files, the method, a training type and a suffix to recognise the result.
4. **Monitor** the status, event log, metrics and checkpoints. A job can queue before it starts, and the pages say not to resubmit a queued one.
5. **Compare** checkpoints on held-out tasks. Do not assume the latest checkpoint is the best.
6. **Deploy** through the Foundry portal, however you submitted, then run evaluations against your held-out set.
7. **Clean up.** Cancel jobs you do not need and delete uploaded files separately. Cancelling training deletes no deployment and stops none of its charges.

<!-- volatile verified=2026-11 -->
Training needs the **Foundry User** role, and **Foundry Owner** if you also deploy. These were recently renamed from *Azure AI User* and *Azure AI Owner*, and the old names still appear in places. You can work in the portal (**Build** > **Fine-tune**), in Python with either the Foundry SDK or the OpenAI SDK, over REST, or with the Azure Developer CLI's fine-tuning extension. Pause and resume are not available for every model or method.
<!-- /volatile -->

*Adapted from the Python example on the SFT page. The `client` is created as that page shows, and the model and training type come from the environment:*

```python
import os

with open("training.jsonl", "rb") as f:
    training_file = client.files.create(file=f, purpose="fine-tune")
with open("validation.jsonl", "rb") as f:
    validation_file = client.files.create(file=f, purpose="fine-tune")
client.files.wait_for_processing(training_file.id)
client.files.wait_for_processing(validation_file.id)

job = client.fine_tuning.jobs.create(
    model=os.environ["FINE_TUNING_MODEL"],
    training_file=training_file.id,
    validation_file=validation_file.id,
    suffix="qn-defect-type",
    method={"type": "supervised", "supervised": {"hyperparameters": {
        "batch_size": "auto", "learning_rate_multiplier": "auto",
        "n_epochs": "auto"}}},
    extra_body={"trainingType": os.environ["FINE_TUNING_TRAINING_TYPE"]},
)
print(job.id, job.status)
```

### Where each method goes wrong

| | SFT | DPO | RFT |
|---|---|---|---|
| **You trust** | The examples | The preference labels | The grader |
| **Job body** | `method.supervised` | `method` of type `dpo` | `method.reinforcement`, with the grader |
| **The metric that misleads** | Token accuracy | Training loss and token accuracy | Reward |
| **Evaluate with** | Held-out task results | The same rubric as the labels | Held-out results, plus a look at the responses |

**SFT** exposes three hyperparameters: batch size, a learning-rate multiplier and the number of epochs. More epochs give the model more chances to learn and can increase overfitting, and a smaller multiplier can reduce it. Keep your model's defaults for the first job and change one setting at a time. The reported metrics are training loss, full validation loss and the token accuracy of each. If training loss falls while validation loss rises, inspect the failing validation examples. Token accuracy only measures how well the model predicts your target text, so confirm that an improvement also helps the task.

**DPO** needs a method type and nothing else for a first job, and the page advises leaving hyperparameters alone. They trade learning your preferences against staying close to the starting model. Token accuracy is not a measure of whether responses match your preferences, so compare candidates on held-out preference examples with the same rubric your labels used, and count how often each meets the preferred behaviour. To run DPO after SFT, pass the fine-tuned model's identifier and not its deployment name, and check that the model supports it.

**RFT** takes a **grader**, the reward function that scores each generated response. There are five types: string comparison, text similarity, a model grader, a Python grader and a combination of graders. Test the grader before training on correct, incorrect and malformed responses, and check that a superficial response cannot score high without solving the task. A Python grader runs without network access. A model grader needs a grading model, which Foundry hosts or you deploy separately, depending on the model being trained. The metrics to read are mean reward, per-grader rewards, grader error rates and reasoning-token use. The page's warning is blunt: a rising reward does not establish better task performance if the model exploits the grader.

<!-- volatile verified=2026-11 -->
The page validates a grader with `client.fine_tuning.alpha.graders.validate`, a name that marks the API as early. Reinforcement fine-tuning is limited to a few models, and one of them needs an invitation ({{topic:lifecycle}}).
<!-- /volatile -->

## In practice at Technik

The classifier from {{topic:decide}} is an SFT job on a model that lists SFT, such as the one the Production Assistant runs on. A person submits it, with the Foundry User role on their own sign-in. The Production Assistant's identity reads Snowflake through one read-only role and has no part in training, and the rule that agents never borrow people's roles applies here too.

First job: defaults, Standard training, and the 420 training and validation notifications from {{topic:dataprep}}. When it finishes, run each checkpoint over the 100 held-out QNs with the exact-match check, and read the full validation loss only to know when to look closer. A checkpoint that beats the baseline by less than the baseline's own variation on a hundred cases has shown nothing yet. Deploy the best one on a Developer deployment to evaluate it ({{topic:deploytypes}}), and decide then whether to host it.

An RFT version would grade with a string comparison on the label, as the page's own exact-answer example does. This course's reading is that for a single correct answer RFT adds a grader to maintain without adding signal.

<!-- unknown since=2026-11 -->
Nobody ran this job. The SFT page shows `GlobalStandard` as the API value for Global training and gives none for Standard, so the value Technik would pass is unknown. The CLI sample's `epochs: 4`, `batch_size: 8` and `learning_rate_multiplier: 0.1` are, in the page's words, "not defaults for every model". The pages do not say how long a queued job waits.
<!-- /unknown -->

## Design guidance

- **Use the method that matches your signal, then SFT if unsure**, with defaults for the first job.
- **Change one setting at a time**, and keep every job's record.
- **Choose a checkpoint on held-out task results**, never on loss or reward alone.
- **Test an RFT grader adversarially** before spending a training run on it.
- **Keep the job's identity human.** An engineer submits and owns it.
- **Delete what you do not use**, files and deployments both.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Loss falls and the model gets worse | Training fits the examples, not the task | Compare validation loss and held-out results; reduce epochs or the learning-rate multiplier |
| RFT reward climbs and answers look the same | The model found a shortcut the grader rewards | Test the grader on adversarial responses, and read the responses |
| A job looks stuck, so it is submitted again | Jobs can queue before training starts | Read the status and event log, and do not resubmit a queued job |
| A grader returns errors on every example | Its fields do not match the response format or dataset | Align `output_text` or `output_json` and the dataset field names with the grader |
| Charges continue after cancelling | Deployments are separate from jobs | Delete unused deployments as well |

## Key terms

**Hyperparameter**: a setting of the training run, such as batch size, learning-rate multiplier or epochs.

**Checkpoint**: a saved version of the model partway through training, compared on its own.

**Validation loss**: the loss measured on examples the job did not train on.

**Grader**: the function that scores a generated response during RFT.
