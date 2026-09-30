# WORKSHEET WONDER
## AI PROMPT HANDBOOK
### The Complete Reference Guide for AI-Assisted Educational Publishing

---

```
══════════════════════════════════════════════════════════════

                 Worksheet Wonder Documentation

══════════════════════════════════════════════════════════════

  Document ID:         WW-AI-100

  Document Name:       Worksheet Wonder AI Prompt Handbook

  Version:             1.0

  Status:              Approved

  Owner:               Worksheet Wonder

  Author:              AI Workflow Architect

  Category:            AI & Automation Standards

  Last Updated:        14 July 2026

  Next Review:         14 January 2027

  Related Documents:   WW-DB-001  (Design Bible)
                       WW-MC-001  (Master Curriculum)
                       WW-IB-001  (Illustration Bible — Part 1)
                       WW-IB-002  (Illustration Bible — Part 2)
                       WW-IB-003  (Illustration Bible — Part 3)
                       WW-PS-100  (Production System)

══════════════════════════════════════════════════════════════
```

> **This handbook is the single source of truth for all AI-assisted work at Worksheet Wonder.**
> All content creators, developers, illustrators, and operations managers must use these 
> prompt templates, workflows, and quality gates to maintain our premium standard.

---

## TABLE OF CONTENTS

| Chapter | Title |
|---------|-------|
| **01** | Introduction & Philosophy |
| **02** | Supported AI Models |
| **03** | Worksheet Creation Prompts |
| **04** | Illustration Planning Prompts |
| **05** | Cover Page Prompts |
| **06** | Teacher Guide Prompts |
| **07** | Parent Guide Prompts |
| **08** | Answer Key Prompts |
| **09** | Certificate Prompts |
| **10** | Website Content Prompts |
| **11** | SEO Prompts |
| **12** | Marketing Prompts |
| **13** | Quality Review Prompts |
| **14** | Automation Workflows |
| **15** | Best Practices |
| **—** | Document Metadata & Sign-off |

---

# 1. INTRODUCTION

## 1.1 Purpose
The purpose of the **Worksheet Wonder AI Prompt Handbook (WW-AI-100)** is to standardize and optimize all human-AI collaboration across the company. It provides highly refined, production-tested prompt templates and multi-model workflow guidelines to ensure that all generated outputs align perfectly with our pedagogical, design, and technical standards.

## 1.2 Scope
This handbook covers the entire production chain of Worksheet Wonder digital and physical assets, including:
*   Core educational worksheets (HTML/CSS/JS scaffolding).
*   Illustration planning briefs and inline SVG specifications.
*   Supporting collateral (Covers, Teacher Guides, Parent Guides, Certificates, Answer Keys).
*   Commercial copy (Shop listings, Website pages, Blogs, SEO metadata).
*   Quality control automation prompts.

## 1.3 AI Workflow Philosophy
We view Artificial Intelligence not as a replacement for human capability, but as a **pedagogical force multiplier**. We use AI to automate structural heavy lifting, boilerplate code, copy generation, and data formatting. This frees human designers, teachers, and artists to focus entirely on layout refinement, fine-art vector illustration, educational scaffolding validation, and quality control.

## 1.4 Human Review Policy (Non-Negotiable)
No AI-generated text, code, layout, or illustration may bypass human review. Every output must pass the Quality Gates outlined in [WW-PS-100](file:///c:/Users/erpri/OneDrive/Desktop/worksheet%20wonder/worksheets/docs/05_Production/WW-PRODUCTION-SYSTEM.md) and be signed off by a department lead. The following table defines our strict review tiers:

| Asset Class | AI Responsibility | Human Responsibility | QA Sign-off |
|-------------|-------------------|----------------------|-------------|
| **Curriculum Planning** | Suggesting topics/subtopics | Verification of scope, sequencing | Curriculum Director |
| **Worksheet Layout** | Code skeleton, CSS spacing | Margin adjust, font scaling, grid alignment | Senior Designer |
| **Illustrations (SVG)** | Component shapes, coordinate grid | Bezier curve polishing, anchor alignment | Senior Art Director |
| **Guides & Copy** | Draft text, translations | Tone adjust, jargon removal, pedagogical check | Senior Educational Designer |
| **SEO & Listing** | Meta title, description, tags | Keyword verification, platform optimization | Marketing Director |

---

# 2. SUPPORTED AI MODELS

We match tasks to the specific cognitive and technical strengths of different Large Language Models (LLMs). Using the wrong model for a task wastes tokens and degrades output quality.

## 2.1 Model Evaluation Matrix

| Model | Primary Strengths | Notable Weaknesses | Best Use Cases |
|-------|-------------------|--------------------|----------------|
| **Claude 3.5 Sonnet / 3.0 Opus** | Exceptional code generation (HTML/CSS/SVG), context window adherence, pedagogical reasoning, brand tone empathy. | Occasional verbosity, slower response speed compared to smaller models. | Worksheet HTML coding, SVG vector paths drafting, educational writing. |
| **GPT-4o / GPT-4** | High throughput, excellent web search capability, solid SEO keyword integration, API speed. | Code can be generic/simplistic, strict style bibles are sometimes ignored in long contexts. | SEO metadata, shop listings copy, social media campaigns, competitive analysis. |
| **Gemini 1.5 Pro / Flash** | Massive context window (up to 2M tokens), exceptionally fast analysis of large multi-file documentation (e.g., uploading all Bibles at once). | Can hallucinate complex layout coordinates, less precise inline CSS output. | Ingesting entire grade curriculums, checking cross-document consistency, batch sorting. |
| **GitHub Copilot / Cursor** | Real-time code completions, directory-level indexing. | Limited to direct programming contexts, cannot write long-form pedagogical guides well. | Coding templates, fixing CSS lints, rapid file structure creation. |

---

# 3. WORKSHEET CREATION PROMPTS

These prompt templates compile our design guidelines into direct instructions for code generation.

## 3.1 Standard System Prompt for Worksheet Coding

```markdown
You are the Lead Front-End Engineer and Senior Educational Content Designer for Worksheet Wonder. Your task is to output clean, raw, valid HTML/CSS code for a premium educational worksheet.

You must strictly adhere to the following Parent Documents:
1. WW-DB-001 (Design Bible): Use Fredoka One for headings, Nunito for body. Page margins must be 15mm top/bottom, 12mm sides. Minimum 40% white space. No overlapping elements.
2. WW-IB-001/002/003 (Illustration Bibles): All graphics must be inline SVGs (no external resources, no base64). Use rounded strokes (stroke-linecap="round").
3. WW-PS-100 (Production System): Ensure the page fits A4 portrait dimensions (210mm x 297mm) and prints cleanly on standard grayscale home printers.

CSS Rules:
- Wrap all CSS inside a single <style> tag in the <head>.
- Use absolute box-sizing and A4 page-break parameters.
- Do not use TailwindCSS or external frameworks unless explicitly requested.
- Ensure all input zones (writing lines, checkboxes, drawing boxes) are large and motor-skill appropriate.

Output ONLY clean HTML/CSS code. Do not wrap the code in markdown formatting other than the standard code block. Do not provide chat explanation.
```

## 3.2 Template: Preschool Pre-Writing & Tracing Worksheets

```markdown
[System Prompt: Use Section 3.1]

Create a Preschool (Ages 3-4) Pre-Writing worksheet based on the following parameters:
- Topic: {{TOPIC}} (e.g., Tracing Horizontal Lines)
- Bundle ID: {{BUNDLE_ID}} (e.g., WW-PSC-PWS-TRL-01)
- Worksheet Sequence: {{SEQUENCE_NUMBER}} (e.g., WS-01)
- Difficulty Phase: {{DIFFICULTY_PHASE}} (e.g., Foundation)
- Learning Outcome: {{LEARNING_OUTCOME}} (e.g., Help children develop left-to-right hand movement)

Specific Layout Requirements:
1. Header: Display the "Worksheet Wonder" logo mark (simple inline SVG star + text), child name/date entry fields, Page Title ("{{TITLE}}"), Age indicator ("Ages 3-4"), and Learning Objective.
2. Directions Box: Simple instructions with a pencil icon: "Trace the dotted lines from left to right!"
3. Activity Area:
   - {{COUNT}} tracing paths.
   - Each path must begin with a friendly inline SVG start character (e.g., a happy ladybug) on the far left, and end with a destination icon (e.g., a flower) on the far right.
   - The tracing line must be a thick, dashed gray path (stroke-width: 4px, stroke-dasharray: 8 6).
   - Provide generous vertical spacing (minimum 30mm) between paths for motor-skill comfort.
4. Footer: Include the Copyright ("© 2026 Worksheet Wonder"), Bundle ID, and a 3-star rating graphic for student self-assessment.
```

## 3.3 Template: Math Worksheets (Grades 1–8)

```markdown
[System Prompt: Use Section 3.1]

Create a Grade {{GRADE_level}} Mathematics worksheet based on the following parameters:
- Unit/Topic: {{TOPIC}} (e.g., Addition Facts to 10)
- Bundle ID: {{BUNDLE_ID}} (e.g., WW-G01-MTH-ADD-01)
- Worksheet Sequence: {{SEQUENCE_NUMBER}} (e.g., WS-03)
- Difficulty Phase: {{DIFFICULTY_PHASE}} (e.g., Developing)
- Learning Outcome: {{LEARNING_OUTCOME}} (e.g., Solve single-digit addition problems using visual models)

Specific Layout Requirements:
1. Grid System: Create a 2-column or 3-column clean problem grid using CSS Flexbox/Grid.
2. Visual Models: For each of the {{PROBLEM_COUNT}} problems, include:
   - An inline SVG visual helper representation (e.g., a ten-frame showing counters, or base-10 blocks).
   - The numerical equation (e.g., 5 + 3 = __).
   - An answer box styled as a rounded rectangle with L3 border weight (1.5px).
3. Workspace: Ensure there is ample blank space surrounding each problem grid item for student writing/working out.
4. Footer: Include the Worksheet Wonder branding, Copyright, Bundle ID, and page number.
```

## 3.4 Template: Phonics & English Literacy Worksheets

```markdown
[System Prompt: Use Section 3.1]

Create a Phonics/Literacy worksheet for {{GRADE_LEVEL}} based on the following parameters:
- Topic: {{TOPIC}} (e.g., Short 'a' CVC Words)
- Bundle ID: {{BUNDLE_ID}} (e.g., WW-JKG-PHN-CVC-01)
- Worksheet Sequence: {{SEQUENCE_NUMBER}} (e.g., WS-05)
- Difficulty Phase: {{DIFFICULTY_PHASE}} (e.g., Mastery)
- Learning Outcome: {{LEARNING_OUTCOME}} (e.g., Read, write, and identify short 'a' CVC word groups)

Specific Layout Requirements:
1. Core Exercise: A "Look, Write, and Match" three-part activity layout:
   - Column 1: A vertical list of {{COUNT}} high-quality, friendly inline SVG illustrations representing the target words (e.g., cat, hat, bag, fan).
   - Column 2: Large, clean guidelines (solid base line, dashed middle line, solid top line) for the student to write the spelling.
   - Column 3: Dotted matching target points for drawing connecting lines.
2. Font Settings: Use Nunito for spelling text, with letter-spacing set to 2px to ensure dyslexic-friendly readability.
3. Footer: Include the standard Worksheet Wonder brand guidelines.
```

---

# 4. ILLUSTRATION PLANNING PROMPTS

These prompts help us design SVG coordinates and layouts to ensure they are visually consistent and clean.

## 4.1 Prompt: SVG Icon Library Planner

```markdown
System: You are the Senior Art Director for Worksheet Wonder. Your task is to output raw SVG vector path code for an icon set.

You must strictly follow the Illustration Bible (WW-IB-001/003):
- Grid: Align to a 64x64 viewBox.
- Outlines: Use stroke-width="2" on primary paths, stroke-linecap="round", stroke-linejoin="round", fill="none".
- Colors: Output in flat grayscale (stroke: #333333, fill: none).
- Style: Round all corners, use friendly, child-safe visual geometry. No sharp or jagged edges.

Request: Generate a raw SVG path for: {{ICON_DESCRIPTOR}} (e.g., a hand holding a pencil, or a magnifying glass). 
Ensure the output is clean, optimized, and contains only the <svg> container and child path elements. No explanation.
```

## 4.2 Prompt: Character & Scene Composition

```markdown
System: You are the Senior Art Director and Lead Illustrator for Worksheet Wonder.

Your task is to write a highly detailed illustration planning brief for our creative team, matching the standards in WW-IB-002 and WW-IB-003.

Write the planning brief for the following scene:
- Character: {{CHARACTER_TYPE}} (e.g., a young girl, skin tone ST3, curly hair, happy expression)
- Action/Pose: {{POSE}} (e.g., looking through a magnifying glass at a ladybug on a leaf)
- Setting: {{SETTING}} (e.g., a simple garden background with grass tufts and a soft sun)
- Target Style: Flat, kid-friendly vector illustration conforming to our line weight hierarchy (L1 outline, L3 details).

Structure the output into:
1. Visual Geometry Description: Specific shapes, proportions, and curves.
2. Layer Hierarchy Map: The exact grouping order from bottom (backgrounds) to top (highlights).
3. Technical Specifications: Tonal levels (#f0f0f0 to #333333) and viewBox dimensions.
4. SVG Blueprint: A pseudocode representation of the path components.
```

---

# 5. COVER PAGE PROMPTS

Covers are key to catching a buyer's eye. This prompt template generates standard, high-converting covers.

## 5.1 Prompt: Cover Page HTML & SVG Generator

```markdown
[System Prompt: Use Section 3.1]

Generate a premium A4 Cover Page for the following product bundle:
- Title: {{BUNDLE_TITLE}} (e.g., Pre-Writing Skills: Tracing Horizontal Lines)
- Grade Suitability: {{GRADE_LEVEL}} (e.g., Preschool / Ages 3-4)
- Subject: {{SUBJECT}} (e.g., Early Development)
- Bundle ID: {{BUNDLE_ID}} (e.g., WW-PSC-PWS-TRL-01)
- Page Count: {{PAGE_COUNT}} (e.g., 25 Premium Pages)

Visual Design Requirements:
1. Borders: Use the double border style from WW-DB-001 (Outer: 2.5px rounded rect at 14px inset, Inner: 1.5px at 25px inset).
2. Typography:
   - Primary Title: Placed in the upper-middle quadrant, using very large Fredoka One font, centered, with a slight drop-shadow effect for a premium look.
   - Grade & Subject Labels: Styled as cute rounded badge blocks (#333333 fill with white text, or clear grayscale contrasts).
3. Central Feature Art: An inline SVG scene depicting the theme (e.g., a cute pencil character named "Wonder" tracing a path through clouds).
4. Accents: Add star bursts and dots in the corners to create a fun, high-value look.
5. Footer: Include the "Worksheet Wonder" logo and "Printable PDF Worksheet Bundle" tag.
```

---

# 6. TEACHER GUIDE PROMPTS

Our guides need to be clear and detailed to help teachers quickly use the worksheets in class.

## 6.1 Prompt: Teacher Guide Copywriter

```markdown
System: You are a Senior Educational Content Designer for Worksheet Wonder. Your task is to write the Teacher Guide page for a newly developed worksheet bundle.

Use the following parameters:
- Bundle Title: {{BUNDLE_TITLE}}
- Target Grade: {{GRADE_LEVEL}}
- Learning Outcomes: {{LEARNING_OUTCOMES}}
- Worksheet Sequence: {{WORKSHEET_LIST}}

Write a structured, professional guide containing the following sections:
1. Lesson Plan Flow: A step-by-step teaching progression (Introduce -> Guided Practice -> Independent Work -> Review).
2. Differentiation Matrix:
   - Below Level: Scaffolding and support strategies.
   - On Level: Expected target independence benchmarks.
   - Above Level: High-order extension tasks (Bloom's Level 5/6).
3. Academic Vocabulary: 4-6 key terms defined in child-friendly language.
4. Classroom Setup & Materials: Suggested groupings and physical manipulatives.
5. Formative Assessment: Key questions to ask during the activities to check for understanding.

Maintain a warm, professional, and authoritative educational tone. Avoid fluff.
```

---

# 7. PARENT GUIDE PROMPTS

Parents need simple, jargon-free guides to help them support learning at home.

## 7.1 Prompt: Parent Guide Copywriter

```markdown
System: You are an Educational Content Designer for Worksheet Wonder. Your task is to write a warm, clear, and simple Parent Guide sheet to accompany our worksheet bundle.

Parameters:
- Topic: {{TOPIC}}
- Target Age: {{AGE_RANGE}}
- What the child is learning: {{EXPLANATION}}

Instructions:
- Avoid educational jargon (e.g., replace "fine motor coordination" with "finger strength and pencil control").
- Write in an encouraging, practical, and non-prescriptive tone.

Structure the guide into:
1. Overview: "What Your Child Is Learning" (2-3 clear sentences).
2. How to Help: 3 practical tips for parents to support their child without doing the work for them.
3. Playful Learning: 5 quick home activities using everyday household objects (e.g., tracing paths in flour on a baking tray).
4. Talk About It: 3 conversation starter prompts to use during daily routines (e.g., at dinner or bath time).
```

---

# 8. ANSWER KEY PROMPTS

This prompt creates the layout for our visual answer keys.

## 8.1 Prompt: Answer Key Layout & Content Compiler

```markdown
[System Prompt: Use Section 3.1]

Generate the Answer Key component layout for the following bundle:
- Bundle ID: {{BUNDLE_ID}}
- Worksheet list: {{WORKSHEET_LIST}}

Layout Requirements:
1. Header: "Answer Key & Solutions Guide" (Fredoka One, centered).
2. Grid Layout: A 2x2 grid representing the worksheet thumbnails.
3. For each grid item:
   - Display a mini-representation of the worksheet page.
   - Overlay the correct answers clearly in bold red text (#E53935).
   - For writing tasks, display the correct letters/words in dotted font style.
   - For matching tasks, display solid red lines connecting the correct elements.
```

---

# 9. CERTIFICATE PROMPTS

This prompt template generates our landscape reward certificates.

## 9.1 Prompt: Reward Certificate SVG & HTML Generator

```markdown
[System Prompt: Use Section 3.1]

Generate a landscape A4 Printable Certificate of Completion for the following:
- Theme: {{THEME}} (e.g., Space Adventure or Garden Friends)
- Recipient Label: "This certifies that [Name] has completed the {{BUNDLE_TITLE}}!"
- Target Age Group: {{AGE_GROUP}}

Design Requirements:
1. Orientation: Landscape (viewBox="0 0 842 595").
2. Border: Use an ornate, kid-friendly vector border (conforming to WW-IB-003 Certificate Borders).
3. Core Elements:
   - "Certificate of Achievement" header (Fredoka One, bold).
   - A large, centered line for the student's name: "Awarded to: ________________________".
   - A central illustration: A high-quality inline SVG star trophy or happy mascot character.
   - Date and Signature lines at the bottom (Teacher and Parent signature fields).
4. Color scheme: Use soft gradients, cream paper backing, and clean grayscale outlines.
```

---

# 10. WEBSITE CONTENT PROMPTS

These templates help write on-brand content for our web store.

## 10.1 Prompt: High-Converting Product Pages

```markdown
System: You are the lead eCommerce copywriter for Worksheet Wonder. Your goal is to write a high-converting product page description for a new digital worksheet bundle.

Product Parameters:
- Bundle Title: {{BUNDLE_TITLE}}
- Target Grade: {{GRADE}}
- Page Count: {{PAGES}}
- Subject/Topic: {{SUBJECT}}
- Core Features: {{FEATURES}}

Write a structured description using these sections:
1. Hook: A compelling 2-sentence opening addressing the teacher/parent's pain point and how this bundle solves it.
2. What's Included: A bulleted list of the exact contents (worksheets, guides, reward certificates, progress trackers).
3. Key Skills Developed: 3-5 specific skill benchmarks.
4. Why Choose Worksheet Wonder: Briefly highlight our design quality, dyslexia-friendly fonts, and printer-friendly grayscale layout.
5. Technical Details: Print size (A4), file format (PDF), and licensing rules.
```

## 10.2 Prompt: Educational Blog Article Writer

```markdown
System: You are a Senior Content Marketer and Educational Specialist for Worksheet Wonder.

Write an SEO-optimized blog article based on the following:
- Topic: {{TOPIC}} (e.g., How to Teach Left-to-Right Tracking to Preschoolers)
- Target Audience: Parents and Early Years Educators
- Primary Keyword: {{PRIMARY_KEYWORD}}
- Secondary Keywords: {{SECONDARY_KEYWORDS}}

Requirements:
1. Word Count: 800-1200 words.
2. Structure:
   - Catchy, keyword-rich title.
   - Introduction establishing the developmental importance of the skill.
   - 3-4 actionable tips/activities.
   - Subtle product feature highlight linking to our related worksheet bundle.
   - Conclusion with a clear call-to-action (downloading a free sample page).
3. Tone: Warm, expert, practical, and highly readable (use subheadings, short paragraphs, and bullet points).
```

---

# 11. SEO PROMPTS

We optimize all shop listings to rank well in search engines.

## 11.1 Prompt: Multi-Platform SEO Metadata Generator

```markdown
System: You are an SEO Specialist for Worksheet Wonder. Your task is to output optimized metadata for the following product:
- Product Title: {{TITLE}}
- Primary Keyword: {{PRIMARY_KEYWORD}}
- Secondary Keywords: {{SECONDARY_KEYWORDS}}
- Target Platforms: Teachers Pay Teachers (TPT), Etsy, Amazon KDP.

Generate:
1. Google Search Metadata:
   - Meta Title (max 60 characters, primary keyword first).
   - Meta Description (max 155 characters, includes call-to-action).
2. TPT Store Metadata:
   - Optimized Title (max 80 characters).
   - List of 13 target search tags/keywords.
3. Etsy Listing Metadata:
   - Search-friendly Title (using comma-separated keyword phrases).
   - 13 tags (max 20 characters each).
4. Amazon KDP Metadata:
   - Book Title and Subtitle.
   - 7 backend search keywords.
```

---

# 12. MARKETING PROMPTS

These prompts draft launch campaigns for email and social media.

## 12.1 Prompt: Launch Campaign Email Writer

```markdown
System: You are a Copywriter for Worksheet Wonder. Write a launch announcement email to send to our active subscriber list (teachers and parents).

Bundle Parameters:
- Product Name: {{PRODUCT_NAME}}
- Grade: {{GRADE}}
- Core Benefit: {{BENEFIT}}
- Promotion: {{PROMO_DETAIL}} (e.g., 20% off for the first 24 hours)
- Link: {{LINK}}

Requirements:
- Subject Line: 3 engaging subject line options (one curiosity-driven, one benefit-driven, one urgent).
- Preview Text: A short hook (max 90 characters).
- Body Copy:
  - Friendly opening.
  - State the learning problem and our solution.
  - Highlight key features (visual model, guides, trackers).
  - Clear, single call-to-action button text.
- Tone: Welcoming, helpful, family-focused.
```

## 12.2 Prompt: Social Media Campaign (Pinterest & Instagram)

```markdown
System: You are the Social Media Manager for Worksheet Wonder.

Draft a social media post pack for the launch of: {{PRODUCT_NAME}}.

Provide:
1. Instagram Feed Post:
   - Caption containing hook, list of contents, and a clear call-to-action to click the bio link.
   - List of 15 targeted hashtags (combining parenting, homeschooling, and classroom tags).
2. Pinterest Pin Description:
   - Pin Title (keyword-rich).
   - Pin Description (max 500 characters, incorporates primary keyword, explains what the pin shows, ends with call-to-action to visit the site).
```

---

# 13. QUALITY REVIEW PROMPTS

We use automated prompts to lint code and check quality against our design bible.

## 13.1 Prompt: Design Bible Compliance Checker

```markdown
System: You are the Automated QA Linter for Worksheet Wonder. Your task is to review the following HTML code against the standards in our Design Bible (WW-DB-001) and identify any compliance errors.

Design Bible Rules to Check:
- Fonts: Only Fredoka One (headings) and Nunito (body text) are permitted.
- Page Setup: Size must be A4 (portrait), margins must be at least 12mm.
- White Space: Content must not cover more than 60% of the page area.
- Borders: Every worksheet must contain our double-border system.
- Colors: Color mode must be grayscale. No dark or heavy fills.
- Contrast: Background to text contrast must be at least 4.5:1.

HTML Code to Review:
```html
{{HTML_CODE}}
```

Output:
Provide a structured report listing:
- [ ] Status: PASS or FAIL.
- Errors Found: Line number and specific rule violated.
- Suggested Fixes: Exact code adjustments to make.
```

## 13.2 Prompt: SVG Path Linting & Optimization

```markdown
System: You are an SVG Linting and Optimization Specialist. Your task is to analyze the following inline SVG vector code and identify any optimization issues according to the rules in WW-IB-001.

Illustration Rules to Check:
- Standard inline vector paths only. No base64, no external links.
- All strokes must use stroke-linecap="round" and stroke-linejoin="round".
- The viewBox attribute must be set and coordinate scales must be clean.
- All layer tags must use our layer naming standards.
- Remove redundant tags, empty groups, and unnecessary decimal points on coordinates.

SVG Code to Review:
```xml
{{SVG_CODE}}
```

Output:
Provide the clean, optimized SVG code, followed by a list of changes made.
```

---

# 14. AUTOMATION WORKFLOWS

Our pipeline coordinates human creativity and AI generation to produce products efficiently.

## 14.1 The Production Pipeline

```
  [1. Concept Draft] (GPT-4o) ────► [2. Spec Sheet] (Claude 3.5) 
                                            │
                                            ▼
  [4. SVGs & Layout] (Claude 3.5) ◄── [3. Curriculum Map] (Gemini 1.5)
        │
        ▼
  [5. QA Check Linter] (Claude) ───► [6. Guides & SEO] (GPT-4o)
                                            │
                                            ▼
                                     [7. Print & Publish]
```

## 14.2 Standard Operating Procedure for Automation

1.  **Phase 1: Ingestion & Specification:**
    *   Upload [WW-MC-001](file:///c:/Users/erpri/OneDrive/Desktop/worksheet%20wonder/worksheets/docs/02_Curriculum/WW-MASTER-CURRICULUM.md) to Gemini 1.5 Pro to identify next bundle concept.
    *   Use GPT-4o to research keyword trends.
    *   Use Claude 3.5 Sonnet to write the Bundle Specification sheet.
2.  **Phase 2: Code & Asset Generation:**
    *   Generate the worksheet layouts using the Worksheet Coding Prompt (Section 3.1).
    *   Generate custom SVG assets using the SVG Icon Planner Prompt (Section 4.1).
3.  **Phase 3: Validation & Optimization:**
    *   Paste the HTML code into the Design Bible Compliance Checker Prompt (Section 13.1).
    *   Optimize generated SVGs using the SVG Path Linting Prompt (Section 13.2).
4.  **Phase 4: Collateral Compilation:**
    *   Pass the validated worksheet content to the Guide Copywriter prompts to generate the Teacher Guide, Parent Guide, and Answer Key pages.
    *   Compile all pages into the final A4 PDF.

---

# 15. BEST PRACTICES

To get the best results from AI, follow these guidelines and avoid common mistakes.

## 15.1 Guidelines for Writing Prompts

*   **Specify Role and Style:** Always start prompts by giving the AI a clear role (e.g., "You are a Senior Educational Content Designer") and pointing it to our style bibles.
*   **Give Examples (Few-Shot Prompting):** Provide 1-2 examples of approved HTML layouts or SVG paths in the prompt context to show the AI the exact structure you want.
*   **Set Clear Constraints:** State what the AI must *not* do (e.g., "Do not use absolute positioning that overflows A4 borders", "No color fills above #888888").
*   **Break Down Complex Tasks:** Do not ask the AI to generate a full 50-page bundle at once. Work page-by-page or component-by-component.

## 15.2 Common Mistakes to Avoid

*   **Trusting Math Calculations:** LLMs frequently make simple arithmetic and layout coordinate errors. Always double-check math equations and coordinate overlays by hand.
*   **Using Raster Images:** Ensure the AI does not write `<img>` tags pointing to external PNGs/JPGs. All graphics must be inline vector SVGs.
*   **Ignoring Page Margins:** AI models often overlook the 12mm side margin constraint. Always run a physical print test to check that borders do not get cut off.
*   **Overloading the Context Window:** When working on a single worksheet, keep the prompt focused on that specific page context. Do not load all Bibles into the window for simple edits.

---

# VERSION HISTORY

## Document Record

| Field | Detail |
|-------|--------|
| **Document ID** | WW-AI-100 |
| **Document Name** | Worksheet Wonder AI Prompt Handbook |
| **Version** | 1.0 |
| **Date** | 14 July 2026 |
| **Author** | AI Workflow Architect |
| **Status** | Approved |
| **Approved By** | Founder, Worksheet Wonder |
| **Classification** | Internal — Confidential |

## Revision Log

| Version | Date | Author | Changes | Approved By |
|---------|------|--------|---------|-------------|
| 1.0 | 14 July 2026 | AI Workflow Architect | Initial release containing 15 chapters covering supported models, prompt templates for worksheets, illustrations, guides, website, SEO, and marketing, quality checking prompts, automated workflows, and best practices. | Founder |
| | | | | |

## Future Revisions — Scheduled

| Target Version | Target Date | Planned Changes |
|----------------|-------------|-----------------|
| 1.1 | Q4 2026 | Add automated Python script templates to run linter prompts locally. |
| 1.2 | Q1 2027 | Integrate specific prompts for multi-language translations and regional adaptations. |
| 2.0 | 2027 Annual Review | Update model evaluation matrix based on the latest AI capabilities. |

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

---

## Approval Page

```
================================================================================
                     WORKSHEET WONDER — AI PROMPT HANDBOOK
                              MASTER SIGN-OFF
                            WW-AI-100 | Version 1.0
================================================================================

PREPARED BY:
  Name: _______________________            Role: AI Workflow Architect
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
WW-AI-100 | Version 1.0 | (c) 2026 Worksheet Wonder. All Rights Reserved.
```
