## TL;DR

You shape a harness mainly through files it discovers in your repository: always-on project
instructions (`.github/copilot-instructions.md` or `AGENTS.md`), targeted instruction files that
attach themselves when a glob or a description matches, prompt files you invoke as slash commands, and
custom agents that bundle instructions with a restricted tool list. The rule that catches people is
that **discovery is per-harness and additive, with no general precedence order** — so a conflict
between two files is not resolved by any rule you can rely on. And one capability does not travel:
"Prompt files run only in Local harness sessions in the Chat view." For a reusable task on any other
harness, the answer is a skill.

## Why it matters

This is the cheapest lever you have on agent quality. An agent that keeps proposing plausible, wrong
changes usually lacks repository context, not reasoning — and a committed file fixes it for everyone
who clones the repo, which a better prompt does not.

It is also the only part of harness configuration that belongs under review. Approvals and tool sets
live in your user profile and move with you rather than with the project; instructions, prompt files
and custom agents are files in the repository, so they get a diff, a reviewer and a history
({{topic:git}}).

The caveat has to arrive with the capability. None of this is enforcement. The documentation says of
verification that it "verifies discovery, but not whether the instructions are followed" — the file
reliably reaches the model, and the model reliably decides what to do with it. Rules that must hold
belong in code ({{topic:loop}}).

## How it works

### Always-on project context

Two file names do the same job for the Copilot harness: `.github/copilot-instructions.md` at the
repository root, and `AGENTS.md`, also at the root. For Copilot, `AGENTS.md` instructions are
discovered "at the repository root, the session's working directory, and intermediate directories
between them", and Copilot "combines applicable instructions from `AGENTS.md` and other supported
instruction files". Other harnesses read their own: Claude reads `CLAUDE.md` and Markdown in
`.claude/rules`, Codex reads `AGENTS.md` and nested ones in subfolders.

`AGENTS.md` is not a Microsoft format. It is an open one, "used by over 60k open-source projects" and
stewarded by the Agentic AI Foundation under the Linux Foundation, with VS Code among its listed
supporters. Its own rule for nesting is "the closest AGENTS.md to the edited file wins; explicit user
chat prompts override everything" — a monorepo puts one in each package ({{topic:openformat}}).

### Targeted instruction files

Files named `*.instructions.md` under `.github/instructions` (searched recursively) carry optional
front matter, and the keys are what makes them targeted:

<!-- volatile verified=2026-11 -->
```markdown
---
name: 'Seed data'
description: 'Use when changing the capstone seed or its CSV fixtures.'
applyTo: 'seed/**'
---
Every figure quoted in a lesson comes from these rows. Changing a value breaks a lesson.
```

`applyTo` is a glob relative to the workspace root, and VS Code attaches the file "when its `applyTo`
pattern matches a file that the agent creates or modifies" — not merely one you have open. With a
`description` and no `applyTo`, the agent loads it when the description matches the task. With neither,
the file has to be attached by hand. Claude's `.claude/rules` files use `paths` instead, an array that
"defaults to `**` when omitted".
<!-- /volatile -->

On the Local harness, `chat.useAgentsMdFile` is enabled by default and
`chat.useNestedAgentsMdFiles` is disabled and experimental; neither controls Copilot's own discovery.

The precedence warning is explicit and unusual: "Applicable instruction sources are additive", and "Do
not depend on a file order or precedence rule to resolve conflicts because discovery and merge
behavior can differ by harness." Two files that disagree are a bug in your repository, not a question
for the documentation. One more boundary: custom instructions "are not taken into account for inline
suggestions as you type in the editor."

### Prompt files and custom agents

A prompt file is a `.prompt.md` in `.github/prompts`, invoked by typing `/` and its name, or by
**Chat: Run Prompt**. Its front matter can pin the `agent`, the `model` and a `tools` list, and its
body takes `${input:variableName}`, `#file:` references and `#tool:` references. Unavailable tools are
simply ignored at run time.

The restriction is the headline: prompt files run only in Local harness sessions in the Chat view, and
"Authoring a `.prompt.md` file in a Copilot session doesn't make that file runnable by the Copilot
harness." The documented alternative is to "create an agent skill or convert an existing prompt file to
a skill", which is what the next module is about ({{module:authoring-skills}},
{{topic:skillsvscode}}).

A custom agent is a `.agent.md` in `.github/agents` — previously called a chat mode — combining
instructions, a tool list and an optional model into a role you pick from the Agent dropdown. Its
front matter can declare `name`, `description`, `tools`, `handoffs`, `user-invocable`,
`disable-model-invocation` and `hooks`. Two behaviours matter: "If the agent specifies a `tools` list,
only those tools are available", and on the Copilot harness "the agent's instructions are added to your
custom instructions and take precedence if they conflict" — the one precedence rule you are given.

## In practice at Technik

The capstone repository ships `.vscode/mcp.json` and nothing else for agents, and the gap is
instructive. Its single most dangerous property is invisible: it is **two** uv projects, because Agent
Framework requires `mcp<2` while the server needs v2. An agent asked to tidy dependencies will
reconcile those pins, and the repository will stop working ({{topic:localenv}}).

That is exactly what an always-on file is for. An `AGENTS.md` at the root would state the split, that
`uv.lock` and `agent/uv.lock` are both committed, that tests run offline against fakes, and that the
code has never run live — four facts no amount of reading the tree reveals.

The targeted file above earns its place differently. The seed's CSV rows reproduce every figure the
lessons quote — welding at Plant 1 at 110.9% before the stale confirmations are dropped, the 3.0 mm
overlay minimum — so an agent "fixing" an inconsistency in `seed/data/` silently invalidates prose
elsewhere in the course ({{topic:qualify}}).

A custom agent is the right shape for the review job nobody wants: given a changed eval case, work out
which stage page and which lesson describe it. Give it `tools: ['read', 'search']` and it cannot edit
anything while it answers, which makes the answer safe to ask for casually.

What Technik should not do is reach for a prompt file for any of it. The repository is worked on from
more than one harness, and a prompt file would run for exactly one of them.

## Design guidance

- **Put the facts a newcomer would get wrong in an always-on file**, and keep them to facts rather
  than style preferences.
- **Scope with `applyTo` rather than writing one long file.** A targeted file arrives only when it is
  relevant, which is also cheaper in context ({{topic:budget}}).
- **Never let two files disagree.** There is no precedence rule to fall back on.
- **Restrict a custom agent's tools** when its job is to answer rather than to act.
- **Prefer a skill to a prompt file** for anything that must work on more than the Local harness.
- **Expect instructions to be followed, not obeyed.** Invariants go in middleware or in CI.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A slash command works for you and not for a colleague | Prompt files run only in Local harness sessions | Convert it to a skill |
| An instruction file never seems to apply | No `applyTo` and no `description`, so it must be attached manually | Add one, or attach it explicitly |
| Two instruction files contradict each other and behaviour varies | Sources are additive with no general precedence order | Resolve the conflict in the files |
| The agent followed none of it and the file was discovered | Discovery is verified; compliance is not | Enforce in code; keep instructions short and concrete |
| Customizations work on your machine only | User-folder instructions do not roam through Settings Sync | Move the project's share into the repository |
| A custom agent cannot reach a tool it needs | Its `tools` list is exhaustive | Add the tool, or use a different agent |

## Key terms

**Project instructions** — an always-on file (`.github/copilot-instructions.md`, `AGENTS.md`) giving
repository-wide context.

**Targeted instructions** — a `*.instructions.md` file that attaches itself by `applyTo` glob or by
description.

**Prompt file** — a `.prompt.md` reusable task invoked as a slash command, on the Local harness only.

**Custom agent** — a `.agent.md` role bundling instructions, a tool list and an optional model.

