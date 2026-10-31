from pathlib import Path
import json,re,html,zipfile,uuid,datetime,sys
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,PageBreak,Table,TableStyle,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT,TA_CENTER
ROOT=Path('/workspace/scratch/9479164905bd');OUT=ROOT/'commentary-downloads';SITE=ROOT/'work/srananbijbel-v02-main'
BOOKS=json.loads((SITE/'public/books.json').read_text())
for b in BOOKS:
 b['content']=[]
 for n in range(1,b['chapters']+1):
  f=SITE/f'public/commentary/{b["id"]}-{n}.json'
  if f.exists():b['content'].append(json.loads(f.read_text()))
 assert b['id'] in [13,14] or len(b['content'])==b['chapters'],b['name']
E=lambda t:html.escape(str(t),quote=True)
def plain(t):return re.sub(r'\s+',' ',t).strip()
def ref(b,c,n):return f'{b["name"]} {c["chapter"]}:{n["verseStart"]}'+(f'–{n["verseEnd"]}' if n['verseEnd']!=n['verseStart'] else '')
def chapter_items(c,include):
 through=0
 def scripture(end):
  nonlocal through
  verses=[v for v in c['verses'] if through<v['verse']<=end];batch=[]
  for v in verses:
   headings=[s for s in c['sections'] if s['beforeVerse']==v['verse']]
   if headings:
    if batch and include:yield ('scripture',batch)
    batch=[]
    for h in headings:yield ('heading',h['text'])
   batch.append(v)
  if batch and include:yield ('scripture',batch)
  through=max(through,end)
 for block in c.get('preface',[]):yield ('heading' if block['type']=='heading' else 'paragraph',block['text'])
 for n in c['notes']:
  yield ('reference',n);yield from scripture(n['verseEnd'])
  for block in n['blocks']:yield ('paragraph',(f'{block["number"]}. ' if block.get('type')=='listItem' and 'number' in block else '')+block['text'])
 last=max(v['verse'] for v in c['verses'])
 if include and through<last:
  yield ('reference',{'verseStart':through+1,'verseEnd':last,'id':f'text-{through+1}-{last}'})
 yield from scripture(last)
ABOUT=['Dit commentaar is geschreven in Sranantongo. Gebruik de inhoudsopgave om een Bijbelboek te kiezen en de hoofdstuknummers om verder te navigeren.','De oorspronkelijke bewoordingen van de aangeleverde commentaardocumenten zijn behouden. Bijbelcitaten volgen die documenten; de versnummering kan afwijken van andere Bijbeluitgaven.','Voor 1 en 2 Kronieken is geen afzonderlijk commentaar aangeleverd. Zie het commentaar op Samuël en Koningen.']
# EPUB 3, with an EPUB 2 NCX for older readers.
CSS='''body{font-family:serif;line-height:1.65;margin:5%;}h1,h2,h3{line-height:1.25;page-break-after:avoid;break-after:avoid}h1{font-size:2em;font-weight:normal;margin:1.5em 0 .5em}h2{font-size:1.5em;font-weight:normal;margin:1.6em 0 .7em}h3{font-size:1.12em;margin:1.6em 0 .6em}p{margin:.7em 0;orphans:3;widows:3}a{color:#2b6558}.eyebrow,.ref,.back,.caption{font-family:sans-serif}.eyebrow{font-size:.75em;letter-spacing:.14em;text-transform:uppercase;color:#52776d}.caption{font-size:.85em}.title{font-size:2.7em;margin-top:1em}.subtitle{font-size:1.35em}.cover{padding:7% 0;page-break-after:always}.cover .author{margin:2em 0}.edition{font-family:sans-serif;font-size:.9em}.booklist{list-style:none;padding:0;columns:2;column-gap:2em}.booklist li{break-inside:avoid;margin:.6em 0}.booklist a{text-decoration:none}.chapterlist{list-style:none;padding:0;line-height:2.9}.chapterlist li{display:inline}.chapterlist a{display:inline-block;text-align:center;min-width:2.5em;margin:.15em;border:1px solid #8aaba1;border-radius:.25em;text-decoration:none;padding:.05em .3em;font-family:sans-serif}.back{font-size:.82em;margin:1em 0 2em;line-height:2}.back a{display:inline-block;margin-right:1em}.ref{font-size:.8em;color:#52776d;font-weight:bold;margin:1.6em 0 .3em}.scripture{font-size:.94em;margin:1em 0 1em .2em;padding-left:1em;border-left:2px solid #8aaba1;line-height:1.6}.scripture sup{font-family:sans-serif;font-size:.7em}.section-note{font-size:.85em;font-family:sans-serif;margin:2em 0}.bottom{border-top:1px solid #8aaba1;margin-top:2em;padding-top:1em}@media(prefers-color-scheme:dark){a,.ref,.eyebrow{color:#9dccb9}}'''
def xhtml(title,body):return f'''<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="srn" lang="srn"><head><title>{E(title)}</title><meta charset="utf-8"/><link rel="stylesheet" type="text/css" href="style.css"/></head><body>{body}</body></html>'''
def bfile(b):return f'book-{b["id"]:02}.xhtml'
def cfile(b,c):return f'c-{b["id"]:02}-{c["chapter"]:03}.xhtml'
def make_epub(include):
 edition='Met Bijbeltekst' if include else 'Zonder Bijbeltekst';stem='Patton-commentaar-met-Bijbeltekst' if include else 'Patton-commentaar-zonder-Bijbeltekst';files={};spine=[];uid='urn:uuid:'+str(uuid.uuid4());title='Bijbelcommentaar in Sranantongo — '+edition
 body=f'<section class="cover"><p class="eyebrow">Oude en Nieuwe Testament</p><h1 class="title">Bijbelcommentaar</h1><p class="subtitle">Sranantongo</p><p class="author">ds. Robert D. Patton</p><p class="edition">{edition}</p><p><a href="index.xhtml">Kies een Bijbelboek →</a></p></section>'
 files['cover.xhtml']=xhtml(title,body);spine.append('cover.xhtml')
 index='<p class="eyebrow">Bijbelcommentaar · Sranantongo</p><h1>Inhoud</h1><p class="caption">'+edition+'</p>'
 for testament,subset in [('Oude Testament',BOOKS[:39]),('Nieuwe Testament',BOOKS[39:])]:
  index+=f'<h2>{testament}</h2><ol class="booklist">'+''.join(f'<li><a href="{bfile(b)}">{E(b["name"])}</a></li>' for b in subset)+'</ol>'
 index+='<h2>Over deze uitgave</h2>'+''.join('<p>'+E(t)+'</p>' for t in ABOUT)
 files['index.xhtml']=xhtml('Inhoud',index);spine.append('index.xhtml')
 navitems=[];ncxpoints=[];order=0
 for b in BOOKS:
  bid=b['id'];landing=f'<nav class="back"><a href="index.xhtml">← Alle boeken</a></nav><p class="eyebrow">'+('Oude Testament' if bid<=39 else 'Nieuwe Testament')+f'</p><h1>{E(b["name"])}</h1>'
  if b['content']:
   landing+='<h2 id="chapters">Kies een hoofdstuk</h2><ol class="chapterlist">'+''.join(f'<li><a href="{cfile(b,c)}">{c["chapter"]}</a></li>' for c in b['content'])+'</ol>'
   if b['content'][0].get('introduction'):
    landing+='<h2>Inleiding</h2>'+''.join('<p>'+E(plain(t))+'</p>' for t in b['content'][0]['introduction'])
   landing+=f'<p><a href="{cfile(b,b["content"][0])}">Begin met lezen →</a></p>'
  else:landing+='<p>Voor dit boek is geen afzonderlijk commentaar beschikbaar. Zie het commentaar op Koningen.</p><p><a href="book-11.xhtml">1 Koningen</a> · <a href="book-12.xhtml">2 Koningen</a></p>'
  files[bfile(b)]=xhtml(b['name'],landing);spine.append(bfile(b));children=[];ncxchildren=[];order+=1;parentorder=order
  for j,c in enumerate(b['content']):
   cnum=c['chapter'];name=f'{b["name"]} {cnum}';nav=f'<nav class="back"><a href="index.xhtml">Boeken</a><a href="{bfile(b)}#chapters">Hoofdstukken</a>'
   if j>0:nav+=f'<a href="{cfile(b,b["content"][j-1])}">← Vorige</a>'
   if j+1<len(b['content']):nav+=f'<a href="{cfile(b,b["content"][j+1])}">Volgende →</a>'
   nav+='</nav>';body=nav+f'<h1>{E(name)}</h1>'
   for kind,value in chapter_items(c,include):
    if kind=='heading':body+='<h2>'+E(plain(value))+'</h2>'
    elif kind=='reference':body+=f'<p class="ref" id="note-{E(value["id"])}">{E(ref(b,c,value))}</p>'
    elif kind=='scripture':body+='<div class="scripture"><p>'+''.join(f'<span id="v{v["verse"]}"><sup>{v["verse"]}</sup> {E(plain(v["text"]))} </span>' for v in value)+'</p></div>'
    else:body+='<p>'+E(plain(value))+'</p>'
   body+='<div class="bottom">'+nav+'</div>';fn=cfile(b,c);files[fn]=xhtml(name,body);spine.append(fn);children.append(f'<li><a href="{fn}">Hoofdstuk {cnum}</a></li>');order+=1;ncxchildren.append(f'<navPoint id="n-{bid}-{cnum}" playOrder="{order}"><navLabel><text>Hoofdstuk {cnum}</text></navLabel><content src="{fn}"/></navPoint>')
  navitems.append(f'<li><a href="{bfile(b)}">{E(b["name"])}</a>'+('<ol>'+''.join(children)+'</ol>' if children else '')+'</li>');ncxpoints.append(f'<navPoint id="b-{bid}" playOrder="{parentorder}"><navLabel><text>{E(b["name"])}</text></navLabel><content src="{bfile(b)}"/>'+''.join(ncxchildren)+'</navPoint>')
 files['nav.xhtml']=xhtml('Inhoud','<nav epub:type="toc" id="toc"><h1>Inhoud</h1><ol>'+''.join(navitems)+'</ol></nav><nav epub:type="landmarks" hidden="hidden"><ol><li><a epub:type="cover" href="cover.xhtml">Titelpagina</a></li><li><a epub:type="toc" href="index.xhtml">Boeken</a></li><li><a epub:type="bodymatter" href="book-01.xhtml">Commentaar</a></li></ol></nav>')
 files['toc.ncx']=f'''<?xml version="1.0" encoding="utf-8"?><ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head><meta name="dtb:uid" content="{uid}"/><meta name="dtb:depth" content="2"/><meta name="dtb:totalPageCount" content="0"/><meta name="dtb:maxPageNumber" content="0"/></head><docTitle><text>{E(title)}</text></docTitle><navMap>{''.join(ncxpoints)}</navMap></ncx>'''
 manifest='<item id="css" href="style.css" media-type="text/css"/><item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>'
 ids={fn:f'i{i}' for i,fn in enumerate(files) if fn.endswith('.xhtml')}
 for fn,id in ids.items():manifest+=f'<item id="{id}" href="{fn}" media-type="application/xhtml+xml"'+(' properties="nav"' if fn=='nav.xhtml' else '')+'/>'
 opf=f'''<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="srn"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="uid">{uid}</dc:identifier><dc:title>{E(title)}</dc:title><dc:creator>ds. Robert D. Patton</dc:creator><dc:language>srn</dc:language><meta property="dcterms:modified">2026-10-31T00:00:00Z</meta></metadata><manifest>{manifest}</manifest><spine toc="ncx">{''.join(f'<itemref idref="{ids[f]}"/>' for f in spine)}</spine></package>'''
 with zipfile.ZipFile(OUT/(stem+'.epub'),'w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('mimetype','application/epub+zip',compress_type=zipfile.ZIP_STORED);z.writestr('META-INF/container.xml','''<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>''');z.writestr('OEBPS/content.opf',opf);z.writestr('OEBPS/style.css',CSS)
  for fn,body in files.items():z.writestr('OEBPS/'+fn,body)
 print('EPUB',stem,flush=True)
# PDF reading editions, with book/chapter destination links and outline bookmarks.
GREEN=colors.HexColor('#285e51');INK=colors.HexColor('#24312d');MUTED=colors.HexColor('#60736b');LINE=colors.HexColor('#d5dfd9')
FONT='/usr/share/fonts/truetype/dejavu/'
for name,fn in [('Serif','DejaVuSerif.ttf'),('SerifBold','DejaVuSerif-Bold.ttf'),('Sans','DejaVuSans.ttf'),('SansBold','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,FONT+fn))
pdfmetrics.registerFontFamily('Serif',normal='Serif',bold='SerifBold',italic='Serif',boldItalic='SerifBold');pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='SansBold',italic='Sans',boldItalic='SansBold')
ST={
 'body':ParagraphStyle('body',fontName='Serif',fontSize=10.5,leading=15.4,textColor=INK,spaceAfter=7,splitLongWords=True,allowWidows=0,allowOrphans=0),
 'scripture':ParagraphStyle('scripture',fontName='Serif',fontSize=10,leading=14.7,textColor=GREEN,leftIndent=14,borderColor=LINE,borderWidth=.5,borderPadding=9,spaceBefore=9,spaceAfter=12,allowWidows=0,allowOrphans=0),
 'section':ParagraphStyle('section',fontName='SansBold',fontSize=11,leading=16,textColor=INK,spaceBefore=14,spaceAfter=8,keepWithNext=True),
 'reference':ParagraphStyle('reference',fontName='SansBold',fontSize=8,leading=11.5,textColor=GREEN,spaceBefore=10,spaceAfter=5,keepWithNext=True),
 'chapter':ParagraphStyle('chapter',fontName='Serif',fontSize=22,leading=28,textColor=INK,spaceBefore=22,spaceAfter=14,keepWithNext=True),
 'book':ParagraphStyle('book',fontName='Serif',fontSize=34,leading=42,textColor=GREEN,spaceAfter=18,keepWithNext=True),
 'small':ParagraphStyle('small',fontName='Sans',fontSize=8.5,leading=13,textColor=MUTED,spaceAfter=10),
 'toc':ParagraphStyle('toc',fontName='Sans',fontSize=10,leading=15,textColor=GREEN,spaceAfter=6),
 'grid':ParagraphStyle('grid',fontName='Sans',fontSize=10,leading=17,alignment=TA_CENTER,textColor=GREEN),
 'title':ParagraphStyle('title',fontName='Serif',fontSize=42,leading=50,textColor=GREEN,spaceAfter=18),
 'subtitle':ParagraphStyle('subtitle',fontName='Serif',fontSize=23,leading=32,textColor=INK,spaceAfter=20)
}
class PDFDoc(BaseDocTemplate):
 def __init__(self,path,edition):
  super().__init__(str(path),pagesize=(612,792),leftMargin=54,rightMargin=54,topMargin=58,bottomMargin=53,title='Bijbelcommentaar in Sranantongo — '+edition,author='ds. Robert D. Patton',pageCompression=1)
  self.currentBook=0;self.currentTitle='Bijbelcommentaar';self.chapterIndex='contents';self.addPageTemplates(PageTemplate(id='normal',frames=[Frame(54,53,504,681,id='main',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPageEnd=self.decorate));self.audit=[]
 def afterFlowable(self,flow):
  if not hasattr(flow,'dest'):return
  dest,title,level=flow.dest;self.canv.bookmarkPage(dest);self.canv.addOutlineEntry(title,dest,level=level,closed=(level==0));self.audit.append({'destination':dest,'title':title,'page':self.page})
  if dest.startswith('book-'):self.currentBook=int(dest.split('-')[1]);self.chapterIndex=dest;self.currentTitle=title
  elif dest.startswith('chapter-'):self.currentTitle=title
 def decorate(self,canvas,doc):
  if self.page==1:return
  canvas.saveState();canvas.setFillColor(MUTED);canvas.setFont('Sans',8);canvas.drawString(54,761,self.currentTitle);canvas.drawRightString(558,761,'Bijbelcommentaar · Sranantongo');canvas.setStrokeColor(LINE);canvas.setLineWidth(.4);canvas.line(54,750,558,750);canvas.drawString(54,29,'Inhoud');canvas.linkRect('', 'contents',(54,23,94,39),relative=0,thickness=0)
  if self.currentBook:canvas.drawString(111,29,'Hoofdstukken');canvas.linkRect('',self.chapterIndex,(111,23,180,39),relative=0,thickness=0)
  canvas.drawRightString(558,29,str(self.page));canvas.restoreState()
def para(text,style='body'):return Paragraph(escape(plain(text)),ST[style])
def heading(text,style,dest=None,level=0):
 p=para(text,style)
 if dest:p.dest=(dest,text,level)
 return p
def link(text,dest):return f'<link href="#{dest}" color="#285e51">{escape(text)}</link>'
def make_pdf(include):
 edition='Met Bijbeltekst' if include else 'Zonder Bijbeltekst';stem='Patton-commentaar-met-Bijbeltekst' if include else 'Patton-commentaar-zonder-Bijbeltekst';story=[Spacer(1,105),para('OUDE EN NIEUWE TESTAMENT','small'),para('Bijbelcommentaar','title'),para('Sranantongo','subtitle'),Spacer(1,14),para('ds. Robert D. Patton','body'),Spacer(1,28),para(edition,'section'),Paragraph(link('Open de inhoudsopgave →','contents'),ST['toc']),Spacer(1,90),para('De Bijbel na ini Sranantongo','small'),PageBreak()]
 story.append(heading('Inhoud','book','contents'))
 for title,subset in [('Oude Testament',BOOKS[:39]),('Nieuwe Testament',BOOKS[39:])]:
  story.append(heading(title,'section'));rows=[]
  for j in range(0,len(subset),3):rows.append([Paragraph(link(b['name'],f'book-{b["id"]}'),ST['toc']) for b in subset[j:j+3]]+['']*(3-len(subset[j:j+3])))
  table=Table(rows,colWidths=[168]*3,hAlign='LEFT');table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.append(table)
 story.extend([Spacer(1,18),heading('Over deze uitgave','section')]+[para(t,'small') for t in ABOUT])
 for b in BOOKS:
  bid=b['id'];story.extend([PageBreak(),para('OUDE TESTAMENT' if bid<=39 else 'NIEUWE TESTAMENT','small'),heading(b['name'],'book',f'book-{bid}')])
  if not b['content']:
   story.extend([para('Voor dit boek is geen afzonderlijk commentaar beschikbaar. Zie het commentaar op Koningen.'),Paragraph(link('1 Koningen','book-11')+' · '+link('2 Koningen','book-12'),ST['toc'])]);continue
  cells=[Paragraph(link(str(c['chapter']),f'chapter-{bid}-{c["chapter"]}'),ST['grid']) for c in b['content']];rows=[cells[j:j+12]+['']*(12-len(cells[j:j+12])) for j in range(0,len(cells),12)];table=Table(rows,colWidths=[42]*12,hAlign='LEFT');table.setStyle(TableStyle([('BOX',(0,0),(-1,-1),.4,LINE),('INNERGRID',(0,0),(-1,-1),.3,LINE),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]));story.append(table)
  intro=b['content'][0].get('introduction',[])
  if intro:story.append(heading('Inleiding','section'));story.extend(para(t) for t in intro)
  for c in b['content']:
   story.append(heading(f'{b["name"]} {c["chapter"]}','chapter',f'chapter-{bid}-{c["chapter"]}',1))
   for kind,value in chapter_items(c,include):
    if kind=='heading':story.append(para(value,'section'))
    elif kind=='reference':story.append(para(ref(b,c,value),'reference'))
    elif kind=='scripture':story.append(Paragraph(' '.join(f'<super><font name="Sans" size="7">{v["verse"]}</font></super> {escape(plain(v["text"]))}' for v in value),ST['scripture']))
    else:story.append(para(value))
 doc=PDFDoc(OUT/(stem+'.pdf'),edition);doc.build(story);(OUT/'qa'/f'{stem}-destinations.json').write_text(json.dumps(doc.audit,ensure_ascii=False));print('PDF',stem,'pages',doc.page,flush=True)
if __name__=='__main__':
 for inc in [True,False]:make_epub(inc)
 for inc in [True,False]:make_pdf(inc)
