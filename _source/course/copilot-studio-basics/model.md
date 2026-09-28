## TL;DR

Every agent has one model doing its reasoning, and you can change it to trade speed, cost and depth. The
choice matters less than what follows it: **behaviour shifts when the model changes, even with identical
instructions**, so a model change invalidates every test you ran before it. Pick a generally available
default, build, measure, and change models only with an evaluation set to hand — and know that on the
standard harness the default itself is upgraded under you.

## Why it matters

Model choice is the most visible knob and rarely the most consequential one ({{topic:models}} makes that
case in general). What is specific to Copilot Studio is the discipline around changing it. An agent is a
system of instructions, tool descriptions and knowledge tuned against one model's tendencies, and swapping
the model perturbs all of it at once.

Teams that change model casually end up with agents nobody can reason about, because no two behaviours
can be traced to a single cause. And a model someone chose from a list may not be allowed in production,
may send data out of region, or may not be enabled in your tenant at all — all of which Copilot Studio
documents, and none of which the list shows at a glance.

## How it works

<!-- volatile verified=2026-09 -->
| | GitHub Copilot harness | Standard harness |
|---|---|---|
| **Where** | **Build** tab → components panel → **Model** list → **Save** | The agent's **Overview** page → **Model** section |
| **What it drives** | The agent's reasoning | Generative orchestration. Deep reasoning, generative answers and the prompt builder have **separate** model settings |
| **When the chosen model is unavailable** | A configured fallback model is used; otherwise the turn fails with an error code | The **default** model is used as the fallback |
<!-- /volatile -->

The model list changes too often to learn, and spans providers — OpenAI models alongside external ones
from Anthropic, Mistral and xAI. What is stable is how the list is labelled.

### Release types

| Tag | Means | Production? |
|---|---|---|
| **Generally available** (no tag) | Tested for scaled use; may still have regional limits | Yes |
| **Default** | The model every agent starts on — usually the best GA model | Yes |
| **Preview**, **Experimental** | Early access, subject to preview terms. May vary in quality, latency and consumption, time out, or be unavailable | **No** |
| **Cross-geo** | May process and store data outside your region | Ask first |
| **Retired** | Replaced as the default; usable for up to a month | Move off it |

Two consequences are easy to miss. Publishing an agent on a preview or experimental model does not make
its use free: it is billed at the established rates. And on the standard harness the **default is
periodically upgraded** as better models become generally available, so an agent left on the default can
change model without anyone touching it.

<!-- unknown since=2026-09 -->
Whether the GitHub Copilot harness also moves agents on its default model when that default is upgraded.
Microsoft documents this for the standard harness only. Check the model the agent is actually on before
comparing two evaluation runs.
<!-- /unknown -->

### Use categories

The standard harness also tags each model by what it is good for, and the categories are a sound way to
think on either harness:

| Tag | Good at | Latency and cost |
|---|---|---|
| **General** | Drafting, summarising, FAQ-style grounded answers, simple actions | Lowest |
| **Auto** | Mixed workloads; routes each turn dynamically | Variable |
| **Deep** | Multi-step reasoning, tool-rich work, long-document synthesis | Highest |

### What administrators decide

Much of the list is not yours to choose. Administrators allow or block **preview and experimental**
models per environment, and experimental ones additionally need data movement across regions turned on.
**External** models are a separate switch: turned on in the Power Platform admin center *and* allowed per
provider in the Microsoft 365 admin center. The two sets overlap but are governed independently.
When a model is blocked, the GitHub Copilot harness says so with an error code rather than a vague
failure: `MODEL_CONSENT_DENIED`, `CROSS_GEO_NOT_ALLOWED`, or `DEPLOYMENT_NOT_FOUND` for one that has been
retired or removed ({{topic:tenantvaries}}).

## In practice at Technik

The Technik Production Assistant does seven things of quite different difficulty. It has one model, so:

- the most frequent requests are lookups — *"What's the status of work order `100004521`?"* — and they are
  the most latency-sensitive;
- the hardest routine work is choosing between tools and knowledge, and drafting a QN write-up;
- so a capable **general** model, generally available, is the right default. A deep model would serve
  the rare hard question and slow down every status check.

The sequence that matters is what happens around the choice:

1. Build with that default.
2. Get the instructions, knowledge and tools right. That is where the quality is.
3. Build an evaluation set across the seven capabilities ({{module:testing-and-evaluation}}).
4. Only then try another model, and run the same set on both — recording which model produced which run.

Step 4 without step 3 is an opinion.

> [!WARNING]
> Changing the model invalidates prior testing. Not *might affect* — the same instructions produce
> different phrasing, a different willingness to call a tool, and a different willingness to say *I could
> not find that*. If you change it, re-run everything.

## Design guidance

- **Start on a generally available default.** Model choice is not where an agent becomes good.
- **Never publish on a preview or experimental model.** It is billed anyway and is not supported for
  production.
- **Record the model with every evaluation run.** A run whose model you cannot reconstruct is not
  evidence.
- **Change one thing at a time**, and re-run the whole set.
- **Do not default to a deep model.** Use one where the work is genuinely hard, or split that work out
  ({{topic:connected}}).
- **Check what your tenant allows** before designing around a model you read about.
- **Watch for default upgrades.** A behaviour change with no edit behind it may be a new model.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent changed behaviour and nobody changed anything | The default model was upgraded | Check which model it is on now; re-run the evaluation set |
| The agent changed behaviour after a model switch | Models follow instructions differently | Re-run the set; re-tune. There is no portable prompt |
| A model in the documentation is not in your list | Blocked by an administrator, or not offered in your region | Ask; do not design around it |
| `MODEL_CONSENT_DENIED` or `CROSS_GEO_NOT_ALLOWED` | The model is not enabled, or would move data out of region | An administrator decision; pick an allowed model meanwhile |
| `DEPLOYMENT_NOT_FOUND` | The model was retired or removed | Select an available model |
| Slower and dearer with no quality gain | A deep model doing routine work | Use a general model; reserve depth for hard steps |
| "It felt better" is the only evidence | No evaluation set | Build one. Ten questions is enough to start |

## Key terms

**Primary model** — the model an agent reasons with.

**Default model** — the model every agent starts on, and the standard harness's fallback. Upgraded over
time.

**Preview / experimental model** — early access, not for production, billed if used in production.

**Cross-geo** — may process data outside your region.

**External model** — a model from Anthropic, Mistral or xAI, which administrators enable separately.

**Evaluation set** — a fixed set of questions with known answers, run before and after a change.
