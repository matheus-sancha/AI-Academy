## TL;DR

Saving keeps your draft; **publishing** makes the latest version live on every channel the agent is connected
to. Copilot Studio won't publish an agent that has no name, description or instructions, which makes the
**description** user-facing copy you have to write, not a field to fill. A published change reaches users only
in a **new session**, so the first conversation after a publish may still be the old agent. Publish to yourself
first, and retest in the real channel, because authentication and rendering there differ from the preview pane.

## Why it matters

Publishing feels like the end of the work. It is the moment the agent stops being tested by the person who
built it and starts being used by people who did not. Three things change at once: **who** is talking to it
(not you), **where** (Teams or Microsoft Copilot, not the preview pane), and **which version** (whatever was
last published, not what you are looking at in Build).

Each of those has caught somebody out. A fix that *"didn't work"* because the user's Teams conversation was
still on the old version. An answer that read well in the preview and arrived in Teams as a wall of asterisks.
An agent nobody opened twice because its description said *"AI assistant for production"*.

## How it works

### Save, then publish

<!-- volatile verified=2026-10 -->
**GitHub Copilot harness.** The first publish opens the **Publish agent** dialog from the chevron next to
**Publish**. It reviews the agent's details, lets you select and configure channels ({{topic:channels}}), and
runs readiness checks: if the name, description or instructions are missing, it shows what to complete. It also
evaluates your organisation's data policies, and a channel blocked by policy can't be selected ({{topic:dlp}}).
When it succeeds, it offers to share the agent or add it to the organisation catalog. Later changes are made in
**Build** and published from the **Publish your changes** dialog; *the new version replaces the previous
published version*.

**Standard harness.** **Publish**, then confirm; publishing can take a few minutes and applies to every
connected channel. Channels are added after the first publish.
<!-- /volatile -->

Either way, nothing you change after publishing reaches users until you publish again.

### When users see the new version

Microsoft's standard-harness guidance explains the delay. To avoid disrupting conversations in progress, *the
latest published content only becomes available after a new session starts*, and in most channels a session
ends after **30 minutes** of inactivity. In channels with persistent conversations, such as Teams, typing
**start over** begins a new session with the latest content at once; otherwise it can take up to **an hour**
after publishing for the new version to take effect.

<!-- unknown since=2026-10 -->
The GitHub Copilot harness pages don't say how long a published change takes to reach an open Teams or
Microsoft Copilot conversation, or whether *start over* applies there.
<!-- /unknown -->

So the first test after a publish is in a **new** conversation, never the one you had open.

### The description is copy

The publish checks make you write a description; the channels show it to people. In Teams and Microsoft
Copilot, the agent's icon, colour, short and long descriptions appear in the app store and on the **About**
tab, which is where a user decides whether to open it at all. Microsoft adds two details that make it worth
getting right the first time: users who installed the agent from a link or from the **Built with Power
Platform** section *don't see changes to an agent's details* until they reinstall, and an admin-approved agent
must be **resubmitted** for approval to change them.

A useful description answers three questions in the user's words: **who it is for**, **what they can ask**,
and **what it will not do**.

### Publish to yourself first

Microsoft's advice for the standard harness: publish the agent *only for yourself* and test the published
version before releasing it to a wider audience, for example by installing it in your own Teams with **Open
the agent in Teams**. And *avoid making your agent widely available in Teams or Microsoft Copilot before it's
fully configured and tested*. The **demo website** is for teammates and stakeholders to try the agent, not for
production, and its URL shouldn't go to users.

What you are checking in the real channel is what the preview pane cannot show: sign-in, what the user's own
access returns ({{topic:share}}), and how answers render ({{topic:channels}}).

## In practice at Technik

The Production Assistant's description, first draft:

> *AI assistant for production and engineering.*

It passed the publish check and told a planner nothing. Rewritten from the brief's users, tasks and out-of-scope
slots ({{module:designing-an-agent}}):

> **Short:** *Work orders, QNs and released revisions, answered from SAP and Teamcenter.*
>
> **Long:** *For planners, quality and manufacturing engineers, and supervisors. Ask for a work order's status and operation,
> efficiency or lead time, open QNs on a project, or the latest released revision of a drawing, part or
> document and the ECN behind it. It can draft a document revision for its owner to review. Data is as of last
> night's SAP replication. It doesn't change anything in SAP or Teamcenter, and it doesn't disposition
> nonconformances.*

The engineer published, installed the agent in their own Teams, and asked *"What's the status of work order
`100004521`?"* in a new chat. The answer was right. Then they fixed a tool description, published again and
asked the same question in the same chat: the old behaviour. In a new chat, the fix was there.

## Design guidance

- **Write the description for the person deciding whether to open the agent**: who, what to ask, what not.
- **Get the details right before wide release.** Installed users don't see changes until they reinstall.
- **Publish to yourself first** and test the published agent in its real channel.
- **Test every publish in a new conversation**, or with *start over* in Teams.
- **Republish after every change you want users to have.** Saving isn't publishing.
- **Keep the demo website for stakeholders**, never for users.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Publish is blocked | Name, description or instructions missing, or a data policy | Complete what the dialog lists; for a policy, see {{topic:dlp}} |
| The fix is published but users still get the old answer | Their session started before the publish | New session; *start over* in Teams; wait out the delay |
| Changed the description, users still see the old one | Installed copies don't pick up detail changes | Users reinstall; admin-approved agents are resubmitted |
| Nobody uses the agent | The description doesn't say what to ask | Rewrite it from the brief's users and tasks |
| Right in the preview, wrong in Teams | Rendering and identity differ in the real channel | Test the published agent where users meet it |

## Key terms

**Publish**: making the latest saved version live on every connected channel.

**Readiness checks**: the publish dialog's checks for a name, description, instructions and data policies.

**Session**: a conversation's unit of time; a new one is needed to see newly published content.

**Short / long description**: the user-facing text in Teams and Microsoft Copilot's store and About tab.

**Demo website**: a prebuilt page for trying an agent with teammates. Not for production.
