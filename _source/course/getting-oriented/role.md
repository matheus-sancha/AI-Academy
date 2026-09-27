## TL;DR

An AI engineer builds on top of pre-trained models and platforms instead of training models. The job
is to combine models, prompts, data, tools and automation into something that keeps working for
people you are not watching — and then to measure and govern it. Most of the artifact is not code.
It is prose: instructions, descriptions, test cases and a written record of what the thing is for.

## Why it matters

Everything in {{module:what-you-already-know}} was about your own use of Copilot. You asked, you read
the answer, and you judged it. If it was wrong you noticed, because you knew the material.

From here on, someone else asks. They do not know the material — that is why they asked — and you are
not in the room. The question stops being *did I get a good answer* and becomes *will this give a
sound answer to a colleague, tomorrow, about data that has changed since I tested it*. Everything
that makes this level harder than Basic follows from that one shift, including the parts that look
like paperwork.

It also means the mistakes become yours. A model that invents a revision number is a curiosity when
you catch it and a defect when your colleague acts on it.

## How it works

The work divides into six recurring activities. They are not phases — you will revisit all of them —
but every one of them is somebody's job on a finished agent, and on a small team it is yours.

| Activity | What it produces | Where this level covers it |
|---|---|---|
| **Deciding what to build** | A brief: users, tasks, inputs, outputs, rules, refusals, escalation | {{module:designing-an-agent}} |
| **Specifying behaviour** | Instructions the model reads on every turn | {{module:writing-instructions}} |
| **Grounding** | Knowledge sources the answers come from | {{module:knowledge-and-rag}} |
| **Giving reach** | Tools that read and write other systems | {{module:tools-connectors-mcp}} |
| **Proving it** | An evaluation set that can fail, and its results over time | {{module:testing-and-evaluation}} |
| **Shipping and operating** | A published agent, in a solution, with analytics | {{module:publishing-and-environments}} |

The surprise for most engineers is the second row. The main artifact you author is **natural
language**, and it is load-bearing: the orchestrator decides which knowledge to search and which tool
to call by reading descriptions you wrote ({{topic:orchestration}}). A badly worded description is not
untidy documentation. It is a routing bug.

### What this is not

Three adjacent roles get confused with this one, and the distinction is about where the work sits
rather than seniority.

A **data scientist or ML engineer** creates and trains models. You almost certainly will not: the
problems in this level are solved with instructions and grounding, and {{topic:training}} exists to
give you the vocabulary and then tell you that you do not need it.

A **solution architect** works a level above. Microsoft's own description of that role — the audience
profile for the AB-100 exam — is about architecture strategy, ROI analysis, multi-agent solution
design and a cohesive application-lifecycle-management strategy across a portfolio. Useful to
recognise, because those are the questions that arrive once your agent works and someone asks for
five more.

A **maker** builds low-code solutions for their own team, usually in one environment, usually without
an evaluation set. That is a legitimate and valuable way to work — {{topic:agentbuilder}} is exactly
that surface — and the difference is not skill. It is that you are expected to produce evidence.

## In practice at Technik

The Technik Production Assistant answers questions across seven capability areas. A Copilot user can
already ask about a work instruction and get a decent answer. Here is what the engineer decides that
no model decides for them:

| Decision | Made by the engineer | Not made by |
|---|---|---|
| Work-order status comes from a query over SAP data, not from the model's memory | A tool over `SAP_WORK_ORDERS` | The model, which would answer plausibly and wrongly |
| Engineering questions come from the documents, not a table | A knowledge source | The model, which cannot tell the difference |
| "Which revision?" is answered by the database's released flag | A view, where the rule is enforced | A sentence in the instructions, where it is a suggestion |
| The agent reads Snowflake as a read-only role | `TECHNIK_AGENT_RO` | Convenience, which would reuse yours |
| It refuses to state an acceptance criterion it cannot cite | A must-never rule with its reason attached | Politeness |

Every one of those is a specification decision, and each is cheap now and expensive after the agent
is in Teams. The third is the one that separates this level from Basic: the same question can be
answered by the model, by a prompt, or by the data model, and only the last one is still right in six
months.

## Design guidance

- **Write the specification before the agent.** Not because process is virtuous, but because the
  evaluation set and the instructions are both derived from it ({{topic:brief}}).
- **Reach for instructions and knowledge before tools, and tools before code.** The triage is
  learnable and it has a right answer most of the time ({{topic:triage}}).
- **Treat prose as engineering.** Budget real time for descriptions and instructions. They are the
  parts the runtime actually reads.
- **Measure before you improve.** Without a fixed set of cases, "better" is a feeling
  ({{topic:whyeval}}).
- **Treat every product claim as a claim to check.** Including the ones in this course
  ({{topic:tenantvaries}}).
- **Assume you will hand it over.** The record of *why* is the part nobody can reconstruct.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| You built something nobody asked for | No brief; requirements gathered as a conversation | Fill a brief before configuring anything ({{topic:brief}}) |
| It works for you and fails for the first colleague | The connection authenticates as you | Decide who it runs as, deliberately ({{topic:connauth}}) |
| You cannot tell whether your change helped | No fixed evaluation set, so every judgement is anecdotal | Build one that can fail ({{topic:testsets}}) |
| You wrote code for something the platform does natively | Assumed an agent is software first | Check the harness first ({{topic:createdfiles}}) |
| A documented feature is missing in your environment | Tenant variation, not error | Check licence, policy and toggles ({{topic:tenantvaries}}) |
| The agent is confidently wrong about your own data | Nothing grounded the claim; the model filled the gap | Ground it, and require it to say when it cannot ({{topic:citations}}) |

## Key terms

**AI engineer** — builds solutions on pre-trained models and platforms; combines models, prompts,
data, tools and automation, then measures and governs the result.

**Pre-trained model** — a model someone else trained, which you configure rather than build
({{topic:training}}).

**Grounding** — making an answer come from named content rather than the model's parameters
({{topic:rag}}).

**Maker** — someone building low-code solutions for their own team, typically without an evaluation
set.

**Brief** — the written design record of what an agent is for. Not the Instructions field
({{topic:brief}}).

**Evaluation set** — a fixed list of cases run after every change, so improvement is measurable
({{topic:testsets}}).
