# WORKSHEET WONDER
## SVG LIBRARY ROADMAP
### The Official Illustration Production Roadmap & Asset Development Database

---

```
══════════════════════════════════════════════════════════════

                 Worksheet Wonder Documentation

══════════════════════════════════════════════════════════════

  Document ID:         WW-SL-100

  Document Name:       Worksheet Wonder SVG Library Roadmap

  Version:             1.0

  Status:              Approved

  Owner:               Worksheet Wonder

  Author:              Senior Illustration Production Manager

  Category:            Illustration Standards

  Last Updated:        14 July 2026

  Next Review:         14 January 2027

  Related Documents:   WW-DB-001  (Design Bible)
                       WW-MC-001  (Master Curriculum)
                       WW-IB-001  (Illustration Bible — Part 1)
                       WW-IB-002  (Illustration Bible — Part 2)
                       WW-IB-003  (Illustration Bible — Part 3)
                       WW-PS-100  (Production System)
                       WW-AS-100  (Digital Asset Registry)
                       WW-AI-100  (AI Prompt Handbook)

══════════════════════════════════════════════════════════════
```

> **This document is the official master roadmap for our vector illustration pipeline.**
> All graphic designers, animators, artists, and automation scripts must execute 
> asset creation and quality sign-off in accordance with these milestones.

---

## TABLE OF CONTENTS

| Chapter | Title |
|---------|-------|
| **01** | Production Philosophy & Scale Roadmap |
| **02** | Asset Categories & Folder Structure |
| **03** | Core Illustration Families & Metadata |
| **04** | Master Production Roadmap & Priority Matrix |
| **05** | Grade Usage Mapping (PSC to Grade 8) |
| **06** | Asset ID Allocation System |
| **07** | Production Milestones & Dashboard |
| **08** | QA Checklists for SVG Assets |
| **09** | Version History |
| **10** | Approval Page |

---

# 1. PRODUCTION PHILOSOPHY & SCALE ROADMAP

Our strategy revolves around **designing for reuse**. Rather than drawing individual standalone scene compositions from scratch, Worksheet Wonder assets are built as modular, nested layers. This allows us to scale our asset catalog to more than 10,000 unique vector resources with minimum drawing overhead.

## 1.1 The Nested Library Architecture

```
  [Level 01: Core Reusable Parts] (Eyes, mouths, hands, leaf outlines)
               │
               ▼
  [Level 02: Modular Characters & Props] (Complete kids, individual animals)
               │
               ▼
  [Level 03: Setting Assets & Backgrounds] (Classroom desks, trees, clouds)
               │
               ▼
  [Level 04: Full Scene Compositions] (Structured template worksheet pages)
```

## 1.2 Scaling Path to 10,000+ Assets
*   **Combinatorial Expansion:** An 8-head character base (Level 2) with 4 skin tone variations, 5 hair types, 9 expression sets, and 12 clothing colors yields over 2,160 unique variations from a single set of base vectors.
*   **Dynamic Asset Assembly:** Utilizing build scripts to inject varying vector elements (Level 1 parts) into base layouts (Level 2/3) dynamically generates specific worksheet illustrations at scale.

---

# 2. ASSET CATEGORIES & FOLDER STRUCTURE

All SVG assets must be organized into these five main folders inside the shared repository `assets/svg/`:

```
assets/svg/
├── characters/                    # Category: SVG-CHR (Kids, adults, mascots)
├── animals/                       # Category: SVG-ANI (Mammals, sea life, insects)
├── environments/                  # Category: SVG-ENV (Classroom, school, nature)
├── structural/                    # Category: SVG-STR (Borders, frames, patterns)
└── icons/                         # Category: SVG-ICN (Instruction, difficulty)
```

---

# 3. CORE ILLUSTRATION FAMILIES

We classify illustrations into families based on their complexity and target use:

| Category | Illustration Family | Est. Assets | Priority | Comp | Est. Hours | Reuse % | Dependencies |
|----------|---------------------|-------------|----------|------|------------|---------|--------------|
| **SVG-ICN** | Instruction Icons | 120 | P1 (High) | Low | 0.5 hrs | 95% | None |
| **SVG-STR** | Worksheet Borders | 60 | P1 (High) | Low | 1.0 hrs | 90% | None |
| **SVG-CHR** | Kids Poses Set | 200 | P1 (High) | Med | 2.5 hrs | 85% | Eyes, hands |
| **SVG-ANI** | Farm & Wild Animals | 150 | P2 (Med) | Med | 3.0 hrs | 75% | Eye library |
| **SVG-ENV** | Classroom Objects | 100 | P2 (Med) | Low | 1.5 hrs | 80% | Colors |
| **SVG-ENV** | Landscape Settings | 80 | P3 (Low) | High | 5.0 hrs | 60% | Trees, foliage |

---

# 4. MASTER PRODUCTION ROADMAP

## 4.1 Production Priority Matrix

```
       [P1: Core Setup] ────────────────► [P2: Subject Assets]
       - Instruction Icons                - Base animals & characters
       - Borders & Frames                 - Classroom environments
       - Grade Templates                  - Core math manipulatives
              │                                   │
              ▼                                   ▼
       [P4: Specialized Collections] ◄─── [P3: Thematic Settings]
       - World cultures                   - Science diagrams
       - Festival decorations             - Complex space & ocean scenes
```

---

# 5. GRADE USAGE MAPPING

The following matrix tracks asset requirements across grade levels:

| Grade | Primary Target Subject | Core Illustration Families Required | Unique Assets | Reuse |
|-------|------------------------|-------------------------------------|---------------|-------|
| **PSC** | Pre-Writing (PWS) | Tracing icons, basic animals, simple paths | 150 | 80% |
| **JKG** | Phonics (PHN) | Letter characters, CVC keywords | 200 | 75% |
| **SKG** | Phonics, Pre-Math | Number characters, ten-frame templates | 250 | 75% |
| **G01** | Math, ELA | Coins, clock faces, basic classroom maps | 300 | 70% |
| **G02** | Math, Science | Animal lifecycles, states of matter | 350 | 70% |
| **G03** | Math, Science | Fractions, solar system models | 400 | 65% |
| **G04** | Science, SST | Simple machines, world maps | 450 | 60% |
| **G05** | Science, SST | Human body organs, timeline grids | 500 | 60% |
| **G06** | Math, Science | Ratios visual, cell structures | 550 | 55% |
| **G07** | Science, ELA | Periodic table, story plot mapping | 600 | 50% |
| **G08** | Math, Science | Coordinate graph zones, physics diagrams | 650 | 50% |

---

# 6. ASSET ID ALLOCATION SYSTEM

Every SVG library item must occupy a block in our ID registry to prevent collisions:

```
  WW - [CATEGORY CLASS] - [0000 to 9999]

ID Blocks:
  WW-ICN-0001 to 0999:  Instructional and Navigation Icons
  WW-BRD-0001 to 0999:  Page Borders and Structural Frames
  WW-CHR-0001 to 1999:  Character Assets (Kids, Adults, Mascots)
  WW-ANI-0001 to 1999:  Animals and Living Organisms
  WW-ENV-0001 to 1999:  Backgrounds and Environmental Props
  WW-DIA-0001 to 1999:  Science and Math Diagrams
```

---

# 7. PRODUCTION DASHBOARD

This dashboard tracks development sprints across the current quarter (Q3 2026):

| Milestone ID | Target Library | Target Count | Start Date | Due Date | Status | Lead Artist |
|--------------|----------------|--------------|------------|----------|--------|-------------|
| **MS-SVG-01** | Instruction Icons Set | 120 SVGs | 2026-07-01 | 2026-07-15 | 🔄 In Progress | Sr Illustrator |
| **MS-SVG-02** | Master Borders (Tiers 1–3) | 60 SVGs | 2026-07-16 | 2026-07-31 | 📋 Planned | Sr Illustrator |
| **MS-SVG-03** | Kids Core Poses Set | 200 SVGs | 2026-08-01 | 2026-08-31 | 📋 Planned | Character Lead |
| **MS-SVG-04** | Math Manipulatives (Ten-frames, Base-10) | 80 SVGs | 2026-09-01 | 2026-09-15 | 📋 Planned | Diagram Lead |

---

# 8. QA CHECKLISTS FOR SVG ASSETS

All library items must pass the following QA checklist before code review merge:

```
[ ] 1. VALIDITY: SVG passes official validation linter checks (no stray code).
[ ] 2. STRUCTURE: Follows strict group layer conventions (<g id="animal--body">).
[ ] 3. DESIGN BIBLE: Stroke weights conform to L1-L5 specifications; stroke-linecap is round.
[ ] 4. OPTIMIZATION: Removed redundant shapes, paths, metadata tags, and empty groups.
[ ] 5. GRayscale: Tonal fills read cleanly in grayscale (min 30% contrast gap).
[ ] 6. ACCESSIBILITY: SVG contains <title> and <desc> tags for screen readers.
```

---

# VERSION HISTORY

## Document Record

| Field | Detail |
|-------|--------|
| **Document ID** | WW-SL-100 |
| **Document Name** | Worksheet Wonder SVG Library Roadmap |
| **Version** | 1.0 |
| **Date** | 14 July 2026 |
| **Author** | Senior Illustration Production Manager |
| **Status** | Approved |
| **Approved By** | Founder, Worksheet Wonder |
| **Classification** | Internal — Confidential |

## Revision Log

| Version | Date | Author | Changes | Approved By |
|---------|------|--------|---------|-------------|
| 1.0 | 14 July 2026 | Senior Illustration Production Manager | Initial release of the library roadmap, including category priority matrices, folder directories, grade mappings, and target production sprints. | Founder |
| | | | | |

## Future Revisions — Scheduled

| Target Version | Target Date | Planned Changes |
|----------------|-------------|-----------------|
| 1.1 | Q4 2026 | Add detailed SVG path snippets for the core reusable part library. |
| 1.2 | Q1 2027 | Integrate specific world culture asset lists and regional clothing maps. |
| 2.0 | 2027 Annual Review | Review actual production rates and calibrate time estimates for remaining milestones. |

---

## Dependencies

| Document ID | Title | Relationship | Minimum Version |
|-------------|-------|--------------|-----------------|
| **WW-DB-001** | [Worksheet Wonder Design Bible](file:///c:/Users/erpri/OneDrive/Desktop/worksheet%20wonder/worksheets/docs/01_Brand/WW-DESIGN-BIBLE.md) | Parent design standards | v1.0 |
| **WW-MC-001** | [Worksheet Wonder Master Curriculum](file:///c:/Users/erpri/OneDrive/Desktop/worksheet%20wonder/worksheets/docs/02_Curriculum/WW-MASTER-CURRICULUM.md) | Parent curriculum scope | v1.0 |
| **WW-IB-001** | [Worksheet Wonder Illustration Bible Pt. 1](file:///c:/Users/erpri/OneDrive/Desktop/worksheet%20wonder/worksheets/docs/03_Illustration/WW-ILLUSTRATION-BIBLE-PART-1.md) | Parent illustration standards | v1.0 |
| **WW-IB-002** | [Worksheet Wonder Illustration Bible Pt. 2](file:///c:/Users/erpri/OneDrive/Desktop/worksheet%20wonder/worksheets/docs/03_Illustration/WW-ILLUSTRATION-BIBLE-PART-2.md) | Sibling subject categories | v1.0 |
| **WW-IB-003** | [Worksheet Wonder Illustration Bible Pt. 3](file:///c:/Users/erpri/OneDrive/Desktop/worksheet%20wonder/worksheets/docs/03_Illustration/WW-ILLUSTRATION-BIBLE-PART-3.md) | Sibling environmental standards | v1.0 |
| **WW-PS-100** | [Worksheet Wonder Production System](file:///c:/Users/erpri/OneDrive/Desktop/worksheet%20wonder/worksheets/docs/05_Production/WW-PRODUCTION-SYSTEM.md) | Core production standards | v1.0 |
| **WW-AS-100** | [Worksheet Wonder Digital Asset Registry](file:///c:/Users/erpri/OneDrive/Desktop/worksheet%20wonder/worksheets/docs/05_Production/WW-ASSET-REGISTRY.md) | Core digital asset database | v1.0 |

---

## Approval Page

```
================================================================================
                     WORKSHEET WONDER — SVG LIBRARY ROADMAP
                              MASTER SIGN-OFF
                            WW-SL-100 | Version 1.0
================================================================================

PREPARED BY:
  Name: _______________________            Role: Senior Illustration Production Manager
  Signature: __________________            Date: 14 July 2026

REVIEWED BY:
  Name: _______________________            Role: Senior Art Director
  Signature: __________________            Date: ____________________

REVIEWED BY:
  Name: _______________________            Role: Publishing Director
  Signature: __________________            Date: ____________________

APPROVED BY:
  Name: _______________________            Role: Founder, Worksheet Wonder
  Signature: __________________            Date: ____________________
================================================================================
```

---

```
End of Document
WW-SL-100 | Version 1.0 | (c) 2026 Worksheet Wonder. All Rights Reserved.
```
