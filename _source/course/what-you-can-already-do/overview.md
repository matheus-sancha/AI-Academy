## How to use this page

Nothing here is taught again, and nothing here is new. The questions below check the Intermediate ideas
that the rest of this level builds on in code. Answer each one in your head before you open it.

If an answer surprises you, reread the Intermediate topic it names before you start
{{module:developer-tooling}}. This level moves the same decisions out of Copilot Studio's panels and into
files, schemas and pipelines, so it assumes you already know why each decision matters. No Advanced lesson
stops to explain it again. If your answers match, go straight on. Every assumed topic is listed at the end
of the page, each linked to where Intermediate teaches it.

## Self-check

<details>
<summary>1. An agent reads supplier material certificates as they arrive and files the values. It worked well in the test pane, with you watching. What has to exist before nobody is watching?</summary>

Everything the person in the test pane was doing for free. That means a trigger narrow enough to fire
only on certificates, and a named place for failures to go. It needs an alert when nothing has been
processed, because an agent that silently stopped looks exactly like one with nothing to do. It needs a
cost cap. And it needs an approval before anything irreversible, placed at the last point where reversing
is still cheap. The model's reasoning is the same either way. What changes is who is there to catch it.
This level builds the loop, the stop conditions and the approvals itself, so it assumes you already
design for the missing person. Reread {{topic:autonomous}} and {{topic:hitl}}.
</details>

<details>
<summary>2. A planner asks for "a connector to the SAP status code list". There are five work order codes and three operation codes. Where does that requirement go?</summary>

In the instructions. Ask the triage questions in order. Does it read live data or write to another
system? Is it a fixed process? Is it content to answer from? Is it a procedure or a template? Eight
codes are none of those, and they fit in four lines, which is less than one tool's description. A tool
would be paid for on every turn, by every unrelated question. Pro-code adds more places to put
things: MCP servers, skills in a repository, prompts in templates. The question stays the same, and so
does the answer. Reread {{topic:triage}}.
</details>

<details>
<summary>3. The agent's instructions say "9 in 10 revision answers should match Teamcenter". A user asks how reliable it is, and the agent quotes that line. What went wrong?</summary>

A success criterion was put where the agent reads it. The agent sees one answer at a time, never ten, so
it cannot act on an aggregate target. The line costs context on every turn and changes nothing. Criteria
belong in the brief, where they become test-case acceptance criteria, the human review rubric and the
pass mark. When a criterion hides a rule, such as *name the revision, its status and its ECN*, split it:
the rule goes to the instructions, and the criterion stays with the evaluation. This level automates
that evaluation, and an automated grader is only as sharp as the criterion it was given.
Reread {{topic:successcriteria}}.
</details>

<details>
<summary>4. Two tools return work order data. On one day the agent answers "how long are these taking?" with efficiency, and on the next with lead time. Nothing changed. Why?</summary>

The two descriptions are near-twins. The orchestrator never sees what a tool does, only what its name and
description say, and when two descriptions overlap the pick between them is unpredictable. The fix is in
the text. Name each tool's measure, define it, and write the boundary into **both** descriptions, naming
the neighbour. Then re-run the whole routing set, because changing two descriptions can move a third tool.
In this level you write MCP tool schemas yourself, so every description is yours, and so is every
near-twin. Reread {{topic:tooldesc}}.
</details>

<details>
<summary>5. Snowflake has good role-based access. Why does the Production Assistant read it as `TECHNIK_AGENT_RO` instead of as each user?</summary>

Because the agent must not be able to write, whoever is asking. A connection runs either as the end user or
as one fixed identity. End-user authentication is more faithful to who is asking, but it is less safe when
the agent reads untrusted text. A quality notification that talks the agent into an update would carry
the asking engineer's write access. A read-only identity is the one guarantee that survives a prompt
injection. SharePoint knowledge is the opposite case, because there the per-user slice is real. This
level's agent identity and MCP authorisation lessons ask the same question with stronger answers.
Reread {{topic:connauth}}.
</details>

<details>
<summary>6. A skill's script imports `requests` without an error and then fails on its first call. The same script runs on your laptop. What is different?</summary>

The sandbox. A bundled script runs with **no network access** and **cannot install packages** at
runtime. A library can be present and still be useless for the one thing it is for. Before you write a
script at all, check whether the harness already does the job, since it creates Word, Excel, PowerPoint
and PDF files natively. A script earns its place when the answer must be computed exactly, and it should
work offline with what is already installed. Authoring skills here starts from those constraints, not
from the file layout. Reread {{topic:sandbox}}.
</details>

<details>
<summary>7. Your evaluation set passes everything, including an answer you know cites the wrong revision. The expected response was right. How did the case pass?</summary>

On the GitHub Copilot harness, a model grades the answer, and its General quality method **does not
compare responses to expected answers**. It judges relevance and completeness, so a vague question lets
almost any relevant answer pass. The test prompt and its acceptance criteria are the whole lever.
Expected responses describe what a correct answer must contain, for the person who audits a failure, not
for the grader. This level builds graders of its own. That only helps if you already know what a grader
cannot see. Reread {{topic:judge}} and {{topic:testsets}}.
</details>

<details>
<summary>8. A tool reads `SAP_WO_OPERATIONS` directly, and it reports welding at Plant 1 at about 111%. The SQL is correct. Where should the fix go?</summary>

Into a view, not the tool. The raw table keeps superseded partial confirmations, so a correct query over
it still counts some operations twice. A view fixes the grain, removes known flaws, puts business words on codes and
columns, and exposes only what the agent should see. Every tool and knowledge source that reads it
inherits all of that, and the agent's role is granted the view, not the tables. The capstone's MCP server
in this level is built over exactly such a surface. Reread {{topic:sfviews}}.
</details>

If you didn't need to reread anything, start with {{module:developer-tooling}}.
