## TL;DR

The test pane lets you chat with the draft agent; the **activity map** shows what it actually did —
which topic fired, what was searched, which tool ran with which inputs, and what came back. Read the
map before you change anything. Most time lost debugging agents is spent rewriting instructions to
fix a problem that was never in the instructions.

## Why it matters

A bad answer has at least four possible causes, and they look identical from the outside:

1. the agent never retrieved anything;
2. it retrieved the wrong thing;
3. it retrieved the right thing and misread it;
4. it did the right thing and the question was ambiguous.

Only the third is an instructions problem. The reflex is to rewrite the instructions for all four,
which fixes one case in four and makes the agent longer and slower in the other three. The activity
map tells you which one you have, in about ten seconds.

This is also the point in the course where debugging an agent stops resembling debugging code. The
same input can produce different output. That changes what evidence means, and the second half of
this lesson is about that.

## How it works

<!-- volatile verified=2026-09 -->
The test or preview pane, and where the activity map appears within it, have moved and been renamed
more than once. What it shows is stable; where you click is not. Follow the linked documentation if
the pane does not look like this description.
<!-- /volatile -->

You type a question, the agent answers, and the map for that turn shows the steps it took. Read it
top to bottom and match what you see against this table:

| What the map shows | What it means | Where the fix is |
|---|---|---|
| No retrieval, no tool call | It answered from the model | Generative AI settings ([genai](genai.html)), then the instructions |
| Knowledge searched, nothing relevant returned | A retrieval problem | The source content, its chunking, its description (B6) |
| The right passage retrieved, a wrong answer | A reading problem | Instructions, or the model |
| The wrong tool called | Its description does not say when to use it | The tool description (B7) |
| The right tool, wrong inputs | Parameter descriptions, or an ambiguous question | The tool's input descriptions (B7) |
| The wrong topic fired | Overlapping trigger phrases | The topic ([Topics](topics.html)) |
| Nothing fired and the fallback answered | Nothing matched | Trigger phrases, or the question is genuinely out of scope |

That table is most of the diagnostic skill in this course. Three of its seven rows point somewhere
other than the instructions.

### One run is not a result

The model is not deterministic. The same question can retrieve the same passage and answer
differently, and that has two consequences people learn the hard way:

- **One failure is a hypothesis.** Run it three times. If it fails three times out of three, it is a
  defect. If it fails once, you have found variance, and you will not be able to tell whether your
  fix worked.
- **One success is not a pass.** An abstention rule that held once may not hold next time. This is
  precisely why B13 exists: a fixed question set, run repeatedly, is the only way "it works" becomes
  a measurement rather than an impression.

### The test pane runs as you

Whatever you can see, the agent can see. That is convenient now and misleading later: a SharePoint
source that answers perfectly for you may return nothing for a planner with fewer permissions, and
the agent will abstain rather than error — which looks like a retrieval bug and is not one.

So before you publish (B12), have somebody else try it. You cannot discover this by testing harder
yourself.

### What the pane is not

It is manual, it forgets what you asked yesterday, and nothing stops you from testing only the
questions you already know work. It is a debugger, not a test suite. Keep a written list of
questions from the first day — that list is what becomes the evaluation set in B13, and starting it
later means reconstructing it from memory.

## In practice at Technik

This module's agent has no knowledge and no tools, so the only honest answer to almost anything is
that it cannot look it up. That makes it an unusually good subject for a first reading of the map,
because there is nothing to hide behind.

Ask *"What is the minimum overlay thickness?"* and you get one of two things:

| Answer | Map | Meaning |
|---|---|---|
| "I don't have a source for that" | Nothing retrieved, no tool | Correct. The settings and instructions are doing their job |
| "The minimum overlay thickness is typically 3 mm…" | Nothing retrieved, no tool — **the same map** | The model answered from training. General knowledge is on, or the grounding rule is not holding |

The two answers are miles apart and the maps are nearly identical. That is the lesson: the map tells
you what the agent *had*, and the answer tells you what it *did with it*. You need both, and neither
alone is enough.

Then ask *"What's the status of work order 100004521?"* and you should see the *Work order status*
topic fire, `Global.WorkOrderNo` set to `100004521`, and a message saying it cannot be looked up yet.
Ask the same thing with a part number — `P7000001088` — and you should see the validation branch
reject it. Two questions, two visible paths, and you have confirmed the topic works without
believing anything.

Keep the answer to the overlay thickness question. B6 asks it again with documents attached, B7 with
a tool, and the shape of the map each time is how the whole Beginner track shows its work.

> [!TIP]
> When an answer is wrong, write down the question, the answer and what the map showed, before you
> change anything. Three of those notes usually make the pattern obvious, and none of them survive
> being remembered.

## Design guidance

- **Read the map before changing anything.** Diagnosis, then treatment.
- **Run a failing question three times** before treating it as a defect.
- **Change one thing, then re-run the whole list**, not just the case you were fixing.
- **Keep a written question list from day one.** It becomes your evaluation set (B13).
- **Test the abstention cases deliberately.** Ask things it should refuse; those are the ones that
  fail quietly in production.
- **Have someone with different permissions test it** before publishing (B12).
- **Record the model and settings** with any result you intend to rely on.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Hours spent rewriting instructions with no improvement | The problem was retrieval or a tool description | Read the map; fix where it points |
| A fix works, then does not | Variance was mistaken for a defect, or for a fix | Three runs before and after |
| It works for you, not for users | The test pane runs with your permissions | Have someone else test before publishing (B12) |
| Only the happy path was ever tested | Abstention cases are easy to skip | Write them into the question list |
| Nobody can reproduce last week's result | The model or settings changed and were not recorded | Record both with every result |
| "It feels better after the change" | No fixed question set | Start one now; formalise it in B13 |
| The agent answers well in the pane and badly once published | Different channel, permissions or authentication | Re-test in the channel (B12) |

## Key terms

**Test pane** — the chat-with-your-draft surface.

**Activity map** — what the agent did in one turn: topics, knowledge, tools, inputs and results.

**Variance** — different output from the same input. Normal, and the reason one run proves little.

**Abstention** — the agent saying it cannot find something. A behaviour to test, not just to hope for.

**Question list** — the growing set of questions with known answers that becomes an evaluation set
(B13).

**Fallback** — the system topic that answers when nothing matched ([Topics](topics.html)).
