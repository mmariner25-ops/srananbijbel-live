# De Bijbel na ini Sranan Tongo — Next.js Reader

## Start on Mac

```bash
cd ~/Desktop/SRNBIBLEWEBSITE
npm install
npm run dev
```

Open http://localhost:3000. If another project is already running, stop it first with Control+C.

This is a genuine React/Next.js reader, not an iframe. The Bible JSON files are in `public/data` and are separate from the design in `app/reader.css`.

The original data still has outstanding validation flags. This package retains the data from the last Next.js reader and does not invent missing verses.

Navigator: click the current book/chapter or Navigeren button. Select book in side-by-side OT/NT columns, chapter, then optionally verse. Use Lees hoofdstuk to finish in two clicks.


Sidebar update: On desktop, click ‹ at the top right of the book list to collapse it. Click ☰ Bijbelboeken in the reading toolbar to reopen it. Mobile navigation remains unchanged.
