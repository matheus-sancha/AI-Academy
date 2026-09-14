# B6 checkpoint — notes for the maintainer

Not published. `lab.md` and `exercise.md` are the only Markdown files under `labs/` that become
pages; this file stays in the repository.

## What to produce

| File | Contents |
|---|---|
| `start/TechnikAssistant_B5_end.zip` | Unmanaged solution, the agent at the B5 end state described under **What the starter contains** in `lab.md`: instructions, one *Work order status* topic, no knowledge, no tools, no connection references |
| `solution/TechnikAssistant_B6_end.zip` | The same agent after steps 2–8 |

## The contract with B7

`solution/TechnikAssistant_B6_end.zip` **is** B7's starter. Its name is the contract — do not rename
it — and so is its content. `labs/B7/lab.md` has a section headed *What the starter contains* that
describes this exact state. If the build here comes out differently, fix B7's description in the
same change.

The B6 end state is:

- agent *Technik Production Assistant*, standard harness, generative orchestration on;
- the B5 instructions plus the four rules added in step 5 and the description from step 8;
- the *Work order status* topic from B5, unchanged;
- knowledge: five uploaded PDFs, one SharePoint site, and Snowflake `SAP_WORK_ORDERS` and
  `SAP_WO_OPERATIONS`;
- tools: none;
- connection references: SharePoint and Snowflake.

## Prerequisite: run a --pdf build first

Step 2 uploads **PDFs** from `labs/_setup/documents/`, which only exist after `python build.py
--pdf`. Make sure the shared folder has them before anyone starts this lab.

## Before committing either zip

This repository is public. Open the zip and check for:

- environment URLs and environment IDs;
- the SharePoint site URL, which is tenant-specific — it belongs in a connection reference the
  learner re-binds, never baked into the agent;
- connection ids, and connection reference display names that embed a tenant or a person;
- Snowflake account locators, usernames, or role names other than the `<you>` placeholders.

Re-export rather than editing a zip in place.

## Things most likely to need correcting after the first build

1. **Whether Snowflake can be added as knowledge at all in your tenant and harness**, and what the
   screen calls it. If it cannot, step 6 becomes the B7 tool a module early, and both labs need
   rewriting — report this first.
2. **Whether question 8 actually produces an abstention.** If the agent still invents an ovality
   figure with the step 5 instruction in place, the instruction needs strengthening; report what
   worked.
3. **Whether question 10 is reliably wrong.** The lab claims the generated query double-counts. If
   the model finds `QUALIFY` on its own some of the time, say so — the lesson text in
   `snowflakeknowledge.md` already allows for that and the lab's step 11 depends on the variability,
   but the checklist wording may need softening.
4. **Indexing time** for the five PDFs, so step 2's warning can name a realistic figure.
5. **Credit consumption** for the fifty-odd test turns, to replace the estimate at the top.

## Re-export triggers

Re-export both zips whenever a volatile block in the B6 lessons or in `lab.md` is re-verified, when
a Technik document under `labs/_setup/documents/` is revised, or when a platform update changes the
solution format. Note the export date in the commit message.
