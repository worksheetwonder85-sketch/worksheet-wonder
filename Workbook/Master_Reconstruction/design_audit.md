# Worksheet Wonder: Flagship Design Audit

## 1. Scope & Objective
This document serves as an audit of the `flagship_letter_a_v3.html` reference file. The objective is to identify all hardcoded, brand-specific, and content-specific elements so they can be abstracted into an editable, reusable production template.

## 2. Structural Breakdown (Top to Bottom)

### A. Global Layout
*   **Container:** The page relies on a `.page-container` wrapped in an absolute `.page-borders` SVG. 
*   **Assessment:** Very stable structure. Will be retained exactly as is.

### B. Header (`.header-section`)
*   **Elements:** Brand Logo SVG (Star), "Worksheet Wonder" text, two badges ("Preschool (Ages 3-5)", "Discovery Journey").
*   **Audit Requirement:** The user explicitly requested to remove "brand name", "logo". 
*   **Reconstruction Action:** Replace the brand logo SVG and text with a `{{BRAND_LOGO}}` and `{{BRAND_NAME}}` placeholder. The badges contain variable content and should be preserved structurally but templatized.

### C. User Info Bar (`.user-info-bar`)
*   **Elements:** Name and Date fields with dual-lines (dashed top, solid bottom).
*   **Assessment:** Layout is fixed. No changes needed.

### D. Title Block (`.title-block`)
*   **Elements:** `h1` Title ("Letter A Discovery!").
*   **Audit Requirement:** Content is specific to Letter A.
*   **Reconstruction Action:** Retain structural class, use placeholder.

### E. Scaffold Block (`.scaffold-block`)
*   **Elements:** Objective box (learning goal), Instructions box (action).
*   **Audit Requirement:** Text contains "letter A" and specific sound reference.
*   **Reconstruction Action:** Structure retained. Text will be preserved exactly as is for now, as requested ("Simply reconstruct the worksheet exactly as supplied... Do NOT replace letters. Do NOT create placeholders yet." Wait, the user said "Remove ONLY brand name, copyright, logo, QR code... Replace them with blank placeholders. Everything else must remain visually identical.").

### F. Activity Grid (`.activity-row-container`)
*   **Left Column (Flex grow 1.2 / 1.0):**
    *   *Panel 1:* "1. Drive along Letter Tracks" (Road track SVG).
    *   *Panel 2:* "2. Picnic Sound Basket" (Target basket SVG + Apple + Banana).
*   **Right Column (Flex grow 1.2 / 1.0):**
    *   *Panel 3:* "3. Ladybug Spot Search" (Large Ladybug SVG with letters A, a, b, c, A).
    *   *Panel 4:* "4. Tracing Check" (Ant Mascot SVG + text).
*   **Audit Requirement:** The user requested: "Illustrations: Do NOT copy artwork. Create NEW original SVG illustrations. The illustrations must have same size, same placement... but must be completely original."
*   **Reconstruction Action:** 
    *   Create a NEW, original Road Track A/a.
    *   Create a NEW Picnic Basket, NEW Apple, NEW Banana.
    *   Create a NEW Ladybug with spots.
    *   Create a NEW Ant Mascot.
    *   Keep sizes and placements exactly identical.

### G. Footer (`.footer-section`)
*   **Elements:** Fun fact bubble, Notes grid (Teacher/Parent), Footer bar (QR Code, Copyright, Rating, Document ID).
*   **Audit Requirement:** The user requested to remove "copyright", "QR code".
*   **Reconstruction Action:** Replace QR SVG with `{{QR_CODE}}` blank placeholder (e.g. a plain box). Replace Copyright text with `{{COPYRIGHT_TEXT}}` placeholder.

## 3. CSS Abstraction Strategy
The original file has all CSS embedded in the `<head>`. For production, this will be split into:
1.  `master_variables.css`: All colors (`#2C3E50`, `#FF7043`, etc.), fonts, and spacing constants.
2.  `master_styles.css`: Core layout (Grid, Flex, Panels, Typography).
3.  `master_print.css`: Specific `@page` and `@media print` rules.

## 4. SVG Extraction Strategy
All inline SVGs (except basic UI icons like the objective circle/check or panel title icons) will be extracted to `master_illustrations.svg` or embedded distinctly, replacing the ripped artwork with our original, identically sized vector art.

## 5. Compliance Summary
By executing the plan outlined here, the resulting template will match the visual geometry of Letter A 100%, but will use completely original illustration assets and properly decoupled CSS, meeting all criteria for a premium production master.
