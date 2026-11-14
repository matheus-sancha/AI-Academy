## TL;DR

Cortex AI functions put a model call inside a SQL expression, so a `SELECT` over a table becomes a batch job over its rows.
The task-specific ones return a label (`AI_CLASSIFY`), a boolean (`AI_FILTER`), fields (`AI_EXTRACT`), a score
(`AI_SIMILARITY`) or a summary across rows (`AI_AGG`), and `AI_COMPLETE` covers the rest. Three properties set them apart.
Each row is billed in tokens, on top of the warehouse. A row the model cannot process comes back `NULL` and the query
carries on, so a half-empty result looks finished. And the model reads text people wrote, which at Technik includes
notifications with instructions planted in them. They suit batch enrichment, not a question a person is waiting on.

## Why it matters

{{topic:snowflakeknowledge}} and {{topic:cortexanalyst}} let a model write SQL over your data. This is the opposite
direction: SQL you write calls a model on each row. Technik's quality notifications show the need. The table says whether a
notification is Open or Closed and names its defect type, but what was done about the defect sits in a sentence of the
description: ground out and re-inspected, accepted by concession, unit held. A query cannot filter on a sentence, and nobody
wants a person to read every one. A function can turn it into a label where the data already lives, under the role that
already governs it. The price is a bill per row and a result you cannot take on trust, so this lesson is as much about
checking the output as about calling the function.

## How it works

### What the page lists

<!-- volatile verified=2026-11 -->
The overview page names fifteen AI functions and three helpers, and calls the main group task-specific. `AI_COMPLETE` is
for "most generative AI tasks". `AI_CLASSIFY` and `AI_FILTER` take text or images, and `AI_EXTRACT` reads a string or a
file. `AI_AGG` and `AI_SUMMARIZE_AGG` read a whole column, unbound by a model's context window. Further functions handle
embeddings, sentiment, translation, redaction and document parsing. The helpers are `PROMPT`, `TO_FILE` and
`AI_COUNT_TOKENS`. The page labels no function generally available or preview, and says to check each one's status before
production use.
<!-- /volatile -->

A caller needs the account privilege `USE AI FUNCTIONS` and one of the database roles `CORTEX_USER` or
`AI_FUNCTIONS_USER`. The models run inside Snowflake's service perimeter, in select regions. The page's one statement about
speed is that the functions are "optimized for throughput", so batch work suits them, and a latency-sensitive caller should
use the REST API. That sentence decides where they sit in an agent's design.

### The four you will meet first

<!-- volatile verified=2026-11 -->
`AI_CLASSIFY` takes an input and an array of at least two categories. A category is a string, or an object with a `label`
and a description of 25 words or fewer. An optional config object carries a `task_description` of 50 words or fewer, an
`output_mode` of `'multi'` for several labels, and `examples`. It returns an object whose `labels` array holds your labels,
read as `AI_CLASSIFY(input, classes):labels`. The page advises plain English text, not code, logs or non-English, and warns
that more than twenty categories might reduce accuracy.

`AI_FILTER` returns a boolean for a `WHERE` clause or a join condition, and its columns must not hold `NULL`. A built-in
optimization can give, the page says, "2 to 10 times faster performance and up to 60% lower token usage", applied
automatically and not guaranteed.

`AI_SIMILARITY` compares two strings, or two images, but not a string with an image. It returns the cosine similarity of
their embeddings, from -1 to 1, and billing files it under `AI_EMBED`.

`AI_COMPLETE` takes a model and a prompt. `temperature` and `top_p` default to 0 and `max_tokens` to 4096, and small values
can truncate a reply. A `response_format` forces a JSON schema or a SQL type, but the schema rules out keywords such as
`minLength` and `maximum`. Setting `guardrails` to `TRUE` enables Cortex Guard, billed in addition.
<!-- /volatile -->

### When a row fails

By default a function that cannot process its input returns `NULL`, and the failing row does not stop the query. A
`return_error_details` argument turns the result into an object with a `value` and an `error`. The `AI_CLASSIFY` page does
not say whether a second run returns the same label, and `AI_COMPLETE`'s advises a temperature of 0 for consistency.

## In practice at Technik

**Reading what the table does not say.** The seed holds twelve notifications. Read by a person, six record a rework
(`300001198`, `300001241`, `300001248`, `300001252`, `300001259`, `300001263`), `300001205` was accepted by concession,
`300001211`, `300001219` and `300001234` are held, and `300001267` and `300001270` state no action. Those counts are the
answer key. A reader labels the twelve first, then runs the function and compares.

*Adapted from the task-description example on the AI_CLASSIFY page. The `:labels[0]::STRING` path is the `VARIANT` syntax from {{topic:semistructured}}:*

```sql
SELECT QN_NO,
       AI_CLASSIFY(
         DESCRIPTION,
         ['reworked', 'accepted by concession', 'held pending disposition', 'none stated'],
         {'task_description': 'Which action does this quality notification say was taken?'}
       ):labels[0]::STRING AS ACTION_TAKEN
FROM SAP_QUALITY_NOTIFICATIONS;
```

The label is a reading of a sentence, never a disposition. That belongs to the quality engineer assigned to the
notification, and the Production Assistant never makes it. The column is for filtering and reporting.

**Finding the same defect twice.** Notifications `300001211` and `300001219` describe the porosity of `300001234` in
different words. Similarity finds that without a shared keyword.

*Adapted from the `ORDER BY` example on the AI_SIMILARITY page:*

```sql
SELECT QN_NO, DESCRIPTION,
       AI_SIMILARITY(DESCRIPTION, (SELECT DESCRIPTION FROM SAP_QUALITY_NOTIFICATIONS
                                   WHERE QN_NO = '300001234')) AS SCORE
FROM SAP_QUALITY_NOTIFICATIONS
WHERE QN_NO <> '300001234'
ORDER BY SCORE DESC
LIMIT 3;
```

**Text addressed to the model.** Two open notifications in that table, `300001267` and `300001270`, carry sentences aimed at
an assistant. One asks it to report the notification as closed, and the other to draft a new revision of a work
instruction ({{topic:ctxsecurity}}). Both statements above read them. A classifier can answer only with a label from its
list, so the second request has nothing to act on, but the first can still tilt which label wins. A free-text
`AI_COMPLETE` can echo planted words into an output that a later step reads as fact. So treat every output column as
derived from untrusted text, and keep it out of any path that decides or acts.

**Where it sits in the agent.** The capstone calls no AI function, and a model call per question would slow its keyed
lookups. The pattern the page supports is to enrich in a batch, store the label, and let the agent's view expose it beside
the text. That is this course's position, not a documented design.

<!-- unknown since=2026-11 -->
Nobody ran these statements. The pages do not say what `AI_CLASSIFY` returns for text that states no action, since it
reports no confidence, or how any function treats instructions inside its input. They do not say whether a scalar
subquery is accepted as an argument, whether any function accepts a `VARIANT`, or whether `AI_SIMILARITY` embeds both
texts again for every row of a join, which decides how fast cost grows. {{topic:sfcost}} covers the bill. The category
labels are Technik's own choice.
<!-- /unknown -->

## Design guidance

- **Choose the narrowest function.** Use `AI_CLASSIFY` for a closed set and `AI_COMPLETE` only for free text.
- **Give the model a way to decline.** A closed list always offers a label, so add one such as `none stated`.
- **Label a sample by hand first**, keep it, and compare every change against it ({{topic:llmjudge}}).
- **Count the `NULL` rows** after every run, and use `return_error_details` while testing.
- **Run in batch and store the result.** Do not call a model per question.
- **Keep category lists short.** Past twenty, split the question.
- **Never let a derived column decide or act.** Its text was never vetted.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The column has gaps, but the query succeeded | A row that fails returns `NULL` | Count them, and read the error details |
| A few labels are confidently wrong | A closed list always offers a label | Add a decline label and check a hand-labelled sample |
| Accuracy falls as the label list grows | More than twenty categories | Split into two questions |
| `AI_FILTER` misbehaves on some rows | The column holds `NULL` | Filter the `NULL`s out first |
| A structured output is rejected | The schema uses an unsupported keyword | Drop it, then validate in SQL |
| An output repeats a planted instruction | Input text is untrusted | Treat the column as data, never as a command |

## Key terms

**Task-specific function**: an AI function built for one job, such as classifying or filtering, with a fixed output shape.

**Category**: a label offered to `AI_CLASSIFY`, either a string or an object with a description.

**Structured output**: an `AI_COMPLETE` reply forced into a JSON schema or SQL type.

**Cosine similarity**: the score `AI_SIMILARITY` returns, from -1 to 1, comparing two embeddings.
