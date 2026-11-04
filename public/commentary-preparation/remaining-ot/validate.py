import json,re,collections
from pathlib import Path
D=json.loads(Path('remaining-ot/data.json').read_text());classified=json.loads(Path('remaining-ot/classifications.json').read_text());total=0
norm=lambda s:re.sub(r'\s+','',s)
for source,handled in classified.items():
 P=json.loads((Path('remaining-ot')/source).read_text());assert {str(x['index']) for x in P if x['text'].strip()}==set(handled),source
 parts=[]
 for x in P:
  if any(k in handled.get(str(x['index']),[]) for k in ['book','chapter']):parts.append(x['text'])
 for b in D['books']:
  if b['source']!=source:continue
  parts.extend(x['text'] for x in b['introduction'])
  for c in b['chapters']:
   nums=[v['verse'] for v in c['verses']];assert nums==list(range(nums[0],nums[-1]+1)),(b['id'],c['chapter'],nums)
   parts.extend(x['text'] for x in c['sections']);parts.extend(x['text'] for x in c['preface'])
   for v in c['verses']:
    label=',' if b['id']=='1SA' and c['chapter']==24 and v['verse']==22 else '.'
    parts.append(str(v['verse'])+label+v['text'])
   for n in c['notes']:
    assert n['verseStart'] in nums and n['verseEnd'] in nums and n['verseStart']<=n['verseEnd'],(b['id'],c['chapter'],n)
    parts.extend(z['text'] for z in n['blocks'])
 original=collections.Counter(norm(''.join(x['text'] for x in P)));actual=collections.Counter(norm(''.join(parts)))
 assert original==actual,(source,original-actual,actual-original)
 total+=len(handled)
print('All',total,'nonempty source paragraphs accounted for; character inventories preserved.')
# Keep the standalone Esther, whose commentary is absent from the copy in Nehemiah.
kept=[b for b in D['books'] if not(b['id']=='EST' and b['source']=='NEHEMIA-paragraphs.json')]
assert len(set(b['id'] for b in kept))==32
psalms=sorted(c['chapter'] for b in kept if b['id']=='PSA' for c in b['chapters']);assert psalms==list(range(1,151))
report={'suppliedBooks':32,'suppliedChapters':sum(len(b['chapters']) for b in kept),'notes':sum(len(c['notes']) for b in kept for c in b['chapters']),'sourceVerses':sum(len(c['verses']) for b in kept for c in b['chapters']),'nonemptySourceParagraphs':total,'sourceCharacterInventoriesPreserved':True,'missing':['1 Chronicles','2 Chronicles'],'esther':'Standalone ESTER.doc used; Scripture-only Esther appended to Nehemiah retained separately.','psalmNumbering':'Source superscriptions often occur as unnumbered chapter opening text; numbered verses may begin at 2 or 3. No renumbering applied.','repairs':json.loads(Path('remaining-ot/repairs.json').read_text())}
Path('remaining-ot/conversion-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print({k:v for k,v in report.items() if k not in ['repairs']})
