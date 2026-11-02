# Brief: generate a storyboard model

Adapt the bracketed parts, and give this to a fresh agent. First read `docs/AGENT_PLAYBOOK.md` and `docs/MODEL_FORMAT.md` in this repo. The playbook's database safety rules are mandatory.

---

Generate a storyboard model for [PAGE or NEW MOCK]. Code: [FRONTEND PATH], [BACKEND PATH]. Table definitions: [SCHEMA PATH]. [For a design: the new mock is at PATH, and the rough data model is at PATH.]

Write everything to [PRIVATE OUTPUT DIR], and nothing anywhere else. Read application code as text only: don't run or import it, don't read `.env` files or credentials, and don't connect to any shared database. Use [THE LOCAL DEV DATABASE, or A THROWAWAY CLUSTER per the playbook].

Steps, writing each file as soon as it's done so a stopped run keeps its work. On restart, skip what exists.

1. Confirm which mock matches which page. List regions with selectors, and mismatches in both directions.
2. List every endpoint the screen calls. Do not cap or sample. Do one endpoint fully first, then report before continuing.
3. Write `ddl.sql` for only the tables and columns involved, and `seed.sql` with invented data that exercises every branch: nulls, mismatched keys, soft-deleted rows, duplicates, permission differences.
4. Write `expected.json` from the seed and the code text, BEFORE running any query, for each role. Don't edit it afterward.
5. Run the actual SQL, copied from the code with only parameters substituted. Break each query into stages, recording rows per stage per role. Transcribe non-SQL logic into your own script, and mark those values `transcribed`.
6. Write `compare.md`: expected vs. actual, explaining every mismatch.
7. Write the model files per `docs/MODEL_FORMAT.md`. Cover every response field and what the browser derives from it. Every link in a path needs a real `file:line`. Include what happens outside the handler: authentication, and what the frontend waits for. Mark guesses `inferred: true`, and list what you can't determine under `unresolved`. [For a design: mark everything that doesn't exist yet `status: "proposed"`, and write the build order, including what populates new tables.]
8. Flag a step only if a reader should stop and look at it. If you're flagging more than about a quarter of the steps, raise your bar.
9. Write `NOTES.md`: what was hard, what you guessed, and bugs, separating "demonstrated on seed" from "read in code."

Stop and report if this passes [40] minutes per endpoint. Clean up any database you created, and confirm that it's gone.
