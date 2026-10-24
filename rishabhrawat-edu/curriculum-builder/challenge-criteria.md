# Challenge Criteria

Two sets of checks. Section A runs after Stage 2 (Design) and before activities are written. Section B runs after Stage 7 (Final Review) on the complete output. Each check is pass/fail with a specific condition.

---

## Section A: Post-Design Checks

Run these after strands.csv, levels.csv, and groups.csv are created (Stage 2), before building activities (Stage 4).

### A1. Outcome coverage

**Check:** Every learning outcome code from `research/01-outcomes.md` appears in at least one level's `curriculum_code` field in `levels.csv`.

**How to run:** Extract all outcome codes from 01-outcomes.md. For each code, search the curriculum_code column in levels.csv. List any codes that appear in the outcomes file but not in any level.

**Pass condition:** Zero unmapped codes, OR unmapped codes are explicitly documented with a reason (e.g. "this outcome is addressed through classroom practice, not a separate skill level").

**Fail action:** Add levels to cover the missing outcomes, or document why they are excluded.

### A2. Prerequisite chain integrity

**Check:** The prerequisite links in levels.csv form a valid directed acyclic graph.

**How to run:**
1. For each level, follow the prerequisite_level_id chain to its root. If any chain loops back to a level already visited, there is a cycle.
2. Check that every prerequisite_level_id value either matches a level_id in the file or is empty.
3. Check that every strand has at least one entry level (prerequisite_level_id = empty).

**Pass condition:** No cycles. No broken references. Every strand has at least one entry level.

**Fail action:** Fix the prerequisite references.

### A3. Group spacing

**Check:** The three groups start at different levels in every strand, with enough distance between them that they won't collide within a typical school year.

**How to run:** For each strand, read the default entry levels for groups A, B, and C from groups.csv. Check that all three are different level_ids and that A's level_no < B's level_no < C's level_no. Check that there are at least 2 levels between each pair of groups' entry levels.

**Pass condition:** All three groups start at different levels in every strand, with adequate spacing.

**Fail action:** Adjust group entry levels in groups.csv.

### A4. Level count

**Check:** The total number of levels is between 30 and 80.

**Rationale:** Fewer than 30 means each level covers too much ground and activities will be too broad. More than 80 means the plan generator has too many levels to pace across the available weeks.

**Pass condition:** 30 to 80 levels total.

**Fail action:** Merge or split levels. As a rule of thumb, target (total_weeks × number_of_groups × 0.6) levels, since some weeks are review weeks and some levels take multiple weeks.

### A5. Bloom distribution

**Check:** Lower-group levels are weighted toward remember/understand. Higher-group levels include more apply/analyse.

**How to run:** For each group, count levels in that group's range by bloom tag. Calculate the percentage of remember+understand vs apply+analyse. Group A = beginning range, Group B = middle range, Group C = advanced range.

**Pass condition:**
- Group A: at least 60% remember/understand.
- Group C: at least 40% apply/analyse.

**Fail action:** Reassign bloom tags. This usually means lower levels are tagged too high (a "remember" activity labeled as "apply") or upper levels are tagged too low.

### A6. Textbook alignment

**Check:** Every textbook chapter from `research/03-textbook-inventory.md` maps to at least one level.

**How to run:** Extract all chapter entries from the textbook inventory. For each chapter, check that at least one level in levels.csv covers the skills listed for that chapter.

**Pass condition:** Zero orphan chapters, OR orphan chapters are documented with a reason (e.g. "this chapter covers craft/art, which is outside this subject's scope").

**Fail action:** Add levels or adjust level can_statements to cover the missing chapters.

### A7. Subject-specificity check (anti-hallucination)

**Check:** Can_statements in levels.csv do not contain terms, concepts, or skills from a different subject.

**How to run:** Read every can_statement. Flag any that reference skills clearly belonging to another subject (e.g. a maths curriculum with a level about "reads a short passage aloud", or a language curriculum with "adds two-digit numbers").

**Pass condition:** Zero cross-subject contamination.

**Fail action:** Remove or rewrite the contaminated levels.

### A8. Language check

**Check:** If the output_language is not English, all can_statements, strand names, and strand descriptions are in the specified language (not left in English or partially translated).

**Pass condition:** All user-facing text is in the output_language.

**Fail action:** Translate the remaining text.

---

## Section B: Post-Build Checks

Run these after all CSVs are complete (Stage 7), before packaging.

### B1. Level coverage in plans

**Check:** Every level_id in levels.csv appears in at least one row of plans.csv (in group_a_level_id, group_b_level_id, or group_c_level_id).

**Pass condition:** Zero uncovered levels.

**Fail action:** Add plan rows that use the missing levels.

### B2. Activity coverage in plans

**Check:** Every activity_id in activities.csv is referenced in at least one plan row (in group_a_activity_id, group_b_activity_id, or group_c_activity_id).

**Pass condition:** Zero unused activities, OR unused activities are documented as "reserve" activities for the AI plan generator to use when adjusting plans based on feedback.

**Fail action:** Use the unused activities in at least one plan row, or mark them as reserves.

### B3. Activity reference validity

**Check:** Every activity_id referenced in plans.csv exists in activities.csv.

**How to run:** Extract all activity_id values from plans.csv (group_a_activity_id, group_b_activity_id, group_c_activity_id). Check each one against the activity_id column in activities.csv.

**Pass condition:** Zero invalid references.

**Fail action:** Replace invalid references with valid activity_ids for the same level.

### B4. Bloom progression over time

**Check:** Across the day sequence, earlier days target lower-bloom levels and later days target higher-bloom levels, within each group.

**How to run:** For each group, list the target levels in day order. Look up their bloom tags. The sequence should trend from remember → understand → apply → analyse. Some back-and-forth is fine.

**Pass condition:** No group starts with analyse-level targets on day 1, and no group ends with only remember-level targets in the final days.

**Fail action:** Adjust the weekly plan sequence so harder skills come later.

### B5. Materials feasibility

**Check:** No activity in activities.csv uses materials from the unavailable_materials list in the input schema.

**How to run:** For each activity, parse the materials column. Check each item against the unavailable list.

**Pass condition:** Zero violations.

**Fail action:** Rewrite the activity to use only available materials.

### B6. Time feasibility

**Check:** The total activity time for each day fits within the teaching period.

**How to run:** For each daily plan row, look up the minutes for each activity_id. Add them up. Add 5 minutes for the shared opening and 5 minutes for the check question.

**Pass condition:** Total minutes per day is less than or equal to period_minutes from the input schema.

**Fail action:** Replace longer activities with shorter ones, or split the day differently.

### B7. Plan completeness

**Check:** No required field in plans.csv is empty.

**How to run:** Check every row. The following columns must not be empty: day_no, strand_id, shared_opening, group_a_level_id, group_a_activity_id, group_b_level_id, group_b_activity_id, group_c_level_id, group_c_activity_id, rotation, check_question_a, check_question_b, check_question_c.

**Pass condition:** Zero empty required fields.

**Fail action:** Fill in the missing fields.

### B8. Group separation

**Check:** The three groups are on different levels every day.

**How to run:** For each row in plans.csv, check that group_a_level_id, group_b_level_id, and group_c_level_id are all different.

**Pass condition:** Zero days where any two groups share a level.

**Fail action:** Adjust levels so all three groups are on different levels.

### B9. Activity-level match

**Check:** Every activity_id in plans.csv matches the level_id assigned to the same group on that day.

**How to run:** For each row, look up group_a_activity_id in activities.csv and check that its level_id matches group_a_level_id. Same for groups B and C.

**Pass condition:** Zero mismatches.

**Fail action:** Replace the activity with one that matches the assigned level.

### B10. Mode check

**Check:** Group A activities are all oral or hands-on (never written).

**How to run:** For each row in plans.csv, look up group_a_activity_id in activities.csv and check that its mode is "oral" or "hands-on".

**Pass condition:** Zero written-mode activities for group A.

**Fail action:** Replace written activities with oral or hands-on ones for group A.

### B11. Cross-subject contamination (anti-hallucination)

**Check:** Activity steps and check questions do not contain content from a different subject.

**How to run:** Sample 20% of activities (at least 30). Read the steps column. Flag any that teach content clearly outside the subject (e.g. a maths activity that asks children to "write a paragraph about shapes" or an EVS activity that asks children to "solve 45 + 23").

**Pass condition:** Zero contaminated activities in the sample.

**Fail action:** Rewrite contaminated activities.

---

## Severity levels

| Severity | Definition | Action |
|---|---|---|
| Critical | Broken data integrity (cycles, missing references, empty required fields) | Must fix before proceeding to the next stage |
| High | Missing coverage (unmapped outcomes, uncovered levels, unused activities) | Should fix. Can proceed but flag for human review. |
| Medium | Quality issues (bloom imbalance, pacing, consecutive activity repeats) | Fix if time allows. Note in the review report. |
| Low | Suggestions (alternative phrasing, extra activities, pacing tweaks) | Note in the review report. Do not block. |
