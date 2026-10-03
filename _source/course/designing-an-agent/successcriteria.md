## TL;DR

Success criteria are how you will know the agent is working, and they go **nowhere in the instructions**.
They measure the agent; the agent cannot act on them. Telling it *"answers should be accurate"* changes nothing
about its behaviour and costs context on every turn. They belong in the brief, where the evaluation set's
acceptance criteria and the human review rubric are derived from them. A criterion is filled when it says how
someone would judge **one run** good, in terms **visible in the output**.

## Why it matters

This lesson has to survive being obvious. Nobody sets out to put a measurement into the instructions. It
happens because success criteria *sound* like instructions: *"accurate"*, *"helpful"*, *"answers match
Teamcenter"*. They are about the agent's behaviour, they are written in the imperative mood, and the
Instructions field is right there.

The result is two failures at once. The instructions grow by sentences that change nothing, because the agent
was already trying to be accurate. And the evaluation has nothing sharp to grade against, because the criterion
was written to be read by the model rather than checked by a person. Microsoft's guidance on agent evaluation
puts the order the other way round: *before you run evaluations, define what success looks like for your
agent*.

## How it works

### The test: can the agent do anything differently?

Read each candidate line and ask: **on this turn, with this question, what would the agent do differently
because of this sentence?**

| Candidate | Can the agent act on it? | Where it goes |
|---|---|---|
| "Answers should be accurate." | No. It is already trying | The brief only |
| "9 in 10 revision answers should match Teamcenter." | No. It sees one answer, never ten | The brief: the evaluation's pass mark |
| "Every revision answer names the revision, its release status and the ECN." | **Yes.** It is a property of this answer | Instructions, as an output rule, **and** the brief, as a criterion |

The third row is the useful case. A good criterion often has a rule hiding in it. When it does, the rule goes
to the instructions in the agent's terms (*name the revision, status and ECN*), and the criterion stays in the
brief in the reviewer's terms (*does the answer name all three?*). They are two lines with two readers, never
one line copied into both.

### Visible in the output

A criterion that cannot be checked on a single run does not grade anything. *"Users trust it"* is a fine goal
and a useless criterion: no reviewer can look at one answer and score it. Rewrite it until a person could:

| Rejected | Accepted |
|---|---|
| "It works well." | "A planner can act on a work order answer without opening SAP." |
| "Good drafts." | "The document owner submits the draft after editing fewer than five sentences." |
| "Accurate answers." | "Every revision named is the latest Released one in `TC_*`, and the answer names its ECN." |

Each accepted line names a reader and something that reader can see.

### Where criteria go next

Criteria feed three things, and none of them is the agent:

- **Acceptance criteria on test cases.** Microsoft's evaluation checklist gives every case a test prompt, an
  optional expected response and acceptance criteria: *what passes and what doesn't*. A criterion from the
  brief becomes that column ({{topic:testsets}}).
- **The human review rubric.** The checklist's questions for judging a response, *does it answer the main
  question, does it use the correct information, is the tone appropriate, does it respect sharing
  permissions*, become concrete once the brief says what correct and appropriate mean for this agent
  ({{topic:feedback}}).
- **The pass mark.** Because agents give different answers to the same prompt, the checklist advises running a
  test set more than once and averaging, and aiming for a realistic pass rate of **80 to 90%** set by business
  need. The brief is where that number is agreed, with the people who will be told it later
  ({{topic:runeval}}).

The checklist ends on a standard worth adopting from the start: you are done when you can answer stakeholders
with specifics, not with *"the agent seems okay"*.

## In practice at Technik

The Production Assistant's success criteria slot, as first offered: *"It should give accurate answers and save
people time."* Neither half is visible in an output. Two rounds later:

> **Per answer**
> - A planner or supervisor can act on a work order answer without opening SAP.
> - Every revision answer names the revision, its release status and the ECN that released it, and the revision
>   is the latest Released one.
> - A revision draft is submitted by its owner after editing fewer than five sentences.
>
> **Across the evaluation set**
> - 9 in 10 revision answers pass, averaged over three runs.

Then each line was sent where it belongs:

| Criterion | Instructions get | Evaluation gets |
|---|---|---|
| Act without opening SAP | Nothing new. The tone and the output example already say *plain answer first* | A rubric line for human review of work order answers |
| Names revision, status and ECN | *"Name the revision, its release status and the ECN that released it."* | Acceptance criterion on every revision case |
| Fewer than five edits | Nothing. The skill's template carries the format | A reviewer's count on drafting cases |
| 9 in 10, three runs | **Nothing** | The pass mark |

This is the brief from {{topic:brief}} done properly. The first build had pasted the brief into the
instructions, and asked how reliable it was, the agent quoted *"9 in 10 of my revision answers should match
Teamcenter"* to a user. That line was true, and it did nothing for the answer it appeared in.

## Design guidance

- **Ask "what would the agent do differently?"** of every line before it enters the instructions.
- **Split a criterion that hides a rule**: the rule to the instructions, the criterion to the brief.
- **Write each criterion so one person can check one run.**
- **Name a reader in every criterion.** *Good* means good for someone.
- **Agree the pass mark in the brief**, and decide how many runs it is averaged over.
- **Keep aggregate targets out of the instructions entirely.** The agent never sees an aggregate.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent quotes its own targets to users | Criteria pasted into the instructions | Remove them; keep them in the brief |
| Instructions grew and behaviour did not change | Lines the agent cannot act on | Apply the *differently* test; delete what fails it |
| Evaluation passes everything | Criteria too vague to fail | Rewrite until one run can be judged |
| A rule appears in two wordings | The criterion was copied, not split | One line for the agent, one for the reviewer |
| Nobody can say whether a 78% run is bad | No pass mark agreed | Set it in the brief, with the number of runs |

## Key terms

**Success criterion**: how someone judges one run good, visible in the output. Lives in the brief.

**Acceptance criteria**: a test case's statement of what passes and what does not, derived from the brief.

**Pass mark**: the share of cases that must pass, averaged over several runs.

**Human review rubric**: the questions a person uses to judge a response, made concrete by the brief.
