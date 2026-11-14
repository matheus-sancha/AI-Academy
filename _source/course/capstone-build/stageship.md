## TL;DR

Stage 5 deploys two things and ties them to one identity. The stage 2 server goes to Azure Container Apps over
stateless streamable HTTP, with its Snowflake key in Key Vault. The agent goes to Foundry as a hosted agent with its
own Entra Agent ID, and reaches the server through a Foundry toolbox. The server answers only an identity that holds
its `Teamcenter.Read` role, and you assign that role to the agent yourself after the first deploy. The release
workflow gates on the stage 4 evals before it deploys. You finish with something a colleague can open, and a trace
you can read when they tell you it was wrong.

## Why it matters

A hosted agent serves one version at a time, so there is no canary to catch a bad release. The judgement has to come
before the deployment, which is why the release is the evals first and the deployment second ({{topic:foundryagents}}).

The identity design is the other reason. A server that anyone with the URL can call is a public window onto
Technik's controlled documents. Here no token for the server's audience means no request, and a token is issued only
to an identity holding one role ({{topic:agentid}}). And tracing is a decision to take before the first user, not
after the first complaint ({{topic:tracing}}).

## How it works

### Two deployments, one identity

| Part | Where it runs | Authenticates how |
|---|---|---|
| The MCP server | Azure Container Apps, from `infra/base.bicep` and `infra/server.bicep` | Entra built-in authentication, role required. Snowflake with the key in Key Vault |
| The Foundry toolbox | The Foundry project, from `azure.yaml` | A connection that signs in as the agent's Entra Agent ID |
| The agent | A Foundry hosted agent, from `agent/hosted.py` and `azure.yaml` | The identity Foundry creates when it deploys the agent |

The agent no longer starts the server. It asks the toolbox, and Foundry calls the server with a token for the agent's
own identity.

### The server's side

Two Bicep files and a Dockerfile deploy it. `base.bicep` creates Key Vault, a container registry, the Container Apps environment,
Application Insights and the server's own Entra application. `server.bicep` creates the Container App. The server
runs `--http`, which is stateless, so any replica can answer any request ({{topic:transports}}). Two pieces of the
Bicep carry the design. *From [`infra/base.bicep`, lines 110–114](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/infra/base.bicep#L110-L114):*

```bicep
// Assignment required: Entra issues a token only to an identity that holds Teamcenter.Read.
resource serverPrincipal 'Microsoft.Graph/servicePrincipals@v1.0' = {
  appId: serverApp.appId
  appRoleAssignmentRequired: true
}
```

*From [`infra/server.bicep`, lines 49–56](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/infra/server.bicep#L49-L56):*

```bicep
      secrets: [
        {
          // The agent's Snowflake key, read from the vault by the server's identity. Never in the image.
          name: 'snowflake-private-key'
          keyVaultUrl: 'https://${keyVaultName}${az.environment().suffixes.keyvaultDns}/secrets/snowflake-private-key'
          identity: identityId
        }
      ]
```

The first makes the role mandatory. The second means the key lives in the vault, and the server's managed identity
reads it at start-up. The same file turns on Container Apps' built-in authentication with `Return401`, so a request
without a token is refused before your code runs ({{topic:mcpauth}}). Put the key in the vault before you deploy the
app:

```powershell
az keyvault secret set --vault-name <keyVaultName> -n snowflake-private-key --file keys/technik_agent_svc.p8
```

### The agent's side

*From [`azure.yaml`, lines 24–35](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/azure.yaml#L24-L35):*

```yaml
  # The stage 2 server on Container Apps. Foundry calls it with a token for the agent's identity.
  teamcenter:
    host: azure.ai.connection
    uses:
      - ai-project
    category: RemoteTool
    target: ${TEAMCENTER_MCP_URL}
    authType: AgenticIdentityToken
    audience: ${TEAMCENTER_AUDIENCE}
    env:
      TEAMCENTER_MCP_URL: ${TEAMCENTER_MCP_URL}
      TEAMCENTER_AUDIENCE: ${TEAMCENTER_AUDIENCE}
```

`AgenticIdentityToken` is the line that makes the agent its own caller, and no key or secret appears in the
connection. The toolbox and the agent that follow it in the file are in {{topic:foundryagents}}. *From [`agent/hosted.py`, lines 18–29](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/agent/hosted.py#L18-L29):*

```python
def host(client, tools):
    # Foundry keeps the conversation, so the model call stores nothing.
    return ResponsesHostServer(build_agent(client, tools, default_options={"store": False}))


if __name__ == "__main__":
    credential = DefaultAzureCredential()
    client = FoundryChatClient(project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
                               model=os.environ["MICROSOFT_FOUNDRY_MODEL_DEPLOYMENT_NAME"],
                               credential=credential, function_invocation_configuration=TOOL_LOOP)
    # The toolbox URL is built from FOUNDRY_PROJECT_ENDPOINT and TOOLBOX_NAME, so it follows the default version.
    host(client, FoundryToolbox(credential)).run()
```

This is stage 3's `build_agent`, called with a toolbox for its tools and wrapped in a Responses server. Nothing in the
agent changed, which is why the guard still applies.

### The guard's streaming half

<!-- unknown since=2026-11 -->
That the hosted server always streams its answer is the capstone's own finding, and only an in-process test
supports it. Check it on your first deployment.
<!-- /unknown -->

A guard that waits for the finished answer has nothing to check once the answer is already leaving in pieces. *From [`agent/main.py`, lines 35–41](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/agent/main.py#L35-L41):*

```python
    if not context.stream:
        refuse_unless_grounded(context.result)
        return
    # The hosted server always streams. Hold the updates until the answer is final, check it,
    # and release only what passed: the answer, or the refusal in its place.
    context.result = context.result.with_result_transform(refuse_unless_grounded).buffer_updates(
        result_to_updates=lambda r: [AgentResponseUpdate(role=m.role, contents=m.contents) for m in r.messages])
```

The streamed path holds every update, applies the same check to the final result and releases only what passed. The
price is that the user sees nothing until the answer is complete.

### The order, and the step everyone misses

The capstone's README has eight steps, and the order carries the design: the resource group and `base.bicep`, the key
into the vault, the server's image and Container App, the two values `azd` needs, `azd up`, the role, tracing, and a
question. Step 6 is the one that fails silently. Until the agent's identity holds the role, Entra refuses it a token
and every tool call fails. *From [`README.md`, lines 217–220](https://github.com/matheus-sancha/technik-capstone/blob/v1.0.0/README.md#L217-L220):*

```powershell
$agent = (azd ai agent show --output json | ConvertFrom-Json).instance_identity.principal_id
$body = @{ principalId = $agent; resourceId = "<serverPrincipalId>"; appRoleId = "<readRoleId>" } | ConvertTo-Json
az rest --method post --body $body `
  --url "https://graph.microsoft.com/v1.0/servicePrincipals/<serverPrincipalId>/appRoleAssignedTo"
```

<!-- unknown since=2026-11 -->
The property that holds the agent's identity in that output, and the identity the server then sees, come from the
capstone's README and have not been run. Check both, and trust what Entra shows you.
<!-- /unknown -->

### The release, and the trace

The release workflow runs the stage 4 evals as its gate, then `azd deploy` creates a new agent version, then Foundry's
Action compares it with the one before and reports in the run summary ({{topic:cicd}}). The Action has no threshold,
so the gate that blocks is yours. The capstone never sets `SHIP_LIVE`, so its own release skipped both jobs.

Tracing is a portal step. In the Foundry project you connect the Application Insights resource that `base.bicep`
created, and the hosted code adds no instrumentation.

<!-- unknown since=2026-11 -->
The portal path to **Traces** and the connection-string injection come from the capstone's README and were not
checked against the portal. What a trace shows of the server's own work is also open ({{topic:tracing}}).
<!-- /unknown -->

## In practice at Technik

You finish holding a Container App that answers 401 to anyone without the right token, a Foundry project whose agent
holds `Teamcenter.Read`, and one command:

```powershell
azd ai agent invoke "Which documents does operation 0010 of work order 100004510 use?"
```

Ask a colleague who has access to the project to open the agent in the portal's playground and ask something else.
When they report a wrong answer, open its trace and ask three things in order. Did the agent call
`list_operation_documents`, and with which arguments? What did the server return? Did the answer use the result? That
sequence separates a model fault from a data fault.

## Design guidance

- **Judge before you deploy.** A hosted agent has no canary, so the gate comes first.
- **Make the server refuse by default.** No token, no role, no request.
- **Put every secret in a vault**, and let the server's identity read it.
- **Give the agent its own identity** and assign it the one role it needs, by hand and on the record.
- **Turn on tracing before the first user**, and decide who may read traces.
- **Keep the guard on the streamed path.** Hold, check, release.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Every tool call fails after `azd up` | The agent's identity has no `Teamcenter.Read` role | Run step 6 ({{topic:foundryagents}}) |
| A browser or `curl` gets 401 from the server | Built-in authentication refuses an unauthenticated caller | That is intended. Test through the agent |
| The server rejects the request's host name | The allowed host is not the app's own fully qualified name | Set `MCP_ALLOWED_HOSTS` to it, as `server.bicep` does |
| The release skips both jobs | `SHIP_LIVE` is not set | Set it to `true` once you want a live release |
| The trace view is empty | Application Insights was never connected to the project | Connect it in the portal |
| An answer arrives all at once | The guard holds a streamed answer until it is final | That is the guard working |

## Key terms

**Hosted agent**: your code running in Foundry Agent Service as a container, with an identity of its own.

**Toolbox**: a Foundry resource that gives an agent a set of tools, here the server behind one connection.

**App role**: a permission an application identity must hold before Entra issues it a token for an API.

**Streaming guard**: the check that holds a streamed answer until it is final, then releases it or the refusal.
