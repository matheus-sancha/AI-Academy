## TL;DR

{{topic:solutions}} taught what a solution carries. This lesson is about what it does not carry, and how
the values inside it behave on the way. An **environment variable** is two records: a *definition* that
travels with the solution and a *value* that belongs to the environment it lands in. Export without the
current value, and the importer is asked for one. Some parts of a Copilot Studio agent are not
solution-aware at all: Application Insights settings, authentication, channels and sharing. Every
deployment therefore ends with a short manual checklist. The solution is half of a release, and that
checklist is the other half.

## Why it matters

The first deployment usually looks fine. The solution imports and the agent appears. The failures arrive a
week later and look unrelated: an approval flow writing to the development site, an agent nobody can open,
traces that never reach Application Insights. They share a cause. Something the author assumed travelled
stayed behind, or travelled with the wrong value. The pipelines in {{topic:pipelines}} automate the move.
They do not tell you what is in it, so it is worth learning by hand once.

## How it works

### One variable, two records

An environment variable keeps a key and a value apart from the components that use them, so the value can
change without touching them. Microsoft's page lists six data types: decimal number, text, JSON, two
options, data source and secret. A secret reads from Azure Key Vault, and {{topic:connrefs}} covers that
setup and why it is not a connection reference. A *data source* variable holds what a connection does not,
such as a SharePoint site and list: the connection supplies a credential, the variable names the place.

The record split is where deployments go wrong. The **definition** holds the name, the type and an
optional **default value**. The **current value** is a separate record, and when one exists it wins over the
default. Microsoft's advice is explicit: include the definition in the solution, and provide the value for
the target at deployment. The definition then arrives as a managed object and the value stays an
unmanaged record.

<!-- volatile verified=2026-11 -->
To keep a value out of an export, open the variable, choose **Current Value** > **…** > **Remove from this
solution**. The value stays in development and the export carries none. At import the maker is prompted,
and a prefilled value carries a label saying where it came from: the solution, the target environment or
the default.
<!-- /volatile -->

Four consequences follow from that split, and each is stated on the page.

- **A managed solution hides the value.** You see it only from the Default solution, because a value is
  "an unmanaged customization".
- **A value that arrived in a managed solution is deleted by an upgrade.** Update the source solution to
  exclude it, export again, and import as an *upgrade*, not an update.
- **A deleted value fails quietly.** Unless a dependency blocks the deletion, the runtime uses the last known value.
- **A change is not instant.** It can take up to an hour to reach canvas apps and cloud flows, because the
  value is pushed asynchronously.

Values are limited to 2,000 characters, and nothing in Dataverse validates one set through code. SharePoint
variables need matching metadata in both environments: a list rebuilt by hand gets different internal
names, and a site duplicated and copied does not.

<!-- unknown since=2026-11 -->
The environment-variable page names canvas apps, cloud flows, plug-ins and Power BI as consumers and never
mentions an agent. A variable used by an agent's flow tool is covered by extension. Whether a knowledge
source or an agent setting can read one is not documented.
<!-- /unknown -->

### What a solution does not carry

Microsoft's Copilot Studio guidance lists the items that are **not solution-aware**: they "don't follow the
normal solution deployment process" and need steps in the downstream environment. They are Application
Insights settings, manual authentication settings, Direct Line and web channel security settings,
deployed channels, and sharing with makers or users. A solution that imports cleanly has therefore not yet
produced a working agent.

### The rules, and where the pages disagree

The same page gives seven golden rules: do not customise outside development, always work in solutions,
use your own publisher and prefix, split solutions only to deploy parts independently, use variables for
settings and secrets that change, export and deploy as managed except for development, and consider
automating. It asks for at least three environments, production as the production type and the rest as
sandboxes, and an Entra security group on each.

<!-- unknown since=2026-11 -->
The pages disagree on the development environment. The ALM guidance makes it a sandbox and wants a
security group on it. The pipelines overview's example makes it a Developer environment, and {{topic:envs}}
says a Developer environment cannot take a security group. Neither page says which to prefer, and neither
explains **layering**, the roadmap's other promise here: what a managed component looks like once someone
edits it downstream. The one case on the pages is the value, an unmanaged layer over a managed definition.
<!-- /unknown -->

## In practice at Technik

The *Technik Production Assistant* solution from {{topic:solutions}} holds three variables.

| Variable | Type | Why it is a variable |
|---|---|---|
| `tke_SnowflakeWarehouse` | Text | `TECHNIK_AGENT_WH` everywhere today, named so it can differ |
| `tke_ApprovalsSite` | Data source | The SharePoint site the approval flow writes to |
| `tke_ApprovalsList` | Data source | The list on that site |

The first import into *Technik Agents Test* went wrong in a way no error reported. The engineer had
exported with the current values still in. The prompt prefilled both approval variables with a label
reading *solution value*, nobody read the label, and test approvals landed in the development site's list.
The fix was upstream: remove the two values before export, so the prompt is empty. The second problem was
the test list itself, which someone had rebuilt by hand. Its internal names differed, and the flow failed
until the site was duplicated and copied instead.

Then the checklist. After every deployment to *Technik Agents*, the engineer works through five items.

| Item | At Technik |
|---|---|
| Application Insights | Connect it, since {{topic:tracing}} depends on it |
| Authentication | Set Microsoft Entra sign-in again |
| Channels | Deploy to Teams |
| Sharing | The four security groups, one per user group ({{topic:share}}) |
| Direct Line and web channel security | Nothing to do, since the data policy blocks Direct Line and unauthenticated chat ({{topic:dlpdesign}}) |

## Design guidance

- **Provide values at import, never in the export.** Remove each current value from the solution first.
- **Make anything that differs a variable**, even if it matches today. A fixed value costs a rebuild when it changes.
- **Read the source label on every prefilled value** during an import.
- **Copy a SharePoint site rather than rebuilding it** when a variable points at its list.
- **Keep the post-deployment checklist in the repository**, next to the solution, and review it with the same care.
- **Test the deployed agent in a new conversation as a real user**, because sharing and authentication are exactly what did not travel.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Test writes to development data | The export carried the current value | Remove the value, and prompt at import |
| A flow breaks on a list that looks identical | Rebuilt by hand, so internal names differ | Duplicate and copy the site |
| Nobody but the maker can open the agent | Sharing is not solution-aware | Share it in the target, per the checklist |
| A value cannot be deleted in production | It arrived in a managed solution | Remove it in the source and import an upgrade |
| A changed value seems ignored | Propagation is asynchronous | Wait up to an hour, then retest |
| Traces are missing after a release | Application Insights settings stayed behind | Connect them again |

## Key terms

**Environment variable**: a named setting kept apart from the components that use it.

**Definition and current value**: the setting that travels, and the record that belongs to one environment.

**Default value**: what is used when an environment has no current value.

**Solution-aware**: carried by export and import. Application Insights, authentication, channels and sharing are not.

**Post-deployment step**: a setting made by hand in the target environment after an import.
