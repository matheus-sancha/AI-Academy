## TL;DR

This level taught seven things you should now be able to do **without a guide**: fill a brief, structure
instructions, triage a requirement, author and package a skill, add a connector and an MCP server, evaluate an
agent, and publish it somewhere you did not build it. Each has a test below that you run on **an agent of your
own, not the Technik one**, because recognising a worked example is not the same as producing one. Pass all
seven and you are ready to go on. Fail one and reread the module that taught it, not the whole level.

## Why it matters

The guided build carries you. The router hands you the next stage's instructions, each skill checks its own
output, and the files say where you are. That is what makes it a good first build and a weak test of what you
learnt: finishing it shows the route works, not that you could do the same work without it.

What comes next assumes you can. It goes on to build agents in code, where nothing interviews you for
the brief or warns you that a tool should have been a sentence in the instructions. A gap you carry forward
surfaces there as a problem that looks like something else.

## How it works

Each check names a task, says what passing looks like and points at the module that taught it. Write your
answers down. A check passed in your head usually turns out to have been recognition.

1. **Fill a brief that will not stall a design interview.** Take a request someone has actually made of you,
   fill every slot, and give the brief to a colleague who has not seen it. You pass if they can write three
   test cases from it without asking you anything: tasks are verb phrases with a trigger and an object, the
   escalation names a recipient you could look up, and the refusal is one a user might plausibly ask for.
   Reread {{module:designing-an-agent}}.
2. **Write XML-structured instructions and say which section a line belongs in.** Take ten lines from
   instructions you did not write and sort each into `<role>`, `<tone>`, `<tasks>`, `<instructions>` or
   `<rules>`, or out of the instructions altogether. You pass if you can say what goes wrong when each line
   sits in the wrong place, and why tags are not the defence against text injected into retrieved content.
   Reread {{module:writing-instructions}}.
3. **Decide whether a requirement is instructions, knowledge, a tool or a skill.** Place ten requirements
   from a real brief. You pass if every tool reads live data, writes or runs a fixed process, every skill
   carries a procedure or bundled material, and at least one request for a connector turned into a sentence
   in the instructions ({{topic:triage}}). Reread {{module:designing-an-agent}}.
4. **Author and package a skill, and diagnose one that never fires.** Write a skill, package it, upload it,
   then break it three ways: a folder-wrapped archive, a frontmatter error, a description that matches no
   one's words. You pass if you can tell which break you caused from what you see, checking in order: a new
   chat, then the **Skills** list, then the description. Reread {{module:agent-skills}}.
5. **Add a connector and an MCP server, and explain who the connection runs as.** Add one of each to a test
   agent. For each, write one sentence naming the identity that reaches the system and what that identity
   could do if an injected instruction were obeyed. You pass if a second account gets exactly the result
   you predicted. Reread {{module:tools-connectors-mcp}}.
6. **Write an evaluation set that can fail, and read the results without trusting the percentage.** Write
   ten cases and run them. You pass if you can name the plausible wrong answer each case would catch, and
   your report of the run never needs its score: which cases flipped since the last run, which account it
   ran as, and which passes you checked by hand. Reread {{module:testing-and-evaluation}}.
7. **Publish into a solution and an environment you did not build in.** Create a publisher and a custom
   solution before the agent exists, build into it, export it as managed, import it into a second
   environment, bind its connection references and publish to one channel. You pass if a colleague gets an
   answer there and you made no edit in that environment. Reread {{module:publishing-and-environments}}.

<!-- unknown since=2026-10 -->
Check 7 rests on solutions, which Microsoft documents only for the standard harness. If your agent is on the
GitHub Copilot harness, finding out whether it travels in a solution is part of the check.
<!-- /unknown -->

### What the two links measure

The study guide for Exam AB-620 describes its candidate as a professional developer or advanced builder, and
much of what it lists sits beyond this level: Microsoft Foundry, the Agent2Agent protocol, custom connectors,
Power Platform Pipelines, Application Insights. Its *Test and manage agents* area is this level's ground:
creating a test set, choosing an evaluation method, reviewing results, solutions and environment variables.
Read it as a map of what comes next, not as a second checkpoint.

Microsoft's *Create agents in Microsoft Copilot Studio* learning path is rated intermediate, and most of its
modules use the classic experience, now the standard harness. It is the quickest way to see in Microsoft's own
words what this level taught as standard-harness designs, such as topics and generative answers.

## In practice at Technik

An engineer finishes the guided build with the Production Assistant and sits the checkpoint against a
different agent: a small FAT checklist helper they built earlier the same month, which tells a test lead which
tests a unit still needs before its project's `FAT_DUE_DATE`. Four checks pass. Three do not.

**The brief.** A colleague trying to write test cases from it gets stuck on the first task: *help with FAT
prep*. That is an area, not a verb phrase. Rewritten as *given a serial number, list the FAT tests with no
recorded result*, it gives them the trigger, the object and an obvious first case.

**The connection.** Asked who the Snowflake connection runs as, the engineer writes *the agent*. It runs as
them: they made it with their own account while prototyping. Every test lead reaches whatever the engineer can
reach, and the engineer never noticed, because every test ran as them. The fix is the pattern the Production
Assistant already uses, a read-only service account.

**The publish.** The helper lives in the default solution, so it cannot be exported. The engineer can name the
fix: create a solution, add the agent and its flow, and live with the default prefix on the flow. They count
check 7 as failed anyway, because the check was the publish, not the explanation.

Three rereads, of three modules, and the checkpoint again on the rebuilt helper.

## Design guidance

- **Use your own agent.** Every example in this level is the Production Assistant; using it tests memory.
- **Close the guide.** Look things up in Microsoft's documentation, as you would at work, not in this course.
- **Write the answer before you check it.** An answer you only thought of cannot be wrong.
- **Fail a check, reread one module.** The checks are independent, so a gap does not mean starting over.
- **Count an explanation as a fail.** Knowing how to fix something is not the same as having done it.
- **Ask a colleague for checks 1 and 5.** A brief and an identity both fail only for someone else.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Every check passes in an hour | It was sat against the Technik example | Sit it against an agent of your own |
| The brief passes, then a colleague cannot test from it | You judged it as its author | Hand it over and let them try |
| Check 5 is answered as "the agent" | The connection was never looked at | Open the connection; name the account |
| The evaluation report leads with a percentage | The run was read as a score | Report flips, the account and the hand checks |
| Check 7 is passed by describing it | Recall counted as doing | Export, import and publish, then ask a colleague |
| The whole level gets reread | One failed check felt like many | Reread only the module the check names |

## Key terms

**Checkpoint**: seven tasks this level taught, each with a test you run on your own agent.

**Without a guide**: with Microsoft's documentation open but not this course, the router or the six skills.
