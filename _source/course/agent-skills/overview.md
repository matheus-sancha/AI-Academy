## What this module is for

By now the Technik Production Assistant has instructions, knowledge and tools. It can find things and it can call
things. What it lacks is **know-how**: a written, reusable account of how Technik does a particular kind of task,
such as writing up a quality notification in the format `SOP70000101` requires.

A skill is that know-how as a file: a name, a description, Markdown instructions, and optionally the templates,
reference lists and scripts the procedure needs. The runtime keeps only the description in view and loads the
rest when a request matches it, so an agent can hold a great deal of procedure without paying for all of it on
every turn. The fact the module is built around is that **the description is the whole activation mechanism**.
A skill whose description does not match how people ask is indistinguishable from a skill that is not there.

Skills also mark the point where what you write stops belonging to Copilot Studio. The format is an open
specification, so the `SKILL.md` you write here is the same artifact {{module:authoring-skills}} picks up in an
editor.

## Before you start

You want {{topic:instructions}} and {{topic:contextcost}}, because a skill is mostly an argument about what
should *not* be in the instructions. {{topic:tooldesc}} matters most: skills are chosen by the same
description-matching as tools, and this module reuses its four-part description without re-teaching it.
{{topic:conversation}} explains the one behaviour that wastes the most time here: a skill does not reach a
conversation that is already running.

Skills exist only on the GitHub Copilot harness ({{topic:chooseharness}}). The last lesson covers agents on the
standard harness. Nothing here needs a tenant to read; allow about 90 minutes.

## What you will be able to do

By the end of this module you should be able to:

- say what a skill is made of, and how progressive disclosure decides what it costs;
- decide whether a behaviour belongs in a tool, a skill, a topic or the instructions, and defend the choice;
- explain what the open format makes portable and what it does not;
- write a `SKILL.md` whose frontmatter loads and whose description fires on the right requests;
- add a skill from elsewhere, and say what you checked before you did;
- create a skill in the portal and test its trigger before its output;
- package a skill so it arrives intact, and check the archive before uploading it;
- say when a skill needs a script, and what the sandbox will not let one do;
- manage the set of skills on an agent other people use;
- share behaviour between standard-harness agents without skills.

## The thread through this module

One skill runs through it: `qn-write-up`, which drafts a quality notification in Technik's format from a
described defect.

{{topic:skill}} and {{topic:skillsvs}} establish why it is a skill: a template, a procedure, an output format of
its own, and a request that comes up a few times a week among hundreds of others. {{topic:openformat}} puts its
source in the quality team's Git repository and writes its tool dependency as a fallback, so the same folder
works in VS Code. {{topic:skillmd}} takes the file apart, line by line. {{topic:addskill}} uploads it and works
through the order of checks when it seems to be ignored.

The second half builds outwards. {{topic:createskill}} writes a smaller skill from blank, `wo-delay-note`, and
tests its trigger against six real requests. {{topic:packaging}} ships `qn-write-up` as an archive that does not
break on Windows. {{topic:sandbox}} gives it a script to check 140 thickness readings against `SWI70000318`, and
turns down two others. {{topic:skillscs}} looks at the assistant's whole installed set at publish time.
{{topic:reuse}} takes the procedure to a help desk on the standard harness, which cannot hold a skill at all.

## Self-check

<details>
<summary>1. Your new skill never fires. Where do you look, and in what order?</summary>

A new chat first, because a skill binds when a conversation starts, and the chat you uploaded from cannot see it
({{topic:conversation}}). If the skill is still ignored, open **Skills** in the components panel. Not listed
means a load-time check failed silently: a byte-order mark, an unquoted colon, a missing field
({{topic:addskill}}).

Only if it is listed and still unused is the description the problem. Compare it with the words people actually
used. What almost never helps is rewriting the body. The runtime does not read the body until the description
has already matched ({{topic:skill}}).
</details>

<details>
<summary>2. A colleague wants "always cite the document number and revision" as a skill, so it is in one place. What do you tell them?</summary>

That it belongs in the instructions. A skill applies only when its description matches the request, so a rule
that must hold on every answer would depend on whether this particular question looked like a citation request.

The earns-a-skill test makes the same point: no bundled material, no procedure, no output format of its own,
and needed on every turn, not some of them ({{topic:skillsvs}}). One sentence in the instructions, always read,
is strictly better.
</details>

<details>
<summary>3. The quality team zipped the qn-write-up folder in Explorer and the upload failed with no useful explanation. What are the likely causes?</summary>

Two, both about the archive rather than the skill. The archive wraps the `qn-write-up/` folder, and Copilot
Studio wants `SKILL.md` at the **root**. Or it was built with `Compress-Archive`, which writes backslash entry
paths the zip format forbids.

List the entries before uploading: the first should be `SKILL.md`, and none should contain a backslash. If the
upload succeeds and the skill then fails to appear, it is the load-time checks instead ({{topic:packaging}}).
</details>

<details>
<summary>4. A skill bundles a script that fetches a work order's QN history from an API, and it fails every time, though the import works. Why, and what is the fix?</summary>

The sandbox has no network. `requests` imports cleanly, which is why the script looks fine, and the first call
fails because there is nothing to call over. Availability is not usability.

The fix is not a better script. The data should come from a tool: `Find quality notifications` already returns
it, through the orchestrator, which scripts cannot reach. Then pass the data to a script only if something has
to be computed exactly. Usually nothing does, and the script can go ({{topic:sandbox}}).
</details>

<details>
<summary>5. Technik's standard-harness help desk wants the QN write-up. Name two ways to give it the behaviour, and what each costs.</summary>

**Delegate** to the Production Assistant as a connected agent. One copy of the procedure stays in the skill;
the cost is a hop of latency and a handoff that has to carry context. Whether a standard-harness agent can
connect to a GitHub Copilot harness agent has not been confirmed, so test it before relying on it.

**Duplicate** it into a prompt or a flow the help desk calls. It works today, and from then on two copies of the
procedure exist. If you do that, generate the copy from the skill's file and record that you did, so the next
revision of `SOP70000101` updates both ({{topic:reuse}}).
</details>
