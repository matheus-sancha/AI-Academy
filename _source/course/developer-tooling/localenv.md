## TL;DR

Four decisions, made once per repository, prevent most of the failures that look like bugs: **pin the
runtime** so everyone is on the same interpreter, **isolate dependencies per project** so two
projects cannot fight over one version, **commit a lock file** so a colleague resolves exactly what
you resolved, and **keep secrets in a file Git cannot see**. None of this is AI-specific — it is
ordinary engineering hygiene — but it is where a first MCP server usually dies: a server that will
not start looks identical whether the cause is a missing package, the wrong interpreter or an unset
variable.

## Why it matters

In Copilot Studio the platform owned the runtime. There was no version to pin, because there was no
process of yours to run. Credentials lived in a connection, and the worst you could do was point one
at the wrong account ({{topic:connauth}}).

Pro-code moves all of that onto your machine, and the failure modes move with it. The most expensive
is the quiet one: code that works for you and nobody else. It works because your interpreter happens
to have a package installed globally, or because an environment variable is set in your shell and in
no script. Nothing in the repository records either fact, so the next person's identical clone
behaves differently and the investigation starts from the wrong end.

The second reason is that secrets now exist as files. An agent that reads Snowflake needs a key, and
that is a real credential in a folder an editor agent can read and Git will happily commit. Where it
lives is a security decision, usually learned after a push ({{topic:git}}).

## How it works

### Pin the runtime

A `.python-version` file naming the interpreter version is the smallest useful commitment a
repository can make. It is one line, it is read by the tooling, and it converts *"which Python?"*
from a conversation into a fact. The capstone pins `3.12`.

VS Code's side of this is the **Python Environments** extension, which works alongside the Python
extension. Opening a workspace with no explicit choice, it prefers a workspace-local `.venv` or
`venv` and falls back to a global interpreter. **Python: Select Interpreter** makes the choice
explicit.

<!-- volatile verified=2026-11 -->
Two details are worth knowing because they surprise people. The extension uses **uv** automatically
for creating environments and installing packages when uv is installed — `python-envs.alwaysUseUv`
defaults to `true`, and package installs go through `uv pip`. And the settings it writes record the
**environment manager** rather than a hardcoded interpreter path, in `python-envs.pythonProjects`, so
a committed `.vscode/settings.json` stays portable instead of embedding your home directory. Only
venv and conda environments can be *created* from VS Code; other managers are discovered, not
created.
<!-- /volatile -->

### Isolate per project, and expect more than one

One environment per project is the rule. The interesting case is when one repository needs two,
which is more common in agent work than it sounds, because the SDKs move at different speeds.

*From [`pyproject.toml`, lines 6–12](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/pyproject.toml#L6-L12):*

```toml
requires-python = ">=3.12"
dependencies = [
    "cryptography==50.0.2",
    "mcp==2.3.0",
    "python-dotenv==1.2.4",
    "snowflake-connector-python==4.8.0",
]
```

*From [`agent/pyproject.toml`, lines 5–12](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/agent/pyproject.toml#L5-L12):*

```toml
requires-python = ">=3.12"
dependencies = [
    "agent-framework-core==1.22.0",
    "agent-framework-foundry==1.15.0",
    "agent-framework-foundry-hosting==1.0.0b261015",
    "mcp==1.30.0",
    "python-dotenv==1.2.4",
]
```

Read the two `mcp` pins together: `2.3.0` in one project, `1.30.0` in the other, in the same
repository. Agent Framework's MCP client requires `mcp<2`, so the server and the agent cannot share
an environment. They do not need to — they talk over a protocol, not in-process — so two projects is
the right answer rather than a compromise ({{topic:transports}}).

Every version there is exact. That matters more in this field than most: a young SDK can move a
class between releases, and a floating dependency turns that into a failure on a machine you were
not watching.

### Commit the lock file, and make CI enforce it

A lock file records the resolution, not the request: every transitive package at a single version.
Committing it makes two clones identical; pointing CI at it keeps them that way. The capstone's
workflows resolve with locking enforced, so a dependency change arrives as a reviewed diff rather
than as drift.

### Keep secrets out of the tree

The pattern is the same whichever language you chose: values live in a local file, the file is
ignored, and the code reads them from the environment.

*From [`.gitignore`, lines 1–3](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/.gitignore#L1-L3):*

```gitignore
# Secrets: never committed
.env
keys/
```

A committed `.env.example` with placeholder values is the other half: it documents every variable
the project needs without holding one real value, so a new clone is a copy and a fill-in rather than
an archaeology exercise.

One trap is specific to this work. **Agent Framework does not load `.env` by itself** — the
documentation says so plainly and recommends calling `load_dotenv()` or setting the variables in
the shell. A script that reads `os.environ` and finds nothing is usually this, not a missing value.

If you chose C#, the equivalent is the **Secret Manager** tool, which keeps secrets in a JSON file
in your user profile, outside the project tree, reached with `dotnet user-secrets`. Its own
documentation is explicit about the limit: the values are **not encrypted**, it is **for development
only**, and production secrets belong in something like Azure Key Vault — which is where the
capstone puts the Snowflake key when it ships ({{topic:stageship}}).

## In practice at Technik

The capstone's `.env.example` is the whole identity story in seven lines, and it is deliberately
readable as a design document rather than as configuration.

*From [`.env.example`, lines 11–17](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/.env.example#L11-L17):*

```ini
# The agent's identity. seed/seed.py creates all of these and writes the key file.
SNOWFLAKE_USER=TECHNIK_AGENT_SVC
SNOWFLAKE_PRIVATE_KEY_FILE=keys/technik_agent_svc.p8
SNOWFLAKE_ROLE=TECHNIK_AGENT_RO
SNOWFLAKE_WAREHOUSE=TECHNIK_AGENT_WH
SNOWFLAKE_DATABASE=TECHNIK_DW
SNOWFLAKE_SCHEMA=OPS
```

Those are the names from Technik's agent identity: the service user, the read-only role and the
agent's own warehouse ({{topic:sfroles}}). The key is a *path*, not a value, so the secret is a file
the repository ignores rather than a string it holds. The admin credentials the seed script needs
sit in a separate block used by one script, keeping the agent's identity and the operator's visibly
distinct — the separation {{topic:connauth}} argued for, now expressed as environment variables.

## Design guidance

- **Pin the interpreter in the repository**, not in a README sentence.
- **One environment per project, and accept two when the SDKs demand it.** Processes that talk over a
  protocol do not need matching dependencies.
- **Pin exact versions while an SDK is in preview.** A floating pin is a scheduled surprise.
- **Commit the lock file and enforce it in CI.** Otherwise it is a snapshot nobody checks.
- **Never let code hold a credential.** Read the environment; keep the value in an ignored file.
- **Commit an example env file.** It is the only documentation of required variables that cannot go
  stale silently.
- **Keep key material as a path.** A file can be permissioned, rotated and ignored; a string in a
  settings file gets copied.
- **Load the env file explicitly.** Do not assume a framework does it.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Works for you, fails on a clean clone | A package installed globally, or a shell variable set only in your shell | Reproduce from a fresh environment; move the fact into `pyproject.toml` or `.env.example` |
| `os.environ` raises for a variable that is in `.env` | The framework does not load `.env` automatically | Call `load_dotenv()`, or set the variable in the shell |
| Two SDKs cannot be installed together | A shared transitive pin, such as Agent Framework needing `mcp<2` | Split into two projects that communicate over the protocol |
| CI resolves different versions from yours | The lock file is not committed, or CI does not enforce it | Commit it and resolve with locking enforced |
| A secret reached the remote | `.env` or a key folder was not ignored before the first commit | Rotate the credential first, then clean up ({{topic:git}}) |
| The wrong interpreter runs on a colleague's machine | A hardcoded interpreter path in committed settings | Let the tooling record the environment manager instead |
| An MCP server exits immediately with no useful error | Missing dependency, wrong interpreter or unset variable — indistinguishable from outside | Run the server directly in its own project first ({{topic:mcpvscode}}) |
| The build worked last month and not today | A floating version resolved to a new preview release | Pin exactly, and change pins deliberately |

## Key terms

**Pinned runtime** — the interpreter version recorded in the repository, so clones agree.

**Virtual environment** — a per-project dependency tree, isolated from the system interpreter and
from other projects.

**Lock file** — the exact resolved version of every direct and transitive dependency. Committed.

**`.env`** — the local, ignored file holding this machine's values. Its committed sibling holds
placeholders only.

**Secret Manager** — the .NET tool that stores development secrets outside the project tree,
unencrypted and for development only.

**Least-privilege identity** — the agent's own role and service user, distinct from yours
({{topic:sfroles}}).
