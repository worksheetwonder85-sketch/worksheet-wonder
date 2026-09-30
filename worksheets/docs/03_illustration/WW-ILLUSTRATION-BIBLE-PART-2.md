# WORKSHEET WONDER
## ILLUSTRATION BIBLE — PART 2
### The Complete Reusable Illustration Library Standards

---

```
══════════════════════════════════════════════════════════════

                 Worksheet Wonder Documentation

══════════════════════════════════════════════════════════════

  Document ID:         WW-IB-002

  Document Name:       Worksheet Wonder Illustration Bible — Part 2

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
                       WW-IB-003  (Illustration Bible — Part 3)
                       WW-PS-100  (Production System)

══════════════════════════════════════════════════════════════
```

> **This document defines the complete reusable illustration library for
> Worksheet Wonder — 22 subject categories, thousands of assets,
> one consistent visual language.**
> Read WW-IB-001 before this document. These standards build on that foundation.

---

## TABLE OF CONTENTS

| Category | Title | Est. Assets |
|----------|-------|-------------|
| 01 | Animals | 120–150 |
| 02 | Birds | 60–80 |
| 03 | Sea Animals | 70–90 |
| 04 | Dinosaurs | 50–70 |
| 05 | Insects | 50–70 |
| 06 | Pets | 50–60 |
| 07 | Kids | 150–200 |
| 08 | Parents | 60–80 |
| 09 | Teachers | 50–70 |
| 10 | Family | 60–80 |
| 11 | Alphabet Characters | 78–104 |
| 12 | Number Characters | 60–80 |
| 13 | Shapes | 80–100 |
| 14 | Vehicles | 80–100 |
| 15 | Food | 100–130 |
| 16 | Fruits | 60–80 |
| 17 | Vegetables | 60–80 |
| 18 | Flowers | 50–70 |
| 19 | Trees | 40–60 |
| 20 | Nature | 80–100 |
| 21 | Weather | 60–80 |
| 22 | Seasons | 60–80 |
| **TOTAL** | | **~1,530–1,954** |

---

## HOW TO USE THIS DOCUMENT

Each category entry in this document defines:

1. **Illustration Philosophy** — Why this category exists and what role it plays
2. **Visual Style** — Specific style rules on top of WW-IB-001 global standards
3. **Expression Library** — Applicable expressions from the approved nine (WW-IB-001 §7)
4. **Pose Library** — Approved poses and actions for this category
5. **Line Weight** — Which L1–L5 levels apply and any category-specific rules
6. **SVG Standards** — Category-specific SVG construction rules
7. **Reusable Parts** — Which elements are modular and interchangeable
8. **Black & White Printing Rules** — Tonal assignments specific to this category
9. **Colour Version Rules** — Approved colour assignments
10. **Asset Naming Convention** — Category-specific file naming
11. **Estimated Asset Count** — Target production count
12. **Commercial Usage Notes** — Notes on commercial sensitivity, cultural considerations

---

---

# CATEGORY 01 — ANIMALS

## 1.1 Illustration Philosophy

Animals are the most universally loved illustration category in educational publishing. They appear in every subject area — counting sheep in maths, labelling a frog in science, reading a story about a rabbit in literacy. The Worksheet Wonder animal library must be large, diverse, and instantly recognisable.

Animals in our system serve two distinct roles:
- **Realistic-style animals** — For science, nature, and identification activities
- **Anthropomorphic/cartoon animals** — For narrative, character, and motivational roles

Both styles must be consistent with the WW visual language. Both must be pedagogically honest.

## 1.2 Visual Style

| Attribute | Realistic-Style | Anthropomorphic |
|-----------|----------------|-----------------|
| Proportions | Accurate silhouette; simplified detail | Child-character proportions (WW-IB-001 §6.3) |
| Features | Correct anatomical features simplified | Large expressive eyes; reduced snout |
| Posture | Natural animal posture | Upright; 2-legged stance where appropriate |
| Expression | Neutral or mild suggestion of expression | Full expression library available |
| Complexity | Medium — enough detail to be identifiable | Simple — emotion-first design |

**All animals — regardless of style — follow:**
- Rounded, soft forms (no sharp aggressive edges)
- L1 primary outline with L3 internal detail
- Minimum 8mm height at A4 print size
- `stroke-linecap="round"` and `stroke-linejoin="round"` on all strokes

## 1.3 Expression Library (Anthropomorphic Only)

| Expression | Available? | Notes |
|------------|-----------|-------|
| Happy (Default) | ✅ | Primary expression for most activities |
| Excited | ✅ | For celebration, reward moments |
| Proud | ✅ | For achievement-related scenes |
| Curious | ✅ | For discovery, science activities |
| Concentrating | ✅ | When depicted working/doing a task |
| Surprised | ✅ | For "aha!" moments |
| Encouraging | ✅ | For motivational positions |
| Thinking | ✅ | For problem-solving activities |
| Welcoming | ✅ | For introduction/cover pages |

Realistic animals: expression is limited to neutral pose with eye highlight for warmth.

## 1.4 Pose Library

### Realistic-Style Animals
| Pose | Use |
|------|-----|
| Standing profile (right-facing) | Default; science labels; identification |
| Standing front-facing | Eye contact; character moments |
| Seated/resting | Nature scenes; calm activities |
| In motion (mid-stride) | Action scenes; sequencing |
| Eating/feeding | Life science; habitat activities |
| Baby/juvenile version | Life cycle sequences |

### Anthropomorphic Animals
| Pose | Use |
|------|-----|
| Standing upright, arms wide | Welcome; celebration |
| Pointing (one arm extended) | Instruction; guidance |
| Running/mid-stride | Energy; active scenes |
| Seated at desk | Writing/learning activities |
| Holding object (pencil, book) | Learning-in-action |
| Waving | Greeting; cover pages |
| Thinking pose (hand to chin) | Problem-solving activities |

## 1.5 Line Weight

| Element | Weight Level |
|---------|-------------|
| Primary silhouette outline | L1 (2.5px) |
| Major body divisions (leg/body/head) | L2 (2.0px) |
| Facial features (eyes, nose, mouth) | L3 (1.5px) |
| Fur/feather/scale texture lines | L4 (1.0px) |
| Ground shadow | L5 (0.75px) |

## 1.6 SVG Standards

```
Standard viewBox sizes for animals:
  Small icon:    0 0 64 64   (used in icon rows, small rewards)
  Standard:      0 0 120 120 (used in activity illustrations)
  Large:         0 0 200 200 (used in science diagram context)
  Scene:         0 0 300 200 (used in habitat/environment scenes)

Required group structure:
  <g id="animal--[species]--shadow">
  <g id="animal--[species]--body">
  <g id="animal--[species]--head">
  <g id="animal--[species]--face">
  <g id="animal--[species]--markings">  (spots, stripes, patches)

Tails: drawn as separate <path> element (modular — can be removed)
```

## 1.7 Reusable Parts

| Part | Reusable Across |
|------|-----------------|
| Eye system (white + iris + pupil + highlight) | All animal characters |
| Ground shadow ellipse | All animals standing on ground |
| Body base shape | Animals in same size class |
| Ear shapes | Similar species groups |
| Tail shapes | Species families |

## 1.8 Black & White Printing Rules

| Body Zone | B&W Tone |
|-----------|----------|
| Main body (light-coloured animals) | #f0f0f0 (near-white) |
| Main body (dark-coloured animals) | #888888 (mid-grey) |
| Markings/patterns | #555555 (dark) or white |
| Nose/muzzle area | #cccccc (light) |
| Eyes | White + black pupil (standard) |
| Ground shadow | #dddddd (very light grey ellipse) |

## 1.9 Colour Version Rules

| Animal Type | Primary Colour | Accent | Eyes |
|-------------|---------------|--------|------|
| Farm animals | Natural tan/brown/white | Pink snout | Brown or blue |
| Wild mammals | Natural brown/grey/tawny | Markings as per species | Dark brown |
| Reptiles | Mid-green or brown | Lighter belly | Yellow-amber |
| Amphibians | Bright green or orange | Lighter belly | Large gold/black |
| All cartoon | Character-distinguishing colour | Brand palette accent | Per character design |

## 1.10 Asset Naming Convention

```
WW--ANIMAL--[species]--[style]--[pose]--[size].svg

STYLE:  realistic | cartoon
POSE:   standing | seated | running | pointing | waving | eating | baby
SIZE:   sm | md | lg

Examples:
  WW--ANIMAL--cat--cartoon--sitting--md.svg
  WW--ANIMAL--frog--realistic--standing--md.svg
  WW--ANIMAL--elephant--cartoon--waving--lg.svg
  WW--ANIMAL--frog--realistic--baby--sm.svg
```

## 1.11 Estimated Asset Count

| Sub-category | Assets |
|-------------|--------|
| Farm animals (cow, pig, sheep, horse, chicken, duck, goat, donkey) | 24–32 |
| Wild mammals (lion, elephant, giraffe, zebra, bear, fox, rabbit, deer) | 24–32 |
| Australian animals (kangaroo, koala, platypus, wombat) | 12–16 |
| Pets (covered in Category 06) | — |
| Reptiles (snake, lizard, turtle, crocodile) | 12–16 |
| Amphibians (frog, toad, salamander) | 8–10 |
| Rodents (mouse, hamster, squirrel, beaver) | 12–16 |
| Arctic/polar animals (polar bear, penguin, arctic fox, seal) | 12–16 |
| **TOTAL** | **~120–150** |

## 1.12 Commercial Usage Notes

- Avoid any breed-specific animal representation that could be culturally insensitive
- Predator/prey scenes are shown without aggression; never show hunting, killing, or predation
- Baby animals are always depicted as safe, protected, and with parent nearby in scene-based illustrations
- All species must be identifiable — do not abstract to the point of ambiguity

---

---

# CATEGORY 02 — BIRDS

## 2.1 Illustration Philosophy

Birds appear across science (life cycles, migration, habitats), literacy (story characters), maths (counting), and environmental themes. The bird library must include both identifiable realistic birds and charming cartoon birds.

## 2.2 Visual Style

| Attribute | Specification |
|-----------|---------------|
| Body shape | Rounded egg-body; never elongated or raptor-like for preschool/KG |
| Beak | Short and stubby (preschool); anatomically appropriate (Grade 3+) |
| Wings | Clearly defined; at rest folded neatly; in flight spread symmetrically |
| Feet | Simple two- or three-toed talons; rounded; never clawed in threatening way |
| Eyes | Standard WW-IB-001 eye system; birds have proportionally large eyes |
| Feathers | Suggested by light curved L4 strokes, not individually drawn |

## 2.3 Expression Library

Birds use the full expression library for anthropomorphic versions. Realistic birds: neutral + eye highlight only.

## 2.4 Pose Library

| Pose | Use |
|------|-----|
| Perched on branch (facing right) | Default science/nature |
| In flight (wings spread, side view) | Migration; freedom; aerial concepts |
| Standing on ground (front-facing) | Character/narrative |
| Nesting (in nest with eggs) | Life cycle; spring theme |
| Feeding (head down) | Nature observation |
| Singing (beak open, head tilted up) | Music; spring; joy themes |
| Chick (in nest, mouth open) | Life cycle sequences |

## 2.5 Line Weight, SVG Standards, Reusable Parts

Same as Category 01 with these additions:
- Wing feather edge: L4 (1.0px) curved strokes along wing trailing edge
- Beak is a separate `<path>` element (modular)
- Tail feathers are a separate `<g>` (modular by species)
- Standard viewBox: `0 0 120 120` for perched; `0 0 200 120` for in-flight (wide)

## 2.6 Black & White Rules

| Zone | Tone |
|------|------|
| Body (light birds: sparrow, seagull) | #f0f0f0 |
| Body (dark birds: crow, raven) | #555555 |
| Wing tips/markings | #888888 |
| Beak (yellow beaks) | #cccccc |
| Beak (orange beaks) | #888888 |
| Red breast (robin) | #888888 |
| Tail feathers | Slightly darker than body |

## 2.7 Asset Naming Convention

```
WW--BIRD--[species]--[style]--[pose]--[size].svg

Examples:
  WW--BIRD--robin--realistic--perched--md.svg
  WW--BIRD--owl--cartoon--waving--md.svg
  WW--BIRD--penguin--cartoon--standing--md.svg
  WW--BIRD--eagle--realistic--flying--lg.svg
```

## 2.8 Estimated Asset Count & Commercial Notes

| Sub-category | Assets |
|-------------|--------|
| Common birds (robin, sparrow, pigeon, seagull, duck) | 15–20 |
| Exotic birds (parrot, toucan, flamingo, peacock) | 12–16 |
| Nocturnal birds (owl, nightjar) | 8–10 |
| Large birds (eagle, hawk, pelican, ostrich) | 12–16 |
| Penguins (Antarctic theme) | 8–10 |
| Chicks and eggs (life cycle) | 8–10 |
| **TOTAL** | **~60–80** |

**Note:** Eagles and hawks are always shown in gentle, non-aggressive poses. No talons-forward attack poses.

---

---

# CATEGORY 03 — SEA ANIMALS

## 3.1 Illustration Philosophy

The ocean is one of the richest visual themes in educational content — used across science, geography, maths, and creative writing. Sea animals are inherently colourful, visually diverse, and universally engaging for children. Our sea animal library must be comprehensive enough to serve marine biology units, counting activities, and creative writing prompts.

## 3.2 Visual Style

| Attribute | Specification |
|-----------|---------------|
| Silhouette | Always clearly identifiable by outline alone |
| Body fluidity | All sea animals have flowing, curved forms — no sharp edges |
| Eyes | Large, proportionally oversized for cartoonisation; standard WW eye system |
| Fins/tentacles | Rounded tips; gentle curves; never sharp-pointed |
| Scale/texture | Suggested by scale-pattern L4 lines, not individual scales |
| Bubbles | Accompany most sea animal illustrations; simple circles with highlight |

## 3.3 Expression Library

Cartoon sea animals use the full expression library. Fish and jellyfish: simplified expression (eyes + mouth arc). Octopus/cuttlefish: full expression possible.

## 3.4 Pose Library

| Pose | Use |
|------|-----|
| Swimming profile (right-facing) | Default; science; counting |
| Swimming upward-diagonal | Dynamic; playful scenes |
| Front-facing | Character moments; eye contact |
| Jumping from water | Celebration; dynamic scenes (dolphin/orca/salmon) |
| On the seabed | Habitat scenes (crab, starfish, seahorse) |
| In seaweed | Hiding; nature observation |

## 3.5 SVG Standards

```
Bubble companion: every sea animal includes an optional
<g id="bubbles--[animal]"> group with 3–5 circles of varying size
positioned naturally above the animal.

Wave environment: use <path> sinusoidal wave at top of viewBox
for underwater scenes — L5 weight, #cccccc fill

ViewBox sizes:
  Standard:  0 0 120 120  (single animal)
  Wide:      0 0 300 200  (underwater scene)
```

## 3.6 Black & White Rules

| Animal | B&W Treatment |
|--------|---------------|
| Fish (generic) | #f0f0f0 body; #888888 fins; L4 scale lines |
| Octopus/squid | #cccccc body; L4 sucker dots on tentacles |
| Crab | #888888 shell; #cccccc claw tips |
| Jellyfish | #f0f0f0 dome; L5 trailing tentacle lines |
| Starfish | #cccccc solid; L4 texture dots |
| Whale | #888888 dark back; #f0f0f0 belly |
| Dolphin | #cccccc body; white belly |
| Shark | #888888 body — NOTE: shark must have closed friendly mouth |

## 3.7 Asset Naming Convention

```
WW--SEA--[species]--[style]--[pose]--[size].svg

Examples:
  WW--SEA--clownfish--cartoon--swimming--md.svg
  WW--SEA--dolphin--cartoon--jumping--lg.svg
  WW--SEA--crab--cartoon--waving--md.svg
  WW--SEA--whale--realistic--swimming--lg.svg
```

## 3.8 Estimated Asset Count

| Sub-category | Assets |
|-------------|--------|
| Common fish (clownfish, goldfish, angelfish, swordfish) | 12–16 |
| Marine mammals (dolphin, whale, seal, walrus, otter) | 15–20 |
| Molluscs (octopus, squid, clam, snail) | 10–12 |
| Crustaceans (crab, lobster, shrimp) | 8–10 |
| Echinoderms (starfish, sea urchin, sea cucumber) | 6–8 |
| Coral and reef (background elements) | 6–8 |
| Jellyfish and medusae | 6–8 |
| Shark (friendly, closed mouth only) | 4–6 |
| **TOTAL** | **~70–90** |

---

---

# CATEGORY 04 — DINOSAURS

## 4.1 Illustration Philosophy

Dinosaurs are among the highest-engagement subjects for children aged 4–10. They serve science units on prehistoric life, classification, and extinction, as well as creative writing and vocabulary activities. Worksheet Wonder dinosaurs are always designed as friendly, approachable characters — never as terrifying predators — while maintaining enough anatomical accuracy to be educational.

## 4.2 Visual Style

| Attribute | Specification |
|-----------|---------------|
| Size impression | Large body; small head (unlike child-character proportions) — except Triceratops/hadrosaurs |
| Expression | Default: Happy or Curious — never aggressive |
| Teeth | Visible teeth permitted only in smile; never bared in aggression |
| Horns/spikes | Rounded tips; not sharp-pointed |
| Texture | Smooth with L4 scale-pattern suggestions; no hyper-detailed scales |
| Stance | Bipedal dinosaurs: upright and stable; not menacing lean-forward posture |
| Quadrupedal: | Strong, stable stance; friendly face toward viewer |

## 4.3 Expression Library

Full expression library available. Concentrating and Thinking are especially useful for academic activity dinosaurs.

## 4.4 Pose Library

| Pose | Dinosaur Types |
|------|----------------|
| Standing profile (right-facing) | All types — default |
| Waving one arm | Bipedal (T-Rex, Raptor, Iguanodon) |
| Holding book/pencil | Bipedal — learning scenes |
| Running | Bipedal — energy/speed activities |
| Seated on ground | Bipedal — calm activities |
| Grazing/eating leaves | Quadrupedal long-neck (Brachiosaurus) |
| Standing protective with baby | Parent/child size comparison activities |

## 4.5 SVG Standards & Reusable Parts

```
Reusable: tail, spine ridges (Stegosaurus plates), eye system, ground shadow
Standard viewBox for single dinosaur: 0 0 200 200
Wide viewBox for scene (two dinosaurs): 0 0 400 200
```

## 4.6 B&W Rules and Colour Version

| Element | B&W | Colour |
|---------|-----|--------|
| Body | #cccccc | Variable (earth tones: green, brown, blue-grey) |
| Belly/lighter underside | #f0f0f0 | Lighter version of body colour |
| Horns/claws | #888888 | Dark grey-brown |
| Stegosaurus plates | #888888 with L4 lines | Terracotta, teal, or orange-red |

## 4.7 Asset Naming Convention

```
WW--DINO--[species]--[pose]--[size].svg

Examples:
  WW--DINO--triceratops--standing--md.svg
  WW--DINO--trex--waving--lg.svg
  WW--DINO--brachiosaurus--grazing--lg.svg
  WW--DINO--stegosaurus--standing--md.svg
```

## 4.8 Estimated Asset Count & Commercial Notes

| Species | Assets |
|---------|--------|
| T-Rex, Velociraptor, Spinosaurus (bipedal) | 12–18 |
| Triceratops, Stegosaurus, Ankylosaurus | 9–12 |
| Brachiosaurus, Diplodocus (long-neck) | 6–9 |
| Pterodactyl (flying) | 4–6 |
| Plesiosaur (water) | 4–6 |
| Baby/egg versions | 8–12 |
| Scene compositions | 6–8 |
| **TOTAL** | **~50–70** |

**Note:** All dinosaurs must pass the child safety review (WW-IB-001 §2.1, Law 1). Any pose that could be read as aggressive or threatening must be corrected before approval.

---

---

# CATEGORY 05 — INSECTS

## 5.1 Illustration Philosophy

Insects are essential to science curricula across all grade levels — from simple "living things" activities in Preschool to detailed life cycle and classification work in Grades 3–6. They are also popular decorative elements for nature themes. The insect library must be comprehensive, anatomically informed, and visually approachable.

## 5.2 Visual Style

| Attribute | Specification |
|-----------|---------------|
| Body segments | Clearly shown but simplified (head, thorax, abdomen as distinct rounded forms) |
| Legs | 6 legs (anatomically correct) simplified to clean curves; evenly spaced |
| Wings | Semi-transparent suggested by L4 lines on white fill; or simple filled outlines |
| Eyes | Compound eyes shown as large rounded ovoid forms; highlights included |
| Antennae | Simple curved lines with rounded ball tips; L3 weight |
| Expression | Full cartoon expression library for anthropomorphic insects; none for realistic |

## 5.3 Pose Library

| Pose | Use |
|------|-----|
| Standing on leaf (profile) | Default nature/science |
| In flight (wings spread) | Metamorphosis; pollination |
| On flower | Pollination activities |
| Digging/building (ant) | Social insects; behaviour |
| Spinning web (spider) | Life science — note: spiders are arachnids, not insects |
| Life cycle stages | Caterpillar, chrysalis, butterfly sequence |

## 5.4 Line Weight, SVG Standards, Reusable Parts

```
Reusable across insect species:
  - Eye system (shared module)
  - Antennae (2 curve paths with ball tip circles)
  - Ground shadow ellipse
  - Wing template (4-wing symmetric base)
  - Leg set (6 curved paths as a group)

ViewBox: 0 0 120 120 (standard)
         0 0 64 64 (icon size — for counting rows)
```

## 5.5 B&W Rules and Colour Assignments

| Insect | B&W Body | Colour |
|--------|----------|--------|
| Butterfly | #f0f0f0 wings; L4 wing pattern | Varied: orange/black; blue/white; yellow/black |
| Bee | #888888 striped; #cccccc between | Yellow + black stripes |
| Ladybird | #888888 body; white dots | Red + black spots |
| Caterpillar | #cccccc segments | Green with yellow segment rings |
| Ant | #555555 (dark) | Black or dark red-brown |
| Grasshopper | #cccccc; L4 leg joints | Mid-green |
| Dragonfly | #f0f0f0 body; L4 wing veins | Blue-teal body |

## 5.6 Asset Naming Convention

```
WW--INSECT--[species]--[style]--[pose]--[size].svg

Examples:
  WW--INSECT--butterfly--cartoon--flying--md.svg
  WW--INSECT--bee--cartoon--onflower--md.svg
  WW--INSECT--caterpillar--realistic--crawling--md.svg
  WW--INSECT--ant--cartoon--carrying--sm.svg
```

## 5.7 Estimated Asset Count

| Sub-category | Assets |
|-------------|--------|
| Butterflies + life cycle stages | 12–18 |
| Bees + honeycomb scene elements | 8–10 |
| Beetles (ladybird, stag, dung) | 6–8 |
| Ants + colony scene elements | 6–8 |
| Flying insects (dragonfly, mosquito, moth) | 8–10 |
| Garden insects (grasshopper, cricket, worm) | 6–8 |
| Spiders + web (arachnid — clearly labelled) | 4–6 |
| **TOTAL** | **~50–70** |

---

---

# CATEGORY 06 — PETS

## 6.1 Illustration Philosophy

Pets are emotionally resonant for nearly every child. Cats and dogs appear in early literacy, creative writing, social-emotional learning, and even maths activities. The pet library bridges realistic animal depictions and the fully anthropomorphic characters of the Kids/Family library.

## 6.2 Visual Style, Expressions, Poses

**Visual Style:** Blend of realistic anatomy with cartoon proportions. Larger eyes, rounder heads, shorter snouts than real animals. Full expression library for all pets.

**Key Poses:**
| Pose | Use |
|------|-----|
| Sitting (facing forward) | Default; character introduction |
| Playing with toy | Creative writing; energy |
| Sleeping/curled | Calm scenes; night theme |
| Running/mid-leap | Action scenes |
| With owner/child | Social-emotional; care themes |
| Wearing collar | Identity/name activities |

## 6.3 Asset Naming Convention

```
WW--PET--[species]--[breed-style]--[pose]--[size].svg

Examples:
  WW--PET--cat--tabby--sitting--md.svg
  WW--PET--dog--shaggy--running--md.svg
  WW--PET--rabbit--lop--eating--sm.svg
  WW--PET--goldfish--cartoon--swimming--sm.svg
```

## 6.4 Estimated Asset Count

| Pet | Assets |
|-----|--------|
| Cats (3 visual styles: tabby, fluffy, short-hair) | 12–15 |
| Dogs (4 visual styles: small, medium, large, fluffy) | 15–18 |
| Rabbits | 6–8 |
| Hamsters/guinea pigs | 6–8 |
| Pet fish/goldfish | 4–6 |
| Pet birds (budgie, canary) | 4–6 |
| **TOTAL** | **~50–60** |

---

---

# CATEGORY 07 — KIDS

## 7.1 Illustration Philosophy

Kid characters are the heart of the Worksheet Wonder illustration library. They appear on almost every worksheet — pointing, writing, celebrating, exploring, reading. They must be diverse, active, emotionally expressive, and perfectly proportioned for their represented age.

> **Cross-reference:** WW-IB-001 Chapter 06 (Character Proportions), Chapter 07 (Facial Expressions), Chapter 08 (Eye Design), Chapter 09 (Mouth Design), Chapter 10 (Hands & Feet)

## 7.2 Visual Style

All kid characters follow the full WW-IB-001 character system without exception:
- 8-unit head proportion grid (child proportions)
- Full nine-expression library
- Four hand type options by age
- Diverse skin tones (minimum 4 in any set): ST1 through ST7
- Diverse hair types: straight, wavy, curly, coiled
- Diverse body types: not all identical builds
- Ability representation: glasses, hearing aids appear naturalistically

## 7.3 Expression Library

Full nine-expression library — all expressions available for all characters. See WW-IB-001 Chapter 07.

## 7.4 Pose Library — Kids

| Pose ID | Pose | Primary Use |
|---------|------|-------------|
| KID-P-01 | Writing at desk (3/4 view) | Handwriting, literacy, maths worksheets |
| KID-P-02 | Reading book (seated) | Literacy, comprehension |
| KID-P-03 | Pointing right (standing) | Instruction arrows, guidance |
| KID-P-04 | Pointing down (standing) | "Start here" instruction |
| KID-P-05 | Running right | Energy, action, movement activities |
| KID-P-06 | Jumping with arms raised | Celebration, reward, achievement |
| KID-P-07 | Thinking pose (hand to chin, seated) | Problem-solving, assessment |
| KID-P-08 | Waving (standing) | Cover pages, introductions |
| KID-P-09 | Holding pencil up (displaying) | Pre-writing themes |
| KID-P-10 | Looking through magnifying glass | Science, investigation |
| KID-P-11 | Holding book forward (displaying) | Literacy, reading |
| KID-P-12 | Carrying backpack | School theme, beginning of year |
| KID-P-13 | Arms crossed, proud stance | Achievement, confidence |
| KID-P-14 | Mid-stride, forward lean | Purpose, direction |
| KID-P-15 | Seated on floor, legs crossed | Circle time, story time |
| KID-P-16 | Drawing/colouring (seated) | Art, creative activities |
| KID-P-17 | Counting on fingers | Maths, number activities |
| KID-P-18 | Standing with trophy/award | Achievement, reward |
| KID-P-19 | Clapping | Celebration, rhythm activities |
| KID-P-20 | Looking upward-left (thinking/recalling) | Assessment, question prompts |

## 7.5 Age Range Variants

| Age Variant | Grade Range | Proportion System | Notes |
|-------------|-------------|------------------|-------|
| Toddler | Preschool | Head:body = 1:3 | Maximum head size; mitten hands |
| Young child | Junior–Senior KG | Head:body = 1:4 | Large head; Type B hands |
| Child | Grade 1–3 | Head:body = 1:4.5 | Core child proportion; Type C hands |
| Older child | Grade 4–6 | Head:body = 1:5 | More elongated; Type C hands |
| Tween | Grade 7–8 | Head:body = 1:5.5 | Near-adult proportion |

## 7.6 Diversity Standard for Kid Sets

Any set of 6 or more kid characters must include:
- ≥ 4 distinct skin tones (from ST1–ST7)
- ≥ 2 hair types (from straight, wavy, curly, coiled)
- ≥ 1 character with visible accessibility feature (glasses, hearing aid, or similar)
- Mix of perceived gender expression (not all identical)

## 7.7 Asset Naming Convention

```
WW--CHAR--child-[gender-neutral|girl|boy]--[pose-id]--[skin-tone]--[size].svg

Gender: Use gender-neutral as default; girl/boy only when clothing/activity is gender-coded
Skin tone: st1 through st7
Pose: Use Pose Library IDs (KID-P-01 through KID-P-20)

Examples:
  WW--CHAR--child-gn--KID-P-01--st3--md.svg   (writing at desk, skin tone 3)
  WW--CHAR--child-gn--KID-P-06--st5--md.svg   (jumping celebration, skin tone 5)
  WW--CHAR--child-gn--KID-P-09--st1--sm.svg   (holding pencil, skin tone 1)
```

## 7.8 Estimated Asset Count

| Pose | Skin Tone Variants | Total Assets |
|------|-------------------|-------------|
| 20 poses | 4 skin tone variants per pose | 80 base |
| + Hair variation sets | — | 30–40 |
| + Age variant sets | Toddler/Tween extremes | 20–30 |
| + Ability variants | Glasses, hearing aids | 10–20 |
| Scene compositions | Multi-character | 10–15 |
| **TOTAL** | | **~150–200** |

---

---

# CATEGORY 08 — PARENTS

## 8.1 Illustration Philosophy

Parent characters appear in social studies, SEL, family theme activities, parent guides, and back-cover illustrations. They are warm, approachable, and diverse. Parents are never depicted as authoritarian or threatening.

## 8.2 Visual Style

Adult character proportions: WW-IB-001 §6.2 (7.0–7.5 units total height).

Parent characters are noticeably larger than child characters. In scenes with children, the size ratio communicates safety and support — not power or threat.

## 8.3 Expression Library

Full nine-expression library. Welcoming and Encouraging are the default expressions for parent characters.

## 8.4 Pose Library — Parents

| Pose | Use |
|------|-----|
| Standing, arms open (welcoming) | Cover pages, family themes |
| Kneeling to child level (helping) | SEL, homework help scenes |
| Reading to child (seated) | Literacy, story themes |
| Cooking with child | Life skills, maths measurement |
| Hugging child | SEL, emotional wellbeing |
| Waving | Greeting; school drop-off |
| Pointing (guiding) | Instruction support |

## 8.5 Diversity Standard for Parent Sets

- Minimum 4 skin tones across a set of 4+ parent characters
- Single parents, dual-parent families, and grandparent caregivers represented
- Father-figures and mother-figures equally represented
- A parent character with accessibility features (glasses, wheelchair) included

## 8.6 Asset Naming Convention

```
WW--CHAR--parent-[m|f|gn]--[pose]--[skin-tone]--[size].svg

Examples:
  WW--CHAR--parent-f--kneeling--st4--md.svg
  WW--CHAR--parent-m--reading--st2--md.svg
  WW--CHAR--parent-gn--waving--st6--md.svg
```

## 8.7 Estimated Asset Count: 60–80 assets

---

---

# CATEGORY 09 — TEACHERS

## 9.1 Illustration Philosophy

Teacher characters appear on teacher guides, instruction pages, and activity introductions. They must communicate warmth, authority, competence, and approachability in equal measure.

## 9.2 Visual Style, Expressions, Poses

**Default expression:** Welcoming or Encouraging

**Key Poses:**
| Pose | Use |
|------|-----|
| Standing at board/flipchart | Instruction scenes |
| Seated at desk | Administration/assessment context |
| Pointing to board | Teaching moments |
| Holding clipboard | Assessment/observation |
| Kneeling beside student | Support/guidance |
| Reading aloud (book raised) | Story time; literacy introduction |
| Thumbs up | Encouragement; reward section |

**Attire:** Classroom-appropriate: smart-casual; no uniform. Teacher characters wear a distinguishing visual marker (lanyard, glasses, or clipboard) to signal their role.

## 9.3 Asset Naming Convention

```
WW--CHAR--teacher-[m|f|gn]--[pose]--[skin-tone]--[size].svg

Examples:
  WW--CHAR--teacher-f--pointing-board--st3--lg.svg
  WW--CHAR--teacher-m--thumbsup--st6--md.svg
```

## 9.4 Estimated Asset Count: 50–70 assets

---

---

# CATEGORY 10 — FAMILY

## 10.1 Illustration Philosophy

Family illustrations serve social studies (families and communities), SEL (relationships, emotions), and creative writing (personal narratives). The Worksheet Wonder family library represents the full diversity of family structures: nuclear, single-parent, extended, blended, same-gender parent, grandparent-led, and foster/adoptive families.

## 10.2 Visual Style & Standards

Family group illustrations combine character components from Categories 07 (Kids), 08 (Parents), and introduce grandparent variants.

**Grandparent visual markers:**
- White or grey hair (H1 or H10 codes from WW-IB-001 §16.4)
- Slightly rounder posture (not hunched — dignified)
- Optional glasses, walking stick (drawn as mobility aid, not crutch-dependent)
- Same proportion grid as parent characters

**Family group composition rules:**
- Always ground all characters on the same floor plane
- Taller characters stand behind or beside shorter characters
- Children always at child height — never floating or out-of-scale
- No single "correct" family shape — all structures are illustrated with equal dignity

## 10.3 Pose Library — Family Groups

| Composition | Description |
|-------------|-------------|
| Family of 2 (parent + child) | Standing side by side, one arm around |
| Family of 3 (parents + child) | Triangle composition |
| Family of 4 (2 parents + 2 children) | Row or V-shape composition |
| Multi-generational (grandparent + parent + child) | 3-tier height composition |
| Extended family (5+ members) | Wide scene composition |

## 10.4 Asset Naming Convention

```
WW--SCENE--family--[composition]--[skin-tone-range]--[size].svg

Examples:
  WW--SCENE--family--parent-child--st3-st3--lg.svg
  WW--SCENE--family--foursome--st1-st5--xl.svg
  WW--SCENE--family--multigenerational--st6--lg.svg
```

## 10.5 Estimated Asset Count: 60–80 assets

---

---

# CATEGORY 11 — ALPHABET CHARACTERS

## 11.1 Illustration Philosophy

Alphabet characters are letters given personality — turning the abstract symbol into a memorable, warm character. Used in phonics worksheets, alphabet charts, and literacy activities from Preschool through Grade 1. Each letter has a consistent visual identity across all uses.

## 11.2 Visual Style

| Attribute | Specification |
|-----------|---------------|
| Base | Each character is built ON the letter form — the letter IS the body |
| Letter style | Based on the WW display letterform (Fredoka One-inspired, rounded) |
| Eyes | Placed within or directly on the letter form |
| Arms | Short curved strokes extending from letter |
| Legs | Small rounded stubs below the letter baseline |
| Expression | Happy (default); Excited (for featured/title use) |
| Keyword | Each letter character is always paired with its keyword illustration |

## 11.3 Alphabet Character Set Specification

| Version | Description | Count |
|---------|-------------|-------|
| Uppercase character (A–Z) | Full 26 characters | 26 |
| Lowercase character (a–z) | Full 26 characters | 26 |
| Uppercase + keyword pair | Letter + keyword object illustration | 26 |
| **Base set total** | | **78** |
| Festive/seasonal variants | Holiday-themed letter characters | +26 |
| **Full extended set** | | **~104** |

## 11.4 Asset Naming Convention

```
WW--ALPHA--[letter]--[case]--[variant]--[size].svg

Examples:
  WW--ALPHA--A--upper--standard--md.svg
  WW--ALPHA--b--lower--standard--sm.svg
  WW--ALPHA--C--upper--withkeyword--lg.svg  (shows C + cat illustration)
  WW--ALPHA--s--lower--seasonal--md.svg
```

## 11.5 Estimated Asset Count: 78–104 assets

---

---

# CATEGORY 12 — NUMBER CHARACTERS

## 12.1 Illustration Philosophy

Number characters transform numerals 0–9 into memorable personalities. Used in early numeracy from Preschool through Grade 1. Each number character has a consistent visual design referencing its numeral form.

## 12.2 Visual Style

Same system as alphabet characters (Category 11), built ON the numeral form with eyes, arms, and legs added.

| Number | Character personality theme |
|--------|-----------------------------|
| 0 | Round, bouncy, open |
| 1 | Tall, proud, pointing upward |
| 2 | Curious, leaning forward |
| 3 | Cheerful, double-curved |
| 4 | Angular but friendly |
| 5 | Energetic, belly-forward |
| 6 | Swirling, playful |
| 7 | Tall, diagonal, adventurous |
| 8 | Symmetrical, twins-like |
| 9 | Curly-tailed, cheerful |

## 12.3 Number Character Set Specification

| Version | Description | Count |
|---------|-------------|-------|
| Standard 0–9 | Each numeral as character | 10 |
| With objects (quantity shown) | Character + dots/objects = the quantity | 10 |
| Paired with ten-frame | Character + ten-frame template | 10 |
| Number word pairs | Numeral character + word character (e.g., 5 + "five") | 10 |
| Operational symbols (+, -, ×, ÷, =) as characters | 5 |
| **Base total** | | **~45** |
| Extended (teen numbers 10–20) | — | +15 |
| **Full set** | | **~60–80** |

## 12.4 Asset Naming Convention

```
WW--NUM--[numeral]--[variant]--[size].svg

Examples:
  WW--NUM--5--standard--md.svg
  WW--NUM--3--withobjects--lg.svg
  WW--NUM--0--tenframe--md.svg
  WW--NUM--plus--symbol--sm.svg
```

---

---

# CATEGORY 13 — SHAPES

## 13.1 Illustration Philosophy

Shapes serve both direct mathematical education (geometry) and decorative/structural purposes across the catalogue. The shape library includes pure geometric shapes, shape characters (anthropomorphised), and shape-in-environment illustrations.

## 13.2 Visual Style

**Pure Geometry (Maths context):** Mathematically precise using SVG primitives. Rendered with L2 stroke only; minimal fill. Labels optional.

**Shape Characters (Early years):** Shapes with eyes, arms, and expression — following the same character approach as Alphabet Characters (Category 11).

**Shape in Environment:** Shapes appearing as objects in scenes (a triangular mountain, a circular sun, a rectangular door).

## 13.3 Shape Library

| Shape | Geometric Version | Character Version | In-Environment |
|-------|-----------------|------------------|----------------|
| Circle | ✅ | ✅ | Sun, wheel, ball |
| Square | ✅ | ✅ | Block, window, tile |
| Rectangle | ✅ | ✅ | Door, book, brick |
| Triangle | ✅ | ✅ | Mountain, roof, arrow |
| Oval/Ellipse | ✅ | ✅ | Egg, mirror, lake |
| Diamond | ✅ | ✅ | Kite, gem |
| Pentagon | ✅ | — | Sign, house shape |
| Hexagon | ✅ | — | Honeycomb, tile |
| Star (5-point) | ✅ | ✅ | Star badge, sparkle |
| Heart | ✅ | ✅ | SEL themes |
| Arrow shapes | ✅ | — | Direction |
| 3D Shapes (cube, sphere, cone, cylinder, pyramid) | ✅ | — | Science, architecture |

## 13.4 Asset Naming Convention

```
WW--SHAPE--[shape]--[version]--[size].svg

VERSION: geo | char | env
Examples:
  WW--SHAPE--circle--geo--md.svg
  WW--SHAPE--triangle--char--md.svg
  WW--SHAPE--hexagon--geo--sm.svg
  WW--SHAPE--cube--geo--md.svg  (3D)
```

## 13.5 Estimated Asset Count: 80–100 assets

---

---

# CATEGORY 14 — VEHICLES

## 14.1 Illustration Philosophy

Vehicles appear across maths (counting, sorting), social studies (community helpers, transport), science (forces, motion), and creative writing. Vehicle illustrations must be friendly, identifiable, and consistent with the Worksheet Wonder visual language.

## 14.2 Visual Style

| Attribute | Specification |
|-----------|---------------|
| Silhouette | Instantly recognisable by outline; distinctive proportions |
| Windows | Large rounded rectangles; light fill; no occupants visible (unless intentional) |
| Wheels | Circles; concentric rings for tyre + hub; rounded spoke lines |
| Friendly face | Optional for preschool/KG — adds eyes and smile to headlights |
| Lines | Clean mechanical lines softened with rounded corners (rx minimum 4) |
| Direction | Always facing right by default; flip variant available |

## 14.3 Vehicle Library

| Category | Vehicles |
|----------|---------|
| Road (small) | Car, bike, scooter, motorbike |
| Road (large) | Bus, truck, lorry, ambulance, fire engine, police car |
| Construction | Digger, bulldozer, crane, dumper truck |
| Emergency | Ambulance, fire engine, police car (also in road) |
| Air | Aeroplane, helicopter, hot air balloon, rocket |
| Water | Boat, ferry, submarine, sail boat, speedboat |
| Rail | Train, tram, underground/metro |
| Special | Tractor, ice cream truck, recycling truck, school bus |

## 14.4 Asset Naming Convention

```
WW--VEH--[type]--[style]--[direction]--[size].svg

STYLE:   plain | with-face (friendly eyes on headlights)
DIR:     right | left | front

Examples:
  WW--VEH--car--plain--right--md.svg
  WW--VEH--bus--with-face--right--lg.svg
  WW--VEH--rocket--plain--up--lg.svg
  WW--VEH--train--plain--right--xl.svg
```

## 14.5 Estimated Asset Count: 80–100 assets

---

---

# CATEGORY 15 — FOOD

## 15.1 Illustration Philosophy

Food illustrations appear in maths (fractions, measurement, sorting), science (nutrition, food groups), social studies (culture), and general activities. The food library covers complete meals, individual items, and food group classifications.

## 15.2 Visual Style

| Attribute | Specification |
|-----------|---------------|
| Form | Plump, rounded forms; never flat or angular |
| Surface | L4 texture suggestions (bread grain, orange peel texture, etc.) |
| Colour richness | Among the most vibrant colour uses in the WW library |
| Steam | Optional animated suggestion (curved L5 lines above hot food) |
| Plating | Food shown on plate/in bowl when serving context; standalone for ingredient context |
| Expression | Optional "happy food" character (eyes + smile) for preschool/KG |

## 15.3 Food Category Library

| Group | Items | Est. Assets |
|-------|-------|------------|
| Grains & Bread | Bread, pasta, rice, cereal, toast, crackers | 12–15 |
| Proteins | Egg, chicken, fish, beans, meat, nuts | 12–15 |
| Dairy | Milk, cheese, yoghurt, butter, ice cream | 8–10 |
| Sweets/Treats | Cake, cupcake, biscuit, chocolate, lollipop, doughnut | 12–15 |
| Meals | Sandwich, pizza, burger, soup, salad, spaghetti | 12–15 |
| Drinks | Water, juice, milk, hot chocolate, smoothie | 8–10 |
| **TOTAL** | | **~64–80** |

## 15.4 Asset Naming Convention

```
WW--FOOD--[item]--[style]--[size].svg

STYLE: plain | with-face | on-plate

Examples:
  WW--FOOD--pizza--plain--md.svg
  WW--FOOD--apple--with-face--sm.svg
  WW--FOOD--cake--on-plate--lg.svg
  WW--FOOD--sandwich--plain--md.svg
```

## 15.5 Estimated Total (Food + Fruits + Vegetables combined): ~100–130 assets

---

---

# CATEGORY 16 — FRUITS

## 16.1 Visual Style & Standards

Fruits are among the highest-frequency illustrations in the library — appearing in counting, sorting, vocabulary, and cultural activities across all grade levels.

**Style:** Plump and rounded; bright in colour; cross-section variants available for science/nutrition activities.

**Cross-section variant:** Shows internal seed pattern; used in science and health worksheets.

## 16.2 Fruit Library

| Fruit | Variants Available |
|-------|--------------------|
| Apple | Whole; halved; with face |
| Banana | Whole; peeled; bunch |
| Orange | Whole; halved; segmented |
| Strawberry | Whole; halved |
| Grapes | Bunch; individual |
| Watermelon | Whole; slice; wedge |
| Pineapple | Whole |
| Mango | Whole; halved |
| Lemon | Whole; halved |
| Cherry | Single; pair |
| Blueberries | Bunch |
| Pear | Whole |
| Peach | Whole |
| Kiwi | Whole; halved |

## 16.3 Asset Naming Convention

```
WW--FRUIT--[name]--[variant]--[size].svg

VARIANT: whole | halved | slice | bunch | with-face

Examples:
  WW--FRUIT--apple--whole--md.svg
  WW--FRUIT--orange--halved--md.svg
  WW--FRUIT--watermelon--slice--lg.svg
  WW--FRUIT--banana--bunch--md.svg
```

## 16.4 Estimated Asset Count: 60–80 assets

---

---

# CATEGORY 17 — VEGETABLES

## 17.1 Visual Style & Standards

Same principles as fruits. Vegetables appear in science (plants, food groups), maths, and cultural activities.

**Special consideration:** Root vegetables are shown both as grown (above ground with leaves) and as the root portion alone — important for plant science activities.

## 17.2 Vegetable Library

| Vegetable | Notes |
|-----------|-------|
| Carrot | Whole with tops; cross-section |
| Broccoli | Floret; stem visible |
| Corn/Maize | Whole; husk on/off |
| Pea pod | Closed pod; open with peas |
| Tomato | Whole; halved (technically fruit, categorised here) |
| Potato | Whole; with sprouts (growth) |
| Onion | Whole; halved |
| Lettuce/cabbage | Head |
| Bean | Pod; individual bean |
| Pumpkin | Whole; carved (seasonal) |
| Cucumber | Whole; sliced |
| Bell pepper | Whole; halved |
| Mushroom | Whole (technically fungus, categorised here) |
| Spinach/Kale | Leaf form |

## 17.3 Asset Naming Convention

```
WW--VEG--[name]--[variant]--[size].svg

Examples:
  WW--VEG--carrot--whole--md.svg
  WW--VEG--carrot--crosssection--md.svg
  WW--VEG--pumpkin--carved--lg.svg
  WW--VEG--peasinpod--open--sm.svg
```

## 17.4 Estimated Asset Count: 60–80 assets

---

---

# CATEGORY 18 — FLOWERS

## 18.1 Illustration Philosophy

Flowers serve botanical science, seasons themes, spring activities, and decorative illustration roles. The flower library must be botanically recognisable while maintaining the WW visual warmth.

## 18.2 Visual Style

| Attribute | Specification |
|-----------|---------------|
| Petals | Rounded; evenly distributed; slight variation in size for organicism |
| Stem | Slightly curved; L2 weight |
| Leaves | Symmetrical; pointed-oval; L3 vein lines |
| Centre | Solid circle with L4 dot texture (pollen suggestion) |
| Roots | Shown for plant science activities; same style as stem |
| Expression | Happy face version available for preschool (eyes in centre circle) |

## 18.3 Flower Library

| Flower | Variants |
|--------|---------|
| Daisy | Whole; with face; in pot |
| Sunflower | Small; large; with seeds visible |
| Rose | Bud; full bloom; with leaves |
| Tulip | Whole; in field |
| Daffodil | Whole; in field |
| Poppy | Whole; with seed pod |
| Cherry blossom | Branch; single flower; in cluster |
| Dandelion | Full bloom; seed clock (seed-puff) |
| Lotus | Whole; on water |
| Generic flower (5-petal) | Whole; in pot; in field row |

## 18.4 Asset Naming Convention

```
WW--FLOWER--[name]--[variant]--[size].svg

Examples:
  WW--FLOWER--sunflower--large--lg.svg
  WW--FLOWER--daisy--with-face--sm.svg
  WW--FLOWER--dandelion--seedclock--md.svg
  WW--FLOWER--cherryblossom--branch--xl.svg
```

## 18.5 Estimated Asset Count: 50–70 assets

---

---

# CATEGORY 19 — TREES

## 19.1 Illustration Philosophy

Trees serve multiple subjects: science (plant types, photosynthesis, forest habitats), geography (biomes), seasons (deciduous trees showing seasonal change), and creative writing (settings). Trees must be identifiable by type and seasonally variant.

## 19.2 Visual Style

| Attribute | Specification |
|-----------|---------------|
| Trunk | Tapered cylinder; L2 weight; bark texture with L4 vertical strokes |
| Canopy | Rounded cloud-shape for deciduous; geometric for coniferous |
| Roots | Visible in cross-section/soil science context |
| Seasonal variants | Same tree silhouette, different canopy: full leaf, sparse, bare, snow-covered, blossom |
| Scale | Always implies being larger than human by proportion to character when both appear |

## 19.3 Tree Library

| Tree | Seasonal Variants |
|------|------------------|
| Oak | Spring blossom; summer full leaf; autumn orange; winter bare |
| Pine/Christmas tree | Summer; snow-covered; decorated |
| Apple tree | Blossom; fruit; bare |
| Palm tree | Year-round (tropical) |
| Cherry blossom tree | Bloom; leaf; bare |
| Birch tree | White bark distinctive; leaf; bare |
| Willow tree | Cascading branches; by water |
| Cactus (desert) | Tall single; multi-arm |
| Coconut palm | With coconuts; tropical |
| Generic round tree | Multi-purpose filler |

## 19.4 Asset Naming Convention

```
WW--TREE--[species]--[season]--[size].svg

SEASON: spring | summer | autumn | winter | bare | blossoming | fruiting

Examples:
  WW--TREE--oak--summer--lg.svg
  WW--TREE--oak--bare--lg.svg
  WW--TREE--appletree--fruiting--lg.svg
  WW--TREE--pine--snowcovered--lg.svg
```

## 19.5 Estimated Asset Count: 40–60 assets

---

---

# CATEGORY 20 — NATURE

## 20.1 Illustration Philosophy

The broader nature library covers environmental and landscape elements that provide the setting for science, geography, and creative writing activities. These are background, context, and scene-building elements.

## 20.2 Nature Asset Sub-categories

| Sub-category | Items | Est. Assets |
|-------------|-------|------------|
| Landscapes | Meadow, forest, desert, mountain, beach, arctic, jungle, swamp | 16–20 |
| Water features | River, lake, waterfall, stream, pond, ocean horizon | 10–12 |
| Sky elements | Clouds (types), sun, moon, stars, rainbow, northern lights | 12–16 |
| Ground elements | Soil cross-section, grass tuft, rock, boulder, pebbles, sand | 10–12 |
| Environmental | Leaf (fallen), acorn, pine cone, feather, mushroom, nest with eggs | 12–16 |
| Habitats | Burrow, nest, beehive, anthill, coral reef, tree hollow | 8–10 |
| **TOTAL** | | **~68–86** |

## 20.3 Asset Naming Convention

```
WW--NATURE--[category]--[item]--[variant]--[size].svg

Examples:
  WW--NATURE--sky--cloud--fluffy--md.svg
  WW--NATURE--ground--soilcross--labelled--lg.svg
  WW--NATURE--habitat--beehive--plain--md.svg
  WW--NATURE--landscape--mountain--winter--xl.svg
```

## 20.4 Estimated Asset Count: 80–100 (including extended library)

---

---

# CATEGORY 21 — WEATHER

## 21.1 Illustration Philosophy

Weather illustration appears across science (weather systems, water cycle), geography (climate), seasons activities, and daily observation worksheets. The weather library must cover all major weather types with both symbolic/icon representations and detailed scene representations.

## 21.2 Weather Icon System

All weather icons follow a consistent icon style:
- `viewBox="0 0 64 64"` (standard icon grid)
- L1 outline only; simple interior detail
- Friendly, non-threatening — even stormy weather is depicted warmly
- Expression optional (smiling sun, cheerful cloud)

## 21.3 Weather Library

| Weather Type | Icon | Scene | Animated Variant |
|-------------|------|-------|-----------------|
| Sunny / Clear | ✅ | ✅ | ✅ (rotating rays) |
| Partly cloudy | ✅ | ✅ | — |
| Overcast | ✅ | ✅ | — |
| Rainy / Light rain | ✅ | ✅ | ✅ (falling drops) |
| Heavy rain | ✅ | ✅ | — |
| Thunderstorm | ✅ | ✅ | — |
| Snowy | ✅ | ✅ | ✅ (falling flakes) |
| Windy | ✅ | ✅ | — |
| Foggy / Misty | ✅ | ✅ | — |
| Rainbow | ✅ | ✅ | — |
| Hail | ✅ | — | — |
| Tornado | ✅ (stylised, safe-looking) | — | — |
| Sunrise / Sunset | ✅ | ✅ | — |
| Night / Clear sky | ✅ | ✅ | — |

## 21.4 Weather Character System

Each major weather type has a character variant (preschool/KG):
- **Sunny Sam** — Sun with face; happy; ray arms
- **Cloudy Claude** — Cloud with face; content expression
- **Rainy Ray** — Cloud with umbrella and face; gentle expression
- **Snowy Stella** — Snowflake with face; excited expression
- **Windy Wren** — Swirl form with face; playful expression

## 21.5 Asset Naming Convention

```
WW--WEATHER--[type]--[variant]--[size].svg

VARIANT: icon | scene | character

Examples:
  WW--WEATHER--sunny--icon--sm.svg
  WW--WEATHER--rainy--scene--lg.svg
  WW--WEATHER--snow--character--md.svg
  WW--WEATHER--thunder--icon--sm.svg
```

## 21.6 Estimated Asset Count: 60–80 assets

---

---

# CATEGORY 22 — SEASONS

## 22.1 Illustration Philosophy

Seasons content is used across science (seasonal change, Earth's orbit), social studies (calendar, festivals), environmental education, and creative writing. Season illustrations must communicate the visual essence of each season instantly and joyfully.

## 22.2 Season Visual Identity

| Season | Key Visual Elements | Colour Palette | Dominant Shapes |
|--------|-------------------|----------------|-----------------|
| **Spring** | Blooming flowers, green shoots, baby animals, rain + sun, nests | Green, pink, yellow, sky blue | Circles (flowers), arches (rainbow), ovals (eggs) |
| **Summer** | Bright sun, beach, lush trees, ice cream, insects, long days | Bright yellow, aqua, coral orange, white | Circles (sun, balls), waves (water) |
| **Autumn / Fall** | Falling leaves, harvest vegetables, warm oranges, bare branches | Orange, red, brown, gold, burgundy | Organic leaf shapes, ovals (pumpkin), arcs (branches) |
| **Winter** | Snow, bare trees, warm clothing, ice, snowflakes | White, grey-blue, dark blue, silver, warm red accents | Hexagons (snowflakes), circles (snowballs), rectangles (sleds) |

## 22.3 Season Illustration Types

For each of the four seasons, the library provides:

| Asset Type | Description |
|------------|-------------|
| Season icon | Simple 64×64 symbol representing the season |
| Season scene | Full landscape scene, 300×200 viewBox |
| Season character | Child character dressed for the season |
| Season word card | "Spring" etc. with decorative seasonal elements |
| Season change strip | 4-panel horizontal showing all 4 seasons (tree across seasons) |
| Calendar elements | Monthly icons (12 icons, one per month) |
| Festival/event markers | Key events within each season (covered in WW-IB-003) |

## 22.4 Asset Naming Convention

```
WW--SEASON--[season]--[asset-type]--[variant]--[size].svg

SEASON:    spring | summer | autumn | winter
ASSET:     icon | scene | character | wordcard | strip | calendar

Examples:
  WW--SEASON--spring--icon--plain--sm.svg
  WW--SEASON--autumn--scene--full--xl.svg
  WW--SEASON--winter--character--girl-st3--md.svg
  WW--SEASON--all--strip--fourtree--xl.svg
  WW--SEASON--calendar--january--icon--sm.svg
```

## 22.5 Estimated Asset Count

| Season | Assets |
|--------|--------|
| Spring | 15–20 |
| Summer | 15–20 |
| Autumn | 15–20 |
| Winter | 15–20 |
| **TOTAL** | **~60–80** |

---

---

# MASTER ASSET COUNT SUMMARY

| Category | Min Assets | Max Assets |
|----------|-----------|-----------|
| 01 Animals | 120 | 150 |
| 02 Birds | 60 | 80 |
| 03 Sea Animals | 70 | 90 |
| 04 Dinosaurs | 50 | 70 |
| 05 Insects | 50 | 70 |
| 06 Pets | 50 | 60 |
| 07 Kids | 150 | 200 |
| 08 Parents | 60 | 80 |
| 09 Teachers | 50 | 70 |
| 10 Family | 60 | 80 |
| 11 Alphabet Characters | 78 | 104 |
| 12 Number Characters | 60 | 80 |
| 13 Shapes | 80 | 100 |
| 14 Vehicles | 80 | 100 |
| 15 Food | 64 | 80 |
| 16 Fruits | 60 | 80 |
| 17 Vegetables | 60 | 80 |
| 18 Flowers | 50 | 70 |
| 19 Trees | 40 | 60 |
| 20 Nature | 80 | 100 |
| 21 Weather | 60 | 80 |
| 22 Seasons | 60 | 80 |
| **GRAND TOTAL** | **~1,532** | **~1,954** |

> **Production note:** The complete library represents approximately 18–24 months of illustration production at a rate of 2–3 finished SVG assets per day. Prioritise Categories 07 (Kids), 01 (Animals), and 21 (Weather) as they appear most frequently across all worksheets.

---

---

# VERSION HISTORY

## Document Record

| Field | Detail |
|-------|--------|
| **Document ID** | WW-IB-002 |
| **Document Name** | Worksheet Wonder Illustration Bible — Part 2 |
| **Version** | 1.0 |
| **Date** | 10 July 2026 |
| **Author** | Senior Art Director |
| **Status** | Approved |
| **Approved By** | Creative Director, Worksheet Wonder |
| **Classification** | Internal — Confidential |

## Revision Log

| Version | Date | Author | Changes | Approved By |
|---------|------|--------|---------|-------------|
| 1.0 | 10 July 2026 | Senior Art Director | Initial release — 22 subject categories each with illustration philosophy, visual style, expression library, pose library, line weight specs, SVG standards, reusable parts, B&W rules, colour rules, naming conventions, estimated asset counts, and commercial notes. Grand total: ~1,532–1,954 assets planned. | Creative Director |
| | | | | |

## Future Revisions

| Target Version | Target Date | Planned Changes |
|----------------|-------------|-----------------|
| 1.1 | Q4 2026 | Add SVG code templates for each category's standard asset; add pose reference sketches |
| 1.2 | Q1 2027 | Add additional categories: Space, Ocean Environments, Classroom Objects, Sports, Musical Instruments |
| 1.3 | Q2 2027 | Add cultural variants for global market adaptation (South Asian, African, Latin American festivals and clothing) |
| 2.0 | 2027 Annual Review | Full review against completed asset library; update counts; add new categories from Part 3 |

---

## Dependencies

| Document | Relationship | Required Before Using This Document |
|----------|-------------|-------------------------------------|
| WW-IB-001 | Parent document — all standards in this document extend WW-IB-001 | ✅ Must read first |
| WW-DB-001 | Root design standards — colour palette, typography, border systems | ✅ Must read |
| WW-MC-001 | Curriculum — determines which categories are highest priority | ✅ Reference throughout |
| WW-PS-100 | Production system — determines how assets are filed and exported | ✅ Reference for naming |

---

## Approval Page

```
══════════════════════════════════════════════════════════════
   WORKSHEET WONDER — ILLUSTRATION BIBLE PART 2
              MASTER APPROVAL PAGE
            WW-IB-002 | Version 1.0
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
    [ ] CONDITIONAL — Minor revisions required
    [ ] RETURNED — Major revision required

══════════════════════════════════════════════════════════════
```

---

```
══════════════════════════════════════════════════════════════

WORKSHEET WONDER — ILLUSTRATION BIBLE PART 2
WW-IB-002 | Version 1.0 | 10 July 2026

"Every character is a promise. Every illustration, a gift."

(c) 2026 Worksheet Wonder. All Rights Reserved.

══════════════════════════════════════════════════════════════
```
