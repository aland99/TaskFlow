"""Verify exported XML, PDF inventories, page geometry and render review samples."""
import hashlib
from html.parser import HTMLParser
import importlib
import json
from pathlib import Path
import re
import subprocess
import sys
from xml.etree import ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parent))
from config import ROOT,roster
from pypdf import PdfReader
import pdfplumber

OUT=ROOT/'qa/project1/final'
RENDER=ROOT/'qa/project1/tmp/final-review'

class Plain(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.parts=[]
    def handle_data(self,data):self.parts.append(data)
def plain(text):
    parser=Plain();parser.feed(text or '');return ''.join(parser.parts)

def main():
    RENDER.mkdir(parents=True,exist_ok=True)
    entries=[];all_cases=set();all_reqs=set();xml_checks=[]
    for m in roster():
        data=importlib.import_module(Path(m['data_file']).stem)
        cases={c['id']:c for s in data.SUITES for c in s['cases']}
        reqs={rid for s in data.REQ_SPECS for rid,_,_ in s['reqs']}
        all_cases.update(cases);all_reqs.update(reqs)
        base=ROOT/'qa/project1'/data.AUTHOR
        tree=ET.parse(base/f'{data.AUTHOR}-testsuites.xml')
        exported=tree.findall('.//testcase');assert len(exported)==len(cases)
        links=0
        for tc in exported:
            cid=re.match(r'TC-[A-E]-[0-9]{3}',tc.attrib['name']).group(0)
            expected=cases[cid]; steps=tc.findall('./steps/step')
            assert len(steps)==len(expected['steps']),cid
            for step,(a,e) in zip(steps,expected['steps']):
                assert plain(step.findtext('actions'))==a,(cid,'action content')
                assert plain(step.findtext('expectedresults'))==e,(cid,'expected content')
            actual={r.text for r in tc.findall('./requirements/requirement/doc_id')}
            assert actual==set(expected['reqs']),(cid,'XML requirement links')
            links+=len(actual)
        reqtree=ET.parse(base/f'{data.AUTHOR}-requirements.xml')
        assert {r.findtext('docid') for r in reqtree.findall('.//requirement')}==reqs
        xml_checks.append({'author':data.AUTHOR,'cases':len(exported),'links':links,'all_steps_and_mappings_match':True})
        for kind in ('TestLink_Test_Case_Report','Test_Basis_Requirements'):
            entries.append((base/f'{data.AUTHOR.capitalize()}_{kind}.pdf',set(cases),reqs))
    for name in ('TaskFlow_TestLink_Test_Case_Report.pdf','TaskFlow_Test_Basis_Requirements.pdf','TaskFlow_Requirements_Traceability_Matrix.pdf'):
        entries.append((OUT/name,all_cases,all_reqs))
    results=[]
    selected_authors=next((x.split('=',1)[1].split(',') for x in sys.argv if x.startswith('--authors=')),None)
    for index,(path,cases,reqs) in enumerate(entries,1):
        if selected_authors and (path.parent.name not in selected_authors or 'Test_Basis' not in path.name):
            continue
        reader=PdfReader(path);texts=[page.extract_text() or '' for page in reader.pages]
        combined='\n'.join(texts)
        found_cases=set(re.findall(r'TC-[A-E]-[0-9]{3}',combined))
        found_reqs=set(re.findall(r'REQ-[A-E]-[0-9]{3}',combined))
        assert found_cases==cases,(path.name,'case inventory',cases-found_cases,found_cases-cases)
        assert found_reqs==reqs,(path.name,'requirement inventory',reqs-found_reqs,found_reqs-reqs)
        with pdfplumber.open(path) as pdf:
            outside=[n+1 for n,p in enumerate(pdf.pages) if any(c['x0'] < -1 or c['x1'] > p.width+1 for c in p.chars)]
        assert not outside,(path.name,'text outside page',outside)
        sampled=sorted({1,len(texts)//2+1,len(texts),min(6,len(texts))})
        samples=[]
        for page in sampled:
            prefix=RENDER/f'{index:02d}-{page:03d}'
            subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-scale-to','1100','-png',str(path),str(prefix)],check=True,capture_output=True)
            samples.append(str(prefix.with_suffix('.png').relative_to(ROOT)))
        result={'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                'pages':len(texts),'distinct_cases':len(found_cases),'distinct_requirements':len(found_reqs),
                'inventory_matches':True,'out_of_bounds_pages':outside,'rendered_sample_pages':sampled,'rendered_images':samples}
        results.append(result)
        print(path.name,len(texts),'pages; inventory and geometry passed; samples rendered',flush=True)
    if selected_authors:
        previous=json.loads((OUT/'pdf-verification.json').read_text())
        updated={r['path']:r for r in results}
        results=[updated.get(r['path'],r) for r in previous['pdf_checks']]
    report={'xml_checks':xml_checks,'pdf_checks':results,'visual_review':'Rendered first/body/middle/last samples pending visual inspection before packaging.'}
    (OUT/'pdf-verification.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
