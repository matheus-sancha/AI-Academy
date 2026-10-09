## TL;DR

Copilot in Word gets thin in specific places, and the reasons aren't mysterious. There's a limit to how
much it processes per prompt, so long documents lose detail. Its quality is highest in English. It
works with words, so meaning carried only by formatting can fall out. Microsoft doesn't say how it
treats tracked changes, comments or embedded objects. And it can't judge whether anything is true.
Expect to check structure and numbers yourself.

## Why it matters

These failures don't announce themselves. A summary reads just as smoothly when it has skipped the
last third. A rewrite that loses a red **HOLD POINT** looks tidier,
not broken. Knowing where Copilot is weak tells you where to read yourself, and saves you from reading
everything else twice.

## How it works

### Length

Microsoft's FAQ says Copilot in Word is **limited in the number of words it can process per prompt**.
The summary page adds that Copilot takes the whole document into account but **doesn't always cite
later content**. Neither page gives the number, and you don't need it: the longer the document, the more you ask about a section by name rather than about the
whole.

### Language

Copilot in Word supports fewer languages than Word itself, and Microsoft says quality is **highest in
English**. Ask in another language and the answer may still be fluent, so fluency tells you nothing.
Check harder.

### What isn't plain text

<!-- verified tenant=2026-10 -->
Microsoft's pages on Copilot in Word don't say how it treats **tracked changes**, **comment threads**,
**embedded objects** such as a pasted Excel table, or **text inside images**. Don't
assume it sees them the way you do on screen.
<!-- /verified -->

Formatting is a related case. A cell shaded red, a step in bold capitals, a strike-through on a
superseded limit: each carries meaning for you. Copilot works with the words. If something matters, it
needs to be said in words, or it may not survive a rewrite.

### What it can't open

Copilot works within your own permissions: it only uses content you could already open
({{topic:visibility}}). When a file is encrypted with a sensitivity label, it honours the rights that
label gives you ({{topic:sensitive}}). And your organisation can switch Copilot off in Word entirely,
through the privacy settings for connected experiences. An empty pane isn't always a fault on your side.

### What it can't judge

Microsoft is blunt about this: Copilot in Word **can't understand meaning or evaluate accuracy**, and it
can make mistakes or misread facts. It can tell you what the document says. Whether the document is
right, current or applicable is still your call.

## In practice at Technik

### Reviewing a draft with tracked changes

Engineering change `ECN70000042` is released, and a draft of revision C of `SWI70000318` is circulating
with tracked changes on. It adds an ultrasonic check before cladding in section 4 and tightens the
porosity limit in section 5. You're asked to review it.

The tempting prompt is *"summarise what changed in this revision"*. Given the unknown above, you don't
know whether Copilot reads a deletion as gone, as still there, or at all. So:

1. **Use Word's own review tools for what changed.** Tracked changes and *Compare* show it exactly.
   This is the job they exist for.
2. **Use Copilot on sections.** *"Quote the porosity limit in section 5"*, then read it in place, with
   the markup showing.
3. **Read the numbers yourself.** A tightened limit is exactly the kind of detail a paraphrase blurs.

### A long procedure

Asked to summarise a long SOP, Copilot gives a good account of the first sections and one line on the
appendices. Ask about each appendix by name instead of asking for the summary again.

## Using it well

- **Ask about sections, not whole long documents.**
- **Resolve or show tracked changes deliberately** before you ask, and know which you did.
- **Read embedded tables and figures yourself.**
- **Say it in words.** Don't rely on colour or bold to carry a requirement through a rewrite.
- **Check harder outside English.**
- **Treat "it can't do that" as information.** It may be a permission, a label or a setting, and the
  answer is different for each.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The summary thins out towards the end | The per-prompt limit, and fewer citations to later content | Ask about later sections by name |
| A rewrite lost a **HOLD POINT** | The meaning was in the formatting | State it in words, then rewrite |
| *"What changed?"* gives a confident wrong list | How it reads tracked changes isn't documented | Use Word's review and compare tools |
| A clumsy or wrong answer in another language | Quality is highest in English | Check against the source, or ask in English |
| Copilot won't work on a file | Its label restricts what you may do, or Copilot is off | Ask whoever owns the label or the setting |

## Key terms

**Per-prompt limit**: the cap on how many words Copilot in Word processes for one request.

**Tracked changes**: Word's record of edits. How Copilot treats it isn't documented.

**Sensitivity label**: your organisation's classification on a file, which can limit what Copilot does
with it.
