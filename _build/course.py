"""Course lessons, module pages, the scenario page and the search index (called from build.py).

Source layout (see docs/course-design.md):
    _source/course/<SECTION>/module.md        optional module overview (outcomes, prerequisites)
    _source/course/<SECTION>/<topic>.md       lesson body; file name = roadmap topic id, title/links come from the roadmap
    _source/course/<SECTION>/<topic>.pt-BR.md optional translation (may start with front matter "title: ...")

Markdown extras:
    > [!NOTE] / [!TIP] / [!IMPORTANT] / [!WARNING] / [!CAUTION]   callouts (GitHub syntax)
    ```mermaid                                                       diagrams
    <!-- volatile verified=YYYY-MM --> ... <!-- /volatile -->        hidden maintenance tag; content shows normally
"""
import datetime, html, json, re, shutil, subprocess
from pathlib import Path
from markdown_it import MarkdownIt

LANGS = {"en": "", "pt-BR": ".pt-BR"}  # language -> file suffix
PAGES = ("module",)  # reserved file names that are not lessons
SCENARIO_HREF = "course/scenario/index.html"  # the running scenario, shared by both tracks
STALE_MONTHS = 6
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
CALLOUT = {"NOTE": "Note", "TIP": "Tip", "IMPORTANT": "Important", "WARNING": "Warning", "CAUTION": "Caution"}
TYPE_LABEL = {"doc": "Docs", "video": "Video", "article": "Article", "course": "Course"}
VOLATILE = re.compile(r"<!--\s*(/?)volatile(?:\s+verified=(\S+))?\s*-->")
MERMAID_TAG = ('<script src="https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"></script>'
               '<script>mermaid.initialize({startOnLoad:true});</script>')
BUILD_DIR = Path(__file__).resolve().parent


class Report:
    def __init__(self): self.warnings, self.errors = [], []
    def warn(self, msg): self.warnings.append(msg)
    def error(self, msg): self.errors.append(msg)


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


def render(text, where, report):
    """Markdown -> (html, headings, uses_mermaid). Strips volatile markers and reports stale or unbalanced ones."""
    depth, today = 0, datetime.date.today()
    for n, line in enumerate(text.splitlines(), 1):
        for m in VOLATILE.finditer(line):
            if m[1]:
                depth -= 1
                if depth < 0: report.error(f"{where}:{n}: <!-- /volatile --> without an opening tag")
                continue
            depth += 1
            try:
                y, mo = map(int, (m[2] or "").split("-"))
                if (today.year - y) * 12 + today.month - mo > STALE_MONTHS:
                    report.warn(f"{where}:{n}: volatile block verified {m[2]} is older than {STALE_MONTHS} months")
            except ValueError:
                report.error(f"{where}:{n}: volatile tag needs verified=YYYY-MM")
    if depth > 0: report.error(f"{where}: unclosed <!-- volatile --> block")
    text = VOLATILE.sub("", text)

    env = {}
    tokens = MD.parse(text, env)
    headings, used = [], set()
    for i, tok in enumerate(tokens):
        if tok.type == "heading_open" and tok.tag in ("h2", "h3"):
            title = tokens[i + 1].content
            hid = base = slug(title) or "section"
            k = 2
            while hid in used: hid, k = f"{base}-{k}", k + 1
            used.add(hid); tok.attrSet("id", hid)
            if tok.tag == "h2": headings.append((hid, title))
    out = MD.renderer.render(tokens, MD.options, env)
    out = re.sub(r"<blockquote>\s*<p>\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*",
                 lambda m: f'<blockquote class="callout {m[1].lower()}"><p><strong class="callout-title">{CALLOUT[m[1]]}</strong><br>',
                 out)
    return out, headings, bool(env.get("mermaid"))


def front_matter(text):
    if m := re.match(r"---\n(.*?)\n---\n(.*)", text, re.S):
        return dict(l.split(": ", 1) for l in m[1].splitlines() if ": " in l), m[2]
    return {}, text


def plain(markup):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", markup))).strip()


def discover(tracks, root, report):
    """Attach course pages to roadmap sections/topics and validate the source tree."""
    course_dir = root / "_source" / "course"
    sections = {s["id"]: (track, s) for track, secs in tracks.items() for s in secs}
    for s_id, (track, s) in sections.items():
        s["track"] = track
        sdir = course_dir / s_id
        s["module"] = sdir / "module.md" if (sdir / "module.md").exists() else None
        for t in s["topics"]:
            t["slug"] = t["id"].split("-", 1)[1]
            t["sources"] = {lang: sdir / f"{t['slug']}{suf}.md" for lang, suf in LANGS.items()
                            if (sdir / f"{t['slug']}{suf}.md").exists()}
            if t["slug"] in PAGES: report.error(f"{s_id}: topic id '{t['slug']}' collides with a reserved course page name")
            if t["sources"] and "en" not in t["sources"]:
                report.error(f"{s_id}/{t['slug']}: translation without the English lesson")
            elif not t["sources"]:
                report.warn(f"{s_id}/{t['slug']}: no lesson yet")
    known = {f"{t['slug']}{suf}.md" for _, s in sections.values() for t in s["topics"] for suf in LANGS.values()}
    for sdir in sorted(p for p in course_dir.glob("*") if p.is_dir()):
        if sdir.name not in sections:
            report.error(f"_source/course/{sdir.name}: no roadmap section with that id"); continue
        for f in sorted(sdir.glob("*.md")):
            if f.name != "module.md" and f.name not in known:
                report.error(f"_source/course/{sdir.name}/{f.name}: orphan lesson (no matching roadmap topic id)")


def lesson_href(t, lang="en"):
    return f"course/{t['id'].split('-', 1)[0]}/{t['slug']}{LANGS[lang]}.html"


def sequence(sections):
    """Reading order within a track: module overview -> lessons, section by section."""
    pages = []
    for s in sections:
        if not has_course(s): continue
        pages.append(("module", s, None))
        pages += [("lesson", s, t) for t in s["topics"] if t["sources"]]
    return pages


def has_course(s):
    return bool(s["module"] or any(t["sources"] for t in s["topics"]))


def page_href(page):
    kind, s, t = page
    base = f"course/{s['id']}/"
    return base + ("index.html" if kind == "module" else f"{t['slug']}.html")


def page_title(page, lang="en"):
    kind, s, t = page
    return f"{s['id']} · {UI[lang]['overview']}" if kind == "module" else t["title"]


def sidebar(s, active, lang):
    ui, items = UI[lang], []
    def item(href, label, cls="", data_id=""):
        cur = ' aria-current="page"' if href == active else ""
        did = f' data-id="{data_id}"' if data_id else ""
        return f'<li><a class="{cls}" href="../../{href}"{cur}{did}>{label}</a></li>'
    items.append(item(f"course/{s['id']}/index.html", ui["overview"], "overview"))
    for t in s["topics"]:
        label = html.escape(t["title"])
        if t["sources"]:
            items.append(item(lesson_href(t), label, "lesson" + (" opt" if t["opt"] else ""), t["id"]))
        else:
            items.append(f'<li><span class="soon">{label} <em>{ui["soon"]}</em></span></li>')
    return (f'<div class="side-kicker">{s["id"]}</div><div class="side-title">{html.escape(s["title"])}</div>'
            f'<ul class="side-list">{"".join(items)}</ul>')


def scenario_sidebar(tracks, lang="en"):
    """The scenario page sits outside the modules, so its sidebar lists the modules instead."""
    ui, items = UI[lang], []
    for track, sections in tracks.items():
        for s in sections:
            if has_course(s):
                items.append(f'<li><a href="../../course/{s["id"]}/index.html">'
                             f'{s["id"]} · {html.escape(s["title"])}</a></li>')
    return (f'<div class="side-kicker">{ui["scenario"]}</div>'
            f'<div class="side-title">Technik</div>'
            f'<ul class="side-list">{"".join(items) or ""}</ul>'
            if items else f'<div class="side-kicker">{ui["scenario"]}</div><div class="side-title">Technik</div>')


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


def build_scenario(tracks, root, out, template, stamp, report):
    """Render _source/course/scenario.md at course/scenario/index.html. Returns its index entry."""
    src = root / "_source" / "course" / "scenario.md"
    if not src.exists():
        return None
    ui = UI["en"]
    body = src.read_text(encoding="utf-8")
    title = ui["scenario"]
    if m := re.match(r"#\s+(.+)\n", body):  # the H1 becomes the page title
        title, body = m[1].strip(), body[m.end():]
    content, headings, mermaid = render(body, src.relative_to(root).as_posix(), report)
    toc = "".join(f'<li><a href="#{hid}">{html.escape(h)}</a></li>' for hid, h in headings)
    write_page(out, SCENARIO_HREF, template,
        LANG="en", TITLE=html.escape(title), TRACK="beginner", TRACK_LABEL="Beginner",
        CRUMBS=crumbs(("../../index.html", ui["home"]), (None, ui["scenario"])),
        PILLS="", SWITCH="", STATUS="", CONTENT=content, DEEPER="",
        SIDEBAR=scenario_sidebar(tracks), TOC=f'<div class="toc-title">{ui["onpage"]}</div><ul>{toc}</ul>' if toc else "",
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


def build(tracks, root, out, report):
    """Render every course page and write the search index. Returns pages built."""
    template = (BUILD_DIR / "lesson_template.html").read_text(encoding="utf-8")
    stamp = f"{datetime.date.today().isoformat()}" + (f" · {git_sha(root)}" if git_sha(root) else "")
    index, built = [], 0
    for track, sections in tracks.items():
        seq = sequence(sections)
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
                    body = s["module"].read_text(encoding="utf-8") if s["module"] else ""
                    where = s["module"].relative_to(root).as_posix() if s["module"] else ""
                    title = s["title"]
                    body = f"{s['intro']}\n\n{body}"
                content, headings, mermaid = render(body, where, report)
                if kind == "module":
                    content += (f'<h2 id="lessons">{ui["lessons"]}</h2><ol class="module-lessons">' + "".join(
                        (f'<li><a href="../../{lesson_href(x)}" data-id="{x["id"]}">{html.escape(x["title"])}</a></li>' if x["sources"]
                         else f'<li class="soon">{html.escape(x["title"])} <em>{ui["soon"]}</em></li>') for x in s["topics"]) + "</ol>")
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
                        f'<option value="{v}">{label}</option>' for v, label in zip(("", "progress", "done", "skip"), ui["status"])) + "</select>")
                def nav_link(p, cls, label):
                    return (f'<a class="btn {cls}" href="../../{page_href(p)}"><small>{label}</small>{html.escape(page_title(p))}</a>'
                            if p else "<span></span>")
                write_page(out, href, template,
                    LANG=lang, TITLE=html.escape(title), TRACK=track, TRACK_LABEL=track.capitalize(),
                    CRUMBS=crumbs((f"../../{track}.html", track.capitalize()),
                                  (f"../../course/{s['id']}/index.html", f'{s["id"]} · {html.escape(s["title"])}'),
                                  (f"../../{track}.html#{status_id or s['id']}", f"{track.capitalize()} roadmap ↗")),
                    PILLS=pills, SWITCH=switch, STATUS=status,
                    CONTENT=content, DEEPER=deeper, SIDEBAR=sidebar(s, page_href(page), lang),
                    TOC=(f'<div class="toc-title">{ui["onpage"]}</div><ul>{toc}</ul>' if toc else ""),
                    PREV=nav_link(prev_p, "prev", "← " + ui["prev"]), NEXT=nav_link(next_p, "next", ui["next"] + " →"),
                    SEARCH_PLACEHOLDER=ui["search"], STAMP=f'{ui["build"]} {stamp}',
                    MERMAID=MERMAID_TAG if mermaid else "")
                index.append({"t": title, "s": f"{s['id']} · {s['title']}", "u": href, "k": kind if lang == "en" else f"{kind} · {lang}",
                              "x": plain(content)[:12000]})
                built += 1
        for s in sections:
            for t in s["topics"]:
                if not t["sources"]:
                    index.append({"t": t["title"], "s": f"{s['id']} · {s['title']}", "u": f"{track}.html#{t['id']}",
                                  "k": "roadmap", "x": plain(t["html"])})
    if entry := build_scenario(tracks, root, out, template, stamp, report):
        index.append(entry)
        built += 1

    assets = out / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "search-index.js").write_text(
        "window.SEARCH_INDEX=" + json.dumps(index, ensure_ascii=False, separators=(",", ":")) + ";", encoding="utf-8")
    shutil.copyfile(BUILD_DIR / "search.js", assets / "search.js")
    return built
