# Course Design — Three Levels

> Agreed in a design interview on 2026-09-13; revised 2026-09-14 (documentation only, no labs);
> **re-cut 2026-09-20 → 2026-09-27 into three levels**, replacing the two-track Beginner/Advanced
> design this file used to describe. The re-cut is recorded ticket by ticket on
> [the restructure map](https://github.com/matheus-sancha/AI-Academy/issues/2); each decision below
> links to the ticket that holds its reasoning.
>
> This file is the **standing design reference for the writing effort**: what a lesson has to look
> like, where it may point and how a claim has to be sourced. Authoring *syntax* — every macro,
> marker and flag — lives in [`_build/README.md`](../_build/README.md) and is not repeated here.
> The three roadmaps in `_source/` own every id, title, flag and link.

## Vocabulary

One word per thing ([#4](https://github.com/matheus-sancha/AI-Academy/issues/4)); these are the words
to use in prose, commit messages and tickets.

| Word | Means |
|---|---|
| **Level** | Basic, Intermediate, Advanced. One roadmap file, one `<level>.html` page. Not *track*, not *tier*. |
| **Module** | A `# ` section of a roadmap: one directory under `_source/course/`. Not *section* in prose. |
| **Topic** | A `## ` entry: one id, one title, its flags and its curated links. |
| **Lesson** | The page that teaches a topic — `<module>/<topic-id>.md`. A topic exists from the moment the roadmap names it; a lesson exists once it is written. |
| **Overview** | A module's own page, `<module>/overview.md`: outcomes, what it assumes, the self-check. (The old `module.md` is gone.) |
| **Assumed pointer** | A topic flagged `assumed`, reusing a lower level's topic id to say *you need this and it is taught there*. Not a topic of its own and never counted as one. |

Module and topic ids are globally unique **slugs**; the old `B*`/`A*` numbering is retired. What the
reader sees in a badge or crumb (`B3`, `I7`, `A11`) is **derived** — level letter plus file position,
stored nowhere ([#21](https://github.com/matheus-sancha/AI-Academy/issues/21)). Reordering modules
renumbers them, so a badge is never an identifier and never appears in prose.

Each level's **assumed-knowledge module is a real module**: it holds badge position 1, so a level's
first content module is `2`. It has caught two tickets out already — count content modules and the
file always holds one more.

## The three levels

| Level | Audience | Promise | Modules | Topics |
|---|---|---|---|---|
| **Basic** | Everyone at the company | Use Microsoft Copilot well: what it is, why it invents things, how to prompt it, what it can see, and Copilot in Chat, Word, Excel, PowerPoint, Outlook and Teams. Nothing here builds anything. | 11 | 37 |
| **Intermediate** | Engineers | Design, build, test and publish an agent in **Copilot Studio**, ending in a guided build followed end to end. | 18 | 108 |
| **Advanced** | Engineers who finished Intermediate | Master the editor agent, then build, ship and operate **pro-code** agents (Agents SDK, Agent Framework, Foundry), with evals, observability, security and ALM — ending in a capstone build written in full. | 17 | 121 |

The levels **stack**: each one opens with an assumed-knowledge module and nothing is taught twice
([#3](https://github.com/matheus-sancha/AI-Academy/issues/3)). Basic doubles as the engineers' entry
gate. Advanced's assumed module draws on **Intermediate only** — Basic sits behind Intermediate's,
so it is not restated a second time
([#23](https://github.com/matheus-sancha/AI-Academy/issues/23)).

**The boundary rule.** A topic belongs to the **earliest level that needs it to ship on that level's
build surface**, recurring later only for genuinely different technique. Basic admits whatever
**changes how a non-builder uses Copilot**, and nothing more. Nothing from the two old roadmaps was
dropped: all 211 topics were redistributed, Snowflake, automation, safety, governance and ALM
included.

**A moved topic is re-pitched, not relocated.** Three tickets in a row found the same thing
([#13](https://github.com/matheus-sancha/AI-Academy/issues/13),
[#21](https://github.com/matheus-sancha/AI-Academy/issues/21),
[#20](https://github.com/matheus-sancha/AI-Academy/issues/20)): text written for an agent builder does
not serve a Copilot user, the id still resolves, and no check notices. When a topic changes level,
re-read every sentence for who it addresses — and check the far side too, because a re-pitch can
silently strip what the *other* level depended on (Intermediate's `output` lost its JSON half that
way).

## Pedagogy

| Decision | Choice |
|---|---|
| Delivery | **Purely self-paced documentation.** No facilitator, labs, exercises or environment to provision. Every lesson has to make sense on its own. |
| Practice | **One guided build per engineer level, and no other hands-on.** Worked examples live inside lessons (*In practice*, *Pitfalls*). The scenario's data model exists on paper only. |
| Lesson depth | **Full original textbook** for stable content; short guidance plus a curated link where content moves (Copilot Studio click-paths, preview features, pricing). The course has to hold up as reference documentation. |
| Lesson length | **Basic 600–900 words. Intermediate and Advanced 1,000–1,450** — the pilot's approved band. `opt` / `prev` lessons **390–520** anywhere. ([#13](https://github.com/matheus-sancha/AI-Academy/issues/13)) |
| Curated links | **2–3 per topic**, each label quoting the target page's **real current title**. Labels inherited from the old roadmaps have been wrong 24 times in one level; compare the label head against the title prefix, not word overlap. ([#21](https://github.com/matheus-sancha/AI-Academy/issues/21), [#23](https://github.com/matheus-sancha/AI-Academy/issues/23)) |
| Self-checks | **Five questions per module**, in `overview.md`, answers hidden in `<details>` and explaining the reasoning rather than stating a verdict. |
| Product name | **Microsoft Copilot** (following Microsoft's own docs), except where a licence name or a link label says otherwise. ([#21](https://github.com/matheus-sancha/AI-Academy/issues/21)) |
| Languages | **English first.** Each lesson can get an optional `<topic>.pt-BR.md`; the language switch appears only where a translation exists. |

### The lesson skeleton

Both variants end in *Go deeper*, auto-filled from the roadmap's links.

| Level | Skeleton |
|---|---|
| Intermediate, Advanced | TL;DR → Why it matters → How it works → In practice at Technik → **Design guidance** → Pitfalls (*symptom → cause → fix*) → Key terms |
| Basic | TL;DR → Why it matters → How it works → In practice at Technik → **Using it well** → Pitfalls → Key terms |

Basic renames the fifth slot because its reader designs nothing (settled here, raised by
[#25](https://github.com/matheus-sancha/AI-Academy/issues/25)); the slot's job is unchanged and the
three written Basic lessons already use the new heading.

**Pitfalls is the load-bearing section**, not a footnote. It is where a tenant-dependent step, a
result that differs with nothing to grade it against, and a click-path that has moved all get said
([#12](https://github.com/matheus-sancha/AI-Academy/issues/12)).

### The guided builds

Each engineer level ends in one build the reader follows end to end, and they are **deliberately
asymmetric** ([#12](https://github.com/matheus-sancha/AI-Academy/issues/12),
[#9](https://github.com/matheus-sancha/AI-Academy/issues/9)):

- **Intermediate — `guided-build`, three ordinary lessons** (`whatyouneed`, `theroute`,
  `whenitstalls`). The seven-stage narrative stays **upstream** in
  [copilot-studio-skills](https://github.com/matheus-sancha/copilot-studio-skills); the course hands
  the reader to it rather than re-narrating it, so it cannot drift. No new page type: the skeleton
  above carries all three, with the stage table in `theroute` doing the *what you should be holding
  when a stage ends* job the skeleton has no slot for.
- **Advanced — `capstone-build`, six pages written in full** (scaffold → MCP server over Technik's
  Teamcenter data → agent → evals → ship, with `buildsetup` first because a missing grant surfaces
  three stages later as an empty result set). There is no upstream route here, so there is nothing to
  drift from, and Advanced uses the stage-page treatment Intermediate rejected. **No new Agent Skills
  are authored for Advanced** — that reverses the original framing; see
  [#9](https://github.com/matheus-sancha/AI-Academy/issues/9).

## The scenario

**One scenario for all three levels, as a technical reference rather than a story**
([#11](https://github.com/matheus-sancha/AI-Academy/issues/11),
[#18](https://github.com/matheus-sancha/AI-Academy/issues/18)). `_source/course/scenario.md` holds
Technik's operation chain, systems, identifier formats, the 13-table model, five deliberate data
flaws, the Production Assistant's seven capabilities and the document set. Personas, the business
narrative and the industry intro were **deleted** — no lesson may reintroduce a persona name.

Worked examples are **standalone**: no example depends on an earlier module. The scenario page keys
its example tables on module slugs, and states which part of itself each level may use:

- **Basic — the document layer only.** No data model, no SQL, no table names.
- **Intermediate and Advanced** — the full model.

One object (`SWI70000318`) is met at three depths as the reader climbs.

## Cross-references

**No hand-written path, no id, no level name.** Every reference to another part of the course goes
through `{{topic:<id>}}` or `{{module:<id>}}`, which render the target's current title and resolve
against the **roadmap**, not the filesystem — so a target with no lesson yet links to its roadmap
entry and retargets itself when the lesson lands
([#13](https://github.com/matheus-sancha/AI-Academy/issues/13),
[#19](https://github.com/matheus-sancha/AI-Academy/issues/19)).

The rule is *no path, no id, no level name* for a reason: the switchover's reference count looked for
retired **ids** and therefore could not see 18 plain relative links like
`[Context & Context Window](context.html)`, two of which a module split silently broke
([#20](https://github.com/matheus-sancha/AI-Academy/issues/20)). A stale **level name** ("the Beginner
track") carries no id either, and survived two id sweeps.

`{{topic:<id>#section}}` deep-links to a section. **The build never checks a `#fragment`** — not in a
macro and not in a link — so the rule for writers is *keep the heading you name*. A target with no
lesson yet drops the anchor. (This corrects an older claim in this file that the build catches broken
internal links: it checks the **file**, only ever the file.)

Assumed knowledge is not written as a link at all: it is the topic flag **`assumed`**, which states no
target, because globally-unique ids let the build resolve it
([#16](https://github.com/matheus-sancha/AI-Academy/issues/16)).

## Sourcing: doc, tenant, unknown

**No bare assertions** ([#15](https://github.com/matheus-sancha/AI-Academy/issues/15)). Every product
claim is sourced one of three ways:

| Tier | For | How it is written |
|---|---|---|
| **Doc** | The default — most claims. | Cited to Microsoft documentation. |
| **Tenant** | Claims a reader **acts on**, where being wrong makes them do the wrong thing. | `<!-- verified tenant=YYYY-MM -->`, hidden from the reader, aged by the build. |
| **Unknown** | Nobody has checked. | `<!-- unknown since=YYYY-MM -->`, **visible** to the reader as *Not yet verified*, counted and aged by the build. |

An open unknown is legitimate content; only a stale one fails `--strict`. **Silence is not an option**
— a reader told that skills don't reach a running conversation, and told nothing about tools, will
assume tools behave the same way, so the marker goes next to the fact the wrong generalisation would
hang off.

**Where a claim can be marked matters.** All three markers are **lesson syntax**. The roadmap format
has no marker mechanism, so a topic description cannot carry an unknown — keep an unverified assertion
out of the roadmap and make it in the lesson, where it can be marked
([#22](https://github.com/matheus-sancha/AI-Academy/issues/22)).

A contradiction between the course and the skills repo is **fixed upstream**: the course marks it
unknown, the fix lands upstream, upstream cuts a release, the course bumps its pin, the marker comes
off. The two repos never disagree in front of a reader mid-build. Two claims sit at this stage today —
the 8-skill cap (a tenant check: add a ninth skill) and whether an added tool reaches a running
conversation. The second is now **documented** — the GitHub Copilot harness testing page says a new tool
reaches the next turn, found by [#30](https://github.com/matheus-sancha/AI-Academy/issues/30) — so what
remains is checking upstream agrees; an added **knowledge source** is still unknown.

## The skills pin, and the checklist for bumping it

Intermediate's `guided-build` and `the-six-skills` depend on a repo this course does not own, and that
repo cut **five releases in eight hours** on 2026-09-20
([#14](https://github.com/matheus-sancha/AI-Academy/issues/14)). So:

- The course pins a **named release tag** — not `latest`, not `main`, not a SHA — declared once as
  `skills_pin:` in `_source/intermediate.md`'s front matter and substituted everywhere via
  `{{skills-version}}` / `{{skills-release-url}}`. Today: **v0.3.0**.
- The pin is **stated to the reader** on the page, so someone returning months later can tell whether
  what they downloaded matches what they are reading.
- The dependency is **bounded to two modules**. Intermediate's module list stands on its own
  pedagogical merits and does **not** track the upstream route; the blast radius of an upstream change
  is `guided-build`, `the-six-skills` and a version string.
- Drift is detected by **`check_links.py`**, which is already the one script allowed online.
  `build.py` stays offline and deterministic, because the course is opened over `file://`.

**When the pin moves, re-check in this order:**

0. Does `docs/research/copilot-studio-skills-survey.md` still describe the pinned release? *(It does
   not today: it cites `74f8916`, one commit ahead of v0.3.0 and untagged — a reader cannot download
   what it documents.)*
1. Did the stage count or order change? → `guided-build`
2. Was a skill renamed, added or removed? → `the-six-skills`
3. Did any constraint change (the 8-skill cap, the 8,000-character instruction ceiling, the mandatory
   instruction sections)? → `writing-instructions`, `agent-skills`
4. Do the survey's findings still hold? → re-run the sourcing policy above over anything that moved.

## One course, with a door at the Basic seam

The two seams are not alike ([#17](https://github.com/matheus-sancha/AI-Academy/issues/17)): Basic →
Intermediate goes from *everyone* to engineers and is a continuation for only a few readers, while
Intermediate → Advanced is the same reader carrying on. So the pager differs per seam:

- **Basic** ends on its closing module and the lesson pager **stops there**. The offer to continue is
  a soft link on the roadmap page (*"Want to build agents?"*), not a push. Basic's front matter has no
  `continues:`.
- **Intermediate** sets `continues: yes`, so its last page carries on to **`advanced.html`** — the
  roadmap, not Advanced's first lesson, because that is the only page where a level's assumed
  knowledge is listed.
- **Search is one flat index** with a level badge on every result. Filtering by level was rejected:
  stacking means an Intermediate reader *should* find a Basic page.

## Delivery & tooling

- **Repository:** source lives in the **public** GitHub repo `matheus-sancha/AI-Academy`: `_source/`,
  `_build/`, `docs/`. Built HTML and PDFs are **not** committed.
- **Public-repo rule:** only the fictional company Technik (identifier formats and document codes
  follow the maintainer's conventions, but every value is invented) and placeholders
  (`<your-account>`). No real organization names, tenant or account identifiers, internal URLs or
  tenant screenshots, and never credentials or `.env` files.
- **Working copy:** cloned **outside OneDrive** so OneDrive never syncs `.git`. `build.py` writes to
  `--out DIR`, else `AI_ACADEMY_OUT`, else `dist/`; the maintainer points `AI_ACADEMY_OUT` at the
  OneDrive share.
- **Distribution:** files only (HTML + PDF, shared over OneDrive). Everything must work from
  `file://` — no `fetch`, a search index inlined into the JS, relative links only.
- **Progress** is stored per browser under **`aiem:<topic-id>`** — no level segment, so a topic keeps
  its ticks when it changes level. Roadmap node, lesson and assumed pointer share the one key.
  `progress.js` migrates the old `aiem:<track>:<MODULE>-<topic>` keys once per browser; delete it a
  release or two after the re-cut ships.

```
_source/
  basic.md  intermediate.md  advanced.md     roadmaps: ids, titles, flags, links, front matter
  course/
    scenario.md                              Technik: systems, identifiers, data model, flaws
    how-copilot-works/
      overview.md                            outcomes, assumed knowledge, self-check
      llm.md  context.md  hallucination.md   lessons (file name = topic id)
      llm.pt-BR.md                           optional translation
```

### What the build enforces

Run `python build.py --strict` before anything ships; `python check_links.py <level>.md` verifies
external links and the pin. Full syntax and flag reference:
[`_build/README.md`](../_build/README.md).

| Enforced | Not enforced |
|---|---|
| Duplicate module or topic ids, across every level | `#fragment` targets, in links or macros |
| A lesson in the wrong module's directory; orphan lessons | Whether a lesson sits in its level's word band |
| An `assumed` pointer to an unknown id, or to the same or a higher level | Whether a moved topic was re-pitched for its new reader |
| Unresolvable `{{topic:}}` / `{{module:}}` targets | The core / reference split (below) |
| Broken relative links — the **file**, never the fragment | Whether a link label matches its target's real title |
| Malformed markers; `volatile` / `tenant` / `unknown` blocks older than 6 months | |
| A full lesson that does not open with `## TL;DR` | |
| `continues: yes` on the last level; two roadmaps declaring different `skills_pin` values | |

**Topics with no lesson are counted, never a failure** — `--strict` included. That is a deliberate
demotion (2026-09-20): 249 unwritten topics would otherwise make the release gate unreachable for the
whole writing effort, and the count doubles as its progress meter.

### The one convention the build cannot check

Each engineer level orders its modules as a **core path** ending in the guided build, followed by
**reference modules** a reader visits on demand (`snowflake-sql`, `automation-and-workflows` in
Intermediate; `llm-internals`, `advanced-rag`, `snowflake-cortex`, `automation-advanced`,
`models-and-fine-tuning` in Advanced), with a closing module last where there is one.

This is an **editorial convention, and nothing enforces it**
([#22](https://github.com/matheus-sancha/AI-Academy/issues/22)). The roadmap format has no
core/reference distinction: the split is carried by file order plus one sentence in the module intro
(*"Reference, not a read-through. Come here when…"*), and a later edit can interleave a reference
module back into the core path with no warning. Keep reference modules last, and keep that intro
sentence — it is the only signal the reader gets.

## Scope

| | Modules | Topics | Lessons written | Remaining |
|---|---|---|---|---|
| Basic | 11 | 37 | 3 | 34 |
| Intermediate | 18 | 108 | 96 | 12 |
| Advanced | 17 | 121 | 0 | 121 |
| **Total** | **46** | **266** | **99** | **167** |

Kept current by the writing effort: every ticket on
[the Intermediate writing map](https://github.com/matheus-sancha/AI-Academy/issues/26) updates this
table, the paragraph below it and the first open risk as it closes. `build.py` prints the remaining
count on every run, so the table is checkable against the build rather than trusted.

Module counts include each level's assumed-knowledge module; the 42 assumed pointers are not topics.
At the bands above, the 167 remaining topics — plus an overview for each module that has none, less the
three assumed-knowledge modules, which may not need one — come to roughly **240–260k words**. The
~270–290k figure was accepted as the target on 2026-09-27, superseding the pilot's "~160 full lessons
plus ~25 short ones, roughly 195k words". Written so far: 114 pages, ~145.6k words.

## Build order

1. ✅ `build.py`: Markdown library, lesson pages, inlined search, marker handling, macros, derived
   badges, `--strict`. Syntax documented in `_build/README.md`.
2. ✅ `scenario.md` as a technical reference.
3. ✅ **Pilot slice** (2026-09-14, reviewed and approved): lesson length, tone, depth, the Technik
   examples and the self-checks all kept. See *Pilot outcomes*.
4. ✅ **Three-level re-cut** (2026-09-27): `basic.md`, `intermediate.md`, `advanced.md` written and
   live, the pilot's two modules migrated and re-pitched, `--strict` passing.
5. ◆ **Lesson prose for the remaining 167 topics**, and an overview per module. A level at a time, in
   file order, following the written modules as the template. Intermediate is under way as
   [map #26](https://github.com/matheus-sancha/AI-Academy/issues/26), whose tickets carry the writing
   itself; Basic's 34 and Advanced's 121 are separate efforts.

## Pilot outcomes

Settled by writing the pilot's two modules, and still binding:

| Question | Answer |
|---|---|
| **Self-check format** | Per module, in `overview.md`, five questions in `<details><summary>` so the answer is hidden until asked for and prints expanded. Answers explain the reasoning. |
| **Lesson length** | Full lessons land at 1,000–1,450 words; `opt` lessons at 390–520. Confirmed as *not too long* in review. Basic's narrower 600–900 band came later, from re-framing three of these lessons for a non-builder. |
| **Links to unwritten topics** | Handled by the macros above — `{{topic:}}` links to the roadmap entry until the lesson exists. (The pilot hand-wrote `../../beginner.html#B5`; that is exactly what broke.) |
| **Where the scenario lives** | `_source/course/scenario.md` → `course/scenario/index.html`. Lessons link to it rather than restating the model. |
| **Standalone examples** | Confirmed workable: examples specify their own starting point, so a reader who skipped a module loses nothing. |

## Open risks

- **Authoring volume — accepted, not solved.** 167 topics at ~240–260k words is the single biggest
  commitment on this course, and the levels are back-loaded: Advanced alone is 121 topics with nothing
  written. If it stalls, the lever is depth per topic, not topic count — reference modules can drop to
  short curated-link lessons without losing a topic or a link.
- **Volatile content is the recurring maintenance load.** Every `volatile`, `tenant` and `unknown`
  block ages out at 6 months and then fails `--strict`. Re-verifying a module is a real task, and
  there are now three levels of them.
- **Stale copies.** With files-only distribution, readers can keep working from old copies. Every page
  shows the build date; consider a "the latest version lives at…" note.
- **No practice outside the two builds.** A reader can finish a level without building anything.
  Marking a lesson *Done* means it was read.
- **Search over `file://` at volume** is untested: the index holds 21 pages today and will hold
  several hundred, inlined into the JS.
- **PDF export of lesson pages** has never been tried — only roadmaps have PDFs — and browsers differ
  on whether a closed `<details>` prints its content. Both bite at publish time.
- **Translation.** `<topic>.pt-BR.md` is supported and unused. Basic has the widest audience and the
  shortest lessons, which is where that calculus would change first; nobody has decided.
