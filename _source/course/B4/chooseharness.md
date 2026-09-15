## TL;DR

Copilot Studio offers three harnesses. The **GitHub Copilot harness** does reasoning-heavy,
multi-step work with skills, memory and files. The **standard harness** builds rule-based agents with
topics and agent flows. The **Copilot chat harness** extends Microsoft 365 Copilot Chat with
enterprise knowledge. You choose when you create the agent, and **you cannot change it afterwards**.

## Why it matters

This is the only decision in the Beginner track that cannot be undone. Everything else — bad
instructions, the wrong model, a clumsy tool — is an edit. The harness is a rebuild: new agent, new
topics, new connections, re-tested, re-published, and users told to move to a different agent.

It is also easy to make by accident, in the first two minutes, by accepting a default.

## How it works

| | GitHub Copilot harness | Standard harness | Copilot chat harness |
|---|---|---|---|
| **For** | Reasoning-heavy, multi-step work | Rule-based agents with designed paths | Extending Microsoft 365 Copilot Chat |
| **Topics** | No | **Yes** | No |
| **Skills** | **Yes** | No | No |
| **Tools** | Yes | Yes | Limited |
| **Agent flows** | Yes | **Yes** | No |
| **Memory and files** | **Yes** | Limited | — |
| **Users meet it** | Where you publish it | Where you publish it | Inside Microsoft 365 Copilot Chat |

<!-- volatile verified=2026-09 -->
The harnesses, their names and their capability boundaries change between releases — this is among
the fastest-moving parts of Copilot Studio, and skills in particular have moved. Check the linked
documentation for the current comparison before creating anything. What is stable is that the choice
is made at creation and cannot be changed.
<!-- /volatile -->

### How to choose

Work through these in order and stop at the first yes:

1. **Does it need a conversation path that must run exactly as drawn** — a structured intake, a
   compliance check, a confirmation before something irreversible? → **standard harness**. Topics are
   the only way to guarantee a path, and they live only here.
2. **Is it primarily extending Microsoft 365 Copilot Chat with company knowledge**, for users already
   working there? → **Copilot chat harness**.
3. **Does it need to hold written procedures, work over several steps, or keep files and memory?** →
   **GitHub Copilot harness**.
4. **Genuinely unsure?** → **standard harness**. A scripted exchange somewhere is more common than
   people expect, and it is the harder capability to add later.

Then write down *why*, in the agent's own description.

### What you are foreclosing

Being explicit about the cost of each choice:

| Choosing | Gives up |
|---|---|
| Standard harness | Skills. A specialist behaviour has to live on a second agent and be delegated to (B8) |
| GitHub Copilot harness | Topics. Nothing guarantees a conversation path; everything is orchestrated |
| Copilot chat harness | Most authoring surface. It is an extension, not a platform |

None of those is fatal — each has a workaround — but each workaround is a design you will live with.

## In practice at Technik

The Technik Production Assistant is built on the **standard harness** in B5. The reasoning, recorded
in the agent's own description:

> Built on the standard harness because it needs topics: the work order intake is a scripted
> exchange that must validate the number every time. The cost is that it cannot hold skills; the QN
> write-up skill lives on a connected agent instead.

Working through the questions above:

1. **Does it need an exact path?** Yes. Ana gives a work order number, and it must be format-checked
   before anything uses it. An instruction would usually catch a part number typed into the wrong
   field; a topic always does.
2. Not primarily a Copilot Chat extension — it needs its own tools and its own publishing.
3. It does need a written procedure, the QN write-up. But that is **one** capability, and it can be
   delegated.

So: standard harness, knowingly, with one thing given up and a plan for it. That plan is B8, where
the skill goes on *Technik QN Assistant* on the GitHub Copilot harness and the main agent hands over.

By A6 Technik runs a mixed estate — a standard-harness front door and specialist agents behind it.
That is a normal end state, not a mistake, and it starts with this decision being made on purpose.

> [!WARNING]
> The most expensive version of this is choosing by default. If you cannot say why your agent is on
> the harness it is on, you have not chosen — and you will find out which one you needed at the
> point where changing it costs most.

## Design guidance

- **Decide before creating.** It is not a setting.
- **Write the reasoning into the agent's description**, not just a document.
- **Ask about exact paths first.** It is the sharpest discriminator.
- **When unsure, standard.** Topics are harder to add later than delegation.
- **Plan the workaround for what you gave up**, at the time you give it up.
- **Do not rebuild to gain a capability** unless it is genuinely central. Delegate instead (B8).
- **Re-check the comparison** when the product changes.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| No Topics area | GitHub Copilot harness | Topics are not coming. Redesign or rebuild |
| No Skills area | Standard harness | Put the skill on a connected agent (B8) |
| "We'll switch it later" | You cannot | Plan a rebuild, or delegate |
| Nobody knows why this harness | Chosen by default | Record it now; it will be asked |
| A second agent appeared to work around a limit | Normal and often correct | Make sure it is deliberate and documented |
| Users confused by two agents | Two front doors | Publish one; keep the specialist internal |

## Key terms

**Harness** — the runtime an agent is created on ([What Is a Harness](harness.html)).

**Standard harness** — topics and agent flows. No skills.

**GitHub Copilot harness** — skills, memory, files, multi-step reasoning. No topics.

**Copilot chat harness** — extends Microsoft 365 Copilot Chat with enterprise knowledge.

**Connected agent** — a separate agent another hands work to. The usual workaround for a harness
limit (B7, B8).

**Front door** — the agent users actually talk to.
