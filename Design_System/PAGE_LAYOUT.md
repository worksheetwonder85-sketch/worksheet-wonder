# Worksheet Wonder: Page Layout & Grid System

## 1. Document Specifications
*   **Format:** A4 Portrait (210mm × 297mm)
*   **Resolution:** 300 DPI (Print standard)
*   **Color Profile:** CMYK optimized (though authored in RGB/Hex for digital HTML/CSS).
*   **Margins (Safe Print Area):**
    *   Top: 15mm
    *   Bottom: 15mm
    *   Left: 12mm
    *   Right: 12mm

## 2. Grid Architecture
The page utilizes a modular block system rather than a strict column grid. This allows for clear compartmentalization of activities, which is critical for children aged 4–6 who struggle with visually parsing dense information.

*   **The Container System:** All content is contained within clearly defined "Panels" or "Cards" with thick, rounded borders (`border-radius: 16px`, `border: 3px solid #2C3E50`).
*   **Shadows for Depth:** Panels use a hard drop-shadow (`4px 4px 0px #2C3E50`) to create a tactile, pop-out aesthetic reminiscent of high-quality board books.
*   **Whitespace Strategy (Macro):** 4mm to 5mm gaps between major panels. This negative space is essential; it acts as a visual palate cleanser between activities.
*   **Whitespace Strategy (Micro):** Generous internal padding within panels (minimum 4mm) to ensure text and illustrations never feel crowded against the borders.

## 3. Structural Hierarchy (Top to Bottom)

1.  **Global Header (10% of page height):** 
    *   Brand Logo, Grade Badges, Name, and Date lines. 
    *   *Purpose:* Establishes professional credibility and ownership.
2.  **Title & Objective Zone (15% of page height):**
    *   Massive Hero Title (e.g., "Letter A Discovery!").
    *   A scaffolded instruction block (yellow background) outlining the learning goal.
    *   *Purpose:* Directs focus immediately to the subject matter.
3.  **Active Learning Zone (60% of page height):**
    *   Usually split into a 2-column grid (`1fr 1fr`).
    *   Contains the Finger Trace, Vocabulary, and Handwriting Practice panels.
    *   *Purpose:* The core educational payload. The 2-column split prevents the child's eyes from having to track too far horizontally.
4.  **Footer Companion Zone (15% of page height):**
    *   Fun Facts, Teacher Notes, Self-Rating, and Document ID.
    *   *Purpose:* Adds value for the educator/parent without distracting the child from the main tasks.

## 4. Visual Balance
Visual weight must be evenly distributed. If the left column features a heavy, dark illustration (like a bear), the right column should counter-balance with a lighter, more intricate activity (like a ladybug spot search or dotted tracing lines). The hard borders provide structural stability so the page never feels chaotic.
