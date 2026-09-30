# WORKSHEET WONDER
## ILLUSTRATION BIBLE — PART 3
### Environmental Settings, Functional Assets & Decorative Element Standards

---

```
══════════════════════════════════════════════════════════════

                 Worksheet Wonder Documentation

══════════════════════════════════════════════════════════════

  Document ID:         WW-IB-003

  Document Name:       Worksheet Wonder Illustration Bible — Part 3

  Version:             1.0

  Status:              Approved

  Owner:               Worksheet Wonder

  Author:              Senior Art Director

  Category:            Illustration Standards

  Last Updated:        10 July 2026

  Next Review:         10 January 2027

  Related Documents:   WW-DB-001  (Design Bible)
                       WW-MC-001  (Master Curriculum)
                       WW-IB-001  (Illustration Bible — Part 1)
                       WW-IB-002  (Illustration Bible — Part 2)
                       WW-PS-100  (Production System)

══════════════════════════════════════════════════════════════
```

> **This is Part 3 of 3 of the Worksheet Wonder Illustration Bible.**
> Parts 1 and 2 MUST be read before this document.
> This document completes the system by defining environmental settings,
> structural graphic assets, and every decorative and functional element
> used across the catalogue.

---

## TABLE OF CONTENTS

| # | Category | Est. Assets |
|---|----------|------------|
| 01 | School | 60–80 |
| 02 | Classroom | 80–100 |
| 03 | Library | 50–70 |
| 04 | Playground | 50–70 |
| 05 | Science | 80–100 |
| 06 | Math | 80–100 |
| 07 | Space | 70–90 |
| 08 | Ocean | 60–80 |
| 09 | Fantasy | 70–90 |
| 10 | Buildings | 60–80 |
| 11 | Furniture | 60–80 |
| 12 | Community Helpers | 60–80 |
| 13 | Music | 60–80 |
| 14 | Sports | 70–90 |
| 15 | Festival Decorations | 80–100 |
| 16 | Borders | 60–80 |
| 17 | Frames | 40–60 |
| 18 | Patterns | 40–60 |
| 19 | Icons | 100–130 |
| 20 | Badges | 60–80 |
| 21 | Certificates | 20–30 |
| 22 | Reward Stickers | 60–80 |
| 23 | Background Elements | 60–80 |
| 24 | Scene Templates | 40–60 |
| 25 | Master Asset Inventory | — |
| — | Version History | — |
| — | Dependencies | — |
| — | Future Revisions | — |
| — | Approval Page | — |
| **TOTAL** | | **~1,540–2,020** |

---

## SYSTEM NOTES FOR PART 3

### What This Part Covers

Part 1 (WW-IB-001) defined the foundational visual language — style rules, shape language, character anatomy, SVG coding standards, and technical specifications.

Part 2 (WW-IB-002) defined the character and subject illustration library — living subjects and objects that appear as primary content in worksheet activities.

**Part 3 defines everything else:**
- The environments in which characters exist (settings)
- The objects that fill those environments (props and furniture)
- The professional and community roles (community helpers)
- The structural graphic assets used in every worksheet (borders, frames, icons, badges, certificates)
- The decorative and motivational elements (stickers, reward elements, patterns)
- The compositional tools (scene templates, backgrounds)

### Cross-Reference Requirement

Every asset defined in this document must comply with:
- Line weight hierarchy: WW-IB-001 §11
- SVG coding standards: WW-IB-001 §12
- Layer naming standards: WW-IB-001 §13
- File naming standards: WW-IB-001 §14
- B&W printing standards: WW-IB-001 §15
- Colour standards: WW-IB-001 §16
- Accessibility: WW-IB-001 §17

---

---

# CATEGORY 01 — SCHOOL

## 1.1 Purpose

School exterior and campus illustrations provide contextual settings for the beginning of worksheets, cover pages, school-themed activities, back-to-school bundles, and social studies units on community. The school asset library establishes the physical world in which the Worksheet Wonder educational experience takes place.

## 1.2 Design Standards

| Attribute | Specification |
|-----------|---------------|
| **Architectural style** | Generic, culturally neutral school building — not specific to any national style; brick or painted wall texture suggested only with L4 strokes |
| **Colour** | B&W: varied tonal zones; Colour: warm brick red, cream walls, blue roof, green lawn |
| **Scale** | Always scaled consistently — child characters appear at correct relative size to building |
| **Perspective** | Isometric (slight angle, 2.5D) for environment scenes; flat front elevation for icon use |
| **Friendliness** | Rounded window corners; slightly curved roofline; never imposing or institutional |
| **Signage** | Generic "School" or "Worksheet Wonder Academy" signage; no real institution names |

## 1.3 SVG Structure

```xml
<svg viewBox="0 0 400 300" role="img" aria-labelledby="school-ext-title">
  <title id="school-ext-title">School building exterior</title>
  <g id="school--sky">         <!-- background colour fill -->
  <g id="school--ground">      <!-- lawn, path, ground plane -->
  <g id="school--building">    <!-- main wall body -->
    <g id="school--roof">
    <g id="school--windows">   <!-- modular: each window is a child group -->
    <g id="school--door">      <!-- modular: can swap open/closed door -->
    <g id="school--sign">
  <g id="school--surrounds">   <!-- trees, fencing, flagpole, path -->
  <g id="school--foreground">  <!-- foreground overlay elements -->
```

**ViewBox standards:**
| Asset Type | ViewBox |
|-----------|---------|
| School exterior full scene | `0 0 400 300` |
| School exterior icon | `0 0 64 64` |
| School gate / entrance only | `0 0 200 200` |
| Aerial/top-down layout | `0 0 400 400` |

## 1.4 Asset Naming Convention

```
WW--SCHOOL--[asset-type]--[variant]--[size].svg

ASSET TYPES:
  exterior     = full building exterior
  entrance     = gate and entrance area
  playground   = playground area (see Category 04 for detail)
  icon         = simplified icon version
  aerial       = top-down school map

VARIANTS:
  front | angle | night | winter | summer | decorated

Examples:
  WW--SCHOOL--exterior--front--xl.svg
  WW--SCHOOL--exterior--autumn--xl.svg
  WW--SCHOOL--entrance--front--lg.svg
  WW--SCHOOL--icon--plain--sm.svg
```

## 1.5 Folder Location

```
assets/svg/environments/school/
```

## 1.6 Asset Reuse Strategy

- Building body is a single reusable base `<g>` element — seasonal variants swap only the `school--surrounds` group
- Windows are modular: swap to lit/unlit for day/night variants
- Door group is modular: open/closed/decorated variants
- This base saves re-drawing the building for every season or context variant

## 1.7 Printing Considerations

- Full exterior scenes: use as page header illustration only, never as background behind text (contrast risk)
- Icon version (64×64): safe for all uses including in-line with text
- Ensure no element in the scene is thinner than L5 (0.75px) — fine detail will disappear on standard laser print
- Night variant: use L4 window glow suggestion only; avoid true "dark background" — causes toner overuse

## 1.8 Accessibility

- All school scenes must include `<title>` and `<desc>` elements in SVG
- Ensure school building silhouette reads as identifiable at 50% zoom
- Do not rely on colour alone to distinguish building zones (use tonal contrast or linework)

## 1.9 Commercial Guidelines

- School buildings must be culturally neutral — no cross, crescent, Star of David, or other religious symbol incorporated into architecture
- No real school name, address, or logo depicted
- No depictions of security-related features (fences with barbed wire, surveillance cameras, locked gates)

## 1.10 Estimated Asset Count: 60–80 assets

---

---

# CATEGORY 02 — CLASSROOM

## 2.1 Purpose

Classroom illustrations are the most frequently used environmental assets in the catalogue. They appear in nearly every subject area as the context for learning activities, teacher guide illustrations, and instructional page headers.

## 2.2 Design Standards

| Attribute | Specification |
|-----------|---------------|
| **Perspective** | Slight 3/4 angle (student's eye view, as if seated at a desk looking toward the front) |
| **Elements** | Whiteboard/blackboard; teacher's desk; student desks; bookshelves; window (optional); bulletin board |
| **Scale** | All furniture scaled for both teacher (adult) and student (child) characters to appear at correct relative size |
| **Orderliness** | Classroom is always tidy and inviting — no mess, no chaos |
| **Bulletin board** | Generic "well done" display style — no specific student names; abstract artwork or geometric shapes on display |
| **Clock** | On wall; shows a pedagogically relevant time (e.g., 9:00 for start of school) |
| **Plants** | 1–2 small potted plants visible for warmth |

## 2.3 SVG Structure

```xml
<svg viewBox="0 0 500 350" role="img" aria-labelledby="classroom-title">
  <title id="classroom-title">Classroom interior</title>
  <g id="classroom--walls">        <!-- back wall, side wall, ceiling line -->
  <g id="classroom--floor">        <!-- floor plane with optional rug -->
  <g id="classroom--board">        <!-- whiteboard/blackboard — modular content -->
  <g id="classroom--teacher-zone"> <!-- teacher desk, chair -->
  <g id="classroom--student-zone"> <!-- student desks — modular count: 4, 6, 8, 12 -->
  <g id="classroom--storage">      <!-- bookshelves, cubbies, trays -->
  <g id="classroom--walls-deco">   <!-- bulletin board, clock, posters -->
  <g id="classroom--windows">      <!-- windows with outside view suggestion -->
  <g id="classroom--characters">   <!-- placeholder group for character insertion -->
```

## 2.4 Classroom Object Asset Library

Individual classroom objects are stored as standalone SVGs for modular use:

| Object | Variants | Est. Count |
|--------|---------|-----------|
| Whiteboard (blank) | Clean; with writing; with drawing | 3 |
| Blackboard (blank) | Clean; with chalk writing | 2 |
| Teacher's desk | Front view; angle view | 2 |
| Student desk (single) | Empty; with book; with pencil case | 3 |
| Student desk (pair, side by side) | Empty; occupied | 2 |
| Bookshelf | Half-full; full; with coloured spines | 3 |
| Bulletin board | Blank; with work displayed; with banner | 3 |
| Globe | Standard; on stand | 2 |
| Pencil holder | On desk; wall-mounted | 2 |
| Ruler (on desk) | Horizontal; diagonal | 2 |
| Clock | Round face; digital variant | 2 |
| Pot plant | Small cactus; small leafy | 2 |
| Storage bin / cubby | Open; with label | 2 |
| Recycling bin | Standard | 1 |
| Hand sanitiser stand | Standard (post-2020 standard) | 1 |

**Total classroom objects: ~32 individual assets**

## 2.5 Asset Naming Convention

```
WW--CLASSROOM--[asset]--[variant]--[size].svg

Examples:
  WW--CLASSROOM--scene--full--xl.svg
  WW--CLASSROOM--whiteboard--blank--md.svg
  WW--CLASSROOM--desk-student--empty--md.svg
  WW--CLASSROOM--bookshelf--full--md.svg
  WW--CLASSROOM--globe--onstand--sm.svg
```

## 2.6 Folder Location

```
assets/svg/environments/classroom/
assets/svg/environments/classroom/objects/
```

## 2.7 Asset Reuse Strategy

- Student desk module: create once; multiply within scene using SVG `<use>` element
- Wall decoration group: swap in/out for seasonal or themed variants
- Character placeholder `<g id="classroom--characters">`: add characters from WW-IB-002 Category 07–09 without redrawing the room
- Board content group: swap blank / writing / diagram versions per worksheet theme

## 2.8 Printing Considerations

- Full classroom scene: use as page header only; minimum height 60mm on A4
- Individual objects: safe at any size above 12mm × 12mm
- Reduce interior linework weight for smaller print sizes (below 30mm): suppress L4 and L5 layers

## 2.9 Accessibility

- Classroom scene: alt text describes the general setting ("A bright classroom with desks and a whiteboard")
- Individual objects: each has descriptive `<title>` ("Student desk, empty")
- Clock face: always includes both hand positions AND a text label ("9:00") for time-telling accessibility

## 2.10 Commercial Guidelines

- No visible brand logos on any classroom equipment
- No phone or tablet devices depicted in preschool/KG classrooms (age-appropriate)
- Tablets may appear on desks in Grade 3+ content as educational tools
- No real curriculum materials from other publishers displayed on bulletin boards

## 2.11 Estimated Asset Count: 80–100 assets (scenes + objects combined)

---

---

# CATEGORY 03 — LIBRARY

## 3.1 Purpose

Library settings are used in literacy units, comprehension activities, reading promotion worksheets, and library skills activities. The library is one of the warmest and most aspirational settings in the WW environment catalogue.

## 3.2 Design Standards

| Attribute | Specification |
|-----------|---------------|
| **Atmosphere** | Warm, welcoming, cosy — the opposite of cold or institutional |
| **Bookshelves** | Tall, full, colourful spines (B&W: varied tonal rows of books) |
| **Lighting** | Warm reading lamps; large window with natural light |
| **Reading corners** | Beanbags, cushions, low comfortable seating |
| **Organisation** | Shelves labelled with genre/section signs (generic: "Fiction", "Animals", "Science") |
| **Desk** | Librarian's desk at entrance; with computer monitor (closed lid or screen-off) |

## 3.3 SVG Structure

Same layered approach as Classroom (Category 02). Key groups:

```xml
<g id="library--shelves">       <!-- tall bookshelves — modular units -->
<g id="library--books">         <!-- book rows per shelf — modular -->
<g id="library--seating">       <!-- chairs, beanbags, reading nook -->
<g id="library--desk">          <!-- librarian's desk -->
<g id="library--lighting">      <!-- lamp, window light overlay -->
<g id="library--signage">       <!-- shelf labels, "Quiet Please" sign -->
<g id="library--characters">    <!-- placeholder -->
```

## 3.4 Individual Library Assets

| Asset | Est. Count |
|-------|-----------|
| Bookshelf (full) — front view | 3 |
| Book (closed, standing) — varied spine colours/widths | 12 |
| Book (open, flat) — reading position | 2 |
| Book stack (3–5 books) | 3 |
| Library card | 1 |
| "Shhh / Quiet Please" sign | 2 |
| Reading nook scene | 2 |
| Librarian's desk | 2 |
| Library scene (full) | 3 |

## 3.5 Asset Naming Convention

```
WW--LIBRARY--[asset]--[variant]--[size].svg

Examples:
  WW--LIBRARY--scene--full--xl.svg
  WW--LIBRARY--bookshelf--full--lg.svg
  WW--LIBRARY--book--standing-blue--sm.svg
  WW--LIBRARY--readingnook--beanbag--md.svg
```

## 3.6 Folder Location

```
assets/svg/environments/library/
```

## 3.7 Printing, Accessibility, Commercial Guidelines

- Book spines: in B&W, use alternating tones (#f0f0f0, #cccccc, #888888, #555555) to suggest variety
- Accessibility: "Quiet Please" signs must have text as actual SVG `<text>` not just depicted as image
- No real book titles or authors depicted; use abstract decorative spine designs only

## 3.8 Estimated Asset Count: 50–70 assets

---

---

# CATEGORY 04 — PLAYGROUND

## 4.1 Purpose

Playground scenes appear in SEL worksheets (cooperation, sharing, friendship), physical education, maths (spatial concepts, sorting by use), and descriptive writing activities. They are among the most joyful settings in the catalogue.

## 4.2 Design Standards

| Attribute | Specification |
|-----------|---------------|
| **Equipment** | Slide, swings, climbing frame, seesaw, roundabout, sandpit, benches |
| **Safety design** | All equipment has rounded edges, protective surfacing suggested below items |
| **Ground** | Grass + rubberised safety surface shown as tonal zones |
| **Characters** | Playground scenes are designed to accommodate WW-IB-002 Category 07 (Kids) character insertion |
| **Time of day** | Default daytime; bright sky |

## 4.3 Playground Equipment Library

| Equipment | Variants |
|-----------|---------|
| Slide | Standard; curved; with platform |
| Swings | 2-swing set; 3-swing set; with child |
| Climbing frame | Standard dome; bridge variant |
| Seesaw | Empty; with children (placeholder seats) |
| Roundabout | Standard |
| Sandpit | Empty; with toys |
| Bench | Standard |
| Basketball hoop | With backboard |
| Hopscotch markings | Numbered 1–10 |
| Painted number/alphabet grid | Floor grid |

## 4.4 Asset Naming Convention

```
WW--PLAYGROUND--[asset]--[variant]--[size].svg

Examples:
  WW--PLAYGROUND--scene--full--xl.svg
  WW--PLAYGROUND--slide--standard--md.svg
  WW--PLAYGROUND--swings--3seat--md.svg
  WW--PLAYGROUND--hopscotch--numbered--lg.svg
```

## 4.5 Folder Location

```
assets/svg/environments/playground/
```

## 4.6 Asset Reuse, Printing, Accessibility, Commercial Notes

- Equipment is modular: assemble scenes by combining individual equipment SVGs over a background
- All equipment must include clear `<title>` labels ("Slide playground equipment")
- Safety surfacing below equipment is a separate layer — can be shown or hidden
- No brand names on any playground equipment

## 4.7 Estimated Asset Count: 50–70 assets

---

---

# CATEGORY 05 — SCIENCE

## 5.1 Purpose

Science illustration assets support the full Worksheet Wonder science curriculum from Preschool (living/non-living) through Grade 8 (cells, atoms, circuits). This is one of the most content-diverse categories in the library — spanning life science, physical science, earth science, and environmental science.

## 5.2 Design Standards

| Attribute | Specification |
|-----------|---------------|
| **Accuracy** | Scientific diagrams must be anatomically/conceptually correct at the grade level targeted |
| **Labels** | Label lines use L5 weight; horizontal label text only (never rotated labels) |
| **Arrows** | Direction arrows use solid arrowhead (filled triangle tip); consistent L3 shaft weight |
| **Cross-sections** | Interior sections shown with lighter fill than exterior; boundary lines L2 |
| **Magnification** | Suggest scale with a circular "zoom lens" border effect for microscopic views |
| **Diagram style** | Clean, uncluttered; minimum detail needed for educational clarity |
| **Safety** | No flames, electrical sparks, or chemical hazards depicted in an exciting/attractive way |

## 5.3 Science Asset Library — Sub-categories

### Life Science

| Asset Group | Key Items | Est. Count |
|-------------|-----------|-----------|
| Plant parts | Root, stem, leaf, flower, fruit, seed — individual and labelled full plant | 10–14 |
| Animal cell | Labelled diagram (nucleus, membrane, cytoplasm, etc.) | 2–3 |
| Plant cell | Labelled diagram (cell wall, chloroplast, vacuole, etc.) | 2–3 |
| Life cycles | Butterfly, frog, plant, chicken — 4-stage sequences | 12–16 |
| Human body | Outline front/back; organ overlays (heart, lungs, skeleton, muscles) | 10–14 |
| Senses | Eye, ear, nose, tongue, skin — labelled diagram | 5–7 |
| Habitats | Forest, desert, ocean, arctic, rainforest — labelled scene | 5–7 |
| Food webs/chains | 3-level and 5-level arrow diagrams | 4–6 |

### Physical Science

| Asset Group | Key Items | Est. Count |
|-------------|-----------|-----------|
| Simple machines | Lever, pulley, wheel+axle, inclined plane, wedge, screw | 6–8 |
| Magnets | Bar magnet with field lines; horseshoe magnet; poles labelled | 4–6 |
| States of matter | Solid/liquid/gas particle diagrams | 3 |
| Light and shadow | Sun ray diagram; shadow diagram | 4–6 |
| Circuits | Simple circuit with battery, bulb, switch — open and closed | 4–6 |
| Forces | Push/pull arrows; gravity diagram; friction diagram | 6–8 |
| Sound waves | Wave diagram with amplitude/frequency labels | 2–3 |

### Earth Science

| Asset Group | Key Items | Est. Count |
|-------------|-----------|-----------|
| Rock cycle | Cyclic diagram (igneous/sedimentary/metamorphic) | 2 |
| Water cycle | Full labelled cycle diagram | 2 |
| Layers of Earth | Cross-section (crust, mantle, outer core, inner core) | 2 |
| Weather systems | Cloud types (cumulus, stratus, cirrus, cumulonimbus) | 4–6 |
| Solar system | Planets in orbital order; individual planet icons | 10–12 |
| Moon phases | 8-phase sequence | 1 (8-panel strip) |

## 5.4 SVG Structure for Science Diagrams

```xml
<!-- Standard labelled diagram structure -->
<svg viewBox="0 0 400 300" role="img" aria-labelledby="sci-diag-title">
  <title id="sci-diag-title">[Diagram description]</title>
  <desc>[Full text description of diagram content]</desc>
  <g id="diagram--background">    <!-- white base; no texture -->
  <g id="diagram--subject">       <!-- the main subject illustration -->
    <g id="diagram--subject-body">
    <g id="diagram--subject-detail">
    <g id="diagram--subject-crosssection">  <!-- if applicable -->
  <g id="diagram--labels">        <!-- all label lines and text -->
    <g id="diagram--label-lines"> <!-- L5 lines from part to label -->
    <g id="diagram--label-text">  <!-- text — SVG <text> elements -->
  <g id="diagram--arrows">        <!-- process arrows if applicable -->
  <g id="diagram--legend">        <!-- colour key if applicable -->
```

**Important:** All label text in science diagrams must be actual SVG `<text>` elements — NEVER rasterised or converted to outlines. This ensures screen reader accessibility and allows translation for localised editions.

## 5.5 Asset Naming Convention

```
WW--SCI--[domain]--[subject]--[variant]--[size].svg

DOMAIN:  life | phys | earth | env
VARIANT: labelled | unlabelled | blank-labels | colour | bw

Examples:
  WW--SCI--life--plantparts--labelled--lg.svg
  WW--SCI--life--lifecycle-butterfly--4stage--xl.svg
  WW--SCI--phys--circuit-simple--closed--md.svg
  WW--SCI--earth--watercycle--labelled--xl.svg
  WW--SCI--earth--layers--crosssection--lg.svg
```

## 5.6 Folder Location

```
assets/svg/diagrams/science/
  life/
  physical/
  earth/
  environmental/
```

## 5.7 Asset Reuse Strategy

- **Blank-label variant**: produce every labelled diagram in a blank-labels version (label lines present, text boxes empty) for "label the diagram" worksheet activities — this doubles the usable asset count without redesign
- **Colour/BW split**: produce colour version first; BW version is a separate export with tonal fills replacing colour fills
- **Modular anatomy**: body outline is one SVG; each organ/system is a separate overlay `<g>` that can be shown/hidden

## 5.8 Printing Considerations

- Science diagrams are typically used as the primary content of a full worksheet — not as decorative elements
- Minimum label text size: 10pt equivalent in the SVG coordinate system
- Label lines: minimum L5 (0.75px); dash pattern permitted for leader lines: `stroke-dasharray="4 2"`
- Cross-section fills: must maintain 30% minimum tonal difference from adjacent zone

## 5.9 Accessibility

- Every science diagram has a full `<desc>` element describing the content for screen readers
- Colour-coded diagrams (e.g., food webs) must also use shape or pattern differentiation
- All label text is live SVG text — never traced to outlines

## 5.10 Commercial Guidelines

- All scientific content must be reviewed against a current authoritative source before publication
- Evolutionary diagrams must show accurate phylogenetic relationships — no "great chain of being" style ladders
- Climate and environmental content must reflect current scientific consensus

## 5.11 Estimated Asset Count: 80–100 primary assets + 80–100 blank-label variants = ~160–200 total

---

---

# CATEGORY 06 — MATH

## 6.1 Purpose

Math illustration assets are the most systematic category in the library. They span concrete manipulative representations (blocks, counters, rods), abstract mathematical tools (number lines, grids, graphs), and visual problem contexts (word problem scenes). Every asset is designed to be pedagogically precise.

## 6.2 Design Standards

| Attribute | Specification |
|-----------|---------------|
| **Precision** | All geometric figures are mathematically exact using SVG primitives |
| **Grid alignment** | All maths diagrams align to an implied 10px grid within the SVG coordinate space |
| **Number line** | Horizontal baseline at consistent y-position; tick marks evenly spaced using SVG `<line>` elements; numbers as SVG `<text>` |
| **Graph axes** | Clean, right-angle axes; no decorative embellishment; simple arrowheads |
| **Manipulatives** | Concrete objects (cubes, counters) are rounded and tactile-looking — not flat geometric shapes |
| **Clarity** | No decorative element may visually compete with the mathematical content |

## 6.3 Math Asset Library — Sub-categories

### Number & Counting

| Asset | Variants | Est. Count |
|-------|---------|-----------|
| Ten-frame (empty) | 1×10; 2×5 orientation | 2 |
| Ten-frame (filled) | Filled 1–10; with counters | 10 |
| Twenty-frame | Empty; various fills | 4 |
| Hundred chart | Blank; numbered 1–100; shaded multiples | 3 |
| Number line | 0–10; 0–20; 0–100; negative numbers | 6 |
| Counters (circles) | Single; group of 5; group of 10 | 8 |
| Base-10 blocks | Unit cube; rod (10); flat (100); block (1000) | 4 |
| Tally marks | Groups of 5; blank tally table | 3 |
| Place value chart | Ones/Tens/Hundreds/Thousands; decimal | 4 |

### Operations

| Asset | Variants | Est. Count |
|-------|---------|-----------|
| Addition visual (part-part-whole) | Blank; example-filled | 4 |
| Subtraction visual (crossing out) | Blank; example | 4 |
| Multiplication array | 2×3; 3×4; 4×5; 5×6 | 6 |
| Area model | Blank grid; labelled | 4 |
| Bar model (Singapore) | 1-bar; 2-bar comparison; 3-bar | 6 |
| Number bond | 2-bond; 3-bond | 4 |

### Fractions & Decimals

| Asset | Variants | Est. Count |
|-------|---------|-----------|
| Fraction circles | Halves through tenths; coloured and outline | 18 |
| Fraction bars | Halves through tenths | 10 |
| Fraction strips (comparison) | Side-by-side 3-strip set | 3 |
| Decimal grid | Tenths; hundredths | 2 |
| Number line with fractions | Halves; quarters; eighths | 3 |

### Measurement

| Asset | Variants | Est. Count |
|-------|---------|-----------|
| Ruler (30cm, metric) | Blank; marked | 2 |
| Measuring tape | Coiled; extended | 2 |
| Weighing scales | Balance scale; kitchen scale | 2 |
| Measuring jug | 250ml; 500ml; 1L; 2L — empty and marked | 8 |
| Thermometer | Celsius; Fahrenheit; dual | 3 |
| Clock face | Blank (no hands); with standard hands; digital | 3 |
| Protractor | 180°; 360° | 2 |
| Set square | Standard | 1 |

### Geometry

| Asset | Variants | Est. Count |
|-------|---------|-----------|
| Dot grid paper | Square dots; isometric dots | 2 |
| Square grid | 5×5; 10×10; 20×20; blank | 4 |
| Coordinate grid | 1st quadrant; 4 quadrants | 2 |
| 2D shapes (labelled) | All standard shapes + angles marked | 12 |
| 3D shapes (wireframe) | Cube, cylinder, cone, sphere, pyramid, prism | 6 |
| Angles (labelled) | Acute, right, obtuse, straight, reflex | 5 |
| Compass directions | N/S/E/W grid | 2 |
| Maps and grids | Simple grid map with key | 2 |

### Data & Statistics

| Asset | Variants | Est. Count |
|-------|---------|-----------|
| Bar graph (blank) | Vertical; horizontal | 2 |
| Pictograph (blank) | With key legend | 2 |
| Tally chart (blank) | 3-column; 4-column | 2 |
| Pie chart (blank) | 2-way; 3-way; 4-way | 3 |
| Line graph (blank) | Single axis | 1 |
| Venn diagram | 2-circle; 3-circle | 2 |
| Carroll diagram | 2×2; 2×3 | 2 |

## 6.4 SVG Structure for Math Assets

```xml
<!-- Number line example -->
<svg viewBox="0 0 400 60" role="img" aria-labelledby="numline-title">
  <title id="numline-title">Number line from 0 to 10</title>
  <g id="numline--baseline">
    <line x1="20" y1="30" x2="380" y2="30" stroke="#333" stroke-width="2"/>
  </g>
  <g id="numline--ticks">
    <!-- evenly spaced <line> elements for each tick -->
  </g>
  <g id="numline--labels">
    <!-- <text> elements for each number label -->
  </g>
  <g id="numline--markers">
    <!-- optional: jump arcs, highlighted points -->
  </g>
```

**Critical rule:** All maths grid lines use L4 weight (1.0px) and #cccccc fill. Student answer/activity space must remain visually distinct from the diagram framework.

## 6.5 Asset Naming Convention

```
WW--MATH--[domain]--[asset]--[variant]--[size].svg

DOMAIN:  num | ops | frac | meas | geo | data

Examples:
  WW--MATH--num--tenframe--empty--md.svg
  WW--MATH--num--tenframe--filled8--md.svg
  WW--MATH--frac--circle--quarters--md.svg
  WW--MATH--meas--clock--blank--md.svg
  WW--MATH--geo--grid--10x10--lg.svg
  WW--MATH--data--bargraph-blank--vertical--lg.svg
```

## 6.6 Folder Location

```
assets/svg/diagrams/math/
  number/
  operations/
  fractions/
  measurement/
  geometry/
  data/
```

## 6.7 Asset Reuse Strategy

- **Blank vs. filled variants**: all data assets (graphs, charts, grids) are produced blank first, then filled variants are created by adding data layers — same base asset
- **Scaled variants**: the 10×10 grid base scales to 5×5 or 20×20 by adjusting viewBox — no redraw
- Clock face: the blank clock is the base; hand positions are a separate `<g id="clock--hands">` group that is swapped per time value

## 6.8 Printing Considerations

- All grid lines must print at the design weight — verify on lowest-quality laser setting
- Fraction shading: uses L4 hatching lines (not fills) in the B&W version to ensure print clarity and toner economy
- Number and label text: minimum 9pt equivalent; Nunito or monospace font; embedded as SVG `<text>`

## 6.9 Accessibility

- All graphs and charts include a `<desc>` element providing a data table text alternative
- No data conveyed by colour alone: bar graphs use pattern fills (diagonal lines, dots, cross-hatch) as secondary coding
- All interactive elements (student-fill grids) have ARIA regions for digital access

## 6.10 Commercial Guidelines

- No currency symbols specific to a single country on money activities — provide as customisable layer
- Measurement: provide both metric and imperial variants (or dual-labelled) for global market
- Avoid real-world prices on shopping/money worksheets

## 6.11 Estimated Asset Count: 80–100 base assets + blank/filled variants = ~160–200 total

---

---

# CATEGORY 07 — SPACE

## 7.1 Purpose

Space illustrations serve the science curriculum (solar system, Earth in space, astronomy basics) from Grade 2 onwards, and appear as a high-engagement theme for maths and literacy activities across all ages.

## 7.2 Design Standards

| Attribute | Specification |
|-----------|---------------|
| **Background** | Space backgrounds use deep navy/black fill (#0a0a1a in colour; #333333 in B&W dark mode); stars as small white dots of varied sizes |
| **Planets** | Spherical forms; each planet has distinctive rings/features while maintaining simplified style |
| **Scale accuracy** | Relative size is suggested (Jupiter much larger than Mercury) but not to true scale |
| **Spacecraft** | Friendly, rounded designs — not military or weapon-bearing |
| **Astronaut** | Human figure in spacesuit; WW character proportions; diverse skin tone visible through helmet visor |
| **Black & White rule** | Space scenes invert: dark background with white/light elements — label this in the filename |

## 7.3 Space Asset Library

| Asset Group | Items | Est. Count |
|-------------|-------|-----------|
| Solar system | Sun + 8 planets (Mercury through Neptune) — individual and in orbital scene | 10–14 |
| Moon | Full, half, crescent, new — 4 phases; detailed surface for larger views | 5–7 |
| Stars | Single star; constellation (Big Dipper); star cluster; shooting star | 6–8 |
| Spacecraft | Rocket (classic); Space shuttle; Satellite; Space station | 8–10 |
| Astronaut | Standing; floating; planting flag; waving | 6–8 |
| Space objects | Asteroid; Comet; Galaxy spiral; Nebula | 6–8 |
| Space scenes | Full solar system; Moon surface; Deep space | 4–6 |
| Planet labels | Individual planet "card" with name and key fact | 8 |
| Space background tile | Repeating star field pattern | 2–3 |

## 7.4 SVG Structure for Space Scenes

```xml
<svg viewBox="0 0 500 350" role="img" aria-labelledby="space-scene-title">
  <title id="space-scene-title">Solar system scene</title>
  <g id="space--background">    <!-- dark fill + star dots -->
  <g id="space--deep-objects">  <!-- distant galaxies, nebulae -->
  <g id="space--sun">           <!-- central sun body -->
  <g id="space--orbits">        <!-- optional orbital path rings - L5 dashed -->
  <g id="space--planets">       <!-- planet groups in orbital order -->
    <g id="space--mercury">
    <g id="space--venus">
    <!-- ... -->
  <g id="space--foreground">    <!-- spacecraft, astronaut, large asteroid -->
  <g id="space--labels">        <!-- text labels -->
```

## 7.5 Asset Naming Convention

```
WW--SPACE--[asset]--[variant]--[size].svg

VARIANT for scenes: darkbg (inverted) | lightbg (for print on white)

Examples:
  WW--SPACE--planet--jupiter--md.svg
  WW--SPACE--rocket--classic--md.svg
  WW--SPACE--scene--solarsystem--darkbg--xl.svg
  WW--SPACE--astronaut--floating--st4--md.svg
  WW--SPACE--moon--crescent--sm.svg
```

## 7.6 Folder Location

```
assets/svg/themes/space/
```

## 7.7 Printing Considerations

- **Dark background space scenes** — label explicitly as `darkbg` in filename and usage notes
- Dark background scenes require HEAVY toner coverage — not recommended as full-page background for B&W economy print
- Provide a `lightbg` (white background) variant of every space scene for standard print use
- Planet rings (Saturn): L3 weight minimum; below L3, rings disappear on home laser print

## 7.8 Accessibility

- Space scenes: all planet names as live `<text>` labels within the SVG
- Astronaut: `<title>` specifies "Astronaut in spacesuit, floating in space"
- Dark background scenes: verify WCAG contrast for any text overlaid (white text on dark: minimum 4.5:1 contrast)

## 7.9 Commercial Guidelines

- No national flags on spacecraft or spacesuits (culturally neutral)
- No weapons or military iconography
- Moon landing scenes: factually accurate — astronaut depicted with correct number of limbs, functional suit, appropriate equipment

## 7.10 Estimated Asset Count: 70–90 assets

---

---

# CATEGORY 08 — OCEAN

## 8.1 Purpose

Ocean environment illustrations serve marine science, geography (ocean zones, coastlines), and creative writing themes. The ocean is also among the richest visual themes for cross-subject maths and literacy activities.

## 8.2 Design Standards

Ocean environments use a distinctive layered depth system:

```
ZONE STRUCTURE (from top to bottom):
  ┌─────────────────────────────┐  Sky zone
  │  Sky and clouds             │  (above waterline)
  ├─────────────────────────────┤
  │  Surface zone               │  (0–10m)
  │  Light filtering through    │
  ├─────────────────────────────┤
  │  Sunlit zone               │  (10–200m)
  │  Coral, fish, kelp          │
  ├─────────────────────────────┤
  │  Twilight zone              │  (200–1000m)
  │  Fewer creatures            │
  └─────────────────────────────┘  Deep (optional)
```

Each zone has distinct tonal fill in B&W (from light at surface to dark at depth) and colour fill in colour version.

## 8.3 Ocean Asset Library

| Asset Group | Items | Est. Count |
|-------------|-------|-----------|
| Ocean zone scenes | Full depth scene; surface only; reef scene; deep scene | 4–6 |
| Coastline | Beach scene; cliff scene; rock pool | 3–4 |
| Coral reef | Full reef scene; individual coral types | 6–8 |
| Seabed elements | Sand, rocks, treasure chest, anchor, shipwreck | 8–10 |
| Ocean plants | Kelp, seagrass, sea anemone | 4–6 |
| Waves | Simple wave; breaking wave; ripple pattern | 4–6 |
| Ocean surface | Calm; choppy; sunset | 3 |
| Underwater backgrounds | Blank blue gradient (for character placement) | 3 |

Note: Sea animals appear in WW-IB-002 Category 03. This category covers the environment in which they live.

## 8.4 Asset Naming Convention

```
WW--OCEAN--[asset]--[variant]--[size].svg

Examples:
  WW--OCEAN--scene--reef--full--xl.svg
  WW--OCEAN--scene--depth--labelled--xl.svg
  WW--OCEAN--bg--underwater--lightblue--xl.svg
  WW--OCEAN--coral--branching--md.svg
  WW--OCEAN--coastline--beach--lg.svg
```

## 8.5 Folder Location

```
assets/svg/themes/ocean/
```

## 8.6 Printing, Accessibility, Commercial Notes

- Underwater backgrounds: B&W tonal gradient from #f0f0f0 (surface) to #555555 (deep); ensure no text is placed over dark gradient zones without white fill box behind it
- Accessibility: ocean depth zones diagram: all zones labelled with live `<text>` elements and `<desc>` for full description
- No polluted ocean imagery (plastic waste) in standard classroom illustrations — environmental education worksheets require a separate, sensitively designed variant

## 8.7 Estimated Asset Count: 60–80 assets

---

---

# CATEGORY 09 — FANTASY

## 9.1 Purpose

Fantasy elements appear in creative writing worksheets, comprehension activities, imaginative play prompts, and storytelling sequences. They must be magical, joyful, and culturally inclusive — never frightening, violent, or associated with any specific religious tradition.

## 9.2 Design Standards

| Attribute | Specification |
|-----------|---------------|
| **Magic quality** | Depicted through sparkles (6-point star dots), glowing halos, and rainbow elements — never darkness, fire, or menace |
| **Characters** | All fantasy characters follow WW-IB-001 character proportions |
| **Creatures** | Must be unambiguously friendly; no sharp teeth displayed; no aggressive postures |
| **Architecture** | Fairy-tale castles are round towers, bright flags, friendly proportions — not imposing fortresses |
| **Cultural neutrality** | Fantasy elements drawn from broad imagination — not tied to any single cultural mythology |

## 9.3 Fantasy Asset Library

| Asset Group | Items | Est. Count |
|-------------|-------|-----------|
| Fantasy characters | Fairy (winged child); Wizard; Elf; Mermaid; Friendly dragon; Unicorn | 12–18 |
| Fantasy creatures | Friendly dragon (small); Unicorn; Talking animal variants | 6–8 |
| Fantasy settings | Castle exterior; Enchanted forest; Underwater palace; Cloud kingdom | 4–6 |
| Magic elements | Wand; Magic hat; Sparkle/star burst; Rainbow; Magic door | 8–10 |
| Story props | Treasure chest; Magic book; Crystal ball; Lamp | 6–8 |
| Storybook elements | Storybook frame; "Once upon a time..." banner | 4–6 |
| Fantasy vehicles | Flying carpet; Magic broom; Balloon ship | 4–6 |

## 9.4 Asset Naming Convention

```
WW--FANTASY--[asset]--[variant]--[size].svg

Examples:
  WW--FANTASY--dragon--friendly--waving--md.svg
  WW--FANTASY--castle--exterior--front--xl.svg
  WW--FANTASY--unicorn--standing--md.svg
  WW--FANTASY--magic--sparkle--burst--sm.svg
  WW--FANTASY--char--fairy--flying--st3--md.svg
```

## 9.5 Folder Location

```
assets/svg/themes/fantasy/
```

## 9.6 Asset Reuse, Printing, Accessibility, Commercial Notes

- Fantasy character builds on WW-IB-001 character system — same eye and expression modules
- Magic sparkle element is a reusable component across reward stickers, certificates, and badges
- No imagery associated with witchcraft, demonology, or occult symbolism — sparkle magic only
- Accessibility: all fantasy scene characters have diverse skin tones following WW-IB-002 §7.6 diversity standard

## 9.7 Estimated Asset Count: 70–90 assets

---

---

# CATEGORY 10 — BUILDINGS

## 10.1 Purpose

Building illustrations support social studies (community, architecture), geography (urban/rural), maths (shapes in the world), and creative writing (settings). The building library covers community buildings, homes, and public spaces.

## 10.2 Design Standards

| Attribute | Specification |
|-----------|---------------|
| **Style** | Friendly isometric 2.5D; simplified but identifiable |
| **Cultural neutrality** | Standard building forms with no explicit cultural markers unless specifically building a diversity series |
| **Scale** | Consistent scale within scenes — characters appear at 1/6th to 1/8th of building height |
| **Details** | Windows, doors, signage — all modular and swappable |

## 10.3 Building Library

| Building Type | Variants | Est. Count |
|--------------|---------|-----------|
| House (family home) | Small; medium; large; detached; semi-detached | 8–10 |
| Flat/apartment block | Low-rise (3 floor); high-rise (8 floor) | 4 |
| Shop / store | Grocery; bakery; toy shop; generic | 6–8 |
| Hospital | Exterior; with helipad | 2 |
| Fire station | With fire engine visible | 2 |
| Police station | Standard | 2 |
| Post office | Standard | 2 |
| Library | Exterior (links to Category 03) | 2 |
| Community centre | Standard | 2 |
| Park | With paths and benches | 2 |
| Street scene | 3–4 buildings in row | 3 |
| Farm | House + barn + fields | 3 |
| Factory / warehouse | Generic industrial | 2 |

## 10.4 Asset Naming Convention

```
WW--BLDG--[type]--[variant]--[size].svg

Examples:
  WW--BLDG--house--medium--md.svg
  WW--BLDG--shop--bakery--md.svg
  WW--BLDG--hospital--exterior--lg.svg
  WW--BLDG--street--3buildings--xl.svg
```

## 10.5 Folder Location

```
assets/svg/environments/buildings/
```

## 10.6 Estimated Asset Count: 60–80 assets

---

---

# CATEGORY 11 — FURNITURE

## 11.1 Purpose

Furniture and interior object assets support home and classroom scene building, maths (position and direction), and SEL worksheets. They are primarily used as modular props within scene templates.

## 11.2 Design Standards

Furniture follows the same 2.5D perspective as classroom and building environments. All edges are rounded. No sharp corners visible. Modular design allows pieces to be combined into complete room scenes.

## 11.3 Furniture Asset Library

| Category | Items | Est. Count |
|----------|-------|-----------|
| Seating | Sofa, armchair, office chair, wooden chair, stool, beanbag | 8–10 |
| Tables | Dining table, coffee table, desk, round table | 6–8 |
| Storage | Wardrobe, bookcase, sideboard, toy chest | 6–8 |
| Beds | Single bed, bunk bed, cot/crib | 4–5 |
| Kitchen | Kitchen counter, fridge, oven, sink | 6–8 |
| Bathroom | Bath/tub, toilet, sink, mirror | 4–6 |
| Decor | Lamp, rug, clock, curtains, plant, picture frame | 8–10 |
| Classroom furniture | (See Category 02 for classroom-specific items) | — |

## 11.4 Asset Naming Convention

```
WW--FURN--[type]--[variant]--[size].svg

Examples:
  WW--FURN--sofa--2seat--md.svg
  WW--FURN--bed--bunk--md.svg
  WW--FURN--bookcase--full--md.svg
  WW--FURN--lamp--floor--sm.svg
```

## 11.5 Folder Location

```
assets/svg/environments/furniture/
```

## 11.6 Estimated Asset Count: 60–80 assets

---

---

# CATEGORY 12 — COMMUNITY HELPERS

## 12.1 Purpose

Community helper characters appear in social studies (occupations, community roles), SEL (helping others), and career awareness activities. They are among the most diversity-critical illustrations in the catalogue — every occupation must represent diverse genders, skin tones, and body types.

## 12.2 Design Standards

| Attribute | Specification |
|-----------|---------------|
| **Character base** | Builds on WW adult character proportions (WW-IB-001 §6.2) |
| **Uniform accuracy** | Uniforms are recognisable but not brand-specific to any country's service |
| **Gender neutrality** | All occupations are available in at least 2 gender expression variants |
| **Diversity** | Each occupation set includes minimum 3 distinct skin tones |
| **Props** | Each character is shown with a characteristic prop (stethoscope, hose, wrench) |
| **Expression** | Default: Proud or Welcoming — community helpers are celebrated |

## 12.3 Community Helper Library

| Role | Props | Variants | Est. Count |
|------|-------|---------|-----------|
| Doctor | Stethoscope, clipboard | 2 genders × 2 skin tones | 4 |
| Nurse | Stethoscope, tray | 2 × 2 | 4 |
| Firefighter | Helmet, hose | 2 × 2 | 4 |
| Police officer | Badge, notepad | 2 × 2 | 4 |
| Teacher | Book, pointer | 2 × 2 | 4 |
| Chef | Chef's hat, spatula | 2 × 2 | 4 |
| Farmer | Hat, pitchfork | 2 × 2 | 4 |
| Builder/Constructor | Hard hat, tool belt | 2 × 2 | 4 |
| Postman/Delivery | Bag, parcel | 2 × 2 | 4 |
| Shopkeeper | Apron, bag | 2 × 2 | 4 |
| Bus driver | Uniform, steering wheel | 2 × 2 | 4 |
| Librarian | Book, reading glasses | 2 × 2 | 4 |
| Scientist | Lab coat, test tube | 2 × 2 | 4 |
| Astronaut | Full suit, helmet | 2 × 2 | 4 |
| Vet | Stethoscope, small animal | 2 × 2 | 4 |

## 12.4 SVG Structure

```xml
<svg viewBox="0 0 120 200" role="img" aria-labelledby="helper-title">
  <title id="helper-title">[Role] character</title>
  <g id="helper--shadow">
  <g id="helper--body">
    <g id="helper--legs">
    <g id="helper--torso">    <!-- includes uniform/clothing -->
    <g id="helper--arms">
    <g id="helper--hands">
  <g id="helper--head">
    <g id="helper--face">    <!-- expression: proud/welcoming -->
    <g id="helper--hair">
    <g id="helper--hat">     <!-- role-specific headwear -->
  <g id="helper--prop">      <!-- held item: stethoscope, hose, etc. -->
  <g id="helper--uniform-detail">  <!-- badges, buttons, pockets -->
```

## 12.5 Asset Naming Convention

```
WW--HELPER--[role]--[gender]--[skin-tone]--[size].svg

Examples:
  WW--HELPER--doctor--f--st3--md.svg
  WW--HELPER--firefighter--m--st6--md.svg
  WW--HELPER--chef--gn--st2--md.svg
  WW--HELPER--scientist--f--st5--lg.svg
```

## 12.6 Folder Location

```
assets/svg/characters/community-helpers/
  [role]/
```

## 12.7 Asset Reuse Strategy

- Uniform layer (`helper--torso`) is separate — same body base can swap uniform for different occupations reducing redraw time
- Hat/headwear group: modular — worn/not worn variants without body redraw
- Prop group: fully swappable — same character can hold different tools

## 12.8 Printing, Accessibility, Commercial Notes

- Each character's occupation must be identifiable in B&W through uniform silhouette alone (stethoscope shape, firefighter helmet shape, chef's toque shape)
- `<title>` and `<desc>` must state the role, not just "person": "Female doctor character holding stethoscope"
- No real-world police department or fire service logos or badges — generic badge shapes only

## 12.9 Estimated Asset Count: 60–80 assets (15 roles × 4 variants each)

---

---

# CATEGORY 13 — MUSIC

## 13.1 Purpose

Music illustration assets support music education worksheets, rhythm and rhyme activities in literacy, cultural studies, and creative arts activities.

## 13.2 Design Standards

| Attribute | Specification |
|-----------|---------------|
| **Instrument accuracy** | Instruments are recognisable to the correct family — string, wind, percussion, keyboard |
| **Friendly quality** | Instruments appear slightly rounded and approachable — not hyper-realistic |
| **Musical notation** | Note shapes (crotchet, quaver, minim, semibreve) are precisely correct; no invented notation |
| **Character musicians** | Builds on WW-IB-002 Category 07 (Kids) base — add instrument prop |

## 13.3 Music Asset Library

| Asset Group | Items | Est. Count |
|-------------|-------|-----------|
| String instruments | Guitar (acoustic), Violin, Cello, Ukulele, Harp | 5–7 |
| Wind instruments | Trumpet, Flute, Recorder, Saxophone, Clarinet | 5–7 |
| Percussion | Drums (kit), Tambourine, Xylophone, Maracas, Triangle | 5–7 |
| Keyboard | Piano (upright), Electric keyboard | 2–3 |
| Traditional/world | Tabla, Sitar, Djembe, Pan flute, Didgeridoo | 5–7 |
| Voice | Microphone; child singing (character) | 3–4 |
| Music notation | Treble clef, Bass clef, Bar lines, Note types (×4), Rest types (×4) | 12–16 |
| Music paper | Blank 4-line staff, Blank 5-line staff | 2–3 |
| Music scene | Concert stage; school music room; choir | 3–4 |

## 13.4 Asset Naming Convention

```
WW--MUSIC--[asset]--[variant]--[size].svg

Examples:
  WW--MUSIC--guitar--acoustic--md.svg
  WW--MUSIC--notation--trebleclef--sm.svg
  WW--MUSIC--notation--crotchet--sm.svg
  WW--MUSIC--paper--5linestaff--blank--lg.svg
  WW--MUSIC--instrument--xylophone--md.svg
```

## 13.5 Folder Location

```
assets/svg/themes/music/
  instruments/
  notation/
  scenes/
```

## 13.6 Cultural Diversity Note

The world music instrument group (tabla, djembe, etc.) is included to ensure global cultural representation across curriculum content. These instruments must be drawn with the same visual quality and dignity as Western instruments — not as "exotic props" but as primary musical tools.

## 13.7 Estimated Asset Count: 60–80 assets

---

---

# CATEGORY 14 — SPORTS

## 14.1 Purpose

Sports illustrations appear in PE worksheets, health and wellbeing units, maths (sorting, counting), and cultural studies (international sports). They must represent diverse body types and abilities.

## 14.2 Design Standards

| Attribute | Specification |
|-----------|---------------|
| **Action** | Sports characters are always in motion — dynamic but stable poses |
| **Equipment accuracy** | Sports equipment is immediately identifiable by silhouette |
| **Safety** | Appropriate safety gear shown (helmet on cycling/skating; shin guards in football) |
| **Inclusive sport** | Para-sport variants available (wheelchair basketball, para-athletics) |
| **Team colours** | Generic jersey colours — no real team colours or logos |

## 14.3 Sports Asset Library

| Sport | Character Pose | Equipment | Est. Count |
|-------|---------------|-----------|-----------|
| Football/Soccer | Kicking; running; goalkeeper | Ball, goal | 4–6 |
| Basketball | Shooting; dribbling | Ball, hoop | 4–6 |
| Cricket | Batting; bowling | Bat, ball, stumps | 4–6 |
| Tennis | Serving; forehand | Racket, ball | 3–4 |
| Swimming | Freestyle stroke; diving | — | 3–4 |
| Athletics | Running (sprint); long jump; throwing | Track | 4–6 |
| Gymnastics | Cartwheel; balance beam; somersault | — | 3–4 |
| Cycling | Riding (with helmet) | Bike, helmet | 2–3 |
| Skating | Ice skates; roller skates | — | 2–3 |
| Yoga/mindfulness | Tree pose; seated | Mat | 2–3 |
| Para-sport | Wheelchair basketball; para-athletics | Wheelchair | 2–3 |
| Team scene | Mixed team in huddle | — | 2–3 |

## 14.4 Asset Naming Convention

```
WW--SPORT--[sport]--[action]--[skin-tone]--[size].svg

Examples:
  WW--SPORT--football--kicking--st4--md.svg
  WW--SPORT--gymnastics--cartwheel--st2--md.svg
  WW--SPORT--para--wheelchair-basketball--st5--md.svg
  WW--SPORT--athletics--running--st6--md.svg
```

## 14.5 Folder Location

```
assets/svg/themes/sports/
```

## 14.6 Estimated Asset Count: 70–90 assets

---

---

# CATEGORY 15 — FESTIVAL DECORATIONS

## 15.1 Purpose

Festival decoration elements appear in seasonal worksheets, cultural studies units, and themed bundle covers. They must represent a diverse global festival calendar with consistent visual quality across all cultures.

## 15.2 Design Standards

| Attribute | Specification |
|-----------|---------------|
| **Cultural respect** | All festival elements are researched and drawn with accuracy and dignity |
| **Religious symbols** | May be depicted in educational context (star and crescent, cross, Star of David, Diwali diya) but never as a branding element on a product cover |
| **Decorative quality** | Rich and celebratory; more detail permitted in this category than in general illustrations |
| **Inclusive calendar** | At minimum: Christmas/winter; Diwali; Eid; Hanukkah; Chinese New Year; Easter; Harvest/Thanksgiving; Holi; Lunar New Year; Halloween; Bonfire Night |

## 15.3 Festival Decoration Library

| Festival | Decoration Items | Est. Count |
|----------|-----------------|-----------|
| Christmas/Winter | Bauble, star, candy cane, snowflake, holly, gift box, Santa hat, stocking, Christmas tree, nativity silhouette | 12–16 |
| Diwali | Diya lamp, rangoli pattern, firework burst, lotus, lantern, toran | 8–10 |
| Eid al-Fitr | Moon and star, lantern, henna hand, mosque silhouette, Eid gift | 6–8 |
| Hanukkah | Menorah, dreidel, Star of David, gold coin (gelt) | 4–6 |
| Chinese/Lunar New Year | Red lantern, dragon silhouette, lucky envelope (hongbao), kumquat | 6–8 |
| Easter | Easter egg, bunny, chick, spring flowers, Easter basket | 6–8 |
| Halloween | Pumpkin (friendly/smiling), ghost (friendly), bat, witch hat, spider web | 6–8 |
| Holi | Colour splash burst, water pistol, flowers | 4–6 |
| Harvest / Thanksgiving | Pumpkin, corn, leaves, cornucopia, apple | 6–8 |
| Bonfire Night | Firework burst, bonfire, sparkler | 4–6 |
| Generic celebration | Balloon, confetti, party popper, banner, party hat, streamer | 8–10 |

## 15.4 Asset Naming Convention

```
WW--FEST--[festival]--[item]--[variant]--[size].svg

FESTIVAL:  xmas | diwali | eid | hanukkah | cny | easter | halloween
           holi | harvest | bonfire | generic

Examples:
  WW--FEST--diwali--diya--lit--md.svg
  WW--FEST--xmas--bauble--round--sm.svg
  WW--FEST--cny--lantern--red--md.svg
  WW--FEST--generic--balloon--round--sm.svg
  WW--FEST--easter--egg--decorated--md.svg
```

## 15.5 Folder Location

```
assets/svg/themes/festivals/
  christmas/  diwali/  eid/  hanukkah/  cny/  easter/
  halloween/  holi/  harvest/  generic/
```

## 15.6 Commercial Guidelines

- Festival bundles must clearly state the festival in the product title and not use ambiguous "seasonal" language that obscures the specific cultural context
- All religious symbols are used in an educational, respectful context only
- Halloween decorations: no gore, blood, or frightening elements — pumpkins are always smiling; ghosts are friendly

## 15.7 Estimated Asset Count: 80–100 assets

---

---

# CATEGORY 16 — BORDERS

## 16.1 Purpose

Borders are among the most-used structural elements in the entire library. Every worksheet has a border. The border system must be comprehensive, consistent with the Design Bible's dual-border system, and adaptable to all themes.

> **Cross-reference:** WW-DB-001 Chapter 08 (Border Rules) governs all border usage. This category provides the SVG implementation of those rules.

## 16.2 Design Standards — The Dual Border System

```
┌─────────────────────────────────────────────┐  ← OUTER BORDER
│  outer margin (4mm)                         │    L1 weight (2.5px)
│  ┌───────────────────────────────────────┐  │    rx="8" (rounded corner)
│  │  inner margin (3mm)                   │  │
│  │                                        │  │  ← INNER BORDER
│  │  CONTENT AREA                         │  │    L3 weight (1.5px)
│  │                                        │  │    rx="6" (rounded corner)
│  │                                        │  │
│  └───────────────────────────────────────┘  │
│                                             │
└─────────────────────────────────────────────┘
```

**Non-negotiable border rules:**
- Both borders always have rounded corners (`rx` minimum 6)
- Outer border: always L1 weight
- Inner border: always L3 weight
- 4mm gap between outer and inner border — no element may be placed in this zone
- Border must never be a raster image — always a SVG `<rect>` or `<path>` element

## 16.3 Border System Tiers

### Tier 1 — Standard Borders (No Decoration)

| Border ID | Description | Use |
|-----------|-------------|-----|
| BRD-STD-01 | Plain double border — rounded | Standard worksheets |
| BRD-STD-02 | Plain single outer border only | Assessment pages |
| BRD-STD-03 | Thick outer, thin inner — heavyweight | Cover pages |

### Tier 2 — Themed Borders (Decorative Elements at Corners)

| Border ID | Description | Theme |
|-----------|-------------|-------|
| BRD-THM-01 | Corner stars | General achievement |
| BRD-THM-02 | Corner animals (4 different corners) | Nature/science |
| BRD-THM-03 | Corner pencils and books | Back-to-school |
| BRD-THM-04 | Corner flowers | Spring/Seasons |
| BRD-THM-05 | Corner snowflakes | Winter |
| BRD-THM-06 | Corner leaves | Autumn/Harvest |
| BRD-THM-07 | Corner shells and waves | Ocean theme |
| BRD-THM-08 | Corner stars and rockets | Space theme |
| BRD-THM-09 | Corner alphabet letters | Literacy theme |
| BRD-THM-10 | Corner numbers and shapes | Maths theme |

### Tier 3 — Continuous Pattern Borders

| Border ID | Description | Theme |
|-----------|-------------|-------|
| BRD-PAT-01 | Dot-dash pattern | General |
| BRD-PAT-02 | Stars repeated | Reward/certificate |
| BRD-PAT-03 | Hearts repeated | Valentine/SEL |
| BRD-PAT-04 | Animal pawprints | Pet/animal theme |
| BRD-PAT-05 | Zigzag / chevron | Modern/geometric |
| BRD-PAT-06 | Wavy line | Ocean/water theme |

### Tier 4 — Certificate Borders (Premium)

| Border ID | Description |
|-----------|-------------|
| BRD-CERT-01 | Ornate double scroll border |
| BRD-CERT-02 | Ribbon and laurel border |
| BRD-CERT-03 | Star and swirl border |
| BRD-CERT-04 | Simple elegant border |

## 16.4 SVG Structure for Borders

```xml
<!-- Standard double border implementation -->
<svg viewBox="0 0 595 842" preserveAspectRatio="none"
     role="img" aria-labelledby="border-title">
  <title id="border-title">Worksheet border</title>

  <!-- A4 coordinate space: 595 × 842 units -->

  <!-- Outer border -->
  <rect x="14" y="14" width="567" height="814"
        rx="8" ry="8"
        fill="none"
        stroke="#333333"
        stroke-width="2.5"/>

  <!-- Inner border -->
  <rect x="25" y="25" width="545" height="792"
        rx="6" ry="6"
        fill="none"
        stroke="#333333"
        stroke-width="1.5"/>

  <!-- Corner decorations (Tier 2 only) — placed at corners -->
  <g id="border--corner-tl"> <!-- top left decoration -->
  <g id="border--corner-tr"> <!-- top right decoration -->
  <g id="border--corner-bl"> <!-- bottom left decoration -->
  <g id="border--corner-br"> <!-- bottom right decoration -->

  <!-- Pattern repeat (Tier 3 only) -->
  <g id="border--pattern-top">
  <g id="border--pattern-bottom">
  <g id="border--pattern-left">
  <g id="border--pattern-right">
```

## 16.5 Asset Naming Convention

```
WW--BORDER--[tier]--[id]--[page-size].svg

TIER: std | thm | pat | cert
PAGE: a4 | letter | half  (half = A5/half sheet)

Examples:
  WW--BORDER--std--01--a4.svg
  WW--BORDER--thm--05--a4.svg       (snowflake corners)
  WW--BORDER--pat--02--a4.svg       (star pattern)
  WW--BORDER--cert--01--a4.svg      (ornate certificate)
```

## 16.6 Folder Location

```
assets/svg/structural/borders/
  standard/
  themed/
  pattern/
  certificate/
```

## 16.7 Asset Reuse Strategy

- Every worksheet template includes the standard border as an embedded `<svg>` reference — not redrawn per worksheet
- Corner decoration groups are interchangeable — swap without affecting the base border rectangles
- A4 and Letter variants differ only in the outer `viewBox` and `<rect>` dimensions — the corner decoration groups are identical

## 16.8 Printing Considerations

- Borders must print at their design weight on the lowest quality laser setting
- Pattern borders (Tier 3): minimum 8pt gap between pattern elements — below this, elements merge on low-DPI printers
- Certificate borders (Tier 4): require high-quality print setting — add a note to the Printing Guide component

## 16.9 Accessibility

- Borders are decorative — add `aria-hidden="true"` to the border SVG group; it should not be read by screen readers
- Exception: borders that contain meaningful content (such as a "Congratulations!" banner integrated into a certificate border) must have live text elements

## 16.10 Estimated Asset Count: 60–80 border SVG files

---

---

# CATEGORY 17 — FRAMES

## 17.1 Purpose

Frames differ from borders in that they are smaller, used to contain a specific element — an illustration, a "Draw your answer here" zone, a portrait circle for a child's name, or a photo frame for a family portrait activity.

## 17.2 Frame Library

| Frame Type | Description | Est. Count |
|-----------|-------------|-----------|
| Portrait oval/circle | For "draw yourself" activities | 4 |
| Square illustration frame | For "draw the scene" activities | 4 |
| Cloud frame | Thought bubble / dream / imagination | 3 |
| Speech bubble | Rectangular; oval; spiky | 3 |
| Chalkboard frame | Dark bordered "chalkboard" zone | 2 |
| Decorative photo frame | For family/personal photo activities | 4 |
| TV / screen frame | For "show and tell" / media activities | 2 |
| Magnifying glass frame | For science observation activities | 2 |
| Book page frame | Open book as content frame | 2 |

## 17.3 Asset Naming Convention

```
WW--FRAME--[type]--[variant]--[size].svg

Examples:
  WW--FRAME--portrait--oval--md.svg
  WW--FRAME--speech--oval--sm.svg
  WW--FRAME--cloud--standard--md.svg
  WW--FRAME--magnify--standard--md.svg
```

## 17.4 Folder Location

```
assets/svg/structural/frames/
```

## 17.5 Estimated Asset Count: 40–60 assets

---

---

# CATEGORY 18 — PATTERNS

## 18.1 Purpose

Pattern assets serve as repeating background textures, coloring activity patterns, and decorative elements for covers and certificates. They must be visually engaging while printing cleanly.

## 18.2 Pattern Types

| Pattern | Description | Use |
|---------|-------------|-----|
| Polka dots | Regular; varied size | Background; coloring |
| Stripes | Horizontal; vertical; diagonal | Background; sorting |
| Chevron / Zigzag | Regular zigzag | Decorative; maths |
| Checkerboard | Regular grid | Maths; sorting |
| Stars scattered | Random and regular | Reward; space |
| Hearts scattered | Random | SEL; Valentine |
| Dots and dashes | Morse-code style | Science; code |
| Scales (fish) | Semicircle repeat | Ocean; art |
| Honeycomb | Hexagon tessellation | Science; nature |
| Triangles | Regular tessellation | Geometry; maths |
| Waves | Horizontal wavy repeat | Ocean; weather |
| Leaves | Scattered leaf forms | Nature; autumn |

## 18.3 Pattern SVG Implementation

All patterns are implemented as SVG `<pattern>` elements with a `patternUnits="userSpaceOnUse"` specification:

```xml
<defs>
  <pattern id="ww-pat-dots" x="0" y="0" width="20" height="20"
           patternUnits="userSpaceOnUse">
    <circle cx="10" cy="10" r="3" fill="#cccccc"/>
  </pattern>
</defs>
<!-- Apply pattern as fill on any rect: -->
<rect width="595" height="842" fill="url(#ww-pat-dots)"/>
```

## 18.4 Asset Naming Convention

```
WW--PATTERN--[type]--[scale]--[density].svg

Examples:
  WW--PATTERN--dots--md--regular.svg
  WW--PATTERN--stars--sm--scattered.svg
  WW--PATTERN--honeycomb--md--regular.svg
  WW--PATTERN--chevron--md--diagonal.svg
```

## 18.5 Folder Location

```
assets/svg/structural/patterns/
```

## 18.6 Printing Considerations

- All patterns must print cleanly at 10% grey equivalent fill minimum — verify on B&W laser
- Minimum element size in any pattern tile: 4px × 4px at A4 print scale
- Never use patterns as background behind readable text — tonal contrast drops below accessible threshold

## 18.7 Estimated Asset Count: 40–60 pattern definitions

---

---

# CATEGORY 19 — ICONS

## 19.1 Purpose

Icons are the functional navigation and instructional micro-illustrations of the Worksheet Wonder system. Every worksheet uses icons to guide the child through the activity — pencil icon for "write", scissors for "cut", colouring pencil for "colour". Icons must be instantly readable at very small sizes (as small as 10mm × 10mm on an A4 page).

## 19.2 Design Standards

| Attribute | Specification |
|-----------|---------------|
| **Grid** | All icons designed on a 64×64 unit grid; optical centre maintained |
| **Weight** | L2 outline (2.0px) at 64×64; always `stroke-linecap="round"` |
| **Fill** | Generally solid or simple split fills; no gradients; no complex texture |
| **Silhouette** | Every icon must be identifiable by silhouette alone (no colour dependency) |
| **Consistency** | All icons in the same set use identical stroke weight and corner radius |
| **Padding** | 4-unit optical padding from edge of 64×64 grid on all sides |

## 19.3 Icon Library — Complete Set

### Instruction Icons (Most Critical — Used on Every Worksheet)

| Icon | Description |
|------|-------------|
| ✏️ | Pencil (write / fill in) |
| 🖍️ | Crayon / colouring pencil (colour in) |
| ✂️ | Scissors (cut out) |
| 🔵 | Circle (circle the answer) |
| ✅ | Tick / checkmark (tick the correct answer) |
| ❌ | Cross (cross out / eliminate) |
| 🔗 | Line / connecting (draw a line to match) |
| 🖼️ | Frame / box (draw in the box) |
| 📖 | Open book (read) |
| 👂 | Ear (listen) |
| 🗣️ | Speech bubble (say aloud / discuss) |
| 👀 | Eyes (look carefully) |
| 🔢 | Number grid (count / number) |
| 📐 | Ruler (measure) |
| 🔬 | Magnifying glass (observe / investigate) |
| ⭐ | Star (rate yourself / award) |
| 🏆 | Trophy (challenge / bonus activity) |
| ⏱️ | Timer / clock (timed activity) |
| 🎯 | Target (learning objective) |
| 👨‍🏫 | Teacher figure (teacher guide note) |
| 👪 | Family figure (parent guide note) |

### Subject Icons

| Icon | Description |
|------|-------------|
| ABC | Literacy / English |
| 123 | Mathematics |
| 🔭 | Science |
| 🌍 | Social Studies / Geography |
| 🎵 | Music |
| 🏃 | Physical Education |
| 🎨 | Art |
| 💻 | Technology / Computing |

### Difficulty Icons

| Icon | Description |
|------|-------------|
| ⭐ | Foundation (1 star) |
| ⭐⭐ | Developing (2 stars) |
| ⭐⭐⭐ | Mastery (3 stars) |
| 🌱 | Beginner / seed |
| 🌿 | Growing / sprout |
| 🌳 | Expert / tree |

### Navigation Icons

| Icon | Description |
|------|-------------|
| ➡️ | Start here / next |
| ◀️ | Go back |
| ⬇️ | Continue below |
| 🔄 | Repeat / try again |
| ✔️ | Done / complete |
| 🔓 | Next section unlocked |

### Reward / Feedback Icons

| Icon | Description |
|------|-------------|
| ⭐ | Great job / well done |
| 🌟 | Excellent / super star |
| 🏅 | Achievement badge |
| 💡 | Hint / tip |
| ⚠️ | Attention / important note |
| 💬 | Discussion question |

## 19.4 SVG Structure for Icons

```xml
<svg viewBox="0 0 64 64" role="img" aria-labelledby="icon-pencil-title">
  <title id="icon-pencil-title">Pencil icon — write your answer</title>
  <g id="icon--pencil">
    <!-- All paths use: stroke="#333" stroke-linecap="round"
         stroke-linejoin="round" fill="none" or solid fill -->
  </g>
</svg>
```

## 19.5 Asset Naming Convention

```
WW--ICON--[function]--[variant]--[size].svg

FUNCTION: write | colour | cut | circle | tick | cross | match | draw |
          read | listen | speak | look | count | measure | observe |
          star | trophy | timer | objective | teacher | parent

SIZE: sm (32×32 output) | md (64×64 output) | lg (128×128 output)

Examples:
  WW--ICON--write--standard--sm.svg
  WW--ICON--observe--magnify--md.svg
  WW--ICON--trophy--challenge--md.svg
  WW--ICON--subject--science--sm.svg
  WW--ICON--difficulty--mastery--sm.svg
```

## 19.6 Folder Location

```
assets/svg/icons/
  instruction/
  subject/
  difficulty/
  navigation/
  reward/
```

## 19.7 Printing Considerations

- Icons must read at 10mm × 10mm on a printed A4 page — test on laser at minimum
- At small sizes, suppress inner detail lines (remove L4 and L5 strokes from the small variant)
- Icon background circle (optional container circle): L5 weight (0.75px), never filled — outline only

## 19.8 Accessibility

- Every icon used on a worksheet must have a text label adjacent to it — never rely on icon alone
- Icon `<title>` describes the action, not the visual: "Write your answer in the box" not "Pencil icon"
- Icons used for difficulty levels must also have text labels ("Easy / Medium / Hard" or equivalent)

## 19.9 Estimated Asset Count: 100–130 icons

---

---

# CATEGORY 20 — BADGES

## 20.1 Purpose

Badges serve as achievement markers, section identifiers, skill level indicators, and motivational elements throughout bundles. They appear on cover pages, within worksheets, and in teacher guides. A well-designed badge system creates a cohesive visual identity across the catalogue.

## 20.2 Design Standards

| Attribute | Specification |
|-----------|---------------|
| **Shape** | Shield, circle, hexagon, star, ribbon — each shape carries a consistent meaning |
| **Hierarchy** | Badge size and complexity increases with achievement level |
| **Text** | Achievement text as live SVG `<text>` — never traced to paths |
| **Depth** | Subtle badge "body" with L2 outer stroke + L4 inner shadow line to suggest physical badge |
| **Premium feel** | Badges should feel like something a child would be proud to display |

## 20.3 Badge Shape Meanings

| Shape | Meaning | Use |
|-------|---------|-----|
| Circle | General achievement | Star of the Week, Well Done, Try Again |
| Shield | Subject mastery | "Maths Master", "Reading Champion" |
| Hexagon | Skill badge | Specific skill completion |
| Star (5-pt) | Top achievement | Gold Star, Top Scorer |
| Ribbon/rosette | First place / competition | Winner badges |
| Oval banner | Informational | Section labels, "Extension Activity" |

## 20.4 Badge System Sets

### Achievement Badges (Curriculum-linked)

| Badge | Description |
|-------|-------------|
| Counting Champion | Maths — Number |
| Shape Star | Maths — Geometry |
| Word Wizard | Literacy — Vocabulary |
| Reading Rockstar | Literacy — Reading |
| Writing Warrior | Literacy — Handwriting |
| Science Explorer | Science |
| Super Speller | Literacy — Spelling |
| Maths Master | Mathematics general |
| Creative Thinker | Creative Arts |
| Team Player | SEL |

### Effort and Participation Badges

| Badge | Description |
|-------|-------------|
| Great Effort | Universal encouragement |
| Try Again | Growth mindset |
| Super Improver | Progress recognition |
| I Did It! | Completion |
| First Attempt | Beginning a challenge |
| I Persevered | Resilience recognition |

### Difficulty Level Badges

| Badge | Tier |
|-------|------|
| Seed Badge (green) | Foundation |
| Sprout Badge (teal) | Developing |
| Tree Badge (dark green) | Mastery |

## 20.5 SVG Structure for Badges

```xml
<svg viewBox="0 0 120 120" role="img" aria-labelledby="badge-title">
  <title id="badge-title">Maths Master badge</title>
  <g id="badge--shadow">         <!-- light drop shadow ellipse, L5 -->
  <g id="badge--body">           <!-- main badge shape fill -->
  <g id="badge--inner-ring">     <!-- decorative inner ring, L4 -->
  <g id="badge--illustration">   <!-- central icon or character -->
  <g id="badge--text-band">      <!-- curved or straight text band area -->
  <g id="badge--text">           <!-- achievement text, live SVG text -->
  <g id="badge--stars">          <!-- star decoration elements -->
```

## 20.6 Asset Naming Convention

```
WW--BADGE--[shape]--[achievement]--[colour-theme]--[size].svg

Examples:
  WW--BADGE--circle--greateffort--blue--md.svg
  WW--BADGE--shield--mathsmaster--gold--lg.svg
  WW--BADGE--star--goldstar--gold--lg.svg
  WW--BADGE--hexagon--scienceexplorer--teal--md.svg
  WW--BADGE--ribbon--winner--red--lg.svg
```

## 20.7 Folder Location

```
assets/svg/reward/badges/
```

## 20.8 Printing Considerations

- Badges print optimally at 30mm × 30mm minimum on A4
- B&W version: use tonal fills (dark shield, lighter centre, white text) — maintains hierarchy without colour
- Star burst background detail: reduce to L5 in B&W to avoid toner density issues

## 20.9 Estimated Asset Count: 60–80 badges

---

---

# CATEGORY 21 — CERTIFICATES

## 21.1 Purpose

Certificates of completion are the premium reward element in every Worksheet Wonder bundle. A well-crafted certificate has high perceived value — parents frame them; children treasure them. Certificate quality must be the highest in the entire catalogue.

> **Cross-reference:** WW-DB-001 Chapter 18 (Certificate Standards) governs all certificate content requirements.
> WW-PS-100 §2.12 defines the certificate as Component 12 of every bundle.

## 21.2 Design Standards

| Attribute | Specification |
|-----------|---------------|
| **Quality** | Certificate must feel like a premium document — ornate border, clear hierarchy, dignified layout |
| **Border** | Always BRD-CERT tier (Category 16 §16.3 Tier 4) — never standard worksheet border |
| **Typography** | Title: Fredoka One; Recipient name area: Nunito, large, underline or box; Body text: Nunito |
| **Illustration** | Central illustration: matching bundle theme; always joyful; trophy/star/badge element always present |
| **Signature lines** | Teacher signature line; Parent signature line; Date line |
| **Recipient field** | "Awarded to: _______________" — large enough for pencil writing |
| **Size** | Always A4; landscape orientation preferred for premium feel; portrait available |

## 21.3 Certificate Template Variants

| Variant | Description |
|---------|-------------|
| CERT-01 | Landscape — ornate border, star central illustration, gold/grey colour scheme |
| CERT-02 | Landscape — ribbon border, animal character, warm colour scheme |
| CERT-03 | Portrait — simple elegant border, abstract geometric central design |
| CERT-04 | Landscape — subject-specific (Maths/Science/Literacy/Arts variants) |
| CERT-05 | Landscape — seasonal (Christmas, Spring, Autumn, etc.) |
| CERT-06 | Portrait — preschool age-appropriate (large text, large character, simpler layout) |

## 21.4 SVG Structure for Certificates

```xml
<svg viewBox="0 0 842 595" role="img" aria-labelledby="cert-title">
  <!-- Landscape A4: 842 × 595 units -->
  <title id="cert-title">Certificate of completion</title>
  <g id="cert--background">      <!-- background fill, paper texture -->
  <g id="cert--border">          <!-- premium border (BRD-CERT-01 to 04) -->
  <g id="cert--header">          <!-- "Certificate of Achievement" title -->
  <g id="cert--awarded-to">      <!-- "Awarded to:" label + name line -->
  <g id="cert--body-text">       <!-- "for successfully completing..." -->
  <g id="cert--bundle-title">    <!-- specific bundle name text -->
  <g id="cert--illustration">    <!-- central or flanking illustration -->
  <g id="cert--stars">           <!-- decorative star elements -->
  <g id="cert--signature">       <!-- 2 signature lines + date line -->
  <g id="cert--footer">          <!-- Worksheet Wonder logo/name + date -->
```

## 21.5 Asset Naming Convention

```
WW--CERT--[variant]--[theme]--[orientation].svg

ORIENTATION: landscape | portrait

Examples:
  WW--CERT--01--standard--landscape.svg
  WW--CERT--04--maths--landscape.svg
  WW--CERT--06--preschool--portrait.svg
  WW--CERT--05--christmas--landscape.svg
```

## 21.6 Folder Location

```
assets/svg/reward/certificates/
```

## 21.7 Printing Considerations

- Certificates require: print at 100% scale; do not scale to fit; use best quality print setting
- Always include a "Printing Guide" note on the certificate page: "For best results, print at 100% on A4 paper using 'Best Quality' printer settings"
- Certificate border: minimum L2 weight — lighter borders disappear on home inkjet

## 21.8 Accessibility

- All text elements on certificates are live SVG `<text>` — never traced
- The recipient name blank is implemented as a `<line>` or `<rect>` with appropriate `aria-label="Space for child's name"`

## 21.9 Estimated Asset Count: 20–30 certificate templates

---

---

# CATEGORY 22 — REWARD STICKERS

## 22.1 Purpose

Reward stickers appear on self-assessment pages, progress trackers, and as printable cut-out reward sheets at the end of bundles. They are powerful motivators in early childhood education. The sticker library must be generous, diverse, and irresistibly collectible.

## 22.2 Design Standards

| Attribute | Specification |
|-----------|---------------|
| **Shape** | Circle or star primary shapes for visual unity; varied sizes S/M/L |
| **Content** | Central character or symbol + short praise phrase |
| **Outline** | All stickers have a thick white stroke outline (L1 on white, 3px minimum) — this is their "sticker cut edge" |
| **Density** | Rich, detailed designs — more illustrative complexity than standard icons |
| **Praise language** | Positive, specific, growth-mindset ("I tried!", "Great effort!", "I learned something new!") not generic superlatives only |
| **Cut marks** | Dashed circle border as cut line when stickers appear as a printable sheet |

## 22.3 Sticker Set Library

### Star Stickers
5-point and 8-point star forms; star character (smiling star); gold/silver/bronze variants in colour.

### Character Stickers
WW mascot + supporting animals/characters from WW-IB-002 in small sticker format with praise text.

### Expression Stickers
Circular stickers with face expressions from the WW-IB-001 expression library + caption:
- 😄 "Great job!"
- 🤩 "You're a star!"
- 💪 "I tried hard!"
- 🧠 "I thought carefully!"
- 🌱 "I'm growing!"

### Subject-Specific Stickers
| Subject | Sticker Design | Praise Text |
|---------|---------------|------------|
| Maths | Number character or shape | "Number Ninja!" / "Shape Champion!" |
| Literacy | Book character or letter | "Word Wizard!" / "Super Reader!" |
| Science | Magnifying glass or beaker | "Super Scientist!" |
| Art | Palette or star | "Creative Star!" |

### General Achievement Stickers
"Completed!", "I did it!", "All done!", "Try again ⭐", "Best effort!", "I persevered!", "I helped!", "I listened!"

## 22.4 SVG Structure for Stickers

```xml
<!-- Individual sticker -->
<svg viewBox="0 0 100 100" role="img" aria-labelledby="sticker-title">
  <title id="sticker-title">Well Done sticker with smiling star</title>
  <circle cx="50" cy="50" r="48"
          fill="#ffe066" stroke="white" stroke-width="4"/>
  <g id="sticker--illustration">   <!-- central character/symbol -->
  <g id="sticker--text">           <!-- praise text, curved if needed -->
  <!-- Text on sticker is live SVG <text> -->
```

```xml
<!-- Sticker sheet layout -->
<svg viewBox="0 0 595 842">
  <!-- 20–30 stickers arranged in rows, with dashed cut circles -->
  <g id="sticker-sheet--row-1">
    <use href="#sticker-01" transform="translate(x,y)"/>
    ...
  </g>
```

## 22.5 Asset Naming Convention

```
WW--STICKER--[type]--[achievement]--[size].svg

TYPE: star | character | expression | subject | general

Individual sticker:
  WW--STICKER--star--goldstar--md.svg
  WW--STICKER--expression--greatjob--md.svg
  WW--STICKER--subject--maths--mathsninja--sm.svg

Sheet:
  WW--STICKER--sheet--mixed-achievement--a4.svg
  WW--STICKER--sheet--stars-only--a4.svg
```

## 22.6 Folder Location

```
assets/svg/reward/stickers/
  individual/
  sheets/
```

## 22.7 Printing Considerations

- Sticker sheets: label with instruction "Print on sticker paper for best results; standard paper also works"
- Minimum sticker diameter: 25mm on A4 for legibility
- White stroke outline ("sticker edge"): must print clearly — minimum 2pt at final print size

## 22.8 Estimated Asset Count: 60–80 sticker designs + 10–15 pre-assembled sheets

---

---

# CATEGORY 23 — BACKGROUND ELEMENTS

## 23.1 Purpose

Background elements are large-format SVG assets that cover the full worksheet background or a significant portion of it. They establish the visual setting of a worksheet before any content or characters are placed. They must support content legibility at all times.

## 23.2 Design Standards

**The single most important rule for background elements:**

> **A background element must NEVER compromise the legibility of content placed over it.**

| Attribute | Specification |
|-----------|---------------|
| **Opacity** | Background illustrations are rendered at 15–30% opacity maximum over white in most cases |
| **Tonal value** | Must remain in the #e8e8e8 to #f8f8f8 range (very light) — nothing darker is permitted as a background field |
| **Detail** | Reduced detail compared to foreground illustrations — L3 and below only, L1 and L2 suppressed |
| **Safe zones** | Every background has a defined "content-safe zone" — the central 80% of the page must be clear of any elements that could interfere with reading or writing |

## 23.3 Background Element Library

| Background | Description | Theme |
|-----------|-------------|-------|
| BG-SKY-01 | Open sky with light cloud puffs | General, weather, space |
| BG-GRASS-01 | Simple grass field, low horizon | Outdoors, nature, animals |
| BG-UNDERWATER-01 | Light tonal underwater gradient | Ocean, sea animals |
| BG-SPACE-01 | Star field (light version, printable) | Space |
| BG-CLASSROOM-01 | Light classroom texture (floor, wall suggestion) | School activities |
| BG-FOREST-01 | Light forest canopy suggestion (leaf forms) | Nature, science |
| BG-DESERT-01 | Sand dunes, horizon | Geography, desert animals |
| BG-ARCTIC-01 | Ice and snow horizon | Polar animals, winter |
| BG-FARM-01 | Farm field and fence horizon | Farm animals, seasons |
| BG-DOTS-01 | Light polka dot pattern | General, activity page |
| BG-LINES-01 | Light horizontal line rule | Writing activities |
| BG-GRID-01 | Light square grid | Maths activities |
| BG-ISOGRID-01 | Light isometric dot grid | Geometry, 3D maths |
| BG-BLANK-01 | Plain white — no background element | Default for complex content |

## 23.4 Asset Naming Convention

```
WW--BG--[theme]--[variant]--[density]--[size].svg

DENSITY: light (15% opacity) | medium (25%) | plain

Examples:
  WW--BG--sky--clouds--light--a4.svg
  WW--BG--underwater--gradient--light--a4.svg
  WW--BG--dots--regular--light--a4.svg
  WW--BG--grid--square--plain--a4.svg
```

## 23.5 Folder Location

```
assets/svg/structural/backgrounds/
```

## 23.6 Printing Considerations

- Background elements at 15–20% opacity print as very faint tonal washes — verify this is visible enough to be aesthetically meaningful while not consuming toner
- Rule: if the background causes text readability to drop below WCAG 4.5:1, replace with BG-BLANK-01
- B&W backgrounds must use only #f0f0f0 to #e0e0e0 range — nothing darker

## 23.7 Estimated Asset Count: 60–80 background SVGs

---

---

# CATEGORY 24 — SCENE TEMPLATES

## 24.1 Purpose

Scene templates are pre-built compositional frames that define the spatial layout for common worksheet activity types. They include placeholder zones for illustrations, instruction text, activity areas, and footers — but contain no content. They are the "structural blueprint" layer over which all worksheet content is placed.

## 24.2 The Scene Template System

A scene template defines:
1. The page layout geometry (zones and proportions)
2. The placeholder positions for each element type
3. The background and border assignment
4. The character position zone(s)

Templates do NOT define:
- The specific illustrations used
- The text content
- The learning objective
- The answer format

## 24.3 Scene Template Library

### Preschool / Junior KG Templates

| Template ID | Layout Description | Primary Use |
|-------------|-------------------|-------------|
| TMPL-PSC-01 | Large central activity area; top header illustration zone; bottom instruction strip | Tracing, matching, coloring |
| TMPL-PSC-02 | Split 50/50: left illustration; right activity grid | Matching pairs |
| TMPL-PSC-03 | 4-quadrant grid; each quadrant equal | Sorting, categorising |
| TMPL-PSC-04 | Top-to-bottom strip layout (3 rows) | Sequencing, ordering |
| TMPL-PSC-05 | Full-page tracing area; corner mascot | Tracing lines, letter tracing |

### Senior KG / Grade 1–2 Templates

| Template ID | Layout Description | Primary Use |
|-------------|-------------------|-------------|
| TMPL-G12-01 | Instruction box (top 20%); main activity (centre 65%); self-rating (bottom 15%) | Standard worksheet |
| TMPL-G12-02 | 3-column layout for 3 parallel activities | Multiple exercises |
| TMPL-G12-03 | Left sidebar character; right main activity | Guided practice |
| TMPL-G12-04 | Top story/diagram context; bottom question area | Comprehension, word problems |
| TMPL-G12-05 | Cut-and-paste layout (top half illustrations; bottom half answer strips) | Sorting, classification |

### Grade 3–8 Templates

| Template ID | Layout Description | Primary Use |
|-------------|-------------------|-------------|
| TMPL-G38-01 | Clean single-column; instruction + lined answer area | Writing, extended response |
| TMPL-G38-02 | 2-column: questions left, diagram/image right | Science, geography worksheets |
| TMPL-G38-03 | Maths layout: problem strip + working area + answer box | Maths problem solving |
| TMPL-G38-04 | Reading passage top (40%); questions bottom (60%) | Comprehension |
| TMPL-G38-05 | Full-page graph/grid area with axis labels | Data, geometry |
| TMPL-G38-06 | Essay/extended writing: full page lined area + title box | Creative writing |

## 24.4 SVG Structure for Scene Templates

```xml
<svg viewBox="0 0 595 842" role="img" aria-labelledby="tmpl-title">
  <!-- A4 coordinate space -->
  <title id="tmpl-title">Worksheet template TMPL-PSC-01</title>

  <!-- Zone markers (removed in final export; used in design only) -->
  <g id="tmpl--zones" display="none">
    <rect id="zone--header" .../>    <!-- illustration zone -->
    <rect id="zone--activity" .../>  <!-- main activity area -->
    <rect id="zone--footer" .../>    <!-- footer/self-rating zone -->
  </g>

  <!-- Structural elements (visible in final output) -->
  <g id="tmpl--border">             <!-- from border library -->
  <g id="tmpl--header-rule">        <!-- separator lines -->
  <g id="tmpl--footer-rule">
  <g id="tmpl--activity-boxes">     <!-- answer boxes, grid, writing lines -->

  <!-- Content placeholder groups (filled at design time) -->
  <g id="content--illustration">    <!-- insert character/scene SVG here -->
  <g id="content--text">            <!-- all text content -->
  <g id="content--activity">        <!-- activity-specific content -->
```

## 24.5 Asset Naming Convention

```
WW--TMPL--[grade-range]--[id]--[orientation].svg

Examples:
  WW--TMPL--psc--01--portrait.svg
  WW--TMPL--g12--03--portrait.svg
  WW--TMPL--g38--04--portrait.svg
```

## 24.6 Folder Location

```
assets/svg/structural/templates/
  preschool/
  grade-1-2/
  grade-3-8/
```

## 24.7 Asset Reuse Strategy

Templates are the highest-leverage assets in the system. A single template may be used across hundreds of worksheets. Any change to a template must be versioned carefully as it will affect all downstream worksheets.

When a template needs to be modified for a specific bundle, create a **bundle-specific variant** — never modify the master template file.

## 24.8 Estimated Asset Count: 40–60 scene templates

---

---

# CATEGORY 25 — MASTER ASSET INVENTORY

## 25.1 Complete Asset Count — All Three Parts

### WW-IB-002 (Part 2) Summary

| Category | Min | Max |
|----------|-----|-----|
| Animals | 120 | 150 |
| Birds | 60 | 80 |
| Sea Animals | 70 | 90 |
| Dinosaurs | 50 | 70 |
| Insects | 50 | 70 |
| Pets | 50 | 60 |
| Kids | 150 | 200 |
| Parents | 60 | 80 |
| Teachers | 50 | 70 |
| Family | 60 | 80 |
| Alphabet Characters | 78 | 104 |
| Number Characters | 60 | 80 |
| Shapes | 80 | 100 |
| Vehicles | 80 | 100 |
| Food | 64 | 80 |
| Fruits | 60 | 80 |
| Vegetables | 60 | 80 |
| Flowers | 50 | 70 |
| Trees | 40 | 60 |
| Nature | 80 | 100 |
| Weather | 60 | 80 |
| Seasons | 60 | 80 |
| **PART 2 TOTAL** | **~1,532** | **~1,954** |

### WW-IB-003 (Part 3) Summary

| Category | Min | Max |
|----------|-----|-----|
| School | 60 | 80 |
| Classroom | 80 | 100 |
| Library | 50 | 70 |
| Playground | 50 | 70 |
| Science Diagrams | 80 | 100 |
| Math Diagrams | 80 | 100 |
| Space | 70 | 90 |
| Ocean | 60 | 80 |
| Fantasy | 70 | 90 |
| Buildings | 60 | 80 |
| Furniture | 60 | 80 |
| Community Helpers | 60 | 80 |
| Music | 60 | 80 |
| Sports | 70 | 90 |
| Festival Decorations | 80 | 100 |
| Borders | 60 | 80 |
| Frames | 40 | 60 |
| Patterns | 40 | 60 |
| Icons | 100 | 130 |
| Badges | 60 | 80 |
| Certificates | 20 | 30 |
| Reward Stickers | 60 | 80 |
| Background Elements | 60 | 80 |
| Scene Templates | 40 | 60 |
| **PART 3 TOTAL** | **~1,540** | **~2,020** |

### Grand Total — All Three Parts

| Part | Document | Min Assets | Max Assets |
|------|----------|-----------|-----------|
| Part 1 | WW-IB-001 | — | — (Standards only; no assets counted) |
| Part 2 | WW-IB-002 | ~1,532 | ~1,954 |
| Part 3 | WW-IB-003 | ~1,540 | ~2,020 |
| **GRAND TOTAL** | | **~3,072** | **~3,974** |

## 25.2 Production Priority Matrix

Not all assets will be produced at once. The following matrix governs production priority based on frequency of use across the curriculum:

| Priority | Category | Reason |
|----------|----------|--------|
| **P1 — Immediate** | Icons (all 100+) | Used on every single worksheet |
| **P1 — Immediate** | Borders (Tier 1 + 2) | Required for every product |
| **P1 — Immediate** | Scene Templates (PSC + G12) | Required before any worksheet production |
| **P1 — Immediate** | Kids characters (core 20 poses × 4 skin tones) | Appears on most worksheets |
| **P1 — Immediate** | Certificate (CERT-01 + CERT-06) | Required for every bundle |
| **P2 — Month 1–3** | Animals (farm + wild primary) | High curriculum frequency |
| **P2 — Month 1–3** | Math diagrams (core manipulatives) | Required for maths bundles |
| **P2 — Month 1–3** | Science diagrams (life science core) | Required for science bundles |
| **P2 — Month 1–3** | Community Helpers (core 8 roles) | Social studies curriculum |
| **P3 — Month 3–6** | Space, Ocean, Fantasy themes | High engagement; seasonal |
| **P3 — Month 3–6** | Festival Decorations | Seasonal bundle releases |
| **P3 — Month 3–6** | Reward Sticker sheets | Bundle enhancement |
| **P4 — Month 6–12** | Extended character variants | Diversity expansion |
| **P4 — Month 6–12** | Buildings, Furniture | Scene-building support |
| **P4 — Month 12+** | Full diagram blank variants | Assessment worksheet expansion |

## 25.3 Asset Production Rate Targets

| Production Mode | Daily Output | Monthly Output | Time to Full Library |
|----------------|-------------|----------------|---------------------|
| Human illustrator (solo) | 2–3 SVG assets | ~50 assets | ~60–80 months |
| Human illustrator (team of 3) | 6–9 SVG assets | ~150 assets | ~20–27 months |
| AI-assisted + human review | 10–15 assets/day | ~250 assets | ~12–16 months |
| AI-assisted + team QA | 25–40 assets/day | ~500 assets | ~6–8 months |

## 25.4 Asset Storage and Version Control

```
assets/svg/
│
├── characters/      → WW-IB-002 Categories 07–10, 12
├── animals/         → WW-IB-002 Categories 01–06
├── subjects/        → WW-IB-002 Categories 11–22
├── diagrams/        → WW-IB-003 Categories 05–06
├── themes/          → WW-IB-003 Categories 07–09, 13–15
├── environments/    → WW-IB-003 Categories 01–04, 10–11
├── structural/      → WW-IB-003 Categories 16–19, 23–24
└── reward/          → WW-IB-003 Categories 20–22

Version control:
  Each asset carries a version suffix in its metadata comment:
  <!-- WW Asset: WW--ICON--write--standard--sm | v1.0 | 2026 -->
  When an asset is updated, the old version moves to:
    assets/svg/[folder]/archive/[filename]_v[old]_[date].svg
```

---

---

# VERSION HISTORY

## Document Record

| Field | Detail |
|-------|--------|
| **Document ID** | WW-IB-003 |
| **Document Name** | Worksheet Wonder Illustration Bible — Part 3 |
| **Version** | 1.0 |
| **Date** | 10 July 2026 |
| **Author** | Senior Art Director |
| **Status** | Approved |
| **Approved By** | Creative Director, Worksheet Wonder |
| **Classification** | Internal — Confidential |

## Revision Log

| Version | Date | Author | Changes | Approved By |
|---------|------|--------|---------|-------------|
| 1.0 | 10 July 2026 | Senior Art Director | Initial release — 24 categories (School, Classroom, Library, Playground, Science, Math, Space, Ocean, Fantasy, Buildings, Furniture, Community Helpers, Music, Sports, Festival Decorations, Borders, Frames, Patterns, Icons, Badges, Certificates, Reward Stickers, Background Elements, Scene Templates) plus Master Asset Inventory. Grand total library across all 3 parts: ~3,072–3,974 assets. Production priority matrix and rate targets included. | Creative Director |
| | | | | |

## Future Revisions — Scheduled

| Target Version | Target Date | Planned Changes |
|----------------|-------------|-----------------|
| 1.1 | Q4 2026 | Add SVG code snippets for each structural category; add production batch scripts |
| 1.2 | Q1 2027 | Add additional community helper roles (social worker, mental health counsellor, IT technician); add extended festival calendar (Nowruz, Vesak, Onam) |
| 1.3 | Q2 2027 | Add digital/interactive variant standards for tablet-based product line |
| 2.0 | 2027 Annual Review | Full review against completed asset library; remove planned counts; replace with actual; add new categories from production experience |

---

## Dependencies

| Document | Relationship | Requirement |
|----------|-------------|-------------|
| WW-IB-001 | Parent document — ALL standards in this document inherit from Part 1 | ✅ Must read first |
| WW-IB-002 | Sibling — Part 2 character and subject library | ✅ Must read before building scenes |
| WW-DB-001 | Root design standards | ✅ Must read |
| WW-MC-001 | Curriculum — governs which environmental assets are needed and when | ✅ Reference throughout |
| WW-PS-100 | Production System — governs file naming, folder structure, and QA | ✅ Reference for asset delivery |

---

## Approval Page

```
══════════════════════════════════════════════════════════════
   WORKSHEET WONDER — ILLUSTRATION BIBLE PART 3
              MASTER APPROVAL PAGE
            WW-IB-003 | Version 1.0
══════════════════════════════════════════════════════════════

PREPARED BY:

  Name:              ____________________________
  Role:              Senior Art Director
  Date:              ____________________________
  Signature:         ____________________________

──────────────────────────────────────────────────────────────

REVIEWED BY (Lead Illustrator):

  Name:              ____________________________
  Role:              Lead Illustrator
  Date:              ____________________________
  Signature:         ____________________________
  Comments:          ____________________________

──────────────────────────────────────────────────────────────

REVIEWED BY (Production):

  Name:              ____________________________
  Role:              Production Manager / Publishing Director
  Date:              ____________________________
  Signature:         ____________________________
  Comments:          ____________________________

──────────────────────────────────────────────────────────────

REVIEWED BY (Educational):

  Name:              ____________________________
  Role:              Curriculum Director
  Date:              ____________________________
  Signature:         ____________________________
  Comments:          ____________________________

──────────────────────────────────────────────────────────────

APPROVED BY:

  Name:              ____________________________
  Role:              Creative Director
  Date:              ____________________________
  Signature:         ____________________________

  Decision:
    [ ] APPROVED — Active and mandatory
    [ ] CONDITIONAL — Minor revisions required before activation
    [ ] RETURNED — Major revision required

  Notes: ________________________________________________
         ________________________________________________

──────────────────────────────────────────────────────────────

FINAL SIGN-OFF:

  Name:              ____________________________
  Role:              Founder, Worksheet Wonder
  Date:              ____________________________
  Signature:         ____________________________

══════════════════════════════════════════════════════════════

           THE ILLUSTRATION BIBLE IS NOW COMPLETE.

   WW-IB-001  Foundation Standards & Visual Identity
   WW-IB-002  Character & Subject Illustration Library
   WW-IB-003  Settings, Structural Assets & Decoration

   Combined system: ~3,072–3,974 planned SVG assets
   across 46 categories, 3 documents, 1 visual language.

══════════════════════════════════════════════════════════════
```

---

```
══════════════════════════════════════════════════════════════

WORKSHEET WONDER — ILLUSTRATION BIBLE PART 3
WW-IB-003 | Version 1.0 | 10 July 2026

"Every setting is a stage. Every asset, a story."

(c) 2026 Worksheet Wonder. All Rights Reserved.

══════════════════════════════════════════════════════════════
```
