# Prompts in the live feedback loop

| Where | File | Edit in |
|---|---|---|
| 1.3 Diagnose | `1.3-diagnose.md` | n8n |
| 1.3 Plan (also the retry and revise text) | `1.3-plan.md` | n8n |
| 1.3 Write | `1.3-write.md` | n8n |
| 1.4 Email template | `1.4-email.md` | n8n |
| Voice agent "Teacher_feedback" | set in ElevenLabs (not copied here) | ElevenLabs |
| Structurer 5ff26e8e (used by 1.2) | `../agenticorg-system-prompt.txt` (may be older than the live one) | AgenticOrg |
| Challenger 0b35a2a4 (used by 1.3) | set in AgenticOrg | AgenticOrg |

1.2 has no prompt of its own in n8n: it sends the call to AgenticOrg as data (transcript, collected_data, summary, plan_rows, call_date).

Shared wording used by all n8n prompts: Group A (Beginning), Group B (Middle), Group C (Advanced); Completed is Yes / Partly / No / No class; group results are Yes / Partly / No / Not taught; extra days are written like Day 12a; no words that label children (weak, slow, struggling, behind, poor, bright, smart); no activity or level IDs in teacher-facing text.
