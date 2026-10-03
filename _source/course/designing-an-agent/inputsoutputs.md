## TL;DR

For each **input**, write down three things: what format it arrives in, where it comes from, and **whether it
always arrives**. That last question is the whole of your edge-case testing. For each **output**, write down
its format, who reads it, and a **real example**, not a description of one. Inputs that sometimes do not arrive
are where agents quietly invent things, and an output with no named reader has no standard to be judged
against.

## Why it matters

An agent rarely fails on the input you designed for. It fails on the one that is missing, half-filled, out of
date, or visible to one user and not another, and in those cases it does not stop. A model asked for a work
order status with no work order still produces something status-shaped. Nothing errors, and the user has no
way to tell.

Outputs fail more quietly still. *"A clear summary"* cannot be wrong, because nothing says what clear means or
to whom. Name the reader and the standard appears: a supervisor's summary that needs a code table to read is
wrong, whatever it contains.

## How it works

### Inputs: three questions each

| Question | Rejected | Accepted |
|---|---|---|
| **Format** | "the work order" | "a nine-digit SAP work order number, typed in the question" |
| **Source** | "from SAP" | "`SAP_WORK_ORDERS` in Snowflake, through a tool" |
| **Always or sometimes** | (not asked) | "always for this task; users sometimes give a serial number instead" |

The third column is where the testing is. Every *sometimes* is an edge case with a decision attached: what
does the agent do when this input is not there? Microsoft's guidance for instructions names the failure,
*overeager tool use*, where the model calls a tool without the inputs it needs, and gives the remedy: only
call the tool if the necessary inputs are available, otherwise ask the user. Its deterministic-workflow
pattern goes further: if any input is missing, stop and ask **one** question listing what is missing. The
brief is where you find out which inputs need that line.

### Knowledge is an input, and it is per user

Content the agent answers from is an input too, and it has a property that is easy to miss. Copilot Studio's
SharePoint, Dataverse and connector knowledge sources authenticate as the user asking, so the agent only
surfaces content that **that user** can access. The same question, from two people, arrives with different
inputs.

That turns *"always or sometimes"* into a question about people as well as data. Microsoft's evaluation
checklist asks of every response, among other things, *does it respect sharing permissions?* A brief that
records which knowledge is per user is what makes that question testable.

### Outputs: three answers each

| Answer | Why |
|---|---|
| **Format** | A Teams message, a table, a document in a template. Decides what the agent produces and how it is checked |
| **Reader** | The person who acts on it. Decides tone, length and what counts as appropriate |
| **A real example** | The standard. A description of an example still has to be interpreted; an example does not |

Microsoft's **output contract** pattern for instructions is the runtime form of this slot: goal, format,
detail level, tone, what to include and what to exclude. Every line of the contract is easier to write once
the reader and a real example are in the brief, and impossible to write well before.

## In practice at Technik

The Production Assistant's inputs, as the brief records them:

| Input | Format | Source | Arrives |
|---|---|---|---|
| Work order number | Nine digits, e.g. `100004521` | Typed by the user | Usually. Users sometimes give a serial number (`XT-V2-1042`) or a project (`PRJ-2031`) instead |
| Work order and operation data | Rows | `SAP_WORK_ORDERS`, `SAP_WO_OPERATIONS` in Snowflake, through a tool as `TECHNIK_AGENT_RO` | Always, but **replicated nightly**: today's confirmations are not there yet |
| Controlled documents and standards | Documents | SharePoint knowledge sources | **Per user.** A document the asking user cannot open does not arrive |
| The ECN behind a revision | `ECN700XXXXX` | Named by the user; checked in `TC_ECNS` | Sometimes. The ECN may not be released yet |

Each *sometimes* became a decision, and each decision became a test case:

- **A serial number instead of a work order**: list the open work orders for that unit and ask which one.
- **Today's confirmations**: say the data is as of last night's replication when the user asks about today.
- **A document the user cannot open**: say nothing covers it in the sources they can see, never answer from
  memory ({{topic:citations}}).
- **An unreleased ECN**: do not draft. Say the ECN must be released first, because a revision with no released
  change behind it is exactly what the release approval rejects.

The second row surprised the planners. The input always arrives, and it is still wrong by up to a day. Nobody
had asked *when* the data was true, only *whether* it existed.

The outputs, with a real example for the first:

| Output | Format | Reader |
|---|---|---|
| Work order status | A Teams message: one plain sentence, then the details | Planner or supervisor |
| Open QN list | A table: QN number, defect type, priority | Quality engineer |
| Revision draft | A document in the `GWI70000027` template, change history included | The document owner |

```text
Work order 100004521 (part P7000001042, unit XT-V2-1042, Plant 1) is released
and in progress at Welding.

Operation 0040 Welding · work centre W-12 · status INPROC
Status code REL: released, not yet confirmed. Data as of last night's SAP replication.
```

That example settled three arguments the description had not: the plain sentence first, for supervisors;
codes kept but explained; and the replication note, which planners had asked for after seeing the second row
of the inputs table.

## Design guidance

- **Ask "does it always arrive?" for every input**, and write the answer down.
- **Turn each *sometimes* into a decision**: ask, list, abstain or refuse. Then into a test case.
- **Record which knowledge is per user**, so permission cases get tested.
- **Ask when the data is true**, not only whether it exists.
- **Name the reader of every output**, and judge the output against that reader.
- **Put a real example in the brief.** It becomes the output contract and the expected response.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A plausible answer to a question with a missing input | No decision recorded for the missing case | Add the *ask, don't guess* line; test the missing case |
| One user gets an answer and another gets nothing | Knowledge is per user; the brief treated it as fixed | Record it as per user; test as a user without access |
| "The agent is wrong about today" | Replicated data treated as live | Record the data's age; say it in the answer |
| Output disputed after release with nothing to judge it against | No named reader, no example | Name the reader; get a real example into the brief |
| The format drifts between answers | Format described in words, never shown | Use the example as the output contract |

## Key terms

**Input**: anything a task needs, with its format, its source and whether it always arrives.

**Edge case**: an input that sometimes does not arrive, arrives late or arrives in another form.

**Per-user knowledge**: a knowledge source that returns only what the asking user can access.

**Output contract**: the runtime statement of an output's goal, format, detail, tone and contents.

**Reader**: the person who acts on an output, and so the standard it is judged against.
