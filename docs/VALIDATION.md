# Validation record

Release: 1.0.0. Checks performed during creation on 2026-10-15.

## Portable code

37 standard-library unit tests passed on local Python 3.12. Tests cover valid examples, deterministic SVG/TikZ generation, XML validity, editable/accessibility text, Unicode SVG text, literal TeX escaping, malformed schemas, duplicate IDs, invalid endpoints, coordinate handling, port offsets, geometric diagnostics, CLI exit behavior, and installer preservation of an existing modified skill. Host skill metadata validation also passed.

The workflow in `.github/workflows/ci.yml` adds Linux/Windows and Python 3.10/3.12 jobs plus a figure build. A workflow definition is not a claim that every remote matrix job has already passed. Check the repository's Actions page for the current hosted result.

## Figure generation

The full build generated:

- Six architecture scenes in three themes: 18 SVG, 18 TikZ, 18 PNG, and 18 SVG-derived PDFs.
- Six additional PDFs compiled from the paper-theme TikZ sources.
- Three native mathematical/neuron diagrams, each compiled to PDF and rasterized to PNG.
- Eighteen geometry reports, all with zero warnings/errors under strict validation.

SVG masters preserve text and shapes. Every scene report records the JSON SHA-256. The native templates do not use JSON geometry linting; they are reviewed as compiled figures.

The local LuaLaTeX binary was present but its installation lacked required modules/packages. The compiler's fallback successfully used pdfLaTeX. Generated paper-theme figures and the native templates compiled successfully with shell escape disabled. That is evidence for the tested TeX path, not a guarantee about arbitrary fonts or TeX installations.

## Visual review

Reviewed the six paper-theme architecture compositions and native figures, including topology, labels, crop, arrows, residual origins, and distinctions between context, tool calls, and results. Reviewed rendered gallery images and the desktop/mobile gallery layout. The initial review prompted separate ports for overlapping agent-system paths and a mobile grid-width correction. Geometry reports are heuristic; the visual and semantic reviews are separate checks.

## Fresh agent tasks

Two agents received only the skill path and a concrete diagram request, without this implementation history. Each used the skill, created new artifacts, corrected a visual issue discovered during its own inspection, and returned source plus rendered output.

1. **Query-time RAG with citation revision.** User question -> query encoder -> hybrid retrieval; an existing document index supplies candidates; passages go through a reranker and generator; a citation checker returns an answer or requests revision. The agent produced eight components and eight relationships, zero strict lint issues, editable SVG/TikZ, PNG, SVG-derived PDF, and TeX-derived PDF. It inspected full/reduced renders and both PDF routes. The indexing pipeline remained outside scope.
2. **Single-head cross-attention.** Decoder states supply Q; encoder states supply K and V. The agent produced the requested scaled dot-product formula and appropriate sequence dimensions without adding a mask, residual, or output projection. It compiled the native TeX, checked the one-page vector PDF and log, and inspected full and 900 px renders. The reviewed source is included as the cross-attention template.

These are concrete transfer checks, not a blind statistical benchmark or a guarantee that all future diagrams will be correct. Architectural evidence and visual inspection remain necessary for every task.

## Browser and distribution

The static gallery was exercised with a headless Chromium browser across all six examples and three themes. Checks covered image loading, the four source/export links for each selection (72 link checks), zoom/reset, clipboard installation/prompt actions, and mobile page width. Browser results are recorded in `validation.json`. Screenshots were used for internal review and are not part of the skill.

All 11 reference repositories have pinned commits and explicit license observations. Original source code, templates, and figures are MIT; no upstream code/images are vendored. A credential-pattern scan of the publishable source was clean. New repositories are published under the account identities authenticated by the supplied tokens; credentials are not included in repository files.
