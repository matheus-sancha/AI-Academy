# Does Advanced's roadmap still match the products it teaches?

> Research for [AI-Academy #88](https://github.com/matheus-sancha/AI-Academy/issues/88), on
> [Write every Advanced lesson](https://github.com/matheus-sancha/AI-Academy/issues/87). Audited 2026-10-18 against
> `_source/advanced.md` as of `afcc034`. Link statuses come from `python _build/check_links.py advanced.md`. Product
> facts are cited to the page that owns them. The `ms.date` of a Learn page is given where it dates the claim.

## Answer in brief

**Yes, with corrections. No topic needs cutting.** All 121 topics still name live products. All 203 unique links
resolve (0 broken, 0 blocked). Five changes since the roadmap was written in 2026-09 affect what lessons say, and the
roadmap has been corrected for each of them:

1. **MCP is now stateless.** Revision **2026-07-28** removed the `initialize` handshake, protocol sessions, the
   `Mcp-Session-Id` header and SSE resumability. It deprecated Roots, Sampling, Logging and Dynamic Client
   Registration ([changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)). The Python and C#
   SDKs shipped **v2.0.0 on release day**, and Python v1.x is security-fixes-only
   ([Python v2.0.0](https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.0.0),
   [C# v2.0.0](https://github.com/modelcontextprotocol/csharp-sdk/releases/tag/v2.0.0)). **This is the main input to
   [the capstone stack ticket](https://github.com/matheus-sancha/AI-Academy/issues/89).** Pin SDK v2, and expect
   tutorials from before 2026-07 to show v1 APIs.
2. **Work IQ Dev Tools (preview)** is now Microsoft's recommended pro-code starting point for declarative agents. The
   page lists it ahead of Microsoft 365 Agents Toolkit, which is now the route for "lower-level manifest, package, or
   command control" ([Choose development tools for your plugin](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/choose-plugin-development-tools),
   2026-09-30; [Compare tools for declarative agents](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-tool-comparison),
   2026-09-30). The roadmap now mentions it in `lowvspro`. **Whether `declarative` should teach it instead of Agents
   Toolkit is the maintainer's call** (see [Raised for the maintainer](#raised-for-the-maintainer)).
3. **Copilot Studio has three harnesses**: GitHub Copilot, **standard**, and Copilot chat
   ([Harnesses in Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview),
   2026-09-21). Several features are now scoped to one harness, and Learn page titles carry the qualifier. Memory,
   skills and workflows say "(GitHub Copilot)". Application Insights telemetry is for agents "powered by the standard
   harness" ([Agent-level telemetry with Application Insights](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-bot-framework-composer-capture-telemetry),
   2026-07-28). The `tracing` blurb said this without the scope.
4. **Foundry Agent Service changed its vocabulary.** It is now prompt agents, voice-based prompt agents and hosted
   agents, on an Agent Runtime that "manages conversations" (not threads), with shared **Toolboxes** and an Agent
   optimizer in preview ([What is Microsoft Foundry Agent Service?](https://learn.microsoft.com/en-us/azure/foundry/agents/overview),
   2026-09-25).
5. **Foundry's deployment types were reorganised** into standard, provisioned and batch categories. Each can be
   global, data zone or regional, and there is a Developer type for evaluating fine-tuned models. Global Standard is
   the recommended start ([Understanding deployment types](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types),
   2026-08-06).

Separately, **26 link labels** no longer match their target's title prefix, which is the rule in
[`course-design.md`](../course-design.md). Two GitHub URLs redirected to different pages. All of these are fixed.

## Status changes the blurbs now carry

| Topic | Finding | Source |
|---|---|---|
| `agentid` | Since July 2026, Copilot Studio **automatically creates an Entra Agent ID for every new agent**, with no environment-level opt-out. | [What's new in Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/whats-new) (2026-10-05) |
| `agent365` | Agent 365 has been **generally available** (Commercial, per user) since 2026-05-01. | [Microsoft Agent 365 overview](https://learn.microsoft.com/en-us/microsoft-agent-365/overview) (2026-08-19) |
| `mcpcert` | MCP server certification submission is **preview**. | [What's new in Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/whats-new) |
| `redteam` | The AI Red Teaming Agent page is now "Run AI Red Teaming Agent **locally (preview)**", through the Azure AI Evaluation SDK. | [the page](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/run-scans-ai-red-teaming-agent) (2026-04-10) |
| `plugins` | The plugins page is now "**MCP and API plugins** for declarative agents". Remote MCP servers are a plugin type alongside OpenAPI. | [the page](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/overview-plugins) (2026-09-30) |
| `maf` | Agent Framework now has a **Go** SDK in public preview, alongside Python and .NET. Its "direct successor" to Semantic Kernel and AutoGen line still holds. | [Agent Framework overview](https://learn.microsoft.com/en-us/agent-framework/overview/) (2026-07-29) |
| `csvscode` | The Copilot Studio extension for VS Code is **generally available**. | [What's new in Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/whats-new) |
| `a2a` | Copilot Studio connects to external agents over the **A2A protocol**. Foundry, Fabric data and Agents SDK agents are still preview. | [Add other agents overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-add-other-agents) (2026-05-15) |
| `agentkit` | The kit's README is titled **Copilot Agent Kit**. Its repository is still `Power-CAT-Copilot-Studio-Kit`, which bears out "formerly the Copilot Studio Kit". | [microsoft/Power-CAT-Copilot-Studio-Kit](https://github.com/microsoft/Power-CAT-Copilot-Studio-Kit) |
| `agentic` | Some Foundry IQ features are GA and others remain preview, depending on the Search REST API version. The portals give preview-only access. | [What is Foundry IQ?](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq) (2026-07-31) |
| `foundryevals` | Intent Resolution and Task Adherence are **preview**. Tool Call Accuracy is not marked preview. New composite evaluators (Tool Use Quality, a batched quality judge) exist. | [Agent evaluators](https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/agent-evaluators) (2026-09-30) |

Verified unchanged, with no edit needed:

- **MCP architecture.** It is still host, client and server ([Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)).
- **Transports.** stdio and Streamable HTTP are the standard transports. HTTP+SSE is formally Deprecated ([transports](https://modelcontextprotocol.io/specification/latest/basic/transports), [changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)).
- **Snowflake-managed MCP server.** It serves Cortex Analyst, Cortex Search, Cortex Agents, custom tools and SQL execution ([Snowflake-managed MCP server](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp)).
- **Cortex AI functions.** `AI_COMPLETE`, `AI_CLASSIFY`, `AI_EXTRACT`, `AI_FILTER` and `AI_AGG` all exist. Some functions are preview, so a lesson checks each function it names ([Cortex AI Functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql)).
- **Hosted agents.** They still take any framework, Agent Framework included ([Hosted agents](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents), 2026-09-11).
- **The GitHub Copilot cloud agent** is still named that ([Concepts for GitHub Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent)).
- **AI Builder credits** still exist alongside Copilot Credits ([Licensing and AI Builder credits](https://learn.microsoft.com/en-us/ai-builder/credit-management), 2026-10-08).
- **Copilot Tuning** is still early access preview ([overview](https://learn.microsoft.com/en-us/microsoft-365/copilot/copilot-tuning-overview)).

## The capstone's stages

Every stage still names a live product: scaffold (Agent Framework), MCP server (MCP SDK), agent (Agent Framework,
function calling), evals (Foundry evaluation GitHub Action, agent evaluators) and ship (hosted agents, Entra Agent ID,
Foundry tracing). The links all resolve, and the pages are dated from 2026-07 to 2026-09. The one stage
whose ground moved is **Stage 2**. A server written against SDK v2 serves 2026-07-28 and earlier revisions from the
same code ([Python v2.0.0](https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.0.0)). The C# SDK
defaults its HTTP transport to stateless
([C# v2.0.0](https://github.com/modelcontextprotocol/csharp-sdk/releases/tag/v2.0.0)).
**Unverified:** whether Copilot Studio's MCP client and VS Code already negotiate 2026-07-28. That is for the
capstone build to observe.

## Link labels fixed

Each label head now matches the target's title prefix. Labels that differed only by a site suffix ("— Microsoft
Learn", "\ Anthropic", "· GitHub") were left alone.

| Topic | Was | Now |
|---|---|---|
| `ghharness` | About GitHub Copilot CLI (URL redirected) | GitHub Copilot CLI, at its new URL |
| `ghharness` | About GitHub Copilot cloud agent (redirected to *GitHub Copilot on GitHub.com*) | Concepts for GitHub Copilot cloud agent |
| `customize`, `stagescaffold` | Custom instructions in VS Code / Prompt files in VS Code | Use custom instructions in VS Code / Use prompt files in VS Code |
| `harnessvssdk`, `lowvspro` | Choose the right tool to build a declarative agent | Compare tools for declarative agents |
| `declarative` | Create declarative agents using Microsoft 365 Agents Toolkit | Create declarative agents by using Microsoft 365 Agents Toolkit and JSON |
| `plugins` | Plugins for Microsoft 365 Copilot; …using… TypeSpec | MCP and API plugins for declarative agents; …by using… TypeSpec |
| `memory`, `disclosure`, `descriptions`, `wfagentnodes` | Copilot Studio titles without the harness | the titles' "(GitHub Copilot)" qualifier added |
| `mcparch`, `transports`, `mcpsec` | MCP architecture overview / MCP transports specification / MCP security best practices | Architecture overview / Overview — Transports / Security Best Practices. The security page moved from the spec into the docs' tutorials, and the URL now goes there. |
| `redteam` | Run AI Red Teaming Agent | Run AI Red Teaming Agent locally (preview) |
| `functioncalling`, `stageagent`, `structured` | Function calling… / Structured outputs… | How to use function calling… / How to use structured outputs… |
| `grounded`, `rageval` | RAG evaluators | Retrieval-Augmented Generation (RAG) Evaluators for Generative AI |
| `finetune`, `dataprep` | Customize a model with fine-tuning / Direct preference optimization / Reinforcement fine-tuning | Fine-tune a model with supervised fine-tuning / direct preference optimization / reinforcement fine-tuning in Microsoft Foundry |
| `lifecycle`, `distill` | Fine-tune models with Microsoft Foundry — concepts | Fine-tune models with Microsoft Foundry (classic) — concepts |
| `copilottuning` | Microsoft Copilot Tuning overview | Microsoft Copilot Tuning Overview (early access preview) |
| `connrefs`, `gitintegration` | Devaney titles re-cased | his titles as published ("How To Setup…", "Setup Dataverse Git Integration For A Solution") |
| `detvsagentic` | blog URL under `/microsoft-copilot/blog/` | the `/copilot/blog/` URL it redirects to |

## Notes for the writing tickets

These don't change the roadmap, but a lesson would get them wrong without them.

- **`lifecycle`, `decide` and `distill` are sourced from "(classic)" portal pages.** The current fine-tuning page
  doesn't mention distillation, serverless or managed compute. It talks about *training types* ("Global training uses
  `GlobalStandard`") instead
  ([SFT in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/fine-tuning), 2026-10-05).
  The classic overview is dated 2025-12-03
  ([Fine-tune models (classic)](https://learn.microsoft.com/en-us/azure/foundry-classic/concepts/fine-tuning-overview)).
  `finetune`'s "serverless or managed compute" rests on the classic page, so it is **unverified for the current
  portal**. Searches for a current-portal concepts page found none, and both guessed URLs return 404.
- **The Foundry RBAC roles were renamed**: Azure AI User → Foundry User, and so on. The role IDs are unchanged (same
  SFT page). This affects any setup step in the capstone.
- **OWASP's 2025 list is still the latest.** Its URL is now an archive page titled "LLMRisks Archive", which leads
  with the 2025 list ([genai.owasp.org/llm-top-10](https://genai.owasp.org/llm-top-10/)). The label was kept because it
  names the list the page leads with.
- **The Matthew Devaney MCP video and article in `buildmcp` predate SDK v2.** Teach the technique from them, but take
  the code from the capstone.
- **Agent Skills specification.** The label "Agent Skills specification" doesn't prefix-match the page title
  "Specification - Agent Skills". It is kept as Intermediate's own label for the same link, for consistency.

## Raised for the maintainer

The ticket reserves these calls for the maintainer.

1. **`declarative`: Agents Toolkit or Work IQ Dev Tools?** Microsoft now recommends Work IQ Dev Tools (preview) as the
   starting point, and keeps Agents Toolkit for lower-level control. Agents Toolkit is GA and still documented for
   declarative agents, MCP plugins and TypeSpec. Work IQ Dev Tools is preview, and "individual capabilities can require
   feature flags"
   ([Choose development tools for your plugin](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/choose-plugin-development-tools)).
   **Decided (2026-10-18): "Agents Toolkit, mention WIQD".** The lesson teaches Agents Toolkit and names Work IQ Dev
   Tools as Microsoft's newer preview starting point. The topic stays as it is, and `lowvspro` already lists both.
2. **No cut or merge is proposed.** Every topic still names a live product.
