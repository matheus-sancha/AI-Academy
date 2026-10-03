# AI-Academy

Source for the **AI Engineering on Microsoft** learning program: Basic, Intermediate and Advanced roadmaps, plus self-paced course modules (in progress).

## Browse the course locally

From the repo root:

```
pip install -r _build/requirements.txt          # once
python _build/build.py --out dist               # build into dist/ (gitignored)
```

Then open **[dist/index.html](dist/index.html)**, the home page linking every roadmap and course module. Everything works straight from disk; no server needed.

- Roadmaps: [Basic](dist/basic.html) · [Intermediate](dist/intermediate.html) · [Advanced](dist/advanced.html)
- [Technik reference scenario](dist/course/scenario/index.html)

Always pass `--out dist` for a local look: a bare `build.py` writes to `AI_ACADEMY_OUT` when it's set, which may be the shared folder learners open.

- `_source/` — roadmap content (and, later, course lessons)
- `_build/` — build and link-check scripts; see [`_build/README.md`](_build/README.md)
- `docs/` — topic trees and course design decisions

All scenario content uses the fictional company Technik (subsea equipment). Keep every client, project, site and part number invented. Don't commit real organization names, tenant or account details, or credentials.
