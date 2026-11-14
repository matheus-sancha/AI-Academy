## TL;DR

Stage 1 builds a project that runs and does nothing, and puts into the first commit the three files that decide
what the agent is: its dependencies pinned exactly, its instructions, and the questions it will be judged on.
You create your own repository beside the capstone clone, split it into two uv projects, and make sure no secret
can be committed. You finish with `uv run main.py` exiting cleanly. It calls no model and no tool, and that is
the point. Every later stage is then a diff over something already working, and a diff is what a reviewer can read.

## Why it matters

A change to instructions, tools or a model rarely shows in the diff that made it. Behaviour shows only in a run,
so the run has to exist before the change does. Stage 1 makes the two things a run needs, the instructions and the
cases, files in version control from the first commit, which gives every later edit something to be compared with
({{topic:git}}).

It also fixes the order of a habit that is easy to reverse. Writing the cases before the tools means they cannot be
shaped to what the agent happens to do. A case written after the answer exists tends to describe the answer.

## How it works

### Two projects, pinned exactly

The capstone has two uv projects. The root one holds the seed, the setup check and, from stage 2, the MCP server.
`agent/` holds the agent. They are separate because Agent Framework's MCP client requires `mcp<2` and the server
uses the v2 SDK ({{topic:localenv}}). The two talk over the protocol, so their SDKs never meet.

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

Every version is an exact pin with `==`. The hosting package's version ends in `b261015`, a pre-release, and a pre-release
can change between builds. Commit each project's `uv.lock` as well. The Dockerfiles install with `--frozen`, and CI
sets `UV_LOCKED`, so a build that disagrees with the lockfile fails instead of resolving something new.

The root project's dependency block is shown in {{topic:localenv}}. It pins the MCP SDK at v2 and the Snowflake
connector, and you write it the same way now, so that both lockfiles exist when the stage ends.

### No secret can be committed

Ignore rules come before the first `git add`, because a file in one commit stays in the history.

*From [`.gitignore`, lines 1–14](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/.gitignore#L1-L14):*

```gitignore
# Secrets: never committed
.env
keys/

# Python
.venv/
__pycache__/
*.pyc

# Evals: written by every run
evals/report.md

# azd: environments hold resource names and can hold secrets
.azure/
```

Two entries are the secrets, `.env` and `keys/`. The next two are build products. The last is `azd`'s
environment folder, which stage 5 creates and which can hold values you would not publish. The capstone also
ships `.env.example`, which is committed and holds placeholders only ({{topic:localenv}}). Your `.env` is a
copy, filled in once.

### The instructions, as a file

*From [`agent/instructions.md`, lines 1–15](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/agent/instructions.md#L1-L15):*

```markdown
<role>
You answer questions about Teamcenter controlled documents and released revisions for Technik's
production planners, quality and manufacturing engineers, and supervisors at Plants 1 and 2.
</role>

<tone>
Plain and technical. Short answers first, detail on request. Spell out every code for supervisors.
</tone>

<tasks>
- Given a document number, report its title, revision, status, owner and next review date.
- Given an operation, name the controlled documents that cover it.
- Given a part, drawing, CNC program or document number, report the latest released revision and
  the ECN that released it.
</tasks>
```

Stage 1 commits a short version of this file. Stage 3 grows it into six layers, adding the procedure, the rules and
a refusal ({{topic:sysprompt}}). It is a Markdown file the agent reads at start-up, not a string inside the code,
because a file diffs in review and a string in a function does not.

### The eval set, written before the tools

*From [`evals/eval_set.jsonl`, line 3](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/evals/eval_set.jsonl#L3):*

```json
{"id": "rev-03", "category": "trap", "query": "Is revision C of SWI70000318 the one to use?", "ground_truth": "No. Revision B is the released revision. Revision C is In Work, waiting on ECN70000042.", "expected_tool_calls": [{"name": "get_revision_status", "arguments": {"item_no": "SWI70000318", "revision": "C"}}], "must_include": ["rev B|revision B", "not released|in work"]}
```

One line per case, eight in all: a question, the answer a correct agent gives, the tool calls it should make and the
facts its answer must contain. The cases name `get_revision_status` before stage 2 builds it, which is deliberate.
They are the questions Technik's planners and engineers would ask, sorted by what each tests: four happy paths, a
trap, two abstentions and an out-of-scope request ({{topic:evalstrategy}}, {{topic:testsets}}). The capstone's questions
differ from the ones Intermediate asks its own agent, because three were rewritten to fit the three tools you will
build.

### The agent that does nothing

`agent/main.py` at this stage reads `instructions.md` and exits. The final file reads it on [line 53](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/agent/main.py#L53),
and everything else in that file arrives in stage 3. Run it from `agent/`:

```powershell
cd agent
uv run main.py
```

## In practice at Technik

You finish this stage holding a repository whose first commit contains these files, and nothing the reader of your
pull request would need to guess at:

| Path | What it holds at the end of stage 1 |
|---|---|
| `pyproject.toml`, `agent/pyproject.toml` and both `uv.lock` | The pins, one project per SDK generation |
| `.gitignore`, `.env.example` | What can never be committed, and the names of the settings |
| `agent/instructions.md` | The first layers of the instructions |
| `agent/main.py` | A program that loads them and exits |
| `evals/eval_set.jsonl` | Eight cases, none graded yet |

The capstone at its tag is the answer key. Compare your files with its `agent/pyproject.toml` and
`.gitignore`, but not yet with `main.py`, which is stage 3's work. Where yours differ on purpose, such as a different
model deployment, note the reason in the commit message. Stage 5 will ask for it.

## Design guidance

- **Make the first commit a project that runs.** A skeleton that fails teaches you nothing at stage 3.
- **Pin every dependency exactly, and commit the lockfile.** An agent's behaviour changes when its SDK does.
- **Split projects when their pins disagree.** Never negotiate between them with an override.
- **Ignore secrets before the first `git add`.**
- **Keep instructions and cases as files.** What is not in a file cannot be reviewed.
- **Write the cases before the code that answers them.**

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `uv` cannot resolve the agent's dependencies | The MCP SDK v2 and Agent Framework share one project | Move the server to the root project and leave `agent/` on `mcp<2` |
| `git status` lists `.env` | The ignore rule came after the first `git add` | Add the rule, then `git rm --cached .env` so the file leaves the index |
| The agent builds on your machine and not in CI | The lockfile was not committed, or no longer matches `pyproject.toml` | Commit `uv.lock` after every change to the pins |
| The cases all pass trivially at stage 4 | They were written from the agent's answers | Rewrite the ground truths from the Teamcenter data, not from a run |
| `uv run main.py` asks for a model | The program already calls one | Stage 1 reads the instructions and stops. Move the model call to stage 3 |

## Key terms

**Pin**: an exact dependency version, written with `==`.

**Lockfile**: the resolved versions of everything, committed so every machine installs the same set.

**Eval set**: the versioned file of questions and expected behaviour the agent is judged on.

**Skeleton**: a project that runs and does nothing, so each later change is a reviewable diff.
