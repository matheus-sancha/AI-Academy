## TL;DR

From here on, the thing you build is a **repository**, and VS Code is where you build it. Everything
this level produces — an MCP server, an agent definition, a SQL seed, an evaluation script — is a
file under source control rather than a form in a browser. Set up four things once: GitHub Copilot
signed in, the Copilot Studio extension if you maintain low-code agents, the language tooling for
whichever language you picked, and the workspace files that make a clone of your repository behave
the same on a colleague's machine. The last of those is the one engineers skip, and it is the one
that makes the difference between a toolchain and a pile of personal settings.

## Why it matters

Up to now the editor was optional. Agents were built in a browser, their knowledge was uploaded,
their tools were picked from a list, and the artifact was a row in an environment you could not
diff. That worked, and {{module:copilot-studio-basics}} is where it works best.

It stops working as soon as two people maintain the same agent, or as soon as the agent's behaviour
has to be reviewed before it reaches anyone. A browser form has no history, no branches, no second
reader and no way to say *this change, these three files, because of this ticket*. Moving to files
buys all of that, and the cost is that you now own a machine — a runtime, dependencies and secrets
({{topic:localenv}}).

There is a second reason, less obvious and more important. The editor is also where you talk to an
agent that edits your code. The same repository that holds your work holds the instructions, tool
configuration and permissions that shape how that agent behaves ({{topic:customize}}). Your editor
setup is therefore part of your agent design, not a preference.

## How it works

### Signing in to Copilot

Copilot is reached from the Copilot icon in the **Status Bar**, which offers **Use AI Features** and
then a choice of sign-in method. An account that already has a Copilot subscription uses it; an
eligible account without one is enrolled in the **Copilot Free** plan, which carries a monthly
allowance of inline suggestions and AI credits.

<!-- volatile verified=2026-11 -->
Two settings are worth knowing on day one. `chat.disableAIFeatures` turns chat and inline
suggestions off and can be set per workspace as well as per user — useful on a repository where you
do not want suggestions at all. Telemetry is enabled in the free plan, and
`telemetry.telemetryLevel` set to `off` is the documented way out. Signing in against a GitHub
Enterprise instance is a separate choice in the sign-in dialog, and can be pinned with the
`github.copilot.advanced` setting's `authProvider` key.
<!-- /volatile -->

### What "agent" means in the editor

The vocabulary has settled in a way worth stating plainly, because it differs from Copilot Studio's.
An agent here is a model plus tools that finds code, changes it and runs checks, while you set the
goal and review the result. It runs in two places: the **Chat view**, beside your editor, terminal
and debugger, and the **Agents window**, where sessions are assigned and tracked across projects.
There is also **inline chat** for a single focused edit.

Three things follow. First, the editor hosts more than one **harness** — the documentation names
Copilot, Claude and Codex — so *which harness* is a question here as much as it was in
{{topic:chooseharness}}. {{topic:ghharness}} takes that further. Second, a session has explicit
controls for its target, its agent, its language model and its **permissions**, which is the subject
of {{topic:agentmode}}. Third, the editor is customised by files in the repository — instructions,
skills and MCP servers — which is {{topic:customize}} and, for skills specifically,
{{module:authoring-skills}}.

### The extensions worth installing

| Extension | Why | Covered in |
|---|---|---|
| GitHub Copilot and Copilot Chat | Inline suggestions, chat, agent sessions | this lesson, {{topic:agentmode}} |
| Your language's tooling | Interpreter selection, debugging, test discovery | {{topic:localenv}}, {{topic:language}} |
| Microsoft Copilot Studio | Clone a low-code agent to YAML and sync it back | {{topic:csvscode}} |

Keep that list short and put it in the repository. A `.vscode/extensions.json` file recommends
extensions to anyone who opens the folder, and it is the difference between a documented toolchain
and a colleague guessing.

<!-- unknown since=2026-11 -->
**Dev containers** are the usual answer to "it works on my machine", and they would pin the runtime
and the tooling together rather than only the dependencies. Neither of this topic's curated links
covers them, and the capstone does not use one, so treat the fit as unchecked here —
{{topic:localenv}} pins the runtime a simpler way.
<!-- /unknown -->

## In practice at Technik

The capstone repository is the worked example for this whole module, and it is a plain VS Code
workspace: a pinned Python version, two dependency projects, a gitignored `.env`, and one MCP server
that the editor can start.

That last file is the point at which the editor stops being a text editor and becomes part of the
agent. `.vscode/mcp.json` tells VS Code how to launch the Teamcenter MCP server, and once it is
running, agent mode can be asked about work order `100004510` and will answer from Technik's data
rather than from the model's memory.

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

Three things in nine lines are worth reading. The top-level key is `servers`, which is the VS Code
format rather than the portable one — {{topic:agentmode}} explains why that distinction bites,
and {{topic:mcpvscode}} why the course keeps a file VS Code now labels deprecated.
`${workspaceFolder}` keeps the file machine-independent, so it is committed rather than personal.
And the server is the same process the agent will use later ({{topic:stagemcp}}); the editor is
simply the first client to call it.

## Design guidance

- **Commit the workspace, not your preferences.** `.vscode/mcp.json` and
  `.vscode/extensions.json` describe the project and belong in Git. Your theme and keybindings do
  not.
- **Use workspace-scoped settings deliberately.** A setting that must hold for everyone who opens
  the repository belongs in the workspace; a setting that is about you belongs in your profile.
- **Treat the editor's agent configuration as reviewable.** It shapes behaviour, so it goes through
  the same pull request as the code ({{topic:git}}).
- **Decide the harness before the habits.** Switching later means re-learning approvals, tool
  configuration and customisation files.
- **Open unfamiliar repositories carefully.** Restricted mode disables agents in a workspace, which
  is the correct default for code you have not read ({{topic:agentmode}}).
- **Keep the browser for what the browser is better at.** Testing a low-code agent's conversation
  and reading analytics still belong there ({{topic:csvscode}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Copilot is signed in but chat is missing | `chat.disableAIFeatures` is set, possibly at workspace level | Check the workspace settings as well as your user settings |
| A colleague's clone behaves differently | The configuration that matters is in your user profile, not the repository | Move project-level configuration into `.vscode/` and commit it |
| The MCP server starts for you and nobody else | An absolute path in `mcp.json` | Use `${workspaceFolder}` |
| Agent mode cannot see the project's tools | The workspace is open in restricted mode | Trust the workspace, having read it, or open it as a folder you own |
| The allowance ran out mid-week | The Copilot Free plan's monthly allowance is finite | Check the Status Bar dashboard; a paid plan removes the ceiling ({{topic:costs}}) |
| Suggestions appear in a repository where they should not | Copilot is on for every workspace | Disable AI features for that workspace specifically |
| Two engineers get different agent behaviour from the same repository | Instructions and tool sets are in personal profiles | Put them in the repository ({{topic:customize}}) |

## Key terms

**Chat view** — the agent session that sits beside the editor, terminal and debugger.

**Agents window** — where agent sessions are assigned and tracked across projects.

**Harness** — the runtime around the model that holds the loop, tools and permissions. The editor
offers more than one ({{topic:ghharness}}, {{module:agent-harness}}).

**Workspace settings** — configuration stored in the repository's `.vscode/` folder and shared by
everyone who opens it, as opposed to your user profile.

**Restricted mode** — the state VS Code opens untrusted folders in, which disables agents there.

**`mcp.json`** — the file that tells the editor how to start an MCP server ({{topic:mcpvscode}}).
