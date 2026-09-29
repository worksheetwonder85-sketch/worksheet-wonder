# 04. Illustration Standard Specification

To ensure Worksheet Wonder maintains a premium, cohesive "Disney meets Oxford" visual identity, every vector asset must comply with these exact standards.

## 1. Technical SVG Rules
*   **Format:** 100% SVG. No embedded raster images (`<image>`).
*   **Maximum Size on Page:** 90 mm x 90 mm (for Colouring sections).
*   **Minimum Size on Page:** 30 mm x 30 mm (for Vocabulary tags).
*   **ViewBox Padding:** Minimum 5% empty space on all sides of the internal viewBox coordinates to prevent edge clipping during CSS scaling.
*   **Outline Generation:** Every asset MUST have a separate `[Name]_outline.svg` where all fills are `#FFFFFF` and all strokes remain intact for coloring activities.

## 2. Stroke & Outline Rules
*   **Stroke Width:** Exactly 3.5 px (relative to a 100x100 grid).
*   **Stroke Color:** Dark Slate `#1E293B`. Pure black `#000000` is strictly forbidden as it is too harsh for kindergarten aesthetics.
*   **Corner Radius:** `stroke-linejoin="round"` and `stroke-linecap="round"` are mandatory on all paths. No sharp points.

## 3. Character Design (Animals/People)
*   **Eye Style:** Vertical ovals. Solid fill (`#1E293B`). Distance between eyes = 1.5x width of one eye.
*   **Smile Style:** "U" curve, 3 px stroke, placed high and tight to the eyes.
*   **Proportions:** 1:1 or 1:1.5 Head-to-Body ratio (Chibi style) to maximize emotional expression readability at small print sizes.

## 4. Colour Palette & Shading
*   **Fills:** Flat, vibrant, CMYK-safe colors only.
*   **Shadow Rules:** Gradients and drop-shadows are banned. Use hard-edged cell shading for depth, occupying maximum 15% of the object volume.
*   **Watermarks:** AI watermarks or creator signatures are strictly forbidden in the final SVG markup.
