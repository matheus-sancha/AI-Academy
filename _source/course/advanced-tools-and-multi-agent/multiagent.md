## TL;DR

Five patterns are documented — sequential, concurrent, group chat, handoff and magentic — and
choosing between them is the easy part. The hard part is the page's opening instruction: "Before you
adopt a multiagent orchestration pattern, evaluate whether your scenario requires one. ... Use the
lowest level of complexity that reliably meets your requirements." A single agent with tools is
"Often the right default for enterprise use cases", and the documented justification for more is
never ambition: it is that one agent "can't reliably handle certain tasks due to prompt complexity,
tool overload, or security requirements."

## Why it matters

{{topic:connected}} gave you child and connected agents and the failure to design against — an agent
that hoards work it should pass on, or passes on work it should have done. This lesson is that
judgement with the arithmetic attached, because orchestration "Adds coordination overhead, latency,
and failure modes."

The spectrum has three rungs. A direct model call is "The least complex option. If prompt engineering
can solve the problem, you don't need an agent." Then a
single agent with tools, "Simpler to debug and test than multiagent setups, but still supports
dynamic logic." Only then orchestration — and the argument against splitting early is explicit:
"Decision-making and flow-control overhead often exceed the benefits of breaking the task into
multiple agents."

## How it works

### The five patterns, and what each one is sold on

**Sequential** chains agents "in a predefined, linear order", and the routing is yours rather than
the model's: "The choice of which agent gets invoked next is deterministically defined as part of the
workflow and isn't a choice given to agents in the process." Its listed risks are "Failures in early
stages propagate. No parallelism."

**Concurrent** "runs multiple AI agents simultaneously on the same task", and they are isolated —
agents "operate independently and don't hand off results to each other". You own the merge, which is
why its risks are "Requires conflict resolution when results contradict. Resource-intensive."

**Group chat** puts agents in "a shared conversation thread where they collaborate through
discussion", with "A chat manager" deciding who speaks. Agents here "are typically in a *read-only*
mode" — they discuss rather than act — and the advice is blunt about scale: "consider limiting group
chat orchestration to three or fewer agents." Its special case is the **maker-checker loop**, where a
checker returns work "until the checker approves the result or the orchestration reaches a maximum
iteration limit".

**Handoff** is "dynamic delegation of tasks between specialized agents", one at a time: "Full control
transfers from one agent to another agent." Its avoid-when list holds the sentence most teams need:
"The appropriate agent, or sequence of agents, is identifiable from the initial input. In that case,
use deterministic routing or a simpler dispatcher."

**Magentic** is for "open-ended and complex problems that don't have a predetermined plan of
approach", where a manager agent builds a task ledger as it goes. Its agents "typically have tools
that help them make direct changes in external systems", and its risks are "Slow to converge. Stalls
on ambiguous goals."

Three of the five share a documented failure: a loop. Infinite handoff loops, conversation loops,
stalls with no resolution — so an iteration cap and a termination rule complete the pattern rather
than polish it.

### What it costs, and where the context goes

"Multiagent orchestrations multiply model invocations, and each agent consumes tokens for its
instructions, context, reasoning, and tool interactions", and "context windows can grow rapidly
because each agent adds its own reasoning, tool results, and intermediate outputs". Everything
{{topic:budget}} and {{topic:history}} taught now applies per agent and again across the seams.

The handoff decision is a context decision: "decide what context the next agent requires to be
effective. In some scenarios, you need the full, raw context gathered so far. In other scenarios, a
compacted version ... is more appropriate. If your agent can work without accumulated context and
only requires a new instruction set, take that approach." Two mitigations are named — match each
agent's model to its task, since "Not every agent requires the most capable model", and "apply
context compaction between agents" ({{topic:jit}}).

### Reliability and security do not split cleanly

The reliability guidance reads like distributed systems because it is: timeouts, retries, graceful
degradation, circuit breakers, checkpoints, and the one that bites hardest — "Validate agent output
before you pass it to the next agent. Low-confidence, malformed, or off-topic responses can cascade
through a pipeline."

Security does not decompose at all. "Security trimming must be implemented in every agent in the
pattern", and guardrails belong "at multiple points in the orchestration, including user input, tool
calls, tool responses, and final output", because "Intermediate agents might introduce or propagate
harmful content" ({{topic:dlpdesign}}). Testing shifts too: outputs are nondeterministic, "so use
scoring rubrics or language-model-as-judge evaluations rather than exact-match assertions"
({{topic:llmjudge}}).

<!-- unknown since=2026-11 -->
Three things the source does not give. No numeric iteration limit, timeout or retry count anywhere —
every cap is yours to choose. No mention of Copilot Studio, so {{topic:connected}}'s child and
connected agents map onto these patterns by resemblance only. And nothing says evaluations should
decide how many agents you need; the documented test is whether one agent *can* do it.
<!-- /unknown -->

Where the patterns are implemented is stated: Agent Framework "provides built-in support" for all
five, with human-in-the-loop on each ({{topic:mafworkflows}}), while Foundry Agent Service offers "a
managed, no-code approach to agent chains" whose workflows "are primarily nondeterministic, which
limits the range of patterns that you can fully implement" ({{topic:foundryagents}}).

## In practice at Technik

The obvious split follows the systems: a production agent over SAP, an engineering agent over
Teamcenter, documents and standards, with handoff between them. It is also the wrong first move, and
the data says why.

Technik's sharpest question is whether a work order is running against a superseded revision —
`100004510` still names drawing `DU700001042` revision B after `ECN70000051` released C. Answering it
means joining `SAP_WO_OPERATIONS` to the Teamcenter revision view in one query. Under a handoff the
question crosses the boundary mid-thought: one agent holds the work order, the other the revisions,
and neither can perform the join. The split follows Technik's systems; its questions do not.

So the Production Assistant stays one agent with tools, the documented default. The one justification
that would survive here is the page's third reason — a security requirement. SAP and Teamcenter data
reach Snowflake through one read-only service role, while the controlled documents in SharePoint are
read with each user's own permissions ({{topic:connrefs}}). Two identities is a real boundary, not a
tidiness preference, and if Technik ever splits, that is the seam — with the superseded-revision
query kept whole on the Snowflake side.

## Design guidance

- **Justify the split with one of the three documented reasons** — prompt complexity, tool overload,
  or a security requirement. Tidiness is not one of them.
- **Prefer deterministic routing to handoff** when the right agent is knowable from the input. The
  page says so outright.
- **Cap the loop before you ship.** Three of the five patterns fail by looping, and no default cap is
  documented.
- **Decide each seam's context deliberately** — full, compacted, or a fresh instruction set — and
  right-size each agent's model, watching token spend per agent and per run ({{topic:costs}}).
- **Re-implement security trimming in every agent**, and guardrail the tool results as well as the
  final answer.
- **Keep queries that must join whole** inside one agent, whatever the org chart suggests.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Two agents pass work back and forth | No termination rule in a handoff | Add an iteration cap and a rule for who may finish |
| A pipeline's output is confidently wrong | An early stage's bad output propagated | Validate each agent's output before passing it on |
| Cost rises far more than quality | Every agent re-reads the accumulated context | Compact between agents; use smaller models where they suffice |
| A group chat never converges | No objective completion test, or too many agents | Define acceptance criteria; keep it to three or fewer |
| An agent returns data a user may not see | Trimming was implemented once, upstream | Implement trimming in every agent |

## Key terms

**Magentic orchestration** — the task-ledger pattern for open-ended problems, where a manager agent
plans, backtracks and delegates as the work reveals itself.

**Maker-checker loop** — a group-chat special case where a checker returns work to a maker until it
passes or an iteration cap is reached.

**Context compaction between agents** — summarising or pruning the accumulated context at a seam, the
named mitigation for multi-agent token growth.
