## TL;DR

AI Builder document processing reads a file, such as an invoice, a receipt, an ID or your own form, and
returns **named fields**, **tables** and a **confidence score** for each value. Prebuilt models cover common
documents, and custom models are trained on yours. Extraction is the easy part. A score says how sure the
model is that it *read* a value, not whether the value is *acceptable*. So a document flow has three stages:
**extract**, **validate** the values against data you trust, and **review**, where a person decides before
anything reaches a business system.

## Why it matters

Typing values off documents is slow and error-prone, and document models do it in seconds. That speed is
dangerous in a process that trusts the result. A model that misreads `345` as `545` with high confidence
produces a clean record with a wrong number in it, and nothing downstream knows the difference.

The engineering is around the model: knowing which fields it is unsure of, checking values against rules and
reference data, and routing what fails to a named person. A flow that skips those stages has only moved the
typing errors somewhere harder to see.

## How it works

### What a model returns

The prebuilt invoice processing model shows the shape every document model shares:

| Output | Example |
|---|---|
| **Fields** | `InvoiceId`, `InvoiceDate`, `VendorName`, `InvoiceTotal`, `AmountDue`, about thirty more |
| **Tables** | `Items`, with description, quantity, unit price and amount for each line |
| **Confidence score** | Between 0 and 1, for every field and table cell |
| **Key-value pairs** | Every label and value detected, including fields the model does not define |
| **Detected text** | The raw OCR of the whole document |

In Power Automate it is one action, **Extract information from invoices**, given the file's content. Its outputs
are dynamic content for later steps.

<!-- volatile verified=2026-10 -->
Files must be JPEG, PNG or PDF, at most 20 MB, one document per file. For a PDF, only the first 2,000 pages are
processed. Calls are limited to 360 per environment per 60 seconds, across all document processing models.
<!-- /volatile -->

### Prebuilt, custom, or both

When the prebuilt model misses a field or misreads a layout, there are three documented routes. A **custom
invoices model** adds fields and examples to the prebuilt one. The **detected text** can be searched for a
simple value. A **custom document processing model** can be trained on your own documents.

Models also combine in one flow. Microsoft's examples call a custom model only for vendors whose invoices carry
an extra field. One retries with a custom model when a field's confidence is below 0.65, and another uses the
prebuilt model as a fallback for layouts the custom model was never trained on.

### Confidence, validation and review

These are three different questions, and each needs its own stage:

| Stage | Asks | Catches | Misses |
|---|---|---|---|
| **Confidence** | Did the model read this value clearly? | Smudged scans, odd layouts, fields it could not find | A value read wrongly with high confidence |
| **Validation** | Is the value well formed, consistent and allowed? | Wrong format, totals that do not add up, values outside limits, duplicates | A plausible value that is still wrong |
| **Review** | Does a responsible person accept it? | Whatever the first two let through | Nothing, if the reviewer has what they need |

The confidence check is a threshold. A common pattern collects each field's score, filters for those below the
threshold and lists their names on the record, marking it **Needs review**. There is no correct threshold to
copy: Microsoft's examples use 0.65 and community patterns use 0.75. Set yours from test documents.

Validation compares extracted values with something you already trust, such as an order, a master list or a
specification. Review is a status and a named person, not an email to a shared mailbox ({{topic:hitl}}).

Store extracted identifiers as **text**. A number column drops leading zeros and rejects identifiers with
letters in them.

## In practice at Technik

Supplier material certificates arrive as PDFs in a SharePoint library, one per heat of material. Quality
inspects each one before the material is accepted. {{topic:aibuilder}} chose a custom document processing model
for them, because every supplier's layout differs. This is the cloud flow around that model:

| Step | Does |
|---|---|
| Trigger | A file is created in *Incoming certificates* |
| Extract | Custom model returns `SupplierName`, `CertificateNo`, `HeatNo`, `Grade`, `YieldStrength`, `TensileStrength`, `Elongation` |
| Confidence | Any field below **0.80** is added to `FlaggedFields` |
| Validate | Required fields present. `CertificateNo` not already registered. `Grade` and the strength minimums match Technik's purchase specification for the bar. Tensile strength above yield strength |
| Record | A row in the *Certificate register*, status **Needs review** with the reasons, or **Ready for sign-off** |
| Review | A quality inspector opens the certificate beside the row and signs off. Only then is the status **Accepted** |

Every certificate goes to a person, including clean ones. The material ends up in pressure-containing subsea
equipment, and a confident misread that lands above the minimum passes every automated check. What changes is
the inspector's job. They no longer type seven values. They confirm them, starting with the flagged fields and
the reasons the flow wrote down.

Two test certificates showed why both automated stages exist. On one, a smudged heat number scored 0.41 and
validation had nothing to say about it, so only the confidence check caught it. On the other, every field
scored above 0.90, but the yield strength sat below the purchase specification's minimum, and only validation caught it.

The register's `HeatNo` and `CertificateNo` columns are text, because some suppliers' heat numbers start with a
zero.

## Design guidance

- **Design the three stages before choosing the model.** Extract, validate, review.
- **Validate against data you already trust**, not against the document itself.
- **Set the confidence threshold from test documents**, and log which fields fail it.
- **Write the reasons onto the record** so the reviewer starts with what failed.
- **Send everything to review when a wrong value is costly**, and use the flags to order the work.
- **Store identifiers as text.**
- **Start prebuilt, add custom when your layouts defeat it**, and combine them where volumes differ.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Wrong values in the register with no flags | Only confidence was checked | Add validation against reference data |
| Reviewers approve without looking | Every record looks the same | Write the flagged fields and failed checks onto the record |
| Heat numbers lose a leading zero | Stored in a number column | Use a text column |
| A supplier's certificates fail every time | Its layout is missing from the training set | Add its documents to the custom model and retrain |
| A bulk upload starts failing | 360 calls per 60 seconds per environment | Process in batches, or spread the runs out |
| The prebuilt invoice model misses a field you need | It is not one of the model's fields | Use a custom invoices model, the key-value pairs, or a custom model |

## Key terms

**Document processing** — AI Builder models that extract fields and tables from documents.

**Confidence score** — the model's certainty, from 0 to 1, that it read a value correctly.

**Validation** — checking extracted values against rules and data you already trust.

**Human review** — a named person accepting a record before it is used.

**Key-value pairs** — every label and value a model detects, beyond its defined fields.
