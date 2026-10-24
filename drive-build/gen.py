import csv,itertools,json,html,os
import html as H
S='/mnt/user-data/uploads/edu/rishabhrawat-edu/maths-curriculum/output/'
p=list(csv.DictReader(open(S+'plans.csv')))
a={r['activity_id']:r for r in csv.DictReader(open(S+'activities.csv'))}
l={r['level_id']:r for r in csv.DictReader(open(S+'levels.csv'))}
st={r['strand_id']:r['name'] for r in csv.DictReader(open(S+'strands.csv'))}
e=html.escape
topics=[];day2topic={}
for i,(k,g) in enumerate(itertools.groupby(p,key=lambda r:r['strand_id']),1):
  g=list(g);d0,d1=g[0]['day_no'],g[-1]['day_no']
  name=f"T{i:02d} {st[k]} (Days {d0}-{d1})"
  topics.append({'no':i,'strand':k,'name':name,'days':[r['day_no'] for r in g]})
  for r in g: day2topic[r['day_no']]=i
os.makedirs('docs',exist_ok=True)
for r in p:
  t=topics[day2topic[r['day_no']]-1]
  out=[f"<h1>Day {r['day_no']}: {e(st[r['strand_id']])}</h1>",f"",
       f"<h2>Whole class opening (5 min)</h2><p>{e(r['shared_opening'])}</p>",f"<h2>Rotation</h2><p>{e(r['rotation'])}</p>"]
  for G,N in (('a','A, Beginning'),('b','B, Middle'),('c','C, Advanced')):
    lv=l[r[f'group_{G}_level_id']];ac=a[r[f'group_{G}_activity_id']]
    steps=ac['steps_english']
    import re
    def cands(k,frm):
      return [x for x in re.finditer(r'(?:^|(?<=\s))%d\.\s(?=[A-Z0-9"(])'%k,steps) if x.start()>=frm]
    def pick(k,frm):
      c=cands(k,frm)
      if not c: return None
      nxt=cands(k+1,c[0].end())
      lim=nxt[0].start() if nxt else len(steps)+1
      c=[x for x in c if x.start()<lim] or c
      good=[x for x in c if re.search(r'[.)"]\s*$',steps[:x.start()])]
      return (good or c)[0]
    items=[];m=pick(1,0)
    if not m: items=[steps]
    else:
      n=1
      while m:
        m2=pick(n+1,m.end())
        items.append(steps[m.end():m2.start() if m2 else len(steps)].strip());m=m2;n+=1
    out.append(f"<h2>Group {N}</h2><p><b>Skill ({lv['level_id']}):</b> {e(lv['can_statement'])}</p><p><b>Activity ({ac['activity_id']}):</b> {e(ac['title'])}, {ac['minutes']} min. <b>Materials:</b> {e(ac['materials'])}</p><ol>"+''.join(f"<li>{e(s)}</li>" for s in items)+f"</ol><p><b>Check:</b> {e(r['check_question_'+G])}</p>")
  open(f"docs/day{int(r['day_no']):03d}.html",'w').write(''.join(out))
json.dump(topics,open('topics.json','w'),indent=0)
print(len(topics), sum(os.path.getsize('docs/'+f) for f in os.listdir('docs')))
