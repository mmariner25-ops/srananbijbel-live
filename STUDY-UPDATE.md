# Old Testament commentary update

This complete project includes all supplied Old Testament commentary, all 150 Psalms, the existing Pentateuch, and the existing New Testament.

There are 37 OT commentary books, 864 OT chapters and 11,083 OT notes. Chronicles has no supplied commentary; both books display a note linking to 1 and 2 Kings. With the NT, there are 1,124 commentary chapters and 13,897 notes.

## Update and preview

1. Keep the `study-commentary` branch selected in GitHub Desktop.
2. Copy the contents of this project folder into the existing repository folder and replace matching files. Keep the repository folder itself.
3. Commit and push to the branch, then check its preview before merging into `main`.
4. Test `/study?book=6&chapter=1`, `/study?book=19&chapter=150`, `/study?book=39&chapter=4` and `/study?book=13&chapter=1`.

The shared navigator, themes, text size and remembered Bible-text toggle remain. Quotes come from the commentary source, so they stay paired with their notes. Bible translation files have not been changed. Chapter data loads only when opened.

`OT-commentary-review.html` is a standalone review copy for all 37 supplied OT books. Open it directly without running the website. Source extraction and conversion details are retained in `commentary-preparation/`, outside public website assets. The standalone Esther document is used; the Scripture-only Esther copy found after Nehemiah is retained separately.

## Validation and editorial limits

All supplied chapters and source verse sequences are checked. All commentary note ranges are within their source verses. All nonempty source paragraphs in the new uploads are accounted for, and source character inventories are preserved, ignoring whitespace and reconstructing verse labels. Four embedded verses and four inline notes were separated, 16 Scripture continuations and three commentary continuations were rejoined. A comma in the 1 Samuel 24:22 label is accepted as source numbering; the text is unchanged.

Some Psalm superscriptions are part of unnumbered opening text; source numbered verses can begin at 2 or 3. Source numbering is retained. The closing verse of 1 Samuel 24 is verse 23 in the commentary source, whereas the current website ends at verse 22. No silent mapping or Bible-text correction was applied.

Production build and data checks pass. Final phone layout and browser interactions should be reviewed in the branch preview. Nothing is published by this ZIP.
