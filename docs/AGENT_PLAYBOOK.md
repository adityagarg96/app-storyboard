# Generating a storyboard

## Before you start

- **Check you're allowed to send this code to a model.** If the code belongs to an employer or client, follow their policy on AI tools first. Ask if you're unsure.
- **Keep the output private.** A generated model contains real file paths, schema, and notes on possible bugs. Never commit it to this repository, which is public. Keep it in a private location, such as a folder inside the project you're working on, and don't commit it there without asking.

## Database safety (read this first)

A test harness pointed at the wrong database has wiped production data before. These rules exist to make that impossible:

1. **Never connect to a shared or production database** to build a storyboard, unless the owner explicitly says so for this task. Then read-only, bounded, with a statement timeout.
2. **Never read `.env` files or credentials.**
3. **Never import or run the application's code, its migrations, or its tests.** Its configuration can open a real connection. Read those files as text.
4. **Use the team's seeded local dev database if there is one,** after confirming with its owner that it's local. Otherwise create a throwaway cluster:
   - in a new folder, listening on a Unix socket only (`listen_addresses=''`), on a non-default port
   - with every command run through `env -i` so no `PG*` variable can leak in
   - scripts hard-code that socket and read no environment variables
   - run `SHOW data_directory` first, and confirm it's your folder
   - stop it and delete it when you're done, and confirm that
5. **Seed data is invented.** Use obviously fake names.
6. **Don't copy real customer data into a model.** If you were given real data, mask personal fields.

## Inputs

**To understand a feature:** the frontend and backend code, table definitions, and a screenshot or mock of the screen.

**To design a change:** the same, plus the new mock and the rough data model. Expect the data model to be vague, and list what it leaves open under `unresolved` rather than guessing.

## Steps

### 1. Map the screen
Find which page the mock actually corresponds to, and check it. On a real run, the obvious-looking design file turned out to be for a different page. List each meaningful region of the mock with a CSS selector, and what implements it. Render the mock in headless Chrome, take a screenshot, and measure each region's box.

Note mismatches in both directions: designed but not built, and built but not designed.

### 2. Trace each endpoint
Extract **every** endpoint the screen calls. Never cap or sample. A big app should stay manageable through grouping and filtering, not by leaving things out.

For each step, record what it does in plain language, its `file:line`, the columns it reads, and what it produces. Don't forget what happens **outside** the handler, because that's where a real audit found the worst errors: authentication middleware (where does the role really come from?) and request ordering (what waits for what on the frontend?).

### 3. Write down what you expect, then run it
Seed a small fixture that exercises every branch: nulls, mismatched keys, soft-deleted rows, duplicates, permission differences.

**Before running any query**, write down the values you expect. Don't edit that file afterward. Then run the real SQL, copied from the code, breaking each query into stages. Record real rows for each stage and each role.

Run non-SQL logic by transcribing it into your own small script, and mark those values `transcribed`. Be honest about what this proves: if you wrote both the seed and the expectations, a perfect match shows you read the code consistently. It doesn't show you covered what matters. On a real run, actually executing the SQL found a bug that reading alone had missed.

### 4. Write the model
See [`MODEL_FORMAT.md`](MODEL_FORMAT.md). For every response field, give the path that computes it, with a real `file:line` for each link. Write `unresolved` for what you can't determine. Mark guesses `inferred: true`.

### 5. Get it audited
Start a separate agent with [`briefs/auditor.md`](../briefs/auditor.md). It sees the model and the source, but not your notes or reasoning. Fix what it finds, or report it. As a benchmark, an audit of one real endpoint found 137 of 170 items correct, 29 partly right and 4 wrong; the wrong ones were mostly about what happens outside the handler.

### 6. Render and check it
Run `python3 renderer/build.py <input-dir> <output.html>`, and test it with a script. Measure rather than eyeball:

- Grid positions are identical across stages.
- Rows the page strikes out match the model's `lost` counts. Computing these from raw rows gives you an independent check.
- Every response field's path walks from start to finish.
- No cells are cut off, and no sideways page overflow.
- **Test every state.** A bug once looked fixed because only the last stage was measured.

### 7. For a design: read off the plan
Mark anything that doesn't exist yet as `status: "proposed"`: tables, columns, steps, response fields. Regions with `implementedBy: null` show as designed but not built. Give each proposed step representative values, and say they're invented in `provenance`.

Then write the build order from the dependencies: schema first (including whatever populates new tables, which is easy to miss), then endpoints whose gaps are closed, then wiring the screen, then empty states. Bring the open questions in `unresolved` to the person, since those are the real decisions.

## Known limits of the renderer

- **One endpoint per page.** A real screen calls several. Adapt it with one page per endpoint and an index, or several endpoints on one page. Clicking a region of the mock should open the endpoints behind it.
- **Too many fields gets unreadable.** A real endpoint produced 79 response fields, mostly near-duplicates across item types. Group them, and show repeated shapes once.
- **Tracing starts from the response.** Starting from a number on the mock would be better, and isn't built.
- **Paths are written by an agent,** so they can be wrong in the ways listed above.
- **Generation took about 12 minutes** for one endpoint with 15 steps. Budget for that per endpoint, and stream results to disk so a stopped run keeps its work.
