import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/draw-architecture'
s=importlib.util.spec_from_file_location('ad',SKILL/'scripts/archdiagram.py');ad=importlib.util.module_from_spec(s);s.loader.exec_module(ad)

def base():
    return dict(version=1,title='A & B',nodes=[dict(id='a',label='Read <evidence>',col=0,row=0),dict(id='b',label='Answer',col=1,row=0)],edges=[{'from':'a','to':'b'}])

class RendererTests(unittest.TestCase):
    def reject(self,change):
        raw=base();change(raw)
        with self.assertRaises(ad.SpecError): ad.normalize(raw)
    def test_examples_strict(self):
        for p in (SKILL/'assets/examples').glob('*.json'):
            with self.subTest(p=p.name): self.assertEqual(ad.lint(ad.normalize(json.loads(p.read_text()))),[])
    def test_default_canvas_fits_legend(self):
        s=ad.normalize(dict(version=1,nodes=[dict(id='only')]))
        self.assertGreaterEqual(s['width'],520);self.assertEqual(ad.lint(s),[])
    def test_input_not_mutated(self):
        raw=base();before=copy.deepcopy(raw);ad.render_svg(raw);ad.render_tikz(raw);self.assertEqual(raw,before)
    def test_deterministic_svg(self): self.assertEqual(ad.render_svg(base()),ad.render_svg(base()))
    def test_deterministic_tex(self): self.assertEqual(ad.render_tikz(base()),ad.render_tikz(base()))
    def test_svg_is_valid_xml(self):
        root=ET.fromstring(ad.render_svg(base()));self.assertTrue(root.tag.endswith('svg'))
    def test_svg_keeps_text_and_accessibility(self):
        output=ad.render_svg(base());self.assertIn('<text ',output);self.assertIn('aria-labelledby=',output);self.assertIn('<desc ',output)
    def test_script_in_label_is_text(self):
        raw=base();raw['nodes'][0]['label']='<script>alert(1)</script>'
        svg=ad.render_svg(raw);ET.fromstring(svg);self.assertNotIn('<script>',svg);self.assertIn('&lt;script&gt;',svg)
    def test_tex_literals_are_escaped(self):
        raw=base();raw['nodes'][0]['label']=r'\input{secret} $x_y$ & 50%'
        output=ad.render_tikz(raw);self.assertNotIn(r'\input{secret}',output);self.assertIn(r'\textbackslash{}input\{secret\}',output);self.assertIn(r'\$x\_y\$',output)
    def test_unicode_svg(self):
        raw=base();raw['nodes'][0]['label']='관측 → 행동';self.assertIn('관측',ad.render_svg(raw))
    def test_unknown_field(self): self.reject(lambda s:s.update(layout_magic=True))
    def test_duplicate_id(self): self.reject(lambda s:s['nodes'][1].update(id='a'))
    def test_missing_endpoint(self): self.reject(lambda s:s['edges'][0].update(to='missing'))
    def test_bad_endpoint_type(self): self.reject(lambda s:s['edges'][0].update(to=[]))
    def test_bad_role_type(self): self.reject(lambda s:s['nodes'][0].update(role={}))
    def test_bad_coordinates(self): self.reject(lambda s:s['nodes'][0].update(x=30))
    def test_mixed_coordinates(self): self.reject(lambda s:s['nodes'][0].update(x=30,y=40))
    def test_nonfinite(self): self.reject(lambda s:s.update(width=float('nan')))
    def test_boolean_number(self): self.reject(lambda s:s.update(width=True))
    def test_bad_version(self): self.reject(lambda s:s.update(version=True))
    def test_small_canvas(self): self.reject(lambda s:s.update(width=300))
    def test_unknown_kind(self): self.reject(lambda s:s['nodes'][0].update(kind='cloud'))
    def test_bad_group_member(self): self.reject(lambda s:s.update(groups=[dict(id='g',members=['absent'])]))
    def test_bad_group_box(self): self.reject(lambda s:s.update(groups=[dict(id='g',members=['a'],x=1)]))
    def test_long_label_warns(self):
        raw=base();raw['nodes'][0]['label']='many words '*20
        self.assertIn('text-fit',[x['code'] for x in ad.lint(ad.normalize(raw))])
    def test_overlap_is_error(self):
        raw=base();raw['nodes'][1]['col']=0
        self.assertIn('node-overlap',[x['code'] for x in ad.lint(ad.normalize(raw))])
    def test_edge_intersection_detected(self):
        raw=base();raw['nodes'].append(dict(id='obstacle',x=270,y=150,width=30,height=84))
        self.assertIn('edge-through-node',[x['code'] for x in ad.lint(ad.normalize(raw))])
    def test_edge_label_collision_detected(self):
        raw=base();raw['edges'][0].update(label='crossing',label_at=[150,190])
        self.assertIn('edge-label-overlap',[x['code'] for x in ad.lint(ad.normalize(raw))])
    def test_custom_route_preserved(self):
        raw=base();raw['edges'][0]['via']=[[285,192],[285,300],[400,300]]
        normalized=ad.normalize(raw);path=ad.route(normalized['edges'][0],{n['id']:n for n in normalized['nodes']})
        self.assertEqual(path[1],(285,192));self.assertIn((400,300),path)
    def test_side_relative_ports(self):
        raw=base();raw['edges'][0].update(from_side='right',to_side='left',from_offset=.25,to_offset=-.25)
        normalized=ad.normalize(raw);path=ad.route(normalized['edges'][0],{n['id']:n for n in normalized['nodes']})
        self.assertEqual(path[0],(250,213));self.assertEqual(path[-1],(320,171))
    def test_invalid_port_offset(self): self.reject(lambda s:s['edges'][0].update(from_offset=.8))
    def test_all_themes_parse(self):
        for theme in ad.THEMES: ET.fromstring(ad.render_svg(base(),theme))
    def test_unknown_theme(self):
        with self.assertRaises(ad.SpecError): ad.render_svg(base(),'unknown')
    def test_cli_svg_and_tex(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);(d/'spec.json').write_text(json.dumps(base()));result=subprocess.run([sys.executable,str(SKILL/'scripts/archdiagram.py'),'render',str(d/'spec.json'),'--out',str(d/'figure.v1'),'--strict'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr+result.stdout);self.assertTrue((d/'figure.v1.svg').is_file());self.assertTrue((d/'figure.v1.tex').is_file())
    def test_cli_strict_warning_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw=base();raw['nodes'][0]['label']='many words '*20;d=Path(tmp);(d/'spec.json').write_text(json.dumps(raw))
            result=subprocess.run([sys.executable,str(SKILL/'scripts/archdiagram.py'),'render',str(d/'spec.json'),'--out',str(d/'figure'),'--strict'],capture_output=True)
            self.assertEqual(result.returncode,2);self.assertFalse((d/'figure.svg').exists());self.assertTrue((d/'figure.report.json').exists())
    def test_paper_svg_is_monochrome(self):
        import re
        colors=re.findall(r'#[0-9A-Fa-f]{6}',ad.render_svg(base(),'paper'))
        self.assertTrue(colors)
        self.assertTrue(all(c[1:3].lower()==c[3:5].lower()==c[5:7].lower() for c in colors))
    def test_complete_atlas_inventory(self):
        expected={'vision':20,'text':20,'audio':20,'multimodal':15,'agents':15,'robotics-graphs':10}
        identities=[]
        for family,count in expected.items():
            folder=SKILL/'assets/atlas'/family;rows=json.loads((folder/'index.json').read_text())
            self.assertEqual(len(rows),count)
            for row in rows:
                self.assertEqual(row['family'],family);self.assertTrue((folder/row['source_file']).is_file())
                self.assertTrue(row.get('sources'));identities.append(row['id'])
        self.assertEqual(len(identities),100);self.assertEqual(len(set(identities)),100)
    def test_atlas_search_and_copy(self):
        command=[sys.executable,str(SKILL/'scripts/atlas.py')]
        result=subprocess.run(command+['find','cross attention','--family','text','--json'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr);rows=json.loads(result.stdout);self.assertTrue(rows)
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'figure.tex';result=subprocess.run(command+['copy','--id',rows[0]['id'],'--out',str(out)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr);self.assertIn('documentclass',out.read_text())
            out.write_text('user edit');result=subprocess.run(command+['copy','--id',rows[0]['id'],'--out',str(out)],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0);self.assertEqual(out.read_text(),'user edit')
    def test_installer_copies_portable_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            command=[sys.executable,str(ROOT/'scripts/install_skill.py'),'--dest',tmp]
            for _ in range(2):
                result=subprocess.run(command,capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stderr)
            self.assertTrue((Path(tmp)/'draw-architecture/SKILL.md').exists())
    def test_installer_preserves_modified_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'draw-architecture';target.mkdir();(target/'SKILL.md').write_text('user edits')
            result=subprocess.run([sys.executable,str(ROOT/'scripts/install_skill.py'),'--dest',tmp],capture_output=True)
            self.assertNotEqual(result.returncode,0);self.assertEqual((target/'SKILL.md').read_text(),'user edits')

if __name__=='__main__': unittest.main()
