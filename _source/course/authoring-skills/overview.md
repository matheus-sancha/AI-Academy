## What this module is for

You can already write a skill that works. This module is about the three things that decide whether it
keeps working: whether it fires, what it costs when it does, and whether anyone can tell it broke.

One sentence runs through all six lessons. **A skill is a way of delivering context, not a way of
enforcing anything.** Every control it offers turns out to be advisory when you read the small print.
Discovery "does not guarantee" invocation. Instructions are followed, not obeyed. `allowed-tools`
removes a confirmation rather than granting a capability, and GitHub says plainly what that enables.
The `scripts/`, `references/` and `assets/` folders are "recommendations". So the things you genuinely
control are narrower than they look, and they are the two worth designing carefully: **what a skill
brings into the context, and what it is allowed to run.**

The second thing to expect is that the documentation thins out as you go. The frontmatter is specified
to the character — 64 for `name`, 1,024 for `description`. The craft of writing that description is
two sentences and one example pair. What executes a bundled script outside Copilot Studio is not
documented at all, and no page describes a way to test whether a skill triggered. Three of these
lessons end in an `unknown` block for that reason. Knowing where the map ends is part of working at
this level.

## Before you start

You need the format itself: {{topic:skill}} and {{topic:skillmd}}, whose anatomy this module assumes
rather than repeats, and {{topic:openformat}}, which is why any of it travels. {{topic:createskill}}
and {{topic:packaging}} covered authoring and shipping on Copilot Studio, and {{topic:sandbox}}
covered that harness's script limits — this module does not restate them, and one lesson explains why
they do not extend to the other surfaces. {{topic:reuse}} holds the fact that settles a question in
{{topic:skilltest}}: standard-harness agents support no skills at all.

From this level, {{topic:budget}} and {{topic:jit}} are the arithmetic behind the first lesson, and
{{topic:customize}} already drew the line between a skill and an instruction file — including why a
prompt file is not the portable option.

Nothing here needs to be run, though the trigger test in {{topic:skilltest}} is worth doing in a real
editor on a real repository. The capstone repository is public and tested offline only
({{module:capstone-build}}).

Allow about two hours.

## What you will be able to do

By the end of this module you should be able to:

- name the three loading levels, say what triggers each one, and place a given fact in the right one;
- defend a `SKILL.md` that is short, and say what moved out of it and where;
- explain why a bundled script can be cheaper than a reference file of the same length;
- write a description with a trigger clause and a boundary clause, and say which of those no source
  asks for;
- say what discovery guarantees and what it does not, and name the two frontmatter fields that make a
  skill's use certain or impossible;
- decide between a script, a reference file and an asset by asking who does the work;
- explain why `allowed-tools: shell` is a worse idea than it looks;
- put a project skill in the directory that reaches every surface, and say which locations do not;
- design a trigger test and an output test, and say which tool exists for each;
- version and pin a skill in a format that has no version field;
- govern a shared library with an owner, a tiered review, a pin and a re-review date.

## The thread through this module

Outward from the file: what it costs, what makes it fire, what it carries, where it lives, how you
know it works, and who is responsible for it.

{{topic:disclosure}} does the arithmetic first, because every later decision is a placement decision —
and finds that a script's cost is its output while a reference file's cost is its length.
{{topic:descriptions}} takes the one field that decides everything and finds the guidance for it is
almost absent, so the conventions it teaches are marked as choices rather than rules.
{{topic:bundling}} splits the directory by *who does the work*, then hits the module's hardest silence:
nobody documents what runs your script, or in what isolation. {{topic:skillsvscode}} moves the skill
into a repository, where six locations, one self-contradicting setting and two silent failures are
waiting — along with the only real versioning mechanism, `gh skill`. {{topic:skilltest}} asks how you
would know any of this worked, and answers honestly: by hand for triggering, in your own eval harness
for output, and in CI for structure only. {{topic:skillgov}} closes with the library, borrowing a
working governance model from a published collection.

## Self-check

<details>
<summary>1. A colleague's skill is a single 700-line <code>SKILL.md</code> holding a procedure, a reference table of document codes and two worked examples. It works. What would you change, and why is "it works" not an answer?</summary>

Split it. The body is level-two material — loaded in full the moment the skill activates, and charged
every turn it stays active — so the reference table and the examples are being paid for on every
revision request, including the ones that never consult them. Move them to `references/` and have the
body name each file at the step that needs it.

"It works" measures the wrong thing. The failure here is cost and crowding, not correctness, and it
shows up as other context being squeezed out rather than as a wrong answer. The specification's own
limits point the same way — under 500 lines, and about 5,000 tokens — and its advice when you reach
either is to move material to separate files ({{topic:disclosure}}, {{topic:budget}}).
</details>

<details>
<summary>2. A compliance rule says every ECN applied to a controlled document must produce a change summary. Can the skill's description make that happen?</summary>

No, and it is worth being precise about why. VS Code states it twice: discovery and installation
"don't guarantee that the agent selects it for every relevant request." A description raises the
probability of selection; nothing turns it into a certainty.

There are two honest answers. Make the use explicit — slash-invoke the skill, or set
`disable-model-invocation: true` so it can only be invoked deliberately. Or move the guarantee out of
the skill entirely, into code that runs on the ECN rather than in a request the model interprets. This
is the same conclusion the harness module reached about rules that must hold every time
({{topic:descriptions}}, {{topic:loop}}).
</details>

<details>
<summary>3. A pull request adds a skill with a bundled shell script and <code>allowed-tools: shell</code> in the frontmatter. It was approved by the person who reviews documentation. Name the two problems.</summary>

The first is the review. A skill carrying a script is code arriving in a document, and it needs the
reviewer who reads code. Published collections put exactly this content in their highest risk tier —
bundled scripts, hook commands and MCP configuration — with more approvals required.

The second is the field. `allowed-tools` lists tools usable "without asking for confirmation each
time", so pre-approving `shell` deletes the only check in the path. GitHub's warning is explicit that
this "can allow attacker-controlled skills or prompt injections to execute arbitrary commands in your
environment", and the advice is to omit it when in doubt. It is not a sandbox, and no page says what
sandbox, if any, the script runs in on that surface ({{topic:bundling}}, {{topic:skillgov}}).
</details>

<details>
<summary>4. Your skill works in your editor. A colleague who cloned the repository doesn't see it, and the cloud agent ignores it. What are the likely causes?</summary>

Location, in one of three ways. It may be in a personal folder such as `~/.copilot/skills/`, which is
invisible to everyone else and to review. It may be in a custom location, and the CLI and the Copilot
app "do not inherit editor settings". Or it may be in a project directory that this surface's
documentation does not list — `.github/skills/` is the only one every list includes.

If it is in the right place, suspect the name. An invalid character, or a namespace prefix like
`myorg/skillname`, makes a skill "silently fail to load" — no error, just absence. Prefixing is the
plugin mechanism's job, so writing one yourself breaks the skill ({{topic:skillsvscode}}).
</details>

<details>
<summary>5. Someone proposes pointing your Copilot Studio test sets at the new skill to prove it works. Why won't that work, and what would you do instead?</summary>

Two reasons. The single response test set is documented for the **standard** harness, and
standard-harness agents support no skills at all. And the one grading method that inspects what the
agent *chose* rather than what it said checks "the expected tools or topics" — skills are not named.

So split the question. Triggering is tested by hand, and in two stages: a fresh chat to confirm the
skill is discovered and runnable from the `/` menu, then, separately, an unprompted request that
should match its description. Output is tested at the agent level in your own eval harness, with code
checks where the answer is decidable. Structure — frontmatter and specification conformance — is the
only part you can automate, with `skills-ref validate` or `gh skill publish --dry-run`
({{topic:skilltest}}, {{topic:evalharness}}).
</details>
