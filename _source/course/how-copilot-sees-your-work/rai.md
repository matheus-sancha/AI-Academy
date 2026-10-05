## TL;DR

Microsoft builds Copilot against six **responsible AI principles**: fairness, reliability and safety,
privacy and security, inclusiveness, transparency, and accountability. They were written for the people
who build AI systems, but they work just as well as a checklist on your own use. Two questions cover
most of it: **who is affected by this answer**, and **how would anyone know if it were wrong?**

## Why it matters

Most of this course is about getting Copilot to give a better answer. This lesson is about what you
*do* with an answer, once it's good enough to use.

Copilot makes text that looks finished cheap to produce. Looking finished is not the same as being
fair, correct or appropriate, and the principles catch the cases where it isn't, before your name is on
it.

## How it works

Microsoft states each principle in one line. Here they are, with what each asks of you as a user:

| Principle | Microsoft's wording | The question for your own use |
|---|---|---|
| **Fairness** | AI systems should treat all people fairly. | Does this answer judge or describe a person or group? On what evidence? |
| **Reliability and safety** | AI systems should perform reliably and safely. | What happens if this is wrong? Have I checked the parts that matter? |
| **Privacy and security** | AI systems should be secure and respect privacy. | Should this content be in an AI tool at all, and in which one? ({{topic:sensitive}}) |
| **Inclusiveness** | AI systems should empower everyone and engage all people, regardless of their backgrounds. | Can everyone who needs this read and use it? |
| **Transparency** | AI systems should be understandable. | Would the reader know where this came from, and what it's based on? |
| **Accountability** | People should be accountable for AI systems. | Am I prepared to stand behind this as my own work? |

Accountability carries the others. Copilot drafts. **You** decide what is sent, signed, filed or acted
on. "Copilot wrote it" explains how a mistake happened. It doesn't move the responsibility.

A reformatted table needs none of this. The principles earn their keep when an answer is about
**people**, feeds a **decision**, or leaves your hands.

## In practice at Technik

### A summary about people

A team lead asks Copilot to summarise last month's Teams chat about delays on project `PRJ-2031`, and
then:

> *Which operators caused the most delays?*

Copilot produces a confident ranked list of names. Run the checklist:

- **Fairness.** The list reflects who was *mentioned* near "delay" in a chat. Whoever reported
  problems most often may top it.
- **Reliability.** No work order, timesheet or quality record was consulted. It's an impression of a
  conversation.
- **Accountability.** If this reaches a performance discussion, it's the team lead's judgement, not
  Copilot's, that a person is held to.

The useful question was a different one: *"What causes of delay were raised in this chat, and which
are still open?"* That's about the work, and every answer can be checked against the messages.

> [!IMPORTANT]
> Don't use Copilot to judge people from their messages. Asking for causes, decisions and open items
> gives you something useful without turning a chat summary into an assessment of a colleague.

### A note that leaves your hands

You draft a note to the plant about a change to the inspection steps in `SWI70000318`, with Copilot's
help. Before sending:

- **Reliability.** Every step in the note matches the released document, section by section.
- **Transparency.** The note names the document and section it comes from, so a reader can check it.
- **Inclusiveness.** Many readers on the floor read English as a second language. Short sentences, the
  steps as a numbered list, and no idioms.

## Using it well

- **Slow down when an answer is about a person.** Ask about the work, not the worker.
- **Scale the checking to the consequence.** Anything that changes what someone does on the floor needs
  every claim checked.
- **Say where a statement comes from** when you pass it on: the document and section, not "Copilot".
- **Write for the reader who has it hardest**: plain words, short sentences, a list where there are steps.
- **Own what you send.** If you wouldn't sign it without Copilot, don't sign it with Copilot.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A ranked list of people from a chat | Asking Copilot to judge people from impressions | Ask about causes and open items instead |
| A note goes out with a step that isn't in the procedure | No check before sending | Check every claim that changes what someone does |
| Readers can't tell what a summary is based on | No source given | Name the document and section |
| "Copilot said so" when a mistake is found | Treating the draft as the decision | The sender is accountable; check before sending |

## Key terms

**Responsible AI**: Microsoft's approach to building AI systems according to six principles.

**Accountability**: the principle that people, not AI systems, are responsible for what is done with
their output.

**Transparency**: the principle that people should be able to understand an AI system, and where an
answer came from.
