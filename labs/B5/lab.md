> **About 75 minutes.** You need your Power Platform developer environment and Copilot Studio.
> Budget a small number of Copilot Credits — roughly thirty test turns, all of them short.
>
> **You do not need Snowflake for this lab.** The assistant gets its first data in B6.
>
> **This lab is independent** — and unusually so, because it is the one lab with nothing to import.
> You build the agent from an empty environment, which is the start state every other lab ships in a
> zip.

## What you are building

The Technik Production Assistant, for the first time. By the end of this lab it will:

- exist, on a harness you chose on purpose and can defend;
- have instructions specific enough to change its behaviour, and short enough not to crowd out the
  answer;
- refuse to answer from general knowledge, because of a setting rather than a sentence;
- run one topic, *Work order status*, which captures a work order number, validates its format,
  remembers it, and then says plainly that it cannot look anything up yet.

That last capability is useless, and that is deliberate. You are building the front end of something
before its back end exists, so that when B6 adds knowledge and B7 adds a tool you can see exactly
which part of the behaviour came from where.

> [!IMPORTANT]
> **Step 2 contains the one irreversible decision in this course.** The harness is fixed when the
> agent is created. Read [Copilot Studio Tour](../../course/B5/tour.html) before you start, and do
> not skim step 2.

## What the starter contains

Nothing. This is the first agent, and the start state is an empty developer environment with
Copilot Studio available to you.

If you are arriving here from somewhere else and already have a *Technik Production Assistant* in
this environment, delete it or rename it before you begin. Two agents with the same name in one
environment is a problem you will meet again in B12, and it is not worth meeting twice.

## Step 1 — Create the solution

Create an unmanaged solution in your developer environment before you create anything else.

| Field | Value |
|---|---|
| Display name | `Technik AI Academy` |
| Name | `TechnikAIAcademy` |
| Publisher | Your own publisher, with a prefix you recognise — not the default `CDS Default Publisher` |

Everything you build in the Beginner track goes in this solution. An agent created outside one
cannot move cleanly to another environment, and retrofitting it is real work — B12 covers why.

<!-- volatile verified=2026-09 -->
Whether you create the solution in the Power Apps maker portal or from within Copilot Studio, and
where the option sits, changes between releases. Either route is fine; what matters is that the
agent ends up inside a custom solution with your own publisher prefix.
<!-- /volatile -->

## Step 2 — Create the agent

Create the agent **inside the solution** you just made.

| Setting | Value |
|---|---|
| Name | `Technik Production Assistant` |
| Harness | **Standard** |

<!-- volatile verified=2026-09 -->
The creation flow asks you to describe the agent in natural language and drafts a name, description
and instructions from it. Where the harness choice appears in that flow changes between releases. If
you do not see it, find it before you finish creating — it cannot be changed afterwards, and getting
it wrong means deleting the agent and starting again.
<!-- /volatile -->

Use this as the description you type:

```
An internal assistant for Technik manufacturing and engineering staff: production planners,
quality engineers, manufacturing engineers and supervisors. It answers questions about work orders,
manufacturing operations, quality notifications, controlled documents and Teamcenter revisions.

It answers only from the knowledge and tools it has been given, and says plainly when it cannot
find something rather than guessing. It never invents a part number, drawing number, work order
number or measurement.

It is concise and factual, writes in British English, and does not use exclamation marks or
enthusiasm. It is a tool people use dozens of times a day.

It does not answer questions about pay, HR policy, or anything outside manufacturing and
engineering. When asked, it says so and suggests the intranet.
```

Then, before you move on, **write the harness reasoning into the agent's own description field**:

```
Built on the standard harness because it needs topics: the work order intake is a scripted exchange
that must run the same way every time. The cost is that it cannot hold skills (see B8) — those go on
a separate agent that this one delegates to.
```

That sentence is the whole point of this step. In six months the person asking "why can't this one
have skills?" will be looking at the agent, not at your notes.

## Step 3 — Replace the drafted instructions

Copilot Studio will have drafted instructions from your description. They will be reasonable,
generic and unbounded. Replace them entirely with this:

```xml
<identity>
You are the Technik Production Assistant, an internal assistant for Technik manufacturing and
engineering staff: production planners, quality engineers, manufacturing engineers and supervisors.
</identity>

<scope>
You answer questions about work orders, manufacturing operations, quality notifications, controlled
documents and Teamcenter part, drawing and document revisions.
You do not answer questions about pay, HR policy, or anything outside manufacturing and engineering.
When asked one, say so in one sentence and suggest the intranet.
</scope>

<grounding>
Answer only from the knowledge and tools you have been given.
If they do not cover the question, say so plainly. Do not answer from general knowledge.
Never invent a part number, drawing number, work order number, document number or measurement.
</grounding>

<style>
Be concise and factual. Write in British English.
Do not use exclamation marks or enthusiasm.
Prefer a short table to a paragraph when reporting more than two facts.
</style>
```

Around 160 words. It will roughly double by B11, and that is close to the sensible limit — the
reasoning is in [Instructions](../../course/B5/instructions.html).

Note what is **not** in there: nothing about work orders being nine digits, because that is the
topic's job in step 6, and nothing about which source wins, because there are no sources yet. B6
adds that rule when it is earned.

## Step 4 — Set the generative AI settings

Open the agent's settings and set:

| Setting | Value |
|---|---|
| Orchestration | **Generative** |
| General knowledge | **Off** |
| Web search | **Off** |
| Content moderation | Leave at the default — you will test it in step 5 |
| Response format | Markdown, if it is offered |

<!-- volatile verified=2026-09 -->
These settings have moved between the agent settings page and a generative AI or orchestration page
more than once, and their names have changed with them. Find the four above by what they do; the
linked documentation has the current names and locations.
<!-- /volatile -->

**General knowledge off is the load-bearing one.** Your instructions already say "do not answer from
general knowledge". That is a request. This is the mechanism.

## Step 5 — Establish a baseline

Ask these five, in a fresh conversation, and keep every answer. Five minutes now saves an hour in
B6.

1. **"What is the minimum overlay thickness?"**
   Expected: it cannot find that in its sources. **Keep this answer verbatim** — B6, B7 and B8 each
   ask it again, and the four answers side by side are the clearest evidence in the Beginner track
   that grounding changed the mechanism and not just the wording.
2. **"What do I do about porosity found during cladding inspection?"**
   Expected: the same abstention. This one is also your moderation check: *porosity*, *defect* and
   *rejection* are ordinary words here and sit close to what moderation systems watch for. If this
   is blocked rather than answered, moderation is stricter than your vocabulary — note it, and read
   [Generative AI Settings](../../course/B5/genai.html) before changing the level.
3. **"How much holiday do I get?"**
   Expected: one sentence saying it does not cover HR, pointing at the intranet. This tests the
   `<scope>` boundary.
4. **"Tell me about subsea christmas trees."**
   Expected: this is the interesting one. It is in scope *as a subject* and not in its sources. A
   general answer about subsea equipment means general knowledge is still reaching the model — go
   back to step 4.
5. **"Write me a poem about welding."**
   Expected: a refusal or a redirect, not a poem. Not because poems are harmful, but because an
   internal tool that does this is an internal tool people stop trusting to be literal.

Open the activity map on questions 1 and 4. Both should show **nothing retrieved and no tool
called** — the map that [Testing in the Preview Pane](../../course/B5/test.html) describes. Question
1 is correct with that map; question 4 is only correct if the answer matches it.

## Step 6 — Build the *Work order status* topic

Create a topic named `Work order status`.

### Trigger phrases

Write them the way people type in Teams, not the way examples are written:

```
status of work order
where is work order
what's the status of 100004521
is 100004512 finished
work order status
where has this WO got to
which operation is 100004506 on
has work order 100004503 been confirmed
```

Two of those have no work order number in them, on purpose. The topic has to work either way.

### Nodes

Build this path:

| # | Node | Detail |
|---|---|---|
| 1 | **Trigger** | The phrases above |
| 2 | **Condition** | Did the trigger capture a work order number? If yes, set `Global.WorkOrderNo` and go to 5 |
| 3 | **Question** | *"Which work order? Give me the nine-digit number."* Store the reply in `Topic.Answer` |
| 4 | **Set variable** | `Global.WorkOrderNo = Trim(Topic.Answer)` |
| 5 | **Condition** | `IsMatch(Global.WorkOrderNo, "^\d{9}$")` |
| 6 | **Message** (false branch) | *"`{Global.WorkOrderNo}` doesn't look like a Technik work order number — those are nine digits. Part numbers start with P70000 and are eleven characters."* Then back to node 3 |
| 7 | **Message** (true branch) | *"Work order `{Global.WorkOrderNo}`. I can't look up work order status yet — I don't have access to the production data. Ask me again once that's connected."* |

<!-- volatile verified=2026-09 -->
How a trigger hands a captured value to the topic — entities, slot filling, or the orchestrator
passing it — has changed between releases, and node 2 depends on it. If you cannot make the
capture work, build the topic so it always asks (delete node 2, start at node 3) and note it in
your checklist. The rest of the lab is unaffected.
<!-- /volatile -->

Put an **attempt limit on node 3**: after two failed tries, say you cannot get a valid number and
end the topic. A question node that re-asks forever is the most common way a topic traps a user.

Three things in this small topic are worth naming as you build them, because each is a decision you
will make again:

- **It validates the format in Power Fx, not in an instruction.** `IsMatch` is true or false. An
  instruction is usually obeyed.
- **It stores the number globally.** Ana asks two or three follow-ups about the same work order, and
  re-asking every time is the fastest way to make an agent annoying.
- **It says plainly what it cannot do.** The honest apology is the whole deliverable of this lab.

## Step 7 — Test the topic

Run all six, and read the activity map on at least the first three.

| # | Say | Expected |
|---|---|---|
| 1 | "What's the status of work order 100004521?" | The topic fires, `Global.WorkOrderNo` = `100004521`, node 7's message |
| 2 | "Where is work order P7000001088?" | Node 6 rejects it, then asks again. `P7000001088` is a **part** number, and this is what people actually type |
| 3 | "Work order status" | No number captured, so node 3 asks. Answer `100004506` and you should reach node 7 |
| 4 | "Where is it?" as a follow-up to test 1 | `Global.WorkOrderNo` is still set. Note whether the agent uses it — with generative orchestration the variable is available, not compulsory |
| 5 | "What's the status of 999999999?" | Node 7's message, with the number confirmed back |
| 6 | "Has work order 12345 been confirmed?" | Node 6 rejects it — five digits, not nine |

**Test 5 is the one to think about.** `999999999` is nine digits and is not a work order. The topic
accepts it, because format validation is not existence validation and nothing in this agent can tell
the difference yet. That is a correct outcome today and a real gap: B6 gives the agent the work order
data that makes "no such work order" an answer it can actually give. Write down which of your six
tests would change once that data exists.

## Step 8 — Customise the fallback topic

Open the system **fallback** topic — what the agent says when nothing matched — and replace its
message:

```
I couldn't work out what you're asking for. I can help with work orders, manufacturing operations,
quality notifications, controlled documents and Teamcenter revisions. Try naming the work order or
document you mean.
```

This is your agent's worst moment, it ships with generic wording, and almost nobody changes it. It
costs two minutes.

## Step 9 — Record the model

Find the agent's primary model and **write down which one it is**, next to the five baseline answers
from step 5.

Do not change it. You have nothing to measure a change against — that is the argument in
[Model Selection](../../course/B5/model.html), and B13 is where it gets settled properly. What
matters now is that a result you might rely on in B6 is recorded together with the model that
produced it.

## Step 10 — Start the question list

You now have eleven questions with known expected answers: the five from step 5 and the six from
step 7. Put them in a file, with what you expect and what you got.

That file is the single most useful artefact this lab produces. It becomes the evaluation set in
B13, it is what tells you whether B6 improved things or only changed them, and it is far easier to
write now than to reconstruct from memory in eight modules' time.

---

## Checklist

- [ ] The agent exists **inside a custom solution**, with your own publisher prefix.
- [ ] Its harness is **standard**, and the reason is written in the agent's own description field.
- [ ] The instructions are the four-section block from step 3, not the drafted ones.
- [ ] General knowledge and web search are **off**.
- [ ] Step 5 question 1 produced an abstention, and you have kept the exact wording.
- [ ] Step 5 question 4 did **not** produce a general answer about subsea equipment.
- [ ] Step 5 question 2 was answered rather than blocked, or you have noted that moderation blocked
      it.
- [ ] The *Work order status* topic fires on all eight trigger phrases.
- [ ] A part number (`P7000001088`) is rejected with the message from node 6.
- [ ] A five-digit number is rejected; a nine-digit one is accepted.
- [ ] The question node gives up after two failed attempts instead of looping.
- [ ] The fallback topic no longer uses its default wording.
- [ ] The primary model is written down next to the baseline answers.
- [ ] **Written down:** which of your six topic tests would change once the agent has work order
      data, and why. Test 5 is the one to start from.

## What you should have learned

- The harness decision is made in the first two minutes and comes due three modules later. Recording
  *why* is what makes it a decision rather than an accident.
- Instructions influence; a topic runs; a setting guarantees. The same rule — "don't answer from
  general knowledge" — lives in all three places in this lab, and only one of them enforces it.
- Validation belongs in Power Fx at the point of capture, where it is deterministic and cheap.
- Format validation is not existence validation. Knowing which one you have is most of knowing what
  your agent can promise.
- The activity map for a correct abstention and for a confident invention look nearly identical. The
  answer and the map are two different pieces of evidence and you need both.
- An agent that honestly says it cannot help is a better foundation than one that plausibly says
  anything.

## Next

`solution/TechnikAssistant_B5_end.zip` is the reference solution, and it is the starter for
[B6](../B6/index.html), where the assistant gets five controlled documents, a SharePoint site and
its first look at Snowflake — and answers the overlay thickness question properly.

The *Work order status* topic stays in place for the rest of the Beginner track. It barely changes
again; what changes is what the agent can do with `Global.WorkOrderNo` once something is on the
other end of it.
