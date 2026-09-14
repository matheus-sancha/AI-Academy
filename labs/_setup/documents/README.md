# Technik documents

Fictional controlled documents and intranet pages that labs use as knowledge sources. Written as
Markdown so they can be reviewed and diffed like the rest of the course; the build renders them to
HTML next to this folder in the output, and to PDF as well on a `--pdf` build.

Learners upload the **PDFs** as agent knowledge in B6, so a release build must be run with `--pdf`
before the shared folder is updated.

| File | Used by |
|---|---|
| `SOP70000101.md` Quality Notification Handling | B6, B8, A8 |
| `SOP70000114.md` Engineering Change Notification Process | B6, A4 |
| `SWI70000318.md` Cladding Preparation and Inspection | B6, B9, A4 |
| `SWI70000402.md` Hydrostatic Test During Assembly and Testing | B6, A8 |
| `DGL70000009.md` Cladding Design Guidelines | B6, A8 |
| `GWI70000027.md` Controlled Document Authoring Template | B8, A4 |
| `sharepoint/weld-overlay-acceptance.md` | B6 SharePoint knowledge |
| `sharepoint/plant-safety-and-ppe.md` | B6 website / SharePoint knowledge |

## Rules for anything added here

- **Every value is invented.** No real client, project, field, part, procedure or person.
- **Industry standards are referenced by title and number only.** Never reproduce their text; they
  are copyrighted. `sharepoint/weld-overlay-acceptance.md` shows the pattern.
- **Keep them consistent with the seed.** These documents state the numbers the seeded data is
  built around — the 3.0 mm overlay minimum behind quality notification `300001228`, the 1 bar
  hydrostatic acceptance behind the `XT-V2-1042` test failures, the priorities and states used by
  `SAP_QUALITY_NOTIFICATIONS`. Changing a number here without changing the seed makes the agent's
  answers wrong in a way that is hard to spot.
- **`SWI70000318` §4.2 is quoted verbatim in the B1 exercise.** If you edit it, edit
  `labs/B1/exercise.md` to match, and re-check the word count the exercise's answer states.
- Front matter must carry `title`, `doc`, `type`, `revision`, `owner` and `status`; the build errors
  if any is missing. `applies` is optional.

## Deliberate content

`SOP70000114` §5 explains why a released ECN does not update work orders that are already released.
That is the reasoning behind the superseded-revision defect in the seed, and B7's lab expects an
agent grounded in this document to be able to explain it.
