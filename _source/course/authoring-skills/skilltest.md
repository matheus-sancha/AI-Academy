## TL;DR

A skill has two failure modes and the products test neither directly. **Did it fire?** is checked by
hand: a fresh chat, the `/` menu, then an unprompted request that should match. **Was the answer
right?** needs an eval harness you build, because Copilot Studio's test sets are documented for the
standard harness — the one that has no skills — and its only advice for a skill is to try it in the
Preview tab. What *is* automatable is structural: `skills-ref validate` and `gh skill publish
--dry-run` check the frontmatter and the specification, and nothing about behaviour. Versioning is the
same story — no version field in the format, so Git history and `gh skill`'s pinning are the whole
mechanism.

## Why it matters

Both failures are quiet. A skill that never fires produces a competent answer from the model's own
reasoning, so nobody reports it ({{topic:descriptions}}). One that fires and drafts the wrong revision
produces a document that looks right, reviewed by the person who asked for the draft.

So the gap matters here. You have already built an agent with test sets over it ({{topic:testsets}}),
and the instinct is to point that machinery at the skill. It does not reach: the one documented method
that inspects what the agent *chose* checks tools and topics, not skills.

The consequence is a design rule, not a tooling one. If a step must happen, don't test that a skill
chose to do it — invoke it explicitly, or put the step in code ({{topic:loop}}).

## How it works

### The trigger test, done by hand

<!-- volatile verified=2026-11 -->
VS Code splits it into two questions, and the order is the point. First discovery: "Start a fresh chat
with the intended harness and workspace", and if the skill appears in the `/` menu, "run the skill
yourself", then "Review the tool activity and result" to confirm it used the files you expected. Only
then selection, which you "test separately with a request that matches its description".

They are separate because of the guarantee that is withheld: discovery and installation "don't
guarantee that the agent selects it for every relevant request." A skill can pass the first test
perfectly and fail the second every time.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
No page documents a way to automate either half — no assertion that a skill was selected, no fixture
for a prompt set, no report. Treat a trigger set as a checklist a person runs, re-run when a
neighbouring skill is added or a description changes.
<!-- /unknown -->

### The output test, and the harness mismatch

<!-- volatile verified=2026-11 -->
Copilot Studio's single response test set is the obvious candidate. It "tests your agent on one
unconnected question at a time, instead of a full conversation", holds up to **100 test cases** with
questions up to 1,000 characters, and grades with eight methods: general quality (an LLM over
relevance, groundedness, completeness and abstention, out of 100% and on by default), content safety,
compare meaning, tool use, keyword match, text similarity, exact match, and a custom method whose
labels roll into a pass rate. Expected responses are optional at import but required by every method
except general quality, and results are kept for 89 days.

Two sentences decide whether it is usable for a skill. The article "describes features used in agents
or agent flows powered by the standard harness" — and standard-harness agents support no skills at all
({{topic:reuse}}). And the one method that inspects a choice rather than an answer, *tool use*, checks
"whether the agent used the expected tools or topics". Skills are not named.
<!-- /volatile -->

So on the harness that has skills, the documented guidance is one line from the skill-creation page:
"test your agent in the **Preview** tab to verify the skill works as expected."

That is a boundary rather than a dead end. A skill is part of an agent, and an agent's behaviour is
testable with an eval harness you own — fixed inputs, graded outputs, a baseline that blocks on
regression ({{topic:evalharness}}). The capstone does this, and a skill is another thing whose effect
the cases measure ({{topic:stageevals}}).

### What you can automate: structure

<!-- volatile verified=2026-11 -->
Two structural checks exist, both worth wiring into CI. The specification ships a reference library —
`skills-ref validate ./my-skill` — which "checks that your `SKILL.md` frontmatter is valid and follows
all naming conventions". `gh skill publish --dry-run` validates against the specification, and
`--fix` corrects what it can without publishing.
<!-- /volatile -->

Both catch the silent killers — an invalid `name`, a prefix, frontmatter that is not valid YAML — and
neither has an opinion about whether the skill is any good. That is the right division of labour.

### Versioning

<!-- volatile verified=2026-11 -->
There is no version field. The specification's optional `metadata` map is an "Arbitrary key-value
mapping", and its example happens to contain `version: "1.0"`, but the specification gives no
versioning rules and no field for it.

What exists is distribution-side. `gh skill install` writes provenance into the installed skill's
frontmatter — "the source repository, ref, and tree SHA" — and accepts a tag, a SHA, or `--pin`, which
are "mutually exclusive". "Pinned skills are skipped during updates".
<!-- /volatile -->

So for a skill you author, the version is the commit and the review is the pull request
({{topic:git}}). For one you consume, pin it: an unpinned skill changes behaviour under you on the
next update.

## In practice at Technik

`document-revision` gets a trigger table, kept beside the skill in the repository:

| Prompt | Should fire? |
|---|---|
| *Revise `SWI70000318` for `ECN70000042`* | yes |
| *Apply the ECN to the weld prep work instruction* | yes |
| *Bump the cladding SOP to the next revision* | yes |
| *What revision of `SWI70000318` is released?* | no, a lookup |
| *Write up the porosity defect on `100004521`* | no, `qn-write-up` |
| *Why is `100004521` late?* | no, `wo-delay-note` |

Six prompts, run in a fresh chat on each surface the skill reaches, `/` menu first. Ten minutes, and
the only test of the description that exists.

The output test belongs in the eval set, not in the skill. One case asks for revision C of
`SWI70000318` from `ECN70000042`, and three code checks grade it: the change summary matches
`TC_ECN_AFFECTED_ITEMS` for that ECN, sections 4 and 5 are both named, and no untouched section is
edited. Code checks rather than a judge, because each is decidable ({{topic:llmjudge}}).

One governance detail from the test-set documentation applies on any harness: testing "uses the
authentication of the currently signed-in user", and generated cases "can include sensitive data that
the connected account can access" — so a set generated by a quality engineer can carry QN text no
planner should see ({{topic:dlp}}).

## Design guidance

- **Test discovery and selection separately.** The first can pass while the second always fails.
- **Keep a written trigger table**, with the prompts that should *not* fire.
- **Put structural validation in CI** — `skills-ref validate`, or `gh skill publish --dry-run`.
- **Test a skill's output at the agent level**, in your own eval harness.
- **Grade with code wherever the answer is decidable.** Keep judges for wording.
- **Version by commit, pin by SHA or tag.** The format gives you nothing.
- **Never let a test stand in for a guarantee.** Evaluations "don't guarantee that an agent is safe or
  appropriate for every scenario."

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The skill passes review and never fires in use | Only discovery was tested | Test unprompted selection separately |
| A test set cannot see the skill at all | Test sets are documented for the standard harness | Test at the agent level, in your own harness |
| A skill broke and no test failed | Structural checks passed; none check behaviour | Add an eval case for what it produces |
| A skill changed after an update | Installed unpinned | Pin by tag or SHA |
| Nobody can say which version shipped | No version field in the format | The commit is the version |
| A test set exposes data to the wrong people | Generation runs as the signed-in user | Generate with an account scoped to the audience |

## Key terms

**Trigger test** — a manual check that a skill is discovered, then selected unprompted.

**Structural validation** — frontmatter and specification conformance, nothing behavioural.

**Single response test set** — Copilot Studio's up to 100 unconnected graded questions, for
standard-harness agents.

**Pinning** — installing a skill at a fixed tag or SHA so an update cannot change it.
