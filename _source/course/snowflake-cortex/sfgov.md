## TL;DR

Three Snowflake features put a rule where the database enforces it, and each answers a different question. A **secure
view** hides its definition and closes the ways a user's own query could infer rows the view filters out. A **row access
policy** decides which rows a role gets from a table or view, owner included. A **masking policy** changes what a column
shows. All three decide from the session's role and context, which is why they hold against a prompt injection: the model
can ask for anything, and the role it runs as does not change. What they cost is real. Secure views are slower and hide
their profile, row access and masking need Enterprise Edition, and none of them can tell one caller of a single-identity
agent from another.

## Why it matters

{{topic:sfroles}} gave the agent a role and {{topic:sfviews}} gave it views, which protect by omission: a column that is
not in the view cannot leak. Two gaps remain in the capstone's grants. `SAP_QUALITY_NOTIFICATIONS` and `TC_DOCUMENTS`
are granted as raw tables, so nothing but the grant limits what they hold. And every view is plain, so its definition is
visible to other users. Whether either matters depends on what is behind it. The agent's reach is bounded by Snowflake's
grants and not by a sentence in a prompt ({{topic:ctxsecurity}}), so the question is which tool a given rule needs.

## How it works

### Secure views

The secure views page opens with the risk. For a non-secure view, "internal optimizations can indirectly expose data":
user code can reach what the view hides. Its example is a user who may see only red widgets and adds
`WHERE 1/iff(color = 'Purple', 0, 1) = 1`. If the optimizer runs that predicate first, a division-by-zero error shows
that a purple widget exists. A secure view skips those optimizations and runs its own `WHERE` before the user's. Its
definition is also shown only to the role that owns it, in `SHOW VIEWS`, `GET_DDL` and the information schema.

The price is stated too: secure views "can execute more slowly", so the page says not to use them for views "defined
solely for query convenience". The profile of a secure view is hidden even from its owner. You add `SECURE` to
`CREATE VIEW`, or set it with `ALTER VIEW`. The page lists what it still leaves open. A sequence-generated key lets a user
count hidden rows from the gap between two visible ids, 1455 less 315 in its example. And run time can hint at data volume.

### Row access policies

<!-- volatile verified=2026-11 -->
A row access policy is a schema-level object that returns a boolean, attached to the columns of a table or view. It decides
which rows a `SELECT` returns and which rows an `UPDATE`, `DELETE` or `MERGE` touches. It binds the object's owner too. It
does not stop an insert. Its expression is evaluated with the policy owner's role, so a mapping table need not be readable
by the caller. When a table and a view over it both have one, the table's runs first. The page prefers a simple expression,
such as a `CASE` on the role, to a mapping-table lookup, and warns that a policy defeats metadata shortcuts: `COUNT(*)`
must scan, and statistics describe only the rows the caller may see. It needs Enterprise Edition.
<!-- /volatile -->

### Masking policies

<!-- volatile verified=2026-11 -->
Dynamic Data Masking is also Enterprise Edition. A masking policy is applied "at every location where the column appears", and
the role, context and role hierarchy decide whether a query sees the plain value, a partial one or a masked one. A
security or privacy officer chooses the columns, not the object owner, and a policy can keep even `ACCOUNTADMIN` from
reading data it has no need for. A column takes one masking policy. If a row access policy is also present, it runs
first, and a column cannot appear in both policies' signatures.
<!-- /volatile -->

## In practice at Technik

**The capstone's views stay plain.** They deduplicate, translate status codes and leave out unreleased work orders. None
of that is secret, and the agent's role cannot read the tables behind them anyway. The page's own rule is to spare
convenience views the slower path.

**A view that exists for privacy.** Say Plant 2's quality team gets its own agent and must see only Plant 2's notifications.
This is a secure view over an access table, adapted from the page's `widgets_view`:

*Adapted from the access-table example on the secure views page:*

```sql
CREATE OR REPLACE SECURE VIEW V_PLANT_QUALITY_NOTIFICATIONS AS
SELECT q.QN_NO, q.WO_NO, w.PLANT, q.OPERATION, q.PRIORITY, q.STATUS, q.DESCRIPTION
FROM SAP_QUALITY_NOTIFICATIONS q
JOIN SAP_WORK_ORDERS w ON w.WO_NO = q.WO_NO
WHERE w.PLANT IN (SELECT PLANT FROM PLANT_ACCESS_RULES
                  WHERE UPPER(ROLE_NAME) = CURRENT_ROLE());
```

The sequence pitfall applies here. QN numbers are SAP's own, one range for both plants, and the seed's notifications
interleave them. A Plant 2 reader who sees `300001263` and `300001270` can suspect that notifications numbered in between
exist and are hidden from them. In the seed, `300001267` is one. The view must show `QN_NO`, because the agent cites it,
so whether to accept that leak is the data owner's call.

**The same rule as a policy.** A policy on the table has no view to bypass:

*Adapted from the `rap_it` and `ALTER TABLE` examples on the row access policies page:*

```sql
CREATE OR REPLACE ROW ACCESS POLICY rap_plant AS (plant VARCHAR) RETURNS BOOLEAN ->
  CASE
    WHEN CURRENT_ROLE() IN ('SYSADMIN', 'TECHNIK_DEV', 'TECHNIK_AGENT_RO') THEN TRUE
    WHEN CURRENT_ROLE() = 'TECHNIK_PLANT2_RO' THEN plant = 'Plant 2'
    ELSE FALSE
  END;

ALTER TABLE SAP_WORK_ORDERS ADD ROW ACCESS POLICY rap_plant ON (PLANT);
```

Two things in it are decisions. `SYSADMIN` owns the seeded tables and the policy binds owners too, so without a branch
for it, the owner would see no rows. And `TECHNIK_AGENT_RO` gets every plant, because the agent holds one role for all its callers.
Policies filter by the session's role, so a per-person answer needs the person's own role, which the connector's per-user
sign-in can supply ({{topic:sfconnector}}), or a rule outside Snowflake. The capstone chose one identity, and no policy
changes that.

**Masking** is for the opposite case: a column the role must reach but should not read. If `SAP_PROJECTS` were ever
granted so the assistant could name a project, a policy on `CLIENT_NAME` and `FIELD_NAME` would show the agent role masked
values while `TECHNIK_DEV` read them. It is the wrong tool for `TC_DOCUMENTS.OWNER`, which the agent must quote to escalate.

<!-- unknown since=2026-11 -->
Nobody ran these two statements. `PLANT_ACCESS_RULES` and `TECHNIK_PLANT2_RO` are invented and not in the seed. The row
access page's `IS_AGENT_ACTIVATED` example hides rows whenever an agent is active, and does not say what makes one active,
so whether a session from the capstone's connector counts is open. The pages also do not say which edition a trial
account is, and the reader's run of the seed may not be able to create these policies.
<!-- /unknown -->

## Design guidance

- **Leave plain views plain.** Make a view secure only when it exists for privacy.
- **Don't expose sequential ids through a secure view**, or accept that gaps count what is hidden.
- **Put a rule that must hold on every path on the table**, as a row access policy, not in a view that a table grant bypasses.
- **Name the administrator roles in every policy.** It binds owners too.
- **Prefer a `CASE` on the role to a mapping-table lookup**, and bind few columns.
- **Mask what the agent must reach and never quote**, not what it must say.
- **Test as the role.** `POLICY_CONTEXT` simulates a query, and `EXPLAIN` shows `DynamicSecureView` where a policy applies.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A user infers hidden rows from an error in their own predicate | A non-secure view's optimizer can run the user's predicate first | Make the view secure |
| A user counts hidden rows from ids | A sequence-generated key is exposed | Omit it, or use random ids |
| A secure view is slower and its profile is empty | It skips optimizations and hides its internals | Use it only where privacy needs it |
| The table's owner sees no rows | The policy binds owners | Add the administrator role to the policy |
| `COUNT(*)` is slow on a protected table | Metadata shortcuts do not apply | Expect a scan |
| Attaching a masking policy fails | A column takes only one | Choose one policy |

## Key terms

**Secure view**: a view that hides its definition and skips optimizations that could expose filtered rows.

**Row access policy**: a boolean expression, bound to a table or view, that decides which rows a role gets.

**Masking policy**: an expression bound to a column that decides how much of its value a role sees.

**Mapping table**: a table of role-to-entitlement pairs that a policy or secure view reads to decide access.
