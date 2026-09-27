---
id: basic
order: 1
title: AI Engineering on Microsoft
subtitle: Basic Roadmap
tagline: For everyone at the company — what Copilot is, how to prompt it, and how to use it well in Chat and the Office apps.
next: intermediate.html
next_label: Want to build agents? Start Intermediate
audience: Everyone
card: What an LLM is and why it invents things, prompting craft, what Copilot can and cannot see in your tenant, Microsoft Copilot Chat, Copilot in Word, Excel, PowerPoint, Outlook and Teams, and using agents other people built.
---

# how-copilot-works | How Copilot Works
The three ideas that explain everything Copilot does well and everything it gets wrong.

## llm | What Is an LLM
A large language model is a neural network trained on huge amounts of text to predict the next token in a sequence. By repeatedly predicting next tokens it can answer questions, summarise, write code and follow instructions. Its output depends on its input and some randomness, so the same prompt can give different answers.
- doc | LLM fundamentals (Microsoft Agent Framework learning journey) | https://learn.microsoft.com/en-us/agent-framework/journey/llm-fundamentals
- doc | How generative AI and LLMs work (.NET AI docs) | https://learn.microsoft.com/en-us/dotnet/ai/conceptual/how-genai-and-llms-work
- video | Introduction to AI concepts (AI-901) | https://www.youtube.com/watch?v=-MkEEXFODZU

## context | Context & Context Window
The context is everything the model sees in one request: instructions, conversation history, retrieved content and your own message. The context window is the maximum number of tokens that fits, covering both input and output. When the window fills up, content has to be dropped or summarised, and quality can fall before you reach the limit.
- doc | Understanding tokens (.NET AI docs) | https://learn.microsoft.com/en-us/dotnet/ai/conceptual/understanding-tokens
- doc | Prompt engineering techniques (Microsoft Foundry) | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering

## hallucination | Hallucinations & Grounding
LLMs can produce confident, fluent answers that are wrong ("hallucinations") because they generate plausible text, not verified facts. Grounding is the main fix: the model is given trusted content to answer from and asked to cite it. This is why a Copilot answer with citations you can open is worth more than a fluent one without them.
- doc | Groundedness detection (Azure AI Content Safety) | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/groundedness
- doc | Retrieval-augmented generation (.NET AI docs) | https://learn.microsoft.com/en-us/dotnet/ai/conceptual/rag

# prompting | Prompting
Writing requests that get predictable answers — the one skill that pays off in every tool in this course.

## anatomy | Anatomy of a Prompt
A prompt usually has three layers. Standing instructions set who the assistant is and its rules. Context is the content it should use. Your message is the actual request. Keeping these layers separate makes a prompt easier to fix when it goes wrong, and makes it harder for instructions hidden in a document to take over.
- doc | System message design | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/advanced-prompt-engineering
- course | Understanding prompt engineering fundamentals (Generative AI for Beginners) | https://learn.microsoft.com/en-us/shows/generative-ai-for-beginners/understanding-prompt-engineering-fundamentals-generative-ai-for-beginners

## clarity | Clarity & Specificity
Vague prompts get vague answers. State the role, the task, the audience, constraints (length, tone, what not to do), and what a good result looks like. Microsoft's guidance: be specific and leave as little to interpretation as possible.
- doc | Prompt engineering techniques (Microsoft Foundry) | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering
- course | Write effective prompts (Microsoft Learn training) | https://learn.microsoft.com/en-us/training/modules/write-effective-prompts-do-more-prompting/
- video | Better prompts = better AI (Microsoft Learn) | https://www.youtube.com/watch?v=k4geocw07nc

## fewshot | Few-Shot Examples
Showing the model one or more input → output examples ("few-shot") is often more effective than describing the format in words. Keep examples short, realistic and consistent with the output you want.
- doc | Prompt engineering techniques — few-shot learning | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering
- doc | Prompt engineering concepts (.NET) | https://learn.microsoft.com/en-us/dotnet/ai/conceptual/prompt-engineering-dotnet

## output | Output Formats
Say exactly how you want the answer shaped: a bullet list, a table with named columns, a one-paragraph summary, an email you can send. Asking for a shape is the cheapest way to make an answer usable without editing it, and it makes a wrong answer easier to spot — a missing column is obvious in a way a missing sentence is not.
- doc | Prompt engineering techniques — specify output structure | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering
- course | Write effective prompts (Microsoft Learn training) | https://learn.microsoft.com/en-us/training/modules/write-effective-prompts-do-more-prompting/

## decompose | Breaking Down Tasks
Models do better when a complex task is split into ordered steps: extract the facts first, then compare them, then write the summary. Ask for one step at a time and check each result before moving on, rather than asking one long question and hoping.
- doc | Prompt engineering techniques — break the task down | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering

## iterate | Iterating on Prompts
Prompting is experimental: write a prompt, try it on a few realistic cases, compare the answers and refine. Most of the gain comes from the second and third attempt, not the first. Keep the prompts that worked somewhere you can find them again — your own notes, or a page your team shares.
- doc | Prompt engineering techniques — iterate and evaluate | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering
- course | Write effective prompts for Microsoft 365 Copilot | https://learn.microsoft.com/en-us/training/modules/write-effective-prompts-do-more-prompting/

# how-copilot-sees-your-work | How Copilot Sees Your Work
What Copilot can reach inside the company, what it cannot, and what you should never hand it. Everything in the five app modules that follow rests on this one.

## tenantgrounding | Grounded in Your Own Work
With a Microsoft 365 Copilot licence, Copilot can answer from your organisation's own content — documents, mail, chats and meetings — not only from what the model learnt during training. That is what makes it useful at work and also what makes its mistakes specific to your company rather than generic.
- doc | What is Microsoft Copilot? | https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-overview
- doc | How does Microsoft Copilot work? | https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-architecture
- doc | Semantic indexing for Microsoft Copilot | https://learn.microsoft.com/en-us/microsoftsearch/semantic-index-for-copilot

## visibility | You Only See What You Could Already Open
Copilot works inside your existing permissions. It cannot show you a document you would be refused if you clicked the link yourself, and using it does not widen your access. The flip side matters just as much: content that is over-shared becomes much easier to find, so Copilot surfaces sharing mistakes that were always there.
- doc | Data, Privacy, and Security for Microsoft Copilot | https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy
- doc | How Copilot Chat works in Microsoft 365 apps | https://support.microsoft.com/en-us/microsoft-365-copilot/how-copilot-chat-works-in-microsoft-365-apps

## missingcontent | Why Copilot Missed a File
An answer that leaves out the obvious document is the most common complaint, and it is rarely the model's fault. The usual causes are permissions, where the file lives, a format that was never indexed, and content that is too new. Knowing the shortlist turns "Copilot is useless" into a question you can actually answer.
- doc | How does Microsoft Copilot work? | https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-architecture
- doc | Semantic indexing for Microsoft Copilot | https://learn.microsoft.com/en-us/microsoftsearch/semantic-index-for-copilot

## sensitive | What Not to Paste In
Not every assistant that says "Copilot" is the same assistant, and they do not all handle your content the same way. Know which one you are in, what your organisation's sensitivity labels mean for a file you are about to summarise, and treat anything covered by a customer or supplier agreement as something to check before sharing rather than after.
- doc | Data, Privacy, and Security for Microsoft Copilot | https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy
- doc | Learn about sensitivity labels (Microsoft Purview) | https://learn.microsoft.com/en-us/purview/sensitivity-labels
- doc | Microsoft Purview data security and compliance protections for Microsoft 365 Copilot | https://learn.microsoft.com/en-us/purview/ai-microsoft-purview

## rai | Responsible AI Principles
Microsoft's six responsible AI principles are fairness, reliability and safety, privacy and security, inclusiveness, transparency, and accountability. Use them as a checklist on your own use of Copilot: who is affected by this answer, and how would anyone know if it were wrong?
- doc | Responsible AI Principles and Approach | https://www.microsoft.com/en-us/ai/principles-and-approach
- video | Responsible AI Principles (AI-3017 Ep. 3) | https://www.youtube.com/watch?v=8Ra5L1aQ5YM

# copilot-chat | Microsoft Copilot Chat
The assistant that is not inside any one document — where you go when the question spans your whole working week.

## m365chat | Microsoft Copilot Chat
Microsoft Copilot Chat is the everyday assistant you reach in Teams, Outlook, the Office apps and the browser. It can ground answers in the web or, with a Microsoft 365 Copilot licence, in your work content. It is the right place for questions that are not about one open file — finding which document covers a procedure, or pulling together what happened on a job.
- doc | Microsoft Copilot hub | https://learn.microsoft.com/en-us/microsoft-365/copilot/
- video | Explore Microsoft 365 Copilot Chat (MS-4023) | https://www.youtube.com/watch?v=jdwx6ztuJpE
- course | Write effective prompts for Microsoft 365 Copilot | https://learn.microsoft.com/en-us/training/modules/write-effective-prompts-do-more-prompting/

# copilot-in-word | Copilot in Word
Reading, drafting and rewriting long documents — the app where Copilot's summarising is worth the most.

## wordask | Asking About the Document You Have Open
Copilot in Word can answer questions about the document in front of you: what it covers, where a particular requirement is stated, what changed in this revision. Ask narrow questions and read the answer against the text, because a confident paraphrase of a procedure is not the same as the procedure.
- doc | Create a summary of your document with Copilot in Word | https://support.microsoft.com/en-us/word/copilot/create-a-summary-of-your-document-with-copilot-in-word
- doc | Welcome to Copilot in Word | https://support.microsoft.com/en-us/word/welcome-to-copilot-in-word

## wordmake | Drafting and Rewriting
The two things Copilot in Word does most are start a draft from a description and rework a passage you already have — shorter, plainer, in a different tone, or as a table. Drafting from a description is the weaker of the two, because nothing constrains what it writes; reworking text you supplied is the stronger, because the content is already yours.
- doc | Draft and add content with Copilot in Word | https://support.microsoft.com/en-us/word/copilot/draft-and-add-content-with-copilot-in-word
- doc | Edit content and rewrite with Copilot in Word | https://support.microsoft.com/en-us/word/edit-with-copilot-in-word

## wordtemplate | Starting from a Controlled Template
Controlled documents have a required structure, and a draft that ignores it costs more to fix than it saved. Start from the template, keep its headings, and use Copilot to fill sections rather than to invent the shape. Whatever it produces still goes through the same review as anything you typed yourself.
- doc | Create a file from a template with the Microsoft Copilot app | https://support.microsoft.com/en-us/microsoft-365-copilot/create-a-file-from-a-template-with-the-microsoft-365-copilot-app
- doc | Draft and add content with Copilot in Word — reuse format and structure | https://support.microsoft.com/en-us/word/copilot/draft-and-add-content-with-copilot-in-word

## wordlimits | Where Copilot in Word Falls Short
Long documents, tracked changes, comment threads, embedded objects and heavy formatting are where results get thin, and the reasons are specific rather than mysterious — there is a limit to how much of a document reaches the model at once, and formatting is not content. Expect to check structure and numbers yourself.
- doc | Frequently asked questions about Copilot in Word | https://support.microsoft.com/en-us/office/frequently-asked-questions-about-copilot-in-word-7fa03043-130f-40f3-9e8b-4356328ee072
- doc | Data, Privacy, and Security for Microsoft Copilot | https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy

# copilot-in-excel | Copilot in Excel
Reading and shaping tabular data — the app with the strictest prerequisites and the most checkable output.

## excelask | Asking About a Table
Copilot in Excel answers questions about the data in front of it: what the columns mean, which rows stand out, how one group compares with another. Because the answer is about data you can see, this is the easiest place in Office to catch Copilot being wrong — the number either matches the sheet or it does not.
- doc | Get started with Copilot in Excel | https://support.microsoft.com/en-us/excel/copilot/get-started-with-copilot-in-excel
- doc | Get data insights with Copilot in Excel | https://support.microsoft.com/en-us/excel/copilot/data-insights-with-copilot-in-excel

## excelmake | Building a Table from Documents
A common job is turning a stack of documents — certificates, reports, forms — into one table you can sort and filter. Decide the columns before you start, get a few rows right by hand, and use those as the pattern. The columns you chose are what makes the result checkable later.
- doc | Get data insights with Copilot in Excel | https://support.microsoft.com/en-us/excel/copilot/data-insights-with-copilot-in-excel
- doc | Overview of Excel tables | https://support.microsoft.com/en-us/office/overview-of-excel-tables-7ab0bb7d-3a9e-4b56-a3c9-6c94334e492c

## excelformula | Formulas It Writes, and Checking Them
Copilot will explain a formula you do not understand and propose one for a result you describe, which is the single most useful thing it does in Excel. Both need checking: read the formula against what you asked for, and test it on rows where you already know the answer. A formula that is wrong in the same direction every time looks right in a chart.
- doc | Turn Copilot formula suggestions on or off in Excel | https://support.microsoft.com/en-us/excel/copilot/copilot-formula-suggestions-turn-on-off
- doc | Overview of formulas in Excel | https://support.microsoft.com/en-us/office/overview-of-formulas-in-excel-ecfdc708-9162-49e8-b993-c311f47ca173
- doc | Get data insights with Copilot in Excel | https://support.microsoft.com/en-us/excel/copilot/data-insights-with-copilot-in-excel

## excellimits | Where Copilot in Excel Falls Short
Excel is the app where Copilot most often refuses outright, and the reasons are structural: data has to be a real table with a header row, and merged cells, blank rows, inconsistent types and values stored as text all get in the way. Tidying the sheet is usually the fix, and it is work you would have had to do anyway.
- doc | Get started with Copilot in Excel | https://support.microsoft.com/en-us/excel/copilot/get-started-with-copilot-in-excel
- doc | Overview of Excel tables | https://support.microsoft.com/en-us/office/overview-of-excel-tables-7ab0bb7d-3a9e-4b56-a3c9-6c94334e492c

# copilot-in-powerpoint | Copilot in PowerPoint
Turning something you already wrote into something you can present — and keeping it on-brand.

## pptask | Asking About a Deck
Copilot in PowerPoint can summarise a deck someone sent you and answer questions about what is in it, which is faster than clicking through fifty slides to find the one number you came for.
- doc | Frequently asked questions about Copilot in PowerPoint | https://support.microsoft.com/en-us/office/frequently-asked-questions-about-copilot-in-powerpoint-3e229188-9086-4f4c-9f9f-824cd25ae84f
- doc | Create a new presentation with Copilot in PowerPoint | https://support.microsoft.com/en-us/powerpoint/copilot/create-a-new-presentation-with-copilot-in-powerpoint

## pptmake | Turning a Document into a Deck
The best use of Copilot in PowerPoint is building a first draft from a document you already have, rather than from a one-line description — the source document constrains the content, so there is far less to invent. Expect to cut slides: a draft deck is generous with them.
- doc | Create a new presentation with Copilot in PowerPoint | https://support.microsoft.com/en-us/powerpoint/copilot/create-a-new-presentation-with-copilot-in-powerpoint
- doc | Copilot tutorial: Create a branded presentation from a file | https://support.microsoft.com/en-us/powerpoint/copilot-tutorial-create-a-branded-presentation-from-a-file

## pptbrand | Templates and Themes: What Survives
A generated deck follows the template it was started from, so which template you open first decides how much rework you face. Start from your organisation's template, and check the things generation is careless with — layouts, placeholder text, image choices and slide order.
- doc | Keep your presentation on-brand with Copilot | https://support.microsoft.com/en-us/powerpoint/copilot/keep-your-presentation-on-brand-with-copilot
- doc | Copilot tutorial: Create a branded presentation from a file | https://support.microsoft.com/en-us/powerpoint/copilot-tutorial-create-a-branded-presentation-from-a-file

## pptlimits | Where Copilot in PowerPoint Falls Short
Generated slides tend to be wordy, evenly weighted and light on the one point you actually needed to make. Copilot cannot tell which slide matters, and it will not notice that a chart contradicts the text beside it. Treat the output as a draft to edit down, never as a deck to present.
- doc | Frequently asked questions about Copilot in PowerPoint | https://support.microsoft.com/en-us/office/frequently-asked-questions-about-copilot-in-powerpoint-3e229188-9086-4f4c-9f9f-824cd25ae84f
- doc | Keep your presentation on-brand with Copilot | https://support.microsoft.com/en-us/powerpoint/copilot/keep-your-presentation-on-brand-with-copilot

# copilot-in-outlook | Copilot in Outlook
Mail is where most people meet Copilot first, and where a bad draft does the most damage.

## mailask | Summarising a Thread
A long reply-all thread is the clearest case for summarising: you want the decision and the open questions, not forty messages. Ask for what you need — what was decided, what is still open, who owes what — rather than for a summary, and check the conclusion against the last few messages, which is where threads change direction.
- doc | Summarize an email thread with Copilot in Outlook | https://support.microsoft.com/en-us/office/summarize-an-email-thread-with-copilot-in-outlook-a79873f2-396b-46dc-b852-7fe5947ab640
- doc | Welcome to Copilot in Outlook | https://support.microsoft.com/en-us/outlook/welcome-to-copilot-in-outlook

## mailmake | Drafting and Coaching a Reply
Copilot can draft a reply from a few words about what you want to say, and can also review a draft you wrote and comment on tone, clarity and length. The second is the safer habit: it keeps your intent and your facts, and only changes how they land.
- doc | Draft an email message with Copilot in Outlook | https://support.microsoft.com/en-us/office/draft-an-email-message-with-copilot-in-outlook-3eb1d053-89b8-491c-8a6e-746015238d9b
- doc | Get email coaching with Copilot in Outlook | https://support.microsoft.com/en-us/office/get-email-coaching-with-copilot-in-outlook-91a3cd56-1586-4a31-85c7-2eb8cdb02405

## mailtriage | Catching Up on Your Inbox
After time away, the useful question is not "summarise my mail" but "what needs me". Copilot can group what arrived and point at what looks like it is waiting on you, which is a starting point for triage rather than a decision — nothing knows which of your threads actually matters.
- doc | Prioritize my inbox with Copilot in Outlook | https://support.microsoft.com/en-us/outlook/copilot-outlook/prioritize-my-inbox
- doc | Welcome to Copilot in Outlook | https://support.microsoft.com/en-us/outlook/welcome-to-copilot-in-outlook

## maillimits | Where Copilot in Outlook Falls Short
Mail has two specific traps. A summary flattens a thread, so a caveat someone added once and everyone ignored can disappear; and a drafted reply is fluent enough to send without reading, which is how a wrong commitment leaves the building with your name on it. Attachments and older mail are also not always within reach.
- doc | Frequently asked questions about Copilot in Outlook | https://support.microsoft.com/en-us/office/frequently-asked-questions-about-copilot-in-outlook-07420c70-099e-4552-8522-7d426712917b
- doc | Data, Privacy, and Security for Microsoft Copilot | https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy

# copilot-in-teams | Copilot in Teams
Meetings and chats — the only app module where what Copilot can do depends on a setting somebody else controls.

## teamsask | Catching Up on a Chat or Channel
Copilot in Teams can tell you what a long chat or channel thread has come to, which is the fastest way back into a conversation that ran while you were elsewhere. Ask what was decided and what is unresolved, and open the messages it points at before acting on them.
- doc | Catch up on meetings with Microsoft Copilot in Teams | https://support.microsoft.com/en-us/teams/copilot/catch-up-on-meetings-with-microsoft-365-copilot-in-teams
- doc | Frequently asked questions about Copilot in Microsoft Teams | https://support.microsoft.com/en-us/office/frequently-asked-questions-about-copilot-in-microsoft-teams-e8737767-4087-4ae6-b1d8-10264152b05a

## teamsmake | Drafting Messages and Notes
Copilot can draft a message for a channel, tidy a note you typed in a hurry, or turn a scrappy list into something readable. The same rule as mail applies: reviewing your own draft is safer than accepting one you did not write.
- doc | Frequently asked questions about Copilot in Microsoft Teams | https://support.microsoft.com/en-us/office/frequently-asked-questions-about-copilot-in-microsoft-teams-e8737767-4087-4ae6-b1d8-10264152b05a
- doc | Catch up on meetings with Microsoft Copilot in Teams | https://support.microsoft.com/en-us/teams/copilot/catch-up-on-meetings-with-microsoft-365-copilot-in-teams

## teamsrecap | Meeting Recap and Action Items
A meeting recap gives you what was discussed, what was decided and who agreed to do what — the highest-value thing Copilot does for most people, because the alternative is nobody writing it down. It also has the highest cost when wrong: an action item attributed to the wrong person is a commitment they never made.
- doc | Recap in Microsoft Teams | https://support.microsoft.com/en-us/teams/meetings/recap-in-microsoft-teams
- doc | Catch up on meetings with Microsoft Copilot in Teams | https://support.microsoft.com/en-us/teams/copilot/catch-up-on-meetings-with-microsoft-365-copilot-in-teams

## teamslimits | Where Copilot in Teams Falls Short
Copilot can be used during a meeting without it being transcribed or recorded, but asking it about the meeting **afterwards** needs live transcription to have been on — a choice the organiser makes under a policy your organisation sets, so the same licence gives different results in two meetings on the same day. Transcripts also mishear names, part numbers and anything said over someone else, and a recap inherits every one of those errors.
- doc | Catch up on meetings with Microsoft Copilot in Teams | https://support.microsoft.com/en-us/teams/copilot/catch-up-on-meetings-with-microsoft-365-copilot-in-teams
- doc | Start, stop, and download live transcripts in Microsoft Teams meetings | https://support.microsoft.com/en-us/teams/meetings/start-stop-and-download-live-transcripts-in-microsoft-teams-meetings

# using-agents-others-built | Using Agents Other People Built
Agents your colleagues publish show up in the tools you already use — and are judged the same way as any other answer.

## usingagents | Using Agents Someone Published
A published agent appears where you already work — in Teams, in Microsoft Copilot, on a website — and is usually built for one job, with a specific set of documents behind it. Treat it exactly as you would Copilot: read what it cites, notice when a question falls outside what it was built for, and tell whoever published it when an answer is wrong. You are the only person who can.
- doc | Connect and configure an agent for Teams and Microsoft 365 Copilot | https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-add-bot-to-microsoft-teams
- doc | Agents for Microsoft 365 Copilot overview | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agents-overview

# finishing-basic | Finishing Basic
What this level did and did not qualify you to do, and where to go if you want to build.

## basiccovered | What You Can Now Do
You know why Copilot invents things, how to ask for what you actually want, what it can and cannot see inside the company, and how to use it in Chat and the five Office apps without taking its word for anything. That is the whole of this level, and for most people it is the whole of what they need. It does not qualify you to build an agent — that is what Intermediate is for, and it is a door you can leave shut.
- doc | Microsoft Copilot hub | https://learn.microsoft.com/en-us/microsoft-365/copilot/
- doc | Microsoft Copilot (Microsoft Adoption) | https://adoption.microsoft.com/en-us/copilot/
