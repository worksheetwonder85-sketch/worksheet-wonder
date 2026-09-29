# 📁 "My First Alphabet Workbook" File Structure & Asset Taxonomy

This document specifies the complete directory hierarchy, file naming standards, and asset compilation pipeline for **"My First Alphabet Workbook"**.

---

## 1. Directory Tree Architecture

```
Workbook/
├── Cover/
│   ├── front_cover.html               (Full-color printable A4 Front Cover)
│   ├── back_cover.html                (Product overview & store QR Back Cover)
│   ├── copyright_page.html            (P02 Imprint & legal credits)
│   └── about_workbook.html            (P03 Brand mission & pedagogy overview)
│
├── Letters/
│   ├── letter-a-worksheet.html        (P09 Letter A Printable Worksheet)
│   ├── letter-b-worksheet.html        (P10 Letter B Printable Worksheet)
│   ├── ...                            (Letters C through Y)
│   └── letter-z-worksheet.html        (P34 Letter Z Printable Worksheet)
│
├── Answer Keys/
│   ├── letter-a-answer-key.html       (P44 Letter A Teacher/Parent Key)
│   ├── letter-b-answer-key.html       (P45 Letter B Teacher/Parent Key)
│   ├── ...                            (Answer Keys C through Y)
│   └── letter-z-answer-key.html       (P63 Letter Z Teacher/Parent Key)
│
├── Teacher Guide/
│   ├── teacher-guide.html             (P06 Complete 20-min lesson plans & rubrics)
│   └── curriculum_alignment.html     (EYFS, CCSS & ACARA mapping specs)
│
├── Parent Guide/
│   ├── parent-guide.html              (P05 Home practice tips & 7-day schedule)
│   └── learning_outcomes.html         (P07 Milestone targets & progress chart)
│
├── Certificate/
│   └── completion_certificate.html   (P43 Full-page printable graduation award)
│
├── Preview/
│   ├── workbook_preview_sheet.html    (Multi-page bundle preview grid)
│   └── thumbnails/                    (High-res PNG thumbnail package)
│
├── PDF/
│   ├── My_First_Alphabet_Workbook.pdf (Compiled 64-page full commercial PDF)
│   └── Answer_Keys_Bundle.pdf         (Standalone 20-page teacher key PDF)
│
└── Assets/
    ├── css/
    │   ├── style.css                  (Design system CSS tokens & page layout)
    │   └── print.css                  (CSS @media print rules & page bounds)
    ├── js/
    │   ├── workbook-engine.js         (Dynamic page generation & interactive preview)
    │   └── print-helper.js            (Print dialog trigger & scale helper)
    └── svg/
        ├── alphabet/                  (78 vocabulary vector SVG files: A–Z)
        ├── ui/                        (Activity icons, badges, borders, stars)
        └── characters/                (Worksheet Wonder mascots & reward graphics)
```

---

## 2. File Naming Conventions
- **Worksheet Files**: `letter-[a-z]-worksheet.html` (Strict lowercase hyphens).
- **Answer Keys**: `letter-[a-z]-answer-key.html`.
- **SVG Assets**: `[vocabulary_word].svg` (e.g. `apple.svg`, `bear.svg`, `cat.svg`).
- **CSS / JS Assets**: Lowercase hyphenated (e.g. `workbook-engine.js`).

---

## 3. Production Manifest Integration
All files within this directory structure map directly to `database/data/worksheets.json` and `database/data/products.json` for web platform distribution and CMS management.
