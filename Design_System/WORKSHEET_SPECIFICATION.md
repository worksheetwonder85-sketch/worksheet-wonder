# Worksheet Wonder: Master Specification Blueprint

## 1. Document Overview
This specification is the final architectural blueprint bridging the design philosophy with the technical implementation (HTML/CSS). It dictates exactly how the `master.html` template will be structured.

## 2. CSS Architecture
The template will rely on standard CSS properties with a heavy emphasis on:
*   `display: flex` and `display: grid` for robust, unbreakable layouts.
*   `@media print` queries to ensure backgrounds render (`-webkit-print-color-adjust: exact`).
*   CSS Variables (`:root`) for all colors and fonts to allow instant global rebranding.

## 3. Component Mapping (HTML Structure)

### `<body>` -> `.page-container`
The master wrapper handling the A4 210x297mm dimensions, 15mm/12mm padding, and the `relative` positioning context for the borders.

### ↳ `.page-borders`
Absolute positioned SVG overlapping the container, featuring `.outer-border` (thick) and `.inner-border` (thin, rounded).

### ↳ `.header-section`
Flexbox row (`justify-content: space-between`).
*   Left: `.brand-logo-container` (SVG + Fredoka text).
*   Right: `.meta-badges` (Grade & Subject tags).

### ↳ `.user-info-bar`
Flexbox row.
*   Field 1: "Name:" + `.info-line-wrapper` (dashed top line, solid bottom line).
*   Field 2: "Date:" + `.info-line-wrapper`.

### ↳ `.title-block`
Centered container holding the `.worksheet-title` (`<h1>`, Fredoka 26pt+).

### ↳ `.scaffold-block`
The pale yellow instruction card.
*   `.objective-box`: Small, italicized learning goal.
*   `.instructions-box`: Large, bold, actionable instruction with a supporting icon.

### ↳ `.activity-row-container`
The core grid: `display: grid; grid-template-columns: 1fr 1fr;`.

#### ↳ Left `.grid-column`
*   **`.panel` 1 (Gross Motor):** "Drive along Letter Tracks". Contains massive SVG path with starting dots and dashed center-lines.
*   **`.panel` 2 (Vocabulary Match):** "Sound Basket". Contains the target letter/sound and 2-3 colorful SVG objects.

#### ↳ Right `.grid-column`
*   **`.panel` 3 (Search & Find / Coloring):** "Spot Search". Contains a large character (e.g., Ladybug, Tree) with letters hidden inside circles. A secondary instruction asks the child to color specific letters.
*   **`.panel` 4 (Fine Motor / Writing):** "Tracing Check". Contains the mascot giving a tip, or acts as the dedicated space for the 3-line dotted handwriting guides. *(Note: Depending on the specific worksheet, Handwriting may span full-width across the bottom of the activity grid).*

### ↳ `.footer-section`
*   `.fun-fact-bubble`: Pale blue pill-shaped container.
*   `.notes-grid`: 2-column grid for Teacher Guide and Parent Companion text boxes.
*   `.footer-bar`: Flexbox row containing the QR code placeholder, copyright, star self-rating system, and technical Document ID string.

## 4. Reusability Strategy
The template will be built using placeholder text (e.g., `{{LETTER_UPPER}}`, `{{VOCAB_1}}`). The CSS (`master.css`) will be completely decoupled from the HTML content, ensuring that a script can generate Letters A through Z simply by swapping the variables and SVG blocks, without ever touching the styling rules.
