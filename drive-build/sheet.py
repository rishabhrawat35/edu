import csv,json,sys,io
O='/mnt/user-data/uploads/edu/rishabhrawat-edu/maths-curriculum/output/'
acts={r['activity_id']:r['title'] for r in csv.DictReader(open(O+'activities.csv'))}
plans=list(csv.DictReader(open(O+'plans.csv')))
t=json.load(open('topics.json'));ids=json.load(open('ids.json'));docs=json.load(open('docids.json'))
d2t={int(x):tt for tt in t for x in tt['days']}
H=['Day','Topic','Group A today','Group B today','Group C today','Plan','Plan status','Original plan','Completed','What went well','What went wrong','How to improve','What is left','Reported on']
def link(u,txt): return f'=HYPERLINK("{u}","{txt}")'
demo=sys.argv[1]=='demo'
out=io.StringIO();w=csv.writer(out);w.writerow(H)
for p in plans:
  n=int(p['day_no']);tt=d2t[n];topic=tt['name'].split(' (')[0]
  if str(n) in docs: u=f"https://docs.google.com/document/d/{docs[str(n)]}";lt="Open"
  else: u=f"https://drive.google.com/drive/folders/{ids['folders'][str(tt['no'])]}";lt="Uploading, open folder"
  row=[n,topic,acts[p['group_a_activity_id']],acts[p['group_b_activity_id']],acts[p['group_c_activity_id']],link(u,lt),'Original','','','','','','','']
  if demo and n==1: row[8:]=['Yes','All three groups enjoyed the hands-on counting. Group C finished early.','Group A needed more time to count past 15.','Give Group C an extra challenge card.','','2026-10-21']
  if demo and n==2: row[8:]=['Partly','Body counting worked well for Group A. Group C wrote number names correctly.','Group B mixed up tens and ones when zero was in the middle (408 written as 48). Dictation not finished.','Revisit zero-in-the-middle with bundles before moving on.','Group B: last 2 dictation rounds','2026-10-22']
  if demo and n==3:
    row[5]=link('https://docs.google.com/document/d/1hqXWOjRBGyZFDr4xHdfLGOTpmmPg2ioaGv-84tJeJRM','Open (updated)');row[6]='Updated 2026-10-24';row[7]=link(f"https://docs.google.com/document/d/{docs['3']}",'Open')
  w.writerow(row)
print(out.getvalue(),end='')
