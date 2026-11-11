## TL;DR

Red teaming sends an agent adversarial prompts before anyone else does. Foundry's AI Red Teaming
Agent (preview) automates the first pass: it generates attack prompts for harm categories, applies
attack strategies and reports an **attack success rate**. It is built on PyRIT, an open-source
toolkit you can also run yourself. A scan finds a model that can be pushed. It does not find the
attacks that are specific to what your agent does.

## Running a scan

<!-- volatile verified=2026-11 -->
Install `azure-ai-evaluation[redteam]`, which "provides the PyRIT functionality", on Python 3.10 to
3.13, with a Foundry project. The page says the local agent "is not compatible with the Foundry(new)
portal and SDK". You pass a target, which can be a model configuration, a function that takes a
query and returns a string, or a PyRIT chat target:

*Adapted from the sample on [Run AI Red Teaming Agent Locally (Azure AI Evaluation SDK)](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/run-scans-ai-red-teaming-agent):*

```python
red_team_agent = RedTeam(
    azure_ai_project=os.environ["AZURE_AI_PROJECT"],
    credential=DefaultAzureCredential())

def simple_callback(query: str) -> str:
    return "I'm an AI assistant that follows ethical guidelines."

result = await red_team_agent.scan(target=simple_callback)
```

By default it uses four risk categories, violence, sexual, hate and unfairness, and self-harm, with
ten attack prompts each. Without strategies it sends only "baseline direct adversarial queries", and
the page recommends starting there, then adding strategies graded **Easy**, **Moderate** and
**Difficult**. The headline is the **Attack Success Rate**, "the percentage of attacks that
successfully elicit undesirable responses". The scorecard is JSON, by category and strategy.
<!-- /volatile -->

PyRIT's own docs describe "automated and human-led AI red teaming", with a command-line scanner, a
browser interface and multi-turn attacks. Its repository moved: the old `Azure/PyRIT` page says it
was archived in March 2026 and points to `microsoft/PyRIT`.

<!-- unknown since=2026-11 -->
The Foundry page says the agent "only supports single-turn interactions in text-only scenarios",
yet lists multi-turn strategies, Multiturn and Crescendo, among its Difficult ones. It does not say
whether an agent with tools can be a target beyond a callback you write.
<!-- /unknown -->

## At Technik

The four default categories are harm categories. A default scan asks whether the assistant can be
talked into saying something harmful. Technik's worse risk is a quiet false claim: a record told the
assistant to report an open QN as closed ({{topic:injection}}). No default category looks for that.
It needs cases of your own, and the evaluation harness is where they live ({{topic:evalstrategy}}).

So treat a scan as one input. Run it against a callback that calls the agent, in the live job, since it
needs a Foundry project and an offline run cannot supply one. The capstone has no scan and has
never run live.

## Design guidance

- **Start with the baseline**, then add strategies.
- **Add cases for your own threats**, from {{topic:threats}}, because the defaults are generic.
- **Read the failures by category**, and turn each into a fixed case or a control.
- **Keep a person in the loop.** Automation widens the first pass.

## Key terms

**Attack success rate** — the share of adversarial prompts that got an undesirable response.

**PyRIT** — Microsoft's open-source toolkit for red teaming generative AI, behind the Foundry agent.
