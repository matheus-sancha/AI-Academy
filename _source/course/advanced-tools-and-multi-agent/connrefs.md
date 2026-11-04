## TL;DR

A connection holds a credential; a connection reference is "a solution component that contains a
reference to a connection about a specific connector", and solution-aware flows and apps "bind to a
connection reference instead of directly to a connection". That indirection is what lets one solution
move between environments and pick up each one's own credential. What it does *not* do is make the
credential non-human: enabling a flow still needs someone who owns every connection, and the only
documented way to make that someone a machine is to share the connection with "a user representing a
service principal".

## Why it matters

{{topic:connauth}} named the choice — a connection runs as the end user, or as the maker or a service
account — and called getting it wrong "the single most common reason an agent that worked for its
author breaks the day it is shared". This lesson is the mechanism underneath that sentence, and where
{{topic:envs}} and {{topic:solutions}} stop being administrative trivia.

The rule is simple once stated: "Flows created outside a solution use connections directly. Flows
created in a solution use connection references." So anything you intend to ship has to be born
inside a solution, because retrofitting is explicitly not automatic — "Canvas apps and flows added
from outside solutions will not automatically be upgraded to use connection references."

<!-- unknown since=2026-11 -->
Read the rest of this lesson knowing that its primary source never mentions agents: the words *agent*
and *Copilot* do not appear on the connection-reference page at all. Everything below applies to an
agent's connector tools by extension rather than by documentation, so confirm it in your own
environment before depending on it.
<!-- /unknown -->

## How it works

### What moves, and what stays

The payoff is one sentence: "During solution import into a target environment, a connection is
provided for all the connection references so any referencing flows can be turned on automatically
after the import completes." The solution carries the *shape* of the dependency; each environment
supplies the credential. To repoint something later "you edit the connection reference component
within the solution" rather than touching the flow.

<!-- volatile verified=2026-11 -->
Create one explicitly from a solution with **New** > **More** > **Connection Reference**, giving it a
display name, a connector and a connection. One also appears on its own: "A connection reference is
automatically created when you create new connections from the flow designer or Power Apps Studio."
Power Automate will even reuse an existing one — "Power Automate will try to reuse existing
connection references from the current solution or other solutions before creating a new connection
reference" — which is how a reference ends up outside the solution that needs it.
<!-- /volatile -->

### Who turns it on

Here is where the indirection stops. "When a flow is turned on (enabled), the user turning on the
flow needs to own or have permission to use all the connections in the flow." The usual remedy is
"having the flow owner create the connections inside all the connection references that the flow
uses"; otherwise "the flow needs to be turned on by the owner of those connections or the connections
need to be shared with the user who is turning on the flow".

The service-principal path exists, but it is narrow and it is a *sharing* operation rather than a
binding one: "OAuth connections can only be explicitly shared with a user representing a service
principal", at **Can use** permission, done by hand on the connection or through the **Edit Connection
Role Assignment** action. And a reference cannot be handed over afterwards — ownership "can't be
transferred to another user from the Solutions area in Power Apps". So plan the owner before the
first import, not after.

### Secrets are a separate mechanism

The roadmap puts environment variables next to connection references, and they are worth keeping
apart. A connection reference points at a *connector's* credential. An environment variable secret is
"a special type of environment variable" that "makes a secure connection to Azure Key Vault to
retrieve secrets" — a value *your logic* reads, not one the platform authenticates with.

<!-- volatile verified=2026-11 -->
Setting one up is mostly Azure work. The vault needs the **Key Vault Secrets User** role granted to
the reading user *and* to "the application named Dataverse", plus a matching access policy for each,
and the subscription needs `Microsoft.PowerPlatform` registered as a resource provider. The variable
itself takes **Data Type: Secret**, **Secret Store: Azure Key Vault**, then the subscription id,
resource group, vault name and secret name. A flow reads it through the Dataverse **Perform an
unbound action** step `RetrieveEnvironmentVariableSecretValue`.
<!-- /volatile -->

One detail is load-bearing: **Secure Inputs** and **Secure Outputs** hide the value from run history
going forward, and "Prior flow runs will still expose the secret value." Switch them on before the
first test, not after.

### Custom connectors break the pattern twice

Both known issues on the page are about {{topic:customconn}}. "Custom connectors need to be imported
in a separate solution, before connection references or flows", and after a copy-environment
operation "a new connection reference must be created to the new custom connector", with every app
and flow using the old reference needing repair. Canvas apps are worse still: they "don't recognize
connection references on custom connectors" and need the connection removed and re-added after
import. A custom connector you build therefore carries an ALM cost that a prebuilt one does not
({{topic:solutionsdeep}}, {{topic:pipelines}}).

## In practice at Technik

Technik's Production Assistant reads Snowflake through the connector in {{topic:sfconnector}}, and
the scenario fixes the identity: one read-only role, `TECHNIK_AGENT_RO`, held by the service user
`TECHNIK_AGENT_SVC`. Three environments mean three Snowflake accounts and three sets of credentials,
and exactly one solution component should know that: a `Technik Snowflake (Agent)` connection
reference, bound per environment at import.

The credential itself belongs in Key Vault, with a different secret per environment — and a separate
vault for production, so that reading the test secret is not an accident away from reading the live
one. Technik's engineers never own that connection: it is created by the service principal and shared
to whoever activates, which is the one combination the page supports.

Two consequences follow. {{topic:testidentity}}'s question gains a new answer — the test runs as
`TECHNIK_AGENT_SVC` in *that* environment, so a pass in dev proves nothing about production's grants.
And the `Technik Teamcenter Live` connector from {{topic:customconn}} inherits the rules above: ship
it in its own solution, ahead of everything that references it.

## Design guidance

- **Create inside a solution from the first day.** Retrofitting is manual and nobody budgets for it.
- **One connection reference per dependency per solution**, created deliberately, so Power Automate
  does not reuse one from somewhere you do not control.
- **Decide the owner before the first import.** Ownership cannot be transferred afterwards.
- **Use a service principal for anything an agent runs**, and share the OAuth connection to it
  explicitly — then govern it as an identity ({{topic:agentid}}).
- **Keep connector credentials and secrets separate.** A connection reference is for the former;
  Key Vault through an environment variable is for the latter.
- **Ship custom connectors in their own solution, first.** Both documented known issues here are
  theirs.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `ConnectionAuthorizationFailed` on activation | The activating user lacks rights to at least one connection | Have the connection owner activate it, or share the connection |
| The reference shows a red exclamation mark | "the underlying connection is in a bad state" | Re-authenticate the connection, then re-activate |
| Import leaves flows switched off | No connection was bound to a reference | Bind every reference, then activate as the connection owner |
| A canvas app ignores the reference | It is a custom connector, or an OAuth connection | Remove and re-add the connection in the app after import |
| Everything breaks after a copy environment | References still point at the old custom connector | Create new references and repair each consumer |
| A secret is readable in run history | Secure inputs and outputs were turned on later | Turn both on, and treat earlier runs as leaked |

## Key terms

**Connection reference** — the solution component a flow or app binds to instead of a connection, so
each environment can supply its own credential at import.

**Environment variable secret** — an environment variable whose value is a reference into Azure Key
Vault, read at run time through `RetrieveEnvironmentVariableSecretValue`.

**Can use** — the sharing permission granted on a connection, and the only documented route to
letting a service principal activate a flow it does not own.
