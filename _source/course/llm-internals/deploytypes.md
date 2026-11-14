## TL;DR

A Foundry deployment type decides three things: where your prompts are processed, how you pay, and how predictable
latency is. There are three families, **Standard** (pay per token), **Provisioned** (reserved capacity) and **Batch**
(discounted and asynchronous), plus a **Developer** type for evaluating fine-tuned models. Start with **Global
Standard** and move only for a stated reason: data residency, reserved throughput or batch work.

## How it works

<!-- volatile verified=2026-11 -->
Each family comes in up to three processing locations. **Global** types may process a prompt in any Azure region.
**Data Zone** types stay within the US, the EU or Asia Pacific. The plain **Standard** and **Regional Provisioned** types
stay within the Azure geography you choose, though the service may move traffic between regions inside it. Batch has Global and Data Zone variants and no geography one. Data stored at rest remains in the
designated geography whichever type you pick.

Standard deployments suit bursty, low to medium volume and have no latency target. Provisioned deployments reserve
capacity for steady high volume and give a defined latency target and lower variance ({{topic:latency}}). Batch
takes a file of requests at 50% off, with a 24-hour target and no real-time promise.

Global Standard is the starting point. It gets new models first, has the lowest price and the broadest region
coverage, and Data Zone and geography types arrive later, with no guaranteed date for the last. Not every model
supports every type, and Azure Policy can deny a type by its SKU name. Priority and Flex processing are request-level
tiers on the Global and Data Zone Standard types, not deployment types, although the provisioned throughput page lists
priority processing beside them.
<!-- /volatile -->

## Where it fits at Technik

The capstone's one model deployment is `gpt-4.1-mini` as `GlobalStandard` ([`azure.yaml`, lines 20–22](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/azure.yaml#L20-L22)).
That is the page's default, and it means a prompt, with any Teamcenter lookup in it, may be processed in any Azure
region. Nothing in the capstone records a residency requirement, so the type was a default and not a decision. If
a customer contract limited where prompts may be processed, such as the one behind a confidential specification
like `PRJ-2031`'s, the move would be to Data Zone Standard, and `azure.yaml` is the one place to change it.

The other families fit work the capstone does not have yet. The certificate extraction in {{topic:structured}}
runs overnight and nobody waits for it, which is Batch work on its own deployment ({{topic:tokenbudget}}). Provisioned
throughput pays only at steady, high volume, where per-token billing costs more and latency variance matters.

## Key terms

**Deployment type**: the choice of processing location and billing model for a deployed model.

**Data zone**: a Microsoft-defined processing boundary, the US, the EU or Asia Pacific.

**Global Standard**: the default type, pay per token, processed in any Azure region.
