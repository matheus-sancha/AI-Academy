## TL;DR

The preview pane lets you chat with your draft agent and see what it did. On the GitHub Copilot harness
that is the **Preview** tab and its **activity trace**; on the standard harness, the **test panel** and its
**activity map**. Both show which knowledge, tools and skills or topics were used, with what inputs, and
what came back. Read that before changing anything: most bad answers come from the model choosing
reasonably among descriptions you wrote badly, and rewriting the instructions fixes none of them.

## Why it matters

A bad answer has at least four causes, and from the outside they look the same:

1. the agent retrieved nothing;
2. it retrieved the wrong thing;
3. it retrieved the right thing and misread it;
4. it did the right thing, and the question was ambiguous.

Only the third is an instructions problem. The reflex is to rewrite the instructions anyway, which fixes
one case in four and makes the agent longer and slower in the other three. The trace tells you which case
you have in about ten seconds.

This is also where debugging an agent stops looking like debugging code. The same input can produce a
different output, which changes what counts as evidence.

## How it works

<!-- volatile verified=2026-09 -->
**GitHub Copilot harness.** Open the **Preview** tab. With **End user preview** off — the default maker
view — the activity trace sits beside the chat and updates as the turn runs, and a **reasoning card** in
each reply shows the agent's chain of thought. Turn End user preview on to see what a user sees.
Selecting a component in the trace opens it in Build.

**Standard harness.** Select **Test** to open the test panel. With generative orchestration, the activity
map follows the orchestrator's plan; with it closed and **Track between topics** on, you follow the path
node by node, and each node that fired is marked. The **Variables** panel's **Test** tab shows variable
values as the conversation runs ({{topic:variables}}).
<!-- /volatile -->

The trace is a list of steps. On the GitHub Copilot harness the node types are **User message**,
**Knowledge**, **Ran action**, **Tool**, **Connector**, **Flow**, **Skill**, **Error**, **Agent response**
and **Complete**; each opens to show its input, its output, how long it took and any error. Read it top to
bottom against this table:

| What the trace shows | What it means | Where the fix is |
|---|---|---|
| No knowledge, no tool | It answered from the model | Grounding: the instructions, or {{topic:genai}} |
| Knowledge searched, nothing relevant back | A retrieval problem | The source, its content, its description |
| The right passage back, a wrong answer | A reading problem | Instructions, or the model |
| The wrong tool or skill ran | Its description does not say when to use it | The description ({{topic:orchestration}}) |
| The right tool, wrong inputs | Parameter descriptions, or an ambiguous question | The tool's input descriptions ({{topic:tooldesc}}) |
| An **Error** node | Authentication, access, a timeout or a moderation flag | Build or Settings, as the error says |

Three of those six rows point somewhere other than the instructions.

### Editing while you test

<!-- volatile verified=2026-09 -->
On the GitHub Copilot harness you do not have to stop a conversation to change the agent. A turn in
progress finishes on the old configuration; the next turn picks up your Build edits — including a new
tool, a model change or turning on memory. If a change has not taken effect after a couple of turns,
Microsoft's advice is to start a **New chat**.
<!-- /volatile -->

The one known exception is a skill, which binds when the conversation starts ({{topic:conversation}}).

### One run is not a result

The model is not deterministic, and repeating a question within a chat almost guarantees a different
answer, because earlier turns are part of the input. So:

- **One failure is a hypothesis.** Run it three times, each in a new chat. Three out of three is a defect;
  one out of three is variance, and you will not be able to tell whether a fix worked.
- **One success is not a pass.** An abstention that held once may not hold next time. A fixed question
  set, run repeatedly, is what turns *it works* into a measurement ({{topic:whyeval}}).

### What the pane is not

It is not your users. It runs with **your** access, and knowledge sources such as SharePoint answer each
user from what that user can open — so a source that answers you perfectly can return nothing for a
planner, and the agent abstains rather than erroring. The standard harness also states that its test panel
does not replicate every channel behaviour: timer and inactivity triggers may not fire there. And it is a
debugger, not a test suite: keep a written list of questions from day one, because that list becomes your
evaluation set ({{topic:testsets}}).

## In practice at Technik

In a new chat in Preview, ask the Technik Production Assistant:

> *What's the latest released revision of drawing `DU700001042`, and which ECN changed it?*

The answer names revision D, which you know is wrong: D is still in work. Before touching the
instructions, open the trace:

1. **Tool** — the revision lookup ran, with `DU700001042`. Right tool, right input.
2. Its output lists revisions A to D with their `RELEASE_STATUS` values.
3. **Agent response** — it picked the highest letter.

That is row three: the right data, misread. The fix is one line in the tool's output description — *only
rows with `RELEASE_STATUS = Released` count as released* — not a paragraph in the instructions. Ask again
three times, in three new chats.

Now ask something the assistant should refuse: *"What torque does the industry use for these flange
bolts?"* The trace shows no Knowledge node and no Tool node. If the answer is an abstention, grounding
held. If it is a confident number, the model answered from its own knowledge — and on this harness only
the instructions stand in the way ({{topic:genai}}).

> [!TIP]
> Before changing anything, write down the question, the answer and what the trace showed. Three of those
> notes usually make the pattern obvious, and none of them survive being remembered.

## Design guidance

- **Read the trace before changing anything.** Diagnosis, then treatment.
- **Start a new chat before every test that is meant to tell you something.**
- **Run a failure three times** before treating it as a defect.
- **Change one thing, then re-run the whole list**, not just the failing case.
- **Test the refusals deliberately.** They fail quietly in production.
- **Have someone with different access test it** before you publish ({{topic:testidentity}}).
- **Record the model and settings** with any result you mean to rely on.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Hours rewriting instructions, no improvement | The problem was retrieval or a description | Read the trace; fix where it points |
| A fix works, then does not | Variance mistaken for a fix | Three runs, before and after, in new chats |
| It works for you, not for users | The pane runs with your access | Test as another user before publishing |
| Only the happy path was tested | Refusal cases are easy to skip | Write them into the question list |
| Last week's result cannot be reproduced | Model or settings changed unrecorded | Record both with every result |
| An inactivity message never appears in the test panel | The standard-harness test panel does not replicate timer triggers | Test it in a published channel |
| No activity trace beside the chat | End user preview is on | Switch to the maker view |

## Key terms

**Preview tab / test panel** — where you chat with a draft agent, on the GitHub Copilot and standard
harness respectively.

**Activity trace / activity map** — the per-turn record of what the agent did, per harness.

**End user preview** — the Preview toggle that hides the trace and shows what a user sees.

**Variance** — different output from the same input. Normal, and why one run proves little.

**Abstention** — the agent saying it cannot find something. A behaviour to test, not to hope for.
