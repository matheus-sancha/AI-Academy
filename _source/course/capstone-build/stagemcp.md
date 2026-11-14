## TL;DR

Stage 2 builds the MCP server, and it builds it from the questions backwards. Three questions, each already named
in your eval set, become three narrow tools over three views. A tool returns a short answer, rejects an input
that is the wrong shape, and when it fails it says what to do next. You prove it twice: once with a test that
starts the real server over stdio against a fake Snowflake, and once by calling it from agent mode in VS Code
before any agent of yours exists.

## Why it matters

The server is the part of the capstone that every other part trusts. The agent believes what a tool returns, the
evals grade what the agent says, and the deployment ships the server unchanged. A wrong description, or an error
that gives the model nothing to act on, costs you a stage later and a redeployment after that. In the editor it is
a five-second edit ({{topic:mcpvscode}}).

It is also the stage where the scenario's data meets an identity. The server connects as `TECHNIK_AGENT_SVC`,
the service user the check proved, so a query that works for you here works for the agent later, and one that cannot
will fail now and not in production.

## How it works

### Start from the questions

The eval cases already say what the agent will be asked. Read them for the questions that need a lookup, and give
each its own tool.

| Tool | The question it answers | Reads |
|---|---|---|
| `get_document` | What is this document, who owns it and which revisions exist? | `TC_DOCUMENTS` |
| `list_operation_documents` | Which drawing, CNC program and work instruction does this operation use? | `V_OPERATION_DOCUMENTS` |
| `get_revision_status` | Is this revision the released one, and which change notice released it? | `V_RELEASED_REVISIONS` |

None needs the result of another, which is what a stateless server wants ({{topic:mcparch}}). When a person's
question needs two facts, the agent makes two calls and joins them.

### A new view for a new question

The first two views were built for other questions, and neither links an operation to the items it uses. A third
view does, and the stage reads it rather than inventing it. *From [`seed/02_views.sql`, lines 54–77](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/seed/02_views.sql#L54-L77):*

```sql
CREATE OR REPLACE VIEW V_OPERATION_DOCUMENTS (
    WORK_ORDER    COMMENT 'SAP work order number, for example 100004521',
    OPERATION_SEQ COMMENT 'Position of the operation in the work order routing',
    OPERATION,
    ITEM_NO       COMMENT 'Teamcenter number of the drawing, CNC program or work instruction',
    ITEM_TYPE     COMMENT 'Drawing, CNC Program or Document, as in V_RELEASED_REVISIONS',
    REVISION      COMMENT 'Revision the operation was released against. Empty for work instructions,
                           which follow the current released revision'
)
COMMENT = 'The Teamcenter items each work order operation uses: one row per linked item.'
AS
WITH ops AS (
    SELECT o.*
    FROM SAP_WO_OPERATIONS o
    JOIN SAP_WORK_ORDERS w ON w.WO_NO = o.WO_NO
    WHERE w.STATUS <> 'CRTD'
    QUALIFY ROW_NUMBER() OVER (PARTITION BY o.WO_NO, o.OP_SEQ
                               ORDER BY o.CONFIRMATION_NO DESC) = 1
)
SELECT WO_NO, OP_SEQ, OPERATION, DRAWING_NO,          'Drawing',     DRAWING_REV     FROM ops WHERE DRAWING_NO IS NOT NULL
UNION ALL
SELECT WO_NO, OP_SEQ, OPERATION, CNC_PROGRAM_NO,      'CNC Program', CNC_PROGRAM_REV FROM ops WHERE CNC_PROGRAM_NO IS NOT NULL
UNION ALL
SELECT WO_NO, OP_SEQ, OPERATION, WORK_INSTRUCTION_NO, 'Document',    NULL            FROM ops WHERE WORK_INSTRUCTION_NO IS NOT NULL;
```

An operation carries three item columns on one row. The view turns them into one row per linked item, so the tool
needs no `CASE`, and the one NULL left is a work instruction's revision, which the tool words as *the current
released revision*. It repeats the first view's `QUALIFY`, because
the same superseded confirmations would otherwise duplicate every item ({{topic:sfviews}}). And the column
comments are the schema the tool's author reads. The new view needs a fifth grant, which the seed script already
makes. *From [`seed/03_access.sql`, line 19](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/seed/03_access.sql#L19):*

```sql
GRANT SELECT ON VIEW  TECHNIK_DW.OPS.V_OPERATION_DOCUMENTS     TO ROLE TECHNIK_AGENT_RO;   -- stage 2: the MCP server
```

### Errors that say what to do

The interesting code in the server is the failures. The input types reject a wrong shape before a tool runs
({{topic:buildmcp}}). What remains is a valid number that matches nothing, and an operation with no rows can mean
three different things. *From [`server/teamcenter.py`, lines 116–127](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/server/teamcenter.py#L116-L127):*

```python
def no_items(work_order, operation_seq):
    """Say why an operation has no linked items: it has none, or the operation does not exist."""
    ops = rows("""SELECT OPERATION_SEQ, OPERATION FROM V_WORK_ORDER_OPERATIONS
                  WHERE WORK_ORDER = %(wo)s ORDER BY OPERATION_SEQ""", wo=work_order)
    if not ops:
        raise ToolError(f"No released work order {work_order}. Check the number with the user.")
    for op in ops:
        if op["OPERATION_SEQ"] == operation_seq:
            return f"{work_order} operation {operation_seq} ({op['OPERATION']}) uses no drawing, " \
                   "CNC program or work instruction in Teamcenter."
    listed = ", ".join(f"{op['OPERATION_SEQ']} {op['OPERATION']}" for op in ops)
    raise ToolError(f"Work order {work_order} has no operation {operation_seq}. Its operations are: {listed}.")
```

A work order that is not released is an error. An operation that exists and uses nothing is a fact, returned as
text. A wrong operation number is an error that lists the right ones. The model can act on each: ask the user,
report the fact, or try again with a real number. A bare *not found* would leave it to guess, and a model told
nothing will often invent an answer ({{topic:toolshaping}}).

`get_revision_status` makes the same choice from the other side. Its docstring tells the model that a revision which
is not released was superseded or is still in work, and its answer names the released revision and the change
notice. A tool description is where a tool says when to use it ({{topic:tooldesc}}).

### Test it with no model and no account

The tests never touch Snowflake. A fake connection loads `seed/data/` into an in-memory SQLite database and exposes
only the five objects the role is granted, so a query that reaches a table behind a view fails here as it would for
the real role. *From [`tests/fake_server.py`, lines 11–17](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/tests/fake_server.py#L11-L17):*

```python
import teamcenter  # noqa: E402
from fakes import FakeConnection  # noqa: E402

teamcenter.connect = FakeConnection

if __name__ == "__main__":
    teamcenter.serve_http() if "--http" in sys.argv else teamcenter.mcp.run()
```

Everything in the process is the real server except the connection. The stdio test spawns this file and talks to
it through an MCP client. *From [`tests/test_stdio.py`, lines 30–36](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/tests/test_stdio.py#L30-L36):*

```python
def test_server_answers_over_stdio():
    names, calls = asyncio.run(session())
    assert names == TOOLS
    assert text(calls["document"]).startswith("SOP70000101: Quality Notification Handling (SOP)")
    assert text(calls["operation"]).splitlines()[1] == "  Document SWI70000318, the current released revision"
    assert "the released revision is rev B" in text(calls["revision"])
    assert calls["bad_input"].is_error and not calls["document"].is_error
```

Run `uv run pytest` from the root. At the tag the root suite is 20 tests, and the ones in `test_http.py` and
`test_deploy.py` belong to stage 5.

### Call it from the editor

Create `.vscode/mcp.json` as {{topic:mcpvscode}} shows it, start the server from that file and open agent mode.
VS Code's documentation labels this file deprecated in its guided flow, in favour of a workspace-root `.mcp.json`,
and the capstone stays on it on purpose. The newer file needs an experimental setting and a renamed top-level key, and keeping
the capstone's file means every line range in this course still points at it. Moving yours is one small commit.

Then ask the question that catches an agent answering from habit: *which drawing does work order `100004510`
operation `0010` use, and is that revision still released?* The two calls return this against the seed's rows:

```text
100004510 operation 0010 (Machining) uses:
  Drawing DU700001042, rev B
  Document SWI70000331, the current released revision
  CNC Program T7000000217, rev B
```

```text
Drawing DU700001042 (XT V2 valve body, clad bore): the released revision is rev C, released 2026-09-15 under ECN70000051 (XT V2 body: increase bore overlay machining allowance).
```

The operation was released against revision B and revision C is current, so a correct answer names both. An answer
from one tool alone is wrong.

## In practice at Technik

You finish holding a server that starts over stdio, a test suite that passes without a network, and the two
outputs above in front of you in agent mode. Nothing here is an agent yet. If the editor shows a different
protocol version, or runs the launch command from a different folder than you expect, you have met the first of
the unchecked points on {{topic:buildsetup}}. Note what you saw.

## Design guidance

- **Derive the tools from the questions.** One tool per question, none depending on another.
- **Make a view for a question the others cannot answer**, and grant it by name.
- **Separate three outcomes**: an input that is the wrong shape, a lookup that finds nothing, and a fact that happens
  to be empty.
- **Write each error as an instruction** to the model about what to do next.
- **Test the real process over stdio**, and fake only the connection.
- **Call it from the editor before an agent exists**, so a wrong description costs seconds.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The tool says *No released work order* for a number you can see in Snowflake | `V_WORK_ORDER_OPERATIONS` leaves out work orders not yet released | Check the order's status. The message is accurate |
| An answer names revision B as current | `list_operation_documents` returns the revision the operation was released against, not the current one | Make the second call, `get_revision_status`, and say so in the description |
| The model invents a document after a miss | The error told it what failed and not what to do | Add the instruction, as `get_document`'s error does |
| The editor lists no tools | `uv` is not on the path the editor uses, or the launch folder is wrong | Read the server's output in the editor ({{topic:mcpvscode}}) |
| A query works as admin and fails as the agent | It reaches a table behind a view | Query the view, or add one |

## Key terms

**Narrow tool**: a tool that answers one question over one view, with typed inputs.

**Tool error**: a failure returned to the model as text it can act on.

**Stdio transport**: the server runs as a child process that the client starts and talks to over its input and output.

**Fake connection**: a stand-in for Snowflake that exposes only what the role may read.
