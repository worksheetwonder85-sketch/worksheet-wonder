# Gold Master: Typography Specification

Choosing fonts for 4–6 year olds requires balancing extreme legibility with a joyful aesthetic. Standard adult fonts (like Arial or Times) are too rigid, while overly "fun" fonts (like Comic Sans) lack the structural integrity required for teaching proper letterforms (e.g., single-story 'a' and 'g').

## 1. Font Families
*   **Primary Display (Titles & Headers):** `Outfit` or `Fredoka`
    *   *Role:* Used for all structural headings. It is rounded, friendly, yet highly geometric and modern.
*   **Secondary Body (Instructions & Words):** `Nunito`
    *   *Role:* Used for vocabulary words and parent tips. Nunito is incredibly readable, soft, and utilizes the correct infant letterforms for 'a' and 'g'.
*   **Tracing / Handwriting (The Grid):** Custom SVG / CSS Dashed Fonts
    *   *Role:* Standard web fonts do not align perfectly with 3-line educational grids. All tracing dots and stroke-order numbers will be rendered via precisely calculated SVG paths or specialized CSS tracking to ensure the stroke mechanics are flawless.

## 2. Typographic Hierarchy & Sizing

| Element | Font Family | Size (pt) | Weight | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Worksheet Title / Meta** | `Fredoka` | 10pt | 600 | Small enough to stay out of the child's way; clear enough for the teacher. |
| **Section Headings** | `Fredoka` | 14pt | 700 | Provides clear visual compartmentalization for the page zones. |
| **Parent Tip / Instructions** | `Nunito` | 11pt | 600 | Easy for parents to read quickly while leaning over a desk. |
| **Vocabulary Words** | `Nunito` | 16pt | 800 | Massive and bold. 4-6 year olds track words by overall shape; thick weights aid this. |
| **Big Hero Letter** | `Nunito` / SVG | 60pt | 800 | The absolute focal point of the page. |
| **Guided Tracing Letters** | `Nunito` / SVG | 36pt | 400 | Perfectly scaled to fit between the 16mm baseline/topline guides. |
| **Footer Meta** | `Nunito` | 8pt | 400 | Institutional and quiet. |

## 3. Color Usage in Typography
*   **Primary Text:** `#1E293B` (Dark Slate). Easier on the developing eye than `#000`.
*   **Stroke Order Numbers:** `#FFFFFF` text on a `#EF4444` (Red) or `#3B82F6` (Blue) circular background to draw immediate attention.
*   **Tracing Dashes:** `#94A3B8` (Muted Grey). Dark enough to see, light enough to be easily drawn over by a standard HB pencil or crayon.
