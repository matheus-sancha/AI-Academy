## TL;DR

Microsoft Agent Framework is the engine {{topic:customengine}} left you to bring. Its overview calls
it "the direct successor" to Semantic Kernel and AutoGen, "created by the same teams", and "the next
generation of both". An agent in it is a model client plus instructions, tools and middleware, and
the tutorial builds one "in just a few lines of code". Its most useful sentence is the one that
talks you out of it: "If you can write a function to handle the task, do that instead of using an AI
agent."

## Why it matters

{{topic:harnessvssdk}} said an SDK gives you the loop as code you compile, test and host. That is a
trade, and this lesson is the inventory: what the framework hands you, and what it leaves with you.
The second list is the longer one, and the overview says so at its very end. You are responsible for
"implementing your own responsible AI mitigations such as metaprompt, content filters, or other
safety systems". A managed harness came with those. Here they are code you write.

Advice about this framework is also often written under an older name. {{topic:customengine}} found
a Microsoft page calling it "formerly Semantic Kernel", which is half of its history.

## How it works

### Four areas

The overview sorts the framework into four areas.

| Area | What the overview says it is |
|---|---|
| Agents | "Individual agents that use LLMs to process inputs, call tools and MCP servers, and generate responses" |
| Harness Agent | "An opinionated agent with batteries-included capabilities for long, multi-step tasks" |
| Workflows | "Functional and graph-based workflows that connect agents and functions through explicit execution paths" |
| Integrations | "Connections to model providers, agent services, tools, context providers, middleware, evaluation services, and UI frameworks" |

The Harness Agent is the packaged loop from {{topic:loop}}, with planning, compaction, file memory
and tool approval already assembled. Workflows have their own lesson ({{topic:mafworkflows}}).

### The building blocks

Under the four areas the overview names the parts: "model clients (chat completions and responses),
an agent session for state management, context providers for agent memory, middleware for
intercepting agent actions, and MCP clients for tool integration."

Read that list as five seams. The **client** is where the provider lives. The **session** holds a
conversation's state ({{topic:history}}). A **context provider** adds memory to what the model sees
({{topic:memory}}). **Middleware** wraps a run, so code of yours executes around the model's. The
**MCP client** turns a server into tools ({{topic:mcparch}}). Each seam is something you can
replace, and something you now maintain.

### What was merged

The framework "combines AutoGen's simple agent abstractions with Semantic Kernel's enterprise
features — session-based state management, type safety, middleware, telemetry — and adds graph-based
workflows for explicit multi-agent orchestration." The overview links a migration guide from each
predecessor, so the documented move for inherited code is to migrate it.

### The smallest agent

The tutorial's first agent is a client, instructions and one call: an `Agent` built around a
`FoundryChatClient`, then `await agent.run(...)`. The overview lists the providers a client can
reach, "Microsoft Foundry, Anthropic, Azure OpenAI, OpenAI, Ollama, and more", so changing provider
means changing the client and keeping the agent. The capstone's agent has the same shape with two
more arguments:

*From [`agent/main.py`, lines 44–54](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/agent/main.py#L44-L54):*

```python
def teamcenter_server(command="uv", args=("run", "--directory", str(ROOT), "server/teamcenter.py")):
    """The stage 2 server over stdio, run in the root project, which holds MCP SDK v2."""
    return MCPStdioTool(name="teamcenter", command=shutil.which(command) or command, args=list(args),
                        load_prompts=False, tool_result_content="content_first")


def build_agent(client, tools, **options):
    """The agent. Its tools are the stage 2 server: over stdio here, through the Foundry toolbox when hosted."""
    return Agent(client=client, name="technik-production-assistant",
                 instructions=INSTRUCTIONS.read_text(encoding="utf-8"),
                 tools=tools, middleware=[grounded_or_refuse], **options)
```

`tools` is an MCP client pointed at the Teamcenter server. `middleware` is the refusal guard that
runs on every answer ({{topic:loop}}). `client` is a parameter, and that is the design decision in
these eleven lines.

### Credentials are a choice the samples make for you

The Python sample signs in with `AzureCliCredential`, which is a developer's own login. The .NET and
Go tabs of the same tutorial carry a warning the Python tab lacks: `DefaultAzureCredential` "is
convenient for development but requires careful consideration in production", and a specific
credential avoids "latency issues, unintended credential probing, and potential security risks from
fallback mechanisms." The warning applies in any language. A credential that tries several sources
in turn uses whichever it finds first.

<!-- unknown since=2026-11 -->
The capstone's hosted entry point uses `DefaultAzureCredential`, the credential this warning is
about. It never ran live, so which source that chain settles on inside a hosted agent's sandbox is
unverified. Check it on your first deployment ({{topic:stageship}}).
<!-- /unknown -->

### Agent, workflow, or neither

The overview gives a two-column test.

| Use an agent when… | Use a workflow when… |
|---|---|
| "The task is open-ended or conversational" | "The process has well-defined steps" |
| "You need autonomous tool use and planning" | "You need explicit control over execution order" |
| "A single LLM call (possibly with tools) suffices" | "Multiple agents or functions must coordinate" |

The sentence about writing a function sits directly under it. Read together they give three options,
and the cheapest comes first.

<!-- volatile verified=2026-11 -->
The overview covers .NET, Python and Go. Go "is in public preview and requires Go 1.26 or later",
and "Declarative agents, CodeAct, and functional workflows aren't implemented in Go." The .NET
install command carries `--prerelease`. The two pages give different Python install commands and
name three different models in their samples, so treat every sample value as a placeholder
({{topic:language}}).
<!-- /volatile -->

## In practice at Technik

The rebuild of the Production Assistant is one call to `build_agent`, and three callers use it.

| Caller | Client it passes | Tools it passes |
|---|---|---|
| The offline tests | A scripted client that never reaches a model | The real server, on a faked Snowflake connection |
| `uv run main.py` on a laptop | `FoundryChatClient` with the developer's sign-in | The Teamcenter server over stdio |
| The hosted entry point | `FoundryChatClient` with the host's credential | The Foundry toolbox ({{topic:foundryagents}}) |

Because the client is a parameter, the tests exercise the framework's real function-calling loop and
the real middleware with no model behind them. That is why the refusal guard has a test at all, and
why the capstone could be built without ever running live ({{topic:stageagent}}).

The framework's preference order shows in what the capstone did not build. The guard,
`refuse_unless_grounded`, checks whether any tool result backs the answer. It is five lines with no
model in them, because a function could do the job. The assistant is an agent, not a workflow,
because its questions are open-ended. And it is not a Harness Agent. Three read-only lookups are not
a "long, multi-step" task, and every packaged capability would be something else to test.

What the rebuild gave up is equally concrete. The Intermediate assistant had Teams, skills, two
knowledge sources and five tools from configuration. This one has three tools and no channel, and
getting it in front of a user is a separate decision ({{topic:customengine}}).

## Design guidance

- **Write the function first.** Reach for an agent when the task is open-ended, and say which part
  is.
- **Make the client a parameter.** One construction function, called by tests, local runs and the
  host.
- **Put every-time rules in middleware.** Instructions ask. Middleware runs.
- **Choose the credential on purpose.** Name the one you expect in production instead of letting a
  chain find one.
- **Skip the packaged harness until the task is long.** Its features are features you must verify.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The agent cannot be tested without a model deployment | The client is created inside the function that builds the agent | Pass the client in; give tests a scripted one |
| A rule in the instructions holds most of the time | Instructions are a request to the model | Enforce it in middleware or in the tool |
| Sign-in works locally and fails, or is slow, once deployed | A fallback credential chain found a different source | Use a specific credential for the deployed path |
| A fixed three-step process was built as an agent | The first row of the test was skipped | Write it as functions, or as a workflow ({{topic:mafworkflows}}) |

## Key terms

**Microsoft Agent Framework** — Microsoft's SDK for agents and multi-agent workflows in .NET, Python
and Go, the successor to both Semantic Kernel and AutoGen.

**Chat client** — the object that talks to one model provider. The agent is built around it, so
swapping it changes the provider and nothing else.

**Middleware** — code that wraps an agent's run and can inspect or replace the result.

**Harness Agent** — the framework's packaged agent for long, multi-step tasks, with planning,
compaction, file memory and tool approval already assembled.
