"""Build the roadmap pages and PDFs from _source/*.md.

    python build.py            # HTML only
    python build.py --pdf      # HTML + PDFs (needs Microsoft Edge or Chrome)

Output goes to --out DIR, else $AI_ACADEMY_OUT, else dist/ (gitignored).

Source format (see _source/beginner.md):
    ---  front matter (id, title, subtitle, tagline, next, next_label)  ---
    # <SECTION-ID> | <Section title>
    <one-line section intro>
    ## <topic-id> | <Topic title> [| opt, prev]
    <description, may use **bold** and `code`>
    - doc|video|article|course | <label> | <url>
"""
import datetime, html, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_source"
OUT = Path(sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv
           else os.environ.get("AI_ACADEMY_OUT") or ROOT / "dist")
TEMPLATE = Path(__file__).resolve().parent / "template.html"
VERIFIED = datetime.date.today().isoformat()


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
    sections, sec, topic = [], None, None
    for line in body.splitlines():
        if m := re.match(r"# (\S+) \| (.+)$", line):
            sec = {"id": m[1], "title": m[2], "intro": "", "topics": []}
            sections.append(sec); topic = None
        elif m := re.match(r"## (\S+) \| (.+?)(?: \| (.+))?$", line):
            flags = {f.strip() for f in (m[3] or "").split(",") if f.strip()}
            topic = {"id": f"{sec['id']}-{m[1]}", "title": m[2], "opt": "opt" in flags, "prev": "prev" in flags,
                     "lines": [], "links": []}
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


def node(t):
    cls = "node topic" + (" opt" if t["opt"] else "")
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


def build_track(md):
    meta, sections = parse(md)
    data = {"track": meta["id"], "sections": [
        {"id": s["id"], "title": s["title"], "intro": s["intro"],
         "topics": [{k: t[k] for k in ("id", "title", "opt", "prev", "html", "links")} for t in s["topics"]]}
        for s in sections]}
    n_topics = sum(len(s["topics"]) for s in sections)
    other = "advanced.html" if meta["id"] == "beginner" else "beginner.html"
    page = TEMPLATE.read_text(encoding="utf-8")
    repl = {
        "{{TITLE}}": html.escape(meta["title"]), "{{SUBTITLE}}": html.escape(meta["subtitle"]),
        "{{TAGLINE}}": html.escape(meta["tagline"]), "{{TRACK}}": meta["id"],
        "{{OTHER}}": other, "{{OTHER_LABEL}}": "Advanced roadmap" if other == "advanced.html" else "Beginner roadmap",
        "{{NEXT}}": meta.get("next", other), "{{NEXT_LABEL}}": html.escape(meta.get("next_label", "")),
        "{{N_TOPICS}}": str(n_topics), "{{N_SECTIONS}}": str(len(sections)), "{{VERIFIED}}": VERIFIED,
        "{{ROADMAP}}": roadmap_html(sections), "{{HANDBOOK}}": handbook_html(sections),
        "{{DATA}}": json.dumps(data, ensure_ascii=False).replace("</", "<\\/"),
    }
    for k, v in repl.items():
        page = page.replace(k, v)
    out = OUT / f"{meta['id']}.html"
    out.write_text(page, encoding="utf-8")
    print(f"built {out.name}: {len(sections)} sections, {n_topics} topics")
    return out, meta, n_topics


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


def build_index(tracks):
    page = (Path(__file__).resolve().parent / "index_template.html").read_text(encoding="utf-8")
    for key, prefix in (("beginner", "B"), ("advanced", "A")):
        sections = tracks[key]
        ids = [t["id"] for s in sections for t in s["topics"]]
        page = (page.replace(f"{{{{{prefix}_SECTIONS}}}}", str(len(sections)))
                    .replace(f"{{{{{prefix}_TOPICS}}}}", str(len(ids)))
                    .replace(f"{{{{{prefix}_IDS}}}}", json.dumps(ids)))
    (OUT / "index.html").write_text(page.replace("{{VERIFIED}}", VERIFIED), encoding="utf-8")
    print("built index.html")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    tracks = {}
    for md in sorted(SRC.glob("*.md")):
        out, meta, _ = build_track(md)
        tracks[meta["id"]] = parse(md)[1]
        if "--pdf" in sys.argv:
            pdf(out, f"ai-engineering-on-microsoft-{meta['id']}.pdf")
    build_index(tracks)
