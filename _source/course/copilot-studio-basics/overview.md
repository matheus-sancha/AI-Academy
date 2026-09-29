## What this module is for

{{module:agent-fundamentals}} decided what the Technik Production Assistant is and which harness it runs
on. This module is the build surface: where things are, what is fixed the moment you create an agent,
what a conversation holds, and how to see what your agent actually did.

None of it is difficult. What makes it worth a module is that Copilot Studio is two products behind one
name. An agent on the **GitHub Copilot harness** is four tabs, has no topics and no variables, and has
barely any switches. An agent on the **standard harness** has topics, Power Fx and a full page of
generative AI settings. Half of Microsoft's pages describe one and half the other, and a reader who does
not check which harness a page is written for will look for a Topics area, a variables panel or a
grounding switch that does not exist on their agent.

So every lesson here leads with the GitHub Copilot harness, because that is what the assistant is built
on, and names the standard-harness equivalent beside it. Three of them — topics, variables and most of the
generative AI settings — exist only on the standard harness, and those lessons say where the same
guarantee lives on the other.

## Before you start

You want {{module:agent-fundamentals}} first, above all {{topic:chooseharness}}: the choice is permanent,
and it decides which half of this module applies to your agent. {{topic:orchestration}} matters for
{{topic:topics}} and {{topic:test}}, because a description is the routing signal on both harnesses.

You need access to Copilot Studio in a developer environment ({{topic:devenv}}) to follow along, though
every lesson reads on its own. Allow about 100 minutes.

## What you will be able to do

By the end of this module you should be able to:

- find your way around Copilot Studio on either harness, and tell from a Microsoft page which harness it
  describes;
- create an agent and say what was fixed at that moment and cannot be changed;
- choose and change a primary model, knowing that the default can change underneath you and that a change
  means re-testing;
- explain what a conversation carries, what binds at its start, and why a new chat is the first
  diagnostic step;
- design a standard-harness topic, with its variables and a Power Fx check, and say where the same
  guarantee goes on the GitHub Copilot harness;
- review an agent's generative AI settings, and say what enforces grounding on each harness;
- recognise the files the harness makes for you before writing code to make them;
- read an activity trace or activity map and put the fix where it points.

## The thread through this module

The Technik Production Assistant gets built, and every lesson looks at the same agent from a different
side.

{{topic:tour}} and {{topic:create}} set it up: one knowledge source, `SOP70000101`, a description that
names its scope, and an instruction about how to handle QNs. {{topic:model}} chooses what reasons for it.
{{topic:conversation}} then establishes the habit the rest of the level depends on — *new chat before any
test that is meant to tell you something* — through a skill that looked broken and was not.

{{topic:topics}} and {{topic:variables}} work through the one exchange the assistant would guarantee if it
could: a *Work order status* path that captures a nine-digit number, rejects `P7000001042` as a part
number, and stores the value for the follow-up. The assistant cannot have topics, so both lessons end by
moving that guarantee into the lookup tool's input contract.

{{topic:genai}} finds that on the assistant's harness, the grounding rule has no switch behind it — only an
instruction and a test. {{topic:createdfiles}} stops a spreadsheet script before it is written.
{{topic:test}} closes the module on a wrong revision answer that turns out to be the right data misread,
fixed with one line in a tool description rather than a paragraph of instructions.

## Self-check

<details>
<summary>1. You follow a Microsoft page that tells you to open the Topics page and edit a trigger phrase. Your agent has no Topics area. What happened, and what do you do?</summary>

The page describes the **standard harness** and your agent is on the **GitHub Copilot harness**, which has
no topics at all. Every Copilot Studio page carries a note near the top saying which harness it describes;
reading that first saves the search.

What to do depends on why the page wanted a topic. If it was to guarantee a step — capturing and checking a
value, confirming before something irreversible — put that guarantee in a tool's input contract or a flow,
where it is enforced rather than requested. If it was to route a question, that is the job of your
instructions and your tool and skill descriptions. Switching harness is not an option: the choice cannot be
transferred in either direction ({{topic:tour}}, {{topic:topics}}).
</details>

<details>
<summary>2. You upload a skill, ask for a QN write-up in the chat you have been using, and get generic prose. A colleague says to re-zip the package and upload it again. What do you do first, and why?</summary>

Start a **new chat** and ask again. A skill binds when a conversation starts, so the chat you uploaded from
cannot see it whether the upload worked or not — and a skill that fails its load-time checks is skipped
silently, so both cases look identical there.

If the new chat produces Technik's format, nothing was wrong. If it does not, check whether the skill is
listed in Build; if it is missing, it failed a check. Only a skill that is listed but not used is a real
description problem. Repackaging first wastes the afternoon on a skill that was probably fine. Note the
contrast: saved instructions, a new tool and a model change reach a running conversation on the next turn;
a skill does not ({{topic:conversation}}, {{topic:test}}).
</details>

<details>
<summary>3. Your standard-harness agent has an instruction to answer only from its sources and to say so when they have nothing. Why is that not enough, and what does the GitHub Copilot harness do differently?</summary>

On the standard harness, an instruction is followed *usually*. **Allow ungrounded responses**, turned off,
is the mechanism behind it: a turn in which no knowledge source or tool was used is blocked, and the
fallback fires. It is not a complete guarantee — the model can still blend general knowledge into an answer
built from a source — and it has a cost: answers without an in-text citation are withheld, so a citation
instruction has to go with it.

The GitHub Copilot harness has no such switch. There, the instruction carries the whole load, which means
it has to be **tested**: a question the sources do not cover, whose only acceptable answer is the
abstention, kept in the evaluation set permanently ({{topic:genai}}).
</details>

<details>
<summary>4. The assistant tells you the latest released revision of a drawing is C. C is still in work. Where do you look first, and what are the likely fixes?</summary>

The **activity trace**, before touching anything. It tells you which of four things happened: nothing was
retrieved; the wrong thing was retrieved; the right thing was retrieved and misread; or the question was
ambiguous. Only the third is fixed in the instructions, and even then the tightest fix may be elsewhere.

Here the trace shows the revision tool ran with the right drawing number and returned all three revisions
with their status — the agent then picked the highest letter. That is the right data misread, and the
narrowest fix is in the tool's output description: only `Released` rows count. Then re-test three times,
each in a new chat, because one success after a change is not evidence the change worked
({{topic:test}}).
</details>

<details>
<summary>5. Someone on the team has written a Python script, packaged in a skill, that turns QN rows into an Excel file. Is that a good use of a skill?</summary>

Probably not. On the GitHub Copilot harness the agent creates and edits Word, Excel, PowerPoint and PDF
files natively and offers them for download, with nothing to configure — so the script reproduces something
the harness already does, and adds code to maintain and a sandbox run to pay for.

What the harness cannot know is Technik's rules: which columns a QN summary carries, that `DEFECT_TYPE` is
quoted verbatim, how a controlled document is laid out. Those belong in a skill's instructions or template,
and the harness still writes the file. Two limits to design around: a created file over 10 MB is not
returned, and files are deleted 28 days after the conversation's last activity, so anything worth keeping
gets downloaded ({{topic:createdfiles}}).
</details>
