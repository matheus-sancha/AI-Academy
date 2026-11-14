## TL;DR

In agent mode the model does not suggest code, it **acts**: it plans a change, edits several files,
runs terminal commands and calls tools, including MCP servers you configured. The engineering in
using it well is almost entirely about **approvals** — which actions it may take without asking, and
which it may never take unattended. The defaults ask you about most things. The settings that stop
it asking are convenience features and the documentation is unusually blunt that they are **not
security boundaries**. Treat an agent session as a junior engineer with your credentials: give it
context, review every diff, and never let it run unattended against anything you cannot undo.

## Why it matters

Agent mode changes what a mistake costs. An inline suggestion you ignore costs nothing; an agent
that ran six terminal commands and edited nine files costs a review, and occasionally a recovery.

It also opens a path that did not exist before. Tool results come from outside your repository — a
web page, an issue description, a row in a database — and the documentation says plainly that they
can carry prompt-injection attempts, with tool approval as the protection. That is
{{topic:injection}}'s argument arriving in your editor, where the tools in reach include your shell
and your files.

The third reason costs the most time: an agent working without context produces plausible, wrong
changes quickly. The fix is better repository context, not a better prompt
({{topic:customize}}, {{topic:tooldesc}}).

## How it works

### Modes and permission levels

Agent mode is chosen from the agent picker in the chat input. On the Copilot harness, **Autopilot**
is a further mode that auto-approves all tools, retries after errors and answers questions that
would otherwise block it; on the Local harness, Autopilot is a *permission level* rather than a
mode. The same word means two things in two menus, with the same safety implication.

<!-- volatile verified=2026-11 -->
Permission levels are chosen per session from the permissions control, and the default for new
sessions is set by `chat.permissions.default`:

| Level | What it does |
|---|---|
| **Manual** (default) | Uses your approval settings; prompts as configured |
| **Assisted** | An LLM judge assesses each tool call. The documentation states this is **not a security boundary** |
| **Allow all** | Runs every tool call without confirmation |
<!-- /volatile -->

### Approvals, and what the scopes mean

When a tool needs approval, the prompt can be expanded to show the call's inputs first. Approval
can be granted for a single use, for the session, for the workspace, or for all future invocations
— and that last option outlives the problem you were solving. **Chat: Manage Tool Approval** lists
what you have approved, and **Chat: Reset Tool Confirmations** clears the lot, which is the right
move after a week of clicking *allow* under deadline.

<!-- volatile verified=2026-11 -->
The auto-approval settings are worth reading as a group, because they are the policy surface:

| Setting | Controls |
|---|---|
| `chat.tools.global.autoApprove` | Auto-approval across all workspaces |
| `chat.tools.eligibleForAutoApproval` | Per tool; `false` always forces a manual prompt |
| `chat.tools.terminal.autoApprove` | Per command: `true`, `false`, or a `/regex/` |
| `chat.tools.terminal.enableAutoApprove` | Turn terminal auto-approval off entirely |
| `chat.tools.edits.autoApprove` | Glob patterns over files, e.g. `"**/.env": false` |
| `chat.agent.sandbox.enabled` | Sandboxing for terminal commands |

Two sentences there are worth memorising. A `false` rule **requires approval; it does not block the
command** — a speed bump, not a wall. And terminal auto-approval is a best-effort convenience, not
a security boundary. Sandboxing is described the same way: an added layer, not a virtual machine or
user-account boundary. It confines shell execution and child processes on Windows, macOS and Linux,
independently of the permission level. Sandboxing a local **MCP server** is macOS and Linux only, and
only over stdio ({{topic:permissions}}).
<!-- /volatile -->

### Tools, and the ceiling on them

The agent picks from the enabled tools. There are three sources — built-in, MCP and extension — and
one hard limit: **a request may have at most 128 tools enabled**. Connecting four chatty MCP
servers reaches that faster than expected, which is a reason to curate tools per task rather than
enable everything ({{topic:toolshaping}}).

### Where MCP configuration actually lives

There are three configuration formats: the VS Code
format in `.vscode/mcp.json` with a top-level `servers` key, a portable `.mcp.json` at the workspace
root with `mcpServers`, still experimental, and a Copilot user file. They are not interchangeable,
and — the part that surprises people — **the agent does not read `.vscode/mcp.json` directly**. VS Code forwards
eligible servers from it, excluding any that need an `${input:...}` variable. A server that starts
fine from the file you edited and stays invisible to the agent is usually this
({{topic:mcpvscode}}).

## In practice at Technik

The capstone's Teamcenter server is the first tool an agent session at Technik gets, and the first
question is which approvals it should run under.

Reads are the easy half. The server's three tools are read-only by construction — they connect as
`TECHNIK_AGENT_RO`, which cannot write anything ({{topic:sfroles}}) — so approving them for the
session costs little, because the platform rather than a setting bounds the damage. The approval
dialog is the weaker guarantee; the role is the stronger one.

Edits and terminal commands are the other half, and here one glob earns its place:

```json
"chat.tools.edits.autoApprove": {
  "**": true,
  "**/.env": false
}
```

The agent may edit the repository freely and must ask before touching the file that holds Technik's
Snowflake key — a prompt, not a prohibition.

The injection path is not hypothetical here. Technik's quality notifications are free text typed on
the shop floor, and the seed carries one whose description addresses the agent directly. In Copilot
Studio that text reached an agent whose tools were read-only; in your editor it can reach a session
holding your shell. The server has not changed, and the blast radius has
({{topic:ctxsecurity}}, {{topic:threats}}).

<!-- unknown since=2026-11 -->
Two things about this setup were never confirmed against a running editor, because the capstone was
built and tested offline: **which MCP protocol version VS Code negotiates** with a v2 server, and
the **working-directory behaviour** of a launch command that passes its own directory flag from
`mcp.json`. Both are things to check on your first run rather than assume ({{topic:buildsetup}}).
<!-- /unknown -->

## Design guidance

- **Keep approvals scoped to the session.** *Always allow* outlives the task that justified it.
- **Rely on identity, not on dialogs.** A read-only role is a boundary; an approval setting is a
  reminder.
- **Require approval for secrets and for anything outside the repository**, knowing it prompts
  rather than blocks.
- **Curate tools per task.** A smaller tool set also improves the agent's choices.
- **Review every diff before it is committed**, and never delegate that review to the agent that
  wrote the change.
- **Never run unattended against production, or against anything without a backup.**

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent cannot see an MCP server you configured | The agent does not read `.vscode/mcp.json` directly; servers needing `${input:...}` are not forwarded | Remove the input variable, or use the portable format behind its experimental setting |
| A request fails complaining about the number of tools | More than 128 tools enabled | Disable servers or tool sets you are not using for this task |
| The agent edited a file it should have asked about | A broad auto-approve glob, or an approval granted for all future invocations | Add a `false` rule for the path; reset tool confirmations |
| A `false` rule did not stop a command | `false` requires approval rather than blocking | Remove the tool, or do not enable the server |
| A local MCP server runs unsandboxed | MCP server sandboxing is macOS and Linux only, unlike agent sandboxing | Use a container or a disposable machine instead |
| Behaviour changed after switching machines | Approvals and tool sets live in your user profile | Put project configuration in the repository ({{topic:customize}}) |
| The agent followed an instruction found in data | A tool result carried an injection, and the tool was pre-approved | Approve tools that read external text per use; keep tool identities read-only |

## Key terms

**Agent mode** — the mode in which the model plans, edits multiple files, runs commands and calls
tools, rather than suggesting text.

**Autopilot** — the mode (or, on the Local harness, permission level) that auto-approves tools,
retries on error and answers blocking questions.

**Permission level** — the per-session policy for tool calls: Manual, Assisted or Allow all.

**Approval scope** — how long an approval lasts: one use, the session, the workspace, or forever.
