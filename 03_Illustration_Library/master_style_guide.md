# Worksheet Wonder: Master Illustration Style Guide

This document defines the strict visual rules for the Worksheet Wonder permanent asset database. To maintain a cohesive "Disney meets Oxford" brand identity, all SVGs must adhere to these standards.

## 1. Character Anatomy & Expressions
*   **Eye Style:** Vertical ovals. Solid fill (`#1E293B`). Distance between eyes should be approximately 1.5x the width of one eye. No complex irises or anime-style highlights.
*   **Smile Style:** A simple, friendly "U" curve. Stroke thickness `3px`, `stroke-linecap="round"`. Placed relatively high, close to the eyes to create a cute, child-like "chibi" proportion.
*   **Facial Proportions:** Large head-to-body ratio (usually 1:1 or 1:1.5). This maximizes facial expression visibility on small printed pages.
*   **Body Proportions:** Soft, stubby limbs. Avoid sharp elbows or knees.

## 2. Line & Stroke Rules
*   **Stroke Width:** All outlines MUST be exactly `3.5px` (when drawn on a 100x100 viewBox).
*   **Stroke Color:** Dark Slate (`#1E293B`). **NEVER** use pure black (`#000000`).
*   **Corner Radius (Joints):** All strokes must use `stroke-linejoin="round"` and `stroke-linecap="round"`. There should be zero sharp points in the entire library.

## 3. Colour & Shading
*   **Colour Palette:** CMYK-safe flat colors. Stick to pastel backgrounds with vibrant primary/secondary focal points.
*   **Shadow Rules:** **No gradients. No drop shadows.** If shading is required for depth, use cell-shading (a solid block of a slightly darker color) occupying no more than 15% of the object's volume.
*   **Highlights:** A simple white stroke or pill-shape can be used for specular highlights, but keep it minimal.

## 4. Object Proportions & White Space
*   **Object Proportions:** Simplified and iconic. An apple shouldn't look photorealistic; it should be the perfect Platonic ideal of an apple.
*   **White Space (Padding):** All SVGs must include at least 5% padding inside their viewBox. If the viewBox is `0 0 100 100`, no path should exceed the 5 to 95 coordinate range.

## 5. Scaling & Technical Rules
*   **Scaling Rules:** All artwork must be 100% vector (SVG). Raster graphics (`<image href="...png">`) are strictly forbidden.
*   **Transforms:** Flatten all matrix transforms before exporting.
*   **Outline SVGs:** Every full-color illustration must have a corresponding `_outline.svg` where all fills are removed (or set to `#FFFFFF`), ensuring it can be used in the "Colouring" section of the worksheets.
