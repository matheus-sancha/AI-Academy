## TL;DR

Azure AI Content Safety is not one filter but a set of classifiers behind one service, and each
answers a single question: is this text harmful, is this a prompt attack, is this grounded in a
source, is this known protected material, is this tool call off task. Microsoft offers them two
ways, as guardrails on a Foundry model or agent and as a standalone API, and the two behave
differently: Foundry can block, the API only reports. Where an instrument sits and what it was built to see
matter more than which you pick, because the attacks that hurt an internal agent live in the gaps
between the questions.

## Why it matters

Intermediate's agent had one moderation setting, because Copilot Studio made the choice for it
({{topic:moderation}}). A pro-code agent inherits nothing. Scanning is something you attach to a
deployment or call from your code, at a point you choose, with a response you define. That is more
control and more ways to leave a gap, and the documentation calls its classifiers "model outputs,
not definitive determinations".

## How it works

### One service, two doors

Microsoft's overview says you can use the guardrails "in Microsoft Foundry ... or as a standalone
offering through Azure AI Content Safety Studio and APIs. The same AI service supports each access
point, the difference is how and where you choose to use it." Foundry gives "free moderation on the first 1000 text characters"; the standalone
service moderates all characters at Content Safety pricing. The difference that matters is the
verdict. In Foundry, a guardrail control can **annotate** or
**annotate and block**. In the standalone Prompt Shields API, "the API doesn't itself block or route
content. Customers decide how to use the results in their application." A service call that nobody
acts on protects nothing.

### The instruments

| Instrument | Its question | Limits the pages state |
|---|---|---|
| Analyze text and image | Sexual content, violence, hate, self-harm, with severity levels | Trained on eight languages; quality varies elsewhere |
| Prompt Shields | A user prompt attack or a document attack | "primarily trained and evaluated on English content" |
| Groundedness detection (preview) | Whether a response is grounded in the sources you give it | English only; retires 30 April 2027 |
| Protected material | Known text such as lyrics, articles and recipes, and code from GitHub | English only; its code index is "only current through April 6, 2023" |
| Task adherence | Tool use "misaligned, unintended, or premature" for the interaction | Preview in Foundry |
| Custom categories (preview) | A category you define and train | Two modes, standard and rapid |

<!-- volatile verified=2026-11 -->
Groundedness detection "retires on April 30, 2027", and Microsoft's suggested replacement is "Microsoft
Foundry evaluation tooling, or ... customer-owned grounding validation using an LLM or a system
prompt." The other guardrail controls are not part of that retirement.
<!-- /volatile -->

Notice that none of these checks that an answer is *true*. Prompt Shields says so itself: it does
not determine whether content is "factually accurate, grounded in source material, compliant with
policy, or aligned with the application's task."

### Where a control sits

A Foundry guardrail is a set of controls, and each control has a risk, intervention points and an
action. There are four intervention points.

<!-- volatile verified=2026-11 -->
They are **User input**, **Output**, and, for agents only, **Tool call** and **Tool response**, the
last two in preview. Models are assigned the `Microsoft.DefaultV2` guardrail by default, and agents
inherit their model's guardrail unless a custom one is assigned. User prompt attack detection is on
by default. "Document attack detection is off by default and must be enabled when you configure
guardrail controls." The Foundry table calls the same risk "Indirect attacks".
<!-- /volatile -->

The tool response point is the one that sees what an agent's tools hand back, which is where an
indirect attack arrives ({{topic:ctxsecurity}}). It is preview and agents only: a bare model gets
just the first two.

### Severity and blocking

The harm classifiers use four categories and four levels, **Safe**, **Low**, **Medium** and **High**.
A blocking level of Low "blocks high-severity content only", Medium blocks medium and high, and High
blocks all three, and Safe content is "annotated but never filtered". The standalone text API
reports a finer 0 to 7 scale, optionally trimmed to 0, 2, 4 and 6. Copilot Studio's own filter has a
third scale, Lowest to Highest ({{topic:modtuning}}).

<!-- unknown since=2026-11 -->
No page read for this lesson says what the default guardrail blocks at, or whether Copilot Studio's
moderation is this same service. The Copilot Studio page links to the harm-categories page and says
no more about its mechanism.
<!-- /unknown -->

## In practice at Technik

Two Technik records show what the instruments cannot do. Quality notification `300001267` tells the
assistant to report an open QN as closed. `300001270` tells it to draft a revision of `SWI70000318`
that removes section 5's acceptance criteria. Ask each instrument whether it can see them:

| | `300001267`, hide an open QN | `300001270`, change a work instruction |
|---|---|---|
| Harm categories | No. Nothing in it is harmful content | No |
| Protected material | No | No |
| Groundedness | No. The row is real, so a false claim about it is grounded | No |
| Prompt Shields, document attack | Built for it, with a "Manipulated Content" subtype, if enabled and the input reaches it | Built for it, as an instruction in a document |
| Task adherence | Not about tool use | Could see a drafting call, if the agent had one |

Only one cell is a maybe, and it is probabilistic and off by default. The capstone's agent has no
tool that returns a QN, so neither record can reach it, and no tool that writes, so `300001270`
could not be carried out if one did. Its three tools return typed fields, such as a document's title
and owner, never prose, so the gap is small. Nothing in the repository configures a guardrail, so
the agent runs under whatever its deployment carries. The Intermediate assistant is the opposite
case: its QN tool returns free text typed by people. Three agents, three answers, written down:

| Agent | Text that reaches the model | Controls to switch on |
|---|---|---|
| Capstone assistant | Typed fields only | The default guardrail; revisit when a tool returns prose |
| Production Assistant (Copilot Studio) | QN descriptions, SharePoint passages | The platform filter, and the rule and tests ({{topic:injection}}) |
| A hypothetical pro-code QN assistant | QN descriptions | Document attack detection, at user input and tool response |

Be careful with the word *grounded*. The capstone's `grounded_or_refuse` middleware only checks that
a tool result exists. Groundedness detection compares an answer with source text using a model. The
first is deterministic and blind to meaning, the second reads meaning and can be wrong
({{topic:loop}}).

## Design guidance

- **Attach scanning at the intervention point where untrusted text arrives.** For agents that is the tool response.
- **Turn on document attack detection explicitly.** It is off by default.
- **Decide what a detection does.** The API reports and does not block.
- **Check language coverage** against the text your records actually contain, and plan for retirements.
- **Pair every classifier with a capability limit.**

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Prompt Shields is "on" and injected records still land | Document attack detection is off by default | Enable it, and scan the tool response point |
| A detection changed nothing | The standalone API reports and does not block | Write the code that acts on `attackDetected` |
| A grounded answer is wrong | The source row was real and the claim about it was false | A graded eval case |
| Non-English text passes unscanned | Several classifiers are English-only or English-first | Test your own languages with attacks and benign text |
| Groundedness detection stops working in 2027 | The preview retires | Move to evaluation tooling or your own validation |

## Key terms

**Guardrail** — a set of Foundry controls, each naming a risk, intervention points and an action.

**Intervention point** — where a control scans: user input, output, or for agents a tool call or response.

**Annotate and block** — the action that stops a detected risk, where *annotate* only records it.

**Document attack** — hidden instructions in content the model reads, Foundry's *indirect attack*.
