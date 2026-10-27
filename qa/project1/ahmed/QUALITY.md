# Member D quality and evidence

**Author:** AhmedAzad240358 (GitHub CLI name is still unavailable; `git config user.name` fallback)  
**Slot:** Member 4, letter D  
**Source baseline:** TaskFlow main@5133a6c  
**Design status:** Manual test design; all cases are Not Run.

## Design inventory

- 40 designed cases in 4 suites, spanning 14 requirements for search, status/priority filters, sorting, result counts, empty-state precedence, and clear actions.
- Structural and imported traceability both cover 14/14 requirements (100%); the local TestLink database has 81 designed requirement-to-case links.
- Independent six-task fixtures use distinct creation timestamps, due-date ties, and undated records; explicit one-task and zero-task boundaries are included.
- Local TestLink records 40 cases, 57 steps, all cases by author `ahmed`, all assigned to the Project 1 plan, and zero executions. No case is reported Passed.

## Checks and report review

- `python -I qa/testlink/scripts/validate.py ahmed` — passed: 40 cases, 4 suites, 14 requirements, 100% structural traceability.
- `qa/testlink/setup.sh` — completed with Docker Desktop/WSL2 on local port 8090. Windows required invoking the checked-in Bash setup via bundled Git Bash/Python, and copying the existing overlay contents into the generated ignored app directory because of Windows `cp -R` behavior. No shared setup script was changed.
- `python -I qa/testlink/scripts/load.py ahmed` — completed: 14 requirements, 40 cases, plan assigned.
- Database audit — confirmed 40 imported cases, 57 steps, 81 expected links, all authored by `ahmed`, all in plan, 0 executions. The checked-in audit script's name split mishandles case names containing ` - `; its parsing correction was applied only in memory, leaving shared tooling untouched. Results and traceability matrix are in `quality.json` and `traceability.csv`.
- TestLink-generated PDFs and XML exports are included. Both PDFs are A4; the case report is 32 pages and the requirements report is 9 pages. Visually checked first, middle, and last pages of both reports, including multi-step fixture content. XML parsing is recorded in evidence after generation.
- `report.py` hardcodes a macOS Chrome path; it ran with an in-memory Windows Chrome path substitution. No shared report script was changed.
- TaskFlow Vite dev server returned HTTP 200 at `http://127.0.0.1:5173/`. App interaction through a dedicated disposable Chrome profile was not completed; the Windows computer-use approval was rejected. Test cases remain Not Run.
- `npm install` completed with 20 packages added and 0 reported vulnerabilities; generated `package-lock.json` changes were restored.

## External submission status

- GitHub CLI authentication is still pending in the workspace's saved config. No fork, commit, push, or pull request has been created. After the user completes the current `gh auth login` device approval, the fork/PR steps remain.
- Only the local TestLink environment was used. No new project was created on the lecturer's server and no lecturer-server import was attempted.
