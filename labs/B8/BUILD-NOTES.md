# B8 checkpoint — notes for the maintainer

Not published. `lab.md` and `exercise.md` are the only Markdown files under `labs/` that become
pages; this file stays in the repository.

## What to produce

| File | Contents |
|---|---|
| `start/TechnikAssistant_B7_end.zip` | The same file as `labs/B7/solution/TechnikAssistant_B7_end.zip`. Export once, copy here |
| `solution/TechnikAssistant_B8_end.zip` | One solution containing **both** agents: the Technik Production Assistant with the connected agent added, and the Technik QN Assistant with the skill, its tool and its three knowledge files |

Two agents in one solution is deliberate. They are published and permissioned separately (B12) but
they version together, and B9's starter needs both.

## The harness problem — read this before building

This lab exists because the Technik Production Assistant is on the **standard harness** and cannot
hold a skill. That follows from the roadmap's own `B4 chooseharness` and `B8 reuse` topics, and from
B5 giving the assistant a topic. Three things to verify on the first build, in this order, because
each one invalidates more of the lab than the last:

1. **Can a GitHub Copilot harness agent be created in your developer environment at all?** If not,
   the whole module needs rethinking — report immediately.
2. **Can a standard-harness agent connect to a GitHub Copilot harness agent?** Step 7 assumes yes
   and the volatile block offers a fallback. If the answer is no, promote the fallback to the main
   path: an agent flow on the assistant calling an AI Builder prompt that carries the skill's
   instructions. Say so, because `reuse.md` describes the connected-agent pattern as the
   recommended one and would need softening.
3. **Does the standard-harness assistant really have no Skills area?** Step 1 has learners confirm
   the constraint by looking. If the product now shows one, step 1 and the module's framing are
   wrong and this is the most urgent correction in the course.

## Before committing either zip

This repository is public. Check both agents for:

- environment URLs and environment IDs;
- the SharePoint site URL — it belongs in a connection reference the learner re-binds;
- connection ids and connection reference display names embedding a tenant or a person;
- Snowflake account locators, usernames, or role names other than the `<you>` placeholders.

Export the skill file itself as well, and keep it in the repository next to this file if the
platform lets you export it — `addskill.md` tells learners to keep skills in source control, and the
course should do the same.

## Things most likely to need correcting after the first build

1. **Whether the skill actually performs step 4 of *Before you draft*.** The lab's headline check is
   that request 6 produces "already covered by `300001211`" rather than a third notification. If the
   agent drafts anyway, the skill's step ordering needs strengthening — report what worked, because
   the checklist depends on it.
2. **Whether request 13 is safe.** The injected notification `300001270` is read by the skill. If the
   draft follows it, say so plainly; B11 is where that is meant to be exposed, but B8 should not ship
   a lab that walks into it silently.
3. **Whether request 17 carries the serial number across the handoff.** The lab allows for it not
   working and asks learners to write down why. Record the real behaviour so the checklist can be
   made definite.
4. **Credit consumption.** Skills are reasoning-heavy; the sixty-turn estimate is a guess.
5. **Whether `V_RELEASED_REVISIONS` really needs recreating** in step 0, or whether learners arriving
   from B7 still have it. The reset drops views by design, so the step should stand, but confirm the
   wording is not confusing for someone who has just done B7.

## Re-export triggers

Re-export both zips whenever a volatile block in the B8 lessons or in `lab.md` is re-verified, when
`SOP70000101`, `GWI70000027` or `SWI70000318` is revised — the skill quotes all three by revision —
or when a platform update changes the solution format.
