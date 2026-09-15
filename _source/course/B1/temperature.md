## TL;DR

At every step the model produces a probability for each possible next token. **Temperature** decides
how much that distribution is flattened before one is picked: near zero, the most likely token almost
always wins and output is focused and repeatable; higher, and less likely tokens get a real chance,
which reads as variety and creativity. **Top-p** is a related control that limits the choice to the
smallest set of tokens covering a given share of the probability. For the work in this course the
useful advice is short: keep it low, and know that many reasoning models ignore the setting
entirely.

## Why it matters

Temperature is the setting people reach for when an agent gives a bad answer, and it is almost never
the cause. Turning it down makes a wrong answer *consistently* wrong. Turning it up makes a correct
answer *occasionally* wrong. Understanding what it actually does saves you from tuning the one knob
that will not fix your problem — and lets you use it deliberately for the cases where it helps.

It also explains something that unsettles people the first time they meet it: the same prompt giving
different answers is not a bug, and no setting makes it perfectly deterministic.

## How it works

After the model computes a score for every token in its vocabulary, those scores are converted into
probabilities. Temperature scales them first:

- **Low (0 to about 0.3)** — the gap between the best token and the rest is exaggerated. The top
  choice nearly always wins. Output is focused, conventional and close to repeatable.
- **Medium (about 0.7)** — a common default. Reasonable alternatives get a fair chance. Text reads
  more naturally and varies between runs.
- **High (1.0 and above)** — the distribution flattens. Unlikely tokens get picked. Output becomes
  varied, then loose, then incoherent.

**Top-p** (nucleus sampling) works differently: it sorts tokens by probability and keeps only the
smallest group whose probabilities add up to *p*, sampling from that. Top-p 0.1 considers only the
most likely handful; top-p 1.0 considers everything. Tune one or the other, not both — changing both
at once makes the effect impossible to reason about.

Two things are worth being precise about.

**Temperature 0 is not determinism.** It makes the most likely token overwhelmingly likely, and in
practice output is stable, but ties, floating-point behaviour and infrastructure differences mean
identical output is not guaranteed. Never design a system whose correctness depends on byte-identical
responses.

**Temperature does not change what the model knows.** It changes which of the candidates it
considers gets chosen. If the right answer is not among the plausible continuations, no temperature
setting will produce it.

<!-- volatile verified=2026-09 -->
In Copilot Studio you do not set temperature on the agent itself. You control it where prompts are
authored — in the prompt editor's model settings, and in AI Builder prompts — and through the choice
of model for the agent. Reasoning models generally do not expose temperature at all, and will ignore
it if it is supplied. Check the linked documentation for the current surface before you go looking
for a slider that may not be there.
<!-- /volatile -->

## In practice at Technik

Four Technik tasks, four different answers about temperature.

| Task | Setting | Why |
|---|---|---|
| Read back the status of work order `100004521` | Lowest available | There is one right answer. Variation is pure downside, and the answer must be the same for Ana at 09:00 and her supervisor at 09:05 |
| Extract fields from a supplier material certificate into JSON (B9) | Lowest available | Structured output consumed by a flow. A creative variation is a broken flow |
| Draft a quality notification write-up in Technik's format (B8) | Low to moderate | The format is fixed, but the prose describing a defect benefits from a little natural variation |
| Suggest possible causes for repeated overlay porosity | Moderate | You want a range of hypotheses, not the single most predictable one. This is the only case on the list where variety is the point |

Note what is *not* on the list: nothing is improved by a high temperature. In an internal engineering
assistant, "creative" is rarely a compliment.

There is one more Technik-specific reason to stay low. Identifiers like `DU700001042` tokenise into
fragments, and at higher temperatures the chance of sampling a wrong digit somewhere in that sequence
is no longer negligible. A drawing number that is right 98% of the time is not usable.

> [!WARNING]
> A low temperature is not a defence against hallucination. It makes the model's inventions stable
> and confident rather than varied. The fix for invented content is grounding, every time.

### Telling variation from error

Carla asks the assistant the same thing three times: *"Summarise the purpose of section 4.2 of
`SWI70000318` in one sentence."* Same model, same context, same prompt; only the sampling setting
changed between runs.

| Run | Answer |
|---|---|
| A | Section 4.2 sets out how the bore must be prepared and inspected before overlay is deposited, including roughness, cleanliness and thickness checks recorded on `DCP70000076`. |
| B | Section 4.2 sets out how the bore must be prepared and inspected before overlay is deposited, including roughness, cleanliness and thickness checks recorded on `DCP70000076`. |
| C | Before any overlay goes down, 4.2 wants the bore clean, smooth and — where an old overlay came off — measured in at least four places, with everything written up on the DCP sheet. |

A and B are the low-temperature runs: identical wording, because the most likely token wins at nearly
every step and the two runs converge. C came from a higher setting. The phrasing is looser ("goes
down", "came off"), but the content is the same and nothing in it is wrong. Temperature moves style
far more than it moves substance. Carla is pasting this sentence into a controlled document, so the
low setting is the right one: the answer she reviews has to be the answer that ends up in the file.

Now suppose a fourth run says the thickness must be measured at *no fewer than six points*. The
source says four. That is not variation, it is a wrong fact, and a lower temperature would only make
the model say "six" consistently. The cause is in the context — was section 4.2 actually retrieved,
and was the model told to quote rather than summarise? That diagnosis belongs to
[Hallucinations & Grounding](hallucination.html).

The rule to keep: **wording that varies is sampling; facts that vary are a grounding problem.**

## Design guidance

- **Default to low** for anything an engineer will act on.
- **Raise it only where variety is the goal** — brainstorming causes, generating test questions,
  drafting alternative wordings.
- **Change one knob at a time**, temperature or top-p, and re-test with a fixed set of questions
  afterwards.
- **Do not tune temperature to fix accuracy.** If answers are wrong, the cause is missing or wrong
  context, not sampling.
- **Re-evaluate after any change**, including a model change. Behaviour shifts even when your
  instructions do not (B13).
- **Record the setting** alongside your evaluation results. A test run whose temperature you cannot
  reconstruct tells you nothing later.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The same question gives different answers | Normal sampling behaviour | Lower the temperature for repeatable tasks; evaluate over a test set, not single runs |
| Output is repetitive and flat | Temperature too low for a task that wants variety | Raise it modestly, or vary the prompt instead |
| JSON output is occasionally malformed | Sampling picked an unlikely token inside the structure | Lowest temperature, an explicit schema, and validate in the flow rather than trusting the model |
| Changing temperature did not fix wrong answers | It never does. The problem is the context | Ground the agent; check what the tool actually returned |
| The temperature setting appears to do nothing | A reasoning model that ignores it, or a surface that does not expose it | Check the model's documentation; change model rather than hunting for the setting |
| Answers drifted after a model change, with identical settings | Models differ in how they respond to the same temperature | Re-tune and re-evaluate per model |

## Key terms

**Temperature** — a scaling factor applied to token probabilities before sampling. Low is focused,
high is varied.

**Top-p (nucleus sampling)** — restricts sampling to the smallest set of tokens whose probabilities
sum to *p*.

**Greedy decoding** — always taking the single most likely token; what temperature 0 approximates.

**Sampling** — choosing the next token from the probability distribution rather than always taking
the top one. The reason answers vary.

**Determinism** — producing identical output for identical input. Not something an LLM guarantees,
at any setting.
