## TL;DR

The editor is the cheapest client to fail in, so it is where a server you are building should run
first. Adding one is now a guided flow — **MCP: Add Server** — that asks for a transport, an ID and a
scope, and writes the file for you. Which file has moved: the global target is
`$COPILOT_HOME/mcp-config.json`, a workspace-root `.mcp.json` is shared with the team behind an
experimental setting, and `.vscode/mcp.json` plus the user-profile `mcp.json` are "labeled deprecated
in the guided flow". Tools are controlled outside the file, trust is asked for once, and your
organization "can restrict which servers are available".

## Why it matters

Your server will meet three clients in its life — the editor, Copilot Studio ({{topic:mcpcs}}) and
your own agent ({{topic:stageagent}}) — and only the first lets you watch it while the code is still
open. A wrong tool description is a five-second edit here and a redeployment later.

The second reason is less pleasant. {{topic:vscode}} commits `.vscode/mcp.json` as a workspace
artefact and {{topic:agentmode}} explains why the agent does not read it directly; the current
documentation marks that file deprecated in favour of two other places. Nothing has broken, but
anyone saying "put it in `.vscode/mcp.json`" is teaching the compatibility path, and knowing that is
the difference between following a prompt and understanding it.

## How it works

### Six ways in, one of which you should use

<!-- volatile verified=2026-11 -->
**MCP: Add Server** from the Command Palette is the path to learn. It asks for the transport — "HTTP
(HTTP or Server-Sent Events)" for a URL or "Command (stdio)" for a launch command — then a server ID
not already in use, then a scope, then shows "any server trust or authentication prompts". The same
picker offers **Browse MCP Servers…**, an **Add from another application…** discovery option, and
model-assisted setup from an **NPM Package**, **Pip Package** or **Docker Image**, where you should
select "Allow" "only if you trust the source".

The others are a gallery in the Extensions view under `@mcp` (Preview), where **Install in Workspace**
shares the configuration "with the project"; a Customization Marketplace under **Chat: Open
Customizations** → **Browse** (Preview); and a publisher's own URL or command. Agent plugins can
bundle servers, and Copilot connectors are in preview.
<!-- /volatile -->

### Where the file goes now

<!-- volatile verified=2026-11 -->
| Scope | File |
|---|---|
| Personal, all workspaces | `$COPILOT_HOME/mcp-config.json`, or `~/.copilot/mcp-config.json` when `COPILOT_HOME` is unset |
| Shared with a team | `.mcp.json` at the workspace root, offered "only when experimental setting `chat.mcp.workspaceRootConfig.enabled`" is on |
| Compatibility | `.vscode/mcp.json` and the user-profile `mcp.json`, which "remain available for compatibility and are labeled deprecated in the guided flow" |

Two format facts decide which you can use. "Portable files use a top-level `mcpServers` object. The
VS Code format uses `servers`", and "Portable configurations don't support VS Code input variables or
environment files."
<!-- /volatile -->

That second sentence closes a loop from {{topic:agentmode}}: the VS Code format's `${input:…}`
variables are what stops a server being forwarded to the agent, and the portable format that fixes
the forwarding has no input variables to offer. A server needing a secret at launch reads it from the
environment instead ({{topic:localenv}}).

### Trust, and what it is not

The caution is blunt: "Local MCP servers can run code on your machine, and tools can access external
services using your permissions." The advice is to "Review the publisher, command or endpoint, and
requested access before installing or starting a server", and "Only trust configurations you have
reviewed." Approval requests appear as you go — "Approve only actions you understand."

Trust here is a decision, not a sandbox. The page says nothing about isolating a server, and what
sandboxing exists is narrower than people assume: on Windows a local stdio server is not sandboxed
({{topic:permissions}}). A server you trust in the editor is a process with your access.

### Tools, resources and prompts

Tool selection happens outside the server file. "To control available tools in a Copilot session,
open **Chat: Open Customizations** → **Tools**", and "For Local harness sessions, use **Configure
Tools** in the chat input." Keeping that list short is a context decision as much as a correctness
one ({{topic:toolshaping}}).

"Servers can provide more than tools." Resources arrive through **Add Context** → **MCP Resources**
or **MCP: Browse Resources**. Prompts are invoked as `/<server>.<prompt>`. And MCP Apps
(Experimental) mean "supported servers can display interactive forms or visualizations in chat" —
the first case where a server's output is a surface rather than text.

> [!IMPORTANT]
> Availability is not only yours to decide. "Your organization can restrict which servers are
> available", and what you see "depends on the harness and your organization's preview-feature and
> marketplace policies" ({{topic:agent365}}).

<!-- unknown since=2026-11 -->
The page that covers adding a server defers trust details, start/stop/restart, log viewing and
configuration sync to other pages, and names no MCP protocol revision. So what VS Code negotiates
with a server, and how a `uv run --directory` launch resolves its working directory, are still
unverified here as they were in {{topic:agentmode}} — check both on your first real run.
<!-- /unknown -->

## In practice at Technik

The Teamcenter server's whole development loop is a question, an answer and a comparison. The
repository ships the launch definition on the compatibility path:

*From [`.vscode/mcp.json`, lines 1–9](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/.vscode/mcp.json#L1-L9):*

```json
{
  "servers": {
    "technik-teamcenter": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "--directory", "${workspaceFolder}", "server/teamcenter.py"]
    }
  }
}
```

It is the VS Code format, with `servers` and `${workspaceFolder}`, and it is the file now labelled
deprecated — a fair example of what a repository written against one revision of the documentation
looks like months later. Moving it to a workspace-root `.mcp.json` means renaming the key to
`mcpServers` and enabling an experimental setting; keeping it means staying on a supported
compatibility path. Either is defensible, and the choice belongs in a pull request.

The question to ask, once it starts, is the one that catches a lying agent: *which drawing does work
order `100004510` operation `0010` use, and is that revision still released?* The right answer needs
two tools and names drawing `DU700001042` at revision B against released revision C under
`ECN70000051`. An agent that answers from one tool, or from the model's own sense of which letter is
highest, gets it wrong — and watching it do that in the editor is how you learn that the second tool
needs a description saying when to reach for it ({{topic:tooldesc}}).

The failure to expect first is the quiet one: the server starts when you launch it yourself and the
agent insists it has no such tools. The documentation's triage is to "check config scope, runtime,
server output"; the course's answer is in {{topic:agentmode}}.

## Design guidance

- **Run it in the editor before any other client.** Everything after this costs a deploy.
- **Decide the config scope deliberately.** Personal, shared with the team, or compatibility — a
  different file and a different audience each time.
- **Prefer environment variables to launch-time inputs**, since the portable format has no input
  variables and inputs block forwarding.
- **Review a server as a dependency.** It runs with your permissions and is not sandboxed everywhere.
- **Enable only the tools the task needs**, in Customizations rather than by editing the server.
- **Test the question you are afraid of**, not the one you know works.
- **Expect the organization to have a say.** A server that works for you may be blocked for the team.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The server runs for you, the agent sees no tools | The agent does not read `.vscode/mcp.json` directly | Check which file the harness reads ({{topic:agentmode}}) |
| A teammate's server never appears | It was installed personally, not in the workspace | Install in Workspace, or commit the shared file |
| The guided flow calls your file deprecated | It is the compatibility path | Decide between moving and staying, in a pull request |
| A server works at home and not at work | Organization restrictions on available servers | Ask about the allow-list before debugging |
| A `${input:…}` server silently never loads | Input variables stop forwarding, and portable files have none | Read secrets from the environment |
| Nothing explains why a tool was skipped | Tool availability is not tool choice | Read the description the orchestrator saw |

## Key terms

**Server ID** — the key identifying a server in a configuration file; it must be unique in the file
the guided flow writes to.

**Portable configuration** — the `mcpServers` format shared with other Copilot tools; no VS Code
input variables and no environment files.

**MCP Apps** — an experimental capability letting a server render interactive forms or visualizations
in chat rather than returning text.
