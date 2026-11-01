## TL;DR

The Copilot Studio extension for VS Code clones an agent out of the cloud as **YAML files on disk**,
lets you edit topics, tools, triggers and knowledge references with an editor's tooling, and sends
the changes back. It is generally available, not a preview. The thing to understand before you use
it is the synchronisation model: **Get** overwrites your uncommitted local changes, and **Apply**
modifies the live agent immediately — and is *not* a publish. Both of those are safe only if the
folder is under Git from the first minute, which is why the first thing to do after a clone is
commit.

## Why it matters

A low-code agent is a real artifact with real behaviour, and until it is a file it cannot be
diffed, reviewed, branched or reverted. {{module:publishing-and-environments}} was about moving
*packages* between environments; this is the definition itself, in a form two engineers can argue
over line by line.

That unlocks the workflow the rest of this level assumes. A change to an agent's instructions
becomes a pull request with a reviewer ({{topic:git}}), a regression becomes a diff with a date and
an author, and the definition becomes something an editor agent can help write — the documentation
explicitly envisages using Copilot or another harness on these files.

It also closes a gap that would otherwise split this level in two. Pro-code agents get engineering
discipline by default because they are code; without this extension, the low-code agents an
organisation already depends on stay outside it.

## How it works

### What you need

<!-- volatile verified=2026-11 -->
The prerequisites are narrower than most VS Code extensions, and the operating-system line is the
one that catches people: **Windows x64** (Windows 10 version 1809 or later, or Windows 11) or
**macOS**. Linux is not listed. You also need VS Code 1.80 or later, a Copilot Studio licence or
access, permission to reach at least one environment, and read and write access to the agents you
intend to edit.

Installation is from the Extensions pane — search for Copilot Studio and check the publisher is
Microsoft. The first run signs you in through the browser, requesting permission to read and write
agents, read environment information, and sync files to the cloud.
<!-- /volatile -->

Every page of this extension's documentation carries a note that it describes features of agents on
the **standard harness**. If your agent is on a different harness, confirm the fit before planning
a workflow around it ({{topic:chooseharness}}, {{topic:ghharness}}).

### Clone, edit, sync

<!-- volatile verified=2026-11 -->
Cloning downloads the agent definition and its components into a structured folder. The usual route
is the extension's Agents view: pick an environment, right-click the agent, choose **Clone agent**
and select a folder. There is a command-palette equivalent, and a third route that takes the
agent's portal URL. **Copilot Studio: Reattach Agent** connects an existing local folder back to its
cloud agent.

What lands is YAML: a top-level agent definition, plus folders for topics, tools and connector
actions, workflows, triggers, knowledge file references and settings. Editing is ordinary editor
work — IntelliSense over the schema, project-wide search, and the Problems pane for validation
errors.

Three synchronisation operations move work between disk and cloud:

| Operation | Direction | What it does |
|---|---|---|
| **Preview** | Cloud → local | Shows remote changes without applying them |
| **Get** | Cloud → local | Downloads and applies remote changes. **Overwrites uncommitted local changes** |
| **Apply** | Local → cloud | Uploads your changes. **Modifies the live agent immediately** |
<!-- /volatile -->

Two of those deserve to be read twice.

**Apply is not publish.** It changes the agent's definition in the environment; it does not push
that definition to the agent's published channels. Conflating the two steps is how a change appears
to have "not taken effect" ({{topic:publish}}).

**Get overwrites.** The confirmation says so, and the only reliable protection is work already
committed. Apply is also blocked while remote changes remain unretrieved, forcing the merge onto
your machine rather than silently into the cloud.

<!-- volatile verified=2026-11 -->
The documented preconditions for Apply are worth treating as a checklist: no unresolved conflicts,
Preview and Get run against the latest remote state, no validation errors in the Problems pane,
changes committed to Git if you use it, and permission to modify the agent.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
The documentation does not publish a list of agent components the extension cannot represent, and
its own examples use more than one file-naming convention, so the exact layout a clone produces is
best read from a real clone rather than from the page. Nothing here has been checked in a tenant.
<!-- /unknown -->

## In practice at Technik

Technik's Production Assistant was built in a browser, and its instructions have been edited by
three people over two months with no record of who changed what or why. Cloning it changes the unit
of work from *a session in a portal* to *a commit*.

The sequence that makes this safe is short, and the order is the whole point. Clone the agent,
**initialise Git and commit immediately** — that commit is the only copy of the current behaviour
that survives a Get. Branch, edit the instruction file, and open a pull request so a second engineer
reads the change as a diff rather than hearing it described. Merge, Get any remote change, Apply,
test in the browser's test pane, publish separately.

What this buys is specific. The assistant's rule about not naming work orders it did not retrieve,
and its abstention behaviour, are one or two sentences in a file — exactly the kind of change that
is made quickly, breaks a tested behaviour and cannot be attributed a month later. As a diff it is
reviewable; as a commit it is revertible. The evaluation set
{{module:testing-and-evaluation}} built is what tells you a revert was needed.

The browser does not disappear: testing the conversation, reading analytics and publishing stay
there. The editor owns the definition, and the portal owns the runtime.

## Design guidance

- **Commit before you do anything else.** Get overwrites uncommitted work, and a clone with no
  initial commit has no floor.
- **Treat Apply as a deployment**, not a save. It changes a live agent.
- **Keep Apply and publish separate in your head and in your runbook.**
- **Always Preview before Get**, and Get before Apply, so merges happen where you can see them.
- **Review agent definitions like code.** An instruction change deserves the scrutiny a code change
  gets.
- **Let an editor agent draft components, and review them as drafts.** Your pull request is still
  the gate.
- **Check the harness note applies to your agent** before building a team workflow on this.
- **For moving between environments, keep using solutions.** This extension edits an agent in an
  environment; promotion is a different mechanism ({{topic:solutionsdeep}}, {{topic:pipelines}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Local edits vanished | Get overwrote uncommitted changes | Commit immediately after cloning, and before every Get |
| Apply is greyed out | Remote changes have not been retrieved | Preview, then Get, resolve conflicts, then Apply |
| The change is live in the portal but users see the old behaviour | Apply is not publish | Publish separately ({{topic:publish}}) |
| The extension will not install | Linux is not a listed platform, or VS Code is older than 1.80 | Use a supported platform and update VS Code |
| Sign-in succeeds but no agents are listed | No access to an environment, or no read/write on the agents | Check environment access and agent permissions |
| Apply fails validation | Errors in the Problems pane | Fix them before applying; the pane is the gate |
| Knowledge files are missing locally | Remote knowledge documents are not downloaded automatically | Select them for download explicitly |
| Removing the extension left files behind | Uninstalling does not delete local clones | Delete the folders yourself |

## Key terms

**Clone** — downloading an agent's definition and components from Copilot Studio into a local
folder.

**Reattach** — connecting an existing local folder back to its cloud agent.

**Preview / Get / Apply** — inspect remote changes, pull them down, push yours up.

**Apply is not publish** — Apply changes the agent's definition in the environment; publishing
releases it to its channels ({{topic:publish}}).

**Agent definition** — the YAML describing the agent's topics, tools, triggers, knowledge and
settings.

**Standard harness** — the harness this extension's documentation describes
({{topic:chooseharness}}).
