## TL;DR

{{topic:prompts}} taught what a prompt is and why a flow wants JSON. This lesson covers the **per-prompt settings** that a production prompt has to choose on purpose: the **model**, the **temperature**, the **content moderation level**, and how many knowledge records to retrieve. Microsoft's settings page documents all four, with limits that surprise: temperature is off for one model family, the moderation slider is off for the external models, and nothing pins a model version. The roadmap also promised JSON structure, Dataverse grounding and a moderation rule for document or regulated work. Neither page states any of the three, so this lesson drops them.

## Why it matters

A prompt that works in the builder is a draft. In a flow it runs unattended, on every file, on a model that Microsoft updates. Each setting has a failure behind it: a creative temperature on an extraction, a moderation level that blocks a legitimate input, a model quietly replaced. Defaults are still a configuration, one that someone else chose.

## How it works

### Model

<!-- volatile verified=2026-11 -->
You change the model with **Model** at the top of the prompt builder. The page lists nine, each with a rate tier (Basic, Standard or Premium), a category (Mini, General or Deep) and a context size:

| Model | Tier | Category | Context |
|---|---|---|---|
| GPT-4.1 mini, the default | Basic | Mini | 128K |
| GPT-4.1, GPT-5 chat, GPT-5.3 chat | Standard | General | 128K |
| GPT-5 reasoning, GPT-5.2 reasoning | Premium | Deep | 400K |
| Claude Sonnet 4.6 | Standard | General | 200K |
| Claude Opus 4.6 | Premium | Deep | 200K |
| Grok 4.1 Fast (non-reasoning) | Standard | General | not stated |

<!-- /volatile -->

The Claude models are hosted outside Microsoft by Anthropic, and Grok by xAI. The page treats both as experimental, and says Grok is not recommended for production. Models are periodically updated, the default is periodically upgraded, and an agent falls back to the default if its selected model is turned off.

<!-- unknown since=2026-11 -->
Pinning. The page documents no way to hold a prompt to one model version, and gives no retirement dates, referring instead to a separate availability page that this lesson did not read. A prompt's answers can change with no edit to the prompt.
<!-- /unknown -->

### Temperature

<!-- volatile verified=2026-11 -->
Temperature is a slider from 0 to 1, and the default is **0**. Microsoft describes 0 as more predictable and conservative, for high accuracy and less variability, and 1 as more creative. The slider is unavailable for GPT-5 reasoning.
<!-- /volatile -->

The page does not promise determinism: responses can vary at the same temperature. Treat 0 as *less variable*, and put a check after the step.

### Content moderation

<!-- volatile verified=2026-11 -->
The content moderation level is **Low**, **Moderate** or **High**, and it is set per prompt. Moderate is the default and is described as appropriate for most uses. Low is suggested for prompts processing data that could count as harmful content, with violence and medical procedures as the page's examples. High is for filtering more strictly than Moderate. The slider is **not available** for the Anthropic or Azure AI Foundry models.
<!-- /volatile -->

The levels are framed around harmful content: what each one might allow, such as offensive language or prejudiced views. Nothing on the page ties moderation to injected instructions, to document processing or to regulated work. It is a content filter, and {{topic:injection}} and {{topic:moderation}} are where the other defences are.

<!-- unknown since=2026-11 -->
What a blocked prompt returns. The page does not say what the output is, or whether the flow's step fails. For a prompt used as an agent tool it documents one handle: set the completion screen's **After running** option to send a specific response, and use the prompt's text output in the message.
<!-- /unknown -->

### Knowledge, and the rest of the panel

The settings panel also lists **Record retrieval**, the number of records retrieved from the prompt's knowledge sources, **Include links in the response**, which adds link citations for the retrieved records, and **Enable code interpreter**, which has its own page this lesson did not read. The page gives neither a range nor a default for record retrieval, and does not name Dataverse as a source. The overview names Dataverse only as something that must be installed in the environment, so the roadmap's *ground prompts in Dataverse knowledge* has no support here.

The overview adds that prompts need Copilot Credits and may face usage limits or capacity throttling, with no numbers. The settings page says prompts consume credits whatever a model's release stage, and that Power Apps and Power Automate draw AI Builder credits first, which Copilot Studio does not ({{topic:aibuilder}}). Both pages describe the standard harness.

## In practice at Technik

Technik has two prompts in its certificate and document work, and each wants different settings.

| | *Summarise revision change* | *Read a certificate field* |
|---|---|---|
| Job | Tell approvers what revision C of `SWI70000318` changes | Return the yield strength and its unit from a supplier PDF |
| Model | Chosen deliberately, not left on the default | GPT-4.1 mini is the default and its Mini category suits a narrow reading task. Check it on the ten sample certificates before accepting it |
| Temperature | 0 | 0, because the answer is a value to be checked, never a style |
| Moderation | Moderate | Moderate |
| Output | JSON with `acceptance_criteria_changed` ({{topic:prompts}}) | JSON with value and unit |

The summary prompt reads the work instruction's changes, so there is nothing for a stricter level to filter. A near-miss write-up describing an injury is the case the page's Low example points at. Technik has none in its data, so no prompt here is set to Low.

Two habits follow from the page's silence. A **regression set**, the ten sample certificates for the reading prompt and a few past revisions for the summary prompt, is run again after any model change, because the pages say models are updated and give no pin. And every model step is followed by code that checks it, as {{topic:detvsagentic}} argues, so a changed answer lands on a test.

<!-- unknown since=2026-11 -->
JSON output was not checked for the models above. Neither page says whether every model supports it, or the image and document inputs, and {{topic:prompts}} cites other pages for both. The test set above is the only check.
<!-- /unknown -->

## Design guidance

- **Choose the model, the temperature and the moderation level for each prompt**, and write them down.
- **Use 0 for extraction and classification**, and still check the output.
- **Pick the model deliberately**, and re-run a test set after any change you did not make.
- **Avoid the experimental external models in a production flow.** The page says so of Grok.
- **Set moderation from the content the prompt must handle.** Low is for harmful material you must process, High for filtering more.
- **Plan the blocked case**: what the flow does when a prompt returns nothing.
- **Count credits by tier.** The page ties each model to a rate tier and links the rates, so read them before choosing Premium.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| An extraction returns a different value on a rerun | Temperature above 0, or 0 taken as a guarantee | Set 0, and add a check |
| The temperature slider is greyed out | The model is GPT-5 reasoning | Choose another model, or accept the default |
| The moderation slider is missing | An Anthropic or Azure AI Foundry model | Choose a supported model, or filter elsewhere |
| A prompt changes behaviour with no edit | The model or the default was updated | Re-run the regression set |
| A legitimate injury report is blocked | The moderation level is too strict for the content | Set Low for that prompt only |

## Key terms

**Temperature**: a 0 to 1 setting where lower is more predictable and higher is more creative.

**Content moderation level**: a per-prompt Low, Moderate or High setting for filtering harmful content.

**Record retrieval**: the number of records a prompt retrieves from its knowledge sources.

**Regression set**: a fixed group of inputs re-run after any change, to catch changed answers.
