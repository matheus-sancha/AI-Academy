## TL;DR

A shared skill is an **unreviewed dependency that ships instructions and code**, so govern it like a
dependency: an owner, a review gated on what it bundles, a pin, and a date it gets looked at again.
The published collections already work this way, and the fastest way to design a team library is to
copy what they do.

## What a third-party skill actually is

The warnings are blunt. GitHub's documentation states that skills "are not verified by GitHub and may
contain prompt injections, hidden instructions, or malicious scripts", and tells you to "Always inspect
the content of a skill before installation using `gh skill preview`." Anthropic recommends installing
"only from trusted sources" and auditing anything less trusted, because malicious skills may "direct
Claude to exfiltrate data and take unintended actions". Its own collection is "provided for
demonstration and educational purposes only", to be tested thoroughly "in your own environment before
relying on them for critical tasks."

Licensing is not uniform either. That repository says many of its skills are Apache 2.0 while others
are "source-available, not open source", so the licence is a per-skill question.

## The model to copy

<!-- volatile verified=2026-11 -->
`github/awesome-copilot` runs a submission process worth borrowing wholesale:

- **A required gate.** Every pull request is tracked by a check called `submission-gate`.
- **Risk tiers that key on what is bundled.** The high tier is "bundled scripts, hook commands, MCP
  config" — exactly the parts that execute — and "The tier sets how many approvals are needed".
- **Structural lint before human review**, checking "Agent Skills spec compliance", plus an install
  smoke test.
- **Named owners**, through a `CODEOWNERS` file, with an explicit maintainer decision to approve or
  reject.
- **Pinning by "a release tag or tag ref rather than a branch"**, or a full 40-character commit SHA.
- **A re-review clock**: a six-month window that "starts when an approved submission issue is
  closed."

It also states what it will not accept, including instructions designed to "bypass security policies,
exploit vulnerabilities, or weaken system security".
<!-- /volatile -->

## At Technik

Six rules, and none of them needs a tool Technik does not have. Skills live in `.github/skills/` with
a `CODEOWNERS` entry per skill, so a change has a reviewer by default. Anything bundling a script goes
to a code review, not a documentation review ({{topic:bundling}}). `skills-ref validate` runs in CI
({{topic:skilltest}}). Third-party skills are previewed before install and pinned to a tag or SHA.
Each skill's owner re-reads it every six months, which is also when its `volatile` claims are
re-checked. And the catalogue is a page in the repository rather than tribal knowledge: name, owner,
what it is for, what it must not be used for.

Community collections are a good source of *ideas*. Treat a borrowed skill as a draft you now own.

## Key terms

**Risk tier** — a review level set by what a skill bundles, with executable content ranked highest.

**Pin** — installing at a release tag or a full commit SHA, never a branch.

**Re-review window** — the interval after which an approved skill is read again.
