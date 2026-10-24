# Maths Curriculum for Multi-Grade Classrooms (Grades 1-5)

## What is this folder?

This folder contains a complete, level-based maths curriculum for Indian primary schools where one teacher handles grades 1 to 5 in a single room. It is designed to work with an AI-powered plan generation system (n8n + LLM + Google Sheets) that gives the teacher a daily lesson plan and adjusts it based on her feedback.

Children are placed into three level-based groups (A = beginning, B = middle, C = advanced) by a starting check, not by grade. Each day the whole room works on one strand topic, and each group works on its own level of that strand's ladder. The teacher guides one group while the other two practise independently, rotating every 15 minutes across a 45-minute period.

The same folder structure and process can be used to build a curriculum for any other subject (language, EVS, etc.). See `docs/execution-plan.md` for the reusable process.

---

## Content-source notes

- The content is based on **NCERT textbooks in English**, not Uttarakhand state textbooks in Hindi. Activities and levels will need to be checked against the state syllabus before use in Uttarakhand.
- `research/01-ncert-outcomes.md` is **paraphrased and unverified** — the outcomes were written from memory, not copied from the NCERT Learning Outcomes PDF. Verify against the printed document before pilot.
- The activity review in `research/04-activity-review.md` was done by an **AI persona**, not a real teacher. A real teacher must review every activity before the pilot.

---

## Folder structure

```
rishabhrawat-edu/maths-curriculum/
|
|-- sources/                    # Source documents used for research
|   |-- das-mgml-part1.txt      # Parthajeet Das article on MGML (Part 1)
|   |-- das-mgml-part2.txt      # Parthajeet Das article on MGML (Part 2)
|
|-- research/                   # Research outputs (one file per research agent)
|   |-- 01-ncert-outcomes.md    # NCERT Learning Outcomes for Maths, Classes 1-5
|   |-- 02-mgml-rules.md       # 13 rules for multi-grade curriculum design
|   |-- 03-textbook-inventory.md # Chapter inventory of all 5 NCERT maths textbooks
|   |-- 04-activity-review.md   # AI teacher-persona review of all 172 activities
|   |-- 05-challenge.md         # Design challenge checks (stage 3)
|   |-- 06-final-review.md      # Final review checks (stage 6)
|
|-- output/                     # The curriculum data (CSV files)
|   |-- strands.csv             # 5 topic strands (NUM, OPS, GEO, MEA, DAT)
|   |-- levels.csv              # 57 skill levels across all strands (THE MAIN LADDER)
|   |-- groups.csv              # 3 level-based groups (A, B, C) with entry levels
|   |-- activities.csv          # 172 teaching activities (3-4 per level)
|   |-- plans.csv               # 150 daily plans (one strand per day, 3 groups)
|   |-- sample-week.csv         # First 5 days from plans.csv (shows the format)
|
|-- archive/                    # Previous versions
|   |-- 2026-10-24/             # Pre-groups model (had batches, weekly/daily plans)
|
|-- docs/                       # Documentation
|   |-- index.md                # THIS FILE - start here
|   |-- schema.md               # What every CSV column means and how files connect
|   |-- execution-plan.md       # Step-by-step process to build this for any subject
|
|-- mvp-tasks.md                # The 21-task MVP implementation plan
```

---

## How to use this folder

### If you are an AI agent building on this curriculum:

1. **Read `docs/schema.md` first.** It explains every CSV file, every column, and how the files connect.

2. **The core data is in `output/`.** Load `strands.csv`, `levels.csv`, `groups.csv`, and `activities.csv` into your data store (Google Sheets, a database, or just read them as CSVs).

3. **To generate a daily plan:** Read the teacher's current group levels, pick the next level for each group from `levels.csv` (following the prerequisite chain), select one activity per group from `activities.csv` for those levels, and write one row in the format shown in `sample-week.csv`.

4. **To adjust a daily plan after feedback:** If the teacher says "partly" or "no" for a group, pick a DIFFERENT activity from `activities.csv` for the SAME level. Don't move to the next level until the teacher says "yes".

5. **To generate a test:** Read the levels covered in the last 4-5 weeks for each group. Write one check question per level from the can_statement in `levels.csv`. Group A's section is spoken aloud.

### If you are a human reviewing or extending this:

1. **Start with the level ladder.** Open `output/levels.csv`. Each row is one skill. Read the `can_statement` column top to bottom within each strand — that IS the curriculum.

2. **Check the activities.** Open `output/activities.csv`. Read the `steps_english` column. Do the instructions make sense? Would they work in a village classroom? Can the teacher follow them without training?

3. **To add a new activity:** Add a row to `activities.csv` with the level_id it teaches. Use the activity_id format `{level_id}-A{next number}`, e.g. `NUM-01-A4`.

4. **To add a new level:** Add a row to `levels.csv` between the appropriate levels. Update the prerequisite chain. Check that `groups.csv` default entry levels still make sense.

### If you want to build this for another subject:

1. **Read `docs/execution-plan.md`.** It walks through the exact same process, written generically.
2. **Change the strands** to match the subject.
3. **Swap the NCERT outcomes** for the subject's section of the Learning Outcomes document.
4. **Follow stages 1-6** in the execution plan.

---

## Key design decisions

1. **Three level-based groups, not grade-based batches.** Children are placed into groups A (beginning), B (middle), and C (advanced) by a starting check. A grade 4 child working at grade 2 level goes into group A.

2. **One ladder per strand, not per group.** There is no separate curriculum per group — there is one ladder of 57 levels, and each group enters at a different point.

3. **One strand per day, three levels.** Each day the whole room works on one strand topic. Each group works on its own level of that strand, so everyone is doing "maths about shapes" but at different difficulty.

4. **Teacher guides one group at a time.** In a 45-minute period, the teacher guides each group for 15 minutes while the other two do independent practice. The rotation varies day to day.

5. **Plans numbered by day, not by date.** Plans are Day 1, Day 2, ..., Day 150. The teacher sets the pace. If she misses a day, she picks up where she left off.

6. **The AI picks, it doesn't invent.** The plan generator selects activities from the reviewed `activities.csv`. It never makes up new activities, because AI-generated teaching steps need human review.

7. **Feedback is per group, not per child.** The teacher says "yes/partly/no" for each group. The system does not track individual children.

---

## Data quality notes

- NCERT Learning Outcomes in `01-ncert-outcomes.md` are [paraphrased], not copied from the original document. Verify against the printed document before pilot.
- MGML rules in `02-mgml-rules.md` are verified against the Das article. TaRL, Nali Kali, and NEP rules are [unverified].
- Textbook chapter titles are from NCERT CIET and educational sites. Skills per chapter are [inferred] from titles.
- Activities have been reviewed by an AI teacher persona (see `research/04-activity-review.md`) — 20 fixes applied. Still need review by an actual teacher before classroom pilot.

---

## Quick reference: the 5 strands and 3 groups

| Code | Name | Levels | Group A starts at | Group B starts at | Group C starts at |
|------|------|--------|-------------------|-------------------|-------------------|
| NUM | Numbers and Place Value | 9 | NUM-01 | NUM-04 | NUM-07 |
| OPS | Operations | 21 | OPS-01 | OPS-08 | OPS-15 |
| GEO | Shapes and Space | 7 | GEO-01 | GEO-03 | GEO-05 |
| MEA | Measurement | 14 | MEA-01 | MEA-06 | MEA-10 |
| DAT | Data Handling and Patterns | 6 | DAT-01 | DAT-03 | DAT-05 |
| **Total** | | **57** | | | |
