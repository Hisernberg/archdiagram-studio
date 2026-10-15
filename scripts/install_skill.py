#!/usr/bin/env python3
"""Install this repository's skill without downloading or executing upstream code."""
import argparse
import hashlib
import os
from pathlib import Path
import shutil
import sys

def fingerprint(path):
    return {str(p.relative_to(path)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in path.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--agent',choices=['codex','claude'],default='codex')
    p.add_argument('--dest',type=Path,help='Parent skills directory; skill name is appended')
    p.add_argument('--force',action='store_true',help='Replace an existing different skill directory')
    args=p.parse_args(argv)
    source=Path(__file__).resolve().parents[1]/'skills/draw-architecture'
    base=args.dest or (Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'skills' if args.agent=='codex' else Path.home()/'.claude/skills')
    destination=base.expanduser().resolve()/'draw-architecture'
    if destination==source.resolve(): print(f'Already installed: {destination}');return 0
    if not (source/'SKILL.md').is_file(): p.error('Source SKILL.md is missing')
    if destination.exists():
        if destination.is_dir() and fingerprint(destination)==fingerprint(source): print(f'Already up to date: {destination}');return 0
        if not args.force: p.error(f'{destination} already exists with different contents; choose --dest or explicitly use --force')
        if destination.is_symlink() or not destination.is_dir(): p.error('Refusing to replace a symlink or non-directory')
        shutil.rmtree(destination)
    shutil.copytree(source,destination,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    print(f'Installed: {destination}\nInvoke: $draw-architecture')
    return 0

if __name__=='__main__': sys.exit(main())
