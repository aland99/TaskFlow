"""Finalize the actual local TestLink database and package the reviewed group design.

Usage (with Docker available):
  python3 -I qa/testlink/scripts/group_submission.py audit
  python3 -I qa/testlink/scripts/group_submission.py package [--zip /absolute/output.zip]
Requires reportlab for the database-derived matrix PDF. Native TestLink reports
must be generated with report.py for every member and for all before packaging.
"""
import argparse
import csv
import html
import importlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile
from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo
sys.path.insert(0,str(Path(__file__).resolve().parent))
from config import KIT, ROOT, PREFIX, PROJECT, SOURCE_COMMIT, REPO, BUILD, PLAN, roster, refresh_header
from audit import sql, audit
from validate import validate_module

OUT=ROOT/'qa/project1/final'
LABEL='SECJ3343_Project1_Group_TaskFlow'
PACK=OUT/LABEL

def modules():
    result=[]
    for member in roster():
        name=Path(member.get('data_file',member['login']+'_testdata.py')).stem
        data=importlib.import_module(name)
        validate_module(data)
        assert data.LETTER==member['letter'] and data.AUTHOR==member['login']
        result.append((member,data))
    assert [d.LETTER for _,d in result]==list('ABCDE')
    return result

def matrix_pdf(summary,reqrows,links,cases):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4,landscape
    from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,LongTable,TableStyle
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Cell',fontName='Helvetica',fontSize=8.5,leading=11,spaceAfter=1))
    styles.add(ParagraphStyle(name='SmallNote',fontName='Helvetica',fontSize=9,leading=13))
    clean=lambda s: str(s).replace('\u2013','-').replace('\u2014','-').replace('\u2019',"'")
    para=lambda s: Paragraph(html.escape(clean(s)).replace('\n','<br/>'),styles['Cell'])
    req_to_cases=defaultdict(list); case_to_reqs=defaultdict(list)
    for rid,cid,external in links:
        req_to_cases[rid].append(f'{cid} ({external})')
        case_to_reqs[cid].append(rid)
    def footer(canvas,doc):
        canvas.setFont('Helvetica',8); canvas.setFillColor(colors.HexColor('#506175'))
        canvas.drawString(32,22,'SECJ3343 - Group TaskFlow - Actual TestLink req_coverage')
        canvas.drawRightString(landscape(A4)[0]-32,22,str(doc.page))
    def table(rows,widths):
        t=LongTable(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#16324f')),
            ('TEXTCOLOR',(0,0),(-1,0),colors.white),
            ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,0),9),
            ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),
            ('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),
            ('BOTTOMPADDING',(0,0),(-1,-1),6),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f1f5f9')]),
            ('LINEBELOW',(0,0),(-1,0),1,colors.HexColor('#16324f')),
            ('GRID',(0,1),(-1,-1),0.3,colors.HexColor('#d3dce6')),
        ])); return t
    story=[Paragraph('Requirements Traceability Matrix',styles['Title']),
           Paragraph('UTM SECJ3343 Software Quality Assurance - Project 1 - Group TaskFlow',styles['SmallNote']),
           Spacer(1,10),Paragraph(f"{summary['requirements']} / {summary['requirements']} requirements covered (100%). "
                                 f"{summary['test_cases']} / {summary['test_cases']} cases mapped. "
                                 f"{summary['links']} active requirement-to-case links.",styles['Heading2']),
           Paragraph('Both directions below are read from the actual TestLink req_coverage table and joined to requirement and case records. '
                     'Stable TC-A/B/C/D/E IDs are portable names; TF-N is the external ID in this local TestLink project. '
                     'All cases are manual designs. No execution results are claimed.',styles['SmallNote']),
           Spacer(1,8),Paragraph(f'Software baseline: {PROJECT} main@{SOURCE_COMMIT}. Plan: {PLAN}. Build: {BUILD}.',styles['SmallNote']),
           Paragraph('Requirement to test cases',styles['Heading1'])]
    rows=[['Requirement / title','Designer','Mapped cases from TestLink']]
    owner={m['letter']:m['name'] for m in roster()}
    for rid,title in reqrows:
        rows.append([para(rid+'\n'+title),para(owner[rid.split('-')[1]]),para(', '.join(req_to_cases[rid]))])
    story += [table(rows,[210,90,477]),PageBreak(),Paragraph('Test case to requirements',styles['Heading1'])]
    rows=[['Stable case / TestLink ID','Test case title','Mapped requirements']]
    for cid,external,title in cases:
        rows.append([para(cid+' / '+external),para(title),para(', '.join(case_to_reqs[cid]))])
    story.append(table(rows,[140,365,272]))
    dest=OUT/'TaskFlow_Requirements_Traceability_Matrix.pdf'
    SimpleDocTemplate(str(dest),pagesize=landscape(A4),leftMargin=32,rightMargin=32,topMargin=32,bottomMargin=36,
                      title='TaskFlow requirements traceability matrix',author='Group TaskFlow').build(story,onFirstPage=footer,onLaterPages=footer)
    print('wrote',dest,flush=True)

def audit_group():
    OUT.mkdir(parents=True,exist_ok=True)
    members=modules(); refresh_header()
    pid=int(sql(f"SELECT id FROM testprojects WHERE prefix='{PREFIX}'")[0][0])
    spec_order=0
    for order,(member,data) in enumerate(members,1):
        safe=data.TOP_SUITE.replace("'","''")
        sql(f"UPDATE nodes_hierarchy SET node_order={order} WHERE parent_id={pid} AND node_type_id=2 AND name='{safe}'")
        for spec in data.REQ_SPECS:
            spec_order+=1
            sql(f"UPDATE nodes_hierarchy n JOIN req_specs s ON s.id=n.id SET n.node_order={spec_order} WHERE s.testproject_id={pid} AND s.doc_id='{spec['doc_id']}'")
        audit(data.AUTHOR)
    top_ids=[int(r[0]) for r in sql(f'SELECT id FROM nodes_hierarchy WHERE parent_id={pid} AND node_type_id=2')]
    parent_ids=','.join(map(str,top_ids))
    cases_raw=sql(f"SELECT n.name,v.tc_external_id,v.id,u.login FROM nodes_hierarchy n JOIN nodes_hierarchy suite ON suite.id=n.parent_id "
                  f"JOIN nodes_hierarchy vn ON vn.parent_id=n.id AND vn.node_type_id=4 JOIN tcversions v ON v.id=vn.id "
                  f"JOIN users u ON u.id=v.author_id WHERE suite.parent_id IN ({parent_ids}) ORDER BY n.name")
    stable=lambda s: re.match(r'TC-[A-E]-[0-9]{3}',s).group(0)
    cases=[(stable(n),f'{PREFIX}-{ext}',n) for n,ext,vid,user in cases_raw]
    expected_cases={c['id'] for _,d in members for s in d.SUITES for c in s['cases']}
    assert {c[0] for c in cases}==expected_cases and len(cases)==len(expected_cases)
    reqrows=sql(f"SELECT r.req_doc_id,n.name FROM requirements r JOIN req_specs s ON s.id=r.srs_id JOIN nodes_hierarchy n ON n.id=r.id WHERE s.testproject_id={pid} ORDER BY r.req_doc_id")
    raw=sql(f"SELECT r.req_doc_id,n.name,v.tc_external_id FROM req_coverage c JOIN requirements r ON r.id=c.req_id "
            f"JOIN req_specs s ON s.id=r.srs_id JOIN nodes_hierarchy n ON n.id=c.testcase_id JOIN tcversions v ON v.id=c.tcversion_id "
            f"WHERE s.testproject_id={pid} AND c.is_active=1 ORDER BY r.req_doc_id,v.tc_external_id")
    links=[(rid,stable(n),f'{PREFIX}-{ext}') for rid,n,ext in raw]
    expected_links={(r,c['id']) for _,d in members for s in d.SUITES for c in s['cases'] for r in c['reqs']}
    assert {(r,c) for r,c,e in links}==expected_links and len(links)==len(expected_links)
    assert {r for r,t in reqrows}=={r for r,c,e in links}
    assert {c for r,c,e in links}==expected_cases
    plan_id=int(sql(f"SELECT p.id FROM testplans p JOIN nodes_hierarchy n ON n.id=p.id WHERE p.testproject_id={pid} AND n.name='{PLAN}'")[0][0])
    assignments=int(sql(f"SELECT COUNT(DISTINCT p.tcversion_id) FROM testplan_tcversions p JOIN tcversions v ON v.id=p.tcversion_id "
                        f"JOIN user_assignments a ON a.feature_id=p.id AND a.user_id=v.author_id JOIN builds b ON b.id=a.build_id "
                        f"WHERE p.testplan_id={plan_id} AND b.name='{BUILD}'")[0][0])
    assert assignments==len(cases),'Not every case is assigned to its author'
    summary={'course':'SECJ3343','group':'TaskFlow','software_baseline':SOURCE_COMMIT,
             'generated_local':datetime.now(ZoneInfo('Asia/Baghdad')).isoformat(),
             'test_cases':len(cases),'requirements':len(reqrows),'links':len(links),'coverage_percent':100,
             'assigned_to_author':assignments,'suites':sum(len(d.SUITES) for _,d in members),
             'steps':sum(len(c['steps']) for _,d in members for s in d.SUITES for c in s['cases']),
             'execution_results_total':int(sql('SELECT COUNT(*) FROM executions')[0][0]),
             'members':[dict(member,**validate_module(data)) for member,data in members]}
    (OUT/'group-audit.json').write_text(json.dumps(summary,indent=2)+'\n')
    with (OUT/'requirements-traceability.csv').open('w',newline='') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['Requirement','Stable case','TestLink external ID']);w.writerows(links)
    matrix_pdf(summary,reqrows,links,cases)
    print(json.dumps(summary,indent=2),flush=True)

def package(destination=None):
    summary=json.loads((OUT/'group-audit.json').read_text())
    PACK.mkdir(parents=True,exist_ok=True)
    for number,source,label in [(1,'TaskFlow_TestLink_Test_Case_Report.pdf','TestLink_Test_Case_Report'),
                                (2,'TaskFlow_Test_Basis_Requirements.pdf','Test_Basis_Requirements'),
                                (3,'TaskFlow_Requirements_Traceability_Matrix.pdf','Requirements_Traceability_Matrix')]:
        shutil.copy2(OUT/source,PACK/f'{number}_{LABEL}_{label}.pdf')
    for member,data in modules():
        source=ROOT/'qa/project1'/data.AUTHOR
        individual=PACK/'Individual'/member['name'].replace(' ','_')
        individual.mkdir(parents=True,exist_ok=True)
        for suffix in ('TestLink_Test_Case_Report','Test_Basis_Requirements'):
            shutil.copy2(source/f'{data.AUTHOR.capitalize()}_{suffix}.pdf',individual/f'{member["name"].replace(" ","_")}_{suffix}.pdf')
        xml=PACK/'TestLink_XML_Export';xml.mkdir(exist_ok=True)
        for kind in ('requirements','testsuites'):
            shutil.copy2(source/f'{data.AUTHOR}-{kind}.xml',xml/f'{data.AUTHOR}-{kind}.xml')
    sources=PACK/'Source_Documents';sources.mkdir(exist_ok=True)
    for file in sorted((ROOT/'qa/project1/Source_Documents').glob('*.pdf')): shutil.copy2(file,sources/file.name)
    evidence=PACK/'Verification';evidence.mkdir(exist_ok=True)
    for file in ('group-audit.json','requirements-traceability.csv','pdf-verification.json'):
        source=OUT/file
        if source.exists():shutil.copy2(source,evidence/file)
    review=ROOT/'qa/project1/GROUP_REVIEW.md'
    if review.exists():shutil.copy2(review,evidence/review.name)
    lines=['UTM SECJ3343 SOFTWARE QUALITY ASSURANCE','PROJECT 1 - TEST CASE DESIGN','GROUP: TaskFlow',
           'Due: 27 October 2026','Leader: Aland Karwan','Repository: '+REPO,'Software baseline: main@'+SOURCE_COMMIT,'',
           'MEMBERS AND ACTUAL SUBMITTED AREAS']
    for m in summary['members']:
        lines.append(f"{m['letter']} - {m['name']} ({m['author']}): {m['area']}; {m['test_cases']} cases, {m['requirements']} requirements, {m['suites']} suites, 100% mapped.")
    lines += ['',f"TOTAL: {summary['test_cases']} cases, {summary['requirements']} requirements, {summary['suites']} suites, {summary['steps']} numbered steps, {summary['links']} active requirement-to-case links.",
              'All requirements covered; every case mapped. All cases assigned to their own author in the Project 1 plan/build.',
              'Design stage only: no execution results are claimed.','', 'CONTENTS',
              '1_...pdf: combined test case report generated by TestLink and printed with Chrome.',
              '2_...pdf: combined requirements test basis generated by TestLink and printed with Chrome.',
              '3_...pdf: bidirectional requirements traceability matrix read from actual TestLink req_coverage.',
              'Individual/<Member>/: two freshly generated individual TestLink PDFs for every member.',
              'TestLink_XML_Export/: requirements and testsuite exports for each member.',
              'Source_Documents/: committed README and source code baseline as PDFs.',
              'Verification/: actual database audit, CSV mappings, PDF checks and group review notes.','',
              'IDENTITY RECONCILIATION',
              'The original prompts inferred GitHub names. Mhamad submitted B as mhammedazad (GitHub MhammedAzad); Lanya submitted C. Actual authored areas and IDs are preserved.',
              'Each of the four teammates contributed a PR (#1 through #4). Aland authored area A, reviewed/integrated the work and generated all reports locally.',
              'Rasan could not run TestLink in his environment; his original designs were imported and printed on the leader laptop.','',
              'SUBMISSION ACTIONS',
              'The lecturer slides require the existing assigned lecturer TestLink project. Import these XML exports there if required, checking project prefix and requirement links; do not create another lecturer-server project.',
              'The lecturer server has not been accessed and no university submission has been made by this tooling.',
              'Upload the required TestLink case report and test basis through the course submission channel; include the matrix/supporting files where permitted.','']
    (PACK/'README.txt').write_text('\n'.join(lines))
    manifest={str(p.relative_to(PACK)):p.stat().st_size for p in sorted(PACK.rglob('*')) if p.is_file() and p.name!='manifest.json'}
    (PACK/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    destination=Path(destination) if destination else OUT/(LABEL+'.zip')
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED) as z:
        for file in sorted(PACK.rglob('*')):
            if file.is_file():z.write(file,Path(LABEL)/file.relative_to(PACK))
    with zipfile.ZipFile(destination) as z:assert z.testzip() is None
    print('Packaged',destination,'files',len(manifest)+1,'bytes',destination.stat().st_size)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['audit','package']);parser.add_argument('--zip')
    args=parser.parse_args()
    if args.mode=='audit':audit_group()
    else:package(args.zip)
