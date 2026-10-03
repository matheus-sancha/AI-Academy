## TL;DR

`<tasks>` and `<instructions>` are the two sections people mix up, and one test separates them: if a line
answers **what does it produce**, it is a task; if it answers **what does it do next**, it is an
instruction. Mix them and you get instructions that read like a job description and an agent that never
does anything in a particular order. It matters more than it sounds, because the tasks list is also where
your evaluation's **happy-path cases** come from: one task, at least one case.

## Why it matters

Ask someone to describe their agent and they will describe its tasks: *"it reports work order status, it
looks up revisions, it drafts QN write-ups."* Ask how it should handle a work order question and they
describe a procedure: *"check the number, call the tool, then say which operation it is at."* Both
belong in the instructions, but they do different jobs, and putting them in one list ruins both.

A tasks section full of procedure stops telling anyone — the model, a reviewer, the person writing
tests — what the agent is *for*. An instructions section full of outputs has no order in it, so the model
improvises one, and improvises differently each time.

## How it works

### The test

| The line answers… | It is a… | It goes in… | It reads like… |
|---|---|---|---|
| *What does it produce?* | **Task** | `<tasks>` | *Given X, produce Y* |
| *What does it do next?* | **Instruction** | `<instructions>` | *When X happens, do Y, then Z* |

A task is a **contract**: the input it receives and the output it hands back, with nothing about how. An
instruction is a **procedure**: an order of steps, what to check first, what to do when something is
missing. The same capability usually needs one of each.

### Tasks: a list of outputs

Each task names its input and its finished output. Inputs belong here because a task without one is a
wish — *"report revisions"* says nothing about what the user has to provide, so nothing says what happens
when they do not.

Tasks are **independent of each other**. Microsoft's guidance makes the same distinction in general terms:
use bullets for parallel things that can be done independently, and keep numbered steps for things that
must happen in sequence. The tasks list is the bullets.

What does **not** go in `<tasks>`:

- **How a task is done** — that is `<instructions>`.
- **How good it has to be** — success criteria measure the agent, and the agent cannot act on them. *"95%
  of answers cite a document"* is something you test for, not something you tell the agent. It stays in
  the design brief ({{topic:successcriteria}}).

### Instructions: where order lives

Instructions are written as triggers and steps: *when this arrives, do this, then this*. Microsoft's
guidance for step-by-step workflows gives each step three parts — a **goal**, an **action** with the tool
it uses, and a **transition**, the condition for moving on or stopping. The transition is the part people
omit, and without it the model decides by itself when a step is done.

Make each step atomic. *"Look up the work order and summarise its status"* is two steps, and when it fails
you want to know which.

### Why the tasks list feeds your tests

An evaluation needs **happy-path cases**: realistic requests the agent should handle well. The tasks list
is exactly the set of things the agent promises to produce, so each task becomes at least one case — its
input as the question, its output as the expected result ({{topic:testsets}}).

That works in both directions. A task with no test case is a promise nobody checks. A test case that maps
to no task is testing something the agent was never asked to do. And if your tasks are written as
procedure, you cannot derive cases from them at all, which is usually how this mistake gets found.

## In practice at Technik

A first draft of the Technik Production Assistant's `<tasks>`, written in one sitting:

1. Help engineers with work orders.
2. Look up the work order number in SAP, then report its status and current operation.
3. When someone asks about a revision, check the part number format first.
4. Draft QN write-ups in Technik's format.
5. Always cite the document and revision.
6. Be fast.

Run the test over each line:

| Line | Answers… | Verdict |
|---|---|---|
| 1 | Neither — no input, no output | Rewrite as a task |
| 2 | Both | Split: the output is a task, the order is an instruction |
| 3 | *What does it do next?* | Move to `<instructions>` |
| 4 | *What does it produce?* — but with no input | Task; name the input |
| 5 | Neither — it is a constraint on every answer | Move to `<rules>`, with its reason |
| 6 | Neither — it is a success criterion | Remove; it belongs in the brief |

After the split:

```xml
<tasks>
- Given a work order number, report its status and current operation.
- Given a part or drawing number, report the latest released revision and the ECN that released it.
- Given a QN number, draft a write-up in Technik's QN format.
</tasks>

<instructions>
When a question names an identifier:
1. Check its format. If a nine-digit number could be a work order or a QN, ask which.
2. Call the tool that matches. Work orders: Get work order status. Revisions: Get released revision.
3. If the tool returns nothing, say the record was not found. Do not retry with a guessed number.
</instructions>
```

Each task now gives a happy-path case: *"What's the status of work order `100004521`?"*, expecting its
status and its current operation; *"Latest released revision of `DU700001042`?"*, expecting the revision
and the ECN behind it; *"Write up QN `300001211`"*, expecting Technik's format. The step about guessed
numbers gives a different kind of case — the one where the tool comes back empty.

## Design guidance

- **Run the test on every line** before you save: produce, or do next?
- **Write tasks as *given X, produce Y***, with the input named.
- **Write instructions as triggers and numbered steps**, with a transition for each.
- **Keep success criteria out of the instructions**, and in the brief where tests are built from them.
- **Derive one happy-path case per task**, and treat a task with no case as untested.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent skips steps, or does them in a different order each time | The procedure is written as a list of outputs | Move it to `<instructions>` as numbered steps |
| Instructions read like a job advert | Tasks have no inputs or outputs | Rewrite as *given X, produce Y* |
| The evaluation misses a capability | A task has no matching case | Derive one case per task |
| The agent tells users it aims for 95% accuracy | A success criterion went into the instructions | Remove it; keep it in the brief |
| A step "finishes" at the wrong moment | No transition was written | Add the condition for moving on |

## Key terms

**Task** — a line in `<tasks>`: given an input, the output the agent produces.

**Instruction** — a line in `<instructions>`: what the agent does next, and in what order.

**Transition** — the condition that ends one step and starts the next.

**Happy-path case** — an evaluation case for a request the agent should handle well, derived from a task.
