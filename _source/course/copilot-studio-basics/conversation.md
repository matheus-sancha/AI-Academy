## TL;DR

A conversation is the unit that holds history: every turn, the agent works from what has been said so far
as well as from what you built. And not everything you built is read fresh each turn — **saved
instructions reach a conversation already running, but an uploaded skill does not**. So a skill that
installed correctly and one that failed to install look exactly the same until you open a new chat.
Starting a new chat is the first diagnostic step for most apparent failures, and the step people skip.

## Why it matters

Most of the time spent debugging a first agent is spent debugging the wrong thing. You change something,
ask again in the same chat, get the old behaviour, and conclude the change did not work. Then you change
it again — rewording, re-uploading, repackaging — and every one of those edits is aimed at a problem that
was never there. The problem was the conversation you tested in.

That is why this lesson comes before anything you will build. The rest of this level keeps returning to it:
the first step in {{topic:manual}}, the whole of {{topic:notrunning}} and the first thing to check in
{{topic:whenitstalls}} are all *start a new chat*. It is established here, once.

## How it works

A conversation carries two kinds of state, and they behave differently.

**History accumulates.** Every earlier turn is sent again with the next one, which costs context and
money on every turn ({{topic:contextcost}}), and the orchestrator uses recent history when it decides what
to call — so the same question can be answered differently in a fresh chat and in a long one
({{topic:orchestration}}). That is useful for follow-ups and misleading for tests: an old wrong answer, or a
tool call from before your fix, is still in the context steering the next one.

**Some configuration is bound when the conversation starts.** Saving an edit in Build does not
necessarily change the conversation you are having. What is known about each component:

<!-- verified tenant=2026-09 -->
| You changed | Reaches a conversation already running? |
|---|---|
| **Instructions**, saved | **Yes** — the very next reply follows them |
| **A skill**, uploaded or added | **No** — only a new conversation sees it |
<!-- /verified -->

<!-- unknown since=2026-09 -->
Whether a newly added **tool**, or a newly added **knowledge source**, reaches a conversation already
running. Nobody has tested it. Assume it does not, and start a new chat after adding either.
<!-- /unknown -->

The skill row is the one that costs people hours. Copilot Studio checks a skill when it loads, and a skill
that fails a check — invalid frontmatter, a missing `description`, a name used twice — is **skipped
silently**: the rest of the agent loads and nothing errors. So after an upload, *the agent behaves as
though the skill is not there* has two causes, one harmless and one not, and in the conversation you
uploaded from they look identical ({{topic:addskill}}).

### Starting over, on each harness

<!-- volatile verified=2026-09 -->
On the GitHub Copilot harness, select **New chat** in the Preview header. The current conversation is
saved to **History** and a fresh one starts with no prior context. History shows each past conversation's
status — *Completed*, *In progress*, *Failed*, *Auth required*, *Input required* — and which **agent
version** processed it, which is how you check afterwards whether a test ran against the build you
thought it did.

On the standard harness, select the **Reset** icon at the top of the test panel. Saving a topic does
**not** clear the test conversation; you have to reset it yourself.
<!-- /volatile -->

A new chat is also the documented remedy for two of the GitHub Copilot harness's error codes:
`CONTEXT_LENGTH_EXCEEDED`, where history has filled the model's input, and `CONVERSATION_BUSY`, when the
agent appears stuck on an earlier turn. The agent processes one turn at a time per conversation, so a
second message cannot start until the first has finished.

### Conversations after publishing

In Teams, users do not start new chats to suit you. A published agent lives in long-running threads, with
history building up for days, which is why a fault reported from Teams may not reproduce in Preview —
and why {{topic:contextcost}} names long threads as a place limits bite. Monitor reports on **sessions**,
the production view of the same unit.

## In practice at Technik

You have just uploaded the *QN write-up* skill to the Technik Production Assistant, in the Preview chat
you have been using all afternoon. You ask:

> *Draft a QN write-up for `300001234`.*

The answer is a reasonable paragraph in no particular format — nothing like Technik's QN layout. The
tempting conclusion is that the upload failed, and the tempting fix is to re-zip the package and try again.

Instead, in order:

1. **New chat.** Ask the same question. If the reply is now in Technik's format, nothing was wrong: the
   skill was installed, just not bound to the old conversation.
2. **Still generic?** Open Build and look for the skill in the components panel. If it is not listed, it
   was skipped at load; the load-time checks are listed in {{topic:addskill}}.
3. **Listed, but not used?** Now it is a real problem — usually a `description` that does not match how
   people ask ({{topic:skillmd}}).

The same discipline applies the other way. Because saved instructions *do* reach a running conversation,
an instruction edit made mid-test changes the agent you are testing with — which is why the guided build
defers every change to the end ({{topic:notrunning}}).

> [!TIP]
> Make *New chat* a reflex, not a remedy: one new chat before every test that is meant to tell you
> something. It costs nothing and removes the most common false result in the product.

## Design guidance

- **Start a new chat before judging any change.** Always before judging a skill.
- **One question per test chat** when you are checking a specific behaviour; history is a variable.
- **Check History's agent version** when two runs disagree.
- **Do not repackage a skill until a new chat has failed too.** Repackaging a working skill wastes the
  afternoon.
- **Test long conversations deliberately**, because your users will have them.
- **Expect instruction edits to land mid-conversation**, and do not make them in a chat you are relying on.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A just-uploaded skill is ignored | Skills bind when a conversation starts | New chat, then ask again |
| Still ignored in a new chat | The skill failed a load-time check and was skipped silently | Check the components panel; see {{topic:addskill}} |
| A fix appears to have done nothing | History from the old attempt is steering the answer | New chat before re-testing |
| Behaviour changed mid-conversation | A saved instruction edit landed immediately | Expected; do not edit instructions in a chat you are relying on |
| `CONTEXT_LENGTH_EXCEEDED` late in a conversation | History has filled the model's input | New chat; shorten instructions or cut tools if it recurs |
| `CONVERSATION_BUSY` | A previous turn is still running | Wait; if stuck, new chat |
| A Teams user reports a fault Preview cannot reproduce | Their thread has days of history | Reproduce with a long conversation, not a fresh one |

## Key terms

**Conversation** — the unit that holds history; everything said so far travels with every turn.

**New chat / Reset** — start a conversation with no history, on the GitHub Copilot and standard harness
respectively.

**Bound at start** — configuration a conversation picks up when it begins and does not re-read. Skills are;
instructions are not.

**Preview history** — the GitHub Copilot harness's list of past test conversations, with status and agent
version.

**Session** — the unit Monitor reports on in production.
