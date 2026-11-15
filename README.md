# AI Academy

**AI Engineering on Microsoft** is a self-paced learning program in three levels. It goes from *using*
Microsoft Copilot well, to *building* agents in Copilot Studio, to *shipping and operating* pro-code agents
with the Agents SDK, Agent Framework and Foundry.

This repository holds the **source**. Learners read a static website built from it: unzip it, open
`index.html` and read. There's nothing to install, no server, no network calls, and no labs or environments
to provision.

[![Latest release](https://img.shields.io/github/v/release/matheus-sancha/AI-Academy)](https://github.com/matheus-sancha/AI-Academy/releases/latest)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## Get the course

### ▸ **[AI-Academy-course-v1.0.1.zip](https://github.com/matheus-sancha/AI-Academy/releases/download/v1.0.1/AI-Academy-course-v1.0.1.zip)**, 5 MB, all three levels complete

1. Download the zip and unzip it anywhere.
2. Open **`AI-Academy-course/index.html`** in Microsoft Edge or Google Chrome.
3. Pick your level and start.

**On a SharePoint or OneDrive share:** choose **Sync** (or **Add shortcut to My files**), then open
`index.html` from the synced folder on your computer. SharePoint's web view previews one page at a time,
so links, search and progress don't work there.

Everything runs from disk over `file://`, and nothing is sent anywhere. Progress ticks live in your
browser's local storage, so keep using the same browser and folder if you want them to stick. Each roadmap
also ships as a printable PDF under `pdf/`, and printed pages keep their self-check answers.

Every drop, with its release notes and caveats: **[Releases](https://github.com/matheus-sancha/AI-Academy/releases)**.

---

## What's inside

| Level | For | You come out able to | Modules | Topics |
|---|---|---|---|---|
| **Basic** | Everyone | Use Copilot well. That covers what an LLM is and why it invents things, prompting craft, what Copilot can and cannot see in your tenant, and Copilot in Chat, Word, Excel, PowerPoint, Outlook and Teams. Nothing here builds anything. | 11 | 37 |
| **Intermediate** | Engineers | Design, build, test and publish an agent in **Copilot Studio**: instructions, knowledge and RAG, tools, connectors and MCP, Agent Skills, safety, evaluation and environments. It ends in a guided build you follow end to end. | 18 | 108 |
| **Advanced** | Engineers who finished Intermediate | Master the editor agent, then build, ship and operate **pro-code** agents: the agent harness and context engineering, authoring Skills, building MCP servers, multi-agent, the Agents SDK, Agent Framework and Foundry, evals and observability, security and ALM. It ends in a capstone you write yourself. | 17 | 121 |

Every topic has a lesson and every module has an overview: 313 pages in all. Every level also shares the
**Technik reference scenario** (the fictional company every worked example uses), cross-level **search**
and per-topic **progress tracking**. The capstone's code lives in
[technik-capstone](https://github.com/matheus-sancha/technik-capstone).

**Next:** a pt-BR translation of Basic.

## How the course works

- **Documentation, not labs.** Worked examples live inside the lessons. There's nothing to install or
  provision to follow along.
- **The levels stack.** Each level opens with an *assumed knowledge* module. It lists what the level takes
  for granted and links to where that was taught, so nothing is taught twice.
- **Every product claim is sourced.** Each claim is cited to Microsoft documentation, verified in a live
  tenant, or visibly marked **"Not yet verified"** (190 are today), never asserted bare. Anything volatile,
  like UI click-paths, preview features or pricing, carries the date it was last checked. The build warns
  when that date goes stale.
- **Curated links everywhere.** Each topic carries hand-picked Microsoft docs, training modules and videos.
- **Progress and search are local.** Ticks are stored per browser, and search runs from a prebuilt index
  in the zip. Nothing phones home. Diagrams are the one exception: they load a drawing script from a CDN.

---

## Build it from source

For anyone editing the content. You need Python 3 and one dependency.

```bash
pip install -r _build/requirements.txt          # once
python _build/build.py --out dist               # build into dist/ (gitignored)
```

Then open **`dist/index.html`**, the home page that links every roadmap and module.

Always pass `--out` for a local look. A bare `build.py` writes to `AI_ACADEMY_OUT` when that's set, and
that may be the shared folder learners open.

```bash
python _build/build.py --out dist --missing     # list every topic that has no lesson yet
```

```bash
python _build/build.py --out dist --strict --pdf   # release build: any warning fails, plus roadmap PDFs
```

```bash
python _build/check_links.py basic.md intermediate.md advanced.md
```

`build.py` never goes online, because the course is read over `file://`. The one check that needs the
network lives in `check_links.py`.

## Cutting a release

1. Build from a clean tree at the commit you'll tag, so every page footer names that commit:

    ```bash
    python _build/build.py --out <scratch>/AI-Academy-course --strict --pdf
    ```

    `--pdf` matters here. The home page always shows a PDF button per roadmap, so a build without it ships
    three dead links.

2. Copy `LICENSE` into that folder, then zip it so it extracts as `AI-Academy-course/`.
3. Update the download link in this README, commit, then tag and release:

    ```bash
    gh release create vX.Y "AI-Academy-course-vX.Y.zip" --verify-tag --notes-file notes.md
    ```

    Add `--prerelease` for a preview drop.

## Repo layout

| Path | What's there |
|---|---|
| `_source/<level>.md` | One roadmap per level. These own every module id, topic id, title, flag and curated link. |
| `_source/course/<module>/<topic-id>.md` | A lesson body. Its title and "Go deeper" links come from the roadmap. |
| `_source/course/<module>/overview.md` | A module's own page: outcomes, what it assumes, self-check. |
| `_source/course/scenario.md` | The Technik reference scenario, shared by every level. |
| `_build/` | Build and link-check scripts, page templates, and the search and progress JS. See [`_build/README.md`](_build/README.md) for the full lesson syntax and every macro. |
| `docs/` | [`course-design.md`](docs/course-design.md) (the standing design reference: vocabulary, level boundaries, how a claim must be sourced), [`topic-trees.md`](docs/topic-trees.md) and research notes. |

Built files are never committed.

## Contributing

- Read [`docs/course-design.md`](docs/course-design.md) before writing a lesson, and
  [`_build/README.md`](_build/README.md) for the syntax: callouts, verification markers, and the link
  macros that stop a cross-reference from going stale.
- Never write a module id, topic id, path or level into prose by hand. Use the `{{topic:…}}` and
  `{{module:…}}` macros, so a bad reference fails the build instead of rotting.
- Every product claim gets a citation, a tenant verification or an `unknown` marker.
- All scenario content uses the fictional company **Technik** (subsea equipment). Keep every client,
  project, site and part number invented. Never commit real organisation names, tenant or account
  details, or credentials.

By contributing, you agree that your contributions are licensed under the MIT License below.

---

## Disclaimer

- **Independent and unofficial.** AI Academy is an independent learning resource. Microsoft, Snowflake,
  Siemens, GitHub, OpenAI and any other vendor named in it don't produce, endorse or support it.
- **Trademarks.** Microsoft, Copilot, Microsoft 365, Copilot Studio, Azure, Microsoft Foundry, Power
  Platform, GitHub, Snowflake, Cortex, Teamcenter and other product names are trademarks of their
  respective owners. They're used here only to identify the products being taught.
- **Educational, not advice.** The content describes products as they were documented or observed on the
  dates shown in the lessons. Products, prices, licensing and click-paths change often. Check the official
  documentation before relying on anything here. Nothing in the course is legal, security, compliance or
  licensing advice for your organisation.
- **Fictional scenario.** Technik, its plants, people, documents, part numbers and data are invented. Any
  resemblance to a real company or person is coincidental. No real client, project or tenant data is used.
- **Third-party content.** Linked pages, videos and training modules belong to their owners and aren't
  covered by this repository's license.
- **No warranty.** The course and its code are provided "as is", without warranty of any kind. Run the
  examples in a test environment, not in production. You're responsible for what you build with them.

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 Matheus Sancha.
