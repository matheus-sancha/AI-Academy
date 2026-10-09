## What this module is for

Teams is where work gets talked about: chats, channel threads and meetings. Copilot helps with all
three. It catches you up on a thread, reworks a message you typed, and turns a meeting into notes and
follow-up tasks. It's also the one app module where what Copilot can do depends on a setting somebody
else controls. Whether you can ask about a meeting afterwards depends on whether it was transcribed.

Microsoft's own caution covers all of it: answers *"may not always be accurate as they are generated
based on patterns and probabilities in language data."* In Teams, the cost of an error is usually a
person. A wrong decision gets acted on by a whole channel, and a wrong task lands on someone who never
agreed to it.

The five app modules share a shape (ask, make, one speciality, limits). Teams' speciality is the
meeting recap.

## Before you start

{{module:prompting}} applies to every request here, especially {{topic:clarity}} (ask for decisions
and open questions, not a retelling). {{topic:mailmake}} teaches the habit {{topic:teamsmake}} builds
on: write the facts yourself, then let Copilot change how they read. {{topic:visibility}} explains why
Copilot sees only the chats, channels and meetings you're part of.

Allow about 40 minutes.

## What you will be able to do

By the end of this module you should be able to:

- catch up on a chat or channel thread by asking for decisions and open questions, and check each
  point against its sources;
- name the time frame when a thread is older than 30 days, and open shared files yourself;
- use **Rewrite** and **Adjust** on a message you wrote, and spot where a rewrite changed what it
  means;
- check every follow-up task in a meeting recap against the transcript before passing it on;
- explain why Copilot can answer about one meeting and not another, and what to do before a meeting
  that matters.

## The thread through this module

Every example comes from Technik, the fictional manufacturer this course is built around. See the
[scenario](../scenario/index.html) for the company and its documents.

One change carries the module. `ECN70000042` is released and waiting for revision C of `SWI70000318`,
*Cladding Preparation and Inspection*. Revision C adds an ultrasonic check before cladding and
tightens the porosity limit. A quality engineer catches up on the channel thread about it, posts an
update, reviews it in a meeting, and finds where Copilot's memory of that meeting ends. Only the
documents and the conversations about them are used. No system data is involved.

## Self-check

Answer these before moving on. Each answer explains the reasoning, not just the verdict.

<details>
<summary>1. Copilot says a decision in a six-week-old channel thread is "still under discussion". You remember it being agreed. Who's right?</summary>

Probably you. Unless you say otherwise, Copilot reads only the last 30 days of a thread, counted back
from the latest message. An agreement from five weeks ago is outside that window. Ask again and name
the time frame, such as *"since the ECN was released"*, then open the source it gives. Reread
{{topic:teamsask}}.
</details>

<details>
<summary>2. The draft of a revised work instruction was posted in a thread as a Word file. Copilot's summary says the draft "was shared for review" but not what changed. Why?</summary>

Copilot in Teams can't read files, images or Loop components shared in a chat or channel. It can see
that a file was posted, but not what's in it. Open the file yourself, and ask Copilot in Word if you
want a summary of it. Reread {{topic:teamsask}}.
</details>

<details>
<summary>3. You typed "should be released next week if the inspector is confirmed", and chose Adjust > confident. The new version says "will be released next week". Is that just tone?</summary>

No. The condition is gone, and *should* became *will*. A tone adjustment can turn a hope into a
promise, and a channel post is read by people who will plan around it. Compare every rewrite with
your own words before you select **Replace**, looking hardest at dates and conditions. Reread
{{topic:teamsmake}}.
</details>

<details>
<summary>4. The recap lists "NDT lead to arrange inspector qualification". How do you check it before forwarding the tasks?</summary>

Find the moment in the transcript, using the speaker names and timestamps. Read who said they'd do
it, not who raised it. A recap can attach a task to the person who mentioned it. Correct the task,
post the list where its owners will see it, and ask each to confirm. Reread {{topic:teamsrecap}}.
</details>

<details>
<summary>5. Yesterday's afternoon meeting used Copilot throughout. Today Copilot can't tell you anything it said. What happened, and what would have prevented it?</summary>

The meeting was set to let Copilot run *only during the meeting*, or simply wasn't transcribed. After
the meeting, Copilot answers from the transcript, and without one it has only the meeting chat. The
organiser controls that in the meeting options. Before a meeting whose decisions you'll need, make sure
it's transcribed, or take your own notes. Reread {{topic:teamslimits}}.
</details>
