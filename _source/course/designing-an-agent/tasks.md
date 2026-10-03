## TL;DR

A task is a **verb phrase with a trigger and a finished state**: what starts it, and how you know it is done.
*"Help with reporting"* is not a task. *"Draft the weekly production summary from the shift logs, ready for the
supervisor to sign"* is one, because you can tell whether it happened. Write one line per task, one output per
line. Every happy-path test case you write later comes out of this list, so a vague task produces a vague test.

## Why it matters

Ask what an agent should do and you get **areas**: reporting, quality, documents. Areas are a fine way to
introduce an agent and no way to build one. An area cannot be tested, because nothing in it says what a
finished answer looks like, so it cannot fail. It cannot be instructed either: the model gets a topic and
invents the job.

The tasks slot is where areas become jobs. It is also the slot every later stage leans on hardest. The
instructions' `<tasks>` section is drafted from it ({{topic:tasksvsinstr}}), and the evaluation set takes its
happy-path cases from it, one or more per task.

## How it works

### The four parts of a task

| Part | Says | Weak | Strong |
|---|---|---|---|
| **Verb** | What the agent does, precisely | help with, handle, support | draft, list, report, compare |
| **Object** | What it does it to, or from | reports | the weekly production summary, from the shift logs |
| **Trigger** | What starts it | (unstated) | the supervisor asks for this week's summary |
| **Finished state** | The observable end | a good summary | ready for the supervisor to sign |

The **verb** decides whether a person can check it. Microsoft's guidance for instructions asks for precise,
specific verbs such as *ask*, *search*, *send*, *check* and *use*, and the same verbs make a task checkable. You
can look at an output and say whether it *lists* the open notifications. You cannot look at one and say whether
it *helped*.

The **trigger** decides what the agent needs before it starts. A task triggered by *"the user gives a work
order number"* has an input; a task with no trigger has an input nobody has named, and nothing says what
happens when it is missing ({{topic:inputsoutputs}}).

The **finished state** is the part people leave out. Microsoft gives every step of an agent workflow a goal,
an action and a **transition**: clear criteria for moving to the next step or ending. A task's finished state
is that transition for the whole job. Without it the model decides by itself when it is done, and so does
whoever tests it.

### One output per task

Microsoft's guidance makes tasks **atomic**: *"Extract metrics and summarize findings"* becomes two separate
steps, because a model given both at once may merge or reinterpret them. Apply the same test to the brief. If a
task produces two things, it is two tasks, and each gets its own test case and its own way to fail.

### Tasks are where tests come from

Microsoft's evaluation checklist builds the first test set from the agent's key scenarios: one test prompt
per scenario to start, each with an expected response and **acceptance criteria**, written as what passes and
what does not. A well-formed task hands you all three:

- the **trigger** becomes the test prompt;
- the **object and verb** say what the expected response contains;
- the **finished state** is the acceptance criterion.

A task that cannot be turned into a case this way is not finished. Fix the task, not the case.

## In practice at Technik

The Production Assistant's capability areas from the scenario are areas, not tasks. *Work order information*
names a subject. The tasks slot turned each area into one or more jobs:

| Area | Task |
|---|---|
| Work order information | Given a work order number, **report** its status and current operation, in words a supervisor can read |
| Work order efficiency | Given an operation, plant and period, **report** efficiency as routing hours over actual hours, with the hours it came from |
| Quality Notifications | Given a project, and optionally an operation, **list** the open QNs with number, defect type and priority |
| Teamcenter revision information | Given a drawing, part or document number, **report** the latest released revision and the ECN that released it |
| Document revision & creation | Given a controlled document and a released ECN, **draft** the next revision in the authoring template, ready for the document owner to submit for review |

Two of these are worth a second look.

The last row ends *ready for the document owner to submit for review*, not *a revised document*. That finished
state says who acts next and that the agent does not submit anything, which is also where its approval sits
({{topic:hitl}}).

The first draft of the quality task read *"Help engineers stay on top of QNs."* It failed on every part: no
precise verb, no object, no trigger, no end. Pushed for an example, the quality engineer said *"I want the open
ones on my project, so I know what's blocking FAT."* That sentence held the trigger (a project), the object
(open QNs) and the reason, and the task above came almost straight out of it.

The first happy-path case followed from the third row with no extra thought:

| Test prompt | Expected response contains | Passes when |
|---|---|---|
| *Show open QNs on cladding for project `PRJ-2031`.* | Every open cladding QN on `PRJ-2031`, with number, defect type and priority | All open ones are listed, no closed ones are, and each has the three fields |

## Design guidance

- **Turn every area into tasks**, and keep the area only as a heading.
- **Start each task with a precise verb** you could check an output against.
- **Name the trigger**, because it names the input.
- **End each task in an observable state**, ideally naming who acts next.
- **One output per task.** Split anything joined by *and*.
- **Write the first test case beside each task.** If it will not come, the task is not finished.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Tests for an area pass whatever the agent says | The area was never turned into tasks | Write tasks with finished states; derive cases from them |
| The agent does half a job and stops, or never stops | No finished state | State the observable end of each task |
| One test fails and nobody can say which part | A task with two outputs | Split it into two tasks and two cases |
| The agent asks for things users never provide | Task written without its trigger | Name the trigger and check users can supply it |
| Tasks read like procedures | How it is done written into the task | Keep the output in the task; move the steps to instructions ({{topic:tasksvsinstr}}) |

## Key terms

**Task**: a verb phrase with a trigger and a finished state, producing one output.

**Capability area**: a subject an agent covers, such as quality. Not a task.

**Trigger**: what starts a task, and so what the agent must have before it begins.

**Finished state**: the observable end of a task, often naming who acts next.

**Happy-path case**: a test case for a task done as intended, derived from the task itself.
