# Worksheet Wonder: Master Production Template

This directory contains the highly decoupled, production-ready master template reconstructed from the flagship Letter A design. It serves as the immutable structural foundation for generating every letter (A-Z) in the Discovery Journey series.

## Architecture

The monolithic codebase has been separated into modular concerns:

*   **`master_template.html`**: The semantic HTML5 structural skeleton. It contains no embedded CSS. Brand elements (Logo, Brand Name, Copyright, QR) have been explicitly replaced with visual placeholders. Educational content remains intact as a reference placeholder.
*   **`master_variables.css`**: Centralized definitions for all design tokens (colors, font families, base dimensions).
*   **`master_components.css`**: Reusable structural blocks (panels, scaffolds, badges, user info lines).
*   **`master_styles.css`**: High-level page layout logic, grid definitions, and flexbox containers.
*   **`master_print.css`**: Media rules strictly enforcing A4 300DPI output with forced background colors.
*   **`master_illustrations.svg`**: A standalone vector library containing completely original asset recreations (Road Tracks, Picnic Basket, Fruit, Mascot, Ladybug) mapping precisely to the dimensions of the original design. 

## Usage Rules

1.  **Do NOT edit CSS files** to create new letter worksheets. The layout is locked.
2.  **Do NOT change SVG stroke widths.** All SVGs use a mathematically calculated thickness (2.5 - 3px) to ensure uniform printing.
3.  **To create a new worksheet (e.g., Letter B):**
    *   Duplicate `master_template.html`
    *   Replace the raw text payload (e.g., "Apple" -> "Ball")
    *   Replace the specific SVG blocks inside the grid columns with new matching SVGs (e.g., swap the Apple SVG for a Ball SVG).
