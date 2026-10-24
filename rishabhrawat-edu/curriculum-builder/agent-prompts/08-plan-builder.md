# Agent: Plan Builder

## Role
Build day-numbered lesson plans covering the full school year, interleaving all strands.

## Inputs
- `output/levels.csv` — all levels across all strands
- `output/groups.csv` — group definitions with default entry levels per strand
- `output/activities.csv` — all activities across all strands
- `research/02-pedagogy-rules.md` — teaching rules
- Input schema: total_days, groups (A/B/C), period_minutes, output_language

## Context: the 3-group rotation model

The classroom has three level-based groups: A (beginning), B (middle), C (advanced). Each day the whole room works on ONE strand. Each group works on its own level of that strand's ladder. The teacher guides one group for ~15 minutes while the other two do independent practice, then rotates — 3 blocks in the teaching period.

Plans are numbered by day (Day 1, Day 2, ...), not tied to dates or weeks. The teacher sets the pace.

## Task

### Step 1: Plan strand interleaving

Distribute total_days across strands proportionally to each strand's level count. For example, with 57 levels and 150 days:
- A strand with 21 levels gets roughly (21/57) × 150 ≈ 55 days
- A strand with 6 levels gets roughly (6/57) × 150 ≈ 16 days

Arrange days in blocks of 3-5 consecutive days per strand, then cycle to the next strand. Vary block lengths to avoid monotony.

### Step 2: Assign group levels

For each day, assign the three groups to different levels of that day's strand:
1. Group A starts at the group's default_entry level for the strand (from groups.csv)
2. Group B starts higher on the ladder
3. Group C starts near the top

Rules:
- The three groups must ALWAYS be on different levels — no two groups on the same level on any day
- Groups advance through levels every 2-3 days within a strand block
- When a group reaches the end of the ladder, it revisits earlier levels for consolidation

### Step 3: Pick activities

For each group on each day, pick one activity from activities.csv for that group's level:
1. Rotate activities — don't use the same one two days in a row for the same group
2. For Group A, activities must be oral or hands-on (mode = oral or hands-on), never written
3. If multiple activities exist for a level, vary the selection across days

### Step 4: Write shared openings

Each day has a 5-minute shared opening the whole room does together. It should connect to the day's strand and be accessible to all three groups. Vary the openings — do not repeat the same one across consecutive days on the same strand.

Good openings: "Ask: how many legs do three goats have? Let children count aloud." or "Draw a rectangle on the board. Ask: is this a shape you see in the classroom? Where?"

### Step 5: Write check questions

Each day has one check question per group, asked at the end. The question tests whether the day's level target landed. It must be concrete and answerable, not "Did you understand?"

Group A check questions are spoken aloud (these children cannot read). Group B and C check questions can be written on the board.

### Step 6: Write rotations

Describe how the teacher splits the period across 3 blocks. Vary the rotation so the teacher does not always start with the same group.

Example rotations:
- "Guide A (15 min) → Guide B (15 min) → Guide C (15 min)"
- "Guide C first (15 min) → Guide A (15 min) → Guide B (15 min)"
- "Guide B first (15 min) → Guide C (15 min) → Guide A (15 min)"

### Step 7: Validate

After generating all plans:
- Count total rows. Expected: total_days.
- Check that no day has two groups on the same level.
- Check that every activity_id exists in activities.csv and its level matches the group's level for that day.
- Check that all Group A activities have mode = oral or hands-on.
- Check that every level in levels.csv appears in at least one plan row.

Report any validation failures at the top of the output.

## Output
- `output/plans.csv` with columns: day_no, strand_id, shared_opening, group_a_level_id, group_a_activity_id, group_b_level_id, group_b_activity_id, group_c_level_id, group_c_activity_id, rotation, check_question_a, check_question_b, check_question_c

## Quality rules
- Do NOT skip days. Every day from 1 to total_days must have a row.
- Do NOT invent activities. Use only activity_ids from activities.csv. If you need an activity that does not exist, write a placeholder with activity_id = "MISSING-{LEVEL_ID}" and flag it.
- Do NOT front-load all new levels into the first third of the year. Spread them across the year.
- Do NOT write generic openings like "Review yesterday's lesson." Write a specific question.
- Do NOT write generic check questions. "Did you understand?" is not a check question. "Ask each pair: what is 7 + 5?" is.
- Keep all teacher-facing text in the output_language.
- The three groups must be on DIFFERENT levels every single day.
