#!/usr/bin/env python3
"""Create exact raster contact sheets of the compiled diagrams (requires Pillow)."""
import io,json,math
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
def sheet(items,path,cols=3):
    tile_w,tile_h=720,450
    canvas=Image.new('RGB',(cols*tile_w,math.ceil(len(items)/cols)*tile_h),'#e7e7e7');d=ImageDraw.Draw(canvas)
    for i,item in enumerate(items):
        im=Image.open(ROOT/item['png']).convert('RGB');im.thumbnail((tile_w-24,tile_h-38),Image.Resampling.LANCZOS)
        x=(i%cols)*tile_w+(tile_w-im.width)//2;y=(i//cols)*tile_h+12
        canvas.paste(im,(x,y));d.text(((i%cols)*tile_w+12,(i//cols+1)*tile_h-21),item['id'],fill='#333333')
    payload=io.BytesIO();canvas.save(payload,format='PNG',optimize=True)
    with Image.open(io.BytesIO(payload.getvalue())) as check:check.load()
    path.write_bytes(payload.getvalue())
    with Image.open(path) as check:check.load()
def main():
    manifest=json.loads((ROOT/'gallery/atlas/manifest.json').read_text());items=manifest['examples']
    for family in manifest['families']:
        chosen=[x for x in items if x['family']==family];sheet(chosen,ROOT/'gallery/atlas'/('contact-'+family+'.png'))
    overview=[]
    for family in manifest['families']:
        chosen=[x for x in items if x['family']==family];overview.extend([chosen[0],chosen[len(chosen)//2]])
    sheet(overview,ROOT/'gallery/atlas/overview.png')
    print('Created six family contact sheets and a 12-figure overview.')
if __name__=='__main__':main()
