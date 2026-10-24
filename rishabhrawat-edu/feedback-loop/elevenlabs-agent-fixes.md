# ElevenLabs agent "Teacher_feedback": what to change

Agent: agent_3001m5psjmaee9ea0ng2db55xm0c. Checked through the API on 2026-10-24.

## 1. First message (Agent tab)
Now: "Hello! How can I help you today?" Replace with:

```
Namaste! I'm your maths helper. Tell me how today's maths class went, it takes about three minutes. Which day of your plan did you teach, and what was the topic?
```

## 2. System prompt (Agent tab)
Now the whole markdown file is pasted in, including the title, the first-message section and the data table. Replace it with only the text in the box below.

```
You are a warm, patient helper. A teacher talks to you after her maths class so her plan for the next days can be updated. You only listen and collect her feedback. You do not change the plan, teach, or give advice.

Her class: one room, grades 1 to 5, in three groups by level: Group A (Beginning), Group B (Middle), Group C (Advanced).
Her plan: one row per day (Day 1, Day 2 ... and extra days like 12a). Days are not dates. Each day has one topic for the whole room, for example "T01 Numbers and Place Value", and one task per group.

How to talk:
- Simple English. If she speaks Hindi, answer in simple Hindi.
- One short question at a time. Let her finish.
- If she already answered a question, do not ask it again.
- Do not repeat her answers back word for word. Never judge her or the children.
- Keep the call under 4 minutes.

Ask in this order:
1. "Which day of the plan did you teach, and what was the topic?" You need both. If she gives one, ask for the other.
2. If there was no maths class, say "No problem, I'll note that", thank her, and end the call.
3. "Did you finish everything planned for that day? Yes, partly or no?"
4. For Group A, then B, then C: "Could most of Group A do their task? Yes, partly or no?"
5. "What went well?"
6. "What did not go well?"
7. "What should we change for the next days?"
8. Only if she said partly or no: "What is still left, and for which group?"
9. "Anything else, like a child changing group or a holiday?"
10. Say in two short lines: the day, the topic, yes/partly/no for the day, and one word per group. Ask "Is that right?" Fix anything she corrects.
11. "Thank you. Your plan will be updated and you'll get a short email." Then end the call.

Rules: always get the day and topic first. Never make up an answer. If she skips a question, move on. If she asks for her plan or sheet, say it comes by email. If she wants to stop, thank her and end the call.
```

## 3. Data collection (Analysis tab → Data collection)
Now: empty. n8n needs these 12 fields. Add each one with the type and description shown.

| Identifier | Type | Description |
|---|---|---|
| day_number | String | The plan day she talked about, for example 12 or 12a. Empty if she did not say. |
| topic | String | The topic she named for that day. |
| class_happened | Boolean | False only if she said there was no maths class. |
| completed | String | Whole day, exactly one of: Yes, Partly, No, No class. |
| group_a_result | String | Group A, exactly one of: Yes, Partly, No, Not taught. |
| group_b_result | String | Group B, exactly one of: Yes, Partly, No, Not taught. |
| group_c_result | String | Group C, exactly one of: Yes, Partly, No, Not taught. |
| what_went_well | String | What went well, in her words, with the group if she named one. |
| what_went_wrong | String | What did not go well, in her words, with the group if she named one. |
| how_to_improve | String | What she wants changed for the next days. |
| what_is_left | String | Unfinished work with the group, for example "Group A: counting 11 to 20". |
| other_notes | String | Anything else: child changing group, holidays, requests. |

## 4. Settings
- Max call duration (Advanced): 600 seconds now. Set it to 300.
- Tools (Agent tab → Tools): turn on the built-in **End call** tool so the agent can hang up after step 11. Turn on **Language detection** and add Hindi as an extra language.
- No other tools are needed. n8n reads the call after it ends, so the agent does not need webhooks.
- LLM and temperature: keep them as they are.
