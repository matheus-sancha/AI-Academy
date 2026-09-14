> **About 90 minutes.** You need your Power Platform developer environment, Copilot Studio, a
> SharePoint site you can upload two files to, and your Snowflake sandbox with
> `ACADEMY_AGENT_<you>` working. Budget a modest number of Copilot Credits — roughly fifty test
> turns.
>
> **This lab is independent.** It ships its own starter, so you do not need to have finished B5.

## What you are building

The assistant currently knows nothing about Technik. By the end of this lab it will answer, with
citations, from three kinds of knowledge at once:

- five controlled documents, as uploaded PDFs;
- two intranet pages, from SharePoint, with each user's own permissions;
- work order data, queried live in Snowflake.

And it will do the two things that separate a grounded agent from a plausible one: **say which
source it used**, and **say when its sources do not reach**.

## What the starter contains

`start/TechnikAssistant_B5_end.zip` is an unmanaged solution holding the assistant as B5 leaves it:

- **Agent:** *Technik Production Assistant*, standard harness, generative orchestration on.
- **Instructions:** identity (an internal assistant for Technik manufacturing and engineering
  staff), scope (work orders, quality, documents and revisions), tone (concise, factual, British
  English).
- **Topics:** one, *Work order status*, which asks for a work order number and replies that it
  cannot look it up yet. It stays in place for the rest of the Beginner track.
- **Knowledge:** none.
- **Tools:** none.
- **Connection references:** none.

## Step 0 — Reset your sandbox

```sql
USE ROLE ACADEMY_LEARNER_<you>;
USE WAREHOUSE ACADEMY_WH_<you>;
USE SCHEMA AI_ACADEMY.SANDBOX_<you>;

CALL AI_ACADEMY.SHARED.RESET_TO('B6');
```

It should report 13 tables restored.

## Step 1 — Import the starter

<!-- volatile verified=2026-09 -->
Import `start/TechnikAssistant_B5_end.zip` into your developer environment as an **unmanaged**
solution. The import screens change between releases; follow the current documentation if what you
see does not match.
<!-- /volatile -->

Open the agent and ask *"What is the minimum overlay thickness?"*. Keep the answer. It has no
sources, so whatever comes back is the model filling a gap — the mechanism from
[B1](../B1/hallucination.html). You will ask the same question three more times in this
lab, and the shape of the answer should change each time.

## Step 2 — Upload the controlled documents

Add these five PDFs from `labs/_setup/documents/` as file knowledge:

| File | What it covers |
|---|---|
| `SOP70000101.pdf` | Quality Notification Handling |
| `SOP70000114.pdf` | Engineering Change Notification Process |
| `SWI70000318.pdf` | Cladding Preparation and Inspection |
| `SWI70000402.pdf` | Hydrostatic Test During Assembly and Testing |
| `DGL70000009.pdf` | Cladding Design Guidelines |

Give the knowledge source a name and description that say what is in it, not what it is:
*"Technik controlled documents: quality notification handling, engineering change process, cladding
preparation, hydrostatic testing and cladding design guidance."* The orchestrator reads that
description the same way it reads a tool description.

Wait for indexing to finish before testing. It is not instant, and "it does not work" ten seconds
after uploading is the most common false alarm in this module.

> [!NOTE]
> Uploading controlled documents is **not** what Technik would really do — uploaded files have no
> per-user permissions, so everyone who can use the agent sees everything in them. We do it here so
> the lab works on any tenant, and so you have seen the difference by the time step 4 puts content
> in SharePoint instead. The checklist asks you to write down what you would change in production.

## Step 3 — Test document grounding

Ask these five. All are answerable from the uploaded documents.

1. "What is the minimum overlay thickness?" → 3.0 mm at every measurement point, from `SWI70000318`
   §5.1
2. "Why is it 3.0 mm?" → the three allowances, from `DGL70000009` §3
3. "When must I raise a quality notification?" → `SOP70000101` §2
4. "A notification has been open for 45 days. What should happen?" → weekly quality meeting review,
   `SOP70000101` §6
5. "What pressure and hold time does the body hydrostatic test use?" → 690 bar, 60 minutes,
   `SWI70000402` §3

Check the citations, not just the answers. Questions 1 and 2 are the pair that matters: the same
subject, answered from two different documents, because one states the requirement and the other
explains it.

## Step 4 — Add SharePoint knowledge

Upload these two files from `labs/_setup/documents/sharepoint/` to a SharePoint site you control:

- `weld-overlay-acceptance.pdf` — the `TS-014` intranet standard
- `plant-safety-and-ppe.pdf` — the `TS-001` safety rules

Add that site as a SharePoint knowledge source, using a connection reference. Then ask:

6. "What PPE do I need in the coating area?" → respiratory protection, chemical-resistant gloves,
   extraction running, plus eye protection and safety footwear everywhere
7. "What is the minimum overlay thickness?" — **again**

Question 7 is the point of this step. Two sources can now answer it, and one of them is a summary of
the other.

## Step 5 — Teach it which source governs

Add to the agent's instructions:

```
Answer only from your knowledge sources. If they do not cover the question, say so plainly and do
not answer from general knowledge.

Always say which document an answer came from, by its number.

When sources disagree, prefer the controlled document over any summary of it, and say which you
used. Controlled documents are SOP, SWI, LWI, GWI and DGL numbers. Intranet pages summarise them and
may be out of date.

Quote acceptance criteria, tolerances and test parameters exactly as written. Do not paraphrase a
number.
```

Ask question 7 again. The answer should now name `SWI70000318` as the governing source, and may
mention `TS-014` as agreeing with it.

Then ask:

8. "What is the maximum ovality allowed after bending?" → this is in `SWI70000366`, which is **not**
   in your knowledge. The agent should say it cannot find it. If it produces a number, the
   abstention instruction is not working, and that is the finding.

## Step 6 — Add Snowflake work order data

Add the Snowflake connector as a **knowledge source** — not as a tool; tools are B7 — using a
connection with:

| Setting | Value |
|---|---|
| Role | `ACADEMY_AGENT_<you>` |
| Warehouse | `ACADEMY_WH_<you>` |
| Database | `AI_ACADEMY` |
| Schema | `SANDBOX_<you>` |

Select **`SAP_WORK_ORDERS`** and **`SAP_WO_OPERATIONS`**, and no other tables. Use a connection
reference.

> [!WARNING]
> Not `ACADEMY_LEARNER_<you>`, even though it would work. A read-only identity is what makes "the
> agent cannot change the data" a property of Snowflake rather than a promise in a prompt. You will
> attack this agent in B11.

## Step 7 — Watch generated SQL succeed, then fail

9. "What is the status of work order `100004521`, and which operation is it at?" → status `PCNF`,
   currently at operation 0030, Welding, in process. This works well: a lookup with an obvious
   filter, and the column comments carry the status codes.

10. "What was machining efficiency last month?" → you will get a number. **It is wrong.**

Now check it yourself, in a worksheet:

```sql
-- what the agent almost certainly computed
SELECT SUM(ROUTING_HOURS) / SUM(ACTUAL_HOURS) * 100 AS EFFICIENCY_PCT
FROM SAP_WO_OPERATIONS
WHERE OPERATION = 'Machining' AND STATUS = 'CNF';

-- what is actually true: one confirmation per operation, the latest one
SELECT SUM(ROUTING_HOURS) / SUM(ACTUAL_HOURS) * 100 AS EFFICIENCY_PCT
FROM SAP_WO_OPERATIONS
WHERE OPERATION = 'Machining' AND STATUS = 'CNF'
QUALIFY ROW_NUMBER() OVER (PARTITION BY WO_NO, OP_SEQ ORDER BY CONFIRMATION_NO DESC) = 1;

-- and here is why they differ
SELECT WO_NO, OP_SEQ, COUNT(*) AS CONFIRMATIONS
FROM SAP_WO_OPERATIONS
GROUP BY WO_NO, OP_SEQ HAVING COUNT(*) > 1 ORDER BY WO_NO;
```

Six operations were confirmed twice: a partial posting that was never reversed, then the full
re-posting. The first query double-counts both sets of hours. Across all confirmed operations the
raw figure is about **100%** and the deduplicated one about **95%**; for welding at Plant 1 it is
about **111%** against a true **89%** — an operation that looks like it beats its routing and does
not.

Do not try to fix this with a better prompt. It is fixed in B10, with a view that deduplicates
before the model ever sees a row, and B7 points its first tool at a view for the same reason.

11. Ask question 10 once more, in a new conversation. Note whether you get the same number. That,
    not the number itself, is the lesson.

## Step 8 — Describe what the agent knows

Update the agent's description so a user can tell how fresh an answer is:

```
Answers questions about Technik controlled documents, intranet standards, and work order data.
Work order data comes from Snowflake, which is refreshed from SAP overnight, so it is up to one
day old. Document answers reflect the revision currently published.
```

This is not decoration. A planner who knows the data is a day old asks a different question than one
who thinks it is live.

---

## Checklist

- [ ] All five controlled documents are uploaded and cited in at least one answer each.
- [ ] Question 1 answers **3.0 mm** citing `SWI70000318`; question 2 explains the three allowances
      citing `DGL70000009`.
- [ ] Question 6 answers from the SharePoint safety page.
- [ ] After step 5, question 7 names `SWI70000318` as governing, not `TS-014`.
- [ ] Question 8 makes the agent say it cannot find the answer. No number is invented.
- [ ] Question 9 reports work order `100004521` at operation 0030, Welding, in process.
- [ ] You have run the three queries in step 7 and can state the raw and deduplicated figures.
- [ ] Asking question 10 twice gave two different answers, or you can say why it did not.
- [ ] The agent's description states how fresh the work order data is.
- [ ] **Written down:** what you would change about the document knowledge in a real Technik
      deployment, and why. One paragraph. This is the step people skip and the one that matters.

## What you should have learned

- Grounding changes the mechanism, not just the wording. Compare the step 1 answer with the step 3
  one.
- Two sources that agree today are a problem waiting for one of them to be revised. Source
  precedence is an instruction you write before you need it.
- Abstention has to be asked for, and has to be tested with a question you know is not covered.
- Permissions are a property of the source. Uploading a controlled document is a decision about who
  may read it.
- A generated query is fine for exploring and wrong for reporting. The fix is a view, not a prompt.

## Next

`solution/TechnikAssistant_B6_end.zip` is the reference solution, and it is the starter for
[B7](../B7/index.html), where the assistant gets its first tool and finally answers
Carla's revision question properly.

Your sandbox keeps nothing from this lab — you created no objects in Snowflake. B7's step 0 resets
it anyway.
