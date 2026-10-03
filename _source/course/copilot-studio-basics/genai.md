## TL;DR

A handful of agent-level settings decide how an agent routes, whether it may answer with nothing behind
the answer, how strictly it filters content, and whether it searches the public web. They apply to every
turn, nothing prompts you to look at them, and the defaults suit a general-purpose assistant rather than an
internal engineering tool. The **standard harness** has a full **Generative AI** settings page. The
**GitHub Copilot harness** has far fewer switches: moderation is there, the grounding switch is not, so on
that harness grounding lives in the instructions.

## Why it matters

Most of this module is about things you write. This lesson is about things you *switch*, and switches get
skipped because nothing asks you to open the page.

One of them is the most consequential control on the standard harness. **Allow ungrounded responses**
decides whether the agent may answer from the model's general knowledge in a turn where it used no
knowledge source and no tool. Leave it on and every "answer only from your sources" rule you wrote is
advisory: the agent has permission to fill the gap, so sometimes it will, and the invented answer sounds
exactly as confident as a grounded one ({{topic:hallucination}}). Turn it off and the rule has a mechanism
behind it.

Knowing which harness has which switch matters as much. Look for that toggle on a GitHub Copilot harness
agent and you will not find it; the missing switch is a design fact, not a menu you overlooked.

## How it works

### On the standard harness

<!-- volatile verified=2026-09 -->
These sit on the agent's **Settings** page, in the **Generative AI** section. Three of them require
generative orchestration to be on.
<!-- /volatile -->

| Setting | Decides | Default |
|---|---|---|
| **Orchestration** | Whether the orchestrator chooses topics, tools, knowledge and other agents from their descriptions, or topics fire on trigger phrases | Generative, for new agents |
| **Allow ungrounded responses** | Whether a turn may be answered with no knowledge source or tool used | Not documented — check it |
| **Use information from the web** | Whether the agent may search all public sites Bing indexes, not just the ones you added | Not documented — check it |
| **Moderation** | How strictly content is filtered, **Lowest** to **Highest** | **High** |
| **Tenant graph grounding with semantic search** | Whether users *without* a Microsoft 365 Copilot licence also get semantic-index retrieval, at extra cost | Licensed users get it regardless |

**Orchestration** is the switch every other setting leans on. Generative makes descriptions the routing
logic ({{topic:orchestration}}); classic makes trigger phrases the routing logic and reduces tools to
things a topic calls explicitly ({{topic:topics}}). An administrator can switch generative orchestration
off for a whole environment.

**Allow ungrounded responses** is subtler than its name. Off, it blocks any response from a turn in which
the agent used no knowledge source or tool — and the fallback topic fires instead. Two consequences follow,
both documented:

- **It does not guarantee no general knowledge.** The model can still blend what it knows into an answer
  it built from a source. The switch only catches turns where nothing was retrieved at all.
- **It blocks some good answers.** With the switch off, an answer from knowledge is returned only if it
  carries an in-text citation. Models do not always cite, so a correct answer is sometimes withheld, and
  asking again may return it. A follow-up answered from earlier turns — *"does that apply to Plant 2
  too?"* — can be blocked the same way. The documented mitigations are to instruct the agent to always
  cite, and to avoid instructions that suppress citations, such as *respond only in JSON*.

**Moderation** trades false refusals against risk. Lower levels produce more answers, some of which may
contain harmful content; higher levels produce fewer. The agent-level value can be overridden per
generative answers node and per prompt tool, and at runtime the topic-level setting wins.

### On the GitHub Copilot harness

<!-- volatile verified=2026-09 -->
Settings open from the **…** menu in the agent designer toolbar, as an **Agent settings** dialog with four
tabs. **AI & behavior** holds **Moderation level** — **Minimum**, **Low**, **Medium**, **High** or
**Maximum** — and whether other agents may connect to this one. The other tabs hold identity (fixed after
the first save), authentication, user feedback and the greeting. Microsoft states that setting changes
take effect after you **save and publish** the agent.
<!-- /volatile -->

<!-- unknown since=2026-09 -->
Whether a changed moderation level reaches the **Preview** tab before the agent is published, given that
settings are documented to apply after publishing while Build changes reach Preview on the next turn.
Test a moderation change in Preview *and* after publishing.
<!-- /unknown -->

No orchestration switch, no web-search switch and no ungrounded-responses switch appears in that dialog.
The harness reasons through a goal on its own ({{topic:harness}}), and whether it answers from its sources
or from what it knows is decided by the instructions and nothing else.

## In practice at Technik

The Technik Production Assistant is on the GitHub Copilot harness, so its settings review is short:

| Setting | Value | Why |
|---|---|---|
| Moderation level | **High**, then tested | Quality vocabulary is the risk: *crack*, *failure*, *rejection*, *destructive testing* |
| Allow other agents to connect | Off | Nothing calls it yet |
| Grounding | **In the instructions** | There is no switch; the rule has to carry the whole load |

The third row is the one to carry forward. The assistant's instructions say to answer only from its
knowledge sources and tools, to cite the document and revision, and to say *"I could not find that in my
sources"* when nothing matches ({{topic:instructions}}). On this harness that sentence is not backed by a
toggle, so it has to be **tested**: in {{module:knowledge-and-rag}} you ask a question the documents do not
cover — *"What is the minimum overlay thickness for Inconel on a manifold header?"* — and the only
acceptable answer is the abstention. That case goes in the evaluation set and stays there
({{topic:testsets}}).

For moderation, ask twenty real questions in Technik's vocabulary — porosity in `SWI70000318`,
hydrostatic failures under `SWI70000402` — and see what is refused.

If Technik built a second agent on the standard harness, its review would be longer: generative
orchestration on, **Allow ungrounded responses off**, web information off, moderation tested, and a
citation instruction in place so the switch does not withhold correct answers.

> [!WARNING]
> A settings change invalidates earlier testing exactly as a model change does ({{topic:model}}).
> Moderation and orchestration change behaviour across every question, not just the one you had in mind.

## Design guidance

- **Open the settings on every new agent**, before adding anything.
- **Know your harness's switches.** On the GitHub Copilot harness, grounding is an instruction you test;
  on the standard harness, it is a switch plus an instruction.
- **Turn ungrounded responses off** for a standard-harness agent over company data, and add a citation
  instruction with it.
- **Test moderation with your real vocabulary.**
- **Record settings next to the instructions**, so a changed default is visible.
- **Change one setting at a time**, then re-run your questions.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Confident answers with no source behind them | Ungrounded responses allowed, or, on the GitHub Copilot harness, a weak grounding instruction | Turn the switch off; strengthen and test the instruction |
| A correct answer comes back as *nothing found*, intermittently | Ungrounded responses off, and the model did not cite | Instruct it to always cite; remove format rules that suppress citations |
| A legitimate weld-defect question is refused | Moderation stricter than your vocabulary | Test real terms; adjust knowingly |
| The agent cites a public web page | Web information is on | Turn it off |
| There is no ungrounded-responses switch | The agent is on the GitHub Copilot harness | Grounding lives in the instructions |
| A moderation change seems to do nothing | Settings apply on publish | Publish, then re-test |

## Key terms

**Generative orchestration** — the orchestrator choosing topics, tools, knowledge and agents from their
descriptions.

**Allow ungrounded responses** — the standard-harness switch deciding whether a turn may be answered with
no source or tool used.

**Moderation level** — how strictly content is filtered. A trade, not a safety guarantee.

**Grounding posture** — whether an agent may answer beyond its sources, and what enforces it.
