## TL;DR

A declarative agent is configuration that runs on someone else's engine. It "run[s] on Microsoft 365
Copilot's managed orchestration and language-model infrastructure", and you supply instructions,
knowledge and capabilities "rather than implementing and hosting your own conversational runtime".
The Agents Toolkit puts that configuration in a repository and provisions it into a tenant. What it
cannot do is turn configuration into control: "You don't replace the managed orchestrator with custom
runtime code." Every design decision here is about which side of that line a requirement falls on.

## Why it matters

{{topic:stack}} gave you the distinction: a declarative agent borrows Copilot's orchestrator, models
and compliance, and a custom engine agent brings its own. That makes a declarative agent look like
the cheap option, and for retrieval it is. The cost shows up when a requirement quietly needs
something only an owned runtime can promise, such as an exact order of steps, a guaranteed refusal,
or a pinned model. The architecture page says plainly where that line runs.

## How it works

### Who owns what

The architecture page splits every component into a managed side and yours. Three rows carry most of
the weight:

| Component | Microsoft runs | You own |
|---|---|---|
| Orchestrator and model | Selects and invokes capabilities and generates responses | Instructions, tool descriptions, behaviour settings, and evaluating the result |
| Infrastructure | The Copilot orchestration and model runtime | Hosting "any external APIs, MCP servers, or other services it uses" |
| Security and compliance | Microsoft 365 identity, data access and platform protections | Authentication, data flows, and "authorization and data protection in external services" |

Settings help, but they don't hand you the controls: "Supported configuration settings influence the
managed runtime; they don't give you full control over its implementation." The page's example is
small and telling: the manifest sets a default response mode, "which users can override".

In the data flow, Copilot receives a request, selects context and
capabilities from your instructions, knowledge configuration and tool descriptions, retrieves or
calls, and responds. The page warns that this "isn't a fixed execution sequence or a guarantee of how
many retrievals or tool calls occur". You describe the agent and the runtime decides what happens.

### Building one

<!-- volatile verified=2026-11 -->
In VS Code with the Microsoft 365 Agents Toolkit extension: **Microsoft 365 Agents Toolkit** →
**Create a New Agent/App** → **Declarative Agent** → **No Action**, name it, then **Provision** in the
**Lifecycle** pane. You test it in the Copilot app itself, picking the agent from the conversation
drawer. The tenant must allow custom app upload, because "Provision fails if custom app upload isn't
enabled", and "Microsoft 365 Government tenants don't support publishing agents through Agents
Toolkit."
<!-- /volatile -->

The tutorial has no step for running the agent locally. The orchestrator is
Microsoft's, so every test is a provision into a real tenant followed by a conversation in Copilot.
The repository holds the definition; the behaviour lives only in the tenant. Declarative agents now
also run in Word and PowerPoint, where they "can access the entire open document".

<!-- unknown since=2026-11 -->
The tutorial does not say who else in the tenant can see an agent once it is provisioned, or how a
development copy is kept apart from the one users rely on. Until you have checked, treat
**Provision** as deploying into a shared space, and use a development tenant for anything
unfinished.
<!-- /unknown -->

### What configuration cannot promise

The page's sentence to remember is this one: "Instructions guide model behavior; they aren't a
substitute for application logic that must enforce a transaction, exact execution order, or recovery
procedure." It names four requirements that don't fit: custom runtime control, durable business
processes, exhaustive processing of a data set, and current ordered results from a source web search
represents badly. Scoped web search "uses Bing-indexed content rather than directly querying the
underlying data source", so anything dynamic goes through an action instead.

None of these disqualifies the agent as the front end: "A service can own the business process while
the agent gathers inputs, invokes a supported action, and presents the result." The page says to
choose by control, "not simply on whether the task has multiple steps", and declarative agents can
chain API calls themselves.

Two more things are no longer yours. Trust: "Retrieved content and tool responses can contain
untrusted instructions. Platform protections don't replace authorization checks in your services"
({{topic:ctxsecurity}}). And the model: "Platform and model updates can change behavior", so
evaluation is a standing task rather than a release gate, because the version you tested is not one
you can pin.

### Three limits that are not one limit

"A manifest field's character limit, a knowledge-source configuration limit, and a runtime context
limit describe different constraints." Fitting the manifest proves nothing about the context. Knowledge
retrieval does not promise coverage either, since "A response doesn't necessarily include every item
in a source", and large tool payloads can be truncated. The documented fix is on your side of the
line: "design APIs to filter, aggregate, or return the relevant subset rather than sending all
records into a conversation" ({{topic:toolshaping}}).

## In practice at Technik

The standards agent from {{topic:lowvspro}} is the case where a declarative agent fits. A
manufacturing engineer drafting revision C of `SWI70000318` in Word asks whether the tightened
porosity limit in section 5 still agrees with the *Weld Overlay Acceptance Criteria* table on the
Standards site. The agent reads the open draft, retrieves the table, and can point out that the table
itself says the work instruction governs where the two differ. That is retrieval and comparison over
Microsoft 365 content, which is what the managed runtime is for.

Microsoft 365 identity does the access control, and it cuts both ways. A production supervisor using
the same agent cannot reach the drafting team's SharePoint site, so the draft never surfaces for them.
That is correct, and you configured none of it.

Three requests from the same users fall outside the line, and each goes somewhere else:

- *Is work order `100004510` running against a superseded revision?* This needs current, joined SAP
  and Teamcenter data. That calls for an action to the capstone's MCP server ({{topic:plugins}}),
  which checks its own authorization, not knowledge or web search.
- *Average efficiency of every welding operation this year* is exhaustive processing. A Snowflake
  view computes it and the agent presents the answer.
- *Release revision C* is a durable process. Release waits on a qualified UT inspector, so it belongs
  to the document revision approval flow ({{module:automation-and-workflows}}), not to instructions.

## Design guidance

- **Sort each requirement onto a side of the line** before you build: configuration, or a service
  you own.
- **Put enforcement in services.** An exact order, a transaction or a mandatory refusal is code
  behind an action, never a sentence in the instructions.
- **Scope the knowledge, then test it as each user group.** Microsoft 365 identity decides what each
  person sees.
- **Shape tool results at the source.** Filter and aggregate in the API, not in the conversation.
- **Evaluate on a schedule, not only at release.** The model changes underneath you.
- **Use a development tenant.** Provisioning is the only way to test.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent skips a step the instructions call mandatory | Instructions were used as a workflow engine | Move the sequence into a service or flow behind an action |
| An answer on current status is days stale | Scoped web search over Bing-indexed content | Add an API or MCP action over the live source |
| A total is wrong but plausible | Too many records sent into the conversation, truncated | Aggregate in the API and return the subset |
| Behaviour changed with no commit | A platform or model update | Re-run evaluations on a schedule ({{topic:evalstrategy}}) |
| **Provision** fails at once | Custom app upload disabled in the tenant | Ask the administrator, or use a development tenant |
| One user sees an answer another doesn't | Retrieval runs as each user's Microsoft 365 identity | Expected; test with each user group's account |

## Key terms

**Declarative agent** — an agent defined by configuration (instructions, knowledge, capabilities,
actions) that runs on Microsoft 365 Copilot's managed orchestrator and models.

**Provision** — the Agents Toolkit lifecycle step that deploys the agent's package into a tenant,
where it is tested in Copilot itself.

**Managed orchestration** — the runtime Microsoft owns, which decides which knowledge and capabilities
to use on each turn. You influence it through configuration but cannot replace it.
