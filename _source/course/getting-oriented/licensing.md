## TL;DR

**Copilot Credits** are the currency across Copilot Studio: one credit is one request that prompts a
response or an action, and complex tasks cost more than simple ones. Credits are pooled at tenant
level, assigned to an environment, and enforced monthly — unused prepaid capacity does not carry over.
Two facts matter more to you than the monthly bill: running out of capacity is a *failure mode that
looks like a bug*, and a developer environment has the tightest rate limit of any tier.

## Why it matters

You are about to run the same evaluation set repeatedly — after an instruction change, after adding a
tool, after switching the model. That is the correct way to work ({{topic:whyeval}}), and it is also
the reason engineers meet capacity limits before end users do.

More importantly, capacity exhaustion does not announce itself as a billing problem. It shows up as an
agent that used to call a flow and quietly no longer does, or a run that stalls and then works fine an
hour later. Not knowing that shape costs you a day debugging your instructions.

## How it works

### What a credit is

<!-- volatile verified=2026-09 -->
Microsoft's definition is narrow and worth quoting: a Copilot credit "represents a single interaction
between a user and a Copilot agent, counted as one unit of consumption" — a request that prompts a
response or action. The number counted for each response depends on the complexity of the task, so
retrieving from knowledge, calling a tool and running a flow are not all one credit each.

Copilot Credits replaced *messages* as the common currency on 1 September 2025, which is why some quota
tables still say "message packs".
<!-- /volatile -->

### How you get into Copilot Studio at all

Four documented routes, and they are not equivalent. A **Copilot Studio user licence** is free of
charge, but the tenant needs a prepaid Copilot Credit pack subscription before it can be assigned. The
**Copilot Studio authors** role is granted to a security group in the Power Platform admin center. A
**Microsoft 365 Copilot licence** also covers extending Microsoft 365 Copilot with agents. And a
**trial licence** lets you build and test in the test chat panel — but **cannot publish**, which
catches people out at the end of a build rather than the beginning.

### Where credits come from, and where they go

Credits arrive three ways: **pay-as-you-go** through an Azure subscription and a billing policy,
a one-year **prepurchase plan**, or **prepaid Copilot Credit packs**. However they arrive they are
pooled across the tenant, and an administrator must **assign** them to an environment before agents
there can use paid features.

Then two enforcement mechanisms sit on top, and both can stop your agent:

- **Monthly capacity.** Prepaid capacity is enforced per month and unused credits do not carry over.
  When an environment exhausts its allocation, an administrator has already chosen whether it may draw
  from the tenant's pool, bill to pay-as-you-go, or neither. With neither, the documentation is blunt:
  experiences that require credits can stop working.
- **Per-agent monthly limits.** An administrator can cap an individual agent, with notifications as
  it approaches the cap and a **hard stop** that turns the agent off when it reaches it.

There is one partial failure worth memorising because it is so confusing in the moment. When prepaid
capacity is exhausted, **new agent flow runs are blocked while the parent agent keeps answering
everything else**. The agent appears healthy and merely seems to have forgotten one of its
capabilities.

### Reading consumption

Consumption lives in the Power Platform admin center under **Licensing** → **Copilot Studio**, across
all harnesses. You can download reports organised by environment, agent or user; start with the
environment report to find where consumption is happening, then narrow with the agent report. The
detailed report breaks usage down by agent, feature, channel, model and tool — and it distinguishes
**billed** from **non-billed** credits.

**Building, testing and evaluating are billable.** The GitHub Copilot harness documentation states it on
every page it applies to: *"Usage-based billing applies to using, building, testing, and evaluating agents.
These actions might consume Copilot Credits."* A repeated evaluation run is a real cost, not a free
rehearsal. What is not published is the **rate**, so watch your own report across one full run before
budgeting several.

<!-- verified tenant=2026-10 -->
That charge is the GitHub Copilot harness's. On the standard harness, testing in the test panel and running
evaluations consume no Copilot Credits.
<!-- /verified -->

### Zero-rated usage

One genuine discount is documented. With a Microsoft 365 Copilot licence, using agents in Copilot Chat,
Teams or SharePoint for *classic answers*, *generative answers* or *Microsoft Graph tenant grounding*
does not count against the Copilot Studio pack or meter. It is channel- and feature-specific, which has
a sharp edge: an agent that is free in Teams is not free on a website, so a pilot built entirely on
zero-rated paths tells you nothing about what shipping costs.

### The limit that bites first

Cost is not the only budget. Generative AI messages are rate-limited per environment, and the spread
is wide.

<!-- volatile verified=2026-09 -->
Trial and developer environments are capped at roughly 10 requests per minute and 200 per hour, while
pay-as-you-go environments and Microsoft 365 Copilot users get 100 per minute and 2,000 per hour.
<!-- /volatile -->

You will be building in a developer environment ({{topic:devenv}}) — the tightest tier by an order of
magnitude, and the single most common reason a long evaluation run behaves strangely.

## In practice at Technik

The Production Assistant covers seven capability areas, so an evaluation set that treats each one
seriously — happy path, an edge case, a refusal — runs to roughly twenty-five cases
({{topic:testsets}}). Across a build you will run it four or five times.

Every case is an agent conversation; several call a tool, and the document-revision case calls a flow.
On a developer environment capped at 200 requests an hour, two runs back to back will throttle — so a
run that appears to hang is a quota hypothesis before it is a defect hypothesis.

Two consequences follow. The document-revision flow draws on the Developer Plan's own monthly flow-run
allowance as well as on credits, so it has two budgets. And AI Builder — used on supplier material
certificates in {{module:automation-and-workflows}} — is not part of the Developer Plan at all, so that
work needs a trial rather than a credit top-up.

## Design guidance

- **Find out what your environment is billed on before the fourth evaluation run**, not after.
- **Watch your own consumption report across one full evaluation run.** It answers, for your tenant,
  the question the documentation leaves open.
- **Set a per-agent monthly limit on anything shared**, and decide which failure you want.
- **Enable an overage source, or accept that month-end can stop the agent.** Silence is a choice here.
- **Budget flows separately from the agent.** They fail separately, and they fail first.
- **Never demo only on zero-rated paths.** Price the channel you intend to ship on.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent answers normally but a flow silently does nothing | Prepaid capacity exhausted: new flow runs are blocked while the parent agent continues | Reallocate capacity, buy more, or enable pay-as-you-go |
| The agent stopped entirely, late in the month | Monthly enforcement with no overage source, or a per-agent hard stop | Configure an overage source; check the agent's monthly limit |
| Everything is built and you cannot publish | Trial licence — building and testing only | Move to a licence that permits publishing |
| A long evaluation run stalls, then works later | Requests-per-hour quota on a developer environment | Space the runs, or run on a higher tier ({{topic:devenv}}) |
| Credits are draining and nobody knows what is using them | Only the tenant summary was read | Download the environment report, then the agent report |

## Key terms

**Copilot Credit** — one unit of consumption: a request that prompts a response or action, priced by
task complexity.

**Prepaid capacity** — credits bought in advance, pooled at tenant level, assigned per environment,
enforced monthly, and not carried over.

**Pay-as-you-go** — billing Copilot Studio usage to an Azure subscription through a billing policy,
with no upfront commitment.

**Overage source** — where an environment draws credits once its allocation is exhausted: the tenant
pool, a pay-as-you-go plan, or nothing. With nothing, paid features stop.

**Hard stop** — an administrator's per-agent monthly limit that turns the agent off on reaching it.
