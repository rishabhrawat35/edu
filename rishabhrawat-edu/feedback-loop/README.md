# Teacher feedback loop

The teacher talks to an ElevenLabs voice agent after class. n8n picks up the call, AgenticOrg turns it into clean feedback JSON, n8n writes it to her plan sheet, an n8n agent replans the affected days, and she gets a short email.

## Flow

- **n8n "1.1 Remind the teacher at 2 pm to call about today's class"**: Monday to Saturday at 2 pm, if nothing was reported today, emails her the call link.
- **Teacher calls** the ElevenLabs agent "Maths class feedback" (prompt: `elevenlabs-feedback-agent-prompt.md`). It asks for the day and topic, then yes / partly / no for Groups A, B and C, what's left, and what to change.
- **n8n "1.2 Read the feedback call and save it in the teacher sheet"** (checks every minute):
   - pulls each new finished call (transcript and the agent's collected fields)
   - reads the teacher sheet and finds the rows near the day she named
   - runs two branches in parallel: **ElevenLabs data (direct)**, the voice agent's 12 data-collection fields, and **AgenticOrg**, which gets the transcript, those fields and the nearby rows and returns the same 12 fields plus a per-group `pending` list (prompt: `agenticorg-system-prompt.txt`)
   - **Merge both → Combine (ElevenLabs first)**: every ElevenLabs value wins; AgenticOrg only fills fields ElevenLabs left empty. The Feedback (JSON) column records the source of each field
   - writes columns 9-15 of that day's row: Completed, What went well, What went wrong, How to improve, What is left, Reported on, Feedback (JSON)
   - follows the plan's rules: Yes = move on; No = she repeats the day (no change); a second No on the same day = an easier version of that day; Partly or a change request = replan the rest of the topic
- **n8n "1.3 Update the next days' plan from the feedback"**: picks the days it may change (rest of the topic, or the next topic after a topic's last day), replans them, saves new Docs in "Updated plans", updates the sheet rows, then starts 1.4. How it works inside: `replanner-v2.md`. The first version is kept as "Old 1.3 Update the next days' plan (first version, not used)" (prompts in `n8n-replanner-prompts.md`).
- **n8n "1.4 Email the teacher what changed in the plan"**: a short plain-text email: what she told us (one line), what changed (one line per day), and the sheet link.

## Settings (the "Config" node in 1.2)

| Setting | Value now | Change to |
|---|---|---|
| elevenlabs_agent_id | agent_3001m5psjmaee9ea0ng2db55xm0c (Teacher_feedback) | |
| agenticorg_agent_id | 5ff26e8e-8384-4ca9-bead-681542ace025 | |
| teacher_sheet_id | Demo Teacher - Maths Plan, personal Drive (1AIgwO8j8q54vOO9ExB1_wmCjnAigvnY1Pdds23mpP4Y) | |
| teacher_email | rishabhrawat35@gmail.com | |

1.1 has its own Config node with the same sheet and email, plus `call_link` (set it to the new agent's talk-to link).

## Sheet columns (tab "Plan", edited in place in the template and the demo copy)
1 Day, 2 Topic, 3-5 Group A/B/C today, 6 Plan, 7 Plan status, 8 Original plan, 9 Completed (Yes / Partly / No / No class), 10 What went well, 11 What went wrong, 12 How to improve, 13 What is left, 14 Reported on, **15 Feedback (JSON)** (new).

## Where things live (personal Drive, rishabhrawat35@gmail.com)
- Edu Maths MVP/Maths-Master: Curriculum data sheet, Template - Teacher Maths Plan, Day plans/ (42 topic folders, 150 Docs)
- Edu Maths MVP/Teachers/Demo Teacher - Demo School: Demo Teacher - Maths Plan, Updated plans/

## Known limits
- "Test now" in 1.2 uses a pinned sample call (Day 2, Partly). Unpin "ElevenLabs: list calls" and "ElevenLabs: get call" to test with real calls.
- Email is sent from the Gmail connected to n8n (rishabhrawat35@gmail.com).
- Data arrives about a minute after the call ends, not during the call.

## Suggested next workflows
- **New teacher onboarding:** copy the template sheet and an empty "Updated plans" folder for her, then email the links.
- **Weekly summary:** every Friday, one short email listing the days done, what went wrong, and what was changed.

## Workflow names in n8n
| Name | Job |
|---|---|
| 1.1 Remind the teacher at 2 pm to call about today's class | 2 pm email with the call link if nothing was reported today (off) |
| 1.2 Read the feedback call and save it in the teacher sheet | new call → ElevenLabs + AgenticOrg → sheet → starts 1.3 |
| 1.3 Update the next days' plan from the feedback | replans the topic's days, new Docs, sheet update → starts 1.4 |
| 1.4 Email the teacher what changed in the plan | short plain-text email |
| Old 1.3 Update the next days' plan (first version, not used) | earlier replanner, kept for reference |
| 9.1 to 9.6 Test: ... | early AgenticOrg experiments |
