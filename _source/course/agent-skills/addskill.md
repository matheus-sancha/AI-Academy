## TL;DR

You add a ready-made skill to a GitHub Copilot harness agent by uploading it: a bare `SKILL.md`, or a `.zip`
package with `SKILL.md` plus its supporting files. Copilot Studio validates it on the way in, and a skill that
fails a load-time check is **skipped without an error**. Because skills use an open format, the file can come
from GitHub Copilot, a colleague or a public repository, which makes it a dependency you did not write and
whose instructions your agent will follow. Read it before you add it. Then open a **new chat** before
deciding whether it worked: an upload does not reach a conversation that is already running.

## Why it matters

Adding a skill takes a minute and changes what the agent does. Its description joins the catalogue the
orchestrator chooses from on every turn, so it can take requests your tools used to win. Its body directs the
agent once it fires, including how the agent uses the tools *you* gave it. And its files come with it.

There is a good reason to want this. A skill kept in one place and added to several agents is one procedure,
not several drifting copies ({{topic:openformat}}). The cost of that convenience is that a skill is easy to
add without reading.

## How it works

### Uploading

<!-- volatile verified=2026-10 -->
Open the agent, select **Build**, then **Skills** in the components panel, then **Add skill** > **Upload a
skill**, and drag the file onto the upload box. Two shapes are accepted:

- **A Markdown file**: the skill name and description in YAML frontmatter, plus instructions.
- **A ZIP package** that must include a `SKILL.md`, and can include scripts, templates and reference
  documents.

The system validates the file and adds the skill. It then appears under **Skills** in the components panel.
<!-- /volatile -->

How a package has to be laid out inside the `.zip`, and the ways that goes wrong, is {{topic:packaging}}.

<!-- unknown since=2026-10 -->
Microsoft's page opens by saying you can also add a skill "by browsing a skill catalog", but documents only
the upload. Whether a catalogue exists in your tenant, and what is in it, has not been checked.
<!-- /unknown -->

### The load-time checks

Validation does not end at upload. Copilot Studio checks every skill when it loads, and a skill that fails is
**skipped** while the rest of the agent loads normally. Microsoft lists the usual reasons:

| Reason | Fix |
|---|---|
| Invalid YAML frontmatter | Quote values containing a colon; keep it to `key: value` pairs |
| Missing `name` or `description` | Add the field with a non-empty value |
| Description too long | Shorten it to a single line |
| Duplicate skill name in the agent | Rename one; each needs a unique name |
| `SKILL.md` unreadable, usually the encoding | Save as UTF-8 without a byte-order mark |
| A supporting file was not written | Re-export the package and upload again |
| Package rejected by a structural check | Re-export from a working editor and retry |

The supporting-file row has a nasty variant: a skill whose supporting files were only **partly** written still loads,
and then behaves differently because something it refers to is missing. Re-upload the whole package.

### After uploading

Two things are true at once, and they produce the same symptom. A skill **binds when a conversation starts**,
so the chat you uploaded from cannot see it ({{topic:conversation}}). And a skill that failed a check is
silently absent. In the old chat, both look like *the agent ignores the skill*. So the order is fixed: new
chat first; if the skill is still ignored, look for it in the components panel; if it is listed but unused,
the description is the problem ({{topic:skillmd}}).

Adding a skill also changes the routing for everything already in the catalogue, so re-run the routing tests
for your tools, not only for the new skill ({{topic:orchestration}}).

<!-- verified tenant=2026-10 -->
Microsoft's skills pages for the GitHub Copilot harness state no maximum number of skills per agent. The 8
sometimes quoted is Microsoft's figure for Agent Builder, and the quotas page's *100 per agent* is about Bot
Framework skills, a different feature. On this harness an agent accepted more than eight skills, listed them
all, and used one past the eighth in a new chat. The real ceiling has not been tested. Keep the set small
regardless: every description is in context on every turn.
<!-- /verified -->

### Replacing, downloading, deleting

An uploaded skill is edited **outside** Copilot Studio: change the file in your editor, then open the skill
and choose **…** > **Replace**. **Download** gives you the skill back as a Markdown file named after it.
**Delete** is permanent for that agent, so download first if you might want it again.

<!-- unknown since=2026-10 -->
Microsoft says a downloaded skill is "a Markdown file". Whether downloading an uploaded **package** returns its
supporting files as well is not stated. Do not rely on the agent as your copy of a bundle.
<!-- /unknown -->

### Review before you add

An added skill's instructions are read by the model as instructions. One you have not read can direct your
agent to do things you would not choose, using the tools you connected. Treat it as an unreviewed dependency,
because that is exactly what it is. Before adding one, answer in writing:

1. **Who wrote it, and who maintains it?**
2. **What does its description claim?** That is what it will fire on, in competition with your tools.
3. **What does the body tell the agent to do?** All of it, not the first screen.
4. **What does it bundle?** Open every file, scripts above all.
5. **Which tools does it expect?** A skill written for tools your agent lacks fails halfway, which is
   worse than never firing.
6. **Does anything send, post or fetch?** Instructions that move data out deserve the hardest look.

## In practice at Technik

The quality team keeps `qn-write-up` in a Git repository ({{topic:openformat}}). It ships as a package
because it bundles a template and a defect-type list. You upload the `.zip` to the Production Assistant, still
in the Preview chat you have been testing in, and ask:

> *Write up the porosity on the overlay of `XT-V2-1042` as a QN.*

The answer is generic prose. In order:

1. **New chat**, same question. If the draft now follows the template, nothing was wrong.
2. **Still generic?** Check **Skills** in the components panel. Not listed means a load-time check failed. The
   usual culprit for a skill edited on Windows is a byte-order mark, or a colon left unquoted in the
   description.
3. **Listed but unused?** The description does not match the request. Note the words the user chose, *write
   up* and *porosity*, and check they appear in it.
4. **Then re-run the routing set.** *Show open QNs on cladding for `PRJ-2031`* must still reach `Find quality
   notifications`, not the new skill.

## Design guidance

- **Read every skill before adding it**, and write the six answers down.
- **Upload from version control**, never from a copy on someone's desktop.
- **Replace rather than delete and re-add**, so the change is one step you can repeat.
- **Start a new chat after every upload or replace**, before judging anything.
- **Re-review on every update.** A changed skill is an unreviewed skill.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Ignored in the chat you uploaded from | Skills bind when a conversation starts | New chat, same question |
| Missing from the components panel | A load-time check failed, silently | Work down the checks table |
| Loads, then fails partway through | Supporting files were partly written | Re-upload the whole package |
| Takes requests a tool used to win | Its description overlaps the tool's | Narrow one, name the other in its exclusion |
| Fails halfway every time | It expects a tool this agent does not have | Add the tool, or do not use the skill |
| Behaviour changed and nobody edited the agent | Someone replaced the skill | Keep the source in version control; review every replace |

## Key terms

**Skill package**: a `.zip` holding `SKILL.md` and its supporting files.

**Load-time check**: validation Copilot Studio runs when it loads a skill; a failure skips the skill
without an error.

**Replace**: uploading a new version over an existing uploaded skill.
