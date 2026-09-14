> **25–30 minutes, on paper.** No Copilot Studio environment, no Snowflake access and no internet
> connection are needed. Everything you need is on this page, and every answer explains its
> reasoning. An optional extension at the end uses an assistant if you have one to hand.

This exercise is not about producing the right number. It is about building three habits you will
use in every module that follows: **estimating context before you spend it**, **reading variation
for what it is**, and **auditing an answer against its sources**.

---

## Part 1 — Estimate before you paste (8 minutes)

Below is an extract from `SWI70000318` *Cladding Preparation and Inspection*, revision B. It is
fictional, like everything else about Technik.

> **4.2 Surface preparation before overlay**
>
> Before any overlay is deposited, the prepared bore of part `P7000001042` shall be inspected
> against drawing `DU700001042` at the released revision. The surface shall be free of scale, oil and
> machining burrs. Surface roughness shall not exceed the value stated in the drawing for the bore
> zone concerned. Where a previous overlay has been removed, the base metal shall be verified by
> thickness measurement at no fewer than four points around the circumference, and the results
> recorded on the data collection point sheet `DCP70000076`.
>
> | Zone | Preparation | Inspection | Record |
> |---|---|---|---|
> | Bore zone 1 | Machine to drawing | Visual and roughness | DCP sheet, section 3 |
> | Bore zone 2 | Machine to drawing | Visual and roughness | DCP sheet, section 3 |
> | Bore zone 3 | Machine, then degrease | Visual, roughness, thickness | DCP sheet, sections 3 and 4 |
>
> Any surface that fails inspection shall be re-prepared and re-inspected before the overlay is
> started. A quality notification shall be raised where re-preparation is required more than once on
> the same part.

**Your tasks.**

1. Count the words in the extract, or estimate them by counting one line and multiplying. Then apply
   the rule of thumb from the [Tokens](tokens.html) lesson to get a token estimate.
2. Name the three things in this extract that will cost *more* tokens per character than plain
   English prose.
3. The full document is nine pages. Estimate its total tokens. If the agent's context window is
   128,000 tokens and the agent's instructions, tool descriptions and conversation history already
   take 4,000, roughly how many whole documents of this size could you put in one request — and why
   is that the wrong question to ask?

<details>
<summary>Answers and reasoning</summary>

**1.** The extract is about 170 words, counting the table cells. At roughly 1.3 tokens per word that
is **around 220 tokens**.

A real tokeniser will return somewhat more — expect 10–20% above the prose estimate for text like
this. The rule of thumb is calibrated on plain prose, and this extract is not plain prose. Use it to
catch order-of-magnitude errors, not to size something to the last token.

**2.** Three cost drivers, all visible:

- **Identifiers.** `P7000001042`, `DU700001042` and `DCP70000076` are not words the tokeniser has
  ever seen, so each is split into several fragments. Eleven characters may cost five or six tokens
  where eleven characters of prose would cost three.
- **The table.** Every `|` and every newline is a token spent on structure rather than meaning. A
  three-row table costs far more than the same information in a sentence.
- **Heading and section numbering.** `4.2`, `section 3`, `sections 3 and 4` — digits and punctuation
  tokenise poorly.

**3.** Nine pages at roughly 650 tokens a page is **about 6,000 tokens**, and the tables and
identifiers push a realistic figure closer to 7,000. With 124,000 tokens left you could fit **about
17** such documents.

And that is the wrong question, for two reasons the [Context](context.html) lesson
gives you. First, quality falls before the limit does: a clause buried at position 60,000 is
materially less likely to be used than the same clause near the start, so seventeen documents in
context is not seventeen documents the model will actually read. Second, you do not need whole
documents. You need the two or three passages that answer the question, which is a few hundred
tokens, not seven thousand. That is what B6 builds.

The habit to take away: **when you are about to paste something into a prompt, estimate it first.**
Almost every context problem you will meet started with someone not doing that.
</details>

---

## Part 2 — Read the variation (7 minutes)

Carla asks the assistant the same question three times: *"Summarise the purpose of section 4.2 of
`SWI70000318` in one sentence."* The three answers below were produced with the same model, the same
context and the same prompt. Only the sampling setting changed.

**A.** Section 4.2 sets out how the bore must be prepared and inspected before overlay is deposited,
including roughness, cleanliness and thickness checks recorded on `DCP70000076`.

**B.** Section 4.2 sets out how the bore must be prepared and inspected before overlay is deposited,
including roughness, cleanliness and thickness checks recorded on `DCP70000076`.

**C.** Before any overlay goes down, 4.2 wants the bore clean, smooth and — where an old overlay came
off — measured in at least four places, with everything written up on the DCP sheet.

**Your tasks.**

1. Two of these came from the same run at a low temperature and one from a higher one. Which is
   which, and what in the text tells you?
2. Carla will paste this sentence into a controlled document. Which setting should the agent use?
3. Suppose a fourth run returned: *"Section 4.2 requires the bore to be prepared and inspected before
   overlay, with thickness measured at no fewer than six points."* What changed, and is temperature
   the fix?

<details>
<summary>Answers and reasoning</summary>

**1.** A and B are the low-temperature pair — identical wording, because at a low temperature the
most likely token wins at nearly every step and two runs converge on the same sentence. C came from
the higher setting: the content is the same but the phrasing is looser and more conversational
("goes down", "came off", the dash aside). Note what did *not* change: C is not wrong, just
differently worded. Temperature moves style far more than it moves substance.

**2.** Low. A sentence destined for a controlled document must be reproducible, and Carla needs the
answer she reviews to be the answer that ends up in the file. Variety has no value here and one
clear cost.

**3.** The fourth answer says **six** points; the source says **no fewer than four**. That is not
variation, it is a wrong fact, and temperature is not the fix. A lower setting would make the model
say "six" *consistently*. The causes to check, in order: was section 4.2 actually in the context, or
is the model filling a gap; if it was there, did the instructions ask the model to summarise when it
should quote. This is the diagnosis from the
[Hallucinations & Grounding](hallucination.html) lesson, and Part 3 is an exercise in
doing it properly.

The habit to take away: **wording that varies is sampling; facts that vary are a grounding problem.**
Learning to tell them apart quickly will save you a great deal of time.
</details>

---

## Part 3 — Audit the answer (10 minutes)

This is the part that matters.

Carla asks: *"Which CNC program revision should machining use for `P7000001042`, and why did it
change?"*

The agent answers:

> Machining should use CNC program `T7000000217` at **revision A** for part `P7000001042`. The
> program was updated under `ECN70000051`, *Update valve block machining datum scheme*, which was
> raised after first-article findings led to a fixture redesign. The change also updated drawing
> `DU700001042` to revision C and work instruction `SWI70000318` to revision C. Work order
> `100004510` is currently running this part and is using the correct revisions.

Here is everything the agent's tools actually returned.

**From `TC_CNC_PROGRAMS`:**

| PROGRAM_NO | REVISION | PART_NO | MACHINE | RELEASE_STATUS |
|---|---|---|---|---|
| T7000000217 | A | P7000001042 | MAZAK-INTEGREX-1 | Superseded |
| T7000000217 | B | P7000001042 | MAZAK-INTEGREX-1 | Released |

**From `TC_ECNS` and `TC_ECN_AFFECTED_ITEMS`:**

| ECN_NO | TITLE | REASON | STATUS |
|---|---|---|---|
| ECN70000051 | Update valve block machining datum scheme | Fixture redesign after first-article findings | Released |

| ECN_NO | ITEM_NO | ITEM_TYPE | FROM_REV | TO_REV |
|---|---|---|---|---|
| ECN70000051 | P7000001042 | Part | B | C |
| ECN70000051 | DU700001042 | Drawing | B | C |
| ECN70000051 | T7000000217 | CNC Program | A | B |

**From `SAP_WO_OPERATIONS` for work order `100004510`:**

| OP_SEQ | OPERATION | DRAWING_NO | DRAWING_REV | CNC_PROGRAM_NO | CNC_PROGRAM_REV | STATUS |
|---|---|---|---|---|---|---|
| 0010 | Machining | DU700001042 | B | T7000000217 | A | OPEN |

**Your tasks.**

1. Mark every claim in the agent's answer as **supported**, **contradicted** or **unsupported** —
   unsupported meaning nothing in the returned data speaks to it either way.
2. For each problem, name the mechanism: was the material missing, or was it there and misused?
3. Write the answer the agent should have given.

<details>
<summary>Answers and reasoning</summary>

**1. Claim by claim.**

| Claim | Verdict |
|---|---|
| Use `T7000000217` for `P7000001042` | Supported |
| At **revision A** | **Contradicted.** A is Superseded; B is Released |
| Updated under `ECN70000051`, with that title | Supported |
| Raised after first-article findings led to a fixture redesign | Supported — it is the ECN's stated reason |
| Also updated `DU700001042` to revision C | Supported |
| Also updated `SWI70000318` to revision C | **Unsupported.** `SWI70000318` does not appear in this ECN's affected items at all. It is a real document and it really is waiting on a revision C — but under a different ECN. The agent has blended two true facts into a false one |
| Work order `100004510` is using the correct revisions | **Contradicted.** It is on drawing revision B and program revision A, both superseded |

**2. The mechanisms, and they are not the same.**

The revision error and the work-order error are **misuse of material that was present**. Both tables
were in the context. The model had two program rows and picked the first rather than the released
one; it had the work order's actual revisions and asserted the opposite. More grounding would not
have helped — the grounding was there.

The `SWI70000318` claim is **blending**: plausible, adjacent, and not in the data. This is the
failure mode that survives grounding, because nothing in the retrieved material contradicts it
loudly.

Note which error is most dangerous. The revision error is checkable in seconds. The `SWI70000318`
claim reads as a helpful extra detail and is the one a reviewer is least likely to question.

**3. A defensible answer.**

> Machining should use `T7000000217` **revision B**, the released revision for `P7000001042`.
> Revision A is superseded. The change was made under `ECN70000051`, *Update valve block machining
> datum scheme*, raised after a fixture redesign following first-article findings; the same ECN took
> drawing `DU700001042` from revision B to C.
>
> Work order `100004510` operation 0010 is currently on drawing revision B and program revision A —
> both superseded. The paperwork should be checked before machining starts.
>
> Sources: `TC_CNC_PROGRAMS`, `TC_ECNS`, `TC_ECN_AFFECTED_ITEMS`, `SAP_WO_OPERATIONS`.

Two design lessons are hiding in that answer, and both are built in B7 and B10.

- **Filter in the query, not in the prompt.** Had the tool returned only rows where `RELEASE_STATUS =
  'Released'`, the revision error could not have happened. A constraint in SQL is a guarantee; the
  same constraint in instructions is a preference.
- **The most useful part of the answer is the warning.** Work order `100004510` sitting on superseded
  revisions is the thing Carla actually needs to know, and no one asked about it. An agent that
  reports what the paperwork says, without checking it against the released revision, gives a true
  answer to the wrong question.
</details>

---

## Optional extension (10 minutes, needs an assistant)

If you have Microsoft 365 Copilot Chat or GitHub Copilot available:

1. Paste the Part 1 extract and ask for a one-sentence summary. Then ask the same thing again in a
   fresh conversation and compare the wording. You have just measured your own default temperature.
2. Ask it: *"What is the latest released revision of CNC program `T7000000217`?"* with no other
   context. It has no access to Technik data, so watch what it does with the gap — whether it says it
   cannot know, or invents an answer. Both happen, and which one you get is worth knowing about the
   tool you use every day.
3. Ask the same question again, this time pasting the `TC_CNC_PROGRAMS` table from Part 3 above it.
   You have just done grounding by hand. Everything in B6 and B7 is this, automated.

---

## Before you move on

You should now be able to answer the module's [self-check](index.html#self-check)
without looking anything up. If question 3 or 4 still feels uncertain, re-read
[Hallucinations & Grounding](hallucination.html) — it is the lesson the rest of the
Beginner track leans on hardest.

Nothing in this exercise changed any state, so there is nothing to reset. B2 needs nothing from here
except the habits.
