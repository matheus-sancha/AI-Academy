## What this module is for

{{module:automation-and-workflows}} gave you the pieces: a cloud flow, an agent flow, a workflow, a prompt, a document model, an
approval. This module is for the point where a process built from them has to run unattended, every time, on files nobody
chose. A certificate arrives in a layout the model never saw. A flow fails at 02:00 and nobody is told. An approval waits
longer than a run can. Each of those is a design decision, and each has a source behind it that is thinner than you would like.

It is a reference module, not a read-through. Come here with a symptom. Seven lessons cover it: which steps of a process
get a model, how a workflow is shaped around agent nodes, what makes a flow usable as an agent's tool, which settings a
production prompt must choose, what a document pipeline's limits are, how a failure is handled, and what to do when a wait
outlives a run.

Technik's supplier material certificate is the running example. Nothing in this module was run. Its sources are two curated
pages per lesson, several of them short overviews or community articles, so every lesson marks what the pages do not say in
a visible *Not yet verified* block.

## Before you start

You need {{module:automation-and-workflows}}, and in particular {{topic:topicsvsflows}}, which places a requirement among a
topic, a flow and the agent, and {{topic:workflows}} and {{topic:agentflows}}, which teach the two designers this module
builds on. {{topic:prompts}} and {{topic:docproc}} are the foundations of the prompt and document lessons, {{topic:approvals}}
is the mechanism that the last lesson stretches, and {{topic:cloudflows}} introduces the catch scope that the error lesson
extends. {{topic:hitl}} and {{topic:injection}} explain why a person sits where they do and why an agent that reads a
supplier's file holds no tools.

Allow about three hours to read it end to end, though you are not meant to.

## What you will be able to do

By the end of this module you should be able to:

- audit a process step by step and say which steps are code, which belong to a model and who sees the result before it acts;
- keep a workflow's rules as data beside its agent nodes, and say why renaming a node breaks them;
- design a flow's contract for an agent: typed inputs, a short output, a description that routes and a failure that answers;
- choose a prompt's model, temperature and moderation level, and say what none of them guarantees;
- say which limits shape a document pipeline, and which of its stages the documentation does not cover;
- tell a thrown failure from a returned one, and give each a handler;
- say what a run's 30-day limit does to an approval, and split the wait from the process.

## The thread through this module

One pipeline, seen seven ways.

{{topic:detvsagentic}} takes the intake of supplier certificates and decides step by step what is code and what is a model.
{{topic:wfagentnodes}} builds that intake as a workflow, with the rules held as data and an agent node for the two steps
that need one. {{topic:flowtools}} designs the small tool that tells an inspector a heat's status, and what it must say
when it fails. {{topic:promptsadv}} sets the model, temperature and moderation of the prompts inside it, and
{{topic:docpipelines}} lists what the document model can and cannot read: a supplier with too few samples, a table that
breaks across a page. {{topic:errors}} gives every failure a home, and {{topic:longrunning}} lets an approval wait for a
quality lead who is away for six weeks.

Two ideas run through all seven. The first is that **a rule which must hold lives in code, in data or with a person, and
never in a model's judgement**: the validator, the rules array, the check after an AI step, the inspector who accepts.
The second is that **anything that outlives a call leaves a record**: a register row for a failed read, an outcome field on a
tool's answer, an approval id on a list item. A run that holds the state dies with the run.

Four dated facts will have moved by the time you read this, so check them first. The model list for prompts and its rate
tiers change. The workflows overview names its harness differently from the rest of the course. Anthropic's page on agents
dates from December 2024 and says its tooling description has since changed. And the 90-day rule that can turn off an idle
flow bears on the waiting flow in {{topic:longrunning}}.

## Self-check

<details>
<summary>1. A colleague wants the whole certificate intake built as an agent, "because it is smarter". Which steps stay code, and what do you check in the workflow once it is built?</summary>

The ones whose rule you can write down. Converting ksi to MPa, comparing yield with the 485 MPa minimum, checking the
tensile strength is above yield, checking the certificate number and writing the register row are all fixed. Reading the
fields and drafting a query to a supplier are the model's steps, and an inspector accepts. Ask of each step what a
different answer on the second run would cost and who sees it before it acts ({{topic:detvsagentic}}).

In the workflow, keep the rules as an array a person can read, not in an agent's instructions. A later expression reads an
agent's output through the node's generated name, so renaming a node breaks every rule that reads it. Give the agents no
tools, because the PDF is a supplier's file ({{topic:wfagentnodes}}).
</details>

<details>
<summary>2. The assistant calls <em>Get certificate status</em>, the register read fails, and it tells the inspector the heat is accepted. What is missing, and what does the documentation not tell you?</summary>

A path that answers. A flow has no exception to raise, and the one channel the pages document is the outputs of
**Respond to the agent**. Every path, the failing ones included, should end there with an outcome field and a message that
says what to do next and what not to claim. Type the heat number as text, and keep the flow read-only so a repeated call is
harmless ({{topic:flowtools}}).

What the pages do not say is what the agent receives when a flow fails or times out, or whether the response action can run
from a catch scope. That design is a position. In the flow itself the failure is a thrown one, handled by a retry and a
catch that also writes a record ({{topic:errors}}).
</details>

<details>
<summary>3. The prompt that reads a certificate's yield strength returns 497 on one run and 469 on a rerun of the same PDF, with the temperature at 0. Why, and what do you change?</summary>

Zero means more predictable, and the page does not promise determinism: responses can vary at the same temperature. Models are
also updated periodically, the default is upgraded, and nothing pins a version, so the answer can change with no edit to the
prompt ({{topic:promptsadv}}).

Change the checks around it, not the slider. Validate the value in code against the purchase specification, and keep a
regression set of the ten sample certificates, run again after any model change you did not make. Choose the model on
purpose, and treat the experimental external models as unfit for a production flow.
</details>

<details>
<summary>4. A new supplier's certificates come back with empty fields, and an old supplier's table is missing a strength row. Where do you look?</summary>

At the extraction limits. An AI Builder custom model learns a layout from a collection of at least five samples, and ten
samples can fill two collections at most, so a third supplier's layout has none. The pipeline needs a *layout not trained
yet* state that routes to manual entry. A table whose rows break across a page, or a field split by a page boundary, is
documented as unsupported, and the pages do not say what comes back, so validation has to check completeness as well as
plausibility ({{topic:docpipelines}}).

Classifying, validating, reviewing and writing are not covered by either page. They are stages you design, and the write is
keyed so a rerun cannot add a duplicate row.
</details>

<details>
<summary>5. The quality lead is away for six weeks, and revision C of <code>SWI70000318</code> sits at Submitted with nothing to say why. What happened, and how do you redesign it?</summary>

The run timed out. A run lasts at most 30 days, including a run that is only waiting for an approval, and after 30 days the
pending steps time out. The status does not change, because the process lived in the run.

Split it. One flow creates the approval, writes its id to the list item and ends. A second starts when the approval
completes and finds the item by that id. Reminders and escalation are a scheduled sweeper over the persisted record, with
thresholds Technik chooses, and a restart is safe if it marks the old id superseded and the second flow ignores a stale one.
Neither page documents those parts, nor what a timed-out approval record looks like ({{topic:longrunning}}).
</details>
