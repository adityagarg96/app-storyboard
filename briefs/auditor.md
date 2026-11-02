# Brief: audit a storyboard model

Give this to a fresh agent that didn't generate the model.

---

You're auditing machine-generated claims about source code. Assume they contain errors; your job is to find them.

Claims: [PATH]/model.json. Do NOT open any other file in that folder (notes, comparisons, expected values, traces, seed). They contain the author's reasoning and would bias you.

Source of truth, read as text only: [BACKEND PATH], [FRONTEND PATH], [SCHEMA PATH]. Never run anything, never read `.env` files, never connect to a database, and don't edit those repos.

Check:

1. **Coverage:** list every field the endpoint actually returns. Which are missing from the model? Which in the model don't exist?
2. **Paths:** for every `payload` field (at least 20, including every money and count field and everything the browser derives), walk its `via` chain through the code. Does the cited line contain that? Is the `why` true? Is a necessary step missing? Is a step present that doesn't affect the value?
3. **Steps:** are they in true execution order, including what the frontend waits for? Is anything outside the handler missing, such as authentication? Do `reads` match the SQL (spot-check at least 10)?
4. **Stages:** do `use` and `why` match the SQL? Are there invented columns?
5. **Flags:** is each one actually true from the code?

Append one JSON line per item to [OUTPUT PATH] as you go: `{"item","kind":"coverage|via|step|stage|flag","verdict":"correct|wrong|partly|cannot_tell","evidence":"file:line and short verbatim code","why":"under 25 words"}`. Record correct items too, so the error rate can be computed.

Final message under 150 words: counts by verdict per kind, and the 3 most serious errors with `file:line`.
