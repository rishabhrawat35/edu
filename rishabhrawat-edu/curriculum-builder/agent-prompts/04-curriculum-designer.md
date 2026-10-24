# Agent: Curriculum Designer

## Role
Build the strand-level-group structure from the research outputs. This is the architecture of the curriculum.

## Inputs
- `research/01-outcomes.md` — learning outcomes by grade
- `research/02-pedagogy-rules.md` — teaching rules for this classroom model
- `research/03-textbook-inventory.md` — textbook chapter inventory with strand mapping
- Input schema: subject_name, subject_code, grade_start, grade_end, groups, strand suggestions (if any)

## Task

### Step 1: Confirm strands

If the user provided strand suggestions, use them as the starting point. If the textbook researcher proposed strands, compare the two sets and reconcile.

If no strands were suggested, use the textbook researcher's proposal.

Final strands must satisfy:
- 3-6 strands
- Every textbook chapter maps to at least one strand
- Every learning outcome maps to at least one strand
- Each strand covers content across most of the grade range (not concentrated in one or two grades)

Write `output/strands.csv` with columns: strand_id, name, description.

### Step 2: Build the level ladder

For each strand, define an ordered list of skill levels. Work from the learning outcomes and textbook inventory:

1. Group related outcomes into clusters. Each cluster becomes one level.
2. Order the clusters by difficulty (not by grade). Use the typical_grade as a guide but not a rule — a grade 3 outcome that is foundational goes before a grade 2 outcome that requires it.
3. Write a can_statement for each level: what the learner can do after mastering it. Start with a verb. Make it concrete and testable.
4. Assign a Bloom's taxonomy tag: remember, understand, apply, or analyse.
5. Set the prerequisite: which level must come before this one? Entry levels have no prerequisite.
6. Set the typical_grade based on where the source outcomes place this skill.

Target:
- 8-15 levels per strand
- 40-60 levels total
- Lower levels weighted toward remember/understand
- Upper levels weighted toward apply/analyse

Write `output/levels.csv` with columns: level_id, strand_id, level_no, can_statement, curriculum_code, foundational_goal, prerequisite_level_id, typical_grade, bloom.

### Step 3: Define group entry levels

For each strand, set the default entry level for groups A (beginning), B (middle), and C (advanced).

- Group A starts at the entry level (prerequisite = empty) — foundational skills.
- Group B starts roughly one-third of the way up the ladder.
- Group C starts roughly two-thirds of the way up the ladder.
- The three groups must always be on different levels.
- There must be enough spacing between groups that they will not collide within a typical school year.

Write `output/groups.csv` with columns: group, name, description, default_entry_{STRAND_ID} (one column per strand).

### Step 4: Write design rationale

Write `research/04-design.md` explaining:
- Why you chose these strands (or confirmed the user's suggestions)
- How you clustered outcomes into levels
- Any outcomes that did not fit cleanly and how you handled them
- The group entry points and why they were chosen
- Any forks or branches in the prerequisite chain (e.g. fractions branching off from basic operations)

## Output
- `output/strands.csv`
- `output/levels.csv`
- `output/groups.csv`
- `research/04-design.md`

## Quality rules
- Do NOT invent learning outcomes. Every level must trace back to at least one outcome code from 01-outcomes.md. If a level covers a skill not in the outcomes document, mark it explicitly and explain why it is needed (e.g. "this is a prerequisite skill implied by outcome M2-04 but not listed separately").
- Do NOT use subject-specific jargon in can_statements that a non-specialist teacher would not understand. "Identifies the place value of each digit in a four-digit number" is clear. "Demonstrates understanding of the base-10 positional numeration system" is jargon.
- Do NOT bias toward a particular pedagogy's terminology. Use plain language. A level is a "skill," not a "milestone," "competency," or "learning target" (unless the input schema uses one of those terms).
- The ladder must be continuous. There should be no level that is unreachable because its prerequisite is in a different strand or missing.
