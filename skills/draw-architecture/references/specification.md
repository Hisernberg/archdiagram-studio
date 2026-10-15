# JSON scene specification, version 1

Use [scene.schema.json](scene.schema.json) for editor validation. The runtime validator additionally checks IDs, references, finite values, and geometry.

## Coordinate system

Coordinates are canvas units, increasing right and down. SVG uses those units in its viewBox; TikZ maps each unit to one point. Explicit positions use `x`,`y` at the top-left. Grid placement uses `col`,`row` with origin (60,150), column step 260, row step 160. Do not mix explicit and grid placement. When neither is supplied, nodes default to one row in array order. Automatic placement is a starting layout, not a graph-layout optimizer.

## Top-level fields

| Field | Type / default | Meaning |
|---|---|---|
| `version` | required integer `1` | Schema version |
| `nodes` | required array, 1–200 | Visible components |
| `title` | text / `Architecture` | One-line heading, maximum 160 characters |
| `subtitle` | text / empty | One-line explanatory sentence, max 300 |
| `width`,`height` | finite numbers / derived | Canvas; width >= 520, height >= 180, both <= 20000 |
| `edges` | array / empty | Up to 1000 directed connections |
| `groups` | array / empty | Up to 100 container boundaries |
| `footer` | text / empty | One-line note, max 300 |
| `evidence`,`assumptions` | string arrays / empty | Provenance and unverified choices; included in reports |

Unknown fields are errors. Text is literal; HTML/XML and TeX special characters are escaped. Put newlines in node labels/details when needed. Use native TikZ for equations. Fonts and line-wrap metrics differ by environment.

## Nodes

| Field | Type / default | Meaning |
|---|---|---|
| `id` | required string | Unique; ASCII letter then letters/digits/underscore/hyphen; <=80 chars |
| `label` | text / ID | Main text, max 300 |
| `detail` | text / empty | Supporting text, max 500 |
| `tag` | text / empty | Short uppercase category, max 45 |
| `role` | `compute` | One of input, compute, model, memory, tool, control, output, neutral |
| `kind` | `block` | One of block, tensor, store, junction, decision |
| `x`,`y` | paired numbers | Explicit top-left; 0–20000 |
| `col`,`row` | paired numbers | Grid coordinates; 0–100 |
| `width`,`height` | finite numbers | 24–2000; default 190x84, or 48x48 for junction |

Use `junction` for a short merge symbol such as `+`. Keep decision labels short because their diamond has less text space. Roles choose color; kinds choose shape. Colors do not establish architecture semantics. Increase node sizes for long labels, especially when using tags. Tensor depth is decorative, not a scale.

## Edges

`from` and `to` are required node IDs. Optional fields:

- `label`: literal text, max 160; default empty.
- `kind`: `data` (solid), `control` (dashed), `feedback` (dotted).
- `from_side`,`to_side`: left/right/top/bottom. Defaults follow relative centers.
- `from_offset`,`to_offset`: side-relative offset, -0.45 to 0.45 (default 0); multiply by the side length. Use separate ports for calls, results, and residual branches. Ports follow rectangular bounds; use zero offset for junction/decision shapes.
- `via`: up to 100 `[x,y]` waypoints. These form an explicit polyline; diagonal segments are permitted. Default routes use orthogonal midpoint bends.
- `label_at`: explicit label center `[x,y]`. This is independent of the route.
- `label_pos`: 0–1 distance fraction along the polyline, default 0.5; automatic labels sit 11 units above the chosen point.

Self-loops require explicit waypoints. Automatic routing does not avoid obstacles or reserve ports for multiple edges. Add waypoints and use side-relative offsets when routes would be ambiguous. The renderer does not infer arrow direction from labels.

## Groups

Require a unique `id`; `label` defaults to that ID. Use `members` with existing node IDs to derive a box with 24-unit side/bottom padding and 44-unit top padding. Or supply all of `x`,`y`,`width`,`height` explicitly. When members and an explicit box coexist, the linter checks containment and top title padding. Groups draw behind edges and nodes; overlap between groups is allowed.

## Minimal example

```json
{
  "version": 1,
  "title": "Evidence to answer",
  "nodes": [
    {"id": "retrieve", "label": "Retrieve evidence", "col": 0, "row": 0},
    {"id": "answer", "label": "Generate answer", "col": 1, "row": 0, "role": "model"}
  ],
  "edges": [{"from": "retrieve", "to": "answer"}],
  "assumptions": ["Illustrative flow; no implementation supplied."]
}
```

## CLI and API

`python scripts/archdiagram.py validate FILE.json [--strict]` prints a report. Schema and geometry errors return exit 2; warnings normally return exit 0. `--strict` makes warnings fail. `render FILE.json --out PREFIX --formats svg,tex [--theme paper|midnight|blueprint] [--strict] [--compile-tex]` writes outputs and `PREFIX.report.json`. Extensions are appended to the entire prefix.

The report records source SHA-256, counts, issues, evidence, assumptions, and outputs. A report is not a visual review certificate. Files larger than 2 MB are rejected by the CLI. The Python API exposes `normalize(spec)`, `lint(normalized_spec)`, `render_svg(spec, theme)`, and `render_tikz(spec, theme)`. Rendering functions do not run lint automatically; call it explicitly if using the API.

Missing Inkscape or TeX yields an actionable error. SVG or TeX may already have been written before an optional export fails; the command returns nonzero. Treat a failed optional conversion as incomplete, not as a successful export. Re-render to a fresh output prefix when collecting a final deliverable.
