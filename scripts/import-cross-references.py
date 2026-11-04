"""Import CrossReferences.org's KJV verse coordinates from the release ZIP."""
import json
import sys
import re
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile

public = Path(__file__).resolve().parents[1] / 'public'
output = public / 'cross-references'
with ZipFile(sys.argv[1]) as archive:
    def read(name):
        path = next(path for path in archive.namelist() if path.endswith('/json/' + name + '.json'))
        return json.loads(archive.read(path))

    coordinates = {
        row['id']: (row['book_id'], row['kjv_ch'], row['kjv_vs'])
        for row in read('bible_verses') if row.get('kjv_vs') and row.get('kjv_ch')
    }
    chapters = defaultdict(lambda: defaultdict(dict))
    for row in read('cross_references'):
        source = coordinates.get(row['verse_id'])
        if source is None:
            continue
        book, chapter, verse = source
        for passage in row['refs']:
            target = tuple(coordinates[identifier] for identifier in passage if identifier in coordinates)
            if target:
                chapters[book, chapter][verse][target] = None

output.mkdir(exist_ok=True)
for (book, chapter), verses in sorted(chapters.items()):
    (output / f'{book}-{chapter}.json').write_text(
        json.dumps({verse: list(targets) for verse, targets in verses.items()}, separators=(',', ':')) + '\n'
    )
print(f'{len(chapters)} chapters, {sum(len(verses) for verses in chapters.values())} source verses')

def verse_numbers(path):
    return {row['verse'] for row in json.loads(path.read_text())['verses']} if path.exists() else set()


# An unequal set of verse numbers needs a translation-specific mapping before use.
unsafe = {}
for translation in ('srn', 'svv'):
    unsafe[translation] = [
        path.stem for path in sorted((public / 'data' / 'kjv').glob('*.json'))
        if re.fullmatch(r'\d+-\d+', path.stem)
        and verse_numbers(path) != verse_numbers(public / 'data' / translation / path.name)
    ]
(Path(__file__).resolve().parents[1] / 'app' / 'cross-reference-numbering.json').write_text(
    json.dumps(unsafe, separators=(',', ':')) + '\n'
)
