## TL;DR

Threat-modelling an agent starts by drawing the agent as a system: what it can reach, what text it
reads, and what its output is handed to. OWASP's 2025 list names ten risks for LLM applications, and
the one that decides the damage is **Excessive Agency**, whose root cause OWASP states as "excessive
functionality; excessive permissions; excessive autonomy." Prompt injection is how the attack
arrives. Agency is what it can do on arrival. So the order of work is to shrink the agent first and
filter second. The list is also a checklist with gaps: it names no MCP server and no skill, and it
cannot say which of the ten your agent actually has.

## Why it matters

Intermediate gave you five layers of defence for one attack ({{topic:injection}}), and
{{topic:ctxsecurity}} and {{topic:mcpsec}} each took a slice of the surface. None of them asked the
whole question: given this agent, which of the ten risks can happen here, and what is the cheapest
thing that makes each one harmless? A threat model is that question, written down before the
design hardens. It also decides where the rest of this module spends effort, because most of the
controls that follow guard one risk each.

## How it works

### What OWASP gives you

The 2025 list, in order: Prompt Injection, Sensitive Information Disclosure, Supply Chain, Data and
Model Poisoning, Improper Output Handling, Excessive Agency, System Prompt Leakage, Vector and
Embedding Weaknesses, Misinformation, and Unbounded Consumption. Each entry has examples, prevention
and example attack scenarios. The prevention lists repeat three ideas across entries: limit what the
model can touch, treat what it produces as untrusted input, and put a person in front of anything
that cannot be undone.

For prompt injection the page's own headings include "Enforce privilege control and least privilege
access", "Require human approval for high-risk actions", "Segregate and identify external content"
and "Conduct adversarial testing and attack simulations". For output it says "Treat the model as any
other user, adopting a zero-trust approach". None of that is a filter. The page also says it is
unclear whether there are fool-proof prevention methods for injection.

### Excessive agency is three separate faults

OWASP names the root cause as "excessive functionality; excessive permissions; excessive autonomy",
and its mitigations separate them. **Functionality** is what the agent can call: its list of
mitigations starts with "Minimize extensions" and "Avoid open-ended extensions". **Permissions** is
what each call may do, in "Minimize extension permissions" and "Execute extensions in user's
context". **Autonomy** is whether anyone decides before the action, in "Require user approval". The
page adds "Complete mediation", checking every request in the downstream system rather than trusting
the agent to have checked.

The three fail independently. A narrow tool with write permission is too powerful. A read-only
tool called a thousand times is still a cost. And a tool that cannot hurt anyone, given a free choice
of arguments, can still be pointed at the wrong record.

### A method for the whole agent

OWASP gives the categories, not the procedure. The one this course uses is its own: list what the
agent can **read**, what it can **do**, and where its **output goes**, then walk the ten risks
against those three lists and write one of three answers for each: *cannot happen here*, *can happen
and something deterministic stops it*, or *can happen and only a probabilistic control or a person
stops it*. The third answer is the finding. A deterministic control is a role, a schema, a policy;
a probabilistic one is a classifier or an instruction ({{topic:ctxsecurity}}).

### What the list does not name

The supply-chain entry gives nine examples: packages, licences, outdated models, vulnerable
pre-trained models, weak provenance, LoRA adapters, collaborative development, on-device models and
unclear terms. None names an MCP server or a skill. Tool poisoning and the rug pull are in
Microsoft's guidance instead ({{topic:mcpsec}}), and a skill is a bundle of instructions and scripts
you install ({{topic:skillgov}}). A model of an agent that lists only OWASP's examples will miss
the parts that make it an agent.

## In practice at Technik

Take the capstone's assistant. It **reads** three views of Teamcenter data as `TECHNIK_AGENT_RO`,
metadata only, no document text. It **does** nothing: three lookups. Its **output** is text read by a
person in a chat. Walked against the ten:

| Risk | Where it could reach the capstone | What holds |
|---|---|---|
| Prompt injection | Typed fields in tool results, such as document titles | The rule in `<rules>`, and no write path ({{topic:ctxsecurity}}) |
| Sensitive information | Owner names in every document result, and in traces | Views the role reads, and who may read traces ({{topic:tracing}}) |
| Supply chain | The server's dependencies, its docstrings, and the toolbox it is called through | A frozen tag and review ({{topic:mcpsec}}) |
| Poisoning | Nothing is trained or embedded | A wrong replicated row is a data fault, caught by evals |
| Improper output handling | The model's tool arguments reach a database | Patterns and bound parameters, below |
| Excessive agency | Three tools | A read-only identity, below |
| System prompt leakage | `agent/instructions.md` | It is in a public repository and holds no secret |
| Vector weaknesses | No vector store | Does not apply here |
| Misinformation | A tool-backed wrong answer, `rev-03` | A graded case only |
| Unbounded consumption | The tool loop and the warehouse | `max_function_calls` is 6; no token or rate limit is in the repository |

Two rows are deterministic and short enough to show. The model's arguments are untrusted input, so
every parameter has a pattern, and the query binds it rather than formatting it:

*From [`server/teamcenter.py`, line 25](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/server/teamcenter.py#L25) and [lines 83–84](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/server/teamcenter.py#L83-L84):*

```python
DocNo = Annotated[str, Field(pattern=r"^[A-Z]{3}\d{8}$", description="Document number, for example SWI70000318")]
# …
    revisions = rows("""SELECT DOC_TYPE, REVISION, TITLE, OWNER, STATUS, RELEASED_AT, NEXT_REVIEW_DATE
                        FROM TC_DOCUMENTS WHERE DOC_NO = %(doc_no)s ORDER BY REVISION DESC""", doc_no=doc_no)
```

And the identity is the permission limit, held by a service user with one role:

*From [`seed/03_access.sql`, lines 23–29](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/seed/03_access.sql#L23-L29):*

```sql
CREATE USER IF NOT EXISTS TECHNIK_AGENT_SVC
  TYPE = SERVICE
  DEFAULT_ROLE = TECHNIK_AGENT_RO
  DEFAULT_WAREHOUSE = TECHNIK_AGENT_WH
  COMMENT = 'Service user for the Technik Production Assistant and its MCP server. Key-pair auth only.';

GRANT ROLE TECHNIK_AGENT_RO TO USER TECHNIK_AGENT_SVC;   -- the agent's service user
```

The findings are in the third column's weak rows. Misinformation has no control but a grader, and
the last row has no stated limit. Neither is a surprise, and both are written down, which is what
the model is for. Whose authority a hosted agent runs under is the open part:

<!-- unknown since=2026-11 -->
The hosted-agent page gives each hosted agent its own identity and calls the project's managed
identity "Not the agent's runtime identity", while the Foundry overview says published agents
"inherit the enterprise identity and access controls configured for your project". Neither page
says whether an agent version can pin the toolbox version it calls, so a promoted toolbox could
change what a deployed agent may call without a deploy.
<!-- /unknown -->

## Design guidance

- **Draw the agent first:** what it reads, what it does, where its output goes.
- **Walk all ten risks** and write one of three answers for each. Keep the third kind in a list.
- **Reduce agency before adding filters.** Functionality, then permissions, then autonomy.
- **Treat every model-produced argument as untrusted input**, validated where it is used.
- **Add what the list omits:** servers, skills and tool descriptions are part of the supply chain.
- **Write down the risks you accept**, with the evidence that you did.
- **Revisit when the agent gains a tool or a data source.** The model is about the system, not the code.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A threat model that is a copy of the list | The ten were quoted, not applied to this agent | Walk each against reads, actions and output, and answer for this system |
| An agent that can act, guarded only by a prompt | Autonomy was assumed to be controlled by instructions | Put an approval or an identity in front of the action |
| A "read-only" tool that does damage | Permission was granted at the tool and not at the identity | Bound the identity, then the tool ({{topic:connauth}}) |
| Every risk marked mitigated | The probabilistic controls were counted as deterministic | Mark each control as one or the other |
| A new MCP server joins the agent unreviewed | OWASP's examples do not name servers | Add servers and skills to the inventory |

## Key terms

**Excessive agency** — an agent holding more functionality, permission or autonomy than its job needs.

**Threat model** — a written account of what an agent can read and do, which risks apply and what stops each.

**Complete mediation** — checking every request in the downstream system, rather than trusting the agent.

**Deterministic control** — one whose protection does not depend on the model behaving.
