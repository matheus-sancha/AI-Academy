## TL;DR

A model never runs anything. With function calling it answers by returning a structured request: a function name
and a string of JSON arguments. Your code, or the harness around the model, runs the function and sends the result
back in a second call, and the model writes its answer from that. This lesson takes the exchange apart: the three
steps, the message shapes, `tool_choice`, what a definition costs, and why a call is validated like any other
input. The capstone's three Teamcenter tools are this mechanism with an MCP server in the middle.

## Why it matters

The tool lessons ({{topic:tooldesc}}, {{topic:toolshaping}}, {{topic:mcparch}}) describe what surrounds a call.
This one is the call. When an agent invents an argument, calls nothing, or answers without looking anything up, the
cause is in what the model was shown, what it returned, or what your code did with it. You can only say which if
you know the exchange.

## How it works

### Three steps, two model calls

The page splits function calling into three steps. You call the API with your functions and the user's input. You
use the response to call your function. You call the API again with the function's result, for the final response.
The model decides whether to call anything, and your application runs the function, so you stay in control of what
is done. The model proposes and your code disposes.

<!-- volatile verified=2026-11 -->
The page's examples use the Chat Completions API. A response that calls a function carries `tool_calls` instead of
text. Each call has an `id`, a function `name` and `arguments`, which arrive as a JSON string that your code
parses. The result goes back as a message with the role `tool` and a `tool_call_id` that matches the call's `id`.
The Responses API uses a different request and response format, which the page leaves to another page
({{topic:params}} lists the renamed fields).

*Adapted from the single-function sample on the function calling page, with Technik's values:*

```json
[
  { "role": "assistant", "content": null,
    "tool_calls": [ { "id": "<call id>", "type": "function",
      "function": { "name": "get_revision_status",
                    "arguments": "{\"item_no\": \"SWI70000318\", \"revision\": \"B\"}" } } ] },
  { "role": "tool", "tool_call_id": "<call id>", "name": "get_revision_status",
    "content": "Document SWI70000318 (<title>): the released revision is rev B, …" }
]
```
<!-- /volatile -->

### Parallel calls and `tool_choice`

One response can hold several calls. The page asks for the time in three cities and gets three entries in
`tool_calls`, each answered by its own `tool` message. Running them together reduces the number of API calls and can
improve performance, on a deployment that supports parallel calls.

<!-- volatile verified=2026-11 -->
By default, `tool_choice` is `auto`, and the model decides whether to call a function and which. Set it to a
named function to force that call, or to `none` to force a message to the user. The older `functions` and
`function_call` parameters are deprecated in favour of `tools` and `tool_choice`. The page limits a tool or
function description to 1,024 characters and says it will update the article if that changes.
<!-- /volatile -->

{{topic:params}} marked `tool_choice` unknown, because neither of its pages describes it. This page does, for Chat
Completions. It does not say what a description over the limit does: whether it is rejected or cut.

### A definition is prompt text

The page says a function's details are injected into the system message, in a syntax the model was trained on. So
definitions consume prompt tokens ({{topic:tokenbudget}}), and the model chooses from the definition, the system
message and the user's messages together. It gives three remedies for a function that is not called when or how you
expect: a meaningful description, with one for each parameter that is not obvious and an example of its format;
context in the system message; and an instruction to ask when a request is ambiguous rather than assume a value.
To stop calls to functions you never provided, it suggests one sentence saying to use only those given.

### Treat a call as untrusted input

The page says plainly that models can "produce a function call that doesn't match the schema you defined", or name a
function you did not include, and that the JSON may not always be valid. Its safety list is a list of things your
code does:

- Validate each call: the parameters, the function, and whether it matches the intended action.
- Use only trusted data, because untrusted data in a function's output can instruct the model to write calls other
  than you intended ({{topic:ctxsecurity}}).
- Grant least privilege, such as a read-only database login, and do not rely on leaving a capability out of the
  definition as a security control.
- Ask the user to confirm before a function that acts.

<!-- unknown since=2026-11 -->
The roadmap says MCP, Copilot Studio tools and Agent Framework tools all rest on this mechanism. The page describes
Chat Completions and mentions none of the three. The capstone shows Agent Framework only from outside, and nothing
in either curated source covers Copilot Studio, so treat that sentence as the course's reading, not Microsoft's.
<!-- /unknown -->

## In practice at Technik

Take a controlled-document question: *is revision B of `SWI70000318` still the released one?* The capstone's
`get_revision_status` is the definition the model chooses from. Its argument types come first:

*From [`server/teamcenter.py`, lines 26–28](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/server/teamcenter.py#L26-L28):*

```python
ItemNo = Annotated[str, Field(pattern=r"^[A-Z]{1,3}\d{8,10}$",
                              description="Part, drawing, CNC program or document number, for example DU700001042")]
Revision = Annotated[str, Field(pattern=r"^[A-Z]{1,2}$", description="Revision letter, for example B")]
```

Then the tool:

*From [`server/teamcenter.py`, lines 130–141](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/server/teamcenter.py#L130-L141):*

```python
@mcp.tool()
def get_revision_status(item_no: ItemNo, revision: Revision | None = None) -> str:
    """Say whether a revision of a part, drawing, CNC program or document is the released one.

    Leave out the revision to get the released revision. A revision that is not released was
    either superseded or is still in work; the answer names the released one and its change notice.
    """
    released = rows("""SELECT ITEM_TYPE, TITLE, REVISION, RELEASED_AT, ECN_NO, ECN_TITLE
                       FROM V_RELEASED_REVISIONS WHERE ITEM_NO = %(item)s""", item=item_no)
    if not released:
        raise ToolError(f"{item_no} has no released revision in Teamcenter. It may not exist, "
                        "or may never have been released. Do not treat any revision of it as approved.")
```

Each part follows the page's advice. The docstring is the description: when to use the tool, and what the answer
holds. Every parameter carries a format example, which is the page's `location` advice applied to a document
number. And the error text is a prompt that tells the model what to do next. If the model calls the tool, the
exchange is two model calls and one tool run. The first carries the three definitions and the question, and returns
a call for `SWI70000318` revision `B`. The second carries the result and returns the answer. A question about two
documents would return two calls in one response.

The capstone's loop adds two pieces the page does not cover. `TOOL_LOOP` caps the calls per question at six and
shows the model the server's error text ({{topic:loop}}). And a guard checks that a tool result exists:

*From [`agent/main.py`, lines 23–27](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/agent/main.py#L23-L27):*

```python
def refuse_unless_grounded(response):
    """An answer that no tool result backs came from the model's memory: replace it with the refusal."""
    if not any(c.type == "function_result" for m in response.messages for c in m.contents):
        response.messages = [Message(role="assistant", contents=[REFUSAL])]
    return response
```

This applies the page's validation advice to the answer. The offline tests use a fake chat client, so the
framework's request to a real model is never seen.

<!-- unknown since=2026-11 -->
Whether the `pattern` constraints are enforced before a tool body runs is not isolated. The stdio test sends
`quality handling` as a document number and asserts an error, but the fake database also finds no such document,
so the not-found path could have produced it. Nor is it known what schema the SDK generates from these types, or
whether Agent Framework sends tools as strict ({{topic:structured}}).
<!-- /unknown -->

## Design guidance

- **Write the description for the model.** Say when to use the tool, what it returns and what it does not.
- **Describe every parameter that is not obvious**, with a format example.
- **Make errors say what to do next**, not a bare failure.
- **Validate every call in code**, even with a schema: the function, the arguments and the intent.
- **Give the tool the least access it needs**, and never treat the definition as the control.
- **Cap the loop.** Each round is another model call ({{topic:latency}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The model never calls the tool | A thin description, or a system message that never says when to use it | Describe the tool and its parameters, and add context to the system message |
| It calls with a value nobody gave it | The request was ambiguous and the model assumed | Tell it to ask for clarification |
| A call names a function you did not provide | The model can do that, as the page says | State the allowed set, and reject any call outside it in code |
| Arguments fail to parse | The JSON may not always be valid | Parse defensively and return the failure as a tool error |
| Old code stops working | `functions` and `function_call` are deprecated | Use `tools` and `tool_choice` |
| A tool result steers the model | Untrusted text in a result acts as instruction | Least privilege, and a deterministic check ({{topic:ctxsecurity}}) |

## Key terms

**Function calling**: the model returns a function name and arguments, and your code runs the function.

**Tool call**: one entry in `tool_calls`: an `id`, a function name and a JSON string of arguments.

**Tool message**: the message that carries a result back, matched to its call by `tool_call_id`.

**`tool_choice`**: the setting that lets the model decide, forces one function or forces a message.
