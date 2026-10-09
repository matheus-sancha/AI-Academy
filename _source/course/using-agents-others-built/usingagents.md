## TL;DR

An **agent** is an assistant a colleague built for one job, with its own instructions and documents.
It turns up in Teams or Microsoft Copilot and answers the way Copilot does: fluently, with citations,
and sometimes wrongly. Judge it the same way. **Read what it cites,
notice when your question is outside its job, and tell whoever published it when an answer is wrong.**
You're the only person who sees the answer, so you're the only one who can.

## Why it matters

An agent feels more official than Copilot: it has a name, an icon, and a colleague built it. That
makes it easy to over-trust.

But it runs on the same kind of model you met in {{module:how-copilot-works}}. Narrowing it to one job
makes it better at that job, not right. And its publisher can't see your conversation, so a wrong
answer you don't report stays wrong for everyone.

## How it works

### Where you find one

<!-- volatile verified=2026-10 -->
Microsoft documents these ways in for agents built in Copilot Studio:

- **In Teams**, from the app store: **Built for your org** lists agents an admin approved for everyone,
  and **Built with Power Platform** lists agents shared with you. Select **Add**, and the agent appears
  in the list on the left.
- **In Microsoft Copilot**, type **@** and pick the agent.
- **In the Microsoft 365 Agent Store**, under **Built by your org**.
- **From an installation link** a colleague sends you. These don't work in the Teams mobile app.

An admin can also pin an agent to your Teams app bar for you.
<!-- /volatile -->

### What it's built from

Its publisher chose its **instructions** (what it's for and how to answer), its **knowledge** (the
documents and sites it answers from) and sometimes **actions** that look things up in other systems.
You can't see the instructions. You can read the description, and what each answer cites.

Where an agent searches SharePoint, it does so as you, so {{topic:visibility}} still holds: it can't
show you a document you couldn't open yourself.

<!-- unknown since=2026-10 -->
Whether a published agent opens for you depends on how it was built and on your organisation's
settings. If one you were sent won't open, ask its publisher, not the help desk.
<!-- /unknown -->

## In practice at Technik

The **Technik Production Assistant** is an agent in Teams. It answers from the Controlled Documents
library and the Standards site, and looks up work orders and quality notifications. Its description says what it won't do: decide what happens to a nonconforming part,
or change any record.

You ask it, in a one-to-one chat:

> *What's the status of work order 100004521, and which document covers the inspection it's waiting
> on?*

It answers that the work order is released and in process at operation `0020`, Cladding, held up by
open quality notification `300001234`, porosity in the overlay. For the inspection it cites work
instruction `SWI70000318`, section 5.

### Auditing the answer

The two halves come from different places.

**The document half** has a citation, so check it as you would in Chat ({{topic:m365chat}}). Open the
PDF. Is it the released revision? Does section 5 say what the answer claims: overlay not less than
3.0 mm at every measurement point? If it cited the *Weld Overlay Acceptance Criteria* page instead,
remember that page defers to the work instruction.

**The status half** was looked up, not cited. Check what you'll act on:
open QN `300001234` if you have access, or confirm with the planner before re-planning around it.

### Asking outside its job

> *Can we accept the porosity and release the unit?*

A well-built agent says that's the assigned quality engineer's decision. If it answers anyway, with no
citation, report it.

## Using it well

- **Read the description first.** It says what the agent was built to answer.
- **Expect a citation for every claim about a document.** None where you'd expect one means a guess.
- **Report a wrong answer to the publisher**, with the question, the answer and what the cited
  document actually says. If the *document* is wrong, tell its owner instead.

<!-- volatile verified=2026-10 -->
The agent's **About** tab in Teams shows its publisher's name, if they filled it in. Agents in Microsoft
Copilot don't support reactions, so a thumbs-down there may reach nobody: tell the publisher directly.
In Teams channels and group chats an agent can't use knowledge that needs your sign-in, such as
SharePoint, so ask in a one-to-one chat. And a publisher's update doesn't reach a conversation already
under way. Type **Start over** to pick it up.
<!-- /volatile -->

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Fluent answer, no citations, on a topic it should know | Outside its documents, answered from general knowledge | Treat it as a guess; ask the document owner |
| Good answers in a one-to-one chat, thin ones in a channel | No SharePoint knowledge in channels | Ask it one-to-one |
| The publisher says it's fixed, you get the old answer | Your conversation predates the update | Type **Start over** |

## Key terms

**Agent**: an assistant built for one job, with its own instructions, knowledge and sometimes actions.

**Publisher**: the person or team who built the agent and made it available.
