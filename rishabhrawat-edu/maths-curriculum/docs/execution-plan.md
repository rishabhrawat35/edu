# Execution Plan: Build an Integrated Multi-Grade Curriculum

## What this plan produces

A complete, level-based curriculum for one subject (e.g. maths, language, EVS) that a single teacher can use in a multi-grade, multi-level (MGML) classroom with grades 1 to 5. The output is a set of CSV files containing strands, levels, groups, activities, and daily plans — ready to feed into an automated plan-generation system (such as an n8n + AI pipeline).

## Who it's for

- **Teachers** in rural Indian primary schools who teach all five grades in one room.
- **The AI system** that generates and adjusts daily lesson plans based on teacher feedback.
- **Curriculum designers** who want to extend this to other subjects or states.

## Context: the MGML classroom

One teacher, one room, grades 1 to 5. Children are placed into three level-based groups by a starting check (not by grade):
- **Group A (Beginning):** oral/hands-on work, foundational skills. Most children in this group cannot read yet.
- **Group B (Middle):** mix of oral, hands-on, and written work. Building fluency.
- **Group C (Advanced):** written/analytical work, application-level skills.

Each day the whole room works on one strand topic. Each group works on its own level of that strand's ladder. The teacher guides one group for 15 minutes while the other two do independent practice, then rotates — 3 blocks in a 45-minute period.

---

## Inputs needed before you start

| Input | Where to get it | Required? |
|---|---|---|
| NCERT textbooks for grades 1-5 (the subject) | ncert.nic.in/textbook.php or printed copies | Yes |
| NCERT Learning Outcomes at the Elementary Stage (2017) | ncert.nic.in or education.gov.in — pages for the subject | Yes |
| NIPUN Bharat / FLN goals | dsel.education.gov.in — the Lakshya goals | Yes for language and maths; check for other subjects |
| Das MGML article (CSF) | "Making Multi-grade Work" by Parthajeet Das | Yes (gives the 13 teaching rules) |
| RiVER / Rishi Valley "School in a Box" description | India Seminar 2004 article or equivalent | Recommended |
| State textbook PDFs (if different from NCERT) | State education department website | If building for a specific state |

Put all source documents in a folder called `sources/` before starting.

---

## Stage 1: Research (3 agents, run in parallel)

### Agent A — Learning outcomes

**Input**: NCERT Learning Outcomes document (the pages for your subject), NIPUN Bharat guidelines.

**Task**: Extract every learning outcome for classes 1 through 5. For each outcome, record:
- A code (e.g. M1-01 for maths class 1, outcome 1; L3-05 for language class 3, outcome 5)
- The exact text of the outcome
- The class it belongs to
- Whether it's verified (copied from the document) or paraphrased

Also extract NIPUN Bharat / FLN goals for the subject (Balvatika through Class 3).

**Output**: `research/01-outcomes.md`

**Quality check**: Every outcome must be either [verified] (copied from source) or [paraphrased] (written from memory). Paraphrased outcomes are acceptable for an MVP but should be verified before pilot.

### Agent B — MGML teaching rules

**Input**: Das MGML article, RiVER description, NEP 2020 references, NIPUN Bharat guidelines.

**Task**: Extract rules that govern how the curriculum and daily plans should work. Group them as:
- (a) Pace and scope — how much to cover, how fast
- (b) Grouping and levels — how to sort children, how many groups
- (c) Plan contents — what a daily plan must include
- (d) What to avoid — common mistakes

For each rule, note the source and a supporting quote if available. Mark unverified rules clearly.

Also document the RiVER ladder structure: milestones, unit types (introduce, apply, evaluate, remedial, enrichment), diagnostic gates.

**Output**: `research/02-mgml-rules.md`

### Agent C — Textbook inventory

**Input**: NCERT textbooks for grades 1-5.

**Task**: List every chapter in every textbook. For each chapter, record:
- Class, chapter number, chapter title
- Main skills covered (inferred from title and content if book isn't fully readable)
- Strand assignment (which thematic strand this chapter belongs to)

Create a strand mapping table and a count of chapters per strand per class.

**Output**: `research/03-textbook-inventory.md`

**Note on strands**: Define 3-6 strands for the subject before mapping. For maths these are NUM (numbers/place value), OPS (operations), GEO (shapes/space), MEA (measurement), DAT (data/patterns). For language they might be: READ (reading/decoding), WRIT (writing), ORAL (listening/speaking), VOCAB (vocabulary/grammar), LIT (literature/comprehension). Choose strands that group naturally and span all five grades.

---

## Stage 2: Design (1 agent)

**Input**: All three research files.

**Task**: Build the curriculum structure.

### Step 2a — Confirm strands

List 3-6 strands with a one-line description each. Every chapter in the textbook inventory must map to at least one strand. Every NCERT outcome must map to at least one strand.

### Step 2b — Build the level ladder

For each strand, define an ordered list of levels. A level is a skill, not a grade. Rules:
- Each level has a short "can-do" statement (e.g. "Counts objects up to 20")
- Levels are ordered by difficulty, not by grade
- Each level maps to one or more NCERT outcome codes
- Each level has a Bloom's taxonomy tag: remember, understand, apply, or analyse
- Each level has a "typical grade" (the grade where most children would encounter this)
- Each level names its prerequisite level (or "none" for entry levels)
- Aim for 8-15 levels per strand, 40-60 total across all strands

### Step 2c — Define group entry levels

For each strand, set the default entry level for groups A, B, and C. Group A starts at the beginning of the ladder. Group B starts roughly one-third of the way up. Group C starts roughly two-thirds of the way up. The three groups must always be on different levels.

### Step 2d — Write the CSVs

Create `output/strands.csv`, `output/levels.csv`, and `output/groups.csv` using the schema (see schema document).

**Output**: `research/04-design.md` (the reasoning), `output/strands.csv`, `output/levels.csv`, `output/groups.csv`

---

## Stage 3: Challenge (1 agent)

**Input**: The three research files plus the design output.

**Task**: Check the design for gaps and errors.

### Checks to run

1. **Coverage**: Every NCERT outcome code from `01-outcomes.md` appears in at least one level's `ncert_lo_code` field. List any unmapped outcomes.

2. **Prerequisite chain**: Follow the prerequisite links. No cycles. No level points to a prerequisite that doesn't exist. Entry levels (prerequisite = none) exist for every strand.

3. **Group spacing**: The three groups start at different levels in every strand. There is enough distance between groups that they won't collide within a typical school year.

4. **Level count**: 40-60 total is manageable for one teacher. Flag if it's outside this range.

5. **Bloom distribution**: Group A range levels should be mostly remember/understand. Group C range should have more apply/analyse. Flag imbalances.

6. **Textbook alignment**: Every textbook chapter maps to at least one level. Flag any orphan chapters.

**Output**: `research/05-challenge.md` with pass/fail for each check and specific issues to fix.

If issues are found, the design agent should fix them before proceeding.

---

## Stage 4: Activities (parallel, 1 agent per strand)

**Input**: `output/levels.csv` for the assigned strand, MGML rules from `02-mgml-rules.md`.

**Task**: For each level in the strand, write 3-5 teaching activities.

### Rules for activities
- Use only: blackboard, chalk, slates, stones, sticks, leaves, bottle caps, paper, string, water, containers, local coins/notes, the children's own bodies (clapping, jumping, standing in lines)
- No printed worksheets (the school may not have a printer)
- No devices or internet
- Each activity must work for a group of 8-20 children
- Steps must be concrete enough that a teacher who has never done this activity before can follow them
- Write steps in English (Hindi translation is a later task)
- Time estimate: 10-20 minutes per activity
- Tag each activity with its level_id
- Set the mode: oral, hands-on, or written
- Group A range activities (levels in the beginning range) must be oral or hands-on, because those children cannot read yet

**Output**: Append rows to `output/activities.csv`

---

## Stage 5: Daily Plans (1 agent)

**Input**: `output/levels.csv`, `output/activities.csv`, `output/groups.csv`, plus `02-mgml-rules.md`.

**Task**: Build 150 days of plans.

### Plan rules
- Each day the whole room works on one strand
- Each group works on its own level of that strand — the three groups are always on different levels
- Strands are interleaved: a block of 3-5 days on one strand, then the next, cycling through all five
- Strands with more levels get proportionally more days (e.g. OPS with 21 levels gets more days than DAT with 6)
- Plans are numbered by day (Day 1, Day 2, ..., Day 150), not tied to dates or weeks
- Each day has:
  - A shared opening (5 min, whole room, connects to the strand)
  - One activity per group, picked from activities.csv
  - A rotation describing how the teacher splits 45 minutes: guide one group (15 min) while the other two practise, then rotate
  - A check question per group to see if the day's target landed
- Vary the shared openings and rotations across days
- Groups advance through levels every 2-3 days

**Output**: `output/plans.csv`

---

## Stage 6: Final Review (1 agent)

**Input**: All output CSVs, all research files.

**Task**: Run these checks.

1. **Level coverage**: Every level_id in `levels.csv` appears in at least one plan row.
2. **Activity coverage**: Every activity_id in `activities.csv` is used in at least one plan row. Flag unused activities.
3. **Bloom progression**: Group A plans should start with remember/understand levels. Group C should include apply/analyse from early on.
4. **Materials feasibility**: No activity uses materials not available in a village classroom.
5. **Time feasibility**: Each day's total activity time fits within a 45-minute maths period.
6. **Plan completeness**: No empty fields in plans.csv. Every day has a shared opening, activities for all three groups, a rotation, and check questions.
7. **Group separation**: The three groups are on different levels every day.
8. **Activity-level match**: Every activity_id in plans.csv exists in activities.csv, and the activity's level_id matches the group's level_id for that day.
9. **Mode check**: Group A activities are all oral or hands-on (never written).

**Output**: `research/06-final-review.md` with pass/fail and issues.

---

## Output schema

Five CSV files. See `docs/schema.md` for the complete column definitions.

| File | What one row is | Key columns |
|---|---|---|
| `strands.csv` | One thematic strand | strand_id, name, description |
| `levels.csv` | One skill level in a strand | level_id, strand_id, level_no, can_statement, ncert_lo_code, nipun_goal, prerequisite_level_id, typical_grade, bloom |
| `groups.csv` | One level-based group | group, name, description, default_entry per strand |
| `activities.csv` | One teaching activity | activity_id, level_id, title, steps_english, steps_hindi, minutes, materials, mode, reviewed_by |
| `plans.csv` | One day's plan | day_no, strand_id, shared_opening, group levels and activities, rotation, check questions |

---

## Folder structure

```
<subject>-curriculum/
  sources/                          # Input documents (PDFs, articles)
  research/                         # Agent outputs from stages 1-3 and 6
    01-outcomes.md
    02-mgml-rules.md
    03-textbook-inventory.md
    04-design.md (or 04-activity-review.md)
    05-challenge.md
    06-final-review.md
  output/                           # The curriculum CSVs
    strands.csv
    levels.csv
    groups.csv
    activities.csv
    plans.csv
    sample-week.csv
  docs/                             # Documentation
    execution-plan.md               # This file
    schema.md                       # CSV column definitions
    index.md                        # How to use this folder
```

---

## How to adapt this for another subject

1. **Change the strands.** Maths uses NUM, OPS, GEO, MEA, DAT. Language might use READ, WRIT, ORAL, VOCAB, LIT. EVS might use LIVING, EARTH, SOCIETY, HEALTH.

2. **Change the learning outcomes source.** Use the pages for your subject from the same NCERT Learning Outcomes document.

3. **Change the activity materials.** Maths uses stones and sticks for counting. Language uses picture cards, story books, and chalk for writing. EVS uses plants, soil, water, and the school's surroundings.

4. **Keep the structure the same.** The strand-level-activity-plan hierarchy, the three groups, and the daily plan format all work for any subject.

5. **Keep the MGML rules.** The 13 rules from the Das article apply to all subjects, not just maths.

---

## Estimated effort

| Stage | Agents | Time (with AI) | Human review needed? |
|---|---|---|---|
| Research | 3 parallel | 15-30 min | Yes — verify outcomes against source docs |
| Design | 1 | 15-20 min | Yes — check level ladder makes sense |
| Challenge | 1 | 5-10 min | No (automated checks) |
| Activities | 3-6 parallel | 20-30 min | Yes — a teacher must review every activity |
| Plans | 1 | 30-45 min | Yes — spot-check 1 week per strand |
| Final Review | 1 | 5-10 min | No (automated checks) |
| **Total** | | **~2 hours** | **Activities need the most review** |

---

## Key principles (from the Das article and field evidence)

1. Teach fewer topics, but teach them well. Don't try to cover the full textbook.
2. Group by skill level, not grade. A grade 4 child at grade 2 level works with grade 2 material.
3. Move children up only when they show mastery, not when the calendar says so.
4. Give the teacher a ready plan, not a build-your-own toolkit.
5. Keep assessment simple and use it only to decide what to teach next.
6. Don't track every child on a platform. Track groups, not individuals.
