## TL;DR

The same `SKILL.md` is read from **six directories** — three in the repository, three in your home
folder — and which ones a session reads depends on the harness driving it. Put a project skill in
`.github/skills/<name>/SKILL.md` and it reaches the editor, the CLI, the Copilot app, the cloud agent
and code review. VS Code adds frontmatter that exists nowhere else, and two naming mistakes make a
skill "silently fail to load". Versioning and distribution are `gh skill`'s job, not the format's: it
pins by tag or SHA and writes provenance into the frontmatter. The honest summary is VS Code's own —
skills are portable, "but supported locations and optional features vary by agent."

## Why it matters

You learned the format in Copilot Studio, where one agent holds one uploaded set of skills
({{topic:skillscs}}). Here a skill is a file in a repository, which changes three things at once: it
is shared by cloning, reviewed in a pull request, and read by whichever harness happens to be running
— several of which you did not configure.

That last point is where people get caught. The format travels, as promised ({{topic:openformat}}).
The *behaviour* does not: fields like `disable-model-invocation` have no documented equivalent
elsewhere, and the published surface lists do not agree with each other. Portability of the file is
not portability of the design.

It also replaces a packaging problem with a dependency problem. There is no zip to get wrong
({{topic:packaging}}) — there is a directory in Git, which means versioning, pinning, provenance and
review.

## How it works

### Six locations, read per harness

<!-- volatile verified=2026-11 -->
Project skills live in the repository, personal skills in your home directory:

| Harness | Project | Personal |
|---|---|---|
| Copilot | `.github/skills/` | `~/.copilot/skills/` |
| Anthropic Claude | `.claude/skills/` | `~/.claude/skills/` |
| OpenAI Codex | `.agents/skills/` | `~/.agents/skills/` |
| Local | `.github/skills/` | `~/.copilot/skills/` |

Local sessions also read the `.claude/` and `.agents/` paths, project and personal. The Codex
integration is experimental, discovers workspace skills in `.github/skills/` "before your first
prompt", and "is disabled when Copilot enterprise-managed settings apply".

GitHub's documentation lists the same three project directories, but only `~/.copilot/skills` and
`~/.agents/skills` as personal ones — `~/.claude/skills` is absent there. Its surface list differs
too: skills "work with Copilot cloud agent, Copilot code review, the GitHub Copilot CLI, the GitHub
Copilot app, and agent mode in Visual Studio Code", naming no Codex, while VS Code's list names Codex
but neither the cloud agent nor code review.
<!-- /volatile -->

Two consequences. Default to `.github/skills/`, the only location every list includes. And a skill in
a personal folder is invisible to everyone else and to review — fine for your own shortcuts, wrong
for anything the team depends on ({{topic:customize}}).

### What gets loaded, and when

<!-- volatile verified=2026-11 -->
Copilot "reads the skill's `name` and `description` from the YAML frontmatter", loads the body on
selection — GitHub puts it as the `SKILL.md` file being "injected in the agent's context" — and
touches other files "only when it references them". A skill can also be run by hand: type `/` and
pick it.

The frontmatter fields beyond `name` and `description` are VS Code's:

| Field | Effect |
|---|---|
| `argument-hint` | hint text in the chat input, for a slash invocation |
| `user-invocable: false` | hidden from `/`; the agent may still load it automatically |
| `disable-model-invocation: true` | automatic selection off; slash only |
| `context: fork` | runs in "a dedicated subagent context" (experimental) |

Set both of the middle two and the skill is disabled. `context: fork` is the interesting one for
budget: the skill's "instructions and any files they read are loaded into a separate subagent", so a
large reference set never touches the main context ({{topic:disclosure}}). It "might change or be
removed".
<!-- /volatile -->

### Two silent failures, and a contradiction

<!-- volatile verified=2026-11 -->
`name` is capped at 64 characters here, must match the parent directory, and takes no "slashes,
colons, dots, or namespace prefixes". Both naming mistakes fail the same quiet way: "Names with
invalid characters cause the skill to silently fail to load", and so does a prefix like
`myorg/skillname`. Prefixing is the plugin mechanism's job — a plugin-distributed skill gets
`/my-plugin:test-runner` automatically — so writing one yourself breaks the skill. Duplicate names
across workspace roots resolve to "the primary root".

The setting for extra locations contradicts itself on the page. One section says
`chat.agentSkillsLocations` "remains supported and is not deprecated"; the Local section says it "is
deprecated and isn't read by Copilot harness sessions". Both agree on the practical point: custom
locations "are not recommended for Copilot workflows" because the CLI and the app "do not inherit
editor settings."
<!-- /volatile -->

<!-- unknown since=2026-11 -->
Which reading is current is unresolved, so don't build on it: a skill reachable only through that
setting is invisible to every surface except your editor.
<!-- /unknown -->

### Distribution, pinning and provenance

<!-- volatile verified=2026-11 -->
`gh skill` is in public preview and needs GitHub CLI 2.90.0 or later. It searches by topic, renders a
skill "and file tree in your terminal without installing anything", and installs from a repository —
at a tag or SHA, or with `--pin`, which are "mutually exclusive". `gh skill update --all` refreshes
installed skills, and "Pinned skills are skipped during updates". `gh skill publish --dry-run`
validates against the specification.

Installation writes "provenance metadata" into the frontmatter: "the source repository, ref, and tree
SHA". And before any of it: "Always inspect the content of a skill before installation using `gh
skill preview`."
<!-- /volatile -->

## In practice at Technik

The Production Assistant rebuild keeps its skills in the repository, not in anyone's profile:

```text
.github/skills/
├── document-revision/     # SKILL.md + references/, assets/, scripts/
├── qn-write-up/           # the Intermediate skill, unchanged
└── code-review/           # seed-data and quoted-figure rules
```

`document-revision` sits in `.github/skills/` so one file serves the engineer in VS Code, the `gh`
CLI and the cloud agent. Automatic selection stays on, because a revision request should reach it
unprompted ({{topic:descriptions}}).

`code-review` is named for the convention rather than its contents: a review-focused directory name
such as `code-review` is what makes Copilot code review pick it up. The rule it carries is one no
reviewer reliably remembers — a changed row under `seed/data/` invalidates a figure quoted in a
lesson, so welding at Plant 1 reading 110.9% is data, not a bug ({{topic:qualify}}).

Verification is VS Code's two-step, in that order. Start a fresh chat on the intended harness, check
the skill appears in the `/` menu and run it yourself, then "Review the tool activity and result" to
confirm it used the files you expected. Only then test automatic selection, "separately with a request
that matches its description" ({{topic:skilltest}}).

What does not go in a skill: that the capstone repository is two `uv` projects on purpose. That is
always-on context, so it belongs in `AGENTS.md` ({{topic:localenv}}).

## Design guidance

- **Default to `.github/skills/`** — the only location every surface's documentation lists.
- **Keep personal folders for personal shortcuts.** Nothing the team relies on is unreviewed.
- **Treat the VS Code-only fields as editor behaviour**, not part of the skill's contract.
- **Reach for `context: fork`** when a skill drags in a lot of reference material.
- **Never prefix `name`**, and always match the directory. Both mistakes are silent.
- **Pin third-party skills** by tag or SHA, and preview before installing.
- **Don't depend on `chat.agentSkillsLocations`.** Its own page disagrees about it.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The skill is absent with no error | Invalid characters or a namespace prefix in `name` | Lowercase, hyphens, match the directory |
| It works for you and nowhere else | It is in a personal folder, or a custom location | Move it into `.github/skills/` |
| It works in the editor, not the CLI or app | Those surfaces don't inherit editor settings | Use a documented location |
| The cloud agent ignores it | Wrong directory for that surface | `.github/skills/`, committed and pushed |
| Code review never uses it | The directory name gives no review signal | Name it `code-review` |
| An update changed a skill's behaviour | Installed unpinned | `--pin`, or install at a tag or SHA |
| A skill reads files you did not expect | Installed without inspection | `gh skill preview` first |

## Key terms

**Project skill** — a skill committed to the repository, shared by cloning and reviewed in a pull
request.

**Personal skill** — a skill in your home directory, invisible to everyone else.

**Forked context** — running a skill in a separate subagent, so its files never enter the main
context.

**Provenance metadata** — the repository, ref and tree SHA `gh skill install` writes into the
frontmatter.
