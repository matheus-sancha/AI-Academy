## TL;DR

A skill you upload does not reach the conversation you are in. Saved instructions do, on the very next reply.
The guided build is shaped around that pair. **Keep one conversation for the whole build**, because every skill
reads what the earlier ones established. **Change nothing in the agent until stage 7**, because a skill uploaded
mid-build would not be live and instructions pasted mid-build would rewrite the agent you are building with.
Then **open a new chat before you test**, because the build conversation is still bound to the agent as it was.
One conversation for the build, one new chat before the test.

## Why it matters

The two rules of the route look like they contradict each other: never leave this conversation, and always
start a new one. Readers who don't know why both hold break the build in one of two ways. Some apply things as
they go, which is what every other tutorial teaches, and some restart the chat whenever something seems not to
work, which is the right reflex everywhere else in this level. Either one costs the build.

There is a quieter cost too. The route defers so much that a reader who does not know the reason starts
improvising, and an improvised build is one nobody can recover when the thread is lost.

## How it works

### Two bindings, opposite directions

{{topic:conversation}} sets out what reaches a running conversation. Two rows matter here:

<!-- verified tenant=2026-09 -->
| You changed | Reaches a conversation already running? |
|---|---|
| **Instructions**, saved | **Yes**: a token added mid-conversation appeared in the very next reply |
| **A skill**, uploaded | **No**: a skill that looked inert became active in a new chat, unchanged |
<!-- /verified -->

Microsoft's testing page for this harness says the next turn picks up Build edits, that *"structural changes
such as adding a new tool, changing the model, or turning on Memory apply the same way"*, and that *"you don't
need to start a new conversation"*. That is true of what it lists. Skills are not on the list, and the skill row above was observed, not read. Do not
let the general advice talk you out of a new chat after an upload.

### Why the build stays in one conversation

Each skill reads what the earlier stages established: the brief, the draft, the plan. A new chat starts with
none of it. So the route puts the six skills on the agent first, then one **New chat** to make them live, and
that chat is the build. The router says this in its first message, before stage 1.

If the conversation is lost anyway, the recovery is a file. Re-upload `agent-brief.md` and say which stages you
finished. With no brief, you start at stage 1. A half-remembered brief produces an agent nobody checked. Stage 2
is the exposed one, because its draft never became a file. Lose the conversation after stage 2 and expect to
redo that draft.

### Why nothing is applied until stage 7

Deferring costs nothing. No stage needs an installed component to be running, and stage 5 only has to *name*
the tools and skills, not call them. Applying early costs something either way:

- **A skill uploaded mid-build** is not live in the build conversation. Making it live means a new chat, which
  throws the build away.
- **Instructions pasted mid-build** land on the next reply. From then on, the agent you are building *with*
  follows the instructions of the agent you are building.

Tools sit between the two. Microsoft says an added tool reaches the next turn. The route defers tools anyway,
so nothing depends on it.

### Why a new chat before you test

Stage 7 applies everything in one pass, and its checklist's step 5 is *start a new chat, then test*. The router
calls it the one people skip. The build conversation was bound before any of it existed: it has no
`qn-write-up`, and it carries weeks of design history that would steer every answer.

<!-- unknown since=2026-10 -->
Whether deleting a skill removes it from a conversation that is already running. Deletion has not been tested
the way upload was. If deletion behaves like upload, the build conversation still has the six `copilot-*`
skills after stage 7's step 1.
<!-- /unknown -->

### The false diagnosis

Mid-build, the agent may tell you a skill is broken. Ask it to read a packaged skill's own `SKILL.md` and it
finds a storage pointer, not the body, and reports the package as empty ({{topic:packaging}}). It is not empty.
Ignore the diagnosis and open a new chat: what the agent says about its own files is not a test of them.

## In practice at Technik

You are at stage 4 of the Production Assistant build. `copilot-skill-creator` has just handed back
`qn-write-up.zip`, and you want to see it work, so you upload it and ask the build conversation to *write up the
porosity on `XT-V2-1042` as a QN*. The answer is plain prose. Then:

1. **You open a new chat to make the skill live.** It works: the draft follows the QN template.
2. **You go back to the build** and ask what comes next. The new chat has never heard of the brief. The router
   asks its placement question.
3. **You recover.** You re-upload `agent-brief.md` and say *stages 1, 3 and 4 are done*. The stage 2 draft was
   only ever in the old conversation, so it gets redone.

Nothing was broken, and the afternoon is gone anyway. The route would have had you save `qn-write-up.zip` and
upload it at stage 7, after step 1, then test in one new chat.

The opposite case is quicker. At stage 5 you paste the revised instructions into **Build** > **Instructions**
"just to check they save". The next reply comes from an agent whose `<role>` says it answers supervisors about
work orders, and the build conversation now has a production assistant in it. Put back what the field held
before, save, and keep `instructions.md` for stage 7.

## Design guidance

- **Upload the six, open one new chat, and build there.** Nowhere else.
- **Save every file the moment you get it**, and record which stage you are on.
- **Treat stage 2's draft as fragile.** It is the only output that is not a file.
- **Do not apply anything to see it work.** Stage 7 is when you see it work.
- **New chat before every test after stage 7**, and before deciding a skill is broken.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A newly uploaded skill is ignored | Skills do not reach a running conversation | New chat, or wait for stage 7 if you are mid-build |
| The router asks where you are, mid-build | You are in a new conversation | Re-upload `agent-brief.md` and name the finished stages |
| The build agent starts answering as your agent | Instructions were pasted mid-build | Remove them; apply at stage 7 |
| The agent says its own `SKILL.md` is empty | It read the storage pointer, not the body | Ignore it; new chat |
| Stage 7 tests look like nothing changed | Testing in the build conversation | Step 5: new chat, then test |
| It asks for something you already gave it | You are in a new conversation | Re-upload the brief; say which stages finished |

## Key terms

**Build conversation**: the one Preview chat the whole route runs in, opened after the six skills are uploaded.

**Deferral**: the route's rule that nothing is applied to the agent before stage 7.

**Stage 7**: the only stage that changes the agent. It deletes the six, applies the build and ends in a new chat.
