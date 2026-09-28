## TL;DR

A **conversational** agent responds when someone talks to it. An **autonomous** agent starts from an event
instead — a new file, a new record, a schedule — and runs with nobody watching. The work can be identical;
what disappears is the person who would have noticed something was wrong. Everything autonomous agents need
extra is a rebuild of that supervision as design: tighter triggers, tighter instructions, somewhere for
failures to go, and approvals before anything irreversible.

## Why it matters

The appeal is obvious: work that happens without anyone asking. The cost is easy to miss, because in a
conversational agent a great deal of safety is provided free by the user. They notice a wrong answer. They
rephrase a misunderstood request. They abandon a conversation that has gone strange.

Remove them, and every one of those has to be built.

## How it works

| | Conversational | Autonomous |
|---|---|---|
| Starts from | A person | An event or a schedule |
| Runs | While someone is present | Unattended |
| Errors | Seen immediately | Seen when someone looks |
| A wrong result | Usually caught by the user | Enters a system and waits |
| Scope of a mistake | One conversation | Every item it processed |
| Cost control | Bounded by how much people use it | Bounded by whatever triggers it |

### Triggers

An autonomous agent is defined by what starts it: a new item somewhere, a schedule, a change in a record.
The trigger is where most autonomous-agent problems begin, and there are two failure shapes.

**Too broad**, and it runs on things it should ignore — every incoming message, not just the ones with a
certificate attached. It processes them, plausibly, and now you have a hundred wrong records.

**Too narrow**, and it silently never runs. Nothing errors. Weeks later someone asks why the backlog is not
moving.

<!-- volatile verified=2026-09 -->
Copilot Studio adds autonomous behaviour through event triggers on an agent. Which trigger types exist and
how they are configured changes between releases — check the linked documentation before designing around a
specific one. The design questions below do not change.
<!-- /volatile -->

### What has to be rebuilt

1. **Tighter instructions.** No one will rephrase. Ambiguity that a person would resolve in a second becomes
   a systematic error repeated across every item.
2. **Explicit failure handling.** Where does a failure go? A queue, an alert, a named person — but somewhere,
   decided before it runs.
3. **Approvals before anything irreversible.** This is {{topic:hitl}}, and it stops being optional once
   nobody is watching.
4. **Monitoring.** How do you find out it stopped? An agent that silently does nothing looks exactly like an
   agent with nothing to do.
5. **Cost limits.** Usage is bounded by the trigger rather than by demand, and a trigger firing more often
   than you expected is a bill. A per-agent monthly cap with a hard stop is the blunt instrument that exists
   for this ({{topic:licensing}}).

Note that the orchestration is the same machinery either way: an agent with generative orchestration can
respond to an event trigger exactly as it responds to a user, choosing tools and knowledge from their
descriptions ({{topic:orchestration}}). What changes is not the reasoning. It is who is there to catch it.

## In practice at Technik

The Production Assistant is conversational throughout this level, because its users are asking questions
and a person is always present.

One genuinely autonomous case appears in Advanced ({{module:automation-advanced}}): **supplier material
certificates**. They arrive as PDFs, someone files them, and the values get typed into a system. Nobody is
served by a person doing that.

Designed as an autonomous agent:

| Concern | Decision |
|---|---|
| Trigger | A certificate arriving in one specific location — not "any new message", which fires on everything |
| Extraction | AI Builder document processing, which returns named fields with confidence scores, rather than a model describing a PDF ({{topic:docproc}}) |
| Validation | Deterministic: does the heat number match the order, is the grade one Technik uses, do the mechanical values parse |
| Low confidence or failed validation | To a review queue. A person sees it. Nothing is guessed |
| Writing the record | Only after validation passes, and only through a flow ({{topic:agentflows}}) |
| Monitoring | An alert if nothing has been processed in a working day |

Notice how small the *agent* part of that is. Most of it is a pipeline with deterministic validation, and
the model does one job — reading a document — where reading is genuinely hard. That proportion is typical of
autonomous work that survives contact with production.

> [!WARNING]
> The tempting version is "an agent that watches the inbox and files everything". It demos beautifully, and
> it is how a hundred wrong material certificates end up in a system nobody re-checks. The boring version
> above is the one that lasts.

There is a second reason Technik keeps this conversational for now. AI Builder is not included in the Power
Apps Developer Plan, so the extraction step cannot even be built in a stock developer environment without a
separate trial ({{topic:devenv}}) — a useful reminder that an autonomous design's dependencies are wider
than its diagram.

## Design guidance

- **Start conversational.** Learn what the agent gets wrong with a person present, then remove the person.
- **Make the trigger as specific as you can.** It is the most common source of failure.
- **Name where failures go before you switch it on.**
- **Approve anything irreversible**, every time.
- **Alert on silence**, not only on errors.
- **Cap consumption.** A trigger firing more often than expected is a bill, not an outage.
- **Keep the model's job narrow.** Deterministic validation around one narrow model task beats a model
  judging the whole thing.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| It processed things it should have ignored | The trigger is too broad | Narrow it; filter early; do not rely on the model to judge relevance |
| It has not run for weeks and nobody noticed | The trigger is too narrow, and silence looks like idleness | Alert on no activity |
| Errors vanish | No failure path was designed | A queue or an alert, named before go-live |
| A bad result reached a real system | No approval on an irreversible step | Add one ({{topic:hitl}}) |
| A surprise bill | Consumption bounded by the trigger, not by demand | Caps, monitoring, and a hard stop |
| Worked in testing, wrong at scale | Testing was conversational, with a person catching things | Test unattended, on realistic volume |
| It behaves differently unattended than in the test pane | No conversation history to draw on, and nobody to clarify with | Expected; put what it needs in the instructions and the trigger's data |

## Key terms

**Conversational agent** — responds to a person.

**Autonomous agent** — started by an event or a schedule; runs unattended.

**Trigger** — the event that starts it. The most common source of autonomous failure.

**Review queue** — where low-confidence or failed items go for a person to see.

**Alert on silence** — monitoring that fires when nothing happened, not only when something broke.
