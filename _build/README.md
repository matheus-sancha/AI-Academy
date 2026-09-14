# Maintaining the roadmaps and course

```
pip install -r requirements.txt                 # once: markdown-it-py
python check_links.py beginner.md advanced.md   # verify every roadmap link -> link-report-*.tsv (gitignored)
python check_seed.py                            # verify the Snowflake seed data and the values labs assert about it
python build.py                                 # roadmaps + course pages + search index
python build.py --pdf                           # ... plus a PDF per roadmap and per module
python build.py --strict                        # release build: any warning fails the build
```

Built files are not committed. They go to `--out DIR`, else the `AI_ACADEMY_OUT` environment variable, else `dist/`.
Point `AI_ACADEMY_OUT` at the shared folder learners open. Everything works when opened straight from disk.

## Where content lives

| Source | Built page |
|---|---|
| `_source/beginner.md`, `_source/advanced.md`: roadmaps; these own topic ids, titles, flags and links (format at the top of `build.py`) | `beginner.html`, `advanced.html` |
| `_source/course/scenario.md`: the running Technik scenario, shared by both tracks | `course/scenario/index.html` |
| `_source/course/<SECTION>/module.md`: module overview (optional) | `course/<SECTION>/index.html` |
| `_source/course/<SECTION>/<topic-id>.md`: lesson body only; the title and "Go deeper" links come from the roadmap | `course/<SECTION>/<topic-id>.html` |
| `_source/course/<SECTION>/<topic-id>.pt-BR.md`: optional translation (may start with `---` / `title: …` / `---`) | `course/<SECTION>/<topic-id>.pt-BR.html` |
| `labs/<SECTION>/lab.md` or `exercise.md`; other files under `labs/` (zips, SQL) are copied as-is | `course/<SECTION>/lab.html`, `labs/…` |
| `labs/_setup/snowflake/`: the lab database — see its [README](../labs/_setup/snowflake/README.md) | copied to `labs/_setup/snowflake/` |

`.md` files under `labs/` become pages or, like the setup README, stay in the repository. Only the
non-Markdown files are copied to the build, so anything a learner needs must be in a lesson, a lab
page or a comment header inside the file itself.

## Lesson syntax

Standard Markdown (tables and fenced code included), plus:

````
## TL;DR                       first heading of every full lesson (rendered as a highlighted box)

> [!TIP]                       callouts: NOTE, TIP, IMPORTANT, WARNING, CAUTION
> Text…

```mermaid                     diagrams (rendered by Mermaid from a CDN)
flowchart LR
  A --> B
```

<!-- volatile verified=2026-09 -->
Anything that changes often: UI click-paths, preview features, pricing.
Learners see it as normal text; the build warns once it's older than 6 months.
<!-- /volatile -->
````

Self-check questions use `<details><summary>…</summary>` so the answer is hidden until the reader
asks for it. Raw HTML is allowed in lesson Markdown. A closed `<details>` would otherwise print as
its summary alone, so every one is opened on `beforeprint` (and under `?print`) and closed again
afterwards — without that, printing a module silently drops all its answers.

Each module also builds `course/<SECTION>/print.html`: the module overview, every lesson and the
lab on one page, linked from the module overview. `--pdf` renders one PDF per module from it, plus
the two roadmap PDFs. A full build of the finished course takes about 12 seconds and produces
roughly 23 MB.

## Assets

`assets/` holds three files, all loaded from disk so nothing needs a network:

| File | Notes |
|---|---|
| `mermaid.min.js` | Vendored at build time from the npm registry and cached in `_build/.cache/` (gitignored). Without it, diagrams need a CDN and render as raw source offline. If the fetch fails the build warns and falls back to the CDN — delete the cache and rebuild with network access to fix. |
| `search-index.js` | About 1.9 MB for the finished course, so it is **not** loaded with the page. `search.js` pulls it in on first use by injecting a `<script>` element, which works under `file://` where `fetch` does not. |
| `search.js` | Loaded on every page. Small. |

Every relative `<a href>` in the built pages is checked after the build; a link to a page that does
not exist is a warning, and fails a `--strict` release build. Links inside inline JavaScript are
skipped, and `pdf/` links are only checked with `--pdf`.

Progress is stored in each browser's localStorage under `aiem:<track>:<topic-id>` and is shared by roadmap nodes and lessons, so keep topic ids stable.
Search covers lessons, module pages, labs and every roadmap topic that doesn't have a lesson yet.
PDF export uses a Playwright headless shell if installed, otherwise Edge/Chrome headless.
