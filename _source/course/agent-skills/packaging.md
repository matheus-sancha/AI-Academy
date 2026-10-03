## TL;DR

The shape of a skill decides how it ships. A skill that is only `SKILL.md` uploads as a bare `.md`. A skill with
anything else (a template, a reference list, a script) ships as a `.zip` with `SKILL.md` at the **root** of the
archive, not inside a folder. Three failures here are **silent**: a folder-wrapped archive is rejected, a
frontmatter error gets the skill skipped with no error, and Windows' built-in `Compress-Archive` writes entry
paths the zip format forbids. A bad archive looks exactly like a bad skill, so check the package before you
debug the instructions.

## Why it matters

Packaging feels like the step after the real work. It is where a correct skill most often fails to arrive. A
skill can be well described, well written and tested in a text editor, then never appear in the agent because
of how it was zipped. Nothing in the error tells you the archive is the problem, so people rewrite a
description that was fine, or re-upload the same broken archive under a new name.

**Pitfalls is the load-bearing section of this lesson.** Every row in it is a failure that produces no useful
message.

## How it works

### Shape decides packaging

Copilot Studio accepts two formats:

| You have | Ship it as | What arrives |
|---|---|---|
| `SKILL.md` alone | A bare `.md` file | The instructions |
| `SKILL.md` plus `assets/`, `references/` or `scripts/` | A `.zip` containing `SKILL.md` and its supporting files | The instructions and every file |

A bare `.md` carries nothing else, so a skill whose body says *fill in `assets/qn-template.md`* must ship as a
package. Upload only its `SKILL.md` and the body points at a file that is not there. The skill loads, fires, and
improvises the template.

### What goes inside the archive

The archive holds the **contents** of the skill folder, not the folder:

```
qn-write-up.zip                    qn-write-up.zip
├── SKILL.md            ✔          └── qn-write-up/            ✘
├── assets/                            ├── SKILL.md
│   └── qn-template.md                 └── assets/ ...
└── references/
    └── defect-types.md
```

<!-- verified tenant=2026-09 -->
An archive with its files wrapped in a `qn-write-up/` folder is refused with *"Upload failed. Bundle is missing a
root-level SKILL.md file."* The specification's rule that `name` matches the parent folder
({{topic:skillmd}}) describes the folder you author in; it does not mean the archive carries that folder.
<!-- /verified -->

One archive holds one skill. Paths inside it use **forward slashes**: `assets/qn-template.md`, never
`assets\qn-template.md`. The zip format requires them.

### Building the archive on Windows

The obvious tools both get it wrong. Right-click **Compress to ZIP file** on the folder wraps everything in
that folder. `Compress-Archive` in Windows PowerShell writes entry paths with backslashes.

<!-- verified tenant=2026-09 -->
`Compress-Archive` produced `references\defect-types.md` entries, and Copilot Studio can refuse such a package
with no useful error.
<!-- /verified -->

This builds a correct one, with the contents at the root and forward slashes throughout:

```powershell
Add-Type -AssemblyName System.IO.Compression, System.IO.Compression.FileSystem
$src = (Resolve-Path .\qn-write-up).Path
$zip = [System.IO.Compression.ZipFile]::Open("$PWD\qn-write-up.zip", 'Create')
Get-ChildItem $src -Recurse -File | ForEach-Object {
  $entry = $_.FullName.Substring($src.Length + 1).Replace('\', '/')
  [void][System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $_.FullName, $entry)
}
$zip.Dispose()
```

Then **check it before uploading**. Listing the entries takes one line and catches both shapes of mistake:

```powershell
[System.IO.Compression.ZipFile]::OpenRead("$PWD\qn-write-up.zip").Entries.FullName
```

The first line should read `SKILL.md`, and no entry should contain a backslash.

### The load-time checks still apply

A well-formed archive only gets the skill as far as validation. Copilot Studio checks every skill again when
it loads and **skips** one that fails, while the rest of the agent loads normally ({{topic:addskill}}). The
checks that packaging decides are:

| Check | Packaging cause |
|---|---|
| Unreadable `SKILL.md` | Saved with a byte-order mark. Re-save as UTF-8 without BOM |
| Invalid YAML frontmatter | An unquoted colon, often introduced while editing for the release |
| A supporting file was not written | Re-export, check each file is present and readable, upload again |
| Package rejected by a structural check | Re-export from a working editor and retry |

Microsoft adds a warning that matters here: a skill whose supporting files were only **partly** written still
loads, then behaves differently because something it refers to is missing.

<!-- unknown since=2026-10 -->
Copilot Studio publishes no size, file-count or file-type limits for a skill package on this harness. The same
format in Microsoft 365 Copilot's Agent Builder allows a 50 MB archive, 350 files and a directory depth of 3, but
that is a different product. Keep packages small and shallow until the limits are known.
<!-- /unknown -->

## In practice at Technik

The quality team's `qn-write-up` lives in Git as a folder: `SKILL.md`, `assets/qn-template.md` and
`references/defect-types.md` ({{topic:skillmd}}). It is a package, because two of its steps point at files.

A release goes the same way every time: re-save `SKILL.md` as UTF-8 without BOM, build the archive with the
script above, list its entries, and only then upload or **Replace**. Keeping the build in a script, not in
someone's right-click habits, is what makes the next release behave like the last.

One trap is specific to packages. Ask the agent to *show me your `qn-write-up` skill file* and it may report
that the file is empty, or contains only a marker.

<!-- verified tenant=2026-09 -->
A packaged skill is stored as the archive behind a `<!-- bic:bundle=… -->` pointer, while its real `SKILL.md`
and supporting files are stored separately. An agent reading the skill's own entry finds the pointer, not the
body. The skill is intact.
<!-- /verified -->

Never let that reading talk anyone into repackaging a skill that works. The test of a package is whether the
skill fires and follows its template in a new chat, not what the agent says about its own files.

## Design guidance

- **Let shape decide**: one file ships as `.md`, anything more as `.zip`.
- **Zip the contents, never the folder.** `SKILL.md` is the first entry.
- **Build archives with a script**, not with the Explorer menu or `Compress-Archive`.
- **List the entries before every upload.** It is cheaper than any diagnosis afterwards.
- **Re-save as UTF-8 without BOM on every release**; some Windows editors add the mark back.
- **Keep the folder in version control**, and build the archive from it each time.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| *Bundle is missing a root-level SKILL.md file* | The archive wraps a folder | Zip the folder's contents; `SKILL.md` at the root |
| Upload refused, nothing useful said | Backslash entry paths from `Compress-Archive` | Rebuild with forward-slash entries; list them to check |
| The skill is missing from the components panel | A load-time check failed, silently | BOM and unquoted colons first, then the checks table |
| The skill fires and invents its own template | `SKILL.md` was uploaded alone, without its files | Upload the whole package |
| It loads, then behaves differently from the last release | Supporting files only partly written | Re-upload the whole package |
| The agent says its own skill file is empty | It is reading the package pointer | Ignore it; test the behaviour in a new chat |

## Key terms

**Skill package**: a `.zip` with `SKILL.md` at its root and the skill's supporting files beside it.

**Archive root**: the top level of the `.zip`; where `SKILL.md` must be.

**Entry path**: the path a file is stored under inside the archive, which must use forward slashes.

**Byte-order mark (BOM)**: invisible bytes some editors write at the start of a UTF-8 file, which stop
Copilot Studio reading `SKILL.md`.
