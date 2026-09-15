## TL;DR

A connection holds the credentials a connector action runs under. It can run **as the end user**,
with that person's own permissions, or **as the maker or a service account**, with one fixed
identity for everybody. This choice decides what data users can reach through your agent, and it is
the most common reason an agent that worked beautifully in testing breaks — or quietly
over-shares — the moment a second person uses it.

## Why it matters

Two failure modes, and the second is worse.

**The loud one:** you share the agent, a colleague asks a question, and the tool errors or returns
nothing. Annoying, obvious, fixable.

**The quiet one:** you share the agent, a colleague asks a question, and gets an answer built from
data *they are not allowed to see*, because the tool ran as you. Nothing errors. Nobody notices until
an audit does.

Authentication also has a second dimension people conflate with the first: who may *talk to* the
agent at all. An agent can require no sign-in, Microsoft Entra ID sign-in, or manual authentication.
"Who can use it" and "whose permissions do its tools run with" are different questions and need
separate answers.

## How it works

### Who the connection runs as

| Mode | What happens | Use when |
|---|---|---|
| **End user** | Each user supplies their own connection; the action runs with their permissions | Users have differing access and that difference must be respected |
| **Maker / author** | Your connection is used for everyone | Prototyping only. It is almost never what you want in production |
| **Service account** | A dedicated non-personal identity with deliberately scoped permissions | The agent should see exactly one thing, the same for everyone |

The end-user mode is the right default when the source system already enforces the permissions you
care about: SharePoint, Dataverse, Outlook. The answer a person gets is then correct *for them* by
construction.

A service account is right when the agent should see a fixed, deliberately chosen slice — the same
for everybody — and the source system's own permissions are not the control you are relying on. The
Snowflake role in this course is exactly that: one read-only role over one schema.

The maker mode is a trap. It works instantly, which is why people ship it.

<!-- volatile verified=2026-09 -->
Where the choice is made, and how it is worded, differs between the Copilot Studio harnesses and
changes between releases. Follow the linked documentation rather than a remembered screen. What does
not change is the question you are answering: *whose permissions does this call run with?*
<!-- /volatile -->

### Connection references

A connection is a resource in an environment. Move a solution to test or production and its
connections do not travel with it — nor should they, since production should not run on a developer's
credentials.

A **connection reference** is the indirection that makes this work. The flow or agent points at a
named reference; the reference is bound to an actual connection in each environment. Deployment then
means re-binding references rather than editing the agent. B12 does this properly; the rule to adopt
now is simply: **use connection references from the start**, because retrofitting them is far more
work than starting with them.

### Who may talk to the agent

Separately from tool identity, the agent itself has an authentication setting: no authentication,
Entra ID sign-in, or manual. An internal agent over company data should require sign-in — otherwise
"the agent runs as a service account" means *anyone who finds the agent* gets that service account's
view. The two settings only make sense together, and B11 covers the agent-side half.

## In practice at Technik

The Technik Production Assistant reads Snowflake with a **service account** pattern:
`TECHNIK_AGENT_RO`, read-only, on one schema.

Why not end-user authentication, when Snowflake has perfectly good role-based access control? Three
reasons, and the third is the real one:

1. Every user would need their own Snowflake credentials and their own connection in Copilot Studio,
   which is a lot of friction for a read-only lookup.
2. The manufacturing data everyone at Technik may read is the same data. There is no per-user slice
   to respect.
3. **The agent must not be able to write, whoever is asking.** A read-only identity is the one
   guarantee that survives a prompt injection. If the agent held Carla's credentials and Carla can
   update quality notifications, then anything that can talk Carla's agent into a write has Carla's
   write access. With `TECHNIK_AGENT_RO` there is nothing to talk it into.

That third point is worth sitting with, because it inverts the usual intuition. End-user
authentication is *more* faithful to who is asking and *less* safe when the agent's inputs are
untrusted — and a quality notification description is about as untrusted as an input gets. The
Technik data contains notifications that attempt exactly this attack; you will meet them in B11.

The document side of the assistant is the opposite case. SharePoint knowledge (B6) runs with each
user's own permissions, because there the per-user slice is real: not everyone may read every
controlled document. One agent, two identity models, each chosen for its own reason.

> [!WARNING]
> Sharing an agent does not share its connections, and it does not grant its knowledge permissions.
> A colleague who can open your agent may still be unable to use it. Test with a second account
> before you announce anything — it is the only way to find this.

## Design guidance

- **Decide identity before you build the tool**, not when you share the agent.
- **Ask: "if this runs as me, what could someone else see through it?"** If the answer is
  uncomfortable, it is the wrong mode.
- **Default to end-user authentication** where the source system enforces the permissions that matter.
- **Default to a scoped, read-only service account** where the agent should see a fixed slice, or
  where its inputs are untrusted.
- **Never use a personal connection in anything shared.**
- **Use connection references from the first solution.**
- **Test with a second account**, ideally one with fewer permissions than yours.
- **Write down which identity each tool uses.** Future you, debugging an empty result, will be
  grateful.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| "It works for me" and fails for everyone else | Maker connection, or each user needs their own and has not made one | Choose the right mode; document what users must set up |
| A colleague sees data they should not | The tool runs as you | Switch to end-user auth, or scope the service account properly |
| The agent breaks after deployment to another environment | Connections do not move with a solution | Use connection references and re-bind per environment (B12) |
| The agent works, then stops weeks later | Credentials expired or were revoked | Monitor connection health; prefer service accounts with managed credentials |
| An injected instruction caused a write | The agent held an identity that could write | Read-only identity. This is why the course splits the roles |
| Anyone can reach the agent and its service-account data | Agent authentication is set to none | Require Entra ID sign-in (B11) |

## Key terms

**Connection** — stored credentials a connector action runs under.

**End-user authentication** — the action runs with the signed-in user's permissions.

**Service account** — a non-personal identity with deliberately scoped permissions.

**Connection reference** — indirection between a solution and an actual connection, so the same
solution can be bound differently per environment (B12).

**Agent authentication** — whether users must sign in to talk to the agent at all. Separate from
tool identity (B11).

**Least privilege** — granting only the access the job needs. The reason `TECHNIK_AGENT_RO` exists.
