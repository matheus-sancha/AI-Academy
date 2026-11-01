## What this module is for

Everything you built so far lived in a browser, and the platform owned the machine it ran on. From
here the thing you build is a **repository**: files you edit, dependencies you pin, secrets you keep,
and a history somebody reviews. This module sets that up once, so that no later module has to stop
and explain why a server will not start.

It is deliberately unglamorous. Five of its six lessons are about discipline rather than capability
— a pinned runtime, a lock file, an ignored secrets file, a branch, a review. The one lesson that
is about capability, agent mode, turns out to be mostly about discipline too, because the question
it answers is not *what can the agent do* but *what may it do without asking*.

Nothing from the earlier levels is repeated here. Where a lesson touches something already taught,
it links it and moves on to the technique that is new.

## Before you start

You want {{topic:devenv}} from the earlier toolchain discussion, which set up the Power Platform
side and already said the agent gets its own least-privilege role; this module is the other half of
that sentence. {{topic:connauth}} is the idea that an agent runs as something, now expressed as
environment variables rather than as a connection. {{topic:chooseharness}} asked which harness an
agent runs on, and {{topic:agentmode}} asks it again about the harness in your editor.

You need a machine you can install software on, a GitHub account, and — for one lesson only — access
to a Copilot Studio environment with an agent you may edit. Everything else can be read without
running anything. The capstone repository is public, so its files can be read alongside the lessons
whether or not you intend to build it ({{module:capstone-build}}).

Allow about two hours.

## What you will be able to do

By the end of this module you should be able to:

- set up VS Code as a build surface, and say which configuration belongs to the repository rather
  than to you;
- pin a runtime, isolate dependencies per project, and explain why one repository sometimes needs
  two environments;
- keep credentials out of source control, and say what a committed example env file is for;
- choose a permission level and approval scope for an agent session, and name the two things the
  documentation refuses to call security boundaries;
- explain why an MCP server can run for you and stay invisible to the agent;
- clone a low-code agent to YAML, and sequence Preview, Get, Apply and publish without losing work;
- review a machine-written change as a diff, and set up secret scanning and push protection
  appropriately for a repository's visibility;
- say what "enough Python or C#" means concretely, and defend a single-language choice for a team.

## The thread through this module

One repository, set up once, in the order the decisions actually arrive.

{{topic:vscode}} opens the editor and commits the first workspace file — an MCP server definition
that works on a colleague's machine because it names no absolute path. {{topic:localenv}} pins
Python 3.12, then finds that the agent and the server cannot share an environment because Agent
Framework requires an older MCP SDK, and puts Technik's Snowflake key behind a path in a gitignored
file. {{topic:agentmode}} gives an agent session the server's read-only tools, writes one glob so
that `.env` is never edited unasked, and notes that the shop-floor text which once reached a
read-only agent can now reach a session holding your shell. {{topic:csvscode}} clones the Production
Assistant out of the browser as YAML and commits it before doing anything else, because Get
overwrites. {{topic:git}} makes the pull request the gate a machine cannot pass alone, and puts the
evaluation baseline under the same review as the code. {{topic:language}} closes the module with the
choice that made all of it consistent, and the dependency constraint that proves why one language is
cheaper than two.

## Self-check

<details>
<summary>1. Your MCP server starts correctly when you launch it yourself, and the agent in your editor insists it has no such tools. What is the first thing to check?</summary>

Which file the agent actually reads. The VS Code format in `.vscode/mcp.json` is not read by the
agent directly — VS Code forwards eligible servers from it, and excludes any server whose
configuration needs an `${input:...}` variable. The portable workspace-root format and the Copilot
user file are read differently again. So a server that launches perfectly from the file you edited
can be invisible to the agent for a reason that has nothing to do with the server. Check the format
and the forwarding before you debug the process ({{topic:agentmode}}, {{topic:mcpvscode}}).
</details>

<details>
<summary>2. You set <code>chat.tools.terminal.autoApprove</code> so that a destructive command is <code>false</code>. A colleague says the command can no longer be run. Are they right?</summary>

No. A `false` rule means the command **requires approval**; it does not block it. The documentation
is explicit, and it adds that terminal auto-approval is a best-effort convenience rather than a
security boundary — as is the LLM-judge permission level, and as is sandboxing, which is an added
layer and not a virtual machine or user-account boundary. If something must not be possible, the
answer is not an approval setting: it is not granting the capability, or giving the agent an
identity that cannot do it, the way a read-only Snowflake role bounds the damage whatever the
dialog says ({{topic:agentmode}}, {{topic:sfroles}}).
</details>

<details>
<summary>3. One repository holds two dependency projects with different major versions of the same SDK. Is that a mistake to clean up?</summary>

No, it is the correct answer to a real constraint. Agent Framework's MCP client requires an MCP SDK
below version 2, while the server uses version 2, so they cannot share an environment. They do not
need to: they communicate over the protocol rather than in-process, so their SDK versions are
independent. Forcing them together would mean holding the server back for no benefit. The general
rule is that processes separated by a protocol boundary may differ in their dependencies, and the
place to record that is exact pins plus a committed lock file ({{topic:localenv}},
{{topic:language}}).
</details>

<details>
<summary>4. You clone a Copilot Studio agent to YAML, spend an afternoon editing its instructions, then select Get to pick up a colleague's change. What should have happened first, and why?</summary>

A commit — ideally two: one immediately after the clone, recording the agent's current behaviour,
and one for your afternoon's work. Get downloads remote changes and **overwrites uncommitted local
changes**, and the confirmation says so. The commit straight after cloning is the more important of
the two, because without it there is no record of what the agent did before anyone touched it.
Worth remembering alongside this: Apply modifies the live agent immediately and is *not* a publish,
so the sequence is commit, Preview, Get, resolve, Apply, test, then publish
({{topic:csvscode}}, {{topic:publish}}).
</details>

<details>
<summary>5. A credential has been pushed to a public repository. Put the response in order, and say what secret scanning would and would not have done.</summary>

**Rotate the credential first.** GitHub's guidance is that rewriting history is time-intensive and
often unnecessary once the credential is revoked, and a secret in a public repository should be
assumed read the moment it landed. Then clean up if there is still a reason to, and fix the
`.gitignore` so it cannot recur.

Secret scanning would have raised an alert — it runs automatically and free on public repositories,
across the entire history on all branches — and for a partner credential it would also notify the
issuing provider. What it does not do is prevent the push. That is push protection, which is a
separate feature: enabled by default for users pushing to public repositories, and disabled by
default at the repository level, where it needs to be turned on deliberately
({{topic:git}}, {{topic:localenv}}).
</details>
