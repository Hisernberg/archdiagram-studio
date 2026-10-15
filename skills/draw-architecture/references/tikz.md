# TikZ and export

The renderer writes standalone TikZ with absolute point coordinates. Text from JSON is escaped as literal text; dollar signs do not activate math mode. Use the native templates for equations. Both routes preserve editable source.

## Compile generated figures

```bash
python scripts/archdiagram.py render diagram.json --out output/diagram \
  --formats svg,tex,png,pdf --compile-tex --strict
```

SVG and TeX source require only Python 3.10+. PNG/PDF conversion requires Inkscape. TikZ verification requires LuaLaTeX or pdfLaTeX plus PGF/TikZ, standalone, iftex, amsmath, and fonts. Ubuntu packages typically include `inkscape texlive-latex-extra texlive-luatex texlive-fonts-recommended`. Install packages using the environment's authorized package manager.

The CLI tries LuaLaTeX with DejaVu Sans, then falls back to pdfLaTeX with Latin Modern if that installation fails. The report records the successful engine. The `.pdf` export comes from SVG; `.tikz.pdf` comes from TeX. Small differences in font metrics and storage-shape drawing can occur. Inspect both before choosing a publication master. The SVG text is editable; PDF converters may outline text. Keep SVG/JSON or native TeX alongside any PDF.

## Native templates

Compile `assets/templates/transformer-attention.tex` `assets/templates/cross-attention.tex`, and `assets/templates/mlp.tex` with `pdflatex -no-shell-escape -halt-on-error FILE.tex`. Copy a template to the task output directory first. Keep node names stable while editing labels and equations. Use anchor-based paths and named styles for maintainable diagrams.

For Overleaf, upload the standalone source and select a matching compiler. Include a rendered PDF into a paper using `\includegraphics[width=\columnwidth]{figure.pdf}`; recheck final text size. Standalone SVG/TikZ figures can be very wide; reduce conceptual density instead of merely scaling them down.

## Fonts and languages

SVG can contain Unicode, but the viewer/exporter must have the required fonts. The generated LuaLaTeX template uses DejaVu Sans, which does not cover all scripts. Korean/Chinese/Japanese require an appropriate installed font and a native TeX setup such as `ctex` or LuaTeX-ja with suitable fonts. Do not claim universal Unicode support. Keep Latin-only labels or customize the native template when these fonts are unavailable.

## Compilation boundary

The renderer escapes JSON text. Its compiler runs the generated trusted TeX in a temporary working directory with shell escape disabled and a timeout. This is not a sandbox for arbitrary external TeX: TeX can still read files allowed by its environment. Inspect external `.tex` before compiling and use a restricted environment for untrusted sources. Never put credentials in a TeX source or a spec.
