# Validation record

Release: 2.0.0. Local checks performed on 2026-10-15. Machine-readable results are in [validation.json](validation.json).

## Portable code and skill

**40 standard-library unit tests passed on Python 3.12.** They cover deterministic SVG/TikZ generation, XML validity, accessibility/editable text, Unicode SVG text, literal TeX escaping, malformed schemas, duplicate IDs, invalid endpoints, coordinate/port handling, geometric diagnostics, CLI behavior, installer preservation, the exact 100-figure inventory, atlas search/copy, and the monochrome paper palette. Host skill metadata validation passed.

The portable search/copy tool needs only Python 3.10+. Native compilation uses TeX, and PDF-to-SVG/PNG conversion uses Poppler. Contact sheets additionally use Pillow. The local LuaLaTeX installation lacked some modules; the JSON renderer's tested fallback used pdfLaTeX. The native atlas uses pdfLaTeX directly with shell escape disabled.

## The 100 native atlas figures

All **100 standalone TikZ masters** compiled successfully. The build rejected overfull boxes and missing glyphs; none remained. Exact family counts are vision 20, text 20, audio 20, multimodal 15, agents 15, and robotics/graphs 10.

The artifact audit verified all 500 figure files: 100 each of TikZ, PDF, SVG, PNG, and metadata JSON. It compared source SHA-256 values, copied masters, and current metadata; parsed every SVG as XML; validated PNG chunk lengths, CRCs, compressed-stream completion, and decoding; and checked PDF end markers. Separate pdfinfo checks successfully read every one-page vector PDF. Pixel-channel comparisons confirmed that **every atlas PNG is grayscale**.

This audit caught three truncated PNG exports and a backslash interpretation problem in an SVG description. The affected exports were rebuilt, metadata was corrected, and payload checks now run on both cached and newly generated exports. Contact-sheet generation also decodes its saved outputs before reporting success.

Atlas SVG previews use outlined glyphs from PDF conversion. The native TikZ is the editable master. The separate JSON renderer preserves SVG text and shapes and supplies six additional system examples. Three further native math/neuron templates are also included.

## Visual and semantic review

Six agents independently authored and reviewed their assigned families. Each compiled and rasterized its sources, checked logs, inspected contact sheets, and examined complex figures at a larger size. The combined review covered topology, labels, crop, residual origins, encoder/decoder input origins, training versus inference, objectives, message directions, waveform/grid semantics, and crossings. The primary agent also inspected family sheets and desktop/mobile gallery screenshots.

Several revisions improved the actual figures: visible background routes, separate tool/result ports, explicit projection or identity assumptions, bounded storage nodes, and separated detail callouts. The diagrams are original conceptual schematics linked to primary technical sources. They are not exact reproductions of every checkpoint, and symbolic signal panels are not measured observations. Neither clean logs nor geometric checks prove architectural correctness.

## Fresh agent tasks

Two agents used the initial skill with only a concrete task and the skill path. They created and visually checked new artifacts without the implementation history:

1. **Query-time RAG with citation revision:** eight components/eight relationships, an existing document index, retrieval, reranking, generation, citation checking, and an explicit revision route. Strict lint reported zero issues; editable SVG/TikZ, PNG, and both SVG-derived and TeX-derived PDFs were produced.
2. **Single-head cross-attention:** decoder states supplied Q, encoder states supplied K/V, with the scaled dot-product formula and appropriate sequence dimensions. No unrequested mask, residual, or output projection was introduced. Compiled one-page PDF and raster inspection passed; the reviewed source is included as a native template.

These are concrete transfer checks rather than a statistical benchmark. A figure still requires evidence and inspection for its actual task.

## Browser and distribution

A headless Chromium run exercised all **100 selections and 400 download links**. Every SVG loaded. All six family filters returned their expected counts. Matching and empty-result searches, Home/End keyboard navigation, zoom/reset, clipboard installation/prompt actions, and a 390 px mobile viewport passed. No page errors, HTTP failures, or horizontal mobile-page overflow were observed.

The historical [v1 hosted CI run](https://github.com/Hisernberg/archdiagram-studio/actions/runs/38686980040) passed four Linux/Windows × Python 3.10/3.12 test jobs plus the figure build for implementation commit 5e4c5d90bc71cbae4fdd4f8b06e217d28f7b100b. It does not establish the result of the expanded v2 build. The current workflow recompiles all 100 native masters; see [Actions](https://github.com/Hisernberg/archdiagram-studio/actions) for subsequent runs.

All 11 originally requested unique repositories have pinned source and license observations. Original code, templates, and figures are MIT. Upstream code and reference-study images are not vendored. Publishing credentials are kept outside the repository.
