## TL;DR

A transport is "a binding: it defines how messages are framed and delivered […] It does not define
what the messages mean." Two are standard. **stdio** is newline-delimited JSON-RPC over a
client-launched subprocess, so the client owns the process lifecycle. **Streamable HTTP** is one POST
per message to a single endpoint, answered by a JSON object or a request-scoped SSE stream. Revision
`2026-07-28` removed the GET stream and **protocol-level sessions**: no `Mcp-Session-Id`, no
resumable stream. HTTP+SSE is deprecated. Choosing between the two chooses your threat model.

## Why it matters

The transport decides three things the data layer never mentions: who can reach your server, what a
restart costs, and what one stray line on standard output does.

On stdio the client starts your process, so your server inherits the permissions of whoever started
the session, and nothing on the network can reach it. On Streamable HTTP the opposite holds: the
server outlives any one client, anything that resolves its address can try it, and an unvalidated
`Origin` header is a browser-driven attack on a service that looks local ({{topic:mcpsec}}).

There is also a cost to reading the wrong revision. Plenty of writing about MCP still describes
sessions, a GET event stream and resumable SSE. All three were removed, and code written against them
looks like it works — a modern server ignores what it no longer understands.

## How it works

### What any transport must do

Two rules bound every binding, custom ones included. "JSON-RPC messages MUST be UTF-8 encoded", and
the directions are fixed: "A binding MUST deliver client-sent requests and notifications to the
server, and server-sent responses and notifications to the client. No other message direction exists:
[…] servers do not initiate JSON-RPC requests and clients do not send JSON-RPC responses."

That second rule is why a server cannot simply ask the user something. Server-to-client interactions
are "embedded as input requests inside an `InputRequiredResult`" under Multi Round-Trip Requests, and
the client retries with its answers ({{topic:mcparch}}).

### stdio

"the client launches the MCP server as a subprocess", reads its stdout and writes its stdin, "one
message per line". Messages "MUST NOT contain embedded newlines", and one rule is absolute:

> "The server MUST NOT write anything to its stdout that is not a valid MCP message."

Logging has one place to go. "The server MAY write UTF-8 strings to stderr for any logging purposes",
and a client "SHOULD NOT assume stderr output indicates error conditions" — stderr is noise, not
failure. All server messages share the one stdout channel: "there are no per-request streams."

Lifecycle is the client's. Shutdown is to close stdin, wait, then force-terminate — "escalates from
SIGTERM to SIGKILL" on POSIX, `TerminateProcess` or Job Objects on Windows — and "Servers SHOULD exit
promptly when their standard input is closed". A crash is cheap: "Because the protocol is stateless,
any in-flight requests are simply lost and the client can retry them against the fresh process."
Cancellation is an explicit `notifications/cancelled`, after which the server "MUST NOT send any
further messages".

Nothing in stdio depends on standard streams "except the process lifecycle", so it "works unchanged
over Unix domain sockets, TCP connections, or any similar channel" — which is why the spec tells
custom transports to reuse this framing rather than invent one.

### Streamable HTTP

One endpoint, one POST per message. "The server MUST provide a single HTTP endpoint path […] that
supports POST", the client "MUST include an `Accept` header listing both `application/json` and
`text/event-stream`", and the body "MUST be a single JSON-RPC request or notification". A
notification gets "HTTP status code 202 Accepted with no body". A request gets either a JSON object
or an SSE stream scoped to that request, and "The client MUST support both."

Three headers are required on every POST, and one of them is checked against the body:

| Header | Carries |
|---|---|
| `MCP-Protocol-Version` | the revision, which "MUST match" `_meta`, or the server returns 400 and a `HeaderMismatch` error |
| `Mcp-Method` | the JSON-RPC method |
| `Mcp-Name` | `params.name` or `params.uri`, on `tools/call`, `resources/read`, `prompts/get` |

On the SSE stream the server "MAY send JSON-RPC notifications — for example,
`notifications/progress` or `notifications/message` — before the final response", those
notifications "MUST relate to the originating client request", and "The final JSON-RPC response
SHOULD terminate the stream." Cancellation needs no message: "Closing the SSE response stream MUST be
treated by the server as cancellation of that request."

### What `2026-07-28` removed

Sessions and the GET stream are gone, and the spec says how to handle traffic that still arrives: an
`Mcp-Session-Id` header — "ignore it, and do not mint or echo session IDs"; a `Last-Event-ID` header
— "ignore it; streams are not resumable". A GET or DELETE should answer `405 Method Not Allowed`.
Long-lived change notifications now ride a `subscriptions/listen` request's own stream.

<!-- volatile verified=2026-11 -->
The status codes worth recognising: **202** a notification accepted, **400** a malformed
notification or a version/header error, **403** an invalid `Origin`, **404** an unknown method
(JSON-RPC `-32601`, whose body "distinguishes this case from a 404 returned by a legacy HTTP+SSE
server"), **405** a GET or DELETE.
<!-- /volatile -->

### Security is a Streamable HTTP section only

"Servers MUST validate the `Origin` header on all incoming connections to prevent DNS rebinding
attacks", answering 403 when it is present and invalid. "When running locally, servers SHOULD bind
only to localhost (127.0.0.1) rather than all network interfaces (0.0.0.0)", and "Servers SHOULD
implement proper authentication for all connections" — without which "attackers could use DNS
rebinding to interact with local MCP servers from remote websites". The scheme itself is
{{topic:mcpauth}}. stdio has no security section: the process boundary is the control.

HTTP+SSE, from `2024-11-05`, is deprecated — "New implementations SHOULD NOT adopt it; existing
implementations SHOULD migrate to Streamable HTTP."

## In practice at Technik

The Teamcenter server is one program with both transports, chosen by a flag. Nothing about the tools
changes between them.

*From [`server/teamcenter.py`, lines 151–163](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/server/teamcenter.py#L151-L163):*

```python
def serve_http():
    """Streamable HTTP for Container Apps: stateless, so any replica can answer any request.

    The Host header must be the app's own name (MCP_ALLOWED_HOSTS), which guards against DNS rebinding.
    """
    port = int(os.environ.get("PORT", "8000"))
    hosts = [h for h in os.environ.get("MCP_ALLOWED_HOSTS", "").split(",") if h]
    mcp.run("streamable-http", host="0.0.0.0", port=port, stateless_http=True, json_response=True,
            transport_security=TransportSecuritySettings(allowed_hosts=hosts + [f"localhost:{port}"]))


if __name__ == "__main__":
    serve_http() if "--http" in sys.argv else mcp.run()
```

Two lines there are the spec's security section in code. `allowed_hosts` exists because the Python
SDK has rebinding protection on by default, and it rejected the Container App's own fully qualified
name until that name was listed — found while building stage 5 ({{topic:stageship}}). And
`host="0.0.0.0"` looks like exactly what the spec says not to do, which is the point: that *SHOULD*
applies "When running locally". Inside a container the platform, not the bind address, is the
boundary.

Locally the same server runs over stdio, started by the editor, and the stdout rule is why its tools
return formatted strings rather than printing them ({{topic:buildmcp}}). The capstone's offline test
spawns it the way VS Code does and drives it through a real client — the cheapest way to prove the
framing works.

<!-- unknown since=2026-11 -->
Which revision VS Code negotiates with this server was never confirmed, because the capstone has
never run live. If the editor opens with an `initialize` handshake, it is a legacy-era client.
<!-- /unknown -->

## Design guidance

- **Default to stdio while you are still designing.** The process boundary is the strongest control
  you will get for free.
- **Never print.** On stdio, one stray line on stdout corrupts the stream; log to stderr.
- **Validate `Origin` before you expose anything**, and list the hostnames you expect.
- **Do not build on sessions, GET streams or `Last-Event-ID`.** They are removed; a modern server
  ignores them silently, so there is no error to find.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The client reports malformed JSON at random | Something wrote to stdout | Move every print and banner to stderr |
| Messages are concatenated or truncated | An embedded newline in a message | One message per line, newlines escaped |
| A deployed server rejects its own URL | DNS rebinding protection, host not listed | Add the hostname to the allowed hosts |
| A reconnecting client loses notifications | Streams are not resumable in this revision | Re-establish the `subscriptions/listen` stream |
| A 404 is read as "wrong URL" | 404 also means unknown method | Read the JSON-RPC body, not the status alone |
| The server keeps running after the client quits | stdin closed, process ignored it | Exit at end-of-file on stdin |

## Key terms

**stdio** — newline-delimited JSON-RPC over a client-launched subprocess's standard streams. stdout
carries only MCP messages; stderr carries logs.

**Streamable HTTP** — one POST per message to a single MCP endpoint, answered by JSON or a
request-scoped SSE stream.

**DNS rebinding** — the attack `Origin` validation and host allow-lists exist to stop: a remote page
resolving a name to a local address, to reach a server that assumed it was private.
