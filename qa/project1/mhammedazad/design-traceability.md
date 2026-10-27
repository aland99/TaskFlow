# Member B design traceability

**Declared mappings only. Actual TestLink database audit is pending Docker setup.**

14/14 requirements have designed coverage; all 41 cases have requirement references; 83 declared links.

| Requirement | Requirement title | Cases |
|---|---|---|
| REQ-B-001 | Prefill the selected task for editing | TC-B-001, TC-B-002, TC-B-009, TC-B-010, TC-B-025, TC-B-029 |
| REQ-B-002 | Commit a valid edit atomically to the selected task | TC-B-003, TC-B-004, TC-B-005, TC-B-006, TC-B-007, TC-B-008, TC-B-016, TC-B-017, TC-B-029 |
| REQ-B-003 | Preserve identity and creation timestamp while advancing update time | TC-B-003, TC-B-004, TC-B-005, TC-B-006, TC-B-007, TC-B-008, TC-B-009, TC-B-016, TC-B-017, TC-B-018 |
| REQ-B-004 | Reject invalid edits without any partial commit | TC-B-011, TC-B-012, TC-B-013, TC-B-014, TC-B-015, TC-B-016, TC-B-023 |
| REQ-B-005 | Recover a rejected edit and commit only the corrected values | TC-B-016 |
| REQ-B-006 | Persist priority edits through the edit workflow | TC-B-005, TC-B-017, TC-B-018 |
| REQ-B-007 | Apply repeated edits and target only the selected identity | TC-B-008, TC-B-009, TC-B-010, TC-B-018 |
| REQ-B-008 | Discard editing through every supported dismissal path | TC-B-019, TC-B-020, TC-B-021, TC-B-022, TC-B-023, TC-B-024, TC-B-025, TC-B-027, TC-B-041 |
| REQ-B-009 | Reopening a canceled edit discards draft and validation state | TC-B-019, TC-B-020, TC-B-021, TC-B-022, TC-B-025, TC-B-027 |
| REQ-B-010 | Interior modal interaction is not backdrop dismissal | TC-B-026, TC-B-037 |
| REQ-B-011 | Show exact deletion confirmation for the current target | TC-B-028, TC-B-029, TC-B-030, TC-B-032, TC-B-037, TC-B-038, TC-B-039, TC-B-040, TC-B-041 |
| REQ-B-012 | Confirm deletion of only the intended task | TC-B-030, TC-B-031, TC-B-032, TC-B-039, TC-B-040, TC-B-041 |
| REQ-B-013 | Cancel deletion through every supported dismissal path | TC-B-033, TC-B-034, TC-B-035, TC-B-036, TC-B-037, TC-B-038, TC-B-039 |
| REQ-B-014 | Keep deletion targets correct across repeated and mixed operations | TC-B-038, TC-B-039, TC-B-040, TC-B-041 |

## Case-to-requirement direction

| Stable case ID | Requirement references |
|---|---|
| TC-B-001 | REQ-B-001 |
| TC-B-002 | REQ-B-001 |
| TC-B-003 | REQ-B-002, REQ-B-003 |
| TC-B-004 | REQ-B-002, REQ-B-003 |
| TC-B-005 | REQ-B-002, REQ-B-003, REQ-B-006 |
| TC-B-006 | REQ-B-002, REQ-B-003 |
| TC-B-007 | REQ-B-002, REQ-B-003 |
| TC-B-008 | REQ-B-002, REQ-B-003, REQ-B-007 |
| TC-B-009 | REQ-B-001, REQ-B-003, REQ-B-007 |
| TC-B-010 | REQ-B-001, REQ-B-007 |
| TC-B-011 | REQ-B-004 |
| TC-B-012 | REQ-B-004 |
| TC-B-013 | REQ-B-004 |
| TC-B-014 | REQ-B-004 |
| TC-B-015 | REQ-B-004 |
| TC-B-016 | REQ-B-002, REQ-B-003, REQ-B-004, REQ-B-005 |
| TC-B-017 | REQ-B-002, REQ-B-003, REQ-B-006 |
| TC-B-018 | REQ-B-003, REQ-B-006, REQ-B-007 |
| TC-B-019 | REQ-B-008, REQ-B-009 |
| TC-B-020 | REQ-B-008, REQ-B-009 |
| TC-B-021 | REQ-B-008, REQ-B-009 |
| TC-B-022 | REQ-B-008, REQ-B-009 |
| TC-B-023 | REQ-B-004, REQ-B-008 |
| TC-B-024 | REQ-B-008 |
| TC-B-025 | REQ-B-001, REQ-B-008, REQ-B-009 |
| TC-B-026 | REQ-B-010 |
| TC-B-027 | REQ-B-008, REQ-B-009 |
| TC-B-028 | REQ-B-011 |
| TC-B-029 | REQ-B-001, REQ-B-002, REQ-B-011 |
| TC-B-030 | REQ-B-011, REQ-B-012 |
| TC-B-031 | REQ-B-012 |
| TC-B-032 | REQ-B-011, REQ-B-012 |
| TC-B-033 | REQ-B-013 |
| TC-B-034 | REQ-B-013 |
| TC-B-035 | REQ-B-013 |
| TC-B-036 | REQ-B-013 |
| TC-B-037 | REQ-B-010, REQ-B-011, REQ-B-013 |
| TC-B-038 | REQ-B-011, REQ-B-013, REQ-B-014 |
| TC-B-039 | REQ-B-011, REQ-B-012, REQ-B-013, REQ-B-014 |
| TC-B-040 | REQ-B-011, REQ-B-012, REQ-B-014 |
| TC-B-041 | REQ-B-008, REQ-B-011, REQ-B-012, REQ-B-014 |
