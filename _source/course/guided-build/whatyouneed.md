## TL;DR

Have four things before stage 1. You need **the right agent**: on the GitHub Copilot harness, in your own
developer environment, inside a custom solution. You need **the six skills installed** and confirmed live. You
need **a licence that can publish and Copilot Credits you are allowed to spend**, because the route runs a
25-case evaluation several times. And you need **a real task with a real reader**, which matters most. The
first stage is a design interview, and it will not move past a slot you cannot answer. If all you have is an
idea, stage 1 is where the build stalls.

## Why it matters

Each missing prerequisite shows up somewhere else, later.

A standard-harness agent has no **Skills** section, which you find at the first upload. A trial licence fails
at stage 7's last step, **Publish**. A missing credit allocation looks like a stage that stopped answering. And
an idea in place of a task becomes an interview where every answer is rejected, rightly, and the afternoon
produces no file. Check all four first.

## How it works

### The agent, and where it lives

You choose the harness when you create an agent, and the agent cannot be moved to another harness later
({{topic:chooseharness}}). Skills are a GitHub Copilot harness feature. Microsoft's comparison marks skills and
memory *Not a focus* on the other two, and the toolchain's own README says skills are not supported
on the standard or Copilot chat harness. Create the agent on the GitHub Copilot harness, or the route ends at
its first upload ({{topic:installing}}).

Create it in **your own developer environment**, never the default environment and never one your colleagues
test in ({{topic:devenv}}). The Power Apps Developer Plan is free and needs a work account. If sign-up is
blocked, that is a tenant policy and the answer comes from your administrator, not the documentation. Two of
its limits apply to the build:

<!-- volatile verified=2026-10 -->
- **Generative AI is capped at 10 messages a minute and 200 an hour.** A 25-case evaluation with multi-turn
  conversations can reach it. Space the runs, and rerun any cases that fail on a limit ({{topic:whenitstalls}}).
- **An environment inactive for 30 days is disabled automatically.** A build that pauses over a holiday can
  come back to nothing.
<!-- /volatile -->

Create it **inside a custom solution** from the start, so it can move later ({{topic:solutions}}).

### The six skills

Install them as {{topic:installing}} describes. Until the router answers *Help me build this agent. Where do I
start?* with its placement question, the toolchain is not ready.

### A licence that reaches the end

Microsoft documents four ways into Copilot Studio ({{topic:licensing}}). One of them is a trap for this build:
a **trial licence** lets you create agents and test them, but you cannot publish. It fails at the last step of
the route, not the first.

<!-- unknown since=2026-10 -->
The trial licence's limit is stated on Microsoft's licensing page for the standard harness. No GitHub
Copilot harness page says whether a trial can publish there. Assume it cannot until your administrator
confirms otherwise.
<!-- /unknown -->

### Credits you are allowed to spend

Microsoft states it on every GitHub Copilot harness page: building, testing and evaluating agents might consume
Copilot Credits. The route does all three. Every stage is a conversation on the agent, and stage 6 writes a
**25-case evaluation set** that you will not run only once:

| Run | Why |
|---|---|
| 1–3 | One run is one sample. Run the set three times and average before you trust a score ({{topic:whyeval}}) |
| 4 | After the first fix, re-run the whole set, not just the case you fixed |

That is a hundred graded cases before the agent is published. Microsoft does not publish the rate, so read
the estimated credits on the first run before you budget the other three ({{topic:runeval}}). Credits are
also **assigned to an environment** by an administrator. Find out whether yours has an allocation, and what
happens when it runs out, before stage 1. Exhausted capacity looks like a bug, not a bill.

### A real task with a real reader

This is the one most people skip. Stage 1 is `copilot-agent-review`, and it holds thirteen slots, each with an
acceptance test ({{module:designing-an-agent}}). It asks one question per message, never invents an answer
and never moves on from a slot that failed its test. *"An assistant for my team"* fails the role slot.
*"Helps with documents"* fails tasks. The interview will ask again, and it is right to.

So come with what a slot can be tested against:

| Bring | It answers |
|---|---|
| A named task, with what starts it and what finished looks like | Role, tasks |
| The people who will use it: role, site, how expert they are | Users, tone |
| Real artifacts: a sample output, the template it follows, past examples | Outputs, inputs |
| The procedure their team is audited against | Rules, escalation |
| One thing they will plausibly ask that the agent must refuse | Out of scope |
| Someone who will use the agent, reachable during the interview | Anything you are guessing at |

The interview asks for artifacts just after the users slot, and reads them. If you are not the agent's user,
the user's answers are the ones that pass, so book them for stage 1.

## In practice at Technik

Before stage 1 of the Production Assistant build, the checklist reads:

- **Agent**: *Technik Production Assistant*, created on the GitHub Copilot harness in the engineer's developer
  environment, inside a custom solution. Nothing else is in the environment.
- **Toolchain**: six skills from the {{skills-version}} release page, six rows in the panel, and the router
  answering in a new chat.
- **Licence and credits**: a Copilot Studio user licence, not a trial. The administrator confirms the
  environment has an allocation and says what happens when it runs out.
- **Data access**: the engineer's own Snowflake role for exploring `SAP_WORK_ORDERS` and the `TC_*` tables.
  `TECHNIK_AGENT_RO` on `TECHNIK_AGENT_WH` already exists for the agent, so the connection added at stage 7
  has a role to run as ({{topic:connauth}}).
- **Artifacts** in one folder: revision B of `SWI70000318`, the `GWI70000027` authoring template, a closed
  quality notification and `SOP70000101` *Quality Notification Handling*.
- **People**: a supervisor and a quality engineer, each free for an hour on the interview day.

A colleague opens with *"I want an assistant that helps production"*. The interview accepts none of the
replies, because each names a department, not a task. An hour later there is no brief, and the honest next step
is a folder like the one above.

## Design guidance

- **Check the harness before anything else.** No **Skills** section in Build means a new agent, not a fix.
- **Confirm you can publish before stage 1.** A trial licence fails at the end.
- **Find out who pays, and the cap.** Read the first evaluation run's estimated credits before the second.
- **Bring artifacts, not descriptions.** A sample output is worth five answers about one.
- **Bring a user, or their words.** Answer the interview alone only if you are the agent's user.
- **Touch the environment if the build pauses.** Thirty idle days disables it.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| No **Skills** section to upload to | The agent is on the standard harness | Create a new agent on the GitHub Copilot harness |
| **Publish** unavailable at the end of stage 7 | A trial licence, or a data policy ({{topic:dlp}}) | Ask for a user licence; read the policy's hover text or details file |
| The interview keeps re-asking the role slot | You brought an idea, not a task | Name what starts the task and what finished looks like |
| A stage stops answering mid-month | The environment's allocation ran out | Administrator question, not a prompt problem ({{topic:licensing}}) |
| Evaluation runs throttle | The developer environment's hourly cap | Rerun the failed cases; space the runs |
| The environment has gone | 30 days inactive | Recreate it; the files you saved are the build |

## Key terms

**Prerequisite**: something stage 1 assumes is already true, which no stage checks for you.

**Real task**: a verb phrase with a trigger and a finished state, for named users, with artifacts to show it.

**Developer environment**: your own free Power Platform environment, for building and testing only
({{topic:devenv}}).
