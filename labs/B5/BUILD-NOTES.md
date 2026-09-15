# B5 checkpoint — notes for the maintainer

Not published. `lab.md` and `exercise.md` are the only Markdown files under `labs/` that become
pages; this file stays in the repository.

## What to produce

| File | Contents |
|---|---|
| `solution/TechnikAssistant_B5_end.zip` | The unmanaged `Technik AI Academy` solution holding the assistant exactly as `lab.md` leaves it |
| `labs/B6/start/TechnikAssistant_B5_end.zip` | The same file. Export once, copy there |

There is **no start zip**. B5 is the only lab whose start state is an empty environment, so nothing
is imported. That is worth remembering when the export scripts get automated: every other lab has a
`start/` folder and this one legitimately does not.

## The starter contract with B6

`labs/B6/lab.md` describes this zip's contents to learners, and the two must agree. After exporting,
re-read that description against what you actually built:

- **Agent:** *Technik Production Assistant*, standard harness, generative orchestration on.
- **Instructions:** identity, scope, grounding, style — the four-section block from step 3.
- **Topics:** one, *Work order status*.
- **Knowledge:** none.
- **Tools:** none.
- **Connection references:** none.

If the build diverges — a second topic you found necessary, a knowledge source added while testing —
fix `labs/B6/lab.md` in the same sitting. B6 and B7 drifted apart exactly once already, and
reconciling them took longer than writing either.

## Things to verify on the first build

In order of how much of the module each one invalidates:

1. **Can a standard-harness agent still be created, and is the choice visible during creation?**
   The whole Beginner track rests on this agent having topics. If the creation flow no longer
   surfaces the harness, or defaults somewhere else, step 2 and `tour.md` are both wrong and this is
   the most urgent correction in the module.
2. **Is there a general-knowledge switch, and does turning it off actually stop step 5 question 4?**
   `genai.md` makes this the load-bearing example of "use the mechanism, not the sentence", and the
   B6 abstention tests assume it. If the answer to *"tell me about subsea christmas trees"* is still
   a general one with the switch off, say so — `genai.md` overstates the toggle and needs softening,
   and B6's step 1 comparison gets weaker.
3. **Does the trigger hand a captured work order number to the topic (node 2)?** The volatile block
   offers the fallback of always asking. If the fallback is needed, record it, because step 7 test 1
   and test 3 stop being different tests and the checklist should merge them.
4. **Does moderation block step 5 question 2?** *Porosity*, *defect* and *rejection* are ordinary
   Technik vocabulary. If the default level blocks them, the lab needs to say which level works, and
   `genai.md`'s "test with your real vocabulary" becomes a step rather than advice.
5. **Does the attempt limit on node 3 behave as described?** Two failed tries then an exit. If the
   platform's wording or default differs, correct step 6.
6. **Credit consumption.** Thirty short turns is an estimate. Record the real figure; B5 is the
   cheapest lab in the track and is the best baseline for the others.

## Before committing the zip

This repository is public. Check the export for:

- environment URLs and environment IDs;
- the publisher prefix, if it embeds a tenant or a person's name — the lab tells learners to use
  their own, so the shipped one should be neutral;
- anything left over from testing: a knowledge source added and not removed, a connection reference
  created while experimenting.

The last one matters more here than in later labs. B5's zip is the only one whose *emptiness* is the
specification: a stray knowledge source makes B6's step 1 baseline meaningless, and it would not be
obvious from the import screen.

## Re-export triggers

Re-export whenever a volatile block in the B5 lessons or in `lab.md` is re-verified, whenever the
instruction text in step 3 changes — B6, B7 and B8 all quote parts of it back — or when a platform
update changes the solution format.
