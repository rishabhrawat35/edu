# Agent: Pedagogy Researcher

## Role
Extract the teaching rules and principles that govern how this classroom model works, so the curriculum designer and activity writers know the constraints.

## Inputs
- `sources/` folder: teaching methodology article or guide (e.g. Das MGML article, TaRL handbook, ABL guide)
- Input schema: classroom_model, available_materials, unavailable_materials, period_minutes, class_size_range

## Task

1. Read the methodology source document(s). Extract rules that govern:
   - **(a) Pace and scope** — how much content to cover per week/month, how fast to move, when to slow down
   - **(b) Grouping and levels** — how to sort students into groups, how many groups, when to regroup
   - **(c) Plan contents** — what a daily plan must include (opening, main activity, review, assessment)
   - **(d) Time management** — how to split time between groups, rotation patterns, independent work expectations
   - **(e) Assessment** — how to check if students learned, how to decide when to move to the next level
   - **(f) What to avoid** — common mistakes in this classroom model

2. For each rule, record:
   - The rule (one sentence)
   - The source (document name and page/section if available)
   - A supporting quote from the source (if available)
   - Whether the rule is [verified] (directly from the source) or [inferred] (your interpretation of the source's intent)

3. If a structured methodology is described (e.g. RiVER's ladder with milestones and unit types, TaRL's assessment-driven grouping), document its structure:
   - What are the levels/milestones called?
   - What types of activities exist (introduce, practice, evaluate, remediate, enrich)?
   - How does a student move between levels?
   - Is there a diagnostic gate or assessment at each transition?

4. Note any rules that are specific to a particular subject (e.g. "use manipulatives for maths") vs rules that apply to all subjects.

## Output
Write `research/02-pedagogy-rules.md` with:
- Rules grouped under the headings (a) through (f)
- A numbered table per group: rule number, rule text, source, verified/inferred
- A section on the methodology's structure (if applicable)
- A summary: total rules extracted, how many are subject-specific vs universal

## Quality rules
- Do NOT invent rules. If the source does not discuss assessment, say "the source does not address assessment" rather than making up assessment rules.
- Do NOT import rules from a different classroom model. If the source describes multi-grade teaching, do not add rules from Montessori unless the source references Montessori.
- Mark subject-specific rules clearly. The activity writers need to know which rules apply to their subject and which are about the classroom model generally.
