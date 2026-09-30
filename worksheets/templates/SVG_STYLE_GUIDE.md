# Worksheet Wonder — SVG Style Guide

> Every illustration in the Worksheet Wonder library must follow these rules to ensure a consistent, professional, print-friendly visual identity.

---

## 1. Design Principles

### The Worksheet Wonder Illustration Style Is:
- **Simple** — Children can recognise the object instantly
- **Cute** — Rounded shapes, friendly proportions
- **Clean** — No unnecessary detail or noise
- **Printable** — Works perfectly in monochrome at 300 DPI
- **Colourable** — Thick outlines with empty fill areas
- **Original** — No copyrighted artwork, ever

### The Style Is NOT:
- Realistic or detailed
- Shadowed or gradient-heavy
- Cartoon-network style with heavy exaggeration
- Pixel art or retro
- Clip-art or stock-image aesthetic

---

## 2. Technical Specifications

### Canvas & Viewbox
| Use Case           | Viewbox          | Recommended Size |
|:-------------------|:-----------------|:-----------------|
| Worksheet art      | `0 0 100 100`    | 100×100          |
| Activity icons     | `0 0 40 40`      | 40×40            |
| Small decorations  | `0 0 60 60`      | 60×60            |

### Stroke Rules
| Property          | Value                   | Notes                          |
|:------------------|:------------------------|:-------------------------------|
| Main outline      | `3–4px` stroke-width    | Outer edges of the object      |
| Detail lines      | `2px` stroke-width      | Internal features              |
| Fine accents      | `1.5px` stroke-width    | Texture, pattern               |
| Color             | `#1A1A2E` or `#000000`  | The brand ink color            |
| Line cap          | `round`                 | Always rounded ends            |
| Line join         | `round`                 | Always rounded corners         |
| Fill              | `none`                  | Outline only (for colouring)   |

### Exceptions to `fill: none`
These elements MAY use a solid fill:
- Animal eyes (small solid circles)
- Animal noses (small solid shapes)
- Decorative dots or seeds

---

## 3. Composition Guidelines

### Sizing
- The main subject should fill **70–80%** of the viewbox
- Leave **10–15%** breathing room on all sides
- Centre the subject both horizontally and vertically

### Complexity
- Maximum **8–12 path elements** per illustration
- No more than **3 levels of detail** (outline → features → accents)
- If a child can't identify it in 2 seconds, simplify it

### Anatomy for Characters (Animals, People)
- **Head:body ratio** — Aim for 1:1.5 (cuter than realistic)
- **Eyes** — Simple filled circles, positioned in upper third of face
- **No fingers** — Use mitten-shaped hands
- **Expressions** — Simple curves for smiles, avoid complex emotions

---

## 4. Code Structure

### Required Attributes
```xml
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 100 100"
     width="100"
     height="100">
  <!-- Description comment -->
  ...
</svg>
```

### Naming Paths
Use descriptive comments for each major element:
```xml
<!-- Body -->
<path d="..." />
<!-- Head -->
<circle ... />
<!-- Eyes -->
<circle ... />
```

### No External Dependencies
- No `<use>` references to external files
- No CSS classes inside SVG (all styles inline)
- No JavaScript
- No `<image>` tags embedding raster images
- No text elements (except in tracing templates)

---

## 5. Example: Creating an Apple

### Good Example ✅
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Apple Body -->
  <path d="M 50 25 C 40 25, 25 30, 25 55 C 25 75, 40 85, 50 85
           C 60 85, 75 75, 75 55 C 75 30, 60 25, 50 25 Z"
        fill="none" stroke="#1A1A2E" stroke-width="4"
        stroke-linejoin="round"/>
  <!-- Stem -->
  <path d="M 50 25 Q 52 15, 60 10"
        fill="none" stroke="#1A1A2E" stroke-width="4"
        stroke-linecap="round"/>
  <!-- Leaf -->
  <path d="M 52 20 Q 65 15, 60 25 Q 52 27, 52 20 Z"
        fill="none" stroke="#1A1A2E" stroke-width="3"
        stroke-linejoin="round"/>
</svg>
```
**Why it works:** 3 elements, instantly recognisable, clean outlines, colourable.

### Bad Example ❌
```xml
<!-- Too many elements, too much detail -->
<svg ...>
  <path d="..." fill="#ff0000" />       <!-- ❌ Coloured fill -->
  <path d="..." stroke-width="0.5" />   <!-- ❌ Too thin for print -->
  <image href="photo.jpg" />            <!-- ❌ Raster image -->
  <text>Apple</text>                    <!-- ❌ Text in illustration -->
  <!-- 20+ path elements -->            <!-- ❌ Too complex -->
</svg>
```

---

## 6. File Organisation

```
assets/svg/
├── components/        ← UI elements (logo, icons, stars)
│   ├── logo.svg
│   ├── corner-star.svg
│   ├── icon-trace.svg
│   ├── icon-match.svg
│   ├── icon-circle.svg
│   ├── icon-color.svg
│   ├── icon-cut.svg
│   ├── icon-paste.svg
│   ├── icon-find.svg
│   ├── icon-think.svg
│   ├── icon-write.svg
│   ├── icon-draw.svg
│   └── icon-sound.svg
│
├── alphabet/          ← Letter-related illustrations
│   ├── apple.svg
│   ├── astronaut.svg
│   └── ...
│
├── animals/           ← Animal illustrations
├── vehicles/          ← Vehicle illustrations
├── food/              ← Food illustrations
├── nature/            ← Nature illustrations
└── objects/           ← Common object illustrations
```

---

## 7. Quality Checklist

Before adding any SVG to the library:

- [ ] Viewbox is set correctly
- [ ] All strokes use `#1A1A2E` or `#000000`
- [ ] Minimum stroke-width is 1.5px
- [ ] Fill is `none` (except eyes/noses)
- [ ] `stroke-linecap="round"` on all open paths
- [ ] `stroke-linejoin="round"` on all joined paths
- [ ] Object is recognisable at 15mm × 15mm print size
- [ ] No external dependencies
- [ ] Comment describing each major element
- [ ] File named in lowercase with hyphens
