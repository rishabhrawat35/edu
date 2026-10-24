# Methodology: how to build this for any subject or class

This document explains how the Maths 1 to 5 system was built, so the same approach can be reused for another subject, another class range or another language. It covers four things:

1. [The design decisions](#1-the-design-decisions) and why they were made
2. [Building the curriculum](#2-building-the-curriculum-the-orchestration-framework): the multi-agent orchestration framework
3. [Turning the curriculum into the teacher's Drive and sheet](#3-turning-the-curriculum-into-the-teachers-drive-and-sheet)
4. [The daily feedback loop](#4-the-daily-feedback-loop): how the plan keeps up with the class

[At the end](#5-checklist-for-a-new-subject) there is a checklist for starting a new subject.

The ready-to-use kit lives in [`rishabhrawat-edu/curriculum-builder/`](rishabhrawat-edu/curriculum-builder/). This document explains how its parts fit together, and adds what the kit does not cover.

---

## 1. The design decisions

Each decision below was made while building Maths 1 to 5. For a new subject, keep it unless there is a clear reason to change it.

| Decision | Why |
|---|---|
| **Skill ladders, not textbook chapters.** Each strand is an ordered list of skills ("levels"), each one something a teacher can check in a few minutes. | Children in one grade are at very different levels. A ladder lets each child start where they are. |
| **Three level-based groups (A Beginning, B Middle, C Advanced) for the whole room**, not batches by grade. | Two grade batches with three tiers each meant six groups in one period, which one teacher cannot run. Three groups fit three teaching blocks. |
| **One topic per day for the whole room**, with each group on its own level of that topic. | The teacher plans one lesson instead of five, and the whole room shares an opening. |
| **Numbered days, not weeks or dates.** | Teachers move at different speeds, miss days and repeat lessons. The plan follows the class, not the calendar. |
| **The AI picks from a reviewed activity bank; it never invents activities.** | Teaching steps written by an AI need human review. Picking from a reviewed list keeps every lesson checkable. |
| **A full default plan first, personalised later.** | The teacher can start on day one, and feedback improves the plan over time. |
| **Group A work is always spoken or hands-on.** | Most children at the start of the ladder cannot read yet. |
| **Only village-classroom materials.** Blackboard, slates, stones, sticks, bottle caps. No printing. | The plan has to work in the school as it is. |
| **Replan one topic at a time.** Only the remaining days of the current topic change (or the next topic, after a topic's last day). | Small changes are cheaper, faster and easier for the teacher to follow. |
| **Yes moves on, No repeats, Partly replans.** A second No on the same day gives an easier version. Silence changes nothing. | Simple rules the teacher can predict. Nothing ever blocks her next class. |
| **Check before anything reaches a teacher.** Separate challenger agents review the design, the plans and every replan. | Errors are caught by a reviewer that did not write the work. |

The teaching ideas behind these decisions (multi-grade multi-level teaching, Rishi Valley's ladder of learning, Teaching at the Right Level, mastery before moving on and Bloom's taxonomy) are summarised in the [README](README.md#what-it-is-built-on). The full notes, with sources, are in [`rishabhrawat-edu/maths-curriculum/research/`](rishabhrawat-edu/maths-curriculum/research/).

---

## 2. Building the curriculum: the orchestration framework

The curriculum is built by a pipeline of AI agents. Each agent has one job, a fixed input and a fixed output, so stages can be rerun or swapped without redoing everything.

### Inputs you provide

Defined in [`input-schema.md`](rishabhrawat-edu/curriculum-builder/input-schema.md):

- the subject, its short code and the output language
- the grade range and the groups (default: A, B, C as above)
- source documents: official learning outcomes, foundational goals (such as NIPUN Bharat), the textbooks, and an article on the teaching method
- classroom constraints: period length, materials available and unavailable, number of days

Two filled-in examples are in [`examples/`](rishabhrawat-edu/curriculum-builder/examples/): Maths 1 to 5 and Hindi 1 to 5.

### The eight stages

```
Stage 1  Research          3 agents in parallel
           outcomes researcher · pedagogy researcher · textbook researcher
Stage 2  Design            curriculum designer      → strands, levels, groups
Stage 3  Challenge         challenger               → fixes go back to Stage 2
Stage 4  Activities        1 activity writer per strand, in parallel
Stage 5  Activity review   reviewer as a teacher    → fixes go back to Stage 4
Stage 6  Plans             plan builder             → 150 day plans
Stage 7  Final review      final reviewer           → fixes go back to Stage 6
Stage 8  Package           merge files, update docs
```

| Stage | Agent prompt | Produces | Must be true before moving on |
|---|---|---|---|
| 1 Research | [01](rishabhrawat-edu/curriculum-builder/agent-prompts/01-outcomes-researcher.md), [02](rishabhrawat-edu/curriculum-builder/agent-prompts/02-pedagogy-researcher.md), [03](rishabhrawat-edu/curriculum-builder/agent-prompts/03-textbook-researcher.md) | outcomes, teaching rules, textbook inventory | all three notes exist, with sources and a confidence label for each |
| 2 Design | [04](rishabhrawat-edu/curriculum-builder/agent-prompts/04-curriculum-designer.md) | `strands.csv`, `levels.csv`, `groups.csv` | 3 to 6 strands, 40 to 60 levels, every link resolves |
| 3 Challenge | [05](rishabhrawat-edu/curriculum-builder/agent-prompts/05-challenger.md) | challenge report | the 8 design checks pass, or open issues are flagged for a person |
| 4 Activities | [06](rishabhrawat-edu/curriculum-builder/agent-prompts/06-activity-writer.md) | `activities.csv` | at least 3 activities per level, no unavailable materials |
| 5 Activity review | [07](rishabhrawat-edu/curriculum-builder/agent-prompts/07-activity-reviewer.md) | reviewed activities and a review report | every issue fixed or flagged for a person |
| 6 Plans | [08](rishabhrawat-edu/curriculum-builder/agent-prompts/08-plan-builder.md) | `plans.csv` | one row per day, groups always on different levels |
| 7 Final review | [09](rishabhrawat-edu/curriculum-builder/agent-prompts/09-final-reviewer.md) | final review report | the 11 build checks pass |
| 8 Package | (script or agent) | merged files, updated docs | all files in place |

How the stages work together (full detail in [`orchestration.md`](rishabhrawat-edu/curriculum-builder/orchestration.md)):

- **Parallel where it is safe.** The three researchers run together and do not read each other's work. Activity writers run one per strand.
- **Challenge loops.** A challenger that did not write the work checks it against [`challenge-criteria.md`](rishabhrawat-edu/curriculum-builder/challenge-criteria.md). Problems go back to the agent that wrote the work, which fixes only its own part. The challenger then checks again.
- **Gates.** A stage starts only when the previous one meets its gate.
- **Resumable.** A `state.json` file records which stages are done, so a failed stage can be rerun without touching earlier ones.
- **Honest sources.** Every research note says what was read, what could not be opened, and marks anything not verified, so a person knows what to check.

### The 19 checks

- **After design (8):** outcome coverage, prerequisite chains with no loops, spacing between groups, level count, Bloom's spread, textbook alignment, subject accuracy (no invented content), language.
- **After build (11):** every level used, every activity used, every activity ID exists, Bloom's progression over the year, materials available, time fits the period, every plan complete, groups never on the same level, activity matches its level, Group A spoken or hands-on, nothing from another subject.

For Maths 1 to 5 the reports are [`05-challenge.md`](rishabhrawat-edu/maths-curriculum/research/05-challenge.md) and [`06-final-review.md`](rishabhrawat-edu/maths-curriculum/research/06-final-review.md).

### Output

Five CSV files, defined in [`output-schema.md`](rishabhrawat-edu/curriculum-builder/output-schema.md): strands, levels, groups, activities and plans. The Maths 1 to 5 result is in [`rishabhrawat-edu/maths-curriculum/output/`](rishabhrawat-edu/maths-curriculum/output/): 5 strands, 57 levels, 172 activities, 3 groups and 150 days.

---

## 3. Turning the curriculum into the teacher's Drive and sheet

The CSVs are for machines. The teacher gets a Google Drive folder and one sheet.

```
Edu Maths MVP/
  Maths-Master/                      shared master copy, never edited per teacher
    Curriculum data (sheet)          Levels, Activities, Groups, Strands tabs
    Template - Teacher Maths Plan    the sheet every teacher's copy starts from
    Day plans/
      T01 Numbers and Place Value (Days 1-3)/
        Day 1 - T01 ... (Doc)
  Teachers/
    <Teacher name> - <School>/
      <Teacher name> - Maths Plan    her own sheet
      Updated plans/                 Docs the system rewrites for her
```

Steps (scripts in [`drive-build/`](drive-build/)):

1. **Group days into topics.** Consecutive days on the same strand form a topic block (`topics.json`, 42 topics for maths).
2. **Write one Doc per day.** `gen.py` turns each row of `plans.csv` and its activities into a Doc: a shared opening, the rotation, and for each group its skill, activity steps and check question.
3. **Build the teacher sheet.** `sheet.py` writes one row per day. Columns: Day, Topic, Group A/B/C today, Plan (link), Plan status, Original plan, Completed, What went well, What went wrong, How to improve, What is left, Reported on, Feedback (JSON).
4. **Copy on write.** A new teacher gets a copy of the sheet only. Its links point to the master Docs. A Doc is copied into her "Updated plans" folder only when her plan for that day changes. This is much faster than copying 150 Docs per teacher, and fixes to the master reach every teacher.

To reuse this for another subject, change the Doc headings in `gen.py` if the subject needs different sections. The sheet columns stay the same.

---

## 4. The daily feedback loop

This part makes the plan keep up with the class. It runs as four n8n workflows; their exports are in [`n8n-workflows/`](n8n-workflows/) and the details in [`rishabhrawat-edu/feedback-loop/`](rishabhrawat-edu/feedback-loop/).

```
1.1  2 pm reminder (optional)  → email with the call link if she has not called
       │
  Teacher calls the voice agent (about 3 minutes)
       │
1.2  Read the call             → voice answers + AgenticOrg reading, merged
                                 (her direct answers win), written to the day's row
       │  only if Partly, or she asked for a change
1.3  Replan the topic          → gather · diagnose · plan · rule check ·
                                 challenge · write → new Docs, sheet updated
       │
1.4  Email the teacher         → what she said, what changed, sheet link
```

### The voice call

The voice agent asks the same questions in the same order every time. It always gets the day and topic first, so the system can find the right row:

1. Which day of the plan, and which topic?
2. Did the class happen?
3. Did you finish everything? Yes, partly or no?
4. For each group: could most of them do the task?
5. What went well? What went wrong? What should change?
6. If partly or no: what is left, and for which group?
7. A two-line summary to confirm, then goodbye.

It stores 12 fields (day_number, topic, class_happened, completed, group_a/b/c_result, what_went_well, what_went_wrong, how_to_improve, what_is_left, other_notes). Prompt: [`elevenlabs-agent-fixes.md`](rishabhrawat-edu/feedback-loop/elevenlabs-agent-fixes.md).

### Two readings, one record

An AgenticOrg agent reads the full transcript and returns the same 12 fields, plus the unfinished work for each group ([`agenticorg-system-prompt.txt`](rishabhrawat-edu/feedback-loop/agenticorg-system-prompt.txt)). n8n merges the two: the voice agent's values win, and the second reading only fills gaps. The sheet's Feedback (JSON) column records where each value came from.

### Topic-level replanning

The replanner ([`replanner-v2.md`](rishabhrawat-edu/feedback-loop/replanner-v2.md)) works in fixed steps, so each one can be checked:

1. **Gather** the topic's day Docs, the activity bank and the level ladder (code, no AI).
2. **Diagnose** what went wrong, for which group (small model).
3. **Plan** levels and activities using only IDs from the activity bank (strong model).
4. **Rule check** in code. After two failed attempts the old plan is kept and the project owner is told.
5. **Challenge** with a separate AgenticOrg agent, which can send the plan back once.
6. **Write** the teacher-facing Doc, copying activity steps word for word (small model).

### Reusing the loop for another subject

| Part | What changes | What stays |
|---|---|---|
| Voice agent prompt | subject words in the questions | the order of questions and the 12 fields |
| AgenticOrg prompt | subject context in the first lines | the output format |
| Replanner | the subject's teaching rules in the plan and challenge prompts | the six steps and the rule check |
| Sheet and email | nothing | everything |

---

## 5. Checklist for a new subject

1. Collect the sources: official learning outcomes, foundational goals, the textbooks for each class, and one article on the teaching method.
2. Fill in an input file, starting from one of the [`examples/`](rishabhrawat-edu/curriculum-builder/examples/).
3. Run the eight stages with the [agent prompts](rishabhrawat-edu/curriculum-builder/agent-prompts/), keeping a `state.json`.
4. Have a real teacher review the activities, and add steps in the teacher's language.
5. Generate the day Docs and the template sheet with `drive-build/`.
6. Copy the voice agent, AgenticOrg prompt and n8n workflows, changing only the subject wording (section 4).
7. Test with one teacher for a few weeks before adding more.
