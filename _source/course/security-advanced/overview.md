## What this module is for

Earlier modules each took a slice of the attack surface: {{topic:ctxsecurity}} looked at what enters
the context window, {{topic:mcpsec}} at what writing a server adds, and {{topic:agentid}} at whose
authority an agent holds. This module steps back. It threat-models the whole agent, then looks at
the four instruments Microsoft offers around it: a content classifier service, moderation
settings, data governance in Purview, and data policy for connectors. It ends with the one
instrument that goes looking for trouble, red teaming.

The idea that runs through all six lessons is **decide with a capability, report with a
classifier.** A role, a schema, a data policy or an approval decides: the action cannot happen, whatever
the model says. A classifier, an audit log or a scan reports: it tells you something probably
happened, after the model has already read it. Microsoft's own guidance says it does not "rely on our
ability to block all prompt injections", and the module keeps meeting the same shape. Each control is
good at a narrow question. The attacks that matter, such as a true row with a false claim about it,
sit between the questions.

Expect gaps in the documentation, and expect them to point the same way. The pages describe what
each feature does and are quiet about how two of them combine: how two data policies combine, whether
Purview reaches a warehouse row, what a default guardrail blocks, whether a toolbox version can be
pinned. The lessons mark each of those as *Not yet verified* rather than guessing, and the capstone,
which has never run live, cannot settle them.

## Before you start

From Intermediate, {{topic:injection}} is the five-layer defence this module assumes and extends,
{{topic:moderation}} is the vocabulary set and the levels that {{topic:modtuning}} tunes, {{topic:dlp}}
is how to read a data policy, and {{topic:agentauth}} and {{topic:connauth}} are the identity half of
the same question.

From this level, {{topic:ctxsecurity}} and {{topic:mcpsec}} are the two security lessons whose
conclusions this module takes as given. {{topic:agentid}} and {{topic:mcpcs}} supply the identity and
connector facts that {{topic:purview}} and {{topic:dlpdesign}} build on. {{topic:tracing}} explains
the traces whose contents these lessons keep returning to, and {{topic:evalstrategy}} is where an attack
becomes a test case.

Nothing here needs to be run. {{topic:redteam}} shows a scan and needs a Foundry project to execute, and
the capstone, which is public and tested offline only ({{module:capstone-build}}), has no scan.

Allow about two hours. {{topic:redteam}} is optional on a first pass.

## What you will be able to do

By the end of this module you should be able to:

- threat-model an agent by listing what it reads, what it does and where its output goes, and answer
  for each of OWASP's ten risks whether it can happen and what stops it;
- take apart excessive agency into functionality, permissions and autonomy, and shrink each;
- choose a Content Safety instrument by the question it answers, and say where it sits, whether it
  blocks and what it cannot see;
- tune moderation per surface, keep a decision record, and test both what must pass and what must
  still be blocked;
- map each data path of an agent to the control that governs it, and say what Purview records and
  what it does not;
- design a data policy that handles custom connectors, MCP servers and a change to published agents,
  and know the path it does not govern;
- run a red-team scan, read its attack success rate, and say what it does not test.

## The thread through this module

{{topic:threats}} comes first because everything else is a response to something on its list. It
gives the method, applies it to the capstone, and finds the rows that only a grader or a person can
stop. {{topic:contentsafety}} is the classifier half of the response: what each instrument asks,
where it sits, and which of Technik's attacks none of them can see. {{topic:modtuning}} is the
tuning half, because a classifier has thresholds and a threshold is a decision somebody should record.

{{topic:purview}} and {{topic:dlpdesign}} turn from the model to the data. Purview governs what the
organisation can see and prove afterwards, by label and policy and audit record. A data policy
governs which connectors an agent may combine, for every agent in a tenant, without anyone reading
them. Both depend on the data being somewhere they can see, and the capstone's agent reads a
warehouse and calls a server on Container Apps, which is partly out of reach of both.
{{topic:redteam}} closes by testing the whole thing. The pipeline that carries these controls into
production is {{module:alm-and-governance}}.

## Self-check

<details>
<summary>1. A colleague says Prompt Shields is switched on, so QN `300001267` cannot get the assistant to report an open notification as closed. What is wrong with that?</summary>

Three things. User prompt attack detection is on by default, but document attack detection, which is the
indirect kind, is off by default and has to be enabled. The tool response intervention point, where a
record arrives, is preview and for agents only. And Prompt Shields is a probabilistic classifier: it has
a "Manipulated Content" subtype, and Microsoft says a no-attack result "doesn't establish that the
request is benign" ({{topic:contentsafety}}).

Add the part no instrument covers. The row is real, so a false claim about it is grounded. Harm
categories and protected material do not look for it, and a read-only role does not help, because
hiding a row is a lie and not a write. A graded case in the harness is what catches it
({{topic:threats}}).
</details>

<details>
<summary>2. OWASP names three root causes of excessive agency. Which does the capstone's read-only role address, and which does it leave?</summary>

The role addresses **permissions**: the service user holds one read-only role, so no tool call can
write. The three narrow tools address **functionality**, since the agent can look up a document, an
operation's documents and a revision, and nothing else. **Autonomy** is not tested because there is
nothing irreversible to approve.

What the role does not bound is what the agent *says*, and what it spends. A false answer backed by a
real row has no control but a grader, and the repository states no token or rate limit beyond a
cap of six tool calls per loop ({{topic:threats}}).
</details>

<details>
<summary>3. You lower the moderation level on the incident-note prompt so that ordinary incident text stops being refused. What do you run before shipping, and why can't the capstone's CI show it?</summary>

Both sets: the legitimate incident notes that must now pass, and the harmful requests and injection
probes that must still be blocked, with the results written into the decision record. Lowering a
threshold for one set without re-running the other is the usual way a change loosens more than you
meant. Copilot Studio does not document whether the level changes attack detection, so the probes
matter ({{topic:modtuning}}).

The capstone's CI replays a scripted model against a fake Snowflake, so nothing in it can trip a filter.
A moderation test needs a live model and belongs in the live job
({{topic:evalharness}}).
</details>

<details>
<summary>4. A user without access asks the Production Assistant about the Confidential customer specification for `PRJ-2031`. What stops the answer, and does the same control govern a row in `TC_DOCUMENTS`?</summary>

Access does. AI apps "use existing controls to ensure that data stored in your tenant is never
returned" to a user without access, and a label adds markings and, for encrypted content, the
EXTRACT usage right. That governs the SharePoint half, which runs as the asking user.

The Snowflake half runs as `TECHNIK_AGENT_SVC`, and what governs it is the role and the views. The
pages read describe labels on files and Dataverse content, and none describes one on a warehouse row.
So write down, per data path, which control governs it ({{topic:purview}}).
</details>

<details>
<summary>5. The Teamcenter server works in VS Code, but a maker finds Publish unavailable once Copilot Studio calls it. What do you check, and which control governs the capstone's own route?</summary>

The data policy. The server reaches Copilot Studio through a connector, and "blocking Power Platform
connectors also blocks access to tools in connected MCP servers". Check its group against the other
connectors in the agent, since connectors in different groups cannot share data, and check whether
the policy blocks it outright. Download the violation details from the Channels page, and
remember that a new custom connector falls under the default Ignore rule unless the list ends in a
deny ({{topic:dlpdesign}}).

On the capstone's own route, a Foundry agent calling the server through a toolbox, no page read says a
data policy applies. What governs it is the Entra app role the server requires, `Teamcenter.Read`.
One server has two governors, and a review has to find both.
</details>
