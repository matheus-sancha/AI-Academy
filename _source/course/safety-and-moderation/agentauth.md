## TL;DR

An agent's authentication setting decides **who can talk to it**, and whether it knows who they are. There are
up to three options: **No authentication**, **Authenticate with Microsoft** (Entra ID, automatic in Teams), and
**Authenticate manually** (an identity provider you configure). The GitHub Copilot harness offers only the first
two. This is a separate question from **whose permissions a tool runs with**, which {{topic:connauth}} answers,
but the two only make sense together. *Run as the signed-in user* means nothing when nobody signed in. An
internal agent over company data requires authentication.

## Why it matters

Agent authentication is the outer door. Everything inside the agent, from its knowledge and tools to the
service account behind them, is reachable by whoever gets through it. With **No authentication**, Microsoft's
wording is plain: anyone who has the link can chat with the agent. Combine that with a tool running as a
service account and you have published that account's view of your data to anyone with the link.

Authentication also unlocks behaviour. SharePoint knowledge, Dataverse knowledge and Microsoft Copilot
connectors use the **agent user's** Entra ID identity to return only what that person may open. With no
signed-in user, those sources have no one to run as.

## How it works

### The options

<!-- volatile verified=2026-10 -->
| Option | Who can chat | Channels | Harness |
|---|---|---|---|
| **No authentication** | Anyone with the link. You cannot restrict it to people in your organisation | Any | Both |
| **Authenticate with Microsoft** | Signed-in users of your tenant; agent sharing can narrow it further | Teams and Microsoft 365, SharePoint, Power Apps, Microsoft Copilot | Both |
| **Authenticate manually** | Users who sign in with the provider you configure | Others too, such as a custom website | Standard only |

On the standard harness the setting is under **Settings** → **Security** → **Authentication**. On the GitHub
Copilot harness it is the **Authentication** drop-down on the **Safety & access** tab of **Agent settings**.
<!-- /volatile -->

**Authenticate with Microsoft** needs no configuration. In Teams the user is already signed in, so they are not
prompted. The **Teams + Microsoft 365** channels support *only* this option. Choose another and those channels
are blocked.

**Authenticate manually** is for everything else: an agent on a public website, a non-Microsoft identity
provider, or a topic that needs the user's token to call an API. Its providers are several Entra ID variants
and generic OAuth 2. Only manual authentication exposes `User.AccessToken`; **Authenticate with Microsoft**
gives you `User.ID` and `User.DisplayName` and nothing to call an API with. Manual authentication also has a
**Require users to sign in** setting. Turned off, users are asked to sign in only when a topic needs it.

### Who exactly can chat

The authentication option decides whether *sharing* the agent can control who talks to it:

- **No authentication**: sharing controls nothing. Select **Share** and Copilot Studio tells you anyone can
  chat.
- **Authenticate with Microsoft**: users are always signed in, and sharing decides which of them may chat.
- **Authenticate manually** with **Entra ID**: sharing works if **Require users to sign in** is on. With
  **generic OAuth 2**, anyone who can sign in can chat, and sharing cannot narrow it.

<!-- unknown since=2026-10 -->
The GitHub Copilot harness's settings page lists its two options and says nothing about sharing. That sharing
limits who may chat with an agent on this harness, as the standard harness's page describes, is not
documented.
<!-- /unknown -->

### Three rules that catch people

- **Authentication changes take effect only after you publish.** Testing a change before publishing tests the
  old setting.
- **Turning authentication off breaks tools that use the user's credentials.** Microsoft's page warns against
  it for exactly that reason.
- **A data policy can take the choice away.** If your administrator blocks *Chat without Microsoft Entra ID
  authentication in Copilot Studio*, **No authentication** is not offered ({{topic:dlp}}).

## In practice at Technik

The Technik Production Assistant is an internal agent in Teams on the GitHub Copilot harness. The choice
almost makes itself: **Authenticate with Microsoft**, the only option Teams supports, and one the harness
offers.

What matters is how it combines with the identities inside the agent:

| Part of the agent | Runs as | What agent sign-in contributes |
|---|---|---|
| SharePoint knowledge (two sources) | The asking user | The user to run as. Without sign-in, these sources have no one |
| Snowflake tools | `TECHNIK_AGENT_RO`, the same for everyone | The only control over who reaches that view |

The second row is why authentication is not optional here. `TECHNIK_AGENT_RO` sees all of Technik's work-order,
QN and revision data, deliberately, because there is no per-user slice to respect ({{topic:connauth}}). That
decision is safe only because the door is shut: people must sign in with a Technik account, and the assistant
is shared with the engineering and quality groups at Plants 1 and 2, not the whole tenant.

Now the cell to avoid. Put the same agent on **No authentication** and nothing in it errors. The SharePoint
sources return nothing, because there is no user. The Snowflake tools carry on as `TECHNIK_AGENT_RO` for anyone
with the link. That is the quiet failure from {{topic:connauth}}, one level up.

Suppose Technik later wants the assistant on a supplier portal outside Teams, with the supplier's own identity
provider. That needs **Authenticate manually**, which the GitHub Copilot harness does not offer. So it is a
standard-harness design: a second agent, its own authentication, and certainly not `TECHNIK_AGENT_RO` behind it.
Matthew Devaney's video in *Go deeper* walks through manual authentication with single sign-on on a website.

## Design guidance

- **Require authentication** for any agent over company data. **No authentication** is for public content only.
- **Choose authentication together with tool identity.** Ask what an unauthenticated user would reach through
  each tool.
- **Use Authenticate with Microsoft for Teams**; it is the only option those channels support.
- **Choose manual authentication for a reason**: another channel, another identity provider, or a token you need.
- **Narrow who can chat through sharing**, where your option allows it.
- **Publish, then test** any authentication change, with a second account.
- **Ask your administrator to block unauthenticated chat** in environments holding company data.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Anyone with the link can use the agent | **No authentication** | Authenticate with Microsoft, or manually |
| SharePoint knowledge returns nothing for anyone | No signed-in user to run the search as | Require authentication |
| The agent stopped appearing in Teams | Authentication changed from **Authenticate with Microsoft** | Teams supports only that option; change it back |
| A topic shows `User.AccessToken` as *Unknown* | Switched to **Authenticate with Microsoft**, which has no token | Use manual authentication, or remove the dependency |
| Tools that used the user's credentials fail | Authentication was turned off | Turn it back on |
| An authentication change has no effect | It applies only after publishing | Publish, then re-test |
| **No authentication** is missing from the list | A data policy requires sign-in | Working as intended ({{topic:dlp}}) |

## Key terms

**Agent authentication**: whether, and how, a user signs in to talk to an agent.

**Authenticate with Microsoft**: Entra ID sign-in configured automatically; the only option for Teams.

**Authenticate manually**: sign-in through an identity provider you configure. Standard harness only.

**Require users to sign in**: the manual-authentication setting that makes sign-in happen at the start rather
than when a topic needs it.

**Agent user authentication**: knowledge sources returning only what the signed-in user may open.
