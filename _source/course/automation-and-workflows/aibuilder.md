## TL;DR

AI Builder is the Power Platform's catalogue of ready-made AI. It covers document models (invoices,
receipts, IDs, custom forms), text models (classification, entity extraction, sentiment, translation),
image models, prediction and prompts. Each one is used as a step in Power Automate, Power Apps and
Copilot Studio flows. Models are **prebuilt** (use them as they are) or **custom** (train them on your own
examples). It is the shortest way to put one AI step into a process that already exists. Check the billing
before you build. Inside Copilot Studio it always runs on **Copilot Credits**, and seeded AI Builder credits
end on **1 November 2026**.

## Why it matters

Most AI work in a business process is narrow. Read the fields off a certificate, sort a comment into a
category, detect the language of an email. None of that needs an agent. It needs one well-defined step
that returns a predictable shape, and AI Builder is a shelf of exactly those steps.

The other reason to know it is money. AI Builder has had its own currency, **AI Builder credits**, which is
being replaced by **Copilot Credits**, and the two coexist for now. A flow that runs fine for a month can
stop on the first of the next one with an error that reads like a fault. In fact the environment has used
up what it was allocated. A team that never asked which currency it pays in finds out that way.

## How it works

### The catalogue

| Data | Prebuilt models | Custom models |
|---|---|---|
| **Documents** | Invoices, receipts, IDs, business cards, contracts, text recognition | Document processing, for your own forms |
| **Text** | Category classification, entity extraction, key phrases, language detection, sentiment, translation | Category classification, entity extraction |
| **Structured data** | — | Prediction, from your own history |
| **Images** | Image description, text recognition | Object detection |
| **Generative** | Prompts | — |

Use **prebuilt** models for problems every business has, and **custom** ones for data unique to yours.
Custom models are built from **AI hub → AI models** in Power Apps or Power Automate: choose a type, connect
examples, train, publish. Training and testing are free.

Prompts belong to the same family and have a lesson of their own ({{topic:prompts}}). Document processing
with validation and review is covered in {{topic:docproc}}.

### Where it runs, and on which currency

| Used in | Pays with |
|---|---|
| Power Automate cloud flows, Power Apps | AI Builder credits first, then Copilot Credits if those run out |
| Copilot Studio agents and agent flows | **Copilot Credits only** |
| A cloud flow converted to an agent flow | Copilot Credits only, from the conversion on |

<!-- volatile verified=2026-10 -->
AI Builder credits come from an **add-on** of 1,000,000 a month or **seeded** in some licences, such as
5,000 with Power Automate Premium. **Seeded credits are removed on 1 November 2026.** Existing customers can
renew the add-on until then, and new customers can no longer buy it and buy Copilot Credits instead. Credits
reset on the first of each month and do not carry over.
<!-- /volatile -->

Admins either **allocate** AI Builder credits to an environment or leave them in a tenant pool. An
environment with an allocation uses only its allocation. When it runs out, the system tries Copilot Credits.
If there are none, AI Builder steps fail with `EntitlementNotAvailable` or `QuotaExceeded`.

Copilot Credit rates are per unit of work. Basic text and generative tools cost 0.1 Copilot Credits per
1,000 tokens. **Content processing**, which covers document models, costs **8 Copilot Credits per page**.
A detail that is easy to miss: in agent flows, prompts and models consume Copilot Credits **even from the
test panel or the designer**.

Two licensing side-effects are documented too. An AI Builder action in a Power Automate flow does not make
the flow premium. In a Power Apps app it makes the app premium, and so does a flow with an AI Builder action
called from the app.

## In practice at Technik

Supplier material certificates arrive as PDFs, one per heat of material, in each supplier's own layout.
Quality checks a few values against the order, such as material grade, heat number and a handful of
mechanical properties. The ten sample certificates Technik keeps show the problem: the fields are the same
and their positions are not.

That places the model on the shelf:

| Option | Fit |
|---|---|
| Invoice processing (prebuilt) | No. A certificate is not an invoice, and its fields are not invoice fields |
| Text recognition (prebuilt) | It returns all the text, and something else still has to find the fields |
| **Document processing (custom)** | **Yes.** Trained on the supplier layouts, it returns named fields with confidence scores |

Before anyone builds it, the cost is a calculation, not a surprise. Assume 300 certificates a month at two
pages each, processed in an agent flow:

| | |
|---|---|
| Pages a month | 300 × 2 = 600 |
| Copilot Credits a month | 600 × 8 = **4,800** |
| Plus | The flow's own actions ({{topic:agentflows}}) and any test runs, which are charged |

Built as a Power Automate cloud flow instead, the same work would draw on AI Builder credits while
Technik has any allocated, and on Copilot Credits after that. After 1 November 2026 only add-on credits
remain, so the two paths cost the same currency sooner than most plans assume.

<!-- unknown since=2026-10 -->
What a Developer Plan environment offers for AI Builder once seeded credits end. {{topic:devenv}} found
AI Builder absent from the plan. Whether a Copilot Credit trial covers it has not been checked.
<!-- /unknown -->

## Design guidance

- **Reach for AI Builder when the AI is one step**, with a known input and output shape.
- **Prebuilt first, custom when the layout or vocabulary is yours.**
- **Ask which currency the environment pays in** before the first run, and again after 1 November 2026.
- **Cost document work by the page.** Multiply pages by the rate before you promise a volume.
- **Budget for tests inside agent flows.** They are charged.
- **Treat extraction as a draft**, never as data that is already validated ({{topic:docproc}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| AI steps fail with `QuotaExceeded` late in the month | The environment used its allocation and has no Copilot Credits to fall back on | Reallocate credits, add Copilot Credits or enable pay-as-you-go |
| A working flow fails from 1 November 2026 | It relied on seeded AI Builder credits | Plan for add-on credits or Copilot Credits now |
| An app suddenly needs premium licences | An AI Builder action was added to it or to a flow it calls | Expect it, and license for it |
| Test runs show up on the bill | Models and prompts in agent flows are charged even in tests | Test in the AI models page or prompt builder, which are free |
| A prebuilt model misses half the fields | The document is not the type the model was built for | Train a custom document processing model |
| Credits unused in March are gone in April | Monthly reset, no carry-over | Size the allocation to the monthly peak |

## Key terms

**AI Builder** — the Power Platform's catalogue of prebuilt and custom AI models used inside flows and apps.

**Prebuilt model** — a ready-to-use model for a common task.

**Custom model** — a model trained on your own examples.

**AI Builder credit** — AI Builder's own capacity currency, being retired in favour of Copilot Credits.

**Copilot Credit** — Copilot Studio's capacity currency, and the only one AI Builder uses inside Copilot
Studio.

**Content processing** — the Copilot Credit rate for document and image models, charged per page or
image.
