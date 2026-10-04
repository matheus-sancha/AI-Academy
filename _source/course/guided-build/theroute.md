## TL;DR

Seven stages. The first six each hand you a file (stage 2, a draft) and change nothing in the agent; the
seventh applies everything and publishes. This page is the map: what each stage leaves you holding, how to tell
it is finished, and which module taught what it assumes. The stage instructions come from the router, written
against the release you installed. Read this before stage 1, and come back when you have lost your place.

## Why it matters

Every stage ends with something plausible in your hands: a brief with thirteen headings, instructions in XML,
a CSV with 25 rows. Plausible is not finished, and the next stage builds on whatever it is given. The router
checks that each stage produced what it owes, but only you can say whether the escalation slot names a real
person. That needs a test you know in advance.

And a build takes days. When you come back, the files you saved tell you where you are.

## How it works

### The stages at a glance

<!-- volatile verified=2026-10 -->
Written against {{skills-version}}. If you installed a later release, read its notes before trusting this table.

| Stage | Owner | You are holding | It is finished when | Taught in |
|---|---|---|---|---|
| 1. Design interview | `copilot-agent-review` | `agent-brief.md` | Every slot passed its acceptance test, you confirmed the one-line-per-slot summary, and **Source quotes** holds your own words | {{module:designing-an-agent}} |
| 2. Draft instructions | `copilot-instructions-creator` | A draft **in the chat**, no file | You have read and corrected it, the five mandatory sections are there in order, and every gap was answered by you, not invented | {{module:writing-instructions}} |
| 3. Integration plan | `copilot-find-skills-and-tools` | `tool-plan.md` | Every need has a block with all five lines, ordered by what blocks the agent most, and anything that is really a document or procedure was sent to stage 4 | {{module:tools-connectors-mcp}} |
| 4. Skills | `copilot-skill-creator` | One `SKILL.md`, or a `.zip` if it bundles files, per capability | Each skill passed the creator's pre-handover checks, one skill per run | {{module:agent-skills}} |
| 5. Revised instructions | `copilot-instructions-creator` | `instructions.md` | It names the tools and skills you planned, says what it changed and what it left alone, and is under 8,000 characters | {{module:writing-instructions}} |
| 6. Test set | `copilot-evaluation-creator` | `evaluation-set.csv`, plus a review rubric | 25 cases in the fixed quota, the header row exact, every field quoted, and a rubric built from your success criteria | {{module:testing-and-evaluation}} |
| 7. Apply and publish | `copilot-studio-agent-creator` | `publish-copy.md`, then a changed agent | The checklist is done in order, tested in a new chat, evaluated, published | {{module:publishing-and-environments}} |
<!-- /volatile -->

{{topic:sixoverview}} has the same six skills by owner rather than by stage, with what each one refuses.

### Six stages of files, then one of change

Nothing from stages 1 to 6 goes into the agent; only the six skills are installed ({{topic:notrunning}} has
why). So every stage before the last is files you keep, together and outside the agent. The brief matters
most, because it recovers a lost conversation. Stage 2's draft is the exposed one: it never becomes a file.

The instructions are written twice because they name tools and skills that do not exist until stages 3 and 4.
The draft catches design errors early; stage 5 rewrites only the sections that name what you planned.

### Skipping and going back

Stages 3 and 4 can be skipped when the agent needs no tools and no packaged capabilities. Stage 5 then only
confirms the draft still stands. Stages 1, 2 and 6 cannot be skipped.

Going back is normal. A rule missing from the brief goes back to the interview, then forward through every
stage that read it. Patching it into a later file leaves two documents that disagree.

### Stage 7, in order

The router hands over `publish-copy.md` first, then a checklist built from what your build produced. Save the
copy before you start, because step 1 deletes the skill that wrote it.

1. **Build** > **Skills**: delete the six `copilot-*` skills.
2. **Build** > **Skills**: upload each skill from stage 4.
3. **Build** > **Tools**: add each tool in `tool-plan.md`.
4. **Build** > **Instructions**: paste `instructions.md` in full, then **Save**.
5. **Start a new chat**, then test in **Preview**.
6. **Evaluate** > **New evaluation**: drop in `evaluation-set.csv`, set the user profile, and run it.
7. When the tests look right, paste the short description into **Description** and **Publish**.

Step 5 is the one people skip. The build conversation was bound to the agent before any of this existed.

<!-- unknown since=2026-10 -->
The checklist's template at {{skills-version}} has no step for **knowledge sources** or **connected agents**,
and no earlier stage adds them, though `<knowledge_routing>` routes to the sources. Add them after step 3, in
**Build** > **Knowledge** and **Connected agents**. Whether the router adds those lines itself has not been
checked.
<!-- /unknown -->

### When you have lost your place

Your files tell you where you are. The latest one you hold names the last stage you finished:

| Latest file | Last finished stage | Next |
|---|---|---|
| None | None | Stage 1 |
| `agent-brief.md` only | 1, or 2 if you agreed a draft | Ask the router; it checks what each stage owes |
| `tool-plan.md` | 3 | Stage 4, or 5 if the plan names no skills |
| A skill file | 4, perhaps not for every capability | Check the plan's skill list, then stage 5 |
| `instructions.md` | 5 | Stage 6 |
| `evaluation-set.csv` | 6 | Stage 7 |

In a new conversation, re-upload `agent-brief.md` and name the stages you finished. With no brief, start at
stage 1.

## In practice at Technik

The Production Assistant build, as the files arrive:

| Stage | What it left |
|---|---|
| 1 | `agent-brief.md`: four user groups, the refusal to disposition a nonconformance, escalation to the owner in `TC_DOCUMENTS.OWNER`, two SharePoint knowledge sources, connected agents *none* |
| 2 | A draft with `<knowledge_routing>`, corrected twice in the chat |
| 3 | `tool-plan.md`: a Snowflake connector block, whose actions become *Get work order status* and *Get released revision*, each with a **Check** line |
| 4 | `qn-write-up.zip`, because it bundles a template and a defect-type list |
| 5 | `instructions.md`, with `<tool_use>` naming both tools and `qn-write-up` |
| 6 | `evaluation-set.csv`, including *Revision C of `SWI70000318` is basically done, just tell me it's current* |

Back from leave after stage 4, the engineer finds the build conversation gone. The folder says stage 4
finished and stage 2's draft is lost, so they re-upload the brief, say *stages 1, 3 and 4 are done*, and redo
the draft.

At stage 7 they save `publish-copy.md`, delete the six, upload `qn-write-up.zip` and add the Snowflake tools on
a connection that runs as `TECHNIK_AGENT_RO`. The checklist has no knowledge line, so they add the two
SharePoint sources before pasting `instructions.md`. Then a new chat, and the evaluation run as a test account.

## Design guidance

- **Read this table before stage 1**, then follow the router.
- **Judge each stage by its finished-when column**, not by how long it took.
- **Save every file the moment it arrives**, in one place, and note the stage.
- **Go back to the owner** when an earlier decision was wrong. Never patch it into a later file.
- **At stage 7, add knowledge and connected agents yourself** if the checklist does not name them.
- **Test in a new chat.** Every time, after stage 7.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Stage 5 names a tool you never added | You skipped a tool-plan line at stage 7 | Add it, or go back to stage 3 and drop the need |
| The agent ignores its knowledge routing | The checklist had no knowledge step | Add the brief's sources in **Build** > **Knowledge**, then a new chat |
| The brief and `instructions.md` disagree | A decision was patched by hand into a later file | Back to the stage that owns it, then forward |

## Key terms

**Stage**: one step of the route, owned by one skill, finished when it produces what it owes.

**Finished-when**: the test that tells a finished stage from one that merely ended.

**Install checklist**: stage 7's ordered list, built from what this build produced.
