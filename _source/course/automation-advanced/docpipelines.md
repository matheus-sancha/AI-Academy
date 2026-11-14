## TL;DR

{{topic:docproc}} taught the shape: extract, validate against data you trust, and review before anything is written. A production pipeline has five stages, **classify, extract, validate, review and write**, and the two pages this lesson cites document only one of them. They document **extraction**: how an AI Builder custom model is trained, with one *collection* per layout, and the limits that decide what it can read, plus a community route to tables through Azure's Layout model. Classification, validation, review and writing are not covered by either page. They are design, and the lesson says so. The limits matter more than the happy path, because the ones that bite are silent: a table that breaks across a page, and a supplier with no collection yet.

## Why it matters

Intermediate's pipeline assumed the model could read the certificate. At volume, much of the work is knowing when it can't, and a model that fails loudly is the easy case. A value cut by a page break need not raise an error. The pages call it unsupported and don't say what comes back, so it can be a smaller record that nothing flags.

The stage list also protects the cost. Every page that reaches a model costs credits ({{topic:aibuilder}}), and a document that is not a certificate should never get that far.

## How it works

### Collections: one per layout

An AI Builder custom model starts from a document type. **Fixed template** documents, previously called structured, train quickly and put fields, tables, checkboxes and signatures in similar places. **General** documents, previously unstructured, can be anything and have a long training time. **Invoices** extend the prebuilt invoice model with extra fields or with samples it extracted badly. You list what to extract, which can be text, number, date, checkbox or a table with named columns. You then group sample documents into **collections**, where a collection is a group sharing the same layout, with at least five samples each and up to 200 collections per model.

### The limits that shape the pipeline

<!-- volatile verified=2026-11 -->
| Limit | Value |
|---|---|
| File types for training | JPG, PNG, PDF. A text-embedded PDF extracts better than a scan |
| File size | 20 MB at most. Images 50 × 50 to 10,000 × 10,000 pixels |
| TIFF | Not for training. A trained model can process it in a cloud flow |
| Password-locked PDFs | Unlock first |
| Fields split across a page boundary | Not supported |
| Rows that break from one page to the next | Not supported |
| Signature extraction | Fixed template documents only |
| Tagged fields in a cloud flow | 300 |
| Version 4.0 | Adds confidence scores for tables and their cells. A v3.1 model moves up by editing, retraining and publishing, with no re-tagging |

<!-- /volatile -->

### Tables by another route

The community article reaches tables without training. It calls the prebuilt **Layout** model of Azure AI Document Intelligence from an HTTP action, with the file as base64. A 202 response means the work is asynchronous, so the flow keeps the request id from the response headers, waits ten seconds, fetches the result by that id and selects each table's rows, columns and cell text. The author says to raise the wait if processing runs over it. It returns the tables of every page, as separate tables, and the article never says whether a table that spans pages is joined. It needs a Document Intelligence resource at Standard S0 or above and a key, and it writes nowhere: the output is arrays.

The two routes are different products. "No training needed" belongs to the Layout model, and AI Builder's custom model needs collections. The article lists many more file types than AI Builder accepts for training, and the page-break limits above apply only to AI Builder.

### Four stages the pages leave out

<!-- unknown since=2026-11 -->
Neither page covers classifying an incoming file, validating against business rules, routing low-confidence results to a person or writing to a system of record. The model page's only confidence statement is that version 4.0 scores tables. The text this lesson drew on stops after collections, so the tagging, training, accuracy and re-training guidance sits on pages it did not read. Duplicates, idempotency and feeding reviewers' corrections back into training are stated nowhere.
<!-- /unknown -->

Collections group training samples. They are not a runtime router, so deciding which model a file goes to is a stage you build.

## In practice at Technik

The five stages for supplier certificates, with who owns each failure:

| Stage | Done by | A failure here looks like |
|---|---|---|
| **Classify** | Folder and file name, then a person for the rest | A delivery note reaches the certificate model and returns empty fields |
| **Extract** | Custom model, one collection per supplier layout | A field missing or a low score |
| **Validate** | Flow logic: units, grade, 485 MPa yield minimum, tensile above yield, certificate number not registered | A reason written onto the record |
| **Review** | A quality inspector | A decision, with a comment |
| **Write** | Flow, **after** a person accepts | A row in the *Certificate register* |

The first catch is in the sample set. Technik keeps ten sample certificates. A collection needs five, so ten samples can fill two collections at most, and a third supplier's layout has none. The pipeline therefore has a state for *layout not trained yet*, which routes to manual entry and queues the document for the next training round. A first-time supplier is a normal case, and a flow that hands its certificate to the nearest model gets confident nonsense.

The second catch is the page break. Certificates run to two pages, and a mechanical-properties table that runs onto the second page is exactly the unsupported case. The pages don't say what the model returns there, so validation checks for completeness as well as plausibility: all three strength fields and the test row present, or the record goes to review with the reason *table may be incomplete*.

The third is the write. The register row is keyed on certificate number and heat number, and the write step checks the key first, so a rerun after a failure updates the row instead of adding a second. Identifiers go into text columns, since some heat numbers start with a zero. That is the design, and the pages don't back it: they don't mention duplicates.

When an inspector corrects a field, the document goes into its supplier's collection for the next retraining. That too is a position, since the text read gives no retraining guidance beyond the version upgrade.

## Design guidance

- **Design all five stages before picking a model**, and name who owns each failure.
- **Train one collection per layout**, and plan for the supplier with fewer than five samples.
- **Treat page-break limits as a validation rule**: check completeness, not only values.
- **Keep the Layout route for tables** a model cannot read, and keep its key out of the flow's text.
- **Never write before a person has accepted**, and key the write so a rerun cannot duplicate it.
- **Store identifiers as text.**

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A new supplier's certificates come back empty | No collection exists for its layout | Route to manual, collect five samples, retrain |
| A strength value is missing with no error | A field or row broke across a page | Add a completeness check |
| A TIFF cannot be used for training | TIFF is runtime only | Convert to PDF or PNG for training |
| The same heat appears twice in the register | The write was rerun without a key check | Check the key before writing |
| A custom form is expected to work with no training | "No training needed" describes the prebuilt Layout model, used here for tables | Train a custom model for your own fields |
| A password-locked certificate fails | The model cannot open it | Unlock first |

## Key terms

**Collection**: a group of sample documents that share one layout, five or more per collection.

**Fixed template**: the document type for forms whose fields sit in similar places.

**Layout model**: Azure AI Document Intelligence's prebuilt model for text and tables, called here over HTTP.

**Completeness check**: validation that every required field and row was read.
