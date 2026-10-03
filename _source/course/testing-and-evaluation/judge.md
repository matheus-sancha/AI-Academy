## TL;DR

On the GitHub Copilot harness, an evaluation is graded by a **model**, not by comparison against an expected
answer. Its one test method, **General quality**, assesses whether a response meets quality standards such as
relevance and completeness. Microsoft states outright that it **does not compare responses to expected
answers**. So the question is the whole lever: a vague question lets almost any relevant answer pass. Write
expected responses anyway, as **what a correct answer must contain**, never as literal wording. They are for
the human who audits a failure, not for the grader.

## Why it matters

Engineers arrive at evaluation with a unit-test picture: you write the expected output, and the tool diffs the
actual output against it. Hold that picture on this harness and you write the wrong test set. You polish
expected answers nobody reads, you leave the questions loose, and you trust a pass that only means *the agent
said something relevant and complete-sounding*.

The failure is quiet: the score looks healthy while the agent tells a planner that revision C is current.

## How it works

### One method, and what it measures

<!-- volatile verified=2026-10 -->
The GitHub Copilot harness's **Evaluate** tab (preview) offers one test method today: **General quality**,
described as an AI-based assessment of whether responses meet quality standards, such as relevance and
completeness. Each test case gets **Pass** or **Fail**, and the run's score is the share of conversations that
passed. A case may carry an expected agent response, but Microsoft's note on the method is unambiguous: General
quality doesn't compare responses to expected answers.
<!-- /volatile -->

<!-- verified tenant=2026-09 -->
The product's own CSV template says it again, of its `response` column: *the agent response isn't compared to
this reference answer.*
<!-- /verified -->

The standard harness documents the same method in more detail. A large language model scores each response
against four criteria, with a consistent prompt:

| Criterion | The question the grader asks |
|---|---|
| **Relevance** | Does the response stay on the subject and address the question? |
| **Groundedness** | Is it based on the context the agent retrieved, rather than unsupported information? |
| **Completeness** | Does it cover every aspect of the question in enough detail? |
| **Abstention** | Did the agent attempt to answer? |

A response has to meet all of them to score well. It needs no expected answers.

<!-- unknown since=2026-10 -->
The GitHub Copilot harness's pages name only relevance and completeness, with *"such as"* in front. Whether
its General quality also applies the groundedness and abstention criteria the standard harness documents is
not stated.
<!-- /unknown -->

### What a grader with no answer key cannot know

Nothing in the criteria knows **your** facts. The grader can tell that an
answer about a drawing revision is on topic, complete, and drawn from what a tool returned. It cannot tell that
revision C is still *In Work* at Technik unless that is visible in the conversation it grades. *Correct for
your business* is not one of the criteria.

That is why the roadmap calls the question the entire lever. The grader judges the response **against the
question**, so the question has to carry the standard:

| Vague question | What passes | Sharper question | What it now demands |
|---|---|---|---|
| *Tell me about `DU700001042`.* | Any on-topic summary | *What's the latest **released** revision of `DU700001042`, and which ECN released it?* | A revision, a release, and an ECN number |
| *Any QN problems on `PRJ-2031`?* | A general remark about quality | *List the open QNs on cladding for `PRJ-2031`, with number, defect type and priority.* | A list, filtered, with three fields each |

A complete answer to the sharper question has to commit to specifics, and a missing ECN number now makes it
incomplete. It still cannot make the grader know *which* revision is right. That part is yours.

### Expected responses: for the auditor

Write an expected response for every case anyway. When a case fails, or passes suspiciously, the person
reviewing it needs to know what was supposed to happen. Microsoft's evaluation checklist also pairs every test
prompt with **acceptance criteria**: what passes and what does not.

Write them as **content, not wording**:

> **Weak:** *The latest released revision of DU700001042 is B, released by ECN70000031.*
>
> **Strong:** *Must name revision B as the latest released revision. Must name the ECN that released it. Must
> not call revision C current. Should say C is In Work if it mentions C.*

The strong version survives any phrasing, and a move to a method that does use an expected answer. The standard harness has several: **Compare meaning** scores intent against
the expected answer, **Keyword match** checks for required words or phrases, **Text similarity** and **Exact
match** compare wording, and **Tool use** checks which tools or topics ran. A *must contain* list converts
straight into keywords and meanings; a literal sentence, only into an exact match.

### Refusals and abstentions

The abstention criterion has a consequence Microsoft spells out for the standard harness. If a case expects the
agent to refuse, General quality can flag the response for improvement, because it scores whether the agent
attempted to answer. The standard harness's fix is a **Custom** test method, with evaluation instructions and
labels that define the expected refusal.

<!-- unknown since=2026-10 -->
The GitHub Copilot harness offers no Custom method. Whether its General quality marks a correct refusal or a
correct *"I could not find that in my sources"* as a failure is not documented.
<!-- /unknown -->

Until that is known, read every refusal and abstention case by hand, whatever it scored.

## In practice at Technik

The Production Assistant's evaluation set includes this case:

| Field | Content |
|---|---|
| **Question** | *What's the latest released revision of drawing `DU700001042`, and which ECN changed it?* |
| **Expected response** | Must name revision B as latest released and the ECN that released it. Must not call C current. |

In the first run it **passes**, and the response names revision C. It is on topic, names a revision and an
ECN, and comes straight from the revision tool's output: a good answer by every criterion above. Only the expected response shows that it is wrong. Microsoft's checklist names this case: a **false
positive**, an answer marked passing that should fail on human judgement.

Two cases from {{topic:rules}} need the same hand check, for the opposite reason. *"Four indications of
overlay porosity on `XT-V2-1042`. Is that acceptable?"* is correct only as a refusal that names the
assigned quality engineer. *"What is the minimum overlay thickness for Inconel on a manifold header?"* is
correct only as an abstention. Either one may fail on the grader's scoring while being exactly right.

So the team hand-reads three kinds of case on every run: fact-asserting passes, refusals and abstentions.

## Design guidance

- **Sharpen the question until a complete answer must commit to specifics.** It is the grader's only standard.
- **Write an expected response for every case**, as must-contain and must-not-contain lines.
- **Audit passes, not only failures.** Sample passing cases that assert facts; look for false positives.
- **Read refusal and abstention cases by hand**, whatever they scored.
- **Treat the score as relevance and completeness**, not as correctness against your systems.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Polished expected answers, and the score ignores them | General quality does not compare against expected answers | Write expected responses for the reviewer; sharpen the question |
| Everything passes, and users report wrong facts | The grader cannot know your facts | Hand-check fact-asserting passes against the expected response |
| A correct refusal shows as a failure | The abstention criterion scores whether the agent attempted an answer | Read refusal cases by hand; on the standard harness, use a Custom method |
| Loose questions pass whatever the agent says | A vague question accepts any relevant answer | Rewrite it so a complete answer must name specifics |

## Key terms

**Grader**: the model that scores each test case's response.

**General quality**: the test method that scores relevance and completeness (and, on the standard harness,
groundedness and abstention) without an expected answer. The only method on the GitHub Copilot harness.

**Expected response**: what a correct answer must contain, written for the person auditing a result.

**Acceptance criteria**: what passes and what does not, written beside each test prompt.

**False positive**: a case marked passing that should fail on human judgement.
