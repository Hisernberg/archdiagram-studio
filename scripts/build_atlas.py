#!/usr/bin/env python3
"""Compile the original 100-figure monochrome TikZ atlas and refresh its gallery."""
from __future__ import annotations
import argparse,concurrent.futures,hashlib,html,json,re,shutil,struct,subprocess,tempfile,zlib
import xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/draw-architecture'
FAMILIES={'vision':20,'text':20,'audio':20,'multimodal':15,'agents':15,'robotics-graphs':10}

def check_exports(prefix,meta,digest):
    """Check actual payloads, including complete PNG chunks and SVG XML."""
    png=prefix.with_suffix('.png').read_bytes()
    if png[:8]!=b'\x89PNG\r\n\x1a\n':raise ValueError('Invalid PNG signature')
    pos=8;compressed=[];ended=False
    while pos<len(png):
        if pos+12>len(png):raise ValueError('Truncated PNG chunk')
        size=struct.unpack('>I',png[pos:pos+4])[0]
        end=pos+12+size
        if end>len(png):raise ValueError('Truncated PNG payload')
        kind=png[pos+4:pos+8];payload=png[pos+8:pos+8+size]
        crc=struct.unpack('>I',png[pos+8+size:end])[0]
        if zlib.crc32(kind+payload)&0xffffffff!=crc:raise ValueError('PNG CRC mismatch')
        if kind==b'IDAT':compressed.append(payload)
        pos=end
        if kind==b'IEND':ended=True;break
    if not ended or pos!=len(png):raise ValueError('Missing PNG end marker')
    decoder=zlib.decompressobj();decoder.decompress(b''.join(compressed))
    if not decoder.eof:raise ValueError('Incomplete PNG image stream')
    svg=ET.parse(prefix.with_suffix('.svg')).getroot()
    if svg.tag!='{http://www.w3.org/2000/svg}svg':raise ValueError('Invalid SVG root')
    if not prefix.with_suffix('.pdf').read_bytes().rstrip().endswith(b'%%EOF'):raise ValueError('Truncated PDF')
    if hashlib.sha256(prefix.with_suffix('.tex').read_bytes()).hexdigest()!=digest:raise ValueError('TikZ source mismatch')
    if json.loads(prefix.with_suffix('.json').read_text())!=meta:raise ValueError('Metadata mismatch')

def build(meta,force=False):
    source=SKILL/'assets/atlas'/meta['family']/meta['source_file']
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    folder=ROOT/'gallery/atlas';folder.mkdir(parents=True,exist_ok=True)
    prefix=folder/meta['id'];report_path=prefix.with_suffix('.report.json')
    outputs=[prefix.with_suffix('.'+s) for s in ('pdf','png','svg','tex','json')]
    if not force and report_path.exists() and all(p.exists() for p in outputs) and json.loads(report_path.read_text()).get('sha256')==digest:
        try:
            check_exports(prefix,meta,digest)
            return meta|{'cached':True}
        except (ValueError,OSError,ET.ParseError,zlib.error):
            pass  # A partial or stale export must be rebuilt rather than cached.
    with tempfile.TemporaryDirectory(prefix='atlas-build-') as tmp:
        work=Path(tmp);shutil.copy2(source,work/'figure.tex')
        run=subprocess.run(['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','figure.tex'],cwd=work,capture_output=True,text=True,timeout=90)
        log=(work/'figure.log').read_text(errors='replace') if (work/'figure.log').exists() else run.stdout
        if run.returncode:raise RuntimeError(meta['id']+'\n'+log[-3500:])
        warnings=[line for line in log.splitlines() if 'Overfull' in line or 'Missing character:' in line]
        if warnings:raise RuntimeError(meta['id']+': '+'; '.join(warnings))
        shutil.copy2(work/'figure.pdf',prefix.with_suffix('.pdf'))
    shutil.copy2(source,prefix.with_suffix('.tex'))
    subprocess.run(['pdftocairo','-png','-singlefile','-scale-to','1400',str(prefix.with_suffix('.pdf')),str(prefix)],check=True,capture_output=True,timeout=45)
    subprocess.run(['pdftocairo','-svg',str(prefix.with_suffix('.pdf')),str(prefix.with_suffix('.svg'))],check=True,capture_output=True,timeout=45)
    path=prefix.with_suffix('.svg');svg=path.read_text()
    accessible='<title>'+html.escape(meta['title'])+'</title><desc>'+html.escape(meta['description']+' '+meta.get('caption',''))+'</desc>'
    path.write_text(re.sub(r'(<svg\b[^>]*>)',lambda m:m.group(1)+accessible,svg,count=1))
    prefix.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n')
    check_exports(prefix,meta,digest)
    report={'id':meta['id'],'sha256':digest,'compiler':'pdflatex','shell_escape':False,'overfull_or_missing_glyphs':warnings,'source':'skills/draw-architecture/assets/atlas/'+meta['family']+'/'+meta['source_file'],'master':'TikZ','svg_text':'Glyph outlines from PDF; edit the TikZ master.','visual_review':'Family author review plus atlas contact-sheet review; see docs/VALIDATION.md.'}
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    return meta|{'cached':False}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--force',action='store_true');p.add_argument('--jobs',type=int,default=4);p.add_argument('--family',choices=list(FAMILIES));args=p.parse_args()
    items=[]
    for family,count in FAMILIES.items():
        if args.family and args.family!=family:continue
        rows=json.loads((SKILL/'assets/atlas'/family/'index.json').read_text())
        if len(rows)!=count:raise RuntimeError(f'{family}: require {count}, found {len(rows)}')
        for item in rows:
            if item['family']!=family or not re.fullmatch(r'[a-z0-9][a-z0-9_-]+',item['id']):raise RuntimeError('Invalid identity')
            if Path(item['source_file']).name!=item['source_file'] or not item['source_file'].endswith('.tex'):raise RuntimeError('Invalid source path')
            if not item.get('sources'):raise RuntimeError('Missing sources: '+item['id'])
        items.extend(rows)
    if len({i['id'] for i in items})!=len(items):raise RuntimeError('Duplicate IDs')
    errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures={pool.submit(build,i,args.force):i for i in items}
        for future in concurrent.futures.as_completed(futures):
            item=futures[future]
            try:
                result=future.result();print(('Cached ' if result['cached'] else 'Built ')+item['id'],flush=True)
            except Exception as e:errors.append(str(e));print('FAILED '+str(e),flush=True)
    if errors:raise RuntimeError('\n\n'.join(errors))
    if args.family:return
    examples=[]
    for item in items:
        prefix='gallery/atlas/'+item['id']
        examples.append(item|{'mode':'native-tikz','source':prefix+'.json','svg':prefix+'.svg','png':prefix+'.png','pdf':prefix+'.pdf','tex':prefix+'.tex'})
    manifest={'renderer_version':'2.0.0','theme':'monochrome','families':FAMILIES,'examples':examples}
    (ROOT/'gallery/atlas/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (ROOT/'app/gallery-data.js').write_text('window.ARCHDIAGRAM_GALLERY = '+json.dumps(manifest,ensure_ascii=False,indent=2)+';\n')
    lines=['# Architecture atlas: 100 original TikZ figures','','All diagrams use monochrome LaTeX typography. Edit the native TikZ master; SVG previews use outlined glyphs.','','| # | Family | Figure | Files |','|---|---|---|---|']
    for i,item in enumerate(examples,1):
        b='../gallery/atlas/'+item['id'];src='../skills/draw-architecture/assets/atlas/'+item['family']+'/'+item['source_file']
        lines.append(f"| {i:03} | {item['family']} | {item['title']} | [TikZ]({src}) · [PDF]({b}.pdf) · [SVG]({b}.svg) · [PNG]({b}.png) |")
    (ROOT/'docs/ATLAS.md').write_text('\n'.join(lines)+'\n')
    print('Atlas complete:',len(examples),'figures')
if __name__=='__main__':main()
