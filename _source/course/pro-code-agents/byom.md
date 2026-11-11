## TL;DR

You can connect a model you deployed in Microsoft Foundry to a Copilot Studio **prompt**. That is
narrower than the title suggests. "Each time this prompt runs, it uses the selected model", and
nothing else does: the agent's own model is still chosen as in {{topic:model}}. It is this module's
rule in reverse. You keep the configured platform and bring one component you own.

## What connects

The model is added from inside a prompt, and the prompt then runs wherever a prompt can
({{topic:prompts}}).

<!-- volatile verified=2026-11 -->
In the prompt's **Model** dropdown, the plus sign opens **Connect a model from Azure AI Foundry**.
Enter the "**Model deployment name** and **Base model name** exactly as they appear" in Foundry. The
walkthrough article lists four values to copy from the deployment's page: target URI, key, name and
model name. Its table pairs them with Copilot Studio's fields in an order that looks crossed, with
the endpoint field beside the model name, so match them by meaning. The key is an API key, which
means this connection holds a secret ({{topic:connrefs}}).
<!-- /volatile -->

## The limits decide it

- **Chat completions only.** The endpoint URL must end in `/chat/completions`. Give it a Responses
  endpoint and "the connection fails with a **Resource not found** error".
- **Not the newest models.** "The **GPT-5 family and later models** ... aren't currently supported".
  The same page opens by promising "the latest frontier models", so read its limits first.
- **Images narrow the list.** With image input, the dropdown shows only Foundry models that accept
  images.
- **Standard harness.** The page describes "features used in agents or agent flows powered by the
  standard harness".

<!-- unknown since=2026-11 -->
On the GitHub Copilot harness a prompt reaches the Production Assistant only inside a workflow.
Whether a workflow's AI action can select a connected Foundry model is not stated. Neither source
mentions fine-tuned deployments either ({{topic:finetune}}). Test both before planning around them.
<!-- /unknown -->

## Governance moves with it

"The Azure AI Foundry models are connected by connectors." Administrators set data policy for the
connector named **Azure AI Foundry**, and each connected model appears as a connection
({{topic:dlp}}). Content safety moves the other way. Microsoft recommends Responsible AI policies
for these models, and that you "manage that in Azure AI Foundry". The filter on this prompt is the
one on your deployment.

## At Technik

The submission flow's prompt, *Summarise revision change*, is the candidate. It reads a draft
revision as a PDF and returns JSON, and its `acceptance_criteria_changed` field decides whether the
quality lead joins the approval. Moving it to a Foundry model touches one prompt and leaves the
assistant alone. It is still a model change. Rerun the prompt's test cases first, because a model
that gets that one boolean wrong removes an approver.

## Key terms

**Bring your own model** — connecting a Foundry model deployment to a Copilot Studio prompt, in
place of a managed model.

**Chat completions endpoint** — the deployment URL ending in `/chat/completions`, the only type this
feature accepts.
