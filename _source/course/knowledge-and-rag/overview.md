## What this module is for

{{module:copilot-studio-basics}} built the Technik Production Assistant and wrote a grounding rule into it
on day one: answer only from your sources, cite them, say when they have nothing. Until now there were no
sources to ground in. This module gives the assistant Technik's documents and teaches what happens when it
answers from them.

That change, from *plausible* to *grounded and citable*, is the largest single jump in usefulness anywhere
in this level. It is also where agents most often go wrong quietly. Knowledge that returns nothing, an
answer built from the wrong source, a citation to the right document and the wrong clause: none of these
produces an error. Each produces a confident answer. The fact the module is built around is that
**attaching a knowledge source is not the same as being grounded in it.**

## Before you start

You want {{topic:hallucination}}, because RAG is the fix for the failure it describes, and
{{topic:genai}}, which explains why on the GitHub Copilot harness grounding is an instruction you test
rather than a switch. {{topic:xml}} matters too, because the grounding rule lives in its
`<knowledge_routing>` section. {{topic:visibility}} is the user's side of the permissions story told here.

Nothing here needs a tenant to read. Snowflake as knowledge is a preview feature on the standard harness,
and its lesson tells you what to check before you rely on it. Allow about 75 minutes.

## What you will be able to do

By the end of this module you should be able to:

- explain what retrieval-augmented generation does to a request, and what it does not fix;
- choose between uploaded files, SharePoint, public websites, Dataverse and connectors for a body of
  content, and say what each one costs in permissions and freshness;
- tell a Copilot connector from a Power Platform connector used as knowledge, and pick between them;
- say when Snowflake belongs in an agent as knowledge, and when as a tool over a view;
- write instructions that make an agent cite, abstain and prefer the governing source;
- diagnose knowledge that returns nothing, in the order the causes usually occur;
- say what Work IQ and Foundry IQ are for.

## The thread through this module

One question runs through it: *what is the minimum overlay thickness on an XT valve body bore?*

{{topic:rag}} shows the answer assembled from three places: the requirement in `SWI70000318`, the reasoning
in `DGL70000009`, and a summary on the Technik standards site that says the work instruction governs. It
also shows why that summary becomes a hazard once revision C of `SWI70000318` is released.
{{topic:sources}} puts the documents where they belong, in two SharePoint sources with per-user
permissions and proper titles, and explains why nothing is uploaded as a file.

{{topic:connectorknowledge}} and {{topic:snowflakeknowledge}} explain why work order data stays out of the
assistant's knowledge: live knowledge would run as each user's own Snowflake identity, and a generated
efficiency query reports 111% where the truth is 89%. {{topic:citations}} writes the `<knowledge_routing>`
section and tests it with the Inconel question the documents do not cover. {{topic:workiq}} looks ahead
to knowledge shared across agents.

## Self-check

<details>
<summary>1. Why not paste Technik's controlled documents into the agent's instructions and skip knowledge altogether?</summary>

Size first. The controlled document set would run far beyond any instruction budget, and every question
would pay for all of it, relevant or not ({{topic:contextcost}}).

Quality second, and this is the interesting reason. Irrelevant context does not sit there harmlessly; it
competes. A question about hydrostatic testing gets a *worse* answer with the cladding instruction in the
window too, because there is more plausible material to blend. Retrieval exists to put the few passages
that matter into the context instead of everything. Instructions also cannot cite, and a revised document
would mean editing the instructions ({{topic:rag}}).
</details>

<details>
<summary>2. The assistant answers SharePoint questions perfectly for you and returns nothing for a colleague. Is it broken?</summary>

Almost certainly not. SharePoint knowledge is queried as the person asking, and when they lack Read access
it behaves "silently as if the document doesn't exist". Check that the colleague can open the file
directly. If they cannot, the source is working as designed, which is exactly what you want for controlled
documents.

If they can open it, work down the other causes: an encrypted sensitivity label (the file can show
**Ready** and still return nothing), the file size limit, or a question that does not reach the top three
search results ({{topic:sources}}, {{topic:citations}}).
</details>

<details>
<summary>3. A colleague proposes adding Snowflake's work order tables to the assistant as knowledge "so it can answer anything about work orders". What do you need to know first?</summary>

Which harness and which users. Snowflake as knowledge is a preview feature documented for the standard
harness, and it is not in the GitHub Copilot harness's knowledge list. It runs every query as the asking
user's own Snowflake identity, so users without a Snowflake login get nothing, and those with broad roles
reach whatever their role can read. That replaces `TECHNIK_AGENT_RO` with nobody's identity.

Then the questions. Named ones, such as status or efficiency, belong in tools over views, where the
deduplication is enforced. A generated query over `SAP_WO_OPERATIONS` double-counts confirmations and
reports welding efficiency at about 111% instead of 89% ({{topic:snowflakeknowledge}}).
</details>

<details>
<summary>4. An answer cites the right document but quotes the wrong acceptance criterion. What are the possible causes, and how do you tell them apart?</summary>

Three. **Retrieval** brought back a neighbouring passage of the right document. Check what the Knowledge
step retrieved in the activity trace. **The model paraphrased** a passage it retrieved correctly, which is
an instruction problem: tell it to quote criteria exactly. Or **the source itself is stale**: the standards
page summarises `SWI70000318`, and after a revision the summary can be wrong while still being perfectly
retrievable.

The trace separates the first from the other two. Only reading the source separates the second from the
third. Source precedence in `<knowledge_routing>` is what stops the third ({{topic:citations}}).
</details>

<details>
<summary>5. Your agent has never once said "I could not find that." Why should that worry you?</summary>

Because abstention has to be asked for, and then tested. A model with no relevant passage in its context
will produce a plausible answer rather than stop ({{topic:hallucination}}). On the GitHub Copilot harness
no switch withholds that answer; only the instructions do.

An agent that always answers is not well grounded. It is untested: nobody has yet asked it something its
sources do not cover. Ask the Inconel manifold-header question, expect the abstention, and keep that case
in the evaluation set for good ({{topic:testsets}}).
</details>
