## TL;DR

Three decisions, each with a test. Write at least one **must-never rule with the reason attached**, because a
rule with no reason gets reasoned around by a model that is trying to be helpful. Name one **plausible** thing
the agent must refuse: plausible, not absurd, because the interesting refusals are the ones a well-meaning user
would ask for. And state one **escalation condition with a named recipient**, because "escalate to a human"
names nobody and therefore happens to no one.

## Why it matters

These are the slots that decide what happens when the agent is wrong, or right about something it should not
touch. They are also the slots stakeholders fill worst. Asked for rules, people offer virtues: *be accurate*,
*be professional*. Asked what to refuse, they offer jokes: *don't write poems*. Asked about escalation, they say
*a human*. Each answer sounds responsible, and each leaves the agent with nothing to do differently.

Microsoft's responsible AI principles put **accountability** among the six: people should be accountable for AI
systems, which means designing oversight so that humans stay in control. Oversight needs a named person in it.
This lesson is where the brief names them.

## How it works

### Rules: must or must never, and because

A rule in the brief has four parts: *must* or *must never*, the behaviour, **the reason**, and where the rule
came from. The reason is not decoration. A model trying to help meets cases the rule's author never imagined,
and a bare rule leaves it to guess whether this case counts. The reason lets it see what the rule protects, and
lets a reviewer see whether the rule still earns its place. How the rule is then phrased for the model is
{{topic:writinginstructions}}'s job; the brief's job is to make sure the reason exists to be phrased.

| | Rejected | Accepted |
|---|---|---|
| Virtue, not rule | "Be accurate about revisions." | "Never call a revision current unless its status is Released, because work is built to whatever the answer says." |
| No reason | "Never show draft documents." | "Never quote from a document In Work or In Review as if it applied, because it has not been approved and may change." |

The best source of rules is not the interview. It is the policies and procedures the users already work under
({{topic:users}}), where the reasons are usually written down too.

### Refusals: plausible, not absurd

A refusal slot filled with *"anything offensive"* or *"writing poems"* tests nothing. The platform's moderation
handles harmful content ({{topic:moderation}}), and nobody at work asks the production assistant for a poem.

The refusal worth designing is a request that is **in the agent's domain, made in good faith, and still not the
agent's to answer**: usually because a person holds the authority, or because answering would look like a
decision. Two checks find them:

- **Who is accountable for this answer today?** If it is a named role, the agent informs that role's decision
  and does not make it.
- **What would a helpful agent do here that it must not?** That is the refusal, and it goes in the brief with
  what the agent says instead.

This is narrower than **out of scope**, which lists whole areas the agent does not cover ({{topic:scope}}). A
refusal is inside the scope: the agent knows the subject well, and declines one thing about it.

### Escalation: a condition and a recipient

An escalation is a condition under which the agent **stops** and hands the user to someone. Both halves must be
named:

| | Rejected | Accepted |
|---|---|---|
| Condition | "if it gets complicated" | "if two sources state different values for the same requirement" |
| Recipient | "a human" | "the owner of the controlled document, by name" |

*"A human"* fails because nobody receives it. The user is told to ask someone, does not know whom, and asks the
agent again.

How escalation is carried out depends on the harness. On the GitHub Copilot harness there are no topics, so the
escalation is an instruction: stop, say why, and say whom to contact and what to bring. The standard harness
adds an escalation system topic ({{topic:topics}}) and agent flows, whose human-in-the-loop actions send
**approval requests** or **request information** from a person as a step in the flow. The brief records the
condition and the recipient either way; the mechanism is chosen later ({{topic:hitl}}).

## In practice at Technik

The Production Assistant's rules slots, after the interview and after reading `SOP70000101` and `SOP70000114`:

**Must-never rule.**

> Never call a revision current unless its status is **Released**, because work is built to whatever the
> answer says. *Source: the users; Teamcenter's release status is the authority.*

**Refusal.** A quality engineer looking at an open QN asks: *"Overlay porosity on `XT-V2-1042`, four
indications. Is that acceptable? Can we ship it?"* It is in the domain, it is asked in good faith, and the agent
has everything needed to sound sure: the QN, the inspection document, the acceptance criteria. Under
`SOP70000101` the disposition belongs to the quality engineer assigned to the QN.

> The agent must refuse to disposition a nonconformance, because `SOP70000101` gives that decision to the
> assigned quality engineer. Instead, it shows the QN, quotes the acceptance criteria with the document and
> revision they come from, and names the assigned engineer.

The refusal still delivers almost everything the user needed. What it withholds is the one sentence that would
have been a decision.

**Escalation.** Technik's controlled documents in Teamcenter and its internal standards on SharePoint can drift
apart.

> If a released controlled document and an internal standard state different acceptance criteria for the same
> check, stop. Show both, with document, revision and section, and tell the user to contact the document's
> owner, named in Teamcenter.

The recipient is named per document, from the `OWNER` column of `TC_DOCUMENTS`, so *"contact the owner"* always
arrives with a name. A version that said *"escalate to quality"* would have sent every conflict to a shared
mailbox nobody owns.

> [!IMPORTANT]
> Each of these three goes straight into the evaluation set with its pass condition: the disposition question
> passes only if no verdict is given and the engineer is named; the conflict passes only if both sources are
> shown and the owner is named ({{topic:testsets}}).

## Design guidance

- **Write at least one must-never, with its reason and its source.** Then ask whether each rule still earns its
  place.
- **Mine policies for rules**, not only the interview.
- **Design the refusal a good colleague would ask for**, and say what the agent offers instead.
- **Name the escalation recipient by role or by name**, ideally resolved from data.
- **Keep the mechanism out of the brief.** Record the condition and recipient; choose the harness feature later.
- **Turn every rule, refusal and escalation into a test case.**

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A rule is followed in tests and broken in an unforeseen case | No reason, so the model guessed the rule's scope | Add the reason to the brief and the instructions |
| The refusal cases all pass and prove nothing | Refusals chosen to be absurd | Design refusals from requests real users make |
| The agent gives a verdict that belongs to a person | No refusal named for decisions others own | Ask who is accountable; refuse the decision, inform it |
| Users are told to "contact someone" and come back | Escalation named no recipient | Name the role or person, ideally from data |
| Conflicts between sources are silently resolved | No escalation condition for disagreement | Add one; show both sources and stop |

## Key terms

**Must-never rule**: a rule stated as an absolute, with its reason and where it came from.

**Refusal**: a request inside the agent's domain that it declines, with what it offers instead.

**Escalation**: a condition under which the agent stops and hands the user to a named recipient.

**Accountability**: the responsible AI principle that people stay accountable for AI systems, and so stay in
control of them.
