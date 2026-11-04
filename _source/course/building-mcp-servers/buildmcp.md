## TL;DR

In Python the SDK writes the tool definition for you: "The `MCPServer` class uses Python type hints
and docstrings to automatically generate tool definitions." So a decorated function with annotated
parameters and a good docstring *is* the interface, and the two things you still own entirely are how
narrow each tool is and what a failure tells the model. The official tutorial requires "the Python
MCP SDK 2.0.0 or higher", shows `mcp.run(transport="stdio")`, and is categorical about one thing:
"Never write to stdout."

## Why it matters

Everything you learned about tool descriptions in Copilot Studio applies here with one difference —
there is no form to fill in ({{topic:tooldesc}}). The description the orchestrator reads is your
docstring, the input schema is your type annotations, and both ship when you commit. Which means a
sloppy signature is not a style problem; it is a published contract that the model will read literally
and act on wrongly.

The second reason is the shape of the mistake people make. The tutorial's tools catch every exception
and return a sentence. That works for a weather demo and fails for Technik, where "Unable to fetch
alerts" is indistinguishable from "there are none" — and a model that cannot tell those apart will
confidently report an empty result as a fact ({{topic:hallucination}}).

## How it works

### The whole server is a decorator and a `run`

The tutorial's Python server imports `MCPServer` from `mcp.server`, constructs it with a name, puts
`@mcp.tool()` on an `async def`, annotates the parameters with plain Python types (`state: str`,
`latitude: float`), writes a docstring with a Google-style `Args:` block, and ends with:

```python
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

That is all of it. There is no schema to hand-write, no registration call, no manifest. Other SDKs
are not as terse — TypeScript uses `zod` and `server.registerTool`, Kotlin and Ruby hand-write the
JSON schema, C# and Java use attributes and annotations — but Python's is the one the capstone uses,
and "A .NET or TypeScript SDK is named in prose and never shown" at this level.

### What the docstring and the annotations become

The docstring is the model's only explanation of when to reach for the tool, and the annotations
become the input schema that decides what reaches your code at all. The tutorial's three parameter
types are bare (`str`, `float`), which accepts any string at all — adequate for a two-letter state
code, dangerous for anything an identifier format governs.

The SDK's own typing gives you more than the tutorial shows. A `pydantic` `Field` attached with
`Annotated` adds a validation pattern *and* a description, so a malformed argument is rejected before
your function runs and a well-formed one arrives with an example the model has already seen.

### Logging, and the one unbreakable rule

> "For STDIO-based servers: Never write to stdout. Writing to stdout will corrupt the JSON-RPC
> messages and break your server. The `print()` function writes to stdout by default, so keep it out
> of a STDIO server entirely."

Use "the standard library `logging` module, which writes to stderr", with "one logger per module with
`logging.getLogger(__name__)`". On HTTP it stops mattering: "Standard output logging is fine since it
doesn't interfere with HTTP responses" ({{topic:transports}}).

Every other language gets the same instruction with a different function named — `console.log()`,
`System.out.println()`, `println()`, `Console.WriteLine()`, `puts`, `fmt.Println()` — which is a fair
sign of how often it is the bug.

### Paths are absolute, and the launch command is the config

A client launches a stdio server, so the configuration is a command rather than an address. The
tutorial's advice is mechanical and worth taking: "Make sure you pass in the absolute path to your
server", get `uv`'s own path from `where uv` on Windows if the command is not found, and on Windows
"use double backslashes (`\\`) or forward slashes (`/`) in the JSON path". A project-relative launch
is what `${workspaceFolder}` solves in the editor ({{topic:mcpvscode}}).

<!-- unknown since=2026-11 -->
The tutorial gives no error mechanism at all. Its tools swallow exceptions and return prose, and no
page in it names an error type, an `is_error` flag, or the difference between a tool failing and the
protocol failing. It also says nothing about how narrow a tool should be or how large a result may be
— the only hints are two comments trimming output to five items. Treat both as your judgement to
exercise, not as something the documentation has settled.
<!-- /unknown -->

## In practice at Technik

The Teamcenter server takes the typing further than the tutorial does, and the reason is Technik's
identifier formats. Every Teamcenter number is eleven characters with a fixed shape, so that shape
belongs in the schema rather than in a sentence asking for it:

*From [`server/teamcenter.py`, lines 23–28](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/server/teamcenter.py#L23-L28):*

```python
WorkOrder = Annotated[str, Field(pattern=r"^1\d{8}$", description="SAP work order number, for example 100004521")]
OperationSeq = Annotated[str, Field(pattern=r"^\d{4}$", description="Operation in the routing, for example 0020")]
DocNo = Annotated[str, Field(pattern=r"^[A-Z]{3}\d{8}$", description="Document number, for example SWI70000318")]
ItemNo = Annotated[str, Field(pattern=r"^[A-Z]{1,3}\d{8,10}$",
                              description="Part, drawing, CNC program or document number, for example DU700001042")]
Revision = Annotated[str, Field(pattern=r"^[A-Z]{1,2}$", description="Revision letter, for example B")]
```

Those patterns do real work. A user asking about "quality handling" rather than `SOP70000101` is
rejected by the input schema before the tool runs — the capstone's stdio test asserts exactly that,
calling `get_document` with `"quality handling"` and checking the result came back as an error. Free
text never reaches Snowflake, which is one fewer thing for {{topic:mcpsec}} to worry about.

The tool itself is nineteen lines, and the shape is: query, fail loudly if empty, format for reading.

*From [`server/teamcenter.py`, lines 76–94](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/server/teamcenter.py#L76-L94):*

```python
@mcp.tool()
def get_document(doc_no: DocNo) -> str:
    """Look up a controlled document (SOP, SWI, GWI, TDS, DGL or DCP) by its number.

    Returns its title, type and owner, and every revision with its status and review date.
    Use it for a document's metadata. It does not return the document's text.
    """
    revisions = rows("""SELECT DOC_TYPE, REVISION, TITLE, OWNER, STATUS, RELEASED_AT, NEXT_REVIEW_DATE
                        FROM TC_DOCUMENTS WHERE DOC_NO = %(doc_no)s ORDER BY REVISION DESC""", doc_no=doc_no)
    if not revisions:
        raise ToolError(f"No document {doc_no} in Teamcenter. Check the number with the user. "
                        "Do not describe a document you could not find.")
    first = revisions[0]
    lines = [f"{doc_no}: {first['TITLE']} ({first['DOC_TYPE']}), owner {first['OWNER']}"]
    for r in revisions:
        released = f", released {day(r['RELEASED_AT'])}, next review {day(r['NEXT_REVIEW_DATE'])}" \
            if r["STATUS"] == "Released" else ""
        lines.append(f"  rev {r['REVISION']}: {r['STATUS']}{released}")
    return "\n".join(lines)
```

Three decisions are visible there. The docstring's last line — "It does not return the document's
text" — exists because the obvious wrong call is asking this tool what section 5 says. The query is
parameterised, so an identifier is never concatenated into SQL. And the failure is a raised
`ToolError` carrying an instruction rather than a returned sentence, because a model that reads "No
document X" with no instruction attached will often invent one anyway.

That last pattern is the server's house style. An unknown work order says so; a missing operation
lists the operations that *do* exist; an item never released adds "do not treat any revision of it as
approved". Each error is written for a reader who will act on it ({{topic:toolshaping}}).

> [!NOTE]
> The capstone imports `MCPServer` from `mcp.server.mcpserver` and `ToolError` from
> `mcp.server.mcpserver.exceptions`, while the tutorial imports from `mcp.server`. Both work in v2.
> What does not is `mcp.server.fastmcp`, which raises with a pointer to the migration guide — the
> single most common failure when following an older article.

## Design guidance

- **One question per tool.** If the docstring needs the word "and", consider two tools.
- **Put the format in the schema**, not in the prose. A pattern rejects bad input before your code
  runs; a sentence only asks nicely.
- **Say what a tool does not do.** The wrong call is usually the plausible one.
- **Raise errors that tell the model what to do next**, not just what went wrong.
- **Never let "failed" and "none found" read alike.** They are different answers.
- **Parameterise every query.** The identifier came from a model, which got it from a user.
- **Keep results short enough to read.** Everything the tool returns is context someone pays for
  ({{topic:budget}}).
- **Keep `print()` out of a stdio server entirely.**

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The client reports broken JSON | Something wrote to stdout | Log to stderr via `logging` |
| `ImportError` following a tutorial | `mcp.server.fastmcp` is gone in v2 | Import `MCPServer` from `mcp.server` |
| The model calls the wrong tool | Two docstrings describe the same job | Rewrite both to say when *not* to use them |
| Garbage reaches your database | Bare `str` parameters accept anything | Add a `Field(pattern=…)` |
| The agent reports "no results" for an outage | Errors returned as ordinary prose | Raise a tool error instead |
| The server starts for you and not for the client | A relative path in the launch command | Use absolute paths or `${workspaceFolder}` |

## Key terms

**`MCPServer`** — the Python SDK v2 server class; `mcp.server.fastmcp` is its retired predecessor.

**Tool definition** — the name, description and input schema generated from your function's name,
docstring and annotations.

**`ToolError`** — an exception the server raises so a failure reaches the model as an error with a
message, rather than as a plausible-looking answer.
