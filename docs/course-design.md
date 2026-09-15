# Course Modules — Design Decisions

> Step 3 of 3. Agreed in a design interview on 2026-09-13, before any module is written.
> Revised 2026-09-14: the course is **documentation only**, with no labs, exercises or lab environment.
> Steps 1–2 (topic trees, roadmaps) are done: `docs/topic-trees.md`, `_source/beginner.md`, `_source/advanced.md`.

## Pedagogy

| Decision | Choice |
|---|---|
| Delivery | **Purely self-paced documentation.** No facilitator, labs, exercises or environment to provision. Every module has to make sense on its own. |
| Module unit | **1 module = 1 roadmap section** (B0–B14, A0–A14). Each topic becomes a lesson. |
| Lesson depth | **Full original textbook** for stable content. Content that changes often (Copilot Studio UI click-paths, preview features, pricing) gets short guidance plus a curated link. The course has to hold up as reference documentation engineers can rely on. |
| Volatile content | Tagged in the source with a verified date so a script can flag stale blocks. **The tag is never shown to learners**: they see normal content. |
| Lesson skeleton | TL;DR → Why it matters → How it works → In practice (Technik) → Design guidance → Pitfalls (symptom → cause → fix) → Key terms → Go deeper (auto-filled from roadmap links) |
| `[opt]` / `[prev]` topics | Short "good to know" lessons (~300–500 words). Never required by self-checks or by other lessons. Content about `[prev]` features is volatile-tagged. |
| Scenario | **One shared scenario (Technik Production Assistant: a fictional subsea XT and manifold manufacturer)** across both tracks, used for **standalone worked examples**. No example depends on an earlier module. Advanced takes the same company further: an MCP server over its data, a pro-code rebuild, evals, CI/CD. |
| Hands-on practice | **None.** Worked examples live inside lessons (*In practice*, *Pitfalls*). The scenario's data model exists on paper only. |
| Languages | **English first.** Each lesson can get an optional `<topic>.pt-BR.md` translation. The language switch and the roadmap's "Ler em português" link only appear when a translation exists. |
| Self-checks | **Five questions per module** at the end of `module.md`, answers hidden in `<details>` and explaining the reasoning. |

## Delivery & tooling

- **Repository:** source lives in the **public** GitHub repo `matheus-sancha/AI-Academy`: `_source/`, `_build/`, `docs/`. Built HTML and PDFs are **not** committed.
- **Public-repo rule:** only the fictional company Technik (identifier formats and document codes follow the maintainer's chosen conventions, but every value is invented) and placeholders (`<your-account>`). No real organization names, tenant or account identifiers, internal URLs or tenant screenshots, and never credentials or `.env` files.
- **Working copy:** cloned **outside OneDrive** so OneDrive never syncs `.git`. `build.py` writes to `--out DIR`, else `AI_ACADEMY_OUT`, else `dist/`. The maintainer points `AI_ACADEMY_OUT` at the OneDrive share.
- **Distribution:** files only (HTML + PDF, shared via OneDrive). Everything must work from `file://`, which means no `fetch`, a search index inlined into the JS, and relative links only.
- **Build:** extend `_build/build.py` with a real Markdown library (tables, fenced code, admonitions, Mermaid). One pipeline for roadmaps and course.
- **Source of truth:** the roadmap `.md` owns topic id, title, flags and links. Lesson files live at `_source/course/<SECTION>/<topic-id>.md` and contain the body only.
  - **Always errors:** orphan lessons (no matching topic id) and malformed or unclosed volatile tags.
  - **Warnings, which fail with `--strict`** (release builds): topics without a lesson, broken internal links, volatile blocks verified more than 6 months ago, and full lessons that don't start with `## TL;DR`.
  - Each roadmap node's drawer links to its lesson once the lesson exists.
  - Progress is shared: the same `aiem:<track>:<topic-id>` localStorage key covers both the roadmap node and the lesson.

```
_source/
  beginner.md, advanced.md          roadmaps (identity + links)
  course/
    scenario.md                     Technik company, systems, data model, conventions
    B7/
      module.md                     outcomes, prerequisites, self-check
      tools.md  connectors.md ...   lessons (file name = topic id)
      tools.pt-BR.md                optional translation
```

## Build order

1. ✅ `build.py`: Markdown library, lesson pages, inlined search, volatile-tag stripping and staleness report, `--strict`. Authoring syntax is documented in `_build/README.md`.
2. ✅ `scenario.md`: company, systems, identifiers, data model and deliberate data flaws.
3. ✅ **Pilot slice:** B1 and B7. The Snowflake lab environment, the B1 exercise and the B7 lab built for the pilot were
   removed on 2026-09-14 when the course became documentation only; their worked examples were folded into the lessons.
4. ◆ **Review the pilot:** template, lesson length, tone, search over `file://`. See
   *Pilot outcomes* below for what the pilot settled and what is still open.
5. B0, B2–B6, B8–B14, then A0–A14.

## Pilot outcomes

Settled by writing B1 and B7:

| Question | Answer |
|---|---|
| **Self-check format** | Per module, in `module.md`, as a `## Self-check` section of five questions using `<details><summary>` so the answer is hidden until asked for and prints expanded. Answers explain the reasoning rather than stating a verdict. |
| **Lesson length** | Full lessons land at **1,000–1,450 words** (B1 mean 1,124, B7 mean 1,237 — B7 is longer because it carries more decision tables); `[opt]` lessons at **390–520**. At ~160 full lessons plus ~25 short ones that is roughly 195k words, which matches the original estimate. |
| **Links to unwritten modules** | Link to the roadmap section (`../../beginner.html#B5`), not to a module page that does not exist yet. The build's link check catches the alternative. |
| **Where the scenario lives** | `_source/course/scenario.md` renders at `course/scenario/index.html`. Lessons link to it rather than restating the data model. |
| **Standalone examples** | Confirmed workable. B7's examples specify their own starting point, so a reader who skipped B6 loses nothing. |

Still open, and genuinely for the review:

- **Lesson length.** ~1,200 words is a 5–6 minute read, so a nine-lesson module is about an hour of
  reading. If that is too long, the first thing to cut is the *Key terms*
  section, which partly repeats definitions the body already gives.
- **Search over `file://` with the full course** is untested at volume — the index currently holds 22
  pages and will hold several hundred.
- **PDF export of lesson pages** has not been tried; only the roadmaps have PDFs today.
- **`<details>` in print.** Browsers differ on whether a closed `<details>` prints its content.
  Worth checking before PDFs are promised.

## Open risks

- **Authoring volume.** ~160 full lessons plus ~25 short ones, roughly 200k+ words. The pilot review should confirm the target length before committing to it.
- **Stale copies.** With files-only distribution, learners can keep working from old copies. Show the build date (and git commit) on every page, and consider a "latest version lives at…" note.
- **No practice.** Readers can finish the course without ever building an agent. It is reference and training material, not proof of skill; marking a lesson *Done* means it was read.
- **Volatile content is the maintenance load.** B7 carries several volatile blocks and B1 two, all around Copilot Studio surfaces and model availability. Re-verifying a module is therefore a real recurring task, not a formality, and `--strict` will start failing six months after each verification date.
