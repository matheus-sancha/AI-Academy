## TL;DR

{{topic:computeruse}} told you to treat computer use as a last resort. Hardening it for production
means accepting that almost none of its controls is a guarantee. Access control "doesn't stop the
model from opening" a blocked site. Human supervision "might not trigger in every situation where a
person would want a pause". And "it adapts to interface changes" sits beside its own FAQ's
"Sensitive to interface and timing changes." What you actually harden is the machine.

## What the settings do and do not promise

<!-- volatile verified=2026-11 -->
**Credentials to use** chooses between **Maker-provided credentials** — the default, "suitable for
autonomous agents", warning that "anyone using it can act with the original author's access on the
configured machine" — and **End user credentials**. **Stored credentials** hold per-site passwords,
in "Power Platform internal storage (no configuration required)" or a Key Vault you supply, replayed
"if a sign-in prompt appears". Models run from OpenAI's CUA to experimental Claude Opus 4.6, at "5
Copilot Credits, or 15 Copilot Credits when using a premium model" per step.
<!-- /volatile -->

Read both guardrails precisely. **Access control** governs *actions*, not reachability: it "only
prevents the model from taking actions on websites or applications that aren't in the allow list",
and the docs' own example is the model reaching Bing from the Edge search bar. **Human supervision**
is probabilistic — you "shouldn't rely on clarification requests as a safety fail-safe" — yet not
optional either: "If you don't configure reviewers, these requests have nowhere to be routed, so the
session fails when the agent pauses."

This is {{topic:permissions}}' lesson one layer out: the features that look like boundaries are not
sold as boundaries. The documented mitigations are all environmental — "Use dedicated machines for
computer use", a limited account, allow-listed sites and apps — and, because hidden commands arrive
in screenshots and pages, "trusted, isolated environments" ({{topic:ctxsecurity}}).

## Where it runs

Windows 365 for Agents supplies "secure, on-demand Cloud PCs that have a managed identity, device
posture, and a governed agent session lifecycle", checked out per task and reset after.

<!-- unknown since=2026-11 -->
How that composes with stored credentials is undocumented — one page says passwords are kept and
replayed at sign-in prompts, the other that no credentials persist and interactive authentication is
replaced outright. Session length, timeouts, concurrency and log retention are unstated too, and
everything here is standard-harness only.
<!-- /unknown -->

## At Technik

Supplier material certificates arrive through a portal with no API — the one case where this earns
its place. Run it on a dedicated Cloud PC, with that portal and nothing else allow-listed, under an
account that can read certificates and post nowhere, and with a named reviewer. Then budget it: at
five credits a step, one login-navigate-download sequence costs more than the connector it stands in
for — so build that connector ({{topic:customconn}}) the day the portal offers an API.

## Key terms

**Access control** — the allow list of sites and apps the model may *act* on. It prevents nothing
from being opened.

**Human supervision** — an email review request raised when the agent pauses. Mandatory to configure,
model-triggered, and explicitly not a fail-safe.
