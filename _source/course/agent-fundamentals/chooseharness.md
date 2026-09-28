## TL;DR

Copilot Studio offers three harnesses. The **GitHub Copilot harness** is the most capable: reasoning-heavy
multi-step work, skills, memory, and native file creation. The **standard harness** builds rule-based
agents with topics and agent flows. The **Copilot chat harness** extends Microsoft 365 Copilot Chat with
enterprise knowledge. You choose when you create the agent, and the documentation is unambiguous: an agent
created on the GitHub Copilot harness **cannot be transferred** to the standard harness, or the other way
round.

## Why it matters

This is the only decision in the level that cannot be undone. Everything else — bad instructions, the
wrong model, a clumsy tool — is an edit. The harness is a rebuild: new agent, new tools, new connections,
re-tested, re-published, and users told to move to a different agent.

It is also easy to make by accident, in the first two minutes, by accepting a default. There is a toggle
on the Copilot Studio home page that decides which world you are authoring in, and it is entirely possible
to create something on the wrong side of it without noticing.

## How it works

<!-- volatile verified=2026-09 -->
| | GitHub Copilot harness | Standard harness | Copilot chat harness |
|---|---|---|---|
| **Best for** | Complex, multi-step business processes | Rule-based agents and structured conversations | Extending Microsoft 365 Copilot Chat with enterprise knowledge |
| **How it works** | Reasons through a goal on its own, step by step | Follows the topics and rules you define | Connects enterprise knowledge to Copilot Chat |
| **Recovers from problems** | Retries and finds alternative paths automatically | Follows the paths you built | Not a focus |
| **Topics** | No — you describe the agent instead | **Yes**, and only here | No |
| **Skills and memory** | **Yes** | Not a focus | Not a focus |
| **Works with files** | Creates and edits Word, Excel, PowerPoint and PDF natively | Not a focus | Not a focus |
| **Publishing** | Internal teams or external customers | Internal teams or external customers | Internal teams |
| **Billing** | Copilot Credits, usage-based | See standard-harness licensing | Consumption, or included with a Microsoft 365 Copilot licence |

The harnesses, their names and their boundaries move between releases — this is among the fastest-changing
parts of Copilot Studio. Check the linked comparison before creating anything. Note also that Microsoft's
table says "not a focus" rather than "no" for several rows, which is a softer claim than it looks: treat it
as *do not design around this here* rather than as a guarantee either way.

To reach the standard harness, turn **off** the **New experience** toggle on the home page, or use **Other
ways to build**.
<!-- /volatile -->

> [!IMPORTANT]
> The GitHub Copilot harness is a Copilot Studio authoring and orchestration framework — **not** the GitHub
> Copilot service. Microsoft states that customer data is not sent to or processed by GitHub Copilot when
> agents run in Copilot Studio, and that Copilot Studio's privacy, security, compliance and data-residency
> commitments continue to apply. It is a reasonable thing to be asked about, and the answer is documented.

### How to choose

Work through these in order and stop at the first yes:

1. **Does it need a conversation path that must run exactly as drawn** — a structured intake, a compliance
   check, a fixed confirmation sequence? → **standard harness**. Topics are the only way to guarantee a
   path, and they live only here.
2. **Is it only extending Microsoft 365 Copilot Chat with company knowledge**, for users already working
   there? → **Copilot chat harness**.
3. **Does it need skills, memory, native file creation, or multi-step work that recovers when a step
   fails?** → **GitHub Copilot harness**.

Then write down *why*, in the agent's own description.

If you are following this level's guided build, the answer is decided for you: it packages a capability as
a skill, and skills are a GitHub Copilot harness feature ({{topic:whatyouneed}}).

### What you are foreclosing

| Choosing | Gives up | The workaround |
|---|---|---|
| **GitHub Copilot harness** | Topics. Nothing guarantees a conversation path; everything is orchestrated | Put the guarantee in the tool's input contract or a flow, not in a prompt |
| **Standard harness** | Skills and memory. You cannot upload a `SKILL.md` here | Delegate that behaviour to a connected agent on the other harness ({{topic:reuse}}) |
| **Copilot chat harness** | Most of the authoring surface. It is an extension, not a platform | Build in Copilot Studio proper and publish to Teams instead |

None is fatal — but each workaround is a design you will live with, so choose the capability you would
rather rebuild by hand.

## In practice at Technik

The Technik Production Assistant is built on the **GitHub Copilot harness**. The reasoning, recorded in the
agent's own description:

> Built on the GitHub Copilot harness because the QN write-up has to ship as a skill, and because answering
> a revision question takes two tool calls and a comparison that the runtime has to recover from if the
> first call fails. The cost is topics: the work order number format check moves into the tool's input
> contract instead.

Working through the questions above:

1. **Does it need an exact path?** There is one candidate — a work order number must be format-checked
   before anything uses it. But a check is not a conversation, and the check can live where the value is
   consumed rather than where it is typed. That is a real trade, not a free one: an instruction usually
   catches a part number typed where a work order number belongs, and a topic always would.
2. Not a Copilot Chat extension — it needs its own tools and its own publishing.
3. Yes to all of it: a skill, multi-step reasoning across Snowflake and Teamcenter data, and recovery when
   a call fails.

So: the GitHub Copilot harness, knowingly, with one thing given up and a plan for it.

By {{module:advanced-tools-and-multi-agent}} Technik runs a mixed estate — the assistant split into a
production agent and an engineering agent with handoff. That is a normal end state, not a mistake, and it
starts with this decision being made on purpose.

> [!WARNING]
> The most expensive version of this is choosing by default. If you cannot say why your agent is on the
> harness it is on, you have not chosen — and you will find out which one you needed at the point where
> changing it costs most.

## Design guidance

- **Decide before creating.** It is not a setting, and it cannot be transferred.
- **Check which side of the New experience toggle you are on** before you create anything.
- **Write the reasoning into the agent's description**, not just a document.
- **Ask about exact paths first.** It is the sharpest discriminator.
- **Plan the workaround for what you gave up**, at the time you give it up.
- **Do not rebuild to gain a capability** unless it is genuinely central. Delegate instead.
- **Re-check the comparison** when the product changes, and check which harness every limit you read
  belongs to ({{topic:tenantvaries}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| There is no Topics area | GitHub Copilot harness | Topics are not coming. Move the guarantee into a tool or flow |
| There is no Skills area | Standard harness | Put the skill on a connected agent ({{topic:reuse}}) |
| "We'll switch it later" | You cannot — transfer is not supported in either direction | Plan a rebuild, or delegate |
| You created the agent in the wrong world | The **New experience** toggle was where you left it | Check the toggle before creating; recreate on the right harness |
| Nobody knows why this harness | Chosen by default | Record it now; it will be asked |
| Users confused by two agents | Two front doors | Publish one; keep the specialist internal |

## Key terms

**Harness** — the runtime an agent is created on ({{topic:harness}}).

**GitHub Copilot harness** — skills, memory, native files, multi-step reasoning that recovers. No topics.

**Standard harness** — topics and agent flows, for paths that must run as drawn.

**Copilot chat harness** — extends Microsoft 365 Copilot Chat with enterprise knowledge.

**Connected agent** — a separate agent another hands work to, and the usual workaround for a harness limit
({{topic:connected}}). The one users talk to is the **front door**.
