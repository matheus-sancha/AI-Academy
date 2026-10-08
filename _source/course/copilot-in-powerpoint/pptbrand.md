## TL;DR

A generated deck takes its look from the **template** it was built on, so the template you start from
decides most of your rework. Copilot uses the template's **sample slides, placeholders, theme colours
and theme fonts**. It doesn't use one-off formatting, and it doesn't resize text that overflows. Start
from Technik's template or brand kit, then check what generation doesn't: overflowing text, images and
whether the layout suits the content.

## Why it matters

"On-brand" sounds like a promise. Microsoft's page is more careful: it describes what Copilot *reads*
from a template, and what happens when the template doesn't give it enough. Knowing the difference is
ten minutes of fixing instead of slides presented with text running off the edge.

## How it works

### Start from the template, or pick a brand

Open a new presentation from Technik's template before you ask Copilot for anything.

<!-- volatile verified=2026-10 -->
If your organisation has set up a **brand kit**, you can choose it in the Copilot pane: select **+**,
then **Select brand**, and pick the kit. Copilot then generates with that kit's templates, colours,
fonts and assets.
<!-- /volatile -->

### What Copilot takes from a template, and what it ignores

| Copilot uses | Copilot doesn't use |
|---|---|
| The **sample slides** in the template and their layouts | **One-off formatting**: a colour or font someone set by hand on one slide |
| **Placeholders**: their type, position and size | The **wording of placeholder text**. It is styling only, not an instruction |
| **Theme colours and theme fonts** | **Instructions** typed onto template slides, such as *"put the logo here"* |
| Text, shapes, images and charts on the sample slides | |

Two consequences follow. First, if the template has too few sample slides, Microsoft says Copilot
**falls back to the Slide Master**, which can give plainer, less suitable layouts. Second, a template
whose look depends on manual formatting won't pass that look on.

### What generation doesn't fix

- **Overflowing text.** Microsoft says Copilot doesn't resize fonts or placeholders when the text is
  longer than the space. You'll find text running out of its box.
- **Images.** Copilot uses licensed stock images or generates new ones from the slide content. A
  generated image is marked *"AI-generated"* in the speaker notes. Either kind can be irrelevant or
  misleading, and Microsoft says design suggestions should be reviewed before use.
- **Fit.** A layout can be on-brand and still wrong for the content: a three-column layout for one
  point, a photo slide for a table.

### Whose job the template is

Making a template that Copilot uses well is a job for whoever owns it: enough sample slides, real
placeholders rather than text boxes, theme colours and fonts set in the Slide Master. If generated decks
keep coming out plain, tell the template's owner.

## In practice at Technik

You open Technik's corporate template and build the `SOP70000101` briefing from it
({{topic:pptmake}}). The title slide, colours and fonts are right. Then check:

1. **Slide 3**, *How priority is set*, has text running past the bottom of its box. Copilot didn't
   shrink it. Cut the text to what a supervisor needs, using the SOP's wording. Don't shrink the font
   until it fits.
2. **Slide 2** has a stock photo of a person in a hard hat on a building site. It's on-brand and says
   nothing about quality notifications. Delete it, or use a real photo the plant has approved.
3. **Slide 5** uses a plain layout unlike the rest. The template may not have a sample slide for that
   kind of content. Pick a layout from the template yourself, and mention it to the template's owner.

The deck now looks like Technik's. What it *says* still needs checking against the SOP.

## Using it well

- **Open the organisation's template first**, or choose its brand kit in the Copilot pane.
- **Check every slide for overflowing text**, and fix it by cutting words.
- **Check every image.** Delete any that don't help; read the speaker notes for *"AI-generated"*.
- **Pick a layout yourself** when Copilot's choice doesn't fit the content.
- **Report a weak template** to its owner instead of fixing every deck.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A deck in default colours and fonts | It was started from a blank presentation | Start again from the template, or select the brand kit |
| Text running out of its box | Copilot doesn't resize text that overflows | Cut the text; check every slide |
| Plain layouts that don't match the template | Too few sample slides, so Copilot fell back to the Slide Master | Choose a layout yourself; tell the template's owner |
| An irrelevant or invented-looking picture | Images are stock or generated from slide text | Delete or replace it |

## Key terms

**Template**: a `.potx` or `.pptx` file that sets a deck's layouts, colours and fonts.

**Brand kit**: an organisation's approved templates, colours, fonts and assets, which you can choose in
the Copilot pane.

**Slide Master**: the slide that defines a template's base layouts and theme.

**Placeholder**: a box in a layout that is meant to be filled, such as a title or a picture.
