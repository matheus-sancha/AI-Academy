# AI Engineering on Microsoft — Topic Trees (Draft v1 for review)

> Step 1 of 3. Review, edit, strike or add topics directly in this file.
> Once approved, this tree becomes the single data source for the roadmap HTML, the PDFs and the course modules.
>
> Legend: **Section** → Topic — _one-line scope_ · `[opt]` = optional / "good to know" (rendered as a grey node, like roadmap.sh's alternative options) · `[prev]` = preview feature at time of writing (Sept 2026)

---

## ⚠️ What changed since our interview (please read first)

Microsoft shipped changes in 2026 that affect two of your decisions:

1. **Copilot Studio now has three "harnesses"** (Microsoft's own term, docs dated Jul 2026):
   - **GitHub Copilot harness**: goal-driven reasoning, skills, memory, file creation, runs in a sandbox, billed in Copilot Credits.
   - **Standard harness**: topics, trigger phrases, agent flows. This is the "classic" Copilot Studio.
   - **Copilot chat harness**: extends Microsoft 365 Copilot Chat with enterprise knowledge.

   ➜ "Harness" is no longer abstract. **Beginner** now gets a "Choosing a harness" topic. **Advanced** keeps the deep harness concept plus GitHub Copilot in VS Code, as agreed.

2. **Copilot Studio skills are now real SKILL.md skills.** Agents on the GitHub Copilot harness accept an uploaded `SKILL.md` or skill bundle, or a skill written from blank. That's the same format GitHub Copilot uses in VS Code.

   ➜ Your split still works, with a small adjustment:
   - **Beginner** — *using and creating simple skills in Copilot Studio*, plus how topics, tools and child agents relate to them in the standard harness.
   - **Advanced** — *authoring skill packages* (scripts, resources, progressive disclosure) shared across VS Code, GitHub Copilot and Copilot Studio.

3. **Workflows vs. agent flows.** Copilot Studio now has *agent flows* (standard) and a new *Workflows* designer (agent nodes, AI actions, step-level testing). AI Builder's old "Create text with GPT" action is deprecated. Its replacement is **prompts** ("Create text using a prompt").

4. **Azure AI Foundry is now "Microsoft Foundry."** The tree uses the new names.

---

# 🟨 BEGINNER — AI Engineering on Microsoft

_Audience: engineers new to AI. Low-code first. ~14 sections / ~85 topics._

### B0. Getting Oriented
- The AI Engineer role — _what an AI engineer does (uses models, doesn't build them); how it differs from ML engineer / data scientist_
- The Microsoft AI stack map — _where M365 Copilot, Copilot Studio, Power Platform, GitHub Copilot, Foundry and Snowflake fit_
- Licensing & Copilot Credits — _what costs money: seats vs. consumption; why testing and evaluating agents can consume credits_
- Your developer environment — _Power Platform Developer Plan environment, Copilot Studio access, VS Code + GitHub Copilot, Snowflake dev role_

### B1. LLM Fundamentals
- What is an LLM — _next-token prediction, pre-trained models, why outputs vary_
- Tokens — _what a token is, rough word/token ratios, why tokens = cost and limits_
- Context & context window — _everything the model "sees" in one request; what happens when it's full_
- Inference — _what happens when you send a prompt: request → model → generated tokens; latency_
- Temperature & sampling — _temperature, top-p; deterministic vs. creative outputs; where you can/can't set it in Copilot Studio_
- Training vs. fine-tuning (concepts) — _pre-training, instruction tuning, fine-tuning — what each means at a high level_
- Hallucinations & grounding — _why models invent facts; grounding in your data as the main fix_
- Choosing a model — _model families available in Copilot Studio (GPT, Claude), reasoning vs. chat models, trade-offs_
- Multimodal models `[opt]` — _images, documents, voice as inputs/outputs_

### B2. Prompt Engineering
- Anatomy of a prompt — _system/instructions vs. user message vs. context/data_
- Clarity & specificity — _role, task, constraints, audience, success criteria_
- Structuring prompts with XML tags — _`<instructions>`, `<context>`, `<examples>`, `<output_format>`; separating data from instructions_
- Few-shot examples — _showing the model what "good" looks like_
- Output formats — _Markdown, tables, JSON; asking for a structure reliably_
- Breaking down tasks — _step-by-step instructions, decomposition_
- Iterating on prompts — _test, compare, refine; keep a prompt library_
- Writing agent instructions — _applying the above to Copilot Studio / Agent Builder instructions_

### B3. Using AI Assistants
- Microsoft 365 Copilot Chat — _work vs. web grounding, prompting in Word/Excel/Teams, Copilot Prompt Gallery_
- Agent Builder in M365 Copilot — _creating a simple declarative agent without code; when it's enough_
- Using Copilot Studio agents — _finding and using published agents in Teams and M365 Copilot; the Agent Store_
- GitHub Copilot in VS Code — _completions, chat, ask/edit/agent modes at a user level_
- GitHub Copilot custom instructions `[opt]` — _`copilot-instructions.md` as a first taste of context engineering_

### B4. Agent Fundamentals
- What is an agent — _model + instructions + knowledge + tools + a loop that decides what to do_
- Conversational vs. autonomous agents — _chat-triggered vs. event-triggered agents_
- Orchestration — _how an agent picks knowledge/tools/topics to answer a request_
- What is a harness — _the runtime between your agent and the model (concept only)_
- Choosing a harness in Copilot Studio — _GitHub Copilot vs. standard vs. Copilot chat harness; choice is permanent per agent_
- Human-in-the-loop — _approvals, confirmations, escalation to a human_

### B5. Copilot Studio Basics
- Copilot Studio tour — _home, agents, tools, knowledge, test/preview, publish, analytics_
- Create your first agent — _describe in natural language, refine name/description/instructions_
- Instructions — _identity, scope, tone, boundaries_
- Model selection — _picking the agent's primary model and what changes_
- Topics & trigger phrases (standard harness) — _deterministic conversation paths; system topics_
- Variables & Power Fx basics — _topic/global variables, simple formulas_
- Generative AI settings — _generative orchestration on/off, general knowledge, moderation, response settings_
- Testing in the test/preview pane — _activity map, tracing what the agent did and why_

### B6. Knowledge & RAG (concepts)
- What is RAG — _retrieve relevant content → add to context → generate grounded answer_
- Knowledge sources overview — _public websites, SharePoint, OneDrive, uploaded files, Dataverse_
- Copilot connectors vs. Power Platform connectors as knowledge — _indexed vs. real-time; user-level permissions_
- Snowflake as a knowledge source — _select tables; natural-language querying without writing SQL_
- Citations & answer quality — _why citations matter; common reasons knowledge doesn't return results_
- Work IQ & Foundry IQ `[opt]` `[prev]` — _organizational context (mail, calendar, files) and Foundry knowledge bases — awareness only_

### B7. Tools, Connectors & MCP (using)
- What are tools — _how agents act: connectors, flows, prompts, REST, MCP_
- Power Platform connectors — _prebuilt connectors, actions, triggers_
- Connections & authentication — _user vs. maker credentials; why it matters when you share an agent_
- Adding a connector tool to an agent — _inputs, outputs, descriptions that help orchestration_
- What is MCP — _a standard plug for tools; servers expose tools the agent can call_
- Adding an existing MCP server to an agent — _onboarding a prebuilt/certified MCP server in Copilot Studio_
- Connected & child agents — _delegating tasks to other agents_
- Computer use `[opt]` — _agents that click and type in websites/desktop apps; when to prefer APIs_

### B8. Skills (using & creating simple ones)
- What is a skill — _name + description + Markdown instructions the orchestrator invokes when relevant_
- Skills vs. topics vs. tools — _reusable behavior vs. scripted path vs. action_
- Add an existing skill in Copilot Studio — _upload a SKILL.md or skill bundle_
- Create a simple skill from blank — _writing a good name/description so it triggers correctly_
- Standard-harness reuse patterns — _reusable topics, tools and child agents when skills aren't available_

### B9. Workflows & Power Automate with AI Builder
- Power Automate cloud flows basics — _triggers, actions, conditions, expressions_
- Agent flows — _flows built in Copilot Studio and used as agent tools_
- Workflows (new designer) — _agent nodes, AI actions, step-level testing; agent flows vs. workflows_
- AI Builder overview & credits — _prebuilt vs. custom models; AI Builder credits_
- AI Builder prompts — _"Create text using a prompt" in flows; inputs, instructions, output_
- Document processing — _extracting data from invoices/forms with prebuilt models_
- Approvals in flows — _human-in-the-loop automation_
- Topics vs. flows vs. agents — _choosing conversational vs. process automation_

### B10. Data: SQL in Snowflake
- Snowflake architecture basics — _accounts, warehouses, databases, schemas, stages_
- Roles & access — _RBAC basics; why agents should use least-privilege roles_
- Querying basics — _SELECT, WHERE, ORDER BY, LIMIT_
- Joins — _INNER/LEFT joins, keys, avoiding duplicates_
- Aggregation — _GROUP BY, HAVING, COUNT/SUM/AVG_
- CTEs & subqueries — _WITH clauses for readable queries_
- Window functions (intro) — _ROW_NUMBER, running totals_
- Views for AI consumption — _clean, well-named, documented views agents/knowledge can use_
- Snowflake connector in Power Platform — _connecting flows and agents to Snowflake_

### B11. Safety, Moderation & Responsible AI
- Responsible AI principles — _Microsoft's six principles in practice_
- Content moderation in Copilot Studio — _agent / topic / prompt levels; low ↔ high strictness trade-off_
- Prompt injection & jailbreaks — _what they are; why agents with tools raise the stakes_
- Data privacy & DLP awareness — _what data leaves where; DLP policies block connectors_
- Agent authentication options — _no auth vs. Microsoft Entra ID vs. manual; who can talk to your agent_

### B12. Environments & Publishing
- Power Platform environments — _developer, sandbox, production; dev → test → prod idea_
- Solutions basics — _why every agent should live in a solution_
- Publishing an agent — _publish vs. save; what a publish does_
- Channels — _Teams & Microsoft 365 Copilot, website, other channels_
- Sharing & permissions — _editors vs. users; security groups_
- Analytics basics — _sessions, resolution, satisfaction, knowledge usage_

### B13. Testing & Evaluation Basics
- Why evaluate agents — _non-determinism; "it worked once" is not a test_
- Manual testing & activity map — _reproducing and diagnosing bad answers_
- Agent evaluation test sets — _quick question set, generated from knowledge, import from file, from test chat_
- Running evaluations & reading results — _pass/fail, reviewing failures, iterating_
- Feedback loop — _analytics + user feedback → new test cases_

### B14. ➜ Continue to Advanced
- Beginner checkpoint — _self-assessment of what you should be able to do before starting Advanced_

---

# ⬛ ADVANCED — AI Engineering on Microsoft (Developers)

_Prerequisite: Beginner roadmap. Pro-code first. ~15 sections / ~105 topics. Expect to trim during review._

### A0. Prerequisites & Developer Tooling
- Prerequisite: Beginner roadmap — _link back; no fundamentals repeated_
- VS Code for AI engineering — _extensions, workspace setup, dev containers_ `[opt]`
- GitHub Copilot agent mode — _multi-step edits, terminal/tool use, approvals_
- Copilot Studio VS Code extension — _editing agents as YAML, syncing with the cloud_
- Git & GitHub fundamentals for agents — _branching, PRs, reviewing AI-generated changes_
- Python or C# baseline — _enough to call APIs, write an MCP server, run evaluations_

### A1. LLM Internals for Engineers
- Transformers & attention (intuition) — _why context position and length matter_
- Tokenization in practice — _counting tokens, token budgets, cost estimation_
- Inference parameters — _temperature, top_p, max tokens, stop sequences, seed, reasoning effort_
- Reasoning models — _when extra "thinking" helps and what it costs_
- Embeddings — _vectors, similarity, what they're used for_
- Function / tool calling — _how models emit structured tool calls_
- Structured outputs — _JSON schema-constrained responses_
- Latency, throughput & cost — _streaming, rate limits, quotas, model routing_
- Foundry deployment types `[opt]` — _serverless (standard/global), provisioned throughput_

### A2. Context Engineering
- From prompt engineering to context engineering — _designing everything that enters the context window_
- The context window as a budget — _instructions, tools, knowledge, history, tool results_
- XML-structured context & templates — _consistent tagged sections, variables, data isolation_
- System prompt design at scale — _layered instructions, priorities, conflict handling_
- Tool & result shaping — _concise tool descriptions, trimming tool outputs_
- Retrieval vs. stuffing — _just-in-time context vs. preloading_
- Conversation history & compaction — _summarization, truncation, "lost in the middle" / context rot_
- Memory — _short- vs. long-term memory; Copilot Studio memory_ `[prev]`
- Prompt caching `[opt]` — _reusing stable prefixes to cut cost and latency_
- Context as a security boundary — _separating trusted instructions from untrusted data_

### A3. Agent Harness (deep dive)
- The agent loop — _observe → plan → act (tool) → reflect; stop conditions_
- Planning & recovery — _decomposition, retries, alternative paths_
- Sandboxing, permissions & approvals — _what the agent may do unattended_
- Copilot Studio harnesses compared — _GitHub Copilot vs. standard vs. Copilot chat: features, publishing, billing_
- GitHub Copilot as a harness — _agent mode, Copilot CLI, cloud agent_
- Customizing the harness — _`copilot-instructions.md`, `AGENTS.md`, prompt files, custom agents_
- Harness vs. SDK vs. platform — _when to build your own loop (Agent Framework) vs. use a managed harness_

### A4. Agent Skills (authoring)
- The Agent Skills format — _folder + `SKILL.md` (frontmatter `name`, `description`) + optional resources/scripts_
- Progressive disclosure — _metadata always loaded, body on activation, files only when referenced_
- Writing descriptions that trigger — _specific, action-oriented, testable_
- Bundling scripts & reference data — _deterministic helpers inside a skill_
- Skills in VS Code / GitHub Copilot — _`.github/skills`, personal vs. project skills_
- Skills in Copilot Studio — _packaging a bundle, uploading, reusing across agents_
- Testing & versioning skills — _trigger tests, regression on outputs, Git_
- Sharing & governing skills — _team libraries, review, community collections (e.g., awesome-copilot)_ `[opt]`

### A5. Model Context Protocol (MCP)
- MCP architecture — _host, client, server; tools, resources, prompts_
- Transports — _stdio vs. Streamable HTTP; local vs. remote servers_
- Using MCP servers in VS Code — _`mcp.json`, trust, tool selection_
- Building an MCP server — _official SDKs (Python/TypeScript/C#); tool schemas and descriptions_
- Authentication for MCP — _OAuth, Entra ID, API keys; per-user identity_
- Connecting MCP servers to Copilot Studio — _onboarding a custom MCP server as a tool; workflows with MCP tools_
- Snowflake-managed MCP server — _exposing Cortex Analyst, Cortex Search, Agents and SQL as MCP tools with RBAC_
- MCP security — _tool poisoning, over-broad tools, least privilege, DLP_
- MCP certification `[opt]` — _Microsoft certification program for MCP servers_

### A6. Advanced Tools, Connectors & Multi-Agent
- Custom connectors — _OpenAPI definitions, auth, policies_
- Connector SDK & Power Fx `[opt]` — _enhanced connectors_
- REST API tools — _calling APIs directly from agents_
- Connection references & service principals — _shared connections for published agents (e.g., Snowflake)_
- Computer use (advanced) — _credentials, model choice, resilience, Windows 365 for Agents_ `[opt]`
- Multi-agent patterns — _connected agents, handoff, sequential, concurrent, group chat_
- Agent-to-Agent (A2A) — _agents collaborating across systems_
- Agent identity — _Microsoft Entra Agent ID_

### A7. Pro-Code Agents
- Low-code vs. pro-code decision — _Copilot Studio vs. declarative agents vs. Agent Framework vs. Foundry_
- Declarative agents with M365 Agents Toolkit — _manifest, instructions, capabilities, knowledge_
- API plugins & TypeSpec `[opt]` — _extending declarative agents with actions_
- Custom engine agents & M365 Agents SDK — _bring your own orchestration into Teams/M365 Copilot_
- Microsoft Agent Framework — _agents, tools, MCP, context providers, middleware (Python/.NET)_
- Agent Framework workflows — _graph-based multi-agent orchestration_
- Foundry Agent Service & hosted agents — _running agents in Microsoft Foundry_
- Bring a Foundry model into Copilot Studio `[opt]` — _using your own deployed model_

### A8. Advanced RAG
- Embeddings & vector search — _indexing, similarity metrics_
- Chunking strategies — _size, overlap, structure-aware chunking_
- Hybrid search & semantic ranking — _keyword + vector + reranking (Azure AI Search)_
- Agentic retrieval & Foundry IQ knowledge bases — _query planning across multiple sources_
- Snowflake Cortex Search — _managed hybrid search over Snowflake data_
- Cortex Analyst & semantic views — _text-to-SQL over governed semantic models_
- Structured vs. unstructured retrieval — _SQL/semantic layer vs. document search; routing between them_
- Groundedness & citations — _enforcing answers from sources_
- RAG evaluation — _retrieval quality vs. answer quality metrics_

### A9. Snowflake: Advanced SQL & Cortex AI
- Advanced window functions & QUALIFY — _ranking, deduplication, time-series_
- Semi-structured data — _VARIANT, FLATTEN, JSON handling_
- Query performance — _Query Profile, clustering, warehouse sizing_
- Secure views & RBAC for agents — _row access policies, masking, dedicated agent roles_
- Cortex AISQL functions — _AI_COMPLETE, AI_CLASSIFY, AI_EXTRACT, AI_FILTER, AI_AGG in batch SQL_
- Cortex Agents — _Snowflake's managed agent runtime over Analyst + Search + tools_
- Integrating Snowflake with Microsoft agents — _knowledge source vs. connector vs. MCP: when to use which_
- Cost control — _credit monitoring, resource monitors for AI workloads_

### A10. Intelligent Automation (advanced)
- Deterministic vs. agentic automation — _when a workflow should reason and when it must not_
- Workflows with agent nodes & AI actions — _designing hybrid automation_
- Flows as agent tools — _clean input/output contracts, descriptions, error returns_
- AI Builder prompts (advanced) — _structured JSON output, Dataverse grounding, model/moderation settings per prompt_
- Document processing pipelines — _custom document models, validation, human review_
- Error handling & resilience — _retries, scopes, run-after, idempotency_
- Long-running processes & approvals — _state, timeouts, escalation_

### A11. Models: Inference, Training & Fine-Tuning
- The training lifecycle — _pre-training, supervised fine-tuning, preference/RL tuning (concepts)_
- Prompting vs. RAG vs. fine-tuning — _decision framework; why fine-tuning is rarely first_
- Fine-tuning in Microsoft Foundry — _SFT, DPO, RFT; serverless vs. managed compute_
- Training data preparation — _JSONL chat format, data quality, splits_
- Distillation `[opt]` — _teaching a smaller model from a larger one_
- Microsoft 365 Copilot Tuning `[opt]` `[prev]` — _task-specific tuned models for declarative agents_
- Deploying & serving models — _deployments, quotas, versioning, regional considerations_
- Model lifecycle — _model retirements, upgrades and regression testing_

### A12. Evaluation & Observability
- Evaluation strategy — _offline vs. online; system vs. process (step) evaluation_
- Building an eval harness — _test datasets, graders, baselines, regression gates in CI_
- Copilot Studio agent evaluation (advanced) — _set-level grading, custom metrics, automation via API/connectors_
- Foundry evaluators — _groundedness, relevance, task adherence, tool call accuracy, safety_
- Agent Framework evaluation — _local checks + Foundry cloud evaluators_
- LLM-as-judge — _rubrics, calibration, bias pitfalls_
- Tracing & telemetry — _OpenTelemetry, Application Insights, environment-level telemetry_
- Production analytics & feedback — _turning sessions and reactions into new test cases_

### A13. Security, Safety & Moderation (advanced)
- Threat model for agents — _prompt injection (direct & indirect), data exfiltration, excessive agency_
- Azure AI Content Safety — _Prompt Shields, groundedness detection, custom categories_
- Moderation tuning — _per-agent / per-topic / per-prompt sensitivity in regulated scenarios_
- Data protection — _Microsoft Purview, sensitivity labels, auditing of agent sessions_
- DLP for connectors & MCP — _designing DLP policies that allow agents safely_
- AI red teaming `[opt]` — _AI Red Teaming Agent / PyRIT_

### A14. ALM, Governance & Operations
- Solutions deep dive — _environment variables, connection references, managed vs. unmanaged_
- Power Platform pipelines — _one-click dev → test → prod deployments_
- Dataverse Git integration — _committing agent changes to Azure DevOps / GitHub_
- CI/CD with GitHub Actions / Azure DevOps — _Power Platform Build Tools, automated evaluation gates_
- Managed Environments — _sharing limits, usage insights, pipelines requirements_
- Agent 365 & admin controls — _central control plane for agents across environments_
- Copilot Agent Kit `[opt]` — _test automation and governance tooling (formerly Copilot Studio Kit)_
- Cost management — _Copilot Credits capacity, AI Builder credits, Foundry spend_

---

## Review checklist for you

1. **Size.** Beginner is ~85 topics and Advanced ~105. roadmap.sh/ai-engineer has roughly 150. Do you want to cut either one?
2. **Snowflake SQL depth on Beginner (B10).** Keep all nine topics, or merge them into about five?
3. **A7 Pro-code Agents.** Keep all three pro-code routes (declarative agents, Agent Framework, Foundry Agent Service), or focus on one?
4. **Anything missing?** Some candidates:
   - Voice / real-time agents
   - Dataverse as a data platform
   - Fabric
   - Power Apps
5. **Section order.** Tell me if a section should move earlier or later.

## Primary sources used for this draft
- [Harnesses in Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview)
- [Agents powered by the GitHub Copilot harness](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/overview)
- [Skills overview (Copilot Studio)](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-overview)
- [What's new in Copilot Studio, August 2026](https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/new-and-improved-github-copilot-harness-agent-skills-and-richer-context/)
- [What's new in Copilot Studio, May 2026](https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/new-and-improved-computer-using-agents-a-new-workflows-experience-and-real-time-voice-experiences/)
- [What's new in Copilot Studio, April 2026](https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/new-and-improved-agent-governance-intelligent-workflows-and-connected-app-experiences/)
- [Agent flows and workflows overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview)
- [Extend your agent with MCP](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp)
- [Content moderation — generative answers FAQ](https://learn.microsoft.com/en-us/microsoft-copilot-studio/faqs-generative-answers)
- [About agent evaluation](https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-intro)
- [ALM strategy for Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/alm)
- [Add Snowflake as a knowledge source](https://learn.microsoft.com/en-us/power-platform/release-plan/2025wave1/microsoft-copilot-studio/add-snowflake-as-knowledge-source)
- [Agent Builder in Microsoft 365 Copilot](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder)
- [Create declarative agents with M365 Agents Toolkit](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/build-declarative-agents)
- [Microsoft 365 Copilot Tuning (preview)](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agent-builder-tuned-models)
- [AI Builder text generation (deprecated)](https://learn.microsoft.com/en-us/ai-builder/azure-openai-model-pauto)
- [Prompt engineering techniques — Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering)
- [Fine-tune models with Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry-classic/concepts/fine-tuning-overview)
- [Agent evaluators — Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/agent-evaluators)
- [Microsoft Agent Framework overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [Use Agent Skills in VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [Snowflake-managed MCP server](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp)
- [Cortex Agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents)
- [Cortex AISQL](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql)
