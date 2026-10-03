## TL;DR

Before you automate anything, **reproduce the problem by hand**. Take the user's exact words, open a **new
chat**, ask again, and do it three times. Then read the activity trace (the activity map on the standard
harness) to tell which of four faults you have: the **wrong knowledge**, the **wrong tool**, **bad inputs** or
**unclear instructions**. From the answer alone they look identical, and each has a different fix. The
reproduced case then goes into the evaluation set, so the fix is checked on every later run.

## Why it matters

A report arrives as a sentence: *"the assistant got the revision wrong"*. That is not a test case. It has no
exact wording, no conversation before it, no user, and no evidence of what the agent did. Fix from the
sentence and you are fixing a guess.

Manual testing is where a report becomes a case you can see fail. An evaluation run can tell you that a case
failed. The preview pane is where you find out *why*, because you can steer each turn and open each step,
which is the control Microsoft says evaluation gives up ({{topic:whyeval}}).

And the most common reason a fix looks as if it did not work has nothing to do with the fix. It is the
conversation you tested it in ({{topic:conversation}}).

## How it works

### From report to reproduction

1. **Get the exact words**, and the turns before them. A paraphrase changes the question. For a failure
   found in testing, the GitHub Copilot harness's **History** view lists past *preview* conversations,
   filterable by status, including **Failed**. For a user in Teams, ask for the message itself.
2. **Start a new chat.** Earlier turns are part of the model's input, and a skill binds when the
   conversation starts.
3. **Ask exactly what the user asked**, including any earlier turns that set the context.
4. **Repeat it in three new chats.** Three out of three is a defect. One out of three is variance, and you
   will not be able to tell whether a fix worked ({{topic:test}}).
5. **Note who you are.** The pane runs with your access. A failure that needs the user's permissions to
   appear will not reproduce for you ({{topic:testidentity}}).

<!-- volatile verified=2026-10 -->
On the GitHub Copilot harness, **New chat** saves the current conversation to History and starts with no
prior context. On the standard harness the equivalent is the **Reset** icon at the top of the test panel.
Saving a topic there does not clear the conversation.
<!-- /volatile -->

<!-- unknown since=2026-10 -->
Whether the GitHub Copilot harness exposes transcripts of real users' conversations in a published channel
has not been checked. The standard harness's are the subject of the curated video below.
<!-- /unknown -->

### Four faults that look the same

Once it reproduces, open the trace for the failing turn. With **End user preview** off, the GitHub Copilot
harness shows it beside the chat and in each History conversation. The full node-by-node reading is in
{{topic:test}}. For diagnosis, find the **first** step that went wrong, since everything after it is
consequence, and sort it into one of four faults:

| Fault | What the trace shows | Fix it in |
|---|---|---|
| **Wrong knowledge** | A Knowledge step that returned nothing useful, or the wrong document | The source, its content or its description |
| **Wrong tool** | A tool or skill ran that should not have, or none ran | That tool's description ({{topic:tooldesc}}) |
| **Bad inputs** | The right tool, called with the wrong values | The input descriptions, or a clarifying question |
| **Unclear instructions** | The right data came back, and the answer misused it | The instructions ({{topic:instructions}}) |

Only the last row is an instructions problem. The habit to break is rewriting the instructions for all four.
An **Error** step means configuration instead: authentication, access, a timeout or moderation.

### Change one thing, then re-ask

Make the smallest change that addresses the fault you found. On the GitHub Copilot harness you do not have to
restart: the next turn picks up a Build edit, including a new tool or a model change. Microsoft's own advice
still applies, though: if a change has not taken effect after a couple of turns, start a new chat. Then re-ask
in three new chats, as you did before the fix.

### Keep what you learned

A reproduction that lives only in your memory is gone by next week. Write down the exact question, the turns
before it, what the trace showed, and the fix. Then put the case in the evaluation set ({{topic:testsets}}).

<!-- volatile verified=2026-10 -->
Both harnesses help you keep evidence. The GitHub Copilot harness lets you leave thumbs up or down with a
written comment below any preview response, to track quality patterns as you iterate. The standard harness can
**Save snapshot** from the test panel: a `.zip` holding `dialog.json`, the conversational diagnostics with
detailed error descriptions, and the agent's content.
<!-- /volatile -->

> [!WARNING]
> Microsoft warns that a snapshot file contains all of the agent's content, which might include sensitive
> information. Do not attach one to a ticket in a public repository.

## In practice at Technik

A planner writes: *"Asked about blocked work orders on 2031 and it said none, but I know 100004521 is stuck
at cladding."*

**Reproduce.** Asked for the exact message, the planner pastes it from Teams: *"any blocked WOs on 2031?"*. In a new chat
the assistant answers *"No work orders on `PRJ-2031` are blocked."* Three new chats, three times the same
answer. A defect, not variance.

**Diagnose.** The trace shows `Get work order status` ran with `PRJ-2031` and returned
`100004521` with its current operation, cladding, `INPROC`. No QN lookup ran. In the scenario, *blocked*
means an `INPROC` operation **plus** an open notification on that work order; there is no blocked flag
to read. The agent had half the data and called the work order fine.

That is the **wrong tool** row: a tool that should have run did not. The `Get open QNs` description talks about
*"open quality notifications for a project"* and says nothing about blocking.

**Fix one thing.** One sentence goes into the `Get open QNs` description: *"Also use when asked whether work orders
are blocked: a work order is blocked when its current operation is INPROC and an open QN names it."* The next
turn calls both tools and names `100004521`, blocked by QN `300001234`. Three new chats agree.

**Keep it.** The planner's wording, abbreviations and all, goes into the evaluation set as a case
with its expected response: *must name `100004521`; must name the open QN; must not say none are blocked*.

## Design guidance

- **Reproduce from the user's exact words**, with any turns that came before them.
- **Start every meaningful test in a new chat.**
- **Run it three times** before calling it a defect, and three times after the fix.
- **Classify the fault before you fix it**: knowledge, tool, inputs or instructions.
- **Change one thing**, the one the trace points at.
- **Write every reproduced case into the evaluation set.** A fix with no case can quietly come undone.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The fix "did not work" | Tested in the conversation that showed the bug | Start a new chat; re-ask three times |
| Cannot reproduce the user's problem | A paraphrase, or missing earlier turns | Get the exact words and the turns before them |
| It fails for the user, never for you | The pane runs with your access | Test as an account like theirs ({{topic:testidentity}}) |
| Instructions keep growing, the problem stays | Every fault treated as an instructions fault | Classify with the trace; fix where it points |
| A fixed bug returns two weeks later | The reproduction was never kept | Add it to the evaluation set |
| Sensitive content turns up in a bug report | A standard-harness snapshot was attached | Share the diagnostics you need, not the snapshot |

## Key terms

**Reproduction**: the exact question and context that make a reported problem happen, on demand.

**History**: the GitHub Copilot harness's list of past preview conversations, each with its trace.

**New chat / Reset**: starting a conversation with no prior context, on the GitHub Copilot and standard harness.

**Snapshot**: a standard-harness download of the test conversation's diagnostics and the agent's content.

**Fault class**: wrong knowledge, wrong tool, bad inputs or unclear instructions; one fix each.
