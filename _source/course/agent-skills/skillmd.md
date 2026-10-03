## TL;DR

A `SKILL.md` is **YAML frontmatter plus a Markdown body**. The frontmatter needs two fields. `name` is
lowercase letters, numbers and hyphens, up to 64 characters, matching the skill's folder. `description` says
what the skill does and when to use it, on **one line**, and it is the only thing the runtime sees when it
decides whether to activate the skill. The body holds the procedure the agent follows once it has. Anything
else the procedure needs goes in `references/`, `scripts/` or `assets/`, loaded only when the body points
at it. Most broken skills are broken in the frontmatter, and most of those fail silently.

## Why it matters

A skill has two readers. The **runtime** reads the frontmatter of every skill on every turn and decides from
it alone. The **agent**, once a skill is active, reads the body and follows it. A skill can fail at either
stage, and the two failures look nothing alike. A good body behind a vague description never runs. A
frontmatter block that is not valid YAML stops the skill loading at all, and Copilot Studio says nothing:
the rest of the agent loads and the skill is simply absent.

This is also the lesson the Advanced level picks up ({{topic:descriptions}}): the anatomy below is the
specification's, so it holds in VS Code as much as in Copilot Studio ({{topic:openformat}}).

## How it works

### The frontmatter

```markdown
---
name: qn-write-up
description: Drafts a quality notification (QN) write-up in Technik's SOP70000101 format from a described defect. Use when someone has found a defect on a part, weld or coating and wants it written up or worded as a QN. Not for looking up existing QNs or their status.
---
```

**`name`** is the skill's identifier. The specification's rules: 1–64 characters; lowercase letters, numbers
and hyphens only; no leading or trailing hyphen, no `--`; and it **must match the parent folder's name**.
Copilot Studio states the same character rule. `QN-Write-Up`, `qn_write_up` and `-qn` are all invalid.

**`description`** carries the whole activation decision. The specification asks it to say both what the
skill does and when to use it, with the keywords that help an agent recognise a matching task, and caps it at
1,024 characters. Copilot Studio adds a constraint of its own: a description longer than its model-facing
catalogue accepts gets the skill skipped, and the fix it gives is to shorten it "to a single line".

<!-- unknown since=2026-10 -->
Copilot Studio does not publish the length its skill catalogue accepts. Treat 1,024 characters on one line
as the ceiling, and aim far below it: two or three sentences.
<!-- /unknown -->

Three YAML details cause most load failures. **Quote any value containing a colon**: `description: Use
when: a defect` is invalid, `description: "Use when: a defect"` is not. **Save the file as UTF-8 without a
byte-order mark**: that is Copilot Studio's fix for a `SKILL.md` it cannot read, and some Windows editors
add the mark by default.
And **two skills in one agent cannot share a name**.

The specification also defines four optional fields: `license`, `compatibility`, `metadata` and the
experimental `allowed-tools`. Copilot Studio's documentation mentions none of them ({{topic:openformat}}).

### What a description has to say

The craft is the one {{topic:tooldesc}} teaches for tools, with the same four parts: what it produces, when to
use it in the user's words, when not to with the neighbour named, and what it needs. The specification's own
contrast makes the point. *Helps with PDFs* is its poor example. The good one names the actions, then says
*use when working with PDF documents or when the user mentions PDFs, forms, or document extraction*.

A vague description fails in one of two directions. Too narrow, and the skill never fires because nobody
phrases a request the way it does. Too broad, and it fires on requests that belonged to a tool or to plain
instructions, loading a whole procedure into a turn that did not need it.

### The body

After the closing `---` comes Markdown, with no format restrictions. The specification recommends
step-by-step instructions, examples of inputs and outputs, and common edge cases. Microsoft's list for
skills adds response formats and references to the tools the agent should use. Write it for a reader who
knows the product but not your process.

The whole body is loaded the moment the skill activates, so its size is paid for in full. The specification
recommends under 5,000 tokens and under 500 lines, with detail moved out to separate files.

### The folders

| Folder | Holds | Loaded |
|---|---|---|
| `references/` | Documentation the agent reads when needed: a code list, a detailed procedure | When the body points at it |
| `assets/` | Static resources: templates, schemas, lookup tables, images | When the body points at it |
| `scripts/` | Code the agent can run | When the body tells it to run it ({{topic:sandbox}}) |

The body refers to these by **relative path from the skill's root**, one level deep:
`Fill in [the template](assets/qn-template.md)`. A file the body never mentions is a file the agent has no
reason to open.

## In practice at Technik

The complete `qn-write-up` skill is one folder:

```
qn-write-up/
├── SKILL.md
├── assets/
│   └── qn-template.md
└── references/
    └── defect-types.md
```

The body of `SKILL.md`, below its frontmatter:

```markdown
## Steps
1. Get the QN's work order, part, serial number and operation. Use `Find quality notifications`
   if the user gave a QN or work order number; otherwise ask for them.
2. Identify the defect type from references/defect-types.md. If none fits, say so; do not pick
   the nearest.
3. Find the acceptance criterion the defect breaches in the governing work instruction, and quote
   it with the document number and revision.
4. Fill in assets/qn-template.md. Leave the disposition empty unless the user stated one.

## Rules
- Never invent a measurement. If a value was not given, write "not recorded".
- Never close or change a QN. This skill drafts; a person raises the record.
```

Each folder earns its place. The template is the output format, carried rather than described. The
defect-type list is reference the agent needs only during a write-up. Neither would belong in the
instructions ({{topic:skillsvs}}). The description's last sentence, *not for looking up existing QNs*, keeps
the skill clear of the notification tool, whose description says the reverse ({{topic:orchestration}}).

## Design guidance

- **Write the description from real requests**: collect five ways people ask for a write-up before you write
  a word of it.
- **Put the "when not to" in the description**, naming the tool or skill it must not be confused with.
- **Keep the description on one line and the frontmatter to two fields** until a harness documents more.
- **Number the steps and state the rules as imperatives.** Prose about the domain is not a procedure.
- **Carry templates as files**, and point at them by path from the body.
- **Save as UTF-8 without BOM, and quote any value with a colon**, before every upload.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The skill is missing from the components panel | Invalid YAML, usually an unquoted colon | Quote the value; check the block is `key: value` pairs |
| Also missing, YAML is fine | The file is not UTF-8, or starts with a byte-order mark | Re-save as UTF-8 without BOM |
| Listed, never fires | The description does not match how people ask | Rewrite it from real requests, with their words |
| Fires on status questions | The description is too broad | Add the exclusion, naming the tool that owns status |
| Follows some steps and skips others | The body is prose, not steps | Number the steps; make the rules imperative |
| Never uses the template | The body never mentions the file | Refer to it by relative path at the step that needs it |

## Key terms

**Frontmatter**: the YAML block between `---` lines at the top of `SKILL.md`; the part the runtime reads
before activation.

**`name`**: the skill's identifier: lowercase, hyphenated, matching its folder.

**`description`**: one line saying what the skill does and when to use it; the whole activation mechanism.

**Body**: the Markdown procedure loaded when the skill activates.
