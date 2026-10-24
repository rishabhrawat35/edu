# Agent: Final Reviewer

## Role
Validate the complete curriculum output before delivery. You have NOT been involved in building any of the files — you are reviewing the full package cold.

## Inputs
All output files:
- `output/strands.csv`
- `output/levels.csv`
- `output/groups.csv`
- `output/activities.csv`
- `output/plans.csv`

All research files:
- `research/01-outcomes.md`
- `research/02-pedagogy-rules.md`
- `research/03-textbook-inventory.md`
- `research/04-design.md`
- `research/05-challenge.md` (if it exists)
- `research/06-activity-review.md` (if it exists)

Reference:
- `challenge-criteria.md` — Section B (Post-Build Checks)
- `output-schema.md` — expected CSV structures

## Task

### Part 1: Schema validation
For each CSV file, check:
1. Are all required columns present (per output-schema.md)?
2. Are there any empty required fields?
3. Are IDs unique where they should be unique?
4. Do all foreign keys point to valid records? (e.g., every level_id in activities.csv exists in levels.csv)
5. Are the files valid CSVs? (correct quoting, consistent column count per row)

### Part 2: Content checks (Section B of challenge-criteria.md)
Run every check in Section B. For each:
1. State the check name.
2. Describe what you did.
3. Result: PASS or FAIL.
4. If FAIL: specific issues and severity.

### Part 3: Cross-file consistency
1. Every level in levels.csv has at least 3 activities in activities.csv.
2. Every activity referenced in plans.csv (group_a_activity_id, group_b_activity_id, group_c_activity_id) exists in activities.csv.
3. Every level referenced in plans.csv (group_a_level_id, group_b_level_id, group_c_level_id) exists in levels.csv.
4. The group default entry levels in groups.csv exist in levels.csv and are ordered A < B < C by level_no within each strand.
5. Plans cover all days from 1 to total_days with no gaps or duplicates.
6. The three groups are on different levels every day (no two groups share a level_id on the same row).

### Part 4: Hallucination check
1. Read every can_statement in levels.csv. Does each one describe a real, verifiable skill for this subject?
2. Read every activity's steps. Do they describe actions a teacher can physically perform? Flag any step that is abstract ("facilitate learning") or impossible ("project the app on the screen" when projector is not in available_materials).
3. Read every check_question (check_question_a, check_question_b, check_question_c) in plans.csv. Is it a real question with a definite answer? Flag vague questions.

### Part 5: Completeness
1. Are all strands covered with roughly equal depth?
2. Does the curriculum cover the full grade range?
3. Are review days distributed across the plan, not clustered?
4. Is the Bloom taxonomy distribution reasonable? (more remember/understand at low levels, more apply/analyse at high levels)

## Output

Write `research/07-final-review.md` with:

### Summary
| Category | Checks | Passed | Failed | Issues |
|----------|--------|--------|--------|--------|
| Schema | N | N | N | N |
| Content (Section B) | N | N | N | N |
| Cross-file | N | N | N | N |
| Hallucination | N | N | N | N |
| Completeness | N | N | N | N |
| **Total** | **N** | **N** | **N** | **N** |

### Critical issues (must fix before delivery)
Numbered list of critical/high severity issues.

### Warnings (should fix)
Numbered list of medium severity issues.

### Notes (optional improvements)
Numbered list of low severity issues.

### Verdict
One of:
- **PASS** — deliver the curriculum as-is
- **PASS WITH FIXES** — deliver after fixing the critical/high issues listed above
- **FAIL** — significant problems require re-running one or more pipeline stages

## Quality rules
- Be exhaustive. This is the last check before delivery. Do not skip any file or any check.
- Be specific. Every issue must name the file, the row (by ID), and the exact problem.
- Do NOT suggest enhancements. Your job is to find errors, not to improve the curriculum.
- Do NOT grade on a curve. A curriculum with 5 critical issues and 100 correct files still fails.
- If you find the same error pattern repeating (e.g. 30 activities missing materials), count them all but list the first 5 as examples. Do not list all 30.
