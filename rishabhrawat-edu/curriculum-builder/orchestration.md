# Orchestration Model

How to run the curriculum-building pipeline: which agents, in what order, what each one reads and writes, and where parallelism is safe.

## Pipeline overview

```
Stage 1: Research          3 agents in parallel     →  research/*.md
Stage 2: Design            1 agent                  →  output/strands.csv, levels.csv, groups.csv
Stage 3: Challenge          1 agent                  →  research/05-challenge.md (+ fixes to Stage 2 output)
Stage 4: Activities         N agents in parallel     →  output/activities.csv
Stage 5: Activity Review    1 agent                  →  output/activities.csv (reviewed), research/06-activity-review.md
Stage 6: Plans              1 agent                  →  output/plans.csv
Stage 7: Final Review       1 agent                  →  research/07-final-review.md
Stage 8: Package            1 script or agent        →  merged CSVs, updated docs
```

N = the number of strands (typically 3-6). Each parallel agent handles one strand.

## Stage dependencies

```
Stage 1 ──→ Stage 2 ──→ Stage 3 ──→ Stage 4 ──→ Stage 5 ──→ Stage 6 ──→ Stage 7 ──→ Stage 8
  (parallel)                          (parallel)
```

- Stages 1 and 4 can run their internal agents in parallel.
- Stage 6 (Plans) is a single agent because all strands are interleaved in one plans.csv.
- Every other stage must wait for the previous stage to finish.
- Stage 3 (Challenge) may send fixes back to Stage 2. If it does, Stage 2 reruns with the fixes before proceeding.

## State tracking

Use a `state.json` file in the project root to track which stages have completed. Format:

```json
{
  "subject": "Mathematics",
  "subject_code": "MATH",
  "created": "2026-10-24T09:00:00Z",
  "stages": {
    "1_research": { "status": "complete", "completed_at": "2026-10-24T09:15:00Z" },
    "2_design": { "status": "complete", "completed_at": "2026-10-24T09:30:00Z" },
    "3_challenge": { "status": "complete", "completed_at": "2026-10-24T09:35:00Z", "issues_found": 2, "issues_fixed": 2 },
    "4_activities": { "status": "complete", "completed_at": "2026-10-24T10:00:00Z", "activity_count": 172 },
    "5_activity_review": { "status": "complete", "completed_at": "2026-10-24T10:15:00Z", "fixes_applied": 20 },
    "6_plans": { "status": "complete", "completed_at": "2026-10-24T10:45:00Z", "plan_days": 150 },
    "7_final_review": { "status": "complete", "completed_at": "2026-10-24T10:50:00Z", "issues_found": 0 },
    "8_package": { "status": "complete", "completed_at": "2026-10-24T10:55:00Z" }
  }
}
```

If a stage fails or is interrupted, it can be rerun without affecting earlier stages. The state file tells the orchestrator where to resume.

---

## Detailed stage specifications

### Stage 1: Research (3 agents, parallel)

**Purpose:** Extract raw material from the source documents.

| Agent | Prompt file | Input | Output | Time estimate |
|---|---|---|---|---|
| Outcomes researcher | `agent-prompts/01-outcomes-researcher.md` | Official learning outcomes document, foundational goals document | `research/01-outcomes.md` | 10-15 min |
| Pedagogy researcher | `agent-prompts/02-pedagogy-researcher.md` | Teaching methodology article, any pedagogy references | `research/02-pedagogy-rules.md` | 10-15 min |
| Textbook researcher | `agent-prompts/03-textbook-researcher.md` | All textbooks (or chapter listings) | `research/03-textbook-inventory.md` | 10-20 min |

All three agents run at the same time. They read from `sources/` and write to `research/`. They do not read each other's output.

**Completion gate:** All three files exist and are non-empty.

### Stage 2: Design (1 agent)

**Purpose:** Build the strand-level-group structure from the research.

| Agent | Prompt file | Input | Output | Time estimate |
|---|---|---|---|---|
| Curriculum designer | `agent-prompts/04-curriculum-designer.md` | All three research files, user's strand suggestions (if any), input schema | `output/strands.csv`, `output/levels.csv`, `output/groups.csv`, `research/04-design.md` | 15-20 min |

This agent reads all three research outputs and produces the structural CSVs. It also writes a design rationale explaining its choices.

**Completion gate:** strands.csv has 3-6 rows. levels.csv has 40-60 rows. groups.csv has one row per group (typically 3: A, B, C) with default entry levels per strand. All foreign keys resolve.

### Stage 3: Challenge (1 agent)

**Purpose:** Catch errors in the design before activities are built on top of it.

| Agent | Prompt file | Input | Output | Time estimate |
|---|---|---|---|---|
| Challenger | `agent-prompts/05-challenger.md` | All research files + all Stage 2 CSVs | `research/05-challenge.md` | 5-10 min |

This agent has not seen the design agent's work before. It checks the design against the criteria in `challenge-criteria.md` (Section A: Post-Design checks).

If the challenger finds issues, it writes them to `05-challenge.md`. The orchestrator then sends these issues to the design agent for fixing. The design agent updates the CSVs and the challenger re-checks. This loop runs at most 2 times; if issues persist after 2 rounds, they are flagged for human review.

**Completion gate:** `05-challenge.md` exists and either says "all checks pass" or lists only issues marked "for human review."

### Stage 4: Activities (N agents, parallel)

**Purpose:** Write teaching activities for every level.

| Agent | Prompt file | Input | Output | Time estimate |
|---|---|---|---|---|
| Activity writer (one per strand) | `agent-prompts/06-activity-writer.md` | `output/levels.csv` (filtered to this strand), `research/02-pedagogy-rules.md`, classroom constraints from input schema | `output/activities-{STRAND}.csv` | 10-15 min each |

Each agent handles one strand and writes 3-4 activities per level in that strand. Agents run in parallel and do not read each other's output.

**Completion gate:** Every level_id in levels.csv has at least 3 activity rows. No activity uses materials from the unavailable list.

### Stage 5: Activity Review (1 agent)

**Purpose:** Review all activities from a teacher's perspective.

| Agent | Prompt file | Input | Output | Time estimate |
|---|---|---|---|---|
| Activity reviewer | `agent-prompts/07-activity-reviewer.md` | All activities-{STRAND}.csv files merged into activities.csv, classroom constraints | `output/activities.csv` (reviewed), `research/06-activity-review.md` | 15-20 min |

This agent reads the merged activities file and checks every activity for: accuracy, material feasibility, time realism, duplicates, gaps, progression, language, and pedagogy rule compliance. It writes a report listing all issues found with suggested fixes.

If the reviewer finds issues, the orchestrator sends them back to the activity writer agents for fixing (same loop pattern as Stage 3). Each strand's activity writer fixes only its own activities. The reviewer re-checks after fixes. This loop runs at most 2 times; remaining issues are flagged for human review.

**Completion gate:** `activities.csv` has at least 3 rows per level. `06-activity-review.md` exists with a summary of issues and their status (fixed or flagged for human review).

### Stage 6: Plans (1 agent)

**Purpose:** Build the day-numbered baseline plan (typically 150 days).

| Agent | Prompt file | Input | Output | Time estimate |
|---|---|---|---|---|
| Plan builder | `agent-prompts/08-plan-builder.md` | `output/levels.csv`, `output/groups.csv`, `output/activities.csv`, `research/02-pedagogy-rules.md`, input schema (total_days, period_minutes) | `output/plans.csv` | 20-30 min |

One agent builds all plans because strands are interleaved day by day (each day the whole room works on one strand). The plan builder assigns one strand per day, cycles through all strands proportionally, and ensures the three groups are always on different levels of that day's strand.

**Completion gate:** plans.csv has the expected number of rows (total_days). Every activity_id referenced exists in activities.csv. The three groups are on different levels every day.

### Stage 7: Final Review (1 agent)

**Purpose:** Validate the complete output.

| Agent | Prompt file | Input | Output | Time estimate |
|---|---|---|---|---|
| Final reviewer | `agent-prompts/09-final-reviewer.md` | All output CSVs, all research files, challenge-criteria.md (Section B) | `research/07-final-review.md` | 5-10 min |

This agent runs the Post-Build checks from `challenge-criteria.md`.

**Completion gate:** `07-final-review.md` exists. All checks pass or issues are flagged for human review.

### Stage 8: Merge and Package (1 script or agent)

**Purpose:** Merge per-strand activity files into the final combined CSV and update documentation.

Tasks:
1. Merge all `activities-{STRAND}.csv` into one `activities.csv` (if not already done in Stage 5).
2. Extract the first 5 days from `plans.csv` into `sample-week.csv`.
3. Update `state.json` to mark all stages complete.
4. Generate or update `docs/index.md` with file counts and quality notes.

This can be a simple script rather than an AI agent.

---

## Error handling

| Situation | Action |
|---|---|
| A source document is unreadable (password-protected, corrupted) | Skip it. Note in state.json which sources were used. If the learning outcomes document is unreadable, the pipeline cannot proceed — ask the user for an alternative. |
| An agent produces empty output | Rerun the agent once. If still empty, flag for human review. |
| The challenger finds critical issues (broken prerequisite chains, missing entry levels) | Send issues to the design agent for fixing. Rerun challenger. Max 2 loops. |
| The challenger finds minor issues (bloom tag suggestions, pacing advice) | Note them in the challenge report. Do not block the pipeline. |
| An activity references unavailable materials | The activity reviewer (Stage 5) catches this. Replace the material or rewrite the activity. |
| Plans reference activity_ids that do not exist | The final reviewer (Stage 7) catches this. Replace with valid activity_ids for the same level. |
| A stage is interrupted (timeout, crash) | The state file tracks which stages completed. Rerun from the last incomplete stage. |

---

## Resource estimates

| Subject complexity | Strands | Levels | Activities | Total agent time | Total wall-clock time (with parallelism) |
|---|---|---|---|---|---|
| Simple (3 strands, 30 levels) | 3 | 30 | ~100 | ~90 min | ~45 min |
| Standard (5 strands, 57 levels) | 5 | 57 | ~170 | ~150 min | ~60 min |
| Complex (6 strands, 60 levels) | 6 | 60 | ~200 | ~180 min | ~75 min |

Human review of activities adds 2-4 hours on top, depending on the subject.
