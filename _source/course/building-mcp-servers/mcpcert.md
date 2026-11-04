## TL;DR

Microsoft's MCP server certification is a **marketplace gate**, not a quality bar you can apply to
your own work. It "gives customers and administrators confidence that an external service meets
Microsoft expectations for reliability, security, compliance, and responsible operation before it is
broadly available" — and only a **verified publisher** that owns the endpoint may submit. Two answers
in its own FAQ are worth more than the badge: DCR "isn't supported today", and neither is PKCE.

## Who may actually submit

<!-- volatile verified=2026-11 -->
Certification is in preview, with "only a limited number of submissions" processed and a legacy path
open through **18 November 2026**. Eligibility is organizational: a Microsoft Partner Center account
with completed business verification, enrolment in the Microsoft 365 and Copilot program, and
ownership of the endpoint. The exclusion is explicit — "If you're an independent publisher who
doesn't own the underlying service, you're not eligible to submit directly."

The package: a manifest, a tool-definition file, an optional `intro.md`, public documentation, icons
and support links, and an **Azure Key Vault** holding the OAuth secrets under exact, case-sensitive
names (`ClientId`, `ClientSecret`, `TokenUrl` and so on), readable by a fixed Microsoft service
principal. Then six stages: prepare, submit an intake form, automated validation, a functional and
safety review covering "authentication, security, compliance, telemetry readiness, and responsible AI
considerations", publishing, and maintenance — "Resubmit updates when introducing new tools".
<!-- /volatile -->

## Where it parts company with the specification

The FAQ is blunt: no DCR, no PKCE. Hold that against {{topic:mcpauth}}, where clients "**MUST** use
the `S256` code challenge method when technically capable" and **MUST refuse to proceed** when PKCE
support is not advertised. So the certified path is neither the specification's recommended path nor
Copilot Studio's convenient one, which needs the DCR this process rejects ({{topic:mcpcs}}).
Snowflake's managed server also declines DCR
({{topic:sfmcp}}). Three surfaces, three answers, none of them the spec's — the useful fact to carry
out of this lesson.

## At Technik

Technik's server is internal and Technik publishes nothing to other organizations, so it is not
eligible. That is right rather than a gap: certification does not measure whether a server is good,
only whether it is safe to list.

What transfers is the checklist: structural validation automated in CI, then a human pass over
authentication, telemetry and responsible-AI behaviour ({{topic:cicd}}). The post-certification duties transfer too: keep the implementation
aligned with its documentation and re-review when tools are added — the discipline {{topic:mcpcs}}
showed you cannot get from the platform. One tip is worth stealing outright: keep a *known issues and
limitations* section, so consumers learn your server's edges from you rather than from a failure.

And {{topic:mcpadd}}'s advice to prefer "certified or internally approved servers" resolves here:
for anything you build yourself it is always the second half.

## Key terms

**Verified publisher** — an organization with a business-verified Partner Center account, enrolled in
the Microsoft 365 and Copilot program, that owns the endpoint it submits. The eligibility floor for
certification.

**Certification package** — the manifest, tool definitions, documentation, icons and Key Vault
authentication configuration submitted for review, which the running server must stay aligned with
afterwards.
