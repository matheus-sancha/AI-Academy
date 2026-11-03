## TL;DR

A skill is read in **three passes, each paid for separately**. The `name` and `description` of every
installed skill sit in context all the time — about **100 tokens** each. The `SKILL.md` body is read
only once the agent decides the skill is relevant. Everything else in the directory is read only when
the body points at it, and a bundled script can run without being read at all. The cost you pay
continuously is the description, not the skill. So the craft is deciding **which pass each fact
belongs in** — and the usual mistake is a 600-line `SKILL.md` paying level-two cost for level-three
material.

## Why it matters

You already know a skill loads "only when it is needed" ({{topic:skill}}). That sentence hides the
design work. *Needed* is three different events, each with its own trigger and its own price, and a
skill's running cost is set almost entirely by how you split material across them.

The arithmetic makes it concrete. Thirty installed skills cost roughly 3,000 tokens of permanent
context whatever they contain — cheap, and fixed. One of them firing costs whatever its body weighs,
every turn it stays active. Put the ten document type codes, the SWI section conventions and a worked
example in that body and you have spent thousands of tokens to answer a question that needed one of
them ({{topic:budget}}).

It also changes what "too big for a skill" means. There is no such size, because the third level is
read on demand and a script need never be read. The question is never *how much material is there*
but *how much does one task need* — the just-in-time argument, applied to a file tree you own
({{topic:jit}}).

## How it works

### The three levels

<!-- volatile verified=2026-11 -->
The Agent Skills specification numbers them, with budgets:

| Level | What | When it loads | Budget |
|---|---|---|---|
| 1. Metadata | `name` and `description` | "loaded at startup for all skills" | "~100 tokens" |
| 2. Instructions | the `SKILL.md` body | "loaded when the skill is activated" | "< 5000 tokens recommended" |
| 3. Resources | files in `scripts/`, `references/`, `assets/` | "loaded only when required" | as needed |

Anthropic's account of the same mechanism names the mechanics behind level 1: the agent "pre-loads the
`name` and `description` of every installed skill into its system prompt" at startup — which is also
why a skill is "triggered in the context window via your system prompt" rather than by any matching
done outside the model.

VS Code describes the same three passes for the Copilot harness, and is unusually precise about the
boundary between the last two: the body is loaded into context, while other files in the directory are
accessed "only when it references them", and "If a file isn't referenced in the instructions, it won't
be loaded." Its summary of why this matters is the one to remember — the three-level loading system
"means you can install many skills without consuming context."
<!-- /volatile -->

### Why the third level is nearly free

The specification's own reason for splitting files is thin: "smaller files mean less use of context".
Anthropic's is load-bearing, and about capability rather than size. An agent with a filesystem and
code execution does not "need to read the entirety of a skill into their context window", which is why
"the amount of context that can be bundled into a skill is effectively unbounded".

The strongest form of this is a script. A bundled script is executed, not read, so the agent "can run
this script without loading either the script or the PDF into context" — its input stays out of
context too. A reference file costs its own length every time it is read; a script costs its output.
That asymmetry, not tidiness, is the reason to prefer code for anything deterministic
({{topic:bundling}}).

### The two size rules, and a disagreement

<!-- volatile verified=2026-11 -->
The specification gives two level-two limits without reconciling them: "< 5000 tokens recommended" and
"Keep your main `SKILL.md` under 500 lines." Treat them as one instruction — keep the body short — and
follow whichever is stricter for your file. Its advice when you reach either is the same: "Move
detailed reference material to separate files."

It also bounds how deep the third level may go: keep "file references one level deep from `SKILL.md`"
and "Avoid deeply nested reference chains." A reference that points at another reference is a lookup
the agent has to decide to make twice.

The two Microsoft surfaces then describe level 3 differently. VS Code loads a file only when the body
references it. GitHub's documentation says that on invocation Copilot "automatically discovers all of
the files in the skill's directory and makes them available alongside the skill's instructions."
*Available* and *loaded* are not defined against each other on either page.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
So whether a bundle's unreferenced files cost context on the Copilot cloud agent is unresolved. Design
as if they might: reference every file you ship, and ship no file you do not reference. Copilot Studio
confirms the pattern — agents "load only the context they need, when they need it" — but names nothing
about what is always loaded, so the ~100-token figure above is the specification's, not Microsoft's.
<!-- /unknown -->

## In practice at Technik

The document-revision skill is the one that forces the decision. Drafting revision C of `SWI70000318`
from `ECN70000042` needs Technik's SWI section conventions, the ten controlled-document type codes, a
revision template, and a change summary computed from the ECN's affected items. Written as one file,
that is 500 lines before the procedure starts.

Split by level instead:

```text
.github/skills/document-revision/
├── SKILL.md                      # ~100 lines: the procedure, and when to read what
├── references/swi-sections.md    # section numbering, acceptance-criteria conventions
├── references/doc-types.md       # SWI, LWI, GWI, SOP, DCP, TDS, MFG, LST, DGL, DRM
├── assets/revision-template.md   # the skeleton a new revision starts from
└── scripts/change_summary.py     # affected items -> a change summary table
```

Now a planner asking about a work order pays only the description. A revision request loads the
procedure. The section conventions arrive only when a section is being edited, and `doc-types.md` only
when a code has to be spelled out for a supervisor. The change summary never enters context at all:
the script reads `TC_ECN_AFFECTED_ITEMS` and returns the table.

The ordering matters as much as the split. `SKILL.md` says *read `references/swi-sections.md` before
editing section 4 or 5* — a named file at a named moment. Dropping all four paths into a *Resources*
list at the end of the body gets them read opportunistically, or not at all.

## Design guidance

- **Budget each level separately.** Level 1 is per-skill and permanent, level 2 per-activation, level 3
  per-use. A fact's level is set by how often a task needs it.
- **Keep `SKILL.md` to the procedure.** Reference tables, formats and long examples are level-three
  material.
- **Prefer a script to a reference file** when the work is deterministic: a script's cost is its
  output, a reference file's its length.
- **Name the file and the moment.** *Read X before doing Y* beats a list of resources.
- **Reference everything you ship, and ship nothing you don't reference** — one surface may load
  unreferenced files, the other will never load them.
- **Keep references one level deep.** None that points at another reference.
- **Split before you trim.** A body over the recommended size usually means material belongs at level
  3, not that the prose needs tightening.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Context fills as soon as the skill fires | Reference material living in the `SKILL.md` body | Move it to `references/` and point at it by name |
| A bundled file is never used | The body never references it | Name the file at the step that needs it |
| Installing more skills degrades every answer | Descriptions written long; level 1 is permanent | Shorten descriptions, not bodies ({{topic:descriptions}}) |
| A reference is read two steps late, or not at all | A reference chain, or a bare resource list | Flatten to one level; say when to read it |
| A script's input lands in context anyway | The body asks the agent to read the file, then run the script | Let the script read its own input |
| Lean locally, heavy on the cloud agent | Unreferenced files may be made available there | Ship only referenced files |

## Key terms

**Progressive disclosure** — loading a skill in three passes, so material is paid for when it is needed
rather than when it is installed.

**Level 1 / metadata** — `name` and `description`, in context for every installed skill at all times.

**Level 2 / instructions** — the `SKILL.md` body, loaded on activation.

**Level 3 / resources** — bundled files, read when the body references them; a script runs without
being read at all.
