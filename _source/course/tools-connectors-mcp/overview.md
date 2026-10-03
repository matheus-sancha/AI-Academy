## What this module is for

Up to here your agent could only talk. It answers from its instructions and from whatever documents
you gave it. Ask it the status of work order `100004521` and it has nothing — the answer lives in a
database it cannot reach.

Tools are how an agent stops talking and starts doing. This module covers the four ways to give an
agent reach — connector actions, MCP servers, other agents, and, as a last resort, driving a screen
— and the one thing they all have in common: **the orchestrator chooses a tool by reading its name
and description.** Which means the most important engineering in this module is writing.

## Before you start

Conceptually you want {{module:copilot-studio-basics}} and {{module:knowledge-and-rag}} first,
because this module assumes you know what an agent, an instruction and a knowledge source are.

Every example stands on its own, so nothing here depends on having read them. Allow about 90
minutes.

## What you will be able to do

By the end of this module you should be able to:

- explain what an agent can and cannot reach, and why a tool is the only bridge;
- choose between a connector action, an agent flow, an MCP server and a connected agent for a given
  job, and defend the choice;
- write a tool name, description and input descriptions that the orchestrator picks correctly — and
  diagnose the case where it does not;
- explain who a connection authenticates as, why that decides what users can see, and why agents in
  this course use a read-only role;
- add a Snowflake query as a tool and test that it is called with the right values;
- add an existing MCP server to an agent and say what you checked before enabling it;
- recognise the point at which one agent should become several.

## The thread through this module

The Technik Production Assistant gains its first real reach. Here is a question it currently cannot
answer:

> *"Which CNC program revision should machining use for `P7000001042`?"*

The answer is in Teamcenter data replicated to Snowflake. The lessons follow the agent as it
queries that data through a connector tool, returns the released revision rather than whichever row
came first, and — the part that makes it genuinely useful — warns that shop paperwork may still show
a superseded one.

The claim-by-claim audit in {{topic:hallucination#auditing-an-answer-claim-by-claim}}
showed a model with the right material in front of it still picking the wrong entry. This module
builds the tool that makes the equivalent mistake with revisions hard to make: choosing the released
revision becomes the database's job, not the model's.

## Self-check

<details>
<summary>1. An agent has a tool called <code>Run query</code>, described as "Runs a query against the database". It is never called when it should be, and sometimes called when it should not. Why?</summary>

Because the orchestrator has nothing to go on. It chooses tools by matching the user's request
against tool names and descriptions, and this description says nothing about *which* database,
*what* is in it, or *when* asking it would help. A description like "Look up the current released
revision of a part, drawing, document or CNC program in Teamcenter. Use when the user asks which
revision to use, or about revision history" gives the orchestrator something to match on. The name
and description are not documentation — they are the routing logic.
</details>

<details>
<summary>2. Your agent works perfectly. You share it with a colleague and they get an error, or worse, no data. What is the most likely cause?</summary>

The connection. A connector action runs under a connection that authenticates as somebody — you,
a service account, or the end user. If it runs as you, a colleague may be blocked by your credentials not
being shared, or may silently see *your* data rather than their own. If it runs as the end user, each
person needs their own connection and their own permissions in the source system. This is the single most
common way an agent that worked in testing fails when it meets a second person, and it is why
connection references exist ({{module:publishing-and-environments}}).
</details>

<details>
<summary>3. Why does the Technik Production Assistant connect to Snowflake with <code>TECHNIK_AGENT_RO</code> rather than the role of the person asking?</summary>

Because a read-only role cannot be talked into writing. Everything an agent reads is potentially
attacker-controlled — a quality notification description is free text typed by anyone on the shop
floor — and instructions hidden in that text can reach the tools the agent holds. If the only role
the agent has cannot update or drop anything, the worst case is bounded by the platform rather than
by a sentence in a prompt. {{module:safety-and-moderation}} and {{module:security-advanced}} return to
this; it is why agents never borrow a person's role.
</details>

<details>
<summary>4. When should a job be an agent flow rather than a connector action called directly?</summary>

When it must happen the same way every time. A connector action is a single call that the
orchestrator decides to make; a flow is a defined sequence with conditions, error handling and,
where needed, an approval. "Look up a revision" is an action. "Read a work order's current
operation, read its open QNs, and apply the blocked rule" is a flow, and the agent calls the flow as
one tool. {{module:automation-and-workflows}} builds exactly that.
</details>

<details>
<summary>5. Your agent has 14 tools and has started calling the wrong one. What are your options?</summary>

In order of effort: sharpen the names and descriptions so the boundaries between tools are
unambiguous; remove or merge tools that overlap; and, if the agent genuinely has several distinct
jobs, split it — child agents inside the agent, or connected agents that run on their own, each
holding only the tools its job needs. The orchestrator's choice gets harder as the list grows,
in the same way a menu gets harder to read. {{module:advanced-tools-and-multi-agent}} in Advanced
splits the Technik assistant
into a production agent and an engineering agent for this reason.
</details>
