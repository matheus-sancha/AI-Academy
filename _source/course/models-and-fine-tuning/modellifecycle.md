## TL;DR

A model version is a lease, and the lessor sets the dates. Every Foundry model sits in one of five stages, **Preview**, **Generally Available**, **Legacy**, **Deprecated** or **Retired**, and at retirement "all inference requests return 410 Gone". Dates are fixed when a model launches, and the FAQ says plainly that "retirement dates aren't extendable". For most deployments Microsoft upgrades you to a replacement when the date arrives, which changes the model under your agent without a release, so the one control you hold is an evaluation set you run **before** the date. A fine-tuned model adds a second clock of its own.

## Why it matters

Every earlier lesson in this module produces or serves a model, and every one of them stops being true on a date. The capstone's `gpt-4.1-mini` version `2025-04-14` has such a date. The release gate checks a change that someone makes. A retirement is a change that nobody makes, so nothing in a pipeline fires. The habit this lesson builds is to read the dates early and own the test that tells you the replacement is acceptable.

## How it works

### Five stages

<!-- volatile verified=2026-11 -->
The page's table says which stages allow new deployments and which keep existing ones working. **Preview** models are experimental and "might change" in weights, runtime and API schema. **GA** models have fixed weights and APIs. **Legacy** means newer models exist and you "should plan on migrating", and the stage is optional, since a model can skip to **Deprecated**. A deprecated model still serves existing customers, defined by subscription: "A new subscription under the same tenant doesn't inherit access." **Retired** returns 410 Gone.

The standard GA lifecycle is 18 months, with the retirement date set "programmatically" at launch. Deprecation comes at 12 months. The replacement can be tested in Global Standard about 90 days before retirement and in provisioned regions about 30 days before. Anthropic, DeepSeek, Fireworks and Mistral AI models have 12-month lifecycles, and a security or compliance problem can bring an emergency retirement on shortened notice. A GA retirement notice goes by email to subscription owners with active deployments at least 60 days ahead, and a Service Health advisory appears too, under the service name *Azure OpenAI Service*. Preview models get at least 30 days and are upgraded or terminated, with no option to stay.
<!-- /volatile -->

The Models API reports the same stages under different names. `lifecycleStatus: "Deprecating"` is what the docs call Deprecated, and `"Deprecated"` means Retired. The page's pseudo-code reads both fields together.

*Adapted from the lifecycle page's pseudo-code for reading a stage from the Models API's `lifecycleStatus` and `deprecation.inference` fields:*

```python
def stage(status: str, inference_date: str | None, today: str) -> str:
    if status == "Deprecated":
        return "Retired"
    if status == "Deprecating":
        return "Deprecated"
    if inference_date and inference_date < today:
        return "Retired"  # even if lifecycleStatus lags
    return {"GenerallyAvailable": "GA", "Preview": "Preview"}.get(status, "unknown")
```

### What happens on the date

<!-- volatile verified=2026-11 -->
For Global Standard, Data Zone Standard and Standard deployments, Microsoft upgrades you to a replacement, region by region, on a published schedule. "Provisioned deployments are NOT auto-upgraded", so they need a manual move, in place over a window of 20 to 30 minutes, or side by side. Batch is also side by side: deploy the new model, resubmit jobs, retire the old one. The `versionUpgradeOption` property has three values: `OnceNewDefaultVersionAvailable`, `OnceCurrentVersionExpired`, and `NoAutoUpgrade`, which means the deployment "stops working at retirement".
<!-- /volatile -->

So **pinning** is a choice between being upgraded early, upgraded on the date, or switched off on the date. None of them keeps the old model.

<!-- unknown since=2026-11 -->
The page does not say which `versionUpgradeOption` value a new deployment gets by default, so check a real deployment. It names a replacement only for its `gpt-4o` example, and sends you to a retirement schedule for the rest. This lesson did not read that schedule.
<!-- /unknown -->

### A fine-tune runs two clocks

Fine-tuned models retire in two phases. "Unless explicitly stated, training retires no earlier than the base model retirement date." After that, models already trained stay deployable until their own **deployment** retirement, when "inference and deployment return error responses". The current fine-tuning overview adds the constraints that matter: "An adapter isn't interchangeable across similarly named base models", quality must be reassessed "as a base model approaches retirement", and "retraining and redeployment can be necessary".

<!-- volatile verified=2026-11 -->
For `gpt-4.1-mini` version `2025-04-14`, the table gives training "no earlier than 2027-04-14" for existing customers only, and deployment retirement on 2027-10-14. Other customers lose training when the base model retires.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
Neither page says what happens to a fine-tuned deployment when its base model's own deployments are upgraded, or whether a fine-tune can be moved to a successor without retraining. The overview's wording points to retraining. A Developer deployment is no answer, since it lasts 24 hours and is for evaluation only.
<!-- /unknown -->

### Migrating is an evaluation

The page says not to wait for Microsoft's official replacement, which is declared only about 90 to 120 days before the date. It tells you to evaluate candidates against "your own application, prompts, and representative data", and to "compare quality, latency, and cost together rather than relying on public benchmarks alone". Before moving, confirm API compatibility, feature support, deployment type, region, capacity and quota. A separate *Model migration process* page covers the steps. This lesson did not read it.

## In practice at Technik

The capstone pins `version: "2025-04-14"` on `GlobalStandard` ([`azure.yaml`, lines 15–22](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/azure.yaml#L15-L22)). The page's dates give it a retirement of 14 April 2027, and Global Standard is a type Microsoft upgrades. `azure.yaml` sets no upgrade option, so the agent could be answering from a different model on that date, with no commit behind it.

The capstone's gate does not see it. The eval workflow runs on pull requests, pushes and a manual dispatch, and has no schedule ({{topic:stageevals}}). Its live job stays off until a reader turns it on.

*From [`.github/workflows/evals.yml`, lines 4–11](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/.github/workflows/evals.yml#L4-L11):*

```yaml
on:
  pull_request:
    paths: ["agent/**", "server/**", "evals/**", "seed/data/**", "tests/**", "infra/**", "azure.yaml",
            "pyproject.toml", "uv.lock", ".github/workflows/*.yml"]
  push:
    branches: [main]
  workflow_dispatch:
  workflow_call:  # stage 5: the release workflow runs this as its gate
```

The plan is dated backwards from 14 April. Put a Service Health alert where the team will see it. About 90 days out, deploy the candidate as a second deployment, point the evals' `FOUNDRY_MODEL` at it, and dispatch the workflow. Compare it with `evals/baseline.json`. A hosted agent has no canary ({{topic:foundryagents}}), so the evidence has to exist before traffic moves. After the date, a scheduled run would catch a quiet upgrade, and adding one is a change to the workflow, not to the lesson.

The classifier shows the second clock. Fine-tuning `gpt-4.1-mini` would give a model whose deployment retires on 14 October 2027, six months after its base. Retraining needs the 420-example set ({{topic:dataprep}}) and a new baseline ({{topic:decide}}). That is one more cost to add to why the answer was *not yet*. The dates are the page's, the arithmetic is ours.

## Design guidance

- **Read the dates when you choose the model**, and record the retirement beside the version.
- **Choose an upgrade option on purpose.** Be able to say what happens on the date.
- **Keep an evaluation set that can score any replacement**, and run it before the notice.
- **Alert on Service Health** so the notice reaches a team, not only subscription owners.
- **Plan a fine-tune's life from the base model's remaining months.**
- **Migrate side by side**, since a hosted agent has no canary.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Calls return 410 Gone | The version retired and the deployment was never moved | Check `lifecycleStatus` and the dates monthly |
| Answers change on a date nobody deployed | Microsoft upgraded a Standard-family deployment | Run the evaluation set against the replacement before the date |
| A provisioned deployment fails while others carry on | Provisioned deployments are not auto-upgraded | Migrate it in place or side by side |
| The notice email reached nobody useful | It goes to subscription owners with active deployments | Add a Service Health alert to a shared channel |
| A fine-tuned model stops working before its base model | Its deployment has its own retirement date | Retrain on the successor and re-evaluate |
| A script calls a retired model "Deprecated" | The API's `Deprecated` means Retired | Read `lifecycleStatus` and the date together |

## Key terms

**Retirement date**: the date a model version stops serving inference, fixed at launch and not extendable.

**Auto-upgrade**: Microsoft's move of a Standard-family deployment to a replacement when its version retires.

**`versionUpgradeOption`**: the deployment property that sets whether and when it upgrades.

**Two clocks**: a fine-tuned model's training and deployment retirement dates.
