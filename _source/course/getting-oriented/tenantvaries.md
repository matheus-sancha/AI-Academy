## TL;DR

Nothing in this level can tell you what exists in your own environment. Features ship switched off,
entitlements differ by licence, a policy can block a combination that works fine for a colleague, and
the numbers change with the environment type. Treat every tool recommendation — including this
course's — as a claim to check rather than a fact, and learn the three places to check it: your own
environment's lists, the Power Platform admin center, and your administrator.

## Why it matters

This is the standing disclaimer behind every later pitfall that ends *"check your own environment"*,
and the failure mode it describes is specific and demoralising: the documentation describes a feature,
you cannot find it, and you conclude you are doing it wrong.

Usually you are not. It is off, unlicensed, or blocked by policy — and the error message rarely says
so. Recognising that class of problem in five minutes instead of an afternoon is one of the more
valuable habits this level can give you.

## How it works

Four different things vary, and it helps to keep them apart, because each has a different place to
look.

### 1. What is switched on

Features ship behind toggles and previews. Agent Builder can be disabled tenant-wide from the
Microsoft 365 admin center. Developer-environment sign-up can be blocked
({{topic:devenv}}). Web search can be blocked by policy while the interface still shows the setting as
available — a documented UI limitation, and a reliable way to lose an hour
({{topic:agentbuilder}}).

### 2. What you are licensed for

A trial licence lets you build and test but **not publish**. Premium connectors need the right plan.
The Power Apps Developer Plan includes premium and custom connectors but excludes AI Builder and RPA
outright. Skills in an agent created through the Teams app need a standalone Copilot Studio
subscription. None of this is visible from the feature documentation — it lives in the licensing pages
({{topic:licensing}}).

### 3. Which connectors you actually have

This one is widely half-remembered, so it is worth stating exactly.

Microsoft **does** publish a global connector reference — the full catalogue of connectors that exist
is documented, and all of them are described as agent-ready. What is *not* published anywhere is which
of them **your** environment offers you, once licence tier, data policies and administrator decisions
have been applied.

So the published list tells you what *could* exist; only your own environment tells you what *does*.
Search the connector list in your own environment before you design around a connector, and treat the
catalogue as a catalogue rather than an entitlement.

### 4. What the numbers are

Quotas and limits vary by tier and by environment type, sometimes by an order of magnitude:

<!-- volatile verified=2026-09 -->
| Limit | Value |
|---|---|
| Generative AI messages, trial or developer environment | 10 per minute, 200 per hour |
| Generative AI messages, pay-as-you-go | 100 per minute, 2,000 per hour |
| Knowledge sources per agent | 500 across all types |
| Instructions for a Copilot agent | 8,000 characters |
| SharePoint site URLs per agent under generative orchestration | 25 |
| Dataverse knowledge sources per agent | 2, with up to 15 tables each |
| Connector payload | 5 MB — but 450 KB in Government Community Cloud |
<!-- /volatile -->

That last row is the pattern in miniature: a documented number that is simply different in another
cloud.

> [!IMPORTANT]
> Check which **harness** a limit belongs to before you plan around it. The quotas documentation is
> explicitly about the standard harness, so its "100 skills per agent" is a standard-harness skill —
> not an Agent Skill on the GitHub Copilot harness ({{module:agent-skills}}). Same word, different
> thing, and the numbers do not transfer. {{topic:chooseharness}} is where the harnesses are compared.

### Where to look

| Question | Where |
|---|---|
| Does this connector exist for me? | The connector list in your own environment |
| How much capacity do we have, and who is using it? | Power Platform admin center → Licensing → Copilot Studio |
| What is the documented ceiling? | The quotas and limits page for your harness |
| Why is this blocked? | Your administrator — and suspect a data policy first ({{topic:dlp}}) |

The data-policy case deserves singling out: if a tool is blocked, it is often a policy rather than a
bug, and the reason sits where makers rarely look: hover text, or a downloadable details file. Knowing
that a greyed-out option is a *normal* symptom of governance is half the diagnosis.

### How this course handles not knowing

Because this applies to the course as much as to you, every product claim here is sourced one of three
ways: cited to Microsoft documentation, verified in a live tenant, or **marked as unverified**. When
you see a *Not yet verified* note on a page, that is deliberate — it means nobody has checked that
particular claim yet, and you should confirm it in your own tenant before acting on it. Silence would
be worse: a reader told nothing assumes the claim was checked.

## In practice at Technik

Three of the Production Assistant's requirements are tenant-dependent, and all three can be checked
before any design work is wasted:

| Requirement | What to check |
|---|---|
| Query Snowflake for work orders and revisions | That the Snowflake connector exists in your environment, and that data policy permits it alongside the agent's other connectors |
| Package a capability as a skill | That the GitHub Copilot harness is available to you — skills do not exist on the other two ({{topic:chooseharness}}) |
| Route a document revision for approval | That the Approvals connector is permitted in the same policy group as the rest ({{topic:approvals}}) |

This is why the build route's first move is to **check** rather than to configure, and why
{{topic:whenitstalls}} treats a missing connector as an expected outcome with a documented alternative
rather than as a mistake. A plan that names its tenant dependencies up front degrades gracefully; one
that assumes them fails at the point of most sunk cost.

## Design guidance

- **Check before you design, not while you debug.** The checks take minutes and the rework takes days.
- **List your design's tenant-dependent requirements explicitly**, in the brief, where a reviewer can
  see them ({{topic:brief}}).
- **Read every limit together with its harness and environment type.** A number without those two
  qualifiers is not a number you can plan with.
- **Prefer your own environment to the documentation, and the documentation to your memory.**
- **When something is missing, ask "off, unlicensed, or blocked?" before "broken?"**
- **Record what you checked and when.** Entitlements change, and your colleague's tenant is not yours.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The documentation describes a feature you cannot find | Off by default, not licensed, or blocked by policy | Check the admin center, then ask your administrator |
| A connector is in the published catalogue but not in your environment | The catalogue is not an entitlement | Search your own environment's connector list |
| A colleague's exact steps fail for you | Different licence, environment type or data policy | Compare environments before comparing instructions |
| A tool is greyed out, or Publish is unavailable | A data policy, explained only in hover text or a details file | Check DLP before debugging the tool ({{topic:dlp}}) |
| You planned around a limit that turned out not to apply | The limit belonged to a different harness | Re-read it for your harness ({{topic:chooseharness}}) |
| An evaluation run throttles unexpectedly | Developer-environment rate limits | Expected; space the runs ({{topic:licensing}}) |
| Numbers from the documentation do not match your cloud | Government Community Cloud limits differ | Use the limits for your own cloud |

## Key terms

**Tenant** — your organisation's Microsoft 365 and Entra ID boundary; where licences and policies are
decided.

**Environment** — a Power Platform container for agents, flows and data, with its own security,
capacity and quotas ({{topic:envs}}).

**Data policy (DLP)** — the rules deciding which connectors, knowledge sources and channels may be
combined; a blocked tool is often a policy ({{topic:dlp}}).

**Quota** — a rate limit, usually per minute or per hour. **Limit** — a hard ceiling on a count or a
size. Both vary by tier, and both belong to a specific harness.

**Government Community Cloud (GCC)** — a separate cloud with its own, sometimes stricter, documented
limits.
