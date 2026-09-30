# Worksheet Wonder — Naming Convention

> Every file, folder, and ID in the Worksheet Wonder system follows a consistent, predictable naming scheme.

---

## 1. Worksheet File Codes

### Format
```
<GRADE>-<SUBJECT>-<TOPIC>-<NUMBER>
```

### Grade Codes
| Grade        | Code |
|:-------------|:-----|
| Preschool    | `PS` |
| Kindergarten | `KG` |
| Grade 1      | `G1` |
| Grade 2      | `G2` |
| Grade 3      | `G3` |
| Grade 4      | `G4` |
| Grade 5      | `G5` |
| Grade 6      | `G6` |

### Subject Codes
| Subject          | Code  |
|:-----------------|:------|
| English          | `ENG` |
| Maths            | `MTH` |
| Science          | `SCI` |
| Social Studies   | `SOC` |
| Creative Writing | `CRW` |
| Art & Craft      | `ART` |
| Activities       | `ACT` |

### Topic Codes (Examples)
| Topic              | Code     |
|:-------------------|:---------|
| Alphabet           | `ALPHA`  |
| Phonics            | `PHON`   |
| Sight Words        | `SIGHT`  |
| Reading            | `READ`   |
| Numbers            | `NUM`    |
| Addition           | `ADD`    |
| Subtraction        | `SUB`    |
| Multiplication     | `MUL`    |
| Fractions          | `FRAC`   |
| Shapes             | `SHAPE`  |
| Counting           | `COUNT`  |
| Tracing            | `TRACE`  |
| Colouring          | `COLOR`  |
| Animals            | `ANIM`   |
| Plants             | `PLANT`  |

### Number
Sequential 3-digit number: `001`, `002`, ..., `999`

### Examples
| Worksheet                         | Code                |
|:----------------------------------|:--------------------|
| Kindergarten Alphabet Letter A    | `KG-ENG-ALPHA-001`  |
| Kindergarten Alphabet Letter B    | `KG-ENG-ALPHA-002`  |
| Grade 1 Addition Basics           | `G1-MTH-ADD-001`    |
| Grade 2 Sight Words Set 1        | `G2-ENG-SIGHT-001`  |
| Preschool Shape Tracing           | `PS-MTH-SHAPE-001`  |

---

## 2. Folder Structure

### Worksheet Files
```
worksheets/<grade>/<subject>/<topic>/<CODE>.html
```
Example:
```
worksheets/kindergarten/english/alphabet/KG-ENG-ALPHA-001.html
```

### SVG Illustrations
```
assets/svg/<topic>/            ← Topic-specific illustrations
assets/svg/components/         ← Reusable UI components (icons, logo, stars)
```

### Design System Templates
```
worksheets/templates/
├── design-tokens.css          ← CSS variables (source of truth)
├── master-template.css        ← All component styles
├── master-template.html       ← Reference implementation
├── DESIGN_SYSTEM.md           ← This documentation
├── NAMING_CONVENTION.md       ← File naming rules
└── SVG_STYLE_GUIDE.md         ← Illustration guidelines
```

### Thumbnails
```
database/images/worksheet-thumbnails/<CODE>.png
```

---

## 3. CSS Class Naming

All CSS classes use the `ww-` prefix (Worksheet Wonder) with BEM-inspired naming:

```
.ww-<block>
.ww-<block>__<element>
.ww-<block>--<modifier>
```

### Examples
| Class                      | Meaning                           |
|:---------------------------|:----------------------------------|
| `.ww-page`                 | The page container block          |
| `.ww-header__brand`        | Brand element inside the header   |
| `.ww-badge--grade`         | Grade modifier for badges         |
| `.ww-activity__num--3`     | Activity number with accent 3     |
| `.ww-trace-cell--guide`    | A guide variant of a trace cell   |

---

## 4. SVG File Naming

### Illustrations
```
<object>.svg
```
All lowercase, hyphen-separated for multi-word names.

Examples: `apple.svg`, `fire-truck.svg`, `ice-cream.svg`

### Icons
```
icon-<action>.svg
```
Examples: `icon-trace.svg`, `icon-match.svg`, `icon-cut.svg`

### Components
```
<component>.svg
```
Examples: `logo.svg`, `corner-star.svg`

---

## 5. JSON Database IDs

The `id` field in `worksheets.json` uses the worksheet code:
```json
{ "id": "KG-ENG-ALPHA-001" }
```
