## TL;DR

The description is the whole activation decision, and it is a **hint, not a selector**: VS Code states
plainly that discovery "does not guarantee that it invokes a skill for every relevant prompt." So
write it to maximise the chance — what the skill does, when to use it, and the words your users
actually type — keep it far below the 1,024-character cap because level 1 is permanent context, and
when a task *must* use the skill, stop relying on the description and invoke it by name. The craft
here is mostly undocumented: the specification gives two sentences of guidance and one example pair,
and Microsoft gives one sentence. The rest is a design decision you own.

## Why it matters

Everything else about a skill is downstream of this field. A perfect procedure behind a description
that never matches is dead code that costs you 100 tokens a turn forever, and the failure is silent —
the agent answers from its own reasoning, competently enough that nobody files a bug
({{topic:skillmd}}).

The second reason is that the field does two jobs with no syntax to separate them. It has to be
**discriminative** — enough signal that this skill wins when it should — and **bounded** — enough that
it loses when it shouldn't. Those pull in opposite directions, and the common failure flips between
them: a vague description that fires on everything, then an over-specified one that fires on nothing.

It is also the one field whose cost you pay whether it works or not. A 1,000-character description on
twelve skills is a permanent tax on every turn for every user ({{topic:disclosure}}).

## How it works

### What the sources actually require

<!-- volatile verified=2026-11 -->
The specification makes `description` required, non-empty, and at most **1,024 characters**. Its
guidance is two lines: it "Should describe both what the skill does and when to use it", and "Should
include specific keywords that help agents identify relevant tasks". It contrasts one good example —
which names the operations (extract, fill, merge) and then the trigger conditions, including "when the
user mentions PDFs, forms, or document extraction" — against one poor one: "Helps with PDFs."

VS Code repeats the requirement, emphasising "what the skill does **and when to use it**", and the
same 1,024-character maximum. Copilot Studio asks you to "Describe what the skill does and when it
should be activated", and says only that well-written descriptions "help the orchestrator invoke the
right skill at the right time."

How the decision is made: Copilot Studio says the runtime "decides when to activate a skill based on
the user's message and the skill's description". Anthropic puts the mechanism one level down — the
descriptions are pre-loaded into the system prompt, and the model decides.
<!-- /volatile -->

That is the entire documented craft. Two "should" sentences, one example pair, and a character cap.

### What is not documented

<!-- unknown since=2026-11 -->
Three things writers reach for have no source behind them. **Negative scoping** — a closing *Not for…*
clause — is recommended by none of these pages; Copilot Studio is silent on it, and the specification
is silent on it. **Grammatical person** is unaddressed everywhere, so whether a description reads
*Drafts…* or *Use this to draft…* is a house style, not a requirement. And **how a tie is resolved**
when two descriptions both match is documented nowhere: Copilot Studio describes the single-match case
and says nothing about multiple matches or conflicts.

The conventions below are therefore Technik's, chosen because they are cheap and testable — not
because a vendor prescribes them. If one stops working, change it.
<!-- /unknown -->

### The guarantee you do not get

<!-- volatile verified=2026-11 -->
VS Code says it twice, in different sections: discovery "does not guarantee that it invokes a skill
for every relevant prompt", and discovery and installation "don't guarantee that the agent selects it
for every relevant request." Copilot Studio's wording is the same shape — descriptions *help* the
orchestrator, and the runtime *decides*.

There are two levers for when that is not good enough, both frontmatter fields on the Copilot harness.
`disable-model-invocation: true` takes the skill out of automatic selection entirely and requires the
`/` slash command, so the choice moves to the user. `user-invocable: false` does the reverse — it hides
the skill from the `/` menu while the agent may still load it automatically.
<!-- /volatile -->

So the honest design rule is the module's rule and the harness module's rule ({{topic:customize}}): a
description makes a skill *likely*; only an explicit invocation makes it *certain*. If a compliance
step has to run, it is not a description's job.

### The name, and two silent failures

<!-- volatile verified=2026-11 -->
`name` is at most 64 characters, lowercase letters, numbers and hyphens, no leading or trailing
hyphen, no `--`, and it "Must match the parent directory name" — though GitHub's wording is weaker,
saying it "Typically" matches. Two failure modes are explicitly silent: "Names with invalid characters
cause the skill to silently fail to load", and so does a namespace prefix like `myorg/skillname` or
`myorg:skillname`. The prefix is added for you when a skill ships in a plugin.
<!-- /volatile -->

A person choosing from the `/` menu reads the name too, so it carries some triggering weight — but
write it as an identifier and put the signal in the description.

## In practice at Technik

The document-revision skill sits beside two that already exist, `qn-write-up` and `wo-delay-note`
({{topic:createskill}}). Its description has to beat both on a revision request and lose to both
otherwise:

```yaml
name: document-revision
description: >-
  Drafts the next revision of a Technik controlled document (SWI, LWI, SOP, TDS)
  from a released ECN, with the change summary and the affected sections. Use when
  someone asks to revise, re-issue or bump a work instruction or procedure, or to
  apply an ECN to a document. Not for looking up a document's current revision or
  owner, and not for drafting QN write-ups.
```

Three things are deliberate. The operations come first and name the document types, because *SWI* is
what a manufacturing engineer types and *work instruction* is what a supervisor types — both have to
appear. The trigger clause carries the verbs from real requests: *revise*, *re-issue*, *bump*, *apply
an ECN*. And the closing clause names the two neighbours it must lose to — the clause no source asks
for.

The anti-example is on the same agent. A FAT checklist helper described as "Helps with test
checklists" is exactly the specification's poor example: it would compete for *which tests does
`XT-V2-1042` still need* and win nothing else it should.

Testing it is two separate exercises, and VS Code splits them the same way. First, does it load at
all: "Start a fresh chat with the intended harness and workspace", and if the skill is in the `/` menu,
run it by hand. Only then the harder question — whether it is chosen unprompted — which you "test
separately with a request that matches its description" ({{topic:skilltest}}).

## Design guidance

- **Two clauses, in order: what, then when.** Operations first, trigger conditions second.
- **Use the users' words, not the system's.** Both vocabularies if your readers differ.
- **Name what it is not for** when a neighbouring skill exists — undocumented, but cheap and testable.
- **Aim for two or three lines, not 1,024 characters.** The cap is a limit, not a target.
- **Never let a description carry a guarantee.** For a step that must run, use the slash command or
  `disable-model-invocation`, or put the rule in code ({{topic:loop}}).
- **Write `name` as an identifier** — lowercase, hyphens, matching the folder, no prefix.
- **Rewrite the description when a neighbour is added**, because the boundary moved.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The skill never fires, and the answer looks fine | Vague description; failure is silent | Add operations and trigger verbs; test unprompted |
| It fires on unrelated requests | No boundary clause | Add *Not for…* naming the neighbours |
| The right skill loses to a similar one | Overlapping descriptions; tie-breaking undocumented | Make the boundaries explicit on both |
| It fires for you and not for a colleague | Different vocabulary in the request | Add the other user group's words |
| Works in the `/` menu, never automatically | `disable-model-invocation`, or no trigger clause | Check frontmatter first, then rewrite |
| The skill is absent with no error | Invalid characters, or a namespace prefix in `name` | Lowercase, hyphens, match the folder |
| Context is tight before any skill fires | Long descriptions across many skills | Shorten to two or three lines |

## Key terms

**Activation** — the runtime's decision to load a skill's body, made from the user's message and the
description.

**Trigger clause** — the *when to use this* half of the description, carrying the words users type.

**Boundary clause** — a closing statement of what the skill is not for; a convention, not a documented
field.

**Slash invocation** — selecting a skill by name from the `/` menu, the only way to make its use
certain.
