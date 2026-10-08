## What this module is for

PowerPoint is where Technik's documents get retold: an SOP turned into a briefing, a procedure turned
into training, a quarter turned into a review. A deck is short, read fast and often presented by
someone who didn't write it. That makes it the place where a small slip in wording reaches the most
people.

Copilot reads a deck someone sent you and finds the slide you need, and it turns a document you
already have into a first-draft deck, outline first. Both come with one caution from Microsoft's FAQ: Copilot *"can't understand meaning or evaluate accuracy"*. It can
build slides. Deciding what they should say is yours.

The five app modules share a shape (ask, make, one speciality, limits). PowerPoint's speciality is the
template: what a generated deck takes from it, and what you still fix by hand.

## Before you start

{{module:prompting}} applies to every request in this module, especially {{topic:clarity}} (say who
the deck is for) and {{topic:iterate}} (refine the outline in the chat). {{topic:hallucination}}
explains why a deck built from a description invents. {{module:copilot-in-word}} teaches the same
habits on longer text: ask for the quote, and draft from a file.

Allow about 40 minutes.

## What you will be able to do

By the end of this module you should be able to:

- ask Copilot about a deck and get a slide number and a quote you can check, and tell a deck from the
  document it summarises;
- build a draft deck from a document rather than a description, and cut it at the outline, before any
  slides exist;
- read each generated slide against its source for names, roles and limits;
- say what a generated deck takes from a template (sample slides, placeholders, theme colours and
  fonts) and check what it doesn't fix (overflowing text, images, layout fit);
- edit a draft down: find the slide that matters, cut by hand rather than shrink, and read the deck
  end to end for slides that disagree.

## The thread through this module

Every example comes from Technik, the fictional manufacturer this course is built around. See the
[scenario](../scenario/index.html) for the company and its documents.

One document carries the module: `SOP70000101` *Quality Notification Handling*. In the first lesson an
old training deck about it gives a confident, out-of-date answer. In the next three, the quality lead
turns the SOP itself into a six-slide briefing for shift supervisors: built from the file, put on
Technik's template, and edited down until its one key point stands out. That point is who decides what
happens to a nonconforming part: the quality engineer assigned to the QN. Only the documents are used.
No system data is involved.

## Self-check

Answer these before moving on. Each answer explains the reasoning, not just the verdict.

<details>
<summary>1. You ask Copilot about a training deck: "Who decides a QN's disposition?" It answers clearly. Is that enough to act on?</summary>

No. Ask which slide says so and to quote it, then read the slide. Even a correct answer only tells you
what the deck says, and a deck is someone's summary at one moment. Check the deck's date, and check the
governing document, here `SOP70000101`, when the answer matters. Copilot can't tell you the deck is out
of date. Reread {{topic:pptask}}.
</details>

<details>
<summary>2. You reference SOP70000101 and, in the same prompt, ask for "six slides for supervisors". The outline has eleven slides. What went wrong, and where do you fix it?</summary>

Microsoft says that when you reference a file you can't add more instructions in the same prompt, so
the audience and length were lost. Give them in a follow-up and cut at the outline: remove *Purpose*,
*Scope* and *References*, merge what belongs together, then approve. Reread {{topic:pptmake}}.
</details>

<details>
<summary>3. A slide reads "Disposition: agreed between the supervisor and quality". The deck was built from the SOP. Why might it still be wrong?</summary>

Because slides compress, and compression drops qualifiers and names. The SOP gives the disposition to
the quality engineer assigned to the QN; the bullet kept the topic and lost the person. Building from
the file keeps the content close, not exact. Read every slide against the source, roles and limits
first, and restore the source wording. Reread {{topic:pptmake}}.
</details>

<details>
<summary>4. You built the deck from Technik's template. Text runs off the bottom of one slide, and another has an unrelated stock photo. Didn't the template take care of that?</summary>

No. Copilot uses a template's sample slides, placeholders, theme colours and fonts, but Microsoft says
it doesn't resize text that overflows, and its images are stock or generated, so they need checking.
Cut the text rather than shrinking it, and delete pictures that don't help. If layouts keep coming out
plain, the template may lack sample slides; tell its owner. Reread {{topic:pptbrand}}.
</details>

<details>
<summary>5. You use Condense on a slide and it reads better. Slide 3 lists three priority levels; a flowchart on slide 5 shows four. Copilot flagged neither change. Why, and what do you do?</summary>

Copilot can't understand meaning or evaluate accuracy, so it doesn't cross-check slides. And its rewrite
tools work on whole text boxes and skip shapes, so *Condense* may have softened a limit while the
flowchart was never touched. Compare what *Condense* changed against the SOP, fix the diagram yourself,
and read the whole deck end to end before anyone presents it. Reread {{topic:pptlimits}}.
</details>
