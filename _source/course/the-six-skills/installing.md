## TL;DR

The toolchain runs on an agent built with the **GitHub Copilot harness**, because skills exist on no other. Download
the six files from the release this course is pinned to, {{skills-version}}, and upload them through **Build** >
**Skills** > **Add skill** > **Upload a skill**: five `.md` files and one `.zip`. Then open a new chat. The rule
people get wrong comes at the other end. The six are **scaffolding**, and no `copilot-*` skill belongs on an
agent you publish. Removing them is the first step of stage 7, not tidying up afterwards.

## Why it matters

Installing goes wrong in two places, and neither produces an error.

The first is the start. The harness is fixed when an agent is created, so a reader who built their practice
agent on the standard harness has no **Skills** section to upload to. They find out at the first step of the
guided build, and the only fix is a new agent.

The second is the end. A `copilot-*` skill left on a published agent is not inert. Its description stays in
the catalogue the orchestrator reads on every turn, competing with everything you built. The router's
description includes users who *ask what to do next*. That is exactly how a supervisor talks to a production
assistant about a work order.

## How it works

### The prerequisite

<!-- volatile verified=2026-10 -->
You choose the harness when you create an agent, and an agent cannot be moved between harnesses afterwards.
Skills are documented only for the GitHub Copilot harness, and its Build tab lists them beside Instructions,
Knowledge, Tools, Model, Connected agents and Memory.
<!-- /volatile -->

Build in your own developer environment ({{topic:devenv}}), not in an environment other people use. Everything
the route builds stays out of the agent until stage 7, but the six skills are in it from the first upload.
Microsoft also notes on every one of these pages that building and testing on this harness can consume
Copilot Credits ({{topic:whatyouneed}}).

### Download from the pinned release

The upstream README's download links point at the **latest** release. A later release may rename a skill or
change a stage, and this course would not know. Download from
[the {{skills-version}} release page]({{skills-release-url}}) instead, where the release name and the course's
pin should match.

The release carries seven files:

| File | Shape | Why |
|---|---|---|
| `copilot-studio-agent-creator.md` | bare `.md` | A single `SKILL.md` |
| `copilot-agent-review.md` | bare `.md` | A single `SKILL.md` |
| `copilot-instructions-creator.md` | bare `.md` | A single `SKILL.md` |
| `copilot-find-skills-and-tools.md` | bare `.md` | A single `SKILL.md` |
| `copilot-skill-creator.zip` | `.zip` | Bundles output playbooks and Python templates, and only a package brings those along |
| `copilot-evaluation-creator.md` | bare `.md` | A single `SKILL.md` |
| `script-probe.zip` | `.zip` | A tenant diagnostic. Not part of the route; leave it out |

Do not unzip and re-zip `copilot-skill-creator.zip`. The release is built with `SKILL.md` at the archive's root
and forward-slash entries. Re-zipping in Explorer or with `Compress-Archive` can break either, and an archive
that has been broken this way looks like a broken skill ({{topic:packaging}}).

### Upload all six

<!-- volatile verified=2026-10 -->
Open the agent, select **Build**, then **Skills** in the components panel, then **Add skill** > **Upload a
skill**, and drag one file onto the upload box. Copilot Studio validates it and adds it. Repeat for the other
five.
<!-- /volatile -->

<!-- verified tenant=2026-09 -->
All six install into one agent together and all six are listed in the components panel.
<!-- /verified -->

Check that list before anything else. A skill that fails a load-time check is skipped silently, so a missing
row is the only sign ({{topic:addskill}}). Then select **New chat**. The chat you uploaded from cannot see any of
the six ({{topic:notrunning}}), and the new one is the conversation you will keep for the whole build.

The toolchain takes six of the agent's skill slots, and that leaves room.

<!-- verified tenant=2026-10 -->
Eight is Microsoft's figure for Agent Builder, a different surface, and it does not hold here. An agent on the
GitHub Copilot harness accepted more than eight skills, listed them all, and used one past the eighth in a new
chat. How many more it takes has not been tested.
<!-- /verified -->

### Removing them is a step in the build

<!-- volatile verified=2026-10 -->
To delete a skill, select the **X** next to it in the components panel, then **Delete** to confirm. Deletion
is permanent for that agent. Microsoft advises downloading a skill first if you might want it again; for these
six, the release page is your copy.
<!-- /volatile -->

You do not plan this yourself. At stage 7 the router hands over `publish-copy.md` and then an install checklist
whose **first step** deletes all six, before anything the build produced is uploaded. Save `publish-copy.md`
before you start that checklist, because step 1 deletes the skill that wrote it.

The reason for doing it first is not room. The skills in the components panel are part of what you publish
({{topic:skillscs}}), and the six are build tools, not part of the agent you ship. Deleted at step 1, they
cannot be forgotten at step 7. Delete by hand only if you stop part-way through the route, and then check the
panel before any publish.

## In practice at Technik

You create the Technik Production Assistant on the GitHub Copilot harness in your developer environment,
download the six from the {{skills-version}} release page, and upload them. The components panel lists six
skills and nothing else. You select **New chat** and say:

> *Help me build this agent. Where do I start?*

The router answers with its placement question, which is how you know all six are live.

Stage 7, weeks later. You save `publish-copy.md`, then work the checklist. Step 1 deletes the six and step 2
uploads `qn-write-up`. Before publishing you check the panel. It should show `qn-write-up` and nothing that
begins `copilot-`.

Now picture the step skipped. A supervisor asks the published assistant *what do I do next on `100004521`?*
That matches the router's description, *asks what to do next*. Another asks it to *draft a QN in our format*,
and `copilot-skill-creator`'s description, *needs an agent to produce a document in a fixed format*, now
competes with `qn-write-up` for it. Neither user did anything wrong.

## Design guidance

- **Confirm the harness before you download anything.** No Skills section means the wrong harness.
- **Download from the pinned release, not `latest`**, and finish the build on the version you started.
- **Count the rows in the components panel** after uploading. Six, every time.
- **Save `publish-copy.md` before stage 7's first step.**
- **Check the components panel before every publish.** No `copilot-*` row, whether you finished the route or
  abandoned it.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| No **Skills** section in Build | The agent is on the standard harness | Create a new agent on the GitHub Copilot harness |
| Five skills listed after six uploads | One failed a load-time check, silently | Re-download that file from the release and upload again |
| `copilot-skill-creator` rejected or broken | The `.zip` was unzipped and re-zipped | Upload the release asset unchanged |
| The router never answers | You are still in the chat you uploaded from | New chat |
| Stage names do not match this course | Downloaded from `latest`, not the pin | Use the {{skills-version}} release page |
| No short description to paste at publish | Step 1 ran before `publish-copy.md` was saved | Write it from the brief's role and users slots |
| Published agent answers users with build questions | A `copilot-*` skill was left installed | Delete it and publish again |

## Key terms

**Scaffolding**: skills used to build an agent and removed before it is published.

**Release asset**: an uploadable file attached to an upstream release: a bare `.md` or a `.zip`.

**Pinned release**: the upstream release this course is written against, {{skills-version}}.
