# Worksheet Wonder Documentation Library

```
══════════════════════════════════════════════════════════════

                 Worksheet Wonder Documentation

              THE OFFICIAL REFERENCE LIBRARY

══════════════════════════════════════════════════════════════

  Owner:               Worksheet Wonder
  Classification:      Internal — Confidential
  Established:         09 July 2026
  Maintained by:       Documentation Coordinator

══════════════════════════════════════════════════════════════
```

This folder contains all master documentation governing the Worksheet Wonder publishing system. Every document in this library is an authoritative reference — compliance is mandatory for all products, all teams, and all contributors.

---

## Library Structure

```
docs/
│
├── README.md                          ← You are here
│
├── 01_Brand/                          ← Brand philosophy and design standards
│   └── WW-DESIGN-BIBLE.md                [WW-DB-001] v1.0
│
├── 02_Curriculum/                     ← Curriculum framework and learning outcomes
│   └── WW-MASTER-CURRICULUM.md            [WW-MC-001] v1.0
│
├── 03_Illustration/                   ← Illustration standards and reusable asset library
│   ├── WW-ILLUSTRATION-BIBLE-PART-1.md    [WW-IB-001] v1.0
│   ├── WW-ILLUSTRATION-BIBLE-PART-2.md    [WW-IB-002] v1.0
│   └── WW-ILLUSTRATION-BIBLE-PART-3.md    [WW-IB-003] — Planned
│
├── 04_Publishing/                     ← Bundle architecture and publishing workflow
│   ├── WW-PUBLISHING-SYSTEM.md            [WW-PS-001] — Planned
│   ├── WW-BUNDLE-ARCHITECTURE.md          [WW-PS-002] — Planned
│   └── WW-PLATFORM-GUIDES.md             [WW-PS-003] — Planned
│
├── 05_Production/                     ← Production checklists and quality assurance
│   ├── WW-PRODUCTION-SYSTEM.md            [WW-PS-100] v1.0
│   ├── WW-PRODUCTION-CHECKLIST.md         [WW-PR-001] — Planned
│   ├── WW-QA-STANDARDS.md                 [WW-PR-002] — Planned
│   └── WW-PRINT-TESTING-GUIDE.md         [WW-PR-003] — Planned
│
├── 06_AI/                             ← Master prompts and AI workflow documentation
│   ├── WW-AI-PROMPT-LIBRARY.md            [WW-AI-001] — Planned
│   ├── WW-AI-WORKFLOW.md                  [WW-AI-002] — Planned
│   └── WW-AI-QUALITY-GATES.md            [WW-AI-003] — Planned
│
└── 07_Archive/                        ← Archived document versions
    └── (superseded versions stored here with date suffix)
```

---

## Document Registry

### Active Documents

| Doc ID | Document Name | Category | Version | Status | Author | Last Updated |
|--------|---------------|----------|---------|--------|--------|-------------|
| WW-DB-001 | Worksheet Wonder Design Bible | 01_Brand | 1.0 | ✅ Approved | Creative Director | 09 Jul 2026 |
| WW-MC-001 | Worksheet Wonder Master Curriculum | 02_Curriculum | 1.0 | ✅ Approved | Curriculum Director | 09 Jul 2026 |
| WW-PC-100 | Product Catalog | 02_Curriculum | 1.0 | ✅ Approved | Product Management Director | 14 Jul 2026 |
| WW-IB-001 | Illustration Bible — Part 1 | 03_Illustration | 1.0 | ✅ Approved | Senior Art Director | 09 Jul 2026 |
| WW-IB-002 | Illustration Bible — Part 2: Subject Categories | 03_Illustration | 1.0 | ✅ Approved | Senior Art Director | 10 Jul 2026 |
| WW-IB-003 | Illustration Bible — Part 3: Settings, Structural Assets & Decoration | 03_Illustration | 1.0 | ✅ Approved | Senior Art Director | 10 Jul 2026 |
| WW-SL-100 | SVG Library Roadmap | 03_Illustration | 1.0 | ✅ Approved | Senior Illustration Production Manager | 14 Jul 2026 |
| WW-PS-100 | Production System | 05_Production | 1.0 | ✅ Approved | Publishing Director | 11 Jul 2026 |
| WW-AS-100 | Digital Asset Registry | 05_Production | 1.0 | ✅ Approved | Digital Asset Manager | 14 Jul 2026 |
| WW-AI-100 | AI Prompt Handbook | 06_AI | 1.0 | ✅ Approved | AI Workflow Architect | 14 Jul 2026 |

### Planned Documents

| Doc ID | Document Name | Category | Target Date | Owner |
|--------|---------------|----------|-------------|-------|
| WW-PS-001 | Publishing System (Platform Guide) | 04_Publishing | Q3 2026 | Publishing Director |
| WW-PS-002 | Bundle Architecture & File Structure | 04_Publishing | Q3 2026 | Publishing Director |
| WW-PS-003 | Platform Guides (TPT, Etsy, KDP, Gumroad) | 04_Publishing | Q4 2026 | Marketing Director |
| WW-PR-001 | Production Checklist | 05_Production | Q3 2026 | Production Manager |
| WW-PR-002 | Quality Assurance Standards | 05_Production | Q4 2026 | QA Lead |
| WW-PR-003 | Print Testing Guide | 05_Production | Q4 2026 | Production Manager |
| WW-AI-001 | AI Prompt Library | 06_AI | Q3 2026 | AI Content Director |
| WW-AI-002 | AI Workflow Documentation | 06_AI | Q3 2026 | AI Content Director |
| WW-AI-003 | AI Quality Gates & Human Review | 06_AI | Q4 2026 | QA Lead |

---

## Document Hierarchy

```
                        ┌─────────────────────┐
                        │   WW-DB-001         │
                        │   DESIGN BIBLE       │
                        │   (Master Standard)  │
                        └────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                   │
    ┌─────────▼──────────┐ ┌────▼───────────┐ ┌─────▼──────────────┐
    │   WW-MC-001        │ │  WW-IB-001     │ │   WW-PS-100        │
    │   MASTER           │ │  ILLUSTRATION  │ │   PRODUCTION       │
    │   CURRICULUM       │ │  BIBLE PT 1    │ │   SYSTEM           │
    └────────────────────┘ └───┬────────────┘ └────────────────────┘
                               │
                    ┌──────────┼──────────┐
                    │                     │
              ┌─────▼──────────┐  ┌───────▼────────┐
              │  WW-IB-002     │  │   WW-IB-003    │
              │  ILLUSTRATION  │  │  ENVIRONMENT & │
              │  BIBLE PT 2    │  │  DECORATION    │
              └────────────────┘  └────────────────┘
```

The **Design Bible (WW-DB-001)** is the root document. All other documents inherit from it and must not contradict it. In the event of a conflict between any two documents, the Design Bible takes precedence.

---

## How to Use This Library

### For Content Creators
1. **Before creating any new product:** Read the Design Bible (WW-DB-001) — it governs everything.
2. **Before writing content:** Consult the Master Curriculum (WW-MC-001) — every worksheet must map to a unit.
3. **Before illustrating:** Follow the Illustration Bible (WW-IB-001) — every SVG must comply.

### For Reviewers & QA
1. Use the Quality Checklist in each document's final chapter as your acceptance criteria.
2. Every product must pass the checklists in all applicable documents before publication.

### For New Team Members
1. Read documents in this order: WW-DB-001 → WW-MC-001 → WW-IB-001
2. Complete the onboarding quiz (to be included in WW-PR-001)
3. Shadow a senior creator for one full bundle production cycle

---

## Naming Convention for New Documents

All new documents added to this library must follow the naming convention:

```
WW-[CATEGORY CODE]-[SEQUENCE NUMBER]

Category Codes:
  DB  = Design Bible / Brand Standards
  MC  = Master Curriculum
  IB  = Illustration Bible
  PS  = Publishing System
  PR  = Production / QA
  AI  = AI & Automation
  AR  = Archive
```

---

## Version Control Policy

| Action | Rule |
|--------|------|
| **Minor update** (typo, clarification) | Increment patch: 1.0 → 1.0.1 |
| **Section addition** (new chapter, new rule) | Increment minor: 1.0 → 1.1 |
| **Major rewrite** (structural change, philosophy shift) | Increment major: 1.0 → 2.0 |
| **Superseded version** | Move to `07_Archive/` with date suffix (e.g., `WW-DESIGN-BIBLE_v1.0_2026-07-09.md`) |
| **Review cycle** | Every 6 months (Next Review: 09 January 2027) |

---

## Archive Policy

When a document is superseded:

1. Rename the old version with a date suffix: `WW-DESIGN-BIBLE_v1.0_2026-07-09.md`
2. Move it to `07_Archive/`
3. Place the new version in the original folder
4. Update this README's Document Registry
5. Notify all team members via the #documentation channel

---

## Quick Access Links

| I need to... | Read this |
|-------------|-----------|
| Understand our brand and design rules | `01_Brand/WW-DESIGN-BIBLE.md` |
| Find what subjects and topics we cover | `02_Curriculum/WW-MASTER-CURRICULUM.md` |
| Know how to draw characters and illustrations | `03_Illustration/WW-ILLUSTRATION-BIBLE-PART-1.md` |
| Know how to structure and publish a bundle | `04_Publishing/WW-PUBLISHING-SYSTEM.md` *(coming soon)* |
| Run final quality checks before publishing | `05_Production/WW-PRODUCTION-CHECKLIST.md` *(coming soon)* |
| Use AI to generate worksheet content | `06_AI/WW-AI-PROMPT-LIBRARY.md` *(coming soon)* |

---

```
══════════════════════════════════════════════════════════════

These documents are the official reference for every
Worksheet Wonder product.

"If it's not in the docs, it's not approved."

(c) 2026 Worksheet Wonder. All Rights Reserved.

══════════════════════════════════════════════════════════════
```
