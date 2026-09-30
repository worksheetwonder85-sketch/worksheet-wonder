# WORKSHEET WONDER
## DIGITAL ASSET REGISTRY
### The Master Registry and Standard Operating Procedures for Asset Management

---

```
══════════════════════════════════════════════════════════════

                 Worksheet Wonder Documentation

══════════════════════════════════════════════════════════════

  Document ID:         WW-AS-100

  Document Name:       Worksheet Wonder Digital Asset Registry

  Version:             1.0

  Status:              Approved

  Owner:               Worksheet Wonder

  Author:              Digital Asset Manager

  Category:            Production Standards

  Last Updated:        14 July 2026

  Next Review:         14 January 2027

  Related Documents:   WW-DB-001  (Design Bible)
                       WW-MC-001  (Master Curriculum)
                       WW-IB-001  (Illustration Bible — Part 1)
                       WW-IB-002  (Illustration Bible — Part 2)
                       WW-IB-003  (Illustration Bible — Part 3)
                       WW-PS-100  (Production System)
                       WW-AI-100  (AI Prompt Handbook)

══════════════════════════════════════════════════════════════
```

> **This document is the absolute authority on digital asset management at Worksheet Wonder.**
> Every image, vector path, document, layout sheet, and commercial file created by or 
> for the organization must be indexed, cataloged, versioned, and verified in strict 
> compliance with these protocols.

---

## TABLE OF CONTENTS

| Chapter | Title |
|---------|-------|
| **01** | Introduction & Philosophy |
| **02** | Asset Categories |
| **03** | Asset ID System |
| **04** | Folder Structure |
| **05** | File Naming Standards |
| **06** | Asset Metadata Requirements |
| **07** | Version Control & Archival |
| **08** | Quality Checklist |
| **09** | Search & Retrieval |
| **10** | Future Expansion |
| **—** | Document Metadata & Sign-off |

---

# 1. INTRODUCTION

## 1.1 Purpose
The **Worksheet Wonder Digital Asset Registry (WW-AS-100)** serves as the single source of truth for every digital file in the company's ecosystem. It prevents asset duplication, establishes clean tracking from creation to sale, and enforces visual and metadata compliance across our extensive educational catalog.

## 1.2 Scope
This registry governs all visual, code, and document assets, including:
*   Inline SVGs (characters, animals, icons, backgrounds, structures).
*   Worksheet source templates (HTML, CSS, JS).
*   Commercial print outputs (Paperback interior PDFs, mega-bundles).
*   Marketing assets (thumbnails, mockups, banners, email graphics, social pins).
*   Brand identity assets (logos, wordmarks, favicons).

## 1.3 Asset Lifecycle

```
  [01. Ingestion / AI Draft] ────────► [02. QA Verification Gate]
               │                                      │
               ▼                                      ▼
  [04. Active Distribution] ◄──────── [03. Metadata Indexing & Registration]
               │
               ▼
  [05. Maintenance / Updates] ───────► [06. Archival / Deprecation]
```

## 1.4 Naming Philosophy
We believe that files should be self-documenting. Any human developer or automated system script must be able to read an asset's filename and immediately determine its category, size, style, and print constraints without needing to open the file.

---

# 2. ASSET CATEGORIES

The Worksheet Wonder catalog is divided into eighteen specific categories. Every asset must be registered under exactly one primary category.

| Category Code | Description | Standard Formats | Location |
|---------------|-------------|------------------|----------|
| **SVG-CHR** | Character Illustrations | `.svg` | `assets/svg/characters/` |
| **SVG-ANI** | Animal Illustrations | `.svg` | `assets/svg/animals/` |
| **SVG-OBJ** | Object & Prop Illustrations | `.svg` | `assets/svg/objects/` |
| **SVG-BG** | Background & Textures | `.svg` | `assets/svg/backgrounds/` |
| **SVG-STR** | Structural Elements (Borders/Frames) | `.svg` | `assets/svg/structural/` |
| **SVG-ICN** | Instructional & Navigation Icons | `.svg` | `assets/svg/icons/` |
| **DOC-CRT** | Completion Certificates | `.svg`, `.html`, `.pdf` | `assets/svg/reward/` |
| **DOC-COV** | Bundle Cover Sheets | `.html`, `.pdf` | `bundles/[grade]/[id]/source/` |
| **IMG-THM** | Platform Shop Thumbnails | `.png`, `.jpg` | `bundles/[grade]/[id]/exports/` |
| **IMG-MCK** | Product Mockups | `.png`, `.jpg` | `marketing/mockups/` |
| **IMG-WEB** | Website Hero & Content Images | `.png`, `.webp` | `exports/website-images/` |
| **BRD-LGO** | Brand Logo Variants | `.svg`, `.png` | `assets/logos/` |
| **BRD-FAV** | Favicons and Mobile Icons | `.png`, `.ico` | `assets/logos/favicons/` |
| **PDF-BND** | Customer-Facing PDFs | `.pdf` | `exports/pdf/` |
| **HTML-WS** | Worksheet Source Code | `.html` | `bundles/[grade]/[id]/source/` |
| **MKT-GRPH** | Pinterest/Social Media Graphics | `.png`, `.jpg` | `marketing/pinterest/` |

---

# 3. ASSET ID SYSTEM

Every digital asset must be assigned a unique, immutable Asset ID. This ID binds the asset's database record to its physical file and is referenced in version logs, bug reports, and product listings.

## 3.1 ID Format Specifications

Asset IDs must follow a 4-part alpha-numeric structure:

```
                  WW - [CATEGORY CODE] - [UNIQUE SEQUENCE]
                  │          │                  │
            Brand ┘          │                  └──── 4-digit sequential integer
                             └─────────────────────── 3-4 character classification
```

## 3.2 ID Classification Classes

| Class Code | Description | ID Range | Example |
|------------|-------------|----------|---------|
| **SVG** | General Vector Illustration | `0001–9999` | `WW-SVG-0412` |
| **ICON** | Instruction or Navigation Icon | `0001–0999` | `WW-ICON-0056` |
| **WS** | Worksheet Source Page | `0001–9999` | `WW-WS-1284` |
| **PDF** | Compiled Print Bundle PDF | `0001–1999` | `WW-PDF-0092` |
| **IMG** | Raster Image (Mockups, Banners) | `0001–9999` | `WW-IMG-0345` |
| **THUMB** | Retail Shop Thumbnail | `0001–1999` | `WW-THUMB-0081` |

## 3.3 Registration SOP

1.  **Draft Check:** When a designer creates a new asset, they check the Master Registry database to ensure no matching asset exists.
2.  **ID Request:** A request is sent to the Asset Manager (or automated script) for the next sequential ID in the class (e.g., `WW-SVG-0413`).
3.  **Registration:** The asset database entry is populated with the ID, title, and creator information.
4.  **Tag Insertion:** The designer inserts the ID into the asset's metadata header block.
5.  **Commit:** The file is committed to version control with the filename matching the standard naming format.

---

# 4. FOLDER STRUCTURE

All physical storage media must replicate our standard folder hierarchy. This makes it easy for developers and automated systems to find and update assets.

```
worksheet-wonder/
├── docs/                                  # Project Governance Files
│   ├── 01_Brand/                          # Design Bible (WW-DB-001)
│   ├── 02_Curriculum/                     # Master Curriculum (WW-MC-001)
│   ├── 03_Illustration/                   # Illustration Bibles (WW-IB-001 to 003)
│   ├── 04_Publishing/                     # Platform accounts & configurations
│   ├── 05_Production/                     # Production System Manual (WW-PS-100)
│   ├── 06_AI/                             # Prompts, models, and scripts
│   └── 07_Archive/                        # Retired versions of documentation
├── templates/                             # Empty Master Starting Blueprints
│   ├── worksheets/                        # Page layouts by Grade/Subject
│   ├── covers/                            # Standard cover page layouts
│   ├── guides/                            # Teacher and Parent guides
│   ├── certificates/                      # Completion rewards templates
│   └── mockups/                           # PSD/Figma product preview layouts
├── assets/                                # Shared Creative Resources
│   ├── svg/                               # Master Vector Database
│   │   ├── characters/                    # Kids, Parents, Teachers, Mascots
│   │   ├── animals/                       # Mammals, Birds, Sea, Dinosaurs, Insects
│   │   ├── environments/                  # Classroom, School, Library, Nature
│   │   ├── structural/                    # Borders, Frames, Patterns, Grids
│   │   └── icons/                         # Navigation, Instruction, Rating
│   ├── fonts/                             # Nunito and Fredoka One files
│   └── logos/                             # Worksheet Wonder brand identifiers
├── bundles/                               # Active Production Directory
│   ├── preschool/                         # PSC Grade Level Folder
│   ├── junior-kg/                         # JKG Grade Level Folder
│   ├── senior-kg/                         # SKG Grade Level Folder
│   └── grades-1-8/                        # Elementary & Middle folders
└── exports/                               # Outward Commercial Deliverables
    ├── pdf/                               # Production customer files
    ├── preview/                           # 8-page preview sheets
    └── marketing/                         # Social, Web, and Shop media
```

---

# 5. FILE NAMING STANDARDS

All filenames must be lowercase (except for official Document IDs and Bundle IDs). Spaces are forbidden; use hyphens (`-`) or double underscores (`__`) for structural separation.

## 5.1 Extension Conventions

*   **Vector Files (`.svg`):** Used for all illustration components, icons, and page borders.
*   **Vector Documents (`.html`):** Raw worksheet layout source files.
*   **Raster Previews (`.png`):** Used for preview pages and watermarked previews to preserve transparency where needed.
*   **Raster Deliverables (`.jpg`):** Used for platform thumbnails and marketing mockups (sRGB color space).
*   **Web Images (`.webp`):** Primary web image format for our direct store to minimize page load times.
*   **Print Deliverables (`.pdf`):** Standard customer download format (300 DPI, embedded fonts, grayscaled).
*   **Distribution Packages (`.zip`):** Used for large mega-bundles containing multiple PDFs.

## 5.2 Naming Rules

### 5.2.1 SVG Illustrations
All SVG files in our shared library must follow this syntax:
```
ww--[category]--[descriptor]--[variant]--[size].svg

Examples:
  ww--animal--elephant-cartoon--waving--md.svg
  ww--character--teacher-female--welcoming--lg.svg
  ww--icon--pencil-outline--writing--sm.svg
  ww--border--double-rounded--plain--a4.svg
```

### 5.2.2 Compiled PDF Bundles
All compiled PDF files for final release must follow this syntax:
```
[BUNDLE-ID]-COMPLETE-v[VERSION].pdf

Example:
  WW-PSC-PWS-TRL-01-COMPLETE-v1.0.pdf
```

### 5.2.3 Marketing Mockups
All product mockups must follow this syntax:
```
[BUNDLE-ID]-MOCKUP-[SEQUENCE].[EXTENSION]

Example:
  WW-PSC-PWS-TRL-01-MOCKUP-01.jpg
```

---

# 6. ASSET METADATA

Metadata ensures that every file can be searched, filtered, and checked for license compliance.

## 6.1 Required Metadata Schema

Every database record and file header comment must populate these 13 fields:

```
  ┌─────────────────────────────────────────────────────────────┐
  │ 1. Asset ID:       WW-SVG-0412                              │
  │ 2. Title:          Smiling Ladybug Character                │
  │ 3. Category:       SVG-CHR                                  │
  │ 4. Description:    Happy ladybug pointing right             │
  │ 5. Keywords:       insect, bug, red, ladybug, cute, cartoon │
  │ 6. Creator:        Lead Illustrator Name                    │
  │ 7. Date Created:   2026-07-14                               │
  │ 8. Version:        1.0                                      │
  │ 9. Status:         Approved                                 │
  │ 10. License:       Proprietary - Internal Use Only          │
  │ 11. Related Bundle:WW-PSC-PWS-TRL-01                        │
  │ 12. Related Grade: Preschool                                │
  │ 13. Related Subject: Pre-Writing Skills                     │
  └─────────────────────────────────────────────────────────────┘
```

## 6.2 XML/HTML Header Comment Block

For HTML and SVG source files, metadata must be embedded as a header comment block:

```xml
<!--
  Asset ID:        WW-SVG-0412
  Title:           Smiling Ladybug Character
  Category:        SVG-CHR
  Creator:         Lead Illustrator Name
  Date Created:    2026-07-14
  Version:         1.0
  Status:          Approved
  License:         Proprietary - Internal Use Only
  Related Bundle:  WW-PSC-PWS-TRL-01
-->
```

---

# 7. VERSION CONTROL

We use strict version control to track updates, corrections, and deprecations across the catalog.

## 7.1 Asset Update Protocol

```
  [01. Change Request] ──► [02. Update Master File] ──► [03. Run QA Checklists]
                                                                │
                                                                ▼
  [06. Notify Platforms] ◄── [05. Update Version Log] ◄── [04. Export PDF & Archive]
```

## 7.2 Deprecation Workflow

When an asset is retired or updated:
1.  **Tagging:** Change the status field in the metadata to `Deprecated`.
2.  **Archival:** Move the retired file to the `archive/` subfolder. Append the date suffix to the filename: `[FILENAME]_deprecated_[YYYY-MM-DD].[ext]`.
3.  **Dependency Check:** Run a dependency scan to identify any active templates or bundles referencing the retired Asset ID, and update them to point to the new ID.
4.  **Notice:** Update version logs on affected product listings to notify buyers of the update.

---

# 8. QUALITY CHECKLIST

Before any asset is registered or updated, it must pass these verification gates.

## 8.1 SVG Optimization Check

```
[ ] 1. Clean vectors only; no embedded raster images (no PNG/JPG data).
[ ] 2. All strokes use stroke-linecap="round" and stroke-linejoin="round".
[ ] 3. The viewBox attribute is defined correctly (e.g., viewBox="0 0 64 64").
[ ] 4. Remove empty groups (<g>), redundant transforms, and metadata comments.
[ ] 5. File size is optimized (minified SVG code).
```

## 8.2 Print Quality Check

```
[ ] 1. Grayscale rendering: All details read clearly when printed in B&W.
[ ] 2. Contrast: Tonal difference between overlapping shapes is at least 30%.
[ ] 3. Detail safety: No lines or critical features are thinner than 0.75px.
[ ] 4. Print margins: No content enters the 5mm print-safe page edge boundary.
[ ] 5. Ink economy: Grey fills do not cover more than 35% of the page area.
```

## 8.3 Digital & Accessibility Check

```
[ ] 1. Font choices: Use Fredoka One for headings, Nunito for body text.
[ ] 2. Dyslexia accommodation: Nunito body text uses 1.5x line spacing minimum.
[ ] 3. Sizing: Writing lines and check-boxes fit age-group motor skills.
[ ] 4. Web performance: Raster previews are compressed (PNG-8 or WebP).
[ ] 5. Alt text: Descriptive alt text is written for website indexers.
```

---

# 9. SEARCH & RETRIEVAL

As our catalog grows, we need efficient index searching to avoid recreating assets we already have.

## 9.1 Indexing System
*   **Database:** We maintain a master asset catalog database indexing all Asset IDs, categories, descriptions, and keywords.
*   **Automatic Scanning:** A cron job scans the `assets/` directory daily, parsing metadata comments to keep the registry in sync.
*   **Search Protocol:** Designers search the catalog by category or keyword (e.g., searching for `frog` or `ladybug`) before creating new vector assets.

---

# 10. FUTURE EXPANSION

Our systems are designed to scale to over 50,000 assets.

## 10.1 Scaling Roadmap

*   **Database Partitioning:** As the master database grows, partitioning by Grade Level and Subject preserves search speeds.
*   **Distributed File Storage:** Assets are stored in cloud buckets (AWS S3) using a Content Delivery Network (CDN) to ensure fast load times for global teams and customers.
*   **Automated Linting API:** Integrating linting scripts directly into our version control commits automatically rejects assets that violate Design Bible margin, contrast, or font rules.

---

# VERSION HISTORY

## Document Record

| Field | Detail |
|-------|--------|
| **Document ID** | WW-AS-100 |
| **Document Name** | Worksheet Wonder Digital Asset Registry |
| **Version** | 1.0 |
| **Date** | 14 July 2026 |
| **Author** | Digital Asset Manager |
| **Status** | Approved |
| **Approved By** | Founder, Worksheet Wonder |
| **Classification** | Internal — Confidential |

## Revision Log

| Version | Date | Author | Changes | Approved By |
|---------|------|--------|---------|-------------|
| 1.0 | 14 July 2026 | Digital Asset Manager | Initial release of the registry rules, including naming conventions, ID formats, metadata schema, folder structures, quality checklists, and search-retrieval SOPs. | Founder |
| | | | | |

## Future Revisions — Scheduled

| Target Version | Target Date | Planned Changes |
|----------------|-------------|-----------------|
| 1.1 | Q4 2026 | Integrate automated metadata validation scripts. |
| 1.2 | Q1 2027 | Implement automated CDN sync for our cloud asset library. |
| 2.0 | 2027 Annual Review | Full annual review of file organization and metadata indexing performance. |

---

## Dependencies

| Document ID | Title | Relationship | Minimum Version |
|-------------|-------|--------------|-----------------|
| **WW-DB-001** | [Worksheet Wonder Design Bible](file:///c:/Users/erpri/OneDrive/Desktop/worksheet%20wonder/worksheets/docs/01_Brand/WW-DESIGN-BIBLE.md) | Parent design standards | v1.0 |
| **WW-MC-001** | [Worksheet Wonder Master Curriculum](file:///c:/Users/erpri/OneDrive/Desktop/worksheet%20wonder/worksheets/docs/02_Curriculum/WW-MASTER-CURRICULUM.md) | Parent curriculum scope | v1.0 |
| **WW-IB-001** | [Worksheet Wonder Illustration Bible Pt. 1](file:///c:/Users/erpri/OneDrive/Desktop/worksheet%20wonder/worksheets/docs/03_Illustration/WW-ILLUSTRATION-BIBLE-PART-1.md) | Parent illustration standards | v1.0 |
| **WW-IB-002** | [Worksheet Wonder Illustration Bible Pt. 2](file:///c:/Users/erpri/OneDrive/Desktop/worksheet%20wonder/worksheets/docs/03_Illustration/WW-ILLUSTRATION-BIBLE-PART-2.md) | Sibling subject categories | v1.0 |
| **WW-PS-100** | [Worksheet Wonder Production System](file:///c:/Users/erpri/OneDrive/Desktop/worksheet%20wonder/worksheets/docs/05_Production/WW-PRODUCTION-SYSTEM.md) | Core production standards | v1.0 |
| **WW-AI-100** | [Worksheet Wonder AI Prompt Handbook](file:///c:/Users/erpri/OneDrive/Desktop/worksheet%20wonder/worksheets/docs/06_AI/WW-AI-PROMPT-HANDBOOK.md) | Core prompt workflows | v1.0 |

---

## Approval Page

```
================================================================================
                    WORKSHEET WONDER — DIGITAL ASSET REGISTRY
                              MASTER SIGN-OFF
                            WW-AS-100 | Version 1.0
================================================================================

PREPARED BY:
  Name: _______________________            Role: Digital Asset Manager
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
WW-AS-100 | Version 1.0 | (c) 2026 Worksheet Wonder. All Rights Reserved.
```
