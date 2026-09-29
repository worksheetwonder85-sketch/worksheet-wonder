# Worksheet Wonder – Master Alphabet Worksheet Engine

> **Production Template Architecture & Automated Worksheet Generator**
> *Designed for Commercial Publishing, Kindergarten Phonetics, and Scalable Alphabet Production.*

---

## 📁 SYSTEM DIRECTORY STRUCTURE

```
Workbook/
  Master_Template/
    ├── master_alphabet_template.html   # Master HTML structure with dynamic placeholders
    ├── master_alphabet_styles.css     # CSS entrypoint manifest importing modules
    ├── master_components.css          # Core UI components (Header, Title, Tracing, Footer)
    ├── master_print.css               # Exact A4 print geometry & color settings
    ├── master_variables.css           # Design tokens, typography, and line dimensions
    ├── alphabet_template.json         # Data configuration for letter generation
    ├── TEMPLATE_RULES.md              # Immutable rules & strict compliance guide
    ├── generate_letter.js             # Node.js generator script
    └── README.md                      # System documentation (this file)
```

---

## ⚡ QUICK START: GENERATING A WORKSHEET

To generate a new letter worksheet (e.g. `Letter_B.html`):

1. **Configure Data** in `alphabet_template.json`:
   ```json
   {
     "letter": "B",
     "uppercase": "B",
     "lowercase": "b",
     "worksheetTitle": "The Letter B (Uppercase)",
     "themeColor": "#5B9BD5",
     "words": ["Ball", "Bear", "Butterfly"],
     "illustrations": {
       "svg1": "<svg>...</svg>",
       "svg2": "<svg>...</svg>",
       "svg3": "<svg>...</svg>"
     }
   }
   ```

2. **Run Generator Command**:
   ```bash
   node generate_letter.js alphabet_template.json Letter_B.html
   ```

3. **Verify Output**:
   The script will generate a fully standalone, print-ready HTML file `Letter_B.html` with zero unreplaced placeholders.

---

## 🎨 DESIGN SYSTEM & MODULES

- **`master_variables.css`**: Defines A4 dimensions (`210mm × 297mm`), margins (`10mm / 14mm / 8mm`), typography (`Baloo 2`, `Quicksand`), and default color tokens.
- **`master_components.css`**: Modular styles for:
  - Header & Info Bar
  - Title & Subtitle
  - Hero Letter Display
  - Hero Illustration Area (3 SVG Cards)
  - Vocabulary Section ("B is for...")
  - Progressive Tracing Practice (Demo + 4 Rows)
  - Writing Practice (2 Tracing Rows)
  - Independent Handwriting (3 Blank Ruled Lines)
  - Footer & Encouragement
- **`master_print.css`**: Strict A4 print media queries (`@page { size: A4 portrait; margin: 0; }`).
- **`master_alphabet_styles.css`**: Imports all CSS modules into a single manifest.

---

## 🔒 IMMUTABLE COMPLIANCE

Before modifying or generating worksheets, consult **`TEMPLATE_RULES.md`**. Layout sizes, margins, fonts, tracing row heights, and component sequence must remain 100% untouched across all 26 letters of the alphabet.
