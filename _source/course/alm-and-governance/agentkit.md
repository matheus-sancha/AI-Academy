## TL;DR

The Copilot Agent Kit is a toolkit that Microsoft's Power Customer Advisory Team "created and maintains" for
Copilot Studio teams: automated agent testing, conversation KPIs, a compliance hub and an agent inventory,
among other tools. For this module one answer matters. It documents a quality gate inside Power Platform
pipelines, and its test runs sign in in a way that changes your agent's production sign-in.

## What it holds

<!-- volatile verified=2026-11 -->
Test automation configures agents, tests and test sets, runs them in batches and returns latencies, observed
responses and pass or fail results, and supports user-defined rubrics for generative answers. The Compliance Hub
evaluates configurations from the Agent Inventory against controls you set, with actions such as manual review,
quarantine and delete. The test types are in {{topic:csevaladv}}.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
The overview says only "Copilot Agent Kit". The older name, Copilot Studio Kit, survives in a third-party guide
and the repository's name, and no page read here dates the change. The pages give no installation steps, no
support statement beyond who maintains it, and no licence or cost.
<!-- /unknown -->

## The gate, and the sign-in

<!-- volatile verified=2026-11 -->
Microsoft's page on automating tests with pipelines describes a pre-deployment step. A deployment request for a
solution that holds an agent pauses, the kit runs its tests, the results are evaluated and the step decides
whether the deployment proceeds ({{topic:pipelines}}).

Matthew Devaney's guide, from October 2025, sets up the sign-in. The agent configuration uses **Microsoft
Authentication**, which needs an Entra app registration with a single-page application redirect, the delegated
`copilotstudio.copilots.invoke` permission on the Power Platform API, and admin consent. The agent itself must be
switched to **Authenticate with Microsoft**.
<!-- /volatile -->

That last switch is not a test setting. The guide warns that a deployed agent then relies on Entra ID for sign-in
in Teams, SharePoint, Power Apps and Microsoft 365 Copilot.

<!-- unknown since=2026-11 -->
The pipeline page gives no pass mark and no failure behaviour beyond "decides whether to proceed", and no page
shows the kit in GitHub Actions or Build Tools ({{topic:cicd}}). A redirect plus a delegated permission suggests
the run uses a signed-in person's token ({{topic:testidentity}}), but the guide never says so. Nor does any page
say whether the kit can test an agent on the GitHub Copilot harness.
<!-- /unknown -->

## At Technik

The Production Assistant is on the GitHub Copilot harness, so try the kit on a copy before making it the pipeline's
pre-deployment step. The capstone's agent is code and does not use the kit. Its gate is `evals/run.py` in a
workflow ({{topic:cicd}}).

## Design guidance

- **Test the sign-in change** on a non-production copy.
- **Decide the pass mark yourself**, because the kit's page states none.
- **Settle support before depending on it.**

## Key terms

**Compliance Hub**: the kit's policy checks over the agent inventory.

**Test set**: a group of tests the kit runs against an agent in one batch.
