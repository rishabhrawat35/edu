# Maths Curriculum for Multi-Grade Classrooms (Grades 1-5)

## What is this folder?

This folder contains a complete, level-based maths curriculum for Indian primary schools where one teacher handles grades 1 to 5 in a single room. It is designed to work with an AI-powered plan generation system (n8n + LLM + Google Sheets) that gives the teacher a daily lesson plan and adjusts it based on her feedback.

The same folder structure and process can be used to build a curriculum for any other subject (language, EVS, etc.). See `docs/execution-plan.md` for the reusable process.

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
|   |-- 04-activity-review.md   # Teacher-persona review of all 172 activities (20 fixes)
|
|-- output/                     # The curriculum data (CSV files)
|   |-- strands.csv             # 5 topic strands (NUM, OPS, GEO, MEA, DAT)
|   |-- levels.csv              # 48 skill levels across all strands (THE MAIN LADDER)
|   |-- batches.csv             # Batch 1 and 2 level ranges per strand
|   |-- activities.csv          # 172 teaching activities (3-4 per level)
|   |-- weekly_plans.csv        # 300 weekly plan rows (30 weeks × 2 batches × 5 strands)
|   |-- daily_plans.csv         # 1500 daily plan rows (30 weeks × 2 batches × 5 strands × 5 days)
|   |-- weekly_plans-{STRAND}.csv  # Per-strand weekly plans (60 rows each)
|   |-- daily_plans-{STRAND}.csv   # Per-strand daily plans (300 rows each)
|   |-- sample-week.csv         # One example week of daily plans (shows the format)
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

2. **The core data is in `output/`.** Load `strands.csv`, `levels.csv`, `batches.csv`, and `activities.csv` into your data store (Google Sheets, a database, or just read them as CSVs).

3. **To generate a weekly plan:** Read the teacher's current batch levels, pick the next 1-2 levels per batch from `levels.csv` (following the prerequisite chain), select activities from `activities.csv` for those levels, and write 5 daily plan rows in the format shown in `sample-week.csv`.

4. **To adjust a daily plan after feedback:** If the teacher says "partly" or "no" for a batch, pick a DIFFERENT activity from `activities.csv` for the SAME level. Don't move to the next level until the teacher says "yes".

5. **To generate a test:** Read the levels covered in the last 4-5 weeks. Write one check question per level from the can_statement in `levels.csv`.

### If you are a human reviewing or extending this:

1. **Start with the level ladder.** Open `output/levels.csv`. Each row is one skill. Read the `can_statement` column top to bottom within each strand — that IS the curriculum.

2. **Check the activities.** Open `output/activities.csv`. Read the `steps_english` column. Do the instructions make sense? Would they work in a village classroom? Can the teacher follow them without training?

3. **To add a new activity:** Add a row to `activities.csv` with the level_id it teaches. Use the same activity_id format ({STRAND}-L{level}-A{next number}).

4. **To add a new level:** Add a row to `levels.csv` between the appropriate levels. Update the prerequisite chain. Check that `batches.csv` still makes sense.

### If you want to build this for another subject:

1. **Read `docs/execution-plan.md`.** It walks through the exact same process, written generically.
2. **Change the strands** to match the subject.
3. **Swap the NCERT outcomes** for the subject's section of the Learning Outcomes document.
4. **Follow stages 1-6** in the execution plan.

---

## Key design decisions

1. **One ladder per strand, not per grade.** A grade 4 child working at grade 2 level uses grade 2 material. There is no separate "batch 1 curriculum" and "batch 2 curriculum."

2. **Skills, not chapters.** Each level is defined by what the child CAN DO ("counts to 20"), not by a textbook reference ("Chapter 3").

3. **The AI picks, it doesn't invent.** The plan generator selects activities from the reviewed `activities.csv`. It never makes up new activities, because AI-generated teaching steps need human review.

4. **Feedback is per batch, not per child.** The teacher says "yes/partly/no" for each batch. The system does not track individual children.

5. **Three tiers within each batch.** Each daily plan has activities for low, mid, and high groups within the batch. This handles the spread within a single grade.

6. **A baseline "default image" of 30 weeks is preset.** The `weekly_plans.csv` and `daily_plans.csv` files contain a complete 30-week plan across all strands. This is what the teacher sees on day one. Over time, the AI system personalises plans based on teacher feedback — but the preset baseline ensures every teacher has a working plan from the start.

---

## Data quality notes

- NCERT Learning Outcomes in `01-ncert-outcomes.md` are [paraphrased], not copied from the original document. The actual PDF could not be accessed programmatically. Verify against the printed document before pilot.
- MGML rules in `02-mgml-rules.md` are verified against the Das article. TaRL, Nali Kali, and NEP rules are [unverified].
- Textbook chapter titles are from NCERT CIET and educational sites. Skills per chapter are [inferred] from titles.
- Activities have been reviewed by an AI teacher persona (see `research/04-activity-review.md`) — 20 fixes applied. Still need review by an actual teacher before classroom pilot.

---

## Quick reference: the 5 strands

| Code | Name | Levels | Batch 1 range | Batch 2 range |
|------|------|--------|--------------|--------------|
| NUM | Numbers and Place Value | 9 | L01-L06 | L07-L09 |
| OPS | Operations | 21 | L01-L12 | L13-L21 |
| GEO | Shapes and Space | 7 | L01-L03 | L04-L07 |
| MEA | Measurement | 14 | L01-L08 | L09-L14 |
| DAT | Data Handling and Patterns | 6 | L01-L03 | L04-L06 |
| **Total** | | **48** | **32** | **25** (some overlap at boundaries) |
