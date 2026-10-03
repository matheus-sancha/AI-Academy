## TL;DR

On the GitHub Copilot harness, the agent creates and edits **Word, Excel, PowerPoint and PDF** files
itself, as part of doing what it was asked, and hands them back as a download. Nothing needs configuring.
Know this before you write any code to produce a file: the most common waste in a first skill is a script
that builds a spreadsheet the harness would have built anyway ({{topic:sandbox}}).

## What the harness does

<!-- volatile verified=2026-09 -->
This is a **preview** feature, documented for the GitHub Copilot harness only.

When a request naturally produces a file — a report, a deck, a spreadsheet, a chart, a script, or an
edited version of a file the user attached — the agent writes it and shows a **created file card** below
its reply, with the file name, type, a preview or icon, and a **Download** action. The card appears in
the Preview tab and in published channels: Teams, Microsoft 365 Copilot and web chat, each using its own
attachment style. The user can refer back to the file in a later turn — *"add a column for plant"* — and
the agent reads it and produces a new version.

| Limit | Value |
|---|---|
| Size per file | **10 MB**. A larger file is not surfaced; the turn continues and the agent usually says why |
| Retention | **28 days** after the conversation's last activity, then deleted |
<!-- /volatile -->

The standard harness does not list file work among its strengths; if you need a document from a
standard-harness agent, you build it, usually in a flow.

## Where it fits at Technik

Someone asks the Technik Production Assistant for *every open cladding QN on `PRJ-2031`, as a
spreadsheet*. The QN tool returns rows; the harness writes the `.xlsx`. No skill, no script, no flow. The
same applies to *"turn `SOP70000101` into a five-slide briefing"*.

What *does* earn code is what the harness cannot know: the rule that a QN write-up quotes `DEFECT_TYPE`
verbatim, or the layout of a controlled document revision. That belongs in a skill's instructions or
template ({{topic:createskill}}), and the harness still writes the file.

## Design guidance

- **Ask the agent for the file first.** Write code only for what it gets wrong.
- **Put format rules in instructions or a template**, not in a script that rebuilds the file.
- **Download anything you need to keep.** A created file is gone 28 days after the conversation goes
  quiet, and it is not a record.
- **Split large outputs**, one deliverable per file, to stay under 10 MB.
- **Test file output in the channel people use**, since each renders the card differently.

## Key terms

**Created file** — a file the agent writes during a turn and returns for download.

**Created file card** — the download card shown under the reply.

**Retention window** — how long a created file stays with the conversation: 28 days after last activity.
