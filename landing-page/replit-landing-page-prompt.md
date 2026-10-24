# Landing page for the one-room maths plan: Replit prompt and full copy

How to use this file: copy everything from "PROMPT FOR REPLIT" to the end and paste it into Replit as one message. Before pasting, check the feedback link in section 1 (it is the ElevenLabs "talk to agent" link for the Teacher_feedback agent).

---

# PROMPT FOR REPLIT

Build a single-page website (one landing page, no other pages, no backend, no login, no forms, no database). Use React with Vite and Tailwind CSS. Build the page from small reusable components, one file per component, listed in section 4. All copy is given in section 5: use it word for word. Do not add text of your own.

## 1. What this page is

This is the daily home page for a teacher in a village school who teaches maths to grades 1 to 5 together in one room. She already has her plan in a Google Sheet. She opens this page after class. The page has one job: get her to tap "Tell us how today went", which opens a short voice call. Everything else on the page tells the story of how her plan was made and how it changes after each call, so she trusts it.

The only interactive element is the feedback button. Every feedback button on the page opens this link in a new tab:

`https://elevenlabs.io/app/talk-to?agent_id=agent_3001m5psjmaee9ea0ng2db55xm0c`

Store it once as a constant `FEEDBACK_URL` in `src/config.js` so it can be changed in one place. Buttons are `<a href={FEEDBACK_URL} target="_blank" rel="noopener noreferrer">`.

The only other interaction allowed: the FAQ items open and close, and the top bar links scroll to sections. Nothing else.

## 2. Who reads it and what they must feel

- A teacher, often on a cheap Android phone, often on a slow connection. Design mobile first (360px wide), then scale up to desktop.
- English is her second or third language. Short sentences. Big text. No jargon.
- She should feel: "This was made for my room. Somebody did the hard work. It listens to me. I stay in charge."
- A visitor (a judge, a school leader) reading on a laptop should see the depth of work behind the plan.

## 3. Design direction

Theme: a village classroom. Slate, chalk, a blackboard, stones on the floor, warm afternoon light. Calm and respectful, not childish, not a tech startup.

Colours (define as Tailwind theme colours, use only these):
- `paper` #F6F2E8 (main page background, like a notebook page)
- `card` #FFFDF7 (cards)
- `line` #E2DCCB (borders)
- `board` #1D2B28 (blackboard green, dark sections and headings)
- `chalk` #C9D6CF (body text on dark)
- `ink` #26302D (main text on light)
- `muted` #4A524F (body text on light)
- `clay` #A8521A (small labels on light, links)
- `sun` #E8A35F (the one accent: buttons, big numbers on dark)
- Group colours, used only to mark the three groups, always with the group name written next to them:
  - `groupA` #F4D2A6 with border #E8A35F (Group A, Beginning)
  - `groupB` #C9E1EA with border #5B9BB5 (Group B, Middle)
  - `groupC` #CFE3D6 with border #2F6B4F (Group C, Advanced)

How the colours carry meaning: dark blackboard sections are for "what the teacher lives with" (the problem, the daily call). Light paper sections are for "what we built for her". The orange accent appears only on things she can act on (the button) and on numbers that show work done. Group colours appear every time a group is mentioned, so the A, B, C idea is learned by eye.

Type (Google Fonts):
- Headings: Domine, weight 700.
- Body and UI: Nunito Sans, weights 400, 600, 800.
- Sizes on mobile: hero 40px, section titles 30px, card titles 20px, body 18px, labels 14px uppercase with letter spacing 0.12em. On desktop: hero 64px, section titles 44px, body 19px.
- Line height 1.5 for body. Maximum line length 65 characters.

Shapes and texture:
- Cards: radius 16px, 1px `line` border, no heavy shadows (at most a soft 0 1px 2px shadow).
- Dark sections have a very faint chalk texture: a CSS radial noise or a subtle repeating gradient at 4% opacity. No images needed.
- Small hand-drawn feel: section dividers are a thin wavy SVG line in `line` colour, like a chalk stroke.
- Icons: use lucide-react, stroke 1.75. Suggested: Phone, Mic, BookOpen, Layers, Users, CheckCircle2, ShieldCheck, Pencil, Clock, Mail, FileText, RefreshCw, Sprout.
- Illustrations: build them from shapes and SVG (circles for stones, rectangles for slates). No stock photos, no robots, no glowing brains, no sparkles.

Motion: gentle fade-up on scroll (150ms to 300ms, once). Respect `prefers-reduced-motion`. Nothing loops except one slow pulse ring around the main feedback button.

Accessibility: text contrast at least 4.5:1, buttons at least 48px tall, visible focus ring in `sun`, every icon that carries meaning has a text label next to it, semantic headings in order, `lang="en"`.

Performance: no heavy libraries beyond React, Tailwind, lucide-react and (optional) framer-motion. Page must load fast on 3G.

## 4. Components to build (in page order)

1. `TopBar`: sticky, `paper` background with bottom border. Left: wordmark. Right on desktop: anchor links (The problem, How it was built, After class, Questions) and a small feedback button. On mobile: wordmark and the small feedback button only.
2. `Hero`: two columns on desktop, stacked on mobile. Left: label, headline, sub line, main feedback button with pulse ring, a small reassurance line under it. Right: `TodayCard`.
3. `TodayCard`: a mock of one day's plan as a card that looks like a page clipped to a slate. Shows Day 12, the topic, the opening line, and three rows, one per group, each with its group colour chip, activity name and minutes. A small stamp in the corner: "Checked twice".
4. `ProblemSection` (dark `board`): label, title, story paragraph, then `OneRoomVisual`, then three `PainCard`s.
5. `OneRoomVisual`: an SVG or HTML diagram. On the left, five chips "Grade 1" to "Grade 5" scattered. Arrows lead into three wide bars "Group A, Beginning", "Group B, Middle", "Group C, Advanced" in their group colours. Under it one line of caption.
6. `IdeaSection` (light): title, paragraph, then three `GroupCard`s side by side (stacked on mobile), each with a coloured top border, group name, who it is for, starting point, and kind of work.
7. `NumbersBand` (dark): four big numbers in `sun` with labels. Count-up animation once when visible (skip if reduced motion).
8. `BuildTimeline` (light): "How your plan was made". A vertical stepper on mobile, a two-column zigzag on desktop. Eight `TeamMemberStep` cards, each with a step number, an icon, a role name ("The Researchers"), what they did in one or two lines, and a small "What they made" chip. Parallel steps (Researchers are three, Activity Writers are five) show small stacked avatars as circles with initials of the strand or source.
9. `GuardrailGrid` (light, `card` background panel): "Rules every plan must pass". A grid of eight `GuardrailItem`s, each a checkmark icon plus one rule in plain words. Below it, a small honest note.
10. `DayInTheRoom` (light): a 45-minute horizontal bar split 5 / 15 / 15 / 15 with labels, and below it three activity cards in group colours. On mobile the bar becomes a vertical list.
11. `AfterClassFlow` (dark): "After class, two minutes on the phone". Six `FlowStep`s in a horizontal track on desktop with a thin chalk line connecting them and a curved arrow from the last step back to the first labelled "Next day". On mobile, a vertical track. Then a second row, `RevisionTeam`: eight small role cards (a 4 by 2 grid on desktop, 2 columns on mobile) for the roles that rewrite the plan (The Listener, The Note-taker, The Diagnoser, The Planner, The Rule Keeper, The Second Reader, The Writer, The Messenger).
12. `IfThenRules` (light): "What happens after you call". A list of six `IfThenRow`s. Each row: left pill "If you say ..." in `card`, a right arrow icon, right text "Then ...". Rows stack on mobile.
13. `Difference` (light): "What makes this different". A comparison table with two columns, "A usual plan" and "Your plan", seven rows. On mobile each row becomes a small card with both answers.
14. `TrustStrip` (light): four small items in a row with icons: No app to install. No login. No data on single children. You can always see the original plan.
15. `FAQ` (light): six questions as accordion items using `<details>` and `<summary>`.
16. `FinalCTA` (dark `board`, full width): big line, sub line, large feedback button, small line under it.
17. `Footer`: small text.
18. `MobileStickyCTA`: on screens below 768px, a bar fixed to the bottom with the feedback button, shown after the user scrolls past the hero, hidden when `FinalCTA` is on screen.

## 5. Copy (use exactly)

Writing rules for any text the build needs that is not below (for example alt text or aria labels): simple English, short sentences, no em dashes, no exclamation marks. Never use these words: AI, artificial intelligence, agent, agentic, model, LLM, bot, smart, intelligent, magic, powerful, seamless, cutting-edge, revolutionary, transform, empower, unlock, leverage, journey, game-changer, effortless.

### TopBar
- Wordmark: **One Room Maths**
- Links: The problem · How it was built · After class · Questions
- Button: **Tell us how today went**

### Hero
- Label: FOR TEACHERS WHO TEACH GRADES 1 TO 5 TOGETHER
- Headline: **One room. Five grades. One plan that works for all of them.**
- Sub line: Every day you get one maths plan for your whole class. After class, you tell us how it went in a two-minute call. Tomorrow's plan changes to match your room.
- Button: **Tell us how today went**
- Under the button: It is a short phone call. Yes, partly or no for each group, and anything you want to change.

### TodayCard
- Top: Day 12 · Measurement
- Opening (5 min): "Show me a coin. What is it worth?"
- Group A, Beginning · Heavy or light · 10 min
- Group B, Middle · Kilogram and gram · 12 min
- Group C, Advanced · Train timetable · 12 min
- Stamp: Checked twice

### ProblemSection
- Label: THE PROBLEM
- Title: **Textbooks are written for one grade. Your room holds five.**
- Story: It is 10 o'clock. Thirty children sit in one room. Some are six years old and some are eleven. The grade 1 book is about counting. The grade 5 book is about fractions. You have one maths period and one blackboard. Whatever you teach, some children are lost and some are bored.
- OneRoomVisual caption: A child's grade does not tell you what they can do. A grade 4 child may still be counting to 20.
- PainCard 1. **One period, five books.** Five grade-wise lessons do not fit into 45 minutes.
- PainCard 2. **Mixed levels in every grade.** Children in the same grade can be years apart in maths.
- PainCard 3. **No time to plan, no one to ask.** Plans rarely change when a group gets stuck, because nobody hears what happened in class.

### IdeaSection
- Label: THE IDEA
- Title: **Group children by what they can do, not by their grade.**
- Paragraph: A ten-minute spoken check at the start places every child in one of three groups. The whole room works on the same topic each day. Each group works on its own step of that topic. You guide one group while the other two practise, then you move on.
- GroupCard A: **Group A, Beginning.** For children who are just starting. Starts at: counting objects up to 20. Work: spoken and hands-on only, because most cannot read yet.
- GroupCard B: **Group B, Middle.** For children building speed and confidence. Starts at: numbers up to 999 with hundreds, tens and ones. Work: a mix of spoken and written.
- GroupCard C: **Group C, Advanced.** For children ready for upper primary maths. Starts at: five and six digit numbers. Work: more written problems and reasoning.

### NumbersBand
- **5** areas of maths: numbers, operations, shapes, measurement, data
- **57** small steps of skill, from counting to 20 to fractions and decimals
- **172** classroom activities using stones, sticks, slates and the blackboard
- **150** ready day plans, one page each, in your Google Drive

### BuildTimeline
- Label: HOW YOUR PLAN WAS MADE
- Title: **A team of specialists built your year, and each one checked the last.**
- Intro: Nothing in your plan was guessed. It was built in eight stages. Each stage had one job, and no stage could start until the one before it passed its checks.

Steps:
1. **The Researchers** (three, working side by side). One read the national learning outcomes for maths and the NIPUN Bharat goals. One studied how teachers run multi-grade classrooms well. One went through the maths textbooks for grades 1 to 5, chapter by chapter. Made: three research notes.
2. **The Designer.** Turned the research into a ladder of skills for each area of maths. Each step on the ladder is something a child can do, like "reads a three digit number", not a chapter number. Made: 5 areas, 57 steps, 3 groups.
3. **The Challenger.** Saw the design for the first time and tried to break it. Is any learning outcome missing? Does any step depend on a step above it? Are the three groups too close together? Problems went back to the Designer. Made: a list of fixes, all closed.
4. **The Activity Writers** (five, one per area of maths, working side by side). Wrote three or four activities for every step, using only what a village classroom has. Made: 172 activities.
5. **The Teacher Reviewer.** Read every activity as a teacher would. Can this be done in the time? Are the materials really there? Is the language simple? Made: a list of fixes, applied before any plan was built.
6. **The Plan Builder.** Arranged the year into 150 days. One area of maths per day for the whole room, a different step for each group, a short opening everyone can join, and a check question for each group. Made: 150 day plans.
7. **The Final Checker.** Ran nine checks on the whole year before anything reached you. Made: every check passed.
8. **The Publisher.** Put each day on its own page in your Google Drive and linked all 150 in your plan sheet. Made: your sheet and your folders.

### GuardrailGrid
- Label: THE RULES
- Title: **Rules every plan must pass**
- Items:
  1. The three groups are never on the same step on the same day.
  2. Every activity matches the step of the group doing it.
  3. Group A never gets reading or writing work.
  4. Every activity uses only things your classroom has: blackboard, chalk, slates, stones, sticks, leaves, bottle caps.
  5. No activity is longer than 20 minutes.
  6. Every day has an opening, a rotation and one check question for each group.
  7. Every step on the ladder is taught somewhere in the year.
  8. No word that labels a child, like "weak" or "slow". We say Group A, Group B, Group C.
- Note under the grid: Every activity was first reviewed on paper. Before the pilot, a working teacher will review every one again.

### DayInTheRoom
- Label: A DAY IN YOUR ROOM
- Title: **Day 12: one period, three groups, one teacher.**
- Bar: Opening, 5 min, everyone · You with Group C, 15 min · You with Group B, 15 min · You with Group A, 15 min
- Under the bar: While you guide one group, the other two practise on their own. Who goes first changes from day to day.
- Card A (Group A, Beginning, 10 min): **Heavy or light.** Stones, leaves and two bottles, one full of water. Children pass them around and say which is heavier.
- Card B (Group B, Middle, 12 min): **Kilogram and gram.** A one kilo bag of rice. Children write three things lighter and three things heavier on their slates.
- Card C (Group C, Advanced, 12 min): **Train timetable.** Three trains on the blackboard. How long does each one take? Which one can you catch at 2:15?

### AfterClassFlow
- Label: AFTER CLASS
- Title: **Two minutes on the phone. Tomorrow's plan listens.**
- Steps:
  1. **You call.** A friendly voice asks which day you taught, then yes, partly or no for each group, and what is left.
  2. **We pick it up.** Within about a minute of the call ending.
  3. **We write it down.** Your words become a clear note for each group: what went well, what went wrong, what is still left.
  4. **Your sheet is updated.** The note goes on that day's row in your plan sheet.
  5. **Your next days are rewritten.** Only the days that need it. Every other day stays as it was.
  6. **You get an email.** One line on what you told us, one line for each day that changed.
- Loop label: Next day, you teach the new plan and call again.

RevisionTeam:
- Sub title: **Who rewrites your plan**
- **The Listener.** Takes your call and asks the same short questions every day.
- **The Note-taker.** Listens to the full call a second time and fills anything the Listener missed. What you clearly said always wins.
- **The Diagnoser.** For each group: on track, needs a repeat, or ahead. And why, in one line, like "zero in the middle of a number".
- **The Planner.** Picks new activities from the 172, never invents one. Puts unfinished work first.
- **The Rule Keeper.** Checks every rule on this page. If one fails, the Planner tries again. If it still fails, your old plan stays.
- **The Second Reader.** Asks: does the new plan answer what went wrong? Does it follow what you asked for?
- **The Writer.** Writes the new day page in simple words, with the activity steps copied exactly.
- **The Messenger.** Updates your sheet and sends your email.

### IfThenRules
- Label: WHAT HAPPENS AFTER YOU CALL
- Title: **Simple rules, so you always know what to expect.**
- Rows:
  1. If you say **yes, most of the group got it**, then the group moves on to the next day as planned.
  2. If you say **no**, then you repeat the same day. Nothing else changes.
  3. If you say **no again on the same day**, then you get an easier version of that day.
  4. If you say **partly**, or ask for a change, then the rest of the topic is rewritten, with unfinished work first.
  5. If **too much is left to fit**, then one extra day is added, for example Day 12a. Never more than one.
  6. If **you have not called by 2 pm**, then you get one reminder email. Your plan goes on as it is.

### Difference
- Label: WHAT MAKES THIS DIFFERENT
- Title: **Made for one room with five grades.**
- Table header: | | A usual plan | Your plan |
- Rows:
  1. Who it is for | One grade | Grades 1 to 5 in one room
  2. How children are grouped | By grade | By what they can do
  3. What you need | Printouts, kits, devices | Blackboard, slates, stones, sticks
  4. When it changes | At the end of the year, if ever | The day after you tell us
  5. How you give feedback | Forms and reports | A two-minute phone call
  6. Who checks it | Nobody, before it reaches you | Every day page is checked twice
  7. Who is in charge | The plan | You. Your original plan is always kept.

### TrustStrip
- No app to install
- No login, no passwords
- Nothing recorded about a single child, only about groups
- Your original plan is always one tap away in your sheet

### FAQ
- Label: QUESTIONS
1. **What if I miss a day of feedback?** Nothing breaks. Your plan simply goes on as it is. You can call the next day and talk about any day.
2. **What if the plan gets something wrong?** Say so on the call. "Group B needs more time on this" is enough. The next days will change.
3. **Can I see what changed?** Yes. Every changed day has a new page, marked "Updated" in your sheet, and the original is kept beside it.
4. **Do my children need phones or tablets?** No. Every activity uses things already in your classroom.
5. **Is the call recorded?** Yes, so we can write down what you said correctly. You can ask for it not to be recorded.
6. **How is my child's group decided?** By a short spoken check at the start, not by grade. Groups can change as children move up.

### FinalCTA
- Line: **How did today's class go?**
- Sub line: Two minutes. Yes, partly or no for each group. We will do the rest before tomorrow.
- Button: **Tell us how today went**
- Under the button: Opens a short call in a new tab.

### Footer
- One Room Maths · A daily maths plan for multi-grade classrooms, grades 1 to 5
- Built on the national learning outcomes, NIPUN Bharat goals and the NCERT maths textbooks.

### MobileStickyCTA
- Button: **Tell us how today went**

## 6. Final checks before you finish

- Search all text for the em dash character and remove every one.
- Search for every banned word in section 5 and remove it.
- Every feedback button opens `FEEDBACK_URL` in a new tab. No other buttons exist.
- Test at 360px, 768px and 1280px wide. No horizontal scrolling.
- Group A, B and C always show both their colour and their name.
- Lighthouse accessibility score 95 or more.
