## TL;DR

A citation links a statement in the answer back to the passage it came from. It lets a reader check in
five seconds instead of not checking at all. The fact this module exists to teach: **attaching a
knowledge source is not the same as being grounded in it.** Unless the instructions say to answer from the
sources, and to say so when they have nothing, the agent fills the gap from its own reasoning and sounds
just as sure. When knowledge returns nothing, the usual causes are permissions, unfinished indexing, a file
that is too large or unreadable, and a question that does not match the content.

## Why it matters

People come to trust an internal assistant one checkable answer at a time, and stop trusting it after one
confident wrong answer. Citations make the first possible and the second survivable. An engineer who can
see a criterion came from `SWI70000318` §5 will use the answer. One who cannot will check it by hand, and
soon stop using the agent, because checking by hand was the job it was meant to save.

Citations also make failures debuggable. Without them, a wrong answer is a mystery. With them, it is the
wrong source, the wrong passage of the right source, or a misreading of the right passage: three problems
with three different fixes.

## How it works

### Attached is not grounded

On the GitHub Copilot harness, Microsoft says the runtime decides for itself whether a question needs
knowledge, that citations "might be included", and that "the agent's instructions influence how it
interprets and presents knowledge". There is no switch that withholds an uncited answer ({{topic:genai}}).
So an agent with five documents attached and no grounding rule will still answer the question they do not
cover, from its general knowledge, in the same tone.

The standard harness has that switch, and its behaviour shows why citations are central. With **Allow
ungrounded responses** off, an answer from knowledge is returned **only if it carries an in-text citation**.
When the model forgets to cite, a correct answer is withheld as though nothing was found. Microsoft's
mitigation is to instruct the agent to always cite, and to avoid instructions such as *respond only in
JSON* that suppress citation markers.

<!-- volatile verified=2026-10 -->
How citations display depends on the channel. In Microsoft Teams, Microsoft documents at most 20 citations
per response, titles cut to about 80 characters and snippets to about 480. If you render an answer yourself,
for example in an Adaptive Card, citations are not added for you. Citations from a knowledge source cannot
be passed as inputs to other tools.
<!-- /volatile -->

A cited PDF usually opens at page one. A community technique appends `#page=` to the link from page metadata
in the response. It is standard-harness only, built in the conversational boosting topic, and its comments
report that it fails on PDFs that lack that metadata.

### When knowledge returns nothing

Microsoft's troubleshooting page for SharePoint lists the causes, and every one of them is **silent**: no
error, just *"I'm not sure how to help with that"*. Work through them roughly in order:

1. **Permissions.** The user needs at least Read on the file. Without it, the system "behaves silently as
   if the document doesn't exist". The tell: it works for you and not for them.
2. **Indexing hasn't finished.** Recently uploaded files may not be in Microsoft Search yet. The tell:
   searching SharePoint itself for a unique word from the file does not find it either.
3. **The file can't be used.** Over the size limit (7 MB without a Microsoft 365 Copilot licence in the
   tenant, 200 MB with one), an unsupported format, a classic `.aspx` page, or **encrypted** by a
   sensitivity label, Double Key Encryption or a password. Encrypted files can show as **Ready** and still
   return nothing.
4. **The question doesn't match the content.** Only the top three search results are used. If the user's
   words and the document's words do not meet, or the title is generic, the right file never makes the top
   three. The tell: rephrasing finds it.

Microsoft also lists a broken link after a site is renamed, missing authentication scopes, filters that
exclude too much, Restricted SharePoint Search, and content moderation. Note what is not on the list: the
model. Blaming it before working through these is the surest way to lose an afternoon.

### Reading a citation critically

- **Wrong source cited**: retrieval found something else. Usually too many sources, or one too broad.
- **Right source, wrong passage**: the neighbouring chunk. A content and retrieval problem.
- **Right passage, wrong statement**: the model paraphrased where it should have quoted. An instruction
  problem, and the cheapest of the three to fix.

## In practice at Technik

An engineer asks for the minimum overlay thickness on an XT bore. Three sources can answer, and they are
not equal:

| Source | Says | Standing |
|---|---|---|
| `SWI70000318` §5 | Not less than 3.0 mm at every measurement point | **Governs.** Manufacturing works to it |
| `DGL70000009` §3 | 3.0 mm = 0.5 dilution + 1.0 machining + 1.5 service | Explains. Does not set the requirement |
| *Weld Overlay Acceptance Criteria* | 3.0 mm, in a summary table | A summary, and says the work instruction wins |

Today they agree, so any citation looks fine. The test comes when revision C of `SWI70000318` is released
for `ECN70000042` and nobody updates the standards page. An answer citing the page is then confidently and
checkably wrong, and a summary table often outscores a clause buried in section 5.

So the Production Assistant's `<knowledge_routing>` section ({{topic:xml}}) says:

```xml
<knowledge_routing>
Answer engineering questions only from the Controlled Documents library and the Standards
site. Cite the document number, revision and section for every requirement, and quote
acceptance criteria exactly; do not paraphrase numbers.
When sources disagree, the controlled document governs over any Standards page, because
the pages summarise documents and can lag a revision. Say which one you used.
If the sources do not cover the question, say "I could not find that in my sources" and
name the closest document you did find. Do not answer from general knowledge.
</knowledge_routing>
```

Then test it with *"What is the minimum overlay thickness for Inconel on a manifold header?"* The trace
shows a Knowledge step retrieving `SWI70000318`, because it is the closest match, but that instruction
covers XT bores. The right answer abstains and names `SWI70000318` as the nearest document. A cited 3.0 mm
is the failure the citation makes visible. That question goes into the evaluation set ({{topic:testsets}}),
not the demo.

## Design guidance

- **Write the grounding rule before the first source is attached**, and test it with a question the
  sources do not cover.
- **Require citations** for anything an engineer might act on, and quote criteria verbatim.
- **State source precedence** as soon as two sources overlap.
- **Work through the four causes in order** before touching instructions or models.
- **Retire summaries** when the document they summarise is revised.
- **Check a citation opens for a user who is not you.**

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Confident answers with no citation | No grounding rule; the agent answered from general knowledge | Add the rule; test with an uncovered question |
| A correct answer comes back as *nothing found*, sometimes | Standard harness, ungrounded responses off, and the model did not cite | Instruct it to always cite; remove format rules that suppress citations |
| Citations for you, nothing for a colleague | Permissions, working as designed | Confirm their access to the file |
| A file shows **Ready** but is never cited | Encrypted by a label, DKE or a password; or over the size limit | Publish an unprotected copy; check the size |
| Numbers in the answer differ from the document | The model paraphrased | Instruct it to quote criteria exactly |
| Citations missing in a custom card | Answers rendered by hand do not get citations | Render them yourself |

## Key terms

**Citation** — the reference from a statement in an answer to the passage it came from.

**Grounded** — supported by the agent's sources, not merely accompanied by them.

**Source precedence** — the rule for which source wins when two disagree. Something you write; nothing
infers it.

**Security trimming** — returning only what the asking user may see, silently.

**Activity trace** — the GitHub Copilot harness's view of what a turn did, including its Knowledge steps
({{topic:test}}).
