## TL;DR

GitHub Copilot is not one agent but one account's agent reachable from several places: the editor, the
terminal, and GitHub.com and GitHub Mobile. Your work and context carry across them, and the
documentation stops short of calling them the same agent — what differs between them is what matters
anyway. **Autonomy, tools and the review point move together.** In the terminal you approve each tool
call and see every command. In a programmatic run you approve nothing and read the result. In the
cloud the agent works in an environment you do not own and the review point is a pull request, with a
hard 59-minute ceiling on an Actions session and one pull request per task.

## Why it matters

Choosing a surface is choosing how much you will review, and people pick by convenience rather than by
that. A task delegated to the cloud comes back as a pull request, which is a good review point; the
same task run with `--allow-all-tools` in your home directory has no review point at all and your
credentials in reach.

The limits also decide what you can delegate. One pull request per task is an architectural fact, not
a quota: a change spanning the server and the evaluation baseline cannot be one delegated task. A
59-minute ceiling is a design constraint on your test suite. Neither is negotiable — "This limit cannot
be extended or bypassed."

## How it works

### The terminal

Copilot CLI runs on Linux, macOS, and "Windows from within Powershell and Windows Subsystem for
Linux (WSL)". It starts interactive, in ask/execute mode, with a **plan mode** that "will build a
structured implementation plan" and asks clarifying questions "before writing any code" — the review
point moved earlier, before any edit exists ({{topic:planning}}).

<!-- volatile verified=2026-11 -->
Approvals are per tool request: *Yes*, *Yes, and approve TOOL for the rest of the running session*, or
*No, and tell Copilot what to do differently*. Session approval is asked again in new sessions. The
flags work interactively and programmatically:

```powershell
copilot -p "Summarise this week's commits" --allow-tool='shell(git)' --deny-tool='shell(git push)'
```

`--allow-all-tools` allows anything; `--deny-tool` takes precedence over both allow forms. Arguments
take the form `shell(COMMAND)`, a first-level subcommand for `git` and `gh` such as `shell(git push)`,
`write` for non-shell tools that modify files, or a server name as `MCP_SERVER_NAME(tool_name)`.
`/permissions assisted` has a model judge approve requests it deems safe; `/sandbox enable` restricts
filesystem, network and system capabilities; `--cloud` runs the session in a GitHub-hosted environment
instead of on your machine.
<!-- /volatile -->

Two cautions deserve repeating. "Copilot has the same access as you do to files on your computer", and
of the trusted-directory scoping: "Typically, you should not launch Copilot CLI from your home
directory", because "Scoping of permissions is heuristic."

Context is managed for you: the conversation auto-compacts as it "approaches 95% of the token limit",
with `/compact` and `/context` to do it by hand ({{topic:history}}). Models used must support tool
calling and streaming, with a recommended context window of at least 128k tokens.

### GitHub.com and GitHub Mobile

Since 28 October 2026 the cloud experience needs a paid Copilot plan, and "Without write access to a
repository, your Copilot session is read-only." You start work from the Copilot panel in a file, issue
or pull request, from a repository's Agents tab, or from Mobile. Copilot "works against the repository
and branch you provided", and you can review proposed changes and ask for refinements before any pull
request exists — or request one in the prompt.

The environment is a real choice with real consequences:

| | Cloud sandbox | GitHub Actions-based |
|---|---|---|
| Repositories | Can work across several in one org | "Copilot can only make changes in the repository specified when you start a task" |
| Session limit | Not stated | 59 minutes maximum, which "cannot be extended or bypassed" |
| Chat data | Retained for the life of the account | Retained for 28 days |
| Compute | No custom compute or self-hosted runners | Custom compute, network and setup; self-hosted runners |
| Personalization | Dotfiles, connectors, personal MCP servers | Not available |

Both support custom instructions, MCP servers and content exclusions. Both are bounded the same way on
output: "Copilot can only work on one branch at a time and can open one pull request per task."

Beyond delegated changes there are three related surfaces: **Copilot code review**, which reviews a
pull request's changes and suggests fixes; **Agent Merge**, which "watches a pull request and works on
the blockers you select: failed GitHub Actions workflows, merge conflicts, or both"; and
**automations**, a task defined once and run on a schedule or on repository events. Session logs show
the work and the tools used, with the caveat that "Logs do not replace your own review and testing."

## In practice at Technik

The capstone repository gives each surface a job that suits its review point.

The editor keeps anything whose correctness you must read line by line. The streaming fix to
`grounded_or_refuse` is twelve lines that decide whether an ungrounded answer reaches a production
planner; that is a diff to review, not a task to delegate ({{topic:loop}}, {{topic:agentmode}}).

The terminal takes read-only work where the command matters more than the reasoning — the invocation
above, run from the repository root rather than your home directory, with `git push` denied so nothing
can leave the machine even if the model decides it should.

The cloud takes the self-contained, reviewable units. Two capstone realities shape what those can be.
The evaluation suite is well inside the Actions ceiling today — 20 root tests, 11 in `agent/`, and
eight eval cases — but a suite that grows past an hour would stop being delegable, which is a reason to
keep it fast rather than thorough ({{topic:evalharness}}). And the one-pull-request rule means the
baseline and the behaviour it measures cannot move in a single delegated task: `evals/baseline.json`
changes because the agent changed, so either one task changes both files or the baseline update is a
second, human-reviewed pull request ({{topic:cicd}}).

Rulesets are the last thing to check before delegating. A branch protection rule on `main` "can prevent
Copilot from creating or updating pull requests", and a repository admin can configure a bypass for
Copilot. Technik would deliberately not grant that bypass: the whole value of the cloud surface is that
its output arrives as something a person merges ({{topic:git}}).

## Design guidance

- **Match the surface to the review you intend to do.** If you will not read the diff, do not pick a
  surface whose only safeguard is that you might.
- **Never launch the CLI from your home directory**, and prefer an explicit allow list to
  `--allow-all-tools`.
- **Deny the commands that leave the machine** — `git push` above all — in any programmatic run.
- **Size delegated tasks to one branch and one pull request.** Split anything that touches a
  measurement and the thing it measures.
- **Keep the test suite inside the session ceiling**, or accept that it cannot run in a delegated
  session.
- **Do not grant a ruleset bypass to the agent** unless you have another gate.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A programmatic run did something destructive | `--allow-all-tools` with no deny list | Allow named tools; deny `shell(rm)`, `shell(git push)` and the like |
| The agent touched files outside the project | The CLI was launched from a parent or home directory | Launch from the repository root; trusted-directory scoping is heuristic |
| A delegated session was cut off mid-run | The 59-minute Actions ceiling | Shorten the task, or use a cloud sandbox session |
| A task needed changes in a second repository | Actions sessions are limited to the one repository | Use a cloud sandbox session, or split the work |
| Copilot cannot open a pull request | A ruleset or branch protection rule blocks it | Decide deliberately whether to configure a bypass |
| A remote-controlled CLI session stopped | The session runs on your machine, which must stay online | Start it in the cloud instead |

## Key terms

**Surface** — one of the places the same account's agent is reachable: editor, CLI, GitHub.com, Mobile.

**Programmatic mode** — a non-interactive CLI run started with `-p`, which completes the task and exits.

**Plan mode** — the CLI mode that builds a structured implementation plan before writing code.

**Cloud sandbox** — a GitHub-hosted environment for a session, able to span repositories in one
organization.

