# Gold Master: Spacing & Grid Specification

The primary enemy of a Kindergarten worksheet is "visual clutter." When a page is cramped, a child's cognitive load spikes, and they lose focus. The Gold Master utilizes a strict mathematical grid to guarantee generous whitespace (negative space).

## 1. The Canvas & Margins
*   **Page Size:** A4 Portrait (210mm × 297mm).
*   **Hardware Safe Margins (Padding):** 
    *   Top/Bottom: 15mm
    *   Left/Right: 15mm
*   **Usable Canvas:** 180mm × 267mm.

## 2. The Modular Block System
Content is grouped into "Blocks" with defined vertical gaps. This creates a rhythmic pacing as the child moves down the page.

*   **Macro Whitespace (Between Zones):** `8mm`. This gap acts as a "palate cleanser," telling the brain one task is over and a new one is beginning.
*   **Micro Whitespace (Inside Zones):** `4mm` to `5mm` gaps between related elements (e.g., between an SVG illustration and its vocabulary word).

## 3. Handwriting Grid Measurements (Crucial)
The 3-line handwriting system is the core engine of the worksheet. It must be perfectly sized for 4–6 year old motor control.

*   **Total Row Height (Top line to Baseline):** `16mm`. 
    *   *Why:* 16mm is the industry standard for Kindergarten/Grade 1 transitions. It is large enough for gross motor forgiveness, but small enough to begin refining fine motor skills.
*   **Line Distribution:**
    *   `Top Guideline`: Solid, `1.5px` thickness, `#94A3B8`.
    *   `Middle Guideline`: Dashed (`stroke-dasharray: 4 4`), `1.5px` thickness, `#CBD5E1`. Positioned exactly at 50% (8mm).
    *   `Baseline`: Solid, `2.5px` thickness (thicker to anchor the letters), `#475569`.
*   **Row-to-Row Spacing (Line Gap):** `8mm`. 
    *   *Why:* Children write with sweeping, uncontrolled descenders (like the tail of a 'g' or 'y'). An 8mm gap ensures the descenders from row 1 do not crash into the ascenders of row 2.

## 4. Vertical Space Allocation Budget (Approximate)
1.  Header: `10mm`
2.  Zone 1 (Hero + Vocab): `50mm`
3.  Zone 2 (Trace 5 Rows): `16mm * 5` = `80mm` + inter-row gaps = `112mm`
    *   *Wait, 5 rows of tracing + 3 rows of writing is 8 rows. 8 rows * (16mm height + 8mm gap) = 192mm. This is too tight for A4 alongside other elements.*
    *   *Adjustment for Gold Master:* We will compress the row height slightly to `14mm` and the gap to `6mm`. Total row footprint = 20mm. 8 rows = `160mm`. This perfectly leaves 107mm for the Header, Hero, SVGs, and Footer.
4.  Zone 3 (Write 3 Rows): `60mm`
5.  Zone 4 (Colour + Footer): `37mm`
