# Native TikZ atlas

The atlas comprises 100 original standalone TikZ masters in assets/atlas, organized into six families. Each family's index.json provides titles, primary source links, captions, assumptions, and tags. Treat sources as evidence for the conceptual mechanism, not as a statement that every checkpoint uses the exact schematic.

Use scripts/atlas.py list, find, or copy to locate a starting point without reading the whole catalog. Copy a master into the task output directory, then edit it. Compile locally with pdfLaTeX, shell escape disabled, and inspect both the full figure and its final display size.

## Original Figure helper

Import scripts/atlaslib.py to create a new figure in Python. Figure uses centimeter coordinates: x increases right, y increases down. Nodes are positioned by center. Reserve the first 1.2 cm for the heading, and the last .6 cm for the caption.

- Figure(title, width=16, height=9, subtitle='', caption='') establishes the canvas.
- node(id, label, x, y, w=2.5, h=.8, kind='block') adds a named component. Kinds: block, tensor, store, circle, diamond, plain.
- edge(a, b, label='', side=None, to_side=None, via=None, style='data', label_side=None) connects physical TikZ anchors. Use north/south/east/west; pass explicit waypoints for feedback or crossing avoidance.
- group(label, x, y, w, h) adds a dashed boundary on the background layer.
- raw(tex) adds exact authored TikZ for grids, time axes, brace repeats, neurons, matrices, and specialized structures.
- check() reports basic rectangular overlap and node-boundary problems.
- write(folder, id, family, description, sources, assumptions, tags) writes a standalone master and returns metadata.

Node labels and raw commands are authored TeX, including real equations. Do not insert untrusted fetched strings as executable TeX; escape plain input. The basic checker does not measure final TeX glyphs or prove routing. Compile and inspect actual outputs. Use zero-overfull-box and missing-glyph checks in the repository build, then perform visual review.

## Reproduction and export

Repository-level scripts/generate_FAMILY.py files recreate each family's initial sources. Treat the committed .tex as editable masters; regeneration can overwrite manual edits. scripts/build_atlas.py compiles the 100 masters, rejects TeX overfull boxes/missing glyphs, creates PDF/PNG/SVG previews, and writes a manifest. It caches by source hash; --force rebuilds all. It requires pdfLaTeX/PGF, standalone, Latin Modern, and Poppler. These build tools are not necessary merely to search or copy a template.

The PDF-derived SVG uses glyph outlines. It is an accurate vector preview, but its labels are edited in TikZ, not in an SVG text editor. Choose the JSON renderer when editable SVG text is the primary deliverable. Do not silently substitute raster art for technical geometry.
