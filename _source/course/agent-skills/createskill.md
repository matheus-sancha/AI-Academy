## TL;DR

Copilot Studio gives you two ways to create a skill in the portal: **Create from blank**, which is three
fields (name, description, instructions), and **Generate with AI**, where Copilot interviews you and writes the
file. Either way, write in this order: a **description** that triggers on the right requests, **numbered
steps**, explicit **rules** for what the skill must never do, and **one worked example**. Then test the
trigger before you look at the output, because a skill that never fires looks exactly like one that does not
exist.

## Why it matters

Most of what goes wrong with a skill is decided before the body is written. A vague description means the
skill never fires, and a broad one means it fires on requests that belonged to a tool. A missing *never*
means the agent invents what it should have asked for. The portal does not help: three text boxes and a
**Create** button, and nothing checks whether the description would ever match a real request.

The instructions are the easy part, and the part people spend their time on.

## How it works

### Two ways in

<!-- volatile verified=2026-10 -->
On the GitHub Copilot harness, open the agent, select **Build**, then **Skills** in the components panel, then
**Add skill**:

- **Create from blank** asks for a **Name** (lowercase letters, numbers and hyphens, not starting or ending with
  a hyphen), a **Description** of what the skill does and when it should be activated, and **Instructions** in
  Markdown. Select **Create** and the skill appears in the components panel. You can edit all three later from
  the skill's configuration panel.
- **Generate with AI** takes a description of the skill you want, asks you questions to refine it, then offers
  the result with **View**, a download icon and **Add to agent**.
<!-- /volatile -->

Microsoft's create page lists those three fields and nothing for files. A skill made this way is a single
`SKILL.md`. A skill that needs a template or a reference list is written as a folder and uploaded as a package
({{topic:packaging}}).

<!-- unknown since=2026-10 -->
The skills overview says creating from blank also defines "triggers, inputs, outputs", which the create page
does not show. Whether a blank skill can carry supporting files, or anything beyond the three fields, has not
been checked.
<!-- /unknown -->

A generated skill is one you did not write. Read all of it before **Add to agent**, as you would any skill
from elsewhere ({{topic:addskill}}). Then download it, so its source lives in version control and not only in
the agent ({{topic:openformat}}).

### Write it in this order

**1. The description.** Write it from five real ways people ask, not from the feature name. It needs the four
parts a tool description needs ({{topic:tooldesc}}): what it produces, when to use it in the user's words, when
not to with the neighbour named, and what it needs.

**2. The steps.** Numbered, imperative, in the order the agent should work, and each one a single action.
Where an input can be missing, the step says to ask for it.

**3. The rules.** The things it must never do, stated plainly: invent, estimate, conclude, change a record.
They are usually the difference between a draft someone can use and one they check line by line.

**4. One worked example**, with a realistic input and the exact output shape. It does more for a consistent
format than any amount of describing one ({{topic:fewshot}}).

### Test the trigger first

Before judging what the skill produces, check *when* it runs. Write three lists:

- **Should trigger**: five real phrasings of the request.
- **Should not trigger**: five neighbouring requests that a tool or another skill owns.
- **Ambiguous**: one or two you would have to think about.

Ask each in a **new chat**, because a skill binds when a conversation starts ({{topic:conversation}}), and read
the activity trace to see whether the skill activated ({{topic:test}}). A wrong answer in the trace is a
description problem; fix that before touching the steps. Only when the right requests trigger is the output
worth reading.

## In practice at Technik

Planners keep being asked by project managers why work orders are late, and the assistant's answers are
inconsistent: sometimes a status code, sometimes a guess. The fix is a **delay note**, a fixed five-line format. It passes the
earns-a-skill test on three counts: a fixed procedure, an output with its own conventions, and a request that
comes up a few times a week ({{topic:skillsvs}}). It bundles nothing, so it is created from blank:

```markdown
---
name: wo-delay-note
description: Writes a five-line delay note for one work order (where it is, what is holding it, what is not known) for a project manager. Use when someone asks why a work order is late, stuck or blocked, or wants a delay explained. Not for plain status lookups, lead-time averages or efficiency.
---

## Steps
1. Get the work order number. If the user gave none, ask. Never pick one from a project.
2. Call `Get work order status` for its status and current operation.
3. Call `Find quality notifications` for open QNs naming that work order.
4. If the current operation is INPROC and an open QN names the work order, it is blocked.
   Say so and name the QN.
5. Write the note in the format below.

## Format
**Work order <number>: <part>, <serial>**
- Now at: <operation> (<status in words>)
- Holding it: <QN number and defect type>, or "nothing recorded"
- Not known: whatever the tools did not return

## Rules
- Never estimate a completion date.
- Never state a cause the records do not show. "Nothing recorded" is not "no problem".

## Example
Request: "Why is 100004521 late?"
**Work order 100004521: P7000001042, XT-V2-1042**
- Now at: Cladding (in process)
- Holding it: QN 300001234, porosity in overlay
- Not known: when the QN will be dispositioned
```

Step 4 is Technik's own rule: there is no blocked flag, so *blocked* is worked out from two tools' answers.

The trigger test:

| Request | Expected | Why |
|---|---|---|
| *Why is `100004521` late?* | Skill | The core case |
| *Write the PM a note on what's holding up `100004521`* | Skill | Different words, same need |
| *What's the status of `100004521`?* | `Get work order status` | A lookup, not an explanation |
| *Average lead time for `P7000001042`?* | `Get work order lead time` | Named in the exclusion |
| *Write up the porosity on `XT-V2-1042` as a QN* | `qn-write-up` | A different skill's job |
| *Why is `100004521` still at cladding?* | **Ambiguous** | Asks *why*, so the skill; the description says *why*, so it now matches |

The last row is the useful one. You make a decision about it, then write the decision into the description.

## Design guidance

- **Write the description first, and test it before writing anything else.**
- **Choose blank or upload by shape**: one file, blank; anything bundled, a package.
- **Number the steps**, one action each, with an *ask* wherever an input can be missing.
- **State the *never*s explicitly.** Estimate, invent, conclude, change.
- **Show one example** with the exact output shape.
- **Name the tools in the steps**, so the skill uses them instead of reaching for its own data.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Never triggers | Description written from the feature name | Rewrite it from five real phrasings |
| Fires on status questions | No exclusion | Add *not for*, naming the tool that owns them |
| The format drifts between answers | Described, not shown | Add a worked example |
| The note gives a finish date | Nothing said not to | A rule: never estimate a completion date |
| Works in a new chat, not the old one | The skill binds at conversation start | Test every change in a new chat |
| The generated skill does something you did not ask for | It was added without being read | Read it all before **Add to agent** |

## Key terms

**Create from blank**: authoring a skill in the portal from a name, a description and Markdown instructions.

**Generate with AI**: having Copilot interview you and write the skill, for you to review and add.

**Trigger testing**: checking which requests activate a skill before checking what it produces.

**Worked example**: one input and its exact expected output, placed in the skill's body.
