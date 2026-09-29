# Gold Master: SVG Illustration Guide

Vector graphics are mandatory for the Worksheet Wonder pipeline to guarantee infinite resolution at 300 DPI and minimal file size. All placeholders (`{{SVG1}}`, `{{COLORING_SVG}}`, etc.) must adhere to these exact stylistic rules when replaced with final assets.

## 1. The "Worksheet Wonder" Aesthetic
*   **Stroke Width:** Uniform `3px` to `4px`.
    *   *Why:* Thick, confident outlines mimic coloring books. They hold up beautifully in print and provide clear boundaries for young eyes.
*   **Stroke Color:** Dark Slate (`#1E293B`), NEVER pure black (`#000000`).
*   **Joints & Caps:** `stroke-linejoin="round"` and `stroke-linecap="round"`. 
    *   *Why:* Sharp corners feel aggressive; rounded caps feel soft, safe, and toy-like.
*   **Fills:** Solid, bright, flat colors (CMYK-safe). No internal gradients, no drop shadows inside the SVG (use CSS for UI shadows, keep SVGs flat).

## 2. Bounding Box Rules
To ensure the HTML grid never breaks when a template is generated, all SVGs must be drawn to strict square aspect ratios.
*   **Meet the Letter SVGs (x3):** `viewBox="0 0 100 100"`. The artwork must fill at least 80% of this bounding box.
*   **Colouring SVG (x1):** `viewBox="0 0 150 150"`. 

## 3. The Colouring Activity SVG
The final SVG in the layout (`{{COLORING_SVG}}`) has special rules:
*   **No Fills:** All `fill` attributes must be strictly `#FFFFFF` or `none`.
*   **Enclosed Paths:** All strokes must mathematically connect to form closed shapes. If paths are open, children get frustrated because they do not know where to stop coloring.
*   **Complexity:** Medium-low. Too many tiny details will result in crayon-bleeding. Keep shapes large and inviting.

## 4. The Placeholder System
In the `GOLD_MASTER.svg` file, I will create specialized "Placeholder Assets" for the layout. These will not just be empty boxes; they will be stylized, dotted-outline shapes with clear labels (e.g., an icon of an image with `{{SVG1}}` text inside) so the template looks professional even in its unfilled state.
