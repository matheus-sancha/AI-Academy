## TL;DR

A **channel** is where users meet the agent: Teams, Microsoft Copilot, a website, an app. Each one brings its
own authentication, its own formatting and its own limits, so an answer that looks right in the preview pane
can arrive broken, or not arrive, in the channel people actually use. The GitHub Copilot harness offers fewer
channels than the standard harness: **Microsoft Copilot, Teams, a demo website and a web app**, with MCP and
A2A in preview. Choose the channel from where your users already work, then test the agent there.

## Why it matters

The preview pane is a channel too, and the most forgiving one. It renders everything, runs as you, and has no
team chats, no mobile client and no app store. Every other channel takes something away. Teams renders Markdown
only partly. Microsoft Copilot strips embedded links. A Teams group chat can't use SharePoint knowledge at all.

None of that shows up until someone uses the agent where it lives. The cheapest moment to find it is before
the agent is shown to anyone, by publishing to yourself and asking the same questions in the real channel
({{topic:publish}}).

## How it works

### What each harness offers

<!-- volatile verified=2026-10 -->
| Channel | GitHub Copilot harness | Standard harness |
|---|---|---|
| Microsoft Teams | Yes | Yes |
| Microsoft Copilot | Yes | Yes |
| Demo website | Yes | Yes |
| Web app / custom website | Yes (iframe) | Yes |
| MCP client, A2A client | Preview, early-release environments only | — |
| SharePoint | No | Yes |
| Native or mobile app (Direct Line) | No | Yes |
| WhatsApp, Facebook, Slack, Telegram and other messaging | No | Yes, several through Azure Bot Service |
| Contact-centre platforms | No | Yes, some |
<!-- /volatile -->

The **No** column is not permanent. Microsoft's GitHub Copilot harness page lists those channels with
*Currently available?* set to *No*, and they will change. Check the page before promising a channel.

Administrators can also turn channels off. A channel blocked by a data policy, or by the agent's authentication
setting, appears disabled; the information icon beside it says why ({{topic:dlp}}).

### Authentication goes with the channel

Teams and Microsoft Copilot support only **Authenticate with Microsoft**: the user is who Teams says they are,
and that identity is what knowledge sources and user-credential tools see ({{topic:agentauth}}). Websites and
apps are where the other options live, and where *No authentication* means *anyone with the link*.

### Rendering differs

Microsoft's standard-harness reference table shows how far channels diverge:

| Experience | Website | Teams and Microsoft Copilot |
|---|---|---|
| Markdown | Supported | **Partially** supported |
| Multiple-choice options | Supported | Up to **six** |
| Satisfaction survey | Adaptive card | Text only |

Microsoft Copilot adds its own limits: it doesn't render media such as GIFs, *might remove embedded URLs for
security* (so links belong in citations), and on the standard harness agents published there don't support
reactions. Teams applies **rate limiting** to agents, which is one more reason to keep answers short.

### Teams: personal, team and group chats

In Teams an agent can be installed for one person, or added to a **team channel** or a **group or meeting
chat**, where everyone sees its answers. That last option comes with a limit that is easy to miss: *in Teams
group chats and channels, Copilot Studio agents can't use knowledge sources that require end-user
authentication, such as SharePoint*. Microsoft says this is by design, to prevent unintended data exposure.
Those agents are supported only in **1:1 chats**.

### Making it findable

<!-- volatile verified=2026-10 -->
On the standard harness, the Teams and Microsoft Copilot channel offers four routes to users: an **installation
link** (which can't be used in the Teams mobile app), the **Built with Power Platform** section of the Teams app
store (shared users only, up to a tenant limit), **Built for your org** after **admin approval**, which also
reaches the Microsoft 365 Agent Store, and an admin's **app setup policy** to install and pin it for people.
The GitHub Copilot harness's publish dialog offers to add the agent to the **organisation catalog**.
<!-- /volatile -->

Whichever route you use, people still need to be **shared** on the agent to chat with it ({{topic:share}}).

## In practice at Technik

The Production Assistant is published to **Teams** and **Microsoft Copilot**, the two places Technik's planners
and engineers already work, and nothing else. A website would need a different authentication choice and buys
nothing for internal users.

Testing the published agent in Teams found two things the preview pane hadn't:

1. **The QN list.** In the preview, *"Show open QNs on cladding for project `PRJ-2031`"* came back as a clean
   table. In Teams, a long list with descriptions was hard to read on a laptop and unreadable on a phone. The
   output rule became: number, defect type and priority only, with the description on request.
2. **The shift channel.** A supervisor asked for the agent in the Plant 1 shift team's channel. In the channel,
   *"Which document covers weld prep inspection?"* got no answer from SharePoint, because group chats and
   channels can't use knowledge that needs the user's own sign-in. Work order questions, which come through the
   Snowflake tool, worked fine.

The decision went into the brief: the agent is for **1:1 chats**. A channel version that answers only work order
questions is possible, but it would be a different agent with a different description, and nobody asked for it.

## Design guidance

- **Choose channels from where users already work.** For internal agents, usually Teams and Microsoft Copilot.
- **Check the harness's channel list** before promising a channel. The GitHub Copilot harness offers fewer.
- **Write answers for the narrowest channel** you publish to: short, plain Markdown, links in citations.
- **Keep knowledge-backed agents to 1:1 chats** in Teams, or design for the group-chat limit deliberately.
- **Test the published agent in every channel** you publish to, including the Teams mobile app if users have it.
- **Use an app store route, not a link,** if people use Teams on mobile.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A channel can't be selected | Blocked by policy, or by the authentication setting | Read the info icon; see {{topic:dlp}} and {{topic:agentauth}} |
| Tables and formatting arrive broken | Teams supports Markdown only partly | Simplify the output; test in Teams |
| Links vanish in Microsoft Copilot | It may remove embedded URLs | Put links in citations |
| No document answers in a team channel | Group chats can't use knowledge needing user sign-in | Use 1:1 chats, or design without that knowledge |
| Mobile users can't install it | Installation links don't work in Teams mobile | Use the app store routes |
| The channel you planned is missing | Not available on the GitHub Copilot harness | Check the channel list before you choose the harness |

## Key terms

**Channel**: a place users reach the agent, each with its own authentication, formatting and limits.

**Demo website**: a prebuilt test page for teammates. Not a production channel.

**Built with Power Platform / Built for your org**: Teams app store sections for shared users, and for
admin-approved agents.

**1:1 chat**: a personal Teams conversation with the agent, the only place SharePoint knowledge works.
