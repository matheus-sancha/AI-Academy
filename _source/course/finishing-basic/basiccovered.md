## TL;DR

You now know why Copilot invents things, how to ask for what you actually want, what it can and can't
see inside the company, and how to use it in Chat, the five Office apps and other people's agents
**without taking its word for anything**. That's the whole of this course's first level, and for most
people it's all they need. What it doesn't do is teach you to build an agent. That's a different job,
and a door you can leave shut.

## Why it matters

A course that just stops leaves you guessing which parts were the point. Most of what you read was
detail around a few habits, and the habits are what make Copilot worth using. The detail you can look
up again.

It's also worth being clear about what you can't do yet, so nobody, you included, mistakes finishing
for something it isn't.

## How it works

### Seven habits

These are the level, compressed. Each names the module to reread when the habit slips.

1. **Expect fluent and wrong.** Copilot writes what's likely, not what's checked, and fills gaps with
   plausible invention. {{module:how-copilot-works}}
2. **Leave it little to guess.** Say the goal, the source, the audience and the shape of the answer.
   Split big jobs into checked steps. {{module:prompting}}
3. **Know what it could see.** Copilot searches what you can open and nothing more. A missing
   file has a cause you can name. Some content never goes in at all. {{module:how-copilot-sees-your-work}}
4. **Pick the right place.** Chat for questions that span your work, the app for the file that's open.
   {{module:copilot-chat}}
5. **Start from your own content.** Summaries, tables, decks and replies built from a source you supplied
   are checkable. Ones built from a one-line description are not. {{module:copilot-in-word}},
   {{module:copilot-in-excel}}, {{module:copilot-in-powerpoint}}
6. **Read before it leaves your hands.** A drafted reply or a meeting recap goes out under your name.
   {{module:copilot-in-outlook}}, {{module:copilot-in-teams}}
7. **Judge every assistant the same way.** An agent a colleague built is checked like Copilot, and you
   report what's wrong. {{module:using-agents-others-built}}

Underneath all seven: **open the citation.** It's the one step that turns a fluent answer into one you
can use.

### What it didn't cover

Building agents, connecting Copilot to other systems, changing your organisation's settings, and
automating work. Those need a builder's tools and a builder's responsibilities. If you want them, the
course carries on for engineers, and starts with a readiness check on everything above:
{{module:what-you-already-know}}.

## In practice at Technik

Here's one week of work at Technik, with the habit that matters at each step:

- **Monday.** You turn *"summarise this QN"* into a prompt that names the audience and five headings,
  for quality notification `300001234`. *Leave it little to guess.*
- **Tuesday.** You ask Chat which document covers weld prep inspection. It cites `SWI70000318` and a
  summary page, and you open both before choosing the work instruction. *Open the citation.*
- **Wednesday.** You turn ten supplier material certificates into one table, then check every row
  Copilot added against its PDF. *Start from your own content.*
- **Thursday.** You write the reminder about documents past their review date yourself, let Copilot
  coach it, and read what it changed before you send it. *Read before it leaves your hands.*
- **Friday.** The Production Assistant answers a work order question confidently, outside its job. You
  tell its publisher. *Judge every assistant the same way.*

None of that is building anything, and all of it is work done faster without being done worse.

## Using it well

- **Keep the prompts that worked** where you'll find them again ({{topic:iterate}}).
- **Come back to one lesson, not the level.** Each habit above names its module.
- **When your access changes, reread {{topic:visibility}} and {{topic:missingcontent}}.** A new team
  or a new site changes what Copilot can reach overnight, and so do its mistakes.
- **Keep learning from Microsoft's own material.** It changes faster than any course.

<!-- verified tenant=2026-10 -->
Microsoft's adoption site, *Accelerate your Microsoft Copilot adoption*, links a **Prompt Gallery** of
ready-to-run prompts and an **AI Skills Navigator** of learning playlists. The Microsoft Copilot hub
on Microsoft Learn links **Microsoft Copilot training** and a library of **scenarios** for Copilot. Much
of the hub itself is written for IT staff, not for users.
<!-- /verified -->

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| You stopped using Copilot after one bad answer | The cause was never checked: no source, the wrong one, or a vague prompt | Reread {{topic:hallucination}}, then try again with the document attached |
| You've stopped opening citations | Copilot was right often enough that checking felt optional | Keep checking anything that leaves your hands |
| A colleague asks you to build them an agent | Finishing this level reads as qualification | Point them at a builder, or start the engineers' course |

## Key terms

**Citation**: the link to the source an answer came from. The first thing to open.

**Grounded answer**: one written from content you can open and check, not from the model's training
alone.
