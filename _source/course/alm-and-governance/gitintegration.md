## TL;DR

Dataverse Git integration is built into the solutions experience. You connect a development environment to
an Azure DevOps or GitHub repository, commit a solution's objects as readable files, and the repository
stops being a backup and becomes the **source of truth**. Managed solutions are built *from* source
control and deployed, and are never edited downstream. Use it in development environments only. For an
agent the payoff is review: an instruction change becomes a diff that someone approves before it reaches
users. What the pages never show is what an agent looks like once it is committed, so the first job is to
look.

## Why it matters

{{topic:solutions}} told you to export the unmanaged solution to source control after every change worth
keeping. That keeps a copy, and it makes nobody read it. When the maker environment is the source of
truth, whoever saved last is the release. Microsoft lists what moving the truth buys: version control,
code review, auditing and traceability, recovery to an earlier state, and short-lived development
environments rebuilt from the repository. An agent's instructions are its behaviour, so the review is the
point. It is also the defence the capstone relies on against a tool that changes after approval, which is
code review and a frozen tag rather than a runtime control ({{topic:mcpsec}}).

## How it works

### What you connect

<!-- volatile verified=2026-11 -->
From the **Solutions** page of a development environment, choose **Connect to Git**. The wizard asks for
a **connection type**, **Solution** or the whole environment, then the organisation, project, repository
and a root Git folder, `src` in the walkthrough. For a solution it then asks for a branch and a folder,
such as `src/<solution>`. Connect another solution later from its own source control page.
<!-- /volatile -->

The overview's two rules are short. Use Git integration with developer environments, never in test or
production, and use builds to create solution artifacts and pipelines to deploy them
({{topic:pipelines}}).

### What lands in the repository

Only **unmanaged** solutions are committed. A managed solution is built from the repository and deployed,
so the repository stays the single place a change can start. Objects are written in a format meant to be
read, and are stored once and shared by every solution in the same repository and folder, not duplicated
per solution. A change shows up in a diff once.

<!-- unknown since=2026-11 -->
Neither page shows an agent after it is committed: which files hold its instructions, tools and
knowledge, and whether a reviewer can read them. The Copilot Studio extension offers another route from an
agent to files, by cloning it ({{topic:csvscode}}), and nothing says whether they are the same files or how the
two interact. Commit a small
change in a development environment and read the diff before you write a review checklist.
<!-- /unknown -->

### Branches and environments

The reference architecture gives the pattern, and it answers a limit in {{topic:pipelines}}, which allows
one development environment per solution.

| Piece | Rule |
|---|---|
| Each development stream | Mapped to its own Git environment or feature branch |
| Merge into `main` | By pull request, under branch protection |
| Feature drift | Accepted changes are pulled back into every development branch |
| `main` | The authoritative source for integration and release |
| Promotion | `main` syncs to the primary development environment, and pipelines take it from there |
| Hotfix | A dedicated environment tracks the current release branch, and the fix merges back to `main` |

So several engineers build in parallel and one environment feeds the pipeline.

### Code-first objects

For plug-ins and controls the guidance is blunt: do not push a built object straight into a development
environment and commit it. The repository then holds the binary through the solution and the source beside
it, and the two drift. Build the object in a pipeline and import the unmanaged result, so the source stays
the single copy. A pro-code agent is that rule applied to the whole project.
Its code never touches Dataverse, so it lives in a repository of its own.

<!-- unknown since=2026-11 -->
The second link configures Azure DevOps. Whether the GitHub connection asks for the same fields has not
been checked, and the connection page for it is not among this topic's sources.
<!-- /unknown -->

## In practice at Technik

Technik keeps two repositories on GitHub, because the two halves of an agent are different artifacts.

| Repository | Holds | A change reaches `main` by |
|---|---|---|
| `technik-agents` | The *Technik Production Assistant* solution, unpacked under `src/` | A pull request from an engineer's branch, read by a second engineer |
| `technik-capstone` | The server and the agent as code | A pull request that runs the evaluation gate ({{topic:cicd}}) |

Each engineer's developer environment has its own branch. Only `main` feeds the pipeline, from the primary
development environment, and a release branch is cut when a build is promoted out of test.

A reviewer of the assistant reads four things: the instruction text, any tool or endpoint added, the names
of connection references and variables, and anything widening who can reach the agent. A pull request
titled *tidy instructions* once also deleted the sentence telling the agent to refuse questions outside
Technik's documents. The diff showed it and the description did not. That is
{{topic:git}}'s rule about reading the diff, not the explanation, applied to an agent whose definition is
mostly prose ({{topic:csvscode}} says to review those definitions like code).

## Design guidance

- **Connect development environments only.** Test and production receive managed builds.
- **Give each engineer a branch and an environment**, and pull accepted changes back into every branch.
- **Protect `main`** with required pull requests, and never let the author be the only reviewer.
- **Treat an instruction diff as a code diff**, and read it for deletions as well as additions.
- **Never commit a build output without its source.** Build it, then import it.
- **Tag the commit a production build came from**, so a deployed version matches a diff.
- **Run a hotfix through its own environment**, and merge it back at once.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The repository and the environment disagree | Someone edited in the environment and never committed | Commit from development only, and edit nowhere else |
| A fix disappears in the next release | The hotfix was never merged back to `main` | Merge the release branch back after every hotfix |
| Two engineers overwrite each other | They share one development environment | One environment and branch each |
| A binary and its source drift apart | Both were committed | Build in a pipeline and import the result |
| A guardrail vanished in a "tidy-up" | Review was approved on the description | Read the diff, and require a second reader |
| An old fix reappears | Accepted changes were not pulled into other branches | Pull `main` into every development branch |

## Key terms

**Git integration**: the native link from a Dataverse environment's solutions to a Git repository.

**Source of truth**: where a change must start. Here it is the repository, not the environment.

**Feature drift**: development branches falling behind what `main` has already accepted.

**Release branch**: the branch a production build was cut from, and where a hotfix is tracked.

**Code-first object**: a plug-in or control built from source, not edited in the maker experience.
