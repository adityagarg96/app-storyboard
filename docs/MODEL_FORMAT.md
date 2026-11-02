# Input files

`renderer/build.py <dir> <out.html>` reads these from `<dir>`. For a complete working example, see `example/input/` and `example/make_example.py`.

## `model.json`

```jsonc
{
  "provenance": "Where the values came from. Shown on the page.",
  "roles": [{ "key": "manager", "label": "manager" }],   // one set of traces per role; a switch appears if there are 2+
  "endpoint": { "method": "GET", "path": "/api/x", "handler": "file:line" },

  "steps": [{
    "n": 1,                        // order on the page; referenced everywhere below
    "id": "s1",                    // matches the trace filename
    "op": "query",                 // query|call|map|format|join|merge|filter|group|aggregate|sort
    "text": "Under 12 plain words",
    "side": "server",              // server|browser
    "at": "file:line",
    "reads": ["schema.table.column"],
    "flag": null,                  // or one plain sentence if something looks wrong. Be strict.
    "status": "proposed"           // optional: doesn't exist yet
  }],

  "work": [{                       // the lists, maps and values, in order of appearance
    "name": "orders",              // key in the trace
    "step": 2,                     // the step that creates it
    "kind": "list",                // list|map|object|boolean|number|string
    "type": "{id, total}[]"        // short TS-like type
  }],

  "payload": [{                    // every field in the response, plus what the browser derives
    "group": "Response",           // section heading
    "field": "customers[].total",
    "final": { "manager": 65 },    // a value, or one per role
    "token": "Ada",                // optional: in filter mode, show only rows containing this
    "status": "proposed",          // optional
    "via": [{                      // the path that computes it; order by step
      "var": "orders",             // a name from "work"
      "step": 2,
      "why": "Under 10 plain words",
      "at": "file:line",
      "focusCols": ["total"]       // columns to highlight in filter mode
    }]
  }],

  "queries": [{                    // one per query; steps that run it
    "steps": [2],
    "stages": [{
      "tag": "join",               // from|join|where|select|group|union|order
      "plain": "A plain sentence. No SQL.",
      "use": ["schema.table.column"],
      "rows": { "manager": 7 },    // row count at this stage, per role
      "why": "What this stage loses, or null"
    }]
  }],

  "unresolved": ["What the agent could not determine"]
}
```

## `trace_<role>_<stepId>.json`

One per step and role. The renderer reads variables from `vars`, or takes the rows of the last stage.

```jsonc
{ "step": "s1", "vars": { "canSeeRevenue": true } }            // a step that produces values

{ "step": "s2", "stages": [                                    // a step that runs a query
  { "tag": "from orders", "row_count": 8, "rows": [ { "record_id": "101", "total": 40 } ] }
] }
```

- Stages line up with `queries[].stages` by position.
- `transcribed: true` shows a note that values came from a transcription of the code.
- Use a stable `record_id` column across stages where you can. Without one, the first column is used as the row's identity.
- If a stage loses most columns and has no `record_id`, it's treated as changing what a row is, and gets its own result table.

## `tables.json`

```jsonc
[{ "id": "schema.table", "file": "path", "status": "proposed",
   "columns": [{ "name": "shipping_zone", "type": "text", "status": "proposed" }] }]
```

## `screen.json`

```jsonc
{ "regions": [{ "id": "ship", "label": "Shipping panel", "implementedBy": null }],   // null = designed, not built
  "lit": ["ship"] }                                                                  // regions this endpoint feeds
```

## `mock.png` and `mock_bbox.json`

A screenshot of the mock, plus each region's box measured in the page's coordinates.

```jsonc
{ "o": { "ship": [30, 373, 900, 76] },   // [x, y, width, height]; null if not visible
  "w": 960,                              // page width when measured
  "png": 560 }                           // screenshot height at that width
```
