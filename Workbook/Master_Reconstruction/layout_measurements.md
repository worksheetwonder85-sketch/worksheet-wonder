# Worksheet Wonder: Layout Measurements & Specifications

## 1. Document Canvas
*   **Format:** A4 Portrait (210mm × 297mm)
*   **Base Margins (`.page-container` padding):** 
    *   Top / Bottom: 15mm
    *   Left / Right: 12mm
*   **Background Colors:**
    *   Body: `#ffffff`
    *   Page Container: `#FFFDF9`

## 2. Border System (`.page-borders`)
*   **Outer Border:**
    *   Stroke Color: `#2C3E50`
    *   Stroke Width: 0.8mm
    *   Dimensions: 202mm × 289mm (Inset 4mm)
    *   Border Radius (rx, ry): 8
*   **Inner Border:**
    *   Stroke Color: `#2C3E50`
    *   Stroke Width: 0.4mm
    *   Dimensions: 194mm × 281mm (Inset 8mm)
    *   Border Radius (rx, ry): 6

## 3. Vertical Rhythm & Spacing
*   **Header Section:** `margin-bottom: 2mm`, `padding-bottom: 2mm` (Border bottom 3.5px solid `#2C3E50`)
*   **User Info Bar:** `margin-bottom: 3mm`, Gap between fields: 6mm
*   **Title Block:** `margin-bottom: 3mm`
*   **Scaffold Block (Instructions):** `margin-bottom: 4mm`, Padding: `3mm 4mm`
*   **Activity Row Container:** `margin-bottom: 4mm`, Grid Gap: 5mm
*   **Footer Section:** `padding-top: 3mm`, Flex Gap: 3mm (Border top 3px solid `#2C3E50`)

## 4. Typography Matrix
*   **Primary Font:** `Fredoka` (Display, Titles, Labels)
*   **Secondary Font:** `Nunito` (Body, Instructions)
*   **Base Color:** `#2C3E50`

| Element | Font Family | Size | Weight | Color |
| :--- | :--- | :--- | :--- | :--- |
| Brand Logo Text | Fredoka | 16pt | 700 (Bold) | `#FF7043` |
| Badges | Fredoka | 8.5pt | 600 (Semi-Bold) | `#2C3E50` |
| User Info Label | Fredoka | 11pt | 700 (Bold) | `#2C3E50` |
| Worksheet Title | Fredoka | 26pt | 700 (Bold) | `#2C3E50` |
| Objective Text | Nunito | 9.5pt | Italic | `#7F8C8D` |
| Instructions | Nunito | 12.5pt | 700 (Bold) | `#2C3E50` |
| Panel Titles | Fredoka | 12pt | 700 (Bold) | `#2C3E50` |
| Mascot Dialog | Fredoka | 11pt | Regular | `#2C3E50` |
| Fun Fact Text | Nunito | 9.5pt | Regular | `#2C3E50` |
| Fun Fact Title | Fredoka | Inherit | 700 (Bold) | `#00796B` |
| Notes Text | Nunito | 8.5pt | Regular | `#555555` |
| Notes Title | Fredoka | 7.5pt | 700 (Bold) | `#555555` |
| Footer Bar | Nunito | 8.5pt | Regular | `#7F8C8D` |

## 5. UI Components & Panels
*   **Panels (`.panel`):**
    *   Border: 3px solid `#2C3E50`
    *   Border Radius: 16px
    *   Padding: 4mm
    *   Background: `#ffffff`
    *   Box Shadow: `4px 4px 0px #2C3E50`
*   **Scaffold Block:**
    *   Border: 3px solid `#2C3E50`
    *   Border Radius: 16px
    *   Padding: 3mm 4mm
    *   Background: `#FFFDE7`
    *   Box Shadow: `4px 4px 0px #2C3E50`
*   **Badges (`.badge`):**
    *   Border: 2px solid `#2C3E50`
    *   Border Radius: 6px
    *   Padding: 2px 10px
    *   Box Shadow: `2px 2px 0px #2C3E50`

## 6. Grid System
*   **Activity Row:** `display: grid; grid-template-columns: 1fr 1fr; gap: 5mm;`
*   **Notes Row:** `display: grid; grid-template-columns: 1fr 1fr; gap: 4mm;`
*   **User Info Bar:** Flexbox, Name field `flex-grow: 2.2`, Date field `flex-grow: 1`. 
*   **Info Lines:** Height 6mm. Solid base line (2.5px), dashed top line (1.5px, `#BDC3C7`) offset by 2.5mm from bottom.
