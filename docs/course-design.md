# Course Modules — Design Decisions

> Step 3 of 3. Agreed in a design interview on 2026-09-13, before any module is written.
> Steps 1–2 (topic trees, roadmaps) are done: `docs/topic-trees.md`, `_source/beginner.md`, `_source/advanced.md`.

## Pedagogy

| Decision | Choice |
|---|---|
| Delivery | **Purely self-paced.** No facilitator or deadlines, so every module has to make sense on its own. |
| Module unit | **1 module = 1 roadmap section** (B0–B14, A0–A14). Each topic becomes a lesson. |
| Lesson depth | **Full original textbook** for stable content. Content that changes often (Copilot Studio UI click-paths, preview features, pricing) gets short guidance plus a curated link. The course has to hold up as reference documentation engineers can rely on. |
| Volatile content | Tagged in the source with a verified date so a script can flag stale blocks. **The tag is never shown to learners**: they see normal content. |
| Lesson skeleton | TL;DR → Why it matters → How it works → In practice (Contoso) → Design guidance → Pitfalls (symptom → cause → fix) → Key terms → Go deeper (auto-filled from roadmap links) |
| `[opt]` / `[prev]` topics | Short "good to know" lessons (~300–500 words). Never required by labs, exercises or self-checks. Content about `[prev]` features is volatile-tagged. |
| Scenario | **One running scenario (Contoso Ops Assistant)** across both tracks. Advanced takes the same company further: an MCP server over its data, a pro-code rebuild, evals, CI/CD. |
| Labs | Each lab is **independent**: every lab ships its start state, so no lab depends on the learner finishing the previous one. Labs are for modules where something gets built. |
| Concept modules | (e.g., B0, B1, B4, A1, A11) get a **15–30 min exercise** instead of a lab. Exercises don't change the scenario's state. |
| Languages | **English first.** Each lesson can get an optional `<topic>.pt-BR.md` translation. The language switch and the roadmap's "Ler em português" link only appear when a translation exists. |
| Lab verification | **Observable checklist + reference solution.** Lab N's solution is also the starter for lab N+1. |

## Lab environment

- **Snowflake.** Each learner seeds their own `SANDBOX_<user>` schema with scripts from the repo. There are two roles:
  - `ACADEMY_LEARNER_<user>` owns the sandbox (create rights, XS warehouse with a resource monitor).
  - `ACADEMY_AGENT_<user>` has read-only access and is the only role agents, connectors and MCP servers use.
  - Each lab's step 0 runs an idempotent reset to that lab's start state (e.g., `RESET_TO('B7')`).
  - The roadmap `devenv` topic describes this two-role setup.
- **Power Platform.** Starters and solutions are **unmanaged solution .zip** files, imported into the learner's developer environment; learners then re-bind connection references.
- **Checkpoint authoring.** Claude writes `lab.md` as an exact build spec. The maintainer builds it in a dev environment (this doubles as the first test run), reports fixes, then exports the start/solution zips into `labs/<id>/`.

## Delivery & tooling

- **Repository:** source lives in the **public** GitHub repo `matheus-sancha/AI-Academy`: `_source/`, `_build/`, `docs/`, `labs/` (lab zips are source, so they're committed). Built HTML and PDFs are **not** committed.
- **Public-repo rule:** only fictional Contoso and placeholders (`SANDBOX_<user>`, `<your-account>`). No real organization names, tenant or account identifiers, internal URLs or tenant screenshots, and never credentials or `.env` files.
- **Working copy:** cloned **outside OneDrive** so OneDrive never syncs `.git`. `build.py` writes to `--out DIR`, else `AI_ACADEMY_OUT`, else `dist/`. The maintainer points `AI_ACADEMY_OUT` at the OneDrive share.
- **Distribution:** files only (HTML + PDF + lab zips, shared via OneDrive). Everything must work from `file://`, which means no `fetch`, a search index inlined into the JS, and relative links only.
- **Build:** extend `_build/build.py` with a real Markdown library (tables, fenced code, admonitions, Mermaid). One pipeline for roadmaps and course.
- **Source of truth:** the roadmap `.md` owns topic id, title, flags and links. Lesson files live at `_source/course/<SECTION>/<topic-id>.md` and contain the body only.
  - **Always errors:** orphan lessons (no matching topic id), lab folders with no matching section, and malformed or unclosed volatile tags.
  - **Warnings, which fail with `--strict`** (release builds): topics without a lesson, labs without zips, volatile blocks verified more than 6 months ago, and full lessons that don't start with `## TL;DR`.
  - Each roadmap node's drawer links to its lesson once the lesson exists.
  - Progress is shared: the same `aiem:<track>:<topic-id>` localStorage key covers both the roadmap node and the lesson.

```
_source/
  beginner.md, advanced.md          roadmaps (identity + links)
  course/
    scenario.md                     Contoso company, data model, agent storyline
    B7/
      module.md                     outcomes, prerequisites, self-check
      tools.md  connectors.md ...   lessons (file name = topic id)
      tools.pt-BR.md                optional translation
labs/
  _setup/snowflake/                 seed + reset scripts, role setup
  B1/
    exercise.md                     concept modules
  B7/
    lab.md
    start/ContosoOps_B6_end.zip
    solution/ContosoOps_B7_end.zip
```

## Build order

1. ✅ `build.py`: Markdown library, lesson pages, inlined search, volatile-tag stripping and staleness report, `--strict`. Authoring syntax is documented in `_build/README.md`.
2. `scenario.md` and Snowflake role/seed/reset scripts.
3. **Pilot slice:** B1 (concept module with an exercise) and B7 (lab module with zips and PDF).
4. ◆ Review the pilot: template, lesson length, tone, lab packaging, search over `file://`.
5. B0, B2–B6, B8–B14, then A0–A14.

## Open risks

- **Solution zip compatibility.** Exports can break across platform updates, and zips made from GitHub Copilot-harness agents may not import at all. Re-export checkpoints whenever volatile content is re-verified, and test this in the pilot.
- **Authoring volume.** ~160 full lessons plus ~25 short ones, roughly 200k+ words. The pilot review should confirm the target length before committing to it.
- **Copilot Credits.** Labs that test and evaluate agents consume credits. Each lab should state its expected consumption.
- **Stale copies.** With files-only distribution, learners can keep working from old copies. Show the build date (and git commit) on every page, and consider a "latest version lives at…" note.
- **Lab zips in a public repo.** Before committing an exported solution zip, check it for tenant-specific values: environment URLs, connection ids, Snowflake account locators.
- **Honor-system verification.** Nothing enforces lab checklists. This is acceptable for self-paced learning, but completion data can't be trusted for reporting.
- **Self-check format** is still undecided (per module; questions with explained answers). Settle it during the pilot.
