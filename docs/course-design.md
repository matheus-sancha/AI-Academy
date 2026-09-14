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
| Lesson skeleton | TL;DR → Why it matters → How it works → In practice (Technik) → Design guidance → Pitfalls (symptom → cause → fix) → Key terms → Go deeper (auto-filled from roadmap links) |
| `[opt]` / `[prev]` topics | Short "good to know" lessons (~300–500 words). Never required by labs, exercises or self-checks. Content about `[prev]` features is volatile-tagged. |
| Scenario | **One running scenario (Technik Production Assistant: a fictional subsea XT and manifold manufacturer)** across both tracks. Advanced takes the same company further: an MCP server over its data, a pro-code rebuild, evals, CI/CD. |
| Labs | Each lab is **independent**: every lab ships its start state, so no lab depends on the learner finishing the previous one. Labs are for modules where something gets built. |
| Concept modules | (e.g., B0, B1, B4, A1, A11) get a **15–30 min exercise** instead of a lab. Exercises don't change the scenario's state. |
| Languages | **English first.** Each lesson can get an optional `<topic>.pt-BR.md` translation. The language switch and the roadmap's "Ler em português" link only appear when a translation exists. |
| Lab verification | **Observable checklist + reference solution.** Lab N's solution is also the starter for lab N+1. |

## Lab environment

- **Snowflake.** Each learner gets their own `SANDBOX_<user>` schema, cloned from a read-only `SEED` schema by scripts in the repo. There are two roles:
  - `ACADEMY_LEARNER_<user>` owns the sandbox (create rights, XS warehouse with a resource monitor).
  - `ACADEMY_AGENT_<user>` has read-only access and is the only role agents, connectors and MCP servers use.
  - Each lab's step 0 runs an idempotent reset to that lab's start state (e.g., `RESET_TO('B7')`). The procedure runs as the caller and derives the sandbox from the caller's role, so nobody can reset anyone else's schema.
  - Dates in the seed are stored as offsets from an anchor and re-anchored on every reset, so "this month" questions keep working however old the seed is.
  - The roadmap `devenv` topic describes this two-role setup.
- **Power Platform.** Starters and solutions are **unmanaged solution .zip** files, imported into the learner's developer environment; learners then re-bind connection references.
- **Checkpoint authoring.** Claude writes `lab.md` as an exact build spec. The maintainer builds it in a dev environment (this doubles as the first test run), reports fixes, then exports the start/solution zips into `labs/<id>/`.

## Delivery & tooling

- **Repository:** source lives in the **public** GitHub repo `matheus-sancha/AI-Academy`: `_source/`, `_build/`, `docs/`, `labs/` (lab zips are source, so they're committed). Built HTML and PDFs are **not** committed.
- **Public-repo rule:** only the fictional company Technik (identifier formats and document codes follow the maintainer's chosen conventions, but every value is invented) and placeholders (`SANDBOX_<user>`, `<your-account>`). No real organization names, tenant or account identifiers, internal URLs or tenant screenshots, and never credentials or `.env` files.
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
    scenario.md                     Technik company, data model, agent storyline
    B7/
      module.md                     outcomes, prerequisites, self-check
      tools.md  connectors.md ...   lessons (file name = topic id)
      tools.pt-BR.md                optional translation
labs/
  _setup/snowflake/                 seed + reset scripts, role setup
  _setup/documents/                 the fictional Technik documents labs use as knowledge,
                                    as Markdown; built to HTML and (with --pdf) PDF
  B1/
    exercise.md                     concept modules
  B7/
    lab.md
    start/TechnikAssistant_B6_end.zip
    solution/TechnikAssistant_B7_end.zip
```

## Build order

1. ✅ `build.py`: Markdown library, lesson pages, inlined search, volatile-tag stripping and staleness report, `--strict`. Authoring syntax is documented in `_build/README.md`.
2. ✅ `scenario.md`, and the Snowflake role/seed/reset scripts in `labs/_setup/snowflake/`: two-role provisioning per learner, a read-only `SEED` schema, `RESET_TO(<module>)` that clones it into the sandbox and re-anchors dates, and `_build/check_seed.py` to validate the data without a Snowflake account. **Not yet run against a real account** — the first run by the maintainer is its first test.
3. ✅ **Pilot slice:** B1 (concept module with an exercise) and B7 (lab module). Written and building;
   B7's start and solution zips are the maintainer's to produce from `labs/B7/lab.md`, which is
   written as an exact build spec, with `labs/B7/BUILD-NOTES.md` listing what to export and what is
   deliberately left out.
4. ◆ **Review the pilot:** template, lesson length, tone, lab packaging, search over `file://`. See
   *Pilot outcomes* below for what the pilot settled and what is still open.
5. ✅ **B6 Knowledge & RAG**, written next rather than in roadmap order because
   `labs/B6/solution/TechnikAssistant_B6_end.zip` *is* B7's starter — building them in one sitting
   avoids two hand-built copies of the same agent drifting apart. Writing it also required the
   Technik documents (`labs/_setup/documents/`), which nothing had authored yet.
6. ✅ **B8 Skills**, continuing the checkpoint chain B5→B6→B7→B8 so the whole run can be exported
   in one sitting. Writing it surfaced the harness constraint recorded below.
7. B0, B2–B5, B9–B14, then A0–A14.

## Pilot outcomes

Settled by writing B1 and B7:

| Question | Answer |
|---|---|
| **Self-check format** | Per module, in `module.md`, as a `## Self-check` section of five questions using `<details><summary>` so the answer is hidden until asked for and prints expanded. Answers explain the reasoning rather than stating a verdict. |
| **Lesson length** | Full lessons land at **1,000–1,450 words** (B1 mean 1,124, B7 mean 1,237 — B7 is longer because it carries more decision tables); `[opt]` lessons at **390–520**. At ~160 full lessons plus ~25 short ones that is roughly 195k words, which matches the original estimate. |
| **Links to unwritten modules** | Link to the roadmap section (`../../beginner.html#B5`), not to a module page that does not exist yet. The build's link check catches the alternative. |
| **Where the scenario lives** | `_source/course/scenario.md` renders at `course/scenario/index.html`. Lessons link to it rather than restating the data model. |
| **PDF granularity** | One PDF per module, not per lesson and not one enormous file. Lessons start on a fresh page, which costs about a quarter of the page count and is worth it in print. |
| **Exercises for concept modules** | Self-contained: no environment, no network, answers inline. B1 comes before anyone has built anything, so an exercise needing Copilot Studio would be unusable. |
| **Where the Technik documents live** | `labs/_setup/documents/`, as Markdown with front matter, rendered to HTML and PDF by the build. Markdown so they can be reviewed and diffed; PDF because "upload these as knowledge" needs real files. A release build must therefore be run with `--pdf` before B6 is usable. |
| **Authoring order between coupled labs** | Write a module and the module whose starter it produces together. B6 and B7 share one exported solution; discovering that after B7 was written meant reconciling six places in `labs/B7/lab.md`. |
| **Checkpoint solutions may hold more than one agent** | B8's does. The naming convention `TechnikAssistant_<module>_end.zip` still holds — it names the checkpoint, not the agent. |
| **Lab independence** | Confirmed workable. `labs/B7/lab.md` describes its own starter precisely enough that a learner who skipped B6 loses nothing. |

Settled afterwards by measurement, on a stub build of all 15+15 sections (302 course pages, which
is what the finished course looks like):

| Question | Finding |
|---|---|
| **Lesson length** | **Keep ~1,200 words.** Confirmed by the maintainer. A nine-lesson module is about an hour of reading before the exercise or lab, and holds up as reference documentation, which was the goal. |
| **Search over `file://` at volume** | The index reaches **1.87 MB** at full size. It is now loaded on first use rather than with every page, by injecting a `<script>` element — which works under `file://`, where `fetch` and `XHR` do not. Measured: ~20 ms saved per page view on local disk (small), but the distribution target is a OneDrive-synced folder where a 1.87 MB read per page view is not free. First search costs 300 ms including the load; later keystrokes are debounced and the handler costs 0.2 ms. |
| **PDF export of lesson pages** | Works. Each module now also builds `course/<SECTION>/print.html` — the whole module on one page, useful in its own right — and `--pdf` renders one PDF per module. A full release build is **12 s for 302 pages and 32 PDFs**, 23 MB of output. |
| **`<details>` in print** | Confirmed a real problem: a closed `<details>` prints as its summary alone, which would have silently dropped every self-check answer. Fixed by opening them on `beforeprint` and under `?print`, and restoring afterwards. Verified 8/8 and 5/5 open in the B1 and B7 print pages under print media. |
| **Mermaid offline** (found while testing the above) | Diagrams were loaded from a CDN, so with no network **every diagram degraded to its own source code** — which contradicts the files-only distribution model. Mermaid is now vendored into `assets/` at build time, fetched once from the npm registry (canonical, immutable, and reachable from locked-down build machines where CDN hosts are not) and cached in `_build/.cache/`. If the fetch fails the build warns and falls back to the CDN. |

## The harness constraint

Found while writing B8, and it shapes several modules:

- The Technik Production Assistant is on the **standard harness**, because B5 gives it a *Work order
  status* topic and topics are standard-harness only.
- Skills are a **GitHub Copilot harness** feature, and the roadmap's own `B8 reuse` topic says
  standard-harness agents do not support them.
- The harness is chosen at agent creation and **cannot be changed**.

So B8 cannot put a skill on the assistant. Rather than working around it, the module makes it the
lesson: the skill goes on a second agent, *Technik QN Assistant*, on the GitHub Copilot harness, and
the assistant delegates to it as a connected agent. `labs/B8/lab.md` step 1 has learners confirm the
constraint by looking for a Skills area that is not there.

Consequences to keep in mind when writing the remaining modules:

| Module | Consequence |
|---|---|
| B5 | Must state the harness choice and why, since B8 depends on it. Record the reasoning in the agent, not only in the lab |
| B8 | The solution checkpoint contains **two** agents in one solution |
| B12 | Two agents to publish, permission and share, not one |
| A6 | The production/engineering split inherits a mixed-harness estate. That is realistic, and worth saying out loud |

`labs/B8/BUILD-NOTES.md` lists the three things to verify on the first build, in order of how much
of the module each one invalidates. The third — "does the standard-harness agent really have no
Skills area?" — is the most urgent correction in the course if the product has changed.

## Open risks

- **Solution zip compatibility.** Exports can break across platform updates, and zips made from GitHub Copilot-harness agents may not import at all. Re-export checkpoints whenever volatile content is re-verified, and test this in the pilot.
- **Authoring volume.** ~160 full lessons plus ~25 short ones, roughly 200k+ words. The pilot review should confirm the target length before committing to it.
- **Copilot Credits.** Labs that test and evaluate agents consume credits. Each lab should state its expected consumption.
- **Stale copies.** With files-only distribution, learners can keep working from old copies. Show the build date (and git commit) on every page, and consider a "latest version lives at…" note.
- **Output size.** A finished build is roughly 23 MB: 8.6 MB of HTML, 9.5 MB of PDFs, and 4.3 MB of assets (Mermaid 2.6 MB, search index 1.9 MB). Fine for a shared folder, worth knowing before anyone emails it.
- **Lab zips in a public repo.** Before committing an exported solution zip, check it for tenant-specific values: environment URLs, connection ids, Snowflake account locators.
- **Honor-system verification.** Nothing enforces lab checklists. This is acceptable for self-paced learning, but completion data can't be trusted for reporting.
- **Facts stated in more than one place.** The Technik documents state the numbers the seed is built around, the labs quote figures derived from the seed, and B1 quotes a document passage verbatim. `_build/check_seed.py` now checks all three kinds of link, because none of them fail loudly.
- **Volatile content is the maintenance load.** B7 carries six volatile blocks and B1 two, all around Copilot Studio surfaces and model availability. Re-verifying a module is therefore a real recurring task, not a formality, and `--strict` will start failing six months after each verification date.
