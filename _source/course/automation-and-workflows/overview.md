## What this module is for

An agent is good at judgement and unreliable at repetition. Ask it to run two queries and apply a rule, and
most of the time it will. Sometimes it runs one query and reports the half-answer with full confidence. This
module covers everything around an agent that has to run the same way every time: scheduled jobs, processes the
agent hands off, single AI steps inside a process, and the points where a named person has to decide.

There are three automation designers and the Production Assistant uses one of them, so the module keeps
returning to the harness. The assistant is on the GitHub Copilot harness, where a process tool is a
**workflow**. Agent flows are the standard harness's equivalent. Cloud flows sit outside Copilot Studio
altogether. Several lessons also carry costs that change with the calendar: seeded AI Builder credits end on
1 November 2026.

## Before you start

{{topic:triage}} is the lesson that sends requirements here. It places a fixed multi-step process among the
agent's tools, and this module builds that tool. {{topic:hitl}} decides where a person belongs, and
{{topic:approvals}} is the mechanism. {{topic:chooseharness}} explains why the assistant is on the GitHub
Copilot harness, which decides the designer, and {{topic:licensing}} is the background for every cost here.

This is a reference module, so read the lesson you need. If you are deciding where a piece of logic belongs,
start with {{topic:topicsvsflows}}, the last lesson, and follow its links back. Read straight through, it takes
about three hours.

## What you will be able to do

By the end of this module you should be able to:

- say what each designer is for, cloud flow, agent flow and workflow, and which harness each belongs to;
- make a flow callable by an agent, and keep it inside the 100-second limit;
- confine judgement to one agent node in a workflow, with a structured output the rest can branch on;
- say which currency an AI step is paid in, and cost a document workload by the page;
- write a prompt with JSON output, and recognise the deprecated action it replaces;
- design a document flow with separate confidence, validation and review stages;
- build an approval that goes to named people, in the right order, with a tested rejection path;
- decide whether a requirement is a topic, a flow or the agent's, and draw the handovers between them.

## The thread through this module

Each lesson has its own piece of Technik's operation, and the last lesson places all of them.

{{topic:cloudflows}} reminds the owners of `SOP70000114`, `SWI70000318` and `TDS70000044` that they are past
their review date. That runs on a schedule with nobody in a conversation. {{topic:agentflows}} fixes a status
answer the orchestrator kept getting half right. It wraps two queries and the *blocked* rule into one
standard-harness tool, so work order `100004521` is reported as held by QN `300001234`. {{topic:workflows}}
rebuilds that idea for the assistant's own harness. Its example is a morning QN list in which one agent node,
with no tools, judges whether each priority fits `SOP70000101`.

{{topic:aibuilder}} costs a supplier-certificate model before anyone builds it: 600 pages a month at 8 Copilot
Credits a page. {{topic:prompts}} writes the prompt that summarises what revision C of `SWI70000318` changes,
returning a boolean the flow can branch on. {{topic:docproc}} builds the certificate flow and finds that
confidence and validation catch different failures, which is why every certificate still reaches an inspector.
{{topic:approvals}} routes revision C, which the owner submits, to a process engineer and then the quality lead.

{{topic:topicsvsflows}} puts all six side by side and assigns each one to a topic, a flow or the agent. The
revision of `SWI70000318` needs all three.

## Self-check

<details>
<summary>1. The Production Assistant needs a process that runs two queries and applies a rule. A colleague offers an agent flow they already built. Why can the assistant not use it, and what do you build?</summary>

Agent flows belong to the standard harness. The assistant is on the GitHub Copilot harness, whose tools are
connectors, MCP servers and workflows, so the agent flow never appears in its tool list. Build the process as a
workflow with the **When an agent calls the flow** trigger and **Respond to the agent**, published, answering
within 100 seconds. It has to be rebuilt by hand: a Power Automate cloud flow cannot be converted into a
workflow either ({{topic:workflows}}, {{topic:agentflows}}).
</details>

<details>
<summary>2. A flow uses a prompt's text answer and checks whether it contains the word "acceptance". It misses a revision whose summary says "inspection limits". What is the fix?</summary>

Return JSON instead of text, with a field such as `acceptance_criteria_changed`, and test that field. A keyword
search depends on the model's wording, which varies from run to run. Edit the example so the format becomes
**custom**, then save: the format is locked at save time and cannot drift while you tune the instructions. Build
the flow on **Run a prompt**, not the deprecated **Create text with GPT** ({{topic:prompts}}).
</details>

<details>
<summary>3. Every field on a supplier certificate came back with confidence above 0.9. Why does it still go to an inspector?</summary>

Confidence measures how sure the model is that it *read* a value, not whether the value is right or acceptable.
A confident misread that lands above the minimum strength passes the confidence check and the validation check
alike. Validation catches values that break a rule or disagree with `TDS70000044`. Review catches what both let
through. For material going into pressure-containing equipment, everything is reviewed, and the flags tell the
inspector where to look first ({{topic:docproc}}).
</details>

<details>
<summary>4. The assistant has drafted revision C of SWI70000318. Who starts the approval, and why is it sequential?</summary>

The document owner does, by submitting the draft. The agent's task ends at a draft ready for submission, and the
person accountable for the revision is the one who says it is ready. The approval is sequential because the
quality lead's review of inspection limits is only worth having once the process engineer has confirmed the
method. Both approvers are named people from a list, never a shared mailbox, and the release in Teamcenter stays
with the owner ({{topic:approvals}}, {{topic:triage}}).
</details>

<details>
<summary>5. A Power Automate flow with an AI Builder step has run for a year. What should its owner check before 1 November 2026?</summary>

Which currency it pays in. Seeded AI Builder credits are removed on that date. A cloud flow draws on AI Builder
credits first and Copilot Credits after, so a flow living on seeded credits needs add-on credits or Copilot
Credits in place first, or its AI steps fail with `QuotaExceeded`. If the flow moves into Copilot Studio, it
pays in Copilot Credits only, and its AI steps are charged even in tests ({{topic:aibuilder}}).
</details>
