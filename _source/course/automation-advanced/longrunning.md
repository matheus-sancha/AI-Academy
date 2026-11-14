## TL;DR

A Power Automate run lasts at most **30 days**, and the limit includes a run that is only waiting for an approval. After 30 days, pending steps time out. {{topic:approvals}} built a sequential approval inside one run and flagged that nobody had documented how long it can wait. This is the answer, and it changes the design: a process that can outlive a run **cannot hold its state in the run**. The community fix splits it in two. A first flow creates the approval, records its id in a list and ends. A second flow starts when the approval completes and finds the record again. Reminders, escalation and safe restarts are in neither source, so they are built here as a marked design.

## Why it matters

A run that waits is cheap to build and expensive to trust. The approval looks like one step in the designer, so the 30-day limit is invisible until a quality lead takes six weeks to answer, the run times out and the draft sits at **Submitted** with nothing to say why. Intermediate treated silence as not approval. Here silence is the default, and the design has to make it noisy.

## How it works

### The limits, in one place

<!-- volatile verified=2026-11 -->
| Limit | Value |
|---|---|
| Run duration | **30 days**, from the run's start, including flows with pending steps like approvals. After 30 days any pending steps time out |
| Run history retention | 30 days from the start |
| Outbound request, synchronous | 120 seconds. The page suggests asynchronous polling, or an Until loop, for longer work |
| Outbound request, asynchronous | Configurable up to 30 days |
| Inbound request | 120 seconds |
| **Until** loop | 60 iterations by default, 5,000 at most |
| Flow with continuous errors | Turned off after 14 days |
| Flow with no trigger activity | May be turned off after 90 days, with notice 30 days earlier. Owners with premium or capacity licences are exempt |
| Owner leaves | The flow drops to the Low performance profile |

Turning a flow off lets runs in progress finish. Deleting it cancels them.

<!-- /volatile -->

<!-- unknown since=2026-11 -->
What a timeout leaves behind. The page does not say what status the run ends in, what happens to the approval record, how long an approval may wait on its own, or the maximum for a **Delay**. It gives no Until timeout. {{topic:approvals}} listed approval timeouts as unknown. The run limit settles the bound on a waiting run, but not these.
<!-- /unknown -->

### Splitting the wait from the process

The community article's problem is the one above: a budget approval can take more than 30 days. Its fix has two flows and a list:

1. **Flow one** triggers when a list item is created. It creates the approval, writes the approval's id and a status of Submitted onto the item, tags the approval's Dataverse row with a source name, and **ends**. It does not wait.
2. **Flow two** triggers when a row in the Dataverse approvals table changes to Completed, filtered by that source. It finds the list item by the approval id and sets the status to Approved or Rejected from the result.

The approver answers in the Approvals center whenever they like. Completion starts a fresh run, so the 30-day clock starts again. A premium service account owns both flows, and approvers need no licence, the author says.

<!-- unknown since=2026-11 -->
The article is from May 2024, and it is not Microsoft documentation. The completion status it filters on is a numeric code, `192350004`. Its author says he does not fully know how cancelled, abandoned, expired or suspended approvals reach the table. Readers report a source-column error in 2025, approvals made from one portal not starting the second flow at first, and pending approvals being cancelled. Check each in your own environment. The second flow also sits idle waiting for approvals, which is the shape of the 90-day no-trigger rule. The article uses a premium owner and does not mention it, and whether a filtered Dataverse trigger counts as activity is unstated.
<!-- /unknown -->

### What the record has to carry

The split moves the process out of the run and into data. The list item is now the process: its status, the approval's id, who was asked and when. Anything flow two needs must be on it, because flow one's run is gone. If flow one fails between creating the approval and writing the **approval id**, flow two never finds a match, so write both in one step.

### Reminders, escalation and restart

<!-- unknown since=2026-11 -->
Neither page covers reminders, escalations, resubmission or restarting a stalled process. What follows is design built on the persisted record, not documentation.
<!-- /unknown -->

A third flow, on a schedule, reads the list for items still **Submitted** and acts on their age: a reminder to the approver at one threshold, an escalation to the next named person at another, and a flag to the document owner past the third. It is the only part that needs the clock, and it keeps no state of its own. If an approval is abandoned, the sweeper resubmits: it creates a new approval, writes the new id to the same item and marks the old id superseded, and flow two ignores a completion whose id is no longer current. That check is what makes a restart safe.

## In practice at Technik

`ECN70000042` is released and revision C of `SWI70000318` is waiting. The sequential approval in {{topic:approvals}} runs in one run. The cladding process engineer answers in a day. The quality lead is away for six weeks. At day 30 the run times out and the draft sits at **Submitted**.

Re-cut with the split, the submission flow creates the approval and ends. The submission list carries `Status`, `ApprovalId`, `Approver` and `SubmittedAt`. A weekday flow reads the *Document approvers* list, as before, and:

| Age of a **Submitted** item | Action |
|---|---|
| 7 days | Remind the current approver |
| 14 days | Ask the next named person on the *Document approvers* list to cover, and tell the owner |
| 30 days | Replace: create a new approval, record the new id, mark the old one superseded |

The thresholds are Technik's choice. Nothing in the pages sets them. The flow that records the outcome ignores any id that is not the item's current one, so a late answer to the replaced request changes nothing. The release in Teamcenter stays with the owner.

The sweeper itself needs watching: a flow that fails every run for 14 days is turned off, so it ends with the alert from {{topic:errors}}.

## Design guidance

- **Don't design a wait that can pass 30 days inside one run.** Split it.
- **Keep the process in data**: status, approval id, approver and dates on the record.
- **Write the id before the run ends**, and make the second flow match on it.
- **Run a scheduled sweeper** for reminders and escalations, so the clock lives in one place.
- **Make a restart safe**: a new id, the old one marked, and a check that ignores stale completions.
- **Give the flows a lasting owner**, such as a service account, and watch for the 90-day rule.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A draft sits at Submitted for weeks | The run timed out at 30 days | Split the wait from the process |
| The second flow never fires | The id was not recorded, or the source filter does not match | Write the id first, and test the filter |
| A late answer overwrites a newer decision | The restart left two live approvals | Check the id is current |
| The waiting flow is turned off | No trigger activity for 90 days, and the owner is not exempt | Own it with a premium or capacity licence |
| The flows stop when a person leaves | They own the flows | Use a service account |

## Key terms

**Run duration limit**: the 30 days a run may last, waiting steps included.

**Persisted state**: process data kept on a record, so no run has to stay alive to hold it.

**Sweeper**: a scheduled flow that scans records by age and acts on the stale ones.

**Superseded approval**: an approval replaced by a restart, whose completion is ignored.

