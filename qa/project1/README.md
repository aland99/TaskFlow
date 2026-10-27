# SECJ3343 Project 1 - Test Case Design: TaskFlow

Final group integration completed on 27 October 2026: 203 cases, 63 requirements, 100% mapped. See GROUP_REVIEW.md and final/. Actual original-prompt submissions assign Mhamad to B and Lanya to C.

Group: **TaskFlow**. Leader: **Aland Karwan**. Five members. Due **27 October 2026** (Asia/Baghdad).
Repository: https://github.com/aland99/TaskFlow. Source baseline: **main@5133a6c**.

## Assignment and lecturer instructions

Derive test cases in TestLink for the selected software. Submit (1) the **TestLink-generated test case report PDF** and (2) the **test basis**. Retain XML exports and a bidirectional requirements traceability matrix for checking/import.

Read locally: `~/Downloads/Project 1.pptx` (slides 2-7) and `~/Downloads/Testlink - Tutorial.pptx` (all 40 slides).
Project 1 slide 3 explicitly says **DO NOT create a new project** because the lecturer already created each group's project and assigned roles. The Docker instance here is a **local preparation environment only**. Its empty database needs a local TaskFlow project. On the lecturer's server, select the existing assigned project and import the requirements/testsuites XML into it, using the existing roles. No lecturer URL or account has been provided. Local PDFs alone do not prove work exists in that server.

Rubric: accurately applied techniques 20; comprehensive feature/edge/negative coverage 40; explicit accurate bidirectional requirements traceability 20; setup/data/clear steps 10; visible progress and teamwork 10. Each member authors their own area under their own Git/TestLink identity. Do not claim teammate contribution, execution or passing results before it happens.

## Software and test basis

TaskFlow is a single-user React/Vite SPA. No application accounts, backend, HTTP API routes or database exist. Persistence is a JSON task array in `localStorage.taskflow_tasks`, with backup `taskflow_tasks_backup`. The authoritative existing source document is root `README.md`, including TF-REQ-001 through TF-REQ-019 and additional behavior/storage notes. Code-derived requirements supplement it for features not assigned an original TF-REQ number. Cite both README sections and implementation paths; distinguish existing documented requirements from code-derived behavior. Never invent authentication, numeric limits or messages.

Inventory and ownership below covers all testable components/utilities. Code paths shared by multiple members are assigned by behavior, not by whole file. Reusing a fixture action is allowed; do not retest another member's owned assertion.

| Slot | Author / IDs | Exclusive assertions | Main sources |
|---|---|---|---|
| 1 / A | Aland Karwan (`aland`); `SRS-A-*`, `REQ-A-*`, `TS-A1...`, `TC-A-001...` | Create; title/description validation, Unicode and counters; defaults only; cancel/reopen; inline errors/focus; literal text; duplicate-title identity; first-task entry | README TF-REQ-001/002/003/007/008 and defaults only of 004/005/006; TaskFormModal, Modal, validation, buildTask |
| 2 / B | Mhamad (`mhammedazad`); B IDs | Prefilled edit, valid/invalid edits and preservation of id/createdAt; updatedAt; editing cancellation paths; priority edit persistence (not filter semantics); delete confirmation, confirm/cancel and closing paths; deleting only intended task; repeat operations | README TF-REQ-009-015/018; App updateTask/deleteTask; TaskFormModal; ConfirmDeleteModal; Modal |
| 3 / C | Lanya Faraidun (`lanya`); C IDs | All priority/status enum partitions including tampering through unit harness; list status transitions (all six distinct directed transitions plus same-state behavior); summary totals; Completed styling/exemption; optional/valid/invalid dates; leap years and today/yesterday/tomorrow, local date boundaries, date formatting | README TF-REQ-004/005/006/016/017; dates.js, validation.js, SummaryCards, TaskCard, App changeStatus |
| 4 / D | Ahmed (`ahmed`); D IDs | Shared title/description substring search, case/trim, both search boxes; status/priority filters, AND decision table; four sorts, ties/no due date; result singular/plural; filtered/search empty-state precedence; Clear search vs Clear filters vs toolbar Clear Filters | README TF-REQ-019 and Behaviour notes; tasks.filterAndSortTasks; TaskToolbar, TopBar, TaskList; App clearFilters |
| 5 / E | Rasan (`rasan`); E IDs | Normal reload persistence; missing/corrupt/non-array storage, backup and reset; invalid/duplicate-entry recovery, timestamps fallback, storage read/write failure; banners and dismissal; navigation and page title; desktop collapse/mobile drawer around 767/768px; dialog naming/autofocus/restoration; toast dismissal/timing/error role | README Storage/Behaviour/Exact messages; storage.js; StorageBanner, Sidebar, TopBar, Toast, Modal, App.css |

Aim for **30-45 meaningful cases per member**, adjusted for actual feature complexity. Boundary tests use min-1/min/min+1/max-1/max/max+1 where a limit exists; optional text min 0 has no meaningful -1 length. Decision tables state conditions and expected action. State tests name source and destination states. Unit-harness tests must be labelled as such when invalid enum/date inputs cannot be entered through native controls. Keep setup isolated in a disposable Chrome profile.

## Local prerequisites and start

Install git, GitHub CLI, Docker Desktop, Python 3, Google Chrome and Poppler. On macOS:

```bash
brew install git gh python poppler
brew install --cask docker-desktop google-chrome
gh auth status  # if necessary, the human completes gh auth login
open -a Docker
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
bash qa/testlink/setup.sh
```

TestLink: http://localhost:8090, **admin/admin**. Member accounts: **aland/aland**, **lanya/lanya**, **mhammedazad/mhammedazad**, **ahmed/ahmed**, **rasan/rasan** after setup. Local practice passwords only. The loader also creates the submitting member's lowercase first-name account and grants it senior tester on the local project; password is that login. Each known roster member gets role_id 6 on the project. Real names are resolved from member data modules for report headers.

If 8090 is occupied, select a free port and set `export TESTLINK_PORT=8091` consistently for setup/load/report. Docker binds only to 127.0.0.1. The compose project `taskflow-project1-20261026` has its own volume. Never delete unrelated volumes. `seed/` contains only the three clean upstream SQL files, generated after TestLink clone, removing `/*prefix*/` and replacing `YOUR_TL_DBNAME` with `testlink`. There is no other group's project/test seed.

```bash
npm install
npm test
npm run build
npm run dev -- --host 127.0.0.1  # http://localhost:5173
```

If npm omitted a native optional dependency, install the package matching the installed `rolldown` version and your platform (`@rolldown/binding-darwin-x64` on Intel Mac) with `--no-save --package-lock=false`. Preserve unrelated local changes.

## Member workflow

Copy your prompt from TEAM_PROMPTS.md. Fork this public repository with `gh repo fork aland99/TaskFlow --clone`, clone/work in your own fork, create `codex/project1-member-<letter>`, and read this README plus your scope's code.

Author `qa/testlink/scripts/<lowercase-first-name>_testdata.py`. Use **aland_testdata.py for structure and quality only**. Include `AUTHOR`, `FULL_NAME`, `LETTER`, `TOP_SUITE`, `TOP_SUITE_DETAILS`, `REQ_SPECS`, `SUITES`. Each case: globally stable `TC-<letter>-NNN` `id`, name starting with that id, explicit technique, requirement refs, concrete preconditions, numbered action/expected-result tuples and importance (1/2/3). Each requirement tuple contains id/title/description, exact rule and message plus README and code citations. TestLink assigns additional TF-N external ids; stable TC names remain portable across imports.

```bash
python3 -I qa/testlink/scripts/validate.py <name>
python3 -I qa/testlink/scripts/load.py <name>
python3 -I qa/testlink/scripts/report.py <name>
```

Open both PDFs in `qa/project1/<name>/`. Check first/middle/last pages, long data, steps, headers and requirement coverage. Reports must come from TestLink's printDocument.php, logged-in cookie session after selecting the project. Requirements use CSRF web-form import because this version lacks requirement-creation API. Keep the patched overlay.

Loader resumes existing suites and updates cases by exact stable name, then refreshes their requirement links. Re-running is safe for an interrupted import. Keep stable names when revising; renamed/removed cases require export/back up and removal of only those old cases in your own local suite. Requirement descriptions update on each load. Do not destroy another tester's work. TestLink cases are manual/Not Run; Project 1 is design, not fabricated execution evidence.

Commit only your data module and `qa/project1/<name>/` PDFs, XML and quality evidence. Push your own fork and open a PR to `aland99/TaskFlow:main`. No collaborator invitation is needed. Each person should review/own their design and PR. Do not alter shared team tooling or another member's files without agreement.

## Deliverables and progress

Per member: `<Name>_TestLink_Test_Case_Report.pdf`, `<Name>_Test_Basis_Requirements.pdf`, `<name>-requirements.xml`, `<name>-testsuites.xml`, quality/coverage notes. `validate.py all` checks every member and duplicate letters/authors before combined loading.

| Slot | Current design | Review evidence |
|---|---|---|
| A | 43 designed cases, 14 requirements, 3 suites, 14/14 covered structurally | See aland/QUALITY.md; TestLink/PDF verification recorded there when actually completed |
| B-E | All four authored PRs merged; all 203 group cases/63 requirements integrated | See GROUP_REVIEW.md and final/group-audit.json; no execution results claimed |

When all four PRs are open, tell the leader's agent **members are done**. It will inspect and merge member PRs, validate all IDs/coverage, load all members, order suites A-E, generate combined TestLink case/basis PDFs and a matrix from the actual `req_coverage` table, and package the final submission with individual PDFs, XML exports and source documents as PDFs. The final zip will be `~/Downloads/SECJ3343_Project1_Group_TaskFlow.zip`.

Before submitting: verify the roster names (Aland Karwan, Lanya, Mhamad, Ahmed, Rasan), ensure each tester's own authorship is visible, import exports into the lecturer's **existing assigned project**, verify that server's project prefix/mappings, and submit the required PDFs/test basis through the course's stated submission channel. The agent has no submission-channel access in this task.


## Final submission package (27 October 2026)

All four member PRs (#1-#4) are merged. Actual original-prompt assignments are Mhamad B, Lanya C, Ahmed D and Rasan E. Final totals: **203 cases, 63 requirements, 17 suites, 515 steps, 361 actual coverage links, 100% mapped**. Every case is assigned to its own author; no executions are claimed.

The complete package is `final/SECJ3343_Project1_Group_TaskFlow/`; the downloadable zip is `~/Downloads/SECJ3343_Project1_Group_TaskFlow.zip`. It contains three combined PDFs, ten individual PDFs, ten XML files, source PDFs, README and verification records. See GROUP_REVIEW.md for scoped review corrections and identity reconciliation.

| Member | Cases | Requirements |
|---|---:|---:|
| Aland Karwan | 43 | 14 |
| Mhamad | 41 | 14 |
| Lanya Faraidun | 41 | 8 |
| Ahmed | 40 | 14 |
| Rasan soran | 38 | 13 |

The final native TestLink case report is 205 pages; requirements basis 37 pages; database-derived bidirectional matrix 16 pages. All 13 generated PDFs passed inventories/geometry and rendered-page review; exported step content and requirement links match the reviewed design.

To reproduce after loading all members: `python3 -I qa/testlink/scripts/group_submission.py audit` (requires reportlab), then run report.py for each author and all, verify_submission.py (requires pypdf/pdfplumber/Poppler), visually review rendered samples, and `group_submission.py package --zip <absolute-output.zip>`. Use the Codex bundled Python runtime for PDF dependencies when available.
