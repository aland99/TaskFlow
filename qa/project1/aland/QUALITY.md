# Aland Karwan - design and verification record

Baseline: TaskFlow main@5133a6c. Course SECJ3343. Group TaskFlow. Member 1, area A.

## Design inventory

- 43 original manual test cases, stable IDs TC-A-001 through TC-A-043.
- 14 testable requirements REQ-A-001 through REQ-A-014, in SRS-A-CREATE.
- 3 suites: TS-A1 (16 cases), TS-A2 (9), TS-A3 (18).
- Techniques used: EP, BVA, Decision Table, State Transition, Use Case and Error Guessing.
- Title boundaries 0/1/2/3/4/79/80/81; description 0/1/499/500/501.
- Padded text, emoji code-point limits, combining sequences, literal markup, duplicate titles,
  all four draft dismissal paths, live error recovery, simultaneous invalid fields and first-invalid focus.

## Actual TestLink audit

`python3 -I qa/testlink/scripts/audit.py aland` compares the design to the database, rather than
assuming a successful import means complete coverage. Results are in `quality.json` and `traceability.csv`:

- 43 cases authored by `aland`, 149 steps.
- 95 active requirement-to-test links, exactly matching the authored mappings.
- 14/14 requirements covered; every case maps to one or more known requirements.
- All 43 cases in the Project 1 plan and assigned to Aland for the build TaskFlow main@5133a6c.
- Zero execution rows. These are designed cases, not claims that all cases have passed.
- Requirements and specification metadata identify Aland as designer. The initial toolkit-assisted
  admin import metadata was explicitly reassigned to the actual designer by the loader.
- Repeated loader runs preserved 43 cases and repaired the interrupted first Unicode import.

## Checks actually performed

1. Read the complete root README, source utilities/components/CSS and the lecturer's Project 1/tutorial slides.
2. Existing `npm test`: **23 checks passed**. `npm run build`: **passed** after locally repairing the missing
   Intel-native optional Rolldown package, without adding it to package.json. The pre-existing package-lock.json
   change was preserved and excluded from the QA commit.
3. Browser: signed in to local TestLink as admin and inspected the 43-case suite tree and all three suite counts.
4. TaskFlow browser smoke checks: empty form defaults; required-title error and autofocus; live two-character
   title rejection; 81-emoji title rejection/count; padded three-character title accepted/count; 501-character
   description rejection; correction to padded 500-character description; successful creation/toast; card retained
   after reload. These are a limited smoke check, not a full 43-case execution run.
5. Generated the case report and basis through TestLink's logged-in printDocument.php, then printed with Chrome.
   Exported the real TestLink testsuites XML (43 cases) and requirements XML.
6. Opened rendered report pages and inspected representative first/middle/last pages, emoji, 499/500-character
   data, validation steps and related-case mappings. Fixed clipped strings by wrapping, applied A4 and page numbers.
   All report pages were rendered for review. Final case report: **49 pages**. Test basis: **8 pages**.
7. Final PDF extraction finds all 43 stable case IDs and all 14 requirement IDs in both documents, with page numbers
   present on the last page. Geometric inspection found no text outside the page bounds. `pdf-review.json` records
   these checks. The specification's total coverage displays **100% (14/14)**.
8. Saved committed README and source implementation snapshots as PDFs under `../Source_Documents/` and visually
   reviewed source pages. These preserve source material and supplement the TestLink-generated requirements basis.

## Limits and handoff

Only Aland's area is authored here. Members B-E must independently review/write their own requirements/cases
and open their own PRs. Placeholder names remain until their modules arrive; the loader resolves real names
into report headers. No lecturer-server import or university submission has occurred. The slides require using
the lecturer's **existing assigned project**, so import the XML there and check its prefix and mappings before submission.

The final combined PDFs, database-derived traceability matrix PDF and group submission zip are intentionally
deferred until the leader says **members are done** and the four member PRs have been reviewed and merged.


## Leader integration, 27 October 2026

The original environment notes above are historical. All five members were loaded and audited on the leader laptop, and individual PDFs/XML were regenerated after scoped design review. Final authoritative counts/mappings and PDF verification are in ../final/group-audit.json and ../final/pdf-verification.json; review corrections are documented in ../GROUP_REVIEW.md. Original author login and stable IDs are preserved. No full manual execution or passing results are claimed.
