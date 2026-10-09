## TL;DR

Copilot in Teams can tell you what a long chat or channel thread has come to, with **Sources** that
open the messages behind each point. Ask what was decided and what is still open, then open those
messages before you act. Two limits catch people out. By default Copilot reads only the last 30 days.
And it can't read the files, images or Loop components shared in the thread.

## Why it matters

A channel thread about a change can run for weeks while you're elsewhere. Scrolling back through sixty
replies to find one decision is slow, and you'll still miss things. Copilot is faster. But it answers
from what it read, and it reads less than the whole thread unless you tell it otherwise.

## How it works

### Where you find it

<!-- volatile verified=2026-10 -->
In a chat, select **Open Copilot** in the upper-right corner. Pick a suggested prompt (**Show more**
lists others) or type your own, then select **Send**. In a channel, open the post's replies first.
In that view, select **Open Copilot**. For a single long thread there's also **More actions** >
**Summarize thread**. It appears once the thread holds at least 1,000 characters of text.
<!-- /volatile -->

Microsoft's suggested prompts include *"Summarize what I've missed"*, *"What did [member] say?"* and
*"What links were shared?"*. Its FAQ says Copilot can help you *"understand open questions, decisions
made, and more"*. That's the useful framing: ask for decisions and open questions, not a retelling.

### What it reads

Microsoft gives two limits:

| Limit | What it means for you |
|---|---|
| **30 days by default** | Copilot reads messages from the last 30 days, counted back from the most recent message, *"unless you specify otherwise"* |
| **Text only** | It *"cannot summarize images, Loop components, or files shared in the chat"* |

So a decision made five weeks ago, or written down in an attached file, isn't in the answer unless
you go and get it. Name the time frame in the prompt, such as *"since the start of August"*. And open
shared files yourself ({{topic:wordask}}).

### Sources

<!-- volatile verified=2026-10 -->
Copilot's answers list **Sources**, which link to the messages a point came from.
<!-- /volatile -->

Those links make the answer checkable, in the same way as the citations in an Outlook summary
({{topic:mailask}}). A point with no source is Copilot's own wording.

## In practice at Technik

`ECN70000042` is released, but it's still waiting for revision C of `SWI70000318`, *Cladding
Preparation and Inspection*. Revision C adds an ultrasonic check before cladding (section 4) and
tightens the porosity limit (section 5). The manufacturing engineering team's channel has a thread
about it: sixty-odd replies over six weeks. A quality engineer back from leave opens it, opens
Copilot and asks:

> *What has been decided about revision C of SWI70000318, and what is still open?*

The answer reads well. Two points stand out:

> *The porosity limit in section 5 is still under discussion. The draft of revision C was shared for
> review.*

The engineer checks both.

**"Still under discussion."** Its sources open replies from the last three weeks, where people mention
the limit. But the limit was agreed five weeks ago, in a reply Copilot never read. Thirty days back
from the latest message doesn't reach it. The engineer asks again, naming the time frame:

> *Read the whole thread since the ECN was released. What was decided about the porosity limit, and
> when?*

This time the agreement is there, with its source.

**"Shared for review."** The draft itself is a Word file posted in the thread. Copilot can't read
shared files, so it can say a draft exists but not what it says. The engineer opens the file and
checks section 5 there.

What's left is the real open question, near the end of the thread: who will do the ultrasonic check
before cladding? Nobody has answered it. The catch-up took ten minutes, not an hour.

## Using it well

- **Ask for decisions and open questions**, not for everything that was said.
- **Name the time frame** when a thread is older than a month.
- **Open the sources** behind any point you'll act on.
- **Open shared files yourself.** Copilot can't read them.
- **Read the last few replies.** That's where a thread changes direction.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Something "still under discussion" was settled long ago | The answer read only the last 30 days | Name the time frame in the prompt |
| The answer mentions a file but not what it says | Copilot can't read files, images or Loop components in the thread | Open the file |
| No **Summarize thread** option | The thread is under 1,000 characters | Read it, it's short |
| A point you can't find in any message | It has no source | Don't act on it until you find the message |

## Key terms

**Chat**: a conversation between named people in Teams, one-to-one or in a group.

**Channel**: a shared space inside a team, where posts and their replies are visible to the team's
members.

**Thread**: a channel post and all its replies.

**Sources**: the links under a Copilot answer that open the messages it drew on.
