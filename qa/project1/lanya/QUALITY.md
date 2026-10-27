# Lanya Faraidun — Member C quality and coverage evidence

## Design summary

- Author: Lanya Faraidun (`lanya`), submitted as assigned slot C.
- Baseline: TaskFlow `main@5133a6c`.
- Designed: 41 manual cases in four suites; 2 SRS specifications; 8 requirements (`REQ-C-001` through `REQ-C-008`). All eight requirements map to cases and every case maps to an in-scope requirement (100% bidirectional mapping; 61 requirement-to-case links).
- Scope: priority/status partitions; all six directed status transitions and same-state behavior; summary totals under filters; Completed styling and overdue exemption; optional/valid/invalid dates; native date sanitization versus validator rejection; leap/calendar boundaries; fixed local yesterday/today/tomorrow decision table; date formatting.
- Fixed date basis: 2026-10-27 12:00 Asia/Baghdad (UTC+03:00). Harness cases construct the date explicitly so they remain repeatable after October 2026.
- README roster currently lists Lanya as B and Mhamad as C; this submission follows the user's direct assignment of Member 3/letter C and the authenticated GitHub profile name. Shared `team.json` was not changed; leader should reconcile roster labels.

## Checks actually completed

- `python3 -I qa/testlink/scripts/validate.py lanya`: passed; 2 specifications, 8 requirements, 4 suites, 41 cases, 8/8 requirements covered.
- `pnpm install` and `pnpm run build`: completed; Vite production build passed.
- `git diff --check`: passed.
- `gh auth status`: authenticated as `LanyaaFaraidun`; `origin` is the personal fork and `upstream` is `aland99/TaskFlow`; work branch is `codex/project1-member-c`.
- Docker Desktop 29.9.2 running; `bash qa/testlink/setup.sh` completed using local port 8090. TaskFlow dev server was run on `http://localhost:5173/`.
- TestLink import/audit: local Project 1, plan `Project 1 - Test Case Design`, build `TaskFlow main@5133a6c`; the local `lanya` account is Lanya Faraidun with Senior Tester role. All 41 cases are authored by that account and assigned to the plan; 8/8 requirements covered by 61 mapping rows. No executions are recorded.
- Generated TestLink outputs: 41 cases in XML, 8 requirements in XML, case report PDF (45 pages), requirements basis PDF (10 pages). Poppler metadata and rendered PNGs were inspected, including first/middle/last pages and date boundary, sanitization, rejection, and decision-table pages; the inspected pages were legible and unclipped.
- Windows adaptation: the stock report script expects a macOS Chrome path. Used an uncommitted scratch wrapper to point the report renderer at installed Windows Chrome and keep the two specification documents separated in the PDF. Shared report tooling was not modified.

## Execution status and limitations

These are designed manual cases, not execution results. No case is marked Passed; TestLink execution count is zero and all cases remain Not Run. The lecturer's existing project was not accessed or changed; this is a local preparation package for import into the assigned project. The browser control's saved permission/managed policy denied access to `http://localhost:5173/` even after the user authorized it in chat, so no live UI screenshots or visual browser review were made; no alternate browser-control workaround was attempted. TestLink and generated PDFs/XML are local preparation evidence only.
