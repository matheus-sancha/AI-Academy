# B7 checkpoint — notes for the maintainer

Not published. `lab.md` and `exercise.md` are the only Markdown files under `labs/` that become
pages; this file stays in the repository.

`lab.md` is written as an exact build spec. Building it in a developer environment is the lab's
first test run: work through it as a learner would, and record every place the instructions do not
match what the product actually does.

## What to produce

| File | Contents |
|---|---|
| `start/TechnikAssistant_B6_end.zip` | Unmanaged solution, the agent at the B6 end state described under **What the starter contains** in `lab.md` |
| `solution/TechnikAssistant_B7_end.zip` | The same agent after steps 3–7, including `Get released revision` and the step 7 instruction |

The solution zip is also B8's starter, so its name is the contract. Do not rename it.

`start/TechnikAssistant_B6_end.zip` is **the same file as** `labs/B6/solution/TechnikAssistant_B6_end.zip`.
Build B6 first, export once, and copy it here rather than building the B6 end state twice — two
hand-built copies of the same agent will drift. `labs/B6/BUILD-NOTES.md` states that end state; the
*What the starter contains* section of `lab.md` describes it from this side, and the two must agree.

## Deliberately not in the solution zip

- **The MCP server from step 8.** Which servers are approved is tenant-specific and changes; a
  hard-coded server in the checkpoint would break on import and would age badly. Step 8 is a review
  exercise, and the checklist grades the review.
- **Anything Snowflake-side.** The view is created by the learner in step 1 and lives in their
  sandbox, not in the solution.

## Before committing either zip

This repository is public. Open the zip and check for:

- environment URLs and environment IDs;
- connection ids and connection reference display names that embed a tenant or a person;
- Snowflake account locators, usernames or role names other than the `<you>` placeholders;
- anything in the agent description or instructions that names a real organisation or person.

Re-export rather than editing a zip in place.

## Things most likely to need correcting after the first build

1. **Whether the Snowflake connector returns results in one action.** `lab.md` covers both cases in a
   volatile block in step 5. If your environment needs the flow wrapper, promote that to the main
   path and move the single-action case into the note.
2. **Exact field labels** in the tool authoring screen. Names, descriptions and the model-filled /
   fixed distinction are stable; the labels around them are not.
3. **Whether question 11 actually makes the agent ask.** If it invents a part number despite the
   input description, the checklist item is wrong and needs either a stronger input description or a
   rule in the agent instructions. Report what worked.
4. **Credit consumption** for the forty-odd test turns, so the estimate at the top of `lab.md` can be
   replaced with a measured figure.

## Re-export triggers

Re-export both zips whenever a volatile block in the B7 lessons or in `lab.md` is re-verified, or
when a platform update changes the solution format. Note the date of the export in the commit
message.
