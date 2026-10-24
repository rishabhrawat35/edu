# Curriculum Builder Toolkit

A self-contained kit for building an integrated, level-based curriculum for any subject, any class group, in any language. The output is a set of CSV files that an AI plan-generation system (or a human coordinator) can use to give each teacher a ready daily plan.

This toolkit was built from the experience of producing a complete maths curriculum for multi-grade Indian primary schools. It has been stripped of subject-specific content and made generic.

## What it produces

Five CSV files per subject:

| File | What one row is | Row count (typical) |
|---|---|---|
| strands.csv | One topic strand | 3-6 |
| levels.csv | One skill on the ladder | 40-60 |
| groups.csv | One level-based group with entry levels per strand | 1 per group (typically 3) |
| activities.csv | One teaching activity | 150-200 |
| plans.csv | One day's plan (all groups on one strand) | 150 |

Plus research notes, a design rationale, and challenge reports.

## How to use this kit

1. **Read `input-schema.md`** to see what you need to provide (subject, grade range, source documents, classroom constraints).
2. **Read `orchestration.md`** to understand the 8-stage pipeline and which agents run in parallel.
3. **Hand the agent prompts** (in `agent-prompts/`) to your AI system. Each prompt is self-contained and ready to use.
4. **Run the challenge criteria** (in `challenge-criteria.md`) against the output before deploying.
5. **Read `output-schema.md`** for the exact CSV column definitions.

## Folder contents

```
curriculum-builder/
  README.md                         # This file
  input-schema.md                   # What the user provides (inputs and their format)
  output-schema.md                  # What gets produced (CSV column definitions)
  orchestration.md                  # The multi-agent pipeline (stages, dependencies, parallelism)
  challenge-criteria.md             # All validation checks, run at two stages
  resources.md                      # Where to find source materials, by subject and country

  agent-prompts/                    # One file per agent role, ready to paste into an AI system
    01-outcomes-researcher.md       # Extracts learning outcomes from official documents
    02-pedagogy-researcher.md       # Extracts teaching rules for the classroom model
    03-textbook-researcher.md       # Inventories textbook chapters and maps them to strands
    04-curriculum-designer.md       # Builds the strand-level-group structure
    05-challenger.md                # Checks the design for gaps, cycles, and bias
    06-activity-writer.md           # Writes teaching activities for each level
    07-activity-reviewer.md         # Reviews activities as a teacher persona
    08-plan-builder.md              # Builds 150 days of daily plans
    09-final-reviewer.md            # Validates the complete output

  examples/                         # Sample input configurations (for illustration)
    README.md                       # How to use the examples
    maths-india-grades1-5.yaml      # Maths for Indian multi-grade primary school
    hindi-language-grades1-5.yaml   # Hindi language for Indian primary school
```

## Key principles

1. **Skill ladders, not chapters.** Every level is defined by what the learner can do, not which textbook page it comes from.
2. **One ladder per strand.** There is no separate curriculum per student group. Groups are windows on the same ladder.
3. **The AI selects, it does not invent.** Plan generators pick from the reviewed activity bank. They never make up new activities, because AI-generated teaching steps need human review.
4. **Preset baseline, then personalise.** The output includes a full-year default plan. Teachers see a working schedule from day one. Personalisation happens over time based on feedback.
5. **Challenge before deploy.** Two separate challenge stages (post-design and post-build) catch gaps, hallucinations, and bias before the plan reaches a classroom.

## Adapting for a different country or curriculum framework

The kit is country-agnostic. The worked examples use India/NCERT; substitute your country's equivalents. In `input-schema.md`, replace:
- "NCERT Learning Outcomes" with your country's official skill expectations
- "NIPUN Bharat / FLN goals" with your country's foundational literacy/numeracy targets (if they exist)
- "NCERT textbooks" with the textbooks used in your schools

The agent prompts reference these generically as "official learning outcomes" and "national curriculum textbooks." The India-specific resource links are in `resources.md` under the India section.
