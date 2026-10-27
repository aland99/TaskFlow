# Rasan Soran — Member E design quality record

Baseline: TaskFlow `main@5133a6c`; SECJ3343 Project 1, Group TaskFlow.

## Design inventory

- 38 designed manual cases (`TC-E-001` through `TC-E-038`) in three suites.
- 13 derived requirements (`REQ-E-001` through `REQ-E-013`) in `SRS-E-STORAGE-NAV-A11Y`.
- Structural requirements-to-case mapping is 100% bidirectional (13/13); every case maps to at least one requirement.
- Techniques include EP, BVA, Decision Table, State Transition, Use Case and Error Guessing.
- Scope excludes A creation/text limits/draft cancellation, B editing/deletion, C enums/dates/status/counts, and D querying.
- `traceability.csv` is the structural mapping from this module; it is not an imported TestLink `req_coverage` audit.

## Checks and evidence actually available

1. `python3 -I qa/testlink/scripts/validate.py rasan` passed: 1 specification, 13 requirements, 3 suites, 38 cases, 13/13 covered.
2. Python 3.13 and Poppler 25.03.0 are present. Git 2.47.3 and GitHub CLI 2.103.3 are available; `gh auth status` succeeded as Rasan21.
3. TaskFlow Vite dev server started at `http://localhost:5173` using bundled Node.js and pnpm dependencies. No browser UI was exercised.
4. `bash qa/testlink/setup.sh` stopped at its macOS-only `open -a Docker` command (`xdg-open: unexpected option '-a'`). The Docker CLI exists but cannot access `/var/run/docker.sock`; Docker Desktop is not available in this Linux environment.
5. The in-app browser explicitly denied permission to open `http://localhost:5173`; it instructed not to retry through another browser or workaround.
6. `python3 -I qa/testlink/scripts/load.py rasan` could not query the TestLink database because Docker Compose could not connect to its daemon. `report.py rasan` could not connect to local TestLink at port 8090.

## Deliverables not produced here

No TestLink user/project/plan/build, imported cases, author/count/link audit, requirements/test suites XML export, TestLink-generated PDFs, visual PDF review or browser execution evidence exists from this run. These require the local TestLink database and browser permission. The lecturer's existing assigned project was not touched. No execution or peer-review results are claimed.


## Leader integration, 27 October 2026

The original environment notes above are historical. All five members were loaded and audited on the leader laptop, and individual PDFs/XML were regenerated after scoped design review. Final authoritative counts/mappings and PDF verification are in ../final/group-audit.json and ../final/pdf-verification.json; review corrections are documented in ../GROUP_REVIEW.md. Original author login and stable IDs are preserved. No full manual execution or passing results are claimed.
