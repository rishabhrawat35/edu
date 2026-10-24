# Input Schema

Everything the user must provide before the pipeline starts. The pipeline cannot run without the required inputs. Optional inputs improve quality but are not blockers.

## Required inputs

### 1. Subject definition

| Field | Type | Example | Notes |
|---|---|---|---|
| subject_name | text | "Mathematics", "Hindi Language", "Environmental Studies" | The subject this curriculum covers |
| subject_code | text (3-4 chars, uppercase) | "MATH", "HINDI", "EVS" | Used as a prefix in file names |
| output_language | text | "English", "Hindi", "Kannada" | The language all activity steps and plan text will be written in |

### 2. Grade range and grouping

| Field | Type | Example | Notes |
|---|---|---|---|
| grade_start | integer | 1 | The lowest grade this curriculum covers |
| grade_end | integer | 5 | The highest grade |
| groups | list of objects | See below | How students are split for instruction |

Each group object:

| Field | Type | Example | Notes |
|---|---|---|---|
| group_id | text | "A", "B", "C" | Internal identifier (one letter) |
| group_label | text | "Group A (Beginning)" | Human-readable label |
| description | text | "Foundational skills, oral/hands-on" | Who belongs in this group and teaching approach |
| teaching_mode | text | "oral and hands-on" | How this group learns (oral, written, mixed, hands-on) |

**Default if not provided:** Three level-based groups. Group A = beginning (oral/hands-on), Group B = middle (mixed), Group C = advanced (written/analytical). Children are placed by a starting check, not by grade. The pipeline will prompt the user to confirm or adjust.

### 3. Source documents

These go in the `sources/` folder. The pipeline needs at least one of the first two.

| Document | What it contains | Format | Required? |
|---|---|---|---|
| Official learning outcomes | The skills students should have at the end of each grade, published by the curriculum authority | PDF, text, or URL | Yes |
| Textbooks (one per grade) | The actual textbooks students use, or at minimum a table of contents | PDF, text, or scanned images | Yes (at least chapter listings) |
| Foundational literacy/numeracy goals | National targets for early grades (e.g. NIPUN Bharat in India, Early Grade Reading benchmarks elsewhere) | PDF, text, or URL | If they exist for this subject |
| Teaching methodology article or guide | Rules or principles for the classroom model being used (e.g. multi-grade teaching, activity-based learning, TaRL) | PDF, text, or URL | Recommended |
| Existing curriculum ladder or scope-and-sequence | If someone has already built a skill progression for this subject | CSV, spreadsheet, or text | Optional (speeds up design) |

### 4. Classroom constraints

| Field | Type | Default | Notes |
|---|---|---|---|
| classroom_model | text | "multi-grade" | How the room is organized: "multi-grade" (one teacher, multiple grades), "single-grade", "multi-level" (one grade, different skill levels) |
| period_minutes | integer | 45 | How long one teaching period lasts |
| available_materials | list of text | ["blackboard", "chalk", "slates", "paper", "pencil"] | What the teacher has access to. Determines what activities can use. |
| unavailable_materials | list of text | ["printer", "internet", "devices", "projector"] | What the teacher does NOT have. Activities must not require these. |
| class_size_range | text | "15-40" | How many students the teacher typically has |
| days_per_week | integer | 5 | How many days per week this subject is taught |
| total_weeks | integer | 30 | How many teaching weeks in the academic year |

### 5. Strand suggestions (optional but helpful)

If the user already knows how they want the subject divided into topic strands, they can provide them. Otherwise the pipeline will propose strands during Stage 2 (Design).

| Field | Type | Example |
|---|---|---|
| strand_id | text | "NUM", "READ", "LIVING" |
| strand_name | text | "Numbers and Place Value", "Reading and Decoding", "Living World" |
| strand_description | text | One sentence describing what this strand covers |

**Typical strand counts by subject:**

| Subject | Typical strands | Example |
|---|---|---|
| Mathematics | 4-6 | Numbers, Operations, Geometry, Measurement, Data/Patterns |
| Language | 4-5 | Reading/Decoding, Writing, Oral/Listening, Vocabulary/Grammar, Literature |
| EVS / Science | 4-5 | Living World, Physical World, Earth/Environment, Health, Society |
| Social Studies | 3-5 | History, Geography, Civics, Economics |
| Art / Music | 3-4 | Visual Art, Music/Rhythm, Craft, Performance |

---

## Input validation checklist

Before launching the pipeline, verify:

1. At least one source document is readable (not a scanned image with no OCR, not a password-protected PDF).
2. The grade range matches the source documents. If textbooks cover classes 1-5, the grade range should be 1-5, not 1-8.
3. The available materials list reflects reality. If you are unsure, list the minimum: blackboard, chalk, slates, paper, pencil. Activities will be designed for these.
4. The groups make pedagogical sense. In a multi-grade room, grouping by skill level (not grade) is the standard approach. Three level-based groups (beginning, middle, advanced) is the default.
5. The output language is one the AI system can write fluently. For less common languages, consider generating in English first and translating as a separate step.

---

## Example: maths for Indian multi-grade primary school

```yaml
subject_name: Mathematics
subject_code: MATH
output_language: English

grade_start: 1
grade_end: 5

groups:
  - group_id: "A"
    group_label: "Group A (Beginning)"
    description: "Foundational skills, oral/hands-on. Most children cannot read yet."
    teaching_mode: "oral and hands-on"
  - group_id: "B"
    group_label: "Group B (Middle)"
    description: "Building fluency. Mix of oral, hands-on, and written."
    teaching_mode: "mixed"
  - group_id: "C"
    group_label: "Group C (Advanced)"
    description: "Application-level skills. Written and analytical."
    teaching_mode: "written and analytical"

classroom_model: multi-grade
period_minutes: 45
available_materials:
  - blackboard
  - chalk
  - slates
  - stones
  - sticks
  - leaves
  - bottle caps
  - paper
  - string
  - water
  - containers
  - local coins and notes
unavailable_materials:
  - printer
  - internet
  - devices
  - projector
  - printed worksheets
class_size_range: "15-40"
days_per_week: 5
total_weeks: 30

strands:
  - strand_id: NUM
    strand_name: "Numbers and Place Value"
    strand_description: "Counting, reading, writing and comparing numbers; place value and number sense"
  - strand_id: OPS
    strand_name: "Operations"
    strand_description: "Addition, subtraction, multiplication, division, fractions and decimals"
  - strand_id: GEO
    strand_name: "Shapes and Space"
    strand_description: "2-D and 3-D shapes, symmetry, angles, spatial reasoning"
  - strand_id: MEA
    strand_name: "Measurement"
    strand_description: "Length, weight, capacity, time, money; estimating and converting units"
  - strand_id: DAT
    strand_name: "Data Handling and Patterns"
    strand_description: "Sorting, pictographs, bar graphs, tables; number and shape patterns"

sources:
  - "sources/ncert-learning-outcomes-maths.pdf"
  - "sources/ncert-textbook-class1.pdf"
  - "sources/ncert-textbook-class2.pdf"
  - "sources/ncert-textbook-class3.pdf"
  - "sources/ncert-textbook-class4.pdf"
  - "sources/ncert-textbook-class5.pdf"
  - "sources/nipun-bharat-numeracy-goals.pdf"
  - "sources/das-mgml-article.txt"
```

## Example: Hindi language for single-grade remedial class

```yaml
subject_name: Hindi Language
subject_code: HINDI
output_language: Hindi

grade_start: 3
grade_end: 3

groups:
  - group_id: "A"
    group_label: "Group A (Beginning)"
    description: "Below grade level, phonics-based"
    teaching_mode: "oral, phonics-based"
  - group_id: "B"
    group_label: "Group B (Middle)"
    description: "At grade level, mixed reading and writing"
    teaching_mode: "mixed reading and writing"
  - group_id: "C"
    group_label: "Group C (Advanced)"
    description: "Above grade level, independent reading and composition"
    teaching_mode: "reading and composition"

classroom_model: multi-level
period_minutes: 40
available_materials:
  - blackboard
  - chalk
  - slates
  - storybooks (5-6 graded readers)
  - picture cards
  - paper
  - pencil
unavailable_materials:
  - printer
  - internet
  - devices
class_size_range: "20-35"
days_per_week: 6
total_weeks: 30

sources:
  - "sources/ncert-learning-outcomes-hindi.pdf"
  - "sources/rimjhim-class3.pdf"
  - "sources/nipun-bharat-fln-goals.pdf"
```
