# AI Academy

**AI Engineering on Microsoft** — a self-paced learning program in three levels: from *using* Microsoft
Copilot well, to *building* agents in Copilot Studio, to *shipping and operating* pro-code agents with the
Agents SDK, Agent Framework and Foundry.

This repository holds the **source**. The course learners read is a static website built from it: unzip,
open `index.html`, read. No install, no server, no network calls, no labs or environments to provision.

---

## Download the course

### ▸ **[AI-Academy-course-v0.1-preview.zip](https://github.com/matheus-sancha/AI-Academy/releases/download/v0.1-preview/AI-Academy-course-v0.1-preview.zip)** — 3 MB, preview drop

1. Download the zip and unzip it anywhere.
2. Open **`AI-Academy-course/index.html`** in any browser.
3. Pick your level and start.

Everything works straight from disk over `file://` — no web server, and nothing is sent anywhere. Your
progress ticks live in that browser's local storage, so stay in the same browser and keep the same
unzipped folder if you want them to stick. Each roadmap also ships as a printable PDF under `pdf/`.

All drops, with release notes and caveats: **[Releases](https://github.com/matheus-sancha/AI-Academy/releases)**.
This one is marked *pre-release* on purpose — see [Writing status](#writing-status) below.

---

## What's inside

| Level | For | You come out able to | Modules | Topics | Lessons written |
|---|---|---|---|---|---|
| **Basic** | Everyone at the company | Use Copilot well: what an LLM is and why it invents things, prompting craft, what Copilot can and cannot see in your tenant, and Copilot in Chat, Word, Excel, PowerPoint, Outlook and Teams. Nothing here builds anything. | 11 | 37 | **37 — complete** |
| **Intermediate** | Engineers | Design, build, test and publish an agent in **Copilot Studio** — instructions, knowledge and RAG, tools, connectors and MCP, Agent Skills, safety, evaluation, environments — ending in a guided build you follow end to end. | 18 | 108 | **108 — complete** |
| **Advanced** | Engineers who finished Intermediate | Master the editor agent, then build, ship and operate **pro-code** agents: the agent harness and context engineering, authoring Skills, building MCP servers, multi-agent, Agents SDK / Agent Framework / Foundry, evals and observability, security and ALM — ending in a capstone you write yourself. | 17 | 121 | 22 — in progress |

Plus, shared by every level: the **Technik reference scenario** (the fictional company every worked
example uses), cross-level **search**, and per-topic **progress tracking**.

## How the course works

- **Documentation, not labs.** Worked examples live inside the lessons. There is nothing to install or
  provision to follow along, and no exercise environment to wait for.
- **The levels stack.** Each level opens with an *assumed knowledge* module that lists what it takes for
  granted and links to where that was taught. Nothing is taught twice; if a term is unfamiliar, the link
  back is one click away.
- **Every product claim is sourced.** A claim is either cited to Microsoft documentation, verified in a
  live tenant, or visibly marked **"Not yet verified"** — never asserted bare. Anything volatile (UI
  click-paths, preview features, pricing) carries the date it was last checked, and the build warns when
  that date goes stale.
- **Curated links everywhere.** Each topic carries hand-picked Microsoft docs, training modules and
  videos, so a topic is useful even before its lesson is written.
- **Progress and search are local.** Ticks are stored per browser; search runs from a prebuilt index in
  the zip. Nothing phones home.

## Writing status

Basic and Intermediate are **written in full**. Advanced is being written module by module:

- **Written:** Developer Tooling · Agent Harness · Context Engineering
- **Remaining (14 modules):** Agent Skills (Authoring) · Building MCP Servers · Advanced Tools,
  Connectors & Multi-Agent · Pro-Code Agents · Evaluation & Observability · Security, Safety &
  Moderation · ALM, Governance & Operations · The Capstone Build · LLM Internals · Advanced RAG ·
  Snowflake Cortex · Intelligent Automation · Models, Inference & Fine-Tuning

Topics with no lesson yet still appear on the Advanced roadmap with their curated Microsoft links, so the
path and the sources are usable today — you just read Microsoft's pages instead of a lesson. 167 of 266
topics have a lesson; 47 claims across the written lessons are openly marked *Not yet verified*.

---

## Build it from source

For anyone editing the content. Requires Python 3 and one dependency.

```bash
pip install -r _build/requirements.txt          # once
python _build/build.py --out dist               # build into dist/ (gitignored)
```

Then open **`dist/index.html`** — the home page linking every roadmap and module.

Always pass `--out dist` for a local look: a bare `build.py` writes to `AI_ACADEMY_OUT` when that is set,
which may be the shared folder learners open.

Other useful runs:

```bash
python _build/build.py --missing                # list every topic that has no lesson yet
```

```bash
python _build/build.py --strict --pdf           # release build: any warning fails, plus roadmap PDFs
```

```bash
python _build/check_links.py _source/basic.md _source/intermediate.md _source/advanced.md
```

`build.py` never goes online, because the course is read over `file://`. The one check that needs the
network lives in `check_links.py`.

## Cutting a download drop

```bash
python _build/build.py --out /tmp/AI-Academy-course --strict --pdf
```

`--pdf` matters for a drop: the home page always shows a PDF button per roadmap, so a drop built without
it ships three dead links.

Zip that folder (so it extracts as `AI-Academy-course/`), then attach it to a release:

```bash
gh release create vX.Y "AI-Academy-course-vX.Y.zip" --notes-file notes.md --prerelease
```

The README's download link above points at the newest drop — update it in the same commit.

## Repo layout

| Path | What's there |
|---|---|
| `_source/<level>.md` | One roadmap per level. These own every module id, topic id, title, flag and curated link. |
| `_source/course/<module>/<topic-id>.md` | A lesson body. Its title and "Go deeper" links come from the roadmap. |
| `_source/course/<module>/overview.md` | A module's own page: outcomes, what it assumes, self-check. |
| `_source/course/scenario.md` | The Technik reference scenario, shared by every level. |
| `_build/` | Build and link-check scripts, page templates, search and progress JS — see [`_build/README.md`](_build/README.md) for the full lesson syntax and every macro. |
| `docs/` | [`course-design.md`](docs/course-design.md) (standing design reference: vocabulary, level boundaries, how a claim must be sourced), [`topic-trees.md`](docs/topic-trees.md), and research notes. |

Built files are never committed.

## Ground rules for contributions

- Read [`docs/course-design.md`](docs/course-design.md) before writing a lesson, and
  [`_build/README.md`](_build/README.md) for the syntax — callouts, verification markers and the link
  macros that make a cross-reference impossible to let go stale.
- Never write a module id, topic id, path or level into prose by hand; use the `{{topic:…}}` /
  `{{module:…}}` macros so a bad reference fails the build instead of rotting.
- Every product claim gets a citation, a tenant verification or an `unknown` marker.
- All scenario content uses the fictional company **Technik** (subsea equipment). Keep every client,
  project, site and part number invented. Never commit real organization names, tenant or account
  details, or credentials.
