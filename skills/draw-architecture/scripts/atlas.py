#!/usr/bin/env python3
"""Find and copy an original monochrome TikZ template."""
import argparse,json,re,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def catalog():
    result=[]
    for p in sorted((ROOT/'assets/atlas').glob('*/index.json')):
        for row in json.loads(p.read_text(encoding='utf-8')):
            name=row['source_file']
            if Path(name).name!=name or not name.endswith('.tex'):raise ValueError('Invalid filename')
            result.append(row|{'path':str(p.parent/name)})
    return result
def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    for name in ['list','find']:
        s=sub.add_parser(name);s.add_argument('--family');s.add_argument('--json',action='store_true')
        if name=='find':s.add_argument('query');s.add_argument('--limit',type=int,default=6)
    s=sub.add_parser('copy');s.add_argument('--id',required=True);s.add_argument('--out',required=True,type=Path);s.add_argument('--force',action='store_true')
    args=p.parse_args();rows=catalog()
    if args.command=='copy':
        matches=[r for r in rows if r['id']==args.id]
        if not matches:p.error('Unknown figure ID; use list or find')
        if args.out.suffix!='.tex':p.error('--out must end in .tex')
        if args.out.exists() and not args.force:p.error('Output exists; choose another path or use --force')
        args.out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(matches[0]['path'],args.out)
        print('Copied native TikZ:',args.out);return 0
    rows=[r for r in rows if not args.family or r['family']==args.family]
    if args.command=='find':
        terms=re.findall(r'[a-z0-9]+',args.query.lower())
        def score(r):
            title=' '.join(re.findall(r'[a-z0-9]+',(r['title']+' '+r['id']).lower()))
            detail=' '.join(re.findall(r'[a-z0-9]+',(r['description']+' '+' '.join(r.get('tags',[]))).lower()))
            return sum(3*(t in title)+(t in detail) for t in terms)
        rows=sorted((r for r in rows if score(r)>0),key=score,reverse=True)[:max(1,min(args.limit,100))]
    if args.json:print(json.dumps(rows,indent=2))
    else:
        for r in rows:print(f"{r['id']}\t{r['family']}\t{r['title']}")
    return 0 if rows else 1
if __name__=='__main__':sys.exit(main())
