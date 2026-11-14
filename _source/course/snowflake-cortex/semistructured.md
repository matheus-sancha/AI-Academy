## TL;DR

Semi-structured data has no schema fixed in advance, and it nests: objects inside arrays inside objects. Snowflake stores
it in a `VARIANT` column, so a table can keep a bench's JSON readings beside ordinary columns, and `FLATTEN` turns an
array inside it into rows. The flexibility has a cost. The table no longer says which keys exist, `FLATTEN` drops any
row that lacks the path unless `OUTER => TRUE`, and the two curated pages leave open what a missing key returns. So an
agent should read columns, and a view should do the extracting.

## Why it matters

Technik's `FAT_RESULTS` table has ordinary columns, `SERIAL_NO`, `TEST_ID` and `RESULT`, and one `VARIANT` column,
`RAW`, holding what the test bench wrote. The tests do not write alike. The hydrostatic tests record a `readings` array of
pressure samples, the gas seat test records bubble counts, the torque test records limits. A fixed schema would need a
column for every key of every test, empty wherever a test never writes it. A `VARIANT` takes the keys as they come, and
the loading page says entities of one class "may have different attributes". The question *did the body test hold its
pressure?* now lives inside a value.

## How it works

### The types

The loading page names three. A `VARIANT` holds a value of any other type, including an `ARRAY` or an `OBJECT`, and an
`ARRAY` or `OBJECT` holds `VARIANT`s. An `OBJECT` is a dictionary of key-value pairs, not an object in the programming
sense. Nested, they make a hierarchy of almost any depth. No schema has to exist before loading, attributes can be added
at any time, and the order of attributes does not matter.

### Loading

Snowflake reads JSON, Avro, ORC, Parquet and XML. Key-value data can go into an `OBJECT` column and an array into an
`ARRAY`. Hierarchical data can be split across columns or kept whole in a `VARIANT`, and a value of more than about
128 MB calls for combining the two. The entry points are `COPY INTO` with the file format's `TYPE`, or `PARSE_JSON` to
turn JSON text into a `VARIANT`. Snowflake converts it to an internal format built for "fast and efficient SQL querying".

### Querying

The page says Snowflake has operators for reaching an array element, a key's value and the levels of a hierarchy, and
sends you elsewhere for their syntax. What these two pages show is the colon: `f1.value:type` reads the `type` key. The
output they print keeps the JSON quotes, `"phone"`, because the value is a JSON string held in a `VARIANT`, not text in a
text column.

### FLATTEN

`FLATTEN` is a table function. It takes a `VARIANT`, `OBJECT` or `ARRAY` and returns one row per element, with the
columns `SEQ`, `KEY`, `PATH`, `INDEX`, `VALUE` and `THIS`. The source row's columns repeat on each output row. Its
arguments are `INPUT`, `PATH` (the element to expand), `OUTER`, `RECURSIVE` (expand every sub-element) and `MODE`.

Three facts carry the rest. `SEQ` is "not guaranteed to be gap-free or ordered", and `INDEX` is the position in an
array. With `OUTER` false, which is the default, any input row that cannot be expanded is "completely omitted", whether
the path is absent or the array is empty. With `OUTER => TRUE`, a zero-row expansion yields exactly one row, with NULL in
`KEY`, `INDEX` and `VALUE`. And for nested data, chain `LATERAL FLATTEN` calls, because the second needs the first's
output.

## In practice at Technik

The capstone's seed script loads `FAT_RESULTS` from CSV and parses the JSON column on the way in:

*From [`seed/seed.py`, lines 44–46](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/seed/seed.py#L44-L46):*

```python
        if table == "FAT_RESULTS":  # RAW is VARIANT: parse the JSON column on the way in
            source = f"(SELECT $1, $2, $3, $4, $5, PARSE_JSON($6) FROM {source})"
        cur.execute(f"COPY INTO {table} FROM {source} FILE_FORMAT = (FORMAT_NAME = SEED_CSV)")
```

The seven rows are two units' bench tests. Four of them, `FAT-01` and `FAT-02` on each unit, carry a `readings`
array of four samples. `FAT-01` goes from 1034.2 bar at minute 0 to 1033.9 at minute 15 on both units, and `FAT-02` holds
689.5 bar throughout. The gas seat test on `XT-V2-1041`, `FAT-03`, failed, with 7 bubbles a minute where 0 is allowed.
Neither it nor the torque test has a `readings` key. This query turns the samples into rows:

*Adapted from the lateral `FLATTEN` example on the `FLATTEN` page, for `FAT_RESULTS`:*

```sql
SELECT t.SERIAL_NO, t.TEST_ID, r.index, r.value:t_min AS T_MIN, r.value:bar AS BAR
FROM FAT_RESULTS t,
     LATERAL FLATTEN(INPUT => t.RAW, PATH => 'readings') r
ORDER BY t.SERIAL_NO, t.TEST_ID, r.index;
```

It returns 16 rows, four tests with four samples each. The other three tests are not in it: with `OUTER` false their
rows are omitted, so counting tests from this result finds four of seven. A report built on it would read as if the gas
seat failure never happened.

The capstone's agent role cannot read `FAT_RESULTS`, and no tool touches it. A bench question would be a new view for a
new question, as {{topic:stagemcp}} teaches. The view extracts the fields, names and types them, and flattens with
`OUTER => TRUE` so a test without readings stays visible. The agent then sees `PRESSURE_START_BAR`, not a path to guess.

<!-- unknown since=2026-11 -->
Nobody ran this query, and the pages leave three things open that it touches. They do not say what a path to an absent
key returns, which matters because only two of the four test kinds write `readings`. They do not document converting a
`VARIANT` value to a plain type, which a view needs before it can compare or sum a pressure, and the `::` casts on the
loading page appear only while building values. And the `OUTER` text speaks of "zero-row expansions" while its example
shows only an empty array, so 19 rows (the 16 samples and one row for each of the three tests without them) is the
expected result, not a checked one.
<!-- /unknown -->

## Design guidance

- **Keep in a `VARIANT` what varies, and in columns what every question uses.** `SERIAL_NO`, `TEST_ID` and `RESULT` are
  columns for that reason.
- **Extract in a view**, with names and types, so the agent's SQL never holds a path expression.
- **Write `OUTER => TRUE` on any flatten whose source may lack the path**, and compare its row count with the source's.
- **Flatten one `PATH`.** `RECURSIVE => TRUE` expands every sub-element, and the row count follows.
- **Order by `INDEX`, never `SEQ`**, and chain flattens with `LATERAL`.
- **Find out which keys exist** by flattening the object with no `PATH` and reading `KEY`. The table will not tell you.
- **Parse JSON text once, on load**, with `PARSE_JSON`.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Tests are missing from a flattened result | `OUTER` is false by default, so rows with an absent or empty path are omitted | Use `OUTER => TRUE` and compare counts |
| Strings come back in quotes | A `VARIANT` holds JSON values, and the pages' output shows `"phone"` | Convert to a plain type in the view |
| The second `FLATTEN` cannot see the first | Without `LATERAL`, it cannot reference the first's output | Write `LATERAL FLATTEN` |
| Readings arrive in an odd order | `SEQ` is not ordered | Order by `INDEX` |
| Row counts jump after a flatten | One row per element, with the source row's columns repeated | Flatten one path and aggregate before joining |
| A column is NULL for one kind of test only | Entities of one class may have different attributes, and no schema flags it | List the keys per `TEST_ID` first |

## Key terms

**`VARIANT`**: a column type that holds a value of any other type, including arrays and objects.

**`OBJECT`**: a dictionary of key-value pairs whose values are `VARIANT`s.

**`FLATTEN`**: a table function that returns one row per element of a `VARIANT`, object or array.

**`LATERAL`**: the join form that lets a `FLATTEN` read columns of the tables before it, and the output of an earlier
`FLATTEN`.

**`PARSE_JSON`**: the function that turns JSON text into a `VARIANT`.
