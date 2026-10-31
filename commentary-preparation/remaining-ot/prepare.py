import json,re,unicodedata,collections
from pathlib import Path
spec=[('Jozua','JOS',6,24),('Richteren','JDG',7,21),('Ruth','RUT',8,4),('I Samuël','1SA',9,31),('II Samuël','2SA',10,24),('I Koningen','1KI',11,22),('II Koningen','2KI',12,25),('Ezra','EZR',15,10),('Nehemia','NEH',16,13),('Ester','EST',17,10),('Job','JOB',18,42),('Psalm','PSA',19,150),('Spreuken','PRO',20,31),('Prediker','ECC',21,12),('Hooglied','SNG',22,8),('Jesaja','ISA',23,66),('Jeremia','JER',24,52),('Klaagliederen','LAM',25,5),('Ezekiël','EZK',26,48),('Daniël','DAN',27,12),('Hosea','HOS',28,14),('Joël','JOL',29,3),('Amos','AMO',30,9),('Obadja','OBA',31,1),('Jona','JON',32,4),('Micha','MIC',33,7),('Nahum','NAM',34,3),('Habakuk','HAB',35,3),('Sefanja','ZEP',36,3),('Haggai','HAG',37,2),('Zacharia','ZEC',38,14),('Maleachi','MAL',39,4)]
normalize=lambda s:re.sub(r'\s+',' ',unicodedata.normalize('NFC',s)).strip().casefold()
lookup={normalize(n): (n,id,bid,count) for n,id,bid,count in spec};lookup['dem psalm']=lookup['psalm']
books=[];issues=[];repairs=[];classifications={}
for f in sorted(Path('remaining-ot').glob('*-paragraphs.json')):
 P=json.loads(f.read_text());expanded=[]
 for x in P:
  embedded={'Richteren-paragraphs.json':{220:'14. Wan loetoe'},'JOB-paragraphs.json':{191:'11. San de'},'DEM PSALM-paragraphs.json':{813:'16. Mi tem',2128:'22. Opo'}}.get(f.name,{})
  mixed={'DEM PSALM-paragraphs.json':{1549},'JOB-paragraphs.json':{427},'EZEKIËL - MALACHI-paragraphs.json':{4462},'PREDIKER - KLAADLIEDEREN-paragraphs.json':{4521}}.get(f.name,set())
  if x['index'] in embedded:
   k=x['text'].index(embedded[x['index']]);expanded.extend([dict(x,text=x['text'][:k]),dict(x,text=x['text'][k:])]);repairs.append([f.name,x['index'],'recover embedded verse'])
  elif x['index'] in mixed:
   verse=' '.join(r['text'].strip() for r in x['runs'] if r['bold'] and r['text'].strip());comment=' '.join(r['text'].strip() for r in x['runs'] if not r['bold'] and r['text'].strip());expanded.extend([dict(x,text=verse),dict(x,text=comment)]);repairs.append([f.name,x['index'],'separate inline commentary'])
  else:expanded.append(x)
 P=expanded
 b=None;c=None;pending=[];note=None;handled={};classifications[f.name]=handled
 def record(i,kind):handled.setdefault(str(i),[]).append(kind)
 def chapter(n):
  global c,pending,note
  c={'chapter':n,'sections':[],'verses':[],'notes':[],'preface':[]};b['chapters'].append(c);pending=[];note=None
 for x in P:
  i=x['index'];t=x['text'].strip()
  if not t:continue
  key=normalize(t)
  if key in lookup:
   name,id,bid,count=lookup[key];b={'name':name,'id':id,'number':bid,'expectedChapters':count,'source':f.name,'introduction':[],'chapters':[]};books.append(b);c=None;pending=[];note=None;record(i,'book')
   if count==1:chapter(1)
   continue
  m=re.fullmatch(r'(.+?)\s+(\d+)',t)
  if m and normalize(m[1]) in lookup:
   name,id,bid,count=lookup[normalize(m[1])]
   if b is None or b['id']!=id:
    b={'name':name,'id':id,'number':bid,'expectedChapters':count,'source':f.name,'introduction':[],'chapters':[]};books.append(b)
   chapter(int(m[2]));record(i,'chapter');continue
  if b is None:issues.append([f.name,i,'beforeBook',t[:100]]);continue
  if c is None:b['introduction'].append({'text':t,'sourceParagraph':i});record(i,'introduction');continue
  chars=sum(len(r['text'].strip()) for r in x['runs']);both=sum(len(r['text'].strip()) for r in x['runs'] if r['bold'] and r['italic']);bold=sum(len(r['text'].strip()) for r in x['runs'] if r['bold'])
  if both>=max(1,chars*.9) and not re.match(r'^\d+[. ]',t):
   c['sections'].append({'text':t,'beforeVerse':None,'sourceParagraph':i});note=None;pending=[];record(i,'section');continue
  m=re.match(r'^(\d+)(?:[.,]\s*|\s+(?=[A-Z]))(.*)$',t,re.S)
  if m:
   n=int(m[1]);prev=c['verses'][-1]['verse'] if c['verses'] else 0
   if n!=prev+1 and not (b['id']=='PSA' and prev==0 and n in [2,3]):issues.append([f.name,b['id'],c['chapter'],i,'sequence',prev,n,t[:120]])
   c['verses'].append({'verse':n,'text':m[2],'sourceParagraphs':[i]});record(i,'scripture')
   if note is not None:pending=[];note=None
   pending.append(n)
   for s in c['sections']:
    if s['beforeVerse'] is None:s['beforeVerse']=n
   continue
  if bold>=max(1,chars*.9) and c['verses'] and not (f.name=='RUTH-paragraphs.json' and i==144):
   c['verses'][-1]['text']+=' '+t;c['verses'][-1]['sourceParagraphs'].append(i);repairs.append([f.name,i,'Scripture continuation']);record(i,'scriptureContinuation');continue
  if not c['verses']:c['preface'].append({'type':'paragraph','text':t,'sourceParagraphs':[i]});record(i,'preface');continue
  if i in {'NEHEMIA-paragraphs.json':{14,109},'PREDIKER - KLAADLIEDEREN-paragraphs.json':{5261}}.get(f.name,set()):
   assert note and note['blocks']
   note['blocks'][-1]['text']+=' '+t;note['blocks'][-1]['sourceParagraphs'].append(i);repairs.append([f.name,i,'commentary continuation']);record(i,'commentaryContinuation');continue
  if note is None:
   note={'id':f'patton-srn-{b["id"]}-{c["chapter"]}-{i}','verseStart':pending[0] if pending else None,'verseEnd':pending[-1] if pending else None,'blocks':[]};c['notes'].append(note)
   if not pending:issues.append([f.name,b['id'],c['chapter'],i,'unanchored',t[:120]])
  note['blocks'].append({'type':'paragraph','text':t,'sourceParagraphs':[i]});record(i,'commentary')
for b in books:
 nums=[c['chapter'] for c in b['chapters']]
 if nums!=list(range(1,b['expectedChapters']+1)):issues.append([b['source'],b['id'],'chapters',nums,b['expectedChapters']])
 print(b['id'],b['source'],len(nums),sum(len(c['verses']) for c in b['chapters']),sum(len(c['notes']) for c in b['chapters']))
Path('remaining-ot/data.json').write_text(json.dumps({'books':books},ensure_ascii=False,indent=2));Path('remaining-ot/issues.json').write_text(json.dumps(issues,ensure_ascii=False,indent=2));Path('remaining-ot/classifications.json').write_text(json.dumps(classifications));Path('remaining-ot/repairs.json').write_text(json.dumps(repairs,ensure_ascii=False,indent=2));print('ISSUES',len(issues));print(json.dumps(issues,ensure_ascii=False,indent=2))
