# Study page update

The Bible reader is at `/`; the new commentary page is at `/study`.
Both use the same reader and book/chapter/verse navigator. Navigation links keep the current book and chapter. Language, theme and text size persist between pages. The Bible-text toggle remembers its setting.

The Study page includes Patton's 27 New Testament books, 260 chapters and 2,814 notes. It uses the first occurrence of 2 John from the supplied commentary document. Scripture quotations come from that same document so that its verse numbering matches its commentary. These are shown or hidden with “Bijbeltekst tonen.” The Bible reader's translation data is unchanged.

## Update your repository

1. Extract this ZIP.
2. Copy `app/Reader.tsx`, `app/StudyContent.tsx`, `app/page.tsx`, `app/reader.css`, the `app/study/` folder and the `public/commentary/` folder into your existing repository, replacing matching files.
3. Commit and push the changes to GitHub. Your existing hosting provider can then build the update as usual.
4. Open `/study?book=40&chapter=1`. Check navigation, the Bible-text toggle, phone layout and dark mode before announcing it.

There are no new package dependencies. This update does not implement offline commentary downloads in the separate app.

## Text comparison

The current website SRN agrees with the commentary's endings of 2 Corinthians 13 (13 verses) and 3 John (15 verses). Three chapter differences were found: Luke 9 is missing verse 24 in the website data; 1 Peter 3 is missing verse 7; John 1 has 52 verses in the website and 51 in the commentary document. No Bible text has been silently corrected. Study uses its source quotations throughout, rather than mixing numbering systems.
