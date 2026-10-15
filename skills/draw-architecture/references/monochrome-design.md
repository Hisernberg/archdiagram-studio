# Monochrome technical figures

Use black rules, white backgrounds, sparse neutral gray fills, and real LaTeX type. Avoid gradients, shadows, decorative icons, oversized rounded cards, and color-dependent meaning. Convey structure through placement, line style, braces, repeated-block boundaries, and annotations.

For neural architecture towers, show the main stream consistently bottom-to-top or top-to-bottom. Place residual lanes outside the stack, starting at the correct stream. Use a repeat brace instead of drawing dozens of identical layers. Place a detail inset beside a module and connect it with a leader, not a data-flow arrow. Keep exact model counts and dimensions separate from generic concepts unless configuration or paper verifies them.

Use small multiples to compare mechanisms. Use grids for patches and attention positions, time axes for audio/video/recurrent systems, neurons for dense connectivity, and tensors for spatial maps. Do not turn every architecture into the same sequence of boxes.

Sebastian Raschka's public architecture figures were studied for hierarchy, residual clarity, focused detail insets, and explanatory callouts. Original images are credited and linked in the study reference; they are not redistributed here. The book repository's software license explicitly excludes related book images. This skill uses original diagrams and does not imply affiliation.

The 100-figure atlas contains conceptual schematics, not guaranteed exact checkpoint implementations. Read each figure's sources and assumptions. Search with scripts/atlas.py find "cross attention"; copy the nearest native .tex, change the architecture from evidence, compile it, and inspect the result. Its generated SVG preview has outlined glyphs; edit the native TikZ source. The separate JSON renderer preserves SVG text.
