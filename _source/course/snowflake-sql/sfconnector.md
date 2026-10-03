## TL;DR

The Snowflake connector is a premium Power Platform connector with three actions: submit a SQL
statement, check its status and get the results, and cancel it. It authenticates through a **Microsoft
Entra ID application** in one of two ways. **Service principal** connects everyone as one Snowflake user,
with a role named in the connection. **Delegated** maps each person's Entra sign-in to their own Snowflake
user. Choose before you build. The choice decides who needs a Snowflake account, what the agent can reach
and which security setup Snowflake needs.

## Why it matters

Everything in this module so far produces SQL. This is where that SQL meets the agent, and where the
question {{topic:connauth}} asked becomes concrete: *as whom does it run?*

The answer is not a toggle you set in Copilot Studio after the tool works. Each connection type needs its
own app registration permissions in Entra ID and its own security integration in Snowflake, and an admin
on each side. A team that builds with a personal connection and asks about authentication at sharing time
has to start that setup over, with users waiting.

## How it works

### The actions

| Action | Does |
|---|---|
| **Submit SQL Statement for Execution** | Runs one statement and returns its rows, or a statement handle when *Asynchronous* is set |
| **Check the Status and Get Results** | Takes a statement handle and returns the rows once the statement has finished |
| **Cancel the Execution of a Statement** | Stops a running statement |

The submit action accepts one statement: "batches of statements not yet supported". It also accepts
`role`, `warehouse`, `database` and `schema` inputs. In a tool, set these as fixed inputs, never
model-filled ({{topic:addconnector}}). The connection should be the only place they are chosen.

<!-- volatile verified=2026-10 -->
Rows come back in a `Data` array, with a `Schema` array describing the columns and their types. Setting
*Nullable* to false replaces nulls with a string. The deprecated connector's separate step for converting
rows to objects is now part of *Check the Status and Get Results*.
<!-- /volatile -->

### The two connection types

| | Service principal | Service principal Delegated Auth |
|---|---|---|
| Who Snowflake sees | One Snowflake user, mapped from the app's token (the `sub` claim) | Each person, mapped from their sign-in (the `upn` claim) to a Snowflake `login_name` or email |
| Role | Named in the connection, granted to that user | The person's own |
| Who needs a Snowflake account | Nobody but the service user | Every user |
| Connection details | Tenant, client ID and secret, resource URL, Snowflake URL, database, warehouse, role, schema | Client ID and secret, resource URL |
| Microsoft documents it as | Shareable | Shareable |

A third option, *Default*, is deprecated, "only provided for backward compatibility", and not shareable.
Do not build on it.

Both types need the same groundwork, which the connector reference walks through step by step. In Entra
ID you create two app registrations, an OAuth resource and an OAuth client, with a client secret. In
Snowflake you create an `external_oauth` security integration whose user-mapping claim matches the
connection type. Two warnings from that walkthrough matter for an agent. Avoid "high-privilege roles like
`ACCOUNTADMIN`, `SECURITYADMIN` or `ORGADMIN`". And check that the role is not on the integration's
blocked list, or every call fails.

### In Copilot Studio

On the standard harness, a connector tool uses **the user's credentials by default**. Each user is asked to
sign in to the connection the first time the tool runs. The alternative is **Maker-provided credentials**,
set on the tool's overview page, which is allowed only once the agent uses an authenticated channel.

<!-- unknown since=2026-10 -->
Where the GitHub Copilot harness sets which credentials a connector tool uses. The *Use connectors* page
is written for the standard harness.
<!-- /unknown -->

Combine the two layers and the design is clear:

| Connection type | Tool credentials | Result |
|---|---|---|
| Service principal | Maker-provided | Every user reads as the service user's role. One budget, one audit identity |
| Delegated | User's (default) | Every user reads as themselves; each needs a Snowflake user and a connection |
| Delegated | Maker-provided | Every user reads as **the maker**. The case to avoid |

### Limits that a shared agent meets

- **900 API calls per connection per 60 seconds**, and **50 requests** processed concurrently. With one
  shared connection, every user of the agent draws on the same budget.
- **Duplicate column names from a join are not supported.** The workaround Microsoft gives is aliases. A
  view with unique business names avoids the problem ({{topic:sfviews}}).
- **Letter case must match.** Warehouse, role, database and schema must be entered "in the same letter
  case as the Snowflake account".

## In practice at Technik

The Production Assistant's Snowflake tools run on a **service principal** connection:

| Setting | Value |
|---|---|
| Entra app (client) | *Technik Snowflake Agent Client*, single tenant |
| Snowflake user | `TECHNIK_AGENT_SVC`, `login_name` set to the app's `sub` value |
| Role | `TECHNIK_AGENT_RO`, read-only |
| Warehouse, database, schema | `TECHNIK_AGENT_WH`, `TECHNIK_DW`, `OPS` |

The reasons are the ones {{topic:connauth}} gave. Most of the assistant's users have no Snowflake account,
there is no per-user slice of manufacturing data to respect, and a read-only identity is the guarantee
that survives a prompt injection. Delegated authentication fails the first test before the others matter.
A planner without a Snowflake user would get an error, not an answer.

The same connector serves {{topic:snowflakeknowledge}} differently. As knowledge, it always runs as the
asking user, so Technik's design keeps work-order data in tools. One connector, two identities, each chosen
for its job.

Four planning questions settled the design before anyone built a tool:

1. **Who must have a Snowflake user?** Only `TECHNIK_AGENT_SVC`.
2. **What can that role read?** The views the tools query, and nothing writable.
3. **Who owns the client secret, and when does it expire?** The connector walkthrough suggests
   long-lived secrets only "for testing purposes". An expired secret stops every Snowflake tool at once,
   for every user, so its expiry date is in the team's calendar with a named owner.
4. **Is the budget enough?** Forty users asking a few questions an hour is far below 900 calls a minute.
   An evaluation run of 25 cases is a burst worth watching, since a tool may need two calls per question.

## Design guidance

- **Decide the connection type first**, then ask both admins for the setup it needs.
- **Prefer a service principal with a read-only role** for an agent shared with many users.
- **Use delegated only where per-user access is the requirement**, and every user has a Snowflake user.
- **Never pair delegated auth with maker-provided credentials.**
- **Fix role, warehouse, database and schema** in the connection and the tool.
- **Give the secret an owner and an expiry reminder.**
- **Point tools at views**, which also avoids duplicate column names.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Every Snowflake tool fails at once, weeks after launch | The client secret expired | Rotate it; track expiry with a named owner |
| A user gets an authentication error the maker never saw | Delegated auth, and that user has no Snowflake user with a matching `login_name` or email | Create and map the user, or use a service principal |
| The connection fails although the role exists | The role is on the security integration's blocked list, or its letter case differs | Use a dedicated low-privilege role; match the case exactly |
| An error on a query that joins two tables | Duplicate column names in the result | Alias the columns, or query a view |
| Answers slow down or fail at busy times | One shared connection hit its throttling limit | Reduce calls per question; check usage against 900 a minute |
| Users read data with the maker's access | Maker-provided credentials on a delegated connection | Switch to a service principal connection |

## Key terms

**Service principal** — an Entra ID application's own identity, mapped to one Snowflake user.

**Delegated authentication** — the connection acts as the signed-in person, mapped to their Snowflake user.

**Security integration** — the Snowflake object that trusts Entra ID tokens and maps them to users.

**Maker-provided credentials** — a Copilot Studio tool setting that makes every user's call use the maker's
connection.

**Statement handle** — the identifier of a submitted statement, used to fetch its results or cancel it.
