#!/usr/bin/env python3
"""ArchDiagram Studio: deterministic JSON to editable SVG and TikZ. Python 3.10+."""
from __future__ import annotations
import argparse
import copy
import hashlib
import html
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap

VERSION = '1.0.0'
ROLES = {
    'input': ('#2563EB', '#EFF6FF'), 'compute': ('#0F766E', '#F0FDFA'),
    'model': ('#6D28D9', '#F5F3FF'), 'memory': ('#0369A1', '#F0F9FF'),
    'tool': ('#B45309', '#FFFBEB'), 'control': ('#475569', '#F1F5F9'),
    'output': ('#047857', '#ECFDF5'), 'neutral': ('#475569', '#F8FAFC'),
}
THEMES = {
    'paper': dict(bg='#FFFFFF', fg='#14263D', muted='#52627A', line='#52627A', group='#F8FAFC', border='#CBD5E1'),
    'midnight': dict(bg='#101827', fg='#F1F5F9', muted='#B5C4D9', line='#A9BDD8', group='#172236', border='#435470'),
    'blueprint': dict(bg='#F1F7FC', fg='#123452', muted='#45647D', line='#45647D', group='#E7F0F8', border='#A4BDD1'),
}
KINDS = {'block', 'tensor', 'store', 'junction', 'decision'}
SIDES = {'left', 'right', 'top', 'bottom'}
TOP_FIELDS = {'version','title','subtitle','width','height','nodes','edges','groups','footer','evidence','assumptions'}
NODE_FIELDS = {'id','label','detail','role','kind','x','y','col','row','width','height','tag'}
EDGE_FIELDS = {'from','to','label','kind','from_side','to_side','from_offset','to_offset','via','label_at','label_pos'}
GROUP_FIELDS = {'id','label','members','x','y','width','height'}
ID_RE = re.compile(r'^[A-Za-z][A-Za-z0-9_-]{0,79}$')

class SpecError(ValueError):
    """A specification cannot be interpreted without changing its meaning."""

def number(v, where, lo=None, hi=None):
    if isinstance(v, bool) or not isinstance(v, (int,float)) or not math.isfinite(v):
        raise SpecError(f'{where}: expected a finite number')
    if lo is not None and v < lo or hi is not None and v > hi:
        raise SpecError(f'{where}: expected a value between {lo} and {hi}')
    return float(v)

def string(v, where, limit=1000):
    if not isinstance(v,str) or len(v)>limit or any(ord(c)<32 and c!='\n' for c in v):
        raise SpecError(f'{where}: expected plain text of at most {limit} characters')
    return v

def fields(obj, allowed, where):
    if not isinstance(obj,dict): raise SpecError(f'{where}: expected an object')
    if set(obj)-allowed: raise SpecError(f'{where}: unknown fields {sorted(set(obj)-allowed)}')

def point(v, where):
    if not isinstance(v,list) or len(v)!=2: raise SpecError(f'{where}: expected [x, y]')
    return [number(x,where,-20000,20000) for x in v]

def normalize(raw):
    fields(raw,TOP_FIELDS,'diagram')
    s=copy.deepcopy(raw)
    if type(s.get('version')) is not int or s['version']!=1: raise SpecError('version: expected integer 1')
    s['title']=string(s.get('title','Architecture'),'title',160)
    for key in ('subtitle','footer'): s[key]=string(s.get(key,''),key,300)
    for key in ('evidence','assumptions'):
        if not isinstance(s.get(key,[]),list): raise SpecError(f'{key}: expected an array of plain-text strings')
        s[key]=[string(v,key,1500) for v in s.get(key,[])]
    nodes=s.get('nodes')
    if not isinstance(nodes,list) or not 1<=len(nodes)<=200: raise SpecError('nodes: expected 1 to 200 objects')
    ids=set()
    for i,n in enumerate(nodes):
        where=f'nodes[{i}]';fields(n,NODE_FIELDS,where)
        if not isinstance(n.get('id'),str) or not ID_RE.fullmatch(n['id']) or n['id'] in ids:
            raise SpecError(f'{where}.id: require a unique identifier beginning with a letter')
        ids.add(n['id'])
        for key,default,limit in [('label',n['id'],300),('detail','',500),('tag','',45)]:
            n[key]=string(n.get(key,default),where+'.'+key,limit)
        n.setdefault('role','compute');n.setdefault('kind','block')
        if not isinstance(n['role'],str) or n['role'] not in ROLES or not isinstance(n['kind'],str) or n['kind'] not in KINDS:
            raise SpecError(f'{where}: unsupported role or kind')
        if ('x' in n)!=('y' in n): raise SpecError(f'{where}: supply both x and y')
        if ('col' in n)!=('row' in n): raise SpecError(f'{where}: supply both col and row')
        if 'x' in n and 'col' in n: raise SpecError(f'{where}: choose x/y or col/row')
        col=number(n.get('col',i),where+'.col',0,100);row=number(n.get('row',0),where+'.row',0,100)
        n['x']=number(n.get('x',60+260*col),where+'.x',0,20000)
        n['y']=number(n.get('y',150+160*row),where+'.y',0,20000)
        junction=n['kind']=='junction'
        n['width']=number(n.get('width',48 if junction else 190),where+'.width',24,2000)
        n['height']=number(n.get('height',48 if junction else 84),where+'.height',24,2000)
        n.pop('col',None);n.pop('row',None)
    s.setdefault('edges',[])
    if not isinstance(s['edges'],list) or len(s['edges'])>1000: raise SpecError('edges: expected at most 1000 objects')
    for i,e in enumerate(s['edges']):
        where=f'edges[{i}]';fields(e,EDGE_FIELDS,where)
        if any(not isinstance(e.get(key),str) or e[key] not in ids for key in ('from','to')):
            raise SpecError(f'{where}: from/to must reference existing node IDs')
        if e['from']==e['to'] and not e.get('via'): raise SpecError(f'{where}: self-loop requires via waypoints')
        e['label']=string(e.get('label',''),where+'.label',160);e.setdefault('kind','data')
        if not isinstance(e['kind'],str) or e['kind'] not in {'data','control','feedback'}: raise SpecError(f'{where}.kind: use data, control, or feedback')
        for side in ('from_side','to_side'):
            if side in e and (not isinstance(e[side],str) or e[side] not in SIDES): raise SpecError(f'{where}.{side}: unsupported port')
        for key in ('from_offset','to_offset'):
            e[key]=number(e.get(key,0),where+'.'+key,-0.45,0.45)
        if not isinstance(e.get('via',[]),list) or len(e.get('via',[]))>100: raise SpecError(f'{where}.via: expected at most 100 points')
        e['via']=[point(p,where+'.via') for p in e.get('via',[])]
        if 'label_at' in e: e['label_at']=point(e['label_at'],where+'.label_at')
        e['label_pos']=number(e.get('label_pos',0.5),where+'.label_pos',0,1)
    s.setdefault('groups',[])
    if not isinstance(s['groups'],list) or len(s['groups'])>100: raise SpecError('groups: expected at most 100 objects')
    by_id={n['id']:n for n in nodes};group_ids=set()
    for i,g in enumerate(s['groups']):
        where=f'groups[{i}]';fields(g,GROUP_FIELDS,where)
        if not isinstance(g.get('id'),str) or not ID_RE.fullmatch(g['id']) or g['id'] in group_ids: raise SpecError(f'{where}.id: expected a unique group identifier')
        group_ids.add(g['id']);g['label']=string(g.get('label',g['id']),where+'.label',120)
        members=g.get('members',[])
        if not isinstance(members,list) or any(not isinstance(x,str) or x not in ids for x in members): raise SpecError(f'{where}.members: require existing node IDs')
        g['members']=members;box_keys={'x','y','width','height'}
        if box_keys & set(g) and not box_keys<=set(g): raise SpecError(f'{where}: supply all x,y,width,height or none')
        if not box_keys<=set(g):
            if not members: raise SpecError(f'{where}: require members or an explicit box')
            chosen=[by_id[x] for x in members]
            g['x']=min(n['x'] for n in chosen)-24;g['y']=min(n['y'] for n in chosen)-44
            g['width']=max(n['x']+n['width'] for n in chosen)-g['x']+24
            g['height']=max(n['y']+n['height'] for n in chosen)-g['y']+24
        for key in box_keys: g[key]=number(g[key],where+'.'+key,0 if key in {'x','y'} else 1,20000)
    extents=nodes+s['groups']
    s['width']=number(s.get('width',max(560,max(n['x']+n['width'] for n in extents)+60)),'width',520,20000)
    s['height']=number(s.get('height',max(n['y']+n['height'] for n in extents)+100),'height',180,20000)
    return s

def color(role,theme):
    stroke,fill=ROLES[role]
    if theme=='midnight':
        stroke=dict(input='#93C5FD',compute='#5EEAD4',model='#C4B5FD',memory='#7DD3FC',tool='#FCD34D',control='#CBD5E1',output='#6EE7B7',neutral='#CBD5E1')[role]
        fill='#202E44'
    return stroke,fill

def bbox(n): return tuple(n[k] for k in ('x','y','width','height'))
def port(n,side,offset=0):
    x,y,w,h=bbox(n)
    return dict(left=(x,y+h/2+offset*h),right=(x+w,y+h/2+offset*h),top=(x+w/2+offset*w,y),bottom=(x+w/2+offset*w,y+h))[side]

def route(e,nodes):
    a,b=nodes[e['from']],nodes[e['to']]
    dx=b['x']+b['width']/2-a['x']-a['width']/2;dy=b['y']+b['height']/2-a['y']-a['height']/2
    horizontal=abs(dx)>=abs(dy)
    source=e.get('from_side',('right' if dx>=0 else 'left') if horizontal else ('bottom' if dy>=0 else 'top'))
    dest=e.get('to_side',('left' if dx>=0 else 'right') if horizontal else ('top' if dy>=0 else 'bottom'))
    start,end=port(a,source,e['from_offset']),port(b,dest,e['to_offset'])
    if e['via']: result=[start,*e['via'],end]
    elif source in {'left','right'} and dest in {'left','right'}:
        mid=(start[0]+end[0])/2;result=[start,(mid,start[1]),(mid,end[1]),end]
    elif source in {'top','bottom'} and dest in {'top','bottom'}:
        mid=(start[1]+end[1])/2;result=[start,(start[0],mid),(end[0],mid),end]
    else: result=[start,(end[0],start[1]) if source in {'left','right'} else (start[0],end[1]),end]
    cleaned=[]
    for p in result:
        if not cleaned or tuple(p)!=cleaned[-1]: cleaned.append(tuple(p))
    return cleaned

def label_point(e,path):
    if 'label_at' in e: return e['label_at']
    lengths=[math.dist(a,b) for a,b in zip(path,path[1:])];remaining=sum(lengths)*e['label_pos']
    for i,length in enumerate(lengths):
        if remaining<=length and length:
            a,b=path[i:i+2];q=remaining/length
            return a[0]+q*(b[0]-a[0]),a[1]+q*(b[1]-a[1])-11
        remaining-=length
    return path[-1]

def wrap(text,width,size):
    lines=[]
    for line in text.split('\n'):
        lines.extend(textwrap.wrap(line,width=max(1,int(width/(size*0.56))),break_long_words=True,break_on_hyphens=False) or [''])
    return lines

def node_lines(n):
    if n['kind']=='junction': return [n['label']],[]
    inset=42 if n['kind']=='decision' else 28
    return wrap(n['label'],n['width']-inset,15),wrap(n['detail'],n['width']-inset,11.5) if n['detail'] else []

def overlap(a,b,padding=0):
    return a[0]<b[0]+b[2]+padding and a[0]+a[2]+padding>b[0] and a[1]<b[1]+b[3]+padding and a[1]+a[3]+padding>b[1]

def segment_in_box(a,b,n):
    x,y,w,h=bbox(n);x,y,w,h=x+2,y+2,w-4,h-4;dx,dy=b[0]-a[0],b[1]-a[1];lo,hi=0.,1.
    for p,q in ((-dx,a[0]-x),(dx,x+w-a[0]),(-dy,a[1]-y),(dy,y+h-a[1])):
        if p==0:
            if q<0: return False
        elif p<0: lo=max(lo,q/p)
        else: hi=min(hi,q/p)
    return lo<=hi

def lint(s):
    issues=[]
    def add(code,msg,severity='warning'): issues.append(dict(severity=severity,code=code,message=msg))
    nodes=s['nodes'];by_id={n['id']:n for n in nodes}
    for n in nodes:
        x,y,w,h=bbox(n)
        if x+w+12>s['width'] or y+h+12>s['height']: add('canvas-overflow',f"{n['id']}: exceeds canvas padding",'error')
        if y<118: add('header-overlap',f"{n['id']}: enters title/subtitle/legend area")
        label,detail=node_lines(n);used=len(label)*18+len(detail)*15+(18 if detail else 0)+(18 if n['tag'] else 0)
        if used>h-16: add('text-fit',f"{n['id']}: increase height or shorten text")
    for i,a in enumerate(nodes):
        for b in nodes[i+1:]:
            if overlap(bbox(a),bbox(b)): add('node-overlap',f"{a['id']} overlaps {b['id']}",'error')
    for g in s['groups']:
        if g['x']+g['width']>s['width'] or g['y']+g['height']>s['height']: add('group-overflow',f"{g['id']}: exceeds canvas",'error')
        if g['y']<118: add('group-header-overlap',f"{g['id']}: enters title area")
        for ident in g['members']:
            n=by_id[ident]
            if n['x']<g['x'] or n['y']<g['y']+30 or n['x']+n['width']>g['x']+g['width'] or n['y']+n['height']>g['y']+g['height']:
                add('group-fit',f"{g['id']}: {ident} outside group or its title padding",'error')
    label_boxes=[]
    for i,e in enumerate(s['edges']):
        path=route(e,by_id)
        if len(path)<2: add('zero-edge',f'edge {i}: no visible route','error');continue
        if any(x<8 or x>s['width']-8 or y<118 or y>s['height']-36 for x,y in path): add('edge-overflow',f'edge {i}: enters canvas margin/header')
        for n in nodes:
            if n['id'] not in {e['from'],e['to']} and any(segment_in_box(a,b,n) for a,b in zip(path,path[1:])):
                add('edge-through-node',f"edge {i} ({e['from']} -> {e['to']}) crosses {n['id']}")
        if e['label']:
            x,y=label_point(e,path);width=len(e['label'])*6.3+16;box=(x-width/2,y-10,width,20);label_boxes.append((i,box))
            if box[0]<0 or box[1]<0 or box[0]+box[2]>s['width'] or box[1]+box[3]>s['height']: add('label-overflow',f'edge {i}: label exceeds canvas','error')
            for n in nodes:
                if overlap(box,bbox(n)): add('edge-label-overlap',f"edge {i}: label overlaps {n['id']}; set label_at")
    for i,(a,box) in enumerate(label_boxes):
        for b,other in label_boxes[i+1:]:
            if overlap(box,other): add('label-label-overlap',f'edge labels {a} and {b} overlap')
    for key,size in (('title',29),('subtitle',13),('footer',11)):
        if len(s[key])*size*0.54>s['width']-96: add('caption-fit',f'{key}: shorten text or increase canvas width')
    return issues

def f(v): return f'{v:.3f}'.rstrip('0').rstrip('.') if v else '0'
def xml(v): return html.escape(str(v),quote=True)

def render_svg(spec,theme='paper'):
    s=normalize(spec)
    if theme not in THEMES: raise SpecError(f'unknown theme: {theme}')
    t=THEMES[theme];w,h=s['width'],s['height']
    description=s['subtitle']+'. '+'; '.join(f"{n['id']}: {n['label']} {n['detail']}" for n in s['nodes'])+'. '+'; '.join(f"{e['from']} to {e['to']}: {e['label']} ({e['kind']})" for e in s['edges'])
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{f(w)}" height="{f(h)}" viewBox="0 0 {f(w)} {f(h)}" role="img" aria-labelledby="diagram-title diagram-description">',f'<title id="diagram-title">{xml(s["title"])}</title>',f'<desc id="diagram-description">{xml(description)}</desc>',f'<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 1 1 L 9 5 L 1 9" fill="none" stroke="{t["line"]}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>',f'<rect width="100%" height="100%" fill="{t["bg"]}"/>','<g font-family="Inter, DejaVu Sans, Arial, sans-serif">']
    def text(x,y,content,size=13,fill=None,weight=400,anchor='start'):
        out.append(f'<text x="{f(x)}" y="{f(y)}" fill="{fill or t["fg"]}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{xml(content)}</text>')
    text(48,50,s['title'],29,weight=700);text(48,77,s['subtitle'],13,t['muted'])
    for x,label,dash in ((48,'Data flow',''),(188,'Control','7 5'),(316,'Feedback','2 5')):
        out.append(f'<path d="M {x} 104 h 28" stroke="{t["line"]}" stroke-width="1.7" fill="none" stroke-dasharray="{dash}"/>');text(x+36,108,label,10.5,t['muted'])
    for g in s['groups']:
        x,y,gw,gh=bbox(g);out.append(f'<g data-group="{xml(g["id"])}"><rect x="{f(x)}" y="{f(y)}" width="{f(gw)}" height="{f(gh)}" rx="14" fill="{t["group"]}" stroke="{t["border"]}" stroke-dasharray="5 5"/>');text(x+18,y+25,g['label'],11,t['muted'],600);out.append('</g>')
    nodes={n['id']:n for n in s['nodes']}
    for e in s['edges']:
        d='M '+' L '.join(f'{f(x)} {f(y)}' for x,y in route(e,nodes));dash={'data':'','control':'7 5','feedback':'2 5'}[e['kind']]
        out.append(f'<path d="{d}" stroke="{t["line"]}" stroke-width="1.8" fill="none" stroke-dasharray="{dash}" stroke-linejoin="round" stroke-linecap="round" marker-end="url(#arrow)"/>')
    for n in s['nodes']:
        x,y,nw,nh=bbox(n);stroke,fill=color(n['role'],theme)
        out.append(f'<g id="node-{xml(n["id"])}" data-role="{n["role"]}"><title>{xml(n["label"]+": "+n["detail"])}</title>')
        if n['kind']=='junction': out.append(f'<ellipse cx="{f(x+nw/2)}" cy="{f(y+nh/2)}" rx="{f(nw/2)}" ry="{f(nh/2)}" fill="{fill}" stroke="{stroke}" stroke-width="1.7"/>')
        elif n['kind']=='decision': out.append(f'<path d="M {f(x+nw/2)} {f(y)} L {f(x+nw)} {f(y+nh/2)} L {f(x+nw/2)} {f(y+nh)} L {f(x)} {f(y+nh/2)} Z" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
        elif n['kind']=='tensor':
            d=min(12,nw/6,nh/6)
            out.append(f'<path d="M {f(x)} {f(y+d)} L {f(x+d)} {f(y)} H {f(x+nw)} V {f(y+nh-d)} L {f(x+nw-d)} {f(y+nh)} H {f(x)} Z" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
            out.append(f'<path d="M {f(x)} {f(y+d)} H {f(x+nw-d)} V {f(y+nh)} M {f(x+nw-d)} {f(y+d)} L {f(x+nw)} {f(y)}" fill="none" stroke="{stroke}" stroke-width="1.2"/>')
        elif n['kind']=='store':
            out.append(f'<path d="M {f(x)} {f(y+10)} A {f(nw/2)} 10 0 0 1 {f(x+nw)} {f(y+10)} V {f(y+nh-10)} A {f(nw/2)} 10 0 0 1 {f(x)} {f(y+nh-10)} Z" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
            out.append(f'<ellipse cx="{f(x+nw/2)}" cy="{f(y+10)}" rx="{f(nw/2)}" ry="10" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>')
        else:
            out.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(nw)}" height="{f(nh)}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
            out.append(f'<path d="M {f(x+12)} {f(y+14)} v {f(max(10,nh-28))}" stroke="{stroke}" stroke-width="3" stroke-linecap="round"/>')
        labels,details=node_lines(n);total=len(labels)*18+(8+len(details)*15 if details else 0)+(18 if n['tag'] else 0);baseline=y+(nh-total)/2+14
        if n['tag']: text(x+nw/2,baseline,n['tag'].upper(),8.5,stroke,600,'middle');baseline+=18
        for line in labels: text(x+nw/2,baseline,line,15,weight=600,anchor='middle');baseline+=18
        if details: baseline+=6
        for line in details: text(x+nw/2,baseline,line,11.5,t['muted'],anchor='middle');baseline+=15
        out.append('</g>')
    for e in s['edges']:
        if not e['label']: continue
        x,y=label_point(e,route(e,nodes));lw=len(e['label'])*6.3+16
        out.append(f'<rect x="{f(x-lw/2)}" y="{f(y-10)}" width="{f(lw)}" height="20" rx="5" fill="{t["bg"]}"/>');text(x,y+4,e['label'],11,t['muted'],500,'middle')
    text(48,h-22,s['footer'],11,t['muted']);out.append('</g></svg>')
    return '\n'.join(out)+'\n'

def tex_escape(v):
    mapping={'\\':r'\textbackslash{}','{':r'\{','}':r'\}','#':r'\#','$':r'\$','%':r'\%','&':r'\&','_':r'\_','~':r'\textasciitilde{}','^':r'\textasciicircum{}','\n':' '}
    return ''.join(mapping.get(c,c) for c in str(v))

def render_tikz(spec,theme='paper'):
    s=normalize(spec)
    if theme not in THEMES: raise SpecError(f'unknown theme: {theme}')
    t=THEMES[theme]
    out=[r'\documentclass[tikz,border=0pt]{standalone}',r'\usepackage{iftex}',r'\ifLuaTeX',r'\usepackage{fontspec}',r'\setsansfont{DejaVu Sans}',r'\else',r'\usepackage[T1]{fontenc}',r'\usepackage[utf8]{inputenc}',r'\usepackage{lmodern}',r'\fi',r'\usepackage{amsmath}',r'\usetikzlibrary{arrows.meta}',r'\renewcommand{\familydefault}{\sfdefault}']
    for key,value in t.items(): out.append(r'\definecolor{ad'+key+r'}{HTML}{'+value[1:]+'}')
    for role in ROLES:
        stroke,fill=color(role,theme);out.extend([r'\definecolor{ad'+role+r'}{HTML}{'+stroke[1:]+'}',r'\definecolor{ad'+role+r'fill}{HTML}{'+fill[1:]+'}'])
    out.extend([r'\begin{document}',r'\begin{tikzpicture}[x=1pt,y=-1pt,inner sep=0pt,outer sep=0pt]',f"\\path[use as bounding box] (0,0) rectangle ({f(s['width'])},{f(s['height'])});",f"\\fill[adbg] (0,0) rectangle ({f(s['width'])},{f(s['height'])});"])
    def text(x,y,value,size=13,clr='adfg',weight=False,anchor='base west'):
        font=r'\sffamily\fontsize{'+str(size)+'}{'+str(size*1.2)+r'}\selectfont'+(r'\bfseries' if weight else '')
        out.append(f'\\node[anchor={anchor},text={clr},font={{{font}}}] at ({f(x)},{f(y)}) {{{tex_escape(value)}}};')
    text(48,50,s['title'],29,weight=True);text(48,77,s['subtitle'],13,'admuted')
    for x,label,style in ((48,'Data flow',''),(188,'Control',',dashed'),(316,'Feedback',',dotted')):
        out.append(f'\\draw[adline,line width=1.4pt{style}] ({x},104) -- ({x+28},104);');text(x+36,108,label,10.5,'admuted')
    for g in s['groups']:
        x,y,w,h=bbox(g);out.append(f'\\draw[fill=adgroup,draw=adborder,dashed,rounded corners=10pt] ({f(x)},{f(y)}) rectangle ({f(x+w)},{f(y+h)});');text(x+18,y+25,g['label'],11,'admuted',True)
    nodes={n['id']:n for n in s['nodes']}
    for e in s['edges']:
        style={'data':'','control':',dashed','feedback':',dotted'}[e['kind']];coords=' -- '.join(f'({f(x)},{f(y)})' for x,y in route(e,nodes))
        out.append(f'\\draw[adline,line width=1.3pt,-{{Latex[length=5pt,width=4pt]}},line join=round{style}] {coords};')
    for n in s['nodes']:
        x,y,w,h=bbox(n);role=n['role'];style=f'draw=ad{role},fill=ad{role}fill,line width=1.2pt'
        if n['kind']=='junction': out.append(f'\\draw[{style}] ({f(x+w/2)},{f(y+h/2)}) ellipse [x radius={f(w/2)}pt,y radius={f(h/2)}pt];')
        elif n['kind']=='decision': out.append(f'\\draw[{style}] ({f(x+w/2)},{f(y)}) -- ({f(x+w)},{f(y+h/2)}) -- ({f(x+w/2)},{f(y+h)}) -- ({f(x)},{f(y+h/2)}) -- cycle;')
        elif n['kind']=='tensor':
            d=min(12,w/6,h/6)
            out.append(f'\\draw[{style}] ({f(x)},{f(y+d)}) -- ({f(x+d)},{f(y)}) -- ({f(x+w)},{f(y)}) -- ({f(x+w)},{f(y+h-d)}) -- ({f(x+w-d)},{f(y+h)}) -- ({f(x)},{f(y+h)}) -- cycle;')
            out.append(f'\\draw[ad{role},line width=0.8pt] ({f(x)},{f(y+d)}) -- ({f(x+w-d)},{f(y+d)}) -- ({f(x+w-d)},{f(y+h)}) ({f(x+w-d)},{f(y+d)}) -- ({f(x+w)},{f(y)});')
        elif n['kind']=='store':
            out.append(f'\\draw[{style},rounded corners=9pt] ({f(x)},{f(y+8)}) rectangle ({f(x+w)},{f(y+h)});')
            out.append(f'\\draw[{style}] ({f(x+w/2)},{f(y+10)}) ellipse [x radius={f(w/2)}pt,y radius=10pt];')
        else:
            out.append(f'\\draw[{style},rounded corners=8pt] ({f(x)},{f(y)}) rectangle ({f(x+w)},{f(y+h)});')
            out.append(f'\\draw[ad{role},line width=2.2pt,line cap=round] ({f(x+12)},{f(y+14)}) -- ({f(x+12)},{f(y+h-14)});')
        labels,details=node_lines(n);total=len(labels)*18+(8+len(details)*15 if details else 0)+(18 if n['tag'] else 0);baseline=y+(h-total)/2+14
        if n['tag']: text(x+w/2,baseline,n['tag'].upper(),8.5,'ad'+role,True,'base');baseline+=18
        for line in labels: text(x+w/2,baseline,line,15,weight=True,anchor='base');baseline+=18
        if details: baseline+=6
        for line in details: text(x+w/2,baseline,line,11.5,'admuted',anchor='base');baseline+=15
    for e in s['edges']:
        if not e['label']: continue
        x,y=label_point(e,route(e,nodes));lw=len(e['label'])*6.3+16
        out.append(f'\\fill[adbg,rounded corners=4pt] ({f(x-lw/2)},{f(y-10)}) rectangle ({f(x+lw/2)},{f(y+10)});');text(x,y+4,e['label'],11,'admuted',anchor='base')
    text(48,s['height']-22,s['footer'],11,'admuted');out.extend([r'\end{tikzpicture}',r'\end{document}',''])
    return '\n'.join(out)

def convert_svg(svg,target):
    exe=shutil.which('inkscape')
    if not exe: raise RuntimeError('PNG/PDF export requires Inkscape. SVG and TeX need only Python.')
    command=[exe,str(svg.resolve()),'--export-filename='+str(target.resolve())]
    if target.suffix=='.png': command.append('--export-dpi=160')
    subprocess.run(command,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=90)
    if not target.exists() or not target.stat().st_size: raise RuntimeError(f'export failed: {target.name}')

def compile_tex(tex_path,pdf_path):
    """Compile generated trusted TeX. No shell escape; this is not an untrusted-TeX sandbox."""
    engines=[p for p in (shutil.which('lualatex'),shutil.which('pdflatex')) if p]
    if not engines: raise RuntimeError('TikZ verification requires LuaLaTeX or pdfLaTeX.')
    failures=[]
    with tempfile.TemporaryDirectory(prefix='archdiagram-tex-') as tmp:
        for i,engine in enumerate(engines):
            work=Path(tmp)/str(i);work.mkdir();shutil.copy2(tex_path,work/'diagram.tex')
            result=subprocess.run([engine,'-no-shell-escape','-interaction=nonstopmode','-halt-on-error','diagram.tex'],cwd=work,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
            if result.returncode:
                failures.append(Path(engine).name+':\n'+result.stdout.decode('utf-8','replace')[-1800:])
                continue
            shutil.copy2(work/'diagram.pdf',pdf_path)
            return Path(engine).name
    raise RuntimeError('TikZ compilation failed with available engines:\n'+'\n'.join(failures))

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--version',action='version',version=VERSION);sub=parser.add_subparsers(dest='command',required=True)
    for command in ('validate','render'):
        p=sub.add_parser(command);p.add_argument('spec',type=Path);p.add_argument('--strict',action='store_true',help='Treat warnings as failures')
        if command=='render':
            p.add_argument('--out',type=Path,required=True,help='Output prefix without extension');p.add_argument('--formats',default='svg,tex',help='Comma-separated svg,tex,png,pdf');p.add_argument('--theme',choices=sorted(THEMES),default='paper');p.add_argument('--compile-tex',action='store_true',help='Verify TikZ into PREFIX.tikz.pdf')
    args=parser.parse_args(argv)
    try:
        if args.spec.stat().st_size>2_000_000: raise SpecError('spec: maximum size is 2 MB')
        raw=json.loads(args.spec.read_text(encoding='utf-8'));s=normalize(raw);issues=lint(s)
        report=dict(version=VERSION,spec_sha256=hashlib.sha256(args.spec.read_bytes()).hexdigest(),nodes=len(s['nodes']),edges=len(s['edges']),issues=issues,evidence=s['evidence'],assumptions=s['assumptions'])
        failed=any(x['severity']=='error' for x in issues) or bool(args.strict and issues)
        if args.command=='validate': print(json.dumps(report,indent=2,ensure_ascii=False));return 2 if failed else 0
        formats=set(args.formats.split(','))
        if not formats or formats-{'svg','tex','png','pdf'}: raise SpecError('formats: use svg,tex,png,pdf')
        args.out.parent.mkdir(parents=True,exist_ok=True)
        def output(suffix): return args.out.parent/(args.out.name+suffix)
        if failed:
            output('.report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(json.dumps(report,indent=2));return 2
        files=[]
        if formats & {'svg','png','pdf'}: output('.svg').write_text(render_svg(raw,args.theme),encoding='utf-8');files.append(str(output('.svg')))
        if 'tex' in formats or args.compile_tex: output('.tex').write_text(render_tikz(raw,args.theme),encoding='utf-8');files.append(str(output('.tex')))
        for fmt in ('png','pdf'):
            if fmt in formats: convert_svg(output('.svg'),output('.'+fmt));files.append(str(output('.'+fmt)))
        if args.compile_tex: report['tex_engine']=compile_tex(output('.tex'),output('.tikz.pdf'));files.append(str(output('.tikz.pdf')))
        report['outputs']=files;report['visual_review']='Required: inspect rendered output at target width. Lint is heuristic.'
        output('.report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(json.dumps(report,indent=2,ensure_ascii=False));return 0
    except (SpecError,OSError,ValueError,RuntimeError,subprocess.SubprocessError) as exc:
        print(f'archdiagram: {exc}',file=sys.stderr);return 2

if __name__=='__main__': raise SystemExit(main())
