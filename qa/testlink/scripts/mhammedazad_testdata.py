"""Member B editing/deletion design. Manual cases are Not Run, not execution claims.

Basis: TaskFlow main@5133a6c; data shape follows aland_testdata.py only.
"""
AUTHOR = 'mhammedazad'
FULL_NAME = 'Mhamad'
LETTER = 'B'
TOP_SUITE = 'B - Mhamad - Editing and deletion'
TOP_SUITE_DETAILS = (
    '<p>Member 2 / B: Mhamad (GitHub MhammedAzad). Group TaskFlow; leader Aland Karwan. '
    'SECJ3343 Project 1 Test Case Design, due 27 October 2026. '
    'Basis: README.md TF-REQ-009 through TF-REQ-015 and editing persistence in TF-REQ-018, '
    'TaskFlow main@5133a6c. Code-derived refinements are identified in the requirements.</p>'
    '<p>Scope: prefilled edits, valid and rejected edits, identity/timestamps, every edit dismissal path, '
    'priority edit persistence, exact deletion confirmation, every deletion dismissal path, '
    'intended-target isolation and repeated operations. Creation, text boundary sweeps, enum/date '
    'partitions, counts/status transitions, queries, general storage recovery and navigation '
    'belong to other members. Their actions are setup only. All cases are manual and Not Run.</p>'
    '<p>Each case independently resets ONLY a disposable Chrome profile at http://localhost:5173 '
    'using the complete fixture instructions in its preconditions. Never use personal task storage. '
    'Read ISO timestamps in stored JSON, not the day-resolution Created label. '
    'Observe specified success messages within three seconds. Numbered steps are generated from '
    'the ordered action/expected-result tuples.</p>'
)


def requirement(rid, title, rule, source, documented):
    return (rid, title, rule + ' Basis: README.md (' + documented +
            '); implementation: ' + source + '; baseline main@5133a6c. '
            'Code-derived refinements supplement the documented rule; no separate customer SRS is claimed.')


EDIT_REQS = [
    requirement('REQ-B-001', 'Prefill the selected task for editing',
                'Opening Edit shall show "Edit Task", "Cancel" and "Save Changes". Task Title, Description, '
                'Priority, Status and Due Date shall contain that selected task\'s saved values; optional empty '
                'values remain empty. Reopening or selecting another task initializes from its latest saved object.',
                'src/App.jsx editingTask and keyed TaskFormModal; src/components/TaskFormModal.jsx task initializer',
                'TF-REQ-009; Exact messages / Dialog text'),
    requirement('REQ-B-002', 'Commit a valid edit atomically to the selected task',
                'A valid "Save Changes" replaces the selected task\'s normalized form values, immediately saves '
                'taskflow_tasks, closes "Edit Task" and shows "Task updated successfully." Unedited fields and '
                'all other task objects remain unchanged; empty optional description/date may be saved. '
                'Title and description are trimmed by normalizeValues (text boundary testing belongs to A).',
                'src/components/TaskFormModal.jsx handleSubmit; src/App.jsx updateTask/commit; '
                'src/utils/tasks.js normalizeValues; src/utils/storage.js saveTasks',
                'TF-REQ-010; Storage; Exact messages / Edit'),
    requirement('REQ-B-003', 'Preserve identity and creation timestamp while advancing update time',
                'A successful edit preserves id and createdAt exactly and sets updatedAt to the current ISO '
                'timestamp, even when form values are unchanged. With a clock later than the fixture timestamp, '
                'updatedAt must be strictly later than before the save. A title change must not create a new task.',
                'src/App.jsx updateTask object spread and new Date().toISOString()',
                'TF-REQ-010; Storage / Task fields'),
    requirement('REQ-B-004', 'Reject invalid edits without any partial commit',
                'Any validation error keeps "Edit Task" open and leaves every stored task field, including '
                'updatedAt, unchanged. Representative failures: blank/space-only title gives "Title is required."; '
                'two trimmed characters gives "Title must be at least 3 characters."; 81 characters gives '
                '"Title must be 80 characters or fewer."; 501 description characters gives '
                '"Description must be 500 characters or fewer." No "Task updated successfully." is emitted. '
                'These are edit rejection checks, not A\'s text boundary sweep or C\'s enum/date partitions.',
                'src/components/TaskFormModal.jsx handleSubmit return before onSave; src/utils/validation.js validateTask; '
                'src/App.jsx updateTask', 'TF-REQ-011; Exact messages / Validation'),
    requirement('REQ-B-005', 'Recover a rejected edit and commit only the corrected values',
                'A rejected edit retains the entered draft. Correcting its invalid values then choosing '
                '"Save Changes" commits exactly one update, closes the form and shows '
                '"Task updated successfully." Original id/createdAt remain intact.',
                'src/components/TaskFormModal.jsx values/submitted/handleSubmit; src/App.jsx updateTask',
                'TF-REQ-010/011; Exact messages / Edit'),
    requirement('REQ-B-006', 'Persist priority edits through the edit workflow',
                'Saving a changed Priority through "Save Changes" retains the selected priority in '
                'taskflow_tasks, the card badge and the next edit form, including after reload. Repeated priority '
                'edits retain the latest saved choice. Query/filter semantics and enum partition validation are excluded.',
                'src/components/TaskFormModal.jsx priority select; src/App.jsx updateTask/commit; '
                'src/utils/tasks.js normalizeValues; src/components/TaskCard.jsx priority badge',
                'TF-REQ-018 (edit persistence only); TF-REQ-010; Storage'),
    requirement('REQ-B-007', 'Apply repeated edits and target only the selected identity',
                'Successive edit sessions start from the latest committed values. Editing a task among '
                'same-title siblings updates only its id; switching between tasks must not reuse another task\'s draft. '
                'Each successful save shows "Task updated successfully."',
                'src/App.jsx updateTask id comparison, editingTask and keyed TaskFormModal; '
                'src/components/TaskFormModal.jsx task initializer', 'TF-REQ-009/010; Exact messages / Edit'),
]
CANCEL_REQS = [
    requirement('REQ-B-008', 'Discard editing through every supported dismissal path',
                '"Cancel", "Close" (X), Escape and a mouse press on the dark backdrop close "Edit Task" '
                'without saving any draft, changing id/createdAt/updatedAt, or showing '
                '"Task updated successfully." This applies to valid, invalid, unchanged and priority-only drafts.',
                'src/components/TaskFormModal.jsx Cancel; src/components/Modal.jsx Close/onKeyDown/onMouseDown; '
                'src/App.jsx closeModal', 'TF-REQ-012; Exact messages / Dialog text'),
    requirement('REQ-B-009', 'Reopening a canceled edit discards draft and validation state',
                'After dismissal, a new "Edit Task" session contains only the saved values and no previous '
                'draft/error state. A canceled priority edit cannot appear on the next edit session or reload.',
                'src/App.jsx closeModal and conditional TaskFormModal mount; '
                'src/components/TaskFormModal.jsx useState initializers', 'TF-REQ-009/012'),
    requirement('REQ-B-010', 'Interior modal interaction is not backdrop dismissal',
                'A mouse press inside either dialog must not close it or commit an edit/delete. '
                'Only event.target === event.currentTarget on the dark backdrop invokes onClose. '
                'Ordinary interaction with edit controls keeps "Edit Task" open until explicit save/dismissal.',
                'src/components/Modal.jsx onMouseDown target equality; src/App.jsx closeModal',
                'TF-REQ-012/015 supplemented by code-derived backdrop hit-test behavior'),
]
DELETE_REQS = [
    requirement('REQ-B-011', 'Show exact deletion confirmation for the current target',
                '"Delete" opens "Delete Task" with exactly: Are you sure you want to delete "<title>"? '
                'This cannot be undone. The title is the current saved target title (including quotes or '
                'punctuation), and buttons are "Cancel" and "Confirm Delete". Opening the dialog alone '
                'must not remove or mutate any task.',
                'src/App.jsx deletingTask by modal.id; src/components/ConfirmDeleteModal.jsx',
                'TF-REQ-013; Exact messages / Dialog text'),
    requirement('REQ-B-012', 'Confirm deletion of only the intended task',
                '"Confirm Delete" removes only the selected id, immediately saves the remaining array, closes '
                '"Delete Task" and shows "Task deleted successfully." Every other task object remains exactly '
                'unchanged. The deleted object remains absent after reload, including when it was the sole task '
                'or shared a title with another object. Same-title setup is not a creation assertion.',
                'src/App.jsx deleteTask/commit; src/components/ConfirmDeleteModal.jsx onConfirm; '
                'src/utils/storage.js saveTasks', 'TF-REQ-014; Storage; Exact messages / Delete'),
    requirement('REQ-B-013', 'Cancel deletion through every supported dismissal path',
                '"Cancel", "Close" (X), Escape and pressing the dark backdrop close "Delete Task" '
                'without removing or changing any task or timestamp and without '
                '"Task deleted successfully." Reopening must offer confirmation for the correct saved task.',
                'src/components/ConfirmDeleteModal.jsx onClose; src/components/Modal.jsx Close/onKeyDown/onMouseDown; '
                'src/App.jsx closeModal', 'TF-REQ-015 supplemented by shared Modal close paths'),
    requirement('REQ-B-014', 'Keep deletion targets correct across repeated and mixed operations',
                'Canceling and reopening a deletion, deleting different tasks in sequence, or canceling an edit '
                'before deletion shall use the latest selected saved object. A confirmed id is removed once; '
                'siblings remain intact. Each completed deletion shows "Task deleted successfully."',
                'src/App.jsx modal/deletingTask/deleteTask/closeModal; src/components/ConfirmDeleteModal.jsx',
                'TF-REQ-013/014/015 supplemented by code-derived repeated workflow behavior'),
]
REQ_SPECS = [
    {'doc_id': 'SRS-B-EDIT', 'title': 'Member B - Editing and priority persistence',
     'scope': 'README.md TF-REQ-009/010/011/018 edit persistence; src/App.jsx updateTask; '
              'src/components/TaskFormModal.jsx; src/utils/tasks.js and validation.js. '
              'Derived refinements of documented rules, not an invented customer SRS.', 'reqs': EDIT_REQS},
    {'doc_id': 'SRS-B-CANCEL', 'title': 'Member B - Editing dismissal and draft isolation',
     'scope': 'README.md TF-REQ-012 plus code-derived dismissal refinements; '
              'src/components/Modal.jsx, TaskFormModal.jsx; src/App.jsx closeModal.', 'reqs': CANCEL_REQS},
    {'doc_id': 'SRS-B-DELETE', 'title': 'Member B - Deletion confirmation and target isolation',
     'scope': 'README.md TF-REQ-013/014/015; src/components/ConfirmDeleteModal.jsx and Modal.jsx; '
              'src/App.jsx deleteTask. Only normal writable-storage workflows.', 'reqs': DELETE_REQS},
]

# Concrete independent fixture: paste in DevTools Console at localhost:5173, then reload.
# Every case carries this full data; references to A/B/C are object ids, not member slots.
FIXTURE = '''localStorage.removeItem("taskflow_tasks_backup"); localStorage.setItem("taskflow_tasks", JSON.stringify([
{id:"b-alpha",title:"Prepare sprint review",description:"Agenda draft",priority:"Low",status:"In Progress",dueDate:"2028-02-29",createdAt:"2026-01-01T09:00:00.000Z",updatedAt:"2026-01-02T10:00:00.000Z"},
{id:"b-beta",title:"Book meeting room",description:"Room 4",priority:"Medium",status:"To Do",dueDate:"",createdAt:"2026-01-03T09:00:00.000Z",updatedAt:"2026-01-04T10:00:00.000Z"},
{id:"b-gamma",title:"Archive review notes",description:"Keep signed copy",priority:"High",status:"Completed",dueDate:"",createdAt:"2026-01-05T09:00:00.000Z",updatedAt:"2026-01-06T10:00:00.000Z"}
])); location.reload();'''
COMMON = (
    'INDEPENDENT RESET: use ONLY a disposable Chrome profile, http://localhost:5173, TaskFlow '
    'main@5133a6c; writable browser storage; system clock later than 2026-01-06. Open DevTools '
    'Console and run the following exact fixture; close DevTools after reload: ' + FIXTURE +
    ' Dashboard, search empty, status/priority filters All, Newest first (setup only). '
    'A means id b-alpha, B means b-beta, C means b-gamma, irrespective of card order. '
    'Before acting, use Console: window.bBefore = JSON.parse(localStorage.getItem("taskflow_tasks")); '
    'close DevTools. To inspect persisted objects later, reopen Console and evaluate '
    'JSON.parse(localStorage.getItem("taskflow_tasks")); compare by id with bBefore, not array position. '
    'Do not reload before completing an in-memory draft step. Read toasts immediately within 3 seconds. '
    'Inspect id/createdAt/updatedAt as raw JSON; list date formatting, counts, query behavior, '
    'generic reload/recovery, enum/date semantics and creation are not assertions of these cases. '
)


def case(n, title, technique, reqs, steps, pre='', importance=2):
    cid = f'TC-B-{n:03d}'
    return {'id': cid, 'name': cid + ' - ' + title, 'technique': technique,
            'reqs': reqs.split(), 'pre': COMMON + pre,
            'steps': steps, 'importance': importance}


OPEN_EDIT = ('Click "Edit Prepare sprint review" on A.',
             '"Edit Task" opens for A with "Cancel" and "Save Changes".')
SAVED = ('Dialog closes; "Task updated successfully." appears. Stored array has the same three ids; '
         'A retains id b-alpha and createdAt 2026-01-01T09:00:00.000Z; updatedAt is valid ISO, '
         'later than 2026-01-02T10:00:00.000Z and within the recorded save interval. B and C are '
         'field-for-field unchanged from bBefore.')
SAVE_ACTION = ('Record new Date().toISOString() in Console immediately before save; close Console, '
               'click "Save Changes", observe toast, record the time again and inspect saved JSON.')
UNCHANGED = ('All stored objects equal bBefore field-for-field, including id, createdAt and updatedAt. '
             'No "Task updated successfully." appears.')
EDIT_CASES = [
    case(1, 'Prefill all saved fields', 'Use Case - selected existing task opens for edit',
         'REQ-B-001', [OPEN_EDIT,
          ('Inspect the five form controls without changing or submitting them.',
           'Task Title "Prepare sprint review"; Description "Agenda draft"; Priority "Low"; '
           'Status "In Progress"; Due Date value "2028-02-29". No saved value has been replaced by a creation default.'),
          ('Click "Cancel".', 'Dialog closes; no edit is committed.')], importance=3),
    case(2, 'Prefill empty optional fields', 'EP - existing task with absent optional content',
         'REQ-B-001', [
          ('For this case only, before opening edit, set B.description to "" in stored JSON and reload; recapture bBefore.',
           'Fixture B is available with description "" and dueDate "".'),
          ('Click "Edit Book meeting room".',
           '"Edit Task" has title "Book meeting room", empty Description and Due Date, "Medium", "To Do".'),
          ('Click "Cancel".', 'Dialog closes without saving.')]),
    case(3, 'Save title-only edit with identity retained', 'Use Case - single-field edit',
         'REQ-B-002 REQ-B-003', [OPEN_EDIT,
          ('Replace Task Title with "Prepare final sprint review"; leave other controls unchanged.',
           'Draft title is "Prepare final sprint review".'),
          (SAVE_ACTION, SAVED + ' A.title is "Prepare final sprint review"; description, priority, status and dueDate equal bBefore A.')], importance=3),
    case(4, 'Save description-only edit', 'Use Case - optional text edit',
         'REQ-B-002 REQ-B-003', [OPEN_EDIT,
          ('Replace Description with "Final agenda\nBring demo".', 'Draft retains the two entered lines.'),
          (SAVE_ACTION, SAVED + ' A.description is exactly "Final agenda\nBring demo"; A title/priority/status/dueDate stay unchanged.')]),
    case(5, 'Save all editable fields together', 'Use Case - complete valid edit',
         'REQ-B-002 REQ-B-003 REQ-B-006', [OPEN_EDIT,
          ('Enter title "Review launch plan", description "Review checklist"; select High, Completed; set Due Date to 2028-03-15.',
           'Draft contains those five values (status/date selection is setup, not a validation or status/count assertion).'),
          (SAVE_ACTION, SAVED + ' A stores "Review launch plan", "Review checklist", "High", "Completed", "2028-03-15".'),
          ('Reopen "Edit Review launch plan".', '"Edit Task" contains all five saved values.')], importance=3),
    case(6, 'Clear existing optional description and date', 'EP - valid removal of optional values during edit',
         'REQ-B-002 REQ-B-003', [OPEN_EDIT,
          ('Clear Description and Due Date; leave the other values unchanged.', 'Both optional controls are empty.'),
          (SAVE_ACTION, SAVED + ' A.description and A.dueDate are both ""; other editable values remain unchanged.'),
          ('Reopen A edit.', 'Description and Due Date are empty in "Edit Task".')]),
    case(7, 'Save unchanged form still updates metadata', 'Error Guessing - no-op submit still calls updateTask',
         'REQ-B-002 REQ-B-003', [OPEN_EDIT,
          (SAVE_ACTION, SAVED + ' All five editable values equal bBefore A; only updatedAt changes.')]),
    case(8, 'Edit one same-title sibling only', 'Error Guessing - target identity differs despite equal titles',
         'REQ-B-002 REQ-B-003 REQ-B-007', [
          ('Before opening edit, set B.title to "Prepare sprint review" in stored JSON; reload; recapture bBefore.',
           'A and B share the title but retain ids b-alpha and b-beta and distinct descriptions.'),
          ('Within the card whose description is "Room 4", click Edit; replace Description with "Room 7".',
           '"Edit Task" opens with B\'s values and accepts the draft description.'),
          ('Click "Save Changes"; inspect JSON by id.',
           '"Task updated successfully."; only b-beta.description becomes "Room 7" and its updatedAt advances. '
           'Its id/createdAt stay unchanged; A and C equal bBefore. There are still three objects.')], importance=3),
    case(9, 'Repeat edits to the same task', 'State Transition - saved original -> saved revision one -> saved revision two',
         'REQ-B-001 REQ-B-003 REQ-B-007', [OPEN_EDIT,
          ('Set Description to "Revision one"; save; inspect A JSON and record first updatedAt.',
           '"Task updated successfully."; A.description "Revision one"; original id/createdAt preserved.'),
          ('Wait at least 1 second; reopen A edit, set Description to "Revision two"; save.',
           'Form initially shows "Revision one"; closes with "Task updated successfully." after save.'),
          ('Inspect JSON by id.',
           'Only A contains "Revision two"; updatedAt is later than the first save. No extra object; B/C unchanged.')], importance=3),
    case(10, 'Edit different tasks in sequence', 'State Transition - A edit saved -> B edit opened',
         'REQ-B-001 REQ-B-007', [OPEN_EDIT,
          ('Set Description to "A revised"; click "Save Changes"; then click "Edit Book meeting room".',
           'Edit success toast; new "Edit Task" shows B: "Book meeting room", "Room 4", "Medium", "To Do", empty date.'),
          ('Set Description to "B revised"; save; inspect JSON.',
           '"Task updated successfully."; A has "A revised", B has "B revised". Their original ids/createdAt remain; C unchanged.')]),
]


def rejected(n, title, value_action, messages, technique='EP - representative invalid edit partition'):
    return case(n, title, technique, 'REQ-B-004', [OPEN_EDIT,
        (value_action + ' Also select High as a proposed valid edit.', 'Draft is entered; stored A still has Low.'),
        ('Click "Save Changes"; inspect stored JSON without reloading.',
         '"Edit Task" stays open. ' + messages + ' ' + UNCHANGED + ' Priority remains Low in saved A; the valid field change is not partially saved.'),
        ('Click "Cancel".', 'Dialog closes; original A remains.')], importance=3)


EDIT_CASES += [
    rejected(11, 'Reject blank-title edit atomically', 'Replace Task Title with three spaces.', '"Title is required." is displayed.'),
    rejected(12, 'Reject short-title edit atomically', 'Replace Task Title with "ab".', '"Title must be at least 3 characters." is displayed.'),
    rejected(13, 'Reject overlong-title edit atomically',
             'Use DevTools copy("x".repeat(81)); close Console and paste into Task Title.',
             '"Title must be 80 characters or fewer." is displayed.'),
    rejected(14, 'Reject overlong-description edit atomically',
             'Use DevTools copy("d".repeat(501)); close Console and paste into Description.',
             '"Description must be 500 characters or fewer." is displayed.'),
    rejected(15, 'Reject two invalid fields without partial save',
             'Clear Task Title; paste exactly 501 copies of d into Description using copy("d".repeat(501)).',
             'Both "Title is required." and "Description must be 500 characters or fewer." are displayed.',
             'Decision Table - title valid=No, description valid=No, remaining fields valid=Yes; action=reject entire edit'),
    case(16, 'Correct rejected edit and save once', 'State Transition - edit draft -> rejected draft -> corrected saved task',
         'REQ-B-002 REQ-B-003 REQ-B-004 REQ-B-005', [OPEN_EDIT,
          ('Clear Task Title; set Description to "Revised agenda"; click "Save Changes".',
           '"Title is required."; "Edit Task" stays open; Description draft remains "Revised agenda"; stored JSON equals bBefore.'),
          ('Replace Task Title with "Prepare corrected review"; click "Save Changes"; inspect JSON.',
           'Form closes; "Task updated successfully."; A stores corrected title and "Revised agenda"; '
           'same id/createdAt, later updatedAt. Three objects; B and C unchanged.')], importance=3),
    case(17, 'Save priority edit and retain it after reload', 'Use Case - priority-only edit persistence',
         'REQ-B-002 REQ-B-003 REQ-B-006', [OPEN_EDIT,
          ('Change Priority from Low to High; leave every other form value unchanged.', 'Priority control shows "High".'),
          (SAVE_ACTION, SAVED + ' A.priority "High"; its other form values are unchanged; A card badge "High".'),
          ('Reload; inspect A JSON; reopen A edit.',
           'A.priority is still "High"; "Edit Task" Priority is "High"; id and createdAt remain the original values.')], importance=3),
    case(18, 'Latest repeated priority edit wins', 'State Transition - saved Low -> saved High -> saved Medium',
         'REQ-B-003 REQ-B-006 REQ-B-007', [OPEN_EDIT,
          ('Choose High; save; record A.updatedAt; wait at least 1 second; reopen A edit.',
           '"Task updated successfully."; reopened Priority is "High".'),
          ('Choose Medium; save; reload; inspect A JSON and reopen edit.',
           '"Task updated successfully." at save; latest saved/control/card priority is "Medium". '
           'Same id/createdAt; updatedAt later than the first save. B/C unchanged.')]),
]

CANCEL_CASES = []
for n, label, action in [
    (19, 'Cancel button', 'Click "Cancel".'),
    (20, 'Close X button', 'Click the dialog X button with accessible label "Close".'),
    (21, 'Escape key', 'Press Escape while Task Title is focused.'),
    (22, 'dark backdrop', 'Press and release the mouse on the dark backdrop outside the white dialog.'),
]:
    CANCEL_CASES.append(case(n, 'Discard dirty edit using ' + label,
        'State Transition - saved task -> dirty editing -> closed without commit',
        'REQ-B-008 REQ-B-009', [OPEN_EDIT,
         ('Change title to "Discarded draft", Description to "Unsaved agenda" and Priority to High.',
          'Draft values are visible in "Edit Task".'),
         (action, '"Edit Task" closes. ' + UNCHANGED),
         ('Reopen A edit.', 'Title "Prepare sprint review", Description "Agenda draft", Priority "Low"; no discarded values.')], importance=3))

CANCEL_CASES += [
    case(23, 'Cancel a rejected draft', 'State Transition - rejected editing -> closed without commit',
         'REQ-B-004 REQ-B-008', [OPEN_EDIT,
          ('Clear Task Title; click "Save Changes".', '"Title is required."; dialog stays open; saved JSON unchanged.'),
          ('Click "Cancel"; inspect JSON.', '"Edit Task" closes. ' + UNCHANGED)]),
    case(24, 'Cancel untouched edit without advancing timestamp', 'EP - unchanged edit dismissed rather than saved',
         'REQ-B-008', [OPEN_EDIT,
          ('Without touching any field, click "Cancel"; inspect raw JSON.', 'Dialog closes. ' + UNCHANGED)]),
    case(25, 'Reopen after rejected draft dismissal clears draft and errors',
         'State Transition - rejected editing -> closed -> fresh editing',
         'REQ-B-001 REQ-B-008 REQ-B-009', [OPEN_EDIT,
          ('Clear title; set Description to "Abandoned revision"; click "Save Changes".',
           '"Title is required."; draft Description remains "Abandoned revision".'),
          ('Press Escape; reopen A edit.',
           'New "Edit Task" contains "Prepare sprint review" and "Agenda draft"; previous "Title is required." is absent.'),
          ('Click "Cancel"; inspect JSON.', UNCHANGED)]),
    case(26, 'Clicking inside edit modal does not discard draft', 'Error Guessing - bubbling mousedown from interior',
         'REQ-B-010', [OPEN_EDIT,
          ('Set Description to "Interior draft"; click the "Edit Task" heading, then click the Description control.',
           '"Edit Task" remains open with "Interior draft"; neither click saves or discards it.'),
          ('Inspect stored JSON without reload; then click "Cancel".', 'Stored JSON equals bBefore; Cancel closes the draft.')]),
    case(27, 'Cancel priority-only change then reload', 'Use Case - abandoned priority edit persistence',
         'REQ-B-008 REQ-B-009', [OPEN_EDIT,
          ('Choose High; click "Cancel"; reload and inspect A JSON; reopen A edit.',
           'A.priority stays "Low" in JSON and the form; no "Task updated successfully." from cancellation; '
           'all fields and timestamps equal bBefore A.'),
          ('Click "Cancel".', 'Dialog closes without saving.')]),
]

OPEN_DELETE = ('Click "Delete Prepare sprint review" on A.',
               '"Delete Task" opens; A is still present.')
PROMPT = 'Are you sure you want to delete "Prepare sprint review"? This cannot be undone.'
DELETE_UNCHANGED = ('All three saved objects equal bBefore field-for-field including timestamps; '
                    'A is still present. No "Task deleted successfully." appears.')
DELETED = ('"Delete Task" closes; "Task deleted successfully." appears. Only b-alpha is absent from '
           'taskflow_tasks; B and C are unchanged, including all timestamps. Reload still contains exactly B and C.')
DELETE_CASES = [
    case(28, 'Exact confirmation before any deletion', 'Use Case - request deletion without confirmation',
         'REQ-B-011', [OPEN_DELETE,
          ('Read the dialog heading, full text and buttons; inspect JSON without reloading.',
           'Heading "Delete Task"; text exactly ' + PROMPT + ' Buttons "Cancel", "Confirm Delete"; '
           'all saved objects still equal bBefore.'),
          ('Click "Cancel".', 'Dialog closes without deleting.')], importance=3),
    case(29, 'Confirmation uses latest saved title and punctuation', 'Error Guessing - stale title or quote interpolation',
         'REQ-B-001 REQ-B-002 REQ-B-011', [OPEN_EDIT,
          ('Set title to the exact text Review "Beta" & notes; save; click Delete on that newly titled card.',
           '"Task updated successfully." at save; "Delete Task" opens for b-alpha.'),
          ('Read full confirmation text.',
           'Exactly: Are you sure you want to delete "Review "Beta" & notes"? This cannot be undone. '
           'Original title "Prepare sprint review" is not used in the confirmation; no deletion yet.'),
          ('Click "Cancel".', 'Edited task remains saved with its current title.')]),
    case(30, 'Confirm deletion leaves siblings intact', 'Use Case - requested deletion -> confirmed removal',
         'REQ-B-011 REQ-B-012', [OPEN_DELETE,
          ('Click "Confirm Delete"; observe toast, inspect stored objects, then reload.', DELETED)], importance=3),
    case(31, 'Confirm deletion of the sole remaining task', 'EP - one-task deletion partition',
         'REQ-B-012', [
          ('Before opening deletion, replace stored array with only fixture A; reload; recapture bBefore.',
           'Exactly the valid fixture A is present (fixture setup only).'), OPEN_DELETE,
          ('Click "Confirm Delete"; observe toast; inspect taskflow_tasks and reload.',
           'Dialog closes with "Task deleted successfully."; taskflow_tasks is [] and remains [] after reload; '
           'no task with id b-alpha exists. Empty-state copy/counts are outside this assertion.')], importance=3),
    case(32, 'Delete only intended same-title sibling', 'Error Guessing - duplicate titles must not select by title',
         'REQ-B-011 REQ-B-012', [
          ('Before deletion set B.title to "Prepare sprint review" in stored JSON; reload; recapture bBefore.',
           'A/B share a title and retain different ids/descriptions.'),
          ('Within the card with Description "Room 4", click Delete.',
           '"Delete Task" says exactly ' + PROMPT),
          ('Click "Confirm Delete"; inspect JSON and reload.',
           '"Task deleted successfully."; only b-beta is removed; A and C exactly equal their bBefore objects. '
           'The remaining same-title card is A with "Agenda draft".')], importance=3),
]
for n, label, action in [
    (33, 'Cancel button', 'Click "Cancel".'),
    (34, 'Close X button', 'Click X with accessible label "Close".'),
    (35, 'Escape key', 'Press Escape while the dialog is open.'),
    (36, 'dark backdrop', 'Press and release on the dark backdrop outside the white dialog.'),
]:
    DELETE_CASES.append(case(n, 'Dismiss deletion using ' + label,
        'State Transition - saved task -> awaiting confirmation -> saved task retained',
        'REQ-B-013', [OPEN_DELETE,
         (action + ' Inspect stored JSON.', '"Delete Task" closes. ' + DELETE_UNCHANGED),
         ('Reload; inspect saved JSON again.', 'All three original objects remain, including b-alpha and its unchanged timestamps.')], importance=3))
DELETE_CASES += [
    case(37, 'Interior deletion click is not a confirmation or dismissal',
         'Error Guessing - event bubbling within confirmation dialog',
         'REQ-B-010 REQ-B-011 REQ-B-013', [OPEN_DELETE,
          ('Click the warning paragraph (not a button).',
           '"Delete Task" stays open with exactly ' + PROMPT + ' No object is changed or removed.'),
          ('Click "Cancel"; inspect JSON.', DELETE_UNCHANGED)]),
    case(38, 'Reopen after canceled deletion targets newly selected task',
         'State Transition - A confirmation canceled -> B confirmation opened',
         'REQ-B-011 REQ-B-013 REQ-B-014', [OPEN_DELETE,
          ('Click "Cancel"; click "Delete Book meeting room".',
           '"Delete Task" now says exactly: Are you sure you want to delete "Book meeting room"? '
           'This cannot be undone. A is not used as the new confirmation target.'),
          ('Click "Confirm Delete"; inspect JSON.',
           '"Task deleted successfully."; only b-beta is removed. A and C equal bBefore.')]),
    case(39, 'Repeated cancellation then one confirmed deletion',
         'State Transition - confirmation -> cancel -> confirmation -> cancel -> confirmation -> removed',
         'REQ-B-011 REQ-B-012 REQ-B-013 REQ-B-014', [OPEN_DELETE,
          ('Click "Cancel"; reopen A Delete; press Escape; reopen A Delete.',
           'Both dismissals retain all original objects; each reopened dialog contains exactly ' + PROMPT),
          ('Click "Confirm Delete" once; inspect JSON and reload.',
           DELETED + ' There is no second pending deletion dialog.')]),
    case(40, 'Consecutive deletions never reuse old target',
         'State Transition - three saved -> A removed -> B removed',
         'REQ-B-011 REQ-B-012 REQ-B-014', [OPEN_DELETE,
          ('Confirm Delete A, then click "Delete Book meeting room".',
           'First toast "Task deleted successfully."; second dialog warns exactly: '
           'Are you sure you want to delete "Book meeting room"? This cannot be undone.'),
          ('Click "Confirm Delete" on B; observe toast; inspect JSON; reload.',
           'Second "Task deleted successfully."; only fixture C remains, identical field-for-field to bBefore C; '
           'both b-alpha and b-beta are absent.')], importance=3),
    case(41, 'Canceled edit does not contaminate subsequent deletion',
         'State Transition - dirty editing -> canceled -> deletion confirmation -> removed',
         'REQ-B-008 REQ-B-011 REQ-B-012 REQ-B-014', [OPEN_EDIT,
          ('Replace title with "Unsaved deletion title"; click "Cancel"; click "Delete Prepare sprint review".',
           '"Delete Task" shows exactly ' + PROMPT + ' The abandoned title is not used.'),
          ('Click "Confirm Delete"; inspect JSON and reload.', DELETED)]),
]

SUITES = [
    {'name': 'TS-B1 - Prefilled editing and committed changes',
     'details': '18 independent manual cases; valid/rejected edits, atomicity, identity/timestamps, '
                'latest-value/target isolation and priority persistence. Representative invalid text inputs '
                'exercise edit rejection; A owns comprehensive text boundaries; C owns enum/date semantics.',
     'cases': EDIT_CASES},
    {'name': 'TS-B2 - Editing cancellation and draft isolation',
     'details': '9 independent manual cases; Cancel, Close X, Escape, dark backdrop, invalid/unchanged '
                'drafts, clean reopening, interior hit testing and abandoned priority changes. '
                'Dialog focus/navigation accessibility is owned by E.', 'cases': CANCEL_CASES},
    {'name': 'TS-B3 - Deletion confirmation and repeated targeting',
     'details': '14 independent manual cases; exact current-title warning, confirm, all four dismissal '
                'paths, interior click, sole/duplicate-title task identities, repeated/mixed operations. '
                'No execution or passing result is implied.', 'cases': DELETE_CASES},
]
