## TL;DR

Run the set, read the result of **each case**, open the failures to find out why, fix one thing, and run it
again. Keep every run so versions can be compared. Then read the percentage the way you would read a number
someone handed you without its working. A score says **how many cases passed**. It does not say which ones,
whether they should have, who they ran as, or whether the agent is finished. The human review rubric from your
success criteria answers that last one, and no run does.

## Why it matters

A run produces one number, and the number is where everyone's eyes go. *"We're at 92%"* is the sentence that
reaches a stakeholder, and it carries none of the context that would let them judge it.

Everything earlier in this module is a reason that number can mislead. The grader cannot see your facts
({{topic:judge}}). A set can be full of cases that cannot fail ({{topic:advtests}}). The run may have been made
as the wrong person ({{topic:testidentity}}). The same set gives different scores on different runs
({{topic:whyeval}}). Reading a score well means asking each of those questions every time, in the same order,
until it is a habit.

## How it works

### Running it on the GitHub Copilot harness

<!-- volatile verified=2026-10 -->
On the **Evaluate** tab, pick the evaluation, check the **Configure test set** panel (its name and test method,
General quality today) and select **Evaluate**. A run can take several minutes. Each run is **saved
separately**. After you change the agent's instructions, knowledge or tools, select **Evaluate test set again**
under *Recent results*, and compare the new run with the earlier ones.

The results page has two parts. The **test run result** is a table of conversations, each with its message
count and General quality result. The **evaluation summary** gives the score (the share of conversations that
passed), the duration, the number of test cases, the user profile that ran it, and the estimated credits, split
between generating responses and grading them. Open a conversation and you get its user messages, the agent's
responses, Pass or Fail, and that case's credits.

To keep a run, **Export test results** as a CSV, or **Download** the session. The download packages the
evaluation's name, run identifier, **agent version** and test method with every turn's input, response and
score.
<!-- /volatile -->

<!-- unknown since=2026-10 -->
The GitHub Copilot harness's case details list messages, responses, the result and credits. Whether they also
show the grader's reasoning, or the trace of what the agent did, is not documented.
<!-- /unknown -->

Microsoft's advice for acting on results is three lines: low quality, look at the instructions; missing or
incorrect tool use, look at the tool descriptions; incorrect information, look at the knowledge. That is
{{topic:manual}}'s classification. To find out which one a failure is, replay it in the preview pane, where you
can open the trace.

### Running it on the standard harness

<!-- volatile verified=2026-10 -->
The standard harness gives each case **Pass**, **Fail**, **Invalid** or **Error**. *Invalid* means a method
lacked what it needs, such as an expected answer. *Error* can mean the retrieved knowledge made the grading
input too large. Neither is a judgement of the agent. A case's details include the expected and actual
response, the **reasoning** behind the result, the knowledge, topics and tools used, and the activity map. The
results also report **response time** per interaction, which never affects pass or fail. **Compare with** sets
two runs of one set side by side, with arrows on the cases that went from failing to passing and back. Only one
evaluation runs at a time, only the maker who started a run sees its responses and explanations, and results
are kept for **89 days**.
<!-- /volatile -->

### Reading a score: five questions

Ask these in order, every time.

1. **Compared with what?** A score means something only against the last run of the same set. No baseline,
   no meaning ({{topic:whyeval}}).
2. **Which cases flipped?** Two cases swapping between pass and fail leave the score unchanged. Read the
   case-by-case comparison before the headline.
3. **Who ran it?** Read the user profile. A maker's run speaks for the maker ({{topic:testidentity}}).
4. **Which passes are false?** Hand-read the passing cases that assert facts, and every refusal and abstention,
   whatever it scored ({{topic:judge}}).
5. **Is it the same next time?** One run is one sample. Run the set two or three times and average before you
   report anything.

A score that survives all five is evidence about the cases in the set. It is still not evidence that the agent
is **finished**.

### Finished is a human call

Microsoft's checklist pairs automated runs with a **human review rubric**: does the response answer the main
question, use the correct information, take the right tone, respect sharing permissions. Your success
criteria made those concrete for this agent ({{topic:successcriteria}}). The pass mark you agreed there, such as
*9 in 10 over three runs*, is a gate. It is not the definition of done. Sample responses, passing ones
included, and score them against the rubric before anyone says *ready*.

## In practice at Technik

The Production Assistant's fourth run after the baseline scored **92%**, up from 83%. Here is the score read
through the five questions:

| Question | What the team found |
|---|---|
| Compared with what? | The baseline recorded with agent version and date: 83% |
| Which cases flipped? | Three fixed, as intended. **One regressed**: the lead-time case now answers with efficiency |
| Who ran it? | The planner test account. The other three groups' accounts not yet run |
| Which passes are false? | One revision case passed while naming revision D, which is In Work: a false positive |
| Same next time? | Two more runs: 92%, 88%. Average 90% |

So *92%* was really this: about 90% averaged, one regression, one false positive, one user group in four.
The rubric review then sampled ten passing work order answers. Two told a supervisor what was blocking a work
order without saying which operation, which fails *act without opening SAP*. Neither had failed General
quality, because both were relevant and complete-sounding.

The report to the production manager carried the average, the regression and its fix, the two rubric findings,
and the line *quality and supervisor runs pending*. It did not carry *92%*.

## Design guidance

- **Change one thing per run.** Otherwise a flip cannot be traced to its cause.
- **Read cases before the score**, starting with the ones that flipped.
- **Ask the five questions** every time, in order.
- **Treat Invalid and Error as gaps in the set**, not as agent failures.
- **Keep every run you might compare against.** Download it or export it, with the agent version.
- **Score a sample against the rubric** before calling the agent finished.
- **Report the average and its context**, never a single run's percentage on its own.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| The score went up and users report a new failure | A regression hidden by fixes elsewhere | Compare runs case by case |
| A percentage is quoted with no baseline or profile | The number travelled without its context | Report the average, the profile and the comparison |
| Several changes in one run, and nobody knows which helped | No single-variable change | One change, one run |
| Invalid or Error results counted as failures | They mean the set lacked something, not the agent | Fix the case or the method |
| A high score, and reviewers still reject answers | Passing is not the same as done | Score a sample against the rubric |
| Last quarter's runs can't be found | Standard-harness results expire after 89 days | Export or download runs you will compare against |

## Key terms

**Score (pass rate)**: the share of test cases that passed in one run.

**Run**: one execution of a test set against one version of the agent, saved separately.

**Human review rubric**: the questions a person uses to judge a response, made concrete by the success
criteria.

**Pass mark**: the agreed score, over several runs, that a set must reach. A gate, not a finish line.

**Invalid / Error**: standard-harness results that mean the case could not be judged, not that the agent
failed.
