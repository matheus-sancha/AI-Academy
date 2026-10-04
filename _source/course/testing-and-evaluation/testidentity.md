## TL;DR

An evaluation runs **as somebody**, and that identity decides what the agent's knowledge and tools return. Run
it as the maker, who can usually see everything, and the score describes an agent your users never meet. On
the GitHub Copilot harness an evaluation runs as **whoever is signed in** to Copilot Studio, so choosing the
identity means signing in as it. Decide who each run is for **before** you run anything, and treat a
suspiciously clean first run as a reason to check. This is {{topic:connauth}}'s question, arriving where it is
easiest to miss.

## Why it matters

Most evaluation failures are loud: a case fails, you read why. This one is a **pass**.

The agent's builder has the widest access in the room. They created its connections, they can open every
library its knowledge points at, and they have probably been granted things along the way to get the build
working. An evaluation run under that identity finds every document and gets every result, and the score is
excellent. Then the agent is shared, and a planner who cannot open half of those sources gets *"I could not find
that"* to questions the set says it answers.

Nothing in the run was wrong. It measured the agent correctly, for the wrong person.

## How it works

### Which parts of the agent care who is asking

Not every part of an agent changes with the identity. Sort them first, using {{topic:connauth}}'s modes:

| Part | Runs as | Does the test identity change the result? |
|---|---|---|
| SharePoint and OneDrive knowledge | The person asking ({{topic:sources}}) | **Yes.** It returns only what that person can open, and returns nothing silently otherwise |
| A connector tool with end-user credentials (the default) | The person asking | **Yes.** It runs with their permissions, and needs their working connection |
| A connector tool with maker-provided credentials | The maker, for everyone | No. And every user gets the maker's access |
| A tool on a service identity | That identity, for everyone | No |

Only the rows marked *yes* need runs under more than one identity. But those rows are usually where the
answers differ most between groups of users, and differences between users are exactly what the maker's run
cannot show.

### On the GitHub Copilot harness

<!-- volatile verified=2026-10 -->
An evaluation runs with the **signed-in user profile**, and only that profile can run one. To run it as
someone else, sign out of Copilot Studio and sign in with that account before you start. The run's summary
records the **User profile** that ran it. Evaluations support agents set to *No authentication* or
*Authenticate with Microsoft* only; *Authenticate manually* is not supported, and this harness does not offer it
anyway ({{topic:agentauth}}).
<!-- /volatile -->

In practice that means a **test account per user group** you care about, each with the access a real member of
that group has. Not more, because then it is the maker's run again. Not less, because then every case fails for
a reason no user would hit.

### On the standard harness

<!-- volatile verified=2026-10 -->
Each test set carries its own user profile. **Manage profile** lets you pick a different account, such as a
test account. Copilot Studio authenticates it, fetches that user's existing connections, and asks you to fix
any that are broken: if you use a profile, all its connections must be working. Microsoft's example is the
point of the feature: a director's profile can reach different knowledge sources than an intern's, and the
agent returns different results. Test results show which profile was used.
<!-- /volatile -->

<!-- unknown since=2026-10 -->
Microsoft says a profile is optional on the standard harness. What a run with no profile does with knowledge
and tools that need the user's sign-in, whether it skips them, fails the case or errors, is not documented.
<!-- /unknown -->

Two more standard-harness facts follow from the same identity. Generating cases reads knowledge and tools as the
connected account, so generated questions can contain data that account can see, and every maker with access
to the agent can read the set. And evaluations that use user authentication go through the **Microsoft Copilot
Studio connector**. If an admin's data policy blocks it, the evaluation tool stops working ({{topic:dlp}}).

### The suspiciously clean run

A first run that passes everything is not good news until you know who ran it. Check these in order:

1. **Which profile ran it?** Read the run summary. If it is the maker, the run speaks for the maker.
2. **Did the per-user parts answer?** Open the cases that depend on SharePoint knowledge or end-user tools. A
   pass that cites a document the target group cannot open is a pass for the wrong person.
3. **Does any tool use maker-provided credentials?** Then every user gets the maker's access, and the run is
   right to pass. That is a {{topic:connauth}} finding, not an evaluation one.

## In practice at Technik

The Production Assistant reads work orders, QNs and revisions through tools on `TECHNIK_AGENT_RO`, the same
for everyone. Its knowledge is two SharePoint sources, and those run as the asking user ({{topic:sources}}). So
the tools need one identity's run, and the knowledge needs one per group.

The first baseline ran under the maker's account and passed every case. Planners are the largest user group, and the
**Controlled Documents** library is permissioned per document. Planners can read work instructions, but not
`DGL70000009` or the *Weld Overlay Acceptance Criteria* page on the **Standards** site.

The set ran again signed in as a planner test account:

| Case | Maker | Planner account |
|---|---|---|
| *Which document covers weld prep inspection?* | Pass, cites `SWI70000318` | Pass, cites `SWI70000318` |
| *What's the acceptance criterion for overlay porosity?* | Pass, cites the Standards page | **Fail**: *"I could not find that in my sources"* |
| *Any design guidance on cladding thickness?* | Pass, cites `DGL70000009` | **Fail**: the same abstention |
| Work order, QN and revision cases | All pass | All pass |

Both failures are the agent behaving correctly: it abstains rather than inventing, and permissions are
working ({{topic:citations}}). The real finding was in the brief. Planners do ask about acceptance criteria. The
team added a refusal path: when a planner asks one, the agent says the criteria are held by quality, and names
the document owner from `TC_DOCUMENTS.OWNER`. The set now runs under four accounts, one per user
group, and each run is recorded with its profile.

## Design guidance

- **List which parts of the agent run as the user** before you plan any runs.
- **Never baseline under the maker's account** unless the maker is a user.
- **Keep one test account per user group**, with that group's real access and nothing more.
- **Record the profile with every run**, beside the agent version and date ({{topic:whyeval}}).
- **Check the profile first** when a first run is perfect.
- **Treat a correct abstention under a narrow profile as a design question** for the brief, not a bug.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A perfect first run, then *"I could not find that"* from users | The set ran as the maker | Re-run signed in as a test account per user group |
| A case fails for one account and passes for another | Per-user knowledge, working as designed | Decide in the brief what that group should get |
| Every user sees everything the maker can | A tool uses maker-provided credentials | Fix the connection ({{topic:connauth}}), then re-run |
| The evaluation tool stopped working after a policy change | The Copilot Studio connector is blocked | Ask the admin about the data policy ({{topic:dlp}}) |
| Generated cases quote restricted content | They were generated as a privileged account | Generate under an account scoped like your users |

## Key terms

**User profile**: the identity an evaluation runs as. It decides what per-user knowledge and tools return.

**Test account**: a non-personal account with one user group's real access, used to run evaluations as that
group.

**Per-user part**: knowledge or a tool that runs with the asking user's permissions, so its result depends on
who asks.

**Maker's run**: an evaluation run under the builder's own account. It is a valid run for the maker, and for no
one else.
