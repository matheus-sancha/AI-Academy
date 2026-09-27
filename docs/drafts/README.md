# Roadmap drafts

The three new roadmap files are written here, not in `_source/`, because **topic ids are unique across
every roadmap file**: `basic.md` next to today's `beginner.md` duplicates every re-homed topic and fails
the build. [#20](https://github.com/matheus-sancha/AI-Academy/issues/20) moves all three into `_source/`
in one change, together with the B1/B7 lesson migration, and deletes this directory.

Validate a draft with a scratch build — a copy of `_build/` beside a scratch `_source/` holding only the
drafts — rather than by putting it in `_source/`.

## Conventions these drafts follow

Settled in [#21](https://github.com/matheus-sancha/AI-Academy/issues/21); they bind `intermediate.md`
and `advanced.md` too.

- **Module badge.** Module ids are slugs, so the badge, crumb and search row show a *derived* label: the
  level id's first letter plus the module's 1-based position (`B3`, `I7`, `A11`). Nothing stores it,
  reordering renumbers it, and two levels may not start with the same letter. Prose cites
  `{{module:<id>}}`, never the badge — the badge is not an identifier.
- **Links.** Every topic carries 2–3 links, and every label quotes the page's real title. Verify with
  `python check_links.py <name>.md`, which reports the final URL and title so a redirect or a renamed
  page is visible. Treat a 403 from `support.microsoft.com` as throttling, not a dead link.
- **Product name.** The course says **Microsoft Copilot**, following Microsoft's current docs. The
  licence keeps its own name where licensing is the point ("a Microsoft 365 Copilot licence"), and link
  labels keep whatever the page title actually says.
