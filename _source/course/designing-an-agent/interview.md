## TL;DR

You will usually fill the brief in for somebody else, and how you ask decides what you get. **One question per
message.** Offer three or four **genuinely different, concrete options**, one of them recommended, plus a way
out, because someone who has never designed an agent does not know what a tone decision involves until they
read three real alternatives. **Never accept a slot that fails its test**: say what is missing and ask again.
And **keep the answers in their own words**. The binding constraint is usually in *how* they said it, and it
cannot be recovered once you have smoothed it into your own prose.

## Why it matters

The people who know what an agent is for are rarely the people who build it. A quality engineer knows which
decisions are theirs; a planner knows which codes they read without thinking. Neither has a brief in their
head, and neither will produce one if handed a template with thirteen headings. They will fill the easy slots,
leave the hard ones vague, and both of you will believe the design is done.

The interview is how the brief gets filled honestly. Microsoft's AB-100 study guide, for the solution-architect
exam, lists *analyzing and interpreting business and technical requirements* among the architect's key
responsibilities. The interview is what that work looks like in practice.

## How it works

The mechanics below follow the upstream `copilot-agent-review` skill, at {{skills-version}}, which runs this
interview for you in {{module:the-six-skills}}. You will also run it yourself, in a meeting or a chat, and the
rules are the same.

### One question per message

Never two, never a batch. A message with three questions gets the easiest one answered well, the second
answered briefly, and the hardest one skipped. Nobody notices, because the reply looks complete.

### Options that teach, one recommended, a way out

Each question is numbered and offers **three or four concrete options**, one marked *recommended*, plus an
escape hatch:

```text
Q12. How should the assistant sound when it answers a supervisor?

  A. Plain, answer first: one sentence, then the detail (recommended)
  B. Terse: the codes and numbers, nothing else
  C. Explanatory: walk through what each status means

Reply A, B or C, or describe it yourself.
```

The options are not decoration. A person asked *"what tone should it have?"* says *"professional"*, because they
have nothing to compare against. Shown three real answers, they can point. The options must be **genuinely
different**, and **specific to what they have already told you**: this example only works because the users slot
already established that supervisors do not read SAP codes. Generic filler options teach nothing.

The recommendation gives a hesitant person a good default to accept. The escape hatch lets the person who knows
better say so, in their own words, which is the answer you most want.

### Never invent, never move on

If they have not said it, it is not known: ask. And test every answer against its slot's **acceptance test**
({{topic:brief}}) before moving on. When it fails, name what is missing:

> That tells me the format but not who reads it. Who receives the finished draft?

Re-asking is the job. A vague answer accepted now becomes a vague agent later.

### The order, and the artifacts

The skill fills the thirteen slots in a fixed order: role, users, documents, tasks, inputs, knowledge, outputs,
rules, escalation, connected agents, out of scope, tone, success criteria. Tasks, inputs, outputs and rules get
the most effort, because the rest of the build consumes them.

**Documents** comes straight after users, as a single request for the real artifacts: sample outputs,
templates, policies ({{topic:users}}). When files arrive, say in one line each what you learned and which slot it
fills, then ask about what they show.

### Keep their words

When every slot passes, show one line per slot and ask for corrections before writing anything: it is the
cheapest moment to fix a misunderstanding. Then the brief gets a **Source quotes** section: the person's own
words on tasks, inputs, outputs, rules and escalation, verbatim, as block quotes.

This is the rule that is easiest to break with good intentions. Turning a rambling answer into a tidy sentence
feels like doing the job. It also throws away the part that binds: the qualifier, the example, the word they
chose instead of the obvious one. Whoever writes the instructions or the tests later cannot get it back.

## In practice at Technik

The tone question above went to a supervisor and a quality engineer together. The supervisor picked **A**. The
quality engineer used the escape hatch:

> A, but I don't want it telling me it's probably fine.

The tidy version of that, *"be appropriately cautious"*, is the kind of line an interviewer writes without
noticing. It would have been accepted, and it would have failed: it names no behaviour. The verbatim line names
exactly one, which became the tone slot's *never*: **never reassuring about a defect** ({{topic:scope}}).

The quality task went the same way. The first answer, *"help engineers stay on top of QNs"*, failed the tasks
test and was asked again, this time for an example:

> I want the open ones on my project, so I know what's blocking FAT.

That sentence held the trigger, the object and the reason ({{topic:tasks}}). A summary would have kept *open QNs
by project* and dropped *blocking FAT*, the one part that says why the list matters and which miss would hurt
most. The Source quotes entry kept it, and the evaluation writer later used it to choose the first case: a
project with a unit due for FAT.

The escalation slot needed three asks:

| Ask | Answer | Test result |
|---|---|---|
| Q9, with options | "Escalate to quality." | Fails: a department, not a recipient |
| *Who, by name, when sources disagree?* | "Whoever owns the document." | Fails: owner of which, and where is that recorded? |
| *Where is the owner recorded?* | "It's on the document in Teamcenter." | Passes: `TC_DOCUMENTS.OWNER` ({{topic:rules}}) |

Each re-ask named what was missing and nothing else.

## Design guidance

- **Ask one question per message**, always.
- **Write options from what they have already said**, three or four, one recommended, plus a way out.
- **Test every answer against its slot** before moving on, and say what is missing.
- **Ask for artifacts once, early**, and cite what they showed in later questions.
- **Confirm the whole brief in one-line form** before writing it.
- **Quote, do not paraphrase**, anything said about tasks, inputs, outputs, rules or escalation.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Every slot is filled and the design is still vague | Answers accepted without their test | Re-ask, naming what is missing |
| The hardest slots got one-line answers | Questions batched | One question per message |
| Every answer is "professional" or "accurate" | Open questions, no alternatives | Offer real options specific to this agent |
| Picks always match your recommendation | Options were filler around it | Make each option a real, defensible design |
| A constraint resurfaces after the build | It was paraphrased away | Keep Source quotes verbatim |

## Key terms

**Design interview**: filling an agent brief by asking its stakeholders, one slot at a time.

**Escape hatch**: the option to answer in their own words instead of picking one offered.

**Recommended option**: the default you would choose, marked so a hesitant person can accept it.

**Source quotes**: the stakeholders' own words, kept verbatim in the brief.
