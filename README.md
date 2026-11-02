# App Storyboard

A way to see a whole web app feature on one page, so you can understand it or design a change to it: which part of the screen calls which endpoint, what that endpoint does step by step, how its JSON response gets built, and what each SQL query does to the data.

An agent reads the code and produces a small model. A generic renderer draws the page. A person explores it, and sees the gaps.

**See it:** run `python3 renderer/build.py example/input example/storyboard.html`, then open `example/storyboard.html`. The example is an invented bookshop.

## The page

Read top to bottom, high level to low level:

| Layer | Question it answers | What's on it |
|---|---|---|
| **A. App** | What is this feature? | The screen → the endpoint behind it → its steps → the tables they touch (names, expandable to columns) |
| *Contents row* | Where am I? | Every step, clickable, pinned while you scroll |
| **B. Response** | How does the JSON get built? | The lists, maps and values in fixed rows, beside the final response shape |
| **C. Data layer** | What does this step's SQL do? | All tables → logical steps → a grid of rows that keeps its layout across stages |

The most useful interaction: **click a value in the response.** The whole page filters to the steps that compute it, and each step shows only the data feeding that value.

## Two ways to use it

1. **Understand an existing feature.** The model is read from code.
2. **Design a change.** Inputs are a mock, a rough data model, and the existing frontend, backend and tables. The storyboard shows what already exists and marks what doesn't with dashed outlines (`status: "proposed"`). Those gaps are the implementation plan. The example shows this: a new "Shipping estimate" panel needs a column and two steps that don't exist yet.

## If you're an agent picking this up

Read in this order:

1. [`docs/FRAMEWORK.md`](docs/FRAMEWORK.md): the idea, and the design rules that matter. Most were learned by getting them wrong.
2. [`docs/AGENT_PLAYBOOK.md`](docs/AGENT_PLAYBOOK.md): how to generate a storyboard for a real codebase, including the database safety rules.
3. [`docs/MODEL_FORMAT.md`](docs/MODEL_FORMAT.md): the files the renderer reads.
4. [`briefs/`](briefs/): prompts for the generating agent and the independent auditor.

The renderer is a starting point, and you're expected to adapt it. It's plain HTML and JavaScript with no dependencies, apart from web fonts.

## What's here

```
README.md
docs/FRAMEWORK.md       the idea and design rules
docs/AGENT_PLAYBOOK.md  how to generate one
docs/MODEL_FORMAT.md    the input files
briefs/                 prompts for the generator and the auditor
renderer/               build.py + template.html
example/                invented bookshop: inputs, generator, mock
```

## License

Copyright (c) 2026 Aditya Garg. All rights reserved. See [`LICENSE`](LICENSE). This repository is public so it can be read and used by its owner across machines. No license to use, copy or modify it is granted to anyone else.
