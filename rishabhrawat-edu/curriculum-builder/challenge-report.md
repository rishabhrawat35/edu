# Challenger Report: Curriculum Builder Toolkit

Reviewed: all 15 files in `/home/claude/curriculum-builder/`

---

## 1. Maths Bias Check

| # | File | Section | Issue | Severity | Suggested fix |
|---|------|---------|-------|----------|---------------|
| M1 | `agent-prompts/06-activity-writer.md` | Task, point 3 (Be concrete) | The "Good" example is maths-specific: "Write the number 253 on the board. Draw three columns: Hundreds, Tens, Ones." A language or EVS user gets no guidance on what a good activity looks like for their subject. | medium | Add a second "Good" example for a non-maths subject (e.g. a reading activity or a science observation). |
| M2 | `agent-prompts/08-plan-builder.md` | Quality rules | The example opening question ("Ask: what is 7 + 5?") and check question ("what is the area of a rectangle that is 4 units long and 3 units wide?") are both maths-specific. | medium | Add non-maths example questions alongside. E.g. "Ask: what word starts with the letter प?" for Hindi. |
| M3 | `agent-prompts/04-curriculum-designer.md` | Quality rules | Example of jargon uses maths concepts: "Identifies the place value of each digit in a four-digit number" vs "base-10 positional numeration system." | low | Add a non-maths jargon example (e.g. language: "Demonstrates phonemic awareness" → "Hears the separate sounds in a spoken word"). |
| M4 | `challenge-criteria.md` | B10 | Examples of cross-subject contamination are all maths-centric: "a maths activity that asks children to 'write a paragraph about shapes'" and "an EVS activity that asks children to 'solve 45 + 23'." | low | Examples are illustrative and the check is generic. No fix required, but adding a language example would be helpful. |
| M5 | `README.md` | "Adapting for a different country" | References "NCERT/India" as the default and says "replace" items. This frames India as the base and everything else as an adaptation. | medium | Reword to: "The kit is country-agnostic. The examples use India/NCERT. Replace the source document references with your country's equivalents." |
| M6 | `output-schema.md` | levels.csv | The `foundational_goal` column references "national foundational literacy/numeracy goals." For subjects like Art, Music, or Social Studies, most countries have no such goals document. Column is marked "empty otherwise," which is correct, but its name and description assume an FLN context. | low | No structural fix needed — the column is optional. Add a note: "This column is most relevant for early-grade reading and maths. Leave empty for subjects without national foundational goals." |

**Assessment:** The toolkit's structure (strands, levels, groups, activities, plans) is genuinely subject-agnostic. "Strands" work for language (Reading, Writing, Grammar, Oral), science (Living World, Physical World, Earth), and social studies (History, Geography, Civics). The maths bias is limited to illustrative examples, not structural assumptions. The core pipeline would work for any subject without modification.

---

## 2. Hallucination Check

| # | File | Section | Issue | Severity | Suggested fix |
|---|------|---------|-------|----------|---------------|
| H1 | `resources.md` | Section 1, US | URL `https://www.thecorestandards.org/` — the Common Core Standards Initiative's canonical domain is `corestandards.org`, not `thecorestandards.org`. Both may resolve, but the canonical form differs. | low | Verify and use the canonical URL. Add the disclaimer already present: "Always verify links before running the pipeline." |
| H2 | `resources.md` | Section 1, India | URL `https://nipunbharat.education.gov.in/` — the NIPUN Bharat portal URL may have changed since launch. Government portals are frequently reorganized. | low | Already mitigated by the note "Always verify links before running the pipeline." No fix needed. |
| H3 | `resources.md` | Section 2, General | Citation: "Little, A.W. (2006) — 'Education for All and Multigrade Teaching' — Springer." This is a real publication. No issue. | — | — |
| H4 | `resources.md` | Section 4 | URL `https://www.edu-links.org/resources/early-grade-reading-assessment-egra-toolkit` — this is a USAID-hosted URL that may have changed since USAID restructuring. | low | Add "(search USAID EGRA toolkit if link is broken)" after the URL. |
| H5 | `orchestration.md` | Resource estimates | "Total wall-clock time: ~45-75 min" for the full pipeline. These are plausible estimates for AI agent runs but are not sourced — they come from the maths build experience. | low | Add a note: "Estimates based on a single maths build. Actual times will vary by subject complexity and AI system speed." |

**Assessment:** No fabricated frameworks, no invented pedagogy claims. The resource URLs are reference suggestions with appropriate caveats. The Das MGML article, RiVER, TaRL, and all other named frameworks are real. The Little (2006) Springer citation is accurate. Low risk.

---

## 3. Completeness Check

| # | File | Section | Issue | Severity | Suggested fix |
|---|------|---------|-------|----------|---------------|
| C1 | `README.md` | Folder contents | Lists three example files (`maths-strands.csv`, `maths-levels-sample.csv`, `maths-activity-sample.csv`) that do not exist in the `examples/` folder. The actual files are `maths-india-grades1-5.yaml`, `hindi-language-grades1-5.yaml`, and `README.md`. | high | Update the README.md folder listing to match the actual files in `examples/`. |
| C2 | `orchestration.md` | Stage 5 | Says the activity reviewer "fixes problems directly in the CSV" — but `agent-prompts/07-activity-reviewer.md` says "Do NOT rewrite activities. Your job is to flag issues. The activity writer fixes them." Contradictory instructions. | high | Align: either the reviewer flags (and the orchestrator sends fixes back to the activity writer, like the Stage 3 challenger loop) or the reviewer fixes directly. Pick one and update both files. |
| C3 | `input-schema.md` | Groups | Group object uses field `group_label` and `grade_range` and `teaching_mode`, but `examples/maths-india-grades1-5.yaml` uses `name`, `description`, and `grades` (array, not range string). The two schemas don't match. | high | Align the example YAML to the input-schema, or vice versa. Pick one format and use it everywhere. |
| C4 | `input-schema.md` | Groups | Field `teaching_days_per_week` in input-schema, but `agent-prompts/08-plan-builder.md` reads `days_per_week` from the input schema. Different names for the same field. | medium | Pick one name and use it in both files. Recommend `days_per_week` (shorter). |
| C5 | `orchestration.md` | Stage 8 | Says "Generate or update `docs/index.md`" but no agent prompt or script template is provided for Stage 8. A user would not know what to put in index.md. | medium | Either add a short template for docs/index.md, or note that this is a manual step: "Copy the summary statistics from state.json into a markdown file for human reference." |
| C6 | Toolkit-wide | — | **RESOLVED.** The toolkit now uses 3 level-based groups (A/B/C) by default with groups.csv. Examples show all 3 groups. | — | No fix needed. |
| C7 | Toolkit-wide | — | No guidance on **re-running a single stage** after human review. The error handling table says "rerun from the last incomplete stage" but doesn't explain how to rerun just Stage 4 (activities) after humans reviewed and rejected some. Does the user delete the strand CSV and rerun? Edit it? | medium | Add a paragraph on partial reruns: which files to keep, which to regenerate, and how state.json should be updated. |
| C8 | `agent-prompts/08-plan-builder.md` | Output columns | The plan builder writes `weekly_plans-{STRAND_ID}.csv` with columns: `week_no, group_id, strand_id, level_id, week_type, focus`. But `output-schema.md` defines weekly_plans.csv with columns: `plan_id, group_id, strand_id, week_no, target_level_ids, objective`. The column names don't match: `level_id` vs `target_level_ids`, `focus` vs `objective`, `week_type` is absent from the schema, and `plan_id` is absent from the agent prompt. | critical | Align the plan builder's output columns to match output-schema.md exactly. Add `plan_id` and `week_type` to the schema, or remove `week_type` from the agent prompt and use the schema's column names. |
| C9 | `agent-prompts/08-plan-builder.md` | Daily plan columns | The plan builder writes daily plans with columns: `week_no, day_no, group_id, strand_id, level_id, opening, main_activity_id, main_activity_title, check_question`. But `output-schema.md` defines daily_plans.csv with: `day_id, plan_id, day_no, group_id, strand_id, shared_opening, low_level_id, mid_level_id, high_level_id, activity_ids, rotation, check_question`. Major misalignment: the agent prompt has a single `level_id` and `main_activity_id`, while the schema has three tier-level columns and a multi-activity `activity_ids` column plus a `rotation` column. | critical | This is the most significant issue. The schema describes a sophisticated three-tier differentiation model (low/mid/high within each group), but the plan builder prompt describes a simpler one-level-per-day model. Either simplify the schema to match the prompt, or rewrite the plan builder prompt to produce the three-tier output. |
| C10 | Toolkit-wide | — | No `sources/` folder documentation. The input schema says "these go in the `sources/` folder" but there is no template or naming convention. A user doesn't know whether to name files `textbook-grade1.pdf` or `ncert-class1.pdf` or anything else. | low | Add a short note: "Name files descriptively. The agents read everything in `sources/` — file names are for your reference, not parsed programmatically." |

**Assessment:** The two critical issues (C8, C9) are schema misalignments between `output-schema.md` and `agent-prompts/08-plan-builder.md`. These would cause the plan builder to produce files that don't match what the final reviewer expects. Must fix before use.

---

## 4. Language/Country Bias Check

| # | File | Section | Issue | Severity | Suggested fix |
|---|------|---------|-------|----------|---------------|
| L1 | `README.md` | "Adapting for a different country" | Says "The kit is written for NCERT/India by default." Frames India as the default, other countries as adaptations. | medium | Reword: "The kit is country-agnostic. The worked example uses India/NCERT; substitute your country's equivalents." (Same as M5.) |
| L2 | `resources.md` | Overall structure | India gets the most detailed coverage: 4 entries under curriculum frameworks, plus subject-specific NCERT links under every subject. UK and US get 2 entries each. East Africa gets 2 entries. Other regions (Latin America, South/Southeast Asia beyond India, Middle East, Pacific) are absent. | medium | Add a note at the top: "This list is a starting point weighted toward the countries where the toolkit was first tested. For other countries, search for '[country name] national curriculum framework' and '[country name] primary school textbooks' to find equivalents." |
| L3 | `resources.md` | Section 3, Language/Literacy | Lists only Hindi and English materials (Rimjhim, Marigold, StoryWeaver). No resources for other languages. | low | Already partially mitigated by the note about searching for materials in other languages. Could add: "For other languages, check the national curriculum body and organizations like Room to Read or SIL International." |
| L4 | `input-schema.md` | Validation checklist, item 5 | "The output language is one the AI system can write fluently. For less common languages, consider generating in English first and translating as a separate step." This is practical advice but implies non-English languages are second-class. | low | Reword: "Verify that the AI system can write fluently in the output language. If fluency is uncertain, generate in a language the system handles well and translate as a separate step." |
| L5 | `examples/` | Overall | Both examples are India-based (maths-India, Hindi-India). No example for a non-Indian context. | medium | Add one non-India example (e.g. `science-kenya-grades1-6.yaml` or `english-uk-ks1.yaml`) to demonstrate that the toolkit works outside India. |

**Assessment:** The toolkit is structurally country-agnostic — no agent prompt hardcodes India or NCERT. The bias is in the documentation and examples, which lean heavily Indian because that's where the toolkit was built. This is understandable but should be softened with framing and at least one non-India example.

---

## 5. Internal Consistency Check

| # | Files | Issue | Severity | Suggested fix |
|---|-------|-------|----------|---------------|
| I1 | `output-schema.md` ↔ `agent-prompts/08-plan-builder.md` | Weekly plan columns don't match (see C8). | critical | Same as C8. |
| I2 | `output-schema.md` ↔ `agent-prompts/08-plan-builder.md` | Daily plan columns don't match (see C9). | critical | Same as C9. |
| I3 | `input-schema.md` ↔ `examples/maths-india-grades1-5.yaml` | Group object fields don't match (see C3). input-schema uses `group_label`, `grade_range`, `teaching_mode`; example uses `name`, `description`, `grades`. | high | Same as C3. |
| I4 | `input-schema.md` ↔ `agent-prompts/08-plan-builder.md` | Field name mismatch: `teaching_days_per_week` vs `days_per_week` (see C4). | medium | Same as C4. |
| I5 | `README.md` ↔ `examples/` | README lists files that don't exist in examples (see C1). | high | Same as C1. |
| I6 | `orchestration.md` ↔ `agent-prompts/07-activity-reviewer.md` | Contradictory instructions on whether the activity reviewer fixes activities or only flags them (see C2). | high | Same as C2. |
| I7 | `orchestration.md` | Stages are numbered 1-8, agents are numbered 01-09. Stage 3 (Challenge) maps to agent 05. Stage 4 (Activities) maps to agent 06. This is correct — the numbering is consistent. | — | No issue. |
| I8 | `agent-prompts/01-outcomes-researcher.md` | Output file is `research/01-outcomes.md`. Other agents reference `research/01-outcomes.md`. Consistent. | — | No issue. |
| I9 | `agent-prompts/04-curriculum-designer.md` | References `research/01-outcomes.md`, `research/02-pedagogy-rules.md`, `research/03-textbook-inventory.md`. Agent 02 writes `research/02-pedagogy-rules.md`. Consistent. | — | No issue. |
| I10 | `challenge-criteria.md` ↔ `output-schema.md` | Check B7 lists required daily plan fields: `day_id, plan_id, day_no, group_id, strand_id, shared_opening, mid_level_id, activity_ids, check_question`. These match `output-schema.md`. But the plan builder agent (08) doesn't produce `day_id`, `plan_id`, `shared_opening` (uses `opening`), `mid_level_id` (uses `level_id`), or `activity_ids` (uses `main_activity_id`). | critical | Consequence of C9. Fix the plan builder to produce the schema-defined columns. |

---

## Summary Table

| Category | Issues found | Critical | High | Medium | Low |
|----------|-------------|----------|------|--------|-----|
| Maths bias | 6 | 0 | 0 | 3 | 3 |
| Hallucination | 4 (1 no-issue) | 0 | 0 | 0 | 4 |
| Completeness | 10 | 2 | 3 | 3 | 2 |
| Language/country bias | 5 | 0 | 0 | 3 | 2 |
| Internal consistency | 10 (4 no-issue) | 3 | 2 | 1 | 0 |
| **Total unique issues** | **24** | **3** | **4** | **8** | **9** |

Note: Several issues appear in multiple categories (C8=I1, C9=I2=I10, C3=I3, etc.). The unique count above deduplicates.

---

## Verdict: **PASS WITH FIXES**

The toolkit's architecture is sound and genuinely subject-agnostic. The strand-level-group-activity-plan pipeline works for any subject. The agent prompts are well-written with clear anti-hallucination guardrails. The challenge criteria are thorough.

**Must fix before use (3 critical):**
1. Align `agent-prompts/08-plan-builder.md` output columns with `output-schema.md` — specifically the weekly plan columns (plan_id, target_level_ids, objective vs level_id, focus, week_type).
2. Align `agent-prompts/08-plan-builder.md` daily plan columns with `output-schema.md` — specifically the three-tier model (low/mid/high level_ids, activity_ids list, rotation) vs the single-level model the prompt currently describes.
3. Update `challenge-criteria.md` check B7 if the schema changes, or update the plan builder if it doesn't.

**Should fix (4 high):**
1. Update `README.md` folder listing to match actual files in `examples/`.
2. Resolve the contradiction between orchestration.md and agent 07 on whether the activity reviewer fixes or flags.
3. Align input-schema.md group field names with the example YAML files.
4. Decide whether `week_type` belongs in the schema (it's useful — add it).

**Recommended (8 medium + 9 low):**
- Add non-maths examples to agent prompts 06 and 08.
- Soften the India-default framing in README.md.
- Add one non-India example YAML.
- Align field name `teaching_days_per_week` / `days_per_week`.
- Add partial-rerun guidance.
- ~~Correct the batches.csv row count note for >2 groups.~~ RESOLVED: now uses groups.csv with 3 groups by default.
