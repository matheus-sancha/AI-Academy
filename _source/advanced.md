---
id: advanced
order: 3
title: AI Engineering on Microsoft
subtitle: Advanced Roadmap
tagline: For engineers who finished Intermediate — mastering the editor agent, then building, shipping and operating pro-code agents, ending in a capstone build you write yourself.
next: index.html
next_label: Back to the program home
audience: Engineers
card: The pro-code toolchain, the agent harness and context engineering, authoring Agent Skills and building MCP servers, custom connectors and multi-agent, pro-code agents (Agents Toolkit, Agents SDK, Agent Framework, Foundry), evaluation and observability, security and ALM, and a capstone build you write end to end — with LLM internals, advanced RAG, Snowflake Cortex, automation and fine-tuning as reference.
---

# what-you-can-already-do | What You Can Already Do
The Intermediate topics this level takes for granted. None of them is taught again here — each one links back to where it is taught. Basic's own foundations sit behind Intermediate's assumed-knowledge module, so they are not repeated a second time.

## agent | What Is an Agent | assumed
A model in a loop with tools and a goal. Everything in this level is a variation on that sentence.

## autonomous | Conversational vs. Autonomous Agents | assumed
Whether a human is in the turn changes the failure modes, the testing and the approvals.

## orchestration | Orchestration | assumed
Describing what an agent should do and letting the runtime choose. Not re-taught; the loop underneath it is.

## chooseharness | Choosing a Harness in Copilot Studio | assumed
You have already made this choice once. Here you compare it with harnesses you build yourself.

## hitl | Human-in-the-Loop | assumed
Where a person has to confirm. The approval mechanics here assume you know why.

## instructions | Instructions | assumed
What goes in an instruction set and what does not belong there.

## xml | Structuring Instructions with XML Tags | assumed
The convention this level scales into layered, templated system prompts.

## triage | Instructions, Knowledge, Tool or Skill | assumed
The four-way decision. Pro-code adds places to put things; it does not change the question.

## successcriteria | Success Criteria Are Not Instructions | assumed
Why a criterion belongs in an evaluation. This level automates that evaluation.

## rag | What Is RAG | assumed
Retrieve, then answer from what you retrieved. The advanced RAG module engineers each half.

## sources | Knowledge Sources Overview | assumed
What a knowledge source is and what it costs you.

## tools | What Are Tools | assumed
That the model asks for a tool and something else runs it.

## tooldesc | Descriptions Decide Which Tool Fires | assumed
Learned once on Copilot Studio tools; applied here to MCP tool schemas.

## connectors | Power Platform Connectors | assumed
The catalogue you extend with custom connectors in this level.

## connauth | Connections & Authentication | assumed
Who a connection runs as. Agent identity here is the same question with a better answer.

## skill | What Is a Skill | assumed
Know-how the agent loads when it needs it.

## openformat | Agent Skills Is an Open Format | assumed
One artifact, several harnesses — which is why this level does not re-teach the format.

## skillmd | Anatomy of a SKILL.md | assumed
Front matter, body, bundled files. Authoring here starts from the far side of this.

## packaging | Packaging a Skill Without Breaking It | assumed
The mechanics of shipping one. This level covers when to bundle, not how to zip.

## sandbox | Scripts and the Sandbox | assumed
No network, no installs. The constraint every bundled script is written against.

## judge | How the Grading Actually Works | assumed
That a model grades the answer. This level builds graders of its own.

## testsets | Evaluation Sets | assumed
A question, a criterion, a thing that can fail. Eval harnesses automate exactly this.

## envs | Power Platform Environments | assumed
Dev, test and production as separate places.

## solutions | Solutions Basics | assumed
The unit that moves between them. The ALM module takes it apart.

## sfselect | Querying Basics | assumed
Enough SQL to read a result set and know whether it is plausible.

## sfviews | Views for AI Consumption | assumed
Clean, named, commented surfaces. The capstone's MCP server is built over one.

# developer-tooling | Developer Tooling
Set up the pro-code toolchain and the machine it runs on. Nothing from Intermediate is repeated here.

## vscode | VS Code for AI Engineering
VS Code is this level's build surface, not an optional extra: every MCP server, skill, agent definition, SQL file and evaluation script from here on is authored in it. Set up GitHub Copilot, the Copilot Studio extension, the Python or C# tooling, and optionally dev containers for reproducible environments.
- doc | Set up GitHub Copilot in VS Code | https://code.visualstudio.com/docs/setup/copilot
- doc | Build with AI in VS Code | https://code.visualstudio.com/docs/agents/overview

## localenv | Runtimes, Environments & Local Secrets
Copilot Studio gave you a browser. Pro-code gives you a machine to look after: a pinned runtime, an isolated environment per project, a lock file so a colleague gets the same versions, and secrets in a local file that never reaches Git. This is the step that most often breaks a first MCP server, and none of it is AI-specific.
- doc | Python environments in VS Code | https://code.visualstudio.com/docs/python/environments
- doc | Safe storage of app secrets in development (ASP.NET Core) | https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets
- video | Configure and use secret scanning in your GitHub repository (GH-500) | https://www.youtube.com/watch?v=mQB7FKqMq0Y

## agentmode | GitHub Copilot Agent Mode
In agent mode, Copilot plans multi-step changes, edits several files, runs terminal commands and calls tools, including MCP servers. It asks for approval before sensitive actions. Treat it as a junior engineer: give it clear context, review its diffs and keep tests in the loop.
- doc | Use chat in VS Code | https://code.visualstudio.com/docs/chat/chat-overview
- doc | Use tools with agents (VS Code) | https://code.visualstudio.com/docs/agents/run/tools
- video | Building applications with GitHub Copilot agent mode (Microsoft Learn) | https://www.youtube.com/watch?v=XnC6cF1v5OY

## csvscode | Copilot Studio VS Code Extension
The Copilot Studio extension lets you clone an agent into VS Code as YAML, edit topics, instructions and components with Copilot's help, and sync the changes back. It brings agents into Git-based workflows and code review.
- doc | Overview of the Microsoft Copilot Studio extension for Microsoft Visual Studio Code | https://learn.microsoft.com/en-us/microsoft-copilot-studio/visual-studio-code-extension-overview

## git | Git & GitHub for Agents
Version control is not optional once AI writes code and agents are defined as files. You need branching, pull requests, reviewing AI-generated changes and protecting secrets. It is also the basis for Dataverse Git integration and CI/CD later in this level.
- course | Introduction to Git (Microsoft Learn) | https://learn.microsoft.com/en-us/training/modules/intro-to-git/
- video | Configure and use secret scanning in your GitHub repository (GH-500) | https://www.youtube.com/watch?v=mQB7FKqMq0Y

## language | Python or C# Baseline
You need enough Python or C# to call model APIs, write an MCP server, script evaluations and use Microsoft Agent Framework. Pick one language for the team and stick with it.
- doc | Agent Framework — Step 1: Your First Agent (Python / .NET) | https://learn.microsoft.com/en-us/agent-framework/get-started/your-first-agent
- doc | C# Guide (.NET documentation) | https://learn.microsoft.com/en-us/dotnet/csharp/

# agent-harness | Agent Harness
The runtime around the model: loop, tools, permissions and recovery. You used one in Copilot Studio; now you look inside it.

## loop | The Agent Loop
Every agent runs a loop: read the goal and context, decide on an action, call a tool, look at the result, and repeat until done or stopped. Define stop conditions, step limits and failure handling explicitly; otherwise loops wander and cost money.
- article | Building Effective AI Agents (Anthropic Engineering) | https://www.anthropic.com/engineering/building-effective-agents
- doc | Agent Harness (Microsoft Agent Framework) | https://learn.microsoft.com/en-us/agent-framework/concepts/harness

## planning | Planning & Recovery
Capable harnesses break goals into steps, notice failures, retry and try other paths. You improve this with clear goals, good tool error messages and checkpoints, and by keeping deterministic workflows for steps that must never change.
- doc | Harnesses in Copilot Studio — GitHub Copilot harness | https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview
- doc | AI agent orchestration patterns (Azure Architecture Center) | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns

## permissions | Sandboxing, Permissions & Approvals
Decide what an agent may do without asking: read-only tools, a sandboxed file system, approval for writes, sends and payments. GitHub Copilot asks before running terminal commands; Copilot Studio's GitHub Copilot harness runs tasks in a governed sandbox.
- doc | Secure AI-assisted development in VS Code | https://code.visualstudio.com/docs/agents/run/security
- doc | Use tools with agents | https://code.visualstudio.com/docs/agents/run/tools

## ghharness | GitHub Copilot as a Harness
GitHub Copilot is one harness running on several surfaces: agent mode in VS Code, Copilot CLI in the terminal, and the cloud agent on GitHub.com and GitHub Mobile, which works in a hosted environment and opens a pull request per task. Each surface has different autonomy, tools and review points.
- doc | GitHub Copilot CLI | https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-cli
- doc | GitHub Copilot on GitHub.com and GitHub Mobile | https://docs.github.com/en/copilot/concepts/agents/cloud-agent
- video | Delegate issues to GitHub Copilot (Microsoft Learn) | https://www.youtube.com/watch?v=b66COmGO6vw

## customize | Customizing the Harness
You shape a harness through files it loads: `copilot-instructions.md` or `AGENTS.md` for repository context, prompt files for reusable tasks, custom agents for personas with their own tool sets, and skills for on-demand know-how.
- doc | Use custom instructions in VS Code | https://code.visualstudio.com/docs/agent-customization/custom-instructions
- doc | Use prompt files in VS Code | https://code.visualstudio.com/docs/agent-customization/prompt-files
- doc | Custom agents in VS Code | https://code.visualstudio.com/docs/agent-customization/custom-agents
- article | AGENTS.md — open format for agent instructions | https://agents.md/

## harnessvssdk | Harness vs. SDK vs. Platform
Use a managed harness (Copilot Studio, GitHub Copilot) when it fits. Build your own loop with an SDK such as Microsoft Agent Framework when you need custom orchestration, hosting or integration. Use a platform service such as Foundry Agent Service for managed runtime, identity and observability.
- article | Microsoft Agent Framework at BUILD 2026: Agent Harness, Hosted Agents, CodeAct | https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026-announce/
- doc | Choose Development Tools for Your Microsoft 365 Copilot Plugin | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/choose-plugin-development-tools

# context-engineering | Context Engineering
Design everything that enters the context window, not just the prompt.

## fromprompt | From Prompt Engineering to Context Engineering
Context engineering means curating the smallest, highest-signal set of tokens for each model call: instructions, tools, retrieved knowledge, memory and history. In agents, context builds up over many turns, so managing it becomes an engineering discipline.
- article | Effective context engineering for AI agents (Anthropic Engineering) | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- doc | Set up a context engineering flow in VS Code | https://code.visualstudio.com/docs/agents/guides/context-engineering-guide

## budget | The Context Window as a Budget
Treat the window as a limited budget shared by system instructions, tool definitions, knowledge chunks, conversation history, tool results and the output. Measure what each part costs, and cut what doesn't improve evaluation scores.
- article | Effective context engineering for AI agents (Anthropic Engineering) | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- doc | Understanding tokens (.NET AI docs) | https://learn.microsoft.com/en-us/dotnet/ai/conceptual/understanding-tokens

## xmltemplates | XML-Structured Context & Templates
Standardise how context is assembled with consistent XML sections such as `<role>`, `<rules>`, `<tools_guidance>`, `<knowledge>`, `<user_data>` and `<output_format>`, filled from templates and variables. Consistent structure makes behaviour easier to reproduce, test and review.
- doc | Prompt engineering techniques — add clear syntax | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering
- doc | Develop a RAG Solution on Azure — Prompt Engineering | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-prompt-engineering

## sysprompt | System Prompt Design at Scale
Large agents need layered instructions: global policy, then agent role, then task or skill instructions, then per-request data. Include explicit priorities for when rules conflict. Keep them versioned, reviewed and covered by evaluations, like code.
- doc | System message design | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/advanced-prompt-engineering
- video | Manage prompts for agents in Microsoft Foundry with GitHub (AI-300) | https://www.youtube.com/watch?v=10lrxyurK78

## toolshaping | Tool & Result Shaping
Every tool definition uses context, and so does every tool result. Write short, distinct tool descriptions, expose only the tools a task needs, and trim or summarise large tool outputs before they go back into the context.
- article | Effective context engineering for AI agents — The anatomy of effective context | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- doc | Use tools with agents (VS Code) | https://code.visualstudio.com/docs/agents/run/tools

## jit | Retrieval vs. Stuffing
Preloading every document you might need wastes context and confuses the model. Just-in-time retrieval, where the agent searches or opens files when it needs them, keeps context lean. Hybrid approaches preload a small core and retrieve the rest on demand.
- doc | Agentic retrieval overview (Azure AI Search) | https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview
- article | Effective context engineering for AI agents — Context retrieval and agentic search | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

## history | Conversation History & Compaction
Long conversations degrade quality and raise cost. Use compaction (summarising older turns), truncation, and structured notes that live outside the context. Research shows models use information at the start and end of long contexts better than information in the middle.
- article | Lost in the Middle: How Language Models Use Long Contexts (arXiv) | https://arxiv.org/abs/2307.03172
- doc | Agent Harness (Microsoft Agent Framework) | https://learn.microsoft.com/en-us/agent-framework/concepts/harness

## memory | Memory | prev
Short-term memory is the current conversation. Long-term memory keeps facts or preferences across sessions. Copilot Studio agents on the GitHub Copilot harness can turn memory on. Decide what may be remembered, for how long, and how users can see or remove it.
- doc | Memory (GitHub Copilot) (preview) — Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/memory-overview
- doc | Work IQ overview | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/

## caching | Prompt Caching | opt
Prompt caching reuses the processed form of a stable prompt prefix, such as long instructions or tool definitions, across calls. That cuts latency and cost. Design prompts so the stable parts come first and the variable parts come last.
- doc | Prompt caching with Azure OpenAI | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching

## ctxsecurity | Context as a Security Boundary
Anything you put in context can steer the model, including emails, web pages and documents written by attackers (indirect prompt injection). Mark untrusted data clearly ("spotlighting"), never let it act as instructions, and pair this with Prompt Shields and least-privilege tools.
- article | How Microsoft defends against indirect prompt injection attacks (MSRC) | https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks
- doc | Prompt Shields (Azure AI Content Safety) | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection

# authoring-skills | Agent Skills (Authoring)
You can already write a skill. This is the craft of writing one that fires when it should, stays small, and survives review.

## disclosure | Progressive Disclosure
Only the skill's name and description are always in context. The body loads when the skill activates, and bundled files load only when the instructions refer to them. That's why you can install many skills without filling the context window.
- article | Equipping agents for the real world with Agent Skills (Anthropic Engineering) | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- doc | Skills overview for agents (GitHub Copilot) — how the orchestrator invokes skills | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-overview

## descriptions | Writing Descriptions That Trigger
The description decides whether a skill runs at all. Say what the skill does and when to use it, using the words users actually type, and set clear boundaries so it doesn't fire on unrelated requests.
- doc | Create a skill for an agent (GitHub Copilot) — Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-create
- doc | Agent Skills specification — description field | https://agentskills.io/specification

## bundling | Bundling Scripts & Reference Data
Put deterministic work in scripts inside the skill, such as validating SQL, computing a figure with a fixed rule or formatting a report. Put detailed reference material, such as schemas or style guides, in separate files. The model follows the instructions; scripts do the precise parts. A script costs its output rather than its length, which is why code beats prose for anything mechanical.
- doc | Adding agent skills for GitHub Copilot | https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- article | anthropics/skills — Public repository for Agent Skills | https://github.com/anthropics/skills

## skillsvscode | Skills in VS Code / GitHub Copilot
Project skills live in the repository (for example `.github/skills/<name>/SKILL.md`) and are shared with everyone who clones it. Personal skills live in your user profile and reach nobody else. Which directories a session reads depends on the harness, the available frontmatter varies with it, and two naming mistakes stop a skill loading with no error.
- doc | Use Agent Skills in VS Code | https://code.visualstudio.com/docs/agent-customization/agent-skills
- doc | Adding agent skills for GitHub Copilot | https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills

## skilltest | Testing & Versioning Skills
Test skills in two ways, and neither has a product feature behind it. Trigger tests check that the skill activates on the right prompts and not on others, and are run by hand. Output tests check what the skill produces, in an eval harness over the whole agent. Only structural validation can be automated. The format has no version field, so keep skills in Git with change history and a review step, like any other code, and pin the ones you consume.
- doc | Create a single response test set (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-create

## skillgov | Sharing & Governing Skills | opt
A team skill library needs owners, a review process, security checks (bundled scripts run code) and a catalogue. Community collections are a good source of ideas, but review any third-party skill before you use it.
- article | github/awesome-copilot — community-contributed instructions, agents, skills and configurations | https://github.com/github/awesome-copilot

# building-mcp-servers | Building MCP Servers
You have added someone else's MCP server to an agent. Here you build, secure and ship your own.

## mcparch | MCP Architecture
MCP defines hosts (the AI application), clients (a connection held inside the host) and servers (which expose capabilities). Servers offer tools (actions), resources (data) and prompts (templates) over JSON-RPC. Since the 2026-07-28 revision the protocol is stateless: there is no handshake, and every request carries its own protocol version and capabilities. The same revision deprecates sampling and logging, which older tutorials still build on.
- doc | Architecture overview (Model Context Protocol) | https://modelcontextprotocol.io/docs/learn/architecture
- article | Model Context Protocol (MCP) Curriculum for Beginners (Microsoft) | https://github.com/microsoft/mcp-for-beginners

## transports | Transports
Local servers usually use stdio: a process on your machine that the client starts. Remote servers use Streamable HTTP; the older HTTP+SSE transport is deprecated, and the 2026-07-28 revision removed protocol-level sessions, the GET event stream and stream resumability. Remote servers need authentication, network controls and monitoring; local ones inherit your machine's permissions.
- doc | Overview — Transports (MCP specification) | https://modelcontextprotocol.io/specification/latest/basic/transports

## mcpvscode | Using MCP Servers in VS Code
Add a server through the guided flow, which asks for a transport, an ID and a scope, and writes the file. Which file has moved: a global Copilot config and a workspace-root portable file are the current targets, and `.vscode/mcp.json` is now a compatibility path. Check that you trust each server, pick which tools are enabled, and expect your organization to restrict what is available. It's the fastest way to prototype and test a server before giving it to Copilot Studio.
- doc | Add MCP servers in VS Code | https://code.visualstudio.com/docs/agent-customization/mcp-servers

## buildmcp | Building an MCP Server
Use an official SDK — Python here, with TypeScript, Java, Kotlin, C#, Ruby, Rust and Go also documented — to expose a few well-described tools with typed inputs. In Python the type hints and docstring *are* the tool definition. Keep tools small and specific, return concise results, and handle errors with messages the model can act on.
- doc | Build an MCP server | https://modelcontextprotocol.io/docs/develop/build-server
- video | Copilot Studio: Create An MCP Server With Python (Matthew Devaney) | https://www.youtube.com/watch?v=kKJ391VKYJo
- article | Create an MCP server and deploy to Copilot Studio (Matthew Devaney) | https://www.matthewdevaney.com/create-an-mcp-server-and-deploy-to-copilot-studio/

## mcpauth | Authentication for MCP
Remote MCP servers use OAuth 2.1, so every tool call runs with a real identity and can be audited. The server is a resource server: it validates tokens rather than issuing them, and it must check that each token was issued for it. A stdio server does the opposite and takes credentials from its environment. Avoid shared API keys for tools that touch user data, and never forward a client's token upstream.
- doc | Authorization (MCP specification) | https://modelcontextprotocol.io/specification/latest/basic/authorization

## mcpcs | Handing Your Server to Copilot Studio
Consuming someone else's server is behind you; this is the other side of it. Register the server you built, and accept what that makes you responsible for: your tool changes now reach every agent using it automatically, a server-level description written in Copilot Studio rather than in your code decides whether the orchestrator routes to you at all, and the server arrives in the tenant as a Power Platform connector — so connector authentication, data policies and connector governance are now yours. Streamable transport only, tools and resources only.
- doc | Extend your agent with Model Context Protocol | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp
- doc | Configure data policies for agents (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention

## sfmcp | Snowflake-Managed MCP Server
Snowflake hosts MCP servers declared as schema objects, exposing Cortex Analyst, Cortex Search, Cortex Agents, coding agents, custom UDFs and procedures, and SQL execution. Snowflake OAuth and role-based access control govern them in two layers: reaching the server and discovering its tools is one grant, invoking any tool needs another on the object underneath. It gives Microsoft agents governed access to Snowflake data, with tool capabilities only.
- doc | Snowflake-managed MCP server | https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp

## mcpsec | MCP Security
Most MCP-specific risk is in the plumbing rather than in the model:
- tool poisoning (malicious tool descriptions), including definitions amended after approval
- indirect prompt injection through tool results
- confused-deputy authorization, where a proxy's static client ID meets a reusable consent cookie
- token passthrough and missing audience validation
- server-side request forgery through the URLs a client fetches during discovery
- state-handle hijacking, now that the protocol has no sessions
- untrusted local servers, which run with the client's privileges
- over-broad OAuth scopes granted up front

Mitigate with least privilege, per-client consent, audience validation, allow-lists, reviewing servers before use and DLP.
- doc | Security Best Practices (Model Context Protocol) | https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices
- article | Protecting against indirect prompt injection attacks in MCP (Microsoft for Developers) | https://developer.microsoft.com/blog/protecting-against-indirect-injection-attacks-mcp/

## mcpcert | MCP Certification | opt
Microsoft runs a certification program (in preview) for MCP servers that checks reliability, security, compliance and responsible operation. Only verified publishers that own the endpoint may submit, so a server built for your own agents is not eligible — prefer certified servers where you can, and run the program's review stages as your own gate on the ones you build.
- doc | Microsoft MCP server certification overview (preview) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-certification
- doc | What's new in Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/whats-new

# advanced-tools-and-multi-agent | Advanced Tools, Connectors & Multi-Agent
Integrate anything, share connections safely and coordinate several agents.

## customconn | Custom Connectors
When no prebuilt connector exists, wrap a REST or SOAP API as a custom connector, from an OpenAPI definition, a Postman collection or the portal. Add authentication — Entra ID is the recommended option — and clear operation descriptions. A connector built in Power Automate or Power Apps then works in both and in Copilot Studio, though one built in Logic Apps does not travel.
- doc | Custom connectors overview | https://learn.microsoft.com/en-us/connectors/custom-connectors/
- article | Make your first custom connector for Power Automate and Power Apps (Matthew Devaney) | https://www.matthewdevaney.com/make-your-first-custom-connector-for-power-automate-and-power-apps/

## restapi | REST API Tools | prev
Between "a connector exists" and "I will build one" sits a third option, in preview: upload an OpenAPI v2 definition and get tools on one agent, configured per agent rather than registered across the tenant. Describe every operation carefully — the product will not let you leave a description blank, because the orchestration reads it to decide when to call the tool.
- doc | Extend your agent with tools from a REST API (preview) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-rest-api

## connrefs | Connection References & Service Principals
Connection references separate a solution from the credentials it uses, so each environment can bind its own connection on import. Decide the owner before the first import, because ownership cannot be transferred afterwards, and sharing to a service principal is the one documented route to a non-human activator. Secrets your logic reads are a separate mechanism: environment variables backed by Azure Key Vault.
- doc | Use a connection reference in a solution with Microsoft Dataverse | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-connection-reference
- article | How To Setup A Power Platform Environment Variable Secret (Matthew Devaney) | https://www.matthewdevaney.com/how-to-setup-a-power-platform-environment-variable-secret/

## cuaadv | Computer Use (Advanced) | opt
In production, computer use needs secure credential storage, a choice of model, a configured reviewer and monitoring — and an honest reading of what its guardrails promise, since access control governs actions rather than reach and human supervision is not a fail-safe. Windows 365 for Agents gives agents managed Cloud PCs for desktop automation.
- doc | Automate web and desktop apps with computer use | https://learn.microsoft.com/en-us/microsoft-copilot-studio/computer-use
- doc | Windows 365 for Agents documentation | https://learn.microsoft.com/en-us/windows-365/agents/

## multiagent | Multi-Agent Patterns
The five documented patterns:
- **Sequential:** a pipeline, with the next agent chosen by the workflow rather than by a model.
- **Concurrent:** fan out to independent agents, then merge the results yourself.
- **Group chat:** agents discuss in one thread under a chat manager, read-only, three or fewer.
- **Handoff:** control transfers to a specialist, one agent at a time.
- **Magentic:** a manager agent builds a task ledger for an open-ended problem.

Use the lowest level of complexity that works: a single agent with tools is the documented default, and the reasons to go further are prompt complexity, tool overload or a security requirement.
- doc | AI Agent Orchestration Patterns (Azure Architecture Center) | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- video | Multi-Agent Workflows In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=gIlSJHRRoj0
- video | Orchestrate a multi-agent solution using the Microsoft Agent Framework (AI-103 Ep. 14) | https://www.youtube.com/watch?v=l3oAcAWySlE

## a2a | Agent-to-Agent (A2A)
A2A is an open protocol, at version 1.0 and governed by the Agentic AI Foundation, for communication between "opaque agentic applications" — agents you cannot see inside. An Agent Card advertises skills and security schemes, a Task carries a lifecycle, and identity sits at the transport layer rather than in the payload. Copilot Studio can add an A2A agent and delegate to it, sending the full chat history with the request.
- doc | A2A Protocol | https://a2a-protocol.org/latest/
- doc | Connect to an agent over the Agent2Agent (A2A) protocol | https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-agent-to-agent

## agentid | Agent Identity
Microsoft Entra Agent ID gives agents their own identities, so they can be governed, given permissions and audited. A blueprint provisions them and holds their credentials, much as an app registration stands behind a service principal. Design permissions for the agent itself, not only for the maker — and note that the design is mostly subtractive: privileged roles are barred, four Graph permissions cannot be consented to at all, and an agent cannot satisfy MFA.
- doc | Microsoft Entra Agent ID documentation | https://learn.microsoft.com/en-us/entra/agent-id/

# pro-code-agents | Pro-Code Agents
Build agents in code when low-code limits you — and know which of the four routes you are on.

## lowvspro | Low-Code vs. Pro-Code Decision
Choose per component, by its hardest requirement — and a working system usually spans more than one route:
- **Agent Builder:** natural-language configuration with no source project.
- **Copilot Studio:** managed integrations, workflow logic, environments and lifecycle.
- **Declarative agents with Work IQ Dev Tools (preview) or the Agents Toolkit:** source-controlled manifests, environments and CI for Microsoft 365 Copilot agents.
- **A custom engine agent:** your own orchestration and models, through the Agents SDK or another custom-engine stack.
- doc | Choose development tools for your plugin | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-tool-comparison
- video | Choose a Microsoft 365 Copilot extensibility development path (MS-4010) | https://www.youtube.com/watch?v=ARPj2XpkCpU

## declarative | Declarative Agents with M365 Agents Toolkit
Declarative agents customise Microsoft 365 Copilot through a manifest: instructions, knowledge, capabilities and actions. They run on Copilot's own managed orchestrator, which configuration influences but never replaces. The Agents Toolkit in VS Code keeps the definition in source control and provisions it into a tenant, where it is tested in Copilot itself.
- doc | Create declarative agents by using Microsoft 365 Agents Toolkit and JSON | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/build-declarative-agents
- doc | Declarative agent architecture | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-architecture
- video | Build a declarative agent for Microsoft 365 Copilot using Visual Studio Code (MS-4010 Ep. 5) | https://www.youtube.com/watch?v=2VPAPMOfeZc

## plugins | API Plugins & TypeSpec | opt
Plugins give declarative agents actions, from OpenAPI-described APIs or from remote MCP servers, and exist only inside an agent. TypeSpec defines the agent in one typed source that provisioning writes into the manifests.
- doc | MCP and API plugins for declarative agents | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/overview-plugins
- doc | Create declarative agents by using Microsoft 365 Agents Toolkit and TypeSpec for Microsoft 365 Copilot | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/build-declarative-agents-typespec
- video | Build your first action for declarative agents with API plugin (MS-4010 Ep. 6) | https://www.youtube.com/watch?v=692C_5Z6Wtg

## customengine | Custom Engine Agents & M365 Agents SDK
Custom engine agents bring your own orchestration and models into Teams and Microsoft 365 Copilot. The Microsoft 365 Agents SDK handles channels, activities and authentication, and you choose the AI stack behind it.
- doc | Custom engine agents for Microsoft 365 | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/overview-custom-engine-agent
- doc | What is the Microsoft 365 Agents SDK | https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/agents-sdk-overview

## maf | Microsoft Agent Framework
Microsoft Agent Framework is the successor to Semantic Kernel and AutoGen. It is an SDK for Python and .NET (with Go in preview) for building agents with tools, MCP, context providers, middleware and telemetry, and it works with Azure OpenAI, Foundry, Anthropic and other providers.
- doc | Microsoft Agent Framework overview | https://learn.microsoft.com/en-us/agent-framework/overview/
- doc | Step 1: Your First Agent | https://learn.microsoft.com/en-us/agent-framework/get-started/your-first-agent
- video | Develop an AI agent with the Microsoft Agent Framework (AI-103) | https://www.youtube.com/watch?v=WznrISPGx-g

## mafworkflows | Agent Framework Workflows
Workflows in Agent Framework are explicit execution paths for code, agents and human input. Every SDK has a graph API of executors and edges, and Python adds an experimental functional API over the same run model. Capabilities add human-in-the-loop pauses, checkpoints, observability and five prebuilt orchestrations: sequential, concurrent, handoff, group chat and Magentic.
- doc | Workflow capabilities (Microsoft Agent Framework) | https://learn.microsoft.com/en-us/agent-framework/workflows/
- doc | Workflow concepts | https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/
- video | Orchestrate a multi-agent solution using the Microsoft Agent Framework (AI-103 Ep. 14) | https://www.youtube.com/watch?v=l3oAcAWySlE

## foundryagents | Foundry Agent Service & Hosted Agents
Foundry Agent Service runs agents with managed conversations, shared toolboxes of tools, identity and observability. A prompt agent is configuration that Foundry runs. A hosted agent is your own code in a container, for example an Agent Framework agent, on that managed runtime, with its own Entra identity and one immutable version served at a time.
- doc | What is Microsoft Foundry Agent Service? | https://learn.microsoft.com/en-us/azure/foundry/agents/overview
- doc | Hosted agents in Foundry Agent Service | https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents
- video | Develop AI agents with Microsoft Foundry and Visual Studio Code (AI-103) | https://www.youtube.com/watch?v=EmBPT_tIs8Y

## byom | Bring a Foundry Model into Copilot Studio | opt
You can connect a model deployed in Microsoft Foundry to a Copilot Studio prompt, for example an open or specialised model, and the prompt runs on it wherever it is used. The agent's own model, orchestration and channels stay Copilot Studio's. Only chat-completion deployments connect.
- doc | Bring your own model for your prompts | https://learn.microsoft.com/en-us/microsoft-copilot-studio/bring-your-own-model-prompts
- video | Master Copilot Studio Prompts with Azure AI Foundry Models (Matthew Devaney) | https://www.youtube.com/watch?v=ShphK8L3y2Y
- article | Azure AI Foundry model in Copilot Studio custom prompts (Matthew Devaney) | https://www.matthewdevaney.com/azure-ai-foundry-model-in-copilot-studio-custom-prompts/

# evaluation-and-observability | Evaluation & Observability
Measure quality continuously and see what agents actually do. Intermediate ran one evaluation by hand; this automates it and puts it in a pipeline.

## evalstrategy | Evaluation Strategy
Plan evaluation in four stages: a foundational test set, a recorded baseline, expansion by quality category (core, robustness, architecture, edge cases) and a continuous operation that re-runs the suite on model, knowledge or tool changes. Grade the outcome (system evaluation) and the steps (process evaluation), and write acceptance criteria before you build.
- doc | Evaluate your AI agents (Microsoft Foundry) | https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/evaluate-agent
- doc | Review the agent evaluation checklist | https://learn.microsoft.com/en-us/agents/agent-evaluation/evaluation-checklist
- video | Evaluate and optimize AI agents through structured experiments (AI-300) | https://www.youtube.com/watch?v=8zO5hApUxYo

## evalharness | Building an Eval Harness
An eval harness has four parts: versioned datasets, a runner that calls the agent, graders (code checks and LLM judges) and a report that compares against something. Foundry's GitHub Action runs and reports with statistics but has no threshold. Its Azure Developer CLI extension fails a build below a pass rate, and a per-case baseline you commit asks a different question. Run it in CI on the changes that matter, not every commit.
- doc | How to run an evaluation in GitHub Action | https://learn.microsoft.com/en-us/azure/foundry/how-to/evaluation-github-action
- video | Automate AI evaluations with Microsoft Foundry and GitHub Actions (AI-300) | https://www.youtube.com/watch?v=vMleA0GZgSQ

## csevaladv | Copilot Studio Agent Evaluation (Advanced)
Go beyond General quality on the standard harness: choose among seven more test methods, define a custom method with labels (for example, to pass a correct refusal), and run richer tests such as multi-turn, plan validation and attachment checks in the Copilot Agent Kit.
- doc | Choose evaluation methods | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-overview
- doc | Configure tests in Copilot Agent Kit | https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/kit-configure-tests
- video | Copilot Studio Test Automation: STOP Testing Manually!! (Matthew Devaney) | https://www.youtube.com/watch?v=qh4YRqZgaQU

## foundryevals | Foundry Evaluators
Foundry provides built-in evaluators for:
- general quality, text similarity and retrieval (groundedness, relevance, coherence)
- agent behaviour: system evaluators for the outcome (task adherence, intent resolution) and process evaluators for each tool call (tool call accuracy)
- risk and safety, and rubric evaluators scored against weighted criteria you write

Composite evaluators batch several into one judge call, and custom evaluators cover domain-specific rules.
- doc | Agent evaluators | https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/agent-evaluators
- doc | Built-in evaluators reference | https://learn.microsoft.com/en-us/azure/foundry/concepts/built-in-evaluators

## mafeval | Agent Framework Evaluation
Agent Framework includes evaluation support. You can run fast local checks while developing, call Foundry cloud evaluators for production-grade grading, or combine both in one run.
- doc | Evaluation (Microsoft Agent Framework) | https://learn.microsoft.com/en-us/agent-framework/agents/evaluation

## llmjudge | LLM-as-Judge
LLM judges scale grading of open-ended answers, but a judge is a model with its own errors and its own bill. Pick the cheapest grader that can decide, write a rubric with weighted criteria, calibrate the judge against human labels and pin its model, and keep deterministic checks wherever possible.
- doc | Observability in generative AI | https://learn.microsoft.com/en-us/azure/foundry/concepts/observability
- doc | Built-in evaluators reference | https://learn.microsoft.com/en-us/azure/foundry/concepts/built-in-evaluators

## tracing | Tracing & Telemetry
Traces record the steps of a run, its tool calls, tokens, latency and exceptions, which you need to debug agents. Foundry traces hosted agents server-side with no code once Application Insights is connected, and supports OpenTelemetry instrumentation of your own code; Copilot Studio can send telemetry from agents on its standard harness to Application Insights. A trace copies tool arguments and results, so decide who may read it.
- doc | Set up tracing in Microsoft Foundry | https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/trace-agent-setup
- doc | Agent-level telemetry with Application Insights (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-bot-framework-composer-capture-telemetry
- video | Implement observability and monitoring for generative AI workloads (AI-300) | https://www.youtube.com/watch?v=igglwJgwzkI

## prodfeedback | Production Analytics & Feedback
Intermediate taught the loop on Copilot Studio's Monitor page. For a pro-code agent the signals come from Application Insights and Foundry monitoring: operational metrics, sampled continuous evaluation, scheduled evaluation and alerts. Decide where each failure lived, so it becomes a live case or an offline test, and put it into the harness you own.
- doc | Monitor agent performance in Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-overview
- doc | Observability in generative AI | https://learn.microsoft.com/en-us/azure/foundry/concepts/observability
- video | Monitor, analyze, and tune AI agents (AB-100 Ep. 11) | https://www.youtube.com/watch?v=JR6C87ZEtws

# security-advanced | Security, Safety & Moderation (Advanced)
Threat-model agents and apply layered defences.

## threats | Threat Model for Agents
Key risks include prompt injection (direct and indirect), sensitive data disclosure, excessive agency (tools that can do too much), insecure output handling, supply-chain risks in models, MCP servers and skills, and unbounded consumption.
- doc | 2025 Top 10 Risk & Mitigations for LLMs and Gen AI Apps (OWASP) | https://genai.owasp.org/llm-top-10/
- video | Design responsible AI security, governance, risk management, and compliance (AB-100) | https://www.youtube.com/watch?v=yG_Rq-VNJaU

## contentsafety | Azure AI Content Safety
Content Safety provides harm classifiers, Prompt Shields (jailbreak and indirect injection detection), groundedness detection (preview, retiring in April 2027) and protected material detection. Use it in pro-code apps, and understand the equivalent filtering built into Copilot Studio.
- doc | What is Azure AI Content Safety? | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview
- doc | Prompt Shields in Azure AI Content Safety | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection
- video | Implement a responsible generative AI solution in Microsoft Foundry (AI-103) | https://www.youtube.com/watch?v=H5wPr-Ca2UM

## modtuning | Moderation Tuning
Tune moderation for the scenario. Regulated or document-processing work may need per-prompt sensitivity settings so legitimate content (medical, legal, security) isn't blocked. Record why you chose each setting, and cover these cases in evaluations.
- doc | FAQ for generative answers | https://learn.microsoft.com/en-us/microsoft-copilot-studio/faqs-generative-answers
- doc | Resolve responsible AI content filter errors | https://learn.microsoft.com/en-us/troubleshoot/power-platform/copilot-studio/generative-answers/agent-response-filtered-by-responsible-ai

## purview | Data Protection with Microsoft Purview
Purview extends sensitivity labels, data loss prevention, auditing and data security posture management to Copilot and agent interactions. Agents should respect labels, and their interactions should be auditable.
- doc | Microsoft Purview data security and compliance protections for Microsoft 365 Copilot and other generative AI apps | https://learn.microsoft.com/en-us/purview/ai-microsoft-purview
- video | Discover, protect, govern, and detect AI interactions with Microsoft Purview (SC-401) | https://www.youtube.com/watch?v=lVukA34ug4k

## dlpdesign | DLP for Connectors & MCP
Design Power Platform data policies that let agents work safely. Group connectors into business, non-business and blocked. Control HTTP and custom connectors, MCP servers, knowledge sources and channels, and apply stricter policies to production environments.
- doc | Data policies | https://learn.microsoft.com/en-us/power-platform/admin/wp-data-loss-prevention
- doc | Configure data policies for agents (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention

## redteam | AI Red Teaming | opt
Red teaming probes agents with adversarial prompts, such as jailbreaks, injections and harmful requests, before attackers do. Foundry's AI Red Teaming Agent (in preview) and the open-source PyRIT tool automate scans and produce risk reports.
- doc | Run AI Red Teaming Agent Locally (Azure AI Evaluation SDK) | https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/run-scans-ai-red-teaming-agent
- article | microsoft/PyRIT: Open-source AI red teaming toolkit from Microsoft (GitHub) | https://github.com/microsoft/PyRIT

# alm-and-governance | ALM, Governance & Operations
Ship agents like software: repeatable, reviewed, monitored and cost-controlled.

## solutionsdeep | Solutions Deep Dive
A solution carries an environment variable's definition, not its value, and some parts of a Copilot Studio agent aren't solution-aware at all: Application Insights, authentication, channels and sharing. Knowing what travels, and what you must set by hand afterwards, is what makes pipelines work.
- doc | Environment variables for Power Platform overview | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/environmentvariables
- doc | Establish an application lifecycle management strategy | https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/alm

## pipelines | Power Platform Pipelines
Pipelines deploy solutions from development to test to production with approvals, pre-deployment validation and history, all from inside the maker experience. Microsoft's Copilot Studio guidance aims them at citizen developers, and pro-code teams extend them with their own CI/CD.
- doc | Overview of pipelines in Power Platform | https://learn.microsoft.com/en-us/power-platform/alm/pipelines
- article | Create a Power Platform pipeline (Matthew Devaney) | https://www.matthewdevaney.com/the-complete-power-platform-pipelines-alm-setup-guide/create-a-power-platform-pipeline/

## gitintegration | Dataverse Git Integration
Dataverse Git integration connects a development environment to Azure DevOps or GitHub. You commit a solution's objects as source files, review them in pull requests, and keep other development environments in step by pulling accepted changes into their branches.
- doc | Overview of Git integration in Power Platform | https://learn.microsoft.com/en-us/power-platform/alm/git-integration/overview
- article | Setup Dataverse Git Integration For A Solution (Matthew Devaney) | https://www.matthewdevaney.com/the-complete-power-platform-pipelines-alm-setup-guide/setup-dataverse-git-integration-for-a-solution/

## cicd | CI/CD with GitHub Actions / Azure DevOps
For enterprise automation, use GitHub Actions for Power Platform or Power Platform Build Tools for Azure DevOps. They import, export, check and deploy solutions and provision environments. None runs an agent evaluation, so the gate for a pro-code agent or an MCP server is a workflow you write.
- doc | GitHub Actions for Microsoft Power Platform | https://learn.microsoft.com/en-us/power-platform/alm/devops-github-actions
- doc | Automate deployments with Dataverse Git integration and pipelines in Power Platform | https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/enterprise-power-platform-alm
- video | Design ALM process for AI-powered business solutions (AB-100) | https://www.youtube.com/watch?v=bcKJaKNRT1c

## managedenvs | Managed Environments
Managed Environments add governance at environment level and enforce licences. Microsoft's overview names 21 features, among them sharing limits, solution checker, weekly usage insights, maker welcome content and pipelines. Pipeline targets must be managed, and developer environments can no longer stay unmanaged.
- doc | Managed environments overview | https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-overview
- article | Create Power Platform environments for Dev-Test-Prod (Matthew Devaney) | https://www.matthewdevaney.com/the-complete-power-platform-pipelines-alm-setup-guide/create-power-platform-environments-for-dev-test-prod/

## agent365 | Agent 365 & Admin Controls
Microsoft Agent 365, generally available since May 2026, is a central control plane: an inventory of agents across platforms with unified policies, security and lifecycle management. Engineers should build agents that meet these controls from the start.
- doc | Microsoft Agent 365 documentation | https://learn.microsoft.com/en-us/microsoft-agent-365/
- doc | Security and governance (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance

## agentkit | Copilot Agent Kit | opt
The Copilot Agent Kit, formerly the Copilot Studio Kit, adds tooling for Copilot Studio teams: automated testing, conversation KPIs, a compliance hub and an agent inventory. Its pipeline page documents a pre-deployment test step.
- doc | Copilot Agent Kit overview | https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/kit-overview
- article | Configure MS auth for test automation in Copilot Studio Kit (Matthew Devaney) | https://www.matthewdevaney.com/configure-ms-auth-for-test-automation-in-copilot-studio-kit/

## costs | Cost Management
Track the whole bill: Copilot Credits for building, testing and running agents; AI Builder credits; Foundry model tokens and provisioned throughput; Snowflake credits. Set per-agent limits and alerts, and report cost per agent. Copilot Studio's reports give no per-conversation figure.
- doc | Manage Copilot Credits and capacity | https://learn.microsoft.com/en-us/power-platform/admin/manage-copilot-studio-copilot-credits-capacity
- doc | Licensing and AI Builder credits | https://learn.microsoft.com/en-us/ai-builder/credit-management
- doc | Provisioned throughput for Foundry Models | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/provisioned-throughput

# capstone-build | The Capstone Build
Everything in this level, in one project you build yourself: an MCP server over Technik's Teamcenter data, an agent over it, evaluated and shipped. Written in full — there is no route elsewhere to follow. Each page is one stage: what you need, what to do, what you should be holding when it ends, and what to check if yours looks different.

## buildsetup | Before You Start
What the capstone needs before stage one: a Python toolchain, a repository you can push to, a Snowflake account seeded from the capstone's script with a role that reads the Teamcenter views, an Azure subscription with a Foundry project, and an MCP-capable client. Everything is checkable in advance, and every later stage assumes the check passed — a missing Snowflake grant surfaces three stages later as an empty result set, not as an error.
- doc | Build an MCP server | https://modelcontextprotocol.io/docs/develop/build-server
- doc | Overview of access control | https://docs.snowflake.com/en/user-guide/security-access-control-overview

## stagescaffold | Stage 1 — Scaffold the Project
Create the repository, pin the SDK versions, and put the agent's instructions and evaluation set under source control from the first commit. You end this stage with a project that runs and does nothing, which is the point: every later stage is a diff you can review.
- doc | Step 1: Your First Agent | https://learn.microsoft.com/en-us/agent-framework/get-started/your-first-agent
- doc | Use custom instructions in VS Code | https://code.visualstudio.com/docs/agent-customization/custom-instructions

## stagemcp | Stage 2 — An MCP Server over Teamcenter
Expose three narrow tools over the Teamcenter views: look up a document by its identifier, list the documents for an operation, and fetch a revision's status. Typed inputs, concise results, and errors the model can act on. You end this stage with a server you can call from agent mode in VS Code before any agent exists.
- doc | Build an MCP server | https://modelcontextprotocol.io/docs/develop/build-server
- doc | Add and manage MCP servers in VS Code | https://code.visualstudio.com/docs/agent-customization/mcp-servers

## stageagent | Stage 3 — Wire the Agent
Put an agent in front of the server: layered instructions, the three tools, and a refusal path for questions the tools cannot answer. You end this stage with an agent that answers the capstone's questions and declines the rest — and the declining is the part worth checking, because an agent that answers everything has stopped using the tools.
- doc | Microsoft Agent Framework overview | https://learn.microsoft.com/en-us/agent-framework/overview/
- doc | How to use function calling with Microsoft Foundry Models | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/function-calling

## stageevals | Stage 4 — Write the Evals
Turn the questions you have been testing by hand into a versioned set with graders, and run it from CI so a change to instructions, tools or model cannot merge without a result. You end this stage with a report that compares against a baseline, and at least one case that fails on purpose.
- doc | How to run an evaluation in GitHub Action | https://learn.microsoft.com/en-us/azure/foundry/how-to/evaluation-github-action
- doc | Agent evaluators | https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/agent-evaluators
- doc | Evaluation (Microsoft Agent Framework) | https://learn.microsoft.com/en-us/agent-framework/agents/evaluation

## stageship | Stage 5 — Ship It
Deploy the server and the agent, give the agent its own identity, put the evaluation in the release gate, and turn on tracing before anyone else uses it. You end this stage with something a colleague can open, and a trace you can read when they tell you it was wrong.
- doc | Hosted agents in Foundry Agent Service | https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents
- doc | Microsoft Entra Agent ID documentation | https://learn.microsoft.com/en-us/entra/agent-id/
- doc | Set up tracing for AI agents in Microsoft Foundry | https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/trace-agent-setup

# llm-internals | LLM Internals for Engineers
Reference, not a read-through. Come here when quality, latency or cost needs an explanation rather than a guess.

## transformers | Transformers & Attention (Intuition)
LLMs are transformer networks. Attention lets each token's vector be shaped by the tokens around it, and generation runs one token at a time with the whole sequence in view. That explains why longer prompts cost more, why output length sets latency, and why a model answers only from what the sequence holds.
- course | Introduction to generative AI and agents (Microsoft Learn training) | https://learn.microsoft.com/en-us/training/modules/fundamentals-generative-ai/
- doc | LLM fundamentals (Microsoft Agent Framework learning journey) | https://learn.microsoft.com/en-us/agent-framework/journey/llm-fundamentals

## tokenbudget | Tokenization in Practice
Measure tokens with the model's own tokenizer and the usage the service returns, not estimates. Build token budgets for instructions, tools, knowledge and history, and watch for hidden token costs such as tool definitions, retrieved chunks and reasoning tokens. Quota is a shared tokens-per-minute pool, and it can return a 429 before your window is full.
- doc | Understanding tokens (.NET AI docs) | https://learn.microsoft.com/en-us/dotnet/ai/conceptual/understanding-tokens
- doc | Azure OpenAI in Microsoft Foundry Models Quotas and Limits | https://learn.microsoft.com/en-us/azure/foundry/openai/quotas-limits
- video | Why your AI costs spike (tokens explained) | https://www.youtube.com/watch?v=NmkR7V_wTqA

## params | Inference Parameters
Beyond temperature and top_p, engineers set an output cap, a response format, reasoning effort and whether a response is stored. The same intent is spelled differently on Chat Completions and the Responses API, and reasoning models do not support some sampling settings.
- doc | Use the Azure OpenAI Responses API | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses
- doc | Azure OpenAI reasoning models — supported parameters | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning

## reasoning | Reasoning Models
Reasoning models spend extra hidden "thinking" tokens before answering, billed as output and held in the context window. They are better at multi-step logic, planning and coding, at the price of latency and tokens. Set the reasoning effort deliberately, check for incomplete responses, and carry reasoning items between tool calls.
- doc | Azure OpenAI reasoning models | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning
- video | Optimize generative AI model performance with Microsoft Foundry (AI-103) | https://www.youtube.com/watch?v=Ocx76q4p9ME

## embeddings | Embeddings
An embedding is a vector that captures the meaning of text, so similar meanings sit close together. Embeddings power vector search and the retrieval behind RAG. A vector query always returns its nearest neighbours, near or not, so decide what counts as no match, and record the embedding model with the index.
- doc | How embeddings extend your AI model's reach (.NET) | https://learn.microsoft.com/en-us/dotnet/ai/conceptual/embeddings
- doc | Vector search overview (Azure AI Search) | https://learn.microsoft.com/en-us/azure/search/vector-search-overview

## functioncalling | Function / Tool Calling
With function calling, the model returns a structured request to call a tool: a name plus JSON arguments. Your code or the harness runs the tool and sends the result back in a second call, so the model proposes and your code validates and decides. The page's advice is to validate every call, grant least privilege and confirm actions.
- doc | How to use function calling with Microsoft Foundry Models | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/function-calling
- video | Develop generative AI apps that use tools (AI-103) | https://www.youtube.com/watch?v=N5DcQ-ZNp_M

## structured | Structured Outputs
Structured outputs hold a response to a JSON schema, so downstream code, flows and databases can rely on its shape, which the older JSON mode could not guarantee. The schema is a subset of JSON Schema, and it checks shape, never whether a value is true.
- doc | How to use structured outputs with Azure OpenAI in Microsoft Foundry Models | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs
- doc | Prompts overview (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/prompts-overview

## latency | Latency, Throughput & Cost
Production AI trades off time to first token, total latency, throughput and cost. Time to the last token is the time to the first token plus the time between tokens times the tokens generated, so output length usually dominates. The page's levers are model choice, generation size, streaming, content filtering, separate workloads, prompt size and batching requests, and capacity (quota or provisioned throughput) sits beneath them.
- doc | Azure OpenAI in Microsoft Foundry Models performance & latency | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/latency
- doc | Provisioned throughput for Foundry Models | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/provisioned-throughput

## deploytypes | Foundry Deployment Types | opt
Microsoft Foundry models are deployed as Standard (pay-per-token), Provisioned (reserved throughput) or Batch (discounted, asynchronous), plus a Developer type for fine-tuned model evaluation. Standard and Provisioned are each processed globally, within a data zone or within one geography, and Batch globally or within a data zone. Global Standard is the default starting point. The choice affects latency guarantees, where data is processed and how costs are predicted.
- doc | Understanding deployment types in Microsoft Foundry Models | https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

# advanced-rag | Advanced RAG
Reference, not a read-through. Come here when retrieval quality is the thing standing between you and a usable answer.

## vector | Embeddings & Vector Search
Vector search finds content by meaning instead of keywords. You embed chunks, store the vectors in an index, and embed each query to find its nearest neighbours. The index holds vector and ordinary fields side by side, content arrives by indexer or push, and a filter on a metadata field is how a condition such as released revisions only is enforced.
- doc | Vector search overview (Azure AI Search) | https://learn.microsoft.com/en-us/azure/search/vector-search-overview

## chunking | Chunking Strategies
Chunk size and boundaries decide what gets retrieved. Too small loses meaning; too large dilutes relevance and wastes tokens. The page matches approaches to how much structure a document has, from prebuilt models to fixed-size splitting, gives no chunk sizes, and says to experiment and treat the choice as semipermanent.
- doc | Develop a RAG Solution on Azure — Chunking Phase | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase

## hybrid | Hybrid Search & Semantic Ranking
Hybrid search runs keyword (BM25) and vector search together and merges the results. A semantic ranker then re-scores the top results. Benchmark tests the page cites show relevance gains from hybrid retrieval with the ranker. The ranker re-scores only the top 50 results, and only a bounded slice of each.
- doc | Hybrid search overview | https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview
- doc | Semantic ranking overview | https://learn.microsoft.com/en-us/azure/search/semantic-search-overview
- video | Copilot Studio: Azure AI Search Complete Setup Guide (Matthew Devaney) | https://www.youtube.com/watch?v=aDUVpI14hvg

## agentic | Agentic Retrieval & Foundry IQ
Agentic retrieval can use a model to plan queries (a preview feature; the generally available path skips planning): it breaks a question into sub-queries, searches several sources and combines the results. Foundry IQ packages this as reusable knowledge bases that Foundry agents and Copilot Studio can use.
- doc | Agentic retrieval overview (Azure AI Search) | https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview
- doc | What is Foundry IQ? | https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq
- video | Build knowledge-enhanced AI agents with Foundry IQ (AI-103) | https://www.youtube.com/watch?v=c9zns7PX0Io

## cortexsearch | Snowflake Cortex Search
Cortex Search is Snowflake's managed hybrid (vector plus keyword) search over text in Snowflake. It handles embeddings and index refresh itself, and it's a strong RAG source for data that already lives in Snowflake. It searches with its owner's rights, so the source query is the access boundary.
- doc | Cortex Search | https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview

## cortexanalyst | Cortex Analyst & Semantic Views
Cortex Analyst answers natural-language questions by generating SQL over a semantic view: business definitions of tables, metrics and relationships, which the page says improve accuracy over a bare schema. It answers only what SQL can, runs as the requesting role, and Snowflake now recommends Cortex Agents, which supports every Analyst capability.
- doc | Cortex Analyst | https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst
- doc | Overview of semantic views | https://docs.snowflake.com/en/user-guide/views-semantic/overview

## routing | Structured vs. Unstructured Retrieval
A question may need SQL over a semantic layer, document search, or one record found by its key, and a wrong route fails with a plausible answer. A Cortex Agent plans, picks a tool per subtask and reflects, and carries on with whatever tools the caller's role can reach. Copilot Studio says it filters knowledge sources with a model above 25. Neither page measures how well it routes.
- doc | Cortex Agents | https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents
- doc | Knowledge sources summary (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio

## grounded | Groundedness & Citations
Grounded can mean that a source was used, that each claim agrees with it, or that the claim is true, and each needs its own check. Groundedness detection compares an answer with its sources, offers correction in preview, is optimised for English and retires on 30 April 2027. Foundry's Groundedness evaluator is a model judge, and Groundedness Pro (preview) is a service verdict. Neither page covers instructing a model to cite and refuse.
- doc | Groundedness detection in Azure AI Content Safety | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/groundedness
- doc | Retrieval-Augmented Generation (RAG) Evaluators for Generative AI (Microsoft Foundry) | https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/rag-evaluators

## rageval | RAG Evaluation
Evaluate retrieval (did we fetch the right chunks?) separately from generation (did the answer use them correctly?). Document Retrieval scores ranking against human relevance labels, and the Retrieval judge needs none. The answer is scored on groundedness, relevance and completeness, and the architecture page adds utilization and correctness and reads the metrics in pairs. Aim for a range, since answers vary.
- doc | Develop a RAG Solution on Azure — Large Language Model End-to-End Evaluation Phase | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-llm-evaluation-phase
- doc | Retrieval-Augmented Generation (RAG) Evaluators for Generative AI (Microsoft Foundry) | https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/rag-evaluators

# snowflake-cortex | Snowflake: Advanced SQL & Cortex AI
Reference, not a read-through. Come here when an agent needs governed data served fast, or AI run where the data already is.

## qualify | Advanced Window Functions & QUALIFY
QUALIFY filters on window function results, after aggregates and before DISTINCT, ORDER BY and LIMIT. Beyond keeping the latest row per key, it can audit what a deduplicating view hides. ROWS and RANGE frames behave differently where values tie, which matters for running totals and moving averages.
- doc | QUALIFY | https://docs.snowflake.com/en/sql-reference/constructs/qualify
- doc | Analyzing data with window functions | https://docs.snowflake.com/en/user-guide/functions-window-using

## semistructured | Semi-Structured Data
Snowflake stores JSON and other semi-structured data, which has no fixed schema and nests, in VARIANT columns. FLATTEN expands an array or object into one row per element, and drops any row whose path is missing unless OUTER is set. Technik's bench readings arrive in this shape.
- doc | Introduction to loading semi-structured data | https://docs.snowflake.com/en/user-guide/semistructured-intro
- doc | FLATTEN | https://docs.snowflake.com/en/sql-reference/functions/flatten

## performance | Query Performance
Agents run the same queries again and again, so what a call costs adds up. Use Query History and the Query Profile to find the expensive step, check pruning, and watch repeated statements as a group. Warehouse credits follow size and run time, with a 60-second minimum each time a warehouse resumes, so match size and auto-suspend to the workload.
- doc | Monitor query activity with Query History | https://docs.snowflake.com/en/user-guide/ui-snowsight-activity
- doc | Warehouse considerations | https://docs.snowflake.com/en/user-guide/warehouses-considerations

## sfgov | Secure Views & Policies for Agents
Give agents dedicated roles, and put each rule where Snowflake enforces it. A secure view hides its definition and blocks inference through a user's own predicates, at some cost in speed, so reserve it for views that exist for privacy. Row access policies filter rows by role and masking policies change what a column shows, both on Enterprise Edition. They decide from the session's role, not from the prompt.
- doc | Working with Secure Views | https://docs.snowflake.com/en/user-guide/views-secure
- doc | Understanding row access policies | https://docs.snowflake.com/en/user-guide/security-row-intro
- doc | Understanding Dynamic Data Masking | https://docs.snowflake.com/en/user-guide/security-column-ddm-intro

## aisql | Cortex AI SQL Functions
Cortex AI functions such as AI_COMPLETE, AI_CLASSIFY, AI_EXTRACT, AI_FILTER and AI_AGG run LLM tasks directly in SQL across whole tables. They are ideal for batch enrichment, classification and summarisation without moving data out of Snowflake.
- doc | Snowflake Cortex AI Functions | https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql

## cortexagents | Cortex Agents
Cortex Agents is Snowflake's managed agent runtime. It plans, calls Cortex Analyst, Cortex Search and custom tools, and responds, all inside Snowflake governance. You can expose Cortex Agents to Microsoft agents through MCP.
- doc | Cortex Agents | https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents

## sfintegrate | Integrating Snowflake with Microsoft Agents
There are three routes:
- **Knowledge source:** no-code, natural-language queries over selected tables.
- **Snowflake connector:** exact, parameterised queries in flows and tools.
- **Snowflake-managed MCP:** Cortex Analyst, Search and Agents as tools.

Choose by how much control, governance and reasoning you need.
- doc | Add Power Platform connectors (incl. Snowflake) as knowledge | https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-real-time-connectors
- doc | Snowflake (Connectors reference) | https://learn.microsoft.com/en-us/connectors/snowflakev2/
- doc | Snowflake-managed MCP server | https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp

## sfcost | Cost Control
AI workloads use warehouse credits and Cortex AI credits. Use resource monitors, dedicated warehouses for agents, query tags and usage views to track and cap spend.
- doc | Working with resource monitors | https://docs.snowflake.com/en/user-guide/resource-monitors
- doc | Snowflake Cortex AI Functions — cost considerations | https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql

# automation-advanced | Intelligent Automation (Advanced)
Reference, not a read-through. Come here when part of what you are shipping has to run the same way every time, reliably.

## detvsagentic | Deterministic vs. Agentic Automation
Workflows follow fixed paths and are predictable, cheap and auditable. Agents decide dynamically and are flexible but vary between runs. Use AI only at the steps that need judgement, such as classifying, extracting or drafting, and keep the rest deterministic.
- article | Building Effective AI Agents — workflows vs. agents (Anthropic Engineering) | https://www.anthropic.com/engineering/building-effective-agents
- article | Automate business processes with agents plus workflows in Microsoft Copilot Studio | https://www.microsoft.com/en-us/copilot/blog/copilot-studio/automate-business-processes-with-agents-plus-workflows-in-microsoft-copilot-studio/

## wfagentnodes | Workflows with Agent Nodes & AI Actions
Copilot Studio workflows combine triggers, actions, approvals and conditions with agent nodes and AI actions that reason at chosen steps. Step-level testing lets you check each node with sample inputs.
- doc | Workflows overview (GitHub Copilot) — Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/workflows-experience/flows-overview
- article | How to build multi-agent workflows in Copilot Studio (Matthew Devaney) | https://www.matthewdevaney.com/how-to-build-multi-agent-workflows-in-copilot-studio/

## flowtools | Flows as Agent Tools
A flow used as a tool needs a clean contract: named, typed inputs and outputs, a precise description, and error responses that tell the agent what went wrong. Keep flows short enough to finish within the agent's time limits.
- doc | Use agent flows with your agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-flow
- doc | Add an agent flow as a tool to an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/flow-agent

## promptsadv | AI Builder Prompts (Advanced)
For production prompts: use JSON output with a defined structure, ground prompts in Dataverse knowledge where relevant, choose the model and temperature per prompt, and set content moderation sensitivity per prompt for document-processing or regulated scenarios.
- doc | Prompts overview | https://learn.microsoft.com/en-us/microsoft-copilot-studio/prompts-overview
- doc | Change the model version and settings (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/prompt-model-settings

## docpipelines | Document Processing Pipelines
Production document pipelines follow the same sequence: classify the document, extract fields with a prebuilt or custom model, validate against business rules, send low-confidence results to people for review, and only then write to systems of record.
- doc | Create a document processing custom model | https://learn.microsoft.com/en-us/ai-builder/create-form-processing-model
- article | How to extract tables from a PDF in Power Automate (Matthew Devaney) | https://www.matthewdevaney.com/how-to-extract-tables-from-a-pdf-in-power-automate/

## errors | Error Handling & Resilience
Wrap work in Try/Catch/Finally scopes, configure run-after and retry policies, make actions idempotent (safe to repeat), and send failures somewhere people watch. AI steps fail in new ways, such as content filters, timeouts and malformed JSON, so handle those explicitly.
- doc | Employ robust error handling (Power Automate guidance) | https://learn.microsoft.com/en-us/power-automate/guidance/coding-guidelines/error-handling
- article | 3 Power Automate error-handling patterns you must know (Matthew Devaney) | https://www.matthewdevaney.com/3-power-automate-error-handling-patterns-you-must-know/

## longrunning | Long-Running Processes & Approvals
Approvals and multi-day processes run into flow duration limits. Design them with persisted state (for example in Dataverse), reminders, escalations and timeouts, and restart safely instead of waiting forever.
- doc | Limits of automated, scheduled and instant flows | https://learn.microsoft.com/en-us/power-automate/limits-and-config
- article | Extend a Power Automate approval over the 30-day limit (Matthew Devaney) | https://www.matthewdevaney.com/extend-a-power-automate-approval-over-the-30-day-limit/

# models-and-fine-tuning | Models: Inference, Training & Fine-Tuning
Reference, not a read-through. Come here when you are asked to customise a model, or to run one in production yourself.

## lifecycle | The Training Lifecycle
Models go through pre-training on huge general datasets, supervised fine-tuning on instruction examples, and preference or reinforcement tuning to align behaviour. Knowing these stages explains model strengths and weaknesses, and what your own fine-tuning can and can't change.
- doc | Fine-tune models with Microsoft Foundry (classic) — concepts | https://learn.microsoft.com/en-us/azure/foundry-classic/concepts/fine-tuning-overview
- video | Fine Tuning (Microsoft Learn) | https://www.youtube.com/watch?v=ai9Jpw3NkFw

## decide | Prompting vs. RAG vs. Fine-Tuning
Try prompting first, then RAG for knowledge, then fine-tuning for behaviour, style, format or efficiency. Fine-tuning doesn't reliably teach facts that change; RAG does. Always compare options against the same evaluation set.
- doc | Getting started with customizing a large language model (LLM) (classic) | https://learn.microsoft.com/en-us/azure/foundry-classic/openai/concepts/customizing-llms
- video | Compare model optimization strategies (AI-3016) | https://www.youtube.com/watch?v=SkGItraTlHc

## finetune | Fine-Tuning in Microsoft Foundry
Foundry supports supervised fine-tuning (SFT), direct preference optimisation (DPO) and reinforcement fine-tuning (RFT) for supported models, using serverless or managed compute. Each has different data needs, costs and suitable use cases.
- doc | Fine-tune a model with supervised fine-tuning in Microsoft Foundry | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/fine-tuning
- doc | Fine-tune a model with direct preference optimization in Microsoft Foundry | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/fine-tuning-direct-preference-optimization
- doc | Fine-tune a model with reinforcement fine-tuning in Microsoft Foundry | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reinforcement-fine-tuning

## dataprep | Training Data Preparation
Training data uses the chat JSONL format. Quality beats quantity: examples must be consistent, correct and representative, with a held-out validation set. Remove personal data you don't need, and document where every example came from.
- doc | Fine-tune a model with supervised fine-tuning in Microsoft Foundry — prepare your data | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/fine-tuning

## distill | Distillation | opt
Distillation trains a smaller, cheaper model on outputs from a larger one for a narrow task. It's often the best way to cut latency and cost once a large model already does the job well.
- doc | Fine-tune models with Microsoft Foundry (classic) — concepts | https://learn.microsoft.com/en-us/azure/foundry-classic/concepts/fine-tuning-overview

## copilottuning | Microsoft Copilot Tuning | opt, prev
Copilot Tuning, in early access preview, lets organisations tune models on their own content for specific tasks and use them in Microsoft 365 Copilot agents. Evaluate it for domain-heavy document work.
- doc | Microsoft Copilot Tuning Overview (early access preview) | https://learn.microsoft.com/en-us/microsoft-365/copilot/copilot-tuning-overview
- video | Customized AI for your business with Copilot Tuning (Microsoft Ignite 2025) | https://www.youtube.com/watch?v=1KvH2oHhTuk

## serving | Deploying & Serving Models
Deploying a model means choosing a deployment type and region, setting quotas and rate limits, and building retries and fallbacks into clients. Put an AI gateway (such as Azure API Management) in front when many apps share the same models.
- doc | Understanding deployment types in Microsoft Foundry Models | https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types
- doc | AI gateway capabilities in Azure API Management | https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities

## modellifecycle | Model Lifecycle
Model versions get retired, and upgrades change behaviour. Track retirement dates, pin versions where you can, and run your evaluation suite before switching production agents to a new model.
- doc | Foundry Models lifecycle and support policy | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirements
