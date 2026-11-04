import json,re,shutil
from pathlib import Path
root=Path('work/srananbijbel-v02-main');D=json.loads(Path('remaining-ot/data.json').read_text());kept=[]
for b in D['books']:
 if b['id']=='EST' and b['source']=='NEHEMIA-paragraphs.json':
  (root/'commentary-preparation').mkdir(exist_ok=True);(root/'commentary-preparation/duplicate-esther.json').write_text(json.dumps(b,ensure_ascii=False,indent=2));continue
 kept.append(b)
 for c in b['chapters']:
  sections=c['sections'];preface=c['preface']
  if preface:
   initial=[s for s in sections if s['beforeVerse']==c['verses'][0]['verse']];sections=[s for s in sections if s not in initial]
   preface=[{'type':'heading' if 'beforeVerse' in x else 'paragraph','text':x['text']} for x in sorted(initial+preface,key=lambda x:x.get('sourceParagraph',x.get('sourceParagraphs',[0])[0]))]
  else:preface=[]
  out={'chapter':c['chapter'],'sections':[{k:s[k] for k in ['text','beforeVerse']} for s in sections],'preface':preface,'verses':[{k:v[k] for k in ['verse','text']} for v in c['verses']],'notes':[{**{k:n[k] for k in ['id','verseStart','verseEnd']},'blocks':[{'type':p['type'],'text':re.sub(r'\s+',' ',p['text']).strip()} for p in n['blocks']]} for n in c['notes']]}
  if c['chapter']==1:out['introduction']=[x['text'] for x in b['introduction']]
  (root/f'public/commentary/{b["number"]}-{c["chapter"]}.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')))
# Record availability without shipping commentary in the initial reader bundle.
manifest={'schemaVersion':'1.0','books':[]}
for bid in range(1,67):
 chapters=sorted(int(f.stem.split('-')[1]) for f in (root/'public/commentary').glob(f'{bid}-*.json'))
 manifest['books'].append({'book':bid,'chapters':chapters,'seeBooks':[11,12] if bid in [13,14] else []})
(root/'public/commentary/manifest.json').write_text(json.dumps(manifest,separators=(',',':')))
# Preserve source extraction and conversion scripts outside public website assets.
archive=root/'commentary-preparation/remaining-ot';archive.mkdir(parents=True,exist_ok=True)
for p in Path('remaining-ot').glob('*'):
 if p.suffix in ['.json','.py']:shutil.copy(p,archive/p.name)
shutil.copy('remaining-ot/conversion-report.json',root/'OT-conversion-report.json')
# Reuse the standalone review's UI with all supplied OT books.
parts=json.loads(Path('ot-commentary/pentateuch.json').read_text())['books']+kept
combined={}
for b in parts:
 if b['id'] in combined:combined[b['id']]['chapters']+=b['chapters']
 else:combined[b['id']]=b
for b in combined.values():b['chapters'].sort(key=lambda c:c['chapter'])
allbooks=sorted(combined.values(),key=lambda b:b['number'])
reviewpath=root/'Pentateuch-review.html' if (root/'Pentateuch-review.html').exists() else root/'OT-commentary-review.html'
template=reviewpath.read_text();template=re.sub(r'(<script id="dataset" type="application/json">).*?(</script>)',lambda m:m[1]+json.dumps({'books':allbooks},ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+m[2],template,flags=re.S)
template=template.replace('Pentateuch — Commentaar in Sranantongo','Oude Testament — Commentaar in Sranantongo').replace('5 boeken · 187 hoofdstukken','37 boeken · 864 hoofdstukken').replace('de vijf commentaardocumenten','de aangeleverde commentaardocumenten').replace('De bronnummering is behouden en komt overeen met de huidige SRN-bestanden op de website.','De bronnummering is behouden. Psalmopschriften kunnen ongenummerd zijn; genummerde verzen beginnen soms bij 2 of 3.').replace('Genesis · Exodus · Leviticus · Numeri · Deuteronomium.','1 en 2 Kronieken: zie Koningen. Psalmen 106–150 zijn nog niet beschikbaar.').replace('scripture(c.verses.length)','scripture(Math.max(...c.verses.map(v=>v.verse)))')
(root/'OT-commentary-review.html').write_text(template);(root/'Pentateuch-review.html').unlink(missing_ok=True)

p=root/'OT-commentary-review.html';s=p.read_text().replace('37 boeken · 819 hoofdstukken','37 boeken · 864 hoofdstukken').replace(' Psalmen 106–150 zijn nog niet beschikbaar.','');p.write_text(s)
