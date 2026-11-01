## TL;DR

Git stops being optional the moment two things become true at once: an agent writes code faster
than you read it, and your agents themselves are files. The fundamentals are the fundamentals —
branch, commit, pull request, review — and the curated Git module below teaches them. What changes
in this work is **what the review is for** and **what the repository must never hold**. Review
stops being a quality check on a colleague's reasoning and becomes the only place a machine's
output is read by a human. And because credentials now live beside the code, GitHub's secret
scanning and push protection move from nice-to-have to part of the design.

## Why it matters

Three things arrive together at this level, and each on its own would justify source control.

**The diffs got bigger and cheaper to produce.** An agent session can change nine files in two
minutes. The volume is not the problem; the plausibility is. Generated code reads well and compiles,
so the defects that survive are the ones that look right — a wrong table, a dropped filter, an
assumption that held in the example and not in your data. Small, frequent commits let a reader see
each decision instead of a wall.

**The agent is now a file.** A cloned Copilot Studio agent is YAML ({{topic:csvscode}}), an MCP
server is Python, instructions are Markdown. A behaviour change is a diff — reviewable, attributable
and revertible — which also means a careless merge changes how a production agent behaves.

**Secrets are on disk.** {{topic:localenv}} put them in an ignored file. Git is what enforces that,
and GitHub is what catches the day it fails.

## How it works

### The fundamentals, briefly

The working tree, the staging area and the commit as a snapshot; `git status`, `git add`,
`git commit`, `git log`, and `git <command> --help` when stuck. The Microsoft Learn module in *Go
deeper* covers that properly, including configuring your identity and working with branches. If Git
is new to you, do it first — the rest of this level assumes it.

### Reviewing what a machine wrote

The discipline differs from reviewing a colleague's work in three ways.

**Review the diff, not the explanation.** An agent's summary of its own change describes what it
intended. That is useful context, not evidence.

**Commit in small pieces.** One commit per idea is good practice generally and load-bearing here,
because it is the only thing that makes a bad change revertible without unpicking four good ones.

**Keep a gate the agent cannot pass by itself** — a pull request with a human reviewer and a CI run
that executes the tests. {{topic:cicd}} builds this out; what matters now is that the gate exists
before the agent is productive, not after.

### Secrets: two different mechanisms

<!-- volatile verified=2026-11 -->
**Secret scanning** looks for credentials that are already there. It scans the entire Git history on
all branches, and also issues, pull requests, discussions, wikis and secret gists, re-scanning when
new secret types are added. On **public repositories it runs automatically and free**. For
organisation-owned private and internal repositories it comes with GitHub Secret Protection on Team
or Enterprise plans. Detected partner credentials are reported to the issuing provider so they can
revoke them, and those are not shown as repository alerts.

**Push protection** tries to stop the commit arriving at all, blocking the push and explaining why.
It comes in two forms, and the difference matters:

| Form | Default | Scope |
|---|---|---|
| **For repositories** | Disabled; enabled by a repository admin, organisation owner, security manager or enterprise owner. Requires GitHub Secret Protection | Blocks pushes to that repository and raises bypass alerts |
| **For users** | **Enabled by default**, on GitHub.com | Stops *you* pushing a secret to a **public** repository. Raises no alert unless repository-level protection is also on |

Anyone with write access can bypass repository push protection by giving a reason, and the reason
determines what happens: *used in tests* and *false positive* close the alert, while *I'll fix it
later* leaves it open. A bypass writes an audit-log entry and emails owners, security managers and
watching administrators.
<!-- /volatile -->

The remediation order is the part people get backwards. **Rotate the credential first.** GitHub's
own guidance is that rewriting history is time-intensive and often unnecessary once the credential
is revoked — and a secret pushed to a public repository should be assumed read the moment it
landed.

## In practice at Technik

The capstone repository is public, which makes this concrete rather than theoretical: secret
scanning runs on it automatically and at no cost, and user-level push protection is already standing
between an engineer and a key in a commit.

What it must never hold is enforced by three lines of configuration rather than by care: the `.env`
holding the Snowflake account and Foundry endpoint, and `keys/`, holding the service user's private
key ({{topic:localenv}}). It can be public because Technik is fictional and every value is invented
— a policy worth copying, since a training repository with one real account identifier in its
history is indistinguishable from a leak.

Two review gates are wired in. The evaluation workflow runs the server tests, the agent tests and
the offline evaluations on every pull request touching the agent, the server, the evaluations or the
data, so a change that breaks a graded behaviour fails before a human reads it
({{topic:stageevals}}). And the evaluation **baseline** is a committed file: when a result changes
legitimately, the new baseline is a diff somebody approves. That is this level's clearest example of
the pattern worth taking away — *the thing that decides whether behaviour is acceptable is itself
under review*.

The agent-mode risk closes here too. An editor agent with repository access can read `.env` and
write a file. Push protection is the net below that, not the plan; the plan is that the agent asks
first, and the identity it could leak is read-only anyway ({{topic:sfroles}}).

## Design guidance

- **Branch for every change, including an agent's.** The default branch is not a workspace.
- **One idea per commit.** Revertibility is the whole return on this discipline.
- **A human reads every diff before merge.** Not the agent's summary — the diff.
- **Add the ignore rules before the first commit.** Retrofitting them does not remove history.
- **Turn on push protection at the repository level**, since the per-user default does not cover
  private repositories.
- **Rotate first, clean up second.** Treat an exposed credential as used.
- **Commit the lock file, the evaluation set and the baseline.** They are decisions, and decisions
  deserve review.
- **Write commit messages that say why.** With a machine producing the *what*, the *why* is the part
  only you can record.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A secret is in the history of a public repository | It was committed before the ignore rules existed | Rotate the credential immediately, then clean up if still warranted |
| Push protection did not fire on a private repository | The per-user default covers public repositories only | Enable push protection for the repository |
| A bypass went unnoticed | The reason given closed the alert | Review bypass alerts and the audit log; treat *used in tests* as a claim to check |
| An agent's change broke a behaviour nobody tested | The pull request had no test gate | Run the evaluation set in CI on every pull request ({{topic:cicd}}) |
| Review was approved on the agent's description | The summary was read instead of the diff | Require the diff to be read; keep changes small enough that this is realistic |
| Evaluation results changed and nobody knows why | The baseline was updated in the same commit as the code | Keep baseline updates as their own reviewed change |
| A cloned low-code agent lost work | It was never committed after cloning | Commit immediately after a clone ({{topic:csvscode}}) |

## Key terms

**Working tree, staging area, commit** — your files, the changes marked for the next snapshot, and
the snapshot.

**Pull request** — the review gate where a change is read by a person before it reaches the default
branch.

**Secret scanning** — detection of credentials already present, across the whole history. Free and
automatic on public repositories.

**Push protection** — blocking a push that contains a detected secret, before it reaches the
repository.

**Bypass** — overriding push protection with a stated reason, which is alerted and audited.

**Baseline** — the committed record of accepted evaluation results, reviewed like code
({{topic:stageevals}}).
