## What this module is for

Intermediate taught you to attach knowledge to an agent and to read a citation. This module is for the day that is not
enough. An answer is wrong and the trace shows the right document was never retrieved. A draft revision shows up in an
answer to someone who cannot open it. A number from a semantic layer disagrees with the one in the report. A bill grows
with how hard the question was. Each of those is a retrieval problem before it is a model problem, and each has a
mechanism behind it.

It is a reference module, not a read-through. Come here with a symptom and read the lesson that explains it. Nine
lessons cover the ground: four on the Azure side, two on the Snowflake side, and three that cut across both, which
choose between retrieval kinds, check an answer against what came back, and measure all of it.

The capstone is not the running example, because it has no search index and no Cortex service. Its three tools are
lookups by key. So the examples come from the engineering agent that {{module:advanced-tools-and-multi-agent}} splits
out, answering from the scenario's controlled documents. The capstone's code was tested offline only
({{module:capstone-build}}), and nothing in this module was run at all. Each lesson says so in a visible *Not yet
verified* block where it matters.

## Before you start

You need {{topic:rag}}, {{topic:sources}} and {{topic:citations}}, which this module takes further, and
{{topic:snowflakeknowledge}}, the Microsoft-side route to Snowflake data that {{topic:cortexanalyst}} is set against.
{{topic:embeddings}} explains the vector that {{topic:vector}} stores, and {{topic:jit}} treats retrieval as a budget
decision that {{topic:agentic}} gives a mechanism. For the checks at the end you need {{topic:foundryevals}},
{{topic:llmjudge}}, {{topic:contentsafety}} and {{topic:ctxsecurity}}. {{module:snowflake-sql}} supplies the views the
Snowflake lessons keep returning to.

Allow about three hours to read it end to end, though you are not meant to.

## What you will be able to do

By the end of this module you should be able to:

- say what an index must hold beside its vectors to enforce a rule such as *released revisions only*;
- choose a chunking approach from a document's structure, and say what the Azure page does not give you;
- explain what hybrid search and the semantic ranker each add, and where the ranker stops;
- say what agentic retrieval costs, which part of it is preview, and whose identity a knowledge base should run as;
- state what a Cortex Search service exposes, and to whom;
- explain why a semantic view needs checking against a number you know, and what Cortex Analyst needs `SELECT` on;
- sort a question into aggregate, passage or key, and say where the route is decided;
- name the three meanings of *grounded* and the layer that checks each;
- build a labelled question set that separates retrieval from the answer, and read the metrics in pairs.

## The thread through this module

From the document to the answer, and then to the proof.

{{topic:vector}} is the index: which fields hold text, vectors and the metadata a filter needs. {{topic:chunking}} is
what goes into it, and its page gives no chunk size. {{topic:hybrid}} is how it is queried and ranked.
{{topic:agentic}} is the managed pipeline on top, with a planning step that is still preview. {{topic:cortexsearch}} is
the same shape inside Snowflake, with the source query as its access boundary, and {{topic:cortexanalyst}} answers
questions about rows through a semantic view.

{{topic:routing}} chooses between those tools. {{topic:grounded}} checks the answer against what came back, in layers.
{{topic:rageval}} measures retrieval and the answer apart, so that a bad result points at one of them.

Two ideas run through all nine. The first is that **a rule which must hold has to live where the retrieval reads it**,
and not in the prompt: a `status` filter in the index, the source query of a search service, the definition in a
semantic view, the identity a knowledge base runs as, the route chosen in code, the guard around the answer. Each moves
the rule from a request the model may ignore to a condition the data enforces.

The second is a habit, **measure before you tune**. The pages are thin where a designer most wants a number: no chunk
size, nothing on how well a planner routes, nothing on whether every source kind enforces permissions alike. Where that
happens the lesson says so in an `unknown` block, and {{topic:rageval}} gives the method that replaces the missing
figure: a labelled set, the split between retrieval and answer, and the metrics read as pairs.

Three dated facts will have moved by the time you read this, so check them first. LLM query planning in agentic
retrieval is preview. Snowflake now recommends Cortex Agents over calling Cortex Analyst directly. And Content Safety's
groundedness detection retires on 30 April 2027.

## Self-check

<details>
<summary>1. A production planner asks what revision C of <code>SWI70000318</code> changes, and the agent answers with the tightened porosity limit. Revision C is a draft in a site production cannot open. Where do you look?</summary>

At three places, because each is a different failure with a different fix. Start with the index. Was a draft chunk
indexed, and is `status` a filter field applied to every query? An index built from the Controlled Documents library
holds only released PDFs, so a draft in it means the pipeline read the wrong site ({{topic:vector}}). Next is
identity. If the answer came through a knowledge base, did it run as a shared service identity and not as the caller?
The Foundry IQ page says it can run under the caller's identity, and does not say which source kinds enforce which
mechanism ({{topic:agentic}}). Last is a Cortex Search service, which searches with its owner's rights, so whatever its
source query selects, any role with `USAGE` can retrieve ({{topic:cortexsearch}}).

Test with a user who lacks access, and put that case in the evaluation set so it stays fixed ({{topic:rageval}}).
Tightening the prompt is the one fix none of the three needs.
</details>

<details>
<summary>2. After the documents were re-chunked, some answers got better and some got worse. How do you tell what the change did, and what would have told you before it?</summary>

A labelled question set built before the change. Run the same questions through each variant, change one setting per
run, and record the settings beside the scores, which is the parameter sweep the Foundry page describes. Document
Retrieval then separates the halves: if the labelled documents rank no differently and the answers do, the change moved
generation, and the completeness and utilization pair says how. If the ranking moved, the chunks did.

Nothing in the documentation could have answered it in advance. The Azure chunking page gives no size, and the only
figure in this module's sources is Cortex Search's 512 tokens, for that service alone. So the choice is empirical, and the
page calls it semipermanent. That is the reason to measure it first ({{topic:chunking}}, {{topic:rageval}}).
</details>

<details>
<summary>3. A planner asks Cortex Analyst for welding efficiency at Plant 1 in September and gets 110.9%. The report says 88.9%. Is the model wrong?</summary>

Probably not. The arithmetic belongs to the semantic view. 110.9% is what the raw operations table gives, because
operations confirmed twice are counted twice, with 26 rows for 20 operations. 88.9% is what the view gives once the
stale postings are dropped. Snowflake's pages describe a semantic view as sitting over physical tables and say nothing
about carrying a rule from a database view, and the capstone's agent role is deliberately denied the raw table. Whether
a logical table can be defined over the cleaned view is unknown.

So fix it at the definition, and test the result against the number you already know. Granting `SELECT` on the raw table
would make Analyst run and bring the flaw back as a confident answer. Keep the verified queries as a regression set,
because the model underneath is assigned by Snowflake and can change ({{topic:cortexanalyst}}).
</details>

<details>
<summary>4. One question asks which operation is holding work order <code>100004521</code> and what the work instruction says about the porosity. The agent returns the porosity limit and never mentions the order. What went wrong?</summary>

The route. The question holds a keyed lookup, the order's status and the released revision of the work instruction, and a
passage, the limit in revision B's section 5. The planner sent the whole thing to document search, which can answer
only the second half and does so fluently. Neither platform's page measures how well its planner routes, so you
measure it ({{topic:routing}}).

Change three things. Describe each tool by the questions it answers and the ones it does not. Route anything keyed on an
identifier in code, where a wrong route is silent. And give every evaluation case an expected route, scored apart from
the answer. Then test with a role that lacks one grant, because a Cortex Agent can carry on with the tools the role can
reach.
</details>

<details>
<summary>5. The Groundedness evaluator passes an answer that quotes the Standards summary's limit, and once revision C is released the summary is out of date. Is the evaluator broken, and what does the capstone's guard add?</summary>

The evaluator is working. Groundedness measures whether an answer agrees with the context it was given, and the summary
agreed with it. Truth is a third thing that nothing here checks, so the fix is upstream: retire or update the summary,
and add a correctness case. The Content Safety page's own best practice is to keep grounding sources current
({{topic:grounded}}).

The capstone's guard adds less than it sounds. It checks only that a tool result exists in the run, so it passes any
answer a tool backed, including `rev-03`'s wrong one. The capstone has no agreement layer: its live judges are intent
resolution, task adherence and tool call accuracy. And the Content Safety detection API retires on 30 April 2027, so
build the agreement check on an evaluator or a judge you have calibrated against a person ({{topic:llmjudge}}).
</details>
