## What this module is for

Every earlier module taught a piece. This one is the whole thing, built by you: an MCP server over Technik's
Teamcenter data in Snowflake, an agent that answers from it and refuses what it cannot, an evaluation that gates both,
and a deployment with an identity of its own and a trace to read. It is the Production Assistant from Intermediate,
rebuilt as code. There is no route elsewhere to follow, so each page is written in full: what you need, what to do,
what you should be holding when the stage ends, and what to check if yours looks different.

The capstone's code lives in its own public repository,
[`technik-capstone`](https://github.com/matheus-sancha/technik-capstone), and every page quotes it at the tag
`v1.0.0` with a line range. Read the tag, not `main`, because the tag is frozen and the line numbers hold. The code
is Python throughout. The commands are PowerShell, and nothing needs a Windows machine except that spelling.

**The code has been tested offline only.** Its tests fake Snowflake and the model. Its processes really start: the
server answers a client over stdio, the agent loop runs against a scripted model, and the evaluation workflow runs
green in CI on the fakes. No one has run it against a live Snowflake or Azure account. Your run is its first live one.
When a page says something no one has checked, it says so, and {{topic:buildsetup}} collects them.

## Before you start

The pages assume the lessons they build on rather than repeat them. From this level, {{topic:buildmcp}} and
{{topic:mcpvscode}} are the server and its editor loop, {{topic:maf}} is the agent framework,
{{topic:evalharness}} and {{topic:mafeval}} are the evaluation, and {{topic:foundryagents}},
{{topic:agentid}} and {{topic:cicd}} are the deployment. From Intermediate, {{topic:sfviews}} and {{topic:sfroles}}
explain why the agent reads views through one read-only role.

You also need accounts: Snowflake, with an admin who can use two roles, and an Azure subscription with a Foundry
project. Stage 5 needs more tools than the first four, and {{topic:buildsetup}} says which. Allow several sittings.
Each stage ends on a line you can check, so stop at any of them.

## What you will be able to do

By the end of this module you should be able to:

- seed a Snowflake account and prove an agent's identity reads what it should and nothing more;
- start a project that runs and does nothing, with pins, ignore rules, instructions and an eval set in the first commit;
- design narrow MCP tools from a list of questions, with errors a model can act on, and test them over stdio;
- build an agent whose most important rule is enforced in code, and test it through the real loop with a scripted model;
- grade an agent offline, keep a case that fails on purpose, and block a change only on a regression;
- deploy a server and a hosted agent that authenticate to each other as identities, and read the trace of one answer.

## The thread through this module

| Stage | You are holding | It is finished when |
|---|---|---|
| {{topic:buildsetup}} | A seeded account, a key file and an admin-only `.env` | `setup/check.py` ends on *Ready for stage 1.* |
| {{topic:stagescaffold}} | A repository with pins, ignore rules, instructions and eight cases | `uv run main.py` exits cleanly and calls no model |
| {{topic:stagemcp}} | A server with three tools, and tests over stdio | Agent mode in VS Code answers the two-call question with both revisions |
| {{topic:stageagent}} | An agent with a guard | It answers the capstone's questions and refuses the rest |
| {{topic:stageevals}} | A report against a baseline | `rev-03` is red, the run is green, and a regression exits 1 |
| {{topic:stageship}} | A hosted agent behind an authenticated server | A colleague can open it, and you can read a trace of what it did |

The order is the dependency chain. The setup page comes first because a missing grant does not announce itself where
you meet it. Stage 1 gives every later stage something to diff against. Stage 2 comes before the agent so that the
tools can be right before anything depends on them. Stage 4 comes before shipping so that the evaluation is the gate
and not an afterthought, and stage 5 is last because it is the one that costs money and needs the other four.

Two rules carry through. **What must always hold is code**, which is the guard of stage 3 and the role of stage 5. And
**a gate blocks on regression**, so a known failure can sit in the set without stopping work.

## Self-check

<details>
<summary>1. The setup check passes every read and fails one line: `can read TC_DRAWINGS`. The agent works fine. Why is it still a failure?</summary>

The role was meant to read views and two tables, not the tables behind the views. The views carry rules, such as the
repair of superseded confirmations, and an identity that can bypass them can compute different figures from the same
rows. The ceiling is the security boundary, so the check tests it as hard as the floor. Fix the grant, not the check
({{topic:buildsetup}}).
</details>

<details>
<summary>2. In agent mode, `list_operation_documents` returns drawing `DU700001042` at revision B, and the answer calls it the drawing to use. Which call is missing?</summary>

`get_revision_status`. The first tool returns the revision the operation was released against, and revision C is the
released one. The docstring says to check, and the eval case `op-01` expects both calls. An answer from one tool alone
is wrong, which is why you ask this question in the editor before any agent exists ({{topic:stagemcp}}).
</details>

<details>
<summary>3. A lookup for a document that does not exist ends with *there is no document SWI70000381*, not with the refusal. Why does the guard let it through?</summary>

The guard replaces an answer only if the run holds no tool result. The server's error comes back to the loop as a tool
result, so the run is grounded, and the model can say what was wrong because the loop passes the error's text through.
Without that setting it would see a generic failure ({{topic:stageagent}}).
</details>

<details>
<summary>4. The eval workflow is green, and `rev-03` is red in the report. Is something wrong?</summary>

No. The baseline records `rev-03` as a known failure, and only a case that passed there and fails now is a
regression. The case exists to show that a grader can catch a tool-backed wrong answer, which the guard cannot. It
turning green would be the thing to investigate. The offline run also tests the harness and not the model, so a green
run is not evidence about live behaviour ({{topic:stageevals}}).
</details>

<details>
<summary>5. After deployment the server answers locally but every tool call from the hosted agent fails. What do you check first?</summary>

Whether the agent's identity holds the server's `Teamcenter.Read` role. The server refuses a token for an identity
without it, and Foundry creates the identity only when it deploys the agent, so the assignment is a manual step
after `azd up`. A 401 to a browser is the server working as designed ({{topic:stageship}}).
</details>
