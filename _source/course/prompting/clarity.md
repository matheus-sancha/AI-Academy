## TL;DR

A vague prompt gets a vague answer, because the model fills every gap you leave with whatever is most
typical. Microsoft's guidance for Copilot names four things a good prompt states: the **goal** (what you
want done), the **context** (why, and for whom), the **source** (what to work from) and the
**expectations** (length, tone, format, and what to do when the source runs out). The aim is Microsoft's
own: leave as little as possible to interpretation.

## Why it matters

*"Summarise this QN"* is a perfectly reasonable thing to ask a colleague, because a colleague knows who the
summary is for, how long it should be and that it mustn't guess. Copilot knows none of that. Each unstated
choice gets the most generic answer available: a medium-length paragraph, pitched at nobody in particular,
that sometimes adds a likely-sounding detail the document never contained ({{topic:hallucination}}).

Being specific is not about being polite or wordy. Each detail you add removes one way the answer could
miss.

## How it works

Microsoft's training for Copilot Chat breaks a prompt into four elements:

| Element | The question it answers | Example |
|---|---|---|
| **Goal** | What do you want Copilot to do, and what should come back? | *Summarise this QN as five short headings* |
| **Context** | Why do you need it, and who is it for? | *For tomorrow's production meeting; the team leads don't read SAP codes* |
| **Source** | Where should it look? | *Use only the QN text below* |
| **Expectations** | How should it be delivered? | *Under 120 words, plain language, every code spelled out* |

The goal is the only element you can't leave out. The other three are what turn a reasonable answer into
the one you needed.

Two more habits come from Microsoft's prompt engineering guidance:

- **Give it an out.** Tell it what to do when the source doesn't cover something: *"If the QN doesn't say,
  write 'not stated'."* Without one, the most likely completion is an answer, and it will write one.
- **Don't contradict yourself.** *"Brief but comprehensive"* asks for two things without saying which wins.
  The model picks, and you can't predict which.

## In practice at Technik

You have the text of quality notification `300001234` and a production meeting tomorrow morning.

**The vague version**

> Summarise this QN.

What comes back is a paragraph that repeats `XT-V2-1042`, `0020` and `PRJ-2031` without explaining any of
them, and ends: *"The porosity was likely caused by contamination of the bore surface."* The QN says no such
thing. Nothing in the prompt said *only what the QN states*, and a likely cause is exactly the kind of
thing a summary of a defect usually contains.

**The specific version**

> I'm preparing for tomorrow's production meeting. Summarise the quality notification below for the team
> leads, who don't read SAP codes.
>
> Use only the QN text. Cover what was found, on which part and unit, at which operation, what has been
> done so far and what is still open. Keep it under 120 words, in plain language, with every code spelled
> out. If the QN doesn't say something, write "not stated" instead of guessing.
>
> \---
> *(QN 300001234 text)*
> \---

Map it back: the first sentence is **context**; *summarise… for the team leads* is the **goal**; *use only
the QN text* is the **source**; the rest is **expectations**, out included. The answer now says the unit is
held at cladding and that no cause and no disposition are recorded yet. That is less satisfying than a
cause, and it's true.

> [!TIP]
> Read your prompt as if you were a new starter given it with no other briefing. Every question you would
> have to ask is a gap Copilot will fill on its own.

## Using it well

- **Start with the goal**, in one sentence, then add who it's for and what to use.
- **Name the audience.** It decides vocabulary, length and what needs explaining more than anything else.
- **Say what not to do** when it matters: don't guess a cause, don't add recommendations.
- **Always give it an out** for anything it might not find.
- **Spell out Technik's own shorthand** the first time. Internal acronyms are where generic knowledge is most
  likely to fill in the wrong meaning.

The same four elements, written once for every user, are how an agent gets its instructions:
{{topic:writinginstructions}}.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A generic, medium-length answer | Nothing said who it's for or how long | Name the audience and a length |
| A plausible detail the source doesn't contain | No source stated, no out | *Use only…*, plus *"write 'not stated'"* |
| It ignored half the request | Conflicting instructions; it picked one | Remove the conflict, or say which wins |
| The answer explains a Technik code wrongly | It filled an internal acronym with a common meaning | Spell the code out in the prompt |

## Key terms

**Goal**: what you want done, and what should come back.

**Source**: the material Copilot should work from.

**Expectations**: how the answer should be delivered: length, tone, format, audience.

**Out**: an instruction for what to do when the source doesn't cover the question.
