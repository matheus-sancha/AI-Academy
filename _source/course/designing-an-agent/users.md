## TL;DR

Name the users and say how expert they are, and whether they are inside the company or outside it, because a
tone decision and a refusal both depend on it. *"Everyone at the company"* is not a user: nothing about the
agent follows from it. Then stop asking questions and **ask for the artifacts**: a sample of the output, the
template it follows, the policy it works under. A sample output settles the outputs question better than any
description, and a policy document surfaces rules nobody would have thought to mention.

## Why it matters

Every later decision in the brief is made *for someone*. How much to explain a status code, whether to show a
SQL-derived number or a sentence, what to refuse and whom to send a user to: none of these has a right answer
in the abstract. They have a right answer for a planner who has read SAP codes for ten years, and a different
one for a supervisor in their first month.

Descriptions also fail in a predictable way. Asked what a good output looks like, people describe what they
think it should look like, which is rarely what they actually use. The real one has a section nobody mentions
because everybody knows it is there.

## How it works

### The users slot

The slot is filled when it names three things:

| Names | Because it decides | Rejected | Accepted |
|---|---|---|---|
| **Who** | Vocabulary, examples, what counts as obvious | "the team" | "production planners at Plants 1 and 2" |
| **How expert** | Tone, how much to explain, which questions are plausible | "technical people" | "fluent in SAP status codes, not in Teamcenter revision rules" |
| **Internal or external** | Which data may be shown at all, and what must be refused | (not stated) | "internal staff only" |

*"Everyone at the company"* fails all three. It is usually said by someone who wants the agent to be widely
useful, and the effect is the opposite: an agent written for nobody in particular explains too much to experts
and too little to newcomers, and refuses by guesswork.

Where the users work is part of the answer too. Microsoft's comparison of declarative and custom engine agents
chooses between them partly on this: a declarative agent fits users whose work is already in Microsoft 365
apps and is designed to be used by individuals, while group use in a Teams channel or meeting is listed as a
reason to build a custom engine agent. Knowing that the users are individuals asking in Teams chat is a design
fact, not a detail.

### Users you are about to leave out

Microsoft's responsible AI principles include **inclusiveness**, phrased in its AI fundamentals training as
making sure a solution does not exclude some users, and **transparency**, making users aware of how the system
works and what its limits are. Both turn into questions for this slot:

- **Who would use this if they could, and cannot?** Someone without the licence, the channel or the access to
  the data the agent reads.
- **Who will over-trust it?** The less expert the user, the more the agent has to say about where an answer
  came from and what it does not know.

### Ask for the artifacts

Once the users are named, ask for things rather than more answers:

| Ask for | It fills | And often surfaces |
|---|---|---|
| **A real sample of the output** | The outputs slot ({{topic:inputsoutputs}}) | A section, field or convention nobody described |
| **The template it follows** | The output format | Mandatory parts that a description skips |
| **The policy or procedure it works under** | The rules slot ({{topic:rules}}) | Rules, approvals and owners nobody thought to mention |
| **A past case that went wrong** | Edge cases | The input that sometimes does not arrive |

Read each one and say what it settled. Then keep asking questions, but now about what the artifacts show:
*"every sample opens with the ECN reference; should the agent always do that?"* A question about a real
document gets a precise answer; a question about an imagined one gets a guess.

## In practice at Technik

The first answer to *"who uses the Production Assistant?"* was *"everyone in operations"*. The accepted
version, after three rounds:

| User | Expertise | What follows |
|---|---|---|
| **Production planners**, Plants 1 and 2 | Fluent in SAP status codes and work orders | Codes like `PCNF` can be shown; explain the hours, not the code |
| **Quality engineers** | Own quality notifications and their disposition | Expect QN numbers and defect types; own decisions the agent must not make |
| **Manufacturing engineers** | Fluent in drawings, CNC programs and revisions | Expect revision history with the ECN that changed it |
| **Supervisors** | Read summaries; not fluent in either system's codes | Every status code spelled out; a one-line answer first |

All internal, all asking as individuals in Teams. The supervisors row changed the tone decision: the same work
order answer now leads with a plain sentence and puts the codes after it.

Then the artifacts. Asked to describe a good revision draft, the document owner gave a paragraph about
"clear changes". Asked for one, they sent revision B of `SWI70000318` and the `GWI70000027` authoring template.
Together they settled the output format in a minute and showed a change-history table at the end of every
controlled document, which nobody had mentioned.

Asked for the procedures the agent works under, the quality team sent `SOP70000101` *Quality Notification
Handling*. It says a nonconformance is dispositioned only by the quality engineer assigned to the QN, which
became the agent's most important refusal ({{topic:rules}}). Nobody had raised it in the interview, because to
the quality team it was too obvious to say.

> [!TIP]
> When someone says "nothing comes to mind" about rules, ask for the procedure their team is audited against.
> The rules are already written down; they just were not written down *for the agent*.

## Design guidance

- **Name users by role, site and expertise**, never by organisation size.
- **Say internal or external explicitly**, even when it seems obvious.
- **Write down who the agent leaves out**, and whether that is deliberate.
- **Ask for a real output, a template and a policy** before asking another question.
- **Report what each artifact settled**, then ask about what it shows.
- **Keep the artifacts with the brief.** They are evidence for every slot they filled.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Answers explain too much to experts and too little to newcomers | Users named as "everyone" | Name each user group and its expertise; decide tone per group |
| The agent refuses things its users are entitled to, or answers what it should refuse | Internal or external never stated | State it in the users slot; derive refusals from it |
| The built output is missing a section users expected | Output described, never sampled | Get a real example before writing the outputs slot |
| A rule surfaces after release, from an audit or a complaint | Policy documents never asked for | Ask for the procedures the users' team works under |
| A group of intended users cannot reach the agent | Access, licence or channel assumed | List who is left out, and decide it deliberately |

## Key terms

**User**: a named group who talks to the agent, with its expertise and whether it is internal or external.

**Artifact**: a real document the agent will work from or produce: a sample output, a template, a policy.

**Inclusiveness**: the responsible AI principle that a solution should not exclude some users.

**Transparency**: the responsible AI principle that users should know how a system works and what its limits
are.
