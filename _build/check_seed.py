"""Check that the Technik material stays consistent with itself, without a Snowflake account.

    python check_seed.py            # report problems, exit 1 if any

Covers three things that drift apart silently:

  * the seed in labs/_setup/snowflake/ -- row shape against the DDL, referential integrity between
    SAP and Teamcenter, identifier formats, and the deliberate teaching defects, which are features
    a future edit must not quietly remove;
  * the values labs tell learners to expect from that seed;
  * passages that a lesson or exercise quotes verbatim from a Technik document.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = ROOT / "labs" / "_setup" / "snowflake"
DDL = SQL_DIR / "01_seed_tables.sql"
DATA = ["02_seed_sap.sql", "03_seed_teamcenter.sql", "04_seed_quality_fat.sql"]

problems = []


def fail(msg):
    problems.append(msg)


def tokenize_row(text):
    """Split one VALUES tuple into raw values, respecting quoted strings."""
    out, buf, quoted, depth = [], "", False, 0
    i = 0
    while i < len(text):
        ch = text[i]
        if quoted:
            if ch == "'":
                if i + 1 < len(text) and text[i + 1] == "'":
                    buf += "'"; i += 2; continue
                quoted = False
            else:
                buf += ch
            i += 1
            continue
        if ch == "'":
            quoted = True
        elif ch == "(":
            depth += 1; buf += ch
        elif ch == ")":
            depth -= 1; buf += ch
        elif ch == "," and depth == 0:
            out.append(buf.strip()); buf = ""
        else:
            buf += ch
        i += 1
    out.append(buf.strip())
    return out


def split_rows(block):
    """Yield the text inside each top-level (...) tuple of a VALUES list."""
    rows, depth, start, quoted = [], 0, None, False
    for i, ch in enumerate(block):
        if quoted:
            if ch == "'" and not (i + 1 < len(block) and block[i + 1] == "'"):
                quoted = False
            continue
        if ch == "'":
            quoted = True
        elif ch == "(":
            if depth == 0:
                start = i + 1
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                rows.append(block[start:i])
    return rows


def parse_ddl():
    text = DDL.read_text(encoding="utf-8")
    tables = {}
    for m in re.finditer(r"CREATE OR REPLACE TABLE (\w+) \((.*?)\n\) COMMENT", text, re.S):
        cols = [c[1] for c in re.finditer(r"^\s{4}(\w+)\s+\w", m[2], re.M)]
        tables[m[1]] = cols
    return tables


def parse_data():
    """table -> list of dicts, using the column list in the INSERT and the VALUES rows."""
    data = {}
    for name in DATA:
        text = (SQL_DIR / name).read_text(encoding="utf-8")
        text = re.sub(r"--[^\n]*", "", text)                      # line comments
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)          # block comments
        for m in re.finditer(r"INSERT INTO (\w+)\s*\((.*?)\)\s*(SELECT|VALUES)(.*?);", text, re.S):
            table, cols = m[1], [c.strip() for c in m[2].split(",")]
            body = m[4]
            if m[3] == "SELECT":
                # INSERT ... SELECT <expr list> FROM VALUES (...) AS v(<source cols>)
                vals = re.search(r"FROM VALUES(.*?)AS v\((.*?)\)\s*$", body, re.S)
                if not vals:
                    fail(f"{name}: cannot read the VALUES list for {table}")
                    continue
                src_cols = [c.strip() for c in vals[2].split(",")]
                rows = [dict(zip(src_cols, tokenize_row(r))) for r in split_rows(vals[1])]
            else:
                rows = [dict(zip(cols, tokenize_row(r))) for r in split_rows(body)]
            for r in rows:
                if len(r) != len(set(r)):
                    fail(f"{name}: duplicate column name in the {table} row list")
            data.setdefault(table, []).extend(rows)
            bad = [r for r in rows if len(r) != (len(src_cols) if m[3] == "SELECT" else len(cols))]
            if bad:
                fail(f"{name}: {len(bad)} row(s) in {table} do not have the expected number of values")
    return data


def col(rows, name):
    return [r[name] for r in rows]


def nn(values):
    """Non-null values."""
    return [v for v in values if v != "NULL"]


# --------------------------------------------------------------------------
ddl = parse_ddl()
data = parse_data()

# 1. Every table in the DDL is seeded, and the INSERT columns exist.
for table, cols in ddl.items():
    if table not in data:
        fail(f"table {table} is defined but never seeded")

# 2. Referential integrity.
parts = set(col(data["TC_PARTS"], "PART_NO"))
drawings = set(col(data["TC_DRAWINGS"], "DRAWING_NO"))
programs = set(col(data["TC_CNC_PROGRAMS"], "PROGRAM_NO"))
docs = set(col(data["TC_DOCUMENTS"], "DOC_NO"))
projects = set(col(data["SAP_PROJECTS"], "PROJECT_ID"))
units = set(col(data["SAP_UNITS"], "SERIAL_NO"))
wos = set(col(data["SAP_WORK_ORDERS"], "WO_NO"))
ecns = set(col(data["TC_ECNS"], "ECN_NO"))

refs = [
    ("SAP_UNITS.PROJECT_ID", col(data["SAP_UNITS"], "PROJECT_ID"), projects),
    ("SAP_BOM_LINES.PARENT_PART_NO", col(data["SAP_BOM_LINES"], "PARENT_PART_NO"), parts),
    ("SAP_BOM_LINES.COMPONENT_PART_NO", col(data["SAP_BOM_LINES"], "COMPONENT_PART_NO"), parts),
    ("SAP_WORK_ORDERS.PART_NO", col(data["SAP_WORK_ORDERS"], "PART_NO"), parts),
    ("SAP_WORK_ORDERS.SERIAL_NO", col(data["SAP_WORK_ORDERS"], "SERIAL_NO"), units),
    ("SAP_WORK_ORDERS.PROJECT_ID", col(data["SAP_WORK_ORDERS"], "PROJECT_ID"), projects),
    ("SAP_WO_OPERATIONS.WO_NO", col(data["SAP_WO_OPERATIONS"], "WO_NO"), wos),
    ("SAP_WO_OPERATIONS.DRAWING_NO", nn(col(data["SAP_WO_OPERATIONS"], "DRAWING_NO")), drawings),
    ("SAP_WO_OPERATIONS.CNC_PROGRAM_NO", nn(col(data["SAP_WO_OPERATIONS"], "CNC_PROGRAM_NO")), programs),
    ("SAP_WO_OPERATIONS.WORK_INSTRUCTION_NO", nn(col(data["SAP_WO_OPERATIONS"], "WORK_INSTRUCTION_NO")), docs),
    ("SAP_QUALITY_NOTIFICATIONS.WO_NO", col(data["SAP_QUALITY_NOTIFICATIONS"], "WO_NO"), wos),
    ("SAP_QUALITY_NOTIFICATIONS.SERIAL_NO", col(data["SAP_QUALITY_NOTIFICATIONS"], "SERIAL_NO"), units),
    ("SAP_QUALITY_NOTIFICATIONS.PART_NO", col(data["SAP_QUALITY_NOTIFICATIONS"], "PART_NO"), parts),
    ("TC_DRAWINGS.PART_NO", col(data["TC_DRAWINGS"], "PART_NO"), parts),
    ("TC_CNC_PROGRAMS.PART_NO", col(data["TC_CNC_PROGRAMS"], "PART_NO"), parts),
    ("TC_ECN_AFFECTED_ITEMS.ECN_NO", col(data["TC_ECN_AFFECTED_ITEMS"], "ECN_NO"), ecns),
    ("FAT_RESULTS.SERIAL_NO", col(data["FAT_RESULTS"], "SERIAL_NO"), units),
]
for label, values, allowed in refs:
    for v in sorted(set(values) - allowed):
        fail(f"{label}: {v} does not exist in the referenced table")

# 3. Identifier formats.
patterns = [
    ("part", parts, r"P70000\d{5}"),
    ("drawing", drawings, r"DU7000\d{5}"),
    ("CNC program", programs, r"T70000\d{5}"),
    ("document", docs, r"[A-Z]{3}700\d{5}"),
    ("ECN", ecns, r"ECN700\d{5}"),
    ("project", projects, r"PRJ-\d{4}"),
    ("serial", units, r"(XT|MF)-[A-Z0-9]+-\d{4}"),
]
for label, values, pattern in patterns:
    for v in sorted(values):
        if not re.fullmatch(pattern, v):
            fail(f"{label} number {v} does not match {pattern}")
        if len(v) != 11 and label in ("part", "drawing", "CNC program", "document", "ECN"):
            fail(f"{label} number {v} is {len(v)} characters, not 11")

# 4. Each item has exactly one Released revision (or none, if still In Work).
for table, key in (("TC_PARTS", "PART_NO"), ("TC_DRAWINGS", "DRAWING_NO"),
                   ("TC_CNC_PROGRAMS", "PROGRAM_NO")):
    released = {}
    for r in data[table]:
        if r["RELEASE_STATUS"] == "Released":
            released.setdefault(r[key], []).append(r["REVISION"])
    for item, revs in released.items():
        if len(revs) > 1:
            fail(f"{table}: {item} has more than one Released revision ({', '.join(revs)})")
docs_released = {}
for r in data["TC_DOCUMENTS"]:
    if r["STATUS"] == "Released":
        docs_released.setdefault(r["DOC_NO"], []).append(r["REVISION"])
for item, revs in docs_released.items():
    if len(revs) > 1:
        fail(f"TC_DOCUMENTS: {item} has more than one Released revision ({', '.join(revs)})")

# 5. ECN affected items point at revisions that exist (FROM_REV) or are pending (TO_REV).
rev_index = {}
for table, key in (("TC_PARTS", "PART_NO"), ("TC_DRAWINGS", "DRAWING_NO"),
                   ("TC_CNC_PROGRAMS", "PROGRAM_NO"), ("TC_DOCUMENTS", "DOC_NO")):
    for r in data[table]:
        rev_index.setdefault(r[key], set()).add(r["REVISION"])
for r in data["TC_ECN_AFFECTED_ITEMS"]:
    known = rev_index.get(r["ITEM_NO"])
    if known is None:
        fail(f"TC_ECN_AFFECTED_ITEMS: {r['ITEM_NO']} is not a known part, drawing, document or program")
    elif r["FROM_REV"] not in known:
        fail(f"TC_ECN_AFFECTED_ITEMS: {r['ITEM_NO']} has no revision {r['FROM_REV']} to change from")

# 6. Work order and operation consistency.
wo_by_no = {r["WO_NO"]: r for r in data["SAP_WORK_ORDERS"]}
for r in data["SAP_WORK_ORDERS"]:
    if r["STATUS"] == "CRTD" and r["REL_OFF"] != "NULL":
        fail(f"work order {r['WO_NO']} is CRTD but has a release date")
    if r["STATUS"] != "CRTD" and r["REL_OFF"] == "NULL":
        fail(f"work order {r['WO_NO']} is {r['STATUS']} but has no release date")
    if r["STATUS"] == "TECO" and r["COMP_OFF"] == "NULL":
        fail(f"work order {r['WO_NO']} is TECO but has no completion date")
    if r["STATUS"] != "TECO" and r["COMP_OFF"] != "NULL":
        fail(f"work order {r['WO_NO']} is {r['STATUS']} but has a completion date")
    if r["COMP_OFF"] != "NULL" and int(r["COMP_OFF"]) <= int(r["REL_OFF"]):
        fail(f"work order {r['WO_NO']} completes before it is released")

ops_by_wo = {}
for r in data["SAP_WO_OPERATIONS"]:
    ops_by_wo.setdefault(r["WO_NO"], []).append(r)
for wo, ops in ops_by_wo.items():
    statuses = {o["STATUS"] for o in ops}
    wo_status = wo_by_no[wo]["STATUS"]
    if wo_status == "TECO" and statuses != {"CNF"}:
        fail(f"work order {wo} is TECO but not every operation is confirmed")
    if wo_status == "CRTD" and statuses != {"OPEN"}:
        fail(f"work order {wo} is CRTD but some operations have started")
    if wo_status == "PCNF" and "CNF" not in statuses:
        fail(f"work order {wo} is PCNF but no operation is confirmed")
    for o in ops:
        if o["STATUS"] == "CNF" and (o["ACTUAL_HOURS"] == "NULL" or o["CONFIRMATION_NO"] == "NULL"):
            fail(f"{wo} operation {o['OP_SEQ']} is CNF without hours or a confirmation number")
        if o["STATUS"] != "CNF" and o["CONFIRMATION_NO"] != "NULL":
            fail(f"{wo} operation {o['OP_SEQ']} is {o['STATUS']} but has a confirmation number")
        if o["STATUS"] == "OPEN" and o["START_OFF"] != "NULL":
            fail(f"{wo} operation {o['OP_SEQ']} is OPEN but has an actual start")
    seqs = [o["OP_SEQ"] for o in ops]
    if seqs != sorted(seqs):
        fail(f"work order {wo} lists operations out of sequence")

# 7. The deliberate teaching defects must still be there.
dupes = {(o["WO_NO"], o["OP_SEQ"]) for o in data["SAP_WO_OPERATIONS"]
         if sum(1 for x in data["SAP_WO_OPERATIONS"] if (x["WO_NO"], x["OP_SEQ"]) == (o["WO_NO"], o["OP_SEQ"])) > 1}
if len(dupes) != 6:
    fail(f"expected 6 duplicated operation confirmations, found {len(dupes)}")
for wo, seq in dupes:
    rows = [o for o in data["SAP_WO_OPERATIONS"] if (o["WO_NO"], o["OP_SEQ"]) == (wo, seq)]
    if len({o["CONFIRMATION_NO"] for o in rows}) != len(rows):
        fail(f"{wo} operation {seq}: the repeated confirmations share a confirmation number")
    if len({o["ACTUAL_HOURS"] for o in rows}) == 1:
        fail(f"{wo} operation {seq}: both confirmations book the same hours, so the naive "
             f"SUM(ROUTING_HOURS)/SUM(ACTUAL_HOURS) ratio cancels out and the defect is invisible")

latest_released = {}
for table, key in (("TC_DRAWINGS", "DRAWING_NO"), ("TC_CNC_PROGRAMS", "PROGRAM_NO")):
    for r in data[table]:
        if r["RELEASE_STATUS"] == "Released":
            latest_released[r[key]] = r["REVISION"]
superseded_ops = [o for o in data["SAP_WO_OPERATIONS"]
                  if o["DRAWING_NO"] != "NULL" and o["STATUS"] != "CNF"
                  and latest_released.get(o["DRAWING_NO"]) not in (None, o["DRAWING_REV"])]
if not {o["WO_NO"] for o in superseded_ops} >= {"100004510", "100004513"}:
    fail("work orders 100004510 and 100004513 should still sit on superseded revisions")

overdue = [d for d in data["TC_DOCUMENTS"]
           if d["STATUS"] == "Released" and d["REVIEW_OFF"] != "NULL" and int(d["REVIEW_OFF"]) < 0]
if len(overdue) < 3:
    fail(f"expected at least 3 documents past their review date, found {len(overdue)}")

injected = [q for q in data["SAP_QUALITY_NOTIFICATIONS"]
            if re.search(r"ignore all previous instructions|<important>", q["DESCRIPTION"], re.I)]
if len(injected) < 2:
    fail(f"expected at least 2 prompt-injection notifications, found {len(injected)}")

pending = [(a["ECN_NO"], a["ITEM_NO"]) for a in data["TC_ECN_AFFECTED_ITEMS"]
           if a["TO_REV"] not in rev_index.get(a["ITEM_NO"], set())]
if ("ECN70000042", "SWI70000318") not in pending:
    fail("ECN70000042 should still be waiting for revision C of SWI70000318")

# 8. The revisions the B7 lab tells learners to expect from V_RELEASED_REVISIONS.
#    The lab asserts specific values, so the seed must keep producing them.
view = {}
for table, key, title_key, status_key in (("TC_PARTS", "PART_NO", "DESCRIPTION", "RELEASE_STATUS"),
                                          ("TC_DRAWINGS", "DRAWING_NO", "TITLE", "RELEASE_STATUS"),
                                          ("TC_CNC_PROGRAMS", "PROGRAM_NO", "MACHINE", "RELEASE_STATUS"),
                                          ("TC_DOCUMENTS", "DOC_NO", "TITLE", "STATUS")):
    for r in data[table]:
        if r[status_key] == "Released":
            if r[key] in view:
                fail(f"V_RELEASED_REVISIONS would return two rows for {r[key]}")
            view[r[key]] = r["REVISION"]
released_ecns = {e["ECN_NO"] for e in data["TC_ECNS"] if e["STATUS"] == "Released"}
introduced_by = {(a["ITEM_NO"], a["TO_REV"]): a["ECN_NO"]
                 for a in data["TC_ECN_AFFECTED_ITEMS"] if a["ECN_NO"] in released_ecns}
for item, revision, ecn in (("P7000001042", "C", "ECN70000051"),
                            ("DU700001042", "C", "ECN70000051"),
                            ("T7000000217", "B", "ECN70000051"),
                            ("P7000001088", "D", "ECN70000078"),
                            ("SWI70000318", "B", None)):
    if view.get(item) != revision:
        fail(f"labs/B7/lab.md expects {item} at released revision {revision}; the seed has {view.get(item)}")
    if introduced_by.get((item, revision)) != ecn:
        fail(f"labs/B7/lab.md expects {item} revision {revision} to cite "
             f"{ecn or 'no released ECN'}; the seed gives {introduced_by.get((item, revision)) or 'none'}")

# 9. Row counts quoted to learners in 20_learner_start_here.sql.
expected = re.search(r"-- Expected: ([\d, ]+)\.", (SQL_DIR / "20_learner_start_here.sql").read_text(encoding="utf-8"))
if expected:
    quoted = [int(x) for x in expected[1].split(",")]
    order = ["FAT_RESULTS", "SAP_BOM_LINES", "SAP_PROJECTS", "SAP_QUALITY_NOTIFICATIONS", "SAP_UNITS",
             "SAP_WORK_ORDERS", "SAP_WO_OPERATIONS", "TC_CNC_PROGRAMS", "TC_DOCUMENTS", "TC_DRAWINGS",
             "TC_ECNS", "TC_ECN_AFFECTED_ITEMS", "TC_PARTS"]
    listed = ["SAP_PROJECTS", "SAP_UNITS", "SAP_BOM_LINES", "SAP_WORK_ORDERS", "SAP_WO_OPERATIONS",
              "SAP_QUALITY_NOTIFICATIONS", "TC_PARTS", "TC_DRAWINGS", "TC_CNC_PROGRAMS", "TC_DOCUMENTS",
              "TC_ECNS", "TC_ECN_AFFECTED_ITEMS", "FAT_RESULTS"]
    for table, n in zip(listed, quoted):
        if len(data[table]) != n:
            fail(f"20_learner_start_here.sql says {table} has {n} rows; the seed has {len(data[table])}")
else:
    fail("20_learner_start_here.sql no longer states the expected row counts")

# 9b. The facts labs/B6/lab.md states about the seeded work order data.
op_rows = [o for o in data["SAP_WO_OPERATIONS"] if o["WO_NO"] == "100004521"]
current = [o for o in op_rows if o["STATUS"] == "INPROC"]
if len(current) != 1 or current[0]["OP_SEQ"] != "0030" or current[0]["OPERATION"] != "Welding":
    fail("labs/B6/lab.md expects work order 100004521 to be in process at operation 0030, Welding; "
         f"the seed has {[(o['OP_SEQ'], o['OPERATION']) for o in current] or 'no operation in process'}")
if wo_by_no["100004521"]["STATUS"] != "PCNF":
    fail(f"labs/B6/lab.md expects work order 100004521 to be PCNF; "
         f"the seed has {wo_by_no['100004521']['STATUS']}")


def efficiency(rows):
    routing = sum(float(o["ROUTING_HOURS"]) for o in rows)
    actual = sum(float(o["ACTUAL_HOURS"]) for o in rows)
    return routing / actual * 100 if actual else 0.0


def deduplicated(rows):
    # One row per operation, keeping the latest confirmation: the QUALIFY the labs teach.
    seen, kept = set(), []
    for o in sorted(rows, key=lambda x: x["CONFIRMATION_NO"], reverse=True):
        key = (o["WO_NO"], o["OP_SEQ"])
        if key not in seen:
            seen.add(key); kept.append(o)
    return kept


confirmed = [o for o in data["SAP_WO_OPERATIONS"] if o["STATUS"] == "CNF"]
p1_welding = [o for o in confirmed
              if o["OPERATION"] == "Welding" and wo_by_no[o["WO_NO"]]["PLANT"] == "Plant 1"]
for label, rows, raw_target, dedup_target in (
        ("all confirmed operations", confirmed, 100, 95),
        ("welding at Plant 1", p1_welding, 111, 89)):
    raw, dedup = efficiency(rows), efficiency(deduplicated(rows))
    if abs(raw - raw_target) > 1.5:
        fail(f"labs/B6/lab.md says raw efficiency for {label} is about {raw_target}%; "
             f"the seed gives {raw:.1f}%")
    if abs(dedup - dedup_target) > 1.5:
        fail(f"labs/B6/lab.md says deduplicated efficiency for {label} is about {dedup_target}%; "
             f"the seed gives {dedup:.1f}%")
    if abs(raw - dedup) < 3:
        fail(f"the duplicate-confirmation defect is no longer visible in {label}: "
             f"raw {raw:.1f}% and deduplicated {dedup:.1f}% are too close to teach anything")

# 10. Passages quoted verbatim from a Technik document must still match the document.
def normalise(s):
    return re.sub(r"\s+", " ", s.replace("|", " ").replace("*", "")).strip()

QUOTES = [
    # (document, heading in the document, file quoting it, regex capturing the quote)
    ("labs/_setup/documents/SWI70000318.md", r"### 4\.2 Surface preparation before overlay\n(.*?)\n## ",
     "labs/B1/exercise.md", r"> \*\*4\.2 Surface preparation before overlay\*\*\n(.*?)\n\n\*\*Your tasks"),
]
for doc_path, doc_pattern, quoting_path, quote_pattern in QUOTES:
    doc_file, quote_file = ROOT / doc_path, ROOT / quoting_path
    if not (doc_file.exists() and quote_file.exists()):
        fail(f"{doc_path} or {quoting_path} is missing, so their quoted passage cannot be checked")
        continue
    in_doc = re.search(doc_pattern, doc_file.read_text(encoding="utf-8"), re.S)
    in_quote = re.search(quote_pattern, quote_file.read_text(encoding="utf-8"), re.S)
    if not in_doc:
        fail(f"{doc_path}: the passage {quoting_path} quotes can no longer be found")
    elif not in_quote:
        fail(f"{quoting_path}: the quoted passage from {doc_path} can no longer be found")
    elif normalise(in_doc[1]) != normalise(re.sub(r"^> ?", "", in_quote[1], flags=re.M)):
        fail(f"{quoting_path} no longer quotes {doc_path} verbatim; update one to match the other")

# --------------------------------------------------------------------------
for p in problems:
    print(f"error: {p}")
print(f"checked {sum(len(v) for v in data.values())} rows in {len(data)} tables: "
      f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
