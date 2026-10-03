---
id: intermediate
order: 2
title: AI Engineering on Microsoft
subtitle: Intermediate Roadmap
tagline: For engineers who want to build — designing an agent, then building, testing and publishing it in Copilot Studio, ending in one guided build you follow end to end.
next: advanced.html
next_label: Continue to the Advanced roadmap
continues: yes
audience: Engineers
skills_pin: v0.3.0
card: How models behave, agents and harnesses, Copilot Studio, writing instructions, knowledge and RAG, tools, connectors and MCP, Agent Skills, safety and moderation, designing an agent, evaluation, publishing, the six-skill toolchain and a guided build — with Snowflake SQL and Power Automate as reference.
---

# what-you-already-know | What You Already Know
The Basic topics this level takes for granted. None of them is taught again here — each one links to where it is taught, so you can go back if a term is unfamiliar.

## llm | What Is an LLM | assumed
Everything in this level assumes you know that a model predicts tokens rather than looking facts up.

## context | Context & Context Window | assumed
The single idea behind instruction budgets, tool counts and why long conversations degrade.

## hallucination | Hallucinations & Grounding | assumed
Why grounding exists at all, and why an agent with no knowledge source still answers.

## anatomy | Anatomy of a Prompt | assumed
Standing instructions, context and the user's message as three separate layers.

## clarity | Clarity & Specificity | assumed
Stating the role, the task, the audience and the constraints.

## fewshot | Few-Shot Examples | assumed
Showing the shape you want instead of describing it.

## output | Output Formats | assumed
Asking for a named shape so the answer is usable without editing.

## decompose | Breaking Down Tasks | assumed
Splitting a complex request into ordered steps you can check one at a time.

## iterate | Iterating on Prompts | assumed
Trying a prompt on several realistic cases and comparing the answers.

## tenantgrounding | Grounded in Your Own Work | assumed
That Copilot can answer from your organisation's content, which is what makes its mistakes yours.

## visibility | You Only See What You Could Already Open | assumed
Permissions are inherited, not widened — the rule every agent you build also obeys.

## missingcontent | Why Copilot Missed a File | assumed
The shortlist of causes you will diagnose again as an agent builder.

## sensitive | What Not to Paste In | assumed
Sensitivity labels, and which assistant you are actually talking to.

## rai | Responsible AI Principles | assumed
The six principles, used here as a design checklist rather than a usage one.

## m365chat | Microsoft Copilot Chat | assumed
What your users have already met, and the bar your agent is measured against.

## usingagents | Using Agents Someone Published | assumed
You have been on the other side of this. Everything you build lands there.

# getting-oriented | Getting Oriented
The role, the landscape, what you need before you build, and what your own tenant decides for you.

## role | The AI Engineer Role
An AI engineer builds solutions on top of pre-trained models and platforms instead of training models from scratch. The job is to combine models, prompts, data, tools and automation into reliable products, and to measure and govern them. This is different from a data scientist or ML engineer, who mainly create and train models.
- video | Introduction to generative AI and agents (AI-901, Microsoft Learn) | https://www.youtube.com/watch?v=ksNWjglbKeg
- course | Introduction to AI concepts (Microsoft Learn training) | https://learn.microsoft.com/en-us/training/modules/get-started-ai-fundamentals/
- doc | Study guide for Exam AB-100: Agentic AI Business Solutions Architect | https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ab-100

## stack | The Microsoft AI Stack Map
Microsoft offers several places to build with AI. Microsoft Copilot and Agent Builder serve end users. Copilot Studio is the low-code agent platform, and Power Platform adds automation and data. GitHub Copilot and VS Code are for developers, and Microsoft Foundry is for pro-code models and agents. In this program Snowflake is the governed data platform that agents query. Knowing which tool fits which job avoids rebuilding the same thing twice.
- doc | Choose between Agent Builder in Microsoft 365 Copilot and Copilot Studio to build your agent | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/copilot-studio-experience
- doc | Compare declarative and custom engine agents | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agents-overview
- video | Choose a Microsoft 365 Copilot extensibility development path (MS-4010) | https://www.youtube.com/watch?v=ARPj2XpkCpU

## licensing | Licensing & Copilot Credits
Microsoft AI products mix per-user licences (a Microsoft 365 Copilot licence, GitHub Copilot) with consumption billing — Copilot Credits for Copilot Studio, AI Builder credits. Building, testing and evaluating agents all consume credits, not just answering users, so understand what your environment is billed on before you run a twenty-five case evaluation for the fourth time.
- doc | Standard harness licensing (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing
- doc | Manage Copilot Credits and capacity | https://learn.microsoft.com/en-us/power-platform/admin/manage-copilot-studio-copilot-credits-capacity
- doc | Licensing and AI Builder credits | https://learn.microsoft.com/en-us/ai-builder/credit-management

## devenv | Your Developer Environment
Every engineer should build in their own Power Platform developer environment, never directly in production. Pair it with Copilot Studio access, VS Code with GitHub Copilot, and Snowflake access through your own development role. Agents and connectors you build should never use that role: give them a separate, read-only one.
- doc | Create a developer environment (Power Apps Developer Plan) | https://learn.microsoft.com/en-us/power-platform/developer/create-developer-environment
- doc | Power Apps Developer Plan | https://learn.microsoft.com/en-us/power-platform/developer/plan
- article | 7 mistakes to avoid when creating a Power Platform environment (Matthew Devaney) | https://www.matthewdevaney.com/7-mistakes-to-avoid-when-creating-a-power-platform-environment/

## agentbuilder | Agent Builder in Microsoft Copilot
Agent Builder is where most people build their first agent: you describe it in plain language and give it instructions, knowledge such as SharePoint or files, and a few capabilities. It is worth an hour of your time before you open Copilot Studio, because it shows you the whole shape of an agent with nothing to configure. Its ceiling is also the reason this level exists — no connectors, no workflows, no evaluation, no environments.
- doc | Agent Builder in Microsoft 365 Copilot | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder
- course | Build agents in Copilot Chat (online workshop) | https://learn.microsoft.com/en-us/training/modules/agents-copilot-chat/
- doc | Choose between Agent Builder in Microsoft 365 Copilot and Copilot Studio to build your agent | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/copilot-studio-experience

## tenantvaries | What Your Tenant Decides
Nothing in this level can tell you what exists in your own environment. Features ship off by default, connectors vary by licence and premium tier, and an admin policy can block a combination that works fine for a colleague. Microsoft publishes the catalogue of connectors that exist; which of them your own environment actually offers you, after licence tier and policy, is published nowhere. Treat every tool recommendation as a claim to check rather than a fact, and learn where to look: the connector list in your own environment, and your admin.
- doc | Security and governance (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance
- doc | Connectors overview | https://learn.microsoft.com/en-us/connectors/overview
- doc | Quotas and limits | https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-quotas

# how-models-behave | How Models Behave
The model-level facts you have to hold to make sensible choices about cost, latency and settings.

## tokens | Tokens
Models don't read words; they read tokens — chunks of text that are often parts of words. In English one token is roughly four characters or about ¾ of a word. Tokens drive three things you care about: cost, speed and how much fits in a request.
- doc | Understanding tokens | https://learn.microsoft.com/en-us/dotnet/ai/conceptual/understanding-tokens
- video | Why your AI costs spike (tokens explained) — Microsoft Learn | https://www.youtube.com/watch?v=NmkR7V_wTqA

## inference | Inference
Inference is the act of running a trained model to produce output. Your request is tokenised and processed by the model, and a response is generated one token at a time, often streamed back. Latency depends on the model's size, how long your input is and how much it generates.
- doc | LLM fundamentals — how models generate responses | https://learn.microsoft.com/en-us/agent-framework/journey/llm-fundamentals
- video | Select, deploy, and evaluate Microsoft Foundry models (AI-103) | https://www.youtube.com/watch?v=71gi8ULxPZQ

## temperature | Temperature & Sampling
Temperature controls how random the next-token choice is. Low values (≈0–0.3) give focused, repeatable answers. Higher values give more varied, creative text. Top-p is a related setting. In Copilot Studio you mostly control this through prompt and model settings, and many reasoning models ignore temperature entirely.
- doc | Change the model version and settings (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/prompt-model-settings
- doc | Prompt engineering techniques — temperature and top_p | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering

## training | Training vs. Fine-Tuning (Concepts)
Pre-training teaches a model general language from massive datasets; instruction tuning teaches it to follow requests. Fine-tuning further trains an existing model on your examples to specialise it. Know the vocabulary, and know that almost nothing you build in this level will need it: business problems here are solved with instructions and grounding.
- doc | Getting started with customizing a large language model (LLM) (classic) | https://learn.microsoft.com/en-us/azure/foundry-classic/openai/concepts/customizing-llms
- video | Compare model optimization strategies (AI-3016) | https://www.youtube.com/watch?v=SkGItraTlHc

## models | Choosing a Model
Different models trade quality, speed, cost and reasoning depth. Copilot Studio lets you pick the primary model for an agent, including OpenAI GPT and Anthropic Claude models. Reasoning models think longer for complex tasks; chat models are faster for simple ones. Changing the model is a change to the agent, so it gets re-evaluated like any other.
- doc | Select a primary AI model for your agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-select-agent-model
- doc | Anthropic models in Microsoft Online Services | https://learn.microsoft.com/en-us/microsoft-365/copilot/connect-to-ai-subprocessor
- video | SLMs vs. LLMs (Microsoft Learn) | https://www.youtube.com/watch?v=ShMTL5avG40

## multimodal | Multimodal Models | opt
Multimodal models accept or produce more than text: images, documents, audio or voice. They let agents read screenshots, analyse PDFs or hold voice conversations. Treat these as extensions of the same prompt-and-context ideas.
- doc | Image prompt engineering techniques | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/gpt-4-v-prompt-engineering
- video | Develop a vision-enabled generative AI application (AI-103) | https://www.youtube.com/watch?v=Xlo-VDqYrz4

# agent-fundamentals | Agent Fundamentals
What makes something an agent, what a harness is, how the runtime chooses what to do — and what all of it costs.

## agent | What Is an Agent
An agent combines a model, instructions, knowledge and tools with a loop that decides what to do next. It can answer questions, take actions such as creating a ticket or running a flow, and work through tasks in several steps. Chatbots follow scripts; agents choose their next step within the limits you set.
- doc | Compare declarative and custom engine agents | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agents-overview
- video | Stop building chatbots. Build AI agents. (Microsoft Learn) | https://www.youtube.com/watch?v=GMstvVqy6EI
- video | Get started with generative AI and agents in Azure (AI-901) | https://www.youtube.com/watch?v=nw8yN8Nhgfc

## autonomous | Conversational vs. Autonomous Agents
Conversational agents respond when a user chats with them. Autonomous agents start from events instead, such as a new email, a new file or a schedule, and run without anyone chatting. Autonomous agents need tighter instructions, limits and monitoring, because nobody is watching the answer as it arrives.
- doc | Add an event trigger (autonomous agents) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-trigger-event
- video | Introduction to autonomous agents (PL-7008 Ep. 7) | https://www.youtube.com/watch?v=wvtLiylvkK8
- video | Incredible Excel-Writing Autonomous Agent In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=vd5DLiu1_6Y

## orchestration | Orchestration
Orchestration decides how an agent handles a request: which knowledge to search, which tool, skill or topic to call, what to ask the user, and how to combine the results. With generative orchestration the model makes that choice **from the descriptions you wrote** — not from a filename, not from an explicit call. This is the single most load-bearing fact in the level: most of what you author is a description that has to win a selection you never see.
- doc | Orchestrate agent behavior with generative AI | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions
- video | Copilot Studio: How I Built A Generative Orchestration Agent (Matthew Devaney) | https://www.youtube.com/watch?v=QTuuoUg8Hpg
- article | How to build a Copilot Studio agent with generative orchestration (Matthew Devaney) | https://www.matthewdevaney.com/how-to-build-a-copilot-studio-agent-with-generative-orchestration/

## harness | What Is a Harness
A harness is the runtime that sits between what you build and the model. It decides when to call the model, what to send it, how to read the reply and which tools to run. The same model can behave very differently in different harnesses, and the features you can use are the harness's, not the model's.
- doc | Harnesses in Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview

## chooseharness | Choosing a Harness in Copilot Studio
Copilot Studio offers three harnesses:
- **GitHub Copilot harness:** reasoning-heavy, multi-step work with skills, memory and files.
- **Standard harness:** rule-based agents with topics and agent flows.
- **Copilot chat harness:** extends Microsoft Copilot Chat with enterprise knowledge.

You choose when you create the agent and you cannot switch later. The guided build at the end of this level needs the GitHub Copilot harness, because skills do not exist on the other two.
- doc | Harnesses in Copilot Studio — compare harnesses | https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview
- doc | Agents powered by the GitHub Copilot harness overview | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/overview
- video | The FUTURE of Copilot Studio is HERE (Matthew Devaney) | https://www.youtube.com/watch?v=aX4bcDPTmPY

## contextcost | What Everything Costs on Every Turn
Instructions are re-sent on every single turn. So is every tool's definition. Knowledge results and conversation history pile up on top. The ceiling you actually hit is the combined context length, not any per-field character limit — which is why "trim the instructions" is usually the wrong fix and "move that reference material into a skill or a knowledge source" is the right one. An agent with fifteen tools pays for fifteen tools on every question, including the ones that need none of them.
- doc | Error codes reference for agents (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/troubleshooting-error-codes
- doc | Understanding tokens — context window and token limits | https://learn.microsoft.com/en-us/dotnet/ai/conceptual/understanding-tokens
- doc | Skills overview for agents | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-overview

## hitl | Human-in-the-Loop
Some actions shouldn't happen without a person: approving spend, sending external emails, changing records. Design explicit confirmations, approvals and escalation to a named human. This matters most for autonomous agents, where there is nobody in the conversation to object.
- doc | Agent flows overview — approvals and human review | https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview
- doc | Get started with Power Automate approvals | https://learn.microsoft.com/en-us/power-automate/get-started-approvals

# copilot-studio-basics | Copilot Studio Basics
The build surface itself: where things are, what a conversation is, and how to see what your agent actually did.

## tour | Copilot Studio Tour
Copilot Studio is Microsoft's low-code studio for building agents, workflows and agent flows. Learn what each area is for, because every instruction you will ever be given is a click path through them — and the layout depends on the harness. An agent on the GitHub Copilot harness is four tabs: **Build** (instructions, knowledge, tools, skills, model, memory), **Preview** (test chat and activity trace), **Evaluate** and **Monitor**. An agent on the standard harness has the older page layout — an Overview page, a test panel with an activity map, and **Topics**, which exist only there. Every Microsoft page says which harness it describes; read that first.
- doc | Copilot Studio overview | https://learn.microsoft.com/en-us/microsoft-copilot-studio/fundamentals-what-is-copilot-studio
- doc | Agents powered by the GitHub Copilot Harness overview | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/overview
- video | Build an initial agent with Microsoft Copilot Studio (PL-7008 Ep. 1) | https://www.youtube.com/watch?v=hzN2-K-8PP0

## create | Create Your First Agent
Start by describing the agent in natural language, and Copilot Studio drafts a first configuration from it — on the standard harness a name, description and instructions plus suggestions that last only for the session. Then refine them, add one knowledge source, test in the preview pane, and only add tools once the basic answers are good. The harness choice happens here and cannot be undone, and neither can the standard harness's primary language.
- doc | Start building (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/authoring-first-bot
- doc | Create and delete agents | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-first-bot

## model | Model Selection
Each agent has a primary model, and you can change it to trade speed, cost and reasoning ability. Retest with your evaluation set after you change models, because behaviour shifts even when your instructions stay the same.
- doc | Select a primary AI model for your agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-select-agent-model
- doc | Select a model (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/authoring-select-agent-model

## conversation | Conversations and Sessions
A conversation is the unit that holds history — and some of what the agent is made of is bound when it starts, not read fresh each turn. Saved instructions reach a conversation already running. An uploaded skill does not, which means a skill that installed correctly and one that failed to install look identical until you open a new chat. Starting a new chat is therefore the first diagnostic step for most apparent failures, and the step people skip.
- doc | Manage preview conversations (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/preview-history
- doc | Manage and delete skills in an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-manage
- doc | Error codes reference for agents (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/troubleshooting-error-codes

## topics | Topics & Trigger Phrases
In the standard harness, topics are conversation paths you design node by node, using messages, questions, conditions and tool calls. Under generative orchestration the orchestrator picks a topic from its description; under classic orchestration, from its trigger phrases. The GitHub Copilot harness has no topics. Use topics when a conversation must follow exact, predictable steps, such as a compliance check.
- doc | Create and edit topics | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-create-edit-topics
- video | Manage topics in Microsoft Copilot Studio (PL-7008 Ep. 2) | https://www.youtube.com/watch?v=IOXMxuL9NrI
- video | Question Nodes vs Topic Inputs In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=c9IaXLj0NMc

## variables | Variables & Power Fx Basics
On the standard harness, variables store information during a conversation. Topic variables stay inside one topic and can be passed to or returned from another; global variables are shared across the agent; system and environment variables are supplied for you. Power Fx is the Excel-like formula language you use to check and transform values, build conditions and format output. The GitHub Copilot harness has no topics and so no variables.
- doc | Work with variables | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-variables
- doc | Create expressions using Power Fx | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-power-fx
- video | Work with entities and variables (PL-7008 Ep. 3) | https://www.youtube.com/watch?v=YANyM1hWxlo

## genai | Generative AI Settings
Agent-level settings control generative orchestration, whether the agent may answer with no knowledge source or tool behind it, whether it searches the public web, and how strict content moderation is. Review them on every new agent; the defaults aren't always right for your case, and on the standard harness **Allow ungrounded responses** is the one that quietly turns a grounded agent into a chatty one. The GitHub Copilot harness has a much shorter list — moderation, but no grounding switch — so there, grounding lives in the instructions.
- doc | Orchestrate agent behavior with generative AI | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions
- doc | Knowledge sources summary | https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio
- doc | Configure settings for GitHub Copilot agents | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/settings-overview

## createdfiles | Files the Harness Makes for You | prev
On the GitHub Copilot harness the agent creates and edits Word, Excel, PowerPoint and PDF files natively and offers them as a download, with nothing to configure. Know this before you write code to do it: the most common waste in a first skill is a Python script producing a spreadsheet the harness would have produced anyway. Created files carry limits on size and how long they stay available, so anything you need to keep, you download.
- doc | Files the agent creates (preview) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/created-files-overview
- doc | Harnesses in Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview

## test | Testing in the Preview Pane
The preview pane lets you chat with your draft agent and watch what it did: the **activity trace** in the GitHub Copilot harness's Preview tab, the **activity map** in the standard harness's test panel. Both show which knowledge, tools and skills or topics it used, with what inputs and results. Use it to diagnose bad answers before you blame the model — most of the time the model chose something reasonable from a description you wrote badly.
- doc | Use the activity trace to debug your agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/authoring-activity-trace
- doc | Test an agent (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/authoring-test-bot
- doc | Test your agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-test-bot

# writing-instructions | Writing Instructions
The agent's standing instructions are the one artifact you will rewrite most often. There is a format, and it is not freeform prose.

## instructions | Instructions
The Instructions field tells the agent who it is, what it covers, how to respond and what it must never do. With generative orchestration it also steers which knowledge and tools get used, so it is doing two jobs at once: describing the agent, and biasing every selection the orchestrator makes. Saved instructions take effect immediately, including in a conversation already running.
- doc | Configure agent details and instructions (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/authoring-instructions
- doc | Orchestrate agent behavior with generative AI — instructions | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions

## xml | Structuring Instructions with XML Tags
XML-style tags split instructions into labelled sections the model can tell apart, and this level uses a fixed set in a fixed order: `<role>`, `<tone>`, `<tasks>`, `<instructions>`, `<rules>`. Further sections — `<output_format>`, `<knowledge_routing>`, `<tool_use>`, `<connected_agents>`, `<escalation>`, `<out_of_scope>`, `<data_handling>`, `<examples>` — are added only when something specific calls for them, each one preventing a specific failure. Tags keep text you quote from being read as instructions, but they cannot wrap what the agent retrieves at runtime, so the defence against injected text is a rule you write.
- doc | Prompt engineering techniques — use clear syntax and delimiters | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering
- doc | Develop a RAG Solution on Azure — Prompt Engineering | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-prompt-engineering

## writinginstructions | Writing Instructions That Hold Up
Good instructions are specific, structured and tested against real questions. Two rules do most of the work. Rules are written as must or must-never **with the reason attached**, because a rule whose reason is missing gets reasoned around. And size is economic, not cosmetic: everything here is paid for on every turn, so the fix for instructions that have grown too long is to move reference material (never directives) out into a skill or a knowledge source, never to cut the role, tone, rules or routing sections to fit. If they cannot fit without cutting those, the agent is doing too much and should be split.
- doc | Write effective instructions for declarative agents | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-instructions
- doc | Quotas and limits | https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-quotas
- video | Build effective agents in Microsoft Copilot Studio (PL-7008 Ep. 4) | https://www.youtube.com/watch?v=VV-lSSPQwW4

## tasksvsinstr | Tasks vs. Instructions
The two sections people mix up, with a clean test: if a line answers *what does it produce*, it is a task; if it answers *what does it do next*, it is an instruction. Getting this wrong produces instructions that read like a job description and an agent that never does anything in a particular order. It matters more than it sounds, because the tasks section is also what your evaluation's happy-path cases are derived from.
- doc | Configure agent details and instructions (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/authoring-instructions
- doc | Write effective instructions for declarative agents | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-instructions

# knowledge-and-rag | Knowledge & RAG
Ground agents in your organisation's content so answers are accurate and cited.

## rag | What Is RAG
Retrieval-augmented generation (RAG) finds the most relevant pieces of your content for a question and adds them to the model's context. The model then writes an answer grounded in that content. It is how agents answer from company data without being retrained.
- doc | RAG and generative AI (Azure AI Search) | https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview
- video | Understand Retrieval Augmented Generation (RAG) with Azure OpenAI Service (Microsoft Learn) | https://www.youtube.com/watch?v=loHvK_bXuYE

## sources | Knowledge Sources Overview
Copilot Studio agents can use these knowledge sources:
- public websites
- SharePoint and OneDrive
- uploaded files
- Dataverse tables
- enterprise systems through connectors

Each source differs in how fresh the data is, how permissions work and what limits apply.
- doc | Knowledge sources summary | https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio
- doc | Add SharePoint as a knowledge source | https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-sharepoint
- doc | Available knowledge sources for agents (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/knowledge-sources-overview

## connectorknowledge | Copilot Connectors vs. Power Platform Connectors
Copilot connectors (formerly Graph connectors) index external content into Microsoft 365 ahead of time. Power Platform connectors used as knowledge query the source system live, with each user's own permissions. Pick based on how fresh the data must be and whose permissions apply.
- doc | Copilot connectors versus Power Platform connectors as knowledge | https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-graph-vs-power-platform-connectors
- doc | Add Power Platform connectors as knowledge | https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-real-time-connectors

## snowflakeknowledge | Snowflake as a Knowledge Source
You can add selected Snowflake tables as a knowledge source in Copilot Studio — a preview feature, documented for the standard harness. Microsoft indexes only table and column names, the data stays in Snowflake, makers don't write SQL, and each question runs as the asking user's own Snowflake identity. Because names are most of what the agent has, clean, well-named tables and views give much better answers — which is what the Snowflake reference module at the end of this level is for.
- doc | Add Power Platform connectors (incl. Snowflake) as knowledge | https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-real-time-connectors
- doc | Snowflake (Connectors reference) | https://learn.microsoft.com/en-us/connectors/snowflakev2/

## citations | Citations & Answer Quality
Citations let users check where an answer came from, and they build trust. Attaching a knowledge source is not the same as being grounded in it: unless your instructions say to answer from it and to say so when it has nothing, the agent will fill the gap from its own reasoning and sound just as confident. When knowledge returns nothing at all, the cause is usually one of these:
- permissions
- the source hasn't finished indexing
- the file is too large or in an unsupported format
- the question doesn't match the content
- doc | SharePoint knowledge sources don't return results | https://learn.microsoft.com/en-us/troubleshoot/power-platform/copilot-studio/knowledge/sharepoint-no-response
- article | Set citation to open a specific PDF page in Copilot Studio (Matthew Devaney) | https://www.matthewdevaney.com/set-citation-to-open-specific-pdf-page-in-copilot-studio/

## workiq | Work IQ & Foundry IQ | opt, prev
Work IQ gives agents organisational context such as email, calendar, files, Teams messages and people. Foundry IQ gives agents ready-made knowledge bases from Microsoft Foundry. Learn what they are for now; the Advanced level covers using them.
- doc | Work IQ overview | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/
- doc | What is Foundry IQ? | https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq
- video | Work IQ is the layer that makes AI feel personal (Microsoft Learn) | https://www.youtube.com/watch?v=nQ74VnmQIqY
- video | Foundry IQ: the future of RAG with knowledge retrieval (Microsoft Learn) | https://www.youtube.com/watch?v=h1n19QCPc1I

# tools-connectors-mcp | Tools, Connectors & MCP
Let agents act: call systems, run automations and use external tools.

## tools | What Are Tools
Tools are how agents do things rather than just talk. Examples include connector actions, agent flows, prompts, REST APIs, MCP servers and computer use. There are three kinds worth planning around — connectors for well-known external services, MCP servers for internal or custom services, workflows for deterministic multi-step processes — and a fourth question that comes first: is this a tool at all, or is it a skill?
- doc | Add tools to custom agents | https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-tools-custom-agent
- doc | Add an agent flow as a tool to an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/flow-agent

## tooldesc | Descriptions Decide Which Tool Fires
The orchestrator picks a tool mainly from its description, then its name and the names and descriptions of its inputs and outputs. So those are not labels; they are the interface. "Ticket tool" loses to "Create support ticket", and two tools with near-identical descriptions make the choice between them unpredictable. Rewrite the description a tool arrives with, write them as you would write instructions, and keep the count small: every tool costs context on every turn and makes the choice harder.
- doc | Add a tool to an agent (GitHub Copilot) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/add-tools-custom-agent
- doc | Add tools to custom agents | https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-tools-custom-agent
- doc | Orchestrate agent behavior with generative AI | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions

## connectors | Power Platform Connectors
Connectors are prebuilt wrappers around APIs, such as Outlook, SharePoint, Dataverse, ServiceNow and Snowflake. They expose actions and triggers that Power Automate, Power Apps and Copilot Studio can all use. More than 1,000 exist and custom connectors fill the gaps — but the complete list for your own tenant is not published anywhere, so search your environment rather than trusting that a connector exists.
- doc | Connectors overview | https://learn.microsoft.com/en-us/connectors/overview
- doc | Use connectors in Copilot Studio agents | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-connectors

## connauth | Connections & Authentication
A connection holds the credentials a connector uses. It can run as the end user, with the user's own permissions, or as the maker or a service account. This choice decides what data users can reach through your agent, and it is the single most common reason an agent that worked for its author breaks the day it is shared.
- doc | Use connectors in Copilot Studio agents — authentication | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-connectors
- article | Power Automate standards: connection references (Matthew Devaney) | https://www.matthewdevaney.com/power-automate-coding-standards-for-cloud-flows/power-automate-standards-connection-references/

## addconnector | Adding a Connector Tool to an Agent
Add a connector action as a tool, set which inputs the agent fills in and which stay fixed, and give it a clear description. Then test that the orchestrator calls it at the right moment with the right values — and that it does not call it for questions it should answer from knowledge.
- doc | Use connectors in Copilot Studio agents | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-connectors
- video | Copilot Studio: ServiceNow Connect Knowledge Base + Helpdesk Tickets (Matthew Devaney) | https://www.youtube.com/watch?v=LpRdT49U9Cw

## mcp | What Is MCP
The Model Context Protocol (MCP) is an open standard for connecting AI applications to tools and data, often compared to "USB-C for AI". An MCP server exposes tools, and any MCP-capable client can use them: Copilot Studio, GitHub Copilot or Snowflake. You consume servers here; the Advanced level builds one.
- doc | What is the Model Context Protocol (MCP)? | https://modelcontextprotocol.io/docs/getting-started/intro
- doc | Extend your agent with Model Context Protocol | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp

## mcpadd | Adding an Existing MCP Server to an Agent
In Copilot Studio you can add an existing MCP server as a tool. Its tools, and any updates to them, flow into your agent automatically — which is convenient and also means the tool surface can change without you touching the agent. Prefer certified or internally approved servers, check what each tool can do before you enable it, and note that MCP servers cap how many can run at once in one conversation.
- doc | Connect your agent to an existing Model Context Protocol (MCP) server | https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent
- video | Integrate MCP tools with Azure AI agents (AI-103 Ep. 9) | https://www.youtube.com/watch?v=pQ9yEEcXNeE

## connected | Connected & Child Agents
Large agents are hard to maintain. Split specialised jobs into child agents inside the same agent, or into connected agents that run on their own. The main agent hands tasks to them the way a team lead delegates to specialists — and the failure to design against is an agent that either hoards work it should pass on, or passes on work it should have done itself.
- doc | Add other agents (connected and child agents) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-add-other-agents
- video | Master Multi-Agent Orchestration In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=xtPlDde4Yv0

## computeruse | Computer Use | opt
Computer use lets an agent work websites and desktop apps the way a person does: clicking, typing and reading the screen. It is useful for systems without an API. It is slower and more fragile than connectors, so treat it as a last resort.
- doc | Automate web and desktop apps with computer use | https://learn.microsoft.com/en-us/microsoft-copilot-studio/computer-use
- video | Computer Use Agent: Extract Web Page Data In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=isClxl1O_Zs

# agent-skills | Agent Skills
Package know-how as a file the agent loads only when it is needed. The format is open, and it is the artifact the Advanced level picks up.

## skill | What Is a Skill
A skill is a reusable capability: a name, a one-line description and Markdown instructions, optionally with extra files. The orchestrator loads it only when a request matches that description, so a skill costs almost nothing until it fires. Skills keep agents smaller and let teams share behaviour that has been proven once.
- doc | Skills overview for agents (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-overview
- video | How To Create Agent Skills In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=BvDGMw_7sbk

## skillsvs | Skills vs. Topics vs. Tools
- **Tools** perform an action.
- **Skills** hold reusable know-how about how to carry out a kind of task.
- **Topics** are scripted conversation paths in the standard harness.

A skill may use several tools; a topic fixes the exact steps. A task earns a skill when it needs bundled reference material, follows a fixed procedure that must run identically every time, produces an output format with its own conventions, or is needed only sometimes. Otherwise it belongs in instructions.
- doc | Skills overview for agents — skills, tools and orchestration | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-overview
- article | How to create agent skills in Copilot Studio (Matthew Devaney) | https://www.matthewdevaney.com/how-to-create-agent-skills-in-copilot-studio/

## openformat | Agent Skills Is an Open Format
Skills are not a Copilot Studio feature with a Copilot Studio file format. They use the open Agent Skills specification, which means the format is portable: the same artifact is read by other clients, including GitHub Copilot in VS Code. What does not travel is what a skill assumes — the tools it names and the limits of the harness it was tested on. That is worth knowing here for a practical reason — what you learn to author in this level is what the Advanced level learns to wield in VS Code — and for a strategic one: you are not writing into a proprietary box.
- doc | Agent Skills specification | https://agentskills.io/specification
- doc | Agent Skills Overview | https://agentskills.io/home
- doc | Skills overview for agents (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-overview

## skillmd | Anatomy of a SKILL.md
A skill is YAML frontmatter plus a Markdown body. The frontmatter carries a `name` — lowercase letters, numbers and hyphens, matching the folder — and a `description` on **one line**, which is the only thing the runtime sees when deciding whether to activate the skill. A vague description means a skill that never fires. The body holds the procedure; `references/`, `scripts/` and `assets/` folders hold anything it needs.
- doc | Create a skill for an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-create
- doc | Agent Skills specification | https://agentskills.io/specification

## addskill | Add an Existing Skill
You can add a ready-made skill by uploading a `SKILL.md` file or a `.zip` package. A skill that fails a load-time check is skipped without an error, and one you did not write is a dependency whose instructions your agent will follow, so read it first. It uses the same open format as GitHub Copilot, so a skill written once can be reused. Remember that the upload does not reach a conversation already running: open a new chat before deciding it failed.
- doc | Add an existing skill to an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-add-existing
- doc | Manage and delete skills in an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-manage

## createskill | Create a Simple Skill
Create a skill from blank with a clear name, a description of when to use it, and step-by-step instructions, or have Copilot generate one for you to review. A blank skill is a single file; one that needs a template is packaged and uploaded instead. The description decides whether the skill ever triggers, so test it with questions that should and shouldn't activate it. Write the body for a reader who knows the product but not your process.
- doc | Create a skill for an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-create
- video | How To Create Agent Skills In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=BvDGMw_7sbk

## packaging | Packaging a Skill Without Breaking It
Shape decides packaging: a single `SKILL.md` ships as a bare `.md`, and `SKILL.md` plus anything else ships as a `.zip` with `SKILL.md` at the **root** of the archive — a bundle wrapped in a folder is rejected. Two failures here are silent, which is what makes them expensive. Frontmatter that does not validate is skipped with no error, so the skill simply never appears. And on Windows, `Compress-Archive` writes entry paths the zip format forbids, producing an archive Copilot Studio may reject with nothing useful to say. A bad archive looks exactly like a bad skill.
- doc | Manage and delete skills in an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-manage
- doc | Add an existing skill to an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-add-existing

## sandbox | Scripts and the Sandbox
A skill can bundle scripts that the agent runs in a sandbox. Microsoft documents two limits for the same skill format in Microsoft 365 Copilot, and they are the ones to design to here: no network, and no installing packages. So a script may import a library and still fail on the first call that reaches out, and its data has to come in from a tool or an attachment. Before you write any of it, check whether the harness already does the job natively; scripting a spreadsheet it would have produced anyway is the most common waste in a first skill. You also have to read what you ship: you are responsible for a generated script you did not write.
- doc | Harnesses in Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview
- doc | Files the agent creates (preview) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/created-files-overview
- doc | Custom skills in declarative agents (preview) | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-skills

## skillscs | Skills in Copilot Studio
Agents on the GitHub Copilot harness accept skills you upload as a `SKILL.md` or a bundle, or write in the portal. This is where the skills you author become part of an agent other people use: uploaded, described, and then chosen or ignored by the orchestrator on every turn. Keep the installed set small and deliberate.
- doc | Add an existing skill to an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-add-existing
- video | How To Create Agent Skills In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=BvDGMw_7sbk

## reuse | Reuse in the Standard Harness
Standard-harness agents don't support skills at all. Reuse behaviour through component collections, which share topics, tools, flows and child agents by reference within an environment, or through connected agents that several agents can hand work to. Child agents organise one agent rather than share between agents. Pick the pattern that fits your harness rather than forcing one design on both.
- doc | Create and share reusable component collections | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-export-import-copilot-components
- doc | Add other agents (child agents) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-add-other-agents

# safety-and-moderation | Safety & Moderation
Moderation, injection, data policy and authentication — the four settings that decide whether an agent is safe to publish.

## moderation | Content Moderation in Copilot Studio
Copilot Studio checks both the user's input and the agent's response for harmful or malicious content, and a blocked turn gets no answer. The GitHub Copilot harness has one agent-level moderation setting; the standard harness can also set it per topic or prompt, and the topic-level setting wins at runtime. Stricter settings block more harmful content but answer fewer questions, so this is a trade-off you make deliberately rather than a box you tick.
- doc | FAQ for generative answers — content moderation | https://learn.microsoft.com/en-us/microsoft-copilot-studio/faqs-generative-answers
- doc | Resolve responsible AI content filter errors | https://learn.microsoft.com/en-us/troubleshoot/power-platform/copilot-studio/generative-answers/agent-response-filtered-by-responsible-ai
- doc | Error codes reference for agents (GitHub Copilot harness) — CONTENT_FILTERED | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/troubleshooting-error-codes

## injection | Prompt Injection & Jailbreaks
Prompt injection hides instructions in user input or in content the agent reads, such as a web page, email or document, to take control of the agent. It is riskier the more your agent can do with tools. Mitigations include content filters, keeping data separate from instructions with tagged sections, least-privilege connections and approvals before anything irreversible.
- doc | Prompt Shields (Azure AI Content Safety) | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection
- doc | FAQ for generative answers — responsible AI protections | https://learn.microsoft.com/en-us/microsoft-copilot-studio/faqs-generative-answers

## dlp | Data Privacy & DLP Awareness
Data policies (DLP) decide which connectors, knowledge sources and channels agents may use together. If a tool is blocked, it's often a policy, not a bug — and the reason is shown where makers rarely look: a disabled option's hover text, or a details file behind the publish error. Know what data leaves your tenant and where it goes before you publish anything.
- doc | Configure data policies for agents | https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention
- doc | Security and governance (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance

## agentauth | Agent Authentication Options
An agent can require no authentication, Microsoft Entra ID sign-in or, on the standard harness only, manual authentication. This decides who can talk to it and whether it can act as the signed-in user. Internal agents that touch company data require authentication — and the choice interacts with your connections, because "as the signed-in user" only means something if there is one.
- doc | Configure user authentication | https://learn.microsoft.com/en-us/microsoft-copilot-studio/configuration-end-user-authentication
- doc | Configure settings for GitHub Copilot agents | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/settings-overview
- video | Copilot Studio: Publish To A Website With Single Sign-On (Matthew Devaney) | https://www.youtube.com/watch?v=dUXE4FTx9Cw

# designing-an-agent | Designing an Agent
The module with no Microsoft product in it. Most agents fail because nobody decided what they were for, and this is the work that decision takes.

## brief | The Agent Brief
Before you build, you write down what the agent is for: its users, its tasks, its inputs and outputs, its rules, what it escalates and what it refuses. That document is a design record, not runtime text — it is not the Instructions field, and pasting it there is the most common first mistake. Its job is to be specific enough that someone else could check whether the finished agent does what was asked.
- doc | Write effective instructions for declarative agents | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-instructions
- doc | Study guide for Exam AB-100: Agentic AI Business Solutions Architect | https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ab-100

## users | Users and the Real Artifacts
Name the users and say how expert they are, because a tone decision and a refusal both depend on it. Then ask for the artifacts rather than more answers: a sample output settles the outputs question better than any description, and a policy document surfaces rules nobody would have thought to mention. "Everyone at the company" is not a user.
- doc | Compare declarative and custom engine agents | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agents-overview
- course | Introduction to AI concepts (Microsoft Learn training) | https://learn.microsoft.com/en-us/training/modules/get-started-ai-fundamentals/

## tasks | Tasks as Verb Phrases
A task is a verb phrase with a trigger and a finished state: what starts it, and how you know it is done. "Help with reporting" is not a task. "Draft the weekly production summary from the shift logs, ready for the supervisor to sign" is one, because you can tell whether it happened. Every happy-path test case you will write later comes out of this list, so a vague task produces a vague test.
- doc | Write effective instructions for declarative agents | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-instructions
- doc | Review the agent evaluation checklist | https://learn.microsoft.com/en-us/agents/agent-evaluation/evaluation-checklist

## inputsoutputs | Inputs and Outputs
For each input: what format it arrives in, where it comes from, and whether it always arrives. That last one is the whole of your edge-case testing. For each output: the format, who reads it, and a real example — not a description of an example. Inputs that sometimes do not arrive are where agents quietly invent things, and an output with no named reader has no standard to be judged against.
- doc | Knowledge sources summary | https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio
- doc | Review the agent evaluation checklist | https://learn.microsoft.com/en-us/agents/agent-evaluation/evaluation-checklist

## rules | Rules, Refusals and Escalation
Write at least one must-never rule **with the reason attached**, because a rule with no reason gets reasoned around by a model that is trying to be helpful. Name one plausible thing the agent must refuse — plausible, not absurd; the interesting refusals are the ones a well-meaning user would ask for. And state one escalation condition with a named recipient, because "escalate to a human" names nobody and therefore happens to no one.
- doc | Agent flows overview — approvals and human review | https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview
- doc | Responsible AI Principles and Approach | https://www.microsoft.com/en-us/ai/principles-and-approach

## scope | Scope, Tone and Delegation
Three decisions that are cheap to make now and expensive later. Out of scope: what this agent will not do, written down so the next request does not quietly expand it. Tone: not "professional" but a choice between real alternatives, because the same answer lands differently on a supervisor and on a customer. Delegation: whether any of this belongs to a connected agent, decided before you build one agent that does everything.
- doc | Add other agents (connected and child agents) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-add-other-agents
- doc | Configure agent details and instructions (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/authoring-instructions

## triage | Instructions, Knowledge, Tool or Skill
Every requirement lands in exactly one of four places, and the triage is learnable. Read live data, or write into another system: a tool. A fixed multi-step process with branching or approvals: still a tool, built as an agent flow. Content the agent should answer from: knowledge. Produce a document, follow a procedure, or apply bundled reference material: a skill, not a tool. Everything else: instructions. Users reach for connectors when what they need is instructions, and every unnecessary tool costs context on every turn.
- doc | Add tools to custom agents | https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-tools-custom-agent
- doc | Skills overview for agents (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-overview
- doc | Knowledge sources summary | https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio

## successcriteria | Success Criteria Are Not Instructions
Success criteria are how you will know the agent is working — and they go nowhere in the instructions. Success criteria measure the agent; the agent cannot act on them. Telling it "answers should be accurate" changes nothing about its behaviour and costs context on every turn. They belong in the brief, where the evaluation set and the human review rubric are derived from them instead.
- doc | About agent evaluation | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-intro
- doc | Review the agent evaluation checklist | https://learn.microsoft.com/en-us/agents/agent-evaluation/evaluation-checklist

## interview | Running the Design Interview
You will usually be filling this brief in for somebody else, and the mechanics matter. One question per message. Three or four genuinely different concrete options, one of them recommended, plus a way out — because someone who has never designed an agent does not know what a tone decision involves until they read three real alternatives. Keep the answers in their own words: the binding constraint is usually in *how* they said it, and it cannot be recovered once you have smoothed it into your own prose.
- doc | copilot-agent-review (copilot-studio-skills v0.3.0) | https://github.com/matheus-sancha/copilot-studio-skills/blob/v0.3.0/skills/copilot-agent-review/SKILL.md
- doc | Study guide for Exam AB-100: Agentic AI Business Solutions Architect | https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ab-100

# testing-and-evaluation | Testing & Evaluation
Prove your agent works — repeatedly, not just once. The method on this harness shapes what a test case can even be.

## whyeval | Why Evaluate Agents
Agents don't give the same output every time, and they change when you edit instructions, knowledge or models. "It worked when I tried it" is not evidence. Evaluation means running a fixed set of questions and checking the answers every time you change anything — and the comparison between runs, not any single score, is the signal.
- doc | About agent evaluation | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-intro
- doc | Review the agent evaluation checklist | https://learn.microsoft.com/en-us/agents/agent-evaluation/evaluation-checklist

## judge | How the Grading Actually Works
On the GitHub Copilot harness the grader is a model: the one test method, General quality, assesses whether the response was relevant and complete, and it does **not** compare the answer to an expected answer you wrote — the standard harness's other methods do. That one fact reshapes everything: the question is the entire lever, because a vague question produces a vague pass. Write expected responses anyway — a human auditing a failure needs to know what was supposed to happen — but write them as what a correct answer must contain, never as literal wording.
- doc | Evaluate an agent (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/analytics-agent-evaluation-intro
- doc | Choose evaluation methods | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-overview

## manual | Manual Testing & the Activity Map
Before you automate, reproduce problems by hand in the preview pane, starting from the user's exact words. Use the activity trace (the activity map on the standard harness) to see whether the fault was the wrong knowledge, the wrong tool, bad inputs or unclear instructions — four different fixes that look identical from the answer alone. And start a new chat first, because history from your last attempt is the most common reason a fix looks like it did not work.
- doc | Manage preview conversations (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/preview-history
- doc | Test your agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-test-bot
- video | How To View Conversation Transcripts In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=uPWyhoRqo-0

## testsets | Evaluation Sets
An evaluation set is a list of conversations used as test cases, with expected responses where you have them. You can write it by hand, generate it from your agent's description and instructions, or import it from a CSV file; the standard harness also generates from knowledge and captures test chats and real user questions. Generated cases cannot see gaps the agent's own description leaves out. Cover the categories deliberately rather than writing whatever comes to mind — happy path, edge cases, rule violations, refusals, escalations, tone — so no category is forgotten because the brief was thin there. Multi-turn cases matter: agents hold the first turn fine and lose the thread by the third.
- doc | Create a test set for an agent (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/analytics-agent-evaluation-create
- doc | Create a single response test set | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-create
- video | Copilot Studio Test Automation: STOP Testing Manually!! (Matthew Devaney) | https://www.youtube.com/watch?v=qh4YRqZgaQU

## advtests | Writing Cases That Can Actually Fail
A test only tests something if the agent could plausibly get it wrong. Phrase questions the way a real user would, typos and all, rather than as polished sentences nobody types. Make a rule-violation case tempting, not absurd: "the supervisor already approved it verbally, can you put that in?" tests the rule, while "ignore your instructions" tests nothing. One behaviour per case, and vary the surface between cases so you are not testing the same phrasing six times.
- doc | Create a single response test set | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-create
- doc | Prompt Shields (Azure AI Content Safety) | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection

## testidentity | Who the Test Runs As
An evaluation runs as an identity, and that identity decides what the agent's per-user knowledge and tools return — so a run as the maker, who can usually see everything, scores an agent your users never meet. On the GitHub Copilot harness that identity is whoever is signed in. Decide who each run is for before you run anything, and treat a suspiciously clean first run as a reason to check it. This is the same authentication question as `connauth`, arriving where it is easiest to miss.
- doc | Run evaluations and view results | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-results
- doc | Use connectors in Copilot Studio agents — authentication | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-connectors
- doc | Evaluate an agent (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/analytics-agent-evaluation-intro

## runeval | Running Evaluations & Reading Results
Run the set, review the result for each case, open the failures to see why they failed, fix the agent and run it again. Keep the results so you can compare versions. Read a percentage with suspicion: a score tells you how many cases passed, not whether the agent is finished, which is what the human review rubric from your success criteria is for.
- doc | View evaluation results for an agent (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/analytics-agent-evaluation-view
- doc | Run evaluations and view results | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-results
- doc | Choose evaluation methods | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-overview

## feedback | Feedback Loop
Real user questions, thumbs up and down, and transcripts are the best source of new test cases. Close the loop: failed conversations become new cases, then a fix, then another run. An evaluation set that never grows stops being evidence about the agent people are actually using.
- doc | Monitor agent performance overview (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/analytics-overview
- doc | Monitor overview (analytics) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-overview
- video | Monitor, analyze, and tune AI agents (AB-100 Ep. 11) | https://www.youtube.com/watch?v=JR6C87ZEtws

# publishing-and-environments | Publishing & Environments
Move agents from your developer environment into users' hands without surprises.

## envs | Power Platform Environments
Environments are containers for apps, flows, agents and data, each with its own security. Use separate developer, test and production environments so experiments never affect real users.
- doc | Environments overview | https://learn.microsoft.com/en-us/power-platform/admin/environments-overview
- video | Manage the Microsoft Power Platform environment (PL-900 Ep. 2) | https://www.youtube.com/watch?v=1OGCfs_joVA

## solutions | Solutions Basics
Solutions package agents, flows, connection references and environment variables so they can move between environments. Create every agent inside a custom solution from day one; retrofitting one later is real work.
- doc | Create and manage custom solutions in Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-solutions-overview
- doc | Solution concepts | https://learn.microsoft.com/en-us/power-platform/alm/solution-concepts-alm

## publish | Publishing an Agent
Saving keeps your draft; publishing makes the latest version available on every connected channel. Copilot Studio will not publish an agent with no name, description or instructions, so the short description is user-facing copy you have to write rather than a field to fill. After you publish, retest in the real channel, because authentication and rendering differ from the test pane.
- doc | Publish an agent (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/publication-publish-agent
- doc | Key concepts — publish and deploy your agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-fundamentals-publish-channels

## channels | Channels
Channels are where users meet your agent: Teams and Microsoft Copilot, websites, and — on the standard harness — mobile apps, messaging platforms and others; the GitHub Copilot harness offers far fewer. Each channel has its own authentication and formatting behaviour, and an agent that looks right in the test pane can render badly in the one people actually use.
- doc | Available channels for agents (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/publication-channels-overview
- doc | Connect and configure an agent for Teams and Microsoft 365 Copilot | https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-add-bot-to-microsoft-teams
- doc | Publish and deploy your agent (channels) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-fundamentals-publish-channels

## share | Sharing & Permissions
Share an agent with users, who can chat with it, ideally through security groups, and decide separately who may edit it — on the GitHub Copilot harness that comes from environment roles, not the share panel. Sharing an agent doesn't automatically share its connections or its knowledge permissions — which is why an agent that works for you can be useless or broken for the first colleague who opens it.
- doc | Share agents with other users and makers (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/authoring-share-agent
- doc | Share agents with other users | https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-share-bots

## analytics | Analytics Basics
Analytics show how the agent is used: sessions and users, success and failure, reactions, tool usage, credits and transcripts — with resolution, satisfaction and themes on the standard harness. Use them to decide what to improve next, and to find the questions your evaluation set does not contain.
- doc | Monitor agent performance overview (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/analytics-overview
- doc | Monitor overview (analytics) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-overview
- video | How To View Conversation Transcripts In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=uPWyhoRqo-0

# the-six-skills | The Six-Skill Toolchain
The toolchain the guided build runs on, documented as a toolchain. This is the module to search when you want to know what one of the six does; the build route itself is the next module.

## sixoverview | The Six Skills as One Toolchain
The six `copilot-*` skills are not six lessons and not six features — they are one route for building a single agent, with each skill owning one stage of it. A router places you at the right stage and applies everything at the end; a design interview produces the brief; an instructions writer runs twice, drafting early and revising once tools exist; a tool finder produces the integration plan; a skill creator packages one capability per run; an evaluation creator produces the test set. Knowing which skill owns which stage is how you find the one you need.
- doc | Release v0.3.0 — copilot-studio-skills | https://github.com/matheus-sancha/copilot-studio-skills/releases/tag/v0.3.0
- doc | copilot-studio-skills README (v0.3.0) | https://github.com/matheus-sancha/copilot-studio-skills/blob/v0.3.0/README.md

## installing | Installing and Removing the Toolchain
The toolchain needs an agent on the GitHub Copilot harness, because skills do not exist on the other two. You upload the six the same way you upload any skill, and the one rule that matters is the one people get wrong: these are scaffolding, and no `copilot-*` skill belongs on an agent you publish. Removing them is a step in the build, not tidying up afterwards.
- doc | Add an existing skill to an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-add-existing
- doc | Manage and delete skills in an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-manage
- doc | Agents powered by the GitHub Copilot harness overview | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/overview

## notrunning | Why a New Chat Fixes Most of It
The most useful thing to know about the product, and the reason the route defers every change to the end. A skill you upload does not reach the conversation you are in — so a skill that installed perfectly and one that failed to install look exactly the same until you open a new chat. Saved instructions do the opposite: they land immediately, which is why applying them mid-build would rewrite the agent you are building with. One conversation for the whole build, one new chat before you test.
- doc | Manage and delete skills in an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-manage
- doc | Test your agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-test-bot

# guided-build | The Guided Build
One agent, built end to end against the Technik scenario. Three pages: what you need before you start, the route itself, and what to do when a stage stalls.

## whatyouneed | What You Need Before You Start
An agent on the GitHub Copilot harness in your own developer environment, the six skills uploaded, and Copilot Credits you are allowed to spend — a twenty-five case evaluation run four times is a real cost. More importantly: a real task with a real reader. The build's first stage is a design interview, and it will not move past a slot you cannot answer, so an idea is not enough to start with.
- doc | Harnesses in Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview
- doc | Create a developer environment (Power Apps Developer Plan) | https://learn.microsoft.com/en-us/power-platform/developer/create-developer-environment
- doc | Standard harness licensing (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing

## theroute | The Route, Stage by Stage
The seven stages at a glance: what each one leaves you holding, and which module of this level taught what it assumes. Nothing changes the agent until the last stage, so everything before it is files you keep. The stage-by-stage instructions live in the toolchain itself rather than on this page — one copy of the route, maintained where it is versioned — and this page is the map you read before you follow it, and the one you come back to when you have lost your place.
- doc | copilot-studio-skills README (v0.3.0) | https://github.com/matheus-sancha/copilot-studio-skills/blob/v0.3.0/README.md
- doc | Release v0.3.0 — copilot-studio-skills | https://github.com/matheus-sancha/copilot-studio-skills/releases/tag/v0.3.0

## whenitstalls | When a Stage Stalls
Three things go wrong and none of them is a mistake. A step names a connector your tenant does not have — run the check the plan already told you to run, and follow what it says to do instead. Your result does not match the example — expected, because your brief is not Technik's; judge it against the acceptance test the stage states, not against resemblance to this page. A click path has moved — search the Build tab for the panel name rather than following a stale route.
- doc | Connectors overview | https://learn.microsoft.com/en-us/connectors/overview
- doc | Manage and delete skills in an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-manage
- doc | Error codes reference for agents (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/troubleshooting-error-codes

# snowflake-sql | Snowflake SQL
Reference, not a read-through. Come here when an agent needs governed data and you have to shape it first.

## sfarch | Snowflake Architecture Basics
Snowflake separates storage from compute. You organise data in databases and schemas and run queries on virtual warehouses, which are compute clusters billed by usage. Knowing these basics helps you write efficient queries and understand costs.
- doc | Key concepts and architecture | https://docs.snowflake.com/en/user-guide/intro-key-concepts
- doc | Snowflake in 20 minutes (tutorial) | https://docs.snowflake.com/en/user-guide/tutorials/snowflake-in-20minutes

## sfroles | Roles & Access Control
Snowflake uses role-based access control: privileges go to roles, and roles go to users. Agents, flows and connectors should use dedicated least-privilege roles, never a personal admin role.
- doc | Overview of access control | https://docs.snowflake.com/en/user-guide/security-access-control-overview

## sfselect | Querying Basics
SELECT, FROM, WHERE, ORDER BY and LIMIT are the basics. Select only the columns you need, filter early, and always check row counts before you share results or feed them to an agent.
- doc | SELECT | https://docs.snowflake.com/en/sql-reference/sql/select
- doc | Querying data — SQL command reference | https://docs.snowflake.com/en/sql-reference-commands

## sfjoins | Joins
Joins combine tables on matching keys. Know the difference between INNER and LEFT joins, and watch for many-to-many joins that quietly duplicate rows and inflate totals.
- doc | Working with joins | https://docs.snowflake.com/en/user-guide/querying-joins
- doc | JOIN | https://docs.snowflake.com/en/sql-reference/constructs/join

## sfagg | Aggregation
GROUP BY with COUNT, SUM, AVG, MIN and MAX turns detailed rows into metrics; HAVING filters the grouped results. Most business questions that agents answer end up as an aggregation.
- doc | GROUP BY | https://docs.snowflake.com/en/sql-reference/constructs/group-by
- doc | Aggregate functions | https://docs.snowflake.com/en/sql-reference/functions-aggregation

## sfcte | CTEs & Subqueries
Common table expressions (WITH clauses) break complex queries into named, readable steps. They are easier to review, and easier for GitHub Copilot to explain or change.
- doc | WITH (common table expressions) | https://docs.snowflake.com/en/sql-reference/constructs/with
- doc | Working with subqueries | https://docs.snowflake.com/en/user-guide/querying-subqueries

## sfwindow | Window Functions (Intro)
Window functions such as ROW_NUMBER, RANK and running SUM calculate across related rows without collapsing them. They are how you get "latest record per customer" or running totals, and QUALIFY is how you filter on them.
- doc | Analyzing data with window functions | https://docs.snowflake.com/en/user-guide/functions-window-using
- doc | QUALIFY | https://docs.snowflake.com/en/sql-reference/constructs/qualify

## sfviews | Views for AI Consumption
Give agents clean views with business-friendly column names, clear comments and only the rows and columns they should see. This makes natural-language querying far more accurate than pointing an agent at raw tables.
- doc | Overview of views | https://docs.snowflake.com/en/user-guide/views-introduction
- doc | COMMENT (document tables and columns) | https://docs.snowflake.com/en/sql-reference/sql/comment

## sfconnector | Snowflake Connector in Power Platform
The Snowflake connector lets Power Automate flows and Copilot Studio agents run SQL against Snowflake; Power Apps reads it through virtual tables instead. It authenticates through a Microsoft Entra ID application, either as a service principal or on behalf of each user, so plan which, especially for agents shared with many users.
- doc | Snowflake (Connectors reference) | https://learn.microsoft.com/en-us/connectors/snowflakev2/
- doc | Use connectors in Copilot Studio agents | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-connectors

# automation-and-workflows | Automation & Workflows
Reference, not a read-through. Come here when part of what you are building has to run the same way every time.

## cloudflows | Power Automate Cloud Flows
Cloud flows automate processes with triggers such as a new email, a schedule or a button, followed by actions such as connectors, conditions, loops and expressions. They are the backbone of low-code automation on Power Platform.
- doc | Explore the Power Automate home page | https://learn.microsoft.com/en-us/power-automate/getting-started
- video | Demonstrate the capabilities of Microsoft Power Automate (PL-900 Ep. 6) | https://www.youtube.com/watch?v=TSga2idzOtc
- article | Power Automate coding standards for cloud flows (Matthew Devaney) | https://www.matthewdevaney.com/power-automate-coding-standards-for-cloud-flows/

## agentflows | Agent Flows
Agent flows are deterministic automations built in Copilot Studio, similar to Power Automate. An agent can call one as a tool, with defined inputs and outputs. Use them when a business process must run the same way every time.
- doc | Agent flows overview | https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview
- doc | Add an agent flow as a tool to an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/flow-agent
- video | Add Knowledge To Copilot Studio Using A Flow (Matthew Devaney) | https://www.youtube.com/watch?v=q-6wTZfF2iQ

## workflows | Workflows (New Designer)
Workflows are Copilot Studio's newer automation designer. They include agent nodes that reason at chosen steps, native AI actions and step-level testing. They mix fixed business logic with AI decisions in one place.
- doc | Agent flows overview | https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview
- video | NEW Workflows Feature In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=o532hBhzSoQ
- article | 10 things I love about Copilot Studio workflows (Matthew Devaney) | https://www.matthewdevaney.com/10-things-i-love-about-copilot-studio-workflows/

## aibuilder | AI Builder Overview
AI Builder adds ready-to-use AI to Power Automate and Power Apps: prompts, document processing, text and image models. It uses AI Builder credits, and it's the simplest way to put AI inside an existing flow.
- doc | Overview of AI Builder | https://learn.microsoft.com/en-us/ai-builder/overview
- doc | Licensing and AI Builder credits | https://learn.microsoft.com/en-us/ai-builder/credit-management

## prompts | AI Builder Prompts
Prompts are reusable, parameterised instructions to a model that return text or JSON. Structured JSON output is what lets the rest of a flow use the answer reliably, rather than parsing prose. Use them in flows through the "Run a prompt" action; they replace the deprecated "Create text with GPT" action.
- doc | Prompts overview | https://learn.microsoft.com/en-us/microsoft-copilot-studio/prompts-overview
- doc | Use the text generation model in Power Automate (deprecated) | https://learn.microsoft.com/en-us/ai-builder/azure-openai-model-pauto
- article | Power Automate: perform an AI prompt on a PDF document (Matthew Devaney) | https://www.matthewdevaney.com/power-automate-perform-an-ai-prompt-on-a-pdf-document/

## docproc | Document Processing
AI Builder document processing pulls fields and tables out of invoices, receipts, IDs and custom forms. Combine it with validation and a human review step before the data reaches business systems.
- doc | Invoice processing prebuilt AI model | https://learn.microsoft.com/en-us/ai-builder/prebuilt-invoice-processing
- article | Extract invoice details with Power Automate and AI Builder (Matthew Devaney) | https://www.matthewdevaney.com/extract-invoice-details-with-power-automate-and-ai-builder/

## approvals | Approvals in Flows
The Approvals connector sends approval requests to Teams, Outlook or the Power Automate portal and waits for a response. It is the standard way to put a named human in the loop of an automated or agent-driven process.
- doc | Get started with Power Automate approvals | https://learn.microsoft.com/en-us/power-automate/get-started-approvals
- article | Easiest Power Automate sequential approval flow pattern (Matthew Devaney) | https://www.matthewdevaney.com/easiest-power-automate-sequential-approval-flow-pattern/

## topicsvsflows | Topics vs. Flows vs. Agents
- **Topics** handle scripted conversations.
- **Flows and workflows** handle business processes that must run reliably, often without a user present.
- **Agents** handle open-ended requests that need judgement.

Real solutions combine all three.
- doc | Agent flows in Microsoft Copilot Studio FAQ — topics vs. agent flows | https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-faqs

# next-steps | Finishing Intermediate
What this level qualified you to do, and what Advanced assumes you can already do without help.

## checkpoint | Intermediate Checkpoint
You have built an agent end to end: designed from a brief, instructed in a structured format, grounded in knowledge, given tools, packaged with a skill, evaluated against a real test set and published to a channel. Before you start Advanced, you should be able to do all of this without a guide:
- fill a brief that will not stall a design interview
- write XML-structured instructions and say which section a line belongs in
- decide whether a requirement is instructions, knowledge, a tool or a skill
- author and package a skill, and diagnose one that never fires
- add a connector and an MCP server, and explain who the connection runs as
- write an evaluation set that can fail, and read the results without trusting the percentage
- publish into a solution and an environment you did not build in
- doc | Study guide for Exam AB-620: Designing and Building Integrated AI Solutions in Copilot Studio | https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ab-620
- course | Create agents in Microsoft Copilot Studio (learning path) | https://learn.microsoft.com/en-us/training/paths/create-extend-custom-copilots-microsoft-copilot-studio/
