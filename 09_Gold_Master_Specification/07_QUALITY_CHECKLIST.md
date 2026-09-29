# 07. Quality Assurance Checklist

Before a generated PDF can be published to the Worksheet Wonder commercial portal, it must pass 100% of this automated/manual checklist.

## Section 1: Page Geometry
- [ ] Document size is exactly 210 x 297 mm.
- [ ] 15 mm margins are respected on all four sides. No edge bleeding.
- [ ] 8 mm padding exists perfectly between all horizontal sections.
- [ ] No content overflows the `.page-wrapper`.

## Section 2: Handwriting Engine
- [ ] Tracing letters touch the Top line (if Ascender/Caps) or Midline (if Standard).
- [ ] Tracing letters rest perfectly on the Baseline. No floating letters.
- [ ] Starting dots (2.5 mm) are present on every tracing row.
- [ ] The final Independent Writing row is completely empty except for starting dots.

## Section 3: Illustrations
- [ ] All 3 Hero Vocabulary illustrations are loaded successfully (no broken SVGs).
- [ ] Stroke widths on all SVGs visually match the 3.5px standard.
- [ ] The Colouring Section illustration is an `_outline` SVG (no solid fills).
- [ ] There are no pure black `#000000` strokes anywhere on the page.

## Section 4: Typography & Content
- [ ] Fredoka and Nunito fonts have rendered properly (no fallback serif fonts).
- [ ] Phonics matching is correct (e.g., 'Apple' for A, 'Bear' for B).
- [ ] The Mini Review question matches the target letter.

## Section 5: Print Quality
- [ ] PDF exports at 300 DPI.
- [ ] No browser UI artifacts (URLs, Dates, Print buttons) are visible on the PDF.
- [ ] PDF file size is under 2 MB for fast digital distribution.
