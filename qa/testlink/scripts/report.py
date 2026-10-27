"""Print a tester's TestLink deliverables (or the whole group's) to PDF + XML.

Usage: python3 -I qa/testlink/scripts/report.py <name>   -> qa/project1/<name>/
       python3 -I qa/testlink/scripts/report.py all      -> qa/project1/final/
Needs Google Chrome (headless print to PDF).
"""
import http.cookiejar
import importlib
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import BASE, PREFIX, PROJECT

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
NAME = sys.argv[1].lower()
OUT = os.path.join(os.path.dirname(KIT), "project1", "final" if NAME == "all" else NAME)


def sql(q):
    out = subprocess.run(["docker", "compose", "exec", "-T", "db", "mariadb", "-uroot", "-proot", "-N", "testlink",
                          "-e", q], cwd=KIT, capture_output=True, text=True, check=True).stdout
    return [line.split("\t") for line in out.strip().splitlines() if line]


web = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))


def get(path, data=None):
    return web.open(BASE + path, urllib.parse.urlencode(data).encode() if data else None).read().decode("utf-8", "replace")


def csrf(page):
    return dict(re.findall(r"name='(CSRF\w+)' value='([^']+)'", page))


user = "admin" if NAME == "all" else NAME
get("/login.php?viewer=", {**csrf(get("/login.php")), "reqURI": "", "destination": "", "tl_login": user, "tl_password": user})
PID = sql(f"SELECT id FROM testprojects WHERE prefix='{PREFIX}'")[0][0]
get(f"/lib/general/navBar.php?testproject={PID}")


def printed(query):
    html = get(f"/lib/results/printDocument.php?{query}&format=0&allOptionsOn=1")
    if "Table Of Contents" not in html and "<h1" not in html:
        sys.exit(f"TestLink did not return the document ({query}) - is the login '{user}' correct?")
    css = '''<style>@page { size: A4; margin: 15mm;
      @bottom-right { content: counter(page) " / " counter(pages); font: 8pt Arial; color: #555; }
      @bottom-left { content: "SECJ3343 - TaskFlow - Project 1"; font: 8pt Arial; color: #555; }
    }
    @media print {
      body { font-size: 10pt; padding: 0; }
      table { max-width: 100%; table-layout: fixed; }
      table.tc, table.req, table.req_spec { width: 100%; break-inside: avoid; }
      table.tc td, table.tc th, table.req td, table.req th, table.req_spec td, table.req_spec th { font-size: 9pt !important; }
      td, th, p { overflow-wrap: anywhere; word-break: break-word; }
      tr { break-inside: avoid; } pre { white-space: pre-wrap; }
      table.req { margin-left: 0; }
    }</style>'''
    html = re.sub(r'(<table\b[^>]*class="tc"[^>]*>)',
                  r'\1<colgroup><col style="width:12%"><col style="width:44%"><col style="width:44%"></colgroup>', html)
    # Stable IDs must remain copyable and unbroken in related-case cells.
    html = re.sub(r'\b((?:TC|REQ)-[A-E]-[0-9]{3})\b',
                  r'<span style="white-space:nowrap">\1</span>', html)
    return html.replace("<head>", f'<head><base href="{BASE}/lib/results/">', 1).replace('</head>', css+'</head>')


def pdf(html, filename):
    src = os.path.join(OUT, ".print.html")
    open(src, "w").write(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--user-data-dir=" + os.path.join(OUT, '.chrome-profile'),
                    f"--print-to-pdf={os.path.join(OUT, filename)}", "file://" + src], capture_output=True, check=True)
    os.remove(src)
    print("wrote", os.path.join(OUT, filename))


os.makedirs(OUT, exist_ok=True)
if NAME == "all":
    pdf(printed(f"type=testspec&level=testproject&id={PID}"), f"{PROJECT}_TestLink_Test_Case_Report.pdf")
    pdf(printed(f"type=reqspec&level=testproject&id={PID}"), f"{PROJECT}_Test_Basis_Requirements.pdf")
    sys.exit()

data = importlib.import_module(f"{NAME}_testdata")
cap = NAME.capitalize()
top = sql(f"SELECT id FROM nodes_hierarchy WHERE node_type_id=2 AND parent_id={PID} AND name='{data.TOP_SUITE}'")
if not top:
    sys.exit(f"suite '{data.TOP_SUITE}' not in TestLink - run load.py {NAME} first")
SUITE = top[0][0]
if '--basis-only' not in sys.argv:
    pdf(printed(f"type=testspec&level=testsuite&id={SUITE}"), f"{cap}_TestLink_Test_Case_Report.pdf")

# test basis: this tester's requirement specs only, one document
docs = [printed(f"type=reqspec&level=reqspec&id={sid}")
        for (sid,) in [sql(f"SELECT id FROM req_specs WHERE doc_id='{s['doc_id']}'")[0] for s in data.REQ_SPECS]]
body = lambda h: h.split("<body", 1)[1].split(">", 1)[1].rsplit("</body>", 1)[0]  # noqa: E731
pdf(docs[0].rsplit("</body>", 1)[0] + "".join('<div style="break-before:page"></div>'+body(d) for d in docs[1:]) + "</body></html>",
    f"{cap}_Test_Basis_Requirements.pdf")
if '--basis-only' in sys.argv:
    sys.exit()

page = get(f"/lib/testcases/tcExport.php?containerID={SUITE}&tproject_id={PID}&useRecursion=1")
xml = get("/lib/testcases/tcExport.php", {
    **csrf(page), "containerID": SUITE, "tproject_id": PID, "useRecursion": 1, "exportType": "XML",
    "export_filename": f"{NAME}.xml", "exportReqs": 1, "exportKeywords": 1, "exportCFields": 1,
    "exportTCSummary": 1, "exportTCPreconditions": 1, "exportTCSteps": 1, "export": "Export"})
open(os.path.join(OUT, f"{NAME}-testsuites.xml"), "w").write(xml.replace(']]></details> \n', ']]></details>\n'))
print("wrote", os.path.join(OUT, f"{NAME}-testsuites.xml"), xml.count("<testcase "), "test cases")
