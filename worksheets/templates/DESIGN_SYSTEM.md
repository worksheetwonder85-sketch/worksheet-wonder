# Worksheet Wonder — Design System Documentation

> Version 2.0 · Last Updated: July 2026  
> The definitive guide for creating every Worksheet Wonder printable worksheet.

---

## 1. Brand Identity

### Brand Name
**Worksheet Wonder**

### Brand Personality
| Trait         | Expression                                                    |
|:--------------|:--------------------------------------------------------------|
| Fun           | Bright rainbow accents, playful sparkle stars, rounded shapes |
| Premium       | Clean typography, precise spacing, professional borders       |
| Professional  | Consistent design tokens, ink-friendly monochrome content     |
| Creative      | Original SVG illustrations, engaging activity variety         |
| Educational   | Age-appropriate layouts, clear instructions, tracing guides   |
| Modern        | Minimal design, generous whitespace, refined color palette    |
| Friendly      | Rounded fonts, soft corners, warm off-white canvas            |

### Logo
The Worksheet Wonder logo is a stylised "W" formed by two overlapping pencils with a central 4-point sparkle star and a rainbow arc above. It symbolises writing, wonder, and discovery.

**File:** `assets/svg/components/logo.svg`

---

## 2. Color Palette

### Rainbow Spectrum (Brand Signature)
| Token                    | Hex       | Usage                              |
|:-------------------------|:----------|:-----------------------------------|
| `--ww-rainbow-red`       | `#EF5350` | Activity badge accent 1            |
| `--ww-rainbow-orange`    | `#FF9800` | Activity badge accent 2            |
| `--ww-rainbow-yellow`    | `#FFCA28` | Default badge fill, highlights     |
| `--ww-rainbow-green`     | `#66BB6A` | Age badge, nature themes           |
| `--ww-rainbow-blue`      | `#42A5F5` | Subject badge, footer link color   |
| `--ww-rainbow-indigo`    | `#5C6BC0` | Maths/logic themes                 |
| `--ww-rainbow-violet`    | `#AB47BC` | Creative/art themes                |

### Semantic Colors
| Token                    | Hex       | Usage                              |
|:-------------------------|:----------|:-----------------------------------|
| `--ww-color-ink`         | `#1A1A2E` | Borders, headings, primary text    |
| `--ww-color-text`        | `#2D3436` | Body instruction text              |
| `--ww-color-muted`       | `#8395A7` | Secondary labels, captions         |
| `--ww-color-hint`        | `#B2BEC3` | Dotted trace lines, placeholders   |
| `--ww-color-line`        | `#DFE6E9` | Internal dividers                  |
| `--ww-color-canvas`      | `#FAFAF8` | Page background (warm off-white)   |
| `--ww-color-surface`     | `#FFFFFF` | Activity card backgrounds          |
| `--ww-color-highlight`   | `#FFF8E1` | Guide-cell highlight zones         |

---

## 3. Typography

### Font Stack

| Role      | Font Family                        | Weight    | Usage                          |
|:----------|:-----------------------------------|:----------|:-------------------------------|
| Display   | **Fredoka** (Google Fonts)         | 600–700   | Titles, headings, badges       |
| Body      | **Nunito** (Google Fonts)          | 400–800   | Instructions, labels           |
| Tracing   | **Fredoka** (rendered as SVG)      | 700       | Dotted letter/word paths       |

### Size Scale (Print-Optimised)
| Token            | Size    | Usage                               |
|:-----------------|:--------|:------------------------------------|
| `--ww-fs-brand`  | 13pt    | Brand name in header                |
| `--ww-fs-title`  | 22pt    | Worksheet title (H1)               |
| `--ww-fs-section`| 10.5pt  | Activity section headings           |
| `--ww-fs-body`   | 9pt     | Instruction paragraphs             |
| `--ww-fs-label`  | 7.5pt   | Badges, picture captions           |
| `--ww-fs-micro`  | 6.5pt   | Footer, meta info                  |

---

## 4. Spacing System

Based on a **4mm grid** for consistent print alignment.

| Token          | Value  | Usage                              |
|:---------------|:-------|:-----------------------------------|
| `--ww-space-1` | 1mm    | Micro gaps                         |
| `--ww-space-2` | 2mm    | Component internal padding         |
| `--ww-space-3` | 3mm    | Standard gap between elements      |
| `--ww-space-4` | 4mm    | Column gutters, base unit          |
| `--ww-space-6` | 6mm    | Field group spacing                |
| `--ww-space-8` | 8mm    | Large section separators           |
| `--ww-space-10`| 10mm   | Page margins (top/bottom)          |
| `--ww-space-12`| 12mm   | Page margins (left/right)          |

---

## 5. Page Geometry

All worksheets are **A4 Portrait** (210mm × 297mm).

```
┌──────────────────────────────────────┐  ← 4mm outer border
│  ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐  │  ← 6.5mm inner border (dashed)
│  │  ★                          ★  │  │  ← Corner sparkle stars
│  │                                 │  │
│  │   ┌─── Content Area ────────┐   │  │  ← 10mm top, 12mm left/right
│  │   │                         │   │  │
│  │   │  Rainbow Stripe         │   │  │
│  │   │  Header                 │   │  │
│  │   │  Title Bar              │   │  │
│  │   │                         │   │  │
│  │   │  ┌──Col──┐ ┌──Col──┐   │   │  │
│  │   │  │       │ │       │   │   │  │
│  │   │  │ Acts  │ │ Acts  │   │   │  │
│  │   │  │       │ │       │   │   │  │
│  │   │  └───────┘ └───────┘   │   │  │
│  │   │                         │   │  │
│  │   │  Footer                 │   │  │
│  │   └─────────────────────────┘   │  │
│  │  ★                          ★  │  │
│  └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘  │
└──────────────────────────────────────┘
```

---

## 6. Border Design

| Element         | Weight    | Style  | Color          | Radius |
|:----------------|:----------|:-------|:---------------|:-------|
| Page frame      | 2.5px     | solid  | `--ww-color-ink` | 14px |
| Inner frame     | 1px       | dashed | `--ww-color-hint`| 11px |
| Activity card   | 2.5px     | solid  | `--ww-color-ink` | 12px |
| Card divider    | 1px       | dashed | `--ww-color-line`| —    |
| Tracing cell    | 1px       | dashed | `--ww-color-hint`| 6px  |
| Guide cell      | 1.8px     | solid  | `--ww-color-ink` | 6px  |
| Pill badge      | 1.8px     | solid  | `--ww-color-ink` | 20px |

---

## 7. Component Library

Every worksheet is assembled from these reusable components:

### Structural Components
| Component           | CSS Class              | Description                          |
|:--------------------|:-----------------------|:-------------------------------------|
| Page Shell          | `.ww-page`             | A4-locked flex container             |
| Outer Border        | `.ww-border-outer`     | Solid decorative frame               |
| Inner Border        | `.ww-border-inner`     | Dashed inner decorative frame        |
| Corner Star         | `.ww-corner`           | Sparkle decoration at 4 corners      |
| Watermark           | `.ww-watermark`        | Diagonal brand watermark             |
| Rainbow Stripe      | `.ww-rainbow-stripe`   | Signature gradient bar               |

### Header Components
| Component           | CSS Class              | Description                          |
|:--------------------|:-----------------------|:-------------------------------------|
| Header              | `.ww-header`           | Logo + brand name + metadata         |
| Badge               | `.ww-badge`            | Pill-shaped metadata tag             |
| Title Bar           | `.ww-title-bar`        | H1 title + Name/Date/Teacher fields  |
| Info Field          | `.ww-field`            | Label + underline input              |

### Activity Components
| Component           | CSS Class              | Description                          |
|:--------------------|:-----------------------|:-------------------------------------|
| Activity Card       | `.ww-activity`         | Bordered card wrapping any activity  |
| Activity Header     | `.ww-activity__head`   | Number + icon + title row            |
| Activity Body       | `.ww-activity__body`   | Content area for the activity        |
| Instruction Text    | `.ww-instruction`      | Star-bulleted instruction paragraph  |

### Activity-Type Components
| Component           | CSS Class              | Usage                                |
|:--------------------|:-----------------------|:-------------------------------------|
| Tracing Grid        | `.ww-trace-grid`       | Letter tracing rows with cells       |
| Bubble Row          | `.ww-bubble-row`       | Circle-the-letter bubbles            |
| Match Layout        | `.ww-match`            | Two-column picture↔word matching     |
| Picture Grid        | `.ww-pic-grid`         | Grid of illustration cards           |
| Color Row           | `.ww-color-row`        | Side-by-side coloring boxes          |
| Word Grid           | `.ww-word-grid`        | Word tracing boxes (2-column)        |
| Writing Lines       | `.ww-write-lines`      | Handwriting practice lines           |
| Draw Box            | `.ww-draw-box`         | Open drawing area                    |
| Cut Strip           | `.ww-cut-strip`        | Dashed cut-and-paste strip           |

### Footer Components
| Component           | CSS Class              | Description                          |
|:--------------------|:-----------------------|:-------------------------------------|
| Footer              | `.ww-footer`           | Copyright + URL + page number + QR   |
| QR Placeholder      | `.ww-qr-placeholder`  | Space for future QR code             |

---

## 8. SVG Style Guide

### Illustration Rules
All Worksheet Wonder illustrations must follow these rules:

1. **Viewbox:** `0 0 100 100` (standard) or `0 0 60 60` (small icons)
2. **Stroke Color:** `#1A1A2E` (the ink color) or `#000000`
3. **Stroke Width:** 3–4px for outlines, 2px for internal details
4. **Fill:** `none` (outline-only for coloring activities)
5. **Style:** Simple, cute, recognisable silhouettes
6. **Corners:** Use `stroke-linejoin="round"` and `stroke-linecap="round"`
7. **Complexity:** Maximum 8–12 path elements per illustration
8. **No Gradients** in illustrations (print-friendly)
9. **No Text** inside illustrations (language-independent)

### Icon Rules (Activity Type Icons)
1. **Viewbox:** `0 0 40 40`
2. **Stroke Width:** 2.5px
3. **Stroke Color:** `#1A1A2E`
4. **Fill:** `none` (except solid dots/fills for emphasis)
5. **Style:** Minimal line art, immediately recognisable

### Available Activity Icons
| Icon File          | Activity Type    | Visual               |
|:-------------------|:-----------------|:----------------------|
| `icon-trace.svg`   | Trace            | Pencil                |
| `icon-match.svg`   | Match            | Crossed lines         |
| `icon-circle.svg`  | Circle           | Circle with checkmark |
| `icon-color.svg`   | Color            | Paint palette         |
| `icon-cut.svg`     | Cut              | Scissors              |
| `icon-paste.svg`   | Paste            | Glue bottle           |
| `icon-find.svg`    | Find             | Magnifying glass      |
| `icon-think.svg`   | Think            | Lightbulb             |
| `icon-write.svg`   | Write            | Hand writing          |
| `icon-draw.svg`    | Draw             | Crayon                |
| `icon-sound.svg`   | Sound/Listen     | Sound waves           |

---

## 9. Activity Badge Color Sequence

Each numbered activity badge cycles through the rainbow:

| Activity # | Token            | Color          |
|:-----------|:-----------------|:---------------|
| 1          | `--ww-accent-1`  | Red            |
| 2          | `--ww-accent-2`  | Orange         |
| 3          | `--ww-accent-3`  | Yellow         |
| 4          | `--ww-accent-4`  | Green          |
| 5          | `--ww-accent-5`  | Blue           |
| 6          | `--ww-accent-6`  | Indigo         |
| 7          | `--ww-accent-7`  | Violet         |
| 8          | `--ww-accent-8`  | Red (restart)  |

---

## 10. Creating a New Worksheet

To create any worksheet from this template:

### Step 1: Copy the Template
```
worksheets/templates/master-template.html → worksheets/<grade>/<subject>/<topic>/<CODE>.html
```

### Step 2: Replace Template Variables
| Variable               | Location                  | Example                      |
|:-----------------------|:--------------------------|:-----------------------------|
| Grade badge text       | `.ww-badge--grade`        | "Grade 1"                    |
| Subject badge text     | `.ww-badge--subject`      | "Maths"                      |
| Age badge text         | `.ww-badge--age`          | "Ages 6–7"                   |
| Worksheet code         | `.ww-badge--code`         | "G1-MTH-ADD-001"             |
| Difficulty badge       | `.ww-badge--diff`         | "Medium"                     |
| Worksheet title        | `.ww-title`               | "Double-Digit Addition"      |
| Page title tag         | `<title>`                 | "Worksheet Wonder — ..."     |

### Step 3: Compose Activity Sections
Pick and arrange activity components from the library. Each worksheet typically has 4–8 activities arranged in a 2-column layout.

### Step 4: Add Illustrations
Replace placeholder SVG circles with actual illustrations from `assets/svg/alphabet/` or create new ones following the SVG Style Guide.

### Step 5: Test Print
Open in Chrome → Print → Set to A4, No Margins, Background Graphics ON.

---

## 11. Watermark Specifications

| Property    | Value                               |
|:------------|:------------------------------------|
| Text        | "Worksheet Wonder"                  |
| Font        | Fredoka, 700 weight                 |
| Size        | 72pt (`--ww-watermark-size`)        |
| Color       | rgba(26, 26, 46, 0.045)            |
| Rotation    | -32 degrees                         |
| Position    | Centered on page                    |
| Z-Index     | 0 (behind all content)              |

---

## 12. Print QA Checklist

Before releasing any worksheet:

- [ ] Page fits exactly on A4 without clipping
- [ ] All text is within the inner dashed border
- [ ] Rainbow stripe renders with colour
- [ ] Watermark is barely visible when printed
- [ ] Tracing letters render as dotted paths
- [ ] All SVG illustrations print cleanly in monochrome
- [ ] Footer shows correct copyright, URL, and page number
- [ ] Font weights render correctly (not too thin for print)
- [ ] No content overlaps the decorative border frame
- [ ] Works with "Background Graphics" both ON and OFF
