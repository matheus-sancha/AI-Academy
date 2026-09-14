> **About 90 minutes.** You need your Power Platform developer environment, Copilot Studio, and your
> Snowflake sandbox with `ACADEMY_AGENT_<you>` working. The lab consumes a modest number of Copilot
> Credits — roughly forty test turns.
>
> **This lab is independent.** It ships its own starter, so you do not need to have finished B6. If
> you did finish B6, your own agent is at the same state and you can use it instead.

## What you are building

Carla, a manufacturing engineer, asks:

> *"Which CNC program revision should machining use for `P7000001042`?"*

Today the assistant cannot answer. By the end of this lab it will query Teamcenter data in Snowflake
through a connector tool, return the **released** revision rather than whichever row came back
first, and warn Carla that work order `100004510` is running on a superseded one. Then you will add
an existing MCP server alongside it and compare the two ways of giving an agent reach.

B6 already gave this agent Snowflake knowledge, so it is worth being clear why a tool is needed at
all. Two reasons. The revision data lives in the `TC_*` tables, which are **not** in its knowledge —
B6 exposed only `SAP_WORK_ORDERS` and `SAP_WO_OPERATIONS`. And "which revision is released" is a
question you can name, asked every day, that someone will act on: exactly the kind
[Snowflake as a Knowledge Source](../B6/snowflakeknowledge.html) says should be a fixed
query rather than one invented per question.

## What the starter contains

`start/TechnikAssistant_B6_end.zip` is an unmanaged solution holding the Technik Production
Assistant exactly as B6 leaves it:

- **Agent:** *Technik Production Assistant*, standard harness, generative orchestration on.
- **Instructions:** identity (an internal assistant for Technik manufacturing and engineering
  staff), scope (work orders, quality, documents and revisions), tone (concise, factual, British
  English), and the four grounding rules added in B6 — answer only from knowledge, name the document
  an answer came from, prefer a controlled document over any summary of it, and quote criteria and
  test parameters exactly rather than paraphrasing them.
- **Topics:** one, *Work order status*, from B5.
- **Knowledge:** five controlled documents as uploaded files — `SOP70000101`, `SOP70000114`,
  `SWI70000318`, `SWI70000402` and `DGL70000009`; a SharePoint site holding the `TS-014` weld
  overlay acceptance page and the `TS-001` plant safety page; and the Snowflake tables
  `SAP_WORK_ORDERS` and `SAP_WO_OPERATIONS` as connector knowledge.
- **Tools:** none. That is what this lab is for.
- **Connection references:** two, SharePoint and Snowflake.

---

## Step 0 — Reset your sandbox

Every lab starts here. In a Snowflake worksheet:

```sql
USE ROLE ACADEMY_LEARNER_<you>;
USE WAREHOUSE ACADEMY_WH_<you>;
USE SCHEMA AI_ACADEMY.SANDBOX_<you>;

CALL AI_ACADEMY.SHARED.RESET_TO('B7');
```

It should report 13 tables restored. This drops anything you built in an earlier lab, including
views, so run it before step 1 and not after.

## Step 1 — Build the view the tool will query

The tool will not query `TC_PARTS`, `TC_DRAWINGS`, `TC_DOCUMENTS` and `TC_CNC_PROGRAMS` directly. It
will query one view that unions them, filtered to released revisions, with the ECN that introduced
each one. Run this as `ACADEMY_LEARNER_<you>`:

```sql
CREATE OR REPLACE VIEW V_RELEASED_REVISIONS
COMMENT = 'Current released revision of every Teamcenter item, with the ECN that introduced it. One row per item.'
AS
WITH items AS (
    SELECT PART_NO     AS ITEM_NO, 'Part'        AS ITEM_TYPE, DESCRIPTION AS TITLE,
           REVISION, RELEASED_AT
      FROM TC_PARTS          WHERE RELEASE_STATUS = 'Released'
    UNION ALL
    SELECT DRAWING_NO,        'Drawing',        TITLE,
           REVISION, RELEASED_AT
      FROM TC_DRAWINGS       WHERE RELEASE_STATUS = 'Released'
    UNION ALL
    SELECT PROGRAM_NO,        'CNC Program',    'CNC program for ' || PART_NO || ' on ' || MACHINE,
           REVISION, RELEASED_AT
      FROM TC_CNC_PROGRAMS   WHERE RELEASE_STATUS = 'Released'
    UNION ALL
    SELECT DOC_NO,            'Document',       TITLE,
           REVISION, RELEASED_AT
      FROM TC_DOCUMENTS      WHERE STATUS = 'Released'
)
SELECT i.ITEM_NO, i.ITEM_TYPE, i.TITLE, i.REVISION, i.RELEASED_AT,
       e.ECN_NO, e.TITLE AS ECN_TITLE
FROM items i
LEFT JOIN TC_ECN_AFFECTED_ITEMS a
       ON a.ITEM_NO = i.ITEM_NO AND a.TO_REV = i.REVISION
LEFT JOIN TC_ECNS e
       ON e.ECN_NO = a.ECN_NO AND e.STATUS = 'Released';
```

Check it:

```sql
SELECT * FROM V_RELEASED_REVISIONS WHERE ITEM_NO IN ('P7000001042','T7000000217','DU700001042');
```

You should get three rows: `P7000001042` at **revision C**, `T7000000217` at **revision B** and
`DU700001042` at **revision C**, all three citing `ECN70000051`. If `T7000000217` comes back as
revision A, the filter is wrong — fix it here rather than anywhere downstream.

> [!NOTE]
> Views are B10's subject; you are running this one rather than writing it. What matters now is
> *where the rule lives*. "Only released revisions" is a `WHERE` clause the database enforces on
> every call. The same rule written into a tool description would be a preference the model usually
> honours, and [B1's exercise](../B1/exercise.html) showed you what "usually" looks like
> when it fails.

## Step 2 — Prove the agent's role can read it

The agent will sign in as `ACADEMY_AGENT_<you>`, not as you. Check that now, before Copilot Studio
is involved:

```sql
USE ROLE ACADEMY_AGENT_<you>;
SELECT * FROM AI_ACADEMY.SANDBOX_<you>.V_RELEASED_REVISIONS WHERE ITEM_NO = 'P7000001042';
USE ROLE ACADEMY_LEARNER_<you>;
```

It works because your schema carries a future grant on views to the agent role, so the view you
created a minute ago is already readable. Half of all "the tool returns nothing" reports are a
missing grant, and this is the thirty seconds that rules it out.

## Step 3 — Import the starter

<!-- volatile verified=2026-09 -->
Import `start/TechnikAssistant_B6_end.zip` into your developer environment as an **unmanaged**
solution, then open it and re-bind the SharePoint connection reference to a connection of your own.
The import and connection-binding screens change between releases; follow the current documentation
if what you see does not match.
<!-- /volatile -->

Open the agent and ask it *"What does `SWI70000318` say about surface preparation before overlay?"*
You should get a grounded, cited answer. That confirms the starter imported correctly before you
change anything.

Now ask it *"Which CNC program revision should machining use for `P7000001042`?"* and keep the
answer. You will compare it with the one you get at the end.

## Step 4 — Check the Snowflake connection

The starter already carries a Snowflake connection reference, created in B6 for the work order
knowledge. Re-bind it to a connection of your own and confirm it uses:

| Setting | Value |
|---|---|
| Role | `ACADEMY_AGENT_<you>` |
| Warehouse | `ACADEMY_WH_<you>` |
| Database | `AI_ACADEMY` |
| Schema | `SANDBOX_<you>` |

Reuse it for the tool rather than creating a second connection. One connection reference per source
system per environment is the habit that makes B12's deployment step short.

> [!WARNING]
> Do not use `ACADEMY_LEARNER_<you>` here, even though it would work. The whole argument of
> [Connections & Authentication](connauth.html) is that a read-only identity is the
> guarantee that survives a prompt injection. You will attack this agent in B11; make the attack
> land somewhere harmless.

## Step 5 — Add the tool

Add a Snowflake connector action as a tool on the agent, with **exactly** these values.

**Name**

```
Get released revision
```

**Description**

```
Returns the current released revision of a Teamcenter item - a part, drawing, controlled document or
CNC program - with its title, the date it was released, and the Engineering Change Notification that
introduced it. Use when the user asks which revision to use, whether something is up to date, or why
a revision changed. Do not use for work order status, efficiency or quality notifications.
```

**Statement** — fixed, not model-filled:

```sql
SELECT ITEM_NO, ITEM_TYPE, TITLE, REVISION, RELEASED_AT, ECN_NO, ECN_TITLE
FROM V_RELEASED_REVISIONS
WHERE ITEM_NO = :item_no
LIMIT 5
```

**Inputs**

| Input | Mode | Value or description |
|---|---|---|
| `item_no` | Filled by the model | *The Teamcenter number to look up. Exactly eleven characters, for example P7000001042 for a part, DU700001042 for a drawing, T7000000217 for a CNC program, or SWI70000318 for a controlled document. Use exactly the number the user gave. If the user described an item in words instead of giving a number, ask which number they mean - never invent or reformat one.* |
| role | Fixed | `ACADEMY_AGENT_<you>` |
| warehouse | Fixed | `ACADEMY_WH_<you>` |
| database | Fixed | `AI_ACADEMY` |
| schema | Fixed | `SANDBOX_<you>` |

<!-- volatile verified=2026-09 -->
The Snowflake connector may need separate actions to submit a statement and to fetch its result. If
your environment's connector works that way, wrap both calls in an agent flow and add **the flow**
as the tool, keeping the name, description and input above unchanged. Check the connector reference
for the current action list.
<!-- /volatile -->

## Step 6 — Test the routing, not just the tool

The tool working and the orchestrator choosing it are different things. Run all eleven of these and
check the activity map each time.

**Should call the tool:**

1. "Which CNC program revision should machining use for `P7000001042`?"
2. "What is the latest released revision of drawing `DU700001042`?"
3. "Is `SWI70000318` up to date?"
4. "Why did `T7000000217` change?"
5. "What revision is `P7000001088` at?"

**Should not call the tool** — some of these the agent can still answer, from the knowledge B6 gave
it. The test is that it does not reach for the revision tool:

6. "What is the status of work order `100004521`?" — answered from Snowflake **knowledge**, not from
   your tool. Operation 0030, Welding, in process
7. "Show me open quality notifications on cladding." — `SAP_QUALITY_NOTIFICATIONS` is in neither its
   knowledge nor its tools, so it should say it cannot look that up
8. "What does `SWI70000318` say about surface preparation?" — document knowledge
9. "What is the minimum overlay thickness?" — document knowledge, citing `SWI70000318`
10. "What is our policy on overtime?" — out of scope entirely

**Deliberately ambiguous:**

11. "Which revision should I use for the valve block?" — no number given. The agent should **ask**
    which part, not invent `P7000001042`.

If 1–5 do not call the tool, the description is the problem. If 6–10 do call it, the exclusions are.
If 11 invents a part number, the input description is. Question 6 is the one worth watching closely:
two Snowflake routes now exist and the orchestrator has to pick between them, which is why your
tool's description says *"do not use for work order status"* in so many words.

## Step 7 — Make the answer useful

Right now the agent answers the question it was asked. Carla's real problem is the one nobody asked
about: work orders running on superseded revisions.

This agent can now do something neither half could do alone. The revision tool knows what is
released; the Snowflake knowledge from B6 knows what each operation's paperwork says. Put them
together and the agent can name the work orders that are out of date.

Add to the agent's instructions:

```
When you report a released revision for a part, drawing or CNC program, also check whether any
work order operation that has not yet been confirmed still references an older revision of that
item, and list those work orders with their operation numbers. Only list work orders that a
knowledge source or tool has actually returned. If you have not looked, say that the shop paperwork
should be checked rather than naming any work order.
```

Ask question 1 again. The answer should now:

- name `T7000000217` **revision B** and cite `ECN70000051`;
- say that work order `100004510` operation 0010 is still on program revision A — and, if it looked
  at the drawing too, that the same operation is on drawing revision B against a released C;
- name no work order it did not actually retrieve.

> [!IMPORTANT]
> The last sentence of that instruction is doing the real work. An instruction that mentions work
> orders invites the model to produce one, and it will produce a plausible number if it has not
> looked. "Only list what a source returned, otherwise say you have not looked" is the difference
> between a useful warning and an invented one.

> [!NOTE]
> Notice which kind of Snowflake question this is. Finding open operations on a given drawing
> revision is a **filter**, which [B6](../B6/snowflakeknowledge.html) put in the reliable
> class for generated SQL. Had it been a metric — "what share of open operations are on superseded
> revisions" — you should not trust a query invented at question time. B10 makes that one a view.

## Step 8 — Add an existing MCP server

Add an MCP server your organisation has approved to the same agent.

<!-- volatile verified=2026-09 -->
Which servers are available, certified or permitted by your tenant changes constantly, so this lab
does not name one. Ask your admin which servers are approved, or check the current documentation for
what Copilot Studio can connect to. A read-only documentation or knowledge server is ideal — you
want something whose tools plainly cannot change anything.
<!-- /volatile -->

Before you enable it, write down the answers to these. This is the graded part of the step, not the
adding:

1. Who publishes it?
2. What is its full tool list?
3. Which of those tools can change something?
4. What identity does it act with, and what can that identity reach?
5. Where does it run, and what data will it see?
6. How will you find out when its tool list changes?

Then enable the minimum set of tools you need.

## Step 9 — Test again, everything

Adding several tools at once changes the orchestrator's choices for the tool you already had. Re-run
questions 1–5 and 11 from step 6.

If any of them now route to an MCP tool instead of `Get released revision`, you have found the most
common MCP pitfall first-hand: overlapping descriptions. Sharpen yours, or disable the overlapping
tool.

---

## Checklist

You are done when all of these are true. Check them yourself; nothing enforces this.

- [ ] `SELECT * FROM V_RELEASED_REVISIONS` returns one row per released item, and `T7000000217` shows
      revision **B**.
- [ ] `ACADEMY_AGENT_<you>` can read the view; `ACADEMY_LEARNER_<you>` is not used by any connection.
- [ ] The agent answers question 1 with **revision B**, cites `ECN70000051`, and does not mention a
      superseded revision as if it were current.
- [ ] Questions 1–5 call `Get released revision`. You have seen it in the activity map, not assumed it.
- [ ] Questions 6–10 do **not** call it. Question 6 is answered from Snowflake knowledge instead,
      and question 7 produces an honest "I cannot look that up".
- [ ] Question 11 makes the agent **ask which part**, with no invented part number anywhere in the
      answer.
- [ ] After step 7, the revision answer names work order `100004510` as being on a superseded
      revision — and names no work order that was not actually retrieved.
- [ ] An MCP server is connected, and you can answer all six review questions about it from your own
      notes.
- [ ] After adding the server, questions 1–5 still route to your tool.

## What you should have learned

- The description is the routing logic. Most of this lab was writing.
- Constraints belong in the query. `RELEASE_STATUS = 'Released'` in SQL is a guarantee; the same
  sentence in a description is a preference.
- Identity is decided at the connection, and it bounds everything the agent could ever do.
- Input descriptions are read at exactly the moment the model is inventing a value, which makes them
  the cheapest place to prevent an invented part number.
- An MCP server is an address and a review. The address takes a minute; the review is the job.

## Next

`solution/TechnikAssistant_B7_end.zip` is the reference solution, and it is also the starter for B8,
where the assistant gains a skill that drafts quality notifications in Technik's format. Compare it
with yours — particularly the tool description and the instructions — before you move on.

Your Snowflake sandbox keeps `V_RELEASED_REVISIONS` until you reset it. B8's step 0 will replace it.
