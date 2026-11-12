## TL;DR

An agent's bill has several meters, and each one fails differently when it runs out. **Copilot Credits** meter
Copilot Studio agents and can stop an agent, or only its flows. **AI Builder credits** meter AI actions in flows
and apps, and an action simply fails. **Foundry** meters model use by token, or by reserved capacity that you
pay for whether or not anyone calls it. {{topic:licensing}} taught what your environment is billed on. This
lesson is about the limits, the reports and the failure modes, because only some of the meters can be capped,
and none of the pages reports a cost per conversation.

## Why it matters

Cost surprises look like outages. An agent that goes quiet on the 20th, a flow that fails while the agent still
answers, a throttled model deployment: each is a meter doing what it was told. An engineer who has not read the
rules reads them as bugs. The second reason is design. Whoever decides how many tool calls a turn may make is
deciding what a turn costs ({{topic:contextcost}}).

## How it works

### Copilot Credits

<!-- volatile verified=2026-11 -->
Copilot Credits "measure agent usage". One interaction can use several, because each feature it touches has its
own rate, and some features bill per 1,000 tokens instead. The only rate on the capacity page is for reasoning
models: 10 credits per 1,000 billed tokens, so 12,000 credits is about 1,200,000 tokens, though prompt tools on
the same model do not convert this way. Per-feature rates live on a separate billing-rates page. Agents on the GitHub
Copilot harness appear as "Process Agents" in the licensing report.

Capacity is **prepaid**, in packs pooled across the tenant and assigned to an environment before its agents work,
or **pay-as-you-go**, billed through a plan to an Azure subscription. When an environment runs out, you choose an
overage source: draw from the tenant's unallocated pool, or bill the pay-as-you-go plan. With neither, features
"can stop working". Agent flows are checked separately: with no credits, new flow runs are blocked while the
parent agent keeps answering.
<!-- /volatile -->

### The one hard stop

<!-- volatile verified=2026-11 -->
In the Power Platform admin center, **Licensing** > **Copilot Studio** > **Summary** > **Manage Agents** sets a
monthly limit on a single agent, in prepaid or pay-as-you-go environments. It has two guardrails: notifications
to administrators as usage nears the limit, and a **hard stop** that turns the agent off. Two caveats are on the
page. An agent's limit does not stop the flows it calls, and limits "aren't applied instantly", so the agent can
answer for a while past it. Set thresholds with margin.
<!-- /volatile -->

Reports come in three kinds, by environment, agent and user, and the page says to start with the environment
report and drill down. Columns include agent, AI feature, channel, model, knowledge source or tool, and billed and
non-billed credits.

<!-- unknown since=2026-11 -->
The reports do not show one conversation or one message, and they carry no token counts. An agent's Monitor page
shows billed credits only. So the roadmap's "cost per conversation" is not available from Copilot Studio's own
reporting, and the pages do not say where else to get it.
<!-- /unknown -->

### AI Builder credits

<!-- volatile verified=2026-11 -->
AI Builder credits run AI actions in Power Apps and Power Automate, and an AI prompt can draw on them or on
Copilot Credits. New customers "can't purchase" the add-on and must buy Copilot Credits. When an environment
overruns, the system tries Copilot Credits first. If none exist, the action fails with errors such as
`EntitlementNotAvailable` or `QuotaExceeded`. Overage is never charged and counting resets on the 1st. An
environment with allocated credits uses only those: it does not fall back to the tenant pool.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
The page's dates have passed. Renewing the add-on was possible "up to November 1, 2026", and seeded credits "will
be removed" on that day, yet the page also says existing ones are honoured through the end of the contract term.
How seeded credits behave now is unchecked.
<!-- /unknown -->

### Foundry capacity

<!-- volatile verified=2026-11 -->
A Foundry deployment is **Standard** (pay per token, no latency guarantee), **Priority**, **Provisioned** or
**Batch** (discounted, asynchronous). Provisioned throughput holds a fixed amount of capacity, measured in PTUs,
"whether or not requests are being made", billed per PTU per hour "regardless of the number of tokens consumed".
The page recommends it for predictable, latency-sensitive production traffic and Standard for development, low
volume or variable traffic ({{topic:deploytypes}}).

Three details bite. **Quota is not capacity**: having PTU quota "doesn't guarantee that capacity is available",
and capacity released by scaling down may not come back. **Reservations** discount the PTU meter for one month or
one year, are bought per deployment type and scoped to subscriptions or resource groups, and do not guarantee
capacity, so create the deployment first. **Spillover** sends overflow from a provisioned deployment that returns
errors such as 429 to a Standard deployment in the same resource. Reservation utilisation in Cost Management is
the monitor the page names, and it gives no per-conversation figure either.
<!-- /volatile -->

Sizing starts from requests per minute, average input and output tokens and the cache rate, because output tokens
take more capacity than input ones. The page does not give minimum sizes or tokens-per-PTU values, and the
latency target it promises carries no number.

## In practice at Technik

| Meter | What uses it | Exhausted, it | Seen in |
|---|---|---|---|
| Copilot Credits | The Production Assistant, per interaction and per feature | Stops the agent at its hard stop, or blocks its flows | Admin center reports; Monitor shows less |
| AI Builder credits | A prompt in a Technik flow, if one is used | Fails the action | The consumption report |
| Foundry tokens | The capstone's model calls | Nothing: the pages describe no cap | Traces; Cost Management |
| Reserved PTUs | Nothing yet | Returns 429, or spills over | Reservation utilisation |
| Snowflake credits | `TECHNIK_AGENT_WH` | Per resource monitor ({{topic:sfcost}}) | Snowflake usage views |

The capstone's tests cost nothing, since a fake stands in for the model and Snowflake. A per-conversation figure
for the code half would come from its traces, which record tokens ({{topic:tracing}}), multiplied by the model's
price. For the low-code half it does not exist. Give the Production Assistant a hard stop with margin. Notifications go to administrators, not to the owner
({{topic:agent365}}), so someone has to pass them on.

## Design guidance

- **Set a per-agent limit with margin**, since limits are not instant and do not stop flows.
- **Choose each environment's overage source** on purpose, so exhaustion is a decision.
- **Allocate AI Builder credits knowing they never spill** to the pool.
- **Start on Standard**, and reserve capacity only for traffic you can predict.
- **Create a provisioned deployment before buying its reservation.**
- **Build per-conversation cost from traces**, because no report gives it.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent went quiet mid-month | Its hard stop was reached | Raise the limit, and alert earlier |
| The agent answers but flows fail | The environment has no credits, which blocks new flow runs | Reallocate, buy credits or enable pay-as-you-go |
| Spend rose past the limit | The limit is not applied instantly | Leave margin below the real ceiling |
| An AI action fails with `QuotaExceeded` | The environment's own allocation is spent | Reallocate, or add Copilot Credits |
| A PTU deployment will not create | Quota exists but capacity does not | Use fewer PTUs, another region or retry later |
| Requests return 429 on a provisioned deployment | Its PTUs are exhausted | Enable spillover, or add PTUs |
| You scaled down overnight and cannot scale back | The released capacity was taken | Hold the size, or reserve |

## Key terms

**Copilot Credit**: Copilot Studio's unit of agent usage.

**Billing plan**: the grouping of environments billed pay-as-you-go to an Azure subscription.

**PTU**: a provisioned throughput unit, a fixed amount of Foundry model capacity.

**Spillover**: overflow from a full provisioned deployment into a Standard one.
