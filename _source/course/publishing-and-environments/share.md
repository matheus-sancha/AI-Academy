## TL;DR

Sharing gives people one of two things: the right to **use** the agent, or the right to **work on** it. Share
with users through **security groups**, not names. And know what sharing does **not** share: the agent's
**connections**, its **flows** and the **permissions** behind its knowledge stay exactly where they were. That is
why an agent that works perfectly for its author can be useless or broken for the first colleague who opens it.
It is the same root as {{topic:connauth}} and {{topic:testidentity}}, arriving a third time, now in front of
real users.

## Why it matters

Everything you have tested so far ran as you. The preview pane ran as you, the evaluation ran as you unless you
changed it, and your first published conversation ran as you. You have access to every SharePoint site you
added as knowledge, because you added them. The connections were made with your credentials, because you made
them.

The first colleague has none of that. When they ask a question, the agent searches SharePoint **as them** and
finds what they can open, which may be nothing. A tool whose connection is tied to each user asks them to sign
in or fails. Nothing in the agent changed. The person did.

## How it works

### Two kinds of sharing, per harness

<!-- volatile verified=2026-10 -->
**GitHub Copilot harness.** Select the **Share** icon near **Publish**, and add individual users, security
groups or the whole organisation. This share gives **viewing and testing** rights: people see the agent in their
list, open it and test it, but can't edit it. To let the whole organisation simply **use** it, set
**Organization** to **End user access**. Editing rights come from the **environment's security roles**, not from
the share panel. Microsoft lists the prerequisites: **Authenticate with Microsoft**, the agent published to
**Teams + Microsoft 365** with **Make agent available in Microsoft Copilot** on, and a Copilot Studio per-user
licence for the people you share with.

**Standard harness.** Share for **chat** with individuals, security groups or everyone in the organisation; or
for **collaborative authoring** with individual users, who can view, edit, configure, share and publish but not
delete. Co-authors need the **Environment Maker** role. Two narrower roles exist: **Analytics viewer** for the
Monitor page ({{topic:analytics}}) and **Agent viewer** for running evaluations.
<!-- /volatile -->

Whether sharing can restrict who chats at all depends on authentication. With **No authentication**, anyone
with the link can chat and sharing controls nothing. With **Authenticate with Microsoft**, the user is always
signed in, and sharing decides who can use the agent ({{topic:agentauth}}).

### Use security groups

Share with a **security group** that matches a user group in the brief, not with a list of names. People join
and leave a team without anyone remembering the agent; a group they are added to does the remembering. Microsoft
365 groups that aren't security-enabled can't be used for sharing.

### What sharing does not share

| Thing | What happens | What to do |
|---|---|---|
| **Connections** | Microsoft: *connections are tied to the identity of each individual agent user. This means an agent might work for you but not for other users* | A service principal, an **environment-level connection** with a shared identity, or each user authenticating |
| **Knowledge permissions** | SharePoint answers each user from what **they** can open; the agent abstains on the rest ({{topic:sources}}) | Check the users' access to each source, not yours |
| **Flows** (standard harness) | *Sharing an agent doesn't automatically share the flows in the agent.* The test panel still runs them, so tests pass | Share flows in Power Automate; test as a user |

The flow row is the cruellest: Microsoft notes that *users who don't have access to flows in a shared agent can
still run these flows by using the Test panel*. Your test passes for a reason that doesn't exist in production.

### Check as a user, before users do

The only check that catches all three rows is a real conversation by an account like your users': same groups,
same SharePoint access, no special roles. A tester from each user group in the brief is better.

## In practice at Technik

The Production Assistant is shared with three security groups, one per user group in the brief: planners,
supervisors and quality engineers. Nobody is shared by name.

Its two kinds of data behave differently, by design:

- **Work order and revision data** come through the Snowflake tool, whose connection uses the agent's own
  identity, `TECHNIK_AGENT_RO`. That is the *shared, non-user-specific identity* Microsoft describes. It answers
  everyone the same.
- **Documents and standards** come from SharePoint, as each user.

A planner tried it on the first morning: *"Which document covers weld prep inspection?"* The agent said nothing
in its sources covered it. For the engineer who built it, it named `SWI70000318` with a citation. The planner
couldn't open the quality site where the inspection documents live, so for them the knowledge source was empty.
The agent did the right thing, abstaining rather than inventing ({{topic:citations}}).

Two decisions came out of it. The quality site's owner granted planners read access to released work
instructions, which was an access decision, not an agent one. And a planner, a supervisor and a quality engineer
each became a named tester in *Technik Agents Test* ({{topic:envs}}), so the next change is tried by all three
user groups before anyone else sees it.

## Design guidance

- **Share through security groups** that match the brief's user groups.
- **Decide each connection's identity** before sharing: the user's, or a shared agent identity.
- **Use a shared identity only for data everyone may see.** Least privilege still applies ({{topic:dlp}}).
- **Check knowledge access per user group**, not with your own account.
- **Test as a user from every group** before announcing the agent.
- **Give editing rights deliberately**, through environment roles, not as a side effect of sharing.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Works for you, *"nothing found"* for colleagues | SharePoint answers each user from their own access | Check users' access to each source |
| A tool fails or asks colleagues to sign in | The connection is tied to each user | A shared identity, or individual authentication by design |
| Tests pass, users can't run a flow | Sharing the agent didn't share the flow; the test panel runs it anyway | Share the flow; test as a user |
| A colleague can see the agent but not edit it | GitHub Copilot harness sharing grants view and test only | Assign an environment role for editing |
| Anyone with the link can chat | **No authentication** | Authenticate with Microsoft, then share with groups |
| A leaver still has access | Shared by name | Share with security groups |

## Key terms

**Share for use / chat**: permission to talk to the agent.

**Share for authoring**: permission to change it. On the GitHub Copilot harness, through environment roles.

**End user access**: the GitHub Copilot harness setting that lets the whole organisation use an agent.

**Security group**: a Microsoft Entra group used to share with a role, not a list of people.

**Environment-level connection**: a connection with a shared, non-user identity, which works the same for everyone.
