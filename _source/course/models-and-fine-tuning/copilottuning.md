## TL;DR

Microsoft Copilot Tuning is the other way to customise a model, and shares almost nothing with the rest of this module. There is no Foundry job, training file or choice of method. You create an agent from a **tunable template** in Agent Builder, and "model tuning" is one of three things you can adjust on it. It runs "entirely within the Microsoft 365 tenant", for agents that live in Microsoft 365 Copilot. The page title says **early access preview**, so plan nothing around it.

## How it works

<!-- volatile verified=2026-11 -->
A tunable template serves one repeatable task: document writing, document summary, expert answers, document validation, style editing, or an optimization agent for allocation and planning. The page says many agents "meet quality expectations without more customizations", and tuning is for the rest. Three kinds exist:

- **Context tuning** supplies the task, domain and examples, from which the system proposes an evaluation rubric.
- **Tool tuning** adds agents or tools and instructions for orchestrating them.
- **Model tuning** uses "supervised fine-tuning and reinforcement learning techniques" on examples from organisational data. It runs asynchronously, and "evaluation results determine whether the updated model is ready to be published".

Access needs an eligible tenant, and an administrator may have to enable tuning. The page says tuned agents "honor access control lists (ACLs) from the training data". Its disclaimer makes the administrator responsible for data-protection law and for holding rights to copyrighted training material. A valid deletion request for data used in training means retraining, while the tuned model can be deleted at any time.
<!-- /volatile -->

<!-- unknown since=2026-11 -->
The page says access through Frontier was "planned for April 2026". Updated in November 2026, the page still describes limited early access, so the date's status is unclear. It does not say which base model is tuned, what a run costs, how a trained model honours each reader's permissions, or whether a tuned agent can be called from outside Microsoft 365 Copilot. The video the roadmap lists was not watched, and nothing here depends on it.
<!-- /unknown -->

## In practice at Technik

The closest fit is a **document validation** agent that checks a draft revision of `SWI70000318` against a rulebook of Technik's document rules. Nobody has written that rulebook. Start with the template's defaults, give it the rules as context, and tune the model only if evaluation says the defaults miss.

This route does not replace the Foundry one. A tuned agent lives in Microsoft 365 Copilot, so the Production Assistant cannot call it, and none of this module's controls apply: no training type, no hyperparameters. You trade control for a route a domain expert can run. Before asking for access, check whether a skill ({{module:agent-skills}}) can hold the rules, which costs nothing to change.

## Key terms

**Tunable template**: an Agent Builder template with a predefined workflow that can be context-, tool- or model-tuned.

**Model tuning**: the fine-tuning Copilot Tuning runs for an agent, where evaluation decides whether to publish.

**Early access**: availability to a limited set of customers.
