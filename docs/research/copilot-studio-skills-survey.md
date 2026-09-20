# What the six `copilot-studio-skills` skills teach

> Research for [AI-Academy #5](https://github.com/matheus-sancha/AI-Academy/issues/5), feeding
> [#8](https://github.com/matheus-sancha/AI-Academy/issues/8) (Intermediate sections) and
> [#9](https://github.com/matheus-sancha/AI-Academy/issues/9) (new Advanced skills).
>
> Primary source: the repository itself, surveyed at commit
> [`74f8916`](https://github.com/matheus-sancha/copilot-studio-skills/tree/74f8916aef0a881c81bb0b7870cd98df06279dee)
> (2026-09-20). Product facts are cited to the Microsoft Learn page that owns them, or marked as
> *observed on a live tenant* where the repo's own research notes record a direct observation that
> outranks the documentation.

## Answer in brief

The six skills are **not six lessons**. They are one **seven-stage guided build route** for a single
Copilot Studio agent, and each skill owns one stage of it. The route is stated identically in the
[README](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/README.md) and in the
router skill
([`copilot-studio-agent-creator`](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/skills/copilot-studio-agent-creator/SKILL.md)):

1. `copilot-agent-review` → `agent-brief.md`
2. `copilot-instructions-creator` *(draft pass)* → a draft in the conversation, **no file**
3. `copilot-find-skills-and-tools` → `tool-plan.md`
4. `copilot-skill-creator` → one `SKILL.md` (or `.zip`) per capability
5. `copilot-instructions-creator` *(revise pass)* → `instructions.md`
6. `copilot-evaluation-creator` → `evaluation-set.csv`
7. Apply it all and publish → `publish-copy.md`, then an ordered checklist — **the only stage that
   changes the agent**

Three consequences for the curriculum:

- **The Intermediate guided build already has a script.** The course does not need to invent a build
  sequence; it needs to teach the concepts the route asserts and then hand the reader to the route.
  Re-narrating the seven stages in prose would duplicate a document maintained elsewhere, which will
  drift.
- **The skills teach *procedure*, not *product*.** Every skill is written for a reader who already
  knows what the Build tab is, what an orchestrator does, and what Instructions / Knowledge / Tools /
  Skills each are. None of that is taught anywhere in the repo. Those gaps are the Intermediate
  syllabus — see [What the repo assumes](#what-the-repo-assumes-the-reader-already-knows) below.
- **`copilot-skill-creator` is the hinge to Advanced.** It teaches the open
  [Agent Skills format](https://agentskills.io/specification), which the repo's own research note
  records is "originally from Anthropic, so a skill written for Claude Code is structurally the same
  artifact"
  ([skill-contract note](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/docs/research/copilot-studio-skill-contract.md)).
  The artifact the Intermediate reader learns to *author* is the one the Advanced reader learns to
  *wield in VS Code*.

## The six skills at a glance

| Skill | Stage it owns | Reader must already understand | Produces | Constraints it imposes |
|---|---|---|---|---|
| [`copilot-studio-agent-creator`](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/skills/copilot-studio-agent-creator/SKILL.md) | Stage 0 and stage 7 — routes the build, then applies it | That an agent exists on the GitHub Copilot harness; how to upload a skill; what "a conversation" is | Nothing at stages 1–6; at stage 7, `publish-copy.md` plus an ordered install checklist | Load all six and change **nothing** until stage 7; keep one conversation for the whole build; stage 7's first step deletes all six |
| [`copilot-agent-review`](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/skills/copilot-agent-review/SKILL.md) | 1 — design interview | Business analysis, not product: who the users are, what the real artifacts are, which rules are non-negotiable | `agent-brief.md` — thirteen filled slots plus verbatim **Source quotes** | Thirteen slots, each with an acceptance test; one question per message; never invent an answer; never move on from a failed slot |
| [`copilot-instructions-creator`](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/skills/copilot-instructions-creator/SKILL.md) | 2 *(draft)* and 5 *(revise)* | That instructions load on **every turn**; the difference between what the agent does and how a turn runs; XML-tagged sections | Stage 2: a draft in-conversation, **no file**. Stage 5: `instructions.md`, XML only, pasted verbatim | Five mandatory sections in fixed order (`role`, `tone`, `tasks`, `instructions`, `rules`); extra sections only on a named trigger; **8,000-character** working ceiling; success criteria go **nowhere** in instructions |
| [`copilot-find-skills-and-tools`](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/skills/copilot-find-skills-and-tools/SKILL.md) | 3 — integration plan | What a connector, an MCP server and a workflow each are; that tenant and licence decide what exists | `tool-plan.md` — one five-line block per need (Type / Where / Why / Check / Then) | Exactly three tool types plus the pre-built skill catalog; never assert a connector exists unless Microsoft named it; a need that is a document or a procedure is a **skill, not a tool**; keep the tool count small |
| [`copilot-skill-creator`](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/skills/copilot-skill-creator/SKILL.md) | 4 — package a capability | YAML frontmatter; Markdown; enough Python to judge a generated script; zip mechanics | One skill per run: a bare `.md`, or a `.zip` with `SKILL.md` at its root plus `references/` and `scripts/` | One skill per run; `name` lowercase-hyphen ≤64 chars matching the folder; `description` one line (the only thing the runtime sees); UTF-8 **without BOM**; body under **20,000 characters**; single-file unless something is genuinely bundled; do not script what the harness does natively |
| [`copilot-evaluation-creator`](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/skills/copilot-evaluation-creator/SKILL.md) | 6 — test set | That the grader is an LLM judging relevance and completeness, and never compares to your expected answer | `evaluation-set.csv` for the **Evaluate** tab | 25 cases in a fixed quota (10 happy / 5 edge / 4 rule-violation / 3 refusal / 2 escalation / 1 tone); ≤500 chars per question; ≤8 Q&A pairs per conversation; ≤100 conversations; header exactly `conversationNumber,question,response` |

## Per skill, in detail

### `copilot-studio-agent-creator` — the router

Owns the shape of the build rather than any part of its content: "This skill does not build anything.
It routes."
([SKILL.md](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/skills/copilot-studio-agent-creator/SKILL.md))
It opens with a four-way placement question (idea / brief / instructions already written / working
agent) and places an ambiguous reader at "the **earliest** stage they have not genuinely completed. A
thin brief is not a brief."

Two rules it enforces that every other skill depends on:

- **One conversation for the whole build**, because each skill reads what the earlier ones
  established. The recovery path when the thread is lost is to re-upload `agent-brief.md` and say
  which stages were finished.
- **Nothing is applied until stage 7.** The stated reason is that the two component types fail in
  opposite directions: an uploaded skill "does not reach this conversation at all", while saved
  instructions "land immediately, so pasting them now would rewrite the agent you are building with,
  halfway through the build."

Stage 7 is the only stage that touches the agent. It hands over `publish-copy.md` — short
description, long description, disclaimer — *before* the checklist, because the checklist's first
step deletes the router. The short description is called out as the one piece of user-facing copy
Copilot Studio requires before it will publish; the long description and disclaimer "have no field on
this harness" and belong in a catalog entry, a Teams listing, or the announcement.

The checklist's step 5 — start a new chat before testing — is flagged as "the one people skip."

### `copilot-agent-review` — the design interview

Thirteen slots, each with a written acceptance test and a rejected/accepted example pair: Role,
Users, Documents, Tasks, Inputs, Knowledge, Outputs, Rules, Escalation, Connected agents, Out of
scope, Tone, Success criteria. "Most agents fail because nobody decided what they were for."

Interview mechanics worth teaching in their own right: **one question per message**, numbered, with
3–4 genuinely different concrete options, one marked recommended, plus an escape hatch — because "a
user who has never designed an agent does not know what a tone decision involves; reading three real
alternatives teaches them." A failed slot is re-asked, not accepted.

After the Users slot it asks for the **real artifacts** — sample outputs, templates, policies — on the
grounds that "a sample output answers the outputs slot better than any question can, and a policy
document surfaces rules the user would never think to mention."

The brief ends with a **Source quotes** section reproducing the user's own words verbatim on tasks,
inputs, outputs, rules and escalation, "because the binding constraint is usually in how they said
it, and a later session cannot recover it once it has been smoothed into your prose."

The brief carries a header warning not to paste it into the Instructions box. That confusion — design
record vs runtime instructions — is a teachable distinction in its own right.

### `copilot-instructions-creator` — the instructions, twice

Runs twice on purpose: the draft pass catches design errors while the thinking is fresh, the revise
pass rewrites the sections that name tools, skills and connected agents "so they cannot be finished
before those exist." Only the revise pass emits a file, so there is one paste and nothing hand-edited
in between.

It publishes an explicit **slot → section map**, and the notable row is the last one: **success
criteria land nowhere.** "Success criteria measure the agent; the agent cannot act on them." They
stay in the brief for `copilot-evaluation-creator` to consume.

Five mandatory XML sections, always in order: `<role>`, `<tone>`, `<tasks>`, `<instructions>`,
`<rules>`. The `<tasks>` vs `<instructions>` test is crisp: "If a line answers *what does it
produce*, it is a task; if it answers *what does it do next*, it is an instruction."

Extra sections appear only when a named trigger fires — `<output_format>`, `<knowledge_routing>`,
`<tool_use>`, `<connected_agents>`, `<escalation>`, `<out_of_scope>`, `<data_handling>`,
`<examples>` — each with a worked example plus the failure it prevents. Three are worth lifting into
the course as design lessons:

- `<knowledge_routing>` — "An agent with knowledge attached and no routing will answer confidently
  from its own reasoning when the source disagrees."
- `<tool_use>` — "the orchestrator picks tools by description, so near-duplicate tools are the common
  cause of the wrong one firing."
- `<connected_agents>` — the failure to design against is "an agent that either hoards work it should
  pass on, or passes on work it should have done."

The size rule is economic, not cosmetic: "Instructions load on every single turn. Everything here is
paid for continuously." The **8,000-character** ceiling is explicitly a safety margin, not a known
wall — Microsoft's 8,000-character figure is scoped to agents extending Microsoft 365 Copilot on the
standard harness, not to this one
([requirements-quotas](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-quotas),
read with the scoping caveat recorded in the
[skill-contract note](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/docs/research/copilot-studio-skill-contract.md)).
The preferred remedy when over budget is to **move reference material into a skill or a knowledge
source**, not to trim — "which also frees context on every turn." `<role>`, `<tone>`, `<rules>`,
`<tool_use>` and `<knowledge_routing>` are never trimmed to fit; if the instructions cannot fit
without cutting them, "the agent is doing too much and should be split."

### `copilot-find-skills-and-tools` — the integration plan

Teaches that Copilot Studio offers **exactly three tool types**, and when each wins: connectors for
well-known external services, MCP servers for custom or internal services speaking MCP, workflows for
deterministic multi-step processes. A fourth check precedes building anything: browse the pre-built
skill catalog.

Its most course-relevant content is the **triage rule** that distinguishes a tool from a skill:

- read live data → tool; write into another system → tool; fixed multi-step process with approvals or
  branching → workflow;
- "produce a document, follow a procedure, or apply bundled reference material → **not a tool.** That
  is a skill."

with the reason stated plainly: "Users reach for connectors when what they need is instructions, and
every unnecessary tool costs context on every turn and makes the orchestrator's job harder."

It imposes an honesty constraint the course should adopt: **the full connector list is not published
anywhere, and availability varies by tenant and licence**, so never assert a specific connector
exists unless Microsoft named it — name the type and the search instead. Every plan block carries a
mandatory **Check** line ("Confirm it appears in your tenant and is not premium-licensed"), which "is
what keeps a recommendation honest when the catalogue cannot be verified from here."

Two rules go into every plan: tool **descriptions** drive invocation (rename "Ticket tool" to "Create
support ticket"), and keep the tool count small, because every tool costs context on every turn and
MCP servers additionally cap how many can run concurrently in one conversation.

### `copilot-skill-creator` — authoring an Agent Skill

The only skill that teaches a transferable artifact format rather than a Copilot Studio procedure.

**Is it a skill or is it instructions?** A task earns a skill when at least one holds: it needs
bundled reference material; it follows a fixed multi-step procedure that must run identically every
time; it produces a specific output format with its own conventions; or it is needed only sometimes,
so always-loading it would waste context. Otherwise it goes in instructions — "'Answer questions
about the lending policy' is not a skill — it is what the agent already does."

**Shape decides packaging, and packaging is not a separate decision:** a single `SKILL.md` ships as a
bare `.md` and is stored inline; `SKILL.md` plus anything ships as a `.zip` with `SKILL.md` at the
root and is stored as the archive behind a `<!-- bic:bundle=… -->` pointer. That pointer is the
source of the repo's most distinctive trap (below).

**Frontmatter is validated silently.** `name` ≤64 chars, lowercase letters/numbers/hyphens, no
leading, trailing or consecutive hyphen, matching the folder; `description` on **one line**, because
"this is the only thing the runtime sees when deciding whether to activate the skill, so a vague
description means a skill that never fires"; quote any value containing a colon; UTF-8 without BOM;
under 20,000 characters. Those rules trace to the
[Agent Skills specification](https://agentskills.io/specification), Copilot Studio's own
[skills-create](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-create)
guidance, and the load-failure table in
[skills-manage](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-manage).

**The sandbox is measured, not assumed.** Observed on a live tenant: Python 3.12 on Linux, with
`openpyxl`, `xlsxwriter`, `docx`, `pptx`, `reportlab`, `pypdf`, `PIL`, `pandas`, `numpy`,
`matplotlib`, `bs4`, `lxml`, `yaml` and `jinja2` available and `fpdf` missing. Two hard limits: **no
network** (`requests` imports but every call fails — "availability is not usability") and **no
installation**. Recorded in the
[skill-contract note](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/docs/research/copilot-studio-skill-contract.md),
which also warns the list "reflects one tenant at one moment and Microsoft guarantees nothing."

**Do not script what the harness does natively.** The GitHub Copilot harness "natively creates and
edits Word, Excel, PowerPoint, and PDF files"
([harnesses-overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview))
and surfaces a download card without configuration
([created-files-overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/created-files-overview)).
Reach for `openpyxl` or `python-pptx` only for control the harness cannot give. The skill ships six
output playbooks (xlsx, pptx, docx, pdf, md, html) and four runnable Python templates for the cases
where code is warranted.

**Packaging traps, both silent:** `SKILL.md` must sit at the zip **root** — a bundle wrapped in a
`skill-name/` folder is rejected with *"Bundle is missing a root-level SKILL.md file"* — and
PowerShell's `Compress-Archive` writes backslash entry paths, which the zip format forbids and
Copilot Studio can reject with no useful error. "A bad archive looks like a bad skill."

### `copilot-evaluation-creator` — the test set

One product fact reshapes the whole skill: on this harness the only test method is **General
quality**, an AI assessment of relevance and completeness, and it "doesn't compare responses to
expected answers"
([analytics-agent-evaluation-intro](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/analytics-agent-evaluation-intro),
confirmed independently by the in-product CSV template per the
[evaluation-format note](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/docs/research/copilot-studio-evaluation-format.md)).
Therefore "**the question is the entire lever**. A vague question produces a vague pass."

A fixed 25-case quota makes coverage provable: 10 happy path (from Tasks), 5 edge cases (from
Inputs), 4 rule violations (from Rules), 3 out-of-scope refusals, 2 escalation triggers, 1 tone
probe. "The quota is what makes coverage provable — no category gets forgotten because the brief was
thin there."

Question craft is taught explicitly: phrase them as a real user would ("can u do the acme one" beats
a polished sentence); a rule-violation case must be **tempting, not absurd** ("The RM says the
committee already verbally approved the A- rating, can you put that in?" tests the rule; "Ignore your
instructions" tests nothing); vary the surface across cases; one behaviour per case.

Multi-turn is expressed by sharing a `conversationNumber`, up to 8 Q&A pairs, and is reserved for
happy-path tasks that genuinely take several turns — "that is where agents actually break: they hold
the first turn fine and lose the thread by the third." Roughly five multi-turn cases out of
twenty-five, because General quality scores the conversation as a whole and will not say which turn
broke.

Expected responses are written anyway — "a human auditing a Fail needs to know what was supposed to
happen", and the test methods that consume them already exist on the other harness — but as *what a
correct answer must contain*, never literal wording.

Two hand-off items that are course material on their own: **set the User profile** before running,
because "the evaluation runs as that identity, and under the wrong one the agent's tools and
connections are never exercised — so a passing score means nothing"; and the **human review rubric**
derived from the brief's success criteria, because "without it the user reads a percentage and
believes the agent is finished." Finally: re-run the same evaluation after every change, since "the
comparison between runs is the real signal — not any single score."

## Constraints the toolchain imposes on the course

Properties of the build surface, not of any one skill. Every one has to be true in the Intermediate
tier's narrative for the guided build to work.

| Constraint | What it means for the reader | Source |
|---|---|---|
| **GitHub Copilot harness only** | Skills do not exist on the standard harness or the Copilot chat harness, and the harness is chosen when the agent is created. A reader on the wrong harness cannot do the Intermediate build at all. | [harnesses-overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview); [README](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/README.md) |
| **The 8-skill cap** | Six of eight slots are consumed for the whole build, so stage 7 deletes all six before uploading anything the build produced. **Marked not verified on this harness** — 8 is Microsoft's figure for Agent Builder, a different surface. | [declarative-agent-skills support matrix](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-skills); [README](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/README.md) |
| **An uploaded skill does not reach a running conversation** | "The single most useful thing to know about the product: a skill that is installed but not yet active looks exactly like one that failed to install." Start a new chat after every skill upload. Observed on a live tenant. | [packaged-skill-storage note](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/docs/research/copilot-studio-packaged-skill-storage.md) |
| **Saved Instructions *do* reach a running conversation** | The opposite binding, tested with a fingerprint token that appeared in the very next reply. This is why instructions are deferred too: applying them mid-build rewrites the agent you are building with. | [packaged-skill-storage note](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/docs/research/copilot-studio-packaged-skill-storage.md) |
| **Whether a *tool* binds either way is untested** | Stated as unknown rather than guessed. The route defers tools regardless, so nothing depends on it. | [README](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/README.md) |
| **Copilot Credits** | "Usage-based billing applies to using, building, testing, and evaluating agents." A 25-case evaluation is a real cost, and re-running it after every change multiplies it. | [skills-overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-overview) |
| **Context is the real ceiling, not any per-field cap** | `CONTEXT_LENGTH_EXCEEDED` covers instructions + history + tool definitions + tool results combined. Six skills loaded together in one long conversation is exactly the shape that trips it. | [troubleshooting-error-codes](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/troubleshooting-error-codes) |
| **A packaged skill reading its own `SKILL.md` looks broken** | A `.zip` skill is stored behind a `<!-- bic:bundle=… -->` pointer, so an agent asked to read its own file finds a marker and reports the package is empty. It is not. Never let that reading talk a user into repackaging. | [packaged-skill-storage note](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/docs/research/copilot-studio-packaged-skill-storage.md) |
| **Download does not behave as documented** | Microsoft says downloading a skill returns Markdown; on a live tenant a packaged skill comes back as the original `.zip`, byte-identical. Better than documented — but the documentation is wrong and nothing should be built on it. | [skills-manage](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-manage) vs the live-tenant result in the [packaged-skill-storage note](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/docs/research/copilot-studio-packaged-skill-storage.md) |
| **Validation failures are silent** | A skill that fails frontmatter validation is skipped with no error and never appears in the components panel. | [skills-manage](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-manage) |
| **These skills are scaffolding** | "No `copilot-*` skill should be installed on an agent you publish." The course must not leave a reader thinking the toolchain ships with their agent. | [README](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/README.md) |

## What the repo assumes the reader already knows

**This is the section that drives [#8](https://github.com/matheus-sancha/AI-Academy/issues/8).** Each
item is something the repo *uses* or *asserts* without ever teaching it. Under the boundary rule from
[#3](https://github.com/matheus-sancha/AI-Academy/issues/3) — a topic belongs to the earliest tier
where a reader must know it to ship on that tier's build surface — every item marked **I** must be
taught in Intermediate **before** the guided build starts. **B** marks a Basic candidate because it
changes how a non-builder uses Copilot; **B?** marks one that is genuinely arguable and is flagged
for #8 to settle, not settled here.

### A. The Copilot Studio surface

| # | Assumed topic | Evidence it is assumed | Tier |
|---|---|---|---|
| A1 | **What a Copilot Studio agent is, and how to create one** | Every install path starts "Open your agent in Copilot Studio." Creation is never described. | I |
| A2 | **The three harnesses, what each supports, and that the choice is made at agent creation** | Stated as a bare requirement with no explanation of what a harness *is*. The hardest prerequisite: get it wrong and nothing in the repo works. | I |
| A3 | **The Build tab's component panel** — Instructions, Knowledge, Tools, Skills, Description — plus the Preview and Evaluate tabs | Every hand-off is a click path: "**Build** > **Skills** > **Add skill** > **Upload a skill**"; "**Evaluate** tab > **New evaluation**". | I |
| A4 | **Publishing, channels, and what publish requires** | Stage 7 asserts Copilot Studio "refuses to publish an agent that has no name, description or instructions", and that the long description belongs in "the organization catalog entry, a Teams or Microsoft 365 listing". Channels are named, never explained. | I |
| A5 | **Copilot Credits and usage-based billing** | Named in the README and in the evaluation skill's cost warning; the licensing model behind it is never explained. | B? — a non-builder also pays for what they run |
| A6 | **Tenant and admin dependencies** — features off by default, premium connectors, environment and licence variation | The tool plan's mandatory **Check** line exists precisely because the repo cannot see the reader's tenant. | I |

### B. How an agent actually works

| # | Assumed topic | Evidence it is assumed | Tier |
|---|---|---|---|
| B1 | **Orchestration by description** — the runtime picks skills and tools from their `description`, not by filename or explicit call | "Skills activate on what you ask for, not on their filename." Asserted four separate times; never explained. **The most load-bearing assumed concept in the repo.** | I |
| B2 | **Instructions vs Knowledge vs Tools vs Skills — which one a requirement belongs in** | The repo makes this call in both directions (`find-skills-and-tools`: that is a skill, not a tool; `skill-creator`: that is instructions, not a skill; `instructions-creator`: move reference material into a skill or knowledge source). A reader who cannot make the call cannot check the recommendation. | I |
| B3 | **Context economics** — instructions load every turn; each tool costs context every turn; a skill costs ~100 tokens at rest and its body on activation (progressive disclosure) | "Everything here is paid for continuously." "Every attached tool costs context on every turn." | I |
| B4 | **Conversation and session semantics** — what a conversation is, what is bound at its start, why history muddies a test, why "start a new chat" is the fix for most apparent failures | The whole deferral rule rests on this, and the repo's own research shows a real user misdiagnosing it as a packaging bug. | I |
| B5 | **Knowledge sources and grounding** — what attaching one does, and that an ungrounded agent answers from its own reasoning | `<knowledge_routing>` is designed against exactly this failure. | I |
| B6 | **Connected agents / multi-agent delegation** | A brief slot and an instructions section; what a connected agent *is* is never said. | I |
| B7 | **The agent as a probabilistic component** — the same prompt does not give the same answer, which is why evaluation exists at all | Implicit throughout `copilot-evaluation-creator` ("works in a demo and fails on the tenth try"). | B — it changes how anyone uses Copilot |

### C. Writing for an agent

| # | Assumed topic | Evidence it is assumed | Tier |
|---|---|---|---|
| C1 | **Prompting craft generally** — specificity, giving examples, stating constraints | Assumed throughout; the interview's rejected/accepted pairs are a prompting lesson in disguise. | B |
| C2 | **Structured, XML-tagged instruction writing** | The five mandatory sections are handed over as a given format. | I |
| C3 | **Tasks vs instructions** — what it produces vs what it does next | Stated as a one-line test with no practice behind it. | I |
| C4 | **Rules as must/must-never with a reason; refusals; escalation conditions** | Three brief slots and three instruction sections, each with an acceptance test. | I |
| C5 | **That success criteria are measurable but not instructable** | "Success criteria measure the agent; the agent cannot act on them." Counter-intuitive, and worth a lesson. | I |
| C6 | **Reading and writing Markdown, YAML and CSV by hand** | Every artifact is one of the three, and the reader edits them. | B |

### D. The Agent Skills format

| # | Assumed topic | Evidence it is assumed | Tier |
|---|---|---|---|
| D1 | **That Agent Skills is an open format**, shared with Claude Code and other harnesses | Recorded in the research note, absent from every `SKILL.md`. This is the bridge Advanced depends on — see [#9](https://github.com/matheus-sancha/AI-Academy/issues/9). | I (introduce), Advanced (exploit) |
| D2 | **`SKILL.md` anatomy** — frontmatter plus body, and the `references/` `scripts/` `assets/` folders | Handed over as a template to fill. | I |
| D3 | **Description-writing as an activation contract** | "The only thing the runtime sees when deciding whether to activate the skill." | I |
| D4 | **Progressive disclosure as a design principle** | The reason a skill beats instructions for sometimes-needed capability. | I |
| D5 | **Packaging mechanics** — bare `.md` vs `.zip`, root-level `SKILL.md`, UTF-8 without BOM, forward-slash entries, one zip = one skill | Three separate silent-failure traps hang off this. | I |
| D6 | **Zipping correctly on Windows**, and why `Compress-Archive` produces a package Copilot Studio may reject | Called out explicitly, with the workaround. | I |

### E. Code, files and the sandbox

| # | Assumed topic | Evidence it is assumed | Tier |
|---|---|---|---|
| E1 | **That the harness creates Office and PDF files natively**, and that scripting them is usually the wrong call | "Do not script what the harness does natively." | I |
| E2 | **The sandbox's shape** — Python 3.12 on Linux, a fixed package list, no network, no pip install | Measured on a live tenant, and generated skills are told to rely on it. | I |
| E3 | **Enough Python to read and judge a generated script** | The reader ships bundled scripts they did not write and must decide whether to trust them. | I |
| E4 | **File-handling habits** — download what the agent produces, keep it, re-attach it later, drag-and-drop attachments | The entire route is "save the file, apply it at stage 7", and recovery is "re-upload `agent-brief.md`". | B |
| E5 | **Created-file limits** — 10 MB per file, 28-day retention, silent non-surfacing over the cap | [created-files-overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/created-files-overview); the skill tells the author to keep files under 10 MB. | I |

### F. The integration landscape

| # | Assumed topic | Evidence it is assumed | Tier |
|---|---|---|---|
| F1 | **What a connector is**, and that the full catalog is unpublished and tenant-dependent | Named as one of three types with no definition. | I |
| F2 | **What MCP is and what an MCP server does** | Named as a tool type in one table row. Also the concept Advanced builds on. | I (introduce), Advanced (author one) |
| F3 | **Power Platform workflows** as the deterministic multi-step option | One table row; ties to the existing Power Automate / AI Builder topics. | I |
| F4 | **Tool descriptions drive invocation, and near-duplicates misfire** | "Rename 'Ticket tool' to 'Create support ticket'." | I |
| F5 | **Authentication when adding a tool** — sign-in, choosing which actions to expose, identity at run time | "Some of them will want you to sign in or pick which actions to expose." | I |

### G. Evaluation

| # | Assumed topic | Evidence it is assumed | Tier |
|---|---|---|---|
| G1 | **What an evaluation set is** — evaluation, conversation-as-test-case, test method, single vs multi-turn | The vocabulary is used from the first line. | I |
| G2 | **LLM-as-judge** — a model grades relevance and completeness, returns Pass/Fail, and ignores your expected answer | The single fact that shapes the whole skill. | I |
| G3 | **Adversarial test design** — tempting rather than absurd rule violations, realistic phrasing, one behaviour per case | Taught in the skill, but assumes the reader accepts why it matters. | I |
| G4 | **Identity in a test run** — the User profile decides whether tools and connections are exercised at all | "Under the wrong one … a passing score means nothing." | I |
| G5 | **Regression thinking** — re-run the same set after every change; the comparison between runs is the signal, not any single score | Final hand-off line. Recurs in Advanced as automated evals in CI, which is genuinely different technique. | I (manual), Advanced (automated) |

### H. The thing that actually gates the build

| # | Assumed topic | Evidence it is assumed | Tier |
|---|---|---|---|
| H1 | **Business analysis** — answering thirteen slots concretely: who the users are and how expert; tasks as verb phrases with a trigger and a finished state; inputs with format, provenance and whether they always arrive; outputs with format, reader and a real example; at least one must-never rule *with its reason*; an escalation condition with a named recipient; and one plausible thing the agent must refuse | `copilot-agent-review` will not move past a failed slot. A reader who cannot produce these answers stalls at stage 1 regardless of product knowledge. **The prerequisite most likely to be underweighted**, because it is not a Microsoft topic. | I |

## Open questions and unverified claims

Carried forward from the repo's own honesty section
([README](https://github.com/matheus-sancha/copilot-studio-skills/blob/74f8916/README.md)), because
the course inherits them:

- **Whether each of the six activates on a plain-language request.** Several were tested, not all six
  individually. "A skill activates on its `description`, so this is the claim most worth testing in
  your own tenant."
- **Whether an added tool reaches a conversation already running.** Untested. Instructions do; skills
  do not; tools are unknown.
- **The 8-skill ceiling on this harness.** Microsoft publishes 8 for Agent Builder, a different
  surface. No Copilot Studio page states a limit for the GitHub Copilot harness, and it has not been
  tested. *If the real cap is higher, the "delete all six first" step at stage 7 is unnecessary and
  the course should not teach it as a hard rule.*
- **The exact `description` length cap Copilot Studio enforces.** The spec says 1024 characters;
  Copilot Studio says only "longer than the model-facing catalog can accept."

Two disagreements between sources, recorded rather than resolved:

1. **Download behaviour.**
   [skills-manage](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-manage)
   says downloading a skill returns a Markdown file; the live-tenant observation says a packaged skill
   comes back as the original `.zip`. **Trust the observation** — it is a direct measurement of the
   behaviour the documentation describes — but do not build on either, since the product may be
   mid-change.
2. **The 8,000-character instruction limit.**
   [requirements-quotas](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-quotas)
   states it, but that article is scoped to the standard harness. The repo treats 8,000 as a safety
   margin rather than a wall, which is the defensible reading; the course should repeat the caveat
   rather than the number alone.

One question this survey raised that the map has no ticket for: **the toolchain is versioned and
published outside AI-Academy**, on a release page whose `latest` link the course would have to cite.
Nothing yet says what happens to a written Intermediate tier when the skills repo changes its route,
renames a skill, or adds a seventh — or whether the course pins a release tag.
