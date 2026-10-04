## TL;DR

Three things stall the route, and none of them is a mistake. **A connector your tenant does not have**: run the
**Check** line the tool plan carries, find out why it failed, and take the answer back to stage 3. Do not
patch the instructions. **A result that does not match the example**: expected, because your brief is not
Technik's. Judge the output against the stage's finished-when test, not against how much it resembles a
course page. **A click path that has moved**: find the panel by its name in the Build tab, and leave the route's
order alone. A fourth thing looks like a stall and is not one: an **error code**. That is the product
reporting a failure, and the code says who fixes it.

## Why it matters

When a stage stalls, the natural reaction is to improvise: a workaround in the instructions, a stage skipped,
a step out of order. Each breaks something the route depends on, often three stages later.

The opposite reaction costs as much: redoing a finished stage because it differs from the example. Which kind
of stall you are in decides whether you go back, carry on or ask someone.

## How it works

### A connector your tenant does not have

The tool finder never claims a connector exists unless Microsoft names it. Connector catalogues vary by tenant
and licence, and no list says which ones your environment offers ({{topic:tenantvaries}}). So every block in
`tool-plan.md` carries a **Check** line: *confirm it appears in your tenant and is not premium-licensed*. The
line tells you what to check. It does not say what to do if the check fails, and the failure has three causes
with different fixes:

| What you see in **Add a tool** | Cause | What to do |
|---|---|---|
| The connector does not appear at all | Not offered in this environment | Back to stage 3 with that result |
| It appears **disabled**, with a reason in its hover text | A data policy blocks it ({{topic:dlp}}) | Ask your administrator; it is a policy decision |
| It appears, marked premium | A licence question | A developer environment includes premium connectors; check the environment you will publish from |

Run the check when the plan arrives. Opening **Add a tool**, searching, and closing it again changes nothing in
the agent. Waiting for stage 7 means finding out with everything else already applied.

If the connector is missing, go back to `copilot-find-skills-and-tools` and say what the check found. Picking
the alternative is its job. It works down its order of types (connector, then MCP server, then workflow, then
a pre-built skill) and prefers whatever your tenant already has. The need might also be dropped. Then stage 5
names what was actually planned.

A policy block is different. Nothing about the design is wrong, so do not redesign it. The route can continue
while the administrator decides, because stages 4 to 6 only need the tool *named*. Only stage 7 waits.

### A result that does not match the example

Every example in this level is the Technik Production Assistant: seven capability areas, two tools, one skill,
four user groups. Your agent is not that agent. Its brief will have different slots, the tool plan might have
no connector at all, and the skill creator might turn down the skill you asked for, because it fails the
earns-a-skill test ({{topic:skillsvs}}). None of that means the stage failed.

The test is the **finished-when** column in {{topic:theroute}}:

- A brief is finished when every slot passed its acceptance test, not when it is as long as Technik's.
- A tool plan with no blocks is finished if the brief has no live data, writes or fixed processes.
- An evaluation set is finished when it holds 25 cases in the quota, whatever the questions are.

If a stage's output fails that test, the stage is not finished. Go back to its owner and say which part
failed. If it passes, carry on, however unlike the example it looks. Content differs because briefs differ.
Shape does not, so judge the shape.

### A click path that has moved

<!-- volatile verified=2026-10 -->
Today, skills live in the **Build** tab's components panel, under **Skills**, and that is where you add,
replace and delete them. Copilot Studio's interface changes faster than any course. When a button is not where
the route says, the panel usually still exists under its name. Look for **Skills**, **Tools**, **Knowledge**,
**Instructions** or **Description** in the Build tab, then read Microsoft's page for that component for today's
steps.
<!-- /volatile -->

What does not move is the order. Stage 7's sequence has reasons ({{topic:theroute}}), and a renamed button
does not change them. Delete the six skills before you upload, apply everything before the new chat, and test
before you publish.

### Error codes are not stalls

When a turn fails on the GitHub Copilot harness, **Preview**, **Test** and **Evaluate** show an error code. Four
are likely during a build:

| Code | Meaning | What to do |
|---|---|---|
| `CONTEXT_LENGTH_EXCEEDED` | The turn was too large for the model: instructions, history, tools and results together | Microsoft says start a new conversation, which costs the build. Save every file first, then recover from the brief |
| `RATE_LIMIT_REACHED` | A short-lived burst limit | Wait; in **Evaluate**, rerun the failed cases |
| `QUOTA_EXCEEDED` | Your organisation's longer-running quota is spent | Administrator. Retrying now will not help |
| `SYSTEM_ERROR` | Anything unexpected | Retry once. If it persists, take the conversation ID from the activity trace to support |

The first is the build's own risk: a weeks-long conversation is the long history Microsoft names as its most
common cause. Saved files keep it cheap.

## In practice at Technik

At stage 3 the Production Assistant's plan opens with the Snowflake connector block. The engineer runs its
**Check** at once: **Add a tool**, search *Snowflake*. The connector is there but disabled, and the hover text
names the environment's data policy. Nothing about the design is wrong, so they leave the plan as it is and
send the administrator the policy name and the role it will run as, `TECHNIK_AGENT_RO`. Stages 4, 5 and 6
continue meanwhile. Stage 7 waits for the policy to change.

A colleague building a shift-handover agent compares their brief with the one in {{module:designing-an-agent}}.
Theirs has two tasks, no tools and no knowledge source, and they nearly redo the interview. Every slot passed
its test, though, so the brief is finished. Stages 3 and 4 are skipped and stage 5 only confirms the draft.

At stage 7 a third engineer cannot find **Upload a skill**. They find **Skills** in the components panel,
follow Microsoft's page for today's path, and still delete the six first.

## Design guidance

- **Run every Check line when the plan arrives.** Looking changes nothing; finding out at stage 7 does.
- **Tell a missing connector from a blocked one.** One is a design question, the other a policy question.
- **Send design problems back to their owner.** Never write around a missing tool in the instructions.
- **Judge shape, not content.** Your agent's outputs should look different from Technik's.
- **Search by panel name** when a click path moves, and keep the order.
- **Read the error code before improvising.** It says whose problem it is.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The instructions describe a tool the agent does not have | A missing connector was patched at stage 5 | Back to stage 3; let stage 5 name what was planned |
| The connector is greyed out | A data policy blocks it | Read the hover text; ask your administrator |
| A finished stage gets redone | Its output was compared with the example | Check it against the finished-when test |
| A stage-7 step is not where the route says | The interface moved | Find the panel by name; read Microsoft's page |
| `CONTEXT_LENGTH_EXCEEDED` mid-build | The build conversation grew too long | Save files, new chat, re-upload the brief |
| Evaluation cases fail with `RATE_LIMIT_REACHED` | A short-lived burst limit | Wait, then rerun the failed cases |

## Key terms

**Stall**: a stage that cannot finish as written, though nothing is broken.

**Check line**: the tool plan's instruction to confirm a connector exists in your tenant before you rely on it.

**Error code**: the short code Copilot Studio shows when a turn fails, naming whether retrying helps and who
acts.
