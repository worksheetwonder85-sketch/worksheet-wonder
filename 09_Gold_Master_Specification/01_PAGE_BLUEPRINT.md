# 01. Page Blueprint Specification

This document defines the strict mathematical boundaries and physical grid layout for the Worksheet Wonder A4 commercial print standard.

## 1. Canvas Specifications
*   **Format:** A4 Portrait
*   **Physical Width:** 210 mm
*   **Physical Height:** 297 mm
*   **Resolution Target:** 300 DPI
*   **Print Margins (Safe Zone):**
    *   Top Margin: 15 mm
    *   Right Margin: 15 mm
    *   Bottom Margin: 15 mm
    *   Left Margin: 15 mm
*   **Active Content Area:** 180 mm (W) x 267 mm (H)

## 2. Global Typography Hierarchy
*   **Primary Font:** Fredoka (Rounded, friendly, primary headings)
*   **Secondary Font:** Nunito (Clean, legible, instructions and vocabulary)
*   **Font Sizing Lock:**
    *   Hero Letter (Header): 142 pt (50 mm height equivalent)
    *   Section Titles: 24 pt
    *   Vocabulary Labels: 16 pt
    *   Tracing Text: 42 pt
    *   Footer Instructions: 11 pt

## 3. The 12-Column Grid
The Active Content Area is divided into a 12-column rigid CSS-style grid to ensure absolute alignment across thousands of worksheets.
*   **Gutter Width:** 4 mm between columns.
*   **Row Spacing:** Exactly 8 mm of vertical white space (padding) between every major `<section>`. No exceptions.

## 4. Component Bounding Boxes
*   **Hero Card:** 85 mm (W) x 65 mm (H)
*   **Vocabulary Illustration Box:** 45 mm (W) x 45 mm (H)
*   **Colouring Feature Box:** 90 mm (W) x 90 mm (H)
*   **Handwriting Row:** 180 mm (W) x 18 mm (H)
