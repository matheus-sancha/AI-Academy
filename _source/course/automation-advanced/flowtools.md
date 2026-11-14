## TL;DR

A flow that an agent calls is an API with a model on the other side. {{topic:agentflows}} taught what makes a flow callable: the **When an agent calls the flow** trigger, a **Respond to the agent** action, asynchronous response off, published, and an answer inside **100 seconds**. This lesson is about what makes it **usable**: typed inputs that reject a bad value in words, a short output the agent can act on, a description that says what the tool is for and not for, and a failure that comes back as an answer. Microsoft's two pages document the requirements and the 100-second limit. They say nothing about types, error responses or identity, so most of the contract below is design, marked as such.

## Why it matters

An agent calls a tool without seeing inside it. The flow's inputs, outputs and description are everything it knows, and its only way to learn about a failure is what the flow sends back. A flow built for a person to run is full of assumptions that a model will break: it expects a number where an identifier has a leading zero, it fails on an empty field, it returns forty rows where the agent needed one status.

The failure mode is quiet. A flow that errors in the middle returns nothing useful, and nothing in the flow stops the agent answering from memory. The capstone's error messages exist for the same reason ({{topic:buildmcp}}).

## How it works

### What the pages document

<!-- volatile verified=2026-11 -->
A flow can be added as a tool when it has the trigger **When an agent calls the flow** and a **Respond to the agent** action. *Asynchronous response* must be **Off**, under *Networking* in the response action's settings. The flow must be published, and it must respond within the 100-second action limit. Microsoft's guidance is to tune the logic, the queries and the amount of data returned so that a typical run is under it. You add the flow at agent level, through the agent's Tools page, where the orchestrator may call it whenever its description fits. Or you add it to one topic as an action node, where it runs only at that point. A flow that is missing from the list lacks the trigger or the response action. The configuration panel lets you update the description "to help your agent understand the flow's purpose". Both pages carry the standard-harness note.
<!-- /volatile -->

That is the whole documented contract. The overview page, the first of this lesson's links, only says the orchestrator can call the flow at runtime to retrieve data or act for the user.

### The contract you design

A flow tool has four parts, and the pages give you rules for none of them but the last.

| Part | Design rule |
|---|---|
| **Inputs** | Few, named for the question the agent is asking, each with a description, and **typed as text** wherever the value is an identifier |
| **Outputs** | Fields, not rows: a status the agent can quote, never a table it must read |
| **Description** | What it returns, what it needs and what it does not do, so routing has something to match ({{topic:tooldesc}}) |
| **Time** | Under 100 seconds on a typical run, with the data returned trimmed to fit |

The most useful rule is the one about failure. A flow has no exception to raise. Its documented channel to the agent is the **Respond to the agent** outputs. So every path through the flow, the failing ones included, should end in that action with an outcome field the agent can branch on and a message written for the agent to act on.

The capstone's MCP server does the same job with an exception. Its tests ran offline only, and nothing here was run against a flow.

*From [`server/teamcenter.py`, lines 85–87](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/server/teamcenter.py#L85-L87):*

```python
    if not revisions:
        raise ToolError(f"No document {doc_no} in Teamcenter. Check the number with the user. "
                        "Do not describe a document you could not find.")
```

The error states what is wrong and what to do next, and forbids the tempting wrong answer. A flow's `Message` output is the same sentence, delivered as data.

<!-- unknown since=2026-11 -->
Everything about errors is undocumented here. The pages do not say what the agent receives when a flow fails or times out, whether **Respond to the agent** can run from a catch scope after a failure, what types an input or output may have, how many there can be, whose credentials the flow's connections use when an agent calls it, or how to test a flow as a tool. The design above is a position that follows from the one channel the pages do name.
<!-- /unknown -->

## In practice at Technik

An inspector asks the assistant whether heat `0417731` is accepted. A flow, *Get certificate status*, reads the *Certificate register* ({{topic:docproc}}).

| | Contract |
|---|---|
| **Input** | `HeatNo`, text. A heat number can start with a zero, and a number input would drop it |
| **Output** | `Outcome` (`found`, `not_registered`, `invalid_input`, `error`), `Status`, `Message` |
| **Description** | "Returns the register status of one supplier heat of material: Needs review, Ready for sign-off or Accepted. It does not accept, reject or change a certificate." |

The first step checks the input. An empty or malformed `HeatNo` ends the flow at once with `invalid_input` and the message *Ask the user for the heat number printed on the certificate.* An unknown heat returns `not_registered`, with *No certificate is registered for this heat. Do not report a status.* The same rule as the server's: say what to do and what not to claim.

The last scope catches anything else and responds with `error` and a message such as *The register could not be read. Tell the user the status is unavailable.* Without it, a failed SharePoint read gives the agent silence.

Two more choices follow {{topic:agentflows}}. The flow returns three fields, so the agent's context stays small. And it only reads. A tool the model may call twice, or that a retry may call again, should be safe to repeat. A flow that wrote a row on every call would write it twice, so a status check stays a status check, and a write goes behind a person ({{topic:hitl}}).

A flow that needs more than 100 seconds is the wrong shape for a tool. Split it into one that starts the work and records it, and one that reports its state, and keep the state in a store that outlives the run ({{topic:longrunning}}).

## Design guidance

- **Design the inputs and outputs first**, from the question the agent asks.
- **Type identifiers as text**, and validate them in the first step.
- **Return fields, not rows**, and always include an outcome the agent can branch on.
- **Make every path respond.** A failure is an answer with an outcome and an instruction.
- **Write the description for routing**: what it returns, what it needs, what it will not do.
- **Keep a tool safe to call twice.** Put writes behind a person.
- **Stay well under 100 seconds**, and turn long work into start-and-check tools.
- **Test the failure paths on purpose**: an empty input, an unknown value and a broken connection.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The flow is not in the agent's tool list | The trigger or the response action is missing, or it is unpublished | Add both, then publish |
| The agent times out | The run exceeds 100 seconds, or asynchronous response is on | Trim the work and the output; turn it off |
| The agent invents a status when the flow breaks | Nothing came back, and the flow never responded | Catch the failure and respond with `error` |
| A heat number loses its leading zero | The input is a number | Type it as text |
| The agent calls the flow for the wrong question | The description is vague | Say what it returns and what it does not do |
| A record is written twice | The tool writes, and the call was repeated | Make it read-only, or require a person |

## Key terms

**Contract**: the named inputs, the outputs and the description that together tell an agent how to use a flow.

**Outcome field**: an output whose value says what kind of answer this is, so the agent can branch on it.

**Respond to the agent**: the action that returns a flow's outputs, and the one channel the pages document for them.

**Idempotent tool**: a tool that is safe to call again with the same input.
