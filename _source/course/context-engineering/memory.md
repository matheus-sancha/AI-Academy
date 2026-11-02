## TL;DR

Short-term memory is the conversation you are already managing ({{topic:history}}). **Long-term
memory** keeps facts across sessions, and it is a governance decision before it is a context
decision: what may be remembered, for how long, and how a user sees or removes it. Copilot Studio
offers it as a per-user store you switch on per agent.

## What it is

<!-- volatile verified=2026-11 -->
Memory in Copilot Studio is documented for agents on the GitHub Copilot harness, as a
production-ready preview. It "helps an agent remember details from its interactions and use that
context for future interactions", in three steps — capture signals such as preferences and relevant
context, store them as files in a per-user folder in Microsoft-managed storage, then read them back
on later interactions. The maker turns it on with the **Memory** toggle on the **Build** tab.

The governance answers are given, not left to you:

- **Scope.** "Each agent maintains a separate memory store for every user, so one person's context
  is never shared with another."
- **Retention.** "If a user doesn't interact with the agent for 28 days, the system deletes their
  memories from that agent." Turning Memory off "doesn't delete stored memories. It only prevents
  the agent from using them."
- **Visibility.** Memory is "transparent and user-controlled": a user can ask the agent in chat what
  it remembers, update or forget one item, or open the memory portal to **View memories** or
  **Delete all memories**. Makers cannot see any of it.
- **Exclusions.** "User memory is disabled in group chats and Microsoft Teams channels."

Agents on the Customer Conversation harness have a separate memory capability with its own retention
and configuration.
<!-- /volatile -->

Note what memory is *not*. {{topic:workiq}} grounds an agent in a user's organisational content and
gives it persistent working storage — retrieval and scratch space, not remembered facts about a
person. The two solve different problems, and only one of them needs a retention policy.

## Where it fits at Technik

The Production Assistant has one obviously good candidate and one obviously bad one.

Good: the reader's own working context — their plant, the document types they ask about, that they
want codes spelled out. That is a stable preference, cheap to re-earn if it is lost, and harmless if
it is wrong.

Bad: anything the data owns. A remembered *"revision C of `SWI70000318` is the released one"* is a
fact that was never true and would be acted on in the shop. Revision statuses, QN dispositions and
operation links are looked up every time, which is why the capstone's agent remembers nothing and
answers only from tool results ({{topic:jit}}, {{topic:ctxsecurity}}).

The test is simple: if being stale would make a reader do the wrong thing, it is not a memory. It is
a lookup.

## Key terms

**Short-term memory** — the current conversation, managed as history.

**Long-term memory** — facts or preferences an agent keeps across sessions, stored per user and
outside the context window.

**Retention** — how long a stored memory survives; in Copilot Studio, deleted after 28 days of no
interaction with that agent.
