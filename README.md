# One plan for a one-room school

A daily maths plan for a teacher who teaches Classes 1 to 5 in one room. The plan updates itself after a short phone call at the end of each class.

## The problem

In many government primary schools in rural Uttarakhand, one teacher teaches Classes 1 to 5 in a single room: thirty children, five grades, one maths period and one blackboard.

1. **Five books, five sets of notes, one class.** To teach one period, she plans from five textbooks. While she teaches one grade, the other four wait.
2. **No integrated plan.** Every textbook is written for one grade. Nothing shows her how to teach all five grades together, on one topic, in the same period.
3. **No differentiated learning.** Children in the same grade are at very different levels. A Class 4 child may still be counting to 20. Teaching every child at their level means knowing each day what worked and changing the next lesson to match. Today, neither happens.

She cannot fix this alone. She barely has time to teach from five books, let alone rewrite the plan after every class. She was also never trained to plan for a room with many grades and many levels.

## The idea

Two ideas, combined:

- **Integrated learning.** One plan for the whole room. Every child studies the same topic on the same day, such as place value, at a difficulty that suits them.
- **Differentiated learning.** Each child gets work that matches where they are today. That needs feedback from the teacher every day, and a plan that adjusts to it.

This first version does both for Maths, Classes 1 to 5. The room is split into three groups by level, not by grade: **Group A (Beginning)**, **Group B (Middle)** and **Group C (Advanced)**. Each day has one topic, one task per group, and a plan the teacher can run from a blackboard. After class, a three-minute call updates the coming days.

## How it works, day to day

```
 1. The teacher opens her Google Sheet and teaches Day N.
 2. After class she talks to a voice agent for about three minutes:
    which day and topic, yes / partly / no for each group,
    what went well, what went wrong, what should change, what is left.
 3. Her answers are written into Day N's row of the sheet.
 4. If the day was only partly done, or she asked for a change,
    the rest of that topic is replanned. Unfinished work comes first.
 5. She gets a short email: what she said, what changed, and the sheet link.
```

The plan follows simple rules:

- **Yes:** she moves on to the next day.
- **No:** she repeats the same day. A second "No" on the same day produces an easier version of it.
- **Partly, or a change request:** only the remaining days of the current topic are rewritten. If it was the topic's last day, the next topic's days are rewritten instead. At most one extra day is added (for example "12a").
- **Silence:** if she does not call, the plan stays as it is. Nothing blocks her next class.

Her sheet has one row per day: Day, Topic, the task for each group, a link to the day's plan, whether the plan is original or updated (with a link to the original), and her feedback (Completed, What went well, What went wrong, How to improve, What is left, Reported on, and the full feedback as JSON).

## What makes it work

The system has two parts. Each has its own checks, so that no lesson reaches the teacher unverified.

### 1. Building the curriculum (done once)

- **Research:** learning outcomes, multi-grade teaching practice and the current NCERT textbooks were collected first.
- **Skill ladders:** maths was split into 5 strands (Numbers and Place Value, Operations, Shapes and Space, Measurement, Data Handling and Patterns) and **57 skill levels**, ordered from easiest to hardest. Each level is one skill a teacher can check in minutes, such as "counts objects up to 20". Each level is linked to a learning outcome, a NIPUN Bharat goal where one applies, its prerequisite level and a Bloom's level.
- **Activities:** **172 activities**, three to four per level, each using what a village classroom has: a blackboard, slates, stones, sticks and bottle caps.
- **Plans:** **150 day plans** grouped into 42 topic blocks. Each day has a shared opening for the whole room, a rotation for the teacher, one activity per group, and one concrete check question per group.
- **Checks:** the design passes 8 checks before plans are built (outcome coverage, prerequisite chains with no loops, spacing between groups, level count, Bloom's spread, textbook alignment, subject accuracy and language). The finished plans pass 11 more (every level and activity is used, every activity exists and matches its level, groups are never on the same level, Group A work is always spoken or hands-on, materials and time fit a real classroom, and nothing from another subject slips in).

### 2. The daily loop (runs after every call)

- **Two readings of every call.** The voice agent records 12 structured answers. An AgenticOrg agent reads the full transcript and returns the same 12 fields, plus the unfinished work per group. The two are merged: the teacher's direct answers always win, and the second reading only fills gaps.
- **Topic-level replanning.** Only the days of the current topic are touched, which keeps changes small and quick to review. The replanner works in steps:
  1. **Gather:** reads the day plans, the activity list and the skill ladder.
  2. **Diagnose:** works out what went wrong and for which group.
  3. **Plan:** chooses levels and activities, using only IDs from the reviewed activity list.
  4. **Rule check:** code checks every rule above. If a plan fails twice, the old plan is kept and the project owner is told.
  5. **Challenge:** a separate AgenticOrg agent reviews the plan and can send it back once.
  6. **Write:** turns the plan into a teacher-ready Doc, copying activity steps word for word.
- **Close the loop.** New plans are saved as Docs, the sheet rows are updated, and the teacher gets a short, plain email.

## What it is built on

### Teaching approaches

- **Multi-grade, multi-level teaching (MGML).** The core rules come from Parthajeet Das's writing on multi-grade classrooms: slow the syllabus down without lowering the standard, group children by level rather than grade, keep working with children who are behind, give teachers ready materials instead of asking them to build plans from textbooks, and use assessment only to decide what to teach next.
- **Rishi Valley "School in a Box" (RiVER).** The idea of a "ladder of learning": an ordered set of steps that each child climbs at their own pace, with a teacher who guides rather than lectures.
- **Teaching at the Right Level (TaRL).** A short check of where children are, grouping by that level, and moving a child up only after they show mastery.
- **Mastery before moving on.** A group moves to the next level when the current one is secure, not because the calendar moved.
- **Bloom's taxonomy.** Every level is tagged as remember, understand, apply or analyse, so each topic builds from recall to reasoning.

### Guidelines and classroom constraints

- **NCERT Learning Outcomes (2017)** for Classes 1 to 5. Each level is mapped to an outcome code.
- **NIPUN Bharat** foundational numeracy goals for the early grades.
- **NCERT's current maths textbooks (NCF 2023 series)** for Classes 1 to 5, used to check that the ladder covers what each grade is expected to learn.
- **The real classroom:** one teacher, one blackboard, one maths period of about 45 minutes, and no printed worksheets. Each day has a short opening for the whole room, then three guided blocks while the other two groups practise on their own.
- **Group A works orally or with objects.** Most children in this group cannot read yet.
- **Three groups, never more.** One teacher cannot run six groups in one period.

## Where it stands

This is a first version, built to be tested with teachers.

- The content is built from NCERT books in English. Hindi steps still need to be written.
- The learning outcome codes are paraphrased from the 2017 document, because the full text could not be retrieved. They need checking against the original.
- Every activity has so far been reviewed only by an AI acting as a teacher. A real teacher must review each one before classroom use.
- Each class's starting level comes from a default for now. A short starting check for the room is the next step.

If you teach, run a school or work in education, your feedback would help. Please open an issue or get in touch.

## What's in this repository

| Folder | Contents |
|---|---|
| `rishabhrawat-edu/maths-curriculum/` | The curriculum data (strands, levels, activities, groups, 150-day plan), the research notes and the check reports |
| `rishabhrawat-edu/curriculum-builder/` | A reusable kit to build the same kind of curriculum for another subject or language |
| `drive-build/` | The 150 day plans as HTML and the teacher sheet rows used to build the Google Drive copy |
| `rishabhrawat-edu/feedback-loop/` | How the daily loop works, plus the voice agent and AgenticOrg agent prompts |
| `n8n-workflows/` | The four live automation workflows (1.1 reminder, 1.2 read the call, 1.3 replan, 1.4 email), without credentials |
| `landing-page/` | The brief and copy for the project's landing page |

## Run it yourself

You need Docker, a Google account, an ElevenLabs account, an AgenticOrg account and an OpenAI API key.

1. Start n8n:
   ```bash
   docker run -d --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n:latest
   ```
2. In n8n, add credentials for Google (Gmail, Sheets, Docs, Drive), ElevenLabs, AgenticOrg (Header Auth: `Authorization: Bearer <key>`) and OpenAI, then install the ElevenLabs community node.
3. Create the ElevenLabs agent and the AgenticOrg agent from the prompts in `rishabhrawat-edu/feedback-loop/`.
4. Upload the day plans in `drive-build/docs/` to Google Drive as Docs, and create the teacher sheet from `drive-build/template150.csv` (tab "Plan").
5. Import the workflows in `n8n-workflows/`, choose your credentials, fill in the **Config** nodes (agent IDs, sheet ID, teacher email) and switch them on.

No keys or passwords are stored in this repository. Add them only as n8n credentials.
