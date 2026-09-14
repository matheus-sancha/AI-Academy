# Snowflake lab environment

Everything the labs read lives in one Snowflake database, `AI_ACADEMY`, holding
fictional data about Technik (see [`_source/course/scenario.md`](../../../_source/course/scenario.md)).

```
AI_ACADEMY
  SEED             golden copy of the data, read-only, never edited by learners
  SHARED           RESET_TO() and future helper procedures
  SANDBOX_<tag>    one schema per learner, rebuilt from SEED on demand
```

## Run order

| Script | Who runs it | When |
|---|---|---|
| `00_account_setup.sql` | admin, as `ACCOUNTADMIN` | once per account |
| `01_seed_tables.sql` | admin, as `ACADEMY_ADMIN` | once, and after any DDL change |
| `02_seed_sap.sql` | admin | with `01` |
| `03_seed_teamcenter.sql` | admin | with `01` |
| `04_seed_quality_fat.sql` | admin | with `01` |
| `05_seed_metadata.sql` | admin | **always last of the seed scripts** — it reads the catalogue |
| `06_reset_procedure.sql` | admin | once, and after any change to the reset logic |
| `10_provision_learner.sql` | admin, as `ACCOUNTADMIN` | once per learner (edit the two values at the top) |
| `20_learner_start_here.sql` | the learner | once, before their first lab |

Re-running `01`–`05` rebuilds the seed from scratch; it is safe at any time and
does not touch learner sandboxes until each learner next calls `RESET_TO`.

## The two roles

This split is a teaching device as much as a safety measure, and the roadmap
`devenv` topic describes it:

- **`ACADEMY_LEARNER_<tag>`** owns `SANDBOX_<tag>` and drives an XSMALL
  warehouse capped by a monthly resource monitor. Learners use it in worksheets.
- **`ACADEMY_AGENT_<tag>`** is read-only on the same schema, with no create
  rights. Every connector, agent and MCP server in the course signs in with
  this role and nothing else, so "the agent cannot change the data" is enforced
  by Snowflake rather than promised in a prompt.

Both are granted to the learner, so they can switch between building and seeing
the schema the way their agent sees it.

## Resetting between labs

Every lab starts with:

```sql
USE ROLE ACADEMY_LEARNER_<tag>;
CALL AI_ACADEMY.SHARED.RESET_TO('B7');
```

`RESET_TO` runs as the caller and derives the sandbox from the caller's role, so
a learner can only reset their own schema. It drops every view and every
non-seed table, zero-copy clones the seed tables back in, re-anchors the dates,
and applies anything extra the module needs.

**Dates are relative.** Every date in the seed is stored as a whole number of
days from an anchor, the first day of the month the seed was loaded.
`RESET_TO` shifts a sandbox by the difference between that anchor and the
current month, so "efficiency this month" and "notifications older than 30 days"
keep working however long after seeding a learner starts. Relative gaps —
lead times, hold durations, review overdue — never change.

## Adding a table or column

1. Add it to `01_seed_tables.sql` with a `COMMENT`. Sandboxes are clones, so the
   comment reaches the learner's schema and the agents that read it.
2. Seed it in `02`–`04`, using the `DATEADD(day, <offset>, $ANCHOR)` pattern for
   any date.
3. Add the table to `SEED_TABLES` in `05_seed_metadata.sql` and re-run that file
   — `SEED_DATE_COLUMNS` is rebuilt from the catalogue, so new date columns are
   picked up automatically.
4. Run `python _build/check_seed.py` and fix what it reports.
5. Update the expected row counts in `20_learner_start_here.sql`; `check_seed.py`
   verifies they still match.

## Module start state

A module whose start state is more than the seed tables gets rows in
`MODULE_PREREQS` (module, step number, statement; `{{SANDBOX}}` is replaced with
the sandbox schema). Nothing is needed for the modules written so far.

## Deliberate defects

The data is wrong on purpose in five places. They are course content, not bugs,
and `check_seed.py` fails if one is removed:

| Defect | Where | Used by |
|---|---|---|
| Operations confirmed twice — a partial posting never reversed, then the full re-posting | 6 operations in `SAP_WO_OPERATIONS` | B10, A9. Welding at Plant 1 reads about 111% efficiency raw and about 89% once the stale postings are dropped with `QUALIFY` |
| Work orders on superseded revisions | `100004510`, `100004513` | B7 revision questions; found by joining SAP to Teamcenter |
| Documents past their review date | `SOP70000114`, `SWI70000318`, `TDS70000044` | B9, A4 document revision |
| Near-duplicate quality notifications | `300001211` and `300001219` | A9 similarity search |
| Notification text containing instructions aimed at an agent | `300001267`, `300001270` | B11, A13 prompt injection |

`ECN70000042` is released and still waiting for revision C of `SWI70000318`.
That is the change Carla drafts in B9 and A4, not a defect.

## Checking the data without Snowflake

`python _build/check_seed.py` parses these scripts and verifies row shapes,
referential integrity across SAP and Teamcenter, identifier formats, one
released revision per item, work-order/operation status consistency, and that
every deliberate defect is still present. Run it after any edit to the seed.

## Notes

- If you run these in SnowSQL, leave variable substitution off (the default):
  `Assembly & Testing` contains an `&`.
- `$ANCHOR` is a session variable set at the top of each data script, so run
  each file as a whole rather than statement by statement.
- The scripts assume no existing objects with these names. `00` and `10` use
  `IF NOT EXISTS` throughout; the seed scripts use `CREATE OR REPLACE` and
  `TRUNCATE`, so they always rebuild.
- Nothing here contains real client, project, field, part or personal data, and
  nothing contains credentials. Keep it that way — this repository is public.
