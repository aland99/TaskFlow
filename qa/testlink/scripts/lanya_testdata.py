"""Member C test design: enums, transitions, summaries and calendar dates."""

AUTHOR = 'lanya'
FULL_NAME = 'Lanya Faraidun'
LETTER = 'C'
TOP_SUITE = 'C - Lanya Faraidun - Status, dates and counts'
TOP_SUITE_DETAILS = (
    '<p>Tester: Lanya Faraidun (Member 3, C). SECJ3343 Project 1, Group TaskFlow. '
    'Baseline: TaskFlow main@5133a6c. Scope: TF-REQ-004/005/006/016/017; '
    'priority and status partitions, list transitions, summary totals, Completed rendering, '
    'optional and valid/invalid due dates, calendar boundaries, overdue rules, local-day behavior, '
    'and date formatting. Requirements cite README.md and the implementing src/ paths. '
    'Reference local day: 2026-10-27, 12:00 Asia/Baghdad (UTC+03:00); date harnesses pass '
    'this value explicitly and do not depend on the wall clock. All cases are designed/manual '
    'and remain Not Run until actually executed.</p>'
)

REQ_SPECS = [
    {
        'doc_id': 'SRS-C-ENUM',
        'title': 'Priority, status transitions and task summaries',
        'scope': 'README.md TF-REQ-004, TF-REQ-005, TF-REQ-016 and TF-REQ-017. '
                 'Code-derived acceptance detail is cited to validation.js, TaskCard.jsx, '
                 'SummaryCards.jsx and App.jsx. No separate customer SRS exists.',
        'reqs': [
            ('REQ-C-001', 'Priority values and validation',
             'README.md TF-REQ-004 specifies Low, Medium and High. src/utils/validation.js PRIORITIES and validateTask accept exactly those case-sensitive strings; an invalid value returns "Please select a valid priority." The native select in src/components/TaskFormModal.jsx offers only the three valid options.'),
            ('REQ-C-002', 'Status values and validation',
             'README.md TF-REQ-005 specifies To Do, In Progress and Completed. src/utils/validation.js STATUSES and validateTask accept exactly those case-sensitive strings; an invalid value returns "Please select a valid status." The native selects in src/components/TaskFormModal.jsx and src/components/TaskCard.jsx offer only those options.'),
            ('REQ-C-003', 'Status change and summary totals',
             'README.md TF-REQ-016 requires status updates and status counts; Behaviour notes require summary cards to count all tasks regardless of search and filters. src/App.jsx changeStatus ignores unsupported values, persists an accepted status change and shows "Task status updated." src/components/SummaryCards.jsx counts tasks and each status from the complete tasks array.'),
            ('REQ-C-004', 'Completed task presentation',
             'README.md TF-REQ-017 gives Completed its own count and exempts it from overdue treatment. src/components/TaskCard.jsx adds class "completed" for Completed tasks, uses isOverdue for the Overdue badge/red date, and suppresses the Due today badge for Completed tasks; src/utils/dates.js isOverdue excludes status Completed.'),
        ],
    },
    {
        'doc_id': 'SRS-C-DATE',
        'title': 'Due dates, local calendar rules and formatting',
        'scope': 'README.md TF-REQ-006 plus its Behaviour notes on overdue dates. '
                 'Code-derived acceptance detail is cited to dates.js, validation.js, '
                 'TaskFormModal.jsx, TaskCard.jsx and TopBar.jsx. No separate customer SRS exists.',
        'reqs': [
            ('REQ-C-005', 'Optional due date and real calendar validation',
             'README.md TF-REQ-006 allows an optional due date stored as YYYY-MM-DD and Exact messages states "Please enter a valid date (YYYY-MM-DD)." for an invalid real date. src/utils/validation.js validateTask accepts undefined, null and empty string as absent and rejects any other value that is not a real calendar date per src/utils/dates.js isValidDateString. src/components/TaskFormModal.jsx uses a native input type=date, which sanitizes impossible values before application validation.'),
            ('REQ-C-006', 'Leap years and calendar boundaries',
             'README.md TF-REQ-006 requires a due date and the source date format is YYYY-MM-DD. src/utils/dates.js isValidDateString requires the exact four-two-two digit format, month 1-12, day >=1, month-specific maximum days and Gregorian leap-year rule (divisible by 4 except centuries unless divisible by 400). No separate application minimum/maximum year or due-date range is documented.'),
            ('REQ-C-007', 'Overdue and due-today decision',
             'README.md Behaviour notes define overdue as due date earlier than today (local date) AND status not Completed; today is not overdue and displays "Due today" for non-Completed tasks. src/utils/dates.js isOverdue and todayString implement the rule; src/components/TaskCard.jsx displays "Overdue" or "Due today" and colors overdue dates.'),
            ('REQ-C-008', 'Local calendar day and date display',
             'README.md TF-REQ-006 and Behaviour notes define due dates as local calendar days. src/utils/dates.js todayString uses local year/month/day, formatDueDate formats a YYYY-MM-DD value with en-US short month/day/year, and formatToday formats the supplied local Date as a weekday and full date. src/components/TaskCard.jsx renders "Due: <formatted date>" and src/components/TopBar.jsx renders the formatted current day.'),
        ],
    },
]

REFERENCE_DAY = '2026-10-27'
REFERENCE_TIME = '2026-10-27T12:00:00+03:00'
COMMON = (
    'Use a dedicated disposable Chrome profile on TaskFlow http://localhost:5173, baseline '
    'main@5133a6c. Use Asia/Baghdad (UTC+03:00) and fixed local reference '
    '2026-10-27 12:00; for date utility/harness checks pass "2026-10-27" explicitly or '
    'construct new Date(2026, 9, 27, 12, 0, 0) under TZ=Asia/Baghdad. Never use the current '
    'wall clock for a today/yesterday/tomorrow assertion. Clear only this profile’s '
    'taskflow_tasks/taskflow_tasks_backup before each independent UI fixture. Local storage is '
    'available. In unit-harness cases run node from the repository root and import the cited '
    'src/utils module; harness-only cases do not claim a UI execution. ')


def case(n, title, technique, reqs, steps, pre='', importance=2):
    cid = f'TC-C-{n:03d}'
    return {
        'id': cid,
        'name': cid + ' - ' + title,
        'technique': technique,
        'reqs': reqs.split(),
        'pre': COMMON + pre,
        'steps': steps,
        'importance': importance,
    }


enum_cases = []
for n, value in enumerate(('Low', 'Medium', 'High'), 1):
    enum_cases.append(case(n, f'Accepted priority partition: {value}',
        'EP - valid priority enumeration partition', 'REQ-C-001', [
            ('Open Edit Task for the fixture "Priority fixture" and inspect Priority.',
             'The Priority select contains exactly "Low", "Medium" and "High"; its current value is "Medium".'),
            (f'Select "{value}" and click Save Changes.',
             f'The dialog closes; the card shows the "{value}" priority badge; toast "Task updated successfully." appears; storage contains priority "{value}".'),
        ], pre='Fixture: one saved task titled Priority fixture, priority Medium, status To Do, dueDate empty.'))

for n, value in enumerate(('To Do', 'In Progress', 'Completed'), 4):
    enum_cases.append(case(n, f'Accepted status partition: {value}',
        'EP - valid status enumeration partition', 'REQ-C-002', [
            ('Inspect the status select on card "Status fixture".',
             'The select is labelled "Change status of Status fixture" and offers exactly "To Do", "In Progress" and "Completed".'),
            (f'Select "{value}".',
             f'The card status badge reads "{value}"; toast "Task status updated." appears; saved status is "{value}".'),
        ], pre='Fixture: one task titled Status fixture with status To Do, priority Medium and empty dueDate.'))

enum_cases += [
    case(7, 'Reject unsupported priority string in validator harness',
         'EP - invalid priority enumeration partition; unit harness', 'REQ-C-001', [
             ("Run validateTask({title:'Valid task',description:'',priority:'Urgent',status:'To Do',dueDate:''}) in the Node harness.",
              'The returned errors object contains priority: "Please select a valid priority." and no title, status or dueDate error.'),
             ("Run the same fixture with priority:'low'.", 'The returned priority error remains exactly "Please select a valid priority."; the comparison is case-sensitive.'),
         ], pre='Unit harness only: native Priority select cannot submit an unsupported option. Do not call this a browser form test.', importance=3),
    case(8, 'Reject non-string and missing priority values in validator harness',
         'EP - invalid priority type partitions; unit harness', 'REQ-C-001', [
             ("Call validateTask with priority:null, then with the priority property omitted; keep all other required values valid.",
              'Both calls return priority: "Please select a valid priority."; there is no exception.'),
         ], pre='Unit harness only: HTML select controls cannot produce null or an omitted priority field.', importance=2),
    case(9, 'Reject unsupported status string in validator harness',
         'EP - invalid status enumeration partition; unit harness', 'REQ-C-002', [
             ("Run validateTask({title:'Valid task',description:'',priority:'Medium',status:'Blocked',dueDate:''}) in the Node harness.",
              'The returned errors object contains status: "Please select a valid status." and no title, priority or dueDate error.'),
             ("Run the same fixture with status:'completed'.", 'The returned status error remains exactly "Please select a valid status."; the comparison is case-sensitive.'),
         ], pre='Unit harness only: native Status select cannot submit an unsupported option.', importance=3),
    case(10, 'Reject non-string and missing status values in validator harness',
         'EP - invalid status type partitions; unit harness', 'REQ-C-002', [
             ("Call validateTask with status:42, then with the status property omitted; keep all other required values valid.",
              'Both calls return status: "Please select a valid status."; there is no exception.'),
         ], pre='Unit harness only: HTML select controls cannot produce a numeric or omitted status value.'),
    case(11, 'Report both invalid enum fields together',
         'Decision Table - priority invalid AND status invalid; unit harness', 'REQ-C-001 REQ-C-002', [
             ("Call validateTask with priority:'Urgent' and status:'Blocked', keeping title, description and dueDate valid.",
              'The returned object contains both priority: "Please select a valid priority." and status: "Please select a valid status."; no other keys are present.'),
             ("Change only priority to 'High' and call again.", 'Only status: "Please select a valid status." remains.'),
             ("Change status to 'Completed' and call again.", 'The returned errors object is empty.'),
         ], pre='Unit harness only: native controls offer only valid enum values.'),
]

transition_cases = []
transitions = [
    ('To Do', 'In Progress'), ('To Do', 'Completed'),
    ('In Progress', 'To Do'), ('In Progress', 'Completed'),
    ('Completed', 'To Do'), ('Completed', 'In Progress'),
]
for n, (source, target) in enumerate(transitions, 12):
    transition_cases.append(case(n, f'Status transition {source} to {target}',
        'State Transition - source state to distinct destination state', 'REQ-C-002 REQ-C-003', [
            (f'With one card "Transition fixture" in state "{source}", record its updatedAt from localStorage.',
             f'The card status badge and Change status select both show "{source}".'),
            (f'Choose "{target}" in Change status of Transition fixture.',
             f'The badge and select show "{target}"; toast "Task status updated." appears; storage status is "{target}" and updatedAt is later than the recorded value.'),
            ('Inspect the list and localStorage.',
             'Exactly one task remains; its id, title, priority and dueDate are unchanged.'),
        ], pre=f'Fixture: one task titled Transition fixture, status {source}, priority Medium, dueDate empty; no filters active.', importance=3))

for n, status in enumerate(('To Do', 'In Progress', 'Completed'), 18):
    transition_cases.append(case(n, f'Same-state selection behavior for {status}',
        'State Transition - same source and destination state', 'REQ-C-002 REQ-C-003', [
            (f'Load one task "Same state fixture" with status "{status}" and record updatedAt.',
             f'The card badge and select both show "{status}".'),
            ("In DevTools dispatch a bubbling change event on that card's status select with its current value.",
             'The status remains unchanged; toast "Task status updated." appears; changeStatus writes a new updatedAt timestamp.'),
            ('Inspect localStorage.',
             'There is still exactly one task with the same id and status; only updatedAt is refreshed among the recorded task fields.'),
        ], pre='Fixture: one task titled Same state fixture, priority Medium, dueDate empty. Trigger change event explicitly because selecting the already selected native option does not normally emit change.', importance=2))

counts = [
    ('search', 'Type "needle" in the search input.', 'Only matching cards change; summary remains Total Tasks 5, To Do 2, In Progress 2, Completed 1.'),
    ('status', 'Set Status filter to "Completed".', 'Only the completed card remains visible; summary remains Total Tasks 5, To Do 2, In Progress 2, Completed 1.'),
    ('priority', 'Set Priority filter to "High".', 'Only High priority cards remain visible; summary remains Total Tasks 5, To Do 2, In Progress 2, Completed 1.'),
    ('combined', 'Search for "needle" while Status is Completed and Priority is High.', 'The list reflects the combined filters (one matching completed card); summary remains Total Tasks 5, To Do 2, In Progress 2, Completed 1.'),
]
for n, (kind, action, expected) in enumerate(counts, 21):
    transition_cases.append(case(n, f'Summary totals ignore {kind} filtering',
        'Decision Table - summary calculation independent of visible result set', 'REQ-C-003', [
            ('Load five tasks: A (To Do/Low), B (To Do/High), C (In Progress/Medium), needle work (In Progress/High), needle done (Completed/High).',
             'SummaryCards shows "Total Tasks" 5, "To Do" 2, "In Progress" 2 and "Completed" 1.'),
            (action, expected),
            ('Read all four summary cards after the list refresh.',
             'The four counts remain 5, 2, 2 and 1 respectively, regardless of the number of visible cards.'),
        ], pre='Use the exact five-task fixture above, no other saved tasks.'))

transition_cases += [
    case(25, 'Completed overdue card has completed styling and no overdue treatment',
         'Decision Table - overdue date AND Completed state', 'REQ-C-004 REQ-C-007', [
             ('With fixed local today 2026-10-27, load a Completed task due 2026-10-26.',
              'The card has class "completed" and status badge "Completed".'),
             ('Inspect the due-date line and badges.',
              'The line reads "Due: Oct 26, 2026" without overdue red styling; no "Overdue" or "Due today" badge is rendered.'),
         ], pre='Use the fixed local day from COMMON. Fixture title: Completed yesterday; dueDate 2026-10-26; status Completed.', importance=3),
    case(26, 'Completed task due today omits Due today badge',
         'Decision Table - today date AND Completed state', 'REQ-C-004 REQ-C-007', [
             ('With fixed local today 2026-10-27, load a Completed task due 2026-10-27.',
              'The card has class "completed" and status badge "Completed".'),
             ('Inspect its date badges.', 'Neither "Due today" nor "Overdue" is shown.'),
         ], pre='Fixture: Completed today, dueDate 2026-10-27, status Completed; fixed local reference date 2026-10-27.'),
]

date_cases = [
    case(27, 'Empty due date is a valid optional value', 'EP - absent optional due-date partition', 'REQ-C-005', [
        ('Open New Task and inspect Due Date.', 'The native date input is blank and the hint reads "Optional".'),
        ('Create a task with valid required fields and leave Due Date blank.', 'The task is saved; no due-date error appears; localStorage dueDate is the empty string; the card has no "Due:" line.'),
    ], pre='Fixture starts with no tasks. Use title Optional date fixture, Medium priority and To Do status.'),
    case(28, 'Valid leap-day date is retained and formatted', 'EP - valid optional date partition', 'REQ-C-005 REQ-C-006 REQ-C-008', [
        ('Create a task and set Due Date to 2028-02-29.', 'The native date input displays 2028-02-29 and has aria-invalid="false".'),
        ('Save and inspect the card and localStorage.', 'Saved dueDate is "2028-02-29"; the card line reads "Due: Feb 29, 2028".'),
    ], pre='Fixture: empty task list; title Leap fixture, valid enums.'),
    case(29, 'Native date input sanitizes impossible date before validator', 'Error Guessing - native date sanitization boundary', 'REQ-C-005', [
        ("Open New Task; in DevTools assign '2026-02-29' to input[name=dueDate].value and read the value back.", 'The native date input value is the empty string because 2026-02-29 is not a real date; the form has no due-date error because the field is optional.'),
        ('Inspect aria-invalid and submit the otherwise valid task.', 'aria-invalid remains "false" for dueDate; creation is accepted with dueDate "" and no "Please enter a valid date (YYYY-MM-DD)." message.'),
    ], pre='Use Chrome native input[type=date]. This case verifies browser sanitization and does not claim validateTask rejected the impossible date.', importance=3),
    case(30, 'Validator rejects impossible calendar date independently of native control', 'EP - invalid date partition; unit harness', 'REQ-C-005 REQ-C-006', [
        ("Run validateTask with dueDate:'2026-02-29' and all other fields valid.", 'The returned errors object contains dueDate: "Please enter a valid date (YYYY-MM-DD).".'),
        ("Repeat with dueDate:'2026-13-01'.", 'The same exact dueDate error is returned; no other field error is present.'),
    ], pre='Unit harness only: import validateTask from src/utils/validation.js; do not claim native form rejection.', importance=3),
    case(31, 'Leap-year divisibility decision table', 'Decision Table - Gregorian leap-year rule; unit harness', 'REQ-C-006', [
        ("Call isValidDateString for 2024-02-29, 2000-02-29, 1900-02-29 and 2100-02-29.", 'Results respectively are true, true, false and false: divisible by 4 except century years unless divisible by 400.'),
        ("Call validateTask for each date with other fields valid.", 'The first two produce no dueDate error; 1900 and 2100 produce "Please enter a valid date (YYYY-MM-DD).".'),
    ], pre='Unit harness only: use fixed date strings; the check is independent of the current day.'),
    case(32, 'Day-of-month minimum and maximum boundaries', 'BVA - day min-1/min/max/max+1; unit harness', 'REQ-C-005 REQ-C-006', [
        ("Check isValidDateString for January 00, 01, 31 and 32 in year 2026.", '2026-01-00 is false (min-1); 2026-01-01 is true (minimum day); 2026-01-31 is true (maximum day); 2026-01-32 is false (max+1).'),
        ("Check validateTask for the two invalid values.", 'Each invalid value returns dueDate: "Please enter a valid date (YYYY-MM-DD).".'),
    ], pre='Unit harness only: JavaScript object literals use exact YYYY-MM-DD strings.', importance=3),
    case(33, 'Leap-February day maximum and max+1', 'BVA - leap month day max/max+1; unit harness', 'REQ-C-006', [
        ("Check isValidDateString for 2024-02-28, 2024-02-29 and 2024-02-30.", 'February 28 and leap day February 29 are true; February 30 is false.'),
        ("Check isValidDateString for 2023-02-28 and 2023-02-29.", 'February 28 is true; February 29 is false in the non-leap year.'),
    ], pre='Unit harness only; fixed Gregorian dates.'),
    case(34, 'Thirty-day month maximum and max+1', 'BVA - month-specific maximum and max+1; unit harness', 'REQ-C-006', [
        ("Check isValidDateString for 2026-04-30 and 2026-04-31.", 'April 30 is true (month maximum); April 31 is false (max+1).'),
        ("Check isValidDateString for 2026-06-30 and 2026-06-31.", 'June 30 is true; June 31 is false.'),
    ], pre='Unit harness only; verifies separate 30-day months.'),
    case(35, 'Month range min-1/min/max/max+1', 'BVA - month min-1/min/max/max+1; unit harness', 'REQ-C-006', [
        ("Check isValidDateString for months 00, 01, 12 and 13 using year 2026 and day 01.", 'Month 00 is false (min-1); 01 is true (minimum); 12 is true (maximum); 13 is false (max+1).'),
        ("Pass each value through validateTask.", 'Months 00 and 13 return "Please enter a valid date (YYYY-MM-DD)."; months 01 and 12 have no dueDate error.'),
    ], pre='Unit harness only. No application date range beyond calendar month boundaries is inferred.'),
    case(36, 'Date string shape and optional absence partitions', 'EP - valid-format and invalid-format date partitions; unit harness', 'REQ-C-005 REQ-C-006', [
        ("Check isValidDateString for '2026-01-01', '2026-1-01', '26-01-01', and '2026/01/01'.", 'Only exact four-two-two hyphenated YYYY-MM-DD is true.'),
        ("Check validateTask with dueDate omitted, null and empty string.", 'All three absent-value forms are accepted without a dueDate error.'),
        ("Check dueDate:'2026-1-01' in validateTask.", 'The returned dueDate error is exactly "Please enter a valid date (YYYY-MM-DD).".'),
    ], pre='Unit harness only; no native input behavior is asserted.'),
]

date_cases += [
    case(37, 'Fixed local yesterday-today-tomorrow by completion state', 'Decision Table - date relation by completion state', 'REQ-C-004 REQ-C-007', [
        ('Set reference local today to 2026-10-27 (Asia/Baghdad). Evaluate fixtures for due date 2026-10-26 (yesterday), 2026-10-27 (today), 2026-10-28 (tomorrow) against status To Do and status Completed.',
         'Decision table: Yesterday + To Do => isOverdue true, UI badge "Overdue" and red due-date style; Yesterday + Completed => false, no "Overdue" or "Due today"; Today + To Do => false, badge "Due today"; Today + Completed => false, no date badge; Tomorrow + To Do => false, no date badge; Tomorrow + Completed => false, no date badge.'),
        ("Run the six isOverdue({dueDate,status}, '2026-10-27') assertions in the Node harness.", 'Only yesterday + To Do returns true; the other five return false.'),
    ], pre='Run the fixed-day harness, then inspect the matching card states in the disposable UI with the same frozen local day. Fix the test date explicitly; do not rely on October 2026 still being current.', importance=3),
    case(38, 'Overdue result changes when a task becomes Completed', 'State Transition - active overdue to Completed exempt state', 'REQ-C-004 REQ-C-007', [
        ('With fixed today 2026-10-27, load task Overdue transition due 2026-10-26 in To Do.', 'The card shows "Overdue" and its due-date line uses overdue styling.'),
        ('Change its status to Completed.', 'The card gains class "completed"; badge "Overdue" disappears; due-date styling is no longer overdue; toast "Task status updated." appears.'),
        ('Change status back to In Progress.', 'Because its date is still yesterday, "Overdue" returns and the completed class is removed.'),
    ], pre='Fixture dueDate 2026-10-26. Fix the app-local clock to 2026-10-27T12:00:00+03:00 before asserting badges.', importance=3),
    case(39, 'Due-date relation follows local calendar day, not UTC parsing', 'BVA - local day boundary around midnight; unit harness', 'REQ-C-007 REQ-C-008', [
        ("Under TZ=Asia/Baghdad, construct new Date('2026-10-26T21:30:00Z') and pass it to todayString.", 'The instant is 2026-10-27 00:30 in Baghdad and todayString returns "2026-10-27".'),
        ("Call isOverdue({dueDate:'2026-10-27',status:'To Do'}, todayString(theFixedDate)).", 'The result is false because the due date is the local current calendar day, even though the UTC timestamp is on the prior date.'),
        ("Call isOverdue({dueDate:'2026-10-26',status:'To Do'}, todayString(theFixedDate)).", 'The result is true; the prior local calendar day is overdue.'),
    ], pre='Unit harness only. Set process TZ=Asia/Baghdad and use fixed instant 2026-10-26T21:30:00Z; do not use new Date("YYYY-MM-DD") as the clock.', importance=3),
    case(40, 'Due-date formatting is stable for a fixed date', 'EP - valid display-format partition', 'REQ-C-008', [
        ('Load tasks due 2026-02-09, 2028-02-29 and 2026-12-31.', 'Cards display respectively "Due: Feb 9, 2026", "Due: Feb 29, 2028" and "Due: Dec 31, 2026".'),
        ('Call formatDueDate with those same strings in the utility harness.', 'The returned strings are respectively "Feb 9, 2026", "Feb 29, 2028" and "Dec 31, 2026".'),
    ], pre='Use exact local calendar date values. This formatting assertion is independent of current date/time.'),
    case(41, 'Local today helpers use fixed local date rather than wall clock', 'Use Case - fixed local clock and reproducible date formatting; unit harness', 'REQ-C-008', [
        ("Under TZ=Asia/Baghdad create new Date(2026, 9, 27, 12, 0, 0); call todayString(date).", 'The result is exactly "2026-10-27".'),
        ("Call formatToday(date).", 'The result is exactly "Tuesday, October 27, 2026".'),
        ('Repeat on a machine whose wall clock is after October 2026 using the same constructed Date.', 'Both expected results remain the fixed October 27, 2026 local values; neither assertion depends on the machine current date.'),
    ], pre='Unit harness only; set TZ=Asia/Baghdad before starting Node so local Date construction is explicit.'),
]

SUITES = [
    {'name': 'TS-C1 - Priority and status partitions',
     'details': 'Valid enum choices plus invalid string, casing, type, missing and simultaneous invalid partitions. Unit harness is explicitly called out where native controls block tampering.',
     'cases': enum_cases},
    {'name': 'TS-C2 - Status transitions, summaries and Completed tasks',
     'details': 'All six distinct directed transitions, same-state behavior for all three states, filter-independent summary decision table and Completed presentation/exemption.',
     'cases': transition_cases},
    {'name': 'TS-C3 - Optional dates and calendar validation',
     'details': 'Optional/valid/invalid dates, browser sanitization distinguished from validator rejection, exact format and month/day/leap-year boundaries.',
     'cases': date_cases[:10]},
    {'name': 'TS-C4 - Local-day decisions and date formatting',
     'details': 'Fixed Asia/Baghdad reference day, explicit date-relation × completion decision table, local midnight boundary and stable formatting.',
     'cases': date_cases[10:]},
]

# Leader review: use a distinct initial status so native selects really emit change.
for _case in enum_cases:
    if _case['id'] in ('TC-C-004','TC-C-005','TC-C-006'):
        _target = ('To Do','In Progress','Completed')[int(_case['id'][-3:])-4]
        _initial = 'In Progress' if _target == 'To Do' else 'To Do'
        _case['pre'] = _case['pre'].replace('with status To Do,', 'with status '+_initial+',')
        _case['pre'] += ' Initial saved updatedAt is 2026-01-01T00:00:00.000Z; the reference clock is later.'
for _suite in SUITES:
    for _case in _suite['cases']:
        if 'transition' in _case['name'].lower() or 'Same-state' in _case['name']:
            _case['pre'] += ' Seed createdAt and updatedAt as 2026-01-01T00:00:00.000Z so the first reference-clock mutation advances updatedAt.'
TOP_SUITE_DETAILS += ('<p>Reproducible UI clock: set the disposable browser timezone to Asia/Baghdad. After loading the case fixture and reloading, run in DevTools: '
    'window.CRealDate=Date; window.CFixed=Date.parse("2026-10-27T12:00:00+03:00"); '
    'window.Date=class extends CRealDate {constructor(...a){super(...(a.length?a:[CFixed]))} static now(){return CFixed}}; '
    'then type a temporary search query and clear it to force a React render. This freezes application Date calls for this page only; reload restores Date. '
    'For Node utility checks run TZ=Asia/Baghdad node --input-type=module and import functions from the cited src/utils/*.js files. '
    'Each manually seeded task needs a distinct string id, a title of at least 3 code points, description "", valid priority/status, dueDate "" unless specified, '
    'and createdAt/updatedAt 2026-01-01T00:00:00.000Z. Summary fixtures named A/B/C use valid titles Task A/Task B/Task C.</p>')
_midnight = next(c for s in SUITES for c in s['cases'] if c['id']=='TC-C-039')
_midnight['steps'].insert(0, (
    "Under TZ=Asia/Baghdad call todayString(new Date(value)) for 2026-10-26T20:59:59.999Z, 2026-10-26T21:00:00.000Z and 2026-10-26T21:00:00.001Z.",
    'The returned dates are 2026-10-26, 2026-10-27 and 2026-10-27 respectively: immediately before, at and after local midnight.'))
