## TL;DR

Read MCP's own security guidance expecting attacks on the model and you will be surprised: almost all
of it is about **plumbing**. Of the six classes it details, five target discovery, consent, handles or
the host machine, and only one — **tool poisoning** — speaks to the model, which you have already met
as indirect prompt injection ({{topic:ctxsecurity}}). The new surfaces are the ones a server author
creates without noticing: the URLs a client fetches on your word, the consent screen a proxy skips,
the identifiers you hand out and expect back, and the command line that starts a local server.

## Why it matters

Two sources, two different jobs. Microsoft's guidance is about content reaching the model, and its
mitigations — Prompt Shields, Spotlighting, supply-chain review — are the probabilistic ones
{{topic:ctxsecurity}} already graded. The specification's security document reads like an
OAuth threat model, because that is what it is.

The gap between them is the lesson. A server can be perfectly defended against injected text and
still be the weakest thing in the system: its attack surface is authorization and process launch. {{module:security-advanced}} threat-models the whole agent; here the question is narrower —
what did writing a server add to the attack surface?

## How it works

### Tool poisoning, and the rug pull

The one model-facing class. "Tool Poisoning is a vulnerability where an attacker embeds malicious
instructions within the descriptions of MCP tools", and it works through an asymmetry:
"Malicious instructions in tool metadata are invisible to users but can be interpreted by the AI
model and its underlying systems."

The dangerous variant is not the first upload but the second: "This is particularly dangerous in
hosted MCP server scenarios, where tool definitions can be dynamically amended to include malicious
content later (called a 'rug pull' by some researchers). A user that previously approved a tool for
use with their LLM may end up with a tool that changed since their approval happened." That is
exactly the propagation {{topic:mcpcs}} described as a feature. The mitigation is not a filter; it is
the review gate on your own repository ({{topic:cicd}}).

### Confused deputy

The attack the roadmap names, and it needs four conditions together: a proxy server using a **static
client ID** with a third-party authorization server, dynamic client registration for its own clients,
a consent cookie set by that third party, and no per-client consent of its own. An attacker
registers, crafts a link with their own `redirect_uri`, the third party sees the cookie and "skips the
consent screen", and the code lands on the attacker's server.

Two requirements follow. Proxy servers "MUST implement per-client consent", keyed on `client_id`
rather than on "user has consented". And the state value must be stored only *after* approval: "The
consent cookie or session containing the state value MUST NOT be set until after the user has
approved the consent screen", because setting it earlier "renders the consent screen ineffective".

### State handle hijacking

This class exists because `2026-07-28` removed protocol sessions ({{topic:transports}}). "MCP is
stateless and has no protocol-level sessions. Servers that need state spanning multiple requests mint
an explicit handle … and receive it back as an ordinary tool argument on each request." Which makes
the handle a credential by accident. The rules are blunt: servers "MUST NOT treat possession of a
state handle as authentication", handles should be non-deterministic and expiring, and state should
be keyed server-side as `<user_id>:<handle>` "where the user ID is derived from the verified token
rather than supplied by the client".

### SSRF through discovery

A client fetches several URLs purely because a server said so: the `resource_metadata` URL from
`WWW-Authenticate`, the `authorization_servers` URLs, then the endpoints in the authorization
server's metadata. A malicious server points those at `http://169.254.169.254/` — the cloud metadata
endpoint, where "IAM credentials, API keys, and other secrets" live — or at a domain that resolves
safely during validation and internally during the request. The mitigations are HTTPS-only, blocked
private ranges, validated redirect targets and egress proxies, with one line worth taking literally: "Avoid implementing IP validation manually. Attackers exploit
encoding tricks (octal, hex, IPv4-mapped IPv6) that custom parsers often miss." The same risk reaches
authorization servers, which fetch a client's metadata document from a URL an unknown client supplied.

### The local server, and the command that starts it

A local server "may have direct access to the user's system", and the attack does not need the server
to be malicious — a malicious *startup command* in a client configuration is enough, which makes
{{topic:mcpvscode}}'s question of which file holds that command a security question. Clients
supporting one-click configuration "MUST" show "the exact command that will be executed, without
truncation" and warn "that MCP servers run with the same privileges as the client". Your side of it is
short: "Use the stdio transport to limit access to just the MCP client", and if you must serve HTTP
locally, require a token or use a restricted IPC mechanism.

### Scopes, and the thing nobody documents

Scope minimization is the specification's answer to over-broad authority: a minimal initial set, then
elevation through `WWW-Authenticate` challenges carrying only the scopes needed. Its common-mistakes
list is a usable review checklist — publishing every scope in `scopes_supported`, "bundling unrelated
privileges to preempt future prompts", and "treating claimed scopes in token as sufficient without
server-side authorization logic".

<!-- unknown since=2026-11 -->
Note what that is *not*. "Over-broad tools" is an MCP risk every practitioner repeats, but neither
source addresses tool granularity — one discusses OAuth scopes, the other content. {{topic:buildmcp}}
found the build tutorial equally silent. So the rule that a tool should do one thing, over one view,
with validated arguments is this course's position, not a documented requirement.
<!-- /unknown -->

## In practice at Technik

Grading the capstone against the six classes is quick.

Four do not apply, by construction. There is no proxy and no OAuth code of its own, so confused
deputy has nowhere to happen; the deployed server is validated by the platform
({{topic:stageship}}). It is a server, not a client, so it fetches no discovery URLs. It mints no
handles — the three tools take document numbers, work orders and operation sequences, all re-checked
against `TECHNIK_AGENT_RO`'s views on every call. Locally it runs over stdio, the recommended
containment.

Two apply. The local-server class applies to anyone who clones the repository, because the launch
command sits in a committed configuration file, and that file is reviewable precisely because it is
committed. And tool poisoning applies to the project itself: the three docstrings are instructions
that reach a model, and nothing checks them after deployment except the pull request that changed
them. The capstone's defence against a rug pull is code review and a frozen tag, not a runtime
control ({{topic:gitintegration}}).

## Design guidance

- **Treat your tool descriptions as privileged text.** They are instructions to a model, reviewed
  like code or not reviewed at all.
- **Never let a handle authenticate.** Bind it to the identity in the verified token.
- **Validate every URL you fetch**, with a library rather than a regular expression.
- **Consent per client, and store state only after consent.** Either half missing defeats the screen.
- **Challenge with the scopes the operation needs**, not the catalogue.
- **Keep local servers on stdio**, and keep the launch command somewhere a reviewer reads.
- **Assume the next change is the attack.** Rug pulls arrive through your release path.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| An approved tool now does something else | Tool definitions amended after approval | Review description changes; pin what you consume |
| Authorization codes reaching a stranger | Static client ID plus no per-client consent | Per-client consent before the upstream flow |
| One user reading another's state | A handle treated as authentication | Key state by verified user ID and reject mismatches |
| A client leaking cloud credentials | Discovery URLs fetched without validation | Block private ranges; use an egress proxy |
| A clone running arbitrary commands | A malicious startup command in configuration | Show commands in full; review the config file |
| Every token carrying every permission | All scopes published and requested up front | Minimal baseline plus step-up challenges |

## Key terms

**Tool poisoning** — malicious instructions embedded in tool metadata, invisible to users and read by
the model. A rug pull is the version delivered by a later update.

**Confused deputy** — an attack where a proxy server's static upstream client ID plus a reusable
consent cookie lets an attacker obtain authorization codes without consent.

**State handle** — an identifier a stateless server mints for multi-request state. It is a reference,
never a credential.
