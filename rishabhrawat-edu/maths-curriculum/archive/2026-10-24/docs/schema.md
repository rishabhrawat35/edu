# CSV Schema: Multi-Grade Maths Curriculum

This document explains every CSV file produced by the curriculum build, what each column means, and how the files relate to each other.

## Overview

Six CSV files form the complete curriculum data. They are designed to be loaded into Google Sheets (one sheet per file) or any database.

```
strands.csv ──┐
              ├── levels.csv ──┐
batches.csv ──┘                ├── activities.csv
                               ├── weekly_plans.csv ── daily_plans.csv
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
- **GEO** — Shapes and Space: 2D/3D shapes, angles, symmetry, spatial reasoning, maps
- **MEA** — Measurement: length, weight, capacity, time, money, perimeter, area
- **DAT** — Data Handling and Patterns: sorting, pictographs, bar graphs, tables, number/shape patterns

---

## 2. levels.csv

**What it is:** The skill ladder. Each row is one skill that a child masters before moving to the next. This is the heart of the curriculum — it replaces "chapters" with a progression of abilities.

| Column | Type | Description |
|---|---|---|
| level_id | text, primary key | Format: {strand_id}-L{number}, e.g. NUM-L01, OPS-L05 |
| strand_id | text, foreign key → strands | Which strand this level belongs to |
| level_no | integer | Position on the ladder within this strand (1 = easiest) |
| can_statement | text | What the child CAN DO after mastering this level. Plain English, starts with a verb. E.g. "Counts objects up to 20 and says how many" |
| ncert_lo_code | text | Comma-separated codes from NCERT Learning Outcomes 2017 that this level covers. E.g. "M1-01,M1-02". Empty if no direct match. |
| nipun_goal | text | Code from NIPUN Bharat numeracy goals, e.g. "N1-01". Empty if not applicable (mostly empty for grades 4-5). |
| prerequisite_level_id | text, foreign key → levels | The level_id that must be mastered before this one. Empty for the first level in each strand. |
| typical_grade | integer (1-5) | The grade where this skill normally appears in the NCERT textbook. Used for batch mapping, NOT for grouping children. |
| bloom | text | Bloom's taxonomy tag: remember, understand, apply, or analyse. Batch 1 (grades 1-3) levels tend to be remember/understand. Batch 2 (grades 4-5) levels tend to be apply/analyse. |

**Key design rule:** One continuous ladder per strand. A child in any grade can be at any level. There is no separate "batch 1 curriculum" and "batch 2 curriculum" — there is one ladder, and batches are just entry/exit windows on it.

---

## 3. batches.csv

**What it is:** Defines which portion of each strand's ladder each batch typically works through.

| Column | Type | Description |
|---|---|---|
| batch | text | "1" (grades 1-3, oral/pictorial) or "2" (grades 4-5, numerical/written) |
| strand_id | text, foreign key → strands | Which strand |
| entry_level_id | text, foreign key → levels | The first level this batch typically starts at |
| exit_level_id | text, foreign key → levels | The last level this batch typically reaches by year end |

**Important:** These are defaults. The starting check (Task 5 in the MVP plan) determines where each batch actually starts. A batch 1 group that is ahead can work past the exit_level_id.

---

## 4. activities.csv

**What it is:** Teaching activities for each level. The teacher picks from these — the AI plan generator also picks from these (it does not invent new activities).

| Column | Type | Description |
|---|---|---|
| activity_id | text, primary key | Format: {level_id}-A{number}, e.g. NUM-L01-A1 |
| level_id | text, foreign key → levels | Which level this activity teaches |
| title | text | Short name, e.g. "Stone counting race" |
| steps_english | text | Step-by-step instructions for the teacher, in plain English. 3-6 steps. |
| minutes | integer | How long the activity takes (5-15 minutes typical) |
| materials | text | What's needed: "blackboard, chalk" or "stones, sticks" or "slates, chalk". Only things found in a village classroom. |

**Rule:** Each level should have 3-5 activities so the AI can rotate them. Activities must work with a blackboard and locally available materials only.

---

## 5. weekly_plans.csv

**What it is:** One row per week per batch per strand. Defines what levels and objectives the teacher aims for that week.

| Column | Type | Description |
|---|---|---|
| plan_id | text, primary key | Format: W{week}-{batch}-{strand_id}, e.g. W01-1-NUM |
| batch | text | "1" or "2" |
| strand_id | text, foreign key → strands | Which strand |
| week_no | integer | Week number in the year (1-30) |
| target_level_ids | text | Comma-separated level_ids this week works on, e.g. "NUM-L01,NUM-L02" |
| objective | text | One sentence: what most children in this batch should be able to do by Friday |

---

## 6. daily_plans.csv

**What it is:** The actual plan the teacher follows each day. One row per day per weekly plan.

| Column | Type | Description |
|---|---|---|
| day_id | text, primary key | Format: {plan_id}-D{day}, e.g. W01-1-NUM-D1 |
| plan_id | text, foreign key → weekly_plans | Which week this day belongs to |
| day_no | integer | Day within the week (1-5, Monday to Friday) |
| shared_opening | text | A 5-minute activity the whole room does together (both batches). E.g. "Count aloud from 1 to 50 as a class." |
| low_level_id | text, foreign key → levels | The level targeted for the weakest group within this batch |
| mid_level_id | text, foreign key → levels | The level targeted for the middle group |
| high_level_id | text, foreign key → levels | The level targeted for the strongest group |
| activity_ids | text | Comma-separated activity_ids used today, e.g. "NUM-L01-A1,NUM-L02-A3" |
| rotation | text | How the teacher splits 40 minutes between batches. E.g. "10 min batch 1 guided + batch 2 independent, then swap" |
| check_question | text | One question the teacher asks at the end to see if the day's target landed. E.g. "Ask 3 children: what is 15 + 7?" |

---

## How the files connect

1. The **strands** define the topic areas.
2. Each strand has a **level ladder** — an ordered list of skills from easiest to hardest.
3. **Batches** define which window of the ladder each group of grades typically works through.
4. Each level has 3-5 **activities** — concrete things the teacher does in class.
5. **Weekly plans** pick 1-2 levels per batch per strand to focus on that week.
6. **Daily plans** break each week into 5 days, with activities assigned, a rotation schedule, and a check question.

## How the AI plan generator uses these

Every Sunday, the n8n automation:
1. Reads the teacher's current batch levels from the Teachers sheet
2. Reads the last week's feedback from the Feedback sheet
3. Picks activities from activities.csv for the current levels
4. Writes 5 daily_plans rows and saves them as a PDF
5. After daily feedback, if a batch said "no" or "partly", swaps tomorrow's activity for a different one at the same level

The AI never invents activities — it only picks from the reviewed activities.csv.
