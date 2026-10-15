# Working in ArchDiagram Studio

For a diagram request, read `skills/draw-architecture/SKILL.md` and follow its evidence, rendering, and visual review workflow. Resolve its paths relative to the skill directory. Do not infer architecture components from a template alone.

For repository changes:

- Keep the portable skill self-contained under `skills/draw-architecture/`.
- Keep core SVG/TikZ generation dependency-free on Python 3.10+.
- Run `python -m unittest discover -s tests -v` after relevant code changes.
- Run `python scripts/build_gallery.py --compile-tex` after example, renderer, or native-template changes when Inkscape and TeX are available. Inspect actual outputs.
- Rebuild native atlas changes with python scripts/build_atlas.py; that builder synchronizes the atlas manifest and static app data. Run python scripts/build_contact_sheets.py after final native renders. Check compiled exports, rather than trusting an exit code alone.
- Record exact upstream origins and licenses if introducing third-party code. The source catalog currently represents reference-only use.
- Do not commit tokens, temporary credentials, personal paths, or generated TeX logs.
- Distinguish local checks, visual inspection, and hosted CI results in claims.
