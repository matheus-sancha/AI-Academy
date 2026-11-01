## TL;DR

Prompt engineering asks how to word an instruction. **Context engineering** asks what the whole set
of tokens should be on each call — instructions, tool definitions, retrieved knowledge, memory,
history and tool results. Anthropic's engineering team calls it "the natural progression of prompt
engineering": "the set of strategies for curating and maintaining the optimal set of tokens
(information) during LLM inference". Two things change. The job stops being something you write
once and becomes a decision you remake every turn, because "the curation phase happens each time we
decide what to pass to the model." And the window stops being a container you fill and becomes a
budget you spend, because context must be "treated as a finite resource with diminishing marginal
returns".

## Why it matters

You have written instructions before: the Instructions field ({{topic:instructions}}), structured
with tags ({{topic:xml}}), with what each turn costs already accounted for
({{topic:contextcost}}). But the platform assembled the context. Generative orchestration chose
which knowledge and which tools to include, and you influenced that choice rather than making it.

Pro-code hands you the assembly. Nothing selects your knowledge, trims your history or decides how
many tool definitions to publish unless you write the code that does it. The context your model
sees on turn nine is whatever your code put there, and the only way to know what that is, is to be
able to read it. That is why this module comes before skills, MCP servers and multi-agent work:
each of those adds tokens to the same window, and each has to justify its share.

## How it works

### What counts as context

The definition is deliberately wide: "Context refers to the set of tokens included when sampling
from a large-language model (LLM)." For an agent that means "the entire context state (system
instructions, tools, Model Context Protocol (MCP), external data, message history, etc)" — and the
force of "including all the other information that may land there outside of the prompts" is that
most of your context is not prompt at all. The rest of this module takes the parts one at a time:
the budget they share ({{topic:budget}}), how the whole thing is laid out
({{topic:xmltemplates}}), the instruction layers ({{topic:sysprompt}}), the tools and their results
({{topic:toolshaping}}), retrieval ({{topic:jit}}), history ({{topic:history}}), memory
({{topic:memory}}), caching ({{topic:caching}}) and the fact that all of it can steer the model
({{topic:ctxsecurity}}).

### Why curation rather than accumulation

The reason to curate rather than append is that longer context gets worse before it gets full.
Needle-in-a-haystack benchmarking surfaced **context rot**: as context grows, "the model's ability
to accurately recall information from that context decreases", and "this characteristic emerges
across all models." The mechanism is framed as an "attention budget" that models "draw on when
parsing large volumes of context", where "Every new token introduced depletes this budget by some
amount" — attention relates every token to every other one, which "results in n² pairwise
relationships for n tokens" ({{topic:transformers}}).

The result is a soft limit: "These factors create a performance gradient rather than a hard cliff",
where models "remain highly capable at longer contexts but may show reduced precision for
information retrieval and long-range reasoning". So the target is not *fits in the window*. It is
"finding the smallest possible set of high-signal tokens that maximize the likelihood of some
desired outcome", noting that "minimal does not necessarily mean short".

### What the flow looks like in an editor

You already have a harness where this is a documented workflow rather than a theory. VS Code
describes context engineering as "a systematic approach to providing AI agents with targeted
project information", in three steps: curate project-wide context, generate an implementation plan,
then generate the code.

<!-- volatile verified=2026-11 -->
The mechanisms are files in the repository. A `.github/copilot-instructions.md` file holds the
always-on layer — "The instructions in this file are automatically included in all chat
interactions as context for the AI agent" — and the guide has it link out to short `PRODUCT.md`,
`ARCHITECTURE.md` and `CONTRIBUTING.md` files rather than restate them. Custom agents in
`.github/agents/*.agent.md` carry a persona and a `tools:` array, so a planning agent gets read and
search tools and no edit tool. Prompt files in `.github/prompts/*.prompt.md` are invoked by name.
The guidance on growth is strict: "Start small, keeping the initial project-wide context concise
and focused on the most critical information", and after that "only add new rules to address errors
or incorrect behavior the agent makes repeatedly". The named anti-pattern is context dumping —
"Avoid providing excessive, unfocused information that doesn't directly help with
decision-making" — and the hygiene is to "Keep different types of work (planning, coding, testing,
debugging) in separate chat sessions".
<!-- /volatile -->

The same page puts the cost plainly: "More context files, larger instruction sets, and complex
agent chains all increase token usage and AI credit consumption."


## In practice at Technik

The capstone's agent is a small, honest example of an assembled context. Everything the model sees
before the first question comes from three readable places:

*From [`agent/main.py`, lines 50–54](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/agent/main.py#L50-L54):*

```python
def build_agent(client, tools, **options):
    """The agent. Its tools are the stage 2 server: over stdio here, through the Foundry toolbox when hosted."""
    return Agent(client=client, name="technik-production-assistant",
                 instructions=INSTRUCTIONS.read_text(encoding="utf-8"),
                 tools=tools, middleware=[grounded_or_refuse], **options)
```

The first is `agent/instructions.md` — 37 lines, 301 words, 1,836 characters — read from disk at
construction. The second is the three tool definitions the MCP server publishes, each a docstring
of roughly 250 characters plus typed parameters. The third is the server's own one-sentence
`instructions` string, sent when the client connects.

What is *not* there matters as much. No documents are preloaded: the agent answers from tool results
it fetches per question. The server's prompts are switched off at the client (`load_prompts=False`
where the stdio tool is built), so they never enter the window. And the loop caps tool calls at six,
capping how many results pile up behind one answer ({{topic:loop}}).

Compare the Intermediate build of the same assistant: five tools, two SharePoint knowledge sources
and the orchestrator's scaffolding, with no file in the repository telling you what the model
received. The pro-code version is not smaller because pro-code is leaner, but because every
addition had to be written down.

## Design guidance

- **Write the context down.** If you cannot point at the files and calls producing what the model
  sees, you are not engineering it.
- **Budget before you add.** Every new tool, document or instruction block competes for the same
  attention, so ask what it displaces.
- **Grow from failures, not from imagination.** Add a rule once you have seen the agent break
  without it, which is also VS Code's advice.
- **Keep layers in separate files.** Project-wide, module-specific and task-specific context have
  different lifetimes; one blob can be neither reviewed nor reused.
- **Prefer a pointer to a payload.** A path, query or identifier the agent can resolve costs a
  fraction of the document it stands for ({{topic:jit}}).
- **Make the smallest working version the baseline**, then add only what measured failures demand.
- **Separate the sessions.** Planning, coding and debugging accumulate different context; mixing
  them pollutes all three.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Quality drops over a long session, with no code change | Context rot — recall degrades as the window fills | Compact or reset; keep per-turn context small ({{topic:history}}) |
| An instruction that worked in testing is ignored in production | It is now buried among far more tokens | Cut the context, not the instruction, then re-measure |
| Cost per answer climbs steadily | Instructions and tool definitions are re-sent every turn, and history grows | Measure each segment and trim the largest ({{topic:budget}}) |
| Nobody can say what the agent was told | Context is assembled implicitly across several call sites | Assemble it in one function and log what it produced |
| The instructions file grows and behaviour keeps drifting | Rules are added speculatively, not from observed failures | Require a reproducing case before a rule lands |
| The agent ignores a document you supplied | It arrived with everything else, so nothing marked it relevant | Retrieve it on demand, labelled ({{topic:xmltemplates}}) |

## Key terms

**Context** — every token included when sampling from the model: instructions, tool definitions,
retrieved data, history and tool results, not just the prompt.

**Context engineering** — curating the optimal set of those tokens on every call, rather than
writing one good prompt.

**Context rot** — the measured decline in a model's recall accuracy as the context it is given
grows.

**Attention budget** — the finite capacity a model draws on to relate tokens to one another, which
every added token depletes.

**High-signal tokens** — the smallest set of information that makes the desired outcome likely;
minimal, which is not the same as short.
