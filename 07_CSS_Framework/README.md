# Worksheet Wonder: Modular CSS Framework

This directory contains the immutable, production-ready CSS Framework for the Worksheet Wonder publishing engine. 

## 🏗️ Architecture

The framework is strictly decoupled to prevent CSS bloat and duplication when generating thousands of worksheets across different subjects (Alphabet, Math, Shapes, CVC). 

Instead of writing specific CSS for a "Letter B Worksheet," developers use this universal framework.

### File Responsibilities
1.  **`master_variables.css`**: The core DNA. Every color, font, and spacing value is stored here as a CSS variable (e.g., `--color-primary`, `--hw-row-height`). If you need to re-theme the entire platform, you only change this file.
2.  **`master_typography.css`**: Locks the fonts to `Fredoka` and `Nunito`. It prevents arbitrary font sizing, ensuring kindergarten-appropriate legibility (e.g., locking tracing text precisely to `34pt`).
3.  **`master_layout.css`**: Defines the physical A4 canvas bounds and a flexible 12-column grid (`.col-6`, `.col-4`) for arranging content blocks logically without overlap.
4.  **`master_components.css`**: Reusable UI widgets like `.panel`, `.ws-header`, and vocabulary cards. 
5.  **`master_handwriting.css`**: The mathematical engine that generates the 3-line educational guides (top, dashed mid, bottom) and positions the trace letters perfectly on the baseline.
6.  **`master_utilities.css`**: Tailwind-style atomic classes (`.flex`, `.mt-sm`, `.text-center`) for tiny layout adjustments in the HTML without writing new CSS.
7.  **`master_print.css`**: Media queries strictly enforcing A4 boundaries, 0px margins, and perfect background color rendering in PDF generators.

## 🚀 How to Extend (Future Developers)
*   **Do NOT** add specific subject classes (e.g., `.apple-image` or `.math-equation`).
*   **DO** add structural components (e.g., `.fraction-container` or `.matching-game-grid`) inside `master_components.css` using the existing spacing and color variables.
*   **DO** use `master_utilities.css` in your HTML JSON injector templates to arrange data dynamically.
