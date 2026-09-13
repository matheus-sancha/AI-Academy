# Maintaining the roadmaps

Content lives in `_source/beginner.md` and `_source/advanced.md` (format documented at the top of `build.py`).

```
python check_links.py beginner.md advanced.md   # verify every link -> link-report-*.tsv (gitignored)
python build.py --pdf                           # rebuild index/beginner/advanced HTML + pdf/
```

Built files are not committed. They go to `--out DIR`, else the `AI_ACADEMY_OUT` environment variable, else `dist/`.
Point `AI_ACADEMY_OUT` at the shared folder learners open.

PDF export uses a Playwright headless shell if installed, otherwise Edge/Chrome headless.
Progress is stored in each browser's localStorage under `aiem:<track>:<topic-id>` — keep topic ids stable when editing.
