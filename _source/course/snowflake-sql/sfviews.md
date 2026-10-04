## TL;DR

A view is a saved query that, in Snowflake's words, "allows the result of a query to be accessed as if it
were a table." For an agent, the view is the contract. It fixes the grain, removes known data flaws, puts
business words on columns and codes, and exposes only the rows and columns the agent should see. Do that
once, in SQL, and every tool and knowledge source that reads the view inherits it. Then grant the agent's
role the view, not the tables.

## Why it matters

{{topic:snowflakeknowledge}} showed what an agent does with raw tables. It reads `SAP_WO_OPERATIONS`, sums
the hours and reports welding at Plant 1 at about 111%, because nothing in the table says that some
operations were confirmed twice. It returns a work order's status as `REL`, which only a planner can read.
Neither is a prompt problem. The agent did what the names suggested.

A rule in an instruction or a tool description is a request the model usually honours. A rule in a view
is enforced by the database on every query. {{topic:addconnector}} made that argument for one tool; this
lesson is the craft of building the view.

## How it works

### Three kinds of view

| Kind | What Snowflake says | For an agent |
|---|---|---|
| **Non-materialized** (the default) | Results "are created by executing the query at the time that the view is referenced" | The normal choice. Always current, nothing stored |
| **Materialized** | Results "are stored, almost as though the results were a table" | Faster reads, at the cost of storage and maintenance. Rarely needed for a lookup agent |
| **Secure** | Either kind can be secure, for "improved data privacy and data sharing", with "some performance impacts" | Use when the definition itself should be hidden from the role that queries it |

A view is also **read-only**: "you cannot execute DML commands directly on a view." An agent that can
reach only views cannot change a row through them.

### Five jobs a view does for an agent

1. **Fix the grain.** One row per *thing*, stated in the view's comment. Deduplication happens here
   ({{topic:sfwindow}}).
2. **Use business words.** `WORK_ORDER`, not `WO_NO`. `OPERATION_STATUS`, not `STATUS`, which appears in
   five tables and means something different in each.
3. **Translate codes.** `CNF` becomes *Confirmed*. The model then never guesses what a code means, and
   neither does the user.
4. **Expose only what the agent needs.** Leave out columns it has no business with, such as
   `SAP_PROJECTS.CLIENT_NAME`, and rows it has nothing to say about.
5. **Say what it is.** A comment on the view and on each column it would be easy to misread.

### Comments

Snowflake's `COMMENT` command adds a comment to "all objects (users, roles, warehouses, databases, tables,
and so on)", and comments can also be set "when you are creating or altering objects". For a view, put
them in the `CREATE VIEW` statement, so the comments are written and reviewed with the definition. They
show up in `SHOW VIEWS` and `DESC` output, which is where a developer writing a tool description looks.

Whether a Copilot Studio knowledge source reads them is not documented ({{topic:snowflakeknowledge}}). Write
them for people and tools anyway. The names still have to stand on their own.

### Privileges: the view is the boundary

Granting access to a view rather than its tables is the point. Snowflake documents the rule: a user who can
read the view "but has no access to the underlying table of the view" can still query it as long as "the
owner role of the view has access to the underlying table". So the agent's role needs `SELECT` on the view
and nothing on the tables behind it.

### Limits to plan for

- **A definition cannot be edited in place.** You recreate the view with the new definition.
- **"Changes to a table are not automatically propagated to views."** Drop or rename a column in the
  replica and "the views on that table might become invalid", along with every tool that reads them.

## In practice at Technik

The Production Assistant's efficiency tool, `Get operation efficiency`, reads one view. It holds one row per work order
operation, with the stale confirmations removed:

```sql
CREATE OR REPLACE VIEW V_WORK_ORDER_OPERATIONS (
    WORK_ORDER        COMMENT 'SAP work order number, for example 100004521',
    OPERATION_SEQ     COMMENT 'Position of the operation in the work order routing',
    OPERATION         COMMENT 'Machining, Cladding, Welding, Bending, Coating or Assembly & Testing',
    WORK_CENTRE,
    PLANT,
    PROJECT,
    PART_NUMBER,
    OPERATION_STATUS  COMMENT 'Not started, In progress or Confirmed',
    WORK_ORDER_STATUS COMMENT 'Released, Partly confirmed, Confirmed or Technically complete',
    ROUTING_HOURS     COMMENT 'Planned hours for the operation',
    ACTUAL_HOURS      COMMENT 'Hours posted on the confirmation that counts',
    CONFIRMED_AT
)
COMMENT = 'One row per work order operation; superseded partial confirmations removed.
Efficiency % = SUM(ROUTING_HOURS) / SUM(ACTUAL_HOURS) * 100 over confirmed operations.'
AS
SELECT o.WO_NO, o.OP_SEQ, o.OPERATION, o.WORK_CENTER, w.PLANT, w.PROJECT_ID, w.PART_NO,
       CASE o.STATUS WHEN 'OPEN' THEN 'Not started' WHEN 'INPROC' THEN 'In progress'
                     WHEN 'CNF'  THEN 'Confirmed' END,
       CASE w.STATUS WHEN 'REL'  THEN 'Released'    WHEN 'PCNF'   THEN 'Partly confirmed'
                     WHEN 'CNF'  THEN 'Confirmed'   WHEN 'TECO'   THEN 'Technically complete' END,
       o.ROUTING_HOURS, o.ACTUAL_HOURS, o.CONFIRMED_AT
FROM SAP_WO_OPERATIONS o
JOIN SAP_WORK_ORDERS w ON w.WO_NO = o.WO_NO
WHERE w.STATUS <> 'CRTD'                      -- not released yet: nothing to report
QUALIFY ROW_NUMBER() OVER (PARTITION BY o.WO_NO, o.OP_SEQ
                           ORDER BY o.CONFIRMATION_NO DESC) = 1;

GRANT SELECT ON VIEW V_WORK_ORDER_OPERATIONS TO ROLE TECHNIK_AGENT_RO;
```

All five jobs are visible. The grain is in the comment and enforced by `QUALIFY`; the status filter is
safe before the window because it never splits one operation's confirmations. The names are a planner's,
the codes are words, and the project's client and field names are absent. So are drawing and program
revisions, which {{topic:addconnector}}'s `V_RELEASED_REVISIONS` already serves. Snowflake calls this building "hierarchies of views": small views,
each with one job.

The tool's fixed SQL is now short enough to review at a glance:

```sql
SELECT ROUND(SUM(ROUTING_HOURS) / SUM(ACTUAL_HOURS) * 100, 1) AS EFFICIENCY_PCT,
       COUNT(*) AS OPERATIONS
FROM V_WORK_ORDER_OPERATIONS
WHERE PLANT = :plant AND OPERATION = :operation
  AND OPERATION_STATUS = 'Confirmed'
  AND CONFIRMED_AT >= :period_start AND CONFIRMED_AT < :period_end;
```

For welding at Plant 1 in September it returns **88.9%**. No tool built on this view can return 111%,
because the duplicate rows never reach it. Returning `OPERATIONS` alongside the figure lets the agent say
what the number is based on.

The same view helps on the standard harness, where {{topic:snowflakeknowledge}}'s planning agent would point
at it instead of the raw tables. *"What is the status of work order `100004521`?"* then comes back as
*Released*, not `REL`.

## Design guidance

- **One view per question shape**, with the grain in its comment.
- **Put every known data flaw's fix in the view**, never in a description or an instruction.
- **Name columns as users speak**, and make every name unambiguous across views.
- **Translate every code** the agent might repeat to a user.
- **Leave out what the agent should not see.** A column that is not in the view cannot leak.
- **Grant the view, not the tables**, to the agent's role.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent reports a code such as `PCNF` | The view passes raw codes through | Translate in a `CASE` in the view |
| Efficiency over 100% from a tool on a view | The view kept one row per confirmation, not per operation | Fix the grain in the view with `QUALIFY` |
| The tool fails after an overnight change to the replica | A column the view uses was dropped or renamed | Recreate the view; check views whenever the replica's schema changes |
| The agent role cannot query a new view | No `SELECT` grant on it, or the view's owner cannot read the tables | Grant the view; check the owner role's access |
| Two tools disagree on the same figure | Each computes it from the tables in its own way | Both read one view |

## Key terms

**View** — a saved query that can be read as if it were a table. Read-only.

**Secure view** — a view whose definition is hidden from those who query it, at some cost in performance.

**Grain** — what one row of a view represents, such as one work order operation.

**Hierarchy of views** — small views built on tables or other views, each with one job.

**Owner role** — the role that owns a view. Its access to the tables is what lets others query the view
without table grants.
