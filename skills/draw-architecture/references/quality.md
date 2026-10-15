# Quality gates

## Semantic review

Read the original evidence before choosing a template. Confirm each component, arrow direction, label, boundary, and merge. Distinguish data moving between services from a control request sent to a service. Do not present a monitoring component as proof of system correctness. Label logical modules separately from deployment processes.

For agents, show tool-call and tool-result paths. Show retry/stop criteria where known. Distinguish a context read from persistent memory writes. For RAG, separate indexing from queries, preserve source identities, and use compatible document/query embeddings. For neural figures, label shape conventions and residual origins. For robotics, distinguish observations, estimated state, commands, and physical state.

## Layout review

Use 1–2 primary reading directions. Aim for 4–7 conceptual blocks per panel; split large systems into an overview plus detail panels. Preserve a consistent grid and spacing. Keep arrowheads outside labels and on meaningful ports. Route long edges around blocks. Keep storage and feedback paths in reserved lanes.

Run `validate --strict`, then inspect the exported figure. The linter detects rectangular node overlaps, basic canvas overflow, approximate text height, edge intersections with unrelated rectangular node bounds, and approximate edge-label collisions. It does not prove arrow intent, detect all crossing edges, measure actual font glyphs, or verify color contrast. Explicit group boxes are containers, so overlapping groups are not automatically errors.

## Visual review

Inspect the full-resolution PNG or PDF. Check text, line ends, outlines, legend, group headers, and crop boundaries. Inspect a reduced copy at the intended width. A 1,200 px diagram embedded at 600 px halves every font size. For a paper column, simplify the figure until the final text is comfortably readable; do not solve density by shrinking fonts. Re-check PNG and PDF when font substitution changes the layout.

Keep SVG text as `<text>` elements and preserve the JSON/TikZ source. SVG includes a title and textual description for accessibility. Do not rely on color alone: labels, grouping, and line patterns carry meaning. Use the paper theme for print; inspect grayscale if grayscale reproduction matters.

## Acceptance rubric

Score each category 0 (fails), 1 (needs revision), or 2 (ready): semantic fidelity; abstraction consistency; edge clarity; text at final width; editable-source completeness; reproducibility/provenance. Resolve any 0. Treat this rubric as a human/agent review aid, not a measured benchmark. Record actual inspection and assumptions in the handoff; never report visual approval solely from a validator.
