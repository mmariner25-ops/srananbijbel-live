"use client";
import {useEffect,useState} from 'react';
type Note={id:string,verseStart:number,verseEnd:number,blocks:{type:string,text:string,number?:number}[]};
type Content={verses:{verse:number,text:string}[],sections:{text:string,beforeVerse:number}[],notes:Note[]};
export default function StudyContent({book,chapter,lang,pendingVerse,onVerseReached}:{book:number,chapter:number,lang:'nl'|'en',pendingVerse:number|null,onVerseReached:()=>void}){
 const [content,setContent]=useState<Content|null>(null),[loading,setLoading]=useState(true),[failed,setFailed]=useState(false),[showBible,setShowBible]=useState(true);
 useEffect(()=>{try{setShowBible(localStorage.getItem('patton-show-bible')!=='false')}catch{}},[]);
 useEffect(()=>{let cancelled=false;setLoading(true);setContent(null);setFailed(false);if(book<40){setLoading(false);return}fetch(`/commentary/${book}-${chapter}.json`).then(r=>{if(!r.ok)throw Error();return r.json()}).then(d=>{if(!cancelled)setContent(d)}).catch(()=>{if(!cancelled)setFailed(true)}).finally(()=>{if(!cancelled)setLoading(false)});return()=>{cancelled=true}},[book,chapter]);
 useEffect(()=>{if(!content||pendingVerse===null)return;const note=content.notes.find(n=>n.verseStart<=pendingVerse&&n.verseEnd>=pendingVerse);const el=document.getElementById(note?.id||`study-verse-${pendingVerse}`);el?.scrollIntoView({behavior:'smooth',block:'center'});onVerseReached()},[content,pendingVerse,onVerseReached]);
 const toggle=(value:boolean)=>{setShowBible(value);try{localStorage.setItem('patton-show-bible',String(value))}catch{}};
 if(book<40)return <div className="study-empty"><p>{lang==='nl'?'Het commentaar is beschikbaar voor het Nieuwe Testament. Kies een boek via Navigeren.':'Commentary is available for the New Testament. Choose a book using Navigate.'}</p></div>;
 if(loading)return <p className="loading">{lang==='nl'?'Commentaar laden…':'Loading commentary…'}</p>;
 if(failed||!content)return <p role="alert">{lang==='nl'?'Het commentaar kan niet worden geladen. Probeer de pagina opnieuw te laden.':'Could not load commentary. Try reloading the page.'}</p>;
 // Each Scripture verse appears once, before the note following its passage.
 let through=0;
 const scripture=(end:number)=>{const start=through;through=Math.max(through,end);return <>{content.sections.filter(s=>s.beforeVerse>start&&s.beforeVerse<=end).map((s,i)=><h2 className="study-section" key={i}>{s.text}</h2>)}{showBible&&<blockquote className="study-scripture">{content.verses.filter(v=>v.verse>start&&v.verse<=end).map(v=><span key={v.verse} id={`study-verse-${v.verse}`}><sup>{v.verse}</sup> {v.text}{' '}</span>)}</blockquote>}</>};
 return <div className="study-content"><label className="study-toggle"><input type="checkbox" checked={showBible} onChange={e=>toggle(e.target.checked)}/>{lang==='nl'?'Bijbeltekst tonen':'Show Bible text'}</label><p className="study-source">{lang==='nl'?'Bijbelcitaten uit het commentaardocument.':'Scripture quotations from the commentary document.'}</p>{content.notes.map(note=><section className="study-note" id={note.id} key={note.id}>{scripture(note.verseEnd)}<div className="study-reference">{lang==='nl'?'Vers':'Verse'} {note.verseStart}{note.verseEnd!==note.verseStart?`–${note.verseEnd}`:''}</div>{note.blocks.map((block,i)=><p key={i}>{block.type==='listItem'&&block.number!==undefined?`${block.number}. `:''}{block.text}</p>)}</section>)}{through<Math.max(...content.verses.map(v=>v.verse))&&scripture(Math.max(...content.verses.map(v=>v.verse)))}</div>
}
