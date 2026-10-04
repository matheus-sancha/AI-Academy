## TL;DR

A prompt is a saved, reusable instruction to a model, with **input variables** that a flow fills at run
time. It returns **text** or **JSON**. JSON is the reason to use one in a process: each field arrives as its
own value, so the next step can branch on it or write it somewhere without parsing a sentence. In a flow the
action is **Run a prompt**. It replaces **Create text with GPT**, which is deprecated and no longer offered,
so an article or flow that still uses that name is out of date. Generated text is still a draft, and the
documented pattern puts a person between the prompt and anything that acts on it.

## Why it matters

Most AI steps in a process are a single call: summarise this, classify that, pull these values out. A prompt
is that call with the instruction written once, tested in a builder and reused by name. Nobody pastes
instructions into each flow, and nobody edits five copies when the wording changes.

The output format decides whether the step is any use. A flow cannot read *"The acceptance criteria appear to
have changed in section 5"*. It can test `acceptance_criteria_changed` for `true`. Text output pushes the
parsing onto whoever writes the next step, and the model is free to phrase things differently on every run.
JSON output fixes the shape when the prompt is saved, so the step behaves the same way on every run.

## How it works

### What a prompt is made of

| Part | Holds |
|---|---|
| **Instructions** | The task in natural language: what to do with the inputs and what to return |
| **Inputs** | Variables filled at run time: text, or an image or document such as a PDF |
| **Knowledge** | Data the prompt can be grounded in at run time, for context |
| **Output** | Text, or JSON in a format you control |

Prompts are built and tested in the **prompt builder** and can be shared. They run on Azure Foundry models,
need Copilot Credits and Dataverse in the environment, and are available in listed regions only. They may also
be throttled under load.

### Where a prompt runs

| Used in | How |
|---|---|
| A Power Automate cloud flow | The **Run a prompt** action, with its inputs filled from earlier steps |
| An agent flow, or a standard-harness agent | As an action in the flow, or added to the agent as a tool |
| A workflow | As an AI action node ({{topic:workflows}}) |

The prompt pages are written for the standard harness. On the GitHub Copilot harness an agent's tools are
connectors, MCP servers and workflows, so a prompt reaches the Production Assistant only inside a workflow.

### Text or JSON

Select **JSON** as the output and the builder proposes a format from what the model returned during testing.

| Format mode | Behaviour |
|---|---|
| **Auto detected** (default) | Refreshed from the response every time you test. Useful while the instructions are still changing |
| **Custom** | Set as soon as you edit the JSON example, and never changed by later tests |

Either way, **the format is locked when you save**, and every run uses that format whatever the inputs. You can
view the schema generated from your example but not edit it. One limitation shapes the example: every value
needs a key, so a list is written as objects (`[{"section": "5"}]`), never as bare values (`["5"]`). In the
flow, each field appears as its own dynamic content, ready for a condition or a column.

### The deprecation, and which way it runs

| Action | Status |
|---|---|
| **Create text with GPT** | Deprecated and no longer visible. Its prompt lived inside the action |
| **Create text with GPT using a prompt** | The old name of the next row, renamed in May 2025 |
| **Run a prompt** | Current. Calls a saved prompt from the prompt builder |

Migrating a flow is mechanical. Copy the old action's prompt text, create a custom prompt from it, replace the
action with **Run a prompt**, and repoint every later step that used its output. The new prompt needs at least
one input variable, so a prompt that had none gets a dummy input left empty.

### Keeping a person in it

Microsoft's guidance for generated content is that a person reviews it before it is posted, sent or used for a
decision. Its documented pattern is **Start and wait for an approval of text**. The reviewer gets the
generated text and can accept it, edit it or reject it, and the flow continues with the **accepted** text,
not the original ({{topic:approvals}}).

## In practice at Technik

When a document owner submits a draft revision for approval, the approvers need to know what changed before
they read forty pages. Technik's submission flow, a cloud flow covered in {{topic:approvals}}, gets that from
a prompt, *Summarise revision change*.

| Input | From |
|---|---|
| `Draft` (document) | The draft revision as a PDF, from the submission library |
| `ECN` (text) | Number, title and reason of the ECN, read from `TC_ECNS` |

The instructions say to compare the draft's revision history and changed sections against the ECN's reason, and
to return only what the document shows. The custom JSON example, saved with the prompt, reads:

```json
{ "doc_no": "SWI70000318", "to_rev": "C", "ecn": "ECN70000042",
  "summary": "Adds an ultrasonic check before cladding and tightens the porosity limit.",
  "sections_changed": [ { "section": "4 Preparation", "change": "New ultrasonic check" },
                        { "section": "5 Inspection", "change": "Porosity limit tightened" } ],
  "acceptance_criteria_changed": true }
```

Two fields do the work. `summary` goes into the approval request, **beside** the draft and never instead of it.
The approvers still read the document, and the summary only tells them where to look. The flow branches on
`acceptance_criteria_changed`, and when it is `true` the quality lead is added as an approver, because the
shop floor will inspect to different limits from release day.

The first version used text output and a condition that searched the summary for the word *acceptance*. It
missed a revision whose summary said *inspection limits*. The boolean has no wording to miss.

## Design guidance

- **Use JSON output whenever a later step reads the answer.** Use text only when a person reads it.
- **Switch to a custom format before you save**, so tuning the instructions cannot change the shape.
- **Ask for what the inputs show, nothing more**, and say so in the instructions.
- **Put generated text in front of a person** before it is sent, published or acted on.
- **Build on Run a prompt.** Treat any Create text with GPT action you find as migration work.
- **On the GitHub Copilot harness, put the prompt in a workflow.**

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A condition on the prompt's answer misses cases | Searching text output for a keyword | Return a field in JSON output and test the field |
| The output's shape changed after a prompt edit | Auto-detected format refreshed during testing | Edit the example to set a custom format, then save |
| *A JSON could not be generated* | The model wrapped the JSON in Markdown | Add *Don't include JSON markdown in your answer* to the instructions |
| A list will not save as the format | Values without keys | Write the list as objects with a key |
| An article's steps name an action you cannot find | Create text with GPT is deprecated | Use Run a prompt with a saved prompt |
| A migrated flow fails at a later step | Downstream steps still point at the old action's output | Repoint them to Run a prompt's outputs |
| Generated text went out with a mistake in it | No review step | Add *Start and wait for an approval of text* and send the accepted text |

## Key terms

**Prompt** — a saved, reusable model instruction with input variables, built in the prompt builder.

**Run a prompt** — the flow action that calls a saved prompt.

**JSON output** — a prompt response returned as named fields in a format locked when the prompt is saved.

**Custom format** — a JSON format set by editing the example, unchanged by later tests.

**Create text with GPT** — the deprecated flow action that Run a prompt replaces.
