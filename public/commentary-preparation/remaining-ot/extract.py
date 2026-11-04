from pathlib import Path
from docx import Document
import json,re
for f in Path('remaining-ot/converted').glob('*.docx'):
 d=Document(f);out=[]
 for i,p in enumerate(d.paragraphs):
  out.append({'index':i,'text':p.text,'style':p.style.name if p.style else '', 'runs':[{'text':r.text,'bold':bool(r.bold),'italic':bool(r.italic)} for r in p.runs]})
 Path(f'remaining-ot/{f.stem}-paragraphs.json').write_text(json.dumps(out,ensure_ascii=False))
 print(f.stem,len(out),'tables',len(d.tables))
 print('FIRST',[(x['index'],x['text'][:90]) for x in out if x['text'].strip()][:5])
 print('HEADINGS',[(x['index'],x['text'].strip()) for x in out if re.fullmatch(r'[^\d.]{2,40}\s+1',x['text'].strip())])
