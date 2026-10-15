# Create your own architecture diagram

## Install for an agent

```bash
git clone https://github.com/Hisernberg/archdiagram-studio.git
cd archdiagram-studio
python scripts/install_skill.py --agent codex
```

The installer uses `$CODEX_HOME/skills` when configured, otherwise `~/.codex/skills`. Use `--agent claude` for `~/.claude/skills`, or `--dest /your/skills/directory` for another location. The installer will not overwrite a different existing skill unless you explicitly pass `--force`. Start a fresh agent session or refresh skill discovery if your host caches skills.

For another assistant, make `skills/draw-architecture/SKILL.md` available along with its scripts, assets, and reference directory. A standalone SKILL.md without those resources is incomplete. The workflow does not require any particular LLM provider or an API key. It improves instructions and tooling; it does not train or replace the agent's model.

## Search the 100 original TikZ figures

Use scripts/atlas.py find "cross attention" to locate a native master, or list --family vision for a family inventory. Copy a chosen ID with copy --id FIGURE_ID --out output/figure.tex. Compile the standalone file with pdfLaTeX and inspect the actual PDF/PNG. See [all 100 figures](ATLAS.md) and [native authoring](../skills/draw-architecture/references/atlas-authoring.md). The default style is black and white with spare gray fills. Atlas SVGs are outlined vector previews; native TikZ is their editable master.

## Ask your agent

> Use $draw-architecture to diagram the architecture in these source files. Target technical documentation, keep the text editable, label unknown tensor sizes symbolically, and provide SVG, JSON, TikZ, and a verified preview. Inspect the rendered figure before delivering it.

Good inputs include model code, configuration, a paper section, or a precise architecture brief. State the audience and target width if they matter. You can request Korean labels in SVG, but the host must have suitable fonts; native TeX requires additional CJK font configuration.

## Render directly

No Python package installation is needed for SVG/TikZ.

```bash
python skills/draw-architecture/scripts/archdiagram.py validate \
  skills/draw-architecture/assets/examples/agentic-research.json --strict
python skills/draw-architecture/scripts/archdiagram.py render \
  skills/draw-architecture/assets/examples/agentic-research.json \
  --out output/my-agent --formats svg,tex --theme paper --strict
```

Copy an example JSON and replace its architecture, not just its labels. Node positions are explicit and reproducible. The grid option is a quick starting layout; it is not automatic graph routing. Use side-relative port offsets and waypoints to separate calls, results, and feedback.

For PNG/PDF, install Inkscape and add `png,pdf` to `--formats`. Add `--compile-tex` to verify the generated TikZ using available TeX tools. The CLI tries LuaLaTeX then pdfLaTeX and records the successful engine. Compilation failures return a nonzero exit status.

## Revise carefully

A useful revision request names the intent: "separate tool calls from results", "show the second residual starting after the first add", "split the indexing and query paths", or "make this legible at a 9 cm paper column". Preserve the original source so future revisions are straightforward.

Read the [scene specification](../skills/draw-architecture/references/specification.md), [quality rubric](../skills/draw-architecture/references/quality.md), and [architecture recipes](../skills/draw-architecture/references/recipes.md). Keep an evidence note for figures based on code or papers. The bundled examples are explicitly illustrative.

## Rebuild the gallery

```bash
python -m unittest discover -s tests -v
python scripts/build_gallery.py --compile-tex
```

`--svg-only` builds source files without Inkscape, but the full hosted gallery needs the full build to provide PNG/PDF downloads. `--compile-tex` also builds the three additional mathematical/neuron templates. Run python scripts/build_atlas.py to build the 100-figure atlas; contact sheets additionally need Pillow. Optional legacy color themes require --all-themes; monochrome is the default. Open `index.html` directly or serve the repository locally with `python -m http.server 8000`. The viewer and prompt builder run locally in the browser; it does not send your architecture to an inference service.
