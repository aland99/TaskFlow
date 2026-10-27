"""Compare each authored module with actual TestLink rows, links, steps and assignments."""
import csv
import importlib
import json
import re
from pathlib import Path
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from config import KIT, ROOT, PREFIX, PLAN
from validate import validate_module

def sql(q):
    out=subprocess.run(['docker','compose','exec','-T','db','mariadb','-uroot','-proot','-N','testlink','-e',q],
                       cwd=KIT,check=True,capture_output=True,text=True).stdout
    return [line.split('\t') for line in out.strip().splitlines() if line]

def audit(name):
    data=importlib.import_module(f'{name}_testdata')
    result=validate_module(data)
    pid=int(sql(f"SELECT id FROM testprojects WHERE prefix='{PREFIX}'")[0][0])
    cases=[c for suite in data.SUITES for c in suite['cases']]
    rows=sql(f"SELECT n.name,v.tc_external_id,u.login,v.id,COUNT(st.id) FROM nodes_hierarchy n "
             f"JOIN nodes_hierarchy vn ON vn.parent_id=n.id AND vn.node_type_id=4 JOIN tcversions v ON v.id=vn.id "
             f"JOIN users u ON u.id=v.author_id LEFT JOIN nodes_hierarchy sn ON sn.parent_id=v.id AND sn.node_type_id=9 "
             f"LEFT JOIN tcsteps st ON st.id=sn.id WHERE n.name LIKE 'TC-{data.LETTER}-%' GROUP BY v.id ORDER BY v.tc_external_id")
    assert len(rows)==len(cases),'Wrong imported case count'
    by_name={r[0]:r for r in rows}
    for case in cases:
        row=by_name[case['name']]
        assert row[2]==data.AUTHOR, f'Wrong author: {case["id"]}'
        assert int(row[4])==len(case['steps']),f'Wrong step count: {case["id"]}'
        assert sql(f"SELECT 1 FROM testplan_tcversions p JOIN testplans plan ON plan.id=p.testplan_id "
                   f"WHERE p.tcversion_id={int(row[3])} AND plan.testproject_id={pid}"),f'Not in plan: {case["id"]}'
    links=sql(f"SELECT r.req_doc_id,n.name,v.tc_external_id FROM req_coverage c JOIN requirements r ON r.id=c.req_id "
              f"JOIN req_specs s ON s.id=r.srs_id JOIN nodes_hierarchy n ON n.id=c.testcase_id "
              f"JOIN tcversions v ON v.id=c.tcversion_id WHERE s.testproject_id={pid} AND r.req_doc_id LIKE 'REQ-{data.LETTER}-%' "
              f"AND c.is_active=1 ORDER BY r.req_doc_id,v.tc_external_id")
    stable_id=lambda name: re.match(r'TC-[A-Z]-[0-9]{3}',name).group(0)
    actual={(r,stable_id(n)) for r,n,_ in links}
    expected={(rid,c['id']) for c in cases for rid in c['reqs']}
    assert actual==expected, f'Actual DB coverage differs: missing {expected-actual}, extra {actual-expected}'
    out=ROOT/'qa/project1'/name
    out.mkdir(parents=True,exist_ok=True)
    with (out/'traceability.csv').open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n'); writer.writerow(['Requirement','Stable case ID','TestLink external ID'])
        writer.writerows((r,stable_id(n),f'{PREFIX}-{ext}') for r,n,ext in links)
    result.update({'database_cases':len(rows),'database_steps':sum(int(r[4]) for r in rows),
                   'database_requirement_links':len(links),'actual_db_mapping_matches_design':True,
                   'all_cases_authored_by':data.AUTHOR,'all_cases_in_plan':True,
                   'execution_results_total':int(sql('SELECT COUNT(*) FROM executions')[0][0])})
    (out/'quality.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    for name in sys.argv[1:]: audit(name)
