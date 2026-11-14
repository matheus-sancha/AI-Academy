## TL;DR

{{topic:deploytypes}} chose where a prompt is processed and how you pay, and {{topic:tokenbudget}} explained quota as a pool. Both assume one caller. This lesson is for the day a second app calls the same models, and the question changes from *which type* to **who may use how much, and what happens when it is gone**. The deployment-types page says what each type promises and what a regional interruption does. The API Management **AI gateway** page adds a per-consumer token limit, backend load balancing with priorities, a circuit breaker and metrics per caller. Neither documents what a client should do when a call fails, so that part is this course's position.

## Why it matters

A deployment with one caller fails in one way: the caller reaches its quota. With three callers it fails in more. One can starve the others of a shared pool. One region's interruption can take every caller down. A different model can answer after a failover, and nobody notices the answers have changed. None of that is a model problem. It is a question of what stands between callers and deployments, and by default nothing does.

## How it works

### What a deployment promises

<!-- volatile verified=2026-11 -->
The deployment-types page gives each family a guarantee. Standard types are "best-effort service". Provisioned types "provide guaranteed throughput and lower latency variance". Developer deployments have no SLA. Global Standard has the highest default quota and "eliminates the need to load balance across multiple resources", but for Global Standard and Data Zone Standard the page warns that if the primary region "experiences an interruption in service, all traffic initially routed to this region is affected", and points to a high-availability guide this lesson did not read. Its troubleshooting table says that when quota is exceeded you request an increase or use another region. A batch deployment has its own enqueued-token quota, which keeps it from disturbing online work.
<!-- /volatile -->

So a type promises throughput, not survival of a failure. Spreading across deployments is your work, or a gateway's.

### Quota is a pool, so give each consumer a share

The gateway page puts the problem plainly. Providers assign tokens per minute (TPM) to a deployment, and when "multiple apps" call it you must "make sure that one app doesn't use the whole TPM quota and block other apps". A single app can simply have a TPM limit on its deployment. For many, the `llm-token-limit` policy enforces a TPM limit or a token quota over an hour, day, week, month or year, per any counter key: a subscription key, an IP address, or a key from a policy expression. It can also count prompt tokens at the gateway, so a request already over the limit never reaches the backend.

*Adapted from the page's token-limit example, whose figure of 500 is the page's and not a recommendation:*

```xml
<llm-token-limit counter-key="@(context.Subscription.Id)"
    tokens-per-minute="500" estimate-prompt-tokens="false"
    remaining-tokens-variable-name="remainingTokens">
</llm-token-limit>
```

<!-- unknown since=2026-11 -->
The example sets `estimate-prompt-tokens` to false while the prose describes counting prompt tokens in advance, and the page does not say what the setting costs in latency. Nor does it say what a caller receives when the limit trips.
<!-- /unknown -->

### A fallback is routing, not a retry

With backends defined in API Management, the load balancer supports round-robin, weighted, priority-based and session-aware strategies. The page's own use for priority is to "ensure optimal utilization" of Foundry endpoints bought as provisioned throughput. The circuit breaker stops forwarding to a backend that is not responding, and its trip duration is dynamic, "applying values from the `Retry-After` header" the backend provides. The page also warns that the gateway scales only itself: you still scale and distribute the AI backends.

<!-- unknown since=2026-11 -->
Neither page describes client behaviour. Nothing says how a client's retry interacts with a gateway's, whether a gateway retries inside one call, what a caller sees when every backend is tripped, or whether a streamed answer survives a failover halfway through. The quota page, via {{topic:tokenbudget}}, advises retry logic, and the sources go no further. This course's position is to retry only a failure that can succeed on a repeat, to wait for any `Retry-After`, and to cap the attempts so a failing call surfaces as an error the caller can show ({{topic:errors}}).
<!-- /unknown -->

A fallback to a different model is a different model, with different answers. It is not a fallback until it has passed the same evaluation set as the primary ({{topic:evalstrategy}}), and a failover should be visible somewhere a person looks.

### What else a gateway holds

<!-- volatile verified=2026-11 -->
The page lists what sits beside limits. **Managed identity** authenticates to Azure AI services with no keys to store. A **credential manager** handles OAuth for agents reaching APIs or MCP servers, and the gateway can also front an MCP server, an A2A agent or a self-hosted model. A content-safety policy can check prompts. **Semantic caching** stores completions and reuses them when a new prompt is close enough in vector space, which needs Azure Managed Redis, or another RediSearch-compatible cache, and an embeddings deployment. The `llm-emit-token-metric` policy emits token counts with dimensions you choose, such as the caller, and logging can record prompts and completions in Azure Monitor. A preview integration attaches a gateway to a Foundry resource, so token quotas and rate limits can be set in Foundry's own interface. Capabilities vary by API Management tier.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
The page gives no latency figure for the extra hop, no break-even point for adding a gateway, and no word on whether a semantic cache is partitioned by caller. It says nothing on what a logged prompt means for data protection.
<!-- /unknown -->

## In practice at Technik

The capstone has one deployment and one caller. *From [`azure.yaml`, lines 14–22](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/azure.yaml#L14-L22):*

```yaml
    deployments:
      - name: gpt-4.1-mini
        model:
          format: OpenAI
          name: gpt-4.1-mini
          version: "2025-04-14"
        sku:
          name: GlobalStandard
          capacity: 10
```

Nothing in the capstone's own code retries, falls back or sits behind a gateway, and the pages here do not say what unit `capacity` counts in. That suits one agent, since the gateway page says a single app can manage tokens with a limit on the deployment.

The second consumer changes it. Take an invented day at Technik. The Production Assistant answers engineers in daylight. The overnight certificate extraction from {{topic:structured}} runs on its own batch deployment, so its quota is separate and cannot starve the assistant. A pilot for another team shares the assistant's pool. That pilot is the case for a per-consumer limit keyed on the app, and for a second deployment as a priority-ordered backup. The backup would be `gpt-4.1-mini` again, on another resource, the same model, so a failover changes where the answer is computed and not what it says.

The classifier from {{topic:decide}} would not need any of this. At about 40 quality notifications a week, a hosted fine-tune would sit idle and bill for hosting, and a gateway cannot cure that.

## Design guidance

- **Count callers before choosing a gateway.** One app needs a deployment limit. Two sharing a pool need a limit per consumer.
- **Give batch work its own deployment.** Its quota is separate.
- **Prefer a backup that is the same model.** If it is a different model, evaluate it first.
- **Make a failover visible.** Alert when the backup serves traffic.
- **Cap retries and surface the failure** rather than hiding it behind waiting.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| One app gets 429s while another is idle | Callers share one TPM pool with no per-consumer limit | Add a token limit keyed on the consumer |
| An outage takes the app down despite a *Global* deployment | Traffic initially routed to an interrupted region is affected | Add a second deployment or backend, and rehearse the failover |
| Answers change only during incidents | The backup is a different model | Evaluate the backup, and alert when it serves |
| A cached answer is reused for another caller | A semantic cache matches on prompt similarity, and the page does not say it is partitioned | Leave it off for answers that depend on who asks until tested |

## Key terms

**AI gateway**: API Management's set of capabilities for securing, scaling, monitoring and governing AI backends.

**Token limit**: a per-consumer cap in tokens per minute or over a longer period.

**Circuit breaker**: a rule that stops sending requests to a backend that is not responding.

**Semantic caching**: reusing a stored answer for a prompt that is close in meaning to an earlier one.
