## What this module is for

There is no Microsoft product in this module. Everything before it taught what an agent can be made of; this
module is about deciding what a particular agent is **for**, before any of it is built. Most agents that
disappoint were built well and decided badly: nobody wrote down who it serves, what counts as finished, what it
must never do and who it hands over to.

The work produces one document, the **brief**: thirteen slots, each with an acceptance test that a concrete
answer passes and a plausible one fails. The brief is a design record read by people. It is never the agent's
instructions, and the module's recurring point is that the brief and the instructions are different documents
with different readers. Then the brief is triaged into parts: instructions, knowledge, tools and skills.

## Before you start

You want {{topic:contextcost}} first, because the triage is mostly an argument about what each part costs on
every turn. {{topic:skillsvs}} supplies the earns-a-skill test that `triage` reuses, and {{topic:xml}} shows the
instruction sections the brief's slots turn into. {{topic:hitl}} is where escalation and approvals were placed,
and `rules` builds on it.

Nothing here needs a tenant. Every lesson works on paper, and the brief you end with is the input to
{{module:testing-and-evaluation}} and to the interview in {{module:the-six-skills}}. Allow about 90 minutes.

## What you will be able to do

By the end of this module you should be able to:

- explain what an agent brief is, who reads it, and why it is not the Instructions field;
- name users by role and expertise, and ask for the artifacts that settle the outputs and rules slots;
- write a task as a verb phrase with a trigger and a finished state, and derive a test case from it;
- record for every input whether it always arrives, and turn each *sometimes* into a decision;
- write a must-never rule with its reason, a plausible refusal, and an escalation with a named recipient;
- record out of scope, tone and delegation so later requests cannot quietly change them;
- place every requirement in exactly one of instructions, knowledge, tool or skill;
- tell a success criterion from an instruction, and send each to where it belongs;
- run a design interview one question at a time, with options, keeping the answers verbatim.

## The thread through this module

One brief, filled in for the Technik Production Assistant, slot by slot.

{{topic:brief}} writes its role and shows the brief pasted into the instructions going wrong. {{topic:users}}
names four user groups and gets `SOP70000101` out of the quality team. {{topic:tasks}} turns the scenario's
capability areas into tasks. {{topic:inputsoutputs}} finds that SAP data always arrives and is a day old.
{{topic:rules}} makes dispositioning a nonconformance the refusal and names escalation recipients from
`TC_DOCUMENTS.OWNER`. {{topic:scope}} rules out pay questions and writes to SAP, and chooses *plain, answer
first, never reassuring about a defect*. {{topic:triage}} turns the finished brief into a parts list, and
refuses three tools on the way. {{topic:successcriteria}} keeps *9 in 10* out of the instructions.
{{topic:interview}} shows how the answers were got, in the users' own words.

## Self-check

<details>
<summary>1. A stakeholder sends you a polished brief and asks you to paste it into the agent's Instructions field so "the agent knows everything". What do you say?</summary>

No, and the reason is the reader. The brief is written *about* the agent for people: the reviewer, the
instructions writer, the evaluation writer. Pasted in, sentences about the users read as directions, success
criteria arrive as text the agent may repeat to users, and every turn pays for a document written for a
reviewer.

Derive the instructions from the brief, section by section, and keep the brief as the record
({{topic:brief}}, {{topic:successcriteria}}).
</details>

<details>
<summary>2. The quality slot reads "Help engineers stay on top of quality notifications." Why does it fail, and what do you ask next?</summary>

It is a capability area, not a task: no precise verb, no object, no trigger and no finished state, so nothing
says what a finished answer looks like and no test can fail. Ask for an example of the last time they needed
it. The answer usually holds the trigger and the object, as *"the open ones on my project, so I know what's
blocking FAT"* did ({{topic:tasks}}, {{topic:interview}}).
</details>

<details>
<summary>3. A quality engineer asks the assistant whether four porosity indications on a unit are acceptable to ship. The QN, the inspection document and the acceptance criteria are all available to it. What should it do, and which slot decided that?</summary>

Refuse the verdict and deliver everything else: the QN, the acceptance criteria with their document and
revision, and the name of the assigned quality engineer. Under `SOP70000101` the disposition belongs to that
engineer. The rules slot decided it, as a **refusal**: a request inside the domain, made in good faith, that is
not the agent's to answer. It is not out of scope, which would mean the subject itself is off the map
({{topic:rules}}, {{topic:scope}}).
</details>

<details>
<summary>4. A planner asks for "a connector to the SAP status code list" so the assistant can explain codes. Where does that requirement go?</summary>

The instructions. There are five work order codes and three operation codes, and four lines of instructions
cost less than one tool's description, which would be paid on every turn whether or not anyone asks about a code.
Before adding any tool, ask whether a sentence would do it, or whether an existing tool could return the field
({{topic:triage}}, {{topic:contextcost}}).
</details>

<details>
<summary>5. You are interviewing a supervisor about tone and they answer "professional". What went wrong, and how do you recover?</summary>

The question was open, so they had nothing to compare against, and every alternative is professional. Ask again
as one numbered question with three genuinely different registers written for a question they actually ask,
one recommended, plus a way to answer in their own words. Then keep what they say verbatim: an aside like
*"I don't want it telling me it's probably fine"* is the line that becomes the tone's *never*
({{topic:interview}}, {{topic:scope}}).
</details>
