"""Build the roadmap pages, course pages and PDFs from _source/.

    python build.py            # HTML only
    python build.py --pdf      # HTML + PDFs (needs Microsoft Edge or Chrome)
    python build.py --strict   # release build: fail on any warning (stale markers, broken links, ...)
    python build.py --missing  # also list every topic that has no lesson yet (always counted, never a failure)

Output goes to --out DIR, else $AI_ACADEMY_OUT, else dist/ (gitignored).

Source format — one file per level, _source/<level>.md (see _source/beginner.md):
    ---  front matter  ---
        id, order          the level's id (its page is <id>.html) and its place in the course, lowest first
        title, subtitle, tagline, next, next_label
        audience, card     optional: the tag and the description on the home page's card for this level
        continues: yes     optional: the last lesson's Next leads on to the next level's roadmap
        skills_pin: vX.Y.Z optional, in one level only: the copilot-studio-skills release the course is written against
    # <module-id> | <Module title>
    <one-line module intro>
    ## <topic-id> | <Topic title> [| opt, prev, assumed]
    <description, may use **bold** and `code`>
    - doc|video|article|course | <label> | <url>

Module and topic ids are each unique across every level. An `assumed` topic is a pointer: it reuses the id of a
topic taught in a lower level and needs no lesson. Course source format: see course.py.
"""
import datetime, html, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path
import course

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_source"
OUT = Path(sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv
           else os.environ.get("AI_ACADEMY_OUT") or ROOT / "dist")
TEMPLATE = Path(__file__).resolve().parent / "template.html"
VERIFIED = datetime.date.today().isoformat()
COUNT_WORDS = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five"}


def inline(text):
    t = html.escape(text)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)


def blocks(lines):
    """Render description lines: paragraphs plus '- ' bullet lists (resource lines are filtered out earlier)."""
    out, para, items = [], [], []
    def flush():
        if para: out.append("<p>" + inline(" ".join(para)) + "</p>"); para.clear()
        if items: out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>"); items.clear()
    for ln in lines:
        if ln.startswith("- "):
            if para: out.append("<p>" + inline(" ".join(para)) + "</p>"); para.clear()
            items.append(ln[2:])
        elif not ln.strip():
            flush()
        else:
            if items: flush()
            para.append(ln.strip())
    flush()
    return "".join(out)


def parse(path):
    text = path.read_text(encoding="utf-8")
    fm_raw, body = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S).groups()
    meta = dict(l.split(": ", 1) for l in fm_raw.splitlines() if ": " in l)
    if not meta.get("order", "").isdigit():
        sys.exit(f"error: {path.name}: front matter needs 'order: <n>', the level's place in the course")
    sections, sec, topic = [], None, None
    for line in body.splitlines():
        if m := re.match(r"# (\S+) \| (.+)$", line):
            sec = {"id": m[1], "title": m[2], "intro": "", "topics": []}
            sections.append(sec); topic = None
        elif m := re.match(r"## (\S+) \| (.+?)(?: \| (.+))?$", line):
            flags = {f.strip() for f in (m[3] or "").split(",") if f.strip()}
            topic = {"id": m[1], "module": sec["id"], "title": m[2], "opt": "opt" in flags, "prev": "prev" in flags,
                     "assumed": "assumed" in flags, "lines": [], "links": []}
            sec["topics"].append(topic)
        elif m := re.match(r"- (doc|video|article|course) \| (.+?) \| (\S+)$", line):
            topic["links"].append({"type": m[1], "label": m[2], "url": m[3]})
        elif topic is not None:
            topic["lines"].append(line)
        elif sec is not None and line.strip():
            sec["intro"] += line.strip()
    for s in sections:
        for t in s["topics"]:
            t["html"] = blocks(t.pop("lines"))
    return meta, sections


TYPE_LABEL = {"doc": "Docs", "video": "Video", "article": "Article", "course": "Course"}


def real(topics):
    """The topics a level actually teaches: everything but its assumed-knowledge pointers."""
    return [t for t in topics if not t["assumed"]]


def node(t):
    cls = "node topic" + (" opt" if t["opt"] else "") + (" assumed" if t["assumed"] else "")
    badge = '<span class="badge">Preview</span>' if t["prev"] else ""
    return (f'<a class="{cls}" href="#{t["id"]}" data-id="{t["id"]}">'
            f'<span class="label">{html.escape(t["title"])}</span>{badge}</a>')


def roadmap_html(sections):
    out = []
    for s in sections:
        ts = s["topics"]; half = (len(ts) + 1) // 2
        left, right = ts[:half], ts[half:]
        out.append(
            f'<div class="sec" id="sec-{s["id"]}">'
            f'<div class="col left{" empty" if not left else ""}">{"".join(node(t) for t in left)}</div>'
            f'<a class="node section" href="#{s["id"]}" data-id="{s["id"]}">'
            f'<span class="sec-num">{s["id"]}</span><span class="label">{html.escape(s["title"])}</span></a>'
            f'<div class="col right{" empty" if not right else ""}">{"".join(node(t) for t in right)}</div>'
            f'</div>')
    return "\n".join(out)


def handbook_html(sections):
    out = []
    for s in sections:
        out.append(f'<section class="hb-sec" id="{s["id"]}"><h2><span class="sec-num">{s["id"]}</span> {html.escape(s["title"])}</h2>'
                   f'<p class="hb-intro">{inline(s["intro"])}</p>')
        for t in s["topics"]:
            if t["assumed"]:
                taught = (f'<p>Taught in {course.label(t["taught"])}: <a href="{html.escape(t["target"])}">'
                          f'{html.escape(t["title"])} →</a></p>' if t.get("target") else "")
                out.append(f'<article class="hb-topic assumed" id="{t["id"]}"><h3>{html.escape(t["title"])} '
                           f'<span class="pill assumed">Assumed</span></h3>{t["html"]}{taught}</article>')
                continue
            badges = ('<span class="pill opt">Optional</span>' if t["opt"] else "") + \
                     ('<span class="pill prev">Preview</span>' if t["prev"] else "")
            links = "".join(
                f'<li><span class="pill {l["type"]}">{TYPE_LABEL[l["type"]]}</span> '
                f'<a href="{html.escape(l["url"])}" target="_blank" rel="noopener">{html.escape(l["label"])}</a>'
                f'<span class="url">{html.escape(l["url"])}</span></li>' for l in t["links"])
            out.append(f'<article class="hb-topic" id="{t["id"]}"><h3>{html.escape(t["title"])} {badges}</h3>'
                       f'{t["html"]}<ul class="res">{links}</ul></article>')
        out.append("</section>")
    return "\n".join(out)


def build_level(meta, sections, levels):
    order = list(levels)
    above = order[order.index(meta["id"]) + 1] if order.index(meta["id"]) + 1 < len(order) else None
    data = {"level": meta["id"], "sections": [
        {"id": s["id"], "title": s["title"], "intro": s["intro"],
         "topics": [{**{k: t[k] for k in ("id", "title", "opt", "prev", "assumed", "html", "links")},
                     "lessons": {lang: course.lesson_href(t, lang) for lang in t["sources"]},
                     **({"taught": course.label(t["taught"]), "target": t["target"]} if t.get("target") else {})}
                    for t in s["topics"]]}
        for s in sections]}
    n_topics = sum(len(real(s["topics"])) for s in sections)
    page = TEMPLATE.read_text(encoding="utf-8")
    repl = {
        "{{TITLE}}": html.escape(meta["title"]), "{{SUBTITLE}}": html.escape(meta["subtitle"]),
        "{{TAGLINE}}": html.escape(meta["tagline"]), "{{LEVEL}}": meta["id"], "{{LEVEL_NAV}}": course.level_nav(levels),
        "{{NEXT}}": meta.get("next") or (f"{above}.html" if above else "index.html"),
        "{{NEXT_LABEL}}": html.escape(meta.get("next_label", "")),
        "{{N_TOPICS}}": str(n_topics), "{{N_SECTIONS}}": str(len(sections)), "{{VERIFIED}}": VERIFIED,
        "{{ROADMAP}}": roadmap_html(sections), "{{HANDBOOK}}": handbook_html(sections),
        "{{DATA}}": json.dumps(data, ensure_ascii=False).replace("</", "<\\/"),
    }
    for k, v in repl.items():
        page = page.replace(k, v)
    out = OUT / f"{meta['id']}.html"
    out.write_text(page, encoding="utf-8")
    print(f"built {out.name}: {len(sections)} sections, {n_topics} topics")
    return out


def find_browser():
    # Prefer a Playwright headless shell if installed (works where Edge/Chrome headless are blocked by policy).
    shells = sorted(Path.home().glob("AppData/Local/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell.exe"))
    for p in [*map(str, reversed(shells)),
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe"]:
        if Path(p).exists(): return p
    return shutil.which("msedge") or shutil.which("chrome")


def pdf(page, name):
    browser = find_browser()
    if not browser: sys.exit("No Edge/Chrome found for PDF export")
    (OUT / "pdf").mkdir(exist_ok=True)
    target = OUT / "pdf" / name
    profile = Path(tempfile.gettempdir()) / "ai-academy-pdf-profile"  # isolated from any running browser
    flags = [] if "headless-shell" in browser else ["--headless=new", f"--user-data-dir={profile}"]
    subprocess.run([browser, *flags, "--disable-gpu", "--no-pdf-header-footer", "--window-size=1400,2000",
                    "--run-all-compositor-stages-before-draw", "--virtual-time-budget=8000",
                    f"--print-to-pdf={target}", page.resolve().as_uri() + "?print"],
                   check=True, capture_output=True, timeout=180)
    print(f"built pdf/{name} ({target.stat().st_size // 1024} KB)")


def build_index(levels, metas):
    """The home page: one card per level, in level order."""
    page = (Path(__file__).resolve().parent / "index_template.html").read_text(encoding="utf-8")
    cards, ids = [], {}
    for n, (lvl, sections) in enumerate(levels.items(), 1):
        meta = metas[lvl]
        ids[lvl] = [t["id"] for s in sections for t in real(s["topics"])]
        tag = f"Level {n}" + (f" · {html.escape(meta['audience'])}" if meta.get("audience") else "")
        cards.append(
            f'<article class="card"><span class="tag">{tag}</span><h2>{html.escape(meta["subtitle"])}</h2>'
            f'<p>{html.escape(meta.get("card") or meta["tagline"])}</p>'
            f'<div class="stats"><span>{len(sections)} sections</span><span>{len(ids[lvl])} topics</span>'
            f'<span><b id="{lvl}-done">0</b> done</span></div><div class="bar"><i id="{lvl}-bar"></i></div>'
            f'<div class="actions"><a class="btn primary" href="{lvl}.html">Open roadmap</a>'
            f'<a class="btn" href="pdf/ai-engineering-on-microsoft-{lvl}.pdf">PDF</a></div></article>')
    chip = ['<span>{}</span>'] + ['<span style="background:#fff">{}</span>'] * (len(levels) - 1)  # first one filled
    flow = "<b>→</b>".join(c.format(course.label(lvl)) for c, lvl in zip(chip, levels))
    repl = {"{{N_LEVELS}}": COUNT_WORDS.get(len(levels), str(len(levels))), "{{LEVEL_FLOW}}": flow,
            "{{LEVEL_CARDS}}": "\n    ".join(cards), "{{LEVEL_IDS}}": json.dumps(ids), "{{VERIFIED}}": VERIFIED}
    for k, v in repl.items():
        page = page.replace(k, v)
    (OUT / "index.html").write_text(page, encoding="utf-8")
    print("built index.html")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    parsed = sorted((parse(md) for md in SRC.glob("*.md")), key=lambda p: int(p[0]["order"]))
    if len({int(meta["order"]) for meta, _ in parsed}) < len(parsed):
        sys.exit("error: two roadmaps share the same 'order'")
    levels = {meta["id"]: sections for meta, sections in parsed}  # lowest level first
    metas = {meta["id"]: meta for meta, _ in parsed}
    report = course.Report()
    course.validate(levels, metas, report)
    course.discover(levels, ROOT, report)
    for meta, sections in parsed:
        out = build_level(meta, sections, levels)
        if "--pdf" in sys.argv:
            pdf(out, f"ai-engineering-on-microsoft-{meta['id']}.pdf")
    build_index(levels, metas)
    print(f"built {course.build(levels, metas, ROOT, OUT, report)} course pages + search index")
    course.check_internal_links(OUT, report, "--pdf" in sys.argv)

    for w in report.warnings:
        print(f"warning: {w}")
    listing = "--missing" in sys.argv
    print(f"info: {len(report.missing)} topics have no lesson yet" + ("" if listing else " (list them with --missing)"))
    if listing:
        for m in report.missing: print(f"  no lesson yet: {m}")
    if report.unknowns:
        print(f"info: {len(report.unknowns)} unknown claims open, oldest since {min(d for d, _ in report.unknowns)}")
        for since, where in sorted(report.unknowns): print(f"  unknown since {since}: {where}")
    for e in report.errors:
        print(f"error: {e}")
    if report.errors or ("--strict" in sys.argv and report.warnings):
        sys.exit(1)
