## TL;DR

Authorization in MCP is OAuth 2.1 at the transport level, and for HTTP only: "Implementations using
an STDIO transport **SHOULD NOT** follow this specification, and instead retrieve credentials from
the environment." A protected server is an OAuth **resource server** — it validates tokens, it does
not issue them. The requirement doing the most work is **audience binding**: clients send a
`resource` parameter naming the server, servers "MUST only accept tokens that are valid for use with
their own resources", and a server "MUST NOT pass through the token it received from the MCP client".

## Why it matters

Every other control you have met bounds what a tool may do. This one bounds *whose* authority it acts
with — the question an audit asks first, and the one a shared API key cannot answer
({{topic:connauth}}).

The failure worth fearing is silent. A server that accepts any syntactically valid token will act on
one minted for a different service, and its holder needed no permission from you to get it: "An
attacker can gain unauthorized access or otherwise compromise an MCP server if the server accepts
tokens issued for other resources." Nothing in the request looks wrong; there is no error to find.

The mirror of it is the one your own code is likelier to commit — taking the token a client gave you
and forwarding it to the system behind you. That is forbidden, and {{topic:mcpsec}} names the class
it belongs to.

## How it works

### Who is what

| Role | The spec's words |
|---|---|
| **MCP server** | "acts as an OAuth 2.1 resource server, capable of accepting and responding to protected resource requests using access tokens" |
| **MCP client** | "acts as an OAuth 2.1 client, making protected resource requests on behalf of a resource owner" |
| **Authorization server** | issues the tokens; its "implementation details […] are beyond the scope of this specification" and it "may be hosted with the resource server or a separate entity" |

That division is the lesson. You are not building a login; you are building something that tells a
good token from a bad one.

### How a client finds the authorization server

Discovery runs backwards from a refusal. "MCP servers **MUST** implement OAuth 2.0 Protected Resource
Metadata (RFC 9728)", advertised either in a `WWW-Authenticate` header on a `401 Unauthorized` or at
a well-known URI, and that metadata "**MUST** include the `authorization_servers` field containing at
least one authorization server". Clients support both routes, probing the well-known URIs when there
is no header.

The client then fetches the authorization server's own metadata, which must offer "at least one of"
RFC 8414 Authorization Server Metadata or OpenID Connect Discovery 1.0 — and must check that "the
`issuer` value in the document **MUST** be identical to the issuer identifier used to construct the
well-known URL", or a hostile host can pose as an honest one.

<!-- volatile verified=2026-11 -->
Client registration has three routes and a shifting default. **Client ID Metadata Documents** are
where new work goes — clients and servers "**SHOULD** support" them, and the client ID is an HTTPS URL
hosting the client's own metadata. **Pre-registration** suits parties with an existing relationship.
**Dynamic Client Registration (RFC 7591)** is now "deprecated. New implementations should use Client
ID Metadata Documents instead", retained only for servers lacking the newer mechanism.
<!-- /volatile -->

### The `resource` parameter, and why it is the whole point

"MCP clients **MUST** implement Resource Indicators for OAuth 2.0 as defined in RFC 8707", including
the parameter "in both authorization requests and token requests", carrying "the canonical URI of the
MCP server", and sending it "regardless of whether authorization servers support it". A canonical URI
has a scheme, no fragment and preferably no trailing slash: `https://mcp.example.com/mcp` is valid,
`mcp.example.com` is not.

The server side must not be skipped. It "**MUST** validate access tokens as described in OAuth 2.1
Section 5.2", "**MUST** validate that access tokens were issued specifically for them as the intended
audience", and "**MUST** reject tokens that do not include them in the audience claim". Tokens travel
in `Authorization: Bearer <access-token>` on "every HTTP request", and "Access tokens **MUST NOT** be
included in the URI query string."

### The three status codes, and the one that is a conversation

| Code | Means |
|---|---|
| **401** | "Authorization required or token invalid" — also where the metadata pointer lives |
| **403** | "Invalid scopes or insufficient permissions" |
| **400** | "Malformed authorization request" |

A 403 can be an invitation rather than an ending. On a scope shortfall the server "**SHOULD** respond
with" 403 plus a `WWW-Authenticate` header carrying `error="insufficient_scope"` and the scopes
needed, and the client attempts a step-up flow with "the union of the client's previously requested
scope set and the scopes from the current challenge", under "retry limits". The challenged scopes are
"authoritative for the current operation".

One client obligation is a hard stop when missing: PKCE is mandatory ("**MUST** use the `S256` code
challenge method when technically capable"), and because nothing advertises PKCE support directly, an
absent `code_challenge_methods_supported` means "MCP clients **MUST** refuse to proceed".

> [!WARNING]
> The spec names no vendor anywhere — not Entra ID, not any other identity provider. Which
> authorization server you use is your design decision, and these requirements apply whichever you
> pick.

## In practice at Technik

The capstone is two deployments with two different answers, and the split follows the transport.

**Over stdio there is no OAuth, by the spec's own instruction.** The server takes the environment
route, and every credential arrives that way:

*From [`server/teamcenter.py`, lines 45–56](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/server/teamcenter.py#L45-L56):*

```python
def connect():
    load_dotenv()
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        authenticator="SNOWFLAKE_JWT",
        **private_key(),
        role=os.environ["SNOWFLAKE_ROLE"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ["SNOWFLAKE_SCHEMA"],
    )
```

No value is in the file. The key is a JWT key pair, the identity is `TECHNIK_AGENT_SVC` holding the
read-only `TECHNIK_AGENT_RO` role and nothing else, and the gitignored `.env` is the only place
anything sensitive lives ({{topic:localenv}}, {{topic:sfroles}}).

Notice what that means about trust: on stdio, whoever started the process decided which Snowflake
identity the tools run as. The protocol has no opinion, so the operating system and the role are the
boundary — which is why {{topic:permissions}} matters more here than any header.

**Over HTTP, stage 5 adds the identity layer outside the code.** The server runs on Container Apps
behind Entra built-in authentication with a required `Teamcenter.Read` app role, and the agent reaches
it through a Foundry connection authenticating as its own Entra Agent ID. Entra is Technik's choice,
not the spec's instruction, and the platform validates the token — so the server code holds no OAuth
at all ({{topic:stageship}}).

<!-- unknown since=2026-11 -->
Two things about that arrangement were never confirmed, because the capstone has never run live:
which identity a hosted agent presents (the documentation disagrees with itself on whether it is per
agent or shared per project), and whether built-in authentication plus a required app role suffices
where the Container Apps documentation says a "custom authentication implementation" is needed.
<!-- /unknown -->

## Design guidance

- **Match the mechanism to the transport.** stdio takes credentials from the environment; HTTP takes
  OAuth. Mixing them gets the weaknesses of both.
- **Validate the audience, every time.** It is the one check that stops a token meant for someone
  else.
- **Never forward the client's token.** Get your own for the system behind you.
- **Advertise the metadata pointer on your 401.** A client that cannot discover you cannot
  authenticate to you.
- **Send `resource` even when it seems ignored**, so the binding works as soon as it is supported.
- **Challenge with the scopes you actually need**, so a step-up has something to aim at.
- **Keep tokens out of URLs.** A query string is a stored secret.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A token from another service works | No audience validation | Reject tokens that do not name you |
| Clients cannot find your authorization server | No metadata pointer and no well-known URI | Implement RFC 9728 both ways |
| A client refuses before it begins | `code_challenge_methods_supported` missing | PKCE support must be advertised |
| Permanent 403 on one tool | A scope shortfall read as a refusal | Return `insufficient_scope` and the scopes needed |
| The upstream system logs the wrong identity | The client's token was passed through | Exchange it for your own |

## Key terms

**Resource server** — the role your MCP server plays: it validates tokens and serves protected
requests, never issuing tokens.

**Audience binding** — tying a token to the one resource it may be used at, via RFC 8707's `resource`
parameter and the server's audience check.

**Token passthrough** — forwarding a client's token to an upstream API. Forbidden; get a separate
token instead.
