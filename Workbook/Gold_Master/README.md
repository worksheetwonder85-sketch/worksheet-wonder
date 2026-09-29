# Worksheet Wonder: GOLD MASTER PUBLISHING SYSTEM

## Overview
This directory contains the final, immutable `GOLD_MASTER.html` template that serves as the permanent publishing foundation for the Worksheet Wonder A-Z curriculum.

## Architecture
The template utilizes semantic HTML5 (`<header>`, `<main>`, `<section>`, `<footer>`) to construct the pedagogical flow: **LOOK → SAY → TRACE → WRITE → COLOUR → SUCCEED**.

The visual layout is locked via a strict CSS Grid engine, distributed across four specific modules to prevent CSS duplication:
1. `master_variables.css`: Design tokens (Colors, Fonts, Sizes).
2. `master_layout.css`: The mathematical grid enforcement.
3. `master_components.css`: Visual styling for panels and the handwriting engine.
4. `master_styles.css`: Global typography and alignment.
5. `master_print.css`: A4 print overrides and overflow prevention.

## Placeholders
The template contains NO hardcoded educational content. To generate a new letter worksheet, replace the standard Handlebars-style placeholders:
*   `{{TITLE}}`: Document title.
*   `{{UPPERCASE}}` / `{{LOWERCASE}}`: Target letter.
*   `{{WORD1}}`...: Vocabulary text.
*   `{{SVG1}}`...: SVG graphics for the "Say" section.
*   `{{COLORING_SVG}}`: The black-and-white decompression SVG.
*   `{{PARENT_TIP}}`: Contextual tip for the parent/educator.

**Note on SVG Injection:** Ensure SVG vector paths replace the generic `placeholder-svg` tags, while maintaining the fixed grid boxes defined in `master_layout.css`.
