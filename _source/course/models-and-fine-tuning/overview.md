## What this module is for

This is a **reference module, not a read-through**. Nothing later in the level depends on it, and most engineers will never need it. Come here when someone says "we should fine-tune it", when a model has to be served to more than one app, or when a retirement notice arrives. Read the lesson that answers the question in front of you and skip the rest.

{{topic:training}} gave you the stages a model goes through and the order to escalate in: prompt, retrieval, then training. This module starts where that stops. It covers what Microsoft lets you run in Foundry, how to decide whether to run it, what the data has to look like, what a smaller model trained on a larger one's answers is worth, how a model is served to several callers, and what happens when the version you trained on is retired. Eight lessons cover it, two of them short and optional.

One example runs through all eight: a classifier that reads a quality notification's description and fills in its defect type. It is a good example because it fails. At Technik's volume the classifier does not repay its hosting, so the module is mostly about how to find that out before you pay for it. The volumes, labels and pass mark are invented, and nothing in the module was run.

## Before you start

You need {{topic:training}}. {{topic:deploytypes}} and {{topic:tokenbudget}} in {{module:llm-internals}} come first for {{topic:serving}}, since that lesson starts where they end. {{topic:evalstrategy}} and {{topic:foundryevals}} in {{module:evaluation-and-observability}} are what {{topic:decide}} and {{topic:modellifecycle}} mean by an evaluation set and a gate. From {{module:agent-skills}}, a skill is the cheaper alternative that several lessons ask you to rule out first.

Allow about three hours to read it end to end, though you are not meant to.

## What you will be able to do

By the end of this module you should be able to:

- name the signal a task can supply, a demonstration, a preference or a score, and say which method it points to and which models support that method;
- run the experiment that decides between a better prompt, retrieval and fine-tuning, and price the result per request;
- prepare a training file that cannot leak the test set, and say which of its safeguards the documentation does not cover;
- say what distillation is in Foundry, and why the student is scored against people and not against its teacher;
- say what Copilot Tuning is and why it is a different route, not a lighter version of this one;
- put an AI gateway in front of shared deployments for the right reason, and say what neither source documents about failure;
- read a model's retirement date, say what the platform does on it, and test a replacement before it arrives.

## The thread through this module

From the question to the date it expires.

{{topic:lifecycle}} gives the methods and the support table. {{topic:decide}} turns "should we?" into an experiment with a baseline and a price per request. {{topic:finetune}} is the job, and {{topic:dataprep}} is the file that decides how good it can be. {{topic:distill}} changes who wrote the answers, and {{topic:copilottuning}} is the no-code route inside Microsoft 365 Copilot. {{topic:serving}} covers what changes when several apps share a model, and {{topic:modellifecycle}} covers what changes when the model is switched off.

Two ideas run through all eight. The first is that **the signal decides everything else**: what you must collect, what you must trust, and what you evaluate. SFT trusts your examples, DPO your preference labels, RFT your grader, and a distilled model trusts its teacher. The second is that **a model you depend on is not yours to keep**. A fine-tune is a new artifact with its own retirement date, a serving choice is a quota shared with others, and an upgrade can change an answer with no release behind it. Both ideas end in the same habit: keep a test set that nothing has been tuned against, and run it whenever the model changes.

Four dated facts will have moved by the time you read this, so check them first. The support table in the current fine-tuning overview, which was updated on 29 October 2026. The retirement dates for the model versions you use. Whether Copilot Tuning has left early access. And which AI gateway capabilities are still preview. Most lessons also carry a visible *Not yet verified* block, because the pages are silent on a good many claims the roadmap once made.

## Self-check

<details>
<summary>1. A product owner wants engineers to pick the better of two QN write-ups and to train a model on those picks, "using o4-mini because it reasons well". What do you check first, and what do you trust?</summary>

The model-by-method table, before any data is collected. Engineers choosing between two answers is **preference** data, which is DPO's signal, and in the page updated on 29 October 2026 `o4-mini` lists RFT and no DPO. The `gpt-4.1` family lists SFT and DPO, and no model lists both DPO and RFT. A model supported for one method is not automatically supported for another ({{topic:lifecycle}}).

What you trust changes with the method. DPO trusts the preference labels, so check that two engineers agree on which write-up is better before counting pairs ({{topic:finetune}}). Also ask whether a skill already holds the template, which costs nothing to change.
</details>

<details>
<summary>2. About 520 closed quality notifications have a defect type that engineers chose. Someone says that is enough to fine-tune a classifier. How do you answer, and what changes if the real problem is labels rather than volume?</summary>

Answer with an experiment, not an opinion. Set the pass mark, keep 100 notifications as a final test, score the best prompt on them, and sort the failures by cause. Then price it per request: twelve examples of about 100 tokens are about 1,200 tokens of prompt overhead per call, and at about 173 notifications a month that is roughly 208,000 tokens, the most fine-tuning could save, against a hosting charge owed whether or not anyone asks. 420 training examples are also under the classic page's 500 or more for production. So the answer is *not yet* ({{topic:decide}}).

If the problem were thousands of unlabelled notes, distillation changes the question. A larger model labels them, and engineers relabel a sample. The student is then scored against the engineers' sample, because agreement with the teacher shows only that it copied it ({{topic:distill}}).
</details>

<details>
<summary>3. A fine-tuned classifier scores 99% on the held-out set and 81% on a month of real notifications. Notifications `300001211`, `300001219` and `300001234` describe the same porosity in different words. What went wrong?</summary>

Evaluation leakage. If one of those three trained the model and another sat in the test set, the model had seen the answer, and a row-by-row random split cannot see that they are one defect. Split **by event**, so near-duplicates land on one side ({{topic:dataprep}}).

Check the rest of the list too. Have a second engineer relabel a sample, since a model learns two engineers' disagreement as readily as agreement. Remove names the task does not need. Screen out text addressed to an assistant, because a shared model should not be trained on instructions. The pages cover duplicates, bias, sensitive information and separate test data. The rest is this course's position, and the lesson says so.
</details>

<details>
<summary>4. A pilot for another team starts calling the Production Assistant's deployment, and the assistant begins to return 429s at 10 a.m. although its own traffic is light. What do you suspect, and when would you add an AI gateway?</summary>

The shared pool. Quota is tokens per minute across callers, so one app can spend another's share ({{topic:tokenbudget}}). With a single app a limit on the deployment is enough, and the gateway page says so. With several, the gateway's token-limit policy gives each consumer its own cap, keyed on a subscription key or any value you choose. Its load balancer can prefer reserved capacity, and its circuit breaker stops sending to a backend that is not responding ({{topic:serving}}).

Do not read a gateway as a fix for a regional interruption by itself, because the pages say traffic routed to an interrupted region is affected, and a backup needs a second deployment. Nor does either source say how clients should retry or whether a streamed answer survives a failover.
</details>

<details>
<summary>5. The Production Assistant runs `gpt-4.1-mini` version `2025-04-14`, and the release gate is green. What happens on 14 April 2027, and what do you do before then?</summary>

The version retires, and because the deployment is Global Standard, Microsoft upgrades it to a replacement on a published schedule. That is not a release, so the gate, which runs on pull requests and pushes, never fires. Retirement dates are not extendable, and `NoAutoUpgrade` only means the deployment stops working on the date ({{topic:modellifecycle}}).

Read the dates early and set a Service Health alert. About 90 days out, deploy the candidate as a second deployment, run the evaluation set against it and compare with the baseline. A hosted agent has no canary, so the evidence has to exist before traffic moves. A fine-tune has its own clock, with deployment retiring on 14 October 2027 for `gpt-4.1-mini`, and retraining needs the data and test set again.
</details>
