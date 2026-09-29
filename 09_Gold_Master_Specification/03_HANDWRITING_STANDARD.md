# 03. Handwriting Standard Specification

Handwriting is the most technically demanding aspect of the publishing engine. This document enforces the exact mathematical parameters for the 3-line guide system.

## 1. Guideline Mathematics
Every handwriting row (`.hw-row`) is a rigidly positioned component.
*   **Total Row Height:** 18 mm.
*   **Top Line (Cap Height):** Solid line, 0.5 mm thickness, `#94A3B8`.
*   **Dashed Midline (X-Height):** Dashed line, 0.5 mm thickness, `#CBD5E1`.
*   **Bottom Line (Baseline):** Solid line, 0.5 mm thickness, `#94A3B8`.
*   **Line Spacing:** Exactly 6 mm between Top and Midline. Exactly 6 mm between Midline and Baseline.

## 2. Letter Height & Positioning
*   **Uppercase Letters:** Must touch the Top line and rest exactly on the Baseline (12 mm physical height).
*   **Lowercase (Ascenders like 'b', 'h'):** Must touch the Top line and rest on the Baseline (12 mm).
*   **Lowercase (Standard like 'a', 'c'):** Must touch the Midline and rest on the Baseline (6 mm).
*   **Lowercase (Descenders like 'g', 'p'):** Must touch the Midline and extend exactly 6 mm *below* the Baseline.

## 3. Tracing Mechanics
*   **Dotted Tracing:** Letters in tracing rows must use a `#E2E8F0` solid fill or a dashed stroke configuration. Font size is locked to `42pt`.
*   **Starting Dots:** A dark circle (`#1E293B`), exactly 2.5 mm in diameter, must indicate the exact starting coordinate for the first pencil stroke.
*   **Direction Arrows:** Red (`#EF4444`) arrows, 1 mm stroke thickness, must indicate stroke direction in the Demonstration section.

## 4. Finger Tracing (Road Style)
*   **Track Width:** 12 mm wide hollow path.
*   **Track Border:** 1.5 mm solid line (`#475569`).
*   **Track Center:** A white/yellow dashed line running exactly down the mathematical center of the letter path to mimic a road.

## 5. Independent Writing
*   The final row provides only the 3-line guides and the 2.5 mm Starting Dots. No tracing letters are permitted in this section.
