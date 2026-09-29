# 📋 "My First Alphabet Workbook" Quality Assurance Checklist

This checklist establishes the mandatory Quality Assurance (QA) gates that every page in **"My First Alphabet Workbook"** must pass prior to master release compilation.

---

## 1. Structural & Template Compliance Gate
- [ ] **8-Panel Matrix Enforced**: All 8 activity panels present, correctly numbered, and titled.
- [ ] **Header Compliance**: Brand logo, Grade badge, Age badge, Free/Premium badge correctly rendered.
- [ ] **User Information Bar**: Name, Date, Teacher fields present with baseline rules.
- [ ] **Footer Compliance**: Website URL, Page Title, Page Number, and Star Rating present.
- [ ] **No Page Spillover**: Page content fits 100% within single A4 portrait page bound (`297mm`).

---

## 2. Visual Design & Typography Gate
- [ ] **Font Hierarchy**: Headers use `'Fredoka'` bold; instructions use `'Nunito'` italic.
- [ ] **Font Point Scale**: Main title 20pt, panel titles 10pt, instructions 7.5pt, display letter 62pt, tracing letters 32pt.
- [ ] **Color Contrast**: Background `#FFFDF9`, text `#2C3E50`; contrast ratio exceeds WCAG AAA (`7:1`).
- [ ] **Dual Border System**: Outer solid border `0.8mm` (`#2C3E50`), Inner dashed border `0.35mm`.
- [ ] **Box Shadows**: All activity cards use 3px solid `#2C3E50` hard offset shadow.

---

## 3. Vector SVG & Illustration Gate
- [ ] **Inline Vector Compliance**: 100% inline SVG; zero external bitmap image links or base64 raster data.
- [ ] **Stroke Weight Standards**: Main outline strokes `1.5px` to `2.5px`; internal strokes `1.0px`.
- [ ] **ViewBox Scalability**: SVG viewBox defined and responsive (`viewBox="0 0 80 65"` or `60 45`).
- [ ] **Visual Clarity**: Illustrations clean, friendly, and instantly recognizable for 4–6 year olds.

---

## 4. Educational & Content Accuracy Gate
- [ ] **Spelling & Vocabulary**: All 3 vocabulary words 100% phonetically accurate and correctly spelled.
- [ ] **Letter Stroke Guidance**: Tracing letters include starting dots (●) and directional arrows (→).
- [ ] **Stroke Height Realism**: Midline dashed rule positioned at exactly 50% height for handwriting lines.
- [ ] **Beginning Sounds Logic**: Exactly 3 correct matches + 3 distinct distractors in Panel 5.
- [ ] **Search Matrix Logic**: Exactly 5 target letters hidden within 5×5 cell grid in Panel 6.

---

## 5. Print & PDF Export Gate
- [ ] **@media print Verification**: Print preview shows zero hidden elements, buttons, or page overflows.
- [ ] **Color Adjustment**: `-webkit-print-color-adjust: exact` enabled in CSS.
- [ ] **Monochrome Laser Compatibility**: Borders and text remain 100% legible when printed in grayscale.
- [ ] **PDF Compilation**: 64-page master PDF compiles with correct page order, bookmarks, and metadata.

---

## 6. Answer Key Matching Gate
- [ ] **1:1 Alignment**: Answer Key sheet matches corresponding worksheet panel-by-panel.
- [ ] **Red Banner Display**: Mandatory `#C62828` answer key top banner present.
- [ ] **Visual Highlighting**: Correct cells circled in red/green; checkmark badges (`✓`) overlayed.
- [ ] **Scoring Summary**: Summary score box present in reward panel.

---

### QA Sign-Off Rationale
Every page must receive **100% pass ticks** across all 6 gates before being marked for commercial release.
