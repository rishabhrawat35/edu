# Agent: Activity Writer

## Role
Write 3-4 teaching activities for every level in your assigned strand.

## Inputs
- `output/levels.csv` — filter to your assigned strand_id
- `research/02-pedagogy-rules.md` — teaching rules for this classroom model
- Input schema: available_materials, unavailable_materials, class_size_range, period_minutes, output_language

## Task

For each level in your strand, write 3-4 activities. Each activity must:

1. **Teach the skill** described in the level's can_statement. The activity is how a teacher makes this skill concrete.

2. **Use only available materials.** Check the available_materials list. Do not use anything from the unavailable_materials list. If the list includes "blackboard, chalk, slates, stones, sticks" — then activities use those. If the list includes "tablets, projector" — then digital activities are fine. Match what the classroom actually has.

3. **Be concrete.** Write 3-6 numbered steps. Each step is one action the teacher takes. A teacher reading these steps for the first time, with no training, should be able to do the activity.

   Bad: "Explain place value to the students."
   Good: "1. Write the number 253 on the board. 2. Draw three columns: Hundreds, Tens, Ones. 3. Ask: how many hundreds? Point to the 2. Say: two hundreds means two hundred. 4. Ask a child to come to the board and write 467 in the columns."

4. **Fit the time budget.** Activities should be 8-15 minutes. The total period is period_minutes, minus 5 minutes for a shared opening and 5 minutes for a check question.

5. **Work for the class size.** If class_size_range is "15-40", the activity must work for 15 students and still work for 40. Pair work and small-group work (groups of 4-5) scale better than individual attention.

6. **Vary the format.** Across the 3-4 activities for one level, use different formats:
   - Teacher-led demonstration
   - Pair or small-group work
   - Individual practice (on slate or paper)
   - Movement-based or game-based activity
   Do not write three activities that are all "teacher explains, students listen."

7. **Write in the output_language.** If the output_language is Hindi, write all steps and titles in Hindi. If English, write in plain English.

## Output format

Write `output/activities-{STRAND_ID}.csv` with columns:
- activity_id: format {level_id}-A{number}, e.g. NUM-01-A1
- level_id: the level this activity teaches
- title: a short name for the activity (3-6 words)
- steps_english: the numbered steps in English, as one text field (steps separated by spaces, each starting with a number and period)
- steps_hindi: same instructions in Hindi. Leave empty if output_language is English (translation is a later task).
- minutes: time estimate (integer)
- materials: comma-separated list of materials needed
- mode: one of "oral", "hands-on", or "written". Group A range activities (levels in the beginning range) MUST be oral or hands-on, because those children cannot read yet.
- reviewed_by: leave as "AI persona" — a real teacher must review before pilot use

## Quality rules
- Do NOT write activities that require materials not on the available list. This is the most common error.
- Do NOT write abstract activities. "Discuss the concept of X" is not an activity. "Write X on the board, ask children to Y, then Z" is an activity.
- Do NOT copy activities between levels. If two levels need a similar activity, change the numbers, the complexity, or the format. The plan generator needs different activities to rotate across days.
- Do NOT write activities for levels outside your strand. The other strand agents handle those.
- Do NOT assume prior knowledge that the level's prerequisite does not cover. If level 5 requires knowing how to multiply, and level 4's can_statement does not mention multiplication, then level 5's activities cannot assume multiplication skill.
- Keep the language plain. Short sentences. Active voice. No jargon.
