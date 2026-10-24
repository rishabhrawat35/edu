# CSV Schema: Multi-Grade Maths Curriculum

This document explains every CSV file produced by the curriculum build, what each column means, and how the files relate to each other.

## Overview

Five CSV files form the complete curriculum data. They are designed to be loaded into Google Sheets (one sheet per file) or any database.

```
strands.csv ──┐
              ├── levels.csv ──┐
groups.csv    │                ├── activities.csv
              │                └── plans.csv
              └────────────────┘
```

---

## 1. strands.csv

**What it is:** The 3-6 broad topic areas that the subject is divided into.

| Column | Type | Description |
|---|---|---|
| strand_id | text, primary key | Short uppercase code, e.g. NUM, OPS, GEO, MEA, DAT |
| name | text | Human-readable name, e.g. "Numbers and Place Value" |
| description | text | One sentence saying what this strand covers |

**For maths, there are 5 strands:**
- **NUM** — Numbers and Place Value: counting, reading/writing numbers, place value, comparing and ordering
- **OPS** — Operations: addition, subtraction, multiplication, division, fractions, decimals
- **GEO** — Shapes and Space: 2D/3D shapes, angles, symmetry, spatial reasoning
- **MEA** — Measurement: length, weight, capacity, time, money, perimeter, area
- **DAT** — Data Handling and Patterns: sorting, pictographs, bar graphs, tables, number/shape patterns

---

## 2. levels.csv

**What it is:** The skill ladder. Each row is one skill that a child masters before moving to the next. This is the heart of the curriculum — it replaces "chapters" with a progression of abilities. There are 57 levels across all strands.

| Column | Type | Description |
|---|---|---|
| level_id | text, primary key | Format: {strand_id}-{number}, e.g. NUM-01, OPS-05 |
| strand_id | text, foreign key -> strands | Which strand this level belongs to |
| level_no | integer | Position on the ladder within this strand (1 = easiest) |
| can_statement | text | What the child CAN DO after mastering this level. Plain English, starts with a verb. |
| ncert_lo_code | text | Comma-separated codes from NCERT Learning Outcomes 2017 that this level covers. Empty if no direct match. |
| nipun_goal | text | Code from NIPUN Bharat numeracy goals. Empty if not applicable. |
| prerequisite_level_id | text, foreign key -> levels | The level_id that must be mastered before this one. Empty for the first level in each strand. |
| typical_grade | integer (1-5) | The grade where this skill normally appears in the NCERT textbook. Used for reference, NOT for grouping children. |
| bloom | text | Bloom's taxonomy tag: remember, understand, apply, or analyse |

**Key design rule:** One continuous ladder per strand. A child in any grade can be at any level. There is no separate curriculum per group — there is one ladder, and the starting check determines where each child enters.

---

## 3. groups.csv

**What it is:** Defines the three level-based groups. A child's group comes from the starting check, not their grade.

| Column | Type | Description |
|---|---|---|
| group | text, primary key | A, B, or C |
| name | text | Beginning, Middle, or Advanced |
| description | text | Who belongs in this group and the teaching approach |
| default_entry_NUM | text, foreign key -> levels | Default starting level for this group in the NUM strand |
| default_entry_OPS | text, foreign key -> levels | Default starting level in OPS |
| default_entry_GEO | text, foreign key -> levels | Default starting level in GEO |
| default_entry_MEA | text, foreign key -> levels | Default starting level in MEA |
| default_entry_DAT | text, foreign key -> levels | Default starting level in DAT |

**Important:** The default entry levels are starting points. The actual starting check (Task 5 in the MVP plan) determines where each child goes.

**Group definitions:**
- **A (Beginning):** Children at the start of the ladder. Activities are oral or hands-on because most cannot read yet. Typically corresponds to early grade 1-2 skills.
- **B (Middle):** Children who have basic skills and are building fluency. Mix of oral, hands-on, and written work. Typically corresponds to grade 2-4 skills.
- **C (Advanced):** Children working at upper-primary level. More written and analytical tasks. Typically corresponds to grade 4-5 skills.

---

## 4. activities.csv

**What it is:** Teaching activities for each level. The teacher picks from these — the AI plan generator also picks from these (it does not invent new activities). There are 172 activities across all 57 levels.

| Column | Type | Description |
|---|---|---|
| activity_id | text, primary key | Format: {level_id}-A{number}, e.g. NUM-01-A1, OPS-05-A3 |
| level_id | text, foreign key -> levels | Which level this activity teaches |
| title | text | Short name, e.g. "Stone counting race" |
| steps_english | text | Step-by-step instructions for the teacher, in plain English. 3-6 steps. |
| steps_hindi | text | Same instructions in Hindi. Empty until translated. |
| minutes | integer | How long the activity takes (5-15 minutes typical) |
| materials | text | What's needed: "blackboard, chalk" or "stones, sticks". Only things found in a village classroom. |
| mode | text | oral, hands-on, or written. Group A activities must be oral or hands-on. |
| reviewed_by | text | Who reviewed this activity. "AI persona" = reviewed by an AI teacher persona, not a real teacher. Must be a real teacher's name before pilot use. |

**Rules:**
- Each level has 3-4 activities so the AI can rotate them.
- Activities must work with a blackboard and locally available materials only.
- Group A activities (levels in the beginning range) are oral or hands-on, because those children cannot read yet.

---

## 5. plans.csv

**What it is:** The daily plan the teacher follows. One row per day. Each day the whole room works on one strand, and each group works on its own level of that strand's ladder. Plans are numbered by day (Day 1, Day 2...), not tied to dates or weeks, so the teacher sets the pace. There are 150 days of plans.

| Column | Type | Description |
|---|---|---|
| day_no | integer, primary key | Day number (1-150). The teacher does these in order at her own pace. |
| strand_id | text, foreign key -> strands | Which strand the whole room works on today |
| shared_opening | text | A 5-minute activity the whole room does together (all groups). |
| group_a_level_id | text, foreign key -> levels | The level group A works on today |
| group_a_activity_id | text, foreign key -> activities | The activity group A does today |
| group_b_level_id | text, foreign key -> levels | The level group B works on today |
| group_b_activity_id | text, foreign key -> activities | The activity group B does today |
| group_c_level_id | text, foreign key -> levels | The level group C works on today |
| group_c_activity_id | text, foreign key -> activities | The activity group C does today |
| rotation | text | How the teacher splits 45 minutes: guides one group (15 min) while the other two practise, then rotates. 3 blocks. |
| check_question_a | text | A quick check question for group A at the end |
| check_question_b | text | A quick check question for group B |
| check_question_c | text | A quick check question for group C |

**Design rules:**
- The three groups are always on different levels of the same strand.
- Strands are interleaved across the year: a block of 3-5 days on one strand, then the next strand, cycling through all five.
- Groups advance through levels at the same rate (every 2-3 days), but start at different points on the ladder.
- The rotation varies so the teacher does not always start with the same group.

---

## How the files connect

1. The **strands** define the topic areas.
2. Each strand has a **level ladder** — an ordered list of 57 skills from easiest to hardest.
3. **Groups** define where each group of children typically enters the ladder (beginning, middle, advanced).
4. Each level has 3-4 **activities** — concrete things the teacher does in class.
5. **Plans** assign one strand per day, with each group working on its own level and activity.

## How the AI plan generator uses these

Every Sunday, the n8n automation:
1. Reads the teacher's current group levels from the Teachers sheet
2. Reads the last two weeks of Feedback
3. Picks activities from activities.csv for the current levels (one per group)
4. Writes one row per day into Plans and saves the plan as a PDF
5. After daily feedback, if a group said "no" or "partly", swaps tomorrow's activity for a different one at the same level

The AI never invents activities — it only picks from the reviewed activities.csv.
