## TL;DR

{{topic:cloudflows}} gave a flow one catch scope that tells its owner. This lesson is the rest of the discipline: **scopes** for Try, Catch and Finally, **run-after** for which outcome each handler answers to, **Terminate** to end a handled failure as Failed, **retry policies**, and a record of every failure somewhere the process can see. The spine is a distinction the pages never state. Error handling catches what **throws**, while an AI step often **returns**, successfully, an answer that is empty, malformed or wrong, and that needs a check after the step. Neither page covers AI steps, idempotency or timeouts, so those parts are marked.

## Why it matters

A flow that fails says so in its run history, and the people it affects never read that. The risk in the other direction is a flow that catches an error and carries on, which can finish green. {{topic:cloudflows}} ends such a flow as Failed on purpose, and Microsoft's guidance is a **Terminate** action set to Failed whenever a flow must stop because of an error.

AI steps add a failure no handler sees. A prompt that returns an empty field did not fail: the run is green, the record is incomplete, and only a check you wrote stands between it and the register.

## How it works

### Try, Catch and Finally

Microsoft's guidance names a **Try** scope and a **Catch** scope, configured to run when the Try scope fails. It has no Finally. The community patterns, from 2022, add one: a Finally step with every run-after box ticked, so it runs whatever happened. The article's first pattern sends its success message even after the Catch ran, as the author admits, and fixes it with a Boolean set in the Catch and tested later. Readers report the variable never being set to true, and the Catch also running when the step before it was only skipped. Treat it as a sketch and test both paths.

### Run-after, and ending as Failed

Run-after settings say what a step does if the one before it fails, times out, is skipped or succeeds. **Terminate** is the step that ends the run: Microsoft says to add it when you need to stop because of an error, set its status to **Failed**, and give it a message. A Catch that notifies and does not terminate leaves a green run.

### Retries

<!-- volatile verified=2026-11 -->
A retry policy repeats an action at **fixed** or **exponential** intervals, and Microsoft prefers exponential, with retries after one, two and four minutes as its example. The limits page gives the defaults. A flow with the Low performance profile retries up to 2 times, with intervals that scale by 5 minutes to about 10 minutes. A Medium or High profile retries up to 12 times, scaling by 7 seconds to about an hour. You can set up to 90 attempts, a delay of up to a day and a minimum of 5 seconds. A flow that fails continuously for 14 days is turned off.
<!-- /volatile -->

A retry runs an action again, so it belongs only on actions that are safe to run twice. The pages say nothing about that.

<!-- unknown since=2026-11 -->
Idempotency, duplicate prevention, per-action timeouts and concurrency are not covered by either page, and neither says what status a run shows once a Catch has handled a failure. The guidance page also says the retry policy is set both in flow settings and in the settings of the action. The advice here, that only repeatable actions are retried and every write is keyed, is a position, not documentation.
<!-- /unknown -->

### Telling someone

Microsoft's advice is to record error details in a SharePoint list or other storage and then notify people, with Application Insights as an alternative. Power Automate also emails flow owners about common failures such as broken connections and throttling, which is a floor and not a design. The page warns that heavy custom logging adds actions and can slow the flow.

A useful alert holds the flow name and a link to the failed run. Both pages build the link from the `workflow()` function, whose output carries the environment name, the flow's identifier and the run.

*Adapted from the article's expression for the run's name, read from a Compose of `workflow()`:*

```text
outputs('Compose:_Get_Workflow_Details')?['run']?['name']
```

<!-- unknown since=2026-11 -->
The guidance page builds its link from the whole `run` value, though its own schema makes `run` an object with an id, a name and a type. The article reads the name. Test the link before relying on either.
<!-- /unknown -->

### AI steps fail in new ways

<!-- unknown since=2026-11 -->
Neither page mentions AI Builder, prompts, content filters, malformed JSON or AI timeouts. What the course has sourced elsewhere: a tool call must answer within 100 seconds ({{topic:flowtools}}), a prompt can return an error when the model wraps its JSON in Markdown ({{topic:prompts}}), what a blocked prompt returns is not documented ({{topic:promptsadv}}), prepaid capacity running out blocks new runs ({{topic:wfagentnodes}}), and an AI step can fail with `QuotaExceeded` ({{topic:aibuilder}}).
<!-- /unknown -->

Sort those into two kinds. A **thrown** failure is a call that errors or times out. A catch handles it, perhaps after a retry. A **returned** failure is a step that succeeds with an unusable answer: an empty string, JSON that doesn't parse, a field that is blank. No scope sees it. Write the check that does, straight after the step, and send what fails it to a person.

## In practice at Technik

The certificate flow from {{topic:docproc}}, with every failure given a home:

| What goes wrong | Kind | Handled by |
|---|---|---|
| A SharePoint read times out | Thrown | Exponential retry, then the Catch |
| The model cannot open a locked or corrupt PDF | Thrown | The Catch |
| The prompt returns JSON that does not parse | Returned | A parse check, one retry, then **Needs review** |
| Every field comes back blank | Returned | A completeness check, then **Needs review** |
| Capacity runs out | Platform | An alert that the flow is not running |

The Catch writes a register row with status **Processing failed**, the reason and the run link, and notifies the quality inspector named for that supplier. The inspector is a person, never a shared mailbox ({{topic:hitl}}). It then **terminates as Failed**. Without the row, a certificate that failed to read looks exactly like one that never arrived.

The write to the register is the one step the flow never retries blindly. It checks the certificate number first, so a retry after a half-finished run updates the row instead of adding a second.

A flow that fails every run for 14 days is turned off, so a team that never looked at its failures would find the process stopped. The Failed status is what a monitor reads.

## Design guidance

- **Wrap the work in Try, with a Catch that records, notifies and terminates as Failed.**
- **Never let Finally claim success.** Say what happened.
- **Retry only actions that are safe to repeat**, with exponential intervals, and key every write.
- **Check each AI step's output in code**, because a green run can hold an empty answer.
- **Leave a record the process can see**, such as a register row with the reason.
- **Notify a named person**, with the flow name and a run link.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The run shows Succeeded, but a certificate is missing | The Catch handled the error and did not terminate | End the Catch with Terminate set to Failed |
| The success email goes out after a failure | A Finally sends its message whatever happened | Branch on a flag, or word it neutrally |
| A green run holds an empty record | The AI step returned nothing, and nothing checked it | Add a completeness check |
| The flow stops with no one told | Fourteen days of continuous failure | Alert on Failed runs |

## Key terms

**Scope**: a container of actions that can be given a shared run-after rule.

**Run-after**: the setting that says which outcome of the previous step lets this one run.

**Terminate**: the action that ends a run with a chosen status, such as Failed, and a message.

**Returned failure**: a step that succeeds and gives an unusable answer, which only a check can see.
