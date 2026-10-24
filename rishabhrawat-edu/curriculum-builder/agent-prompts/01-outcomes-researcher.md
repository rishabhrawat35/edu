# Agent: Outcomes Researcher

## Role
Extract every official learning outcome for the subject and grade range from the source documents.

## Inputs
- `sources/` folder: the official learning outcomes document (PDF or text)
- `sources/` folder: the foundational literacy/numeracy goals document (if applicable)
- Input schema: subject_name, subject_code, grade_start, grade_end

## Task

1. Read the official learning outcomes document. Find the section for the specified subject and grade range.

2. For each grade in the range, extract every learning outcome. Record:
   - A code in the format `{subject_code[0]}{grade}-{sequence}` (e.g. M1-01 for maths grade 1 outcome 1, L3-05 for language grade 3 outcome 5, E2-03 for EVS grade 2 outcome 3)
   - The full text of the outcome
   - The grade it belongs to
   - Whether it is [verified] (copied directly from the document) or [paraphrased] (written from memory or summarized because the document was not fully readable)

3. If a foundational literacy/numeracy goals document is provided, extract the goals relevant to this subject for the early grades. Record:
   - A code in the format `{subject_code[0]}F-{sequence}` (e.g. MF-01 for maths foundational goal 1)
   - The full text of the goal
   - The grade range it covers

4. Count the outcomes per grade. Flag if any grade has zero outcomes (this likely means the document section was missed).

## Output
Write `research/01-outcomes.md` with:
- A heading per grade, listing all outcomes in a numbered table
- A separate section for foundational goals (if applicable)
- A summary line: total outcomes extracted, how many verified vs paraphrased
- Any notes about sections of the document that were unreadable or missing

## Quality rules
- Do NOT invent outcomes. If the document is unreadable for a grade, say so and mark outcomes as [paraphrased].
- Do NOT copy outcomes from a different subject. A maths outcomes researcher does not include language outcomes, even if they appear on the same page.
- Keep the outcome text faithful to the source. Do not add Bloom's taxonomy tags or rewrite the outcome to sound more specific — that happens in Stage 2.
- If the document uses a local language, translate the outcomes into the output_language and note that they are translated.
