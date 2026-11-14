## TL;DR

Fine-tuning is the one stage of a model's training that you can still run, and Foundry lets you run it in a fixed set of ways. **Managed Training** has three methods, each defined by the signal the model learns from: **SFT** learns from prompts and desired responses, **DPO** from preferred and rejected responses to the same input, and **RFT** from a grader's score. **Programmed Training** (preview) lets you write the training loop yourself. Every job produces a new model, and which method, model, training type and deployment option can be combined is a table you check before you collect any data. The spine of the module starts here: **the signal decides the data you need, what you must trust, and what you evaluate.**

## Why it matters

"We should fine-tune it" names no method, model, data shape or test. This lesson turns it into four questions: what signal can we produce, which model supports that method, where may our data go, and what happens when the base model is retired.

{{topic:training}} gave the general stages and the vocabulary. This lesson starts where it stops, at what Microsoft lets you run. One source note: the older overview page applies only to the **Foundry (classic)** portal and points to *Fine-tuning in Microsoft Foundry* for the current experience. This lesson follows the current page, and uses the classic one for its advice on starting.

## How it works

### What a fine-tune changes

The current overview says fine-tuning "adjusts the model's weights rather than adding examples to each prompt", building on what the model already does. The classic page says the result is "a new, optimized GenAI model". So the base model is untouched and you own a new artifact that must be deployed, evaluated and eventually retired.

The current page lists six reasons to do it: accuracy on patterns too numerous for a prompt, less prompt overhead, a consistent style or schema, better tool use, better use of retrieved context, and a smaller model made to meet what a larger one met. It then qualifies all six. Benefits "aren't guaranteed", fine-tuning "adds training and hosting costs", and it "doesn't replace retrieval for current information or application-level safety controls".

### Three signals

| Method | Learns from | Microsoft's fit |
|---|---|---|
| **SFT**, supervised fine-tuning | Prompts and desired responses | You can demonstrate the behaviour |
| **DPO**, direct preference optimization | Preferred and rejected responses to the same input | Quality is a preference, such as tone or completeness, and no single answer is correct |
| **RFT**, reinforcement fine-tuning | Prompts and a grader that scores generated responses | Several solutions are possible and you can reliably score them |

The classic page adds three points. DPO needs no separate reward model. RFT suits objective domains where the model already shows some competency, and needs more machine-learning expertise. And SFT is the place to start, because it covers the most scenarios. The pages describe RFT's fit differently: the classic one wants "clear right and wrong answers", the current one wants a trustworthy score over several acceptable answers. Both depend on the grader, the part {{topic:finetune}} says to distrust.

### Two approaches

In **Managed Training** you submit data and settings and Foundry runs the job. Your controls are the data, the supported hyperparameters and, for RFT, the grader. In **Programmed Training** you write a Python loop and Foundry executes the training and sampling operations, so you control losses, rewards, rollouts and checkpoints. The page recommends Managed Training for anyone new, and Programmed Training for experienced practitioners, who then maintain the driver, environments, tokenization, checkpoints and recovery logic. This course teaches Managed Training only.

<!-- volatile verified=2026-11 -->
### What combines with what

A model supported for one approach, method or modality isn't automatically supported for another. In the page updated on 29 October 2026, `gpt-4.1`, `gpt-4.1-mini` and `gpt-4.1-nano` list SFT and DPO under Managed Training, `o4-mini` lists RFT, `gpt-5` lists RFT and needs an invitation, and no model lists both DPO and RFT. Programmed Training (preview) needs explicit access approval first.

Training types decide where a job runs, separately from how you later serve the model. **Standard** trains in your resource's region, with data-residency guarantees. **Data zone** trains within a zone, and only the US zone is supported. **Global** is cheaper and faster to start, and copies your data and weights to whichever region trains. **Developer** uses idle capacity, can be preempted, and promises neither an SLA nor residency. Serving is a third choice, covered in {{topic:deploytypes}} and {{topic:serving}}.
<!-- /volatile -->

### What stays outside your control

The page's limitations are operational. "An adapter isn't interchangeable across similarly named base models", so confirm method, tier, version and deployment eligibility before training. Quality must be reassessed "as task data changes or a base model approaches retirement", and "retraining and redeployment can be necessary". Retirement is the subject of {{topic:modellifecycle}}.

<!-- unknown since=2026-11 -->
Neither overview says whether a Managed Training job trains all of a model's weights or an adapter. They name adapters only when describing the managed-compute and Fireworks deployment options. Neither describes pre-training or the order in which providers run their stages, so treat those as general background. The video the roadmap lists was not watched, and nothing here depends on it.
<!-- /unknown -->

## In practice at Technik

Take three requests that all arrive as "fine-tune it".

| Request | Signal Technik can produce | Verdict |
|---|---|---|
| Fill the defect type on a quality notification from its description | Hundreds of descriptions with a defect type a person chose | **SFT** fits: it is a demonstration |
| Make the QN write-up shorter | Pairs of drafts where an engineer prefers one | The shape is **DPO**, but a skill holds the template and costs nothing to change ({{module:agent-skills}}) |
| Answer questions about the current revision of `SWI70000318` | Nothing a training run can keep current | Not fine-tuning. The page says it doesn't replace retrieval |

The first request is the one this module follows. RFT would score the label with an exact-match grader, but a task with one correct answer is already fully described by demonstrations. That reading is this course's position, not a statement on either page.

The Production Assistant runs on `gpt-4.1-mini` ({{topic:deploytypes}}), which lists SFT and DPO, so a classifier could start from the same family. For the training type, Technik should pick **Standard** until someone with authority says a QN description, which can name a customer's project, may leave the region.

<!-- unknown since=2026-11 -->
Nobody has run a job, and the pages do not say what a quality notification's description may contain. The defect-type labels used across this module, `porosity`, `lack of fusion`, `crack`, `dimensional`, `coating` and `other`, are an invented choice.
<!-- /unknown -->

## Design guidance

- **Name the signal before the method.** Say what you can demonstrate, prefer or score, and the method follows.
- **Check the support table before collecting data.**
- **Start with Managed Training, SFT and default settings**, as both pages advise.
- **Treat the result as a new artifact**, with its own deployment, evaluation and retirement date.
- **Choose the training type as a data decision**, not a price tier.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Preference pairs are collected, then the chosen model offers only SFT | The method-by-model table was not checked first | Check it before any labelling |
| The steps from a classic page do not match the portal | The page applies only to the classic portal | Use *Fine-tuning in Microsoft Foundry* and its three how-to guides |
| A fine-tuned model is wrong about last week's change | Fine-tuning does not replace retrieval for current information | Move that content to retrieval |
| Data appears to have left the region | The Global training type copies data and weights to the training region | Choose Standard, or get the move approved |
| A fine-tune stops working after a model change | An adapter is not interchangeable across similarly named base models | Re-run training and evaluation against the new base |

## Key terms

**Fine-tuning**: further training of a pretrained model on your data, producing a new model.

**SFT, DPO, RFT**: fine-tuning from desired responses, from preferred and rejected responses, and from a grader's reward.

**Managed Training**: a job Foundry runs from your data and settings.

**Programmed Training**: a preview route in which you write the training loop.

**Training type**: where a job runs, such as Standard, Data zone, Global or Developer.
