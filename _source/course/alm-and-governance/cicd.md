## TL;DR

An agent's release has two halves, and CI/CD treats them differently. The Power Platform half is a
solution, moved by GitHub Actions for Power Platform or, in Azure DevOps, Power Platform Build Tools.
The pro-code half is code, moved by workflows you write. The Power Platform actions export, import,
deploy, provision environments and run the solution checker. None of them runs an agent's evaluation
set, so the gate that matters is yours. Three rules cover most of it: judge a change before it ships,
because a hosted agent has no canary; keep a change to the baseline in its own reviewed pull request; and
give CI a credential of its own.

## Why it matters

A reviewer reads a diff, and a diff of instructions does not show what the agent now does. Only a run
shows that, and only an automated one happens on every change. The evaluation set you built in
{{topic:testsets}} is worth most when nothing can merge or ship without it. Two facts raise the stakes. A
Foundry hosted agent serves one version at a time with no traffic splitting, so the judgement has to come
before the deployment ({{topic:foundryagents}}). And a coding agent that opens pull requests is productive
only behind a gate it cannot pass by itself ({{topic:git}}).

## How it works

### The Power Platform actions

Microsoft's collection groups its tasks into four types: helper, quality check, solution and environment
management. Together they import and export solutions, including those that hold Copilot Studio agents,
deploy to downstream environments, provision or deprovision environments, and run solution checker
analysis. They support only a Dataverse environment with a database, run on Windows and Linux runners, and
are free apart from your GitHub plan.

They sign in with a secret, and there are two kinds. A username and password cannot pass multifactor
authentication. A service principal with a client secret can. Use the second for anything unattended.
Azure DevOps offers the same tasks through Build Tools, and the Copilot Studio guidance rates its setup
effort as high against moderate for GitHub Actions and low for pipelines
({{topic:pipelines}}).

The reference architecture keeps these tools in a supporting role. It promotes with pipelines, keeps
source in Git ({{topic:gitintegration}}) and uses workflows to build the artifacts both consume.

<!-- unknown since=2026-11 -->
None of the four task types evaluates an agent, and the quality check is the solution checker. Whether a
Copilot Studio agent's test set can be run from a workflow and used as a gate is not documented by this
topic's sources. The same gap appears in Work IQ Dev Tools, whose pipeline sign-in does not cover
evaluations ({{topic:lowvspro}}). The Copilot Agent Kit documents a gate inside a pipeline instead
({{topic:agentkit}}).
<!-- /unknown -->

### The capstone's gate

The capstone writes its own. *From [`.github/workflows/evals.yml`, lines 1–11](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/.github/workflows/evals.yml#L1-L11):*

```yaml
# Stage 4: no change to the agent's instructions, tools, model or data merges without an eval result.
name: Evals

on:
  pull_request:
    paths: ["agent/**", "server/**", "evals/**", "seed/data/**", "tests/**", "infra/**", "azure.yaml",
            "pyproject.toml", "uv.lock", ".github/workflows/*.yml"]
  push:
    branches: [main]
  workflow_dispatch:
  workflow_call:  # stage 5: the release workflow runs this as its gate
```

The path list is the real design. It names everything that can change behaviour: instructions, tools,
evaluation data, seed rows and the workflows themselves. A change to the gate is therefore a change that
triggers it, and a reviewer must read that diff with care. The last line lets another workflow call this
one. The workflow only produces a result. Making that result block a merge is a repository setting, which
no file in the capstone can contain ({{topic:ghharness}} covers branch rules).

*From [`.github/workflows/release.yml`, lines 14–22](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/.github/workflows/release.yml#L14-L22):*

```yaml
jobs:
  gate:
    # The tests and the offline evals; with EVALS_LIVE set, the live evals too. A regression stops here.
    if: vars.SHIP_LIVE == 'true'
    uses: ./.github/workflows/evals.yml
    secrets: inherit

  ship:
    needs: gate
```

Release reuses the gate, and `ship` cannot start unless it passes. What blocks is a *regression* against
`evals/baseline.json`, not a perfect score, because the capstone keeps one case failing on purpose
({{topic:evalharness}}). After the deployment, Foundry's `microsoft/ai-agent-evals` action compares the new
version with the one it replaced and reports in the run summary. It has no threshold, so it cannot be the
gate. The capstone never sets `SHIP_LIVE`, so its workflow ran on its own tag and skipped both jobs.

The baseline needs its own rule. It changes because the agent changed, and if one pull request moves both,
the author has marked their own work. A baseline update is a second, separately reviewed change.

### Credentials for CI

*From [`.github/workflows/evals.yml`, lines 61–90](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/.github/workflows/evals.yml#L61-L90):*

```yaml
    permissions:
      contents: read
      id-token: write
    # …
      - uses: azure/login@v3
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
      - name: Write the agent's Snowflake key
        run: |
          mkdir -p keys
          printf '%s\n' "$SNOWFLAKE_PRIVATE_KEY" > "$SNOWFLAKE_PRIVATE_KEY_FILE"
        env:
          SNOWFLAKE_PRIVATE_KEY: ${{ secrets.SNOWFLAKE_PRIVATE_KEY }}
```

The live job holds two credentials of two kinds. Azure gets three identifiers and no secret. Snowflake
gets a private key, held as a repository secret and written to disk for the run. Each answers the same
question: what could a job do with this, if someone altered the workflow?

<!-- unknown since=2026-11 -->
The Azure step is written for a federated credential and has never signed in, since the capstone is
tested offline only ({{module:capstone-build}}).
<!-- /unknown -->

## In practice at Technik

| Change | Gate | Who decides |
|---|---|---|
| The Production Assistant solution | A pull request to `technik-agents`, a workflow that builds it and runs solution checker, then the Power Platform pipeline | A second engineer, then the production approver |
| The server or the agent | The `Evals` workflow on the pull request, again on release | The reviewer, and a baseline that no one edited in the same change |
| A skill | `skills-ref validate` in CI ({{topic:skillgov}}) | The skill's owner |
| A Foundry toolbox promotion | Treated as a release of every agent that uses it ({{topic:foundryagents}}) | The agent's owner |

Order matters when one change touches both halves. The server ships first, so the tool exists before
anything calls it. Then comes the connector's solution, then the assistant's.

## Design guidance

- **Make the gate cover everything that changes behaviour**, including the workflow files.
- **Judge before you deploy.** A hosted agent has no canary.
- **Block on regression against a baseline**, and report the rest.
- **Change the baseline in its own pull request**, never beside the code it measures.
- **Give CI its own identity** with the least role that runs the job, and prefer one with no stored secret.
- **Use a service principal for unattended Power Platform jobs**, since a password account cannot pass multifactor.
- **Read workflow diffs as carefully as code**, because they decide what the gate checks.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A change merged with no evaluation result | The workflow runs but the repository does not require it | Require the check in branch rules |
| A regression was blessed | The code and its baseline changed in one pull request | Split the baseline update out |
| The gate passes after a model change | No path or schedule sees a model update | Add a scheduled run ({{topic:evalstrategy}}) |
| A solution deploys and the agent misbehaves | Only the solution checker ran | Add an evaluation step you wrote yourself |
| A password-based job fails sign-in | The account needs multifactor | Use a service principal and client secret |
| A release shipped a bad version, and nothing rolled back | The report ran after the deploy and does not block | Gate before deploying, and keep the previous version |

## Key terms

**Gate**: a check a change must pass before it merges or ships.

**Baseline**: the saved per-case results a new run is compared against.

**Regression**: a case that passed in the baseline and fails now.

**Service principal**: an application identity for unattended jobs.

**Workflow call**: one workflow reusing another as a job.
