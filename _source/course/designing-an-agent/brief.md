## TL;DR

Before you build an agent, write down what it is for: its role, its users, its tasks, its inputs and
outputs, its rules, what it escalates and what it refuses. That document is the **brief**. It is a design
record, read by people: whoever reviews the design, whoever writes the instructions, whoever writes the
tests. It is **not** the Instructions field, and pasting it there is the most common first mistake. A brief
is done when it is specific enough that someone else could check whether the finished agent does what was
asked.

## Why it matters

Most agents that disappoint were never wrong about the product. They were wrong about the job. Someone
asked for "an assistant for the plant", someone else built one, and both found out what they had each meant
when the first user asked a question neither had pictured.

A brief moves that discovery to the cheapest moment. A slot that cannot be filled ("who reads the output?")
is a conversation to have now, before any knowledge, tool or instruction exists to be redone. It also gives
the build something to be judged against. Without one, "does it work?" means "does it do what the builder
remembered being asked", and nobody else can check that.

## How it works

### Who reads a brief

The model never sees it. Three people do, and the brief is written for them:

- **The reviewer**, who decides whether the design is right before anyone builds it.
- **Whoever writes the instructions**, who turns the parts the agent can act on into runtime text
  ({{module:writing-instructions}}).
- **Whoever writes the evaluation set**, who turns tasks, rules and success criteria into test cases that
  can fail ({{module:testing-and-evaluation}}).

Microsoft's guidance on writing instructions begins with questions, not text: what goal must the agent
accomplish, what workflows do its users go through, and can each workflow be written as steps? The brief is
where those answers are written down, before any instruction is drafted.

### The slots

The design interview in {{module:the-six-skills}} fills thirteen slots, and this module teaches them in
groups. Each slot has an **acceptance test**: a check on the answer, not on the agent.

| Slot | Filled when it names… | Taught in |
|---|---|---|
| Role | What the agent does, for which function, in one sentence a stranger could repeat | this lesson |
| Users, Documents | Who talks to it, how expert they are; the real artifacts | {{topic:users}} |
| Tasks | Each task as a verb phrase with a trigger and a finished state | {{topic:tasks}} |
| Inputs, Knowledge, Outputs | Format, source and reliability of each input; format, reader and real example of each output | {{topic:inputsoutputs}} |
| Rules, Escalation | A must-never with its reason; a stop condition with a named recipient | {{topic:rules}} |
| Out of scope, Tone, Connected agents | What it will not do; a register chosen from real alternatives; what it hands off | {{topic:scope}} |
| Success criteria | How someone would judge one run good, visibly in the output | {{topic:successcriteria}} |

A slot is filled by a **concrete** answer, never a plausible one. *"Be accurate and professional"* sounds
like a rule and fails the test: it names nothing the agent must or must never do. Microsoft's AB-100 study
guide, for the solution-architect exam, lists *analyse requirements* and *define the solution rules and
constraints* as skills in their own right, before any design or deployment skill. Treat them as work, not
preamble.

### Design record, not runtime text

The brief and the instructions overlap in subject and differ in everything else:

| | Brief | Instructions |
|---|---|---|
| Reader | People | The model, on every turn |
| Voice | *About* the agent: "its users are planners" | *To* the agent: "answer in the user's terms" |
| Keeps | Reasons, the users' own words, success criteria | Only what the agent can act on |
| Length | As long as the design needs | Paid for in context on every turn ({{topic:contextcost}}) |

Pasting the brief into the Instructions field fails in three ways at once. The model reads sentences about
its users as if they were directions. Success criteria arrive as text the agent cannot act on and may
repeat to users ({{topic:successcriteria}}). And every turn pays for a document written for a reviewer. The
upstream design-interview skill puts a warning at the top of every brief it writes for exactly this reason.

### Where each part goes next

A brief is the source the rest of the build is derived from, which is why a thin slot shows up later as a
thin component:

| Brief slots | Become |
|---|---|
| Role, Tone, Tasks, Rules, Escalation, Out of scope | Sections of the instructions ({{topic:xml}}) |
| Knowledge, Inputs | Knowledge sources and tools ({{topic:triage}}) |
| Tasks, Rules, Out of scope, Escalation | Test cases ({{topic:testsets}}) |
| Success criteria | The evaluation's pass mark, and nothing in the instructions |

## In practice at Technik

The top of the Technik Production Assistant's brief, as it stands after the design interview:

```markdown
# Agent brief: Technik Production Assistant

> This is a design brief, not the agent's instructions.
> Do not paste it into the Instructions field.

## Role
Answers work order, quality notification and revision questions for Technik's
manufacturing and engineering staff, from SAP and Teamcenter data in Snowflake
and from controlled documents, and drafts document revisions for their owners.
```

The first draft of that role read *"Helps the plant with production information."* It fails the
acceptance test because a stranger cannot repeat it usefully: it names no function, no data and no output.
The accepted version tells a reviewer three things to check: which questions it answers, where the answers
come from, and the one thing it produces that is not an answer.

The brief also caught the most common first mistake before it happened. A first build had the whole brief
pasted under `<role>`. In the test pane the agent opened an answer about work order `100004521` with
*"As an assistant for production planners and quality engineers…"*, and, asked how reliable it was,
quoted the success criterion: *"9 in 10 of my revision answers should match Teamcenter."* Both lines were
true and neither belonged in front of a user. The instructions were rebuilt from the brief, section by
section, and the brief went back to being the record.

## Design guidance

- **Write the brief before you open Copilot Studio.** Every slot you fill now is a component you do not
  redo later.
- **Hold each answer to its slot's acceptance test.** A vague answer accepted now becomes a vague agent.
- **Write it for the person who reviews it**, so it says *about* the agent what someone can check.
- **Keep it out of the Instructions field.** Derive the instructions from it instead.
- **Keep it after the build.** It is the record of why the agent is the way it is, and the first thing to
  re-read when the agent changes.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent describes its own users or targets to the user | The brief was pasted into the instructions | Rebuild the instructions from the brief; keep the brief separate |
| Nobody can say whether the agent does what was asked | No brief, so no slot to check against | Write the brief, even after the fact, and test against it |
| A slot reads well and decides nothing | Answer accepted without its acceptance test | Re-ask until it names something checkable |
| The instructions keep growing | Design reasoning copied in alongside directives | Leave reasons and context in the brief |
| Test cases have no clear pass | Tasks and rules in the brief were vague | Fix the slot first; the case follows from it |

## Key terms

**Brief**: the written design record of what an agent is for. Read by people, never by the model.

**Slot**: one decision in the brief, such as users, tasks or rules.

**Acceptance test**: the check a slot's answer must pass before the design moves on.

**Design record**: a document that explains a system to the people who build, review and test it, as
opposed to runtime text the system reads.
