"""Verify every link in _source/*.md: HTTP status, final URL and page title.
Usage: python check_links.py basic.md [intermediate.md advanced.md]   -> writes _build/link-report-<name>.tsv

Also compares the declared skills_pin against copilot-studio-skills' latest release and reports drift. That check
lives here, not in build.py, because the build must run offline.
"""
import concurrent.futures as cf, html, json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path
from course import SKILLS_REPO

ROOT = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36",
      "Accept-Language": "en-US,en;q=0.9"}

def check(url):
    try:
        if "youtube.com/watch" in url:
            o = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(url, safe="")
            d = json.loads(urllib.request.urlopen(urllib.request.Request(o, headers=UA), timeout=30).read())
            return 200, url, f"{d['title']} — {d['author_name']}"
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30)
        body = r.read(400000).decode("utf-8", "ignore")
        m = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
        return r.status, r.geturl(), html.unescape(m.group(1).strip()) if m else ""
    except urllib.error.HTTPError as e:
        return e.code, url, ""
    except Exception as e:
        return 0, url, f"ERR {e}"

def links(md):
    for line in md.read_text(encoding="utf-8").splitlines():
        m = re.match(r"- (doc|video|article|course) \| (.+?) \| (\S+)$", line)
        if m: yield m.group(2), m.group(3)

for name in sys.argv[1:]:
    items = list(dict.fromkeys(u for _, u in links(ROOT / "_source" / name)))
    with cf.ThreadPoolExecutor(8) as ex:
        res = dict(zip(items, ex.map(check, items)))
    # support.microsoft.com throttles a parallel sweep and answers 403 — indistinguishable in the
    # report from a page that was removed. Retry serially with escalating backoff before believing it.
    for pause in (5, 20):
        retry = [u for u, (s, _, _) in res.items() if s != 200]
        if not retry: break
        print(f"{name}: retrying {len(retry)} failures serially, {pause}s apart")
        for u in retry:
            time.sleep(pause)
            res[u] = check(u)
    out = ROOT / "_build" / f"link-report-{Path(name).stem}.tsv"
    with out.open("w", encoding="utf-8") as f:
        for u, (s, final, title) in res.items():
            f.write(f"{s}\t{u}\t{final if final != u else ''}\t{title}\n")
    # 403 means "refused", not "gone": after the serial retries above it is almost always a bot check
    # or a rate limit, so it is reported apart from the statuses that do mean the page is broken.
    broken = [(u, s) for u, (s, _, _) in res.items() if s not in (200, 403)]
    blocked = [u for u, (s, _, _) in res.items() if s == 403]
    print(f"{name}: {len(items)} unique links, {len(broken)} broken, {len(blocked)} blocked")
    for u, s in broken: print(f"  {s}  {u}")
    for u in blocked: print(f"  403 blocked (bot check or rate limit, not proof it is gone)  {u}")


def pin_check():
    """Report whether the release the course is pinned to is still upstream's latest."""
    pins = {}
    for md in sorted((ROOT / "_source").glob("*.md")):
        fm = re.match(r"---\n(.*?)\n---\n", md.read_text(encoding="utf-8"), re.S)
        for line in (fm[1].splitlines() if fm else []):
            if line.startswith("skills_pin: "): pins[md.name] = line.split(": ", 1)[1].strip()
    if not pins:
        return
    api = f"https://api.github.com/repos/{SKILLS_REPO}/releases/latest"
    try:
        latest = json.loads(urllib.request.urlopen(urllib.request.Request(api, headers=UA), timeout=30).read())["tag_name"]
    except Exception as e:
        print(f"PIN  {SKILLS_REPO}: could not read the latest release ({e})"); return
    for name, pin in pins.items():
        verdict = "ok" if pin == latest else "DRIFT: read the upstream diff, then bump skills_pin"
        print(f"PIN  {SKILLS_REPO}  pinned {pin} ({name})  latest {latest}  {verdict}")


pin_check()
