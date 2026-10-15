"""Original monochrome TikZ primitives for the architecture atlas. Python 3.10+."""
from __future__ import annotations
from dataclasses import dataclass
import re
from pathlib import Path

PREAMBLE=r'''\documentclass[tikz,border=5pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{lmodern,amsmath,amssymb}
\usetikzlibrary{arrows.meta,calc,positioning,fit,backgrounds,shapes.geometric,matrix,decorations.pathreplacing,patterns}
\definecolor{ink}{gray}{0.08}
\definecolor{wash}{gray}{0.965}
\definecolor{soft}{gray}{0.45}
\tikzset{box/.style={draw=ink,line width=.65pt,fill=white,align=center,inner sep=4pt,outer sep=0pt,font=\small},flow/.style={draw=ink,line width=.65pt,-{Latex[length=1.8mm,width=1.3mm]},rounded corners=2pt},annotation/.style={font=\scriptsize,text=soft,align=center},groupbox/.style={draw=soft,dashed,line width=.45pt,fill=wash}}
\begin{document}
\begin{tikzpicture}[x=1cm,y=-1cm,font=\rmfamily,text=ink]
'''
@dataclass
class Node:
    id:str; label:str; x:float; y:float; w:float; h:float; kind:str='block'

class Figure:
    def __init__(self,title,width=16,height=9,subtitle='',caption=''):
        self.title=title;self.width=width;self.height=height;self.subtitle=subtitle;self.caption=caption
        self.nodes={};self.edges=[];self.groups=[];self.commands=[]
    def node(self,id,label,x,y,w=2.5,h=.8,kind='block'):
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',id) or id in self.nodes: raise ValueError('Duplicate or invalid node ID: '+id)
        if kind not in {'block','tensor','store','circle','diamond','plain'}: raise ValueError('Unknown kind '+kind)
        self.nodes[id]=Node(id,label,x,y,w,h,kind);return id
    def edge(self,a,b,label='',side=None,to_side=None,via=None,style='data',label_side=None):
        if a not in self.nodes or b not in self.nodes:raise ValueError('Unknown endpoint')
        self.edges.append(dict(a=a,b=b,label=label,side=side,to_side=to_side,via=via or [],style=style,label_side=label_side))
    def group(self,label,x,y,w,h):self.groups.append((label,x,y,w,h))
    def raw(self,tex):self.commands.append(tex)
    def check(self):
        issues=[]
        for n in self.nodes.values():
            if n.x-n.w/2<0 or n.x+n.w/2>self.width or n.y-n.h/2<1.2 or n.y+n.h/2>self.height-.6:issues.append('Node bounds: '+n.id)
        nodes=list(self.nodes.values())
        for i,a in enumerate(nodes):
            for b in nodes[i+1:]:
                if a.kind!='plain' and b.kind!='plain' and abs(a.x-b.x)<(a.w+b.w)/2-.015 and abs(a.y-b.y)<(a.h+b.h)/2-.015:issues.append('Node overlap: '+a.id+' / '+b.id)
        return issues
    def tex(self):
        def esc(t):return t.replace('&',r'\&')
        out=[PREAMBLE,f'\\path[use as bounding box] (0,0) rectangle ({self.width},{self.height});',f'\\node[anchor=west,font=\\large\\bfseries] at (.2,.4) {{{esc(self.title)}}};']
        if self.subtitle:out.append(f'\\node[anchor=west,font=\\footnotesize,text=soft] at (.2,.85) {{{esc(self.subtitle)}}};')
        out.append(r'\begin{pgfonlayer}{background}')
        for label,x,y,w,h in self.groups:
            out.append(f'\\draw[groupbox] ({x},{y}) rectangle ({x+w},{y+h});')
            out.append(f'\\node[anchor=west,font=\\scriptsize,fill=white,inner sep=2pt] at ({x+.15},{y}) {{{label}}};')
        out.append(r'\end{pgfonlayer}')
        for n in self.nodes.values():
            style='box';extra=''
            if n.kind=='circle':extra=',circle'
            elif n.kind=='diamond':extra=',diamond,aspect=1.7'
            elif n.kind=='store':extra=',fill=wash'
            elif n.kind=='plain':style='align=center,inner sep=0pt,outer sep=0pt,font=\\small'
            elif n.kind=='tensor':extra=',fill=wash'
            out.append(f'\\node[{style}{extra},minimum width={n.w}cm,minimum height={n.h}cm,text width={max(.18,n.w-.25)}cm] ({n.id}) at ({n.x},{n.y}) {{{n.label}}};')
            if n.kind=='tensor':out.append(f'\\draw[ink,line width=.4pt] ({n.x-n.w/2+.10},{n.y-n.h/2-.10}) -- ({n.x+n.w/2+.10},{n.y-n.h/2-.10}) -- ({n.x+n.w/2+.10},{n.y+n.h/2-.10});')
        out.append(r'\begin{pgfonlayer}{background}')
        for e in self.edges:
            a,b=self.nodes[e['a']],self.nodes[e['b']];dx,dy=b.x-a.x,b.y-a.y
            horizontal=abs(dx)>=abs(dy)
            side=e['side'] or (('east' if dx>=0 else 'west') if horizontal else ('south' if dy>=0 else 'north'))
            dest=e['to_side'] or (('west' if dx>=0 else 'east') if horizontal else ('north' if dy>=0 else 'south'))
            style={'data':'','control':',dashed','feedback':',dotted','undirected':',-','skip':',dashed'}.get(e['style'])
            if style is None:raise ValueError('Unknown edge style')
            coord=' -- '.join([f'({a.id}.{side})',*[f'({x},{y})' for x,y in e['via']],f'({b.id}.{dest})'])
            label=''
            if e['label']:
                labelside=e['label_side'] or ('above' if horizontal else 'right')
                label=f' node[midway,{labelside},fill=white,inner sep=1.5pt,font=\\scriptsize] {{{e["label"]}}}'
            out.append(f'\\draw[flow{style}] {coord}{label};')
        out.extend([r'\end{pgfonlayer}',*self.commands])
        if self.caption:out.append(f'\\node[anchor=west,align=left,font=\\scriptsize,text=soft,text width={self.width-.4}cm] at (.2,{self.height-.25}) {{{esc(self.caption)}}};')
        out.extend([r'\end{tikzpicture}',r'\end{document}',''])
        return '\n'.join(out)
    def write(self,folder,id,family,description,sources,assumptions=None,tags=None):
        issues=self.check()
        if issues:raise ValueError(id+': '+'; '.join(issues))
        folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);path=folder/(id+'.tex');path.write_text(self.tex())
        return dict(id=id,title=self.title,family=family,description=description,caption=self.caption,sources=sources,assumptions=assumptions or ['Conceptual schematic; dimensions and details vary by implementation.'],tags=tags or [],nodes=len(self.nodes),edges=len(self.edges),source_file=str(path.name),width_cm=self.width,height_cm=self.height)
