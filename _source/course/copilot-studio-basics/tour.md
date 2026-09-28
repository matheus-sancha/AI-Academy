## TL;DR

Copilot Studio is Microsoft's low-code studio for building agents, workflows and agent flows, and
publishing them to the channels where people already work. What you see when you open an agent depends
on the **harness** it was created on: an agent on the GitHub Copilot harness is four tabs — **Build**,
**Preview**, **Evaluate**, **Monitor** — while an agent on the standard harness has the older page-based
layout, with **Topics** among its pages. Learn what each area is *for*. Where it lives will move.

## Why it matters

Every instruction you are given about Copilot Studio, in this course or anywhere else, is a click path:
*open the agent, go to Build, select the Model list*. When the path matches what is on your screen, that is
fine. When it does not — because the product was reorganised, or because the instruction was written for
the other harness — you need to know what the step was trying to reach, so you can find it yourself.

That second cause is the more common one, and the more confusing. The documentation covers two harnesses
side by side, often with pages of the same name, and a page about the standard harness reads perfectly
sensibly until it tells you to open a Topics page you do not have. Microsoft marks every page with a note
saying which harness it describes. Reading that note first is the habit this lesson is really about.

## How it works

Copilot Studio is reached at `copilotstudio.microsoft.com` in a modern browser. From the home page you
build three kinds of thing: **agents**, which hold conversations and complete tasks; **workflows**, drag-and-drop
automations whose steps can reason; and **agent flows**, the established flow format, which can run on
their own or be attached to an agent as a tool ({{module:automation-and-workflows}}).

Everything you build runs on a harness — the engine behind it ({{topic:harness}}). You choose it when you
create the agent, and you cannot move an agent between harnesses afterwards ({{topic:chooseharness}}). The
home page defaults to the GitHub Copilot harness; the standard harness is behind **Other ways to build**.

### The GitHub Copilot harness: four tabs

<!-- volatile verified=2026-09 -->
| Tab | What it is for |
|---|---|
| **Build** | Everything the agent *is*: instructions, knowledge, tools, skills, the model, connected agents and memory, gathered in one components panel |
| **Preview** | Chat with the draft agent, see the **activity trace** of what it did, and review past test conversations in **History** |
| **Evaluate** | Create and run test sets to measure quality ({{module:testing-and-evaluation}}) |
| **Monitor** | Production health, outcomes, reactions, sessions and credit usage. You can open it before publishing, but it fills only once people use the published agent |

Publishing to channels is its own step in the agent's lifecycle — create, build, test, publish, monitor —
rather than a tab ({{module:publishing-and-environments}}).
<!-- /volatile -->

The design idea behind that layout is stated plainly by Microsoft: instead of drawing conversation flows and
branching logic, you describe the agent in natural language, connect the resources it needs, and set the
boundaries, and the orchestrator decides the rest. So Build is where nearly all of your work happens, and
Preview is where you find out whether it worked.

### The standard harness: pages

<!-- volatile verified=2026-09 -->
A standard-harness agent opens on an **Overview** page, where the name, description, instructions and
primary model live, with separate areas for knowledge, tools, **Topics**, channels, analytics and settings,
and a **Test your agent** panel you open from **Test** at the top of any page. Its per-turn debugging view
is called the **activity map**.
<!-- /volatile -->

Two harnesses, two names for the same idea, is a pattern you will meet repeatedly:

| Job | GitHub Copilot harness | Standard harness |
|---|---|---|
| Configure the agent | **Build** tab | **Overview** page and its siblings |
| Try it out | **Preview** tab | **Test your agent** panel |
| See what happened in a turn | **Activity trace** | **Activity map** |
| Start again from a clean state | **New chat** | **Reset** |
| Designed conversation paths | Do not exist | **Topics** |

## In practice at Technik

The Technik Production Assistant is on the GitHub Copilot harness ({{topic:chooseharness}}), so the course
describes its screens that way. A typical session of work on it touches three tabs, in this order:

1. **Build** — the QN handling instructions say to quote a QN's `DEFECT_TYPE` in the answer. You tighten
   that line in the instructions and save.
2. **Preview** — you select **New chat**, ask *"Show open QNs on cladding for project `PRJ-2031`"*, and
   open the activity trace to confirm the QN tool was called and the answer quotes the defect type.
3. **Evaluate** — you re-run the QN cases in the evaluation set, because one good preview answer is an
   anecdote ({{topic:whyeval}}).

Monitor comes later, once the assistant is published to Teams and there is production traffic to read.

Now suppose a colleague sends you a link to a Microsoft page explaining how to change the model *"on the
Overview page"*. You open the assistant and find no Overview page. Nothing is broken: the page you were
sent begins with a note that it describes the standard harness. The harness-specific equivalent says the
model is in the **Build** tab's components panel ({{topic:model}}).

> [!TIP]
> Before following any Copilot Studio documentation, read the note at the top of the page. It says which
> harness the page describes. It takes two seconds and saves the ten minutes spent looking for a button
> that does not exist on your agent.

## Design guidance

- **Learn the jobs, not the layout.** *Configure, try, trace, evaluate, monitor* survives a redesign; menu
  positions do not.
- **Check the harness note on every page you follow**, and on every page you send someone.
- **Keep Preview open while you build.** It is the only place that shows you what the agent actually did.
- **Treat Build as the source of truth** for what the agent is. If a behaviour is not explained by
  something in Build, look at the model and the conversation history next ({{topic:conversation}}).
- **Use the curated links for click paths.** This course teaches what each area is for and links to the
  page that says where it is today.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| There is no Topics area | The agent is on the GitHub Copilot harness | Topics do not exist there ({{topic:topics}}) |
| The page you are following names a screen you do not have | The page describes the other harness | Read the harness note; find that harness's equivalent page |
| Monitor is empty | Nothing has been published and used yet | Expected. Use Preview and Evaluate until there is production traffic |
| You created a standard-harness agent by accident | **Other ways to build**, or the **New experience** toggle was off | Check the harness before creating; it cannot be changed afterwards |
| A menu has moved since last month | The product changed | Search the linked documentation for the job, not the menu name |

## Key terms

**Copilot Studio** — Microsoft's low-code studio for building and managing agents, workflows and agent
flows.

**Build tab** — where a GitHub Copilot harness agent's components are configured.

**Preview tab** — the test chat for a GitHub Copilot harness agent, with its activity trace and history.

**Evaluate** and **Monitor** — test sets before publishing; production health after.

**Activity trace / activity map** — the per-turn record of what the agent did, named per harness
({{topic:test}}).
