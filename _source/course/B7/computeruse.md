Computer use lets an agent work a website or a desktop application the way a person does: reading
the screen, clicking, typing, scrolling. It exists for systems with no API and no connector — and in
a manufacturing business there are always a few.

## When it is the right answer

Genuinely only when there is no alternative. The order to work through is: connector action, then
custom connector over whatever API exists, then a database or data warehouse copy of the data, then
an export or file drop someone already produces — and only then computer use.

It is slower than every option above it, by an order of magnitude. It is more fragile: a relocated
button, a new consent dialog or a slow page breaks a working automation with no code change. And it
is harder to reason about, because what it did is a sequence of clicks rather than a call with
parameters.

<!-- volatile verified=2026-09 -->
Copilot Studio exposes computer use as a tool type, with its own licensing and consumption
implications and its own set of supported targets. It is an area of rapid change — check the linked
documentation for current capabilities, limits and cost before planning anything around it.
<!-- /volatile -->

## Where it would fit at Technik

A supplier portal that publishes material certificates and offers no API, no feed and no export. A
person logs in weekly and downloads PDFs. Computer use could do that, and the certificates then flow
into the extraction pipeline B9 and A10 build.

Notice what the design does with it: computer use fetches a file, and everything afterwards is
ordinary automation. That is the pattern to aim for — use it at the edge, to get data *out* of a
closed system, and never in the middle of a process where a misclick has consequences.

What it should not do at Technik: anything in SAP or Teamcenter. Both are reachable through the
Snowflake replication, and driving a screen to read data you can query is the wrong answer to a
problem you have already solved.

## Design guidance

- Exhaust every alternative first, and write down why each was rejected. You will be asked.
- Use it to **read**, not to **write**. A failed read is a retry; a failed write is a support ticket
  with a data-correction attached.
- Assume it will break, and plan how you will know: monitoring, a heartbeat, an alert on a missing
  file.
- Give it a dedicated account with the least access that works, never a person's credentials.
- Budget for consumption and for maintenance. Both are higher than they look in a demo.
- Never put it in a path where nobody would notice if it silently stopped.

## Key terms

**Computer use** — an agent operating a user interface directly: reading the screen, clicking,
typing.

**Brittleness** — sensitivity to changes that break the automation without breaking the application.

**Headless automation** — driving an application without a visible interface. Faster, and still
brittle.

**Robotic process automation (RPA)** — the older, broader name for automating work through a user
interface. Power Automate desktop flows are the Power Platform version.
