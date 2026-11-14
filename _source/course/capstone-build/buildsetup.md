## TL;DR

Five things must exist before stage 1: a Python toolchain, a repository you can push to, a Snowflake account
seeded from the capstone's script, an Azure subscription with a Foundry project, and a client that can talk to
an MCP server. One script, `setup/check.py`, proves the Snowflake half by connecting as the agent's own
identity and printing `PASS` or `FAIL` per grant. Run it until every line passes, because every later stage
assumes it did. The capstone's code is tested offline only. Your run of it is the first live one, so this page
also lists what nobody has been able to confirm for you.

## Why it matters

Stages 2 and 3 read Snowflake through a service user with one read-only role. If a grant is missing, nothing
stops you reaching stage 3. Stage 3 is where an agent in front of a tool turns the failure into a sentence,
and a sentence like *I couldn't find that* does not mention a grant.

<!-- unknown since=2026-11 -->
What the server returns for an object its role cannot read has not been checked, so the exact symptom is
unknown. The reason to run the check is that you never have to find out.
<!-- /unknown -->

The second reason is the data. The capstone seeds the scenario's model with its five deliberate flaws, and one
of them, duplicate partial confirmations on a work order operation, is repaired inside a view
({{topic:sfviews}}). An agent that read the tables behind the view would compute a different efficiency from
the same rows. So the check also proves what the role cannot read.

## How it works

### What you need

| You need | First used | You have it when |
|---|---|---|
| Python 3.12 and `uv` | Stage 1 | `uv --version` prints a version, and the repository pins `3.12` ({{topic:localenv}}) |
| `git` and a GitHub repository you can push to | Stage 1 | Your own repository exists. The capstone is a reference you clone beside it |
| A Snowflake account, with an admin who can use `SYSADMIN` and `SECURITYADMIN` and holds a programmatic access token | This page | The seed script runs to its last line. A trial account works |
| An Azure subscription, a Foundry project and a model deployment that supports function calling | Stage 3 | `az login` succeeds and the deployment is in the project. The default is `gpt-4.1-mini` |
| The Azure CLI, the Azure Developer CLI 1.32 or later, and Docker | Stage 5 only | Skip them until then |
| VS Code with agent mode | Stage 2 | {{topic:agentmode}} |

### Seed and check

Clone the capstone as a reference, because the seed script lives there and you never edit it. *From [`README.md`, lines 35–37](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/README.md#L35-L37):*

```powershell
git clone https://github.com/matheus-sancha/technik-capstone
cd technik-capstone
Copy-Item .env.example .env
```

Fill in `.env` with your account identifier, the admin user, its token and a warehouse the admin can use. Both
`.env` and `keys/` are gitignored, and nothing in this course asks you to commit either. Then run the two scripts,
from the repository root, in this order:

```powershell
uv run seed/seed.py
uv run setup/check.py
```

The seed creates `TECHNIK_DW.OPS`, loads 13 tables, creates the three views, and creates the warehouse, the role
and the service user. On its first run it writes the service user's private key to `keys/technik_agent_svc.p8`.
Running it again replaces the data and keeps the role, the user and the key.

### What the check proves

*From [`setup/check.py`, lines 14–16](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/setup/check.py#L14-L16):*

```python
GRANTED = ["V_WORK_ORDER_OPERATIONS", "V_RELEASED_REVISIONS", "V_OPERATION_DOCUMENTS",
           "SAP_QUALITY_NOTIFICATIONS", "TC_DOCUMENTS"]
NOT_GRANTED = ["SAP_WO_OPERATIONS", "TC_DRAWINGS"]  # behind the views: the agent must not read them
```

Two lists are the whole design. The role reads five objects, and the check reads each one and demands rows. It
also tries two objects behind the views and demands a refusal. A check that only proves the agent can read would
pass a role granted too much. The agent's identity is the capstone's security boundary, so the ceiling is tested
as hard as the floor ({{topic:sfroles}}).

*From [`setup/check.py`, lines 52–61](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/setup/check.py#L52-L61):*

```python
def check_data(cur):
    """One known answer through the view: welding at Plant 1 in September, duplicates removed."""
    pct = cur.execute("""
        SELECT ROUND(SUM(ROUTING_HOURS) / SUM(ACTUAL_HOURS) * 100, 1)
        FROM V_WORK_ORDER_OPERATIONS
        WHERE PLANT = 'Plant 1' AND OPERATION = 'Welding' AND OPERATION_STATUS = 'Confirmed'
          AND CONFIRMED_AT >= '2026-09-01' AND CONFIRMED_AT < '2026-10-01'""").fetchone()[0]
    ok = float(pct) == 88.9
    print(f"{'PASS' if ok else 'FAIL'}  welding efficiency at Plant 1 in September is {pct}% (expected 88.9%)")
    return not ok
```

The last check asks one question with one known answer. If it fails, the rows or the view are not the ones the
rest of the course quotes, and every later figure will disagree with you.

### What no one has run for you

The code passes its tests with fakes standing in for Snowflake and the model. The processes really start, but
nobody has run the capstone against a live account. These are the points the lessons marked as unchecked, in the
order you will meet them:

| Check on your first run | Stage | Where it was raised |
|---|---|---|
| Which protocol version VS Code negotiates with the v2 server, and where a launch command with its own directory flag runs | 2 | {{topic:agentmode}} |
| Which source `DefaultAzureCredential` settles on inside the hosted agent | 5 | {{topic:maf}} |
| Which identity the server actually sees from the toolbox | 5 | {{topic:foundryagents}} |
| Whether a trace shows anything of what happened inside the server | 5 | {{topic:tracing}} |

When one of them goes differently, believe your run and not the page.

## In practice at Technik

You finish this page holding four things. A `.env` with the admin settings and the agent's identity. A key file at
`keys/technik_agent_svc.p8`, written once. A Snowflake account where `TECHNIK_AGENT_SVC` holds only
`TECHNIK_AGENT_RO`. And a check whose last line says `Ready for stage 1.`, which is also the exit code: the script
exits 1 and counts the failures when any line fails.

The admin token is used by the seed and nothing else. From here on every call to Snowflake runs as the service
user, the same identity the server will use, so nothing you do in stages 2 to 4 can read more than the agent
can. That is deliberate. You will not be able to excuse a lookup that works for you and fails for the agent.

## Design guidance

- **Run the check from the repository root.** The key path in `.env` is relative to where you run it.
- **Treat the check as part of the setup.** Re-run it after anyone touches the role.
- **Keep the admin token and the agent's key apart.** The token seeds, the key serves.
- **Test the ceiling as well as the floor.** A role that reads too much passes every positive check.
- **Do not fix a failure by granting more.** Fix the seed or the `.env`, and leave the role as the script made it.
- **Write down what differs on your first run.** Stage 5 will thank you.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `FAIL  cannot read V_RELEASED_REVISIONS` | The seed stopped before the access script, or ran under the wrong role | Run `uv run seed/seed.py` again. It keeps the role and key |
| `FAIL  can read SAP_WO_OPERATIONS` | Someone granted the role a table behind a view | Revoke it. The agent reads views and two tables, nothing else |
| The connection fails before any `PASS` | The key file path is wrong, or you ran from another folder | Run from the repository root and match `SNOWFLAKE_PRIVATE_KEY_FILE` |
| The welding figure is not 88.9% | Rows were edited, or a load stopped partway | Re-run the seed. It replaces the data |
| `FAIL  connected as … with role …` names another role | `SNOWFLAKE_ROLE` in `.env` is not `TECHNIK_AGENT_RO` | Correct `.env`. The service user's default is that role |
| A step in stage 5 fails and nothing earlier did | You skipped the Azure tools until then | Install them before you start stage 5 |

## Key terms

**Seed**: the script that builds `TECHNIK_DW.OPS` and its identity in your own account.

**Service user**: a Snowflake user of `TYPE = SERVICE`, for an application rather than a person, signing in with a key.

**Programmatic access token**: the admin's credential for the seed. It is never the agent's.

**Ceiling check**: a test that an identity cannot read what it should not.
