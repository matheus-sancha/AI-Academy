---
id: beginner
order: 1
title: AI Engineering on Microsoft
subtitle: Beginner Roadmap
tagline: For engineers new to AI — concepts plus low-code building with Copilot, Copilot Studio, Power Platform and Snowflake.
next: advanced.html
next_label: Continue to the Advanced roadmap
continues: yes
audience: Engineers new to AI
card: LLM fundamentals, XML prompt engineering, Microsoft 365 Copilot, Copilot Studio agents, knowledge & RAG, tools, connectors, MCP, skills, Power Automate with AI Builder, SQL in Snowflake, moderation, publishing and evaluation.
---

# B0 | Getting Oriented
Understand the role, the Microsoft AI landscape and what you need before you start building.

## role | The AI Engineer Role
An AI engineer builds solutions on top of pre-trained models and platforms instead of training models from scratch. The job is to combine models, prompts, data, tools and automation into reliable products, and to measure and govern them. This is different from a data scientist or ML engineer, who mainly create and train models.
- video | Introduction to generative AI and agents (AI-901, Microsoft Learn) | https://www.youtube.com/watch?v=ksNWjglbKeg
- course | Introduction to AI concepts (Microsoft Learn training) | https://learn.microsoft.com/en-us/training/modules/get-started-ai-fundamentals/
- doc | Study guide AB-100: Agentic AI Business Solutions Architect | https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ab-100

## stack | The Microsoft AI Stack Map
Microsoft offers several places to build with AI. Microsoft 365 Copilot and Agent Builder serve end users. Copilot Studio is the low-code agent platform, and Power Platform adds automation and data. GitHub Copilot and VS Code are for developers, and Microsoft Foundry is for pro-code models and agents. In this program Snowflake is the governed data platform that agents query. Knowing which tool fits which job avoids rebuilding the same thing twice.
- doc | Choose between Agent Builder and Copilot Studio | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/copilot-studio-experience
- doc | Agents for Microsoft 365 Copilot overview | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agents-overview
- video | Choose a Microsoft 365 Copilot extensibility development path (MS-4010) | https://www.youtube.com/watch?v=ARPj2XpkCpU

## licensing | Licensing & Copilot Credits
Microsoft AI products mix per-user licences (e.g., Microsoft 365 Copilot, GitHub Copilot) with consumption billing (Copilot Credits for Copilot Studio, AI Builder credits). Building, testing and evaluating agents can consume credits, so understand what your environment is billed on before you run large tests.
- doc | Standard harness licensing (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing
- doc | Manage Copilot Credits and capacity | https://learn.microsoft.com/en-us/power-platform/admin/manage-copilot-studio-copilot-credits-capacity
- doc | AI Builder licensing and credits | https://learn.microsoft.com/en-us/ai-builder/credit-management

## devenv | Your Developer Environment
Every engineer should build in their own Power Platform developer environment, never directly in production. Pair it with Copilot Studio access, VS Code with GitHub Copilot, and Snowflake access through your own development role. Agents and connectors you build should never use that role: give them a separate, read-only one.
- doc | Create a developer environment (Power Apps Developer Plan) | https://learn.microsoft.com/en-us/power-platform/developer/create-developer-environment
- doc | Power Apps Developer Plan | https://learn.microsoft.com/en-us/power-platform/developer/plan
- article | 7 mistakes to avoid when creating a Power Platform environment (Matthew Devaney) | https://www.matthewdevaney.com/7-mistakes-to-avoid-when-creating-a-power-platform-environment/

# B1 | LLM Fundamentals
The core ideas behind large language models that every other topic depends on.

## llm | What Is an LLM
A large language model is a neural network trained on huge amounts of text to predict the next token in a sequence. By repeatedly predicting next tokens it can answer questions, summarise, write code and follow instructions. Its output depends on its input and some randomness, so the same prompt can give different answers.
- doc | LLM fundamentals (Microsoft Agent Framework learning journey) | https://learn.microsoft.com/en-us/agent-framework/journey/llm-fundamentals
- doc | How generative AI and LLMs work (.NET AI docs) | https://learn.microsoft.com/en-us/dotnet/ai/conceptual/how-genai-and-llms-work
- video | Introduction to AI concepts (AI-901) | https://www.youtube.com/watch?v=-MkEEXFODZU

## tokens | Tokens
Models don't read words; they read tokens — chunks of text that are often parts of words. In English one token is roughly four characters or about ¾ of a word. Tokens drive three things you care about: cost, speed and how much fits in a request.
- doc | Understand tokens | https://learn.microsoft.com/en-us/dotnet/ai/conceptual/understanding-tokens
- video | Why your AI costs spike (tokens explained) — Microsoft Learn | https://www.youtube.com/watch?v=NmkR7V_wTqA

## context | Context & Context Window
The context is everything the model sees in one request: instructions, conversation history, retrieved knowledge, tool results and the user's message. The context window is the maximum number of tokens that fits, covering both input and output. When the window fills up, content has to be dropped or summarised, and quality can fall before you reach the limit.
- doc | Understand tokens — context window and token limits | https://learn.microsoft.com/en-us/dotnet/ai/conceptual/understanding-tokens
- doc | Prompt engineering techniques (Microsoft Foundry) | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering

## inference | Inference
Inference is the act of running a trained model to produce output. Your request is tokenised and processed by the model, and a response is generated one token at a time, often streamed back. Latency depends on the model's size, how long your input is and how much it generates.
- doc | LLM fundamentals — how models generate responses | https://learn.microsoft.com/en-us/agent-framework/journey/llm-fundamentals
- video | Select, deploy, and evaluate Microsoft Foundry models (AI-103) | https://www.youtube.com/watch?v=71gi8ULxPZQ

## temperature | Temperature & Sampling
Temperature controls how random the next-token choice is. Low values (≈0–0.3) give focused, repeatable answers. Higher values give more varied, creative text. Top-p is a related setting. In Copilot Studio you mostly control this through prompt/model settings, and many reasoning models ignore temperature entirely.
- doc | Change the model version and settings for prompts (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/prompt-model-settings
- doc | Prompt engineering techniques — temperature and top_p | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering

## training | Training vs. Fine-Tuning (Concepts)
Pre-training teaches a model general language from massive datasets; instruction tuning teaches it to follow requests. Fine-tuning further trains an existing model on your examples to specialise it. As a beginner, know the vocabulary: most business problems are solved with prompting and grounding, not training.
- doc | Getting started with customizing an LLM | https://learn.microsoft.com/en-us/azure/foundry-classic/openai/concepts/customizing-llms
- video | Compare model optimization strategies (AI-3016) | https://www.youtube.com/watch?v=SkGItraTlHc

## hallucination | Hallucinations & Grounding
LLMs can produce confident, fluent answers that are wrong ("hallucinations") because they generate plausible text, not verified facts. Grounding is the main fix: supplying trusted content in the context and instructing the model to answer only from it, with citations.
- doc | Groundedness detection (Azure AI Content Safety) | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/groundedness
- doc | Retrieval-augmented generation (.NET AI docs) | https://learn.microsoft.com/en-us/dotnet/ai/conceptual/rag

## models | Choosing a Model
Different models trade quality, speed, cost and reasoning depth. Copilot Studio lets you pick the primary model for an agent, including OpenAI GPT and Anthropic Claude models. Reasoning models think longer for complex tasks; chat models are faster for simple ones.
- doc | Select a primary AI model for your agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-select-agent-model
- doc | Anthropic models in Microsoft Online Services | https://learn.microsoft.com/en-us/microsoft-365/copilot/connect-to-ai-subprocessor
- video | SLMs vs. LLMs (Microsoft Learn) | https://www.youtube.com/watch?v=ShMTL5avG40

## multimodal | Multimodal Models | opt
Multimodal models accept or produce more than text: images, documents, audio or voice. They let agents read screenshots, analyse PDFs or hold voice conversations. Treat these as extensions of the same prompt-and-context ideas.
- doc | Vision prompt engineering techniques | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/gpt-4-v-prompt-engineering
- video | Develop a vision-enabled generative AI application (AI-103) | https://www.youtube.com/watch?v=Xlo-VDqYrz4

# B2 | Prompt Engineering
Write instructions that make models behave predictably — the skill you'll use in every Microsoft tool.

## anatomy | Anatomy of a Prompt
A prompt usually has three layers. System or agent instructions set who the model is and its rules. Context is the data it should use. The user message is the actual request. Keeping these layers separate makes prompts easier to debug and safer against injected instructions.
- doc | System message design | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/advanced-prompt-engineering
- course | Understanding prompt engineering fundamentals (Generative AI for Beginners) | https://learn.microsoft.com/en-us/shows/generative-ai-for-beginners/understanding-prompt-engineering-fundamentals-generative-ai-for-beginners

## clarity | Clarity & Specificity
Vague prompts get vague answers. State the role, the task, the audience, constraints (length, tone, what not to do), and what a good result looks like. Microsoft's guidance: be specific and leave as little to interpretation as possible.
- doc | Prompt engineering techniques (Microsoft Foundry) | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering
- course | Write effective prompts (Microsoft Learn training) | https://learn.microsoft.com/en-us/training/modules/write-effective-prompts-do-more-prompting/
- video | Better prompts = better AI (Microsoft Learn) | https://www.youtube.com/watch?v=k4geocw07nc

## xml | Structuring Prompts with XML Tags
XML-style tags such as `<instructions>`, `<context>`, `<examples>` and `<output_format>` split a prompt into clear sections. They show the model where data starts and stops, which helps it tell instructions apart from content. This team standard works in Copilot Studio instructions, AI Builder prompts and GitHub Copilot.
- doc | Prompt engineering techniques — use clear syntax and delimiters | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering
- doc | RAG prompt engineering — separating sources with delimiters | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-prompt-engineering

## fewshot | Few-Shot Examples
Showing the model one or more input → output examples ("few-shot") is often more effective than describing the format in words. Keep examples short, realistic and consistent with the output you want.
- doc | Prompt engineering techniques — few-shot learning | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering
- doc | Prompt engineering concepts (.NET) | https://learn.microsoft.com/en-us/dotnet/ai/conceptual/prompt-engineering-dotnet

## output | Output Formats
Say exactly how you want the answer shaped: bullet list, table, Markdown, or JSON with named fields. Structured output is what lets flows and tools use the response reliably. Copilot Studio and AI Builder prompts can return JSON directly.
- doc | Prompts overview — JSON output | https://learn.microsoft.com/en-us/microsoft-copilot-studio/prompts-overview
- doc | Prompt engineering techniques — specify output structure | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering

## decompose | Breaking Down Tasks
Models do better when a complex task is split into ordered steps: extract facts first, then analyse, then write. You can do this inside one prompt, or chain several prompts, which is a first step towards workflows and agents.
- doc | Prompt engineering techniques — break the task down | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering

## iterate | Iterating on Prompts
Prompting is experimental: write a prompt, test it on several realistic inputs, compare the results and refine. Save good prompts in a shared library. In Copilot Studio the prompt editor lets you test prompts and change the model before you use them in agents and flows.
- doc | Prompts overview — create and test prompts | https://learn.microsoft.com/en-us/microsoft-copilot-studio/prompts-overview
- video | Master Copilot Studio Prompts with Azure AI Foundry Models (Matthew Devaney) | https://www.youtube.com/watch?v=ShphK8L3y2Y

## writinginstructions | Writing Agent Instructions
Agent instructions are a long-lived system prompt. They define identity, scope, tone, which knowledge or tools to use and when, and what to refuse or escalate. Good instructions are specific and structured, and they are tested against real questions.
- doc | Write effective instructions for declarative agents | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-instructions
- video | Build effective agents in Microsoft Copilot Studio (PL-7008 Ep. 4) | https://www.youtube.com/watch?v=VV-lSSPQwW4

# B3 | Using AI Assistants
Become a strong user of Microsoft's Copilots before building your own agents.

## m365chat | Microsoft 365 Copilot Chat
Microsoft 365 Copilot Chat is the everyday AI assistant in Teams, Outlook, Word, Excel and the browser. It can ground answers in the web or, with a Microsoft 365 Copilot licence, in your work data. Using it well teaches you what users expect from agents.
- doc | Microsoft 365 Copilot documentation hub | https://learn.microsoft.com/en-us/microsoft-365/copilot/
- video | Explore Microsoft 365 Copilot Chat (MS-4023) | https://www.youtube.com/watch?v=jdwx6ztuJpE
- course | Write effective prompts for Microsoft 365 Copilot | https://learn.microsoft.com/en-us/training/modules/write-effective-prompts-do-more-prompting/

## agentbuilder | Agent Builder in Microsoft 365 Copilot
Agent Builder creates simple declarative agents inside Microsoft 365 Copilot in plain language: you give it instructions, knowledge such as SharePoint or files, and a few capabilities. It's the fastest route for personal or team agents. Move to Copilot Studio when you need workflows, connectors or wider publishing.
- doc | Agent Builder in Microsoft 365 Copilot | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder
- course | Build agents in Copilot Chat (online workshop) | https://learn.microsoft.com/en-us/training/modules/agents-copilot-chat/
- doc | Share and manage Agent Builder agents | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-share-manage-agents

## usingagents | Using Copilot Studio Agents
Published Copilot Studio agents show up where people already work: Teams, Microsoft 365 Copilot, websites and other channels. Try agents as an end user so you learn how discovery, sign-in, citations and handoffs feel from the other side.
- doc | Connect an agent to Teams and Microsoft 365 Copilot | https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-add-bot-to-microsoft-teams
- video | Deploy an agent to Teams (PL-7008 Ep. 6) | https://www.youtube.com/watch?v=aW2e4_EoDxs

## ghcopilot | GitHub Copilot in VS Code
GitHub Copilot is an AI pair programmer in VS Code. It offers inline completions, chat, and agent mode, which can edit several files and run commands. Engineers use it to write SQL, Power Fx, scripts and MCP servers faster, and to review what the AI produced.
- doc | Build with agents in VS Code (GitHub Copilot) | https://code.visualstudio.com/docs/agents/overview
- video | Get started with GitHub Copilot (AZ-2007 Ep. 1) | https://www.youtube.com/watch?v=7FDrdrGQ1Oc
- course | Get started with AI-assisted development (learning path) | https://learn.microsoft.com/en-us/training/paths/accelerate-app-development-using-github-copilot/

## custominstr | GitHub Copilot Custom Instructions | opt
A `.github/copilot-instructions.md` file gives GitHub Copilot standing context about your repository: conventions, tools and rules. It is your first taste of context engineering, which the Advanced roadmap covers in depth.
- doc | Custom instructions in VS Code | https://code.visualstudio.com/docs/agent-customization/custom-instructions
- video | Mastering Prompt Engineering with GitHub Copilot (Microsoft Learn) | https://www.youtube.com/watch?v=nWJW1cDptH4

# B4 | Agent Fundamentals
What makes something an agent, and how Copilot Studio runs agents.

## agent | What Is an Agent
An agent combines a model, instructions, knowledge and tools with a loop that decides what to do next. It can answer questions, take actions such as creating a ticket or running a flow, and work through tasks in several steps. Chatbots follow scripts; agents choose their next step within the limits you set.
- doc | Agents for Microsoft 365 Copilot overview | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agents-overview
- video | Stop building chatbots. Build AI agents. (Microsoft Learn) | https://www.youtube.com/watch?v=GMstvVqy6EI
- video | Get started with generative AI and agents in Azure (AI-901) | https://www.youtube.com/watch?v=nw8yN8Nhgfc

## autonomous | Conversational vs. Autonomous Agents
Conversational agents respond when a user chats with them. Autonomous agents start from events instead, such as a new email, a new file or a schedule, and run without anyone chatting. Autonomous agents need tighter instructions, limits and monitoring.
- doc | Add an event trigger (autonomous agents) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-trigger-event
- video | Introduction to autonomous agents (PL-7008 Ep. 7) | https://www.youtube.com/watch?v=wvtLiylvkK8
- video | Incredible Excel-Writing Autonomous Agent In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=vd5DLiu1_6Y

## orchestration | Orchestration
Orchestration decides how an agent handles a request: which knowledge to search, which tool or topic to call, what to ask the user, and how to combine the results. Generative orchestration uses the model to choose from the descriptions you write, which is why names and descriptions matter so much.
- doc | Orchestrate agent behavior with generative AI | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions
- video | Copilot Studio: How I Built A Generative Orchestration Agent (Matthew Devaney) | https://www.youtube.com/watch?v=QTuuoUg8Hpg
- article | How to build a Copilot Studio agent with generative orchestration (Matthew Devaney) | https://www.matthewdevaney.com/how-to-build-a-copilot-studio-agent-with-generative-orchestration/

## harness | What Is a Harness
A harness is the runtime that sits between what you build and the model. It decides when to call the model, what to send it, how to read the reply and which tools to run. The same model can behave very differently in different harnesses.
- doc | Harnesses in Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview

## chooseharness | Choosing a Harness in Copilot Studio
Copilot Studio offers three harnesses:
- **GitHub Copilot harness:** reasoning-heavy, multi-step work with skills, memory and files.
- **Standard harness:** rule-based agents with topics and agent flows.
- **Copilot chat harness:** extends Microsoft 365 Copilot Chat with enterprise knowledge.

You choose when you create an agent, and you can't switch it later.
- doc | Harnesses in Copilot Studio — compare harnesses | https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview
- doc | Agents powered by the GitHub Copilot harness overview | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/overview
- video | The FUTURE of Copilot Studio is HERE (Matthew Devaney) | https://www.youtube.com/watch?v=aX4bcDPTmPY

## hitl | Human-in-the-Loop
Some actions shouldn't happen without a person: approving spend, sending external emails, changing records. Design explicit confirmations, approvals and escalation to a human. This matters most for autonomous agents.
- doc | Agent flows overview — approvals and human review | https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview
- doc | Get started with Power Automate approvals | https://learn.microsoft.com/en-us/power-automate/get-started-approvals

# B5 | Copilot Studio Basics
Build, configure and test your first agents.

## tour | Copilot Studio Tour
Copilot Studio is Microsoft's low-code platform for building agents and agent workflows. The main areas are:
- **Build or overview:** instructions, knowledge, tools, skills
- **Topics:** standard harness only
- **Preview and test**
- **Evaluate**
- **Publish and channels**
- **Analytics and monitoring**
- doc | Copilot Studio overview | https://learn.microsoft.com/en-us/microsoft-copilot-studio/fundamentals-what-is-copilot-studio
- course | Create agents in Microsoft Copilot Studio (learning path) | https://learn.microsoft.com/en-us/training/paths/create-extend-custom-copilots-microsoft-copilot-studio/
- video | Build an initial agent with Microsoft Copilot Studio (PL-7008 Ep. 1) | https://www.youtube.com/watch?v=hzN2-K-8PP0

## create | Create Your First Agent
Start by describing the agent in natural language. Copilot Studio drafts the name, description and instructions for you. Then refine them, add one knowledge source, test in the preview pane, and only add tools once the basic answers are good.
- doc | Create and delete agents | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-first-bot
- course | Get started with Microsoft Copilot Studio (training module) | https://learn.microsoft.com/en-us/training/modules/power-virtual-agents-bots/

## instructions | Instructions
Instructions tell the agent who it is, what it covers, how to respond and what it must never do. With generative orchestration they also guide which knowledge and tools it uses, so write them like an XML-structured system prompt and keep them focused.
- doc | Configure agent details and instructions (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/authoring-instructions
- doc | Orchestrate agent behavior with generative AI — instructions | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions

## model | Model Selection
Each agent has a primary model, and you can change it to trade speed, cost and reasoning ability. Retest with your evaluation set after you change models, because behaviour shifts even when your instructions stay the same.
- doc | Select a primary AI model for your agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-select-agent-model
- doc | Select a model (GitHub Copilot harness) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/authoring-select-agent-model

## topics | Topics & Trigger Phrases
In the standard harness, topics are conversation paths you design node by node. They start from trigger phrases or from orchestration and use messages, questions, conditions and actions. Use topics when a conversation must follow exact, predictable steps, such as a compliance check.
- doc | Create and edit topics | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-create-edit-topics
- video | Manage topics in Microsoft Copilot Studio (PL-7008 Ep. 2) | https://www.youtube.com/watch?v=IOXMxuL9NrI
- video | Question Nodes vs Topic Inputs In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=c9IaXLj0NMc

## variables | Variables & Power Fx Basics
Variables store information during a conversation. Topic variables stay inside one topic; global variables are shared across the agent. Power Fx is the Excel-like formula language you use to transform values, build conditions and format output.
- doc | Work with variables | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-variables
- doc | Create expressions using Power Fx | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-power-fx
- video | Work with entities and variables (PL-7008 Ep. 3) | https://www.youtube.com/watch?v=YANyM1hWxlo

## genai | Generative AI Settings
Agent-level settings control generative orchestration, whether the model may use its general knowledge, how strict content moderation is, and how responses are formatted. Review these settings on every new agent; the defaults aren't always right for your case.
- doc | Orchestrate agent behavior with generative AI | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions
- doc | FAQ for generative answers (moderation settings) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/faqs-generative-answers

## test | Testing in the Preview Pane
The test or preview pane lets you chat with your draft agent and watch what it did. The activity map shows which knowledge, tools and topics it used and why. Use it to diagnose bad answers before you blame the model.
- doc | Test your agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-test-bot
- video | How To View Conversation Transcripts In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=uPWyhoRqo-0

# B6 | Knowledge & RAG
Ground agents in your organisation's content so answers are accurate and cited.

## rag | What Is RAG
Retrieval-augmented generation (RAG) finds the most relevant pieces of your content for a question and adds them to the model's context. The model then writes an answer grounded in that content. It is how agents answer from company data without being retrained.
- doc | Retrieval-augmented generation in Azure AI Search | https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview
- video | Understand Retrieval Augmented Generation (RAG) with Azure OpenAI (Microsoft Learn) | https://www.youtube.com/watch?v=loHvK_bXuYE

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
- video | Build Agents With SharePoint List Knowledge (Matthew Devaney) | https://www.youtube.com/watch?v=BUM4gUc8QUM

## connectorknowledge | Copilot Connectors vs. Power Platform Connectors
Copilot connectors (formerly Graph connectors) index external content into Microsoft 365 ahead of time. Power Platform connectors used as knowledge query the source system live, with each user's own permissions. Pick based on how fresh the data must be and whose permissions apply.
- doc | Copilot connectors versus Power Platform connectors as knowledge | https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-graph-vs-power-platform-connectors
- doc | Add Power Platform connectors as knowledge | https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-real-time-connectors

## snowflakeknowledge | Snowflake as a Knowledge Source
You can add selected Snowflake tables as a knowledge source in Copilot Studio. The agent turns natural-language questions into queries, so makers don't write SQL, and the data stays in Snowflake. Clean, well-named, documented tables and views give much better answers.
- doc | Add Power Platform connectors (incl. Snowflake) as knowledge | https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-real-time-connectors
- doc | Snowflake connector reference | https://learn.microsoft.com/en-us/connectors/snowflakev2/

## citations | Citations & Answer Quality
Citations let users check where an answer came from, and they build trust. When knowledge returns nothing, the cause is usually one of these:
- permissions
- the source hasn't finished indexing
- the file is too large or in an unsupported format
- the question doesn't match the content
- doc | Generative answers with SharePoint don't return results | https://learn.microsoft.com/en-us/troubleshoot/power-platform/copilot-studio/knowledge/sharepoint-no-response
- article | Set citation to open a specific PDF page in Copilot Studio (Matthew Devaney) | https://www.matthewdevaney.com/set-citation-to-open-specific-pdf-page-in-copilot-studio/

## workiq | Work IQ & Foundry IQ | opt, prev
Work IQ gives agents organisational context such as email, calendar, files, Teams messages and people. Foundry IQ gives agents ready-made knowledge bases from Microsoft Foundry. Learn what they are for now; the Advanced roadmap covers using them.
- doc | Work IQ overview | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/
- doc | What is Foundry IQ? | https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq
- video | Work IQ is the layer that makes AI feel personal (Microsoft Learn) | https://www.youtube.com/watch?v=nQ74VnmQIqY
- video | Foundry IQ: the future of RAG with knowledge retrieval (Microsoft Learn) | https://www.youtube.com/watch?v=h1n19QCPc1I

# B7 | Tools, Connectors & MCP
Let agents act: call systems, run automations and use external tools.

## tools | What Are Tools
Tools are how agents do things rather than just talk. Examples include connector actions, agent flows, prompts, REST APIs, MCP servers and computer use. The orchestrator picks a tool from its name, description and inputs, so write those as carefully as your instructions.
- doc | Add tools to custom agents | https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-tools-custom-agent
- doc | Add an agent flow as a tool to an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/flow-agent

## connectors | Power Platform Connectors
Connectors are prebuilt wrappers around APIs, such as Outlook, SharePoint, Dataverse, ServiceNow and Snowflake. They expose actions and triggers that Power Automate, Power Apps and Copilot Studio can all use. More than 1,000 exist, and custom connectors fill the gaps.
- doc | Connectors overview | https://learn.microsoft.com/en-us/connectors/overview
- doc | Use connectors in Copilot Studio agents | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-connectors

## connauth | Connections & Authentication
A connection holds the credentials a connector uses. It can run as the end user, with the user's own permissions, or as the maker or a service account. This choice decides what data users can reach through your agent, and it often breaks agents once they are shared.
- doc | Use connectors in Copilot Studio agents — authentication | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-connectors
- article | Power Automate standards: connection references (Matthew Devaney) | https://www.matthewdevaney.com/power-automate-coding-standards-for-cloud-flows/power-automate-standards-connection-references/

## addconnector | Adding a Connector Tool to an Agent
Add a connector action as a tool, set which inputs the agent fills in and which stay fixed, and give it a clear description. Then test that the orchestrator calls it at the right moment with the right values.
- doc | Use connectors in Copilot Studio agents | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-connectors
- video | Copilot Studio: ServiceNow Connect Knowledge Base + Helpdesk Tickets (Matthew Devaney) | https://www.youtube.com/watch?v=LpRdT49U9Cw

## mcp | What Is MCP
The Model Context Protocol (MCP) is an open standard for connecting AI applications to tools and data, often compared to "USB-C for AI". An MCP server exposes tools, and any MCP-capable client can use them: Copilot Studio, GitHub Copilot or Snowflake.
- doc | Model Context Protocol — introduction | https://modelcontextprotocol.io/docs/getting-started/intro
- doc | Extend your agent with Model Context Protocol | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp

## mcpadd | Adding an Existing MCP Server to an Agent
In Copilot Studio you can add an existing MCP server as a tool. Its tools, and any updates to them, flow into your agent automatically. Prefer certified or internally approved servers, and check what each tool can do before you enable it.
- doc | Connect your agent to an existing MCP server | https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent
- video | Integrate MCP tools with Azure AI agents (AI-103 Ep. 9) | https://www.youtube.com/watch?v=pQ9yEEcXNeE

## connected | Connected & Child Agents
Large agents are hard to maintain. Split specialised jobs into child agents inside the same agent, or into connected agents that run on their own. The main agent hands tasks to them, the way a team lead delegates to specialists.
- doc | Add other agents (connected and child agents) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-add-other-agents
- video | Master Multi-Agent Orchestration In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=xtPlDde4Yv0

## computeruse | Computer Use | opt
Computer use lets an agent work websites and desktop apps the way a person does: clicking, typing and reading the screen. It is useful for systems without an API. It is slower and more fragile than connectors, so treat it as a last resort.
- doc | Automate web and desktop apps with computer use | https://learn.microsoft.com/en-us/microsoft-copilot-studio/computer-use
- video | Computer Use Agent: Extract Web Page Data In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=isClxl1O_Zs

# B8 | Skills
Package reusable agent behaviours and use them across agents.

## skill | What Is a Skill
A skill is a reusable capability. It has a name, a description and Markdown instructions, and can include extra files. The orchestrator loads it only when a request matches the description. Skills keep agents smaller and let teams share proven behaviours.
- doc | Skills overview for agents (Copilot Studio) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-overview
- video | How To Create Agent Skills In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=BvDGMw_7sbk

## skillsvs | Skills vs. Topics vs. Tools
- **Tools** perform an action.
- **Skills** hold reusable know-how about how to carry out a kind of task.
- **Topics** are scripted conversation paths in the standard harness.

A skill may use several tools; a topic fixes the exact steps.
- doc | Skills overview — skills, tools and orchestration | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-overview
- article | How to create agent skills in Copilot Studio (Matthew Devaney) | https://www.matthewdevaney.com/how-to-create-agent-skills-in-copilot-studio/

## addskill | Add an Existing Skill
You can add a ready-made skill by uploading a `SKILL.md` file or a packaged skill bundle. It uses the same open Agent Skills format as GitHub Copilot, so a skill written once can be reused.
- doc | Add an existing skill to an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-add-existing

## createskill | Create a Simple Skill
Create a skill from blank with a clear name, a description of when to use it, and step-by-step instructions. The description decides whether the skill ever triggers, so test it with questions that should and shouldn't activate it.
- doc | Create a skill for an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-create
- video | How To Create Agent Skills In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=BvDGMw_7sbk

## reuse | Reuse in the Standard Harness
Standard-harness agents don't support skills. Reuse behaviour through shared topics, tools, child agents and component collections instead. Pick the pattern that fits your harness rather than forcing one design on both.
- doc | Create and manage component collections | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-export-import-copilot-components
- doc | Add other agents (child agents) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-add-other-agents

# B9 | Workflows & Power Automate with AI Builder
Automate business processes and put AI inside them.

## cloudflows | Power Automate Cloud Flows
Cloud flows automate processes with triggers such as a new email, a schedule or a button, followed by actions such as connectors, conditions, loops and expressions. They are the backbone of low-code automation on Power Platform.
- doc | Get started with Power Automate | https://learn.microsoft.com/en-us/power-automate/getting-started
- video | Demonstrate the capabilities of Microsoft Power Automate (PL-900 Ep. 6) | https://www.youtube.com/watch?v=TSga2idzOtc
- article | Power Automate coding standards for cloud flows (Matthew Devaney) | https://www.matthewdevaney.com/power-automate-coding-standards-for-cloud-flows/

## agentflows | Agent Flows
Agent flows are deterministic automations built in Copilot Studio, similar to Power Automate. An agent can call one as a tool, with defined inputs and outputs. Use them when a business process must run the same way every time.
- doc | Agent flows overview | https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview
- doc | Add an agent flow as a tool to an agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/flow-agent
- video | Add Knowledge To Copilot Studio Using A Flow (Matthew Devaney) | https://www.youtube.com/watch?v=q-6wTZfF2iQ

## workflows | Workflows (New Designer)
Workflows are Copilot Studio's newer automation designer. They include agent nodes that reason at chosen steps, native AI actions and step-level testing. They mix fixed business logic with AI decisions in one place.
- doc | Agent flows and workflows overview | https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview
- video | NEW Workflows Feature In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=o532hBhzSoQ
- article | 10 things I love about Copilot Studio workflows (Matthew Devaney) | https://www.matthewdevaney.com/10-things-i-love-about-copilot-studio-workflows/

## aibuilder | AI Builder Overview
AI Builder adds ready-to-use AI to Power Automate and Power Apps: prompts, document processing, text and image models. It uses AI Builder credits, and it's the simplest way to put AI inside an existing flow.
- doc | AI Builder overview | https://learn.microsoft.com/en-us/ai-builder/overview
- doc | Licensing and AI Builder credits | https://learn.microsoft.com/en-us/ai-builder/credit-management

## prompts | AI Builder Prompts
Prompts are reusable, parameterised instructions to a model that return text or JSON. Use them in flows through the "Run a prompt" / "Create text using a prompt" action. They replace the deprecated "Create text with GPT" action.
- doc | Prompts overview | https://learn.microsoft.com/en-us/microsoft-copilot-studio/prompts-overview
- doc | Text generation with GPT (deprecated — migration guidance) | https://learn.microsoft.com/en-us/ai-builder/azure-openai-model-pauto
- article | Power Automate: perform an AI prompt on a PDF document (Matthew Devaney) | https://www.matthewdevaney.com/power-automate-perform-an-ai-prompt-on-a-pdf-document/

## docproc | Document Processing
AI Builder document processing pulls fields and tables out of invoices, receipts, IDs and custom forms. Combine it with validation and a human review step before the data reaches business systems.
- doc | Invoice processing prebuilt model | https://learn.microsoft.com/en-us/ai-builder/prebuilt-invoice-processing
- article | Extract invoice details with Power Automate and AI Builder (Matthew Devaney) | https://www.matthewdevaney.com/extract-invoice-details-with-power-automate-and-ai-builder/

## approvals | Approvals in Flows
The Approvals connector sends approval requests to Teams, Outlook or the Power Automate portal and waits for a response. It is the standard way to add human-in-the-loop checks to automated and agent-driven processes.
- doc | Get started with approvals | https://learn.microsoft.com/en-us/power-automate/get-started-approvals
- article | Easiest Power Automate sequential approval flow pattern (Matthew Devaney) | https://www.matthewdevaney.com/easiest-power-automate-sequential-approval-flow-pattern/

## topicsvsflows | Topics vs. Flows vs. Agents
- **Topics** handle scripted conversations.
- **Flows and workflows** handle business processes that must run reliably, often without a user present.
- **Agents** handle open-ended requests that need judgement.

Real solutions combine all three.
- doc | Agent flows FAQ — topics vs. agent flows | https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-faqs

# B10 | Data: SQL in Snowflake
Query and prepare governed data that agents and flows can use.

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
Window functions such as ROW_NUMBER, RANK and running SUM calculate across related rows without collapsing them. They are how you get "latest record per customer" or running totals.
- doc | Analyzing data with window functions | https://docs.snowflake.com/en/user-guide/functions-window-using

## sfviews | Views for AI Consumption
Give agents clean views with business-friendly column names, clear comments and only the rows and columns they should see. This makes natural-language querying far more accurate than pointing an agent at raw tables.
- doc | Overview of views | https://docs.snowflake.com/en/user-guide/views-introduction
- doc | COMMENT (document tables and columns) | https://docs.snowflake.com/en/sql-reference/sql/comment

## sfconnector | Snowflake Connector in Power Platform
The Snowflake connector lets Power Automate flows, Power Apps and Copilot Studio agents run queries against Snowflake. Plan how it authenticates, especially for agents shared with many users.
- doc | Snowflake connector reference | https://learn.microsoft.com/en-us/connectors/snowflakev2/
- doc | Use connectors in Copilot Studio agents | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-connectors

# B11 | Safety, Moderation & Responsible AI
Build agents that are safe, fair and secure by default.

## rai | Responsible AI Principles
Microsoft's six responsible AI principles are fairness, reliability and safety, privacy and security, inclusiveness, transparency, and accountability. Use them as a design checklist: who could this agent harm, and how would we know?
- doc | Microsoft Responsible AI principles and approach | https://www.microsoft.com/en-us/ai/principles-and-approach
- video | Responsible AI Principles (AI-3017 Ep. 3) | https://www.youtube.com/watch?v=8Ra5L1aQ5YM

## moderation | Content Moderation in Copilot Studio
Copilot Studio checks both the user's input and the agent's output for harmful content. You can set moderation strictness at agent, topic or prompt level; the topic-level setting wins at runtime. Stricter settings block more harmful content but answer fewer questions.
- doc | FAQ for generative answers — content moderation | https://learn.microsoft.com/en-us/microsoft-copilot-studio/faqs-generative-answers
- doc | Resolve responsible AI content filter errors | https://learn.microsoft.com/en-us/troubleshoot/power-platform/copilot-studio/generative-answers/agent-response-filtered-by-responsible-ai

## injection | Prompt Injection & Jailbreaks
Prompt injection hides instructions in user input or in content the agent reads, such as a web page, email or document, to take control of the agent. It is riskier when agents can use tools. Mitigations include content filters, keeping data separate from instructions, least-privilege tools and approvals.
- doc | Prompt Shields (Azure AI Content Safety) | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection

## dlp | Data Privacy & DLP Awareness
Data policies (DLP) decide which connectors, knowledge sources and channels agents may use together. If a tool is blocked, it's often a policy, not a bug. Know what data leaves your tenant and where it goes.
- doc | Configure data policies for agents | https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention
- doc | Security and governance in Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance

## agentauth | Agent Authentication Options
An agent can require no authentication, Microsoft Entra ID sign-in or manual authentication. This decides who can talk to it and whether it can act as the signed-in user. Internal agents with company data should require authentication.
- doc | Configure user authentication | https://learn.microsoft.com/en-us/microsoft-copilot-studio/configuration-end-user-authentication
- video | Copilot Studio: Publish To A Website With Single Sign-On (Matthew Devaney) | https://www.youtube.com/watch?v=dUXE4FTx9Cw

# B12 | Environments & Publishing
Move agents from your developer environment into users' hands safely.

## envs | Power Platform Environments
Environments are containers for apps, flows, agents and data, each with its own security. Use separate developer, test and production environments so experiments never affect real users.
- doc | Environments overview | https://learn.microsoft.com/en-us/power-platform/admin/environments-overview
- video | Manage the Microsoft Power Platform environment (PL-900 Ep. 2) | https://www.youtube.com/watch?v=1OGCfs_joVA

## solutions | Solutions Basics
Solutions package agents, flows, connection references and environment variables so they can move between environments. Create every agent inside a custom solution from day one.
- doc | Create and manage custom solutions in Copilot Studio | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-solutions-overview
- doc | Solution concepts | https://learn.microsoft.com/en-us/power-platform/alm/solution-concepts-alm

## publish | Publishing an Agent
Saving keeps your draft; publishing makes the latest version available on every connected channel. After you publish, retest in the real channel, because authentication and rendering can differ from the test pane.
- doc | Key concepts — publish and deploy your agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-fundamentals-publish-channels

## channels | Channels
Channels are where users meet your agent: Teams and Microsoft 365 Copilot, websites, mobile apps and others. Each channel has its own authentication and formatting behaviour.
- doc | Connect an agent to Teams and Microsoft 365 Copilot | https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-add-bot-to-microsoft-teams
- doc | Publish and deploy your agent (channels) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-fundamentals-publish-channels

## share | Sharing & Permissions
Share an agent with co-authors, who can edit it, and with users, who can chat with it, ideally through security groups. Sharing an agent doesn't automatically share its connections or its knowledge permissions.
- doc | Share agents with other users | https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-share-bots

## analytics | Analytics Basics
Analytics show how the agent is used: sessions, engagement, resolution, satisfaction, knowledge and tool usage, and errors. Use them to decide what to improve next.
- doc | Monitor overview (analytics) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-overview
- video | How To View Conversation Transcripts In Copilot Studio (Matthew Devaney) | https://www.youtube.com/watch?v=uPWyhoRqo-0

# B13 | Testing & Evaluation Basics
Prove your agent works — repeatedly, not just once.

## whyeval | Why Evaluate Agents
Agents don't give the same output every time, and they change when you edit instructions, knowledge or models. "It worked when I tried it" is not evidence. Evaluation means running a fixed set of questions and checking the answers every time you change something.
- doc | About agent evaluation | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-intro
- doc | Agent evaluation checklist | https://learn.microsoft.com/en-us/agents/agent-evaluation/evaluation-checklist

## manual | Manual Testing & Activity Map
Before you automate, reproduce problems by hand in the test pane. Use the activity map to see whether the fault was the wrong knowledge, the wrong tool, bad inputs or unclear instructions.
- doc | Test your agent | https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-test-bot

## testsets | Agent Evaluation Test Sets
A test set holds questions, with expected answers where you have them. You can build it by hand, generate it from your agent's description or knowledge, import it from a spreadsheet, or capture it from a test chat. Start small, around 10–20 realistic questions.
- doc | Create a test set | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-create
- video | Copilot Studio Test Automation: STOP Testing Manually!! (Matthew Devaney) | https://www.youtube.com/watch?v=qh4YRqZgaQU

## runeval | Running Evaluations & Reading Results
Run the test set, review the results for each case, open the failures to see why they failed, fix the agent and run it again. Keep the results so you can compare versions.
- doc | Run evaluations and view results | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-results
- doc | Choose evaluation methods | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-overview

## feedback | Feedback Loop
Real user questions, thumbs up and down, and transcripts are the best source of new test cases. Close the loop: failed conversations become new test cases, then a fix, then another evaluation run.
- doc | Monitor overview (analytics) | https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-overview
- video | Monitor, analyze, and tune AI agents (AB-100 Ep. 11) | https://www.youtube.com/watch?v=JR6C87ZEtws

# B14 | Next Steps
Check your readiness and move on to the Advanced roadmap.

## checkpoint | Beginner Checkpoint
Before you start Advanced, you should be able to do the following on your own:
- explain tokens, context and temperature
- write an XML-structured prompt
- build an agent with knowledge, a connector tool, a flow and a skill
- query Snowflake with joins and aggregations
- configure moderation and authentication
- publish to Teams
- run an evaluation
- doc | Study guide AB-620: Designing and Building Integrated AI Solutions in Copilot Studio | https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ab-620
- course | Create agents in Microsoft Copilot Studio (learning path) | https://learn.microsoft.com/en-us/training/paths/create-extend-custom-copilots-microsoft-copilot-studio/
