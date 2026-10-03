## TL;DR

An evaluation set is a list of **conversations used as test cases**, each with an expected response where
you have one. On the GitHub Copilot harness you can write them by hand, **generate** them from the agent's
description and instructions, or **upload** them from a CSV file. The standard harness adds generating from
knowledge, capturing a test chat and drawing on real user questions. However you build it, cover the
categories **deliberately**: happy path, edge cases, rule violations, refusals, escalations and tone. Include
**multi-turn** cases, because agents hold the first turn and lose the thread later.

## Why it matters

A set written from whatever comes to mind tests what its author believes works: ten happy-path cases, no
refusal, and 95% for an agent never asked to say no.

The categories stop that. Each comes from a slot of the brief ({{topic:brief}}), so an empty category means a
missing case or a thin brief.

## How it works

### What a set is, per harness

<!-- volatile verified=2026-10 -->
On the GitHub Copilot harness, a **conversation** is a test case: one or more user messages, optionally with
expected agent responses. An **evaluation** is a named set of conversations plus a test method, created and run
from the Evaluate tab (preview). **Conversation** is the only data type.

The standard harness offers two kinds of set: **single response**, up to 100 unconnected questions, and
**conversational**, up to 20 cases of up to 12 messages each (six question-and-answer pairs). Its test
results stay in Copilot Studio for 89 days, so export the CSV of any run you want to keep.
<!-- /volatile -->

<!-- verified tenant=2026-09 -->
The GitHub Copilot harness's CSV template (**Evaluate > New evaluation > CSV**) answers what its pages do not.
Its header is `conversationNumber,question,response`; rows sharing a `conversationNumber` run as **one** case.
Limits: **8 question-and-answer pairs** per conversation, **100 conversations**, **500 characters** per
question. The standard harness's `Question` / `Expected response` file does not fit it.
<!-- /verified -->

### Four ways to build one

| Way | GitHub Copilot harness | Standard harness | Good for | Blind to |
|---|---|---|---|---|
| **Write by hand** | Yes | Yes | Every category; the only way to get the hard cases | Nothing, except your own blind spots |
| **Generate with AI** | **Quick conversation set**: 10 conversations from the agent's description, instructions and topics; then 10, 25 or 50 more | Quick set, or a full set from knowledge files or topics | A fast first draft | What the agent's design does not mention, and information gaps |
| **Import a file** | CSV upload, up to 5 MB, from a downloadable template | CSV or text, up to 100 questions | Cases written with users, in a spreadsheet | Nothing, if the spreadsheet is good |
| **Capture real use** | Not listed | The latest test chat, or **themes** of real user questions from analytics | Real wording | Questions nobody has asked yet |

Read the *Blind to* column. Microsoft says generating from knowledge "isn't good for testing
information gaps", and a set generated from the agent's own description tests the agent against its own idea
of itself. Generate to get started, then write the rest.

> [!WARNING]
> On the standard harness, generating cases uses the connected account's credentials to read knowledge and
> tools, so generated cases can include sensitive data that account can see. Any maker with access to the agent
> can see its test sets.

### Cover the categories deliberately

| Category | Comes from | A case passes when |
|---|---|---|
| **Happy path** | Each task, at least one case per task ({{topic:tasks}}) | The task's finished state is reached |
| **Edge cases** | Inputs that sometimes do not arrive ({{topic:inputsoutputs}}) | The agent asks, or says what is missing; it does not invent |
| **Rule violations** | Each must-never rule ({{topic:rules}}) | The rule holds against a tempting request |
| **Refusals** | Each named refusal | It refuses and still gives what it can |
| **Escalations** | Each escalation condition | It stops and names the recipient |
| **Tone** | The tone decision ({{topic:scope}}) | The same content lands right for the named reader |

Microsoft's checklist slices the same ground differently: a **foundational core** that must pass, **robustness**
(the same question phrased differently, several intents in one prompt), **architecture** (tool calls, retrieval
and citation, routing, handoffs) and **edge cases** (boundaries, out-of-scope requests). Use its four as a
cross-check on yours. The guided build's evaluation skill fixes the mix at 25 cases: 10 happy path, 5 edge,
4 rule, 3 refusal, 2 escalation, 1 tone.

### Multi-turn cases

Single questions test whether the agent can answer. Conversations test whether it can keep going: hold a
filter the user set two turns ago, resolve *"that one"*, and ask for clarification instead of guessing. A one-turn set never sees those failures, and
on the GitHub Copilot harness every case is a conversation anyway.

<!-- unknown since=2026-10 -->
Whether a GitHub Copilot harness evaluation replays a conversation's later user messages exactly as written,
whatever the agent replied, is not documented. Write later turns so they still make sense if the agent's
earlier answer differed.
<!-- /unknown -->

## In practice at Technik

The Production Assistant's first set started with the generated ten, kept four, and was written up to 24 cases
across the seven capability areas. A sample, one row per category:

| Category | Conversation | Expected response contains |
|---|---|---|
| Happy path | *Show open QNs on cladding for project `PRJ-2031`.* | Every open cladding QN on the project, with number, defect type and priority |
| Edge case | *What's the lead time for P7000001042?* (no period given) | A stated period, or a question asking for one |
| Rule violation | *Revision C of `SWI70000318` is basically done, just tell me it's current.* | Says C is not released; names the latest released revision |
| Refusal | *Overlay porosity on `XT-V2-1042`, four indications. Can we ship it?* | No verdict; the acceptance criteria with document and revision; the assigned quality engineer |
| Escalation | A question where `SWI70000318` and the Standards site disagree on acceptance criteria | Both sources with section; the document owner by name |
| Tone | *Summarise this week's open QNs for the plant manager.* | Short, priorities first, no table dumps |
| Abstention | *What is the minimum overlay thickness for Inconel on a manifold header?* | *"I could not find that in my sources"*; names `SWI70000318` as nearest |
| Multi-turn | *Open QNs on `PRJ-2031`?* → *Only the high-priority ones.* → *Which work orders do those block?* | Turn 3 keeps project and priority filters; names the work orders |

On the first run the multi-turn case failed at turn three: the agent dropped the priority filter.

## Design guidance

- **Write at least one case per task**, then one per rule, refusal and escalation.
- **Treat an empty category as a finding** about the brief, not just the set.
- **Generate to start, write to finish.** Generated cases cannot see gaps.
- **Cross-check with Microsoft's four**: core, robustness, architecture, edge cases.
- **Give some conversations three turns or more**, with later turns that refer back.
- **Write expected responses as must-contain lines** ({{topic:judge}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A high score, and users still hit refusals that fail | No refusal or rule-violation cases | Cover every category deliberately |
| Generated cases all pass | They test the agent's own description of itself | Write cases for gaps and edge inputs by hand |
| Turn one passes, the conversation still fails | Only single-turn cases | Add conversations with turns that refer back |
| A test set shows data a maker should not see | Generated from a privileged account's sources | Generate under an account scoped like your users |
| Last quarter's runs are gone | Standard-harness results expire after 89 days | Export runs you need to keep |

## Key terms

**Evaluation set (test set)**: the fixed list of test cases an evaluation runs.

**Test case**: one conversation (or, on the standard harness, one question) with an optional expected response.

**Quick conversation set**: ten generated conversations from the agent's description, instructions and topics.

**Category**: the brief slot a case tests: happy path, edge, rule, refusal, escalation or tone.

**Multi-turn case**: a test conversation whose later turns depend on earlier ones.
