# Output Schema

Five CSV files form the complete curriculum. They can be loaded into Google Sheets, a database, or read as flat files by an AI plan generator.

## File relationship diagram

```
strands.csv ──┐
              ├── levels.csv ──┐
groups.csv    │                ├── activities.csv
              │                └── plans.csv
              └────────────────┘
```

Each arrow means the downstream file references IDs from the upstream file.

---

## 1. strands.csv

One row per topic strand. Typically 3-6 rows.

| Column | Type | Description | Example |
|---|---|---|---|
| strand_id | text, primary key | Short uppercase code, unique | NUM, READ, LIVING |
| name | text | Human-readable strand name | "Numbers and Place Value" |
| description | text | One sentence: what this strand covers | "Counting, reading, writing and comparing numbers" |

Rules:
- Every level, activity, and plan references a strand_id. If a strand has no levels, it should not exist.
- 3-6 strands is the target. Fewer than 3 means the subject is not broken down enough. More than 6 means strands overlap.

---

## 2. levels.csv

One row per skill level. The heart of the curriculum. Typically 40-60 rows.

| Column | Type | Description | Example |
|---|---|---|---|
| level_id | text, primary key | Format: {strand_id}-{number, zero-padded} | NUM-01, READ-03 |
| strand_id | text, FK → strands | Which strand | NUM |
| level_no | integer | Position on the ladder within this strand (1 = easiest) | 1 |
| can_statement | text | What the learner can do after mastering this level. Plain language, starts with a verb. | "Counts objects up to 20 and says how many" |
| curriculum_code | text | Comma-separated codes from the official learning outcomes document. Empty if no direct match. | "M1-01,M1-02" |
| foundational_goal | text | Code from the national foundational literacy/numeracy goals, if applicable. Empty otherwise. | "N1-01" |
| prerequisite_level_id | text, FK → levels | The level_id that must be mastered before this one. Empty for entry levels. | NUM-01 |
| typical_grade | integer | The grade where this skill normally appears in the textbook. Used for group mapping. | 2 |
| bloom | text | Bloom's taxonomy tag: remember, understand, apply, or analyse | understand |

Rules:
- One continuous ladder per strand. No separate ladders per student group.
- Prerequisites form a directed acyclic graph (no cycles). Each strand has at least one entry level (prerequisite = empty).
- The can_statement must be concrete and testable. "Understands place value" is too vague. "Reads and writes three-digit numbers and says how many hundreds, tens and ones" is testable.
- Bloom tags progress from remember/understand at lower levels to apply/analyse at higher levels.

---

## 3. groups.csv

One row per level-based group. Typically 3 rows (A, B, C). A child's group comes from the starting check, not their grade.

| Column | Type | Description | Example |
|---|---|---|---|
| group | text, primary key | A, B, or C | A |
| name | text | Beginning, Middle, or Advanced | Beginning |
| description | text | Who belongs in this group and the teaching approach | "Children at the start of the ladder. Oral/hands-on activities." |
| default_entry_{STRAND} | text, FK → levels | Default starting level for this group in each strand (one column per strand) | NUM-01 |

Rules:
- These are defaults. The starting check determines where each child actually begins.
- Group A starts at the beginning of each strand's ladder, Group B roughly one-third up, Group C roughly two-thirds up.
- The three groups must always be on different levels in every strand.

---

## 4. activities.csv

One row per teaching activity. Typically 150-200 rows (3-4 per level).

| Column | Type | Description | Example |
|---|---|---|---|
| activity_id | text, primary key | Format: {level_id}-A{number} | NUM-01-A1 |
| level_id | text, FK → levels | Which level this activity teaches | NUM-01 |
| title | text | Short name for the activity | "Stone counting race" |
| steps_english | text | Step-by-step instructions in English. 3-6 numbered steps. | "1. Give each pair of children 20 stones. 2. Say a number between 1 and 20..." |
| steps_hindi | text | Same instructions in Hindi. Empty until translated. | "" |
| minutes | integer | How long the activity takes | 10 |
| materials | text | What the teacher needs. Only items from the available_materials list. | "stones, slates, chalk" |
| mode | text | oral, hands-on, or written | "hands-on" |
| reviewed_by | text | Who reviewed this activity. "AI persona" until a real teacher reviews. | "AI persona" |

Rules:
- Each level must have at least 3 activities so the plan generator can rotate them across days and respond to feedback.
- Steps must be concrete enough that a teacher who has never done this activity before can follow them without training.
- No activity may require materials from the unavailable_materials list.
- Time estimates must fit within the period_minutes from the input schema (allow 5 min for the shared opening and 5 min for the check question, so activities get period_minutes - 10).
- Group A activities (levels in the beginning range) must be oral or hands-on, because those children cannot read yet.

---

## 5. plans.csv

One row per teaching day. Each day the whole room works on one strand, and each group works on its own level of that strand's ladder. Plans are numbered by day (Day 1, Day 2...), not tied to dates or weeks, so the teacher sets the pace. Typically 150 rows.

| Column | Type | Description | Example |
|---|---|---|---|
| day_no | integer, primary key | Day number (1-150). The teacher does these in order at her own pace. | 1 |
| strand_id | text, FK → strands | Which strand the whole room works on today | NUM |
| shared_opening | text | A 5-minute activity the whole room does together (all groups). | "Ask: what number comes after 14?" |
| group_a_level_id | text, FK → levels | The level group A works on today | NUM-01 |
| group_a_activity_id | text, FK → activities | The activity group A does today | NUM-01-A1 |
| group_b_level_id | text, FK → levels | The level group B works on today | NUM-04 |
| group_b_activity_id | text, FK → activities | The activity group B does today | NUM-04-A1 |
| group_c_level_id | text, FK → levels | The level group C works on today | NUM-07 |
| group_c_activity_id | text, FK → activities | The activity group C does today | NUM-07-A1 |
| rotation | text | How the teacher splits 45 minutes: guides one group (15 min) while the other two practise, then rotates. 3 blocks. | "A guided → B guided → C guided" |
| check_question_a | text | A quick check question for group A at the end | "Show me 15 stones." |
| check_question_b | text | A quick check question for group B | "What is 23 + 14?" |
| check_question_c | text | A quick check question for group C | "Write the place value of 7 in 4,738." |

Rules:
- The three groups are always on different levels of the same strand.
- Strands are interleaved across the year: a block of 3-5 days on one strand, then the next strand, cycling through all five.
- Groups advance through levels every 2-3 days, but start at different points on the ladder.
- The rotation varies so the teacher does not always start with the same group.
- Group A activities must be oral or hands-on (never written).

---

## Derived columns the AI plan generator adds at runtime

These columns are NOT in the CSV files. They are added by the live system when it generates or adjusts a plan based on teacher feedback.

| Column | Source | Description |
|---|---|---|
| feedback | teacher input | "yes" / "partly" / "no" — did this group meet the day's target? (one per group) |
| adjusted | system | true/false — was this day's plan changed from the baseline? |
| replacement_activity_ids | system | If adjusted, the new activity_ids that replaced the original |
| adjustment_reason | system | Why the plan was changed, e.g. "Teacher said 'no' for group A on Day 12" |

These live in the system's database, not in the CSV files. The CSV files are the baseline.
