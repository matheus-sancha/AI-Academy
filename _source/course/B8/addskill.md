## TL;DR

A ready-made skill is added by uploading a `SKILL.md` file or a packaged bundle. Because Copilot
Studio uses the same open **Agent Skills** format as GitHub Copilot, a skill written once can be
used in more than one place. That portability is the point — and it means an added skill is a
dependency you did not write, whose instructions your agent will follow. Read it before you enable
it.

## Why it matters

Adding a skill takes a minute and changes what your agent does. The skill's description competes
with your tools for routing, its instructions direct the agent's behaviour once it triggers, and any
files it bundles come along with it.

There is also a good reason to *want* this. Technik's quality engineers own `SOP70000101`. If the
write-up procedure lives in a skill file rather than in an agent's configuration, the person who
owns the procedure can own the skill — reviewing it, revising it and handing it to the next team who
needs it. That is a better arrangement than anything you can build by editing agent instructions.

## How it works

<!-- volatile verified=2026-09 -->
In Copilot Studio a skill is added to a GitHub Copilot harness agent from its Skills area, either by
uploading a `SKILL.md` or a bundle. The exact path, the accepted bundle format and the size limits
change between releases; follow the linked documentation rather than a remembered screen.
<!-- /volatile -->

A skill file is Markdown with front matter:

```markdown
---
name: QN write-up
description: Drafts a quality notification write-up in Technik's format from a
  described finding. Use when someone reports a defect and wants it written up.
---

## When to use this
...
```

A bundle is that plus the files it carries — a template, a reference table, a checklist — in a
defined folder layout.

### The same format as GitHub Copilot

This is what makes a skill portable. A skill written for Copilot Studio can be dropped into a
repository for GitHub Copilot to use, and the reverse. For Technik that means the write-up procedure
is available both to Bruno in Teams and to an engineer working in VS Code, from one file.

It also means skills can come from outside your organisation, with everything that implies.

### Review before you enable

An added skill is code someone else wrote, in the sense that matters: it directs your agent's
behaviour and it sits inside your trust boundary. Before enabling one, answer these in writing:

1. **Who wrote it, and who maintains it?**
2. **What does its description claim?** That is what it will trigger on, and it will compete with
   your existing tools and skills.
3. **What do its instructions actually tell the agent to do?** Read them. All of them.
4. **What files does it bundle**, and what is in them?
5. **Which tools does it expect?** A skill written against tools you do not have will fail
   halfway, which is worse than not triggering.
6. **Does anything in it reach outside?** Instructions to send, post, email or fetch deserve
   particular attention.

> [!WARNING]
> A skill's instructions are read by the model as instructions. A skill you did not review can tell
> your agent to do things you would not — including things involving the tools *you* gave it. Treat
> an unreviewed third-party skill exactly as you would an unreviewed dependency, because the
> comparison is exact. A13 covers this as a supply-chain question.

### After you add it

Adding a skill changes the routing for everything else, the same way adding a tool does
([B7](../B7/mcpadd.html) made the same point about MCP servers). So:

- re-run the routing tests for your existing tools and skills, not only the new one;
- check for overlap — if the new skill claims territory a tool already had, one of them will lose;
- watch the first few real conversations, not just your test questions.

## In practice at Technik

In this module's lab you write the write-up skill yourself, so adding an existing one is not the
exercise. It becomes the exercise the moment there is a second agent, which is sooner than it
sounds:

- **A6** splits the assistant into a production agent and an engineering agent. Both need Technik's
  write-up conventions. One skill file, added twice, is the difference between one procedure and
  two that drift.
- **A4** builds a document-revision skill that bundles `GWI70000027` and a change-summary script.
  That bundle is the thing that gets handed around.
- An engineer working in VS Code on Technik's MCP server (A5) wants the same conventions from
  GitHub Copilot. Same file.

The pattern worth adopting now: **keep skills in source control, next to the course's other
sources, and add them to agents from there.** A skill living only inside one agent's configuration is
a procedure with one copy and no history.

## Design guidance

- **Review before enabling**, and write the review down. Author, description, instructions, files,
  expected tools.
- **Check what tools it expects** before you find out at runtime.
- **Enable the minimum.** Every skill is another description in the routing decision.
- **Keep the source file in version control**, not only in the agent.
- **Re-review on update.** A skill that changed is a skill you have not reviewed.
- **Prefer a skill your own organisation owns** for anything that encodes your procedures.
- **Re-test routing** across the whole agent afterwards.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The skill will not upload | Wrong format, missing front matter, or a bundle layout the platform does not accept | Check the current documentation for the accepted shape |
| It triggers instead of your tool | Its description matches better | Narrow one of them; remove the overlap |
| It triggers and then fails halfway | It expects a tool this agent does not have | Add the tool, or do not use the skill |
| Behaviour changed and nobody edited the agent | The skill was updated in place | Version skills; re-review on change |
| The same procedure behaves differently in two agents | Two copies of the skill file | One source, added from it in both places |
| A skill quietly does something unexpected | It was never read | Read it. There is no substitute |

## Key terms

**Agent Skills format** — the open format shared with GitHub Copilot, which makes a skill portable.

**`SKILL.md`** — the skill's front matter and instructions.

**Bundle** — a skill plus the files it carries.

**Trust boundary** — the line inside which components are assumed not to be hostile. An enabled
skill is inside yours.

**Supply-chain risk** — risk inherited from something you did not write (A13).

**Routing** — the orchestrator's choice between tools, skills, topics and knowledge.
