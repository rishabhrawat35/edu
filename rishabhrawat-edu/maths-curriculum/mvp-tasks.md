# Multi-grade maths MVP: the tasks

What we are building: a system for a teacher who has grades 1 to 5 in one room. Children are placed into three level-based groups (A = beginning, B = middle, C = advanced) by a starting check, not by grade. The system gives the teacher a daily maths plan with one line per group, asks her every day how it went (by a short form or a short phone call with a voice agent), changes the next day's plan based on her answer, and at the end of each module gives her a test and a revision plan.

Tools: n8n for all automation, an AI model through an API (OpenAI or similar), Google Sheets and Drive for data, Gmail for sending, ElevenLabs for the voice agent, a Google Form as the second feedback channel. No login. The teacher's phone number is her identity.

The tasks are in the order they should be done. Each one says what to do and what you have at the end.

---

## Phase 1: Get the content ready (before any automation)

### Task 1. Pick one module of maths and go end to end with it
Do not build the whole year. Pick one topic that appears across all levels, for example "numbers and place value". Everything below is done for this one module first. Add more modules only after the pilot works.

End result: one module chosen.

### Task 2. Collect the five maths textbooks
Get the Uttarakhand state maths textbooks for grades 1 to 5 as PDFs. Also download the NIPUN Bharat goals for grades 1 to 3, so our plan matches what the state already asks teachers to do.

End result: five PDFs and the NIPUN goals in one Drive folder.

### Task 3. Pull out the chapters for this module and put them on a ladder
Use the AI to read the five books and list every chapter and page that belongs to the chosen module. Then arrange those into levels, from the simplest skill to the hardest. A level is a skill, not a grade. For example, level 1 is "counts to 20", level 4 is "reads a three-digit number". Grades map onto levels, but a grade 4 child may be at level 2.

Write this into a Google Sheet called Curriculum. Columns: module, level, skill in one sentence, textbook grade and page.

End result: the Curriculum sheet for one module, checked by you.

### Task 4. Write the activities for each level
For each level, write three to five short teaching activities that work with a blackboard, slates, stones, sticks or things found in a village classroom. Each activity has an ID, the level it belongs to, the steps for the teacher in simple Hindi, a mode tag (oral, hands-on or written), and roughly how many minutes it takes. Group A activities must be oral or hands-on, because most of those children cannot read yet.

The AI drafts them. A teacher or someone who has taught small children reads every one and fixes them. AI-written Hindi content needs human editing; do not skip this.

Put them in a sheet called Activities, with a column "reviewed by" that must be filled before an activity can be used.

End result: 15 to 25 reviewed activities for one module.

### Task 5. Write the starting check
Write one starting check for the whole room (all grades 1 to 5 together) that places each child into group A, B or C. The check is spoken aloud, because group A children cannot read yet. It takes about 10 minutes and tests skills from each strand at three difficulty levels. A child who gets the easy questions right but not the middle ones goes into group A. A child who gets the middle questions right but not the hard ones goes into group B. A child who gets most hard questions right goes into group C.

End result: one starting check, spoken, with a simple scoring rule that places each child in a group.

---

## Phase 2: Set up the data

### Task 6. Create the remaining sheets
Six sheets in total. Keep the columns to the minimum.

| Sheet | What one row is | Columns |
|---|---|---|
| Curriculum | one level of one module | module, level, skill, textbook grade and page |
| Activities | one activity | activity ID, module, level, title, steps in Hindi, mode, minutes, reviewed by |
| Teachers | one teacher | phone number, name, school, grades she has, number of children per group (A/B/C), current module, group A level per strand, group B level per strand, group C level per strand |
| Plans | one day's plan for one teacher | phone number, day_no, module, activity ID for group A, activity ID for group B, activity ID for group C, link to the PDF, "followed" (filled from feedback) |
| Feedback | one group on one day | phone number, day_no, group (A/B/C), result (yes, partly, no, no class), note in teacher's words, source (form or call) |
| Tests | one group's test for one module | phone number, module, group (A/B/C), children tested, children passed |

The group profiles (a five-line note on each group) are stored as cells in the Teachers sheet, not a separate sheet. The change log the teacher sees is built from Plans and Feedback, so it is not a sheet.

End result: six sheets with headers, shared with the n8n service account.

### Task 7. Create the teacher sign-up form
A Google Form: name, phone number, school, which grades she has, how many children in each. When submitted, n8n adds a row to Teachers.

End result: form live, n8n writes a row.

---

## Phase 3: Build the automations in n8n

### Task 8. Sunday plan flow
Runs every Sunday evening for each teacher.
1. Reads her current module and her three group levels from Teachers.
2. Reads her group profiles and the last two weeks of Feedback.
3. Asks the AI to write the week's plan: one shared opening for the whole room per day, one activity ID per group per day picked from Activities, a rotation (the teacher guides one group for 15 minutes while the other two practise independently, then rotates — 3 blocks in a 45-minute period), and the blackboard version of each task. The AI chooses activities; it does not invent them.
4. Writes one row per day into Plans and saves the plan as a PDF in Drive.
5. Puts the plan into a review list. You read it and press approve. Only then does step 6 run.
6. Emails the PDF to the teacher. For the pilot, you also forward it on WhatsApp by hand.

End result: a tested flow, one teacher, one week.

### Task 9. Daily feedback form
A short Google Form, one per teacher, sent as a link every afternoon by email and WhatsApp. For each group (A, B, C): "Could most of them do it?" with the answers yes, partly, no, and "no class today". One optional box: "What went wrong?" n8n writes one row per group into Feedback with source = form.

End result: form live, rows appear in Feedback.

### Task 10. Daily feedback by voice agent
Set up an ElevenLabs conversational agent that the teacher calls (she calls in; we do not call out, because automated outbound calls in India need telecom registration).

1. The agent knows the caller by phone number. On the call it looks up today's plan through an n8n webhook.
2. The script is fixed and short: greeting, "Could most of group A do today's task, yes, partly, or no?", same for group B, same for group C, then "What went wrong, in one line?", then a goodbye. If she says there was no class, it records that and ends.
3. Each answer goes to an n8n webhook that writes one row per group into Feedback with source = call. The webhook only writes and replies "saved". Nothing slow runs during the call.
4. The call is capped at three minutes.
5. The agent can also do three commands if asked: "send me tomorrow's plan", "send this week's plan again", "send the test". Each is just an email trigger in n8n.
6. Tell teachers in onboarding that calls are recorded and that they can refuse recording.
7. Set a monthly spend cap on the ElevenLabs account.

End result: a working number, calls save rows, three commands work.

### Task 11. After-the-call flow
Runs when a Feedback row arrives, from the form or the call.
1. If any group said partly or no, the AI picks a different activity for the same level for tomorrow and updates tomorrow's row in Plans.
2. It rewrites that group's five-line profile in Teachers, only when the answer was partly or no, and keeps the old version in a dated cell beside it.
3. It emails the adjusted plan within ten minutes.
4. If no feedback has arrived by evening, tomorrow's plan still goes out unchanged. Silence must never stop the plan.

End result: change an answer to "no" and tomorrow's plan changes.

### Task 12. Friday summary
Every Friday, n8n builds a short list from Plans and Feedback: what we planned, what went wrong in her words, what we changed. It is emailed to her, and the voice agent reads it aloud in about one minute at the start of Friday's call before asking the usual questions. This is how she learns what is working in her own room.

End result: one real summary read on one call.

### Task 13. Module test and revision plan
When the module's last week ends:
1. The AI writes a test from what was actually taught. The test has three sections — one per group — at the appropriate level. Group A's section is spoken aloud. Groups B and C write on paper or slate.
2. It writes a two-day revision plan aimed at the levels that got partly or no most often, one plan per group.
3. Both are emailed to her.
4. On the next call or form, she reports how many children in each group were tested and how many passed. That goes into Tests.

End result: test, revision plan, and a row in Tests.

### Task 14. Review queue
One sheet or a simple n8n approval step where everything the AI writes for a teacher (weekly plan, test, revision plan) waits for a human to approve. Nothing generated goes to a teacher without this during the pilot.

End result: nothing reaches a teacher unreviewed.

### Task 15. Teacher's diary (parked)
Do not build yet. First ask one cluster coordinator for the exact format of the daily teacher diary and whether an app-generated version would be accepted. Build only if the answer is yes, in writing.

---

## Phase 4: Test the voice part before relying on it

### Task 16. Week-zero voice check
Before the pilot, three teachers each make one test call. Compare what the agent saved with what they actually said. If more than about one in five answers is wrong, the form becomes the main channel and the call is used only for the free-text note. Decide this before week one, not during it.

End result: a written decision on which channel is primary.

---

## Phase 5: Run the pilot

### Task 17. Find three to five teachers
Go through a cluster resource coordinator or an NGO already working in the district. Include at least one teacher who is not enthusiastic.

### Task 18. Onboarding, 30 minutes each
In person or on a phone call. Cover: what the weekly plan looks like, how the 3-group rotation works (teacher guides one group while the other two practise, rotating every 15 minutes in a 45-minute period), what the daily form and call ask, that calls are recorded, and whom to message if something breaks (you). Run the starting check (Task 5) in this visit or the next day, and enter the group levels in Teachers.

### Task 19. Write the success numbers before the pilot starts
Three numbers, written down and not changed later:
1. On how many school days did she give feedback without a reminder? Target: more than half of days in weeks three and four.
2. On how many days did she say she followed the plan? Target: more than half.
3. Did the module test pass count beat what the starting check suggested?

### Task 20. Run four weeks, one module
Visit or call unannounced in week two and week four and ask what happened in class that day. Teachers who answer forms may still not be teaching the plan.

### Task 21. Decide
If the three numbers are met, add the second module and two more teachers. If not, the problem is adoption, not the product, and the next step is a human mentor per group of schools, not more features.

---

## What is not in this MVP
- Anything per student. Feedback, tests and profiles are per group.
- A website beyond a single page that shows the day's plan.
- Learning across schools. That needs data from many pilots.
- Automated WhatsApp sending. Done by hand for now.
- The teacher diary, until the format is confirmed.
