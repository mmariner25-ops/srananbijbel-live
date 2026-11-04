import numbering from './cross-reference-numbering.json';
import {useEffect, useRef, useState} from 'react';

export function hasCompatibleNumbering(translation: string, chapterKey: string) {
  return !(numbering as Record<string, string[]>)[translation]?.includes(chapterKey);
}

export type VerseAddress = [book: number, chapter: number, verse: number];
export type ReferenceIndex = Record<number, VerseAddress[][]>;
type Props = {
  title: string;
  references: VerseAddress[][];
  translation: string;
  lang: 'nl' | 'en';
  bookName: (book: number) => string;
  onJump: (address: VerseAddress) => void;
  onClose: () => void;
};

export default function CrossReferences({title, references, translation, lang, bookName, onJump, onClose}: Props) {
  const dialog = useRef<HTMLDialogElement>(null);
  const [active, setActive] = useState<VerseAddress[]>();
  const canOpen = active?.every(([book, chapter]) => hasCompatibleNumbering(translation, `${book}-${chapter}`));
  const [preview, setPreview] = useState<string>();
  const nl = lang === 'nl';
  const label = nl ? 'Kruisverwijzingen' : 'Cross-references';

  useEffect(() => { dialog.current?.showModal(); }, []);
  useEffect(() => {
    if (!active || !canOpen) return;
    const controller = new AbortController();
    const chapters = new Map<string, Promise<{verse: number; text: string}[]>>();
    async function read([book, chapter, verse]: VerseAddress) {
      const key = `${book}-${chapter}`;
      if (!chapters.has(key)) {
        chapters.set(key, fetch(`/data/${translation}/${key}.json`, {signal: controller.signal})
          .then(async response => response.ok ? (await response.json()).verses : []));
      }
      return (await chapters.get(key))?.find(item => item.verse === verse)?.text;
    }
    Promise.all(active.map(read)).then(texts => {
      if (!controller.signal.aborted) setPreview(texts.filter(Boolean).join(' '));
    }).catch(() => {
      if (!controller.signal.aborted) setPreview('');
    });
    return () => controller.abort();
  }, [active, canOpen, translation]);

  return <dialog ref={dialog} className="navigator xref-dialog" aria-label={label} onCancel={onClose}>
    <div className="navigator-header">
      <div><span className="eyebrow">{label}</span><h2>{title}</h2></div>
      <button className="nav-close" onClick={onClose} aria-label={nl ? 'Sluiten' : 'Close'}>×</button>
    </div>
    <div className="xref-list">
      {references.map(passage => {
        const name = passage.map(([book, chapter, verse], index) => {
          const previous = passage[index - 1];
          return previous?.[0] === book && previous[1] === chapter
            ? String(verse) : `${bookName(book)} ${chapter}:${verse}`;
        }).join(', ');
        return <div key={JSON.stringify(passage)} className="xref-item">
          <button aria-expanded={active === passage} onClick={() => {
            setPreview(undefined);
            setActive(active === passage ? undefined : passage);
          }}>{name}</button>
          {active === passage && <div aria-live="polite">
            <p>{!canOpen ? (nl ? 'De versnummering verschilt in deze vertaling.' : 'Verse numbering differs in this translation.') : preview === undefined ? '…' : preview || (nl ? 'Tekst niet beschikbaar.' : 'Text unavailable.')}</p>
            {canOpen && preview && <button onClick={() => onJump(passage[0])}>{nl ? 'Lees in de Bijbel' : 'Read in the Bible'} →</button>}
          </div>}
        </div>;
      })}
      <p className="xref-credit">
        <a href="https://crossreferences.org/project/data/">CrossReferences.org</a> · <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>
        <br/>{nl ? 'Gebaseerd op de Treasury of Scripture Knowledge, gegroepeerd per vers.' : 'Based on the Treasury of Scripture Knowledge, grouped by verse.'}
      </p>
    </div>
  </dialog>;
}
