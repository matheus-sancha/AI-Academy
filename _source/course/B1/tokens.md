## TL;DR

Models do not read characters or words. They read **tokens** — chunks of text produced by a
tokeniser, usually a few characters long. In English prose one token averages about four characters,
or roughly three quarters of a word. Tokens are the unit of three things you will care about every
day: **cost**, **speed** and **how much fits**. Learning to estimate them turns "the agent got slow
and expensive" from a mystery into arithmetic.

## Why it matters

Everything you send and everything you get back is billed, timed and limited in tokens. When a
Technik work instruction is 9,000 tokens and the model's usable window is 128,000, you know
immediately that you can afford to include about a dozen of them, not a hundred. When an agent that
answered in two seconds starts taking twelve, the first question is what grew — and the answer is
almost always the number of tokens going in.

Token counting is also the quiet reason RAG exists. If you could paste every Technik document into
every request, you would. You cannot, so you retrieve the relevant pieces instead (B6).

## How it works

A tokeniser splits text using a vocabulary learned from data, so that common sequences become single
tokens and rare ones are split into several. The practical consequences:

- **Common English words are one token each.** "the", "welding", "inspection".
- **Rarer words split.** "hydrostatic" may become two or three tokens.
- **Identifiers split badly.** `P7000001042` is not a word the tokeniser has ever seen, so it is
  chopped into several pieces — often one per digit group. Technik part, drawing and document
  numbers are expensive per character, and models are correspondingly worse at manipulating them
  than at handling prose.
- **Whitespace and punctuation count.** A token frequently includes its leading space.
- **Non-English text costs more.** The same sentence in Portuguese typically uses noticeably more
  tokens than in English, because the vocabulary is dominated by English.
- **Tables and JSON are expensive.** Every `|`, `{`, `"` and newline is tokens spent on structure
  rather than content.

### Rules of thumb

| Quantity | English prose |
|---|---|
| 1 token | ~4 characters |
| 1 word | ~1.3 tokens |
| 100 words | ~130 tokens |
| 1 page (about 500 words) | ~650 tokens |
| A 10-page work instruction | ~6,500 tokens, more with tables and part numbers |

These are estimates, not measurements. When a number matters — you are close to a limit, or sizing a
bill — count rather than guess. Both input and output are tokens, and output is usually billed at a
higher rate, so "be concise" is not only a style preference.

## In practice at Technik

Take `SWI70000318` *Cladding Preparation and Inspection*: nine pages, with two tables of acceptance
criteria and a list of part numbers. Estimated at 650 tokens a page that is about 5,900 tokens; the
tables and the identifiers push it closer to 7,000.

Now think about what the Technik Production Assistant actually sends when Carla asks a question
about cladding preparation:

| Part of the request | Approximate tokens |
|---|--:|
| Agent instructions | 700 |
| Tool and knowledge descriptions the orchestrator can choose from | 900 |
| Retrieved passages from `SWI70000318` and `DGL70000009` | 2,500 |
| The result of one Snowflake query (30 rows) | 1,800 |
| Conversation so far | 1,200 |
| Carla's question | 40 |
| **Total input** | **~7,100** |

Two things fall out of that table immediately. First, Carla's actual question is under one percent of
what the model reads — the agent's own configuration and the retrieved material dominate. Second,
the SQL result is larger than the documents. A query that returns 300 rows instead of 30 would add
roughly 18,000 tokens, and that single design decision would cost more than everything else on the
list combined. A2 in the Advanced track is about exactly this budget; B10 is about not returning 300
rows in the first place.

> [!TIP]
> When an agent feels slow, look at what it is *reading*, not at what it is *writing*. Users notice
> the answer; the cost is almost always on the way in.

## Design guidance

- **Estimate before you paste.** Words ÷ 0.75 is close enough to catch order-of-magnitude mistakes.
- **Return the smallest useful result.** Select the columns you need, filter in SQL, aggregate in the
  database. A tool that can return an unbounded number of rows is a cost incident waiting to happen.
- **Prefer a view over a raw table.** Fewer columns and shorter names are fewer tokens on every
  single call, forever.
- **Do not re-send what has not changed.** Long conversation histories are re-read in full on every
  turn; summarise or trim rather than accumulating.
- **Watch identifiers.** If a task involves comparing or transforming part numbers, expect the model
  to be less reliable than it is with prose, and prefer a tool or SQL to do the comparison.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Costs rise sharply after adding a knowledge source | Every request now carries retrieved passages | Tune how many passages are retrieved; check chunk size (A8) |
| Responses slow down as a conversation continues | History is re-sent on every turn and keeps growing | Trim or summarise history; start a new conversation for a new task |
| One tool call costs more than the rest of the agent | Unbounded query results | Add a row limit and select fewer columns (B10) |
| The model mangles part numbers — swaps digits, invents a suffix | Identifiers tokenise into fragments the model manipulates poorly | Never ask it to compute an identifier; look it up with a tool and have the model quote it back |
| A prompt that works in English fails in Portuguese at the same length | The same text is more tokens, and may now exceed a limit | Measure in tokens, not characters |

## Key terms

**Token** — the unit a model reads and writes. Roughly four characters of English.

**Tokeniser** — the component that converts text to tokens and back, using a fixed learned
vocabulary.

**Input tokens / output tokens** — what you send and what is generated. Billed separately, usually
at different rates.

**Token limit** — the maximum number of tokens a single request may contain, input and output
together. See [Context & Context Window](context.html).
