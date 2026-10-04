## TL;DR

Snowflake grants **privileges to roles** and **roles to users**, and every object is owned by one role. An
agent gets a **dedicated, read-only role** of its own: Technik's is `TECHNIK_AGENT_RO`, holding usage of one
warehouse, one database and one schema, and `SELECT` on exactly the objects its tools read, views wherever a
rule lives. Never a person's
role, never an admin role. What the agent can reach is every privilege on every role its user holds, so
keep that user to this one role.

## Why it matters

Whatever a role can read, the agent using it can return to anyone who asks. An agent that queries Snowflake
with an engineer's role reads everything that engineer can read, including what the engineer can *change*.
A quality notification description is free text typed on the shop floor, and text the agent reads can try
to steer the tools it holds ({{topic:injection}}). With a role that can only read a few views, the worst an
injected instruction can do is bounded by Snowflake's grants, not by a sentence in the instructions.

{{topic:devenv}} stated the rule: your development role is yours, and the agent gets a different one. This
lesson is how that role is built.

## How it works

### Two models, combined

Snowflake combines two access-control models:

- **Discretionary**: "Each object has an owner, who can in turn grant access to that object." Owning means
  a role holds the `OWNERSHIP` privilege, and by default it is the role that created the object.
- **Role-based**: "Access privileges are assigned to roles, which are in turn assigned to users."

So nobody grants a privilege to a person directly in practice. You grant it to a role, and grant the role.

### Hierarchies inherit upwards

"Roles can be also granted to other roles, creating a hierarchy of roles. The privileges associated with a
role are inherited by any roles above that role in the hierarchy." Granting the agent's role *to* an
administrator's role lets the administrator test what the agent sees. Granting any other role *to* the
agent's role hands the agent everything that role can do.

### The roles that come with every account

| Role | Snowflake's description |
|---|---|
| `ACCOUNTADMIN` | "Top-level role in the system and should be granted only to a limited/controlled number of users" |
| `SECURITYADMIN` | Can manage any object grant globally, and create, monitor and manage users and roles |
| `USERADMIN` | "Dedicated to user and role management only" |
| `SYSADMIN` | Has privileges to create warehouses and databases (and other objects) |
| `PUBLIC` | "Pseudo-role that is automatically granted to every user and every role" |

Snowflake recommends a hierarchy of custom roles, "with the top-most custom role assigned to the system role
`SYSADMIN`". Note `PUBLIC`: anything granted to it, the agent can read too.

### Which roles are active

A session has a current, **primary** role and can activate **secondary** roles (`USE ROLE`,
`USE SECONDARY ROLES`). Creating objects is authorised by the primary role only, "however, for any other SQL
action, any permission granted to any active primary or secondary role can be used". If no role is named on
connection, the user's default role applies. For an agent that means its reach is the union of every role
its Snowflake user can activate, not just the one in the connection settings.

### What a query needs

Querying a table needs `SELECT` on it plus a privilege on its database and schema, normally `USAGE`. Running
the query needs `USAGE` on a warehouse, which "enables using a virtual warehouse and, as a result,
executing queries on the warehouse", resuming it first if it auto-resumes. `OPERATE` is a separate
privilege, to start, stop or suspend a warehouse, and a reader does not need it.

## In practice at Technik

The assistant's role, built by an administrator using `USERADMIN` and `SECURITYADMIN`:

```sql
CREATE ROLE TECHNIK_AGENT_RO
  COMMENT = 'Read-only role for agents and MCP servers. No person uses it.';

GRANT USAGE ON WAREHOUSE TECHNIK_AGENT_WH TO ROLE TECHNIK_AGENT_RO;
GRANT USAGE ON DATABASE  TECHNIK_DW       TO ROLE TECHNIK_AGENT_RO;
GRANT USAGE ON SCHEMA    TECHNIK_DW.OPS   TO ROLE TECHNIK_AGENT_RO;

GRANT SELECT ON VIEW  TECHNIK_DW.OPS.V_WORK_ORDER_OPERATIONS   TO ROLE TECHNIK_AGENT_RO;
GRANT SELECT ON VIEW  TECHNIK_DW.OPS.V_RELEASED_REVISIONS      TO ROLE TECHNIK_AGENT_RO;
GRANT SELECT ON TABLE TECHNIK_DW.OPS.SAP_QUALITY_NOTIFICATIONS TO ROLE TECHNIK_AGENT_RO;
GRANT SELECT ON TABLE TECHNIK_DW.OPS.TC_DOCUMENTS              TO ROLE TECHNIK_AGENT_RO;

GRANT ROLE TECHNIK_AGENT_RO TO USER TECHNIK_AGENT_SVC;   -- the connector's service user
GRANT ROLE TECHNIK_AGENT_RO TO ROLE SYSADMIN;            -- administrators can see what the agent sees
```

Read it for what is absent. No `INSERT`, `UPDATE` or `DELETE`, so it is read-only by construction. No
`OPERATE` on the warehouse, so the agent cannot resize or stop it. The two views carry rules, deduplication
and *released only*, and `SELECT` on a view "is sufficient to query a view; the SELECT privilege is not
required on the objects from which the view is created", so the operations and revision tables behind them
stay out of reach ({{topic:sfviews}}). Two tables are granted directly because tools read them as they are,
the notifications and the document register, and no rule sits between them and the agent. Every other table
is ungranted. And `TECHNIK_AGENT_SVC` holds this
one role and nothing else, so there is nothing for a secondary role to add ({{topic:sfconnector}}).

Engineers query the same data with their own development role, `TECHNIK_DEV`, which can read the raw tables
because understanding the data means exploring it freely. The two roles never meet: no engineer connects a
tool with `TECHNIK_DEV`, and `TECHNIK_DEV` is never granted to `TECHNIK_AGENT_RO`.

To check what the agent can reach, an administrator activates the role and looks:

```sql
USE ROLE TECHNIK_AGENT_RO;
SHOW GRANTS TO ROLE TECHNIK_AGENT_RO;
```

## Design guidance

- **One agent role, one service user, one role on that user.** The reach is then exactly what is granted.
- **Grant a view wherever a rule lives.** Table access bypasses the view's rules; grant a table only when a
  tool reads it as it is.
- **Grant the agent role upwards, never other roles into it.** Inheritance runs upwards only.
- **Keep `PUBLIC` empty of data grants.** Every role, the agent's included, inherits it.
- **Comment the role** with who uses it and why, so nobody repurposes it for a person.
- **Recheck the grants after every new view**, with the role active.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| An agent's tool returns client names that no view exposes | The tool's connection uses a person's role, which reads the raw tables | Connect with the agent's own role |
| The agent can read a table nobody granted it | A role was granted *to* the agent's role to fix a permission error, and its privileges were inherited | Revoke it; grant the specific view instead |
| Access works in a worksheet but not through the tool | The worksheet used secondary roles the service user does not have | Test with `USE ROLE TECHNIK_AGENT_RO` only |
| "Insufficient privileges" on a view the role was granted | `USAGE` on the database, schema or warehouse is missing | Grant all three |
| A new table is readable by every user and agent | It was granted to `PUBLIC` | Grant to named roles only |

## Key terms

**Role** — a named set of privileges. Granted to users and to other roles.

**Privilege** — permission for one action on one securable object, such as `SELECT` on a view.

**Owner** — the role holding `OWNERSHIP` on an object, by default the role that created it.

**Role hierarchy** — roles granted to roles; privileges are inherited by the roles above.

**Primary and secondary roles** — the session's current role, and the extra roles whose privileges also
apply to everything but `CREATE`.
