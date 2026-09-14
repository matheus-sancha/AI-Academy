Multimodal models accept or produce more than text: images, documents as images, audio, sometimes
video. The prompt-and-context ideas from the rest of this module carry over unchanged — an image is
tokenised too, and a page of a scanned drawing can cost more tokens than a page of prose.

## Where it fits at Technik

Two realistic uses, and one trap.

**Reading documents that are really images.** Supplier material certificates arrive as scanned PDFs.
A multimodal model can read one directly, which is sometimes simpler than an extraction pipeline.
B9 and A10 use AI Builder document processing for this instead, and the reason is worth
understanding: document processing gives you named fields, confidence scores and a review step,
which a free-text description of an image does not. Reach for a model when the input is
unpredictable, and for document processing when it is a form you see a thousand times.

**Looking at a photograph of a defect.** A quality engineer photographs surface porosity and asks
what it might be. The model can describe what it sees and suggest causes. It cannot measure, and it
has no idea what Technik's acceptance criteria are unless you supply them.

**The trap** is a drawing. Engineering drawings are dense, precise and full of small annotations,
and a model reading one will produce a fluent, confident, partly invented description. Dimensions and
tolerances are exactly the kind of detail it gets almost right. Read revision data from Teamcenter,
not from a picture of a drawing.

## Design guidance

- Treat an image as expensive context: it competes with everything else for the window.
- Never let a model's reading of a drawing or certificate become a number someone acts on without a
  human check. Extract, validate, then review (A10).
- Say what you want from the image. "Describe this" invites invention; "list any visible surface
  defects, or say none are visible" does not.
- If the input is a repeated form, a purpose-built extraction model beats a general one on accuracy,
  cost and auditability.

## Key terms

**Multimodal model** — one that accepts or produces more than text.

**Vision** — the image-understanding capability of such a model.

**OCR** — optical character recognition: turning pictures of text into text. Often a better and
cheaper first step than handing an image to a model.

**Document processing** — AI Builder's extraction of named fields from forms, with confidence scores
(B9).
