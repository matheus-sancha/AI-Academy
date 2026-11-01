## TL;DR

A tool costs context twice: once for the definition sitting in the window on every turn, and again
for every result it returns. Anthropic's guidance treats the definition as an interface — tools
"define the contract between agents and their information/action space" — and asks that they be
"self-contained, robust to error, and extremely clear with respect to their intended use", with
"minimal overlap in functionality". The overlap test is a human one: "If a human engineer can't
definitively say which tool should be used in a given situation, an AI agent can't be expected to do
better." On the result side you are the one shaping it, and no harness is documented to do it for
you. The ceiling is real, too: VS Code stops at "a maximum of 128 tools enabled at a time."

## Why it matters

Intermediate taught the selection half: the orchestrator picks a tool mainly from its description,
so descriptions are the interface, and every tool costs context on every turn
({{topic:tooldesc}}, {{topic:contextcost}}). That still holds, and this lesson does not repeat it.

What is new is that you write both ends of the call. In Copilot Studio a tool returned what the
connector returned, formatted by the platform. In pro-code you write the function turning rows into
text, so the size, shape and error wording of every result is a design decision — and results
persist in the conversation long after the answer they supported.

## How it works

### The definition side

"One of the most common failure modes we see is bloated tool sets." The remedy is stated as
curation: "curating a minimal viable set of tools for the agent" leads to "more reliable
maintenance and pruning of context over long interactions." Parameters count too — they "should
similarly be descriptive, unambiguous, and play to the inherent strengths of the model", which in
practice means a typed, patterned, example-bearing parameter rather than a bare string.

Note what the guidance does *not* give: a number. There is no recommended tool count, because the
real constraint is ambiguity rather than arithmetic. Two tools whose descriptions a reviewer cannot
separate will be chosen between unpredictably no matter how few tools you have.

### The ceiling, and what to do about it

<!-- volatile verified=2026-11 -->
VS Code has a hard limit and says so in an error: "A chat request can have a maximum of 128 tools
enabled at a time." Two remedies are documented. Manually, "Open the tools picker in the Chat view
and deselect some tools or entire MCP servers to reduce the count." Automatically, "enable virtual
tools with the github.copilot.chat.virtualTools.threshold setting to automatically manage large tool
sets" — the page gives no default and no explanation of the mechanism.

Three facts around it matter more than the number. "All client-side tools are available to the
Copilot harness by default", so the count climbs as you install things, not as you choose things.
"Tool availability is separate from tool approval", and "Enabling a tool makes it available to the
agent, but doesn't bypass the configured approval and permission controls" — availability is a
context decision, approval is a safety one ({{topic:permissions}}). And the old grouping mechanism
is gone: "User-defined tool sets are deprecated and are not supported in the Copilot harness." The
replacement: "For a reusable tool selection, configure a custom agent" ({{topic:customize}}).
<!-- /volatile -->

The general advice is the same one the budget lesson gives: "Limit the selection to tools that are
relevant to your request."

### The result side

Tools should promote efficiency "by returning information that is token efficient and by
encouraging efficient agent behaviours". The cheapest later intervention is "tool result clearing",
described as "One of the safest lightest touch forms of compaction" ({{topic:history}}) — but
clearing a result you should not have returned in full is paying twice.

<!-- unknown since=2026-11 -->
VS Code's tools documentation says nothing about result size, token limits or truncation. So no
harness behaviour here can be assumed: do not rely on anything trimming a 4,000-row query result
before it reaches the model. Shape it in the tool.
<!-- /unknown -->

Errors are results too. Tools should be "robust to error", which means the error text is context
the model reads and acts on — so write it as an instruction to the model, not as a stack trace for
you ({{topic:loop}}).

## In practice at Technik

The capstone publishes three tools where the Intermediate build had five, and each description is
roughly 250 characters. The shape is deliberate on both sides:

*From [`server/teamcenter.py`, lines 76–87](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/server/teamcenter.py#L76-L87):*

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
```

Four things in twelve lines. The description says what the tool returns *and what it does not* — "It
does not return the document's text" is what stops the model reaching for this tool to answer a
question about porosity limits. `DocNo` is an annotated type carrying a pattern and an example, so a
malformed identifier fails before a query runs. The error names the failure and says what to do with
it, including the thing not to do. And the result is a `str` the function assembles, not the rows it
fetched ({{topic:budget}}).

Overlap is managed by having descriptions point at each other. `list_operation_documents` ends with
"Check whether that revision is still the released one with get_revision_status", making the
two-call chain explicit rather than leaving the model to infer it.

The best detail is what happens when a lookup finds nothing. An empty result set tells the model
nothing, so `no_items` works out *why* it was empty: no such work order raises an error saying so; a
work order whose operation does not exist raises an error listing the operations that do; and an
operation genuinely linking no documents returns that as an answer. Three outcomes where a naive
tool returns one empty list — and that operations list is what makes the next call correct rather
than a guess.

## Design guidance

- **Count the definitions as context.** A tool you keep "just in case" is paid on every turn,
  including the turns that need none of them.
- **Apply the reviewer test.** If a colleague cannot say which of two tools fits a case, the model
  will not either. Merge or re-describe.
- **Say what the tool does not do.** The boundary sentence prevents more wrong calls than the
  capability sentence enables right ones.
- **Type and pattern the parameters.** Validation at the edge is cheaper than a tool call that
  queries nothing.
- **Shape the result in the tool.** Assemble lines, drop fields nothing reads, truncate timestamps;
  never return a raw row set.
- **Write error text for the model.** Name the failure, say what to do next, say what not to claim,
  and make an empty result explain what does exist.
- **Keep availability and approval separate.** Narrow the tool list for context; use approvals for
  safety.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| "Cannot have more than 128 tools per request." | Every installed tool is available by default | Deselect tools or whole servers; consider virtual tools |
| Tool choice is inconsistent on the same question | Two descriptions a reviewer cannot separate either | Merge the tools, or re-describe with explicit boundaries |
| Context fills after two tool calls | Results return raw rows with repeated keys and full timestamps | Assemble the result in the tool; drop unread fields |
| The model retries the same failing call | The error text said nothing it could act on | Write errors as instructions; pass detailed errors through |
| An empty result produces an invented answer | Nothing told the model what the emptiness meant | Distinguish *not found* from *exists but has none* |
| A reusable tool selection stopped working | User-defined tool sets are deprecated on this harness | Configure a custom agent instead |
| A tool answers a question it should not | The description claims capability without stating limits | Add the sentence saying what it does not return |

## Key terms

**Tool definition** — the name, description and typed parameters published to the model; an
interface that occupies context on every turn.

**Tool result** — what the function returns into the conversation, where it persists after the
answer it supported.

**Minimal viable set** — the smallest group of tools that covers the agent's tasks with minimal
overlap in functionality.

**Virtual tools** — a VS Code mechanism for managing large tool sets automatically against the
per-request limit.

**Tool error** — a failure returned as text the model reads; context, and therefore written for the
model to act on.
