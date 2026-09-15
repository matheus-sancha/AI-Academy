> **30 minutes, on paper.** No environment, no network. Everything you need is on this page, and
> every answer explains its reasoning.

The Technik Production Assistant has seven capability areas. They sound alike — they are all
"answer questions about manufacturing" — and they are built from four different mechanisms. Choosing
wrongly is not a bug you find later; it is an agent that is rigid where it should be flexible, or
unreliable where it should be exact.

This is the mapping exercise. Do it before B5, and the rest of the Beginner track is you checking
your own answers.

---

## Part 1 — The four mechanisms (5 minutes)

Fill this in from memory before reading on. One sentence each, plus the question that identifies it.

| Mechanism | What it is for | The question that says "this one" |
|---|---|---|
| Knowledge | | |
| Tool | | |
| Topic | | |
| Flow | | |

<details>
<summary>Answers</summary>

| Mechanism | What it is for | The question that says "this one" |
|---|---|---|
| **Knowledge** | Answering from content — documents, pages, records — by retrieving the relevant parts | *Is the answer written down somewhere, in prose or in rows?* |
| **Tool** | Performing one action: a query, an API call, an automation | *Is this one action, with a name I can give it?* |
| **Topic** | Running a conversation path exactly as drawn | *Must this exchange happen the same way every time?* |
| **Flow** | Running a business process identically, with conditions, error handling and approvals | *Must this process run identically, possibly with nobody watching?* |

The single question that separates most cases: **how much of this must be identical every time?**
All of it → flow. The path but not the words → topic. One named action → tool. None of it, it is
just content → knowledge.
</details>

---

## Part 2 — Map the seven capabilities (15 minutes)

For each capability, choose the mechanism (or mechanisms), and write one sentence of justification.
Be specific: "tool over a view" is a better answer than "tool".

| # | Capability | Example question | Your answer |
|---|---|---|---|
| 1 | Work order information | "What's the status of work order `100004521`? Which operation is it at?" | |
| 2 | Work order efficiency | "What's the efficiency of welding work orders at Plant 1 this month?" | |
| 3 | Work order lead time | "What's the average lead time for `P7000001042` work orders?" | |
| 4 | Quality notifications | "Show open QNs on cladding for `PRJ-2031`." and "Draft a write-up for this defect." | |
| 5 | Engineering questions | "Which document covers weld prep inspection, and what does it say about acceptance criteria?" | |
| 6 | Teamcenter revision information | "Which CNC program revision should machining use for `P7000001042`?" | |
| 7 | Document revision and creation | "Draft revision C of `SWI70000318` for `ECN70000042`, then route it for approval." | |

<details>
<summary>Answers and reasoning</summary>

| # | Capability | Mechanism | Why |
|---|---|---|---|
| 1 | Work order information | **Knowledge** over Snowflake, plus a **topic** for intake | The questions are open-ended — status, which operation, what is blocking — and you cannot enumerate them, so knowledge. But the work order *number* must be captured and format-checked every time, and that is a topic |
| 2 | Efficiency | **Tool over a view** | The definition of efficiency must not vary, and the data has duplicate confirmations that must be removed before hours are summed. A generated query gets this wrong plausibly. The rule belongs in SQL |
| 3 | Lead time | **Tool over a view** | Same reasoning. "Release to technical completion in calendar days" is a definition, and definitions belong where they are enforced |
| 4 | Quality notifications | **Tool** to find them, **skill** to draft a write-up | Two different things wearing one name. Finding is a named query. Drafting is a written procedure with judgement in it — which acceptance criterion, which priority — so a skill |
| 5 | Engineering questions | **Knowledge** | It is prose in documents. There is no path to draw and no action to take. Retrieval, with citations |
| 6 | Teamcenter revisions | **Tool over a view** | A named question someone acts on, where "released" must be enforced by the query rather than hoped for in a description |
| 7 | Document revision | **Skill** to draft, **flow** to route and release | The draft is judgement; the release changes what the shop floor works to and must run identically, with an approval. Splitting them is the whole design |

**The pattern.** Notice how often the answer splits a capability in two: find versus draft, draft
versus release, capture versus answer. That is the most useful habit this exercise teaches — a
"capability" as a business person describes it is usually two mechanisms with an approval between
them.

**Notice also that three of seven are "tool over a view".** Every one of those is a number somebody
reports upward. When a metric leaves the room it should come from a fixed query, never from one
invented at question time.
</details>

---

## Part 3 — The harness consequence (5 minutes)

You have just decided that capabilities 4 and 7 need **skills**, and capability 1 needs a **topic**.

1. Can one agent have both? Why?
2. What would you do about it?
3. Which way would you choose, and what would you write down?

<details>
<summary>Answers and reasoning</summary>

**1. No.** Topics are standard harness; skills are the GitHub Copilot harness; and the harness is
fixed when the agent is created. One agent cannot have both.

**2. Three options.**

- **Drop the topic** and build on the GitHub Copilot harness, accepting that work order intake is
  orchestrated rather than guaranteed — so the format check becomes an instruction the model usually
  follows.
- **Drop the skills** and build on the standard harness, rebuilding the write-up as a topic plus an
  AI Builder prompt — which works, and puts the procedure in a canvas where the quality engineer who
  owns `SOP70000101` cannot read it.
- **Use two agents.** Standard harness for the front door with its topic; a GitHub Copilot harness
  agent for the write-up skill; the first delegates to the second.

**3. The third**, which is what the course builds. The front door stays stable and keeps its
guarantee; the procedure stays in one readable file with one owner; the cost is a hop of latency and
a handoff that has to carry context.

What to write down — in the agent's own description, not only in a document:

> Built on the standard harness because it needs topics: the work order intake is a scripted
> exchange that must validate the number every time. The cost is that it cannot hold skills; the QN
> write-up skill lives on a connected agent instead.

If you found this in Part 3 rather than in B8, you have done the thing this module is for.
</details>

---

## Part 4 — Where does the human go? (5 minutes)

For each, say whether it needs no gate, a confirmation, or an approval — and why.

1. The agent reads `SAP_WORK_ORDERS` to answer a status question.
2. The agent drafts a quality notification write-up and shows it to Bruno.
3. The agent creates that notification as a record in SAP.
4. The agent releases revision C of `SWI70000318`.

<details>
<summary>Answers and reasoning</summary>

1. **No gate.** Handled by privilege, not process: the agent reads with a role that can read one
   schema and write nothing. Approving reads would be theatre, and privilege is a stronger guarantee
   than an approval anyway.
2. **No gate.** A draft is not an action. Bruno reads it and decides. Gating it would teach people
   that approvals are noise — and then the one that matters gets the same treatment.
3. **Confirmation.** A record others act on. The agent states exactly what it will create and waits
   for yes.
4. **Approval.** It changes what cladding operators work to, the same day. A named approver, with
   the draft, the ECN and what changed, in the request.

The principle: **the human goes at the last point where reversing is still cheap.** Not at the
start, where they have nothing to judge, and not after the effect, where approval is just
notification.
</details>

---

## Before you move on

Keep your Part 2 table. B5 to B9 build every row of it, and the fastest way to understand why a
module does what it does is to compare it with what you decided here.

Nothing in this exercise changed any state. B5 starts from an empty environment.
