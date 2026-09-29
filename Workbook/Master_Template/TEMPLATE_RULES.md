# Worksheet Wonder – Master Template Rules

> **STRICT COMPLIANCE DIRECTIVE**
> This specification document governs all automated and manual alphabet worksheet generation across the Worksheet Wonder publishing pipeline.

---

## 🚫 IMMUTABLE TEMPLATE RULES (NEVER CHANGE)

When producing letter worksheets (A through Z), AI agents, software scripts, and graphic designers **MUST NEVER** alter or modify any of the following core structural elements:

1. **Page Size & Geometry**
   - Must remain strictly **A4 Portrait** (`210mm × 297mm`).

2. **Margins & Padding**
   - Page container padding: `10mm` (top), `14mm` (sides), `8mm` (bottom).

3. **Typography & Font System**
   - Headings: `Baloo 2` (cursive, weights 600, 700, 800).
   - Body & Instructions: `Quicksand` (weights 500, 600, 700).

4. **Colour Palette Tokens**
   - CSS variables structure must be strictly preserved (`--theme-color-primary`, `--theme-color-secondary`, `--theme-color-light`, `--theme-color-border`).

5. **Spacing & Grid Layout**
   - Card padding (`3mm 4mm`), section gaps (`3mm`), and component flex layouts are locked.

6. **Tracing & Handwriting Line Spacing**
   - Tracing row height: `16mm`.
   - Independent handwriting row height: `14mm`.
   - Baseline stroke: `2.2px solid`.
   - Midline dashed stroke: `1.5px dashed` at `5.5mm` offset.

7. **Illustration Container Sizes**
   - SVG illustration cards: `72px × 72px` or `78px × 72px` bounding box.

8. **Header Structure**
   - Pencil logo icon, brand name, grade tag badge, and age tag badge positions are immutable.

9. **Footer Structure**
   - Encouragement star badge, copyright year, and document code format (`WW-KG-LTR-{LETTER}-01`) are locked.

10. **Activity Sequence & Order**
    - Section 1: Words That Start With {LETTER} (Illustrations)
    - Section 2: {LETTER} is for... (Vocabulary Bar)
    - Section 3: Tracing Practice (1 Demo Row + 4 Tracing Rows + 1 Independent Row)
    - Section 4: Writing Practice (2 Tracing Rows)
    - Section 5: Handwriting (3 Blank Ruled Lines)

11. **CSS Files & Architecture**
    - `master_variables.css`, `master_components.css`, `master_print.css`, and `master_alphabet_styles.css` must remain untouched.

---

## ✅ PERMISSIBLE REPLACEMENTS (ALLOWED ONLY)

Generators and designers are **ONLY** permitted to inject data into the designated template placeholders:

| Placeholder | Permitted Content | Example (Letter B) |
|---|---|---|
| `{{LETTER}}` | Single Uppercase Character | `"B"` |
| `{{LOWERCASE}}` | Single Lowercase Character | `"b"` |
| `{{WORD1}}` | First Vocabulary Word | `"Ball"` |
| `{{WORD2}}` | Second Vocabulary Word | `"Bear"` |
| `{{WORD3}}` | Third Vocabulary Word | `"Butterfly"` |
| `{{SVG1}}` | Clean Vector SVG for Word 1 | `<svg>...</svg>` |
| `{{SVG2}}` | Clean Vector SVG for Word 2 | `<svg>...</svg>` |
| `{{SVG3}}` | Clean Vector SVG for Word 3 | `<svg>...</svg>` |
| `{{THEME_COLOR}}` | Primary Hex Color Code | `"#5B9BD5"` |
| `{{THEME_COLOR_SECONDARY}}` | Darker Accent Hex Code | `"#3A6FA0"` |
| `{{THEME_COLOR_LIGHT}}` | Soft Background Tint Hex | `"#EAF4FB"` |
| `{{THEME_COLOR_BORDER}}` | Soft Card Border Hex | `"#C8DFF0"` |
| `{{WORKSHEET_TITLE}}` | Page Title String | `"The Letter B (Uppercase)"` |
| `{{DOC_CODE}}` | Unique Document Identifier | `"WW-KG-LTR-B-01"` |

---

## 🛠️ ENFORCEMENT & COMPLIANCE

Any generated worksheet HTML that violates the immutable rules will fail the Worksheet Wonder automated publishing QA pipeline.
