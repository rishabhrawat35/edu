# Maths Drive build: reusable assets

Built on 2026-10-24 in the work-account Drive (rishabh.rawat@onsurity.com). This copy is being superseded by a rebuild in Rira's personal Drive.

- docs/dayNNN.html: final HTML for each of the 150 day plans (3 groups, A/B/C). Uploading one with mimeType text/html converts it to a Google Doc. Step-splitting bugs and the truncated day 79-80 check question have already been fixed in these files.
- topics.json: 42 topic blocks (T01-T42) and the days in each block. Folder names are "Txx <Strand>".
- gen.py: regenerates docs/ from output/plans.csv + activities.csv. sheet.py: writes the 14-column teacher sheet CSV.
- template150.csv / demo150.csv: teacher sheet rows. The links in them point at the work-account Docs (docids.json); swap them for the new Doc IDs. Add column O "Feedback (JSON)".
- ids.json / docids.json: work-account folder and Doc IDs.
