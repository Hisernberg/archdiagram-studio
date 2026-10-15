#!/usr/bin/env python3
"""Rebuild gallery from the installed-skill examples; fail on every lint warning."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/draw-architecture'

def load_renderer():
    s=importlib.util.spec_from_file_location('archdiagram',SKILL/'scripts/archdiagram.py')
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--compile-tex',action='store_true');p.add_argument('--svg-only',action='store_true');args=p.parse_args()
    ad=load_renderer();gallery=ROOT/'gallery';gallery.mkdir(exist_ok=True);items=[]
    for spec in sorted((SKILL/'assets/examples').glob('*.json')):
        raw=json.loads(spec.read_text());normalized=ad.normalize(raw);issues=ad.lint(normalized)
        if issues: raise RuntimeError(f'{spec.name}: {issues}')
        for theme in ad.THEMES:
            suffix='' if theme=='paper' else '.'+theme
            prefix=Path('gallery')/(spec.stem+suffix)
            command=[sys.executable,str(SKILL/'scripts/archdiagram.py'),'render',str(spec.relative_to(ROOT)),'--out',str(prefix),'--theme',theme,'--strict','--formats','svg,tex' if args.svg_only else 'svg,tex,png,pdf']
            if args.compile_tex and theme=='paper': command.append('--compile-tex')
            result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
            if result.returncode: raise RuntimeError(result.stderr+result.stdout)
        items.append(dict(id=spec.stem,title=raw['title'],description=raw['subtitle'],caption=raw['footer'],source=str(spec.relative_to(ROOT)),assumptions=raw.get('assumptions',[]),nodes=len(raw['nodes']),edges=len(raw['edges'])))
        print(f'Built {spec.stem}: 3 themes, {len(raw["nodes"])} nodes, {len(raw["edges"])} edges')
    natives=[]
    if args.compile_tex:
        for template in sorted((SKILL/'assets/templates').glob('*.tex')):
            target=gallery/(template.stem+'.pdf');ad.compile_tex(template,target)
            subprocess.run(['pdftocairo','-png','-singlefile','-scale-to','1800',str(target),str(gallery/template.stem)],check=True,capture_output=True)
            natives.append(dict(id=template.stem,source=str(template.relative_to(ROOT)),pdf=str(target.relative_to(ROOT)),png='gallery/'+template.stem+'.png'))
            print('Compiled native template:',template.name)
    manifest=dict(renderer_version=ad.VERSION,examples=items,native_templates=natives)
    (gallery/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    # Bundle JSON as an assignment so the static gallery works even when opened from disk.
    (ROOT/'app/gallery-data.js').write_text('window.ARCHDIAGRAM_GALLERY = '+json.dumps(manifest,ensure_ascii=False,indent=2)+';\n')

if __name__=='__main__': main()
