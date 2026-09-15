## TL;DR

A handful of agent-level settings decide how your agent orchestrates, whether it may answer from the
model's general knowledge, how strictly it moderates content, and how it formats replies. They are
set once, they apply to every answer, and **the defaults are written for a general-purpose
assistant** — which is not what an internal engineering tool is. Review all of them on every new
agent, change the two that matter, and re-test afterwards.

## Why it matters

Most of this module is about things you write: instructions, trigger phrases, Power Fx. This lesson
is about things you *switch*, and switches are easy to skip because nothing prompts you to look at
them.

One of them is the most consequential control in Copilot Studio. The **general knowledge** setting
decides whether the agent may answer from what the model absorbed in training when its own sources
come up empty. Leave it on and every grounding rule you wrote in
[Instructions](instructions.html) becomes advisory: the agent has permission to fill the gap, so
sometimes it will. Turn it off and the same rule has a mechanism behind it.

That is the course's recurring idea again, in the one place where it costs nothing to apply:
[Variables](variables.html) put format validation in Power Fx rather than in a sentence, B6 puts
deduplication in a view rather than in a description, B7 puts a filter in the query rather than in a
prompt. **When something must be true, use the mechanism that makes it true.** Here the mechanism is
a toggle.

## How it works

<!-- volatile verified=2026-09 -->
Where these settings live, what they are called, and which of them appear for which harness all
change between releases — some sit in the agent's settings, some on the generative AI or
orchestration page. Use the table below for what each one *does*; follow the linked documentation for
where it currently is and what the current options are called.
<!-- /volatile -->

| Setting | Decides | What usually matters |
|---|---|---|
| **Orchestration** | Whether the model chooses knowledge, tools and topics, or whether only trigger phrases route | Generative, for anything with more than one source |
| **General knowledge** | Whether the agent may answer from the model's training data | **Off** for an agent over company data |
| **Content moderation** | How aggressively borderline content is blocked | Test with your own vocabulary before assuming |
| **Response format** | Plain text, Markdown, adaptive cards, length | Match the channel people actually use |
| **Web search** | Whether the agent may reach public web content | Off when answers must be traceable to a controlled source |

### Orchestration

Generative orchestration means the model reads your instructions, your knowledge descriptions and
your tool descriptions, and decides what to use. Classic routing means trigger phrases decide, and
nothing else.

Choosing generative makes **descriptions load-bearing**. A tool nobody calls is usually a tool whose
description does not say when to call it — which is why B7 spends as long on descriptions as on
connections. Choosing classic gives you predictability and a ceiling: an agent that can only do what
you enumerated.

### General knowledge

Off means: when the knowledge and tools do not cover the question, the agent says so. On means: it
may answer anyway, from training data that has a cut-off, no revision number and no citation.

For Technik that is not a preference. An answer about overlay thickness that did not come from
`SWI70000318` is wrong even when the number happens to be right, because nobody can check it and
nobody can tell it apart from one that did.

The failure is also silent. A confidently phrased general-knowledge answer looks exactly like a
grounded one until someone checks — the mechanism from
[Hallucination](../B1/hallucination.html), with a switch that prevents it.

### Content moderation

Moderation trades false refusals against risk, and the balance depends on your vocabulary. This is
the setting most likely to surprise an engineering team, because manufacturing quality language sits
close to language moderation systems are tuned to catch: *crack*, *failure*, *defect*, *rejection*,
*blast cleaning*, *destructive testing*.

Do not reason about this from first principles. Ask the agent twenty real questions using the words
your people use, and see what comes back.

### Response format and web search

Format is a channel decision: what renders well in Teams is not what renders well in a website
control, and a table that formats badly is read as a wrong answer. Web search is off for the same
reason general knowledge is: a public page has no revision and no owner.

## In practice at Technik

The Technik Production Assistant's settings, and why each one is what it is:

| Setting | Value | Why |
|---|---|---|
| Orchestration | **Generative** | From B6 it has to choose between five documents, SharePoint, Snowflake knowledge and a topic. Trigger phrases cannot do that |
| General knowledge | **Off** | The instruction "answer only from your sources" needs a mechanism behind it. Without this, B6's abstention tests pass by luck |
| Content moderation | **The default, then tested** | Quality vocabulary is the risk. The lab has you ask about porosity, undercut and hydrostatic failures and check nothing is blocked |
| Response format | **Markdown** | Teams is the channel (B12), and the assistant's answers are tables of operations more often than sentences |
| Web search | **Off** | Every answer must be traceable to a controlled document or to Snowflake |

The second row is the one to carry forward. In B6 you will ask the assistant a question its documents
do not cover, and the correct answer is *"I could not find that in my sources."* If general knowledge
is on, you may still get that answer — the instruction is usually obeyed — and you will have tested
nothing. The toggle is what turns that test into evidence.

> [!WARNING]
> Changing any of these invalidates prior testing, exactly as changing the model does
> ([Model Selection](model.html)). Moderation and orchestration change behaviour across every
> question, not just the ones you were thinking about. Change one, re-run your questions, and write
> down what you changed.

## Design guidance

- **Open the settings page on every new agent**, before you add anything. It takes two minutes.
- **Turn general knowledge off** for any agent over company data, on day one.
- **Test moderation with your real vocabulary**, not with polite examples.
- **Set the format for the channel** people will actually use.
- **Record the settings** alongside the instructions, in the same place you version them.
- **Change one setting at a time**, and re-run your questions.
- **Re-check after a platform update.** Defaults change, and a changed default is a silent behaviour
  change.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent answers confidently about things it has no source for | General knowledge is on | Turn it off. The instruction alone was never going to hold |
| Abstention tests pass, then fail in production | They passed because the model chose to comply, not because it had to | Turn general knowledge off and re-run them |
| A legitimate question about a weld defect is refused | Moderation is stricter than your vocabulary | Test with real terms; adjust the level knowingly |
| A new tool is never called | Classic orchestration, or a description that does not say when to use it | Switch to generative; rewrite the description (B7) |
| Answers look broken in Teams | Format set for a different surface | Match the format to the channel (B12) |
| The agent cites a public web page | Web search is on | Turn it off where answers must be traceable |
| Behaviour changed and nobody touched the agent | A platform update changed a default | Re-check the settings; record them so drift is visible |

## Key terms

**Generative orchestration** — the model choosing knowledge, tools and topics from their descriptions
and your instructions.

**Classic orchestration** — routing by trigger phrase only.

**General knowledge** — whether the agent may answer from the model's training data when its sources
do not cover the question.

**Content moderation** — how aggressively borderline content is blocked. A trade, not a safety
guarantee.

**Grounding posture** — the combination of this setting and the instruction that describes it
([B6](../B6/rag.html)).

**Silent default** — a setting nobody chose, which is doing something anyway.
