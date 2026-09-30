# Worksheet Wonder: Project Roadmap

To transition this repository from a "Collection of Frameworks" into a "Fully Automated Enterprise Publishing Engine", the following sequence must be executed:

## Phase 1: Architectural Remediation (Immediate)
1. **Generate `05_JSON_Schemas`**: We must immediately execute the generation of `worksheet.schema.json`, `alphabet.schema.json`, etc. Without these, the publishing engine has no type-safety.
2. **Refactor HTML for Dynamic Arrays**: Update `vocabulary.html` to use Handlebars `{{#each}}` blocks rather than hardcoded `{{WORD1}}`, `{{WORD2}}` to allow flexible content lengths.

## Phase 2: Engine Development (Backend)
1. **Create `08_Compiler_Engine`**: Build a Node.js script utilizing `Handlebars.js` that pulls `A.json`, reads `master_template.html`, injects the components, and outputs a compiled `A_rendered.html`.
2. **Create `09_PDF_Generator`**: Build a Puppeteer script that automatically opens the compiled HTML and exports a print-perfect A4 PDF, executing across the entire 26-letter database in seconds.

## Phase 3: Asset Population (Creative)
1. **SVG Production**: Commission and add vector artwork to `03_Illustration_Library`, ensuring every SVG includes a corresponding JSON metadata file tracking its curriculum tags.
2. **Expand Content Database**: Populate `Numbers`, `Shapes`, and `SightWords` folders in `04_Content_Database` with rich JSON payloads.

## Phase 4: CI/CD & Cloud Deployment
1. Set up GitHub Actions to automatically run the Compiler and PDF Engine whenever new JSON content is merged to the `main` branch.
2. Store output PDFs in AWS S3 or a similar cloud bucket for distribution to the Worksheet Wonder web portal.
