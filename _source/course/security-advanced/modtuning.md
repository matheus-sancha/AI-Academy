## TL;DR

Content moderation is a threshold, and a threshold has two errors: it lets harm through, and it
refuses legitimate work. Intermediate measured the second with a vocabulary set on one agent-wide
level ({{topic:moderation}}). Advanced adds granularity: Copilot Studio sets a level at the agent,
the topic and the prompt, with the narrowest winning, and Foundry sets a blocking level per harm
category on a guardrail you assign. Tuning means choosing a setting per surface, keeping the
evidence, and testing both directions after every change. Microsoft's own advice for a filtered
answer is modest: reinforce guidelines with users, then optionally adjust the threshold.

## Why it matters

A moderation setting made once, at the default, is a decision nobody made. Technik's records are
full of words that sit near a classifier's edge: a seal that "blew out", a technician "struck" by a
fitting, a test that "failed catastrophically". The same level that is right for a chat answer can be
wrong for a prompt that summarises an incident note. A record of why each setting is what it is
costs an hour, and it is the difference between a tuned system and one that merely hasn't been
complained about.

## How it works

### Three places in Copilot Studio, one winner

The troubleshooting page sends you to the knowledge-sources page for the settings, which lists three:
"The setting in the **Generative AI** settings page sets the moderation at the agent level", the
generative answers node "sets the moderation at the topic level", and the prompt tool's setting
"sets the moderation at the prompt level". At runtime, "the setting at the topic level takes
precedence", and a prompt tool overrides both when its **Completion** setting is set to send a
specific response.

The levels run from **Lowest** to **Highest**, and "The default moderation level is **High**." The
direction of the trade is stated plainly: the lowest level "generates the most answers, but they might
contain harmful content".

<!-- volatile verified=2026-11 -->
These pages describe the standard harness, where topics and prompt tools exist. The GitHub Copilot
harness has one agent-wide level and no topics ({{topic:moderation}}). A per-prompt setting is
therefore a decision for standard-harness agents and for prompts built in a prompt tool.
<!-- /volatile -->

### Finding out what was filtered

A filtered turn ends with "The content was filtered due to Responsible AI restrictions", code
`ContentFiltered`. The page says content "is evaluated twice: once at the stage of user input and
again before the agent provides a response", so the code does not say which stage fired. Its
diagnosis route has two parts: Application Insights, and conversation transcripts. The query it
gives is:

*Adapted from the sample on [Resolve responsible AI content filter errors](https://learn.microsoft.com/en-us/troubleshoot/power-platform/copilot-studio/generative-answers/agent-response-filtered-by-responsible-ai):*

```kusto
customEvents
| where customDimensions contains "ContentFiltered"
```

Its fix is two sentences long. First, "reinforce responsible AI guidelines with your agent users".
Second, "optionally", update the content moderation policies "to adjust the filtering threshold for
your specific use case". It does not tell you to lower the level, and it does not say what to
test afterwards. That part is yours.

### Per category on Foundry

A Foundry guardrail does not have one dial. The four harm categories each take a blocking level of
Off, Low, Medium or High, where Low "blocks high-severity content only" and High "blocks low-,
medium-, and high-severity content." Content classed **Safe** is always annotated and never blocked.
User prompt attacks and indirect attacks are separate controls in the same list, so a harm level you
lower for vocabulary is not the setting that governs them ({{topic:contentsafety}}). An agent
inherits its model's guardrail unless you assign it a custom one, which is how one agent gets
different levels from its neighbour.

<!-- unknown since=2026-10 -->
For Copilot Studio, nothing documents whether a moderation level changes how strictly prompt and
document attacks are detected. Until it does, assume it might, and test attack probes after
any change to the level.
<!-- /unknown -->

### What moderation is still not

The generative answers FAQ says the system "doesn't perform an accuracy check" and that its filters
"aren't foolproof". Tuning moves a threshold. It does not turn a filter into a fact-checker, and it
does not replace the controls in {{topic:threats}}.

## In practice at Technik

Suppose a quality lead wants a prompt that turns a hydrostatic test incident note into the first
draft of a QN write-up. A typical note reads: *Seal on test fixture failed at hold, fitting struck
the operator's glove, no injury, area isolated.* Technik runs three surfaces, and the decision
record states each one.

| Surface | Setting | Reason and evidence | Re-test when |
|---|---|---|---|
| Production Assistant, one agent-wide level | The level the vocabulary set justified | Twenty engineers' questions, no `CONTENT_FILTERED` ({{topic:moderation}}) | Instructions or model change |
| Incident-note prompt (standard harness) | One step below the agent, if the set shows refusals | Twenty invented notes, all passed at the lower level, and eight probes still blocked | The prompt, the model or the note format changes |
| Capstone's Foundry deployment | The default guardrail, unchanged | No vocabulary set was run, and the capstone never ran live | A tool returns prose |

The second row is a hypothesis until someone runs the two sets, and the record should say so. Each
change needs a *must pass* set of legitimate notes and a *must block* set of harmful requests and
injection probes, with the result of both written down. Lowering a threshold for the first set while
leaving the second unchecked is the failure mode.

One property of the capstone matters here. Its offline run replays a scripted model against a fake
Snowflake ({{topic:evalharness}}), so nothing in that run can trip a filter. A moderation test needs
a live model, so a `must pass` set lives in the live job, alongside the cases that can only run
there. The capstone has no such case.

## Design guidance

- **Set moderation per surface** and write down why, with the evidence that justified it.
- **Fix scope before strictness**: clearer instructions first, a lower level last.
- **Keep two sets**, legitimate content that must pass and harmful content that must still be blocked, and re-run both.
- **Diagnose before you tune.** Find the filtered turn and its stage in Application Insights or the transcript.
- **Tune the narrowest surface that needs it**, a prompt before an agent and a category before a guardrail.
- **Re-test after any change** to the model, the prompt or the level.
- **Treat the default as untested**, not as safe.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A prompt ignores the agent's level | A node or prompt tool sets its own, and the narrower setting wins | Check the topic and the prompt first |
| One category was lowered and attacks now get through | The probes were not re-run | Keep the *must block* set and run it every change |
| The same filtered error, and no clue where | The code does not name the stage or category | Query `ContentFiltered` events and read the transcript |
| The filter "fixes" a record that is really hostile | A record in the data, not the vocabulary, trips it | Read the record ({{topic:injection}}) |
| An offline run is green and the filter blocks in production | A scripted model cannot trip a filter | Test moderation in the live job |

## Key terms

**Moderation level** — how strict the filter is: Lowest to Highest in Copilot Studio, Off to High per category on Foundry.

**Topic-level precedence** — the narrower setting wins at runtime, with the agent level the fallback.

**Decision record** — a written account of each surface's setting, the evidence for it and the event that triggers a re-test.

**Must-pass and must-block sets** — legitimate and harmful cases, run together so one change cannot loosen the other.
