## TL;DR

A citation is the link from a sentence in the answer back to the passage it came from. It lets a
reader check in five seconds instead of not checking at all, and its **absence** is a signal worth
reading. Most knowledge problems show up here, and "knowledge returned nothing" has five usual
causes: permissions, indexing not finished, an unsupported or oversized file, a question that does
not match the content, and a source that was never actually enabled.

## Why it matters

Trust in an internal assistant is built one checkable answer at a time and lost in a single
confident wrong one. Citations are what make the first possible and the second survivable: an
engineer who can see that a criterion came from `SWI70000318` §5.2 will use the answer; one who
cannot will verify it by hand, and then stop using the agent, because verifying by hand was the job
they were trying to avoid.

Citations also change what you can debug. Without them, a wrong answer is a mystery. With them, it
is either the wrong source, the wrong passage of the right source, or a misreading of the right
passage — three different problems with three different fixes.

## How it works

The agent knows which retrieved chunks it used, and renders a reference to each. What the reader can
do with that reference depends on the source:

| Source | What a citation gives the reader |
|---|---|
| Uploaded file | The file, and often the page |
| SharePoint | A link to the document, subject to their own permissions |
| Website | The page URL |
| Connector or database | The table or record, not a document |

<!-- volatile verified=2026-09 -->
How citations are rendered, whether they deep-link to a page, and which sources produce them at all
differ between harnesses and change between releases. Check the linked documentation for current
behaviour; the reasoning below does not change.
<!-- /volatile -->

### The five reasons knowledge returns nothing

Work through them in this order, because they are roughly in order of likelihood and of how quickly
they can be ruled out.

1. **Permissions.** SharePoint knowledge is queried as the user asking. If they cannot open the
   document, they get nothing from it. The tell: it works for you and not for them.
2. **Indexing has not finished.** New content is not instantly searchable. The tell: it was added
   recently and nothing about it is found.
3. **The file is unsupported, too large, or not really text.** A scanned PDF with no text layer is
   an image. The tell: one specific file is never cited while its neighbours are.
4. **The question does not match the content.** The user's words and the document's words have
   nothing in common, or the content genuinely does not cover it. The tell: rephrasing finds it.
5. **The source is not enabled for this agent.** Configured, but not switched on, or switched on in
   a different agent. The tell: nothing from that source is ever cited, in any question.

Note what is *not* on the list: the model. Reaching for "the model is bad at retrieval" before
walking these five is the most reliable way to waste an afternoon.

### Reading a citation critically

Three failures look identical from the outside, and the citation tells you which you have:

- **Wrong source cited** — retrieval found something else entirely. Usually too many sources, or one
  that is too broad.
- **Right source, wrong passage** — the chunk next to the one you wanted. A chunking and retrieval
  problem; A8 covers it.
- **Right passage, wrong statement** — the model paraphrased where it should have quoted. An
  instruction problem, and the cheapest of the three to fix.

## In practice at Technik

Bruno asks: *"What is the minimum overlay thickness?"*

Three sources can answer, and they are not equivalent:

| Source | Says | Standing |
|---|---|---|
| `SWI70000318` §5.1 | Not less than 3.0 mm at every measurement point | **Governs.** It is the work instruction manufacturing works to |
| `DGL70000009` §3 | 3.0 mm = 0.5 dilution + 1.0 machining + 1.5 service | Explains the reasoning. Does not set the requirement |
| `TS-014` (intranet) | 3.0 mm, in a summary table | A summary. It says itself that the work instruction wins |

Today all three agree, so any citation looks fine. The interesting moment is later: `ECN70000042` is
released, `SWI70000318` reaches revision C with new criteria, and nobody updates the intranet page.
Now an answer citing `TS-014` is confidently, checkably wrong — and it is *more* likely to be
retrieved than the work instruction, because a summary table is a tighter keyword match than a
clause buried in section 5.

The instruction that prevents this is short, and it belongs in the agent from the day the second
source is added:

```
When sources disagree, prefer the controlled document over any summary of it, and say which you
used. Controlled documents are SOP, SWI, LWI, GWI and DGL numbers. Intranet pages summarise them
and may be out of date.
```

> [!TIP]
> Ask the agent something your sources genuinely do not cover — *"what is the maximum ovality after
> bending?"* is answered by `SWI70000366`, which is not in this module's knowledge. An agent that
> answers it anyway is one you have not yet tested honestly. That question belongs in your
> evaluation set (B13), not in your demo.

## Design guidance

- **Require citations** for anything an engineer might act on.
- **Instruct the agent to quote acceptance criteria, not summarise them.** Numbers should be
  transcribed, not paraphrased.
- **State source precedence** as soon as you have two sources that overlap.
- **Instruct abstention explicitly**, and test that it happens.
- **Walk the five causes in order** before touching instructions or models.
- **Retire summaries** when the thing they summarise is revised, or accept that they will be cited.
- **Check a citation actually resolves** for a user who is not you.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Answers with no citations at all | Nothing retrieved, and the agent answered anyway | Instruct it to answer only from sources and to abstain; check the test pane |
| Citations for you, nothing for a colleague | Permissions — working as designed | Confirm their access to the document, not the agent |
| One document is never cited | Unsupported format, too large, or a scanned image | Check the format; re-export with a text layer |
| A stale summary is cited as current | It matches the question better than the governing document | Source precedence in the instructions; retire the summary |
| The right document, the wrong clause | Retrieval returned a neighbouring chunk | Improve headings; see A8 for chunking |
| Numbers in the answer differ from the document | The model paraphrased | Instruct it to quote criteria verbatim |
| Nothing from a source, ever, for anyone | It is not enabled on this agent | Check it is switched on where you think it is |

## Key terms

**Citation** — the reference from a statement in the answer to the passage it came from.

**Groundedness** — how far an answer is supported by its sources. Measurable, and measured in B13.

**Abstention** — declining to answer when the sources do not cover the question.

**Source precedence** — the rule saying which source wins when two disagree. An instruction you
write; nothing infers it.

**Indexing latency** — the delay between adding content and it becoming retrievable.

**Activity map** — Copilot Studio's view of what an agent did in a turn, including what it retrieved
(B5).
