## TL;DR

A skill is a directory, and three kinds of thing go in it: **scripts** the agent runs, **references**
it reads, and **assets** it copies or fills in. The division is not about tidiness — it is about who
does the work. The model follows instructions; a script does exactly the same thing every time, and
costs only its output rather than its length. The folder names `scripts/`, `references/` and `assets/`
are *recommendations*, not requirements, and real skills in both reference repositories ignore them.
What matters more is the part nobody documents: **outside Copilot Studio, no page says what runs your
script, whether it is sandboxed, or whether it has network access.** Treat `allowed-tools` as a
confirmation bypass, not a boundary.

## Why it matters

This is where a skill stops being a prompt and starts being software, with everything that implies: a
dependency you did not declare, an error nobody reads, a script a reviewer skimmed.

The payoff is precise. Anthropic's argument for bundling code is one sentence: "because code is
deterministic, this workflow is consistent and repeatable." That is the property a model cannot give
you. Technik's efficiency figure reads 110.9% or 88.9% depending on whether stale confirmations were
dropped, and the difference is a `QUALIFY` clause ({{topic:qualify}}). You do not want that decided
per turn.

The hazard is just as precise, and it is not the sandbox you learned in Copilot Studio
({{topic:sandbox}}). It is that a bundled script is **code shipped inside a document**, reviewed by
whoever reviews prose, and executed after a confirmation you may have pre-approved away.

## How it works

### The three kinds, and what each is for

<!-- volatile verified=2026-11 -->
The specification describes a convention and labels it as one: "The conventions below are
recommendations for organizing common types of content."

| Folder | Holds | The specification's words |
|---|---|---|
| `scripts/` | code the agent executes | "Contains executable code that agents can run" |
| `references/` | documentation the agent reads | "additional documentation that agents can read when needed" |
| `assets/` | templates, images, data files | "Contains static resources" |

Its three rules for a script are worth taking literally: be "self-contained or clearly document
dependencies", "Include helpful error messages", and "Handle edge cases gracefully". On what executes
them it is non-committal — "Supported languages depend on the agent implementation", commonly "Python,
Bash, and JavaScript".

Referencing is where the mechanics are fixed. Use "relative paths from the skill root", keep "file
references one level deep", and "Avoid deeply nested reference chains." VS Code accepts a Markdown
link or a `#file:` reference relative to `SKILL.md`, and asks for "Unix-style `/` path separators to
keep skills portable across operating systems."
<!-- /volatile -->

The convention really is only a convention. Anthropic's example bundles `reference.md` and `forms.md`
with no folder at all, GitHub's puts a shell script flat beside `SKILL.md`, and plenty of published
skills are a single file. Use the folders because they make a review legible, not because anything
enforces them.

### Say which kind a file is

Anthropic states the obligation that catches people: "It should be clear whether Claude should run
scripts directly or read them into context as reference." A `.py` file the body does not describe is
ambiguous — read it and you have paid its length for a paraphrase; run it and you executed code on a
guess.

<!-- volatile verified=2026-11 -->
GitHub's documentation shows the instruction shape: name the script, say it runs "from this skill's
base directory", and give the arguments. Copilot, it adds, "automatically discovers all of the files
in the skill's directory and makes them available alongside the skill's instructions."
<!-- /volatile -->

### What runs it, and who approved that

<!-- unknown since=2026-11 -->
Here the documentation goes quiet. VS Code says a skill may include "scripts that run tools or
interact with external systems" and names no interpreter, no sandbox and no network policy. GitHub
shows a `.sh` script and says nothing about what executes it. The Copilot Studio sandbox you measured
is that harness's, and nothing extends it to the editor, the CLI or the cloud agent. So the runtime,
the isolation and the network reach of a bundled script on those surfaces are unverified — assume the
script runs with the access of whoever or whatever started the session.
<!-- /unknown -->

<!-- volatile verified=2026-11 -->
What *is* documented is the approval. `allowed-tools` lists "the tools Copilot may use without asking
for confirmation each time", and anything not listed gets a permission prompt. The specification marks
it "(Experimental)" and warns that "Support for this field may vary between agent implementations".

GitHub's warning about it is as blunt as this documentation gets: pre-approving `shell` or `bash`
"removes the confirmation step for running terminal commands and can allow attacker-controlled skills
or prompt injections to execute arbitrary commands in your environment." The advice is to omit both
when in doubt. And on third-party skills: they "are not verified by GitHub and may contain prompt
injections, hidden instructions, or malicious scripts."
<!-- /volatile -->

So `allowed-tools` is a convenience that *removes* a check — not a capability grant and not an
isolation mechanism, the same shape as every other advisory control on this level
({{topic:permissions}}).

One field does let you be honest about requirements. `compatibility`, up to 500 characters, "Indicates
environment requirements (intended product, system packages, network access, etc.)", and "Most skills
do not need" it. A script needing the network is exactly the case that does.

## In practice at Technik

The document-revision package splits cleanly along *who does the work*:

```text
document-revision/
├── SKILL.md
├── references/swi-sections.md    # read before editing sections 4 and 5
├── assets/revision-template.md   # copy, then fill
└── scripts/change_summary.py     # run: ECN number in, summary table out
```

`change_summary.py` earns its place because its job is a join with a fixed rule: read
`TC_ECN_AFFECTED_ITEMS` for `ECN70000042`, emit one row per affected item with `FROM_REV` and
`TO_REV`, and fail loudly if the ECN is not released. A model doing that over a long result set makes
mistakes a script cannot, and the table never enters context ({{topic:disclosure}}).

`swi-sections.md` is a reference because the judgement is the point. Whether revision C's tightened
porosity limit belongs in section 5 or needs a new subsection is a decision an engineer makes with
the conventions in front of them; scripting it would pretend the rule is mechanical.
`revision-template.md` is an asset because it is copied and filled, not consulted.

The body says which is which, in the shape GitHub's example uses:

```markdown
Run `scripts/change_summary.py` from this skill's base directory with the ECN
number as the first argument. Do not read the script. Before editing section 4
or 5, read `references/swi-sections.md`. Start the draft from
`assets/revision-template.md`.
```

Two things Technik does not do. It does not pre-approve `shell`: the agent reads and drafts, and a
read-only role already bounds the query side ({{topic:sfroles}}). And the script holds no
credentials — it reads `os.environ`, and connects as `TECHNIK_AGENT_RO` like every other agent path.

## Design guidance

- **Script it when the rule is fixed; reference it when there is judgement.** That is the division.
- **Say whether a file is run or read.**
- **Let a script read its own input** so neither the script nor its data costs context.
- **Declare dependencies in the script and in `compatibility`**, not at run time.
- **Write errors for a model to act on**: what failed, and what does exist ({{topic:tooldesc}}).
- **Keep assets small** — community guidance is under 5 MB each — and reference every one.
- **Leave `shell` and `bash` out of `allowed-tools`.** The confirmation is the only check in the path.
- **Review bundled code as code.** A skill from outside your repository is an unreviewed dependency
  ({{topic:skillgov}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent paraphrases a script instead of running it | The body never says to run it | Name it as a command, with arguments |
| A script fails on first use, in front of a user | Undeclared dependency, or no network | Make it self-contained; declare `compatibility` |
| Right in the editor, wrong in the cloud | Different runtime, none of it documented | Test on each surface |
| A terminal command runs with no prompt | `shell` or `bash` pre-approved in `allowed-tools` | Remove them |
| A bundled file is never read | Nothing references it, or the path is nested | One level deep, relative, named |
| Paths work on Windows only | Backslash separators | Use `/` |
| A reviewer approved a skill containing a script | It arrived as a document | Route bundled code to a code review |

## Key terms

**Bundled file** — anything in the skill directory besides `SKILL.md`, referenced by a relative path
from the skill root.

**`allowed-tools`** — an experimental frontmatter list of tools the agent may use without asking,
removing a confirmation rather than granting a capability.

**`compatibility`** — an optional field declaring environment requirements such as system packages or
network access.
