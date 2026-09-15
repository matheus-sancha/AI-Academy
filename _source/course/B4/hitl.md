## TL;DR

Some actions should not happen without a person: approving spend, sending external mail, changing a
record, releasing a document. Human-in-the-loop means designing the confirmation, the approval and
the escalation deliberately — and putting the human at **the last point where reversing is still
cheap**. It matters most for autonomous agents, where nobody is watching by default.

## Why it matters

An agent's reach is exactly its tools. Give it a tool that writes, and it can write — correctly,
usually, and wrongly sometimes, and it cannot tell which. The question is not whether to trust the
agent but where a mistake becomes expensive, and to put a person just before that line.

Get it wrong in one direction and people rubber-stamp everything, which is no control at all. Get it
wrong in the other and the agent is so hedged that nobody uses it.

## How it works

Three mechanisms, in increasing weight:

| Mechanism | Is | Use for |
|---|---|---|
| **Confirmation** | The agent states what it is about to do and waits | Anything with a side effect the user might not have intended |
| **Approval** | A named person approves, out of band, before it proceeds | Anything irreversible, or that affects others |
| **Escalation** | The agent stops and hands to a person | Out of scope, repeated failure, anything it is unsure of |

### Where to put the human

**At the last point where reversing costs little.**

Too early and they approve an empty request — they have nothing to judge, so they approve
everything. Too late and they are approving something already in effect, which is notification
dressed as control.

For a document revision: not when the request is made (nothing to see), not after release (too
late), but **between the draft and the release** — the draft is reviewable and nothing has happened
yet.

### Make approving cheap and rejecting easy

An approval nobody has time to do properly is worse than none, because it creates a record of review
that did not happen. So:

- put everything needed to decide **in** the request — the draft, the sources, what changes;
- make rejection one click, with a reason;
- route to a named role, not a shared mailbox;
- set a timeout and decide what happens on silence. Silence is not consent.

### Least privilege first

The cheapest human-in-the-loop is not needing one. An agent whose Snowflake role is read-only cannot
be talked into a write, by a user, by an injected instruction, or by its own confusion. Approvals
are for what the agent genuinely must do; **privilege** handles everything it never should.

## In practice at Technik

Four points in the Technik design, and the reasoning differs at each:

| Where | Mechanism | Why there |
|---|---|---|
| Reading any Snowflake data | **None — least privilege** | The role is read-only. Nothing to approve because nothing can be changed |
| Drafting a QN write-up (B8) | **None** | A draft is not an action. It is shown, and Bruno decides |
| Creating a quality notification in SAP | **Confirmation** | A record others act on. The agent states what it will create and waits |
| Releasing a document revision (B9) | **Approval** | It changes what the shop floor works to. The approver sees the draft, the ECN and the diff |

Two things in that table are worth arguing with, which is the point.

**Why is drafting not gated?** Because nothing happens. Bruno reads it, edits it, and decides. Adding
an approval to a draft is the "rubber-stamp everything" failure — a step with nothing at stake
teaches people that approvals are noise, and then the one that matters gets the same treatment.

**Why is reading not gated?** Because the identity already bounds it. The assistant reads with
`ACADEMY_AGENT_<you>`, which can read one schema and write nothing. Asking a human to approve reads
would be theatre, and the seeded data contains notification descriptions that try to talk the agent
into more (B11) — against which an approval is far weaker than a privilege.

The document revision flow is where a real approval earns its place. `SWI70000318` is waiting on
revision C under `ECN70000042`; when that revision is released, cladding operators work to different
acceptance criteria the same day. The approver needs the draft, the ECN, and what changed — which is
exactly what B9's flow puts in the approval request.

> [!TIP]
> Test your approvals by rejecting. Most are only ever tested by approving, and the rejection path —
> what the agent says, what happens to the draft, whether the requester finds out — is usually the
> one nobody built.

## Design guidance

- **Least privilege before approvals.** Do not approve what the agent should never have been able to
  do.
- **Put the human at the last cheap-to-reverse point.**
- **Do not gate drafts.** Gate effects.
- **Put the whole decision in the request.** An approver who has to go and look will stop looking.
- **Make rejection easy and reasoned.**
- **Decide what silence means**, and never let it mean yes.
- **Test the rejection path.**
- **Log every decision.** Who approved what, when, on what evidence.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Everything gets approved without reading | Too many approvals, or not enough information in them | Remove the low-stakes ones; put the evidence in the request |
| An approval exists but the action already happened | Placed too late | Move it before the effect |
| Approvals stall for days | Routed to a shared mailbox, or no timeout | Named role, timeout, and a defined outcome on silence |
| The agent did something irreversible | A tool existed for it with no gate | Privilege first, then approval |
| Rejection leaves things in a strange state | The path was never tested | Test by rejecting |
| No record of who approved | Not logged | Log it. This is usually the audit question |

## Key terms

**Human-in-the-loop** — a person in the path before something consequential.

**Confirmation** — the agent states and waits.

**Approval** — a named person decides, out of band, before it proceeds.

**Escalation** — handing over to a person entirely.

**Least privilege** — an identity that cannot do what it should not (B7).

**Timeout** — what happens when an approver does not respond. Never "proceed".
