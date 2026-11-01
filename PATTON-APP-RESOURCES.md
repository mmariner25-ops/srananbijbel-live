# Optional app commentary resources

This folder was generated from the current website's `public/commentary/{book}-{chapter}.json` data. Existing website files and reader code are unchanged.

Public manifest URL: `https://srananbijbel.org/resources/patton/v1/manifest.json`

Each manifest entry identifies a gzip-compressed JSON book at `/resources/patton/v1/books/{book}.json.gz`, with a SHA-256 checksum and compressed size. After decompressing, JSON has shape `{"book": 1, "chapters": {"1": <existing chapter JSON>, ...}}`. The app must implement this format; this website update does not implement app downloading.

For future commentary corrections, regenerate the book packages and manifest together; preserve `/v1/` until an incompatible schema change, then use `/v2/`. Apps should compare hashes and refresh cached files when changed.

The existing `/commentary/` URLs continue to serve the website. This package does not change the STUDIE reader, downloads, or Bible data.
