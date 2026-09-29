# Worksheet Wonder: MASTER GRID SYSTEM

## 1. Grid Philosophy
To ensure 100% layout consistency across the entire A-Z series, the Gold Master uses a rigid **Mathematical Block Grid**. The layout consists of equal-width columns (50/50 splits) and fixed-height rows. The grid is immutable; only the content inside the fixed bounding boxes changes.

## 2. Canvas Dimensions
*   **Physical Format:** A4 Portrait (210mm × 297mm)
*   **Hardware Margins (Padding):** 10mm (Top/Bottom, Left/Right)
*   **Usable Canvas:** 190mm (Width) × 277mm (Height)

## 3. The Column System
The layout utilizes a strict **2-Column Grid** (`1fr 1fr`).
*   **Total Width:** 190mm
*   **Gutter (Gap):** 6mm
*   **Column Width:** 92mm

## 4. Vertical Rhythm (Row Allocations)
To accommodate the extensive requirements without feeling cramped, row heights are mathematically locked to exactly fit the 277mm usable canvas. The gap between every major row is `5mm`.

### Row 1: Header & Meta (Height: 8mm)
*   **Span:** Full Width (190mm)
*   **Content:** Name, Date, Class, Teacher.

### Row 2: Look & Gross Motor (Height: 40mm)
*   **Column 1 (92mm):** `BIG HERO LETTER`. (Fixed bounding box: 40mm x 40mm for the uppercase/lowercase group).
*   **Column 2 (92mm):** `FINGER TRACE`. (Fixed bounding box: 40mm x 40mm).

### Row 3: Meet the Letter / Vocabulary (Height: 42mm)
*   **Span:** Full Width (190mm)
*   **Layout:** Internal 3-column flex (`justify-content: space-between`).
*   **Content:** Three SVGs `{{SVG1}}`, `{{SVG2}}`, `{{SVG3}}`. 
*   **Fixed Dimensions:** SVGs (30mm × 30mm box), Words (10mm height text box below).

### Row 4: Guided Tracing (Height: 65mm)
*   **Span:** Full Width (190mm)
*   **Content:** 5 Rows of perfect handwriting guides.
*   **Grid Math:** `11mm` row height × 5 = 55mm. `2.5mm` gap between rows × 4 = 10mm. Total = 65mm.
*   *(Note: 11mm height is ideal for the transition from gross to fine motor skills in late preschool/kindergarten).*

### Row 5: Independent Writing (Height: 38mm)
*   **Span:** Full Width (190mm)
*   **Content:** 3 Rows of blank handwriting guides.
*   **Grid Math:** `11mm` row height × 3 = 33mm. `2.5mm` gap × 2 = 5mm. Total = 38mm.

### Row 6: Colouring & Support (Height: 42mm)
*   **Column 1 (92mm):** `COLOURING ACTIVITY`. Fixed bounding box (42mm × 42mm) for `{{COLORING_SVG}}`.
*   **Column 2 (92mm):** `PARENT TIP`. A fixed rectangular box (92mm × 42mm) for instructional text.

### Row 7: Footer (Height: 7mm)
*   **Span:** Full Width (190mm)
*   **Content:** Page Number, Title placeholder, Version placeholder.

## 5. Total Height Verification
*   Row Heights: `8` + `40` + `42` + `65` + `38` + `42` + `7` = **242mm**
*   Inter-Row Gaps: 6 gaps × `5mm` = **30mm**
*   **Total Height:** 242mm + 30mm = **272mm** 
*   *This perfectly fits within the 277mm usable canvas, leaving a comfortable 5mm bottom breathing space!*

## 6. Immutable Boundaries
Every element inside these rows acts as a fixed `div` with `overflow: hidden` and explicit `width/height`. This ensures that no matter how large an SVG is uploaded for `{{SVG1}}`, it will safely scale to fit its 30x30mm bounding box, guaranteeing the worksheet never breaks across pages.
