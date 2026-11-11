## TL;DR

A trace is the record of one run: the steps an agent took, the tool calls it made, what came back,
how long each part took and what failed. Foundry's recommended start is server-side tracing, which
needs no code. You connect an Application Insights resource to the project and traces for hosted agents
appear. Client-side instrumentation is the second step, for your own code around an agent call. A trace
is also a copy of the conversation, tool arguments and results included, so deciding who may read it
is part of setting it up. Copilot Studio has its own telemetry, scoped to the standard harness.

## Why it matters

An evaluation tells you how the agent did on cases you chose. A user's complaint is a conversation you
did not choose, and the only way to know what the agent did in it is the record of that run.
{{topic:stageship}} ends with one: something a colleague can open, and a trace you can read when they
say it was wrong. {{topic:prodfeedback}} turns what you find there into the next test case. And
{{topic:foundryagents}} found that a hosted agent has no canary, so after release the trace is how you
see what a bad version did.

## How it works

### Server-side first, client-side second

<!-- volatile verified=2026-11 -->
"Tracing is generally available for prompt and hosted agents. Workflow and external agents are in
preview." The page's advice is to start server-side: Foundry "enables it automatically after you connect
an Application Insights resource to your project", with "no code changes", for "any agent hosted in
Foundry". Traces for prompt agents, hosted agents and workflows are available for the past 90 days.
<!-- /volatile -->

When you need to see your own logic around an agent call, add client-side instrumentation. For Python the
page installs OpenTelemetry and the Azure SDK's tracing plugin.

```powershell
pip install azure-ai-projects opentelemetry-sdk azure-core-tracing-opentelemetry
```

For development there is a third route. The Foundry Toolkit for Visual Studio Code traces locally into
an OTLP-compatible collector with no Application Insights, though "model and tool calls can still use
cloud services and incur charges".

### Connecting it

<!-- volatile verified=2026-11 -->
With the New Foundry toggle on, open the project, select **Build > Agents**, then **Traces**, and
**Connect** an Application Insights resource, new or existing. If the button is missing, use **Manage >
Project details > Connected resources > Add connection**. To query the telemetry you need the Log
Analytics Reader role on the connected resource, and Privileged Monitoring Data Reader as well if the
underlying tables are protected. Foundry stores traces there by using OpenTelemetry semantic conventions.
<!-- /volatile -->

### Reading a trace

The Traces tab lists runs you can search, filter and sort. Open one to step through its spans. The
conversation view starts from a Response ID or a Trace ID and shows the history, the response and its
tokens, "ordered actions, run steps, and tool calls", and the inputs and outputs between user and
agent. The traces sit in Application Insights, so Azure Monitor can query them too.

### What a trace holds, and who reads it

The page's warning is blunt: "Tracing can capture sensitive information, such as user inputs, model
outputs, and tool arguments and results." Its practices are to keep secrets out of prompts, arguments
and span attributes, to redact or minimise personal data before it reaches telemetry, and to "apply the
same access controls and retention policies you use for logs and metrics". Retention follows the
Application Insights and Log Analytics configuration. Whoever holds the reader role can read every
conversation, so the role is the access control.

### Copilot Studio's telemetry

This page's scope is the standard harness. You paste an Application Insights connection string under
**Settings > Advanced**, then choose what to log.

| Setting | Logs |
|---|---|
| Enable logging | Details of incoming and outgoing messages and events |
| Log conversation details | User ID, user name and message text, and with OpenTelemetry tracing on, "tool input arguments and tool output results captured in spans" |
| Log sensitive Activity properties | Values of properties that could be sensitive |
| Node execution events | An event each time a topic node runs |

Queries are Kusto over `customEvents`. Test-canvas conversations are logged too, so filter on the
`designMode` custom dimension. A count of unique users is only right for authenticated users with stable
IDs. A **Copilot Studio Dashboard** workbook (preview) shows conversations, latency, exceptions and tool
usage, and viewers need at least Reader on the Application Insights resource. An administrator can stop
makers connecting at all by blocking the *Application Insights in Copilot Studio* connector in a data
policy.

## In practice at Technik

The capstone's hosted agent gets tracing in stage 5 as a portal step, since azd's project schema has no
Application Insights setting. `base.bicep` creates the resource, and the reader connects it under
**Agents**, then **Traces**. The hosted code adds no instrumentation.

*From [`README.md`, lines 227–231](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/README.md#L227-L231):*

```powershell
azd ai agent invoke "Which documents does operation 0010 of work order 100004510 use?"
```

Suppose a planner says the assistant named the wrong work instruction for that operation. The
conversation view answers the questions in order. Did the agent call `list_operation_documents`, and
with which work order and sequence? What did it return? Did the agent call `get_revision_status`
afterwards, and did the answer use its result? A wrong answer with the right result in the trace is a
model fault. A wrong result is a tool or data fault, and `100004510` is a seed work order on superseded revisions.

`doc-01` returns a document owner's name as a tool result, so a trace holds personal data, and the Log
Analytics Reader assignments on the resource are the list of who may read it. Decide that list before
the first user.

<!-- unknown since=2026-11 -->
The README says the hosted agent "already emits OpenTelemetry", and the page describes server-side
traces that need no code. Which of the two produces the spans you read is not stated. The server on
Container Apps is a separate process with no logging or tracing in `server/teamcenter.py`, and nothing
documents whether the toolbox carries trace context to it. The trace may show the tool call and nothing
of what happened inside it, and the capstone never ran live.
<!-- /unknown -->

<!-- unknown since=2026-11 -->
Both Copilot Studio pages describe the standard harness. Whether an agent on the GitHub Copilot
harness, which is what the Production Assistant is, can connect Application Insights, or sends the
same telemetry, is not documented on either.
<!-- /unknown -->

## Design guidance

- **Start server-side**, and add client-side tracing only where your own code needs to appear.
- **Decide who may read traces** before connecting the resource, and grant the role to named people or one small group.
- **Keep secrets and personal data out of what the agent sends** to tools and prompts, since the trace copies it.
- **Verify with one deliberate run** and a look at Traces.
- **Filter test traffic** out of production questions, with `designMode` in Copilot Studio.
- **Put the Response ID in every incident report**, so the conversation is one search away.
- **Decide what "Log conversation details" costs you** before turning it on or off.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| No traces in the portal | Not connected, no recent traffic, or ingestion delay | Confirm the connection, send traffic, refresh after a few minutes |
| Authorization errors on telemetry | Missing roles on Application Insights or Log Analytics | Assign Log Analytics Reader, and Privileged Monitoring Data Reader if tables are protected |
| Client-side spans missing | Instrumentation not installed or configured | Recheck the packages and the SDK guidance |
| Sensitive content in traces | Prompts, arguments or outputs held it | Redact before it enters telemetry |
| Copilot Studio counts include testing | The test canvas is logged too | Filter `designMode` |
| Tool inputs vanish from Copilot Studio spans | "Log conversation details" is off | Weigh visibility against the data it writes |
| Makers cannot connect Application Insights | A data policy blocks the connector | Ask the administrator, or use another route |

## Key terms

**Trace** — the record of one run, made of spans.

**Span** — one step in a trace, such as a model call or a tool call, with its timing and status.

**Server-side tracing** — traces Foundry records for a hosted agent without code, once Application Insights is connected.

**Client-side instrumentation** — OpenTelemetry code in your own application, adding spans around the agent call.
