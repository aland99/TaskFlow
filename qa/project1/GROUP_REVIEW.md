# Final group integration review - 27 October 2026

Leader: Aland Karwan. Course: SECJ3343. Software baseline: TaskFlow main@5133a6c.
This records design review and TestLink integration, not execution of all cases.

## Actual contributions

The original prompts inferred names from GitHub. Actual submitted letters take precedence
over the provisional named-prompt roster. Original PR history and author logins are preserved.

| Area | Member | Author login | Merged PR | Cases | Requirements |
|---|---|---|---|---:|---:|
| A: Creation/text validation | Aland Karwan | aland | Leader baseline | 43 | 14 |
| B: Editing/deletion | Mhamad | mhammedazad | https://github.com/aland99/TaskFlow/pull/1 | 41 | 14 |
| C: Status/dates/counts | Lanya Faraidun | lanya | https://github.com/aland99/TaskFlow/pull/2 | 41 | 8 |
| D: Search/filters/sorting | Ahmed | ahmed | https://github.com/aland99/TaskFlow/pull/3 | 40 | 14 |
| E: Storage/navigation/accessibility | Rasan soran | rasan | https://github.com/aland99/TaskFlow/pull/4 | 38 | 13 |

Case/requirement IDs and areas are retained. Human display names replace username fallbacks
where the user supplied them. Original member quality notes are historical environment
records; regenerated PDFs and final audit records supersede their earlier limitations/counts.

## Scoped review corrections

- Shared audit: accept stable IDs in both `TC-D-NNN Title` and `TC-A-NNN - Title` names.
- D: correct the billing/status/priority decision table. In Progress/Low yields the search
  no-result message; To Do/High matches Alpha Planning. Remove the description requirement
  link from a title-only punctuation case. Exercise title-only, description-only and both-field
  OR matches without duplicate cards. Remove literal backslashes from quoted expected messages.
- E: fix copyable JavaScript/JSON escaping, replace invalid one-character fixture titles,
  and correct backup/reset behavior: loading corrupt `not-json` replaces the old backup;
  reset keeps the newly created `not-json` backup. Complete exact singular warning text.
  Clarify id-type partitions, missing-field normalization, reset-failure and autofocus setups.
- C: start valid-status selections from a different state so native change fires, specify
  old timestamps, document a page-local fixed clock and add actual before/at/after midnight
  values. Clarify EP/Use Case labels where BVA did not describe the original test.
- Repair requirement-specification expected totals through the existing local loader, so
  the member environment's aggregate N/A display does not carry into final PDFs.
- Rasan's environment could not run TestLink/Chrome. Load his own authored data under his
  account here and generate both PDFs and XML exports on the leader laptop.

Targeted checks verified corrected query, backup/reset and Baghdad-midnight expectations
against the actual TaskFlow utilities. All five modules pass structural validation.
No application source files were changed during integration.

## Coverage of the original documented basis

The following use the full `REQ-<letter>-NNN` prefixes, abbreviated here for readability:

| README basis | Derived requirements |
|---|---|
| TF-REQ-001/002/003 | A-001 through A-005 |
| TF-REQ-004/005 | A-006 defaults; C-001/C-002/C-003 |
| TF-REQ-006 | C-005 through C-008 |
| TF-REQ-007/008 | A-007 through A-010 |
| TF-REQ-009/010/011 | B-001 through B-007 |
| TF-REQ-012 | B-008 through B-010 |
| TF-REQ-013/014/015 | B-011 through B-014 |
| TF-REQ-016/017 | C-003/C-004/C-007 |
| TF-REQ-018 | B-006; C-001; D-006 |
| TF-REQ-019 | D-001 through D-007; D-013/D-014 |
| Additional sorting/results/empty-state notes | D-008 through D-012 |
| Storage/recovery notes | E-001 through E-008 |
| Navigation/responsive behavior | E-009 through E-011 |
| Dialog/toast behavior and accessibility | E-012/E-013 |

## Final evidence

Final database totals: **203 cases, 63 requirements, 17 suites, 515 steps, 361 active
requirement-to-case links**. Every requirement is covered; every case is mapped; all
203 cases are assigned to their authors. Zero execution results are recorded.

`final/group-audit.json`, the mapping CSV and the bidirectional matrix come from the
actual database/req_coverage table. Combined and individual case/basis reports originate
from authenticated TestLink printDocument.php and Chrome printing. The final PDF text,
geometry and rendered-page checks are recorded in `final/pdf-verification.json`.

The package includes three combined PDFs, ten individual PDFs, ten member XML files,
the committed README/code source PDFs and verification records. The lecturer's existing
assigned project has not been accessed and no university upload is claimed.
