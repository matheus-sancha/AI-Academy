"""Course lessons, overview pages, the scenario page and the search index (called from build.py).

Source layout (see docs/course-design.md):
    _source/course/<MODULE>/overview.md       optional module overview (outcomes, prerequisites)
    _source/course/<MODULE>/<topic>.md        lesson body; file name = roadmap topic id, title/links come from the roadmap
    _source/course/<MODULE>/<topic>.pt-BR.md  optional translation (may start with front matter "title: ...")

Markdown extras:
    > [!NOTE] / [!TIP] / [!IMPORTANT] / [!WARNING] / [!CAUTION]   callouts (GitHub syntax)
    ```mermaid                                                       diagrams
    {{topic:<id>}}  {{module:<id>}}     a link to that topic or module, showing its current title. Resolved against
                                        the roadmaps, so a target with no lesson yet links to its roadmap entry.
                                        Not expanded inside code. An unknown id is a build error.
    {{skills-version}}  {{skills-release-url}}   the copilot-studio-skills release the course is pinned to (front
                                        matter `skills_pin` in one roadmap). Expanded everywhere, code included.

Maintenance markers. Dated YYYY-MM; each warns once it is older than STALE_MONTHS:
    <!-- volatile verified=YYYY-MM --> ... <!-- /volatile -->   hidden: click-paths and UI that move
    <!-- verified tenant=YYYY-MM --> ... <!-- /verified -->     hidden: a claim checked in a live tenant
    <!-- unknown since=YYYY-MM --> ... <!-- /unknown -->        SHOWN as a "Not yet verified" callout and listed in the
                                                                build report. Each tag on a line of its own; no nesting.
"""
import datetime, html, json, re, shutil, subprocess
from pathlib import Path
from markdown_it import MarkdownIt

LANGS = {"en": "", "pt-BR": ".pt-BR"}  # language -> file suffix
PAGES = ("overview",)  # reserved file names that are not lessons
SCENARIO_HREF = "course/scenario/index.html"  # the running scenario, shared by every level
STALE_MONTHS = 6
SKILLS_REPO = "matheus-sancha/copilot-studio-skills"  # the toolchain Intermediate's guided build hands off to
SKILLS_RELEASE = "https://github.com/{repo}/releases/tag/{tag}"
UI = {
    "en": {"deeper": "Go deeper", "prev": "Previous", "next": "Next", "overview": "Module overview",
           "soon": "soon", "onpage": "On this page", "search": "Search the academy…",
           "status": ["Pending", "In progress", "Done", "Skip"], "opt": "Optional", "prev_feat": "Preview feature",
           "lessons": "Lessons", "build": "Built", "roadmap": "roadmap", "home": "Home", "scenario": "Scenario",
           "modules": "Modules with lessons"},
    "pt-BR": {"deeper": "Para se aprofundar", "prev": "Anterior", "next": "Próximo", "overview": "Visão geral do módulo",
              "soon": "em breve", "onpage": "Nesta página",
              "search": "Pesquisar na academia…", "status": ["Pendente", "Em andamento", "Concluído", "Pular"],
              "opt": "Opcional", "prev_feat": "Recurso em preview", "lessons": "Lições",
              "build": "Gerado em", "roadmap": "roadmap", "home": "Início", "scenario": "Cenário",
              "modules": "Módulos com lições"},
}
CALLOUT = {"NOTE": "Note", "TIP": "Tip", "IMPORTANT": "Important", "WARNING": "Warning", "CAUTION": "Caution",
           "UNKNOWN": "Not yet verified"}
TYPE_LABEL = {"doc": "Docs", "video": "Video", "article": "Article", "course": "Course"}
MARKER = re.compile(r"<!--\s*(/?)(volatile|verified|unknown)(?:\s+(\w+)=(\S+))?\s*-->")
MARKER_DATE = {"volatile": "verified", "verified": "tenant", "unknown": "since"}  # the date attribute each one needs
MERMAID_TAG = ('<script src="https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"></script>'
               '<script>mermaid.initialize({startOnLoad:true});</script>')
BUILD_DIR = Path(__file__).resolve().parent


class Report:
    """Errors fail the build; warnings fail only --strict; missing lessons and open unknowns are counted, never fail."""
    def __init__(self): self.warnings, self.errors, self.missing, self.unknowns = [], [], [], []
    def warn(self, msg): self.warnings.append(msg)
    def error(self, msg): self.errors.append(msg)


def label(level):
    """The reader-facing name of a level: its roadmap id, capitalised."""
    return level.capitalize()


def level_nav(levels, prefix=""):
    return "".join(f'<a href="{prefix}{lvl}.html">{label(lvl)}</a>' for lvl in levels)


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def markdown():
    md = MarkdownIt("commonmark", {"html": True}).enable(["table", "strikethrough"])
    fence = md.renderer.rules["fence"]
    def render_fence(renderer, tokens, i, options, env):
        if tokens[i].info.strip() == "mermaid":
            env["mermaid"] = True
            return f'<pre class="mermaid">{html.escape(tokens[i].content)}</pre>\n'
        return fence(tokens, i, options, env)
    md.add_render_rule("fence", render_fence)
    return md

MD = markdown()


def markers(text, where, report):
    """Check the maintenance markers, strip the hidden ones and turn each unknown block into a callout."""
    today, stack, out = datetime.date.today(), [], []
    for n, line in enumerate(text.splitlines(), 1):
        found = list(MARKER.finditer(line))
        for m in found:
            close, kind, attr, value = m[1], m[2], m[3], m[4]
            if kind == "unknown" and line.strip() != m[0]:
                report.error(f"{where}:{n}: <!-- {close}unknown --> must be on a line of its own")
            if close:
                if stack and stack[-1] == kind: stack.pop()
                else: report.error(f"{where}:{n}: <!-- /{kind} --> without a matching opening tag")
                continue
            if kind == "unknown" and "unknown" in stack:
                report.error(f"{where}:{n}: unknown blocks cannot nest")
            stack.append(kind)
            want = MARKER_DATE[kind]
            try:
                if attr != want: raise ValueError
                y, mo = map(int, value.split("-"))
            except (ValueError, AttributeError):
                report.error(f"{where}:{n}: {kind} tag needs {want}=YYYY-MM"); continue
            if kind == "unknown": report.unknowns.append((value, f"{where}:{n}"))
            if (today.year - y) * 12 + today.month - mo > STALE_MONTHS:
                report.warn(f"{where}:{n}: {kind} block {want} {value} is older than {STALE_MONTHS} months")
        if any(m[2] == "unknown" and not m[1] for m in found):
            out.append("> [!UNKNOWN]")
        elif any(m[2] == "unknown" and m[1] for m in found):
            out.append("")  # ends the callout's blockquote
        elif "unknown" in stack:
            out.append("> " + MARKER.sub("", line))
        else:
            out.append(MARKER.sub("", line))
    for kind in stack:
        report.error(f"{where}: unclosed <!-- {kind} --> block")
    return "\n".join(out)


def render(text, where, report, refs=None):
    """Markdown -> (html, headings, uses_mermaid). Expands {{...}} macros when given refs, and applies markers()."""
    if refs: text = refs.expand_values(text, where, report)
    text = markers(text, where, report)

    env = {}
    tokens = MD.parse(text, env)
    headings, used = [], set()
    for i, tok in enumerate(tokens):
        if tok.type == "heading_open" and tok.tag in ("h2", "h3"):
            title = refs.plain_titles(tokens[i + 1].content) if refs else tokens[i + 1].content
            hid = base = slug(title) or "section"
            k = 2
            while hid in used: hid, k = f"{base}-{k}", k + 1
            used.add(hid); tok.attrSet("id", hid)
            if tok.tag == "h2": headings.append((hid, title))
    out = MD.renderer.render(tokens, MD.options, env)
    out = re.sub(r"<blockquote>\s*<p>\[!(" + "|".join(CALLOUT) + r")\]\s*",
                 lambda m: f'<blockquote class="callout {m[1].lower()}"><p><strong class="callout-title">{CALLOUT[m[1]]}</strong><br>',
                 out)
    if refs: out = refs.expand_links(out, where, report)
    return out, headings, bool(env.get("mermaid"))


class Refs:
    """Resolves the {{...}} macros in lesson prose against the parsed roadmaps. Built after discover()."""
    MACRO = re.compile(r"\{\{([a-z][a-z-]*)(?::([^{}\s]+))?\}\}")
    CODE = re.compile(r"(<pre\b[\s\S]*?</pre>|<code\b[\s\S]*?</code>)")

    def __init__(self, levels, metas):
        self.topics = {t["id"]: (lvl, t) for lvl, secs in levels.items() for s in secs for t in s["topics"] if not t["assumed"]}
        self.modules = {s["id"]: (lvl, s) for lvl, secs in levels.items() for s in secs}
        self.pins = {m["skills_pin"] for m in metas.values() if m.get("skills_pin")}
        self.pin = next(iter(self.pins)) if len(self.pins) == 1 else None

    def target(self, kind, ref):
        """(title, root-relative href) for a topic or module id, or None if there is no such thing."""
        if kind == "topic" and ref in self.topics:
            lvl, t = self.topics[ref]
            return t["title"], lesson_href(t) if "en" in t["sources"] else f"{lvl}.html#{ref}"
        if kind == "module" and ref in self.modules:
            lvl, s = self.modules[ref]
            return s["title"], f"course/{ref}/index.html" if has_course(s) else f"{lvl}.html#{ref}"
        return None

    def expand_values(self, text, where, report):
        """Before markdown: the pinned-version macros, which may sit inside a URL or a code block."""
        def sub(m):
            if m[1] not in ("skills-version", "skills-release-url") or m[2] is not None:
                return m[0]  # a link macro: expand_links() handles it after markdown
            if not self.pin:
                if not self.pins:  # several differing pins are reported once, by validate()
                    report.error(f"{where}: {m[0]} is used, but no roadmap declares skills_pin")
                return m[0]
            return self.pin if m[1] == "skills-version" else SKILLS_RELEASE.format(repo=SKILLS_REPO, tag=self.pin)
        return self.MACRO.sub(sub, text)

    def expand_links(self, markup, where, report):
        """After markdown: {{topic:}} and {{module:}} become links. Code is left alone, so the syntax can be shown."""
        def sub(m):
            if m[1] in ("topic", "module") and m[2]:
                if hit := self.target(m[1], m[2]):
                    return f'<a class="xref" href="../../{hit[1]}">{html.escape(hit[0])}</a>'
                report.error(f"{where}: {m[0]} names no {m[1]} in any roadmap")
            elif m[1] not in ("skills-version", "skills-release-url"):  # left unexpanded only when already reported
                report.error(f"{where}: unknown macro {m[0]}")
            return m[0]
        parts = self.CODE.split(markup)
        return "".join(p if i % 2 else self.MACRO.sub(sub, p) for i, p in enumerate(parts))

    def plain_titles(self, text):
        """A heading's text with its link macros reduced to the target's title, for the TOC and the anchor."""
        return self.MACRO.sub(lambda m: (self.target(m[1], m[2]) or (m[0],))[0], text)


def front_matter(text):
    if m := re.match(r"---\n(.*?)\n---\n(.*)", text, re.S):
        return dict(l.split(": ", 1) for l in m[1].splitlines() if ": " in l), m[2]
    return {}, text


def plain(markup):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", markup))).strip()


def validate(levels, metas, report):
    """The roadmap invariants (docs/course-design.md), checked on the parsed model before any lesson is read.

    levels is ordered lowest first. Module ids and real topic ids are each globally unique; an `assumed` topic
    reuses the id of a real topic taught in a lower level, which is how it resolves with no target written."""
    order, modules, real = list(levels), {}, {}
    for lvl, secs in levels.items():
        for s in secs:
            if s["id"] in modules:
                report.error(f"module id '{s['id']}' is used in both {modules[s['id']]} and {lvl}")
            modules.setdefault(s["id"], lvl)
            for t in s["topics"]:
                if t["id"] in PAGES:
                    report.error(f"{lvl}/{s['id']}: topic id '{t['id']}' collides with a reserved course page name")
                if t["assumed"]: continue
                if t["id"] in real:
                    report.error(f"topic id '{t['id']}' is used in both {real[t['id']][1]} and {lvl}/{s['id']}")
                real.setdefault(t["id"], (lvl, f"{lvl}/{s['id']}"))
    for lvl, secs in levels.items():
        seen = {}  # one roadmap page: every module and topic id there is an HTML id and a drawer key
        for s in secs:
            for kind, ref in [("module", s["id"])] + [("assumed" if t["assumed"] else "topic", t["id"]) for t in s["topics"]]:
                # module/module and topic/topic are caught globally above, topic/assumed by the level check below
                if ref in seen and ({kind, seen[ref]} in ({"module", "topic"}, {"module", "assumed"})
                                    or kind == seen[ref] == "assumed"):
                    report.error(f"{lvl}: id '{ref}' is used twice on one roadmap page ({seen[ref]} and {kind})")
                seen.setdefault(ref, kind)
            for t in s["topics"]:
                if not t["assumed"]: continue
                if t["id"] not in real:
                    report.error(f"{lvl}/{s['id']}: assumed topic '{t['id']}' is not taught in any level")
                elif order.index(real[t["id"]][0]) >= order.index(lvl):
                    report.error(f"{lvl}/{s['id']}: assumed topic '{t['id']}' is taught in {real[t['id']][0]}, "
                                 f"which is not below {lvl}")
    pins = {lvl: m["skills_pin"] for lvl, m in metas.items() if m.get("skills_pin")}
    if len(set(pins.values())) > 1:
        report.error(f"skills_pin differs between roadmaps: {pins}")
    if order and metas[order[-1]].get("continues") == "yes":
        report.error(f"{order[-1]}: 'continues: yes' on the last level, which has nothing to continue into")


def discover(levels, root, report):
    """Attach course pages to roadmap modules/topics and validate the source tree."""
    course_dir = root / "_source" / "course"
    sections = {}
    # Walk every module, not a dict keyed by id: a duplicate id is validate()'s error to report, not a crash here.
    for lvl, s in ((lvl, s) for lvl, secs in levels.items() for s in secs):
        sections.setdefault(s["id"], (lvl, s))
        s["level"], s_id = lvl, s["id"]
        sdir = course_dir / s_id
        s["overview"] = sdir / "overview.md" if (sdir / "overview.md").exists() else None
        for t in s["topics"]:
            t["sources"] = {} if t["assumed"] else {lang: sdir / f"{t['id']}{suf}.md" for lang, suf in LANGS.items()
                                                    if (sdir / f"{t['id']}{suf}.md").exists()}
            if t["assumed"]: continue  # a pointer to a lower level, never a page
            if t["sources"] and "en" not in t["sources"]:
                report.error(f"{s_id}/{t['id']}: translation without the English lesson")
            elif not t["sources"]:
                report.missing.append(f"{s_id}/{t['id']}")
    for sdir in sorted(p for p in course_dir.glob("*") if p.is_dir()):
        if sdir.name not in sections:
            report.error(f"_source/course/{sdir.name}: no roadmap module with that id"); continue
        s = sections[sdir.name][1]
        known = {f"{t['id']}{suf}.md" for t in s["topics"] if not t["assumed"] for suf in LANGS.values()}
        for f in sorted(sdir.glob("*.md")):
            if f.name != "overview.md" and f.name not in known:
                report.error(f"_source/course/{sdir.name}/{f.name}: orphan lesson (no topic with that id in module {sdir.name})")
    link_assumed(levels)


def link_assumed(levels):
    """Point each assumed topic at the real one: its lesson if written, else its node on the lower level's roadmap."""
    real = {t["id"]: (lvl, t) for lvl, secs in levels.items() for s in secs for t in s["topics"] if not t["assumed"]}
    for secs in levels.values():
        for s in secs:
            for t in s["topics"]:
                if t["assumed"] and t["id"] in real:
                    lvl, target = real[t["id"]]
                    t["taught"] = lvl
                    t["target"] = lesson_href(target) if "en" in target["sources"] else f"{lvl}.html#{t['id']}"


def lesson_href(t, lang="en"):
    return f"course/{t['module']}/{t['id']}{LANGS[lang]}.html"


def sequence(sections):
    """Reading order within a level: module overview -> lessons, module by module."""
    pages = []
    for s in sections:
        if not has_course(s): continue
        pages.append(("overview", s, None))
        pages += [("lesson", s, t) for t in s["topics"] if t["sources"]]
    return pages


def has_course(s):
    return bool(s["overview"] or any(t["sources"] for t in s["topics"]))


def page_href(page):
    kind, s, t = page
    base = f"course/{s['id']}/"
    return base + ("index.html" if kind == "overview" else f"{t['id']}.html")


def page_title(page, lang="en"):
    kind, s, t = page
    return f"{s['id']} · {UI[lang]['overview']}" if kind == "overview" else t["title"]


def sidebar(s, active, lang):
    ui, items = UI[lang], []
    def item(href, label, cls="", data_id=""):
        cur = ' aria-current="page"' if href == active else ""
        did = f' data-id="{data_id}"' if data_id else ""
        return f'<li><a class="{cls}" href="../../{href}"{cur}{did}>{label}</a></li>'
    items.append(item(f"course/{s['id']}/index.html", ui["overview"], "overview"))
    for t in s["topics"]:
        name = html.escape(t["title"])
        if t.get("target"):
            items.append(item(t["target"], f'{name} <em>{label(t["taught"])}</em>', "lesson assumed", t["id"]))
        elif t["sources"]:
            items.append(item(lesson_href(t), name, "lesson" + (" opt" if t["opt"] else ""), t["id"]))
        else:
            items.append(f'<li><span class="soon">{name} <em>{ui["soon"]}</em></span></li>')
    return (f'<div class="side-kicker">{s["id"]}</div><div class="side-title">{html.escape(s["title"])}</div>'
            f'<ul class="side-list">{"".join(items)}</ul>')


def scenario_sidebar(levels, lang="en"):
    """The scenario page sits outside the modules, so its sidebar lists the modules instead, grouped by level."""
    ui, groups = UI[lang], []
    for lvl, sections in levels.items():
        items = [f'<li><a href="../../course/{s["id"]}/index.html">{s["id"]} · {html.escape(s["title"])}</a></li>'
                 for s in sections if has_course(s)]
        if items:
            groups.append(f'<div class="side-kicker">{label(lvl)}</div><ul class="side-list">{"".join(items)}</ul>')
    return f'<div class="side-kicker">{ui["scenario"]}</div><div class="side-title">Technik</div>' + "".join(groups)


def crumbs(*parts):
    """parts: (href, label) for a link, or (None, label) for the current page."""
    out = []
    for href, label in parts:
        if out:
            out.append("<span>›</span>")
        out.append(f'<a href="{href}">{label}</a>' if href else f"<span>{label}</span>")
    return "".join(out)


def check_internal_links(out, report, want_pdf):
    """Every relative link in a built page must point at a file that exists.

    Only <a href> targets are checked, and only ones that look like paths a browser would follow:
    the roadmap pages carry inline JavaScript that builds hrefs at runtime, and those are skipped.
    """
    href = re.compile(r'<a\b[^>]*?\bhref="([^"\'+]+?)"', re.I)
    for page in sorted(out.rglob("*.html")):
        for link in href.findall(page.read_text(encoding="utf-8")):
            target = link.split("#")[0].split("?")[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "javascript:", "/")):
                continue
            if target.startswith("pdf/") and not want_pdf:
                continue  # built only with --pdf
            if not (page.parent / target).resolve().exists():
                report.warn(f"{page.relative_to(out).as_posix()}: broken link to {link}")


def build_scenario(levels, refs, root, out, template, stamp, report):
    """Render _source/course/scenario.md at course/scenario/index.html. Returns its index entry."""
    src = root / "_source" / "course" / "scenario.md"
    if not src.exists():
        return None
    ui = UI["en"]
    body = src.read_text(encoding="utf-8")
    title = ui["scenario"]
    if m := re.match(r"#\s+(.+)\n", body):  # the H1 becomes the page title
        title, body = m[1].strip(), body[m.end():]
    content, headings, mermaid = render(body, src.relative_to(root).as_posix(), report, refs)
    toc = "".join(f'<li><a href="#{hid}">{html.escape(h)}</a></li>' for hid, h in headings)
    write_page(out, SCENARIO_HREF, template,
        LANG="en", TITLE=html.escape(title), LEVEL_NAV=level_nav(levels, "../../"),
        CRUMBS=crumbs(("../../index.html", ui["home"]), (None, ui["scenario"])),
        PILLS="", SWITCH="", STATUS="", CONTENT=content, DEEPER="",
        SIDEBAR=scenario_sidebar(levels), TOC=f'<div class="toc-title">{ui["onpage"]}</div><ul>{toc}</ul>' if toc else "",
        PREV="<span></span>", NEXT="<span></span>", SEARCH_PLACEHOLDER=ui["search"], STAMP=f'{ui["build"]} {stamp}',
        MERMAID=MERMAID_TAG if mermaid else "")
    return {"t": title, "s": ui["scenario"], "u": SCENARIO_HREF, "k": "scenario", "x": plain(content)[:12000]}


def write_page(out, rel, template, **v):
    page = re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: v.get(m[1], m[0]), template)  # one pass: content may contain {{...}}
    target = out / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page, encoding="utf-8")


def git_sha(root):
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=root, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def build(levels, metas, root, out, report):
    """Render every course page and write the search index. Returns pages built.

    levels is ordered lowest first. Prev/Next stay inside a level, except that a level whose front matter says
    `continues: yes` hands its last page on to the next level's roadmap, where that level's assumed knowledge sits."""
    template = (BUILD_DIR / "lesson_template.html").read_text(encoding="utf-8")
    stamp = f"{datetime.date.today().isoformat()}" + (f" · {git_sha(root)}" if git_sha(root) else "")
    refs, order, nav = Refs(levels, metas), list(levels), level_nav(levels, "../../")
    index, built = [], 0
    for i, (lvl, sections) in enumerate(levels.items()):
        seq = sequence(sections)
        onward = order[i + 1] if metas[lvl].get("continues") == "yes" and i + 1 < len(order) else None
        for n, page in enumerate(seq):
            kind, s, t = page
            prev_p, next_p = (seq[n - 1] if n else None), (seq[n + 1] if n + 1 < len(seq) else None)
            langs = t["sources"] if kind == "lesson" else {"en": None}
            for lang in langs:
                ui = UI[lang]
                href = page_href(page) if lang == "en" else lesson_href(t, lang)
                title, pills, deeper, toc_extra, status_id = page_title(page), "", "", "", ""
                if kind == "lesson":
                    meta, body = front_matter(langs[lang].read_text(encoding="utf-8"))
                    title = meta.get("title", t["title"])
                    where = langs[lang].relative_to(root).as_posix()
                    if lang == "en" and not t["opt"] and not re.search(r"^## TL;DR", body, re.M):
                        report.warn(f"{where}: full lesson should start with '## TL;DR'")
                    pills = ((f'<span class="pill opt">{ui["opt"]}</span>' if t["opt"] else "") +
                             (f'<span class="pill prev">{ui["prev_feat"]}</span>' if t["prev"] else ""))
                    if t["links"]:
                        deeper = (f'<section class="deeper"><h2 id="go-deeper">{ui["deeper"]}</h2><ul>' + "".join(
                            f'<li><a href="{html.escape(l["url"])}" target="_blank" rel="noopener">'
                            f'<span class="pill {l["type"]}">{TYPE_LABEL[l["type"]]}</span>{html.escape(l["label"])}</a></li>'
                            for l in t["links"]) + "</ul></section>")
                        toc_extra = f'<li><a href="#go-deeper">{ui["deeper"]}</a></li>'
                    status_id = t["id"]
                else:
                    body = s["overview"].read_text(encoding="utf-8") if s["overview"] else ""
                    where = s["overview"].relative_to(root).as_posix() if s["overview"] else f"{s['id']} intro"
                    title = s["title"]
                    body = f"{s['intro']}\n\n{body}"
                content, headings, mermaid = render(body, where, report, refs)
                if kind == "overview":
                    content += (f'<h2 id="lessons">{ui["lessons"]}</h2><ol class="module-lessons">' + "".join(
                        module_item(x, ui) for x in s["topics"]) + "</ol>")
                    headings.append(("lessons", ui["lessons"]))
                toc = "".join(f'<li><a href="#{hid}">{html.escape(h)}</a></li>' for hid, h in headings) + toc_extra
                switch = ""
                if kind == "lesson" and len(langs) > 1:
                    current = ' aria-current="page"'
                    switch = '<nav class="lang">' + "".join(
                        f'<a href="../../{lesson_href(t, l)}"{current if l == lang else ""}>{"EN" if l == "en" else l}</a>'
                        for l in langs) + "</nav>"
                status = ""
                if status_id:
                    status = (f'<select id="status" data-id="{status_id}" aria-label="Status">' + "".join(
                        f'<option value="{v}">{name}</option>' for v, name in zip(("", "progress", "done", "skip"), ui["status"])) + "</select>")
                def nav_link(p, cls, text):
                    return (f'<a class="btn {cls}" href="../../{page_href(p)}"><small>{text}</small>{html.escape(page_title(p))}</a>'
                            if p else "<span></span>")
                if next_p or not onward:
                    nxt = nav_link(next_p, "next", ui["next"] + " →")
                else:  # the last page of a level that continues: on to the next level's roadmap
                    nxt = (f'<a class="btn next seam" href="../../{onward}.html"><small>{ui["next"]} →</small>'
                           f'{html.escape(metas[onward].get("subtitle", label(onward)))}</a>')
                write_page(out, href, template,
                    LANG=lang, TITLE=html.escape(title), LEVEL_NAV=nav,
                    CRUMBS=crumbs((f"../../{lvl}.html", label(lvl)),
                                  (f"../../course/{s['id']}/index.html", f'{s["id"]} · {html.escape(s["title"])}'),
                                  (f"../../{lvl}.html#{status_id or s['id']}", f"{label(lvl)} roadmap ↗")),
                    PILLS=pills, SWITCH=switch, STATUS=status,
                    CONTENT=content, DEEPER=deeper, SIDEBAR=sidebar(s, page_href(page), lang),
                    TOC=(f'<div class="toc-title">{ui["onpage"]}</div><ul>{toc}</ul>' if toc else ""),
                    PREV=nav_link(prev_p, "prev", "← " + ui["prev"]), NEXT=nxt,
                    SEARCH_PLACEHOLDER=ui["search"], STAMP=f'{ui["build"]} {stamp}',
                    MERMAID=MERMAID_TAG if mermaid else "")
                index.append({"t": title, "s": f"{s['id']} · {s['title']}", "l": label(lvl), "u": href,
                              "k": kind if lang == "en" else f"{kind} · {lang}", "x": plain(content)[:12000]})
                built += 1
        for s in sections:
            for t in s["topics"]:
                if not t["sources"] and not t["assumed"]:
                    index.append({"t": t["title"], "s": f"{s['id']} · {s['title']}", "l": label(lvl),
                                  "u": f"{lvl}.html#{t['id']}", "k": "roadmap", "x": plain(t["html"])})
    if entry := build_scenario(levels, refs, root, out, template, stamp, report):
        index.append(entry)
        built += 1

    assets = out / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "search-index.js").write_text(
        "window.SEARCH_INDEX=" + json.dumps(index, ensure_ascii=False, separators=(",", ":")) + ";", encoding="utf-8")
    for name in ("search.js", "progress.js"):
        shutil.copyfile(BUILD_DIR / name, assets / name)
    return built


def module_item(t, ui):
    """One entry in an overview page's lesson list: the lesson, where an assumed topic is taught, or 'soon'."""
    name = html.escape(t["title"])
    if t.get("target"):
        return f'<li class="assumed"><a href="../../{t["target"]}" data-id="{t["id"]}">{name}</a> <em>{label(t["taught"])}</em></li>'
    if t["sources"]:
        return f'<li><a href="../../{lesson_href(t)}" data-id="{t["id"]}">{name}</a></li>'
    return f'<li class="soon">{name} <em>{ui["soon"]}</em></li>'
