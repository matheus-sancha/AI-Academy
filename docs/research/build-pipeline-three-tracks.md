# What must change in `_build/` to carry three tracks

**Research ticket:** [#6](https://github.com/matheus-sancha/AI-Academy/issues/6) · map [#2](https://github.com/matheus-sancha/AI-Academy/issues/2) · 2026-09-20
**Sources:** the `_build/` source itself (primary — cited by file and line), plus build runs against a
throwaway three-track copy of the repo (observed — cited as "experiment").

## Answer

**Nothing in `_build/` changes the plan.** The pipeline is mostly track-count-agnostic already: `parse`,
`build_track`, `roadmap_html`, `handbook_html`, `course.discover`, `course.sequence` and `course.build`
all loop over whatever `_source/*.md` contains. Three tracks build today except for **one hard crash**
(`build_index`) and a handful of hardcoded strings.

Two things do need a decision rather than an edit:

1. **`--strict` cannot pass at the map's destination** and does not today. See [Blocker 1](#blocker-1--strict-fails-on-unwritten-lessons-so-the-maps-destination-is-unreachable-as-stated).
2. **Cross-tier deep links are not enforced** — the link checker discards `#fragment`s, so the
   assumed-knowledge decision is unenforced until `check_internal_links` learns anchors.
   See [Blocker 2](#blocker-2--the-link-checker-never-validates-fragment-so-cross-tier-deep-links-silently-rot).

Everything else is a small, local edit. The full list is below, ordered: blockers, then required
changes, then hazards to design around.

---

## Blockers and surprises

### Blocker 1 — `--strict` fails on unwritten lessons, so the map's destination is unreachable as stated

The map's destination is "the three roadmap files written and `_build/build.py --strict` passing".
That cannot happen at the end of this effort, because `--strict` fails on every topic that has no
lesson yet, and lesson prose is explicitly out of scope.

`course.discover` warns `"<SECTION>/<slug>: no lesson yet"` for every topic without a lesson file
([`_build/course.py:129`](../../_build/course.py)). `build.py` splits those out of normal runs but
folds them back in under `--strict` ([`_build/build.py:202-212`](../../_build/build.py)):

```python
missing = [w for w in report.warnings if w.endswith("no lesson yet")]
others  = [w for w in report.warnings if w not in missing]
...
if report.errors or (strict and report.warnings): sys.exit(1)
```

Observed on the repo as it stands (`python _build/build.py --strict`): exit code **1**, with **194**
`no lesson yet` warnings. After the re-cut that number goes to ~211 (all topics, minus the ~17 B1/B7
lessons that survive).

**Decide one of:** (a) redefine the destination as "`build.py` clean, `--strict` clean apart from
`no lesson yet`"; (b) demote `no lesson yet` out of `--strict` into a separate `--strict-lessons`
release gate — a three-line change at `build.py:202-212`; or (c) accept a red `--strict` for the
duration of the lesson-writing effort. **(b) is the cheap one** and keeps `--strict` meaningful as a
gate on the things this effort *can* fix: broken links, stale volatile blocks, orphan lesson files.

### Blocker 2 — the link checker never validates `#fragment`, so cross-tier deep links silently rot

`course.check_internal_links` strips the fragment before testing existence
([`_build/course.py:209-224`](../../_build/course.py)):

```python
target = link.split("#")[0].split("?")[0]
if not target or target.startswith(("http://", "https://", "mailto:", "javascript:", "/")):
    continue
```

Two consequences, both confirmed by experiment:

- A link to a **real page with a nonexistent anchor** passes silently. A lesson containing
  `[x](../../atrack.html#B1-NOPE)` built clean under `--strict`, with `atrack.html#B1-NOPE` rendered
  verbatim and no warning.
- A **pure-fragment link** (`[x](#nowhere)`) is skipped entirely — `target` is empty, so `continue`.

The settled decision — "each tier opens with an assumed-knowledge section that links BACK to specific
topics in the tier below … cross-tier deep links must resolve, and the link checker should enforce
that" — is therefore **not enforced by anything today**. This is the single most important build
change the restructure needs, because the assumed-knowledge sections are the load-bearing seam
between the three tiers and they are all fragment links.

**Required:** extend `check_internal_links` to collect every `id="…"` from each built page into a set
keyed by output path (anchors it must know about: roadmap handbook topic ids and section ids from
`build.handbook_html` at [`build.py:107-122`](../../_build/build.py); lesson `h2`/`h3` ids minted by
`course.render` at [`course.py:88-95`](../../_build/course.py); the `go-deeper` and `lessons` synthetic
ids at [`course.py:287,300`](../../_build/course.py)), then check the fragment against that set.
Roughly 15 lines in one function. Nothing else in the plan depends on it being harder than that.

### Surprise 1 — `build_index` is the only hard crash, and it is hardcoded to two tracks by name

[`_build/build.py:176-185`](../../_build/build.py):

```python
for key, prefix in (("beginner", "B"), ("advanced", "A")):
    sections = tracks[key]
```

Experiment: with `_source/{advanced,basic,intermediate}.md` present, `build_track` rendered all three
roadmaps fine and then `build_index` died with `KeyError: 'beginner'`. That is the whole of the
"two tracks" hardcoding in Python — everything upstream of it is generic.

### Surprise 2 — a section id reused across two tiers crashes with an opaque traceback

`course.discover` flattens every section of every track into one dict keyed by section id
([`_build/course.py:116`](../../_build/course.py)):

```python
sections = {s["id"]: (track, s) for track, secs in tracks.items() for s in secs}
```

A duplicate id silently clobbers the earlier tier's section. The clobbered section never gets
`s["module"]` or its topics' `t["sources"]`, and the build dies later in `build_track` with
`KeyError: 'sources'` ([`build.py:129`](../../_build/build.py)) — no message naming the duplicate.
Confirmed by experiment (two tracks both declaring `# B1 | …`).

This matters because the re-cut moves `B*` topics into Intermediate and Advanced. **Section ids must
be globally unique across all three tiers**, and the lesson directory `_source/course/<SECTION>/` is a
single flat namespace shared by all tiers ([`course.py:118-124`](../../_build/course.py)), so the ids
have to be unique anyway. Worth a one-line explicit `report.error` in `discover` so the next person
gets a sentence instead of a traceback.

### Surprise 3 — roadmap topic descriptions cannot contain Markdown links

The roadmap source format is not Markdown. `build.inline` ([`_build/build.py:31-34`](../../_build/build.py))
handles only HTML-escaping, `` `code` `` and `**bold**`. A `[label](url)` in a topic description renders
as literal text — confirmed by experiment; the built page contained
`Body. See [deep link](../../atrack.html#B1-nosuchtopic)` verbatim, in both the handbook and the
drawer JSON.

So the assumed-knowledge sections **cannot** carry their back-links in prose as the roadmap format
stands. The options:

- Use the existing curated-resource line: `- doc | Tokens | basic.html#B1-tokens`. It works, but
  `handbook_html` ([`build.py:115-118`](../../_build/build.py)) renders resources with
  `target="_blank" rel="noopener"` and prints the raw URL underneath — which reads wrong for an
  internal link and opens a new tab. Paths would also be relative to the **dist root** from a
  roadmap page but relative to `../../` from a lesson page.
- Add link support to `inline()` (one `re.sub` for `[label](target)`), plus a new resource `type`
  (e.g. `topic`) in `TYPE_LABEL` ([`build.py:82`](../../_build/build.py) and
  [`course.py:35`](../../_build/course.py)) that renders without `target="_blank"` and without the
  raw-URL line.

The second is cleaner and is what makes Blocker 2's anchor check actually useful. Either way this is
**a required change to the roadmap source format**, which means it lands in the same pass that writes
the three roadmap files — flagging it now rather than discovering it mid-write.

### Surprise 4 — there is no way to add a page to a section that is not a roadmap topic

Relevant to the "one guided build per engineer tier" decision. `discover` errors on any `.md` in a
section directory that is neither `module.md` nor a known topic slug
([`_build/course.py:130-136`](../../_build/course.py)): `"orphan lesson (no matching roadmap topic id)"`.
`sequence` emits only `("module", …)` and `("lesson", …)` ([`course.py:143-150`](../../_build/course.py)),
and `page_href`/`page_title` switch on exactly those two kinds ([`course.py:157-165`](../../_build/course.py)).

So a guided build must either **be a roadmap topic** (one topic = one page, inheriting the
`## TL;DR` requirement and the resource-links "Go deeper" block), or a third page kind has to be
added — touching `PAGES` ([`course.py:18`](../../_build/course.py)), `discover`, `sequence`,
`page_href`, `page_title`, `sidebar` ([`course.py:168-182`](../../_build/course.py)), the module page's
lesson `<ol>` ([`course.py:300-303`](../../_build/course.py)) and the search index `k` field
([`course.py:329`](../../_build/course.py)). *Noted, not solved, per the ticket.* The cheap escape
hatch, if a guided build wants several pages, is to make each step a roadmap topic in its own section —
no build change at all.

---

## Required changes, by file and function

### `_build/build.py`

| Where | Change |
|---|---|
| `build_index` ([:176-185](../../_build/build.py)) | **Crash.** Replace the hardcoded `(("beginner","B"),("advanced","A"))` pair with a loop over the tracks in tier order. Needs a per-track placeholder prefix, or a switch to generating the three cards from data rather than string-substituting a fixed template. |
| `build_track` ([:132,137](../../_build/build.py)) | `other = "advanced.html" if meta["id"] == "beginner" else "beginner.html"` and `OTHER_LABEL` are hardcoded two-track logic. **They are also dead** — no template consumes `{{OTHER}}` or `{{OTHER_LABEL}}` (verified: zero matches in `template.html`). Delete, or make them a real previous-tier link. |
| `build_track` ([:138](../../_build/build.py)) | `{{NEXT}}` falls back to `other` when frontmatter omits `next:`. With three tiers every file should carry an explicit `next:`/`next_label:`; the fallback should become "no arrow" rather than a guess. |
| `inline` ([:31-34](../../_build/build.py)) | Add Markdown-link support, or add a `topic` resource type — see Surprise 3. |
| `TYPE_LABEL` ([:82](../../_build/build.py)) | Mirrored in `course.TYPE_LABEL` ([course.py:35](../../_build/course.py)); both need the new type if one is added. |
| `__main__` ([:190-191](../../_build/build.py)) | `parsed = [parse(md) for md in sorted(SRC.glob("*.md"))]` orders tracks **alphabetically by filename**: `advanced, basic, intermediate`. Every consumer that iterates `tracks` inherits that wrong order. Add an explicit `order:` frontmatter key (or a literal tier list) and sort by it. |
| `__main__` ([:202-212](../../_build/build.py)) | The `--strict` gate — see Blocker 1. |
| `pdf` / `__main__` ([:162-173,196-197](../../_build/build.py)) | Per-track already; produces three PDFs named `ai-engineering-on-microsoft-<id>.pdf`. No change beyond the index's hardcoded PDF links. |

### `_build/course.py`

| Where | Change |
|---|---|
| `discover` ([:116](../../_build/course.py)) | Report duplicate section ids explicitly instead of clobbering — see Surprise 2. |
| `check_internal_links` ([:209-224](../../_build/course.py)) | Validate `#fragment` — see Blocker 2. |
| `build` ([:268-272](../../_build/course.py)) | `seq = sequence(sections)` is built **per track**, so Previous/Next never cross a tier boundary: the last lesson of Basic has an empty `NEXT` and the first lesson of Intermediate an empty `PREV` (`nav_link` renders `<span></span>`, [:315-317](../../_build/course.py)). With three stacking tiers the reader should flow Basic → Intermediate → Advanced. Build one global sequence in tier order, or add an explicit cross-tier hand-off page at each boundary. |
| `SCENARIO_HREF` + `build_scenario` ([:19,227-246](../../_build/course.py)) | `TRACK="beginner"` and `TRACK_LABEL="Beginner"` are hardcoded. `TRACK` sets the page's localStorage namespace (`aiem:beginner:`); harmless today because the scenario page has no status control, but it must become `basic`. `TRACK_LABEL` is dead — no template consumes `{{TRACK_LABEL}}` (verified). The "shared by both tracks" comment becomes "all three tiers". |
| `scenario_sidebar` ([:185-196](../../_build/course.py)) | Lists every module of every track, flat and ungrouped, in `tracks` iteration order — i.e. **Advanced first** today (confirmed in the built `course/scenario/index.html`). At three tiers × ~15 sections this is a ~45-item flat list. Group by tier and order by tier. |
| `sidebar` / `crumbs` ([:168-182,199-206,320-322](../../_build/course.py)) | Generic already. Crumbs use `track.capitalize()` → "Basic", "Intermediate", "Advanced" all read correctly. No change. |
| `PAGES` ([:18](../../_build/course.py)) | `("module",)` only. A topic whose slug is `index` would silently overwrite its module page at `course/<S>/index.html` — not caught. Add `"index"` to the reserved list. |
| `lesson_href` / `discover` ([:139-140,122](../../_build/course.py)) | `t["slug"] = t["id"].split("-", 1)[1]` and `t["id"].split("-", 1)[0]` split on the **first** hyphen, and `t["id"]` is `f"{sec_id}-{topic_slug}"` ([build.py:67](../../_build/build.py)). **New section ids must not contain a hyphen** (`INT-1` breaks; `I1` is fine). Topic slugs may contain hyphens. |
| `build` ([:282-283](../../_build/course.py)) | The `## TL;DR` warning fires only for `lang == "en" and not t["opt"]`. Unchanged by three tracks; relevant only if guided-build pages should be exempt. |

### `_build/template.html` (roadmap pages)

- Header nav hardcodes the two tracks ([:159](../../_build/template.html)):
  `<a href="beginner.html">Beginner</a><a href="advanced.html">Advanced</a>`. Needs three links.
  **This failure is caught, not silent**: the experiment with `basic.md` produced
  `warning: basic.html: broken link to beginner.html` from `check_internal_links`, four times across
  the roadmap and index pages plus 20 more from lesson pages — so `--strict` catches a missed rename.
- `KEY = "aiem:" + DATA.track + ":"` ([:216](../../_build/template.html)) is derived from frontmatter
  `id` — generic, no change.
- The Reset button ([:280-282](../../_build/template.html)) clears only the topics of the current
  roadmap (`topics.forEach(set(t.id,""))`) — no prefix sweep, see Progress below.
- `{{N_TOPICS}}`, `{{ROADMAP}}`, `{{HANDBOOK}}`, `{{DATA}}` are all per-track and generic.

### `_build/lesson_template.html`

- Header nav hardcodes the same two links ([:118](../../_build/lesson_template.html)). Same fix,
  same `--strict` safety net (20 warnings observed).
- `KEY = "aiem:{{TRACK}}:"` ([:146](../../_build/lesson_template.html)) — generic.
- Search markup and `data-root="../../"` ([:119-122,163-164](../../_build/lesson_template.html)) — generic.

### `_build/index_template.html`

The most edited file. Everything about it assumes two cards:

- Copy: "**Two** roadmaps for building with LLMs…" ([:43](../../_build/index_template.html)).
- The flow strip `Beginner → Advanced → Course modules` ([:46](../../_build/index_template.html)).
- Two `<article class="card">` blocks with `Track 1 · Engineers new to AI` / `Track 2 · Developers`
  ([:49-64](../../_build/index_template.html)) — the audience labels both change: Basic is
  "anyone at the company", Intermediate and Advanced are engineers.
- CSS classes `.card.b` / `.card.a` ([:20](../../_build/index_template.html)) — a third variant.
- Placeholders `{{B_SECTIONS}}`, `{{B_TOPICS}}`, `{{B_IDS}}`, `{{A_*}}` — a third set, or a data-driven
  rewrite of `build_index`.
- Hardcoded PDF hrefs `pdf/ai-engineering-on-microsoft-beginner.pdf` and `…-advanced.pdf`
  ([:55,63](../../_build/index_template.html)).
- The inline progress script ([:74-82](../../_build/index_template.html)): `var B={{B_IDS}}, A={{A_IDS}};`
  and element ids `b-done`/`b-bar`/`a-done`/`a-bar`. Hand-unrolled for two; needs a loop.
- The grid is `repeat(auto-fit, minmax(280px, 1fr))` ([:18](../../_build/index_template.html)), so three
  cards lay out without a CSS change.
- **The home page has no search box** (verified: zero `class="search"` in the built `index.html`).
  Worth adding when the corpus triples — it is the page readers land on from OneDrive.

### `_build/search.js`

**No change needed for three tracks.** It reads `window.SEARCH_INDEX`, populated by a plain
`<script src="assets/search-index.js">` ([`course.py:343-345`](../../_build/course.py),
`lesson_template.html:163`, `template.html:315`) — no `fetch`, so `file://` is fine and stays fine.
The index is flat: entries carry `u` (a path relative to the dist root) and `s` (`"<SECTION> · <title>"`),
resolved against each page's `data-root`. Nothing is keyed by track.

Two observations, neither blocking:

- **Size.** Today: 214 KB, 214 entries (194 `roadmap`, 17 `lesson`, 2 `module`, 1 `scenario`);
  lesson extracts average 6.9 KB, capped at 12 KB ([`course.py:330`](../../_build/course.py)). Once
  ~211 lessons exist, roadmap-only entries convert to lesson entries and the index lands around
  **1.5 MB** (worst case ~2.5 MB at the cap) — parsed on **every** page load, with `search.js:7-9`
  building a second lowercased copy of every field in memory. Search is a linear scan with
  `indexOf` per term per keystroke. This is the map's already-open "search over `file://` at several
  hundred pages" risk; three tiers do not change it, but these are the numbers to plan against. If it
  needs cutting: lower the 12 KB cap, or drop `x` for `roadmap`-kind entries.
- **Tier is invisible in results.** The `k` field is the page kind (`lesson`/`module`/`roadmap`/
  `scenario`) and `s` is the section. With three stacking tiers, a Basic reader searching "agent" gets
  Advanced hits with nothing marking them as out of tier. Adding the track to the index entry and
  rendering it as a badge is a small change in `course.build` ([:329,335](../../_build/course.py)) and
  `search.js:42`. Recommended, not required.

### `_build/check_links.py`

Takes file names on the command line ([:31-38](../../_build/check_links.py)) and writes
`link-report-<stem>.tsv`. **Fully generic** — it just needs the new invocation:
`python check_links.py basic.md intermediate.md advanced.md`.

One catch tied to Surprise 3: if internal back-links are expressed as resource lines
(`- doc | … | basic.html#…`), `check_links.py` will try to HTTP-fetch them and report them as errors.
Its `links()` regex ([:26-29](../../_build/check_links.py)) would need to skip non-`http` targets.

### `_build/README.md`

Documentation-only, but every line of it is two-track:

- The `check_links.py beginner.md advanced.md` invocation ([:5](../../_build/README.md)).
- The "Where content lives" table ([:18-19](../../_build/README.md)): "`_source/beginner.md`,
  `_source/advanced.md`" and "shared by both tracks".
- The progress-key line ([:54](../../_build/README.md)): *"Progress is stored … under
  `aiem:<track>:<topic-id>` … so keep topic ids stable"* — that instruction is about to be violated
  wholesale; the README should say what the re-cut does to existing progress.
- If `--strict` is split (Blocker 1), the usage block ([:8](../../_build/README.md)) changes too.

---

## Progress keys: the re-cut orphans every reader's progress

The key is `aiem:<track>:<SECTION>-<slug>`, written in two places — `template.html:216` (the roadmap
drawer) and `lesson_template.html:146` (the lesson status select) — where `<track>` is the roadmap
file's frontmatter `id` and `<SECTION>-<slug>` is the topic id minted at
[`build.py:67`](../../_build/build.py). Example today: `aiem:beginner:B1-tokens`.

The re-cut orphans progress **twice over**:

1. **The track rename alone orphans all 93 Beginner keys**, even for topics whose section and slug are
   unchanged, because `beginner` → `basic` changes every key's middle segment.
2. **Every topic that moves tier changes its section id too** (`B7-mcp` → some `I*-mcp`), so its key
   changes again.

There is **no migration code anywhere** and no prefix sweep: the roadmap Reset button
([`template.html:280-282`](../../_build/template.html)) iterates only the *current* roadmap's topic
ids, so stale `aiem:beginner:*` and `aiem:advanced:A*` entries persist in readers' browsers
indefinitely as invisible garbage. The index page's progress bars count only ids the build knows about
([`index_template.html:76`](../../_build/index_template.html)), so orphaned keys read as "0 done" —
the failure is silent and looks like lost work, not like an error.

**Options, cheapest first:**

- **Accept it.** The course shipped days ago (first roadmap commit `46961c1`, pilot lessons `d1906f4`
  and `58709f2`); real accumulated progress is probably near zero. Say so in a release note.
- **One-shot migration shim** in `template.html`'s IIFE: on load, if `aiem:migrated` is unset, walk
  `localStorage`, map each old `aiem:<old-track>:<old-id>` to its new key via a build-generated table,
  delete the old ones, set the flag. Needs a `{{MIGRATION}}` map emitted by `build_track` — perhaps 25
  lines total. Only worth it if someone has real progress.
- **Drop the track from the key** (`aiem:<topic-id>`) so future re-cuts only lose topics that actually
  move. Changes both templates and `index_template.html:76`. Cheap to do now, impossible to do
  retroactively later — **decide it in this effort, not after**.

The third is worth taking on its own merits: with three stacking tiers and "nothing is taught twice",
a topic id is already globally unique, so the track segment carries no information and only creates
this exact failure mode.

---

## Things that need no change

Confirmed generic by reading and by the three-track experiment:

- `build.parse`, `build.blocks`, `build.node`, `build.roadmap_html`, `build.handbook_html` — pure
  per-file functions; the three-track run rendered all three roadmaps correctly before `build_index` died.
- `course.render`, `course.front_matter`, `course.markdown`, callouts, Mermaid, and the volatile-block
  staleness check (`STALE_MONTHS = 6`, [`course.py:20,66-83`](../../_build/course.py)) — content-level
  and track-blind. Stale volatile blocks behave identically at three tracks; the only interaction is
  Blocker 1's `--strict` gate, which fails the build on them *and* on missing lessons together.
- `course.has_course`, `course.page_href`, `course.write_page`, `course.git_sha`, `course.plain`,
  `course.slug`.
- `build.find_browser` / `build.pdf` — already per-track.
- `_source/course/<SECTION>/<topic-id>.md` **as a convention needs no change**: `discover` derives the
  directory from the section id, whatever it is ([`course.py:118-124`](../../_build/course.py)). The
  constraints on *new* section ids are only: globally unique across all three tiers, and no hyphen.
- The lesson rename cost of the re-cut is **guarded**: `discover` raises a hard `error` (which fails
  even a non-strict build) for a `_source/course/<dir>` with no matching roadmap section, and for a
  `.md` file with no matching topic id ([`course.py:130-136`](../../_build/course.py)). So
  `_source/course/B1/` and `_source/course/B7/` must be renamed in lockstep with the new section ids,
  and the build will say so loudly if they are not.

## Method

Every line reference is to the file as of commit `f146bd7`. Behavioural claims marked "experiment"
come from copying `_build/` and `_source/` to a scratch directory, renaming `beginner.md` to
`basic.md` (frontmatter `id: basic`), adding a minimal `intermediate.md` with sections `I0`/`I1`, and
running `build.py` with `--out` and `--strict`. Index sizes and counts come from parsing the built
`dist/assets/search-index.js`. Dead-placeholder claims (`{{OTHER}}`, `{{OTHER_LABEL}}`,
`{{TRACK_LABEL}}`, the missing home-page search box) come from grepping the templates and the built
output for zero matches.
