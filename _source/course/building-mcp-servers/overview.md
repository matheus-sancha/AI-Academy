## What this module is for

You have added someone else's MCP server to an agent. Here you build, secure and ship your own — and
discover how little the protocol does for you.

One sentence runs through all nine lessons. **MCP gives you almost nothing to hold on to.** Since the
`2026-07-28` revision it is stateless, so your server "infer[s] nothing from previous requests". There
is no versioning, no error model, no guidance on how large a result may be and no opinion about which
identity a tool runs as. The *transport* — not the data layer — decides who can reach you and what a
restart costs. And once you hand the server to a platform, you lose more: on Copilot Studio your
edits ship themselves with no release step, and on Snowflake the server stops being code at all.

So the things you genuinely control are few, and they are the ones worth designing carefully: **how
narrow a tool is, what its docstring promises, which identity executes it, and what your release path
lets through.**

The second thing to expect is disagreement. Every surface answers the same question differently.
Snowflake supports protocol revision `2025-11-25`; the specification is on `2026-07-28`. The spec
deprecates dynamic client registration; Copilot Studio's easiest OAuth option requires it; Microsoft's
certification programme refuses it, and refuses PKCE too, which the spec says a capable client
**MUST** use. Seven of the nine lessons here carry an `unknown` block for the same reason: knowing which
documentation to disbelieve is part of working at this level.

## Before you start

You need the consuming side: {{topic:mcp}} for what the protocol is for, and {{topic:mcpadd}} for
what adding a server to a Copilot Studio agent looks like from the other chair — this module does not
restate either, and one lesson is entirely about what that convenience costs the server's author.
{{topic:tools}} and {{topic:tooldesc}} hold the rule the whole module rests on, that a description is
an interface rather than a label. {{topic:connectors}}, {{topic:connauth}} and {{topic:dlp}} matter
more than they look: on Copilot Studio an MCP server *is* a connector, so connector authentication and
connector policy are the server's own.

From this level, {{topic:localenv}} and {{topic:vscode}} set up the repository the examples assume,
{{topic:agentmode}} explains which process actually reads a server's configuration,
{{topic:toolshaping}} and {{topic:budget}} are the arithmetic behind every result-size decision here,
and {{topic:ctxsecurity}} already covered indirect prompt injection — so the security lesson deals
only with what writing a server *adds*. Snowflake readers want {{topic:sfroles}}.

Nothing here needs to be run, though adding a server to VS Code and watching it answer is twenty
minutes well spent. The capstone repository is public and tested offline only
({{module:capstone-build}}).

Allow about three hours.

## What you will be able to do

By the end of this module you should be able to:

- name the three participants, place tools, resources and prompts correctly, and say what a stateless
  protocol does instead of a handshake;
- choose between stdio and streamable HTTP from what the deployment needs, not from what a tutorial
  used;
- say what `2026-07-28` removed, and why code written against an older article fails silently;
- add a server to VS Code in the location that reaches every surface, and say which locations are
  compatibility paths;
- write a tool whose docstring and type hints are the whole interface, and whose errors a model can
  act on;
- explain audience binding, and why forwarding a client's token is forbidden;
- hand a server to Copilot Studio, and name the three things that stop being yours when you do;
- decide between writing a server and declaring one in Snowflake, by asking whose role the tools run
  as;
- grade a server against MCP's six attack classes, and say which of them your design makes
  impossible;
- say who may be certified, and why certification is not evidence of protocol conformance.

## The thread through this module

Outward from the protocol: what it is, how it travels, where you test it, how you write it, who it
runs as, then the three places it goes to live, and what can go wrong in all of them.

{{topic:mcparch}} draws the participants and finds the handshake gone. {{topic:transports}} shows that
the transport is the real design decision, and lists what the current revision removed.
{{topic:mcpvscode}} puts a server in front of a client you can watch, and finds the configuration file
everyone recommends is now a compatibility path. {{topic:buildmcp}} writes one, where the docstring is
the contract and the tutorial documents no error mechanism at all. {{topic:mcpauth}} answers *whose
authority*, and lands on audience binding.

Then three destinations, each taking something away. {{topic:mcpcs}} hands the server to Copilot
Studio, where a tenant's data policy can make a working server unreachable. {{topic:sfmcp}} skips the
code entirely and finds the identity model changed underneath. {{topic:mcpsec}} grades the result, and
notices that nearly every MCP-specific attack targets the plumbing rather than the model.
{{topic:mcpcert}} closes with the badge, and the reasons you probably cannot have it.

## Self-check

<details>
<summary>1. A colleague wants the server to remember which work order the conversation is about, so later calls need fewer arguments. What do you tell them?</summary>

That the protocol will not help. Since `2026-07-28` MCP is stateless: there is no handshake and no
protocol-level session, and the server "infer[s] nothing from previous requests". If state genuinely
has to span requests, you mint an explicit handle and receive it back "as an ordinary tool argument".

Then the warning that matters. A handle is a reference, not a credential — servers "MUST NOT treat
possession of a state handle as authentication". Make it non-deterministic, expire it, and bind it
server-side to the user in the verified token, keyed as `<user_id>:<handle>`, or you have built
state-handle hijacking on purpose. In most cases the better answer is no handle at all: let the caller
name the work order each time and re-check it against the view ({{topic:mcparch}}, {{topic:mcpsec}}).
</details>

<details>
<summary>2. Your stdio server works in VS Code. A colleague wants it in a Copilot Studio agent next week. What has to change, and what is out of your hands?</summary>

Three things have to change. The transport: "Copilot Studio supports the Streamable transport type"
and dropped SSE after August 2025, so a local stdio process is not a candidate — it needs a reachable
HTTPS endpoint. The authentication story: the wizard offers none, an API key the *user* supplies, or
OAuth 2.0, and a server designed around one trusted machine identity fits none of them neatly. And
the descriptions: a new server-level sentence decides whether the orchestrator routes to you at all,
and it lives in Copilot Studio rather than your repository.

What is out of your hands is governance. MCP reaches tools through a Power Platform connector, so
"Blocking Power Platform connectors also blocks access to tools in connected MCP servers." A
connector landing in the default **Non-business** group in an organization that blocks that group
gives you a server that works perfectly and that nobody can use ({{topic:mcpcs}},
{{topic:transports}}).
</details>

<details>
<summary>3. Technik's data is already in Snowflake. Why write an MCP server at all, rather than declaring a Snowflake-managed one?</summary>

Because the two answer *who is asking* differently, and that is a governance decision rather than a
preference. A managed server authenticates over OAuth and "the OAuth session uses the connecting
user's `DEFAULT_ROLE` as the primary role" — so tools run as each engineer. Technik's own server runs
as one service user holding one read-only role, which a browser OAuth flow cannot represent at all.
Exposing `SYSTEM_EXECUTE_SQL` would also hand the model arbitrary SQL under that role, where three
narrow tools hand it three statements it cannot rewrite.

But the honest answer is *both*. A managed server does the half Technik's cannot: Cortex Search over
the controlled documents and Cortex Analyst over the semantic model. Two servers, two roles, two
audiences ({{topic:sfmcp}}, {{topic:connauth}}).
</details>

<details>
<summary>4. A pull request rewords two tool docstrings. The reviewer says it is a documentation change and approves it. What is wrong with that?</summary>

A docstring is not documentation; it is an instruction that reaches a model, and it is the one piece
of your server that users never see. That asymmetry is the whole of tool poisoning: "Malicious
instructions in tool metadata are invisible to users but can be interpreted by the AI model and its
underlying systems."

The second problem is the delivery mechanism. On a hosted server, "tool definitions can be
dynamically amended to include malicious content later" — a rug pull — and "A user that previously
approved a tool for use with their LLM may end up with a tool that changed since their approval
happened." Copilot Studio's automatic propagation is exactly that path, used benignly. Which means
your review gate is the only control between a reworded docstring and every agent holding the server,
and it has to be a code review ({{topic:mcpsec}}, {{topic:mcpcs}}).
</details>

<details>
<summary>5. A manager proposes getting the internal server Microsoft-certified, so administrators will trust it. Two reasons that won't work?</summary>

Eligibility, first. Certification is for verified publishers: a business-verified Partner Center
account, enrolment in the Microsoft 365 and Copilot program, and ownership of the submitted endpoint.
"If you're an independent publisher who doesn't own the underlying service, you're not eligible to
submit directly." An internal server for one company's own agents is not a candidate, and the badge
is a listing gate rather than a quality measure.

Second, it would not mean what they think. The programme's own FAQ says DCR "isn't supported today"
and neither is PKCE — which the specification says a capable client **MUST** use, refusing to proceed
when support is unadvertised. So certification is not evidence of protocol conformance. What is worth
taking is the review itself: automated structural validation, then a human pass over authentication,
telemetry and responsible-AI behaviour, run as your own gate ({{topic:mcpcert}}, {{topic:mcpauth}}).
</details>
