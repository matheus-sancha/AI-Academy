## TL;DR

Agent instructions are a long-lived system prompt: identity, scope, rules, tone, and — with
generative orchestration — guidance on when to use which knowledge and tool. They are read on
**every single request**, so every word costs tokens on every turn. Write them structured, specific
and short, and test them against real questions rather than admiring them.

## Why it matters

Instructions are the one part of an agent that affects every answer. They are also where people put
everything they cannot think where else to put, which is how a 200-word instruction becomes a
1,500-word one that makes the agent slower, more expensive and worse at the thing it was originally
good at.

The discipline is knowing what belongs here and what belongs somewhere cheaper: a topic, a tool
description, a skill, or a knowledge source.

## How it works

Instructions are sent with every request, ahead of the conversation. Four consequences:

**Everything in them is paid for on every turn.** A rule about drafting notifications is read when
someone asks about PPE. That is fine at 300 words and wasteful at 1,500 — see
[Context](../B1/context.html).

**Position matters.** Models attend most reliably to the beginning and end of a long block. A
critical rule buried in the middle of twelve paragraphs is the one that gets ignored.

**They guide orchestration.** With generative orchestration, instructions influence which knowledge
is searched and which tool is called, alongside the tool descriptions themselves.

**They are not enforcement.** An instruction is a strong suggestion. Anything that must be true
every time belongs in a query, a tool's fixed inputs, a topic or a flow. This distinction runs
through the whole course.

### Structure

Write them as sections, not prose. XML-style tags or headings both work; the point is that the model
can tell where one concern ends and the next begins — the idea from
[B2](../../beginner.html#B2), applied to a system prompt.

```xml
<identity>
Who the agent is and who it serves.
</identity>

<scope>
What it covers. What it does not, and what to say instead.
</scope>

<grounding>
Answer only from knowledge and tools. Cite sources. Say so when you cannot find something.
</grounding>

<style>
Tone, language, length, format.
</style>

<rules>
The specific things that must always or never happen.
</rules>
```

### What belongs here, and what does not

| Put it in instructions | Put it elsewhere |
|---|---|
| Identity, scope, boundary | A scripted exchange → a **topic** |
| Tone and language | A procedure for one kind of task → a **skill** (B8) |
| Grounding and citation posture | How to call one system → a **tool description** (B7) |
| Rules that apply to every answer | A rule that must be guaranteed → a **query filter** or a **flow** |
| Which source wins when two disagree | Domain facts → **knowledge** (B6) |

The last row on the left is worth noticing: source precedence is a genuine instruction-level rule,
because it applies to every answer and there is nowhere else to put it.

## In practice at Technik

The Technik Production Assistant's instructions grow across four modules, and each addition is
justified by something that went wrong:

| Added in | Rule | Why |
|---|---|---|
| B5 | Identity, scope, tone, boundary | Otherwise it answers everything, in a marketing voice |
| B6 | Answer only from sources; name the document; prefer the controlled document over a summary; quote criteria exactly | An intranet summary can go stale and still retrieve perfectly |
| B7 | Check whether open operations sit on a superseded revision; name only work orders actually retrieved | A true answer to the wrong question is still wrong |
| B11 | Moderation and injection handling | Notification text is written by people |

By B11 that is around 400 words, read on every turn, and that is close to the sensible limit. When
it needs to grow beyond that, the right move is not a longer instruction but moving a concern into a
skill or a tool description where it is only read when relevant.

Two rules from that table are worth quoting, because they show the difference between an instruction
that works and one that reads well:

> Answer only from your knowledge sources. If they do not cover the question, say so plainly and do
> not answer from general knowledge.

That changes behaviour: it is testable, and you can write a question that proves it.

> Be helpful and accurate.

That changes nothing. Every model is already trying to be both.

> [!TIP]
> Before adding a rule, ask: *what question would fail today and pass afterwards?* If you cannot name
> one, the rule is decoration and it will cost tokens on every turn forever.

## Design guidance

- **Structure it.** Sections or tags, one concern each.
- **Be specific and negative.** "Never invent a part number" beats "be accurate".
- **Put the critical rules at the top**, not in the middle.
- **Keep it short.** 300–500 words is plenty for most agents.
- **Every rule earns its place by fixing a real failure**, with a question that demonstrates it.
- **Do not use instructions for guarantees.** Constraints live in queries, tools, topics and flows.
- **Re-test the whole set after every change.** Instructions interact.
- **Version them.** Keep the text somewhere you can diff, not only in the maker portal.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A rule is followed sometimes | It is an instruction, not a guarantee | Move it into a query, a tool input or a flow |
| Adding a rule broke something else | Instructions interact; a new rule out-competed an old one | Re-test everything, not just the new case |
| The agent ignores a rule in the middle of a long block | Attention falls off mid-context | Shorten; move critical rules to the top |
| Answers got slower and vaguer over time | Instructions grew without pruning | Move task-specific guidance to skills and tool descriptions |
| Nobody knows why a rule is there | No record of what it fixed | One line of comment per rule, in your source copy |
| Instructions were lost in a rebuild | They only existed in the portal | Keep them in version control |

## Key terms

**Instructions** — the long-lived system prompt read on every request.

**Generative orchestration** — the model choosing knowledge, tools and topics based on descriptions
and instructions (B4).

**Grounding posture** — whether the agent may answer from general knowledge (B6).

**Source precedence** — which source wins when two disagree. An instruction-level rule (B6).

**Guarantee** — something that must be true every time. Never an instruction.
