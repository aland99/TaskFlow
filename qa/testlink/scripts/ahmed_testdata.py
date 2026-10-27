"""Member D search, filter, sorting and list feedback design. Manual cases; no results claimed."""
AUTHOR = 'ahmed'
FULL_NAME = 'AhmedAzad240358'
LETTER = 'D'
TOP_SUITE = 'D - AhmedAzad240358 - Search filters and sorting'
TOP_SUITE_DETAILS = (
    '<p>Member 4 / D, baseline TaskFlow main@5133a6c. Test basis: README.md TF-REQ-019 and Behaviour notes. '
    'Code: src/utils/tasks.js filterAndSortTasks/SORT_OPTIONS; src/components/TaskToolbar.jsx, TopBar.jsx, '
    'TaskList.jsx; src/App.jsx clearFilters.</p>'
    '<p>Fixture CORE installed afresh before each independent case in a disposable Chrome profile through '
    'DevTools Console/localStorage taskflow_tasks, then location.reload(): six records, IDs d1-d6. '
    'd1: Alpha Planning | Build the billing dashboard | High | To Do | due 2026-11-30 | created 2026-01-10T08:00:00Z. '
    'd2: Alpha Support | Reconcile monthly billing | High | In Progress | due 2026-11-20 | created 2026-01-10T10:00:00Z. '
    'd3: Beta Launch | Prepare user notes | Medium | To Do | due 2026-11-20 | created 2026-01-05T09:00:00Z. '
    'd4: Gamma Review | Alpha appears in notes | Low | Completed | no due date | created 2026-01-15T08:00:00Z. '
    'd5: Alpha-100% (urgent) | Review [QA]? | Low | In Progress | due 2027-02-01 | created 2026-01-15T12:00:00Z. '
    'd6: Undated Later | No deadline | Medium | Completed | no due date | created 2026-01-20T08:00:00Z. '
    'For each record updatedAt equals createdAt; dueDate without a date is empty string. The explicit one-record '
    'and zero-record exceptions are stated in their case preconditions.</p>'
    '<p>Reset taskflow_tasks and taskflow_tasks_backup before each case; fixture creation is setup only. '
    'Open http://localhost:5173, use Dashboard, and do not use UI CRUD as an assertion. Sort labels are '
    'Newest first, Oldest first, Due date: soonest, Due date: latest. Cases are manual and initially Not Run.</p>'
)

def req(rid, title, rule, source):
    return (rid, title, rule + ' Source: README.md (TF-REQ-019 / Behaviour notes / Exact messages); '
            + source + '; baseline main@5133a6c.')

REQ_SPECS = [{
    'doc_id': 'SRS-D-SEARCH-FILTER-SORT',
    'title': 'Search, filters, sorting and result feedback',
    'scope': 'Member 4 / D only. README.md TF-REQ-019 and Behaviour notes; code-derived details in '
             'src/utils/tasks.js, src/components/TaskToolbar.jsx, TopBar.jsx, TaskList.jsx, and src/App.jsx. '
             'Fixture setup is not an assertion about CRUD, storage, status transitions, summary counts, or navigation.',
    'reqs': [
        req('REQ-D-001','Trimmed case-insensitive title substring',
            'A nonblank trimmed query shall match a case-insensitive substring of title.',
            'src/utils/tasks.js filterAndSortTasks'),
        req('REQ-D-002','Description substring and title-or-description',
            'A nonblank query shall match a case-insensitive substring in description or title; either field is sufficient.',
            'src/utils/tasks.js filterAndSortTasks'),
        req('REQ-D-003','Blank query and literal punctuation',
            'A query that becomes empty after trim shall not restrict results. Punctuation is literal substring data; no query length limit is specified.',
            'src/utils/tasks.js filterAndSortTasks'),
        req('REQ-D-004','Synchronized search boxes',
            'TopBar and TaskToolbar inputs shall share the same controlled query; typing in either changes the other input and visible results.',
            'src/App.jsx search state; src/components/TopBar.jsx; src/components/TaskToolbar.jsx'),
        req('REQ-D-005','Status filter partitions',
            'All Statuses includes all tasks; To Do, In Progress, and Completed include tasks of only the selected status.',
            'src/components/TaskToolbar.jsx; src/utils/tasks.js filterAndSortTasks'),
        req('REQ-D-006','Priority filter partitions',
            'All Priorities includes all tasks; Low, Medium, and High include tasks of only the selected priority.',
            'src/components/TaskToolbar.jsx; src/utils/tasks.js filterAndSortTasks'),
        req('REQ-D-007','Search/status/priority AND decision table',
            'Visible tasks satisfy status AND priority AND query; query condition is title OR description match.',
            'README.md TF-REQ-019 / Behaviour notes; src/utils/tasks.js filterAndSortTasks'),
        req('REQ-D-008','Four sorts and newest default',
            'Newest first is the default; choices are Newest first, Oldest first, Due date: soonest, and Due date: latest.',
            'src/utils/tasks.js SORT_OPTIONS/filterAndSortTasks; src/components/TaskToolbar.jsx; src/App.jsx'),
        req('REQ-D-009','Creation order and due-date tie order',
            'Newest orders createdAt descending; Oldest orders createdAt ascending. Tasks with equal due dates are ordered by newest createdAt first.',
            'src/utils/tasks.js filterAndSortTasks comparators/byDueDate'),
        req('REQ-D-010','Undated-last behavior',
            'Due-date sorts place every dated task before undated tasks; undated tasks are ordered newest createdAt first.',
            'README.md Behaviour notes; src/utils/tasks.js filterAndSortTasks byDueDate'),
        req('REQ-D-011','Singular and plural result counts',
            'When results exist, display Showing <visible> of <total> task for total 1 and Showing <visible> of <total> tasks otherwise; total counts all tasks before filters.',
            'src/components/TaskList.jsx result-count'),
        req('REQ-D-012','No-result message precedence and actions',
            'With zero total tasks show No tasks yet / Tasks you create will appear here. / Create your first task. Otherwise zero results with nonblank trimmed search show No tasks match "<query>" / Try a different search term. / Clear search. With blank search show No tasks match the current filters / Try changing or clearing your filters. / Clear filters.',
            'README.md Exact messages / Empty states; src/components/TaskList.jsx'),
        req('REQ-D-013','Clear search preserves filters and sort',
            'The search empty-state Clear search action clears only search and preserves status, priority, and sort.',
            'src/components/TaskList.jsx onClearSearch; src/App.jsx setSearch'),
        req('REQ-D-014','Both Clear Filters actions reset all controls',
            'Toolbar Clear Filters and filter-empty-state Clear filters clear search, set status and priority to All, and restore newest sort.',
            'src/App.jsx clearFilters; src/components/TaskToolbar.jsx; src/components/TaskList.jsx onClearFilters'),
    ],
}]

def c(n, title, tech, reqs, steps, extra='', importance=2):
    base = 'Independent setup: clear both TaskFlow storage keys and reload the app. '
    pre = base + (extra if extra else
                  'Install the full six-record CORE fixture defined in TOP_SUITE_DETAILS and confirm six fixture cards.')
    return {'id':f'TC-D-{n:03d}', 'name':f'TC-D-{n:03d} {title}', 'technique':tech,
            'reqs':reqs.split(), 'pre':pre, 'steps':steps, 'importance':importance}

S1 = [
 c(1,'Empty query shows all tasks','EP - empty query partition','REQ-D-003 REQ-D-011',[
  ('Leave both search inputs empty.','All six cards appear; text reads "Showing 6 of 6 tasks".')]),
 c(2,'Whitespace-only query is blank after trimming','EP - whitespace query partition','REQ-D-001 REQ-D-003',[
  ('Enter three spaces in toolbar "Search".','TopBar "Search tasks" also contains three spaces; all six cards remain visible.'),
  ('Inspect result text.','It reads "Showing 6 of 6 tasks"; no empty state appears.')]),
 c(3,'Case-insensitive title substring','EP - title substring partition','REQ-D-001',[
  ('Enter "pLaNn" in toolbar "Search".','Only "Alpha Planning" is visible.')]),
 c(4,'Description-only substring','EP - description partition','REQ-D-002',[
  ('Enter "dashboard" in "Search".','Only "Alpha Planning" is visible because dashboard occurs in its description.')]),
 c(5,'Title OR description returns each match once','Decision Table - title OR description','REQ-D-001 REQ-D-002 REQ-D-007 REQ-D-011',[
  ('Enter "billing" in "Search".','"Alpha Planning" and "Alpha Support" appear once each.'),
  ('Inspect result text.','It reads "Showing 2 of 6 tasks".')],importance=1),
 c(6,'Case-insensitive description substring','EP - case partition in description','REQ-D-002',[
  ('Enter "RECONCILE MONTHLY" in "Search".','Only "Alpha Support" appears.')]),
 c(7,'Nonmatch displays exact search empty state','EP - no-match partition','REQ-D-003 REQ-D-012',[
  ('Enter "  Qzx-No-Task  " in "Search".','The title reads "No tasks match \\"Qzx-No-Task\\""; text reads "Try a different search term."; button reads "Clear search".')],importance=1),
 c(8,'Percent and parentheses are literal search characters','Error Guessing - punctuation','REQ-D-002 REQ-D-003',[
  ('Enter "100% (urgent)" in "Search".','Only "Alpha-100% (urgent)" appears; punctuation is matched literally.')]),
 c(9,'Square bracket and question mark are literal','Error Guessing - regex-like punctuation','REQ-D-002 REQ-D-003',[
  ('Enter "[QA]?" in "Search".','Only "Alpha-100% (urgent)" appears from description "Review [QA]?".')]),
 c(10,'TopBar search synchronizes toolbar value and results','State Transition - TopBar query','REQ-D-001 REQ-D-004',[
  ('Enter "support" in TopBar input aria-label "Search tasks".','Toolbar "Search" reads "support"; only "Alpha Support" appears.')]),
 c(11,'Toolbar search synchronizes TopBar value and results','State Transition - toolbar query','REQ-D-001 REQ-D-004',[
  ('Enter "launch" in toolbar "Search".','TopBar "Search tasks" reads "launch"; only "Beta Launch" appears.')]),
 c(12,'One visible among six uses plural total wording','EP - one visible among many total','REQ-D-011',[
  ('Enter "dashboard" in "Search".','One card appears; text reads "Showing 1 of 6 tasks".')]),
 c(13,'Several visible tasks use plural total wording','EP - many visible partition','REQ-D-001 REQ-D-002 REQ-D-011',[
  ('Enter "alpha" in "Search".','"Alpha Planning", "Alpha Support", "Alpha-100% (urgent)", and "Gamma Review" appear; text reads "Showing 4 of 6 tasks".')]),
 c(14,'Single-task total uses singular wording','EP - total count one','REQ-D-011',[
  ('Inspect the Dashboard list after reload.','One card appears; text reads "Showing 1 of 1 task".')],
  'Use only one valid task record: id d1, title "Alpha Planning", description "Build dashboard", priority High, status To Do, dueDate "2026-11-30", createdAt and updatedAt "2026-01-10T08:00:00.000Z". Store it as the sole array item in taskflow_tasks and reload.'),
]

S2 = [
 c(15,'To Do status partition','EP - status partition To Do','REQ-D-005 REQ-D-011',[
  ('Choose "To Do" from "Status".','Only "Alpha Planning" and "Beta Launch" appear; text reads "Showing 2 of 6 tasks".')]),
 c(16,'In Progress status partition','EP - status partition In Progress','REQ-D-005',[
  ('Choose "In Progress" from "Status".','Only "Alpha Support" and "Alpha-100% (urgent)" appear.')]),
 c(17,'Completed status partition','EP - status partition Completed','REQ-D-005',[
  ('Choose "Completed" from "Status".','Only "Gamma Review" and "Undated Later" appear.')]),
 c(18,'High priority partition','EP - priority partition High','REQ-D-006',[
  ('Choose "High" from "Priority".','Only "Alpha Planning" and "Alpha Support" appear.')]),
 c(19,'Medium priority partition','EP - priority partition Medium','REQ-D-006',[
  ('Choose "Medium" from "Priority".','Only "Beta Launch" and "Undated Later" appear.')]),
 c(20,'Low priority partition','EP - priority partition Low','REQ-D-006',[
  ('Choose "Low" from "Priority".','Only "Gamma Review" and "Alpha-100% (urgent)" appear.')]),
 c(21,'Decision table: To Do AND each priority','Decision Table - To Do by priority','REQ-D-005 REQ-D-006 REQ-D-007 REQ-D-012',[
  ('Select Status "To Do" and Priority "High".','Only "Alpha Planning" appears.'),
  ('Keep Status "To Do"; select Priority "Medium".','Only "Beta Launch" appears.'),
  ('Keep Status "To Do"; select Priority "Low".','"No tasks match the current filters" and button "Clear filters" appear.')],importance=1),
 c(22,'Decision table: In Progress AND each priority','Decision Table - In Progress by priority','REQ-D-005 REQ-D-006 REQ-D-007 REQ-D-012',[
  ('Select Status "In Progress" and Priority "High".','Only "Alpha Support" appears.'),
  ('Keep Status "In Progress"; select Priority "Medium".','"No tasks match the current filters" appears.'),
  ('Keep Status "In Progress"; select Priority "Low".','Only "Alpha-100% (urgent)" appears.')],importance=1),
 c(23,'Decision table: Completed AND each priority','Decision Table - Completed by priority','REQ-D-005 REQ-D-006 REQ-D-007 REQ-D-012',[
  ('Select Status "Completed" and Priority "High".','"No tasks match the current filters" appears.'),
  ('Keep Status "Completed"; select Priority "Medium".','Only "Undated Later" appears.'),
  ('Keep Status "Completed"; select Priority "Low".','Only "Gamma Review" appears.')],importance=1),
 c(24,'Decision table: query AND status AND priority','Decision Table - query/status/priority AND','REQ-D-001 REQ-D-002 REQ-D-005 REQ-D-006 REQ-D-007 REQ-D-012',[
  ('Enter "billing", choose Status "In Progress", Priority "High".','Only "Alpha Support" appears; it meets all three conditions.'),
  ('Keep query and status; select Priority "Low".','"No tasks match the current filters" appears; no task satisfies all three.'),
  ('Keep query "billing"; set Status "To Do" and Priority "High".','"No tasks match the current filters" appears.')],importance=1),
]

S3 = [
 c(25,'Newest first is default and orders creation newest first','EP - default sort','REQ-D-008 REQ-D-009',[
  ('Reload CORE without changing "Sort by".','"Newest first" is selected; order: "Undated Later", "Alpha-100% (urgent)", "Gamma Review", "Alpha Support", "Alpha Planning", "Beta Launch".')]),
 c(26,'Oldest first orders creation oldest first','EP - Oldest sort','REQ-D-008 REQ-D-009',[
  ('Choose "Oldest first" from "Sort by".','Order: "Beta Launch", "Alpha Planning", "Alpha Support", "Gamma Review", "Alpha-100% (urgent)", "Undated Later".')]),
 c(27,'Due soonest orders dates and ties then undated last','BVA - equal due dates and blank boundary','REQ-D-008 REQ-D-009 REQ-D-010',[
  ('Choose "Due date: soonest".','Order: "Alpha Support", "Beta Launch", "Alpha Planning", "Alpha-100% (urgent)", "Undated Later", "Gamma Review".'),
  ('Inspect the 2026-11-20 tie and undated pair.','Newer "Alpha Support" precedes "Beta Launch"; undated tasks are last, newest "Undated Later" before "Gamma Review".')],importance=1),
 c(28,'Due latest reverses date order and keeps tie/blank rules','BVA - latest date and blank boundary','REQ-D-008 REQ-D-009 REQ-D-010',[
  ('Choose "Due date: latest".','Order: "Alpha-100% (urgent)", "Alpha Planning", "Alpha Support", "Beta Launch", "Undated Later", "Gamma Review".'),
  ('Inspect tied and undated tasks.','For 2026-11-20, newer "Alpha Support" precedes "Beta Launch"; undated tasks are last and newest first.')],importance=1),
 c(29,'Soonest sort places both undated tasks last','BVA - empty due-date partition','REQ-D-010',[
  ('Choose "Due date: soonest".','The last two cards are "Undated Later", then "Gamma Review"; all dated tasks precede them.')]),
 c(30,'Latest sort places both undated tasks last','BVA - empty due-date partition','REQ-D-010',[
  ('Choose "Due date: latest".','The last two cards are "Undated Later", then "Gamma Review"; all dated tasks precede them.')]),
]

S4 = [
 c(31,'Search empty state echoes trimmed query','EP - search empty-state partition','REQ-D-003 REQ-D-012',[
  ('Enter "  Missing task  " in "Search".','Title reads "No tasks match \\"Missing task\\""; text reads "Try a different search term."; button reads "Clear search".')]),
 c(32,'Blank query and no matching filters show filter empty state','EP - filter empty-state partition','REQ-D-005 REQ-D-006 REQ-D-012',[
  ('Leave search blank; select Status "To Do" and Priority "Low".','Title reads "No tasks match the current filters"; text reads "Try changing or clearing your filters."; button reads "Clear filters".')]),
 c(33,'Search no-hit takes precedence over filter no-hit','Decision Table - search-empty precedence','REQ-D-007 REQ-D-012',[
  ('Enter "NoSuchTask" and choose Status "Completed", Priority "High".','Title reads "No tasks match \\"NoSuchTask\\""; button reads "Clear search"; filter empty-state title is absent.')],importance=1),
 c(34,'Zero total tasks takes precedence over query and filters','Decision Table - zero total tasks','REQ-D-012',[
  ('Enter "Missing" in "Search" and select Status "Completed".','The list shows "No tasks yet", "Tasks you create will appear here.", and button "Create your first task".')],
  'Use an empty task array instead of CORE: set taskflow_tasks to [] and remove taskflow_tasks_backup before reload; verify there are zero task records.'),
 c(35,'Clear search preserves status priority and sort','State Transition - search-empty to cleared','REQ-D-013',[
  ('Set Status "In Progress", Priority "Low", Sort by "Due date: latest"; search "NoSuchTask".','Search empty state shows button "Clear search".'),
  ('Click "Clear search".','Both search inputs are empty; Status remains "In Progress", Priority "Low", Sort by "Due date: latest"; "Alpha-100% (urgent)" appears.')],importance=1),
 c(36,'Empty-state Clear filters restores all defaults','State Transition - filter-empty to defaults','REQ-D-014',[
  ('Leave search blank; set Status "To Do", Priority "Low", Sort by "Due date: latest".','Filter empty state shows button "Clear filters".'),
  ('Click "Clear filters".','Both search inputs empty; Status "All Statuses", Priority "All Priorities", Sort by "Newest first"; all six cards return newest first.')],importance=1),
 c(37,'Toolbar Clear Filters resets synchronized controls and sort','State Transition - controls to defaults','REQ-D-004 REQ-D-014',[
  ('Search "billing" in TopBar; set Status "In Progress", Priority "High", Sort by "Due date: latest".','Toolbar Search also reads "billing"; controls show the chosen values.'),
  ('Click toolbar button "Clear Filters".','Both search inputs are empty; Status "All Statuses", Priority "All Priorities", Sort by "Newest first"; all six cards appear.')],importance=1),
 c(38,'Toolbar Clear Filters resets sort alone','State Transition - chosen sort to default','REQ-D-008 REQ-D-014',[
  ('Choose "Oldest first"; click toolbar "Clear Filters".','"Newest first" is selected and cards return to newest-first order.')]),
 c(39,'Toolbar Clear Filters clears a matching query','State Transition - matching query to defaults','REQ-D-004 REQ-D-014',[
  ('Search "billing"; click toolbar "Clear Filters".','Both search inputs become empty; all six cards appear; text reads "Showing 6 of 6 tasks".')]),
 c(40,'Search and filter clear actions act in sequence','State Transition - search-empty then filter-empty','REQ-D-004 REQ-D-014',[
  ('Enter "NoSuchTask"; set Status "To Do", Priority "Low", and Sort by "Due date: latest".','Search empty state shows button "Clear search".'),
  ('Click "Clear search".','Both search inputs are empty; Status remains "To Do", Priority remains "Low", Sort by remains "Due date: latest"; filter empty state now shows "Clear filters".'),
  ('Click empty-state "Clear filters".','Both search inputs remain empty; Status "All Statuses", Priority "All Priorities", Sort by "Newest first".')]),
]

SUITES = [
 {'name':'TS-D1 - Search and result feedback','details':'EP and error guessing for query boundaries, title/description match, shared inputs, literal punctuation, counts and no-hit feedback.','cases':S1},
 {'name':'TS-D2 - Status, priority and AND decision tables','details':'EP for status and priority partitions; decision tables cover every non-All status-by-priority cell and combined query/status/priority logic.','cases':S2},
 {'name':'TS-D3 - Sort orders and due-date boundaries','details':'EP for each sort and default; BVA for equal due dates, creation-time tie order and undated-last behavior in both date sorts.','cases':S3},
 {'name':'TS-D4 - Empty states and clearing behavior','details':'Decision-table empty-state precedence and state transitions for Clear search, toolbar Clear Filters and empty-state Clear filters.','cases':S4},
]

