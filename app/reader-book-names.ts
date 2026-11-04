export const kjvBookNames = ['Genesis','Exodus','Leviticus','Numbers','Deuteronomy','Joshua','Judges','Ruth','1 Samuel','2 Samuel','1 Kings','2 Kings','1 Chronicles','2 Chronicles','Ezra','Nehemiah','Esther','Job','Psalms','Proverbs','Ecclesiastes','Song of Solomon','Isaiah','Jeremiah','Lamentations','Ezekiel','Daniel','Hosea','Joel','Amos','Obadiah','Jonah','Micah','Nahum','Habakkuk','Zephaniah','Haggai','Zechariah','Malachi','Matthew','Mark','Luke','John','Acts','Romans','1 Corinthians','2 Corinthians','Galatians','Ephesians','Philippians','Colossians','1 Thessalonians','2 Thessalonians','1 Timothy','2 Timothy','Titus','Philemon','Hebrews','James','1 Peter','2 Peter','1 John','2 John','3 John','Jude','Revelation'];

// Shared spellings fall back to the existing Sranantongo edition catalog.
export const svvBookNames: Record<number, string> = {
  9: '1 Samuël', 10: '2 Samuël', 11: '1 Koningen', 12: '2 Koningen',
  13: '1 Kronieken', 14: '2 Kronieken', 19: 'Psalmen', 26: 'Ezechiël',
  27: 'Daniël', 29: 'Joël', 40: 'Mattheüs', 44: 'Handelingen',
  45: 'Romeinen', 46: '1 Korinthe', 47: '2 Korinthe', 49: 'Efeze',
  50: 'Filippenzen', 51: 'Kolossenzen', 52: '1 Thessalonicenzen',
  53: '2 Thessalonicenzen', 54: '1 Timotheüs', 55: '2 Timotheüs',
  58: 'Hebreeën', 60: '1 Petrus', 61: '2 Petrus',
  62: '1 Johannes', 63: '2 Johannes', 64: '3 Johannes',
};
