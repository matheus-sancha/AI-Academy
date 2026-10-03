## TL;DR

Three decisions that are cheap to make now and expensive later. **Out of scope**: what the agent will not
do, written down with what it says instead, so the next request does not quietly expand it. **Tone**: not
*"professional"* but a register chosen from real alternatives, plus one thing the agent must never sound like.
**Delegation**: which other agents this one hands work to and on what signal, decided before you build one
agent that does everything. *"None"* is a valid answer to the last, but only once you have asked.

## Why it matters

Each of these slots gets filled whether or not you fill it. Leave scope open and the next stakeholder request
fills it: *"while it's at it, could it also…"* is how an agent for work orders ends up answering pay questions
badly. Leave tone open and the model's default fills it, which is friendly, thorough and slightly reassuring,
and wrong for most users at work. Leave delegation open and accretion fills it: every new capability lands in
the one agent that exists, until routing degrades and splitting means redrawing the instructions, the tests and
who owns what.

All three are a few lines in a brief. None of them is a few lines once the agent is in use.

## How it works

### Out of scope: an area, and what the agent says instead

The slot is filled when it names **at least one thing users will plausibly ask for** that the agent must not
do, and **what it says instead**. Both halves matter. A list of exclusions with no redirect leaves the user at a
dead end, and they will rephrase until the agent tries anyway.

| | Rejected | Accepted |
|---|---|---|
| No boundary | "nothing really" | "will not answer pay, leave or overtime questions; says this agent covers production data and points to the HR portal" |
| Implausible | "won't write poems" | "will not post confirmations or change anything in SAP; says where in SAP to do it" |

Out of scope lists **whole areas**. It is not the same as a refusal ({{topic:rules}}), which is one request
*inside* the agent's domain that it declines because a person owns the answer. Out of scope says *not my
subject*; a refusal says *my subject, not my decision*. Both end up in the instructions, and both become test
cases: Microsoft's evaluation checklist lists *not allowed and out of scope behaviors* as edge cases with their
own test set ({{topic:testsets}}).

Microsoft's guidance for the GitHub Copilot harness names the same content: instructions should include the
*subjects or tasks the agent should decline or redirect*. The brief is where you decide which, so the
instructions have something to say.

### Tone: a register, and one thing it must never sound like

*"Professional"* fails because every alternative on the table is professional. A tone decision is a choice
between real registers, and it only becomes visible when you write the same answer three ways:

| Register | The same work order answer |
|---|---|
| Terse | `100004521: REL, op 0040 Welding, INPROC.` |
| Plain, answer first | *Work order 100004521 is released and in progress at Welding (operation 0040).* Then the detail. |
| Explanatory | *Good question! Work order 100004521 has been released, which means…* |

None of these is wrong in general. Each is wrong for somebody, and the users slot already said who
({{topic:users}}). Microsoft's guidance lists tone and style (formal, friendly, concise) among what instructions
should set, and it gets its own `<tone>` section ({{topic:xml}}). Left unset, the model infers a tone, and
not the same one on every model ({{topic:writinginstructions}}).

The second half of the slot, **one thing it must never sound like**, is often the more useful line. A register
describes the centre; the *never* marks the edge a user would notice first.

### Delegation: which agents, and on what signal

The connected-agents slot names every other agent this one hands work to, and the **exact signal** that triggers
each hand-off. *"It might talk to the planning bot"* names a neighbour and no signal, so nobody can build or test
it.

*"None"* is a valid answer, and often the right one, but ask before accepting it. Microsoft's guidance for
multi-agent design starts from caution: it is *not always necessary*, and each hop adds latency and more to
test and govern. It also names when separate agents earn their keep:

- different teams own different parts, or need separate release and lifecycle management;
- a part needs its own settings, such as its own model;
- a part should be reusable by more than one agent, or published on its own;
- the agent's ability to tell its choices apart starts to degrade, which Microsoft's rule of thumb puts at
  **more than 30 to 40** tools, topics and agents, or fewer if their descriptions are similar.

The brief records the decision and the signal, not the mechanism. Whether the neighbour is a child agent or a
connected one, and how the hand-off carries context, is {{topic:connected}}'s job. What the brief has to make
sure of is that the question was asked before the build, because the answer decides how the instructions and
the evaluation set are divided.

## In practice at Technik

The Production Assistant's three slots, after the interview.

**Out of scope.** The first answer was *"nothing really, it's for everything production"*. Asked what planners
actually type into Teams, the team named two things the agent should not touch:

> Will not answer pay, leave or overtime questions; says it covers production data and points to the HR
> portal. Will not post confirmations or change anything in SAP or Teamcenter; says which transaction or
> workflow the user needs, because the agent reads `TECHNIK_AGENT_RO` and writes nothing.

The second one matters most. *"Confirm operation 0040 for me"* is a plausible request from a supervisor with
their hands full, and an agent that answers *"Done"* without a write tool is the worst outcome available.

**Tone.** The interview offered the three registers above for a supervisor's question. The supervisors chose
*plain, answer first*. The quality engineer added the line that became the *never*: *"I don't want it telling
me it's probably fine."* The slot reads:

> Plain and technical. Short answers first, detail on request. Never reassuring about a defect.

**Delegation.** The first answer, *"it might hand things to the planning tool"*, named no signal and no agent
that exists. Asked again, the answer was none: seven capability areas, one owner, one release. The brief records
that, and the condition that would change it:

> None. Revisit if Teamcenter documents and revisions get a separate owner from SAP production data.

That is the split {{module:advanced-tools-and-multi-agent}} later makes, and it is in the brief already.

## Design guidance

- **Write out of scope as areas a real user would ask about**, each with what the agent says instead.
- **Keep refusals and out of scope apart.** One is *not my subject*, the other *not my decision*.
- **Choose tone by writing one answer in three registers** and asking the users which they would act on.
- **Add the one thing it must never sound like.** It is usually the line users remember.
- **Ask about neighbours before accepting "none"**, and record the signal for every hand-off.
- **Record the condition that would change the delegation answer**, so the split is a decision, not a drift.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent keeps growing into nearby subjects | Out of scope never written | Name the areas; route new requests through the brief |
| Users rephrase until an excluded request gets an answer | Exclusion with no redirect | Say what the agent offers instead |
| Answers sound chatty or reassuring | Tone left to the model's default | Pick a register from real alternatives and add a *never* |
| One agent handles everything and routing is slipping | Delegation never decided | Decide it now; see {{topic:connected}} before splitting |
| A hand-off exists and nobody can test it | Neighbour named, signal not | Name the exact signal for each hand-off |

## Key terms

**Out of scope**: an area the agent does not cover, recorded with what it says instead.

**Register**: the voice of an answer: how terse, how technical, how warm.

**Connected-agents slot**: the brief's record of every agent this one hands work to, and the signal for each.

**Hand-off signal**: the condition in a request that sends it to another agent.
