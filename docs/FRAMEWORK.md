# The framework

## The idea

Understanding a web feature usually means holding a chain in your head: this box on the screen, calls that endpoint, which runs these steps, which reads those columns. Reading code gives you the chain one file at a time. Asking an AI gives you an answer you have to ask for again next time.

A storyboard puts the chain on one page that stays put, so your eyes do the work. An agent does the reading and keeps the page accurate. The person does the judging.

It rests on an idea from Colin Ware's *Visual Thinking for Design*: a stable display works as external memory. You don't need to see everything at once, as long as any question can be answered with a glance at a place you already know.

## The layers

**A. App: what the feature is.** Screen → endpoint → steps → table names, expandable to columns. Keep this high level. It should answer "what does this step touch?", not "what's in that column?"

**Contents row.** Every step as a clickable chip, pinned while scrolling. It lets you change steps from anywhere, without scrolling back up.

**B. Response: how the JSON gets built.** This layer answers one question. On the left, every list, map and value in fixed rows, each one blank until it exists. On the right, the final response shape, each field blank until it's computed. Rows open to be inspected, with sorting and filtering.

**C. Data layer: what this step's SQL does.** Only for steps that run SQL, and only that step's query. All tables with columns → the query's logical steps in plain language → a grid of the data at that stage.

Going down the page goes from high level to low level. Most steps have no SQL, so the response layer comes first.

## The filter: click a value

Clicking a value in the response makes the page act as a filter for that value:

- Only the steps that compute it stay lit, in both the step list and the contents row.
- The left side shrinks to only the structures that feed it.
- Each structure shows only the relevant rows, with the relevant columns highlighted.
- Previous and Next walk the path. Later structures stay as faint names, so you see the value only up to that point.

This is the answer to "people don't read code line by line anymore." You start from a number you care about and walk backward through the steps that made it. Don't build this as a separate list of steps beside an otherwise unchanged page. It was tried, and it was confusing.

## Design rules

**Positions don't move.** Rows and columns keep their place from the first stage. Things that don't exist yet, or were dropped, go blank in place. This keeps the map in your head. Column widths must be fixed too, or they shift with the data. Test this by measuring positions across stages. The exceptions are ones the user asks for: opening a row, and entering filter mode.

**Controls change emphasis, not layout.** A slider or filter fades things where they stand. It doesn't add, remove or reorder them.

**Keep the meaningful order.** Steps stay in process order and stages in logical order. Don't re-sort them to make a chart tidier.

**No raw code.** Show what a query does in plain language. Raw SQL with line numbers was rejected on sight. Keep `file:line` as a reference.

**Logical order isn't execution order.** Stages show how a query reads logically. The database may run them in another order. Say so on the page, and don't call it "as it runs."

**A stage that changes what a row is gets its own table.** When rows collapse (per attempt → per card, per order → per customer), matching them to earlier rows by `id` gives wrong results, because `id` no longer means the same thing. Show the result in a separate table that fills in at that stage.

**Every mark explains itself.** Axes have plain titles. Colors have an on-page legend. Red and green only mean bad and good. A click reveals evidence, and never edits a fact.

**Flags are a plain red dot.** The explanation appears when you click the step. Don't number them; "finding 9" on step 2 only confused people. Be strict about what gets flagged. On a real run an agent flagged 11 of 15 steps, which made the dot meaningless.

**Tell invented data from real data on the page.** Say what the values are and where they came from.

## What was tried and rejected

| Tried | Why it failed |
|---|---|
| Showing the raw SQL beside its stages | It reads as raw code, and people ignored it |
| Stages nested in the step list, all in one wide row | Too confusing |
| Data model always visible in a sticky side panel | Only useful in the data layer; it cost width everywhere else |
| A strip of bars showing row counts per step | Meant nothing to the reader; a plain table of contents worked instead |
| Per-step cards chosen from a catalog of chart types | Confusing here. Charts are evidence for a decision, not part of this view |

## What it doesn't do

- **It doesn't replace running the code.** Paths are read by an agent, so check them.
- **It isn't a time-travel debugger.** Stepping through execution line by line is too granular. The unit here is a meaningful data step.
- **It doesn't make decisions.** This repo covers the structure and the data. Choosing what to build stays with the person.
