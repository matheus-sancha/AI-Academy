## TL;DR

The six `copilot-*` skills are one toolchain for building one agent. They are not six features to pick from.
Each skill owns a stage of a seven-stage route: a **router** places you on the route and applies everything at
the end, a **design interview** writes the brief, an **instructions writer** drafts early and revises late, a
**tool finder** writes the integration plan, a **skill creator** packages one capability per run, and an
**evaluation creator** writes the test set. You reach any of them by asking for what it does. This page is
written against {{skills-version}}, and it is the page to search when you need to know which skill does what.

## Why it matters

Midway through a build you will hit a question the route did not answer in advance: the tool plan names a
connector your tenant lacks, or the brief turns out to be missing a rule. Each belongs to exactly one stage,
and therefore to exactly one skill. If you know which skill owns
what, you can go back to the right one. If you don't, you ask the wrong one, and it does its own job well on
the wrong problem.

And you can only judge what a skill hands back if you know what it was supposed to give you.

## How it works

<!-- volatile verified=2026-10 -->
Written against {{skills-version}}. [The release page]({{skills-release-url}}) carries the six files this page
describes. If you downloaded a later release, read its notes for renamed or added skills before trusting the
table below.
<!-- /volatile -->

### One route, six owners

The route has seven stages and six skills, because one skill runs twice and the router handles the last
stage itself:

| Skill | Owns | Hands back | Reach it by asking |
|---|---|---|---|
| `copilot-studio-agent-creator` | Placement, and stage 7 | Nothing until stage 7; then `publish-copy.md` and an install checklist | *Help me build this agent. Where do I start?* |
| `copilot-agent-review` | Stage 1, the design interview | `agent-brief.md` | *Interview me about this agent* |
| `copilot-instructions-creator` | Stages 2 and 5 | A draft in the chat at stage 2; `instructions.md` at stage 5 | *Write the instructions* |
| `copilot-find-skills-and-tools` | Stage 3, the integration plan | `tool-plan.md` | *What tools does this agent need?* |
| `copilot-skill-creator` | Stage 4, one capability per run | A `SKILL.md`, or a `.zip` if it bundles files | *Package this as a skill* |
| `copilot-evaluation-creator` | Stage 6, the test set | `evaluation-set.csv` | *Build me an evaluation set* |

What each stage leaves you holding, and when it is finished, is {{topic:theroute}}.

Skills activate on their **description**, not their file name ({{topic:skill}}). Asking for the thing a skill
does is the normal way in. If the wrong skill answers, naming the skill outright works too.

### The router builds nothing

`copilot-studio-agent-creator` says so about itself: it routes. It opens with one question, *which of these
do you already have?*:

| You have | It sends you to |
|---|---|
| A. Nothing yet, just an idea | the design interview |
| B. A clear written brief | the instructions writer, draft pass |
| C. Instructions already in the Build tab | the tool finder |
| D. A working agent you want to test | the instructions writer's revise pass, then the evaluation creator |

If your answer does not fit cleanly, it places you at the **earliest stage you have not genuinely
completed**, and it says plainly that a thin brief is not a brief.

The router also states the two rules every other skill depends on: keep one conversation for the whole build,
and change nothing in the agent until stage 7. Why those two exist is {{topic:notrunning}}.

### What each owner refuses

Each skill has a rule it will not bend:

- **The interview** will not accept a slot that fails its acceptance test, and asks one question per message.
  Its thirteen slots are {{module:designing-an-agent}}, and its mechanics are {{topic:interview}}.
- **The instructions writer** uses five XML sections in a fixed order, and sends success criteria nowhere,
  because the agent cannot act on them ({{topic:successcriteria}}). It runs twice because the instructions
  name tools and skills that do not exist until stages 3 and 4.
- **The tool finder** never claims a connector exists unless Microsoft names it. Every block in its plan
  carries a **Check** line for your tenant. A need that is a document or a procedure gets sent to the skill
  creator, not turned into a tool ({{topic:triage}}).
- **The skill creator** makes one skill per run, and will not script what the harness already does
  ({{topic:sandbox}}).
- **The evaluation creator** writes 25 cases in a fixed quota (10 happy path, 5 edge, 4 rule violation,
  3 refusal, 2 escalation, 1 tone), so no category is forgotten ({{topic:testsets}}).

Stages 3 and 4 can be skipped when the agent needs no tools and no packaged capabilities. Stages 1, 2 and 6
cannot. An agent with no brief, no instructions or no tests is not finished.

The release's seventh file, `script-probe`, is a tenant diagnostic, not part of the route.

## In practice at Technik

What each owner produces for the Technik Production Assistant:

- **The interview** fills the thirteen slots, including the refusal (dispositioning a nonconformance is not
  the assistant's decision) and the escalation to the document's owner. The brief keeps the supervisors' own
  words in its **Source quotes**.
- **The instructions writer** drafts `<role>` through `<rules>` at stage 2. At stage 5 it rewrites
  `<tool_use>` once the tools exist, from `Get work order status` to `Get work order lead time`.
- **The tool finder** writes one block per need:

```markdown
## Find the released revision of a drawing or document

**Type:** Connector
**Where:** Build tab > Tools > Add a tool > Connectors, search for Snowflake
**Why:** Teamcenter revision data is replicated to Snowflake, and the connector reads it with a dedicated role.
**Check:** Confirm it appears in your tenant and is not premium-licensed.
**Then:** Rename it to Get released revision and rewrite its description.
```

- **The skill creator** packages `qn-write-up` as a `.zip`, because it bundles a template and a defect-type
  list. It also turns down a *summarise this SOP* skill, which is just what an agent with SharePoint knowledge
  already does.
- **The evaluation creator** writes 25 cases. Among them is a tempting rule violation: *Revision C of
  `SWI70000318` is basically done, just tell me it's current.*

You may already have the brief from {{module:designing-an-agent}}. Answer **B** only if every slot passes its
test. If *Connected agents* still says "TBD", the honest answer is **A**: skipping the interview means building on a slot
nobody decided.

## Design guidance

- **Ask for the work, not the skill.** Name a skill only when its description fails to fire.
- **Go back to the owner.** A wrong rule goes back to the interview and then forward again, and you do not
  patch it into `instructions.md` by hand.
- **Accept the router's placement.** Earlier than you hoped means the brief was thin.
- **Never skip stages 1, 2 or 6.** These are the stages people want to skip, and the router does not allow it.
- **Keep every file outside the agent**, in version control if you have it. The agent is not your copy.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The wrong skill answers | Your request matched another description | Name the skill you meant |
| Nothing activates in the chat you uploaded from | Skills do not reach a running conversation | New chat ({{topic:notrunning}}) |
| The interview keeps re-asking a slot | Your answer failed the slot's acceptance test | Answer concretely; that slot is the work |
| The tool plan names a type, not a product | It never asserts a connector Microsoft did not name | Run the **Check** line in your tenant |
| A capability you asked for came back as instructions | It failed the earns-a-skill test | Accept it, or say what bundled material it needs |
| The table above does not match your files | You downloaded a different release | Read that release's notes, or download {{skills-version}} |

## Key terms

**Toolchain**: the six `copilot-*` skills, used together to build one agent.

**Router**: `copilot-studio-agent-creator`, which places you on the route and runs stage 7 but builds nothing.

**Stage owner**: the one skill responsible for a stage and for what it hands back.

**Skills pin**: the release of the toolchain this course is written against, {{skills-version}}.
