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

## What the starter contains

`start/TechnikAssistant_B6_end.zip` is an unmanaged solution holding the Technik Production
Assistant exactly as B6 leaves it:

- **Agent:** *Technik Production Assistant*, standard harness, generative orchestration on.
- **Instructions:** identity (an internal assistant for Technik manufacturing and engineering
  staff), scope (work orders, quality, documents and revisions), tone (concise, factual, British
  English), a rule to cite sources, and a rule to say so when it cannot find something rather than
  guessing.
- **Knowledge:** the fictional controlled documents `SOP70000101`, `SWI70000318`, `SWI70000402` and
  `DGL70000009` as uploaded files, plus a SharePoint site holding the Technik standards pages.
- **Tools:** none. That is what this lab is for.
- **Connection references:** one for SharePoint.

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
> honours, and [B1's exercise](../../course/B1/exercise.html) showed you what "usually" looks like
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

## Step 4 — Create the Snowflake connection

Create a connection for the Snowflake connector using **`ACADEMY_AGENT_<you>`** as the role, your
warehouse `ACADEMY_WH_<you>`, database `AI_ACADEMY` and schema `SANDBOX_<you>`.

Use a connection reference, not a bare connection — B12 will thank you.

> [!WARNING]
> Do not use `ACADEMY_LEARNER_<you>` here, even though it would work. The whole argument of
> [Connections & Authentication](../../course/B7/connauth.html) is that a read-only identity is the
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

**Should not call the tool:**

6. "What is the status of work order `100004521`?" — no tool for that yet; it should say so
7. "Show me open quality notifications on cladding." — likewise
8. "What does `SWI70000318` say about surface preparation?" — knowledge, not a tool
9. "Who is the owner of `SOP70000101`?" — knowledge
10. "What is our policy on overtime?" — out of scope entirely

**Deliberately ambiguous:**

11. "Which revision should I use for the valve block?" — no number given. The agent should **ask**
    which part, not invent `P7000001042`.

If 1–5 do not call the tool, the description is the problem. If 6–10 do call it, the exclusions are.
If 11 invents a part number, the input description is.

## Step 7 — Make the answer useful

Right now the agent answers the question it was asked. Carla's real problem is the one nobody asked
about: work orders running on superseded revisions.

Add to the agent's instructions:

```
When you report a released revision for a part, drawing or CNC program, and the conversation is
about manufacturing that item, say plainly that shop paperwork may still show an older revision and
that the operator should check before starting. Never state which work orders are affected unless a
tool has returned that information - you cannot see work order data yet.
```

Ask question 1 again. The answer should now name revision B, cite `ECN70000051`, and add the
caution — without inventing work order numbers.

> [!IMPORTANT]
> That second sentence is doing real work. Without it, an instruction that mentions work orders
> invites the model to produce one, and it will produce a plausible number. The assistant gains
> genuine work order data in B10; until then the honest answer is a caution, not a list.

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
- [ ] Questions 6–10 do **not** call it, and 6 and 7 produce an honest "I cannot look that up yet".
- [ ] Question 11 makes the agent **ask which part**, with no invented part number anywhere in the
      answer.
- [ ] The revision answer includes the caution from step 7 and names no work order.
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
