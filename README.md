# One-room maths plan

A daily maths plan for a teacher who teaches grades 1 to 5 in one room, which updates itself from a 3-minute call after class.

## The problem

In many village schools, one teacher teaches grades 1 to 5 together. Textbooks are written one grade at a time, and most children are below their grade level. The teacher needs one plan she can run from a blackboard, with work for every child, and a plan that changes when a lesson doesn't land.

## How it works

The class is split into three groups by level, not by grade: **Group A (Beginning)**, **Group B (Middle)** and **Group C (Advanced)**. Each day the whole room works on one topic, and each group gets its own task. The plan is numbered by day (Day 1 to Day 150), not by date, so the teacher sets the pace.

```
 Teacher teaches Day N from her Google Sheet
        │
        ▼
 She calls the ElevenLabs voice agent (about 3 minutes)
   "Which day and topic? Yes, partly or no? How did each group do?
    What went well, what went wrong, what should change, what is left?"
        │
        ▼
 n8n 1.2  reads the call, merges the voice agent's answers with the
          AgenticOrg agent's version (voice answers win), and writes the
          feedback into Day N's row of her sheet
        │  only if the day was "Partly" or she asked for a change
        ▼
 n8n 1.3  rewrites the rest of that topic's days: unfinished work first,
          checked against the teaching rules and by an AgenticOrg
          challenger; saves new plan Docs and updates the sheet
        │
        ▼
 n8n 1.4  emails her a short note: what she said, what changed, sheet link
```

Rules the system follows:
- **Yes**: move on to the next day.
- **No**: she repeats the day as it is. A second "No" on the same day makes an easier version of it.
- **Partly**, or she asks for a change: only the remaining days of the current topic are replanned (or the next topic's days, if it was the last day of a topic). Unfinished work goes first. At most one extra day is added, such as "12a".
- Activities only come from the reviewed Activities list. Group A work is always spoken or hands-on.

## What the teacher sees

Her Google Sheet has one row per day, with these columns:

| # | Column | Filled by |
|---|---|---|
| 1-5 | Day, Topic, Group A today, Group B today, Group C today | the plan |
| 6 | Plan | link to the day's plan Doc (switches to the updated Doc after a replan) |
| 7 | Plan status | "Original", "Updated YYYY-MM-DD" or "Added YYYY-MM-DD" |
| 8 | Original plan | link to the first version, once a day is replanned |
| 9 | Completed | Yes / Partly / No / No class |
| 10-13 | What went well, What went wrong, How to improve, What is left | her call |
| 14 | Reported on | date of the call |
| 15 | Feedback (JSON) | the full structured feedback, with where each answer came from |

## Folder map

| Folder | What's inside |
|---|---|
| `rishabhrawat-edu/maths-curriculum/` | The curriculum: `output/` has strands, 57 skill levels, 172 activities, 3 groups and the 150-day plan as CSV files. `research/` has the teaching rules and reviews, `docs/` explains the columns, and `mvp-tasks.md` is the original product plan. |
| `rishabhrawat-edu/curriculum-builder/` | A reusable kit (agent prompts, schemas, checklists) for building the same kind of curriculum for another subject or language. |
| `drive-build/` | The 150 day plans as HTML (`docs/`), the topic list (`topics.json`), and the teacher sheet rows (`template150.csv`, `demo150.csv`) used to build the Google Drive copy. `gen.py` and `sheet.py` regenerate them from the CSVs. |
| `rishabhrawat-edu/feedback-loop/` | How the feedback loop works (`README.md`), the voice agent prompt (`elevenlabs-feedback-agent-prompt.md`, `elevenlabs-agent-fixes.md`), the AgenticOrg agent prompt (`agenticorg-system-prompt.txt`) and the replanner design (`replanner-v2.md`). |
| `n8n-workflows/` | Exports of the four live n8n workflows (1.1 to 1.4). Credentials are not included. |
| `landing-page/` | A ready prompt and full copy for building the project's landing page on Replit. |
| `agenticorg_test.py` | A small script to check that an AgenticOrg API key and agent work. |

## The n8n workflows

| Workflow | What it does |
|---|---|
| 1.1 Remind the teacher at 2 pm to call about today's class | At 2 pm, Monday to Saturday, emails her the call link if she hasn't called today (off by default). |
| 1.2 Read the feedback call and save it in the teacher sheet | Every minute, picks up finished calls and saves the feedback in her sheet. Starts 1.3 when needed. |
| 1.3 Update the next days' plan from the feedback | Replans the topic's remaining days and saves new Docs and sheet changes. Starts 1.4. |
| 1.4 Email the teacher what changed in the plan | Sends the short update email. |

## Set it up yourself

You need Docker, a Google account, an ElevenLabs account, an AgenticOrg account and an OpenAI or OpenRouter API key.

1. **Run n8n locally.**
   ```bash
   docker run -d --name n8n --restart unless-stopped -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n:latest
   ```
   Open http://localhost:5678 and create your account.
2. **Connect Google.** In Google Cloud, create a project, turn on the Gmail, Sheets, Docs and Drive APIs, and create an OAuth client (type "Web application") with the redirect URL `http://localhost:5678/rest/oauth2-credential/callback`. In n8n, add a "Google OAuth2 API" credential with that client and these scopes: `gmail.modify spreadsheets documents drive`.
3. **Add the other credentials in n8n:** an ElevenLabs credential, a "Header Auth" credential named `AgenticOrg API key` (name `Authorization`, value `Bearer <your AgenticOrg key>`) and an OpenAI credential.
4. **Install the ElevenLabs node.** In n8n, open the node panel, search "ElevenLabs" and click Install.
5. **Create the agents.**
   - ElevenLabs: a conversational agent with the prompt, first message and 12 data-collection fields in `rishabhrawat-edu/feedback-loop/elevenlabs-agent-fixes.md`. Turn on End call and Language detection.
   - AgenticOrg: an agent with `rishabhrawat-edu/feedback-loop/agenticorg-system-prompt.txt` as its system prompt.
6. **Build the Drive copy.** Upload each `drive-build/docs/dayNNN.html` as a Google Doc into one folder per topic (see `topics.json`), and create the teacher sheet from `drive-build/template150.csv` in a tab named "Plan", adding a 15th column, "Feedback (JSON)". Put an empty "Updated plans" folder next to the teacher sheet.
7. **Import the workflows.** In n8n, import the four files in `n8n-workflows/`, pick your credentials in each node, and set the **Config** node in 1.2 (and 1.1): ElevenLabs agent ID, AgenticOrg agent ID, teacher sheet ID and teacher email. In 1.3, set its Config too (challenger agent and admin email).
8. **Turn on** 1.2, 1.3 and 1.4 (and 1.1 if you want the reminder). Make a test call to the ElevenLabs agent, and within a minute the Day row in the sheet fills in.

To check your AgenticOrg key and agent on their own:
```bash
python3 -m venv .venv && .venv/bin/pip install agenticorg
AGENTICORG_API_KEY=ao_sk_yourkey .venv/bin/python agenticorg_test.py
```

## Good to know

- The content was built from NCERT books in English. Every activity has been reviewed only by an AI acting as a teacher; a real teacher must review it before classroom use, and Hindi steps still need to be added.
- n8n reads calls after they end, so feedback lands about a minute after the call, not during it.
- Keys and passwords are never stored in this repository. Add them only as n8n credentials.
