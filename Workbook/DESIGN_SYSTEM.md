# 🎨 Worksheet Wonder Design System & UI Specifications

This document defines the complete visual design system, typography tokens, grid parameters, print specifications, and component standards for **"My First Alphabet Workbook"** and all subsequent Worksheet Wonder commercial print products.

---

## 1. Page Layout & Grid System

### Print Dimensions (A4 Standard)
- **Page Size**: A4 Portrait (`210mm × 297mm`)
- **Outer Padding**: Top `13mm`, Right `12mm`, Bottom `11mm`, Left `12mm`
- **Dual Border System**:
  - **Outer Frame**: `0.8mm` solid `#2C3E50`, inset `5mm` from page edge.
  - **Inner Guideline**: `0.35mm` dashed `#BDC3C7`, inset `7mm` from page edge.
- **Activity Grid Layout**: 2-Column Responsive Flex Grid (`gap: 3mm` between panels).

### CSS Safe Margins Token Structure:
```css
@page { size: A4 portrait; margin: 0; }
body {
  width: 210mm; min-height: 297mm;
  font-family: 'Nunito', sans-serif;
  color: #2C3E50; background: #FFFDF9;
  -webkit-print-color-adjust: exact;
  color-adjust: exact;
}
.page {
  width: 210mm; min-height: 297mm;
  padding: 13mm 12mm 11mm 12mm;
  display: flex; flex-direction: column;
  gap: 2.5mm; position: relative;
}
```

---

## 2. Typography Hierarchy & Point Scale

| Role | Font Family | Size (pt) | Weight | Line Height | Color |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Brand Logo** | `'Fredoka', sans-serif` | `16pt` | `700` | `1.2` | `#FF7043` |
| **Badge Pills** | `'Fredoka', sans-serif` | `8pt` | `600` | `1.0` | `#2C3E50` |
| **Main Page Title** | `'Fredoka', sans-serif` | `20pt` | `700` | `1.1` | `#2C3E50` |
| **Panel Header** | `'Fredoka', sans-serif` | `10pt` | `700` | `1.2` | `#2C3E50` |
| **Instructions** | `'Nunito', sans-serif` | `7.5pt` | `400 (Italic)`| `1.3` | `#546E7A` |
| **Display Model Letter**| `'Fredoka', sans-serif` | `62pt` | `700` | `1.0` | Grade Accent |
| **Tracing Letters** | `'Fredoka', sans-serif` | `32pt` | `700` | `1.1` | `-webkit-text-stroke: 2px rgba(44,62,80,0.25); color: transparent;` |
| **Search Matrix Cell** | `'Fredoka', sans-serif` | `11pt` | `600` | `1.0` | `#2C3E50` |
| **Handwriting Model** | `'Fredoka', sans-serif` | `18pt` | `700` | `1.0` | `rgba(0,0,0,0.3)` |

---

## 3. Color Palette Tokens & Accessibility

### Primary Brand Palette
- **Brand Orange**: `#FF7043` (Primary logo & CTA)
- **Dark Slate**: `#2C3E50` (Primary borders, text, & framing)
- **Paper Background**: `#FFFDF9` (Soft warm white to reduce eye strain)

### Grade Accent Palette System (Alphabet Workbook Colors)
- **Letter A (Red)**: `#FF5252` | Soft BG: `#FFEBEE` | Tracing Stroke: `rgba(229,57,53,0.35)`
- **Letter B (Orange)**: `#FF9800` | Soft BG: `#FFF8E1` | Tracing Stroke: `rgba(230,81,0,0.35)`
- **Letter C (Amber)**: `#F9A825` | Soft BG: `#FFFDE7` | Tracing Stroke: `rgba(245,127,23,0.35)`
- **Letter D (Green)**: `#388E3C` | Soft BG: `#F1F8E9` | Tracing Stroke: `rgba(27,94,32,0.35)`
- **Letter E (Blue)**: `#1565C0` | Soft BG: `#E3F2FD` | Tracing Stroke: `rgba(13,71,161,0.35)`

### Black-and-White Print Compatibility Guardrails:
- All panel borders use `#2C3E50` with minimum `2.5px` stroke weight.
- Contrast ratio between text and panel backgrounds is minimum `7:1` (WCAG AAA compliant).
- Dotted tracing paths use high-contrast outline masks so letters remain crisp even on low-ink laser prints.

---

## 4. UI Components & Activity Cards

### Panel Card Specification:
```css
.panel {
  border: 2.5px solid #2C3E50;
  border-radius: 13px;
  padding: 2.5mm 3mm;
  background: #ffffff;
  box-shadow: 3px 3px 0 #2C3E50;
  display: flex; flex-direction: column;
  gap: 1.5mm;
}
.panel-title {
  font-family: 'Fredoka', sans-serif;
  font-size: 10pt; font-weight: 700;
  border-bottom: 2px solid #2C3E50;
  padding-bottom: 1mm;
}
```

### User Information Header Bar:
Includes Name, Date, and Teacher fields with baseline rules:
```html
<div class="user-bar">
  <div class="user-field"><span class="user-label">Name:</span><div class="user-line"></div></div>
  <div class="user-field"><span class="user-label">Date:</span><div class="user-line"></div></div>
  <div class="user-field"><span class="user-label">Teacher:</span><div class="user-line"></div></div>
</div>
```

---

## 5. Vector Illustration & Icon Style Standards
- **Format**: 100% Inline SVG `<svg viewBox="0 0 W H" fill="none">`.
- **Line Weight**: `1.5px` to `2.5px` stroke paths (`#2C3E50` or `#333333`).
- **Aesthetic**: Soft rounded corners (`rx`, `ry`), warm cheerful expressions, white highlight reflections (`opacity="0.4"`).
- **Iconography**: Standardized unicode & SVG activity icons (🌟 ✏️ ⭕ 🔊 🔍 📝 ⭐).
