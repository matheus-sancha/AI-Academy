---
id: advanced
order: 2
title: AI Engineering on Microsoft
subtitle: Advanced Roadmap
tagline: For developers who completed the Beginner roadmap — context engineering, harnesses, skills, MCP, pro-code agents, RAG, evaluation and ALM.
next: index.html
next_label: Back to the program home
audience: Developers
card: LLM internals, context engineering, agent harnesses, authoring skills, building MCP servers, pro-code agents (Agents Toolkit, Agent Framework, Foundry), advanced RAG, Snowflake Cortex, fine-tuning, evaluation, security and ALM.
---

# A0 | Prerequisites & Developer Tooling
Set up the pro-code toolchain. Fundamentals are not repeated here; they are in the Beginner roadmap.

## prereq | Prerequisite: Beginner Roadmap
This roadmap assumes you finished the Beginner roadmap. That means you can explain tokens, context and temperature, write XML-structured prompts, build and publish a Copilot Studio agent with knowledge, tools, flows and skills, query Snowflake, and run a basic evaluation.
- doc | Study guide AB-620: Designing and Building Integrated AI Solutions in Copilot Studio | https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ab-620
- doc | Study guide AB-100: Agentic AI Business Solutions Architect | https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ab-100

## vscode | VS Code for AI Engineering | opt
VS Code is where pro-code AI work happens. You'll use it to author MCP servers, skills, agent YAML, SQL and evaluation scripts. Set up GitHub Copilot, the Copilot Studio extension, the Python or C# tooling, and optionally dev containers for reproducible environments.
- doc | Set up GitHub Copilot in VS Code | https://code.visualstudio.com/docs/setup/copilot
- doc | Build with agents in VS Code | https://code.visualstudio.com/docs/agents/overview

## agentmode | GitHub Copilot Agent Mode
In agent mode, Copilot plans multi-step changes, edits several files, runs terminal commands and calls tools, including MCP servers. It asks for approval before sensitive actions. Treat it as a junior engineer: give it clear context, review its diffs and keep tests in the loop.
- doc | Use chat and agents in VS Code | https://code.visualstudio.com/docs/chat/chat-overview
- doc | Tools in agent mode (approvals, tool sets) | https://code.visualstudio.com/docs/agents/run/tools
- video | Building applications with GitHub Copilot agent mode (Microsoft Learn) | https://www.youtube.com/watch?v=XnC6cF1v5OY

## csvscode | Copilot Studio VS Code Extension
The Copilot Studio extension lets you clone an agent into VS Code as YAML, edit topics, instructions and components with Copilot's help, and sync the changes back. It brings agents into Git-based workflows and code review.
- doc | Copilot Studio extension for VS Code overview | https://learn.microsoft.com/en-us/microsoft-copilot-studio/visual-studio-code-extension-overview

## git | Git & GitHub for Agents
Version control is not optional once AI writes code and agents are defined as files. You need branching, pull requests, reviewing AI-generated changes and protecting secrets. It is also the basis for Dataverse Git integration and CI/CD later in this roadmap.
- course | Introduction to Git (Microsoft Learn) | https://learn.microsoft.com/en-us/training/modules/intro-to-git/
- video | Configure and use secret scanning in your GitHub repository (GH-500) | https://www.youtube.com/watch?v=mQB7FKqMq0Y

## language | Python or C# Baseline
You need enough Python or C# to call model APIs, write an MCP server, script evaluations and use Microsoft Agent Framework. Pick one language for the team and stick with it.
- doc | Agent Framework — Step 1: your first agent (Python / .NET) | https://learn.microsoft.com/en-us/agent-framework/get-started/your-first-agent
- doc | C# documentation | https://learn.microsoft.com/en-us/dotnet/csharp/

# A1 | LLM Internals for Engineers
Go beyond the concepts: the mechanics that drive quality, latency and cost in production.

## transformers | Transformers & Attention (Intuition)
LLMs are transformer networks. Attention lets each token weigh every other token in the context. That explains why models can use long context, why cost grows with length, and why information buried in the middle of a long prompt can be underused.
- course | Introduction to generative AI and agents (Microsoft Learn training) | https://learn.microsoft.com/en-us/training/modules/fundamentals-generative-ai/
- doc | LLM fundamentals (Agent Framework learning journey) | https://learn.microsoft.com/en-us/agent-framework/journey/llm-fundamentals

## tokenbudget | Tokenization in Practice
Count tokens before you ship. Know your model's tokenizer, input and output prices, and limits. Build token budgets for instructions, tools, knowledge and history, and watch for hidden token costs such as tool schemas, retrieved chunks and reasoning tokens.
- doc | Understanding tokens (.NET) | https://learn.microsoft.com/en-us/dotnet/ai/conceptual/understanding-tokens
- doc | Azure OpenAI quotas and limits | https://learn.microsoft.com/en-us/azure/foundry/openai/quotas-limits
- video | Why your AI costs spike (tokens explained) | https://www.youtube.com/watch?v=NmkR7V_wTqA

## params | Inference Parameters
Beyond temperature and top_p, engineers set maximum output tokens, stop sequences, seed (for best-effort reproducibility), tool choice, response format and reasoning effort. Parameters differ across model families: reasoning models reject some sampling settings.
- doc | Use the Responses API (Microsoft Foundry) | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses
- doc | Reasoning models — supported parameters | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning

## reasoning | Reasoning Models
Reasoning models spend extra hidden "thinking" tokens before answering. They are much better at multi-step logic, planning and coding, but slower and more expensive. Use reasoning effort settings, and route simple requests to faster models.
- doc | Azure OpenAI reasoning models | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning
- video | Optimize generative AI model performance with Microsoft Foundry (AI-103) | https://www.youtube.com/watch?v=Ocx76q4p9ME

## embeddings | Embeddings
An embedding is a vector that captures the meaning of text, so similar meanings sit close together. Embeddings power vector search, RAG, clustering, deduplication and semantic caching. Pick your embedding model once per index; changing it means re-embedding everything.
- doc | How embeddings extend your AI model's reach (.NET) | https://learn.microsoft.com/en-us/dotnet/ai/conceptual/embeddings
- doc | Vector search overview (Azure AI Search) | https://learn.microsoft.com/en-us/azure/search/vector-search-overview

## functioncalling | Function / Tool Calling
With function calling, the model returns a structured request to call a tool: a name plus JSON arguments. Your code or the harness runs the tool and sends the result back. MCP, Copilot Studio tools and Agent Framework tools all rest on this mechanism.
- doc | Function calling with Microsoft Foundry Models | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/function-calling
- video | Develop generative AI apps that use tools (AI-103) | https://www.youtube.com/watch?v=N5DcQ-ZNp_M

## structured | Structured Outputs
Structured outputs force a response to match a JSON schema, so downstream code, flows and databases can rely on its shape. Prefer schema-constrained output over "please answer in JSON" whenever the platform supports it.
- doc | Structured outputs with Azure OpenAI | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs
- doc | Prompts overview — JSON output in Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/prompts-overview

## latency | Latency, Throughput & Cost
Production AI trades off time to first token, total latency, throughput and cost. Levers include model choice, output length, streaming, caching, parallel tool calls, batching and model routing.
- doc | Performance and latency (Azure OpenAI) | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/latency
- doc | Provisioned throughput for Foundry Models | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/provisioned-throughput

## deploytypes | Foundry Deployment Types | opt
Microsoft Foundry models can be deployed as Standard or Global (pay-per-token, shared capacity), Data Zone (for data residency) or Provisioned (reserved throughput). The choice affects latency guarantees, where data is processed and how costs are predicted.
- doc | Understanding deployment types in Microsoft Foundry Models | https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

# A2 | Context Engineering
Design everything that enters the context window — not just the prompt.

## fromprompt | From Prompt Engineering to Context Engineering
Context engineering means curating the smallest, highest-signal set of tokens for each model call: instructions, tools, retrieved knowledge, memory and history. In agents, context builds up over many turns, so managing it becomes an engineering discipline.
- article | Effective context engineering for AI agents (Anthropic Engineering) | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- doc | Set up a context engineering flow in VS Code | https://code.visualstudio.com/docs/agents/guides/context-engineering-guide

## budget | The Context Window as a Budget
Treat the window as a limited budget shared by system instructions, tool definitions, knowledge chunks, conversation history, tool results and the output. Measure what each part costs, and cut what doesn't improve evaluation scores.
- article | Effective context engineering for AI agents (Anthropic Engineering) | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- doc | Understanding tokens (.NET) | https://learn.microsoft.com/en-us/dotnet/ai/conceptual/understanding-tokens

## xmltemplates | XML-Structured Context & Templates
Standardise how context is assembled with consistent XML sections such as `<role>`, `<rules>`, `<tools_guidance>`, `<knowledge>`, `<user_data>` and `<output_format>`, filled from templates and variables. Consistent structure makes behaviour easier to reproduce, test and review.
- doc | Prompt engineering techniques — delimiters and structure | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering
- doc | RAG prompt engineering | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-prompt-engineering

## sysprompt | System Prompt Design at Scale
Large agents need layered instructions: global policy, then agent role, then task or skill instructions, then per-request data. Include explicit priorities for when rules conflict. Keep them versioned, reviewed and covered by evaluations, like code.
- doc | System message design | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/advanced-prompt-engineering
- video | Manage prompts for agents in Microsoft Foundry with GitHub (AI-300) | https://www.youtube.com/watch?v=10lrxyurK78

## toolshaping | Tool & Result Shaping
Every tool definition uses context, and so does every tool result. Write short, distinct tool descriptions, expose only the tools a task needs, and trim or summarise large tool outputs before they go back into the context.
- article | Effective context engineering for AI agents — tools | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- doc | Tools in agent mode (VS Code) | https://code.visualstudio.com/docs/agents/run/tools

## jit | Retrieval vs. Stuffing
Preloading every document you might need wastes context and confuses the model. Just-in-time retrieval, where the agent searches or opens files when it needs them, keeps context lean. Hybrid approaches preload a small core and retrieve the rest on demand.
- doc | Agentic retrieval overview (Azure AI Search) | https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview
- article | Effective context engineering for AI agents — just-in-time context | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

## history | Conversation History & Compaction
Long conversations degrade quality and raise cost. Use compaction (summarising older turns), truncation, and structured notes that live outside the context. Research shows models use information at the start and end of long contexts better than information in the middle.
- article | Lost in the Middle: How Language Models Use Long Contexts (arXiv) | https://arxiv.org/abs/2307.03172
- doc | Agent harness (Microsoft Agent Framework) | https://learn.microsoft.com/en-us/agent-framework/concepts/harness

## memory | Memory | prev
Short-term memory is the current conversation. Long-term memory keeps facts or preferences across sessions. Copilot Studio agents on the GitHub Copilot harness can turn memory on. Decide what may be remembered, for how long, and how users can see or remove it.
- doc | Memory (preview) — Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/memory-overview
- doc | Work IQ overview | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/

## caching | Prompt Caching | opt
Prompt caching reuses the processed form of a stable prompt prefix, such as long instructions or tool definitions, across calls. That cuts latency and cost. Design prompts so the stable parts come first and the variable parts come last.
- doc | Prompt caching with Azure OpenAI | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching

## ctxsecurity | Context as a Security Boundary
Anything you put in context can steer the model, including emails, web pages and documents written by attackers (indirect prompt injection). Mark untrusted data clearly ("spotlighting"), never let it act as instructions, and pair this with Prompt Shields and least-privilege tools.
- article | How Microsoft defends against indirect prompt injection attacks (MSRC) | https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks
- doc | Prompt Shields | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection

# A3 | Agent Harness
The runtime around the model: loop, tools, permissions and recovery.

## loop | The Agent Loop
Every agent runs a loop: read the goal and context, decide on an action, call a tool, look at the result, and repeat until done or stopped. Define stop conditions, step limits and failure handling explicitly; otherwise loops wander and cost money.
- article | Building effective agents (Anthropic Engineering) | https://www.anthropic.com/engineering/building-effective-agents
- doc | Agent harness concepts (Microsoft Agent Framework) | https://learn.microsoft.com/en-us/agent-framework/concepts/harness

## planning | Planning & Recovery
Capable harnesses break goals into steps, notice failures, retry and try other paths. You improve this with clear goals, good tool error messages and checkpoints, and by keeping deterministic workflows for steps that must never change.
- doc | Harnesses in Copilot Studio — GitHub Copilot harness | https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview
- doc | AI agent orchestration patterns (Azure Architecture Center) | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns

## sandbox | Sandboxing, Permissions & Approvals
Decide what an agent may do without asking: read-only tools, a sandboxed file system, approval for writes, sends and payments. GitHub Copilot asks before running terminal commands; Copilot Studio's GitHub Copilot harness runs tasks in a governed sandbox.
- doc | Security considerations for agents in VS Code | https://code.visualstudio.com/docs/agents/run/security
- doc | Tools in agent mode — tool approval | https://code.visualstudio.com/docs/agents/run/tools

## csharnesses | Copilot Studio Harnesses Compared
The three harnesses compared:
- **GitHub Copilot harness:** reasoning, files, skills, memory; billed in Copilot Credits.
- **Standard harness:** topics and agent flows, predictable behaviour.
- **Copilot chat harness:** extends M365 Copilot Chat with knowledge.

Architects need to know what each supports, where it can be published and how it's billed.
- doc | Harnesses in Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview
- doc | Usage-based billing for GitHub Copilot harness agents | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/billing-credit-overview
- video | How To Orchestrate Chat Without Topics In New Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=aZdKeVdiNys

## ghharness | GitHub Copilot as a Harness
GitHub Copilot is one harness running on several surfaces: agent mode in VS Code, Copilot CLI in the terminal, and the cloud agent that works on issues and opens pull requests. Each surface has different autonomy, tools and review points.
- doc | About GitHub Copilot CLI | https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-copilot-cli
- doc | About GitHub Copilot cloud agent | https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent
- video | Delegate issues to GitHub Copilot (Microsoft Learn) | https://www.youtube.com/watch?v=b66COmGO6vw

## customize | Customizing the Harness
You shape a harness through files it loads: `copilot-instructions.md` or `AGENTS.md` for repository context, prompt files for reusable tasks, custom agents for personas with their own tool sets, and skills for on-demand know-how.
- doc | Custom instructions in VS Code | https://code.visualstudio.com/docs/agent-customization/custom-instructions
- doc | Prompt files in VS Code | https://code.visualstudio.com/docs/agent-customization/prompt-files
- doc | Custom agents in VS Code | https://code.visualstudio.com/docs/agent-customization/custom-agents
- article | AGENTS.md — open format for agent instructions | https://agents.md/

## harnessvssdk | Harness vs. SDK vs. Platform
Use a managed harness (Copilot Studio, GitHub Copilot) when it fits. Build your own loop with an SDK such as Microsoft Agent Framework when you need custom orchestration, hosting or integration. Use a platform service such as Foundry Agent Service for managed runtime, identity and observability.
- article | Microsoft Agent Framework at BUILD 2026: Agent Harness, Hosted Agents, CodeAct | https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026-announce/
- doc | Choose the right tool to build a declarative agent | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-tool-comparison

# A4 | Agent Skills (Authoring)
Package expert know-how once and reuse it across VS Code, GitHub Copilot and Copilot Studio.

## format | The Agent Skills Format
A skill is a folder with a `SKILL.md` file. Its YAML front matter holds a `name` and a `description`, and its Markdown body holds the instructions. Optional scripts, templates and reference files can sit alongside. The open format works across GitHub Copilot, Copilot Studio and other harnesses.
- doc | Agent Skills specification | https://agentskills.io/specification
- doc | Use Agent Skills in VS Code | https://code.visualstudio.com/docs/agent-customization/agent-skills

## disclosure | Progressive Disclosure
Only the skill's name and description are always in context. The body loads when the skill activates, and bundled files load only when the instructions refer to them. That's why you can install many skills without filling the context window.
- article | Equipping agents for the real world with Agent Skills (Anthropic Engineering) | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- doc | Skills overview — how the orchestrator invokes skills (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-overview

## descriptions | Writing Descriptions That Trigger
The description decides whether a skill runs at all. Say what the skill does and when to use it, using the words users actually type, and set clear boundaries so it doesn't fire on unrelated requests.
- doc | Create a skill for an agent (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-create
- doc | Agent Skills specification — description field | https://agentskills.io/specification

## bundling | Bundling Scripts & Reference Data
Put deterministic work in scripts inside the skill, such as validating SQL, formatting reports or calling an API. Put detailed reference material, such as schemas or style guides, in separate files. The model follows the instructions; scripts do the precise parts.
- doc | Adding agent skills for GitHub Copilot | https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- article | anthropics/skills — example skills repository | https://github.com/anthropics/skills

## skillsvscode | Skills in VS Code / GitHub Copilot
Project skills live in the repository (for example `.github/skills/<name>/SKILL.md`) and are shared with everyone who clones it. Personal skills live in your user profile. Copilot loads the matching skill automatically in agent mode.
- doc | Use Agent Skills in VS Code | https://code.visualstudio.com/docs/agent-customization/agent-skills
- doc | Adding agent skills for GitHub Copilot | https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills

## skillscs | Skills in Copilot Studio
Agents on the GitHub Copilot harness accept skills that you upload as a `SKILL.md` or a bundle, or write in the portal. Package the skills your team has proven in VS Code and reuse them across Copilot Studio agents.
- doc | Add an existing skill to an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-add-existing
- video | How To Create Agent Skills In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=BvDGMw_7sbk

## skilltest | Testing & Versioning Skills
Test skills in two ways. Trigger tests check that the skill activates on the right prompts and not on others. Output tests check the results with evaluations. Keep skills in Git with change history and a review step, like any other code.
- doc | Create a test set (Copilot Studio evaluation) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-create

## skillgov | Sharing & Governing Skills | opt
A team skill library needs owners, a review process, security checks (bundled scripts run code) and a catalogue. Community collections are a good source of ideas, but review any third-party skill before you use it.
- article | github/awesome-copilot — community instructions, agents and skills | https://github.com/github/awesome-copilot

# A5 | Model Context Protocol (MCP)
Build and secure the standard interface between agents and your systems.

## mcparch | MCP Architecture
MCP defines hosts (the AI application), clients (a connection held inside the host) and servers (which expose capabilities). Servers offer tools (actions), resources (data) and prompts (templates) over JSON-RPC.
- doc | MCP architecture overview | https://modelcontextprotocol.io/docs/learn/architecture
- article | MCP for Beginners (Microsoft open-source curriculum) | https://github.com/microsoft/mcp-for-beginners

## transports | Transports
Local servers usually use stdio: a process on your machine that the client starts. Remote servers use Streamable HTTP. Remote servers need authentication, network controls and monitoring; local ones inherit your machine's permissions.
- doc | MCP transports specification | https://modelcontextprotocol.io/specification/latest/basic/transports

## mcpvscode | Using MCP Servers in VS Code
Configure MCP servers in `mcp.json` for a workspace or for your user profile. Check that you trust each server, pick which tools are enabled, and use them from agent mode. It's the fastest way to prototype and test a server before giving it to Copilot Studio.
- doc | Add and manage MCP servers in VS Code | https://code.visualstudio.com/docs/agent-customization/mcp-servers

## buildmcp | Building an MCP Server
Use an official SDK (Python, TypeScript or C#) to expose a few well-described tools with typed inputs. Keep tools small and specific, return concise results, and handle errors with messages the model can act on.
- doc | Build an MCP server (official tutorial) | https://modelcontextprotocol.io/docs/develop/build-server
- video | Copilot Studio: Create An MCP Server With Python (Matthew Devaney) | https://www.youtube.com/watch?v=kKJ391VKYJo
- article | Create an MCP server and deploy to Copilot Studio (Matthew Devaney) | https://www.matthewdevaney.com/create-an-mcp-server-and-deploy-to-copilot-studio/

## mcpauth | Authentication for MCP
Remote MCP servers should use OAuth, ideally through Microsoft Entra ID, so every tool call runs with a real identity and can be audited. Avoid shared API keys for tools that touch user data.
- doc | MCP authorization specification | https://modelcontextprotocol.io/specification/latest/basic/authorization

## mcpcs | Connecting MCP Servers to Copilot Studio
Copilot Studio can connect to existing or custom MCP servers. Tools and their changes sync automatically, and they can be used by agents and by workflows. Data policies (DLP) and connector governance still apply.
- doc | Connect your agent to an existing MCP server | https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent
- doc | Extend your agent with Model Context Protocol | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp

## sfmcp | Snowflake-Managed MCP Server
Snowflake hosts MCP servers that expose Cortex Analyst, Cortex Search, Cortex Agents, custom tools and SQL execution. Snowflake OAuth and role-based access control govern which tools are visible. It gives Microsoft agents governed access to Snowflake data.
- doc | Snowflake-managed MCP server | https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp

## mcpsec | MCP Security
MCP-specific risks include:
- tool poisoning (malicious tool descriptions)
- indirect prompt injection through tool results
- over-broad tools
- confused-deputy authorization
- untrusted local servers

Mitigate with least privilege, allow-lists, reviewing servers before use and DLP.
- doc | MCP security best practices | https://modelcontextprotocol.io/specification/latest/basic/security_best_practices
- article | Protecting against indirect prompt injection attacks in MCP (Microsoft for Developers) | https://developer.microsoft.com/blog/protecting-against-indirect-injection-attacks-mcp/

## mcpcert | MCP Certification | opt
Microsoft runs a certification program for MCP servers that checks reliability, security and compliance. Prefer certified servers where you can, and apply the same review criteria to servers built in-house.
- doc | What's new in Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/whats-new

# A6 | Advanced Tools, Connectors & Multi-Agent
Integrate anything, share connections safely and coordinate multiple agents.

## customconn | Custom Connectors
When no prebuilt connector exists, wrap a REST API as a custom connector from an OpenAPI definition. Add authentication, policies and clear operation descriptions. The same connector then works in Power Automate, Power Apps and Copilot Studio.
- doc | Custom connectors overview | https://learn.microsoft.com/en-us/connectors/custom-connectors/
- article | Make your first custom connector for Power Automate and Power Apps (Matthew Devaney) | https://www.matthewdevaney.com/make-your-first-custom-connector-for-power-automate-and-power-apps/

## restapi | REST API Tools
Copilot Studio can add tools straight from a REST API definition without building a full connector. That's useful for quick integrations. Name and describe the operations carefully so the orchestrator picks them correctly.
- doc | Extend your agent with tools from a REST API (preview) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-rest-api

## connrefs | Connection References & Service Principals
Connection references separate a solution from the credentials it uses, so each environment can bind its own connection. For shared agents, decide between end-user authentication and a service principal. Store secrets in environment variables backed by Azure Key Vault.
- doc | Use a connection reference in a solution | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-connection-reference
- article | How to set up a Power Platform environment variable secret (Matthew Devaney) | https://www.matthewdevaney.com/how-to-setup-a-power-platform-environment-variable-secret/

## cuaadv | Computer Use (Advanced) | opt
In production, computer use needs secure credential storage, a choice of model, runs that tolerate UI changes and monitoring. Windows 365 for Agents gives agents managed Cloud PCs for desktop automation.
- doc | Automate web and desktop apps with computer use | https://learn.microsoft.com/en-us/microsoft-copilot-studio/computer-use
- doc | Windows 365 for Agents documentation | https://learn.microsoft.com/en-us/windows-365/agents/

## multiagent | Multi-Agent Patterns
Common patterns:
- **Sequential:** a pipeline.
- **Concurrent:** fan out, then merge the results.
- **Handoff:** pass control to a specialist.
- **Group chat:** agents collaborate.
- **Orchestrator–worker:** a lead agent delegates to others.

Start with a single agent; add more only when evaluations show you need them.
- doc | AI agent orchestration patterns (Azure Architecture Center) | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- video | Multi-Agent Workflows In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=gIlSJHRRoj0
- video | Orchestrate a multi-agent solution using Microsoft Agent Framework (AI-103) | https://www.youtube.com/watch?v=l3oAcAWySlE

## a2a | Agent-to-Agent (A2A)
A2A is an open protocol that lets agents on different platforms find each other, exchange tasks and share results. Copilot Studio supports agent-to-agent communication, so agents built in Copilot Studio, Foundry or elsewhere can work together.
- doc | A2A Protocol | https://a2a-protocol.org/latest/
- doc | Add other agents (connected agents) — Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-add-other-agents

## agentid | Agent Identity
Microsoft Entra Agent ID gives agents their own identities, so they can be governed, given permissions and audited like users and apps. Copilot Studio agents get an identity automatically. Design permissions for the agent itself, not only for the maker.
- doc | Microsoft Entra Agent ID documentation | https://learn.microsoft.com/en-us/entra/agent-id/

# A7 | Pro-Code Agents
Build agents in code when low-code limits you.

## lowvspro | Low-Code vs. Pro-Code Decision
Choose by requirements:
- **Agent Builder:** simple personal agents.
- **Copilot Studio:** business agents, fast delivery, Power Platform integration.
- **Declarative agents with the Agents Toolkit:** version-controlled M365 Copilot extensions.
- **Agent Framework or Foundry:** custom orchestration, custom hosting or complex integrations.
- doc | Choose the right tool to build a declarative agent | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-tool-comparison
- video | Choose a Microsoft 365 Copilot extensibility development path (MS-4010) | https://www.youtube.com/watch?v=ARPj2XpkCpU

## declarative | Declarative Agents with M365 Agents Toolkit
Declarative agents customise Microsoft 365 Copilot through a manifest: instructions, knowledge, capabilities and actions. They run on Copilot's own orchestrator. The Agents Toolkit in VS Code gives you source control, local testing and deployment.
- doc | Create declarative agents using Microsoft 365 Agents Toolkit | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/build-declarative-agents
- video | Build a declarative agent for Microsoft 365 Copilot using VS Code (MS-4010 Ep. 5) | https://www.youtube.com/watch?v=2VPAPMOfeZc

## plugins | API Plugins & TypeSpec | opt
API plugins give declarative agents actions from OpenAPI-described APIs. TypeSpec lets you define the agent and its API in one concise, typed source that generates the manifests.
- doc | Plugins for Microsoft 365 Copilot | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/overview-plugins
- doc | Create declarative agents with TypeSpec | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/build-declarative-agents-typespec
- video | Build your first action for declarative agents with API plugin (MS-4010 Ep. 6) | https://www.youtube.com/watch?v=692C_5Z6Wtg

## customengine | Custom Engine Agents & M365 Agents SDK
Custom engine agents bring your own orchestration and models into Teams and Microsoft 365 Copilot. The Microsoft 365 Agents SDK handles channels, activities and authentication, and you choose the AI stack behind it.
- doc | Custom engine agents for Microsoft 365 | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/overview-custom-engine-agent
- doc | Microsoft 365 Agents SDK documentation | https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/

## maf | Microsoft Agent Framework
Microsoft Agent Framework is the successor to Semantic Kernel and AutoGen. It is an SDK for Python and .NET for building agents with tools, MCP, context providers, middleware and telemetry, and it works with Azure OpenAI, Foundry, Anthropic and other providers.
- doc | Microsoft Agent Framework overview | https://learn.microsoft.com/en-us/agent-framework/overview/
- doc | Step 1: your first agent | https://learn.microsoft.com/en-us/agent-framework/get-started/your-first-agent
- video | Develop an AI agent with the Microsoft Agent Framework (AI-103) | https://www.youtube.com/watch?v=WznrISPGx-g

## mafworkflows | Agent Framework Workflows
Workflows in Agent Framework are graph-based: executors and edges connect agents and functions into sequential, concurrent, handoff or group-chat orchestrations. They support streaming, checkpoints and human-in-the-loop steps.
- doc | Agent Framework workflow capabilities | https://learn.microsoft.com/en-us/agent-framework/workflows/
- video | Orchestrate a multi-agent solution using Microsoft Agent Framework (AI-103) | https://www.youtube.com/watch?v=l3oAcAWySlE

## foundryagents | Foundry Agent Service & Hosted Agents
Foundry Agent Service runs agents with managed threads, tools, knowledge (Foundry IQ), identity and observability. Hosted agents let you deploy code-based agents, for example ones built with Agent Framework, onto that managed runtime.
- doc | What is Microsoft Foundry Agent Service? | https://learn.microsoft.com/en-us/azure/foundry/agents/overview
- doc | Hosted agents in Foundry Agent Service | https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents
- video | Develop AI agents with Microsoft Foundry and Visual Studio Code (AI-103) | https://www.youtube.com/watch?v=EmBPT_tIs8Y

## byom | Bring a Foundry Model into Copilot Studio | opt
You can use models deployed in Microsoft Foundry inside Copilot Studio prompts and agents, for example a fine-tuned or specialised model, while keeping Copilot Studio's orchestration and channels.
- video | Master Copilot Studio Prompts with Azure AI Foundry Models (Matthew Devaney) | https://www.youtube.com/watch?v=ShphK8L3y2Y
- article | Azure AI Foundry model in Copilot Studio custom prompts (Matthew Devaney) | https://www.matthewdevaney.com/azure-ai-foundry-model-in-copilot-studio-custom-prompts/

# A8 | Advanced RAG
Engineer retrieval quality for unstructured and structured data.

## vector | Embeddings & Vector Search
Vector search finds content by meaning instead of keywords. You embed chunks, store the vectors in an index, and embed each query to find its nearest neighbours. The index design, embedding model and filters decide what the agent can find.
- doc | Vector search overview (Azure AI Search) | https://learn.microsoft.com/en-us/azure/search/vector-search-overview

## chunking | Chunking Strategies
Chunk size and boundaries decide what gets retrieved. Too small loses meaning; too large dilutes relevance and wastes tokens. Chunking that follows the document's structure (headings, tables, pages) with some overlap usually works best.
- doc | RAG solution design — chunking phase | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase

## hybrid | Hybrid Search & Semantic Ranking
Hybrid search runs keyword (BM25) and vector search together and merges the results. A semantic ranker then re-scores the top results. This combination beats vector-only search for most enterprise content.
- doc | Hybrid search overview | https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview
- doc | Semantic ranking overview | https://learn.microsoft.com/en-us/azure/search/semantic-search-overview
- video | Copilot Studio: Azure AI Search Complete Setup Guide (Matthew Devaney) | https://www.youtube.com/watch?v=aDUVpI14hvg

## agentic | Agentic Retrieval & Foundry IQ
Agentic retrieval uses a model to plan queries: it breaks a question into sub-queries, searches several sources and combines the results. Foundry IQ packages this as reusable knowledge bases that Foundry agents and Copilot Studio can use.
- doc | Agentic retrieval overview | https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview
- doc | What is Foundry IQ? | https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq
- video | Build knowledge-enhanced AI agents with Foundry IQ (AI-103) | https://www.youtube.com/watch?v=c9zns7PX0Io

## cortexsearch | Snowflake Cortex Search
Cortex Search is Snowflake's managed hybrid (vector plus keyword) search over text in Snowflake. It handles embeddings and index refresh inside Snowflake governance, and it's a strong RAG source for data that already lives in Snowflake.
- doc | Cortex Search | https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview

## cortexanalyst | Cortex Analyst & Semantic Views
Cortex Analyst answers natural-language questions by generating SQL over a semantic model: business definitions of tables, metrics and relationships. Semantic views store that model in Snowflake, which makes text-to-SQL far more accurate than querying raw tables.
- doc | Cortex Analyst | https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst
- doc | Overview of semantic views | https://docs.snowflake.com/en/user-guide/views-semantic/overview

## routing | Structured vs. Unstructured Retrieval
"What was Q3 revenue by region?" needs SQL over a semantic layer. "What does the travel policy say?" needs document search. Good agents route each question to the right retrieval type, or combine both.
- doc | Cortex Agents — orchestrating Analyst and Search | https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents
- doc | Knowledge sources summary (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio

## grounded | Groundedness & Citations
Enforce grounding: instruct the agent to answer only from retrieved sources, require citations, and refuse when the sources are insufficient. Measure groundedness automatically, and flag or block ungrounded answers.
- doc | Groundedness detection (Azure AI Content Safety) | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/groundedness
- doc | RAG evaluators (Microsoft Foundry) | https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/rag-evaluators

## rageval | RAG Evaluation
Evaluate retrieval (did we fetch the right chunks?) separately from generation (did the answer use them correctly?). Track retrieval relevance, groundedness, answer relevance and completeness against a labelled question set.
- doc | RAG solution design — LLM end-to-end evaluation phase | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-llm-evaluation-phase
- doc | RAG evaluators (Microsoft Foundry) | https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/rag-evaluators

# A9 | Snowflake: Advanced SQL & Cortex AI
Serve governed, performant data to agents and run AI inside Snowflake.

## qualify | Advanced Window Functions & QUALIFY
QUALIFY filters on window function results without subqueries. It is ideal for deduplication ("latest row per key"), ranking and time-series logic that agents and pipelines rely on.
- doc | QUALIFY | https://docs.snowflake.com/en/sql-reference/constructs/qualify
- doc | Analyzing data with window functions | https://docs.snowflake.com/en/user-guide/functions-window-using

## semistructured | Semi-Structured Data
Snowflake stores JSON and other semi-structured data in VARIANT columns. Query it with path notation and expand arrays with FLATTEN. Tool results, API payloads and AI outputs often arrive in this shape.
- doc | Introduction to semi-structured data | https://docs.snowflake.com/en/user-guide/semistructured-intro
- doc | FLATTEN | https://docs.snowflake.com/en/sql-reference/functions/flatten

## performance | Query Performance
Agents may run queries many times a day, so slow SQL becomes a cost problem. Use query history and profiles to find expensive steps, prune data with filters and clustering, and size warehouses for AI workloads.
- doc | Monitor query activity with Query History | https://docs.snowflake.com/en/user-guide/ui-snowsight-activity
- doc | Warehouse considerations | https://docs.snowflake.com/en/user-guide/warehouses-considerations

## sfgov | Secure Views & Policies for Agents
Give agents dedicated roles and expose data only through secure views. Enforce row access policies and dynamic data masking, so a prompt injection or an over-broad query can't leak data the role shouldn't see.
- doc | Working with secure views | https://docs.snowflake.com/en/user-guide/views-secure
- doc | Understanding row access policies | https://docs.snowflake.com/en/user-guide/security-row-intro
- doc | Understanding dynamic data masking | https://docs.snowflake.com/en/user-guide/security-column-ddm-intro

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
- doc | Snowflake connector reference | https://learn.microsoft.com/en-us/connectors/snowflakev2/
- doc | Snowflake-managed MCP server | https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp

## sfcost | Cost Control
AI workloads use warehouse credits and Cortex AI credits. Use resource monitors, dedicated warehouses for agents, query tags and usage views to track and cap spend.
- doc | Working with resource monitors | https://docs.snowflake.com/en/user-guide/resource-monitors
- doc | Cortex AI Functions — cost considerations | https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql

# A10 | Intelligent Automation (Advanced)
Combine deterministic automation with AI reasoning, reliably.

## detvsagentic | Deterministic vs. Agentic Automation
Workflows follow fixed paths and are predictable, cheap and auditable. Agents decide dynamically and are flexible but vary between runs. Use AI only at the steps that need judgement, such as classifying, extracting or drafting, and keep the rest deterministic.
- article | Building effective agents — workflows vs. agents (Anthropic Engineering) | https://www.anthropic.com/engineering/building-effective-agents
- article | Automate business processes with agents plus workflows in Copilot Studio (Microsoft) | https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/automate-business-processes-with-agents-plus-workflows-in-microsoft-copilot-studio/

## wfagentnodes | Workflows with Agent Nodes & AI Actions
Copilot Studio workflows combine triggers, actions, approvals and conditions with agent nodes and AI actions that reason at chosen steps. Step-level testing lets you check each node with sample inputs.
- doc | Workflows overview (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/workflows-experience/flows-overview
- article | How to build multi-agent workflows in Copilot Studio (Matthew Devaney) | https://www.matthewdevaney.com/how-to-build-multi-agent-workflows-in-copilot-studio/

## flowtools | Flows as Agent Tools
A flow used as a tool needs a clean contract: named, typed inputs and outputs, a precise description, and error responses that tell the agent what went wrong. Keep flows short enough to finish within the agent's time limits.
- doc | Use agent flows with your agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-flow
- doc | Add an agent flow as a tool to an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/flow-agent

## promptsadv | AI Builder Prompts (Advanced)
For production prompts: use JSON output with a defined structure, ground prompts in Dataverse knowledge where relevant, choose the model and temperature per prompt, and set content moderation sensitivity per prompt for document-processing or regulated scenarios.
- doc | Prompts overview | https://learn.microsoft.com/en-us/microsoft-copilot-studio/prompts-overview
- doc | Change the model version and settings | https://learn.microsoft.com/en-us/microsoft-copilot-studio/prompt-model-settings

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

# A11 | Models: Inference, Training & Fine-Tuning
Know when and how to customise models, and how to run them in production.

## lifecycle | The Training Lifecycle
Models go through pre-training on huge general datasets, supervised fine-tuning on instruction examples, and preference or reinforcement tuning to align behaviour. Knowing these stages explains model strengths and weaknesses, and what your own fine-tuning can and can't change.
- doc | Fine-tune models with Microsoft Foundry — concepts | https://learn.microsoft.com/en-us/azure/foundry-classic/concepts/fine-tuning-overview
- video | Fine Tuning (Microsoft Learn) | https://www.youtube.com/watch?v=ai9Jpw3NkFw

## decide | Prompting vs. RAG vs. Fine-Tuning
Try prompting first, then RAG for knowledge, then fine-tuning for behaviour, style, format or efficiency. Fine-tuning doesn't reliably teach facts that change; RAG does. Always compare options against the same evaluation set.
- doc | Getting started with customizing an LLM | https://learn.microsoft.com/en-us/azure/foundry-classic/openai/concepts/customizing-llms
- video | Compare model optimization strategies (AI-3016) | https://www.youtube.com/watch?v=SkGItraTlHc

## finetune | Fine-Tuning in Microsoft Foundry
Foundry supports supervised fine-tuning (SFT), direct preference optimisation (DPO) and reinforcement fine-tuning (RFT) for supported models, using serverless or managed compute. Each has different data needs, costs and suitable use cases.
- doc | Customize a model with fine-tuning | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/fine-tuning
- doc | Direct preference optimization | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/fine-tuning-direct-preference-optimization
- doc | Reinforcement fine-tuning | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reinforcement-fine-tuning

## dataprep | Training Data Preparation
Training data uses the chat JSONL format. Quality beats quantity: examples must be consistent, correct and representative, with a held-out validation set. Remove personal data you don't need, and document where every example came from.
- doc | Customize a model with fine-tuning — prepare your data | https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/fine-tuning

## distill | Distillation | opt
Distillation trains a smaller, cheaper model on outputs from a larger one for a narrow task. It's often the best way to cut latency and cost once a large model already does the job well.
- doc | Fine-tune models with Microsoft Foundry — concepts | https://learn.microsoft.com/en-us/azure/foundry-classic/concepts/fine-tuning-overview

## copilottuning | Microsoft Copilot Tuning | opt, prev
Copilot Tuning, in early access preview, lets organisations tune models on their own content for specific tasks and use them in Microsoft 365 Copilot agents. Evaluate it for domain-heavy document work.
- doc | Microsoft Copilot Tuning overview | https://learn.microsoft.com/en-us/microsoft-365/copilot/copilot-tuning-overview
- video | Customized AI for your business with Copilot Tuning (Microsoft Ignite 2025) | https://www.youtube.com/watch?v=1KvH2oHhTuk

## serving | Deploying & Serving Models
Deploying a model means choosing a deployment type and region, setting quotas and rate limits, and building retries and fallbacks into clients. Put an AI gateway (such as Azure API Management) in front when many apps share the same models.
- doc | Understanding deployment types | https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types
- doc | AI gateway capabilities in Azure API Management | https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities

## modellifecycle | Model Lifecycle
Model versions get retired, and upgrades change behaviour. Track retirement dates, pin versions where you can, and run your evaluation suite before switching production agents to a new model.
- doc | Foundry Models lifecycle and support policy | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirements

# A12 | Evaluation & Observability
Measure quality continuously and see what agents actually do.

## evalstrategy | Evaluation Strategy
Combine offline evaluations (test sets before release) with online monitoring (production signals). Evaluate the system (was the task completed?) and the process (did each step, tool call and retrieval behave?). Define metrics before you build.
- doc | Evaluate your AI agents (Microsoft Foundry) | https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/evaluate-agent
- doc | Agent evaluation checklist | https://learn.microsoft.com/en-us/agents/agent-evaluation/evaluation-checklist
- video | Evaluate and optimize AI agents through structured experiments (AI-300) | https://www.youtube.com/watch?v=8zO5hApUxYo

## evalharness | Building an Eval Harness
An eval harness has four parts: versioned datasets, a runner that calls the agent, graders (code checks and LLM judges) and a report that compares against a baseline. Run it in CI on every change to prompts, skills, tools or models, and block releases that regress.
- doc | Run an evaluation in GitHub Actions (Microsoft Foundry) | https://learn.microsoft.com/en-us/azure/foundry/how-to/evaluation-github-action
- video | Automate AI evaluations with Microsoft Foundry and GitHub Actions (AI-300) | https://www.youtube.com/watch?v=vMleA0GZgSQ

## csevaladv | Copilot Studio Agent Evaluation (Advanced)
Go beyond single test sets: grade whole sets, define custom metrics, generate test cases from analytics, and automate evaluation runs through APIs, connectors or the Copilot Agent Kit.
- doc | Choose evaluation methods | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-overview
- doc | Configure tests in Copilot Agent Kit | https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/kit-configure-tests
- video | Copilot Studio Test Automation: STOP Testing Manually!! (Matthew Devaney) | https://www.youtube.com/watch?v=qh4YRqZgaQU

## foundryevals | Foundry Evaluators
Foundry provides built-in evaluators for:
- quality: groundedness, relevance, coherence
- agent behaviour: intent resolution, task adherence, tool call accuracy
- safety

Custom evaluators cover domain-specific rules.
- doc | Agent evaluators | https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/agent-evaluators
- doc | Built-in evaluators reference | https://learn.microsoft.com/en-us/azure/foundry/concepts/built-in-evaluators

## mafeval | Agent Framework Evaluation
Agent Framework includes evaluation support. You can run fast local checks while developing, call Foundry cloud evaluators for production-grade grading, or combine both in one run.
- doc | Evaluation (Microsoft Agent Framework) | https://learn.microsoft.com/en-us/agent-framework/agents/evaluation

## judge | LLM-as-Judge
LLM judges scale grading of open-ended answers, but they have biases: preferring their own style, favouring longer answers, and position bias. Use clear rubrics, calibrate against human labels, and keep deterministic checks wherever possible.
- doc | Observability in generative AI — evaluators | https://learn.microsoft.com/en-us/azure/foundry/concepts/observability
- doc | Built-in evaluators reference | https://learn.microsoft.com/en-us/azure/foundry/concepts/built-in-evaluators

## tracing | Tracing & Telemetry
Traces record every model call, tool call, token count and latency in a run, which you need to debug agents. Foundry supports OpenTelemetry tracing; Copilot Studio can send agent telemetry to Application Insights.
- doc | Set up tracing for AI agents in Microsoft Foundry | https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/trace-agent-setup
- doc | Agent-level telemetry with Application Insights (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-bot-framework-composer-capture-telemetry
- video | Implement observability and monitoring for generative AI workloads (AI-300) | https://www.youtube.com/watch?v=igglwJgwzkI

## prodfeedback | Production Analytics & Feedback
Production signals include resolution rates, escalations, user reactions, tool errors, cost per conversation and transcripts. Feed them back into your test sets, so every failure found in production becomes a regression test.
- doc | Monitor overview (Copilot Studio analytics) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-overview
- video | Monitor, analyze, and tune AI agents (AB-100) | https://www.youtube.com/watch?v=JR6C87ZEtws

# A13 | Security, Safety & Moderation (Advanced)
Threat-model agents and apply layered defences.

## threats | Threat Model for Agents
Key risks include prompt injection (direct and indirect), sensitive data disclosure, excessive agency (tools that can do too much), insecure output handling, supply-chain risks in models, MCP servers and skills, and unbounded consumption.
- doc | OWASP Top 10 for LLM Applications | https://genai.owasp.org/llm-top-10/
- video | Design responsible AI security, governance, risk management, and compliance (AB-100) | https://www.youtube.com/watch?v=yG_Rq-VNJaU

## contentsafety | Azure AI Content Safety
Content Safety provides harm classifiers, Prompt Shields (jailbreak and indirect injection detection), groundedness detection and protected material detection. Use it in pro-code apps, and understand the equivalent filtering built into Copilot Studio.
- doc | What is Azure AI Content Safety? | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview
- doc | Prompt Shields | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection
- video | Implement a responsible generative AI solution in Microsoft Foundry (AI-103) | https://www.youtube.com/watch?v=H5wPr-Ca2UM

## modtuning | Moderation Tuning
Tune moderation for the scenario. Regulated or document-processing work may need per-prompt sensitivity settings so legitimate content (medical, legal, security) isn't blocked. Record why you chose each setting, and cover these cases in evaluations.
- doc | FAQ for generative answers — content moderation levels | https://learn.microsoft.com/en-us/microsoft-copilot-studio/faqs-generative-answers
- doc | Resolve responsible AI content filter errors | https://learn.microsoft.com/en-us/troubleshoot/power-platform/copilot-studio/generative-answers/agent-response-filtered-by-responsible-ai

## purview | Data Protection with Microsoft Purview
Purview extends sensitivity labels, data loss prevention, auditing and data security posture management to Copilot and agent interactions. Agents should respect labels, and their interactions should be auditable.
- doc | Microsoft Purview protections for Microsoft 365 Copilot and other AI apps | https://learn.microsoft.com/en-us/purview/ai-microsoft-purview
- video | Discover, protect, govern, and detect AI interactions with Microsoft Purview (SC-401) | https://www.youtube.com/watch?v=lVukA34ug4k

## dlpdesign | DLP for Connectors & MCP
Design Power Platform data policies that let agents work safely. Group connectors into business, non-business and blocked. Control HTTP and custom connectors, MCP servers, knowledge sources and channels, and apply stricter policies to production environments.
- doc | Data policies (Power Platform) | https://learn.microsoft.com/en-us/power-platform/admin/wp-data-loss-prevention
- doc | Configure data policies for agents (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention

## redteam | AI Red Teaming | opt
Red teaming probes agents with adversarial prompts, such as jailbreaks, injections and harmful requests, before attackers do. Foundry's AI Red Teaming Agent and the open-source PyRIT tool automate scans and produce risk reports.
- doc | Run AI Red Teaming Agent (Microsoft Foundry) | https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/run-scans-ai-red-teaming-agent
- article | PyRIT — Python Risk Identification Tool (Azure, open source) | https://github.com/Azure/PyRIT

# A14 | ALM, Governance & Operations
Ship agents like software: repeatable, reviewed, monitored and cost-controlled.

## solutionsdeep | Solutions Deep Dive
Real solutions include environment variables (per-environment settings and Key Vault secrets), connection references, managed solutions in test and production, and layering. Getting this right is what makes pipelines work.
- doc | Use environment variables in Power Platform solutions | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/environmentvariables
- doc | Establish an ALM strategy for Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/alm

## pipelines | Power Platform Pipelines
Pipelines deploy solutions from development to test to production with approvals, pre-deployment validation and history, all from inside the maker experience. They are the default ALM path for Copilot Studio teams.
- doc | Overview of pipelines in Power Platform | https://learn.microsoft.com/en-us/power-platform/alm/pipelines
- article | Create a Power Platform pipeline (Matthew Devaney) | https://www.matthewdevaney.com/the-complete-power-platform-pipelines-alm-setup-guide/create-a-power-platform-pipeline/

## gitintegration | Dataverse Git Integration
Dataverse Git integration connects a development environment to Azure DevOps or GitHub. You commit agent and solution changes as source files, review them in pull requests and pull changes into other environments.
- doc | Overview of Dataverse Git integration | https://learn.microsoft.com/en-us/power-platform/alm/git-integration/overview
- article | Set up Dataverse Git integration for a solution (Matthew Devaney) | https://www.matthewdevaney.com/the-complete-power-platform-pipelines-alm-setup-guide/setup-dataverse-git-integration-for-a-solution/

## cicd | CI/CD with GitHub Actions / Azure DevOps
For enterprise automation, use GitHub Actions for Power Platform or Power Platform Build Tools for Azure DevOps. They export, unpack, check, deploy and run evaluations as gates, alongside pro-code agents and MCP servers.
- doc | GitHub Actions for Microsoft Power Platform | https://learn.microsoft.com/en-us/power-platform/alm/devops-github-actions
- doc | Automate deployments with Dataverse Git integration and pipelines (reference architecture) | https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/enterprise-power-platform-alm
- video | Design ALM process for AI-powered business solutions (AB-100) | https://www.youtube.com/watch?v=bcKJaKNRT1c

## managedenvs | Managed Environments
Managed Environments add governance at environment level: sharing limits, solution checker enforcement, usage insights, maker welcome content and pipeline hosting. Turn them on for test and production.
- doc | Managed environments overview | https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-overview
- article | Create Power Platform environments for Dev-Test-Prod (Matthew Devaney) | https://www.matthewdevaney.com/the-complete-power-platform-pipelines-alm-setup-guide/create-power-platform-environments-for-dev-test-prod/

## agent365 | Agent 365 & Admin Controls
Microsoft Agent 365 is a central control plane: an inventory of agents across platforms with unified policies, security and lifecycle management. Engineers should build agents that meet these controls from the start.
- doc | Microsoft Agent 365 documentation | https://learn.microsoft.com/en-us/microsoft-agent-365/
- doc | Security and governance in Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance

## agentkit | Copilot Agent Kit | opt
The Copilot Agent Kit, formerly the Copilot Studio Kit, adds tooling for Copilot Studio teams: automated testing, conversation KPIs, compliance checks and governance dashboards.
- doc | Copilot Agent Kit overview | https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/kit-overview
- article | Configure MS auth for test automation in Copilot Studio Kit (Matthew Devaney) | https://www.matthewdevaney.com/configure-ms-auth-for-test-automation-in-copilot-studio-kit/

## costs | Cost Management
Track the whole bill: Copilot Credits for building, testing and running agents; AI Builder credits; Foundry model tokens and provisioned throughput; Snowflake credits. Set budgets and alerts, and report cost per agent and per conversation.
- doc | Manage Copilot Credits and capacity | https://learn.microsoft.com/en-us/power-platform/admin/manage-copilot-studio-copilot-credits-capacity
- doc | Licensing and AI Builder credits | https://learn.microsoft.com/en-us/ai-builder/credit-management
- doc | Provisioned throughput for Foundry Models | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/provisioned-throughput
