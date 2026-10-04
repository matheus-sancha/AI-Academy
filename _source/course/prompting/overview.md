## What this module is for

How you ask decides a large part of what you get. The same Copilot, given the same document, can return a
generic paragraph that guesses, or a five-line summary that says exactly what the document states and marks
what it doesn't. The difference is the prompt, and writing one is a skill you can learn in an afternoon and
use in every tool in this course.

This module covers that skill in six parts: the layers every request has, what to say in one, showing an
example instead of describing it, naming the shape of the answer, splitting a big job into steps, and
improving a prompt by trying it. None of it is about magic phrases. All of it is about leaving Copilot as
little to guess as possible, and making whatever it does get wrong easy to see.

Everything here works the same whether you have Microsoft Copilot Chat on its own or a Microsoft 365
Copilot licence. What changes with the licence is what Copilot can *reach*, which is the next module.

## Before you start

{{module:how-copilot-works}}. This module keeps coming back to its three ideas: the model writes what is
likely, it works only from what is in front of it, and it fills gaps with plausible invention. Every
technique below is a way of acting on one of them.

Allow about an hour.

## What you will be able to do

By the end of this module you should be able to:

- say which layer of a request (standing instructions, context or your message) is causing a bad answer;
- turn a vague request into one that states its goal, context, source and expectations;
- use a short example to fix the shape of an answer, and spot when the example's details leak into it;
- ask for an answer in a named shape that shows its own gaps;
- split a job into steps you check one at a time;
- test a prompt on several cases before trusting it, and save the version that holds up.

## The thread through this module

Every example comes from Technik, the fictional manufacturer this course is built around. See the
[scenario](../scenario/index.html) for the company and its documents.

One request runs through all six lessons: *"Summarise this QN"*, about quality notification `300001234`,
porosity found in the cladding of a subsea tree unit. Each lesson improves it in one way, until it's a
prompt you could hand to every supervisor: written for a named audience, held to the QN's own text, shaped
into five headings with a place for what isn't known, run in checked steps when it feeds a message, and
tested on QNs that are harder than the first.

## Self-check

Answer these before moving on. Each answer explains the reasoning, not just the verdict.

<details>
<summary>1. Every answer Copilot gives you comes back as terse bullet points, even when you ask for a paragraph to paste into a report. Rewording the request hasn't helped. Where do you look?</summary>

At the **standing instructions**, and in particular any custom instructions you set yourself. A preference
like *"keep answers short and use bullet points"* applies to every chat, so it shapes answers long after
you've forgotten writing it. Rewording the request can't fix a fault in another layer. Override it in the
message for this one answer, or change the setting if it no longer suits you. Reread {{topic:anatomy}}.
</details>

<details>
<summary>2. You ask for a summary of a quality notification, and the answer includes a likely cause the QN never mentions. Which two additions to the prompt make that less likely?</summary>

A **source** and an **out**. *"Use only the QN text"* tells it where the answer has to come from, and
*"if the QN doesn't say something, write 'not stated'"* gives it something to write other than a guess.
Without them, a likely cause is exactly what a summary of a defect usually contains, so it's the most
probable thing to write. A better model or politer wording doesn't change that. Reread {{topic:clarity}}.
</details>

<details>
<summary>3. You paste one summary you wrote by hand as an example of the layout you want. The new answer has the right layout, and one of its lines is word for word from your example. What happened, and what do you do?</summary>

The model copied the example's **content** as well as its pattern. That's example leakage, and it
happens because everything in the example looks like part of what you want. Label the example as a
different case and say what to take from it (layout only), then check the answer for details that came
from the example rather than the source. If one example is copied too literally, a second that differs in
content helps. Reread {{topic:fewshot}}.
</details>

<details>
<summary>4. You need a summary for a meeting and a message to a planner from the same QN. Why is asking for both in one prompt riskier than asking in steps, even if the one-prompt answer reads well?</summary>

Because a fluent combined answer gives you nothing to check it against. A date or an owner can be filled in
because messages like that usually have one, and nothing shows where it came from. In steps, you first get
the facts as a list with the sentence each came from, check it, and build the summary and the message only
from that checked list. A mistake caught at the first step never reaches the message. Reading well is not
the same as being right. Reread {{topic:decompose}}, and {{topic:output}} for asking for the quotes.
</details>

<details>
<summary>5. Your QN summary prompt has worked perfectly on the last three QNs you used it on. A colleague wants to share it with every supervisor. What do you do first?</summary>

Try it on cases that **differ** from the ones it was written for, especially one where the QN lacks what
the prompt asks for, such as a one-line description. Three good runs on typical QNs show it works on
typical QNs. Thin or unusual cases are where a heading invites invented content. Change one thing at a time
if it fails, re-run every case, and save the version that holds up with a note of what each change was for.
Reread {{topic:iterate}}.
</details>
