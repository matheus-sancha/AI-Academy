## What this module is for

The Technik Production Assistant can now answer, look things up and follow procedures. Before anyone else
uses it, four questions need an answer, and each of them is a setting or a policy rather than a feature:

- **What will it refuse to say?** Content moderation, and how strict it is.
- **What happens when something it reads tries to give it orders?** Prompt injection, and the layers that
  contain it.
- **What is it allowed to connect to, and where does the data go?** Data policies.
- **Who is allowed to talk to it?** Agent authentication.

None of the four is a single switch that makes an agent safe. Each is a trade with a cost on both sides, and
the module's recurring point is that you settle each one on evidence: a set of real questions, an injected
record with a pass condition, a written policy footprint, a second account.

## Before you start

You want {{topic:connauth}} first. It decides whose permissions a tool runs with, and three of these four
lessons lean on it, `agentauth` most of all. {{topic:xml}} explains why tags cannot protect retrieved content,
which `injection` builds on. {{topic:genai}} introduced the moderation setting, and `moderation` carries on from
its settings review. {{topic:hitl}} is where approvals were placed, and `injection` reuses them as a layer.

Nothing here needs a tenant to read. Two lessons end with something to take to your administrator. Allow
about 60 minutes.

## What you will be able to do

By the end of this module you should be able to:

- explain what Copilot Studio's content moderation checks, and when;
- choose a moderation level from a vocabulary set rather than a default, and re-test it in both directions;
- tell a direct prompt injection from an indirect one, and name the layers that defend against each;
- say which injection outcome least privilege does not stop, and how you test for it instead;
- recognise a data-policy block from the places Copilot Studio reports it;
- write an agent's policy footprint and say where its data goes;
- choose an agent authentication option for a given channel and harness;
- explain why agent authentication and tool identity have to be decided together.

## The thread through this module

One agent, four reviews, all run before it is published.

{{topic:moderation}} runs a twenty-question vocabulary set, heavy on *crack*, *failure* and *kill wing valve*,
against the assistant's **High** moderation level, and fixes scope in the instructions before it touches the
level. {{topic:injection}} takes the two quality notifications in Technik's data that carry injected
instructions, `300001267` and `300001270`, and walks each through five layers. One attack is finally caught by an
approval. Against the other, only the instruction and the test stand. {{topic:dlp}} writes the assistant's policy
footprint, connector by connector, and asks the administrator to block unauthenticated chat. {{topic:agentauth}}
picks **Authenticate with Microsoft** and shows why `TECHNIK_AGENT_RO` is only safe behind it.

## Self-check

<details>
<summary>1. Engineers report that the assistant sometimes refuses questions about weld cracks. A colleague proposes dropping moderation to Minimum. What do you do instead?</summary>

Measure first. Run a vocabulary set of real questions in the engineers' words and record every
`CONTENT_FILTERED`. If something is being refused, start with the instructions: say who the agent serves and
that defect terms are routine there. That is Microsoft's own first remedy for legitimate input that trips the
filter.

Only then go down one step, and re-test in both directions: the vocabulary set *and* probes that must still be
blocked. Going straight to **Minimum** fixes the complaint by removing the check you cannot see failing
({{topic:moderation}}).
</details>

<details>
<summary>2. The assistant reads Snowflake through a read-only role. Does that make it safe against prompt injection?</summary>

Against injected *actions*, mostly. A read-only role cannot be talked into a write. Against injected *answers*,
not at all. QN `300001267` asks the agent to report an open notification as closed, and hiding a row is a lie,
not a write. Nothing in the role notices.

Against that, the defences are the rule in `<rules>` that retrieved content is data, and an evaluation case
that fails if `300001267` is missing from the open list ({{topic:injection}}).
</details>

<details>
<summary>3. You add the Snowflake tools to the assistant and Publish greys out with an error banner. Nothing in the tools looks wrong. Where do you look?</summary>

At the data policy, before the tools. Open **Channels**, expand the error, and download the details: one row per
violation. The likely causes are a blocked connector, or two connectors that are each allowed but sit in
different data groups, which counts as a violation on its own.

The fix is a conversation with your administrator, ideally with the agent's policy footprint in hand. Better
still, have that conversation before you build ({{topic:dlp}}).
</details>

<details>
<summary>4. A maker sets a new internal agent to No authentication "just for testing", with tools that run as a service account. What has actually been published?</summary>

The service account's view of the data, to anyone who has the link. No authentication means sharing cannot
restrict who chats. Nothing errors, so nothing tells you. Any SharePoint knowledge quietly returns nothing, because
there is no user to search as.

Require authentication from the start, and remember that authentication changes apply only after publishing, so
"just for testing" is a published state ({{topic:agentauth}}).
</details>

<details>
<summary>5. Technik wants the assistant on a supplier portal, with suppliers signing in through their own identity provider. Can the existing agent do it?</summary>

No. A non-Microsoft identity provider needs **Authenticate manually**, and the GitHub Copilot harness offers only
**No authentication** and **Authenticate with Microsoft**. Teams also supports only **Authenticate with
Microsoft**, so one agent cannot serve both.

It is a second agent on the standard harness. It also should not inherit `TECHNIK_AGENT_RO`, which was scoped
for Technik's own engineers, not for suppliers ({{topic:agentauth}}, {{topic:connauth}}).
</details>
