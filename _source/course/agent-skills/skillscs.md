## TL;DR

On the GitHub Copilot harness a skill reaches an agent in one of three ways: **uploaded**, **created from
blank** or **generated with AI**. After that it is part of an agent other people use. Its description sits in
the catalogue on every turn, the orchestrator chooses it or ignores it, and when you publish, it goes out with
everything else. So the question stops being *is this skill good?* and becomes *is this the right set?* Keep the
installed set small and deliberate, give each skill one source and one owner, and treat every **Replace** as a
change to a live agent.

## Why it matters

The lessons before this one treat a skill on its own: what it is, how to write it, how to package it. An agent
does not have *a* skill. It has a set, and the set behaves differently from its members.

Every installed skill costs context on every turn, whether or not it fires. Every description competes with
every other description, and with every tool's. And once the agent is published, a skill edited on a Tuesday
changes what a supervisor in Teams gets on Wednesday. None of that shows when you test one skill in a new chat.
All of it shows in production.

## How it works

### Three ways in, and where the original lives

<!-- volatile verified=2026-10 -->
All three start from **Build** > **Skills** > **Add skill**, and they differ in where the skill's source of
truth ends up:

| Way in | The original lives | You change it by |
|---|---|---|
| **Upload a skill** (`.md` or `.zip`) | In your repository | Editing the file, then **…** > **Replace** |
| **Create from blank** | In the agent | Editing the three fields in the skill's configuration panel |
| **Generate with AI** | Nowhere yet; Copilot wrote it | Downloading it, reading it, then treating it as an upload |
<!-- /volatile -->

The three ways in are not equal over time. A skill created from blank is quick to start and has no history: the
agent holds the only copy, and an edit replaces it with no record of what it said before. Microsoft's pages
document **Download** for blank skills as a Markdown file named after the skill. So the usual path for a skill
that is going to last is to start from blank, download it once it settles, and from then on manage it by upload
from version control ({{topic:openformat}}).

### The installed set costs every turn

Progressive disclosure keeps a skill's body out of context until it fires, but the name and description are in
context **always**, about 100 tokens each ({{topic:skill}}). Ten skills add a thousand tokens to every turn,
including *what's the status of `100004521`?* That is the same arithmetic as instructions and tools
({{topic:contextcost}}), and it is the reason a skill is not free just because its body is cheap.

Microsoft publishes no maximum number of skills for this harness ({{topic:addskill}}). A limit you have not
reached is not a target. The cost and the routing get worse long before any ceiling.

### Skills compete for routing

The orchestrator picks among skills, tools and knowledge using the descriptions you wrote, the same mechanism
{{topic:orchestration}} describes. Adding a skill changes that choice for everything already installed.
Two skills whose descriptions overlap will split requests between them unpredictably, and a broad skill can
take requests a tool used to win.

The defence is the one {{topic:tooldesc}} teaches. Each description names its neighbours in a *not for* clause,
and the routing set is re-run after every add, replace or delete, not just for the skill that changed.

### A skill ships with the agent

Publishing makes the agent's current configuration available to its users ({{topic:publish}}), and the skills in
the components panel are part of that configuration. Three consequences follow:

- **Authoring skills do not belong in a published agent.** A skill you used to *build* the agent, such as the
  guided build's six `copilot-*` skills, is scaffolding. It comes out before publishing ({{topic:installing}}).
- **A replace is a release.** It changes behaviour for everyone once published, so it needs the review a code
  change gets: read the diff, re-run the routing set and the evaluation ({{topic:testsets}}).
- **The procedure has an owner.** The person who owns the procedure is often not the person who built the agent.
  Name both.

Every Microsoft skills page also repeats that using, building, testing and evaluating agents on this harness may
consume Copilot Credits, so a skill that fires on the wrong requests costs money as well as accuracy.

## In practice at Technik

At publish time the Technik Production Assistant has five tools and two skills:

| Skill | Way in | Source | Owner |
|---|---|---|---|
| `qn-write-up` | Uploaded package | The quality team's repository | Quality engineer who owns `SOP70000101` |
| `wo-delay-note` | Created from blank, downloaded, re-uploaded | The assistant's repository | Production planning |

`wo-delay-note` began in the portal ({{topic:createskill}}). Once the project managers stopped asking for changes,
it was downloaded, committed, deleted from the agent and uploaded again, so both skills are now managed the same
way.

Three other proposals were turned down, and the reasons are the lesson:

| Proposed skill | Decision | Why |
|---|---|---|
| `ppe-guidance` | **Knowledge** | The plant safety page answers it; retrieval, not procedure ({{topic:skillsvs}}) |
| `cite-sources` | **Instructions** | Needed on every answer, so it cannot depend on a description matching |
| `ecn-summary` | **Not yet** | Its description overlapped `Get released revision` on *which ECN changed it*; it waits until its trigger test passes |

The six `copilot-*` skills from the guided build were on the agent for weeks. They are deleted before the first
publish, and the deletion is checked in the components panel, not assumed.

After each change to the set, someone asks the routing questions in a new chat:

> *What's the status of `100004521`?* → `Get work order status`
> *Why is `100004521` late?* → `wo-delay-note`
> *Write up the porosity on `XT-V2-1042` as a QN.* → `qn-write-up`
> *Show open QNs on cladding for `PRJ-2031`.* → `Find quality notifications`

## Design guidance

- **Give every skill one source and one owner**, written down next to it.
- **Move a skill into version control once it settles.** Blank is for starting, not for keeping.
- **Add a skill only when it passes the earns-a-skill test** and its trigger test, not because it was easy.
- **Count the set's cost**: every description, every turn.
- **Re-run the routing set after any change to the set**, including deletions.
- **Remove scaffolding before publishing**, and check the components panel to confirm it is gone.
- **Treat Replace as a release**: review it, test it, then publish.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Status questions get delay notes | Two descriptions overlap | Add *not for* clauses naming each neighbour |
| Answers got slower and vaguer as skills were added | Every description costs context on every turn | Remove skills that rarely fire; merge true duplicates |
| A published agent offers to "run the design interview" | A `copilot-*` scaffolding skill was left installed | Delete it, republish, add the check to your publish list |
| Nobody can say what a skill said last month | It was created from blank and edited in place | Download it into version control; manage by upload |
| Users report new behaviour nobody announced | A skill was replaced on a published agent | Review and test every replace before publishing |
| Two agents' copies of a skill disagree | Each was edited in its own agent | One source file; replace both from it |

## Key terms

**Installed set**: all the skills on an agent, whose descriptions are in context on every turn.

**Source of truth**: the one copy of a skill that changes are made to; everything else is a deployment of it.

**Scaffolding skill**: a skill used to build an agent, not to serve its users, and removed before publishing.

**Routing set**: the questions re-asked after any change, to check each still reaches the right tool or skill.
